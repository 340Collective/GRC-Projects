"""S3 restore ownership, data checks, cleanup and running-fixture regressions."""
import copy
import io
import json
import os
import unittest
from unittest.mock import patch
from botocore.session import get_session
from botocore.validate import validate_parameters
from test_recovery import RecoveryTests, AwsError, ENV, START, EXECUTION
from bcdr import common as c, cleanup, fixtures, report, restore, validate

# Reuse harness methods without inheriting/duplicating its existing test cases.
class S3Tests(unittest.TestCase):
    setUp=RecoveryTests.setUp
    get=RecoveryTests.get
    put=RecoveryTests.put
    new=RecoveryTests.new
    ready=RecoveryTests.ready

    def test_full_s3_contents_marker_and_encryption_pass(self):
        job=self.ready('s3')
        self.assertTrue(validate.handler({'job':job},None)['passed'])
        row=self.get(job)
        self.assertEqual(4,row['validation']['actual']['count'])
        self.assertEqual(60,row['rpo_achieved'])
        self.assertEqual('NOT_TESTED',row['service_recovery'])

    def test_same_size_changed_object_fails_hash_validation(self):
        job=self.ready('s3')
        original=self.services['s3'].get_object.side_effect
        def changed(**kw):
            value=original(**kw)
            if kw['Key']=='synthetic/sample-00.txt':
                body=value['Body'].read()
                value['Body']=io.BytesIO(bytes([body[0]^1])+body[1:])
            return value
        self.services['s3'].get_object.side_effect=changed
        self.assertFalse(validate.handler({'job':job},None)['passed'])
        self.assertFalse(self.get(job)['validation']['passed'])

    def test_wrong_object_key_is_not_accepted_as_expected_data(self):
        job=self.ready('s3')
        self.services['s3'].get_paginator.return_value.paginate.return_value=[{'Contents':[{'Key':'unexpected','Size':1}]}]
        self.services['s3'].get_object.side_effect=None
        self.services['s3'].get_object.return_value={'Body':io.BytesIO(b'x'),'ServerSideEncryption':'aws:kms','SSEKMSKeyId':ENV['KEY_ARN']}
        with self.assertRaisesRegex(ValueError,'MarkerMissing'): validate.handler({'job':job},None)

    def test_incorrect_object_encryption_cannot_pass(self):
        job=self.ready('s3')
        self.services['s3'].get_object.side_effect=None
        self.services['s3'].get_object.return_value={'Body':io.BytesIO(b''),'ServerSideEncryption':'AES256'}
        with self.assertRaisesRegex(ValueError,'ObjectEncryptionMismatch'): validate.handler({'job':job},None)

    def test_bucket_public_access_or_wrong_tags_fail_closed(self):
        for mode in ['public','tags']:
            with self.subTest(mode=mode):
                job=self.ready('s3')
                if mode=='public': self.services['s3'].get_public_access_block.return_value={'PublicAccessBlockConfiguration':{}}
                else: self.services['s3'].get_bucket_tagging.return_value={'TagSet':[{'Key':'grc-project','Value':'different'}]}
                with self.assertRaises(ValueError): validate.handler({'job':job},None)

    def test_prepare_hardens_bucket_before_restore_and_persists_intent(self):
        job=self.new('s3'); row=self.get(job); row['recovery_point']='test-point'; self.put(row)
        self.services['s3'].head_bucket.side_effect=AwsError('NoSuchBucket')
        def created(**kwargs):
            self.assertTrue(self.get(job)['target_create_intent'])
            self.assertFalse(self.get(job).get('start_intent',False))
            return {}
        self.services['s3'].create_bucket.side_effect=created
        def started(**kwargs):
            saved=self.get(job)
            self.assertTrue(saved['target_prepared']); self.assertTrue(saved['start_intent'])
            validate_parameters(kwargs,get_session().get_service_model('backup').operation_model('StartRestoreJob').input_shape)
            self.assertEqual('S3',kwargs['ResourceType'])
            self.assertEqual(row['target'],kwargs['Metadata']['DestinationBucketName'])
            self.assertEqual('SSE-KMS',kwargs['Metadata']['EncryptionType'])
            self.services['s3'].put_public_access_block.assert_called_once()
            self.services['s3'].put_bucket_versioning.assert_called_once()
            self.services['s3'].put_bucket_policy.assert_called_once()
            return {'RestoreJobId':'test-job'}
        self.services['backup'].start_restore_job.side_effect=started
        self.assertTrue(restore.handler({'action':'start','job':job},None)['started'])

    def test_existing_bucket_is_never_adopted(self):
        job=self.new('s3'); row=self.get(job); row['recovery_point']='point'; self.put(row)
        self.services['s3'].head_bucket.return_value={}
        with self.assertRaisesRegex(ValueError,'DestinationAlreadyExists'): restore.handler({'action':'start','job':job},None)
        self.services['s3'].create_bucket.assert_not_called()
        self.services['backup'].start_restore_job.assert_not_called()

    def test_uncertain_bucket_creation_is_not_replayed_or_deleted(self):
        job=self.new('s3'); row=self.get(job)
        row.update(recovery_point='point',target_create_intent=True,cleanup_status='PENDING'); self.put(row)
        self.services['s3'].get_bucket_tagging.side_effect=AwsError('NoSuchTagSet')
        with self.assertRaises(AwsError): restore.handler({'action':'start','job':job},None)
        self.services['s3'].create_bucket.assert_not_called()
        with self.assertRaises(AwsError): cleanup.handler({'job':job},None)
        self.services['s3'].delete_bucket.assert_not_called()
        self.assertEqual('FAILED',self.get(job)['cleanup_status'])

    def test_lost_s3_restore_start_uses_exact_job_metadata_without_replay(self):
        job=self.ready('s3'); row=self.get(job); row.pop('restore_job_id'); self.put(row)
        self.services['backup'].get_paginator.return_value.paginate.return_value=[{'RestoreJobs':[{'RestoreJobId':'recovered-s3','RecoveryPointArn':'test-point'}]}]
        self.assertTrue(restore.handler({'action':'start','job':job},None)['started'])
        self.assertEqual('recovered-s3',self.get(job)['restore_job_id'])
        self.services['backup'].start_restore_job.assert_not_called()
        self.services['s3'].create_bucket.assert_not_called()

    def test_cleanup_waits_for_writer_and_rejects_wrong_destination(self):
        job=self.ready('s3')
        self.services['backup'].describe_restore_job.return_value={'Status':'RUNNING'}
        self.assertFalse(cleanup.handler({'job':job},None)['done'])
        self.services['s3'].delete_bucket.assert_not_called()
        self.services['backup'].describe_restore_job.return_value={'Status':'COMPLETED','RecoveryPointArn':'test-point'}
        self.services['backup'].get_restore_job_metadata.return_value={'Metadata':{'DestinationBucketName':'wrong'}}
        with self.assertRaisesRegex(ValueError,'OwnershipMismatch'): cleanup.handler({'job':job},None)
        self.services['s3'].delete_bucket.assert_not_called()

    def test_cleanup_removes_versions_and_markers_then_proves_bucket_absent(self):
        job=self.ready('s3')
        self.services['s3'].get_paginator.return_value.paginate.return_value=[{'Versions':[{'Key':'file','VersionId':'v1'},{'Key':'file','VersionId':'v2'}],'DeleteMarkers':[{'Key':'old','VersionId':'marker'}]}]
        self.services['s3'].head_bucket.side_effect=AwsError('NoSuchBucket')
        self.assertTrue(cleanup.handler({'job':job},None)['done'])
        self.assertEqual(3,self.services['s3'].delete_object.call_count)
        self.services['s3'].delete_bucket.assert_called_once()
        self.assertEqual('DELETED',self.get(job)['cleanup_status'])

    def test_cleanup_access_denied_remains_failed_not_deleted(self):
        job=self.ready('s3')
        self.services['s3'].get_bucket_tagging.side_effect=AwsError('AccessDenied')
        with self.assertRaises(AwsError): cleanup.handler({'job':job},None)
        self.assertEqual('FAILED',self.get(job)['cleanup_status'])
        self.services['s3'].delete_bucket.assert_not_called()

    def test_s3_validation_cleanup_and_report_end_to_end_simulation(self):
        job=self.ready('s3')
        self.assertTrue(validate.handler({'job':job},None)['passed'])
        self.services['s3'].get_paginator.return_value.paginate.return_value=[{'Versions':[],'DeleteMarkers':[]}]
        self.services['s3'].head_bucket.side_effect=AwsError('NoSuchBucket')
        self.assertTrue(cleanup.handler({'job':job},None)['done'])
        self.services['events'].put_events.return_value={'FailedEntryCount':0,'Entries':[{'EventId':'test'}]}
        self.assertTrue(report.handler({'job':job},None)['passed'])
        self.assertTrue(self.get(job)['finalized'])

    def test_refresh_does_not_write_sources_while_a_dr_run_is_unfinished(self):
        self.new('dynamodb')
        with self.assertRaisesRegex(RuntimeError,'RefreshBlocked'): fixtures.handler({'refresh':True},None)
        self.assertFalse(any(call.kwargs['TableName']==ENV['SOURCE_TABLE'] for call in self.services['dynamodb'].put_item.call_args_list))
        self.services['s3'].put_object.assert_not_called()

    def test_refresh_replay_is_idempotent_for_its_schedule_id(self):
        self.assertEqual('READY',fixtures.handler({'refresh':True,'refresh_id':'schedule-instant'},None)['status'])
        before=self.services['s3'].put_object.call_count
        self.assertEqual('ALREADY_READY',fixtures.handler({'refresh':True,'refresh_id':'schedule-instant'},None)['status'])
        self.assertEqual(before,self.services['s3'].put_object.call_count)

    def test_fixture_lease_contention_prevents_registration_and_source_writes(self):
        self.services['dynamodb'].put_item.side_effect=AwsError('ConditionalCheckFailedException')
        with self.assertRaises(AwsError): self.new('s3')
        self.assertEqual({},self.stack)
        self.services['s3'].create_bucket.assert_not_called()

    def test_healthy_custom_counters_do_not_create_metric_or_api_usage(self):
        c.metric('CleanupPending',0)
        self.services['cloudwatch'].put_metric_data.assert_not_called()
        c.metric('CleanupPending',1)
        self.services['cloudwatch'].put_metric_data.assert_called_once()
        self.assertEqual(1,self.services['cloudwatch'].put_metric_data.call_args.kwargs['MetricData'][0]['Value'])

    def test_source_drift_is_not_hidden_by_fixture_refresh(self):
        control={'resource_id':'#fixture','test_date':'v1','ready_at':'2026-10-01T00:00:00Z',
                 'manifest_key':'baseline','manifest_version':'v1','manifest_sha256':c.digest({'dynamodb':{'count':11,'sha256':'expected'}}),'refresh_id':'old'}
        self.put(control)
        previous={'dynamodb':{'count':11,'sha256':'expected'}}
        with patch.object(c,'read_json',return_value=previous),patch.object(validate,'table_summary',return_value=({'count':11,'sha256':'changed'},{})),self.assertRaisesRegex(ValueError,'SourceDrift'):
            fixtures.handler({'refresh':True,'refresh_id':'new'},None)
        self.assertEqual(control,self.get(control))
        self.services['s3'].put_object.assert_not_called()

# Avoid collecting the harness subclass and imported TestCase as duplicate suites.
del RecoveryTests

if __name__=='__main__': unittest.main()
