# Third-Party and Vendor Risk Management - Lab Steps (engineering)

Build, test, hand off, and tear down the Third-Party and Vendor Risk Management design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-02-TPRM-VRM/LAB-STEPS.md](../../non-engineering/Jason-02-TPRM-VRM/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](TPRM-VRM-Architecture.md) and Jason's Handoff 1 Jira Task before you write any template.
2. Turn Jason's questionnaire, weights, and tier rules (Handoff 1) into the registry fields and the scorer's tier logic.
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

## Hand off

1. Create the Handoff 2 Jira Task for Jason: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records an acceptance test result on the Task (pass, or findings), which is not an approval. Adam validates on the Task, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-tprm` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Textract and Comprehend bill per request; confirm no asynchronous job is still running.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, merge it.

## Handoffs

Each handoff is a Jira Task linked to the project epic ([GRC-3](https://340collective.atlassian.net/browse/GRC-3)). The person who sends the handoff creates the Task.

- Handoff 1: vendor questionnaire, weights, and tier rules, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: vendor intake and scoring pipeline ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: three-vendor scorecard and vendor risk report, Jason to Faris (Jira Task, created by Jason)

**Skills:** Serverless pipelines · document parsing · scoring logic · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · API Gateway · Lambda · Step Functions · Textract · Comprehend · DynamoDB · CloudWatch

**Deliverable:** A tested vendor intake and scoring pipeline in the `grc-tprm` stack, accepted on the Handoff 2 Jira Task, and torn down with evidence.

**What it simulates:** An automation engineer building vendor risk intake for a TPRM team.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
