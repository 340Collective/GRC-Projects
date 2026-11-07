"""Out-of-band reconciliation plus quarterly deadline detection."""
import json
from datetime import datetime, timedelta, timezone
from . import common as c


def invoke(function, payload):
    response = c.client("lambda").invoke(FunctionName=c.env(function), InvocationType="RequestResponse", Payload=c.compact(payload).encode())
    data = json.loads(response["Payload"].read())
    if response.get("FunctionError"):
        raise RuntimeError("ReconciliationInvocationFailed")
    return data


def quarter_due(time):
    month = ((time.month - 1) // 3) * 3 + 1
    return datetime(time.year, month, 1, 9, tzinfo=timezone.utc)


def handler(event, context):
    all_records = list(c.records())
    pending = errors = overdue = 0
    current = c.now()
    for record in all_records:
        if record.get("finalized") or "execution_arn" not in record:
            continue
        # Never race a live execution. Timeout and stop events are recovered on
        # the next monitor tick. EventBridge service events are only an aid.
        try:
            status = c.client("stepfunctions").describe_execution(executionArn=record["execution_arn"])["status"]
            if status == "RUNNING":
                if (current - c.dt(record["started_at"])).total_seconds() > int(c.env("MAX_RESTORE_WAIT")):
                    pending += 1
                continue
            job = {k: record[k] for k in ("resource_id", "test_date")}
            if record.get("start_intent") and not record.get("restore_job_id"):
                invoke("RESTORE_FUNCTION", {"action": "start", "job": job})
            if record.get("result") == "RUNNING":
                invoke("RESTORE_FUNCTION", {"action": "fail", "job": job, "reason": "Execution" + status})
            done = invoke("CLEANUP_FUNCTION", {"job": job})["done"]
            pending += int(not done)
            invoke("REPORT_FUNCTION", {"job": job})
        except Exception as exc:
            # Keep reconciling other runs. No exception payloads or data are logged.
            errors += 1
            print(c.compact({"component": "monitor", "error_code": c.error_code(exc)}))
    if c.env("SCHEDULE_STATE") == "ENABLED":
        due = quarter_due(current)
        deadline = due + timedelta(hours=int(c.env("DEADLINE_HOURS")))
        # Do not manufacture an overdue period predating schedule activation.
        activated = c.dt(c.env("SCHEDULE_ACTIVE_FROM"))
        if due >= activated and current > deadline:
            kinds = c.kinds()
            for kind in kinds:
                satisfied = any(r.get("kind") == kind and r.get("validated_at")
                    and due <= c.dt(r["started_at"]) <= deadline and c.dt(r["validated_at"]) <= deadline
                    for r in all_records)
                if not satisfied:
                    overdue += 1
                    key = {"resource_id": "#deadline", "test_date": "%s-%s" % (due.date(), kind)}
                    try:
                        existing = c.get(key)
                    except ValueError:
                        existing = None
                    if not existing:
                        c.put({**key, "kind": kind, "run_id": c.digest(key)[:24], "started_at": c.iso(due),
                               "result": "LATE", "cleanup_status": "NOT_REQUIRED", "finalized": False,
                               "failure_reason": "QuarterlyTestMissingOrLate", "review_due_at": c.iso(current + timedelta(days=7)),
                               "signoff": {"status": "PENDING", "signed_off_by": None}})
                    if not existing or not existing.get("finalized"):
                        invoke("REPORT_FUNCTION", {"job": key})
    c.metric("CleanupPending", pending)
    c.metric("ReconciliationErrors", errors)
    c.metric("OverdueTests", overdue)
    return {"pending": pending, "errors": errors, "overdue": overdue}
