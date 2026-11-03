import copy
from datetime import datetime, timezone
import hashlib
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evidence


class EvidenceTests(unittest.TestCase):
    def jira(self):
        self.record = {'run_id': 'a'*24, 'failure_reason': 'ForcedValidationFailure', 'cleanup_status': 'DELETED',
                       'started_at': '2026-10-23T09:00:00+00:00'}
        self.issue = {'key': 'TEST-1', 'fields': {'labels': ['bcdr-' + 'a'*24], 'creator': {'accountId': 'configured-automation-actor'},
                      'created': '2026-10-23T10:00:00+00:00'}}
        self.results = {'issues': [{'key': 'TEST-1'}], 'isLast': True}
        self.calls = []
        def fetch(url, authorization):
            self.calls.append(url)
            self.assertTrue(authorization.startswith('Basic '))
            return copy.deepcopy(self.results if '/search/jql?' in url else self.issue)
        return fetch

    def receipt(self, fetch):
        return evidence.jira_receipt('https://example.atlassian.net', 'TEST-1', 'configured-automation-actor',
            'synthetic-email', 'synthetic-token', self.record, 'private-audit-record-reference', fetch)

    def test_jira_checks_actual_issue_actor_correlation_and_unique_issue(self):
        fetch = self.jira()
        receipt = self.receipt(fetch)
        self.assertEqual('API_CORRELATED', receipt['status'])
        self.assertEqual('PENDING_HUMAN_REVIEW', receipt['automation_audit_review'])
        self.assertEqual(2, len(self.calls))
        self.assertNotIn('synthetic-token', str(receipt))
        self.assertTrue(any('/search/jql?' in url for url in self.calls))

    def test_human_created_or_unrelated_issue_cannot_confirm_automation(self):
        fetch = self.jira()
        self.issue['fields']['creator']['accountId'] = 'different-actor'
        with self.assertRaises(evidence.EvidenceError):
            self.receipt(fetch)
        self.issue['fields']['creator']['accountId'] = 'configured-automation-actor'
        self.issue['fields']['labels'] = []
        with self.assertRaises(evidence.EvidenceError):
            self.receipt(fetch)

    def test_duplicate_jira_issues_or_stale_issue_are_findings(self):
        fetch = self.jira()
        self.results['issues'].append({'key': 'TEST-2'})
        with self.assertRaises(evidence.EvidenceError):
            self.receipt(fetch)
        self.results['issues'].pop()
        self.issue['fields']['created'] = '2026-10-22T00:00:00+00:00'
        with self.assertRaises(evidence.EvidenceError):
            self.receipt(fetch)

    def spec(self):
        return {'service': 'website', 'url': 'https://example.invalid/approved-smoke-path',
                'expected_sha256': hashlib.sha256(b'approved-content').hexdigest(),
                'disruption_at': '2026-10-23T10:00:00Z', 'recoverable_data_at': '2026-10-23T09:00:00Z',
                'data_timestamp_evidence': 'private-content-manifest', 'source_revision': 'approved-source-revision',
                'configuration_revision': 'approved-configuration', 'dependency_evidence': ['private-identity-dns-checks'],
                'usability_check_evidence': 'private-post-reconnection-check', 'approval_reference': 'accepted-target-reference',
                'rto_seconds': 28800, 'rpo_seconds': 86400}

    def test_service_metrics_use_usability_and_data_time_with_owner_evidence_separate(self):
        receipt = evidence.service_receipt(self.spec(), lambda url: (200, b'approved-content', datetime(2026,10,23,10,10,tzinfo=timezone.utc)))
        self.assertEqual(600, receipt['rto_seconds'])
        self.assertEqual(3600, receipt['rpo_seconds'])
        self.assertTrue(all(receipt['target_checks'].values()))
        self.assertIn('OWNER_EVIDENCE_REVIEW_PENDING', receipt['status'])

    def test_service_missing_inventory_bad_hash_or_future_data_fails_closed(self):
        fetch = lambda url: (200, b'approved-content', datetime(2026,10,23,10,10,tzinfo=timezone.utc))
        spec = self.spec(); spec.pop('source_revision')
        with self.assertRaises(evidence.EvidenceError): evidence.service_receipt(spec, fetch)
        spec = self.spec(); spec['expected_sha256'] = '0'*64
        with self.assertRaises(evidence.EvidenceError): evidence.service_receipt(spec, fetch)
        spec = self.spec(); spec['recoverable_data_at'] = '2026-10-24T00:00:00Z'
        with self.assertRaises(evidence.EvidenceError): evidence.service_receipt(spec, fetch)

    def test_public_summary_excludes_private_identifiers_and_record_contents(self):
        record = {'run_id': 'private-run-id', 'source_arn': 'private-arn', 'report_key': 'private-resource-name',
                  'validation': {'passed': True, 'expected': {'count': 11, 'sha256': 'a'*64, 'contents': 'private-data'},
                                 'actual': {'count': 11, 'sha256': 'a'*64}}}
        summary = evidence.public_summary(record)
        self.assertNotIn('private-', str(summary))
        self.assertEqual('PENDING', summary['partner_assessment'])

    def tabletop(self):
        fields=['Incident ID','Date Detected','Reporter','Severity','Systems Affected','Timeline','Root Cause','Actions Taken','Lessons Learned','Follow-Up Owner']
        return {'record_type':'ACTUAL_TABLETOP','actual_exercise_attested':True,'exercise_id':'unit-test-only',
            'started_at':'2026-10-23T09:00:00Z','ended_at':'2026-10-23T10:00:00Z',
            'roles':['synthetic-role'],'decisions':['synthetic-unit-test-decision'],
            'ir_lead_signoff_reference':'synthetic-unit-test-reference',
            'incident_report':{field:'Synthetic unit-test value' for field in fields}}

    def test_complete_tabletop_form_still_requires_independent_review(self):
        self.assertEqual('ATTESTED_RECORD_REQUIRES_INDEPENDENT_REVIEW',evidence.validate_tabletop(self.tabletop()))

    def test_unattested_tabletop_or_missing_incident_field_cannot_be_imported(self):
        item=self.tabletop();item['actual_exercise_attested']=False
        with self.assertRaises(evidence.EvidenceError): evidence.validate_tabletop(item)
        item=self.tabletop();item['incident_report'].pop('Lessons Learned')
        with self.assertRaises(evidence.EvidenceError): evidence.validate_tabletop(item)

    def test_short_tabletop_or_missing_signoff_remains_incomplete(self):
        item=self.tabletop();item['ended_at']='2026-10-23T09:59:00Z'
        with self.assertRaisesRegex(evidence.EvidenceError,'SixtyMinute'): evidence.validate_tabletop(item)
        item=self.tabletop();item['ir_lead_signoff_reference']=''
        with self.assertRaises(evidence.EvidenceError): evidence.validate_tabletop(item)


if __name__ == '__main__': unittest.main()
