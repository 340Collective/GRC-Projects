# Compliance-as-Code Guardrails - Lab Steps (engineering)

Write 340 Collective's preventive guardrails as policy-as-code and document the control each one enforces. The rules are written for review first, then built and tested in a temporary `grc-guardrails` stack. 340 Collective is the subject organization.

Track: engineering. You: Faris (ISSM). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-11-Compliance-as-Code-Guardrails/LAB-STEPS.md](../../non-engineering/Adam-11-Compliance-as-Code-Guardrails/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Guardrails-Architecture.md) and Adam's Handoff 1 Jira Task: the guardrail list and the control each enforces.
2. Draft an OPA/Rego rule for each guardrail that would fail a CloudFormation template before deploy, with a passing and a failing example template written alongside it.
3. Write the matching AWS Config rule definition for each guardrail (managed rule name or custom rule logic) to catch drift after deploy.
4. Outline a Service Control Policy that denies the highest-risk actions, such as stopping CloudTrail, leaving approved Regions, or disabling Security Hub.
5. SCPs are managed only from the management account, outside this pipeline, and the GRC-Engineer seat cannot change Organizations. The SCP stays an outline for the ISSM.
6. Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html). Guardrail violations reach Jira this way, through their ASFF findings.
7. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
8. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
9. Plan to stay under 10 dollars a month: CodeBuild minutes and Config rule evaluations are the drivers; keep test runs few.

## Deploy

1. Write `infrastructure/cloudformation/grc-guardrails.yaml` in this repo, in the build order from the architecture doc:
   - Rego policy bundle with the first rules and the passing and failing example templates as its test suite
   - CodeBuild gate stage before deploy
   - violation reporter and the Security Hub hand-off
   - Config proactive and custom rules with the rule evaluator
   - exception file, expiry check, and CloudWatch alarms
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed does the code review (Maria as backup). Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Adam's approval (he approves Faris-built work), deploy the `grc-guardrails` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Run the gate on the passing and failing example templates: the good one passes, and the bad one fails the build with the rule ID.
2. Confirm one violation shows up in Security Hub as an ASFF finding, and reaches Jira through path 1.
3. A Config rule flags a deliberately non-compliant test resource, and an expired exception fails the expiry check.
4. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for pipeline artifacts and gate reports.
   - One IAM role per component: CodeBuild can read the source and write reports only; the violation reporter can only call `BatchImportFindings`; the CloudFormation deploy role has no rights to change SCPs or Config.
   - SCPs themselves are managed only from the management account, outside this pipeline.
   - CloudTrail records every SCP, Config rule, and pipeline change.
   - No secrets in templates or logs; gate reports carry rule IDs and resource logical names only.
   - Human approval points: the 340 Collective owner approves every change to Rego policies, SCPs, and Config rules, and every exception with an expiry date.
5. Check the budget's actual spend: it is below the 1 dollar alert.

## Hand off

1. Create the Handoff 2 Jira Task for Adam: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his acceptance and validation on the Task and gives final approval, since you built it.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-guardrails` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete the Config rules, and stop the Config recorder if this build turned it on.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, merge it.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: guardrail list and the control each enforces, Adam to Faris (Jira Task, created by Adam)
- Handoff 2: Rego rules, Config rules, and SCP outline ready for acceptance, Faris to Adam (Jira Task, created by Faris)
- Handoff 3: guardrail-to-control register, Adam to Faris (Jira Task, created by Adam)

**Skills:** Policy-as-code · preventive controls · OPA/Rego · AWS Config · SCP design

**Tools:** Text editor · OPA Playground · AWS Config managed rules documentation · Excel or Google Sheets

**Deliverable:** A set of written Rego rules, Config rule definitions, an SCP outline, and a guardrail-to-control register.

**What it simulates:** A GRC engineer turning compliance requirements into preventive deploy-time controls.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
