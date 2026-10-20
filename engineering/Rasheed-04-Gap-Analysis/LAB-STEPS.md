# 340 Collective Gap Analysis - Lab Steps (engineering)

Build and test the 340 Collective Gap Analysis design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-04-Gap-Analysis/LAB-STEPS.md](../../non-engineering/Jason-04-Gap-Analysis/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Gap-Analysis-Architecture.md) and agree scope and requirements with Jason at the Day 1 kickoff before you write any template.
2. You build only the monthly scoring run: the control library loaded from Jason's matrix, the answers prefix, the gap scorer and history table, and the schedule and alarms. The report builder and the client one-pager (build order step 5) are out of scope; Jason writes the gap report.
3. Read posture from Config and Security Hub as 01 left them; add no conformance pack without a cost check.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Plan to stay under 10 dollars a month: Config rule evaluations and Security Hub checks bill per evaluation; run the scorer by hand during the test instead of waiting a month.

## Deploy

1. Write `infrastructure/cloudformation/grc-gap-scoring.yaml` in this repo, in the build order from the architecture doc:
   - Framework catalogs in S3 and the control library table with the crosswalk.
   - Config conformance packs and Security Hub standards.
   - Questionnaire format and the answers prefix.
   - Gap scorer and history table.
   - Scheduler, alarms, and SNS.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-gap-scoring` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Load Jason's control matrix as the library, upload one synthetic answers file, run the scorer once by hand, and compare each score with Jason's matrix.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for reports, answers, and both tables.
   - Least-privilege IAM: the scorer reads Security Hub and the library and writes history; the builder reads history and writes reports.
   - CloudTrail logs every read of the reports prefix.
   - No client names in logs; logs carry the assessment ID.
   - Human approval point: the assessor reviews the scored report before the one-pager is sent to a client.
3. Check the budget's actual spend (budget reads are allowed) and record it in FINAL-REPORT.md section 6. If an alert has fired, follow the [running system cost](../../GOVERNANCE.md#running-system-cost) rule.

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason commits his test result (pass, or findings) to his own folder and signs off on the Final report item. It is not an approval. Adam validates there, and Faris gives final approval.
3. Put the build notes (what was deployed and the test results; no secrets or raw evidence) in FINAL-REPORT.md sections 3 and 7, in the Day 7 pull request.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-gap-scoring` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Remove any conformance pack or Security Hub standard this build turned on; leave those 01 still needs.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend recorded, with no GRC charges after deletion) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Jason commits his results to his own folder, compares them with your report, and signs off on the Final report item (pass, or findings, not an approval). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Scoring automation · DynamoDB history · scheduled jobs · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Lambda · DynamoDB · S3 · EventBridge Scheduler · Config · Security Hub

**Deliverable:** A tested monthly scoring run in the `grc-gap-scoring` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An engineer automating a recurring assessment for a GRC lead.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
