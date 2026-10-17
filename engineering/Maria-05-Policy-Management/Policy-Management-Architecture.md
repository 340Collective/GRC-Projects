# 340 Collective Policy Management Architecture

## Purpose

Treat policies like code: every change is reviewed, versioned, validated, and published the same way, and every staff member's acknowledgment is recorded. Auditors get a clean history of who approved which version, when it was published, and who attested to it.

## Scope and frameworks

- SOC 2 CC1.4 (commitment to competence and expected conduct) and CC5.3 (control activities through policies and procedures).
- ISO 27001:2022 A.5.1 (policies for information security) and clause 7.5 (documented information).
- NIST CSF 2.0 GV.PO (policy).
- Control areas: policy ownership, approval, version control, publication, staff acknowledgment, and periodic review.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | GitHub (external), CodePipeline | Policy owner approves a pull request; the merge starts the pipeline |
| Processing | CodeBuild | Front matter, links, and banned terms are checked; the PDF is rendered |
| State | S3 (versioned library), DynamoDB (attestations) | Each version is stored; each attestation is recorded |
| Orchestration | EventBridge, EventBridge Scheduler, Lambda | New versions and review dates start attestation requests and reminders |
| Outputs | SES, API Gateway, CloudTrail, CloudWatch | Staff are emailed and attest; activity is logged and pipeline failures alarm |

## Stage details

### Producers

- Each policy is one Markdown file with front matter: `owner`, `version`, `effective_date`, `review_date`, `applies_to`.
- Branch protection on main requires the policy owner's approval.
- CodePipeline uses a GitHub connection (CodeStar Connections), so no long-lived tokens are stored.

### Processing

- CodeBuild fails the build if front matter is missing or the review date is in the past, if links are broken, or if banned terms appear.
- On success it renders each changed policy to PDF.

### State

- S3 with versioning and SSE-KMS stores both Markdown and PDF under `policies/<policy-id>/<version>/`.
- The attestation table records one item per person per policy version.

### Orchestration

- S3 publishes an object-created event to EventBridge; a rule starts the reminder Lambda for each new version.
- EventBridge Scheduler runs a daily check for policies past their review date and staff past their attestation window.
- The reminder Lambda reads the attestation table to find who has not attested.

### Outputs

- SES emails each staff member a link to the policy and the attestation page.
- API Gateway (behind an authorizer for staff sign-in) and the attestation handler write the record.
- CloudTrail logs API activity; CloudWatch alarms on failed pipeline runs.

## Data model

DynamoDB table `attestations`:

- Partition key `policy_id#version`, sort key `person_id`.
- Attributes: `attested_at`, `method`, `reminders_sent`.
- GSI on `person_id` to list one person's outstanding policies.

S3 prefixes: `policies/<policy-id>/<version>/policy.md` and `policy.pdf`.

## Security and privacy controls

- KMS customer managed key for the library and the attestation table.
- Least-privilege IAM: CodeBuild can write only the library prefix; the attestation handler can write only the table.
- The attestation API requires sign-in, so it is never unauthenticated.
- CloudTrail logs every write to the library.
- No personal data in logs beyond a person ID.
- Human approval points: the policy owner approves every pull request before merge.

## 340 Collective testbed

340 Collective's account runs the pipeline against its intended policy set: information security, acceptable use, access control, vendor management, incident response, and data retention. These are listed as the target set; this repo does not claim the documents exist or contain their text. Validation is one policy change going from pull request to a published PDF and a recorded attestation.

## Cost note

The main cost driver is CodeBuild build minutes. CodePipeline, S3, DynamoDB, Lambda, API Gateway, and SES stay at or near the free tier at 340 Collective's size. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Policy repo layout and front matter schema.
2. Versioned, encrypted S3 library.
3. CodePipeline with the GitHub connection and the CodeBuild validation stage.
4. Attestation table, API, and handler.
5. EventBridge rule, reminder Lambda, and SES.
6. Scheduler review checks, CloudTrail, and alarms.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md)
- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
