# Privacy Operations Architecture

## Purpose

Know where personal data lives, why it is held, and answer every data subject request on time. The design keeps the record of processing activities current from real discovery results instead of a spreadsheet, and it turns DSARs into a tracked workflow with a human approval before anything leaves the account.

## Scope and frameworks

- GDPR Art. 15 (access), 16 (rectification), 17 (erasure), 21 (objection), and 30 (records of processing activities). Response clock: one month.
- CCPA and CPRA: right to know, right to delete, right to opt out of sale or sharing. Response clock: 45 days.
- Control areas: data discovery, data inventory, consent records, request intake, identity verification, fulfillment, and deadline tracking.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | S3, DynamoDB, Lambda (table export), EventBridge Scheduler | Client files and form uploads sit in S3; DynamoDB tables are exported weekly to a staging prefix |
| Processing | Macie, EventBridge, Lambda (inventory updater) | Macie classifies PII; findings flow through EventBridge to the inventory updater |
| State | DynamoDB (data inventory, consent ledger) | RoPA entries and consent choices are stored with timestamps |
| Orchestration | API Gateway, Lambda, Step Functions | Privacy API takes consent and DSARs; the DSAR workflow locates data and waits for approval |
| Outputs | S3 (DSAR packages), SES, CloudWatch, CloudTrail | Approved package is delivered; deadline alarms and an access log back every response |

## Stage details

### Producers

- S3 holds client files and contact form uploads.
- DynamoDB holds newsletter subscribers and invoice records.
- A weekly Scheduler run starts the table export Lambda, which writes items as JSON to `staging/<table>/<yyyy>/<mm>/<dd>/`. Macie cannot read DynamoDB or RDS directly, so this export is the bridge. Staging objects expire after the scan through a lifecycle rule.

### Processing

- Macie runs scoped, sampled discovery jobs over the source buckets and the staging prefix, with managed data identifiers (names, emails, addresses, payment data).
- Findings are published to EventBridge. A rule sends sensitive data findings to the inventory updater Lambda.
- The updater maps each finding to a data category and location and updates the inventory row.

### State

- The data inventory table is the RoPA: one row per data category per location.
- The consent ledger is append only: every opt-in, opt-out, and withdrawal is a new item with a timestamp and source.

### Orchestration

- API Gateway exposes the privacy API with request validation and throttling. Requests require a verified email loop before any data is located, so the API never returns personal data to an unverified caller.
- The consent handler writes the ledger.
- A DSAR starts the Step Functions workflow: verify identity, read the inventory to find every location, run the locate and export Lambda, write the package to S3, then pause on a task token until the privacy owner approves.

### Outputs

- On approval, SES sends the response (a time-limited download link or a deletion confirmation).
- CloudWatch alarms fire at set points before each deadline and when it is missed.
- CloudTrail logs every read of the DSAR package bucket.

## Data model

DynamoDB table `data_inventory`:

- Partition key `data_category`, sort key `location`.
- Attributes: `purpose`, `lawful_basis`, `retention`, `last_seen`, `macie_finding_count`, `owner`.

DynamoDB table `consent_ledger`:

- Partition key `subject_hash`, sort key `timestamp`.
- Attributes: `choice`, `scope`, `source`. The subject is stored as a salted hash, not an email address.

DynamoDB table `dsar_requests`:

- Partition key `request_id`. Attributes: `type`, `received_at`, `due_at`, `status`, `approved_by`.

S3 prefixes: `staging/<table>/<yyyy>/<mm>/<dd>/`, `dsar/<request-id>/`.

## Security and privacy controls

- KMS customer managed key for staging, the inventory, the ledger, and DSAR packages.
- Least-privilege IAM per Lambda; only the locate and export Lambda can read source data.
- CloudTrail data events on the DSAR bucket; packages expire after delivery.
- No PII in logs: functions log request IDs and counts only.
- Human approval points: the privacy owner approves every DSAR release and every deletion.

## 340 Collective testbed

340 Collective's own account holds the real data types in scope: 340collective.com contact form submissions, newsletter subscribers, invoice records, and client files. Validation runs Macie over them, confirms the inventory reflects each category, and runs end-to-end DSARs for synthetic test subjects only. No real person's data is exported during testing.

## Cost note

The main cost driver is Macie, billed per GB scanned and per bucket monitored. Keep jobs sampled and scoped to the buckets that can hold personal data. Lambda, Step Functions, DynamoDB, API Gateway, and SES stay at or near the free tier at 340 Collective's volume. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. KMS key, inventory, ledger, and request tables.
2. Table export Lambda and the staging prefix with a lifecycle rule.
3. Macie jobs and the EventBridge rule to the inventory updater.
4. Privacy API with the consent handler.
5. DSAR Step Functions workflow with the approval pause and SES delivery.
6. Deadline alarms and CloudTrail data events.

## Related projects

- [01 GRC-as-Code Platform](../01-grc-as-code-platform/README.md)
- [02 TPRM/VRM](../02-tprm-vrm/README.md)
- [06 Evidence Automation](../06-evidence-automation/README.md)
