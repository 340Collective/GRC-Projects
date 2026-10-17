# Compliance-as-Code Guardrails Architecture

## Purpose

Stop non-compliant infrastructure before it exists. [01](../Faris-01-GRC-as-Code-Platform/README.md) detects problems after they are deployed and [05](../Maria-05-Policy-Management/README.md) manages the written policies; this project turns those policies into checks that block a bad change in the pipeline, deny forbidden actions at the account level, and flag drift at runtime. Every violation becomes a finding in the same Security Hub pipeline 01 already reads.

## Scope and frameworks

- SOC 2 (2017 TSC) CC8.1 change management and CC6.6 boundary protection.
- ISO 27001:2022 Annex A 8.9 configuration management, 8.32 change management, and 8.27 secure architecture principles.
- NIST CSF 2.0 PR.PS: platform security, including configuration baselines and change control.
- Control areas: pre-deploy policy checks, account-level denies, runtime configuration rules, exceptions, and violation reporting.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Intake | GitHub, CodePipeline | A merged pull request starts the deploy pipeline |
| Processing | CodeBuild (OPA, Rego) | The template is synthesized and checked against Rego policies; any violation fails the build |
| State | CloudFormation, Organizations SCPs | Passing changes deploy as change sets; SCPs deny forbidden actions whatever the template says |
| Orchestration | Config, Lambda (rule evaluator) | Proactive and custom Config rules evaluate resources before and after deploy |
| Outputs | Lambda (violation reporter), Security Hub, CloudWatch | Violations become ASFF findings in 01's pipeline; alarms on gate failures |

## Stage details

### Intake

- The GitHub connection starts CodePipeline on a merge to main. Branch protection requires review, so no change reaches the pipeline unreviewed.
- The pipeline has three stages: source, policy gate, deploy. Deploy cannot run if the gate fails.

### Processing

- CodeBuild synthesizes the CloudFormation template and runs `opa eval` (or `conftest`) with the Rego policy bundle against it.
- Example policy names: `s3_block_public_access_required`, `s3_kms_encryption_required`, `cloudtrail_not_disabled`, `iam_no_wildcard_admin`, `approved_regions_only`, `required_tags_present`, `security_group_no_open_admin_ports`.
- Any `deny` result fails the build and writes a JSON report as a build artifact. The developer sees the failing rule and line in the build result.
- Exceptions are explicit: a reviewed exception file with an owner, a reason, and an expiry date. Expired exceptions fail the build again.

### State

- A passing build creates and executes a CloudFormation change set.
- Service Control Policies at the organization or OU level deny non-compliant actions regardless of template or role: for example `cloudtrail:StopLogging` and `cloudtrail:DeleteTrail`, any action outside approved regions, and turning off S3 Block Public Access.
- Because SCPs act at the account level, they also block the change set if a template slips past the gate. The diagram shows this as the dashed "blocks" control action.
- Assumption: SCPs need an AWS Organization. If 340 Collective's account is not in one, this layer is planned only and the gate plus Config rules carry the prevention.

### Orchestration

- AWS Config proactive evaluation checks resource configurations before CloudFormation provisions them, using the same rule set.
- Config custom rules call the rule evaluator Lambda on configuration change for checks managed rules do not cover (for example required tags by data classification).
- Non-compliant evaluations are recorded in Config and forwarded as findings.

### Outputs

- The violation reporter Lambda converts each failed gate result into an ASFF finding with the rule ID, resource, commit, and severity, and calls `BatchImportFindings`.
- Config rule results reach Security Hub through its native Config integration.
- In Security Hub these findings join [01's pipeline](../Faris-01-GRC-as-Code-Platform/README.md): routing, ticketing, and evidence.
- CloudWatch alarms on repeated gate failures and on new high severity guardrail findings.

## Data model

DynamoDB table `guardrail_exceptions` (optional; the exception file in Git is the source of truth):

- Partition key `rule_id`, sort key `resource_or_stack`.
- Attributes: `owner`, `reason`, `approved_by`, `expires_on`, `ticket_ref`.

ASFF finding fields used:

- `GeneratorId` set to the rule ID, `Types` set to the control family, `Resources` from the template or Config item, `Compliance.Status`, and `ProductFields` with the commit and pipeline run.

S3 prefixes:

- `gate-reports/<pipeline>/<yyyy>/<mm>/<dd>/<run-id>.json` for gate results.
- `policy-bundles/<version>/` for the Rego bundle used by each run.

## Security and privacy controls

- KMS customer managed key for pipeline artifacts and gate reports.
- One IAM role per component: CodeBuild can read the source and write reports only; the violation reporter can only call `BatchImportFindings`; the CloudFormation deploy role has no rights to change SCPs or Config.
- SCPs themselves are managed only from the management account, outside this pipeline.
- CloudTrail records every SCP, Config rule, and pipeline change.
- No secrets in templates or logs; gate reports carry rule IDs and resource logical names only.
- Human approval points: the 340 Collective owner approves every change to Rego policies, SCPs, and Config rules, and every exception with an expiry date.

## 340 Collective testbed

340 Collective's real AWS Organization and its GitHub to CloudFormation deploy path, which the 340 platform already uses, are the testbed. Validation uses a set of deliberately non-compliant templates (public bucket, unencrypted bucket, trail disabled, unapproved region) in a sandbox account: each must fail the gate, be denied by an SCP where applicable, and appear as a finding in Security Hub.

## Cost note

The main cost drivers are CodeBuild build minutes and Config rule evaluations (per evaluation, plus configuration items recorded). Lambda and Security Hub finding ingestion stay small at 340 Collective's deploy rate. SCPs have no charge. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Rego policy bundle with the first five rules and a test suite of good and bad templates.
2. CodeBuild gate stage inserted before deploy in the existing pipeline.
3. Violation reporter and the Security Hub hand-off.
4. Config proactive and custom rules with the rule evaluator.
5. SCPs in the Organization, starting in a sandbox OU.
6. Exception file, expiry check, and CloudWatch alarms.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [04 Gap Analysis](../Alex-04-Gap-Analysis/README.md)
- [05 Policy Management](../Maria-05-Policy-Management/README.md)
- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
