# BC/DR and Incident Response Compliance - Lab Steps (engineering)

Build, test, hand off, and tear down the BC/DR and Incident Response Compliance design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md](../../non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](BCDR-IR-Architecture.md) and Jason's Handoff 1 Jira Task before you write any template.
2. Turn Jason's RTO and RPO targets and the tabletop scenario (Handoff 1) into the targets per resource and the runbook list.
3. No vault lock: recovery points expire on the backup plan lifecycle and are deleted at teardown.
4. Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook. Failed or late DR tests become Jira issues this way.
5. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
6. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
7. Plan to stay under 10 dollars a month: AWS Backup storage and restores, and the temporary restored copy; keep restores small and delete them at the end of each test.

## Deploy

1. Write `cloudformation/grc-bcdr.yaml` in the private website repo, in the build order from the architecture doc:
   - Backup plans, vault (no vault lock; recovery points expire and are deleted at teardown), and the RTO and RPO targets per resource.
   - Results table and report bucket.
   - DR test state machine with restore, timing, and guaranteed cleanup, tested on one table.
   - Restore validator and the comparison with targets.
   - EventBridge finding routing to 07 and 06, and CloudWatch alarms.
   - IR runbooks in Systems Manager and the tabletop record template.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `dev` in the website repo; Maria or Alex does the code review. Then move the template `dev` to `test` to `main` under that repo's change-control rule, with cfn-lint clean on `test`.
4. After Faris's approval, deploy the `grc-bcdr` stack from clean `main` with your GRC-Engineer seat and wait for `CREATE_COMPLETE`.

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

## Hand off

1. Create the Handoff 2 Jira Task for Jason: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records an acceptance test result on the Task (pass, or findings), which is not an approval. Adam validates on the Task, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-bcdr` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete every recovery point in the backup vault first (a vault that still holds recovery points cannot be deleted), and any restored test copy.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: IR plan requirements, tabletop scenario, and RTO and RPO targets, Jason to Rasheed (Jira Task, created by Jason)
- Handoff 2: restore test and IR runbook build ready for acceptance testing, Rasheed to Jason (Jira Task, created by Rasheed)
- Handoff 3: tabletop summary and BC/DR test record, Jason to Faris (Jira Task, created by Jason)

**Skills:** Backup and restore testing · Step Functions · Systems Manager runbooks · CloudFormation

**Tools:** Website repo · CloudFormation · AWS Backup · Step Functions · Lambda · Systems Manager · DynamoDB · EventBridge

**Deliverable:** A tested restore test and IR runbook build in the `grc-bcdr` stack, accepted on the Handoff 2 Jira Task, and torn down with evidence.

**What it simulates:** An engineer proving recovery objectives with automated restore tests.

Templates live in the private website repo; nothing in this repo is deployed.
