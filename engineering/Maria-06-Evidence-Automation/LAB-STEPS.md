# Audit Evidence Automation - Lab Steps (engineering)

Build and test the Audit Evidence Automation design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-06-Evidence-Automation/LAB-STEPS.md](../../non-engineering/Adam-06-Evidence-Automation/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Evidence-Automation-Architecture.md) and agree scope and requirements with Adam at the Day 1 kickoff before you write any template.
2. Turn Adam's control list (agreed at kickoff) into the control map table.
3. Build the lake from the foundation's temporary evidence bucket pattern: versioned, private, SSE-KMS, no Object Lock and no legal hold, current objects expire after 30 days, noncurrent versions after 7 days, incomplete multipart uploads after 1 day, DeletionPolicy and UpdateReplacePolicy Delete.
4. Plan the SHA-256 hash per object and the manifest that lists every hash.
5. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
6. Plan to stay under 10 dollars a month: Config recording, S3 storage (kept small by the 30 and 7 day expiry), and Athena scans are the drivers; partition by date and framework.

## Deploy

1. Write `infrastructure/cloudformation/grc-evidence.yaml` in this repo, in the build order from the architecture doc:
   - Temporary evidence lake bucket (versioned, private, SSE-KMS, no Object Lock, lifecycle expiry, DeletionPolicy Delete), KMS key, and the control map table.
   - Collector Lambda with the daily schedule.
   - EventBridge change rules.
   - Mapper Lambda and the Glue catalog with Athena.
   - Package builder and the read-only auditor role.
   - Freshness metrics, alarms, and SNS.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-evidence` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Run the collector once by hand: objects land under `evidence/<framework>/<yyyy>/<mm>/<dd>/`, each with a SHA-256 hash, plus a manifest. Change a copy of one object and confirm verification catches it. Query one control in Athena and build one package.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the lake, packages, and the control map.
   - Integrity is tamper-evident (hashed): each object has a SHA-256 hash and the manifest lists every hash, so any change shows up on verification. There is no Object Lock and no legal hold, so teardown empties the bucket, including all versions, and then deletes the stack.
   - Least-privilege IAM: the collector can write only `evidence/`; the auditor role is read-only and scoped to one audit.
   - CloudTrail data events on the lake.
   - No secrets or personal data in evidence or logs; the collector drops credential fields from configuration items.
   - Human approval point: the owner approves the audit scope before a package is built and shared.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his test result and validation on the project item, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-evidence` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Stop the Config recorder if this build turned it on, and delete any Audit Manager assessment it created.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

**Skills:** Evidence pipelines · S3 lifecycle and integrity hashing · Glue and Athena · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Lambda · EventBridge · S3 · DynamoDB · Glue · Athena · CloudWatch

**Deliverable:** A tested evidence pipeline in the `grc-evidence` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An automation engineer building continuous audit evidence collection.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
