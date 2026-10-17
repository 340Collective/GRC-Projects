# Control Testing and Assessment Architecture

## Purpose

Give an internal assessor one repeatable way to test a control: the same procedure, a sample anyone can reproduce, a recorded result for design and for operating effectiveness, and a workpaper that shows the work. The output is a set of workpapers and a SOC 2 readiness report or a NIST SP 800-53A style Security Assessment Report (SAR) that a control owner can act on and an external auditor can rely on.

## Scope and frameworks

- AICPA SOC 2 (2017 TSC) readiness: test of design (is the control built to meet the criterion) and test of operating effectiveness (did it run as designed across the period).
- NIST SP 800-53A Rev. 5 assessment procedures: examine, interview, and test methods, with objects and determination statements per control.
- NIST SAR style results report: per control result, findings, and recommended actions.
- Control areas: test procedure library, population definition, sample selection, result recording and history, workpapers, and reporting.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Intake | API Gateway, DynamoDB | The assessor starts a run for a control and period; the procedure is read from the test library |
| Processing | Step Functions, Lambda (sampler) | The workflow pulls the population from 06 or 07 and draws a seeded random sample |
| State | Lambda (recorder), DynamoDB | Design and operating results are recorded per sample item, with every prior result kept |
| Orchestration | Step Functions, Lambda (workpaper builder) | The workflow builds one workpaper per control, then assembles the report |
| Outputs | S3, SES, CloudWatch, KMS | Workpapers and report land in an encrypted bucket; SES notifies the control owner; alarms on failed runs |

## Stage details

### Intake

- API Gateway exposes the assessor API (start run, record manual result, get status) behind an authorizer. It is never an open endpoint.
- The test library table holds each control with its procedure steps, test method (examine, interview, test), population source, and a sample size rule by control frequency (for example annual 1, quarterly 2, monthly 2 to 5, daily 25 or more).
- Starting a run creates a `run_id` and starts the Step Functions test workflow with the control ID and the period.

### Processing

- The workflow reads the procedure from the library, then calls the sampling Lambda.
- The sampler queries the population source: Athena over the [06 evidence lake](../Maria-06-Evidence-Automation/README.md) for technical evidence, or the [07 risk register](../Rasheed-07-Risk-Register/README.md) for risk process controls.
- It applies the sample size rule and draws a random sample with a generated seed. The seed, population count, and population query are stored, so the same sample can be redrawn later.

### State

- The test recorder Lambda writes one result row per control, test type, and sample item: `pass`, `exception`, or `not_tested`, with the evidence key it relied on.
- Automated checks (for example "encryption enabled" read from evidence) are recorded directly. Manual steps pause the workflow with a task token until the assessor records the result through the API.
- Results are append only. A retest writes a new version, so the full results and state history stays visible.

### Orchestration

- After all samples are recorded, the workpaper builder writes one workpaper per control: procedure, population and seed, sample list, evidence references, exceptions, and conclusion.
- The assessor signs off each conclusion (a manual task step) before the control is marked complete.
- A report step assembles the chosen format: SOC 2 readiness (by Trust Services Criterion) or SAR style (by 800-53 family), with a summary of exceptions.

### Outputs

- Workpapers and reports are written to S3 under the run and control prefix, encrypted with the workpaper key.
- SES emails the control owner a notice that the report is ready, with no report content in the email body.
- CloudWatch alarms on failed or stalled workflow executions.

## Data model

DynamoDB table `test_library`:

- Partition key `control_id`, sort key `procedure_version`.
- Attributes: `framework_refs`, `test_type` (design, operating), `method`, `steps`, `population_source`, `frequency`, `sample_rule`, `owner`.

DynamoDB table `test_results`:

- Partition key `run_id#control_id`, sort key `test_type#sample_item#version`.
- Attributes: `result`, `evidence_key`, `tested_by`, `tested_at`, `seed`, `population_count`, `notes`.
- GSI on `control_id` and `tested_at` for history by control.

S3 prefixes:

- `workpapers/<run-id>/<control-id>/` for workpapers.
- `reports/<run-id>/` for the assembled report.
- `samples/<run-id>/<control-id>/` for the population snapshot and sample list.

## Security and privacy controls

- KMS customer managed key for the workpaper bucket and both tables.
- One IAM role per Lambda: the sampler can read the population sources and nothing else; the recorder can write results only; the workpaper builder can read results and write workpapers only.
- CloudTrail data events on the workpaper bucket.
- Logs carry run and control IDs only, never evidence content.
- Human approval points: the assessor signs off each conclusion, and the 340 Collective owner, as control owner, accepts each exception or commits to remediation.

## 340 Collective testbed

340 Collective's real AWS account is the first assessed environment. Testing starts with the controls [04 Gap Analysis](../Alex-04-Gap-Analysis/README.md) marks met, using real evidence from 06 and real risks from 07 as populations. Validation means each tested control ends with recorded results, a reproducible sample, a signed workpaper, and a line in the report.

## Cost note

There is no significant cost driver. API Gateway, Step Functions, Lambda, DynamoDB, S3, and SES stay at or near the free tier at 340 Collective's control count. Athena queries over the evidence lake are the only scan cost, and partitioning keeps them small. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Workpaper bucket, KMS key, and the test library and results tables.
2. Assessor API and the Step Functions workflow skeleton.
3. Sampling Lambda with seeded selection against one population source.
4. Test recorder with manual task tokens and append only history.
5. Workpaper builder and report assembly for one format, then the second.
6. SES notice and CloudWatch alarms.

## Related projects

- [04 Gap Analysis](../Alex-04-Gap-Analysis/README.md)
- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
- [07 Risk Register](../Rasheed-07-Risk-Register/README.md)
- [10 Audit Engagement Manager](../Maria-10-Audit-Engagement-Manager/README.md)
