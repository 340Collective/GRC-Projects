"""Read-only Jira/service checks and safe public summaries. Never sends a Jira write."""
import base64
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler


class EvidenceError(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise EvidenceError('RedirectRejected')


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise EvidenceError('TimezoneRequired')
    return result.astimezone(timezone.utc)


def get_json(url, authorization=None, limit=1048576):
    headers = {'Accept': 'application/json'}
    if authorization:
        headers['Authorization'] = authorization
    with build_opener(NoRedirect()).open(Request(url, headers=headers), timeout=30) as response:
        body = response.read(limit + 1)
    if len(body) > limit:
        raise EvidenceError('EvidenceResponseTooLarge')
    return json.loads(body)


def jira_receipt(base, issue_key, actor_id, email, token, record, audit_ref, fetch=get_json):
    if not re.fullmatch(r'https://[a-z0-9][a-z0-9-]*\.atlassian\.net', base):
        raise EvidenceError('ApprovedJiraCloudOriginRequired')
    if not re.fullmatch(r'[A-Z][A-Z0-9_]*-[1-9][0-9]*', issue_key) or not actor_id or not audit_ref:
        raise EvidenceError('IssueActorAndAutomationAuditReferenceRequired')
    if not re.fullmatch(r'[a-f0-9]{24}', record.get('run_id', '')):
        raise EvidenceError('InvalidRunIdentity')
    if record.get('failure_reason') != 'ForcedValidationFailure' or record.get('cleanup_status') != 'DELETED':
        raise EvidenceError('CompletedForcedFailureEvidenceRequired')
    label = 'bcdr-' + record['run_id']
    auth = 'Basic ' + base64.b64encode((email + ':' + token).encode()).decode()
    fields = 'summary,labels,created,creator,project,description'
    issue = fetch(base + '/rest/api/3/issue/' + issue_key + '?' + urlencode({'fields': fields}), auth)
    f = issue['fields']
    if issue.get('key') != issue_key or label not in f.get('labels', []) or f.get('creator', {}).get('accountId') != actor_id:
        raise EvidenceError('JiraIssueCorrelationOrActorMismatch')
    if instant(f['created']) < instant(record['started_at']):
        raise EvidenceError('JiraIssuePredatesTheTest')
    project = issue_key.rsplit('-', 1)[0]
    jql = 'project = "' + project + '" AND labels = "' + label + '"'
    found = fetch(base + '/rest/api/3/search/jql?' + urlencode({'jql': jql, 'maxResults': 2, 'fields': 'key'}), auth)
    if len(found.get('issues', [])) != 1 or found.get('nextPageToken') or found['issues'][0].get('key') != issue_key:
        raise EvidenceError('JiraIssueNotUniqueOrNotYetIndexed')
    # API facts are verified. The audit log reference still needs the assessor's
    # independent review of the received event and successful Create issue step.
    return {'issue_key': issue_key, 'correlation_label': label, 'created_at': f['created'],
            'creator_matched_configured_actor': True, 'unique_matching_issue_observed': True,
            'automation_audit_reference': audit_ref, 'automation_audit_review': 'PENDING_HUMAN_REVIEW',
            'status': 'API_CORRELATED', 'checked_at': datetime.now(timezone.utc).isoformat()}


def service_receipt(spec, fetch=None):
    """Check an owner-approved service endpoint after its documented reconnection."""
    required = ['service', 'url', 'expected_sha256', 'disruption_at', 'recoverable_data_at',
                'data_timestamp_evidence', 'source_revision', 'configuration_revision',
                'dependency_evidence', 'usability_check_evidence', 'approval_reference', 'rto_seconds', 'rpo_seconds']
    if any(not spec.get(k) for k in required) or spec['service'] not in {'website', 'client-data'}:
        raise EvidenceError('CompleteApprovedServiceInventoryAndEvidenceRequired')
    if not spec['url'].startswith('https://') or not re.fullmatch('[a-f0-9]{64}', spec['expected_sha256']):
        raise EvidenceError('ApprovedHttpsEndpointAndHashRequired')
    if fetch is None:
        def fetch(url):
            with build_opener(NoRedirect()).open(Request(url, headers={'User-Agent': 'BCDR-read-only-check'}), timeout=30) as response:
                data = response.read(1048577)
                status = response.status
            if len(data) > 1048576:
                raise EvidenceError('ServiceProbeTooLarge')
            return status, data, datetime.now(timezone.utc)
    status, body, usable = fetch(spec['url'])
    disruption, recovered = instant(spec['disruption_at']), instant(spec['recoverable_data_at'])
    if not recovered <= disruption <= usable:
        raise EvidenceError('InvalidServiceRecoveryTimeline')
    if status != 200 or hashlib.sha256(body).hexdigest() != spec['expected_sha256']:
        raise EvidenceError('ServiceContentCheckFailed')
    rto, rpo = math.ceil((usable - disruption).total_seconds()), math.ceil((disruption - recovered).total_seconds())
    if type(spec['rto_seconds']) is not int or type(spec['rpo_seconds']) is not int or min(spec['rto_seconds'], spec['rpo_seconds']) < 1:
        raise EvidenceError('AcceptedPositiveTargetsRequired')
    return {'service': spec['service'], 'http_and_content': 'PASS', 'usable_at': usable.isoformat(),
            'disruption_at': spec['disruption_at'], 'recoverable_data_at': spec['recoverable_data_at'],
            'rto_seconds': rto, 'rpo_seconds': rpo,
            'target_checks': {'rto': rto <= spec['rto_seconds'], 'rpo': rpo <= spec['rpo_seconds']},
            'rto_target': spec['rto_seconds'], 'rpo_target': spec['rpo_seconds'],
            'source_revision': spec['source_revision'], 'configuration_revision': spec['configuration_revision'],
            'owner_supplied_evidence': {k: spec[k] for k in ['data_timestamp_evidence', 'dependency_evidence', 'usability_check_evidence', 'approval_reference']},
            'status': 'HTTP_CONFIRMED_OWNER_EVIDENCE_REVIEW_PENDING'}


def public_summary(record):
    # An allowlist deliberately excludes ARNs, resource names, URLs, contacts,
    # Jira keys, raw audit logs and record contents.
    keys = ['scope', 'kind', 'result', 'overall_result', 'cleanup_status', 'started_at', 'validated_at',
            'rto_target', 'rto_achieved', 'rpo_target', 'rpo_achieved', 'rpo_measure',
            'target_checks', 'service_recovery', 'website_recovery', 'report_sha256']
    result = {k: record.get(k) for k in keys}
    result['integrity_passed'] = record.get('validation', {}).get('passed')
    for name in ['expected', 'actual']:
        value = record.get('validation', {}).get(name, {})
        result[name + '_summary'] = {k: value.get(k) for k in ['count', 'sha256']}
    result['partner_assessment'] = 'PENDING'
    result['final_project_approval'] = 'PENDING'
    return result


def validate_tabletop(record):
    fields = ['Incident ID','Date Detected','Reporter','Severity','Systems Affected','Timeline',
              'Root Cause','Actions Taken','Lessons Learned','Follow-Up Owner']
    if record.get('record_type') != 'ACTUAL_TABLETOP' or record.get('actual_exercise_attested') is not True:
        raise EvidenceError('ActualTabletopAttestationRequired')
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',record.get('exercise_id','')):
        raise EvidenceError('SafeExerciseIdentityRequired')
    for field in fields:
        value = record.get('incident_report',{}).get(field)
        if not isinstance(value,str) or not value.strip() or value.upper().startswith(('REPLACE','PENDING')):
            raise EvidenceError('CompletedIncidentReportRequired')
    if (instant(record['ended_at']) - instant(record['started_at'])).total_seconds() < 3600:
        raise EvidenceError('SixtyMinuteTabletopRequired')
    if not record.get('roles') or not record.get('decisions') or not record.get('ir_lead_signoff_reference'):
        raise EvidenceError('TabletopParticipantsDecisionsAndSignoffRequired')
    # Input attestation and references are not independent proof of conduct.
    return 'ATTESTED_RECORD_REQUIRES_INDEPENDENT_REVIEW'
