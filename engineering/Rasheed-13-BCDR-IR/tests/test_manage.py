import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from botocore.session import get_session
from botocore.validate import validate_parameters
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import manage
import prepare_06
from bcdr import common as c

class AwsError(Exception):
    def __init__(self,code): self.response={'Error':{'Code':code}}

class OperatorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.addCleanup(patch.stopall)
        patch.dict(os.environ).start()
        names=['cloudformation','sts','dynamodb','backup','s3','kms','events','iam','stepfunctions','lambda','ssm','cloudtrail','sqs','scheduler']
        self.clients={name:MagicMock(name=name) for name in names}
        account='000000000000'
        self.out={'SourceTableName':'grc-test-source','SourceTableArn':'arn:aws:dynamodb:us-east-1:'+account+':table/grc-test-source',
            'SourceBucketName':'grc-test-'+account+'-us-east-1-source','SourceBucketArn':'arn:aws:s3:::grc-test-'+account+'-us-east-1-source',
            'FixtureFunctionName':'grc-test-fixtures','ControllerFunctionName':'grc-test-controller','JanitorFunctionName':'grc-test-janitor',
            'ResultsTableName':'grc-test-results','ReportBucketName':'grc-test-reports','IrBucketName':'grc-test-ir',
            'KeyArn':'arn:aws:kms:us-east-1:'+account+':key/key-id','VaultName':'grc-test-vault',
            'BackupRoleArn':'arn:aws:iam::'+account+':role/grc-test-backup-role',
            'StateMachineArn':'arn:aws:states:us-east-1:'+account+':stateMachine:grc-test-dr',
            'QuarterlyScheduleName':'grc-test-quarterly','FixtureScheduleName':'grc-test-fixture',
            'MonitorRuleName':'grc-test-reconcile','BackupPlanId':'test-plan'}
        self.out['EventBusName']='grc-test-events'
        self.clients['sts'].get_caller_identity.return_value={'Account':account}
        self.clients['cloudformation'].describe_stacks.return_value={'Stacks':[{
            'StackId':'arn:aws:cloudformation:us-east-1:'+account+':stack/grc-test/id',
            'Outputs':[{'OutputKey':k,'OutputValue':v} for k,v in self.out.items()],
            'Parameters':[{'ParameterKey':'EnableFaultInjection','ParameterValue':'true'}]}]}
        original=c.client; self.addCleanup(setattr,c,'client',original)
        self.op=manage.Operator(self.clients,'grc-test',Path(self.temp.name)/'state.json')

    def test_plan_is_offline_and_writes_require_explicit_execution(self):
        with patch.dict('sys.modules',{'boto3':None}),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0,manage.main(['plan']))
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit): manage.main(['exercise'])

    def prepare_inputs(self):
        summary={'count':4,'sha256':'hash'}
        manifest={'schema_version':3,'dynamodb':summary,'s3':summary}
        baseline={'manifest_key':'baseline','manifest_version':'v1','manifest_sha256':c.digest(manifest)}
        self.clients['lambda'].invoke.return_value={'Payload':io.BytesIO(b'{"status":"READY"}')}
        def started(**kwargs):
            kind='s3' if kwargs['ResourceArn'].startswith('arn:aws:s3:') else 'dynamodb'
            self.assertTrue(json.loads(self.op.path.read_text())['backups'][kind]['start_intent'])
            validate_parameters(kwargs,get_session().get_service_model('backup').operation_model('StartBackupJob').input_shape)
            return {'BackupJobId':'job-'+kind}
        self.clients['backup'].start_backup_job.side_effect=started
        def described(BackupJobId):
            kind=BackupJobId.removeprefix('job-')
            return {'State':'COMPLETED','ResourceArn':c.source(kind),'BackupVaultName':self.out['VaultName'],'RecoveryPointArn':'point-'+kind}
        self.clients['backup'].describe_backup_job.side_effect=described
        return summary,manifest,baseline

    def test_prepare_backs_up_both_exact_sources_with_valid_requests(self):
        summary,manifest,baseline=self.prepare_inputs()
        with patch.object(self.op,'preflight'),patch.object(c,'get',return_value=baseline),patch.object(c,'read_json',return_value=manifest),patch.object(manage.validate,'table_summary',return_value=(summary,{})),patch.object(manage.validate,'bucket_summary',return_value=(summary,{})),contextlib.redirect_stdout(io.StringIO()):
            self.op.prepare()
        self.assertEqual({'dynamodb':'point-dynamodb','s3':'point-s3'},self.op.state['recovery_points'])
        self.assertEqual(2,self.clients['backup'].start_backup_job.call_count)
        self.assertEqual(self.out['FixtureFunctionName'],self.clients['lambda'].invoke.call_args.kwargs['FunctionName'])

    def test_unknown_backup_start_is_not_replayed(self):
        summary,manifest,baseline=self.prepare_inputs()
        self.op.state['backups']={'dynamodb':{'start_intent':'uncertain'}}
        with patch.object(self.op,'preflight'),patch.object(c,'get',return_value=baseline),patch.object(c,'read_json',return_value=manifest),patch.object(manage.validate,'table_summary',return_value=(summary,{})),patch.object(manage.validate,'bucket_summary',return_value=(summary,{})),self.assertRaisesRegex(RuntimeError,'StartUnconfirmed'):
            self.op.prepare()
        self.clients['backup'].start_backup_job.assert_not_called()

    def good_records(self):
        rows=[]
        for label,entry in self.op.state['executions'].items():
            for kind in ['dynamodb'] if label=='forced' else ['dynamodb','s3']:
                run,target=c.identity(entry['arn'],kind)
                rows.append({'execution_arn':entry['arn'],'run_id':run,'target':target,'source_arn':c.source(kind),'kind':kind,
                    'finalized':True,'cleanup_status':'DELETED','validation':{'passed':True},
                    'target_checks':{'component_rto_passed':True,'synthetic_rpo_bound_passed':True},
                    'overall_result':'FAIL' if label=='forced' else 'PASS',
                    'failure_reason':'ForcedValidationFailure' if label=='forced' else None,
                    'delivery':{'event_bus':'ACCEPTED_NOT_DOWNSTREAM_CONFIRMED'}})
        return rows

    def exercise_ready(self):
        self.op.state['recovery_points']={'dynamodb':'point-d','s3':'point-s'}
        self.clients['stepfunctions'].describe_execution.side_effect=[{'status':'SUCCEEDED'},{'status':'FAILED'}]

    def test_positive_covers_both_sources_forced_test_is_one_jira_finding(self):
        self.exercise_ready()
        with patch.object(self.op,'records',side_effect=self.good_records),patch.object(self.op,'assert_absent') as absent,contextlib.redirect_stdout(io.StringIO()): self.op.exercise()
        calls=self.clients['stepfunctions'].start_execution.call_args_list
        self.assertEqual(['dynamodb','s3'],json.loads(calls[0].kwargs['input'])['resource_types'])
        self.assertEqual(['dynamodb'],json.loads(calls[1].kwargs['input'])['resource_types'])
        self.assertEqual(3,absent.call_count)
        self.assertEqual('FAILED',self.op.state['executions']['forced']['actual_status'])

    def test_saved_execution_is_described_without_restarting(self):
        self.exercise_ready()
        self.op.state['executions']={k:{'arn':self.out['StateMachineArn'].replace(':stateMachine:',':execution:')+':'+k,'expected_status':s} for k,s in [('positive','SUCCEEDED'),('forced','FAILED')]}
        with patch.object(self.op,'records',side_effect=self.good_records),patch.object(self.op,'assert_absent'),contextlib.redirect_stdout(io.StringIO()): self.op.exercise()
        self.clients['stepfunctions'].start_execution.assert_not_called()

    def test_other_failure_does_not_prove_fault_injection(self):
        self.exercise_ready()
        def bad():
            rows=self.good_records()
            for r in rows:
                if r['overall_result']=='FAIL': r['failure_reason']='AccessDenied'
            return rows
        with patch.object(self.op,'records',side_effect=bad),patch.object(self.op,'assert_absent'),contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(RuntimeError,'ExerciseEvidence'): self.op.exercise()

    def test_access_denied_never_proves_a_bucket_absent(self):
        self.op.state['executions']={'positive':{'arn':self.out['StateMachineArn'].replace(':stateMachine:',':execution:')+':positive'}}
        row=[r for r in self.good_records() if r['kind']=='s3'][0]
        self.clients['s3'].head_bucket.side_effect=AwsError('AccessDenied')
        with self.assertRaises(AwsError): self.op.assert_absent(row)
        self.clients['s3'].head_bucket.side_effect=AwsError('NoSuchBucket')
        self.op.assert_absent(row)

    def test_teardown_is_never_a_day7_action(self):
        with self.assertRaisesRegex(ValueError,'EndOfProgramAuthorization'):
            self.op.teardown()
        self.clients['cloudformation'].delete_stack.assert_not_called()
        self.clients['backup'].delete_recovery_point.assert_not_called()

    def test_end_teardown_requires_evidence_and_blocks_active_workflows(self):
        self.op.parameters.update(EndOfProgramTeardown='true',QuarterlyScheduleState='DISABLED',FixtureScheduleState='DISABLED',EnableScheduledBackups='false')
        with self.assertRaisesRegex(ValueError,'CollectPrivateEvidence'): self.op.teardown(True)
        self.op.state['acceptance_evidence']={'version':'pinned'}
        self.clients['stepfunctions'].get_paginator.return_value.paginate.return_value=[{'executions':[{'status':'RUNNING'}]}]
        with self.assertRaisesRegex(ValueError,'WorkflowStillActive'): self.op.teardown(True)
        self.clients['cloudformation'].delete_stack.assert_not_called()
        self.clients['lambda'].invoke.assert_not_called()

    def test_status_verifies_running_states_without_requiring_collected_evidence(self):
        self.op.parameters.update(EnableRuntimeResources='true',EnableScheduledBackups='true',QuarterlyScheduleState='ENABLED',FixtureScheduleState='ENABLED',EnableFaultInjection='false',EndOfProgramTeardown='false')
        def schedule(Name):
            target=self.out['StateMachineArn'] if Name==self.out['QuarterlyScheduleName'] else 'arn:aws:lambda:us-east-1:'+self.op.account+':function:'+self.out['FixtureFunctionName']
            return {'State':'ENABLED','ScheduleExpression':'cron(...)','ScheduleExpressionTimezone':'UTC','Target':{'Arn':target}}
        self.clients['scheduler'].get_schedule.side_effect=schedule
        self.clients['events'].describe_rule.return_value={'State':'ENABLED'}
        self.clients['backup'].get_backup_plan.return_value={'BackupPlan':{'Rules':[{}]}}
        self.clients['backup'].list_backup_selections.return_value={'BackupSelectionsList':[{'SelectionName':'grc-test-sources','SelectionId':'selection'}]}
        self.clients['backup'].get_backup_selection.return_value={'BackupSelection':{'Resources':[c.source(k) for k in c.kinds()],'IamRoleArn':self.out['BackupRoleArn']}}
        with contextlib.redirect_stdout(io.StringIO()): self.op.status()
        data=json.loads((self.op.path.parent/'status.json').read_text())
        self.assertEqual('TECHNICAL_STATUS_ONLY',data['status'])
        self.assertIsNone(data['evidence'])
        self.assertIn('KEEP_RUNNING',data['lifecycle'])
        self.clients['cloudformation'].delete_stack.assert_not_called()
        self.clients['lambda'].invoke.assert_not_called()

    def test_status_refuses_disabled_schedule(self):
        self.op.parameters.update(EnableRuntimeResources='true',EnableScheduledBackups='true',QuarterlyScheduleState='ENABLED',FixtureScheduleState='ENABLED',EnableFaultInjection='false',EndOfProgramTeardown='false')
        self.op.state['acceptance_evidence']={'version':'pinned'}
        self.clients['scheduler'].get_schedule.return_value={'State':'DISABLED'}
        with self.assertRaisesRegex(ValueError,'ScheduleDisabled'): self.op.status()

    def test_aws_datetime_evidence_is_normalized_for_hashing(self):
        normalized=manage.json_value({'CreationDate':datetime(2026,10,23,tzinfo=timezone.utc)})
        self.assertEqual('2026-10-23T00:00:00+00:00',normalized['CreationDate'])
        self.assertEqual(c.digest(normalized),c.digest(json.loads(c.compact(normalized))))

    def test_ir_evidence_is_versioned_and_forwarded_without_claiming_downstream_receipt(self):
        self.clients['s3'].put_object.return_value={'VersionId':'pinned'}
        self.clients['events'].put_events.return_value={'FailedEntryCount':0,'Entries':[{'EventId':'accepted'}]}
        receipt=self.op.store_ir_evidence('runbook-executions','execution-id',{'status':'Success'})
        self.assertEqual('pinned',receipt['version'])
        self.assertEqual('EVENT_ACCEPTED_DOWNSTREAM_UNVERIFIED',receipt['delivery'])
        event=self.clients['events'].put_events.call_args.kwargs['Entries'][0]
        self.assertEqual('BCDR Evidence Record',event['DetailType'])
        self.assertEqual('pinned',json.loads(event['Detail'])['evidence']['version'])

    def collected_records(self):
        rows=[]
        for number,kind in enumerate(['dynamodb','s3','dynamodb'],1):
            run=str(number)*24
            rows.append({'run_id':run,'kind':kind,'started_at':'2026-11-01T00:00:00Z',
                         'finalized':True,'cleanup_status':'DELETED','overall_result':'FAIL' if number==3 else 'PASS',
                         'report_key':'dr-tests/2026/Q4/'+kind+'/'+run+'.json',
                         'report_version':'synthetic-version','report_sha256':c.digest({'synthetic':True})})
        return rows

    def test_collection_saves_same_verified_private_bundle_for_offline_index(self):
        self.op.state.update(recovery_points={},backups={})
        self.clients['cloudtrail'].get_paginator.return_value.paginate.return_value=[]
        self.clients['backup'].describe_backup_vault.return_value={}
        self.clients['s3'].get_bucket_versioning.return_value={'Status':'Enabled'}
        self.clients['s3'].get_bucket_encryption.return_value={}
        self.clients['dynamodb'].describe_table.return_value={'Table':{}}
        self.clients['lambda'].get_function_configuration.return_value={'Role':self.out['BackupRoleArn']}
        self.clients['iam'].get_role.return_value={'Role':{}}
        with patch.object(self.op,'records',return_value=self.collected_records()),patch.object(self.op,'assert_absent') as absent,\
                patch.object(c,'read_json',return_value={'synthetic':True}) as read,\
                patch.object(c,'write_json',return_value={'VersionId':'synthetic-collection-version'}) as write,\
                contextlib.redirect_stdout(io.StringIO()):
            self.op.collect()
        private_path=self.op.path.parent/'collected-evidence.json'
        private=json.loads(private_path.read_text())
        self.assertEqual(private,write.call_args.args[2])
        self.assertEqual(self.out['ReportBucketName'],private['report_bucket'])
        self.assertEqual(c.digest(private),self.op.state['acceptance_evidence']['sha256'])
        self.assertEqual(3,absent.call_count)
        self.assertEqual(3,read.call_count)
        self.assertTrue(all(call.args[2]=='synthetic-version' for call in read.call_args_list))
        self.assertEqual(3,len(prepare_06.build_index(private)['records']))
        public=json.loads((self.op.path.parent/'public-summary.json').read_text())
        self.assertNotIn(self.out['ReportBucketName'],json.dumps(public))
        if os.name!='nt': self.assertEqual(0o600,private_path.stat().st_mode & 0o777)

    def test_collection_hash_mismatch_never_stages_unverified_evidence(self):
        with patch.object(self.op,'records',return_value=self.collected_records()),patch.object(self.op,'assert_absent'),\
                patch.object(c,'read_json',return_value={'synthetic':'changed'}),patch.object(c,'write_json') as write,\
                self.assertRaisesRegex(RuntimeError,'ReportHashMismatch'):
            self.op.collect()
        write.assert_not_called()
        self.assertFalse((self.op.path.parent/'collected-evidence.json').exists())

if __name__=='__main__': unittest.main()
