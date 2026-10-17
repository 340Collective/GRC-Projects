# User Access Reviews - Lab Steps (engineering)

Build, test, hand off, and tear down the User Access Reviews design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Abdifatah (IAM / Identity Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-08-Access-Reviews/LAB-STEPS.md](../../non-engineering/Adam-08-Access-Reviews/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Access-Review-Architecture.md) and Adam's Handoff 1 Jira Task before you write any template.
2. Turn Adam's worksheet columns and review rules (Handoff 1) into the items table and the package format.
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

## Hand off

1. Create the Handoff 2 Jira Task for Adam: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his acceptance and validation on the Task, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-access-review` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete the Access Analyzer analyzers this build created.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, merge it.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: certification worksheet columns and review rules, Adam to Abdifatah (Jira Task, created by Adam)
- Handoff 2: access review package build ready for acceptance, Abdifatah to Adam (Jira Task, created by Abdifatah)
- Handoff 3: signed certification worksheet and remediation log, Adam to Faris (Jira Task, created by Adam)

**Skills:** Identity governance automation · Step Functions · IAM Access Analyzer · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Step Functions · Lambda · IAM Access Analyzer · DynamoDB · S3 · SES

**Deliverable:** A tested access review package build in the `grc-access-review` stack, accepted on the Handoff 2 Jira Task, and torn down with evidence.

**What it simulates:** An IAM engineer automating quarterly access certification.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
