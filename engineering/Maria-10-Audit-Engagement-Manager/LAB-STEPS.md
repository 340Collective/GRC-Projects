# Audit Engagement Manager - Lab Steps (engineering)

Build and test the Audit Engagement Manager design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-10-Audit-Engagement-Manager/LAB-STEPS.md](../../non-engineering/Jason-10-Audit-Engagement-Manager/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Audit-Engagement-Architecture.md) and agree scope and requirements with Jason at the Day 1 kickoff before you write any template.
2. Turn Jason's PBC request list template and findings SLA rules (agreed at kickoff) into the PBC and findings tables and the reminder rules.
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

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records a test result (pass, or findings) as a comment on the project item, which is not an approval. Adam validates there, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-audit-engagement` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Remove any SES test identity the stack did not create.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Jason reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

**Skills:** Workflow state machines · authenticated portals · SLA reminders · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Cognito · API Gateway · Lambda · Step Functions · DynamoDB · S3 · SES

**Deliverable:** A tested engagement tracker in the `grc-audit-engagement` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An automation engineer building an audit engagement tracker.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
