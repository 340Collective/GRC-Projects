# Audit Engagement Manager - Lab Steps (engineering)

Build, test, hand off, and tear down the Audit Engagement Manager design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-10-Audit-Engagement-Manager/LAB-STEPS.md](../../non-engineering/Jason-10-Audit-Engagement-Manager/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Audit-Engagement-Architecture.md) and Jason's Handoff 1 Jira Task before you write any template.
2. Turn Jason's PBC request list template and findings SLA rules (Handoff 1) into the PBC and findings tables and the reminder rules.
3. Put a Cognito authorizer on every portal route.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Plan to stay under 10 dollars a month: Costs stay near zero at one engagement at a time.

## Deploy

1. Write `infrastructure/cloudformation/grc-audit-engagement.yaml` in this repo, in the build order from the architecture doc:
   - Evidence bucket, KMS key, and the PBC and findings tables.
   - Cognito user pool, groups, and the portal API with the handler.
   - Presigned upload and the intake marker.
   - Finding state machine with the approval and validation steps.
   - Daily reminder through SES, then the weekly status report.
   - CloudWatch alarms.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-audit-engagement` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Create one synthetic engagement: a PBC request with an owner and due date, a presigned upload marked received, a finding moved from plan to validation to closed, and an SLA reminder for an overdue request.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the evidence bucket, both tables, and the status reports.
   - One IAM role per Lambda: the intake marker can update request status only; the reminder can read both tables and send email only.
   - Cognito authorizer on every portal route; auditors have read-only evidence access.
   - CloudTrail data events on the evidence bucket, so every read and upload is attributable.
   - No evidence content or personal data in logs.
   - Human approval points: the 340 Collective owner, as engagement owner, approves each remediation plan; the auditor validates each remediation before a finding closes.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Hand off

1. Create the Handoff 2 Jira Task for Jason: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records an acceptance test result on the Task (pass, or findings), which is not an approval. Adam validates on the Task, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-audit-engagement` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Remove any SES test identity the stack did not create.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, merge it.

## Handoffs

Each handoff is a Jira Task linked to the project epic ([GRC-11](https://340collective.atlassian.net/browse/GRC-11)). The person who sends the handoff creates the Task.

- Handoff 1: PBC request list template and findings SLA rules, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: engagement tracker build ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: engagement status summary, Jason to Faris (Jira Task, created by Jason)

**Skills:** Workflow state machines · authenticated portals · SLA reminders · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Cognito · API Gateway · Lambda · Step Functions · DynamoDB · S3 · SES

**Deliverable:** A tested engagement tracker in the `grc-audit-engagement` stack, accepted on the Handoff 2 Jira Task, and torn down with evidence.

**What it simulates:** An automation engineer building an audit engagement tracker.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
