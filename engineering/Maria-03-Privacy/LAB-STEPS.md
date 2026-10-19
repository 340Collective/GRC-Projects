# Privacy Operations - Lab Steps (engineering)

Build, test, and tear down the Privacy Operations design on AWS as a temporary stack. The stack stays deployed after sign-off and is torn down in the program's final week. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-03-Privacy/LAB-STEPS.md](../../non-engineering/Jason-03-Privacy/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Privacy-Architecture.md) and agree scope and requirements with Jason at the Day 1 kickoff before you write any template.
2. Turn Jason's RoPA fields and DSAR requirements (agreed at kickoff) into the inventory schema and the workflow's approval pause.
3. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
4. Macie is on the deny list. Use synthetic records and a scoped pattern-matching Lambda over the staging prefix, unless an access-change PR allows Macie.
5. Plan to stay under 10 dollars a month: Macie would be the main cost; with synthetic records and a scoped Lambda the rest stays at or near the free tier.

## Deploy

1. Write `infrastructure/cloudformation/grc-privacy.yaml` in this repo, in the build order from the architecture doc:
   - KMS key, inventory, ledger, and request tables.
   - Table export Lambda and the staging prefix with a lifecycle rule.
   - Macie jobs and the EventBridge rule to the inventory updater.
   - Privacy API with the consent handler.
   - DSAR Step Functions workflow with the approval pause and SES delivery.
   - Deadline alarms and CloudTrail data events.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-privacy` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Run one synthetic DSAR (access, then deletion): the approval pause holds until the privacy owner approves, the deadline alarm is set, and the package expires after delivery.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for staging, the inventory, the ledger, and DSAR packages.
   - Least-privilege IAM per Lambda; only the locate and export Lambda can read source data.
   - CloudTrail data events on the DSAR bucket; packages expire after delivery.
   - No PII in logs: functions log request IDs and counts only.
   - Human approval points: the privacy owner approves every DSAR release and every deletion.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records a test result (pass, or findings) as a comment on the project item, which is not an approval. Adam validates there, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## Tear down (final week)

1. Do not tear down at Day 7. After the partner's sign-off and final approval are on the Final report item, the stack stays deployed and you move to your next project. Tear down in the program's final week (Nov 23 to 25, 2026; see [GOVERNANCE.md](../../GOVERNANCE.md#final-week)).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-privacy` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. If an access-change PR let you turn on Macie, turn it off now.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Jason reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

**Skills:** Privacy engineering · Step Functions workflows · data discovery · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Lambda · Step Functions · DynamoDB · API Gateway · S3 · SES

**Deliverable:** A tested PII discovery and DSAR workflow in the `grc-privacy` stack, signed off on the Final report item, and torn down with evidence in the program's final week.

**What it simulates:** A security automation engineer building privacy operations tooling.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, keeps it deployed after sign-off, and tears it down in the program's final week; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
