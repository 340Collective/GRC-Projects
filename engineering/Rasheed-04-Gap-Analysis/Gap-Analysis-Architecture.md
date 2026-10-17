# 340 Collective Gap Analysis Architecture

## Purpose

Answer "how far are we from SOC 2, NIST CSF, and ISO 27001?" the same way every month, with evidence behind every score. One control library is crosswalked to all three frameworks, so a control is assessed once and reported three ways. The output is a detailed gap report for the team and a one-page summary a client can read.

## Scope and frameworks

- SOC 2 (2017 Trust Services Criteria), Common Criteria CC1 to CC9.
- NIST CSF 2.0: Govern, Identify, Protect, Detect, Respond, Recover.
- ISO 27001:2022 Annex A (93 controls).
- Control areas: every control in the library, split into technical controls (scored from AWS posture data) and process controls (scored from questionnaire answers).

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | AWS Config, Security Hub CSPM, S3 (questionnaire answers) | Conformance pack results and standard control status, plus assessor answers as JSON |
| Processing | Lambda (gap scorer) | Each control is scored met, partial, or gap from its mapped inputs |
| State | DynamoDB (control library, gap history), S3 (framework catalogs) | Crosswalked library and a scored history per run |
| Orchestration | EventBridge Scheduler | Monthly run, plus an on-demand run after a questionnaire upload |
| Outputs | Lambda (report builder), S3 (gap reports), SES, CloudWatch, SNS | Gap report and one-pager are written and emailed; failed runs alert |

## Stage details

### Producers

- Config conformance packs (for example the operational best practices packs for NIST CSF and ISO 27001) evaluate resources.
- Config sends results to Security Hub CSPM, which also runs its standards (AWS Foundational Security Best Practices, CIS).
- The assessor uploads questionnaire answers to `answers/<assessment-id>/` as JSON, one answer per process control.

### Processing

- The gap scorer reads the control library, then for each control pulls its mapped Security Hub controls or questionnaire items.
- Scoring rule: met when every mapped input passes, partial when some pass, gap when none pass or no evidence exists.
- Every score carries the input IDs that produced it, so the report can show why.

### State

- Framework catalogs (control text and IDs) are stored in S3 and loaded into the library.
- The control library holds the internal control, its SOC 2, NIST CSF, and ISO 27001 IDs, the expected evidence, and the input mapping.
- Gap history stores one item per control per run, so trends are visible.

### Orchestration

- EventBridge Scheduler runs the scorer monthly.
- An S3 event on a new questionnaire upload can trigger an on-demand run.

### Outputs

- The report builder writes the full gap report (HTML and CSV) and a one-page summary to `reports/<assessment-id>/<yyyy>/<mm>/`.
- The one-pager follows the 340 Collective `client-onepager-style` standard.
- SES emails the owner a time-limited link. CloudWatch alarms on scorer or builder errors and alerts through SNS.

## Data model

DynamoDB table `control_library`:

- Partition key `control_id`.
- Attributes: `title`, `soc2_ids`, `nist_csf_ids`, `iso27001_ids`, `type` (technical or process), `inputs`, `expected_evidence`, `owner`.

DynamoDB table `gap_history`:

- Partition key `assessment_id`, sort key `run_date#control_id`.
- Attributes: `status` (met, partial, gap), `input_results`, `notes`.

S3 prefixes: `catalogs/<framework>/`, `answers/<assessment-id>/`, `reports/<assessment-id>/<yyyy>/<mm>/`.

## Security and privacy controls

- KMS customer managed key for reports, answers, and both tables.
- Least-privilege IAM: the scorer reads Security Hub and the library and writes history; the builder reads history and writes reports.
- CloudTrail logs every read of the reports prefix.
- No client names in logs; logs carry the assessment ID.
- Human approval point: the assessor reviews the scored report before the one-pager is sent to a client.

## 340 Collective testbed

340 Collective's own account is the first assessment. Its Config rules and Security Hub standards provide the technical inputs, and 340 Collective answers its own questionnaire for the process controls. Validation is a complete report whose scores match a manual check of a sample of controls.

## Cost note

The main cost drivers are Config rule evaluations and Security Hub security checks, both billed per evaluation. Lambda, DynamoDB, S3, and SES stay at or near the free tier at a monthly cadence. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Framework catalogs in S3 and the control library table with the crosswalk.
2. Config conformance packs and Security Hub standards.
3. Questionnaire format and the answers prefix.
4. Gap scorer and history table.
5. Report builder, one-pager, and SES delivery.
6. Scheduler, alarms, and SNS.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [05 Policy Management](../Maria-05-Policy-Management/README.md)
- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
