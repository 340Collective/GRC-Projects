# Audit Evidence Automation Architecture

## Purpose

Replace screenshot-driven audit prep with evidence that collects itself. Every object is timestamped and hashed (SHA-256, listed in a manifest), so an auditor can check it was not changed, and every object is mapped to the controls it supports, so the question "show me evidence for this control" has a query, not a scramble.

## Scope and frameworks

- Any framework loaded in Audit Manager or Security Hub, starting with SOC 2, NIST 800-53, and ISO 27001 (the same set as 01).
- Control areas: configuration management, logging and monitoring, access control, and change management evidence.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | AWS Config, Audit Manager, Security Hub CSPM, CloudTrail | Configuration snapshots, assessment evidence, control status, and API activity |
| Processing | EventBridge Scheduler, EventBridge, Lambda (collector) | Daily and on-change runs pull, hash, and timestamp evidence |
| State | S3 evidence lake (versioned, no Object Lock), DynamoDB (control map) | Tamper-evident (hashed), temporary evidence objects and the control-to-evidence index |
| Orchestration | Lambda (mapper, package builder), Glue Data Catalog | Evidence is mapped to controls, cataloged, and bundled per audit |
| Outputs | Athena, S3 (audit packages), CloudWatch, SNS | Auditor queries and packages; freshness alarms alert the owner |

## Stage details

### Producers

- Config delivers configuration snapshots and compliance history.
- Security Hub CSPM reports control status per standard and feeds Config results into Audit Manager.
- Audit Manager assessments collect automated evidence per framework control.
- CloudTrail activity supports change management and access evidence.

### Processing

- EventBridge Scheduler runs the collector daily.
- EventBridge rules on Config compliance changes and Audit Manager evidence events trigger extra runs.
- The collector Lambda calls the Config, Audit Manager, and Security Hub APIs, normalizes each item to JSON, computes a SHA-256 hash, and writes it with a manifest entry.

### State

- The evidence lake is a temporary S3 bucket under `evidence/<framework>/<yyyy>/<mm>/<dd>/`: versioned, private (S3 Block Public Access on), SSE-KMS, with no Object Lock and no legal hold.
- Lifecycle rules expire current objects after 30 days, noncurrent versions after 7 days, and incomplete multipart uploads after 1 day. The bucket's DeletionPolicy and UpdateReplacePolicy are Delete.
- The control map table links each control to its evidence object keys and the latest collection time.

### Orchestration

- An S3 event triggers the mapper Lambda, which reads the manifest and updates the control map.
- The Glue Data Catalog defines tables over the lake, partitioned by framework and date.
- The package builder reads the control map for an audit scope and writes a bundle (manifest, hashes, objects) to `packages/<audit-id>/`.

### Outputs

- Auditors use Athena with a read-only role to query evidence by control and date.
- The audit package is shared through a time-limited link or the read-only role.
- A CloudWatch metric per control tracks hours since last evidence; an alarm fires past the control's window and alerts through SNS.

## Data model

DynamoDB table `control_evidence`:

- Partition key `framework#control_id`, sort key `collected_at`.
- Attributes: `evidence_keys`, `sha256`, `source` (config, audit-manager, security-hub, cloudtrail), `status`, `freshness_window_hours`.

S3 prefixes:

- `evidence/<framework>/<yyyy>/<mm>/<dd>/<source>/<item-id>.json`
- `manifests/<yyyy>/<mm>/<dd>/manifest.json`
- `packages/<audit-id>/`

## Security and privacy controls

- KMS customer managed key for the lake, packages, and the control map.
- Integrity is tamper-evident (hashed): each object has a SHA-256 hash and the manifest lists every hash, so any change shows up on verification. There is no Object Lock and no legal hold, so teardown empties the bucket, including all versions, and then deletes the stack.
- Least-privilege IAM: the collector can write only `evidence/`; the auditor role is read-only and scoped to one audit.
- CloudTrail data events on the lake.
- No secrets or personal data in evidence or logs; the collector drops credential fields from configuration items.
- Human approval point: the owner approves the audit scope before a package is built and shared.

## 340 Collective testbed

340 Collective's AWS account provides the real Config history, Security Hub results, and CloudTrail activity. No client data is collected. Validation is a package for one sample audit scope, with every control in scope showing current evidence and a matching hash.

## Cost note

The main cost drivers are Config recording (per configuration item recorded), S3 storage (kept small by the 30-day expiry of current objects and the 7-day expiry of noncurrent versions), and Athena (per TB scanned, kept small with date and framework partitions). Lambda, DynamoDB, EventBridge, and Glue Data Catalog stay at or near the free tier at 340 Collective's scale. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Temporary evidence lake bucket (versioned, private, SSE-KMS, no Object Lock, lifecycle expiry, DeletionPolicy Delete), KMS key, and the control map table.
2. Collector Lambda with the daily schedule.
3. EventBridge change rules.
4. Mapper Lambda and the Glue catalog with Athena.
5. Package builder and the read-only auditor role.
6. Freshness metrics, alarms, and SNS.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md)
- [08 Access Reviews](../Abdifatah-08-Access-Reviews/README.md)
