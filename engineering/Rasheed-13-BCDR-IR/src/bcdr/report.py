"""Publish private evidence and small integration events with stable identifiers."""
from . import common as c


def handler(event, context):
    record = c.get(event["job"])
    cleanup_ok = record["cleanup_status"] in {"DELETED", "NOT_REQUIRED"}
    if record["result"] == "RUNNING":
        record.update({"result": "FAIL", "failure_reason": "ExecutionEndedWithoutValidation"})
    previous_result = record.get("overall_result")
    record["overall_result"] = record["result"] if cleanup_ok else "FAIL"
    stamp = c.dt(record["started_at"])
    quarter = (stamp.month - 1) // 3 + 1
    path = "dr-tests/%s/Q%s/%s/%s.json" % (stamp.year, quarter, record["kind"], record["run_id"])
    record["report_key"] = path
    record["delivery"] = {"local_evidence": "WRITTEN", "event_bus": "PENDING",
        "project06": "CONFIGURED_UNVERIFIED" if c.env("EVIDENCE_BUS") else "NOT_CONFIGURED",
        "project07": "CONFIGURED_UNVERIFIED" if c.env("RISK_BUS") else "NOT_CONFIGURED",
        "jira": "CONFIGURED_UNVERIFIED" if c.env("JIRA_ENABLED") == "true" else "NOT_CONFIGURED"}
    # A cleanup transition changes the event ID, while repeated attempts at the
    # same state keep the same ID. Consumers deduplicate by event_id and upsert
    # findings by finding_key, rather than creating a new issue on each retry.
    revision = c.digest({"result": record["overall_result"], "cleanup": record["cleanup_status"]})[:12]
    event_id = record["run_id"] + ":" + revision

    def prepare():
        detail = {"schema_version": "1.1", "event_id": event_id,
              "run_id": record["run_id"], "correlation_label": "bcdr-" + record["run_id"],
              "occurred_at": c.iso(),
              "finding_key": "bcdr:" + record["run_id"], "resource_type": record["kind"],
              "result": record["overall_result"], "cleanup_status": record["cleanup_status"],
              "rto_target_seconds": record.get("rto_target"), "rto_achieved_seconds": record.get("rto_achieved"),
              "rpo_target_seconds": record.get("rpo_target"), "rpo_upper_bound_seconds": record.get("rpo_achieved"),
              "rpo_measure": record.get("rpo_measure"), "recovery_point_age_seconds": record.get("recovery_point_age_seconds"),
              "scope": record.get("scope", "SYNTHETIC_COMPONENT_ONLY"), "service_recovery": "NOT_TESTED",
              "reason": record.get("failure_reason"), "owner_role": "BCDR-Engineer", "review_due_at": record.get("review_due_at"),
              "evidence": {"bucket": c.env("REPORT_BUCKET"), "key": path}, "signoff_status": "PENDING"}
        snapshot = {k: v for k, v in record.items() if k not in {"report_version", "report_sha256"}}
        version = c.write_json(c.env("REPORT_BUCKET"), path, snapshot).get("VersionId")
        if not isinstance(version, str) or not version or version == "null":
            raise RuntimeError("VersionedReportRequired")
        detail["evidence"].update({"version": version, "sha256": c.digest(snapshot)})
        entries = [{"Source": "grc.bcdr", "DetailType": "BCDR Test Result", "EventBusName": c.env("EVENT_BUS"), "Detail": c.compact(detail)}]
        if record["overall_result"] != "PASS" or previous_result not in {None, "PASS"}:
            entries.append({**entries[0], "DetailType": "BCDR Finding", "Detail": c.compact({**detail,
                "event_id": event_id + ":finding", "finding_status": "RESOLVED" if record["overall_result"] == "PASS" else "OPEN"})})
        return {"entries": entries}

    entries = c.publication(event_id, prepare)["entries"]
    response = c.client("events").put_events(Entries=entries)
    if response.get("FailedEntryCount", 0) or len(response.get("Entries", [])) != len(entries):
        raise RuntimeError("EventBusRejectedEvidence")
    record["delivery"]["event_bus"] = "ACCEPTED_NOT_DOWNSTREAM_CONFIRMED"
    record["finalized"] = cleanup_ok
    record["reported_at"] = c.iso()
    stored = {k: v for k, v in record.items() if k not in {"report_version", "report_sha256"}}
    version = c.write_json(c.env("REPORT_BUCKET"), path, stored).get("VersionId")
    if not isinstance(version, str) or not version or version == "null":
        raise RuntimeError("VersionedReportRequired")
    record["report_version"] = version
    record["report_sha256"] = c.digest(stored)
    c.put(record)
    return {"passed": record["overall_result"] == "PASS", "report_key": path}
