"""Restore orchestration. This role cannot write the protected source data."""
from . import common as c
from datetime import timedelta

TERMINAL = {"COMPLETED", "FAILED", "ABORTED"}


def select_point(points, source_arn, ready_at):
    candidates = [p for p in points if p.get("Status") == "COMPLETED"
                  and p.get("ResourceArn") == source_arn and c.dt(p["CreationDate"]) >= c.dt(ready_at)]
    if not candidates:
        raise ValueError("NoCompletedBackupAfterBaseline")
    return max(candidates, key=lambda p: c.dt(p["CreationDate"]))


def plan(event):
    with c.fixture_lease():
        return register_plan(event)


def register_plan(event):
    request = event.get("request", {})
    kinds = request.get("resource_types", list(c.kinds()))
    if not isinstance(kinds, list) or not kinds or len(kinds) != len(set(kinds)) or any(k not in c.kinds() for k in kinds):
        raise ValueError("InvalidResourceSelection")
    force = request.get("force_validation_failure", False)
    if type(force) is not bool or (force and c.env("ALLOW_FAULTS") != "true"):
        raise ValueError("FaultInjectionDisabled")
    start = c.iso(c.dt(event["start_time"]))
    jobs = []
    for kind in kinds:
        run_id, target = c.identity(event["execution_arn"], kind)
        record = {"resource_id": kind, "test_date": start + "#" + run_id, "kind": kind,
                  "run_id": run_id, "target": target, "source_arn": c.source(kind),
                  "execution_arn": event["execution_arn"], "started_at": start,
                  "result": "RUNNING", "cleanup_status": "NOT_REQUIRED", "finalized": False,
                  "rto_target": int(c.env(kind.upper() + "_RTO")), "rpo_target": int(c.env(kind.upper() + "_RPO")),
                  "target_approval_reference": c.env("TARGET_APPROVAL"), "force_validation_failure": force,
                  "review_due_at": c.iso(c.dt(start) + timedelta(days=7)),
                  "signoff": {"status": "PENDING", "signed_off_by": None}}
        record.update({"scope": "SYNTHETIC_COMPONENT_ONLY", "service_recovery": "NOT_TESTED",
                       "website_recovery": "NOT_TESTED", "disruption_at": start})
        try:
            c.put(record, create=True)
        except Exception as exc:
            if c.error_code(exc) != "ConditionalCheckFailedException":
                raise
        jobs.append({k: record[k] for k in ("resource_id", "test_date")})
    return {"jobs": jobs}


def prepare(record):
    if record.get("recovery_point"):
        return {"ready": True}
    baseline = c.get({"resource_id": "#fixture", "test_date": "v1"})
    if not baseline.get("ready_at"):
        raise ValueError("SyntheticFixtureNotReady")
    manifest = c.read_json(c.env("REPORT_BUCKET"), baseline["manifest_key"], baseline["manifest_version"])
    if c.digest(manifest) != baseline["manifest_sha256"]:
        raise ValueError("BaselineIntegrityMismatch")
    points = []
    for page in c.client("backup").get_paginator("list_recovery_points_by_backup_vault").paginate(
            BackupVaultName=c.env("VAULT"), ByResourceArn=record["source_arn"], ByCreatedAfter=c.dt(baseline["ready_at"])):
        points.extend(page.get("RecoveryPoints", []))
    point = select_point(points, record["source_arn"], baseline["ready_at"])
    age = int((c.dt(record["started_at"]) - c.dt(point["CreationDate"])).total_seconds())
    if age < 0:
        raise ValueError("BackupNewerThanTestStart")
    record.update({"recovery_point": point["RecoveryPointArn"], "recovery_point_created_at": c.iso(c.dt(point["CreationDate"])),
                   "recovery_point_age_seconds": age, "rpo_achieved": None,
                   "rpo_measure": "NOT_YET_VALIDATED", "baseline": manifest,
                   "manifest_version": baseline["manifest_version"],
                   "baseline_sha256": baseline["manifest_sha256"]})
    c.put(record)
    return {"ready": True}


