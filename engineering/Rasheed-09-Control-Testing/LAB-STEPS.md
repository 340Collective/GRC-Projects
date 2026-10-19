# Control Testing and Assessment - Lab Steps (engineering)

Build and test the Control Testing and Assessment design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-09-Control-Testing/LAB-STEPS.md](../../non-engineering/Jason-09-Control-Testing/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Control-Testing-Architecture.md) and agree scope and requirements with Jason at the Day 1 kickoff before you write any template.
2. Turn Jason's 10-control test plan (agreed at kickoff) into the test library: procedure steps, population source, and sample size rule per control.
3. Seed the sampler so a rerun picks the same sample.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Plan to stay under 10 dollars a month: There is no significant cost driver; Athena scans stay small with partitions.

## Deploy

1. Write `infrastructure/cloudformation/grc-control-testing.yaml` in this repo, in the build order from the architecture doc:
   - Workpaper bucket, KMS key, and the test library and results tables.
   - Assessor API and the Step Functions workflow skeleton.
   - Sampling Lambda with seeded selection against one population source.
   - Test recorder with manual task tokens and append only history.
   - Workpaper builder and report assembly for one format, then the second.
   - SES notice and CloudWatch alarms.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-control-testing` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Load Jason's 10 controls and start one test run: the seeded sample is the same twice, results append to history, one workpaper is written per control, and the report assembles.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the workpaper bucket and both tables.
   - One IAM role per Lambda: the sampler can read the population sources and nothing else; the recorder can write results only; the workpaper builder can read results and write workpapers only.
   - CloudTrail data events on the workpaper bucket.
   - Logs carry run and control IDs only, never evidence content.
   - Human approval points: the assessor signs off each conclusion, and the 340 Collective owner, as control owner, accepts each exception or commits to remediation.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason commits his test result (pass, or findings) to his own folder and signs off on the Final report item. It is not an approval. Adam validates there, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-control-testing` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Jason commits his results to his own folder, compares them with your report, and signs off on the Final report item (pass, or findings, not an approval). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Audit automation · reproducible sampling · Step Functions task tokens · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · API Gateway · Step Functions · Lambda · DynamoDB · S3 · SES

**Deliverable:** A tested control testing workbench in the `grc-control-testing` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An engineer building a control testing workbench for an internal assessor.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
