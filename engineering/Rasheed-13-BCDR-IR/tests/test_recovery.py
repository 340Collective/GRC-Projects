import copy
import io
import json
import math
import os
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from bcdr import common as c, cleanup, fixtures, monitor, report, restore, validate

ENV = {"PREFIX": "grc-test", "PARTITION": "aws", "ACCOUNT_ID": "test-account", "AWS_REGION": "us-east-1",
       "SOURCE_TABLE": "grc-test-source", "SOURCE_TABLE_ARN": "arn:aws:dynamodb:us-east-1:test-account:table/grc-test-source",
       "SOURCE_BUCKET": "grc-test-source-bucket", "RESULTS_TABLE": "grc-test-results", "REPORT_BUCKET": "grc-test-reports",
       "KEY_ARN": "arn:aws:kms:us-east-1:test-account:key/test-key", "IR_BUCKET": "grc-test-ir",
       "VAULT": "grc-test-vault", "RESTORE_ROLE_ARN": "arn:aws:iam::test-account:role/grc-test-restore",
       "DYNAMODB_RTO": "900", "DYNAMODB_RPO": "86400", "S3_RTO": "900", "S3_RPO": "86400",
       "MAX_RESTORE_WAIT": "3600", "ALLOW_FAULTS": "false", "TARGET_APPROVAL": "test-approval", "INCLUDE_S3": "true",
       "EVENT_BUS": "grc-test-events", "EVIDENCE_BUS": "", "RISK_BUS": "", "JIRA_ENABLED": "false",
       "SCHEDULE_STATE": "DISABLED", "SCHEDULE_ACTIVE_FROM": "2026-01-01T00:00:00Z", "DEADLINE_HOURS": "24",
       "RESTORE_FUNCTION": "restore", "CLEANUP_FUNCTION": "cleanup", "REPORT_FUNCTION": "report", "IR_FUNCTION": "ir"}
START = datetime(2026, 10, 1, 9, tzinfo=timezone.utc)
EXECUTION = "arn:aws:states:us-east-1:test-account:execution:grc-test-dr:exercise"


