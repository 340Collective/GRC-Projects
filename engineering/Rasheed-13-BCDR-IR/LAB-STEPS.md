# BC/DR and Incident Response Compliance - Lab Steps (engineering)

Build, test, and tear down the BC/DR and Incident Response Compliance design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md](../../non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](BCDR-IR-Architecture.md) and agree scope and requirements with Jason at the Day 1 kickoff before you write any template.
2. Turn Jason's RTO and RPO targets and the tabletop scenario (agreed at kickoff) into the targets per resource and the runbook list.
3. No vault lock: recovery points expire on the backup plan lifecycle and are deleted at teardown.
4. Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook. Failed or late DR tests become Jira issues this way.
5. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
6. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
7. Plan to stay under 10 dollars a month: AWS Backup storage and restores, and the temporary restored copy; keep restores small and delete them at the end of each test.

## Deploy

1. Write `infrastructure/cloudformation/grc-bcdr.yaml` in this repo, in the build order from the architecture doc:
   - Backup plans, vault (no vault lock; recovery points expire and are deleted at teardown), and the RTO and RPO targets per resource.
   - Results table and report bucket.
   - DR test state machine with restore, timing, and guaranteed cleanup, tested on one table.
   - Restore validator and the comparison with targets.
   - EventBridge finding routing to 07 and 06, and CloudWatch alarms.
   - IR runbooks in Systems Manager and the tabletop record template.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-bcdr` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Run one DR test on one small table: the restore lands in a test target, the validator compares counts and checksums, the achieved RTO and RPO are recorded against Jason's targets, and the test target is deleted at the end. Force one failure and check the finding event and its Jira issue.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed keys for the backup vault, the results table, and the report and tabletop buckets.
   - No vault lock; recovery points expire on the backup plan lifecycle and are deleted at teardown.
   - One IAM role per component: the DR test role can restore only into the test target naming pattern and can delete only test targets; it has no write access to live tables or buckets.
   - The restore validator reads counts and checksums only and never logs record content.
   - CloudTrail records every restore, deletion, and runbook execution.
   - Human approval points: the 340 Collective owner approves RTO and RPO targets; the IR lead signs off each DR test result and tabletop record; destructive IR runbook steps require approval in Systems Manager.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Jason what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records a test result (pass, or findings) as a comment on the project item, which is not an approval. Adam validates there, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## Tear down

1. Tear down after the partner's sign-off and final approval are on the Final report item, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-bcdr` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete every recovery point in the backup vault first (a vault that still holds recovery points cannot be deleted), and any restored test copy.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Jason reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Backup and restore testing · Step Functions · Systems Manager runbooks · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · AWS Backup · Step Functions · Lambda · Systems Manager · DynamoDB · EventBridge

**Deliverable:** A tested restore test and IR runbook build in the `grc-bcdr` stack, signed off on the Final report item, and torn down with evidence.

**What it simulates:** An engineer proving recovery objectives with automated restore tests.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
