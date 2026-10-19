# Audit Engagement Manager Architecture

## Purpose

Run an audit engagement without a spreadsheet of requests and a mailbox of attachments. Every PBC request has an owner and a due date, every upload marks its request received, every finding follows the same remediation path to closure, and nothing goes overdue without a reminder. Stakeholders get one weekly status report instead of ad hoc questions.

## Scope and frameworks

- SOC 2 and ISO 27001:2022 external audit support: PBC lists, evidence delivery, and management responses.
- ISO 27001:2022 clause 9.2 (internal audit) and clause 10.2 (nonconformity and corrective action).
- NIST CSF 2.0 ID.IM: improvements identified from assessments and audits.
- Control areas: request tracking, evidence intake and custody, finding lifecycle, remediation validation, SLA reminders, and status reporting.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Intake | Cognito, API Gateway, Lambda | The auditor signs in and creates PBC requests and findings through the portal |
| Processing | S3, Lambda (intake marker), KMS | Owners upload evidence; the upload event marks the request received |
| State | DynamoDB (PBC requests, findings), Step Functions | Requests and findings are stored; each finding moves through its remediation states |
| Orchestration | EventBridge Scheduler, Lambda, SES | A daily reminder emails owners about overdue requests and findings |
| Outputs | Lambda (status report), S3, CloudWatch | A weekly status report goes to S3 and to stakeholders; alarms on failures |

## Stage details

### Intake

- Cognito user pool with two groups: `auditors` (create requests and findings, read evidence) and `stakeholders` (read status). Control owners sign in to upload only.
- API Gateway uses the Cognito authorizer on every route. The portal handler Lambda checks the caller's group before every write.
- Creating a PBC request writes the request, owner, due date, and `open` status.

### Processing

- The portal returns a short-lived presigned upload URL scoped to `engagement/<id>/pbc/<request>/`. Nothing else in the bucket is writable.
- An S3 `ObjectCreated` event runs the intake marker, which sets the request to `received`, records the object key and checksum, and notifies the auditor.
- Evidence is encrypted with the evidence key, and the checksum recorded at intake makes any later change detectable. There is no Object Lock; engagement evidence is temporary: it is kept until the final-week teardown, then deleted.

### State

- The PBC table tracks `open`, `received`, `accepted`, or `rejected` per request. A rejected request returns to `open` with the auditor's note.
- Each finding starts a Step Functions execution with the remediation path: `open`, `remediation_planned` (owner submits a plan, engagement owner approves), `remediated` (owner submits proof), `validated` (auditor retests), `closed`.
- Each state change is written to the findings table, so the full history is kept.

### Orchestration

- EventBridge Scheduler runs the reminder Lambda daily. It reads requests past their due date and findings past their state SLA.
- SES emails each owner a list of their overdue items with links to the portal. Emails carry IDs and titles only, no evidence content.
- Items still overdue after a set number of reminders are flagged for the engagement owner.

### Outputs

- A weekly schedule runs the status report Lambda: requests by status, findings by state, overdue counts, and items closed this week.
- The report is written to S3 and emailed to the stakeholders group.
- CloudWatch alarms on failed state machine executions, reminder errors, and upload failures.

## Data model

DynamoDB table `pbc_requests`:

- Partition key `engagement_id`, sort key `request_id`.
- Attributes: `title`, `control_refs`, `owner`, `due_date`, `status`, `evidence_keys`, `auditor_note`, `updated_at`.
- GSI on `owner` and `due_date` for overdue queries.

DynamoDB table `findings`:

- Partition key `engagement_id`, sort key `finding_id#version`.
- Attributes: `title`, `severity`, `control_refs`, `state`, `owner`, `plan`, `plan_approved_by`, `validated_by`, `state_due`, `execution_id`.

S3 prefixes:

- `engagement/<id>/pbc/<request>/` for evidence uploads.
- `engagement/<id>/findings/<finding-id>/` for remediation proof.
- `status/<engagement-id>/<yyyy>/<mm>/<dd>/` for weekly reports.

## Security and privacy controls

- KMS customer managed key for the evidence bucket, both tables, and the status reports.
- One IAM role per Lambda: the intake marker can update request status only; the reminder can read both tables and send email only.
- Cognito authorizer on every portal route; auditors have read-only evidence access.
- CloudTrail data events on the evidence bucket, so every read and upload is attributable.
- No evidence content or personal data in logs.
- Human approval points: the 340 Collective owner, as engagement owner, approves each remediation plan; the auditor validates each remediation before a finding closes.

## 340 Collective testbed

340 Collective's real AWS account hosts a mock audit engagement against itself. The [09 Control Testing](../Rasheed-09-Control-Testing/README.md) workpapers are the auditor's starting point, and 340 Collective's real evidence answers the PBC list. Validation means every request ends accepted, every finding reaches closed through the full path, and the weekly report matches the tables.

## Cost note

Costs stay near zero: API Gateway, Lambda, Step Functions, Cognito, DynamoDB, S3, and SES are serverless and low volume at one engagement at a time. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Evidence bucket, KMS key, and the PBC and findings tables.
2. Cognito user pool, groups, and the portal API with the handler.
3. Presigned upload and the intake marker.
4. Finding state machine with the approval and validation steps.
5. Daily reminder through SES, then the weekly status report.
6. CloudWatch alarms.

## Related projects

- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
- [07 Risk Register](../Rasheed-07-Risk-Register/README.md)
- [09 Control Testing and Assessment](../Rasheed-09-Control-Testing/README.md)
- [12 GRC Metrics and Board Reporting](../Rasheed-12-Metrics-Reporting/README.md)
