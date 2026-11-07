"""Idempotent removal of registered restore targets only."""
from . import common as c
from .restore import TERMINAL


def handler(event, context):
    record = c.get(event["job"])
    target = c.owned(record)
    if not record.get("start_intent") and not record.get("target_create_intent"):
        record["cleanup_status"] = "NOT_REQUIRED"
        c.put(record)
        return {"done": True}
    if record.get("start_intent") and not record.get("restore_job_id"):
        # Do not delete a target when StartRestoreJob may still be creating it.
        raise RuntimeError("RestoreJobIdentityNeedsReconciliation")
    if record.get("restore_job_id"):
        job = c.client("backup").describe_restore_job(RestoreJobId=record["restore_job_id"])
        if job["Status"] not in TERMINAL:
            return {"done": False}
        metadata = c.client("backup").get_restore_job_metadata(RestoreJobId=record["restore_job_id"])["Metadata"]
        field = "targettablename" if record["kind"] == "dynamodb" else "destinationbucketname"
        if job.get("RecoveryPointArn") != record["recovery_point"] or {k.lower(): v for k, v in metadata.items()}.get(field) != target:
            raise ValueError("RestoreJobOwnershipMismatch")
    try:
        if record["kind"] == "dynamodb":
            table = c.client("dynamodb").describe_table(TableName=target)["Table"]
            if job["Status"] != "COMPLETED" and job.get("CreatedResourceArn") != table.get("TableArn"):
                raise ValueError("FailedRestoreTargetOwnershipUnproven")
            if table["TableStatus"] == "ACTIVE":
                c.client("dynamodb").delete_table(TableName=target)
            done = False
        else:
            c.verify_s3_target(record)
            s3 = c.client("s3")
            versions = []
            for page in s3.get_paginator("list_object_versions").paginate(Bucket=target, **c.s3_owner()):
                versions.extend(page.get("Versions", []) + page.get("DeleteMarkers", []))
                if len(versions) > 1000:
                    raise ValueError("SyntheticCleanupLimitExceeded")
            for item in versions:
                s3.delete_object(Bucket=target, Key=item["Key"], VersionId=item["VersionId"], **c.s3_owner())
            s3.delete_bucket(Bucket=target, **c.s3_owner())
            record["bucket_deletion_requested"] = True
            c.put(record)
            s3.head_bucket(Bucket=target, **c.s3_owner())
            done = False
    except Exception as exc:
        if not c.missing(exc) or (record["kind"] == "s3" and not record.get("bucket_deletion_requested") and not record.get("restore_job_id")):
            record["cleanup_status"] = "FAILED"
            c.put(record)
            raise
        done = True
    record["cleanup_status"] = "DELETED" if done else "PENDING"
    if done:
        record["cleaned_at"] = c.iso()
    c.put(record)
    return {"done": done}
