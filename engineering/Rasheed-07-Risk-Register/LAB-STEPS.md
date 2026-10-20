# Risk Register - Lab Steps (engineering)

Build and test the Risk Register design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-07-Risk-Register/LAB-STEPS.md](../../non-engineering/Adam-07-Risk-Register/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Risk-Register-Architecture.md) and agree scope and requirements with Adam at the Day 1 kickoff before you write any template.
2. Turn Adam's scoring rules and the seed register in [07-risk-register-lab.xlsx](../../non-engineering/Adam-07-Risk-Register/07-risk-register-lab.xlsx) (agreed at kickoff) into the DREAD+ scoring logic.
3. The heatmap is an HTML report from a Lambda; there is no paid BI tool.
4. Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook. The design's Jira sync Lambda already calls the Jira REST API; keep it consistent with 01.
5. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
6. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
7. Plan to stay under 10 dollars a month: There is no paid dashboard; Cognito, API Gateway, Lambda, DynamoDB, and Athena stay at or near the free tier.

## Deploy

1. Write `infrastructure/cloudformation/grc-risk-register.yaml` in this repo, in the build order from the architecture doc:
   - KMS key and the register table with both GSIs.
   - Cognito user pool, API, and risk handler with the scoring logic.
   - Streams, Jira sync, and the Secrets Manager token.
   - Per risk Scheduler timers, the SLA escalator, and SNS.
   - Nightly export, Athena, and the heatmap report Lambda.
   - CloudWatch alarms.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-risk-register` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Log three seed risks from Adam's sheet through the API: scores match the sheet, each risk gets a Jira ticket, and a review timer set in the past escalates through SNS.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the register, exports, and SNS.
   - The API requires Cognito sign-in; there is no unauthenticated write path.
   - Least-privilege IAM: only the handler writes the register; only the sync Lambda reads the Jira secret.
   - CloudTrail logs API and Scheduler activity.
   - No secrets or personal details in logs; logs carry risk IDs.
   - Human approval point: the risk owner accepts the treatment and any residual rating before the risk is closed.
3. Check the budget's actual spend (budget reads are allowed) and record it in FINAL-REPORT.md section 6. If an alert has fired, follow the [running system cost](../../GOVERNANCE.md#running-system-cost) rule.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam commits his test results to his own folder, signs off, and records his validation on the Final report item. Faris gives final approval.
3. Put the build notes (what was deployed and the test results; no secrets or raw evidence) in FINAL-REPORT.md sections 3 and 7, in the Day 7 pull request.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-risk-register` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Revoke the Jira API token and delete its `/grc/` parameter.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend recorded, with no GRC charges after deletion) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Adam commits his results to his own folder, compares them with your report, and signs off on the Final report item ("Accepted by: <first name>", or findings). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Serverless APIs · Cognito sign-in · DynamoDB Streams · scheduled escalation · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Cognito · API Gateway · Lambda · DynamoDB · EventBridge Scheduler · Athena · Jira

**Deliverable:** A tested risk register service in the `grc-risk-register` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An engineer turning a risk register spreadsheet into a tracked service.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
