"""Shared storage and identity rules. Never log payloads or restored data."""
import hashlib
import json
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import lru_cache
from uuid import uuid4


def env(name):
    return os.environ[name]


@lru_cache(maxsize=None)
def client(service):
    import boto3
    from botocore.config import Config
    return boto3.client(service, config=Config(retries={"mode": "standard", "max_attempts": 4}))


def now():
    return datetime.now(timezone.utc)


def iso(value=None):
    return (value or now()).astimezone(timezone.utc).isoformat()


def dt(value):
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else compact(value).encode()).hexdigest()


def error_code(exc):
    # AWS error messages can include identifiers and data. Persist only the code.
    return getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)


def missing(exc):
    return error_code(exc) in {"ResourceNotFoundException", "NoSuchBucket", "NoSuchKey", "404"}


def key(job):
    return {k: {"S": job[k]} for k in ("resource_id", "test_date")}


def get(job):
    item = client("dynamodb").get_item(TableName=env("RESULTS_TABLE"), Key=key(job), ConsistentRead=True).get("Item")
    if not item:
        raise ValueError("RunNotRegistered")
    return json.loads(item["document"]["S"])


def put(record, create=False):
    args = {"TableName": env("RESULTS_TABLE"), "Item": {
        **key(record), "document": {"S": compact(record)},
        "run_id": {"S": record.get("run_id", "control")},
        "result": {"S": record.get("result", "CONTROL")},
        "cleanup_status": {"S": record.get("cleanup_status", "NOT_REQUIRED")},
    }}
    if create:
        args["ConditionExpression"] = "attribute_not_exists(resource_id)"
    client("dynamodb").put_item(**args)
    return record


def publication(event_id, prepare):
    """Persist one immutable envelope before delivery; concurrent losers reuse it."""
    job = {"resource_id": "#event-" + digest(event_id.encode()), "test_date": "v1"}
    try:
        record = get(job)
    except ValueError as exc:
        if str(exc) != "RunNotRegistered":
            raise
        record = None
    if record is None:
        candidate = {**job, "event_id": event_id, "publication": prepare()}
        try:
            put(candidate, create=True)
            record = candidate
        except Exception as exc:
            if error_code(exc) != "ConditionalCheckFailedException":
                raise
            record = get(job)
    if record.get("event_id") != event_id:
        raise ValueError("PublicationIdentityMismatch")
    return record["publication"]


def records():
    for page in client("dynamodb").get_paginator("scan").paginate(TableName=env("RESULTS_TABLE"), ConsistentRead=True):
        for item in page.get("Items", []):
            if "document" in item:
                yield json.loads(item["document"]["S"])


def source(kind):
    if kind == "dynamodb":
        return env("SOURCE_TABLE_ARN")
    if kind == "s3":
        return "arn:" + env("PARTITION") + ":s3:::" + env("SOURCE_BUCKET")
    raise ValueError("UnsupportedResourceType")


def kinds():
    return ("dynamodb", "s3")


@contextmanager
def fixture_lease():
    """Serialize fixture writes against registration of new DR executions."""
    token = uuid4().hex
    lease_key = key({"resource_id": "#fixture-lock", "test_date": "v1"})
    client("dynamodb").put_item(TableName=env("RESULTS_TABLE"), Item={**lease_key,
        "lease_token": {"S": token}, "expires_at": {"N": str(int(now().timestamp()) + 300)}},
        ConditionExpression="attribute_not_exists(resource_id) OR expires_at < :now",
        ExpressionAttributeValues={":now": {"N": str(int(now().timestamp()))}})
    try:
        yield
    finally:
        client("dynamodb").delete_item(TableName=env("RESULTS_TABLE"), Key=lease_key,
            ConditionExpression="lease_token = :token", ExpressionAttributeValues={":token": {"S": token}})


def identity(execution_arn, kind):
    expected = "arn:{0}:states:{1}:{2}:execution:{3}-dr:".format(
        env("PARTITION"), env("AWS_REGION"), env("ACCOUNT_ID"), env("PREFIX"))
    if not execution_arn.startswith(expected) or kind not in kinds():
        raise ValueError("InvalidExecutionIdentity")
    run_id = digest((execution_arn + ":" + kind).encode())[:24]
    return run_id, env("PREFIX") + "-restore-" + kind + "-" + run_id


def owned(record):
    run_id, target = identity(record["execution_arn"], record["kind"])
    if record["run_id"] != run_id or record["target"] != target or record["source_arn"] != source(record["kind"]):
        raise ValueError("UnownedRestoreTarget")
    if target in {env("SOURCE_BUCKET"), env("SOURCE_TABLE"), env("REPORT_BUCKET"), env("RESULTS_TABLE"), os.environ.get("IR_BUCKET")}:
        raise ValueError("ProtectedSource")
    return target


def s3_owner():
    return {"ExpectedBucketOwner": env("ACCOUNT_ID")}


def verify_s3_target(record):
    target = owned(record)
    actual = client("s3").get_bucket_tagging(Bucket=target, **s3_owner()).get("TagSet", [])
    tags = {t["Key"]: t["Value"] for t in actual}
    if tags.get("grc-project") != "13" or tags.get("bcdr-run-id") != record["run_id"]:
        raise ValueError("S3TargetOwnershipMismatch")
    return target


def write_json(bucket, path, data):
    return client("s3").put_object(Bucket=bucket, Key=path, Body=compact(data).encode(),
                            ContentType="application/json", ServerSideEncryption="aws:kms", SSEKMSKeyId=env("KEY_ARN"))


def read_json(bucket, path, version):
    if not isinstance(version, str) or not version or version == "null":
        raise ValueError("VersionedManifestRequired")
    return json.loads(client("s3").get_object(Bucket=bucket, Key=path, VersionId=version)["Body"].read())


def metric(name, value):
    # Native heartbeat/queue alarms monitor invocations and dead letters. Publish
    # problem counters only while nonzero; missing alarm inputs are non-breaching.
    if value == 0:
        return
    client("cloudwatch").put_metric_data(Namespace="GRC/BCDR", MetricData=[{
        "MetricName": name, "Value": value, "Unit": "Count",
        "Dimensions": [{"Name": "Project", "Value": env("PREFIX")}]}])


def tls_policy(bucket, quarantine=False):
    arn = "arn:" + env("PARTITION") + ":s3:::" + bucket
    statements = [{"Sid": "DenyInsecureTransport", "Effect": "Deny", "Principal": "*",
                   "Action": "s3:*", "Resource": [arn, arn + "/*"],
                   "Condition": {"Bool": {"aws:SecureTransport": "false"}}}]
    if quarantine:
        statements.append({"Sid": "IncidentQuarantineWrites", "Effect": "Deny", "Principal": "*",
                           "Action": ["s3:PutObject", "s3:DeleteObject", "s3:DeleteObjectVersion"], "Resource": arn + "/*"})
    return compact({"Version": "2012-10-17", "Statement": statements})
