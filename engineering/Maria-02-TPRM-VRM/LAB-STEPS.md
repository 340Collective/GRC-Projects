# Third-Party and Vendor Risk Management - Lab Steps (engineering)

Build, test, and tear down the Third-Party and Vendor Risk Management design on AWS as a temporary stack. The stack stays deployed after sign-off and is torn down in the program's final week. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-02-TPRM-VRM/LAB-STEPS.md](../../non-engineering/Jason-02-TPRM-VRM/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](TPRM-VRM-Architecture.md) and agree scope and requirements with Jason at the Day 1 kickoff before you write any template.
2. Turn Jason's questionnaire, weights, and tier rules (agreed at kickoff) into the registry fields and the scorer's tier logic.
3. The risk dashboard is a CloudWatch dashboard inside the free tier; there is no paid BI tool.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Confirm Textract and Comprehend are inside the permissions boundary; if not, raise the access-change PR first.
6. Plan to stay under 10 dollars a month: Textract (per page) and Comprehend (per unit of text) are the cost drivers; test with a few synthetic pages.

## Deploy

1. Write `infrastructure/cloudformation/grc-tprm.yaml` in this repo, in the build order from the architecture doc:
   - Document bucket, KMS key, and the vendor registry table.
   - Intake API and intake Lambda, tested with one vendor.
   - Step Functions workflow with Textract and Comprehend tasks.
   - Scoring Lambda and the tier rules.
   - Scheduler reassessment timers, SES reminders, and SNS alerts.
   - CloudWatch dashboard and alarms.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-tprm` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Submit one synthetic vendor with a short SIG questionnaire and a sample SOC 2 summary, and check the parsed answers, the weighted score, and the tier against Jason's rules.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the document bucket, the registry, and SNS.
   - One IAM role per Lambda with only the actions it needs (for example the scorer can read parsed output and write the registry, nothing else).
   - CloudTrail data events on the document bucket.
   - No document text or vendor contact details in logs; logs carry IDs only.
   - Human approval point: the risk owner reviews and accepts every high tier result before it is final.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records a test result (pass, or findings) as a comment on the project item, which is not an approval. Adam validates there, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## Tear down (final week)

1. Do not tear down at Day 7. After the partner's sign-off and final approval are on the Final report item, the stack stays deployed and you move to your next project. Tear down in the program's final week (Nov 23 to 25, 2026; see [GOVERNANCE.md](../../GOVERNANCE.md#final-week)).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-tprm` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Textract and Comprehend bill per request; confirm no asynchronous job is still running.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Jason reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

**Skills:** Serverless pipelines · document parsing · scoring logic · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · API Gateway · Lambda · Step Functions · Textract · Comprehend · DynamoDB · CloudWatch

**Deliverable:** A tested vendor intake and scoring pipeline in the `grc-tprm` stack, signed off on the Final report item, and torn down with evidence in the program's final week.

**What it simulates:** An automation engineer building vendor risk intake for a TPRM team.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, keeps it deployed after sign-off, and tears it down in the program's final week; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
