"""Validate all of the deliberately small synthetic baseline, not only counts."""
from . import common as c
from .fixtures import MARKER_PK, MARKER_KEY
import json
import math

MAX_ROWS = 1000
MAX_OBJECTS = 100
MAX_OBJECT_BYTES = 1024 * 1024


def table_summary(table):
    rows = []
    for page in c.client("dynamodb").get_paginator("scan").paginate(TableName=table, ConsistentRead=True):
        rows.extend(page.get("Items", []))
        if len(rows) > MAX_ROWS:
            raise ValueError("SyntheticRowLimitExceeded")
    markers = [r for r in rows if r.get("pk", {}).get("S") == MARKER_PK]
    if len(markers) != 1:
        raise ValueError("RecoveredTimestampMarkerMissing")
    return {"count": len(rows), "sha256": c.digest(sorted(rows, key=c.compact))}, markers[0]


def bucket_summary(bucket):
    facts, marker = [], None
    for page in c.client("s3").get_paginator("list_objects_v2").paginate(Bucket=bucket, **c.s3_owner()):
        for obj in page.get("Contents", []):
            if len(facts) >= MAX_OBJECTS or obj["Size"] > MAX_OBJECT_BYTES:
                raise ValueError("SyntheticObjectLimitExceeded")
            response = c.client("s3").get_object(Bucket=bucket, Key=obj["Key"], **c.s3_owner())
            if response.get("ServerSideEncryption") != "aws:kms" or response.get("SSEKMSKeyId") != c.env("KEY_ARN"):
                raise ValueError("RestoredObjectEncryptionMismatch")
            body = response["Body"].read(MAX_OBJECT_BYTES + 1)
            response["Body"].close()
            if len(body) != obj["Size"] or len(body) > MAX_OBJECT_BYTES:
                raise ValueError("SyntheticObjectSizeMismatch")
            facts.append({"key": obj["Key"], "size": len(body), "sha256": c.digest(body)})
            if obj["Key"] == MARKER_KEY:
                marker = json.loads(body)
    if marker is None:
        raise ValueError("RecoveredTimestampMarkerMissing")
    return {"count": len(facts), "sha256": c.digest(sorted(facts, key=lambda x: x["key"]))}, marker


def handler(event, context):
    record = c.get(event["job"])
    target = c.owned(record)
    if record.get("restore_status") != "COMPLETED":
        raise ValueError("RestoreNotCompleted")
    if c.digest(record["baseline"]) != record["baseline_sha256"]:
        raise ValueError("BaselineIntegrityMismatch")
    if record["kind"] == "dynamodb":
        desc = c.client("dynamodb").describe_table(TableName=target)["Table"]
        encryption = desc.get("SSEDescription", {})
        if encryption.get("KMSMasterKeyArn") != c.env("KEY_ARN") or encryption.get("Status") != "ENABLED":
            raise ValueError("TableEncryptionMismatch")
        if desc.get("TableStatus") != "ACTIVE":
            raise ValueError("RestoredTableNotUsable")
        actual, recovered_marker = table_summary(target)
    elif record["kind"] == "s3":
        c.verify_s3_target(record)
        s3 = c.client("s3")
        if s3.get_bucket_versioning(Bucket=target, **c.s3_owner()).get("Status") != "Enabled":
            raise ValueError("RestoredBucketVersioningMismatch")
        block = s3.get_public_access_block(Bucket=target, **c.s3_owner()).get("PublicAccessBlockConfiguration", {})
        if any(block.get(k) is not True for k in ["BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]):
            raise ValueError("RestoredBucketPublicAccessMismatch")
        policy = s3.get_bucket_policy(Bucket=target, **c.s3_owner())["Policy"]
        if json.loads(policy) != json.loads(c.tls_policy(target)):
            raise ValueError("RestoredBucketPolicyMismatch")
        rules = s3.get_bucket_encryption(Bucket=target, **c.s3_owner())["ServerSideEncryptionConfiguration"]["Rules"]
        if len(rules) != 1 or rules[0].get("ApplyServerSideEncryptionByDefault") != {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": c.env("KEY_ARN")}:
            raise ValueError("RestoredBucketEncryptionMismatch")
        actual, recovered_marker = bucket_summary(target)
    else:
        raise ValueError("UnsupportedResourceType")
    expected = record["baseline"][record["kind"]]
    valid = actual == expected
    injected = record["force_validation_failure"]
    rpo_ok = False
    if valid:
        marker = record["baseline"]["data_marker" if record["kind"] == "dynamodb" else "s3_data_marker"]
        written = c.dt(recovered_marker["write_started_at"]["S"] if record["kind"] == "dynamodb" else recovered_marker["write_started_at"])
        acknowledged = c.dt(marker["write_acknowledged_at"])
        disruption = c.dt(record["disruption_at"])
        if written != c.dt(marker["write_started_at"]) or not written <= acknowledged <= disruption:
            raise ValueError("RecoveredTimestampMarkerInvalid")
        # The server commit occurred inside the recorded client write interval.
        # Use its oldest bound conservatively. This proves only the static lab
        # dataset's recoverable age; service/application RPO remains untested.
        upper = math.ceil((disruption - written).total_seconds())
        lower = max(0, math.floor((disruption - acknowledged).total_seconds()))
        record.update({"rpo_achieved": upper, "rpo_lower_bound_seconds": lower,
                       "rpo_measure": "RECOVERED_SYNTHETIC_MARKER_UPPER_BOUND",
                       "recoverable_data_timestamp": c.iso(written)})
        rpo_ok = upper <= record["rpo_target"]
    else:
        record.update({"rpo_achieved": None, "rpo_measure": "NOT_DEMONSTRATED"})
    # Capture completion after all integrity/configuration and marker checks.
    # The stored timestamp and elapsed RTO must describe the same instant.
    completed_at = c.now()
    elapsed = max(0, math.ceil((completed_at - c.dt(record["started_at"])).total_seconds()))
    rto_ok = elapsed <= record["rto_target"]
    record.update({"validation": {"passed": valid, "expected": expected, "actual": actual},
                   "rto_achieved": elapsed, "rto_measure": "TEST_START_THROUGH_VALIDATION",
                   "validated_at": c.iso(completed_at), "result": "PASS" if valid and rto_ok and rpo_ok and not injected else "FAIL",
                   "target_checks": {"component_rto_passed": rto_ok, "synthetic_rpo_bound_passed": rpo_ok}})
    if record["result"] == "FAIL":
        record["failure_reason"] = "ForcedValidationFailure" if injected else "ValidationOrRecoveryTargetFailed"
    c.put(record)
    return {"passed": record["result"] == "PASS"}