class AwsError(Exception):
    def __init__(self, code):
        self.response = {"Error": {"Code": code}}


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.stack = {}
        self.services = {name: MagicMock(name=name) for name in ("dynamodb", "s3", "backup", "events", "lambda", "ssm", "stepfunctions", "cloudwatch")}
        self.services["s3"].put_object.return_value = {"VersionId": "report-version"}
        self.services["s3"].list_objects_v2.return_value = {"Contents":[]}
        self.services["dynamodb"].scan.return_value = {"Items": []}
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, ENV).start()
        patch.object(c, "client", side_effect=lambda service: self.services[service]).start()
        patch.object(c, "now", return_value=START + timedelta(seconds=100)).start()
        patch.object(c, "get", side_effect=self.get).start()
        patch.object(c, "put", side_effect=self.put).start()
        patch.object(c, "records", side_effect=lambda: copy.deepcopy(list(self.stack.values()))).start()

    def get(self, key):
        try:
            return copy.deepcopy(self.stack[(key["resource_id"], key["test_date"])])
        except KeyError:
            raise ValueError("RunNotRegistered")

    def put(self, item, create=False):
        key = (item["resource_id"], item["test_date"])
        if create and key in self.stack:
            raise AwsError("ConditionalCheckFailedException")
        self.stack[key] = copy.deepcopy(item)
        return item

    def new(self, kind="dynamodb"):
        response = restore.plan({"execution_arn": EXECUTION, "start_time": c.iso(START), "request": {"resource_types": [kind]}})
        return response["jobs"][0]

    def ready(self, kind="dynamodb"):
        job = self.new(kind)
        row = self.get(job)
        rows, objects = fixtures.fixture()
        marker_time = c.iso(START - timedelta(seconds=60))
        rows.append(fixtures.marker(marker_time))
        objects[fixtures.MARKER_KEY]=c.compact({'write_started_at':marker_time}).encode()
        facts=[{'key':k,'size':len(v),'sha256':c.digest(v)} for k,v in sorted(objects.items())]
        baseline = {"schema_version":3,"data_marker": {"write_started_at": marker_time, "write_acknowledged_at": marker_time},
                    "s3_data_marker": {"write_started_at":marker_time,"write_acknowledged_at":marker_time},
                    "dynamodb": {"count": len(rows), "sha256": c.digest(sorted(rows, key=c.compact))}, "s3": {'count':len(facts),'sha256':c.digest(facts)}}
        row.update({"baseline": baseline, "baseline_sha256": c.digest(baseline), "recovery_point": "test-point",
                    "rpo_achieved": 60, "start_intent": True, "restore_job_id": "test-job", "restore_status": "COMPLETED", "cleanup_status": "PENDING"})
        self.put(row)
        self.services["backup"].describe_restore_job.return_value = {"Status": "COMPLETED", "RecoveryPointArn": "test-point"}
        self.services["backup"].get_restore_job_metadata.return_value = {"Metadata": {"targetTableName" if kind=='dynamodb' else 'DestinationBucketName': row["target"]}}
        self.services["dynamodb"].describe_table.return_value = {"Table": {"TableStatus": "ACTIVE", "SSEDescription": {"Status": "ENABLED", "KMSMasterKeyArn": ENV["KEY_ARN"]}}}
        self.services["dynamodb"].get_paginator.return_value.paginate.return_value = [{"Items": rows[:5]}, {"Items": rows[5:]}]
        self.services["s3"].get_paginator.return_value.paginate.return_value = [{"Contents": [{"Key": k, "Size": len(v)} for k, v in objects.items()]}]
        self.services["s3"].get_object.side_effect = lambda Bucket, Key, **kw: {"Body": io.BytesIO(objects[Key]), "ServerSideEncryption": "aws:kms", "SSEKMSKeyId": ENV["KEY_ARN"]}
        self.services['s3'].get_bucket_tagging.return_value={'TagSet':[{'Key':'grc-project','Value':'13'},{'Key':'bcdr-run-id','Value':row['run_id']}]}
        self.services['s3'].get_bucket_versioning.return_value={'Status':'Enabled'}
        self.services['s3'].get_public_access_block.return_value={'PublicAccessBlockConfiguration':{k:True for k in ['BlockPublicAcls','IgnorePublicAcls','BlockPublicPolicy','RestrictPublicBuckets']}}
        self.services['s3'].get_bucket_policy.return_value={'Policy':c.tls_policy(row['target'])}
        self.services['s3'].get_bucket_encryption.return_value={'ServerSideEncryptionConfiguration':{'Rules':[{'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'aws:kms','KMSMasterKeyID':ENV['KEY_ARN']}}]}}
        return job

    def test_plan_retries_preserve_original_record_and_unique_ids(self):
        job = self.new()
        existing = self.get(job)
        existing["restore_job_id"] = "saved-job"
        self.put(existing)
        self.assertEqual(job, self.new())
        self.assertEqual("saved-job", self.get(job)["restore_job_id"])
        other = restore.plan({"execution_arn": EXECUTION + "-other", "start_time": c.iso(START), "request": {}})["jobs"][0]
        self.assertNotEqual(self.get(job)["run_id"], self.get(other)["run_id"])

    def test_invalid_resource_and_fault_inputs_rejected(self):
        for request in ({"resource_types": ["production"]}, {"resource_types": []}, {"resource_types": ["s3", "s3"]}, {"force_validation_failure": True}, {"force_validation_failure": "false"}):
            with self.subTest(request=request), self.assertRaises(ValueError):
                restore.plan({"execution_arn": EXECUTION, "start_time": c.iso(START), "request": request})

    def test_backup_selection_rejects_wrong_resource_incomplete_and_old_baseline(self):
        points = [dict(RecoveryPointArn="good", ResourceArn="source", CreationDate=START, Status="COMPLETED"),
                  dict(RecoveryPointArn="incomplete", ResourceArn="source", CreationDate=START + timedelta(seconds=1), Status="PARTIAL"),
                  dict(RecoveryPointArn="wrong", ResourceArn="other", CreationDate=START + timedelta(seconds=2), Status="COMPLETED")]
        self.assertEqual("good", restore.select_point(points, "source", c.iso(START))["RecoveryPointArn"])
        with self.assertRaisesRegex(ValueError, "NoCompleted"):
            restore.select_point(points, "source", c.iso(START + timedelta(seconds=1)))

    def test_no_recovery_points_never_pass(self):
        with self.assertRaises(ValueError):
            restore.select_point([], "source", c.iso(START))

    def test_start_registers_intent_before_aws_and_uses_stable_token(self):
        job = self.new()
        row = self.get(job)
        row["recovery_point"] = "test-point"
        self.put(row)
        observed = []
        def start(**kwargs):
            observed.append(self.get(job))
            return {"RestoreJobId": "test-job"}
        self.services["backup"].start_restore_job.side_effect = start
        restore.handler({"action": "start", "job": job}, None)
        restore.handler({"action": "start", "job": job}, None)
        self.assertTrue(observed[0]["start_intent"])
        self.assertEqual("PENDING", observed[0]["cleanup_status"])
        self.services["backup"].start_restore_job.assert_called_once()
        args = self.services["backup"].start_restore_job.call_args.kwargs
        self.assertEqual(self.get(job)["run_id"], args["IdempotencyToken"])
        self.assertEqual("KMS", args["Metadata"]["encryptionType"])
        self.services["s3"].put_bucket_versioning.assert_not_called()

    def test_dynamodb_full_baseline_and_pagination_pass(self):
        job = self.ready()
        self.assertTrue(validate.handler({"job": job}, None)["passed"])
        record = self.get(job)
        self.assertEqual(100, record["rto_achieved"])
        self.assertEqual("PENDING", record["signoff"]["status"])



    def test_equal_counts_with_changed_content_fail(self):
        job = self.ready()
        rows, _ = fixtures.fixture()
        rows[-1]["value"] = {"S": "corrupt"}
        rows.append(fixtures.marker(c.iso(START - timedelta(seconds=60))))
        self.services["dynamodb"].get_paginator.return_value.paginate.return_value = [{"Items": rows}]
        self.assertFalse(validate.handler({"job": job}, None)["passed"])

    def test_forced_failure_preserves_truthful_integrity_result(self):
        job = self.ready()
        row = self.get(job)
        row['force_validation_failure'] = True
        self.put(row)
        self.assertFalse(validate.handler({'job':job},None)['passed'])
        result=self.get(job)
        self.assertTrue(result['validation']['passed'])
        self.assertEqual('ForcedValidationFailure',result['failure_reason'])

    def test_lost_restore_start_response_discovers_exact_job_without_replay(self):
        job = self.ready()
        row = self.get(job)
        row.pop('restore_job_id')
        self.put(row)
        self.services['backup'].get_paginator.return_value.paginate.return_value = [
            {'RestoreJobs':[{'RestoreJobId':'recovered-job','RecoveryPointArn':'test-point'}]}]
        self.assertTrue(restore.handler({'action':'start','job':job},None)['started'])
        self.assertEqual('recovered-job',self.get(job)['restore_job_id'])
        self.services['backup'].start_restore_job.assert_not_called()

    def test_cleanup_rejects_restore_metadata_for_a_different_target(self):
        job = self.ready()
        self.services['backup'].get_restore_job_metadata.return_value = {'Metadata':{'targetTableName':'different-target'}}
        with self.assertRaises(ValueError):
            cleanup.handler({'job':job},None)
        self.services['dynamodb'].delete_table.assert_not_called()

    def test_stale_backup_and_slow_validation_fail_independently(self):
        for field in ("rto_target", "rpo_target"):
            with self.subTest(field=field):
                job = self.ready()
                record = self.get(job)
                record[field] = 1
                self.put(record)
                self.assertFalse(validate.handler({"job": job}, None)["passed"])
                self.assertTrue(self.get(job)["validation"]["passed"])

    def test_manifest_tampering_and_wrong_encryption_fail_closed(self):
        job = self.ready()
        row = self.get(job)
        row["baseline_sha256"] = "tampered"
        self.put(row)
        with self.assertRaisesRegex(ValueError, "BaselineIntegrity"):
            validate.handler({"job": job}, None)
        job = self.ready()
        self.services["dynamodb"].describe_table.return_value["Table"]["SSEDescription"]["KMSMasterKeyArn"] = "wrong"
        with self.assertRaisesRegex(ValueError, "EncryptionMismatch"):
            validate.handler({"job": job}, None)

    def test_cleanup_refuses_tampered_target(self):
        job = self.ready()
        row = self.get(job)
        row["target"] = ENV["SOURCE_TABLE"]
        self.put(row)
        with self.assertRaisesRegex(ValueError, "Unowned"):
            cleanup.handler({"job": job}, None)
        self.services["dynamodb"].delete_table.assert_not_called()

    def test_cleanup_waits_for_restore_terminal_state(self):
        job = self.ready()
        self.services["backup"].describe_restore_job.return_value = {"Status": "RUNNING"}
        self.assertFalse(cleanup.handler({"job": job}, None)["done"])
        self.services["dynamodb"].delete_table.assert_not_called()

    def test_cleanup_requires_job_reconciliation_before_delete(self):
        job = self.ready()
        row = self.get(job)
        del row["restore_job_id"]
        self.put(row)
        with self.assertRaisesRegex(RuntimeError, "Reconciliation"):
            cleanup.handler({"job": job}, None)
        self.services["dynamodb"].delete_table.assert_not_called()



    def test_cleanup_nonexistent_table_is_idempotent_success(self):
        job = self.ready()
        self.services["dynamodb"].describe_table.side_effect = AwsError("ResourceNotFoundException")
        self.assertTrue(cleanup.handler({"job": job}, None)["done"])
        self.assertTrue(cleanup.handler({"job": job}, None)["done"])

    def test_report_does_not_mask_cleanup_failure_or_claim_integration(self):
        job = self.ready()
        validate.handler({"job": job}, None)
        self.services["events"].put_events.return_value = {"FailedEntryCount": 0, "Entries": [{"EventId": "one"}, {"EventId": "two"}]}
        response = report.handler({"job": job}, None)
        self.assertFalse(response["passed"])
        stored = self.get(job)
        self.assertEqual("PASS", stored["result"])
        self.assertEqual("FAIL", stored["overall_result"])
        self.assertFalse(stored["finalized"])
        self.assertEqual("NOT_CONFIGURED", stored["delivery"]["jira"])
        self.assertEqual("ACCEPTED_NOT_DOWNSTREAM_CONFIRMED", stored["delivery"]["event_bus"])

    def test_event_delivery_failure_leaves_run_for_retry(self):
        job = self.ready()
        self.services["events"].put_events.return_value = {"FailedEntryCount": 1, "Entries": [{"ErrorCode": "InternalFailure"}]}
        with self.assertRaises(RuntimeError):
            report.handler({"job": job}, None)
        self.assertFalse(self.get(job)["finalized"])

    def test_duplicate_report_uses_same_event_id(self):
        job = self.ready()
        self.services["events"].put_events.return_value = {"FailedEntryCount": 0, "Entries": [{}, {}]}
        report.handler({"job": job}, None)
        first = self.services["events"].put_events.call_args.kwargs["Entries"][0]["Detail"]
        report.handler({"job": job}, None)
        second = self.services["events"].put_events.call_args.kwargs["Entries"][0]["Detail"]
        self.assertEqual(json.loads(first)["event_id"], json.loads(second)["event_id"])

    def test_dr_event_pins_evidence_version_and_hash_for_project06(self):
        job=self.ready()
        self.services['events'].put_events.return_value={'FailedEntryCount':0,'Entries':[{},{}]}
        report.handler({'job':job},None)
        detail=json.loads(self.services['events'].put_events.call_args.kwargs['Entries'][0]['Detail'])
        stored=json.loads(self.services['s3'].put_object.call_args_list[0].kwargs['Body'])
        self.assertEqual('report-version',detail['evidence']['version'])
        self.assertEqual(c.digest(stored),detail['evidence']['sha256'])

    def test_end_to_end_table_validation_cleanup_and_passing_report(self):
        job = self.ready()
        self.assertTrue(validate.handler({"job": job}, None)["passed"])
        self.services["dynamodb"].describe_table.side_effect = AwsError("ResourceNotFoundException")
        self.assertTrue(cleanup.handler({"job": job}, None)["done"])
        self.services["events"].put_events.return_value = {"FailedEntryCount": 0, "Entries": [{"EventId": "test"}]}
        self.assertTrue(report.handler({"job": job}, None)["passed"])
        self.assertTrue(self.get(job)["finalized"])

    def test_monitor_does_not_race_running_workflow(self):
        self.ready()
        self.services["stepfunctions"].describe_execution.return_value = {"status": "RUNNING"}
        with patch.object(monitor, "invoke", return_value={}) as invoke:
            monitor.handler({}, None)
        invoke.assert_not_called()

    def test_monitor_recovers_aborted_workflow_and_missing_job_id(self):
        job = self.ready()
        record = self.get(job)
        del record["restore_job_id"]
        self.put(record)
        self.services["stepfunctions"].describe_execution.return_value = {"status": "ABORTED"}
        with patch.object(monitor, "invoke", side_effect=[{}, {}, {"done": True}, {}]) as invoke:
            result = monitor.handler({}, None)
        self.assertEqual(0, result["errors"])
        self.assertEqual(["RESTORE_FUNCTION", "RESTORE_FUNCTION", "CLEANUP_FUNCTION", "REPORT_FUNCTION"], [x.args[0] for x in invoke.call_args_list])

    def test_monitor_reports_missing_quarter_once_per_resource(self):
        with patch.dict(os.environ, {"SCHEDULE_STATE": "ENABLED"}), patch.object(c, "now", return_value=START + timedelta(days=2)), patch.object(monitor, "invoke", return_value={}):
            result = monitor.handler({}, None)
        self.assertEqual(2, result["overdue"])
        self.assertEqual(2, len(self.stack))
        self.assertTrue(all(r["result"] == "LATE" for r in self.stack.values()))

    def test_schedule_activation_does_not_backdate_obligation(self):
        with patch.dict(os.environ, {"SCHEDULE_STATE": "ENABLED", "SCHEDULE_ACTIVE_FROM": "2026-10-20T00:00:00Z"}), patch.object(c, "now", return_value=START + timedelta(days=25)), patch.object(monitor, "invoke", return_value={}):
            self.assertEqual(0, monitor.handler({}, None)["overdue"])




    def test_default_scope_includes_both_sources(self):
        with patch.dict(os.environ, {"INCLUDE_S3": "false"}):
            jobs = restore.plan({"execution_arn": EXECUTION, "start_time": c.iso(START), "request": {}})["jobs"]
            self.assertEqual(["dynamodb","s3"], [j["resource_id"] for j in jobs])

    def test_recovered_marker_bound_is_distinct_from_backup_age(self):
        job = self.ready()
        row = self.get(job)
        row["recovery_point_age_seconds"] = 1
        self.put(row)
        validate.handler({"job": job}, None)
        row = self.get(job)
        self.assertEqual(60, row["rpo_achieved"])
        self.assertEqual(1, row["recovery_point_age_seconds"])
        self.assertEqual("RECOVERED_SYNTHETIC_MARKER_UPPER_BOUND", row["rpo_measure"])
        self.assertEqual("NOT_TESTED", row["service_recovery"])

    def test_missing_timestamp_marker_cannot_pass(self):
        job = self.ready()
        rows, _ = fixtures.fixture()
        self.services["dynamodb"].get_paginator.return_value.paginate.return_value = [{"Items": rows}]
        with self.assertRaisesRegex(ValueError, "MarkerMissing"):
            validate.handler({"job": job}, None)

    def test_fixture_pins_version_and_seeds_only_both_synthetic_sources(self):
        self.services["s3"].put_object.return_value = {"VersionId": "baseline-version"}
        with patch.dict(os.environ, {"INCLUDE_S3": "false"}):
            self.assertEqual("READY", fixtures.handler({}, None)["status"])
            self.assertEqual("ALREADY_READY", fixtures.handler({}, None)["status"])
        self.assertEqual(5,self.services["s3"].put_object.call_count)
        self.assertEqual(11,len([x for x in self.services['dynamodb'].put_item.call_args_list if x.kwargs['TableName']==ENV['SOURCE_TABLE']]))
        self.assertEqual("baseline-version", self.get({"resource_id": "#fixture", "test_date": "v1"})["manifest_version"])

    def test_manifest_read_requires_and_uses_exact_version(self):
        self.services["s3"].get_object.side_effect = None
        self.services["s3"].get_object.return_value = {"Body": io.BytesIO(b'{}')}
        self.assertEqual({}, c.read_json("bucket", "manifest", "fixed-version"))
        self.services["s3"].get_object.assert_called_once_with(Bucket="bucket", Key="manifest", VersionId="fixed-version")
        with self.assertRaisesRegex(ValueError, "VersionedManifest"):
            c.read_json("bucket", "manifest", "null")

    def test_prepare_pins_manifest_and_keeps_backup_age_separate(self):
        job = self.new()
        manifest = {"ready_at": c.iso(START - timedelta(minutes=10)), "schema_version": 2}
        self.put({"resource_id": "#fixture", "test_date": "v1", "ready_at": manifest["ready_at"],
                  "manifest_key": "baseline", "manifest_version": "pinned", "manifest_sha256": c.digest(manifest)})
        self.services["s3"].get_object.side_effect = None
        self.services["s3"].get_object.return_value = {"Body": io.BytesIO(c.compact(manifest).encode())}
        self.services["backup"].get_paginator.return_value.paginate.return_value = [{"RecoveryPoints": [{
            "ResourceArn": ENV["SOURCE_TABLE_ARN"], "RecoveryPointArn": "point", "Status": "COMPLETED",
            "CreationDate": START - timedelta(seconds=30)}]}]
        restore.handler({"action": "prepare", "job": job}, None)
        self.services["s3"].get_object.assert_called_once_with(Bucket=ENV["REPORT_BUCKET"], Key="baseline", VersionId="pinned")
        record = self.get(job)
        self.assertEqual(30, record["recovery_point_age_seconds"])
        self.assertIsNone(record["rpo_achieved"])

    def test_component_rto_rounds_up_at_target_boundary(self):
        job = self.ready()
        row = self.get(job)
        row["rto_target"] = 100
        self.put(row)
        with patch.object(c, "now", return_value=START + timedelta(seconds=100, microseconds=1)):
            self.assertFalse(validate.handler({"job": job}, None)["passed"])
        self.assertEqual(101, self.get(job)["rto_achieved"])

    def test_rto_matches_recorded_validation_completion_when_clock_advances(self):
        job = self.ready()
        ticks = [START + timedelta(seconds=100, microseconds=1),
                 START + timedelta(seconds=101, microseconds=1)]
        with patch.object(c, "now", side_effect=ticks):
            validate.handler({"job": job}, None)
        record = self.get(job)
        measured = math.ceil((c.dt(record["validated_at"]) - c.dt(record["started_at"])).total_seconds())
        self.assertEqual(measured, record["rto_achieved"])

    def test_incomplete_seed_never_silently_rewrites_source(self):
        self.put({"resource_id": "#fixture", "test_date": "v1", "status": "SEEDING"})
        with self.assertRaisesRegex(RuntimeError, "FixtureInitializationIncomplete"):
            fixtures.handler({}, None)
        self.assertFalse(any(x.kwargs['TableName']==ENV['SOURCE_TABLE'] for x in self.services['dynamodb'].put_item.call_args_list))
        self.services["s3"].put_object.assert_not_called()

    def test_first_seed_refuses_an_unexpected_nonempty_source(self):
        self.services['dynamodb'].scan.return_value={'Items':[{'pk':{'S':'unexpected'}}]}
        with self.assertRaisesRegex(ValueError,'MustBeEmpty'):
            fixtures.handler({},None)
        self.assertFalse(any(x.kwargs['TableName']==ENV['SOURCE_TABLE'] for x in self.services['dynamodb'].put_item.call_args_list))
        self.assertEqual({},self.stack)

    def test_deadline_obligates_both_sources(self):
        with patch.dict(os.environ, {"INCLUDE_S3": "false", "SCHEDULE_STATE": "ENABLED"}), patch.object(c, "now", return_value=START + timedelta(days=2)), patch.object(monitor, "invoke", return_value={}):
            result = monitor.handler({}, None)
        self.assertEqual(2, result["overdue"])


if __name__ == "__main__":
    unittest.main()
