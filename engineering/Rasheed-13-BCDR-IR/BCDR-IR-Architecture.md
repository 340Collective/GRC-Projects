# BC/DR and Incident Response Compliance Architecture

## Purpose

Auditors do not accept "we have backups" or "we have an IR plan". They ask for proof that a restore worked within the recovery targets and that the response process was exercised. This project produces that proof on a schedule: a quarterly restore test with measured RTO and RPO, a kept record of every runbook and tabletop, and an automatic finding whenever a test fails or runs late.

## Scope and frameworks

- SOC 2 (2017 TSC) A1.2 (backup and recovery infrastructure), A1.3 (recovery plan testing), CC7.4 (incident response), and CC7.5 (recovery from incidents).
- ISO 27001:2022 Annex A 5.24 to 5.30: incident management planning, assessment, response, learning, evidence collection, security during disruption, and ICT readiness for business continuity.
- NIST CSF 2.0 RS (Respond) and RC (Recover).
- Control areas: backup coverage, restore testing, RTO and RPO targets and evidence, IR runbooks, tabletop exercises, and corrective action.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | AWS Backup, DynamoDB, S3 | Backup plans create recovery points for the protected tables and data |
| Processing | EventBridge Scheduler, Step Functions, Lambda (restore validator) | A quarterly DR test restores into an isolated target and validates it |
| State | DynamoDB (results), S3 (reports) | Achieved RTO and RPO and pass or fail are recorded against targets |
| Orchestration | EventBridge, Systems Manager Automation, S3 | Failed or late tests raise findings; IR runbooks and tabletop records are kept |
| Outputs | DynamoDB (07 risk register), S3 (06 evidence lake), CloudWatch | Findings reach the register, results reach the evidence lake, alarms on failures |

## Stage details

### Producers

- AWS Backup plans cover the DynamoDB tables and S3 data, with a backup vault encrypted by the backup key. There is no vault lock; recovery points expire and are deleted at teardown.
- Each resource carries an RPO target (for example 24 hours) and an RTO target (for example 4 hours), approved by the 340 Collective owner.

### Processing

- EventBridge Scheduler starts the DR test state machine each quarter (and on demand).
- Step Functions picks the latest recovery point per protected resource and calls `StartRestoreJob` into an isolated test target: a new table name or a separate test bucket, never the live resource.
- It waits for the restore job, records start and end times, then calls the restore validator Lambda.
- The validator compares row or object counts and checksums of a known sample against the source, and checks the recovery point age.
- The workflow always ends by deleting the test target, including on failure (a catch path runs the cleanup).

### State

- Achieved RTO is the restore job duration; achieved RPO is the age of the recovery point used. Both are compared with targets.
- The result (pass, fail, late) and the measurements are written to the results table, and a test report is written to S3.
- The IR lead signs off each quarterly result.

### Orchestration

- A failed, late, or skipped test emits an EventBridge event with the resource, targets, measurements, and reason.
- Rules route that event to the [07 risk register](../Rasheed-07-Risk-Register/README.md) (a new or updated risk) and to the [06 evidence lake](../Maria-06-Evidence-Automation/README.md) (the test record, pass or fail).
- IR runbooks are Systems Manager Automation documents (for example isolate an instance, rotate a credential, snapshot for forensics). Every execution is logged.
- Tabletop exercise records (scenario, attendees by role, decisions, gaps, and actions) are stored in S3 and signed off by the IR lead.

### Outputs

- The risk register entry carries the owner and a review date, so the gap gets the same SLA timer as any other risk.
- The evidence lake holds every DR test result and tabletop record for audit, matching SOC 2 A1.3 and ISO 27001 A.5.30.
- CloudWatch alarms on failed restore jobs, overdue tests, and failed cleanup.

## Data model

DynamoDB table `dr_test_results`:

- Partition key `resource_id`, sort key `test_date`.
- Attributes: `recovery_point`, `rto_target`, `rto_achieved`, `rpo_target`, `rpo_achieved`, `validation` (counts, checksums), `result`, `signed_off_by`, `report_key`, `cleanup_status`.

S3 prefixes:

- `dr-tests/<yyyy>/<quarter>/<resource-id>/` for test reports.
- `ir/tabletop/<yyyy>/<mm>/<exercise-id>/` for tabletop records.
- `ir/runbook-executions/<yyyy>/<mm>/<dd>/` for runbook execution logs.

## Security and privacy controls

- KMS customer managed keys for the backup vault, the results table, and the report and tabletop buckets.
- No vault lock; recovery points expire on the backup plan lifecycle and are deleted at teardown.
- One IAM role per component: the DR test role can restore only into the test target naming pattern and can delete only test targets; it has no write access to live tables or buckets.
- The restore validator reads counts and checksums only and never logs record content.
- CloudTrail records every restore, deletion, and runbook execution.
- Human approval points: the 340 Collective owner approves RTO and RPO targets; the IR lead signs off each DR test result and tabletop record; destructive IR runbook steps require approval in Systems Manager.

## 340 Collective testbed

340 Collective's own backup, DR, and IR process is the testbed: its DynamoDB tables and S3 data are the protected resources, and its incident response process is the tabletop subject. Validation means each quarter produces a pass or fail with measured RTO and RPO, a deleted test target, a report in S3, and, for any failure, an entry in the risk register.

## Cost note

The main cost drivers are AWS Backup storage and restores, and the temporary restored copies while a test runs. Keep restores small (a representative table or prefix) and delete them at the end of each test. Step Functions, Lambda, EventBridge, Systems Manager Automation, and DynamoDB stay near the free tier at quarterly frequency. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Backup plans, vault (no vault lock; recovery points expire and are deleted at teardown), and the RTO and RPO targets per resource.
2. Results table and report bucket.
3. DR test state machine with restore, timing, and guaranteed cleanup, tested on one table.
4. Restore validator and the comparison with targets.
5. EventBridge finding routing to 07 and 06, and CloudWatch alarms.
6. IR runbooks in Systems Manager and the tabletop record template.

## Related projects

- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
- [07 Risk Register](../Rasheed-07-Risk-Register/README.md)
- [10 Audit Engagement Manager](../Maria-10-Audit-Engagement-Manager/README.md)
- [12 GRC Metrics and Board Reporting](../Rasheed-12-Metrics-Reporting/README.md)
