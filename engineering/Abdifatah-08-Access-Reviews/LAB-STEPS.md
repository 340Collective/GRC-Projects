# User Access Reviews - Lab Steps (engineering)

Build and test the User Access Reviews design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Abdifatah (IAM / Identity Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-08-Access-Reviews/LAB-STEPS.md](../../non-engineering/Adam-08-Access-Reviews/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Access-Review-Architecture.md) and agree scope and requirements with Adam at the Day 1 kickoff before you write any template.
2. Turn Adam's worksheet columns and review rules (agreed at kickoff) into the items table and the package format.
3. Check the package format against the synthetic dataset in [uar-simulation](uar-simulation/README.md) before the live run.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Use the external access analyzer (no charge). Unused access analysis is a paid analyzer, which the access model denies (`DenyOrgAdminAndCostly`), unless an access-change PR allows it.
6. Plan to stay under 10 dollars a month: The external access analyzer has no charge; the rest stays near the free tier at a quarterly cadence.

## Deploy

1. Write `infrastructure/cloudformation/grc-access-review.yaml` in this repo, in the build order from the architecture doc:
   - KMS key, items table, and campaign bucket.
   - Access Analyzer external and unused access analyzers.
   - Collector Lambda and the Step Functions campaign with the quarterly schedule.
   - Package builder and SES links.
   - Sign-off API, decision handler, and the confirmed removal path.
   - Evidence export, CloudTrail, and the overdue alarm.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed or Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-access-review` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Run one campaign by hand: one package per approver, every decision recorded, and no removal runs without the owner's confirmation.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for packages, evidence, and the items table.
   - Least-privilege IAM: the collector is read-only; only the apply removals Lambda can change assignments, and only for items with a confirmed removal.
   - CloudTrail logs every read and every change.
   - No credentials in packages or logs; logs carry item IDs.
   - Human approval points: approvers decide every item, and the owner confirms every removal.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his test result and validation on the project item, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-access-review` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete the Access Analyzer analyzers this build created.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

**Skills:** Identity governance automation · Step Functions · IAM Access Analyzer · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Step Functions · Lambda · IAM Access Analyzer · DynamoDB · S3 · SES

**Deliverable:** A tested access review package build in the `grc-access-review` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An IAM engineer automating quarterly access certification.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
