# Control Testing and Assessment - Lab Steps (engineering)

Build, test, hand off, and tear down the Control Testing and Assessment design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Alex (Security Automation Engineer). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-09-Control-Testing/LAB-STEPS.md](../../non-engineering/Jason-09-Control-Testing/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Control-Testing-Architecture.md) and Jason's Handoff 1 Jira Task before you write any template.
2. Turn Jason's 10-control test plan (Handoff 1) into the test library: procedure steps, population source, and sample size rule per control.
3. Seed the sampler so a rerun picks the same sample.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Plan to stay under 10 dollars a month: There is no significant cost driver; Athena scans stay small with partitions.

## Deploy

1. Write `cloudformation/grc-control-testing.yaml` in the private website repo, in the build order from the architecture doc:
   - Workpaper bucket, KMS key, and the test library and results tables.
   - Assessor API and the Step Functions workflow skeleton.
   - Sampling Lambda with seeded selection against one population source.
   - Test recorder with manual task tokens and append only history.
   - Workpaper builder and report assembly for one format, then the second.
   - SES notice and CloudWatch alarms.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `dev` in the website repo; Rasheed or Maria does the code review. Then move the template `dev` to `test` to `main` under that repo's change-control rule, with cfn-lint clean on `test`.
4. After Faris's approval, deploy the `grc-control-testing` stack from clean `main` with your GRC-Engineer seat and wait for `CREATE_COMPLETE`.

## Test

1. Load Jason's 10 controls and start one test run: the seeded sample is the same twice, results append to history, one workpaper is written per control, and the report assembles.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the workpaper bucket and both tables.
   - One IAM role per Lambda: the sampler can read the population sources and nothing else; the recorder can write results only; the workpaper builder can read results and write workpapers only.
   - CloudTrail data events on the workpaper bucket.
   - Logs carry run and control IDs only, never evidence content.
   - Human approval points: the assessor signs off each conclusion, and the 340 Collective owner, as control owner, accepts each exception or commits to remediation.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Hand off

1. Create the Handoff 2 Jira Task for Jason: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Jason records an acceptance test result on the Task (pass, or findings), which is not an approval. Adam validates on the Task, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-control-testing` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: 10-control test plan and procedures, Jason to Alex (Jira Task, created by Jason)
- Handoff 2: test automation and sampling ready for acceptance testing, Alex to Jason (Jira Task, created by Alex)
- Handoff 3: internal audit report, Jason to Faris (Jira Task, created by Jason)

**Skills:** Audit automation · reproducible sampling · Step Functions task tokens · CloudFormation

**Tools:** Website repo · CloudFormation · API Gateway · Step Functions · Lambda · DynamoDB · S3 · SES

**Deliverable:** A tested control testing workbench in the `grc-control-testing` stack, accepted on the Handoff 2 Jira Task, and torn down with evidence.

**What it simulates:** An engineer building a control testing workbench for an internal assessor.

Templates live in the private website repo; nothing in this repo is deployed.