def start(record):
    target = c.owned(record)
    if record.get("restore_job_id"):
        return {"started": True}
    if record.get("start_intent"):
        matches = []
        for page in c.client("backup").get_paginator("list_restore_jobs").paginate(ByCreatedAfter=c.dt(record["started_at"]), ByResourceType="DynamoDB" if record["kind"] == "dynamodb" else "S3"):
            for job in page.get("RestoreJobs", []):
                if job.get("RecoveryPointArn") != record["recovery_point"]:
                    continue
                metadata = c.client("backup").get_restore_job_metadata(RestoreJobId=job["RestoreJobId"])["Metadata"]
                destination_key = "targettablename" if record["kind"] == "dynamodb" else "destinationbucketname"
                if {k.lower(): v for k, v in metadata.items()}.get(destination_key) == target:
                    matches.append(job["RestoreJobId"])
        if len(matches) != 1:
            raise RuntimeError("RestoreStartUnconfirmedDoNotReplay")
        record["restore_job_id"] = matches[0]
        c.put(record)
        return {"started": True}
    # Persist intent BEFORE creating anything. An aborted execution is reconciled
    # by discovering the exact existing job, then waiting for it to finish.
    if record["kind"] == "s3":
        prepare_s3_target(record)
    record.update({"start_intent": True, "cleanup_status": "PENDING"})
    c.put(record)
    metadata = ({"targetTableName": target, "encryptionType": "KMS", "kmsMasterKeyArn": c.env("KEY_ARN")} if record["kind"] == "dynamodb"
                else {"DestinationBucketName": target, "EncryptionType": "SSE-KMS", "KMSKey": c.env("KEY_ARN"), "RestoreACLs": "false", "RestoreLatestVersionsUpTo": "1"})
    resource_type = "DynamoDB" if record["kind"] == "dynamodb" else "S3"
    response = c.client("backup").start_restore_job(RecoveryPointArn=record["recovery_point"], Metadata=metadata,
                 IamRoleArn=c.env("RESTORE_ROLE_ARN"), IdempotencyToken=record["run_id"], ResourceType=resource_type)
    record["restore_job_id"] = response["RestoreJobId"]
    c.put(record)
    return {"started": True}


def prepare_s3_target(record):
    """Create and harden a unique operational target before starting its writer."""
    target = c.owned(record)
    s3 = c.client("s3")
    if record.get("target_create_intent"):
        c.verify_s3_target(record)
    else:
        try:
            s3.head_bucket(Bucket=target, **c.s3_owner())
        except Exception as exc:
            if not c.missing(exc):
                raise
        else:
            raise ValueError("S3RestoreDestinationAlreadyExists")
        record.update({"target_create_intent": True, "cleanup_status": "PENDING"})
        c.put(record)
        s3.create_bucket(Bucket=target, ObjectOwnership="BucketOwnerEnforced")
        s3.put_bucket_tagging(Bucket=target, Tagging={"TagSet": [{"Key": "grc-project", "Value": "13"},
            {"Key": "bcdr-run-id", "Value": record["run_id"]}]}, **c.s3_owner())
    s3.put_public_access_block(Bucket=target, PublicAccessBlockConfiguration={k: True for k in
        ["BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]}, **c.s3_owner())
    s3.put_bucket_encryption(Bucket=target, ServerSideEncryptionConfiguration={"Rules": [{
        "ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": c.env("KEY_ARN")}, "BucketKeyEnabled": True}]}, **c.s3_owner())
    s3.put_bucket_versioning(Bucket=target, VersioningConfiguration={"Status": "Enabled"}, **c.s3_owner())
    s3.put_bucket_policy(Bucket=target, Policy=c.tls_policy(target), **c.s3_owner())
    record["target_prepared"] = True
    c.put(record)


def poll(record):
    job = c.client("backup").describe_restore_job(RestoreJobId=record["restore_job_id"])
    record["restore_status"] = job["Status"]
    if job.get("CompletionDate"):
        record["restore_job_seconds"] = max(0, int((c.dt(job["CompletionDate"]) - c.dt(job["CreationDate"])).total_seconds()))
    c.put(record)
    if job["Status"] in TERMINAL:
        return {"state": "VALIDATE" if job["Status"] == "COMPLETED" else "FAIL"}
    if (c.now() - c.dt(record["started_at"])).total_seconds() > int(c.env("MAX_RESTORE_WAIT")):
        return {"state": "FAIL"}
    return {"state": "WAIT"}


def handler(event, context):
    action = event["action"]
    if action == "plan":
        return plan(event)
    if action == "summarize":
        if not all(result.get("passed") for result in event["results"]):
            raise RuntimeError("OneOrMoreRecoveryTestsFailed")
        return {"status": "PASS"}
    record = c.get(event["job"])
    if action == "prepare":
        return prepare(record)
    if action == "start":
        return start(record)
    if action == "poll":
        return poll(record)
    if action == "fail":
        record.update({"result": "FAIL", "failure_reason": event.get("reason", "WorkflowTaskFailed")})
        c.put(record)
        return {"recorded": True}
    raise ValueError("UnsupportedAction")
