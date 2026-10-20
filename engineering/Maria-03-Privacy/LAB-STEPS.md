# Privacy Operations - Lab Steps (engineering)

Build and test the Privacy Operations design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

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
3. Check the budget's actual spend (budget reads are allowed) and record it in FINAL-REPORT.md section 6. If an alert has fired, follow the [running system cost](../../GOVERNANCE.md#running-system-cost) rule.

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason commits his test result (pass, or findings) to his own folder and signs off on the Final report item. It is not an approval. Adam validates there, and Faris gives final approval.
3. Put the build notes (what was deployed and the test results; no secrets or raw evidence) in FINAL-REPORT.md sections 3 and 7, in the Day 7 pull request.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-privacy` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. If an access-change PR let you turn on Macie, turn it off now.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend recorded, with no GRC charges after deletion) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Jason commits his results to his own folder, compares them with your report, and signs off on the Final report item (pass, or findings, not an approval). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Privacy engineering · Step Functions workflows · data discovery · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Lambda · Step Functions · DynamoDB · API Gateway · S3 · SES

**Deliverable:** A tested PII discovery and DSAR workflow in the `grc-privacy` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** A security automation engineer building privacy operations tooling.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
