"""One-time, repeatable seeding of stack-owned synthetic sources."""
from . import common as c

MARKER_PK = "__bcdr_timestamp__"
MARKER_KEY = "__bcdr_timestamp__.json"


def marker(timestamp):
    return {"pk": {"S": MARKER_PK}, "write_started_at": {"S": timestamp}}


def fixture():
    rows = [{"pk": {"S": "synthetic-%03d" % n}, "value": {"S": "recovery-fixture-%03d" % n}}
            for n in range(10)]
    objects = {"synthetic/sample-%02d.txt" % n: ("recovery sample %02d\n" % n).encode() for n in range(3)}
    return rows, objects


def seed(event):
    control = {"resource_id": "#fixture", "test_date": "v1"}
    try:
        existing = c.get(control)
        refresh_id = event.get("refresh_id") or c.now().date().isoformat()
        if existing.get("ready_at") and (not event.get("refresh") or existing.get("refresh_id") == refresh_id):
            return {"status": "ALREADY_READY", "ready_at": existing["ready_at"]}
    except ValueError:
        existing = None
    if existing and not existing.get("ready_at"):
        raise RuntimeError("FixtureInitializationIncomplete")
    if any(r.get("execution_arn") and not r.get("finalized") for r in c.records()):
        raise RuntimeError("FixtureRefreshBlockedByUnfinishedTest")
    if existing:
        from .validate import table_summary, bucket_summary
        previous = c.read_json(c.env("REPORT_BUCKET"), existing["manifest_key"], existing["manifest_version"])
        if c.digest(previous) != existing["manifest_sha256"] or table_summary(c.env("SOURCE_TABLE"))[0] != previous["dynamodb"] or bucket_summary(c.env("SOURCE_BUCKET"))[0] != previous["s3"]:
            raise ValueError("SyntheticSourceDriftRequiresInvestigation")
    else:
        if c.client("dynamodb").scan(TableName=c.env("SOURCE_TABLE"), Limit=1, ConsistentRead=True).get("Items"):
            raise ValueError("SyntheticSourceMustBeEmptyBeforeFirstSeed")
        if c.client("s3").list_objects_v2(Bucket=c.env("SOURCE_BUCKET"), MaxKeys=1, **c.s3_owner()).get("Contents"):
            raise ValueError("SyntheticBucketMustBeEmptyBeforeFirstSeed")
    c.put({**control, "status": "SEEDING"}, create=not existing)
    rows, objects = fixture()
    for row in rows:
        c.client("dynamodb").put_item(TableName=c.env("SOURCE_TABLE"), Item=row)
    write_started = c.iso()
    rows.append(marker(write_started))
    c.client("dynamodb").put_item(TableName=c.env("SOURCE_TABLE"), Item=rows[-1])
    write_acknowledged = c.iso()
    for name, body in objects.items():
        c.client("s3").put_object(Bucket=c.env("SOURCE_BUCKET"), Key=name, Body=body,
            ServerSideEncryption="aws:kms", SSEKMSKeyId=c.env("KEY_ARN"), **c.s3_owner())
    s3_started = c.iso()
    objects[MARKER_KEY] = c.compact({"write_started_at": s3_started}).encode()
    c.client("s3").put_object(Bucket=c.env("SOURCE_BUCKET"), Key=MARKER_KEY, Body=objects[MARKER_KEY],
        ContentType="application/json", ServerSideEncryption="aws:kms", SSEKMSKeyId=c.env("KEY_ARN"), **c.s3_owner())
    s3_acknowledged = c.iso()
    facts = [{"key": name, "size": len(body), "sha256": c.digest(body)} for name, body in sorted(objects.items())]
    manifest = {"schema_version": 3, "dataset": "synthetic-v1", "ready_at": c.iso(),
                "data_marker": {"write_started_at": write_started, "write_acknowledged_at": write_acknowledged},
                "s3_data_marker": {"write_started_at": s3_started, "write_acknowledged_at": s3_acknowledged},
                "dynamodb": {"count": len(rows), "sha256": c.digest(sorted(rows, key=c.compact))},
                "s3": {"count": len(facts), "sha256": c.digest(facts)}}
    path = "baselines/synthetic-v1.json"
    version = c.write_json(c.env("REPORT_BUCKET"), path, manifest).get("VersionId")
    if not isinstance(version, str) or not version or version == "null":
        raise RuntimeError("VersionedManifestRequired")
    c.put({**control, "manifest_key": path, "manifest_version": version,
           "manifest_sha256": c.digest(manifest), "ready_at": manifest["ready_at"],
           "refresh_id": event.get("refresh_id") or c.now().date().isoformat()})
    return {"status": "READY", "ready_at": manifest["ready_at"], "manifest_key": path}


def handler(event, context):
    with c.fixture_lease():
        return seed(event)
