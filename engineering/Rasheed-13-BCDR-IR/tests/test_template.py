"""Deployment invariants that linting alone does not establish."""
import json
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
TEMPLATE = runpy.run_path(str(ROOT / "tools/render_template.py"))["template"]
R = TEMPLATE["Resources"]


class TemplateTests(unittest.TestCase):


    def test_separate_fixture_writer_and_jira_is_required_for_live_scope(self):
        self.assertEqual({'Controller','Validate','Janitor','Fixture'}, {name for name,r in R.items() if r['Type']=='AWS::Lambda::Function'})
        self.assertIn('LiveJiraRequired',TEMPLATE['Rules'])
        self.assertIn('RunningCadenceRequired',TEMPLATE['Rules'])
        env=R['Janitor']['Properties']['Environment']['Variables']
        self.assertNotIn('Janitor',json.dumps(env))

    def test_every_role_has_existing_permissions_boundary(self):
        for name, resource in R.items():
            if resource["Type"] == "AWS::IAM::Role":
                with self.subTest(name=name):
                    self.assertIn("grc-permissions-boundary", json.dumps(resource["Properties"]["PermissionsBoundary"]))
                    self.assertNotIn("ManagedPolicyArns", resource["Properties"])

    def test_approval_cannot_be_overridden_by_runbook_input(self):
        for name in ("IrQuarantine", "IrRelease"):
            content = R[name]["Properties"]["Content"]
            self.assertEqual(["IncidentId"], list(content["parameters"]))
            steps = content["mainSteps"]
            self.assertEqual("aws:approve", steps[1]["action"])
            self.assertEqual("Abort", steps[1]["onFailure"])
            self.assertEqual([{"Ref": "IrApproverArn"}], steps[1]["inputs"]["Approvers"])
            self.assertEqual("PutBucketPolicy", steps[2]["inputs"]["Api"])
            self.assertEqual({"Ref": "IrBucket"}, steps[2]["inputs"]["Bucket"])

    def test_cleanup_permissions_cannot_delete_source(self):
        statements = R["JanitorRole"]["Properties"]["Policies"][0]["PolicyDocument"]["Statement"]
        deletions = [s for s in statements if "Delete" in json.dumps(s["Action"])]
        self.assertTrue(deletions)
        for statement in deletions:
            self.assertIn("-restore-", json.dumps(statement["Resource"]))
            self.assertNotIn("SourceTable", json.dumps(statement["Resource"]))
            self.assertNotIn("SourceBucket", json.dumps(statement["Resource"]))

    def test_validator_has_no_source_access_or_delete_permissions(self):
        policy = R["ValidateRole"]["Properties"]["Policies"][0]["PolicyDocument"]
        text = json.dumps(policy)
        self.assertNotIn("SourceTable", text)
        self.assertNotIn("SourceBucket", text)
        self.assertNotIn("Delete", text)

    def test_all_buckets_private_versioned_and_cmk_encrypted(self):
        for resource in R.values():
            if resource["Type"] == "AWS::S3::Bucket":
                props = resource["Properties"]
                self.assertTrue(all(props["PublicAccessBlockConfiguration"].values()))
                self.assertEqual("Enabled", props["VersioningConfiguration"]["Status"])
                self.assertIn("Key", json.dumps(props["BucketEncryption"]))

    def test_no_vault_lock_or_automatic_secret_creation(self):
        self.assertNotIn("LockConfiguration", R["Vault"]["Properties"])
        self.assertFalse(any(r["Type"] in {"AWS::SecretsManager::Secret", "AWS::Events::Connection"} for r in R.values()))

    def test_no_default_approved_recovery_targets(self):
        for name in ("DynamoDbRtoSeconds", "DynamoDbRpoSeconds", "S3RtoSeconds", "S3RpoSeconds"):
            self.assertNotIn("Default", TEMPLATE["Parameters"][name])

    def test_stateful_resources_are_not_orphaned_on_replacement(self):
        kinds = {"AWS::S3::Bucket", "AWS::DynamoDB::Table", "AWS::Backup::BackupVault"}
        stateful = {name: r for name, r in R.items() if r["Type"] in kinds}
        self.assertEqual({"SourceTable", "ResultsTable", "SourceBucket", "ReportBucket", "IrBucket", "Vault"}, set(stateful))
        for name, resource in stateful.items():
            with self.subTest(name=name):
                self.assertEqual("Delete", resource["DeletionPolicy"])
                self.assertEqual("Delete", resource["UpdateReplacePolicy"])

    def test_evidence_noncurrent_retention_requires_an_explicit_duration(self):
        parameter = TEMPLATE["Parameters"]["EvidenceNoncurrentRetentionDays"]
        self.assertEqual("Number", parameter["Type"])
        self.assertEqual(1, parameter["MinValue"])
        self.assertNotIn("Default", parameter)
        for filename in ("parameters.example.json", "parameters.running.example.json"):
            values = {p["ParameterKey"]: p["ParameterValue"] for p in json.loads((ROOT / filename).read_text())}
            self.assertEqual("REPLACE_APPROVED_INTEGER_DAYS", values["EvidenceNoncurrentRetentionDays"])

    def test_report_and_ir_lifecycle_preserves_current_evidence_and_bounds_old_versions(self):
        for name in ("ReportBucket", "IrBucket"):
            with self.subTest(name=name):
                rules = R[name]["Properties"]["LifecycleConfiguration"]["Rules"]
                self.assertEqual(1, len(rules))
                rule = rules[0]
                self.assertEqual("Enabled", rule["Status"])
                self.assertEqual({"NoncurrentDays": {"Ref": "EvidenceNoncurrentRetentionDays"}}, rule["NoncurrentVersionExpiration"])
                self.assertEqual({"DaysAfterInitiation": 1}, rule["AbortIncompleteMultipartUpload"])
                self.assertNotIn("Prefix", rule)
                self.assertNotIn("Filter", rule)
                self.assertNotIn("ExpirationInDays", rule)
                self.assertNotIn("ExpirationDate", rule)
                self.assertNotIn("ExpiredObjectDeleteMarker", rule)

    def test_fixture_version_and_recovery_point_retention_remain_separate(self):
        rule = R["SourceBucket"]["Properties"]["LifecycleConfiguration"]["Rules"][0]
        self.assertEqual({"NoncurrentDays": 7}, rule["NoncurrentVersionExpiration"])
        self.assertEqual({"DaysAfterInitiation": 1}, rule["AbortIncompleteMultipartUpload"])
        backup_rule = R["BackupPlan"]["Properties"]["BackupPlan"]["BackupPlanRule"][0]
        self.assertEqual({"DeleteAfterDays": {"Ref": "BackupRetentionDays"}}, backup_rule["Lifecycle"])

    def test_independent_monitor_and_running_quarterly_schedule(self):
        self.assertEqual("rate(15 minutes)", R["MonitorRule"]["Properties"]["ScheduleExpression"])
        self.assertEqual("ENABLED", TEMPLATE["Parameters"]["QuarterlyScheduleState"]["Default"])
        self.assertEqual("STANDARD", R["StateMachine"]["Properties"]["StateMachineType"])

    def test_native_template_under_repository_limit(self):
        self.assertLess((REPO_ROOT / "infrastructure/cloudformation/grc-bcdr.yaml").stat().st_size, 51200)
        self.assertNotIn("Transform", TEMPLATE)
        self.assertFalse(any(r["Type"].startswith("Custom::") for r in R.values()))

    def test_function_environment_contracts(self):
        for name in ("Controller", "Validate", "Janitor", "Fixture"):
            env = R[name]["Properties"]["Environment"]["Variables"]
            self.assertTrue(all(k in env for k in ("RESULTS_TABLE", "SOURCE_TABLE", "SOURCE_TABLE_ARN", "SOURCE_BUCKET", "REPORT_BUCKET", "PREFIX", "ACCOUNT_ID", "PARTITION")))
        self.assertIn("REPORT_FUNCTION", R["Janitor"]["Properties"]["Environment"]["Variables"])

    def test_all_resources_and_outputs_are_disabled_by_default(self):
        self.assertEqual("false", TEMPLATE["Parameters"]["EnableRuntimeResources"]["Default"])
        for resource in R.values():
            condition = resource["Condition"]
            self.assertIn(condition, {"Live", "HasSchedule", "HasJira", "HasEvidence", "HasRisk"})
            if condition != "Live":
                self.assertIn({"Condition": "Live"}, TEMPLATE["Conditions"][condition]["Fn::And"])
        self.assertTrue(all(o["Condition"] in {"Live","HasSchedule"} for o in TEMPLATE["Outputs"].values()))

    def test_existing_key_and_daily_backup_for_both_sources(self):
        self.assertFalse(any(r["Type"].startswith("AWS::KMS::") for r in R.values()))
        self.assertEqual({"Ref": "ExistingKmsKeyArn"}, R["Vault"]["Properties"]["EncryptionKeyArn"])
        self.assertEqual("true", TEMPLATE["Parameters"]["EnableScheduledBackups"]["Default"])
        self.assertNotIn("IncludeS3Recovery", TEMPLATE["Parameters"])
        self.assertEqual("HasSchedule", R["Selection"]["Condition"])
        self.assertIn("SourceBucket", json.dumps(R["Selection"]["Properties"]))
        for resource in R.values():
            if resource["Type"] == "AWS::Lambda::Function":
                self.assertNotIn("ReservedConcurrentExecutions", resource["Properties"])

    def test_fixture_cannot_forge_dr_results_and_dr_roles_cannot_mutate_sources(self):
        policy=R['FixtureRole']['Properties']['Policies'][0]['PolicyDocument']['Statement']
        writes=[s for s in policy if 'dynamodb:PutItem' in s['Action'] and 'ResultsTable' in json.dumps(s['Resource'])]
        self.assertEqual(1,len(writes))
        self.assertEqual(['#fixture','#fixture-lock'],writes[0]['Condition']['ForAllValues:StringEquals']['dynamodb:LeadingKeys'])
        for name in ['ControllerRole','ValidateRole','JanitorRole']:
            for statement in R[name]['Properties']['Policies'][0]['PolicyDocument']['Statement']:
                if any(w in json.dumps(statement['Action']) for w in ['PutObject','PutItem','DeleteObject','DeleteTable']):
                    self.assertNotIn('SourceTable',json.dumps(statement['Resource']))
                    self.assertNotIn('SourceBucket',json.dumps(statement['Resource']))

    def test_fixture_schedule_precedes_periodic_backup_and_has_failure_visibility(self):
        self.assertEqual('cron(0 2 * * ? *)',R['FixtureSchedule']['Properties']['ScheduleExpression'])
        self.assertEqual('cron(0 3 * * ? *)',TEMPLATE['Parameters']['BackupSchedule']['Default'])
        self.assertIn('FixtureAsync',R)
        self.assertIn('FixtureAlarm',R)
        self.assertIn('scheduled-time',R['FixtureSchedule']['Properties']['Target']['Input'])


if __name__ == "__main__":
    unittest.main()
