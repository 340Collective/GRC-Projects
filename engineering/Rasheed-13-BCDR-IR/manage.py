#!/usr/bin/env python3
"""One entry point for local build, approved lab operation and evidence collection."""
import argparse
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from bcdr import common as c, validate
import evidence


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    with open(temporary, 'w', encoding='utf-8') as f:
        if os.name != 'nt':
            os.chmod(temporary, 0o600)
        json.dump(value, f, indent=2, default=str)
    os.replace(temporary, path)


def json_value(value):
    return json.loads(json.dumps(value, default=lambda item: item.isoformat()
                                 if isinstance(item, datetime) else str(item)))


def wait(read, done, seconds=10860):
    deadline = time.monotonic() + seconds
    while True:
        value = read()
        if done(value):
            return value
        if time.monotonic() >= deadline:
            raise RuntimeError('LocalWaitExpiredCloudWorkflowAndReconcilerContinue')
        time.sleep(20)


class Operator:
    def __init__(self, clients, stack, state):
        self.clients, self.stack, self.path = clients, stack, Path(state)
        if not re.fullmatch(r'grc-[a-z0-9-]+', stack):
            raise ValueError('GrcStackRequired')
        data = clients['cloudformation'].describe_stacks(StackName=stack)['Stacks'][0]
        self.out = {o['OutputKey']: o['OutputValue'] for o in data.get('Outputs', [])}
        self.parameters = {p['ParameterKey']: p['ParameterValue'] for p in data.get('Parameters', [])}
        account = clients['sts'].get_caller_identity()['Account']
        if data['StackId'].split(':')[3:5] != ['us-east-1', account]:
            raise ValueError('WrongAccountOrRegion')
        if not {'SourceTableName', 'SourceBucketName', 'FixtureFunctionName', 'ControllerFunctionName', 'JanitorFunctionName', 'ResultsTableName'}.issubset(self.out):
            raise ValueError('RuntimeOffOrWrongTemplate')
        self.prefix = self.out['SourceTableName'].removesuffix('-source')
        if not re.fullmatch(r'grc-[a-z0-9-]{1,12}', self.prefix) or self.out['SourceTableArn'] != 'arn:aws:dynamodb:us-east-1:' + account + ':table/' + self.prefix + '-source':
            raise ValueError('SourceOwnershipMismatch')
        self.stack_id = data['StackId']
        self.account = account
        if self.out['SourceBucketName'] != self.prefix + '-' + account + '-us-east-1-source':
            raise ValueError('SourceBucketOwnershipMismatch')
        if not self.out['KeyArn'].startswith('arn:aws:kms:us-east-1:' + account + ':key/'):
            raise ValueError('SharedKeyMustBeInThisAccountAndRegion')
        os.environ.update({'PREFIX': self.prefix, 'PARTITION': 'aws', 'ACCOUNT_ID': account, 'AWS_REGION': 'us-east-1',
            'SOURCE_TABLE': self.out['SourceTableName'], 'SOURCE_TABLE_ARN': self.out['SourceTableArn'], 'SOURCE_BUCKET': self.out['SourceBucketName'],
            'RESULTS_TABLE': self.out['ResultsTableName'], 'REPORT_BUCKET': self.out['ReportBucketName'],
            'IR_BUCKET': self.out['IrBucketName'], 'KEY_ARN': self.out['KeyArn'], 'INCLUDE_S3': 'true'})
        c.client = lambda service: clients[service]
        self.state = json.loads(self.path.read_text()) if self.path.exists() else {
            'setup_id': uuid4().hex, 'stack_id': self.stack_id, 'created_at': c.iso(), 'executions': {}}
        if self.state['stack_id'] != self.stack_id:
            raise ValueError('SavedStateBelongsToAnotherStack')

    def checkpoint(self, **values):
        self.state.update(values)
        save(self.path, self.state)

    def preflight(self):
        d = self.clients['dynamodb'].describe_table(TableName=self.out['SourceTableName'])['Table']
        if d.get('SSEDescription', {}).get('KMSMasterKeyArn') != self.out['KeyArn'] or d.get('TableStatus') != 'ACTIVE':
            raise ValueError('SourceKeyOrReadinessMismatch')
        if self.clients['s3'].get_bucket_versioning(Bucket=self.out['SourceBucketName'], ExpectedBucketOwner=self.account).get('Status') != 'Enabled':
            raise ValueError('SourceBucketVersioningRequired')
        enc = self.clients['s3'].get_bucket_encryption(Bucket=self.out['SourceBucketName'], ExpectedBucketOwner=self.account)['ServerSideEncryptionConfiguration']['Rules']
        if len(enc) != 1 or enc[0].get('ApplyServerSideEncryptionByDefault') != {'SSEAlgorithm':'aws:kms','KMSMasterKeyID':self.out['KeyArn']}:
            raise ValueError('SourceBucketKeyMismatch')
        settings = self.clients['backup'].describe_region_settings()
        if not settings.get('ResourceTypeOptInPreference', {}).get('DynamoDB') or not settings.get('ResourceTypeManagementPreference', {}).get('DynamoDB'):
            raise ValueError('AdvancedDynamoDbBackupPrerequisiteMissing')
        metadata = self.clients['kms'].describe_key(KeyId=self.out['KeyArn'])['KeyMetadata']
        if metadata.get('KeyState') != 'Enabled' or metadata.get('KeySpec') != 'SYMMETRIC_DEFAULT':
            raise ValueError('ApprovedEnabledSymmetricKeyRequired')
        tags = self.clients['kms'].list_resource_tags(KeyId=self.out['KeyArn']).get('Tags', [])
        if not any(t.get('TagKey') == 'grc-project' and t.get('TagValue') for t in tags):
            raise ValueError('SharedKeyProjectTagRequired')
        connection = self.parameters.get('JiraConnectionArn', '')
        if not connection:
            raise ValueError('RequiredJiraConnectionMissing')
        name = connection.split(':connection/', 1)[-1].split('/')[0]
        if self.clients['events'].describe_connection(Name=name).get('ConnectionState') != 'AUTHORIZED':
            raise ValueError('JiraConnectionNotAuthorized')
        # This is a prerequisite read, not proof that Jira, key grants or SNS delivery work.
        print('Read-only prerequisites passed; effective permissions and delivery require the exercise.')

    def prepare(self):
        self.preflight()
        self.checkpoint()
        if not self.state.get('backups'):
            response = self.clients['lambda'].invoke(FunctionName=self.out['FixtureFunctionName'], InvocationType='RequestResponse',
                Payload=c.compact({'refresh':True, 'refresh_id':self.state['setup_id']}).encode())
            if response.get('FunctionError'):
                raise RuntimeError('FixtureRefreshFailedInspectPrivateLogs')
            seeded = json.loads(response['Payload'].read())
        else:
            seeded = {'status':'ALREADY_READY'}
        if seeded.get('status') not in {'READY', 'ALREADY_READY'}:
            raise RuntimeError('FixtureNotReady')
        baseline = c.get({'resource_id':'#fixture', 'test_date':'v1'})
        manifest = c.read_json(self.out['ReportBucketName'], baseline['manifest_key'], baseline['manifest_version'])
        actual = {'dynamodb':validate.table_summary(self.out['SourceTableName'])[0],
                  's3':validate.bucket_summary(self.out['SourceBucketName'])[0]}
        if manifest.get('schema_version') != 3 or c.digest(manifest) != baseline['manifest_sha256'] or any(actual[k] != manifest[k] for k in c.kinds()):
            raise ValueError('SourceNoLongerMatchesSyntheticBaseline')
        self.state.setdefault('backups', {})
        self.state.setdefault('recovery_points', {})
        for kind in c.kinds():
            entry = self.state['backups'].setdefault(kind, {})
            if not entry.get('job_id'):
                if entry.get('start_intent'):
                    raise RuntimeError('SetupBackupStartUnconfirmedInspectExactAwsJobBeforeRetry')
                entry['start_intent'] = c.iso()
                self.checkpoint()
                response = self.clients['backup'].start_backup_job(BackupVaultName=self.out['VaultName'],
                    ResourceArn=c.source(kind), IamRoleArn=self.out['BackupRoleArn'],
                    IdempotencyToken=self.state['setup_id'] + '-' + kind, StartWindowMinutes=60, CompleteWindowMinutes=180,
                    Lifecycle={'DeleteAfterDays':int(self.parameters.get('BackupRetentionDays','7'))},
                    RecoveryPointTags={'grc-project':'13','bcdr-setup-id':self.state['setup_id']})
                entry['job_id'] = response['BackupJobId']
                self.checkpoint()
            def read_job():
                job = self.clients['backup'].describe_backup_job(BackupJobId=entry['job_id'])
                if job.get('ResourceArn') != c.source(kind) or job.get('BackupVaultName') != self.out['VaultName']:
                    raise ValueError('BackupOwnershipMismatch')
                return job
            result = wait(read_job, lambda j:j['State'] in {'COMPLETED','FAILED','ABORTED','EXPIRED','PARTIAL'},15000)
            if result['State'] != 'COMPLETED':
                raise RuntimeError('BackupNotCompleted')
            self.state['recovery_points'][kind] = result['RecoveryPointArn']
            self.checkpoint(backup_completed_at=c.iso(), baseline_summary=actual)
        print('Both synthetic fixtures and completed backups ready. Source data is synthetic only.')

    def exercise(self):
        if set(self.state.get('recovery_points', {})) != set(c.kinds()):
            raise ValueError('RunPrepareFirst')
        if self.parameters.get('EnableFaultInjection') != 'true':
            raise ValueError('ReviewedFaultInjectionParameterMustBeTrueForTheRequiredExercise')
        for label, forced, expected in [('positive', False, 'SUCCEEDED'), ('forced', True, 'FAILED')]:
            entry = self.state['executions'].get(label)
            if not entry:
                name = 'grc-' + self.state['setup_id'] + '-' + label
                machine = self.out['StateMachineArn']
                arn = machine.replace(':stateMachine:', ':execution:') + ':' + name
                entry = {'arn': arn, 'name': name, 'expected_status': expected, 'start_intent': c.iso()}
                self.state['executions'][label] = entry
                self.checkpoint()
                self.clients['stepfunctions'].start_execution(stateMachineArn=machine, name=name,
                    input=c.compact({'resource_types': ['dynamodb'] if forced else list(c.kinds()), 'force_validation_failure': forced}))
            # A lost start response is recovered by describing the deterministic ARN,
            # never by blindly launching another execution.
            job = wait(lambda: self.clients['stepfunctions'].describe_execution(executionArn=entry['arn']),
                       lambda j: j['status'] in {'SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED'})
            entry['actual_status'] = job['status']
            self.checkpoint()
            if job['status'] != expected:
                raise RuntimeError('UnexpectedWorkflowOutcomeInspectPrivateEvidence')
            requested = {'dynamodb'} if forced else set(c.kinds())
            matches = wait(lambda:[r for r in self.records() if r.get('execution_arn') == entry['arn']],
                           lambda rows:len(rows) == len(requested) and all(r.get('finalized') for r in rows),120)
            if {r.get('kind') for r in matches} != requested:
                raise RuntimeError('ExerciseResourceCoverageMismatch')
            for record in matches:
                if (record.get('cleanup_status') != 'DELETED'
                        or not record.get('validation',{}).get('passed')
                        or not all(record.get('target_checks',{}).get(k) for k in ['component_rto_passed','synthetic_rpo_bound_passed'])
                        or record.get('overall_result') != ('FAIL' if forced else 'PASS')
                        or (forced and record.get('failure_reason') != 'ForcedValidationFailure')
                        or record.get('delivery',{}).get('event_bus') != 'ACCEPTED_NOT_DOWNSTREAM_CONFIRMED'):
                    raise RuntimeError('ExerciseEvidenceDoesNotMatchRequiredOutcome')
                self.assert_absent(record)
            entry['correlation_labels'] = ['bcdr-' + r['run_id'] for r in matches]
            self.checkpoint()
            print(label + ': integrity/targets checked and all targets absent. Jira creation requires separate proof.')

    def assert_absent(self, record):
        target = c.owned(record)
        try:
            if record['kind'] == 'dynamodb':
                self.clients['dynamodb'].describe_table(TableName=target)
            else:
                self.clients['s3'].head_bucket(Bucket=target, ExpectedBucketOwner=self.account)
        except Exception as exc:
            if c.missing(exc):
                return
            raise
        raise RuntimeError('RestoreTargetStillPresent')

    def records(self):
        expected = {e['arn'] for e in self.state['executions'].values()}
        return [r for r in c.records() if r.get('execution_arn') in expected]

    def store_ir_evidence(self, category, identifier, data):
        if category not in {'runbook-executions','tabletop'} or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',identifier):
            raise ValueError('SafeIrEvidenceIdentityRequired')
        normalized = json_value(data)
        event_id = c.digest({'category':category,'id':identifier,'sha256':c.digest(normalized)})

        def prepare():
            key = 'ir/' + category + '/' + c.now().strftime('%Y/%m/%d/') + identifier + '.json'
            version = c.write_json(self.out['ReportBucketName'],key,normalized).get('VersionId')
            if not isinstance(version,str) or not version or version == 'null':
                raise RuntimeError('VersionedIrEvidenceRequired')
            receipt = {'bucket':self.out['ReportBucketName'],'key':key,'version':version,'sha256':c.digest(normalized)}
            detail = {'schema_version':'1.1','event_id':event_id,
                'record_type':category,'scope':'IR_EVIDENCE_REQUIRES_HUMAN_REVIEW','evidence':receipt,'signoff_status':'PENDING'}
            return {'evidence':receipt,'entries':[{'Source':'grc.bcdr','DetailType':'BCDR Evidence Record',
                'EventBusName':self.out['EventBusName'],'Detail':c.compact(detail)}]}

        publication = c.publication(event_id, prepare)
        response = self.clients['events'].put_events(Entries=publication['entries'])
        if response.get('FailedEntryCount') or len(response.get('Entries',[])) != 1:
            raise RuntimeError('IrEvidenceEventRejected')
        return {**publication['evidence'],'delivery':'EVENT_ACCEPTED_DOWNSTREAM_UNVERIFIED'}

    def collect(self, input_path=None):
        inputs = json.loads(Path(input_path).read_text()) if input_path else {}
        records = self.records()
        if len(records) != 3 or not all(r.get('finalized') and r.get('cleanup_status') == 'DELETED' for r in records):
            raise ValueError('ThreeCompletedExerciseRecordsRequired')
        public, private = [], {'collected_at': c.iso(), 'report_bucket': self.out['ReportBucketName'],
                              'records': records, 'jira': 'NOT_VERIFIED', 'services': [], 'ir': []}
        for record in records:
            self.assert_absent(record)
            if not record.get('report_version'):
                raise RuntimeError('VersionPinnedReportNotReady')
            stored = c.read_json(self.out['ReportBucketName'], record['report_key'], record['report_version'])
            if c.digest(stored) != record['report_sha256']:
                raise RuntimeError('ReportHashMismatch')
            public.append(evidence.public_summary(record))
        jira = inputs.get('jira')
        if jira:
            forced = [r for r in records if r.get('force_validation_failure')]
            if len(forced) != 1:
                raise ValueError('ExactlyOneForcedFailureRecordRequired')
            private['jira'] = evidence.jira_receipt(jira['base_url'], jira['issue_key'], jira['expected_actor_id'],
                getpass.getpass('Jira email (not saved): '), getpass.getpass('Existing read-only Jira API token (not saved): '),
                forced[0], jira['automation_audit_reference'])
        for spec in inputs.get('service_recovery', []):
            private['services'].append(evidence.service_receipt(spec))
        for execution_id in inputs.get('ir_execution_ids', []):
            if not re.fullmatch(r'[a-f0-9-]{36}', execution_id):
                raise ValueError('InvalidSsmExecutionId')
            value = self.clients['ssm'].get_automation_execution(AutomationExecutionId=execution_id)['AutomationExecution']
            if value.get('DocumentName') not in {self.out['QuarantineDocument'], self.out['ReleaseDocument']}:
                raise ValueError('UnownedIrRunbook')
            private['ir'].append({'execution':value,'stored_evidence':self.store_ir_evidence('runbook-executions',execution_id,value)})
        if inputs.get('tabletop_record_file'):
            tabletop = json.loads(Path(inputs['tabletop_record_file']).read_text())
            evidence.validate_tabletop(tabletop)
            private['tabletop'] = self.store_ir_evidence('tabletop',tabletop['exercise_id'],tabletop)
        else:
            private['tabletop'] = 'NOT_PROVIDED'
        start = min((c.dt(r['started_at']) for r in records), default=c.now() - timedelta(hours=4))
        events = []
        for page in self.clients['cloudtrail'].get_paginator('lookup_events').paginate(StartTime=start, EndTime=c.now()):
            events.extend(e for e in page.get('Events', []) if e.get('EventName') in {
                'StartRestoreJob', 'DeleteTable', 'DeleteBucket', 'DeleteObject', 'StartAutomationExecution', 'SendAutomationSignal'})
        private['audit_events'] = events
        private['audit_coverage'] = 'LOOKUP_RESULTS_REQUIRE_REVIEW_NOT_PROOF_OF_DATA_EVENT_SELECTORS'
        private['backup_configuration'] = self.clients['backup'].describe_backup_vault(BackupVaultName=self.out['VaultName'])
        private['recovery_point_configuration'] = {kind:self.clients['backup'].describe_recovery_point(
            BackupVaultName=self.out['VaultName'], RecoveryPointArn=point) for kind,point in self.state['recovery_points'].items()}
        private['source_bucket_configuration'] = {
            'versioning':self.clients['s3'].get_bucket_versioning(Bucket=self.out['SourceBucketName'],ExpectedBucketOwner=self.account),
            'encryption':self.clients['s3'].get_bucket_encryption(Bucket=self.out['SourceBucketName'],ExpectedBucketOwner=self.account)}
        private['source_encryption_and_capacity'] = self.clients['dynamodb'].describe_table(TableName=self.out['SourceTableName'])['Table']
        private['runtime_role_evidence'] = []
        for function in [self.out['ControllerFunctionName'], self.out['JanitorFunctionName'], self.prefix + '-validate', self.out['FixtureFunctionName']]:
            info = self.clients['lambda'].get_function_configuration(FunctionName=function)
            role = self.clients['iam'].get_role(RoleName=info['Role'].split('/')[-1])['Role']
            private['runtime_role_evidence'].append({'function_role': info['Role'],
                'permissions_boundary': role.get('PermissionsBoundary'), 'runtime': info.get('Runtime'),
                'memory_mb': info.get('MemorySize'), 'timeout_seconds': info.get('Timeout')})
        private['resource_usage'] = {'backup_jobs': {kind:self.clients['backup'].describe_backup_job(BackupJobId=entry['job_id']) for kind,entry in self.state['backups'].items()},
                                     'workflow_usage': []}
        for entry in self.state['executions'].values():
            history = []
            for page in self.clients['stepfunctions'].get_paginator('get_execution_history').paginate(
                    executionArn=entry['arn'], includeExecutionData=False):
                history.extend(page.get('events', []))
            private['resource_usage']['workflow_usage'].append({'execution': entry['arn'],
                'history_events_observed': len(history),
                'state_entries_observed_not_a_billing_total': sum(e.get('type', '').endswith('StateEntered') for e in history)})
        private['owner_evidence'] = inputs.get('owner_evidence', {})
        # AWS responses contain datetime objects. Normalize once before both
        # storage and hashing so the evidence digest covers the exact JSON value.
        private = json_value(private)
        key = 'acceptance/' + self.state['setup_id'] + '/evidence.json'
        version = c.write_json(self.out['ReportBucketName'], key, private).get('VersionId')
        if not isinstance(version, str) or not version or version == 'null':
            raise RuntimeError('VersionedEvidenceRequired')
        self.checkpoint(acceptance_evidence={'key': key, 'version': version, 'sha256': c.digest(private)})
        save(self.path.parent / 'collected-evidence.json', private)
        save(self.path.parent / 'public-summary.json', {'component_results': public,
            'all_pdf_requirements': 'NOT_ALL_DEMONSTRATED',
            'partner_assessment': 'PENDING', 'validator': 'PENDING', 'final_approval': 'PENDING'})
        save(self.path.parent / 'evidence-index.json', self.state['acceptance_evidence'])
        print('Evidence collected privately. Public summary created. Jira audit, controls, costs, tabletop and acceptance still need independent review.')

    def status(self):
        """Optional read-only configuration check, without a handover gate."""
        required = {'EnableRuntimeResources':'true', 'EnableScheduledBackups':'true',
                    'QuarterlyScheduleState':'ENABLED', 'FixtureScheduleState':'ENABLED',
                    'EnableFaultInjection':'false', 'EndOfProgramTeardown':'false'}
        if any(self.parameters.get(k) != v for k,v in required.items()):
            raise ValueError('RunningConfigurationNotReady')
        schedules = {}
        for output in ['QuarterlyScheduleName','FixtureScheduleName']:
            value = self.clients['scheduler'].get_schedule(Name=self.out[output])
            if value.get('State') != 'ENABLED':
                raise ValueError('RunningScheduleDisabled')
            target = self.out['StateMachineArn'] if output == 'QuarterlyScheduleName' else 'arn:aws:lambda:us-east-1:' + self.account + ':function:' + self.out['FixtureFunctionName']
            if value.get('Target',{}).get('Arn') != target or value.get('ScheduleExpressionTimezone') != 'UTC':
                raise ValueError('RunningScheduleTargetMismatch')
            schedules[output] = {k:value[k] for k in ['State','ScheduleExpression','ScheduleExpressionTimezone']}
        monitor = self.clients['events'].describe_rule(Name=self.out['MonitorRuleName'])
        if monitor.get('State') != 'ENABLED':
            raise ValueError('IndependentMonitorDisabled')
        plan = self.clients['backup'].get_backup_plan(BackupPlanId=self.out['BackupPlanId'])
        if not plan.get('BackupPlan',{}).get('Rules'):
            raise ValueError('RunningBackupPlanMissing')
        selections = [s for s in self.clients['backup'].list_backup_selections(BackupPlanId=self.out['BackupPlanId']).get('BackupSelectionsList',[])
                      if s.get('SelectionName') == self.prefix + '-sources']
        if len(selections) != 1:
            raise ValueError('RunningBackupSelectionMissing')
        selection = self.clients['backup'].get_backup_selection(BackupPlanId=self.out['BackupPlanId'],SelectionId=selections[0]['SelectionId'])['BackupSelection']
        if set(selection.get('Resources',[])) != {c.source(k) for k in c.kinds()} or selection.get('IamRoleArn') != self.out['BackupRoleArn']:
            raise ValueError('RunningBackupSourceCoverageMismatch')
        snapshot = {'checked_at':c.iso(), 'status':'TECHNICAL_STATUS_ONLY',
            'stack_id':self.stack_id, 'schedules':schedules, 'backup_plan':plan, 'backup_selection':selection,
            'evidence':self.state.get('acceptance_evidence'), 'source_scope':list(c.kinds()),
            'project06':'CONFIGURED_UNVERIFIED' if self.parameters.get('EvidenceBusArn') else 'NOT_CONFIGURED',
            'project07':'CONFIGURED_UNVERIFIED' if self.parameters.get('RiskBusArn') else 'NOT_CONFIGURED',
            'lifecycle':'KEEP_RUNNING_UNTIL_AUTHORIZED_END_OF_PROGRAM_TEARDOWN'}
        save(self.path.parent / 'status.json', json_value(snapshot))
        print('Running configuration checked read-only. This optional status check is not acceptance evidence. Keep the stack running.')

    def teardown(self, end_of_program=False):
        # Required order: stop new work, finish writers, verify every target absent,
        # preserve approved evidence, empty only the project vault/buckets, delete CFN.
        if not end_of_program or self.parameters.get('EndOfProgramTeardown') != 'true':
            raise ValueError('EndOfProgramAuthorizationRequiredNotADay7Action')
        if self.parameters.get('QuarterlyScheduleState') != 'DISABLED' or self.parameters.get('EnableScheduledBackups') != 'false' or self.parameters.get('FixtureScheduleState') != 'DISABLED':
            raise ValueError('DisableProjectSchedulesThroughReviewedUpdateFirst')
        if not self.state.get('acceptance_evidence'):
            raise ValueError('CollectPrivateEvidenceBeforeTeardown')
        for page in self.clients['stepfunctions'].get_paginator('list_executions').paginate(
                stateMachineArn=self.out['StateMachineArn'], statusFilter='RUNNING'):
            if page.get('executions'):
                raise ValueError('WorkflowStillActive')
        response = self.clients['lambda'].invoke(FunctionName=self.out['JanitorFunctionName'], InvocationType='RequestResponse', Payload=b'{}')
        if response.get('FunctionError'):
            raise RuntimeError('ReconcilerFailed')
        result = json.loads(response['Payload'].read())
        if result.get('pending') or result.get('errors'):
            raise RuntimeError('UnresolvedCleanupPreventsTeardown')
        for record in c.records():
            if record.get('execution_arn') and (not record.get('finalized') or record.get('cleanup_status') not in {'DELETED', 'NOT_REQUIRED'}):
                raise ValueError('UnresolvedRegisteredRun')
        for page in self.clients['dynamodb'].get_paginator('list_tables').paginate():
            if any(n.startswith(self.prefix + '-restore-') for n in page.get('TableNames', [])):
                raise ValueError('RestoreTargetStillPresent')
        if any(b['Name'].startswith(self.prefix + '-restore-s3-') for b in self.clients['s3'].list_buckets().get('Buckets',[])):
            raise ValueError('RestoreBucketStillPresent')
        lease = self.clients['dynamodb'].get_item(TableName=self.out['ResultsTableName'], Key=c.key({'resource_id':'#fixture-lock','test_date':'v1'}), ConsistentRead=True).get('Item',{})
        if int(lease.get('expires_at',{}).get('N','0')) > int(c.now().timestamp()):
            raise ValueError('FixtureWriterLeaseStillActive')
        for kind in c.kinds():
            for page in self.clients['backup'].get_paginator('list_backup_jobs').paginate(ByResourceArn=c.source(kind)):
                if any(j['State'] not in {'COMPLETED', 'FAILED', 'ABORTED', 'EXPIRED', 'PARTIAL'} for j in page.get('BackupJobs', [])):
                    raise ValueError('BackupWriterStillActive')
        queue = self.clients['sqs'].get_queue_attributes(QueueUrl=self.out['DeadLetterQueueUrl'],
            AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible', 'ApproximateNumberOfMessagesDelayed'])['Attributes']
        if any(int(v) for v in queue.values()):
            raise ValueError('DeliveryQueueNotEmptyReviewAndResolveItFirst')
        for page in self.clients['backup'].get_paginator('list_recovery_points_by_backup_vault').paginate(BackupVaultName=self.out['VaultName']):
            for point in page.get('RecoveryPoints', []):
                if point.get('ResourceArn') not in {c.source(k) for k in c.kinds()}:
                    raise ValueError('UnexpectedRecoveryPoint')
                self.clients['backup'].delete_recovery_point(BackupVaultName=self.out['VaultName'], RecoveryPointArn=point['RecoveryPointArn'])
        wait(lambda: list(self.clients['backup'].get_paginator('list_recovery_points_by_backup_vault').paginate(BackupVaultName=self.out['VaultName'])),
             lambda pages: not any(p.get('RecoveryPoints') for p in pages), 3600)
        for name in [self.out['QuarantineDocument'], self.out['ReleaseDocument']]:
            for page in self.clients['ssm'].get_paginator('describe_automation_executions').paginate(
                    Filters=[{'Key': 'DocumentNamePrefix', 'Values': [name]}]):
                if any(e.get('DocumentName') == name and e.get('AutomationExecutionStatus') not in {'Success', 'Failed', 'TimedOut', 'Cancelled', 'Rejected', 'CompletedWithSuccess', 'CompletedWithFailure'} for e in page.get('AutomationExecutionMetadataList', [])):
                    raise ValueError('IrAutomationStillActive')
        # A quarantine policy must be released through its human approval first.
        policy = self.clients['s3'].get_bucket_policy(Bucket=self.out['IrBucketName'], ExpectedBucketOwner=self.account)['Policy']
        if 'IncidentQuarantineWrites' in policy:
            raise ValueError('ReleaseIrQuarantineWithApprovalBeforeTeardown')
        for bucket in [self.out['SourceBucketName'], self.out['ReportBucketName'], self.out['IrBucketName']]:
            versions = []
            for page in self.clients['s3'].get_paginator('list_object_versions').paginate(Bucket=bucket, ExpectedBucketOwner=self.account):
                versions.extend(page.get('Versions', []) + page.get('DeleteMarkers', []))
            for v in versions:
                self.clients['s3'].delete_object(Bucket=bucket, Key=v['Key'], VersionId=v['VersionId'], ExpectedBucketOwner=self.account)
            left = self.clients['s3'].list_object_versions(Bucket=bucket, ExpectedBucketOwner=self.account, MaxKeys=1)
            if left.get('Versions') or left.get('DeleteMarkers'):
                raise RuntimeError('ProjectBucketNotEmpty')
        self.checkpoint(teardown='READY_FOR_OPERATOR_CLOUDFORMATION_DELETION')
        print('Project backup points and buckets drained. The human operator now deletes the stack with the literal reviewed CLI command from clean main. Shared resources remain outside this operation.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'build', 'check', 'prepare', 'exercise', 'collect', 'status', 'teardown'])
    parser.add_argument('--profile')
    parser.add_argument('--stack', default='grc-bcdr')
    parser.add_argument('--state', default='private/operator.json')
    parser.add_argument('--inputs')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--end-of-program', action='store_true')
    args = parser.parse_args(argv)
    if args.action == 'plan':
        print('DynamoDB and S3 samples, daily backups, quarterly tests, optional 06/07 routing, Jira and IR/tabletop evidence. The live system stays running to programme end.')
        return 0
    if args.action == 'build':
        for script in ['tools/render_template.py', 'tools/build.py']:
            subprocess.run([sys.executable, str(ROOT / script)], check=True)
        return 0
    if args.action not in {'check','status'} and not args.execute:
        parser.error('AWS writes require --execute; plan/build are offline.')
    import boto3
    from botocore.config import Config
    session = boto3.Session(profile_name=args.profile, region_name='us-east-1')
    names = ['cloudformation', 'sts', 'dynamodb', 'backup', 's3', 'kms', 'events', 'iam', 'stepfunctions', 'lambda', 'ssm', 'cloudtrail', 'sqs', 'scheduler']
    clients = {name: session.client(name, config=Config(retries={'mode': 'standard', 'max_attempts': 4})) for name in names}
    op = Operator(clients, args.stack, args.state)
    arguments = [args.inputs] if args.action == 'collect' else [args.end_of_program] if args.action == 'teardown' else []
    getattr(op, 'preflight' if args.action == 'check' else args.action)(*arguments)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (Exception, KeyboardInterrupt) as exc:
        print(c.compact({'status': 'UNRESOLVED', 'error_code': c.error_code(exc),
                        'next': 'Preserve private state; inspect the guide. Cloud reconciliation remains independent.'}))
        raise SystemExit(1)
