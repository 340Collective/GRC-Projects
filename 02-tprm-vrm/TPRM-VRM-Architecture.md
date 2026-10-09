# Third-Party and Vendor Risk Management Architecture

## Purpose

Give 340 Collective one automated path for every vendor: collect the right documents, read them without manual copy and paste, score the risk the same way every time, and make sure no vendor silently passes its reassessment date. The output is a vendor registry and a dashboard a risk owner can act on.

## Scope and frameworks

- SOC 2 (2017 TSC) CC9.2: vendor and business partner risk management.
- ISO 27001:2022 Annex A 5.19 to 5.22: supplier relationships, supplier agreements, ICT supply chain, and monitoring of supplier services.
- NIST CSF 2.0 GV.SC: cybersecurity supply chain risk management.
- Control areas: vendor inventory, due diligence evidence, risk tiering, reassessment cadence, and offboarding.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Intake | API Gateway, Lambda, S3 | Vendor submits the intake form and uploads SIG and SOC 2 documents to a private bucket |
| Processing | Step Functions, Textract, Comprehend | Upload event starts the workflow; documents are converted to text, tables, and entities |
| State | Lambda (scorer), DynamoDB | Scorer computes inherent and residual risk and a tier; result is stored in the vendor registry |
| Orchestration | EventBridge Scheduler, Lambda, SES, SNS | Per tier reassessment timers fire reminder emails to vendors and alerts to the risk owner |
| Outputs | QuickSight, CloudWatch | Risk dashboard for the owner; alarms on workflow failures |

## Stage details

### Intake

- API Gateway exposes the intake form endpoint with request validation and throttling. It sits behind an authorizer or a signed one-time link per vendor, so it is never an open upload endpoint.
- The intake Lambda validates fields (vendor name, service, data types shared, criticality) and writes a pending record.
- Documents go to S3 under `vendors/<vendor-id>/<yyyy>/<mm>/`, with Block Public Access on and SSE-KMS.

### Processing

- An S3 `ObjectCreated` event (through EventBridge) starts the Step Functions risk scoring workflow.
- Textract `AnalyzeDocument` (tables and forms) reads SIG answers and SOC 2 report sections.
- Comprehend detects entities and key phrases: report period, auditor opinion, exceptions, carved-out subservice organizations.
- Each task has retries with backoff and a catch that routes the vendor to manual review.

### State

- The scoring Lambda combines intake answers (data sensitivity, access level) with parsed findings (exceptions, report age).
- It writes inherent risk, residual risk, tier, next review date, and the source document keys to DynamoDB.
- A DynamoDB stream can forward high tier vendors to the [07 Risk Register](../07-risk-register/README.md).

### Orchestration

- EventBridge Scheduler holds one schedule per vendor, set by tier (for example 12 months for low, 6 for high).
- At expiry the reassessment trigger Lambda reads the registry, emails the vendor through SES, and publishes an alert to SNS for the risk owner.

### Outputs

- QuickSight reads the registry (through a nightly export to S3) for tier counts, overdue reviews, and open exceptions.
- CloudWatch alarms on workflow failures, Textract throttling, and overdue reassessments.

## Data model

DynamoDB table `vendor_registry`:

- Partition key `vendor_id`, sort key `assessment_date`.
- Attributes: `name`, `service`, `data_types`, `criticality`, `inherent_risk`, `residual_risk`, `tier`, `next_review`, `document_keys`, `exceptions`, `status`.
- GSI on `tier` and `next_review` for overdue queries.

S3 prefixes:

- `vendors/<vendor-id>/<yyyy>/<mm>/` for submitted documents.
- `parsed/<vendor-id>/<assessment-date>/` for Textract and Comprehend output.
- `exports/<yyyy>/<mm>/<dd>/` for the dashboard export.

## Security and privacy controls

- KMS customer managed key for the document bucket, the registry, and SNS.
- One IAM role per Lambda with only the actions it needs (for example the scorer can read parsed output and write the registry, nothing else).
- CloudTrail data events on the document bucket.
- No document text or vendor contact details in logs; logs carry IDs only.
- Human approval point: the risk owner reviews and accepts every high tier result before it is final.

## 340 Collective testbed

340 Collective's real AWS account runs this pipeline against its own vendors: AWS, Stripe, the domain registrar, Google Workspace, and GitHub. Their public SOC 2 summaries and trust center documents are the sample set. Validation means each vendor ends with a registry entry, a tier, a scheduled reassessment, and a dashboard row.

## Cost note

The main cost drivers are Textract (per page), Comprehend (per unit of text), and QuickSight (per user). API Gateway, Lambda, Step Functions, DynamoDB, S3, SES, and SNS stay at or near the free tier at 340 Collective's vendor count. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Document bucket, KMS key, and the vendor registry table.
2. Intake API and intake Lambda, tested with one vendor.
3. Step Functions workflow with Textract and Comprehend tasks.
4. Scoring Lambda and the tier rules.
5. Scheduler reassessment timers, SES reminders, and SNS alerts.
6. QuickSight dashboard and CloudWatch alarms.

## Related projects

- [01 GRC-as-Code Platform](../01-grc-as-code-platform/README.md)
- [04 Gap Analysis](../04-gap-analysis-340collective/README.md)
- [06 Evidence Automation](../06-evidence-automation/README.md)
- [07 Risk Register](../07-risk-register/README.md)
