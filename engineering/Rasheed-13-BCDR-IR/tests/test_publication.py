"""Exercise publication retries with distinct object versions and durable state."""
import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from unittest.mock import patch

import test_recovery as recovery
import test_manage as operator_tests
from bcdr import common as c, report, validate


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.case = recovery.RecoveryTests()
        self.case.setUp()
        self.addCleanup(self.case.doCleanups)
        self.services = self.case.services
        self.writes = []
        self.lock = threading.RLock()
        self.services["s3"].put_object.side_effect = self.write_object
        self.services["events"].put_events.side_effect = lambda **request: {
            "FailedEntryCount": 0, "Entries": [{} for _ in request["Entries"]]}

    def write_object(self, **request):
        with self.lock:
            version = "synthetic-version-" + str(len(self.writes) + 1)
            self.writes.append({"version": version, **request})
        return {"VersionId": version}

    def passing_job(self):
        job = self.case.ready()
        validate.handler({"job": job}, None)
        row = self.case.get(job)
        row["cleanup_status"] = "DELETED"
        self.case.put(row)
        return job

    def operator(self):
        operator = operator_tests.manage.Operator.__new__(operator_tests.manage.Operator)
        operator.clients = self.services
        operator.out = {"ReportBucketName": recovery.ENV["REPORT_BUCKET"],
                        "EventBusName": recovery.ENV["EVENT_BUS"]}
        return operator

    def deliveries(self):
        return [call.kwargs["Entries"] for call in self.services["events"].put_events.call_args_list]

    def assert_same_delivery(self):
        deliveries = self.deliveries()
        self.assertEqual(2, len(deliveries))
        self.assertEqual(deliveries[0], deliveries[1])
        for entry in deliveries[0]:
            pointer = json.loads(entry["Detail"])["evidence"]
            stored = next(w for w in self.writes if w["version"] == pointer["version"])
            self.assertEqual(pointer["key"], stored["Key"])
            self.assertEqual(pointer["sha256"], c.digest(stored["Body"]))

    def test_dr_retry_reuses_exact_event_and_evidence_bytes(self):
        job = self.passing_job()
        report.handler({"job": job}, None)
        with patch.object(c, "now", return_value=recovery.START + timedelta(hours=1)):
            report.handler({"job": job}, None)
        self.assert_same_delivery()

    def test_dr_accepted_event_with_lost_response_is_replayed_unchanged(self):
        job = self.passing_job()
        self.services["events"].put_events.side_effect = [TimeoutError("lost response"),
            {"FailedEntryCount": 0, "Entries": [{}]}]
        with self.assertRaises(TimeoutError):
            report.handler({"job": job}, None)
        self.assertFalse(self.case.get(job)["finalized"])
        report.handler({"job": job}, None)
        self.assert_same_delivery()

    def test_dr_final_record_save_failure_replays_persisted_event(self):
        job = self.passing_job()
        failed = False

        def save(row, create=False):
            nonlocal failed
            if not create and row["resource_id"] == job["resource_id"] and not failed:
                failed = True
                raise TimeoutError("final save failed")
            return self.case.put(row, create)

        with patch.object(c, "put", side_effect=save):
            with self.assertRaises(TimeoutError):
                report.handler({"job": job}, None)
            report.handler({"job": job}, None)
        self.assert_same_delivery()

    def test_saved_envelope_with_lost_write_response_is_reused(self):
        job = self.passing_job()
        failed = False

        def save(row, create=False):
            nonlocal failed
            saved = self.case.put(row, create)
            if create and not failed:
                failed = True
                raise TimeoutError("saved but response lost")
            return saved

        with patch.object(c, "put", side_effect=save):
            with self.assertRaises(TimeoutError):
                report.handler({"job": job}, None)
            self.services["events"].put_events.assert_not_called()
            version = self.writes[0]["version"]
            report.handler({"job": job}, None)
        detail = json.loads(self.deliveries()[0][0]["Detail"])
        self.assertEqual(version, detail["evidence"]["version"])

    def test_failed_envelope_save_never_sends_an_event(self):
        job = self.passing_job()
        with patch.object(c, "put", side_effect=TimeoutError("not saved")):
            with self.assertRaises(TimeoutError):
                report.handler({"job": job}, None)
        self.services["events"].put_events.assert_not_called()
        report.handler({"job": job}, None)
        self.assertEqual(1, len(self.deliveries()))

    def test_concurrent_dr_publishers_choose_one_evidence_pointer(self):
        job = self.passing_job()
        barrier = threading.Barrier(2)

        def write(**request):
            result = self.write_object(**request)
            if json.loads(request["Body"])["delivery"]["event_bus"] == "PENDING":
                barrier.wait(timeout=5)
            return result

        def get(key):
            with self.lock:
                return self.case.get(key)

        def save(row, create=False):
            with self.lock:
                return self.case.put(row, create)

        with patch.object(c, "get", side_effect=get), patch.object(c, "put", side_effect=save):
            self.services["s3"].put_object.side_effect = write
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(report.handler, {"job": job}, None) for _ in range(2)]
                for future in futures:
                    self.assertTrue(future.result(timeout=10)["passed"])
        self.assert_same_delivery()

    def test_cleanup_transition_has_new_id_and_replays_resolution(self):
        job = self.case.ready()
        validate.handler({"job": job}, None)
        report.handler({"job": job}, None)
        row = self.case.get(job)
        row["cleanup_status"] = "DELETED"
        self.case.put(row)
        report.handler({"job": job}, None)
        report.handler({"job": job}, None)
        first, second, third = self.deliveries()
        self.assertNotEqual(json.loads(first[0]["Detail"])["event_id"],
                            json.loads(second[0]["Detail"])["event_id"])
        self.assertEqual(second, third)
        self.assertEqual("RESOLVED", json.loads(second[1]["Detail"])["finding_status"])

    def test_ir_retry_after_restart_and_date_change_reuses_original_pointer(self):
        data = {"status": "Success"}
        first = self.operator().store_ir_evidence("tabletop", "synthetic-exercise", data)
        with patch.object(c, "now", return_value=recovery.START + timedelta(days=1)):
            second = self.operator().store_ir_evidence("tabletop", "synthetic-exercise", data)
        self.assertEqual(first, second)
        self.assertEqual(1, len(self.writes))
        self.assert_same_delivery()

    def test_ir_lost_delivery_response_reuses_saved_event(self):
        self.services["events"].put_events.side_effect = [TimeoutError("lost response"),
            {"FailedEntryCount": 0, "Entries": [{}]}]
        with self.assertRaises(TimeoutError):
            self.operator().store_ir_evidence("runbook-executions", "synthetic-exercise", {"status": "Success"})
        self.operator().store_ir_evidence("runbook-executions", "synthetic-exercise", {"status": "Success"})
        self.assert_same_delivery()

    def test_ir_changed_content_has_distinct_event_id(self):
        for status in ("Pending", "Success"):
            self.operator().store_ir_evidence("tabletop", "synthetic-exercise", {"status": status})
        first, second = [json.loads(entry[0]["Detail"]) for entry in self.deliveries()]
        self.assertNotEqual(first["event_id"], second["event_id"])
        self.assertNotEqual(first["evidence"]["sha256"], second["evidence"]["sha256"])

    def test_invalid_object_version_is_never_published(self):
        self.services["s3"].put_object.side_effect = None
        self.services["s3"].put_object.return_value = {"VersionId": "null"}
        with self.assertRaisesRegex(RuntimeError, "VersionedIrEvidenceRequired"):
            self.operator().store_ir_evidence("tabletop", "synthetic-exercise", {})
        self.services["events"].put_events.assert_not_called()

    def test_inaccessible_envelope_is_not_replaced_or_published(self):
        job = self.passing_job()

        def read(key):
            if key != job:
                raise recovery.AwsError("AccessDenied")
            return self.case.get(key)

        with patch.object(c, "get", side_effect=read), self.assertRaises(recovery.AwsError):
            report.handler({"job": job}, None)
        self.services["s3"].put_object.assert_not_called()
        self.services["events"].put_events.assert_not_called()


if __name__ == "__main__":
    unittest.main()
