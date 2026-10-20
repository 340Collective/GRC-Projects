# GRC Metrics and Board Reporting - Lab Steps (engineering)

Build and test the GRC Metrics and Board Reporting design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-12-Metrics-Reporting/LAB-STEPS.md](../../non-engineering/Adam-12-Metrics-Reporting/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](GRC-Metrics-Architecture.md) and agree scope with Adam at the Day 1 kickoff before you write any template. Adam writes REQUIREMENTS.md in his own folder, and Faris accepts it.
2. Turn Adam's metric definitions, targets, and thresholds (agreed at kickoff) into the metric definitions table.
3. Build after 06, 11, and 07 have produced records; you read their stores read-only.
4. No paid BI tool: trends go on a CloudWatch dashboard inside the free tier (3 dashboards of up to 50 metrics, 10 custom metrics), results go to the GRC Metrics Jira issue, and the board pack is HTML or Markdown emailed through SES.
5. Jira path 3: the daily KRI and KPI job posts its results to the "GRC Metrics" Jira issue, as a comment or custom fields.
6. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
7. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
8. Plan to stay under 10 dollars a month: 0 dollars day to day: the CloudWatch free tier, free Jira, and SES for the board pack.

## Deploy

1. Write `infrastructure/cloudformation/grc-metrics.yaml` in this repo, in the build order from the architecture doc:
   - Metric definitions table and the first four metrics from projects already built.
   - Metrics builder, daily schedule, and snapshot table.
   - Parquet history in S3, Glue table, and Athena queries.
   - CloudWatch trend dashboard, and the Jira poster that updates the GRC Metrics issue.
   - Monthly board pack builder, approval step, and SES delivery.
   - CloudWatch KRI alarms and SNS alerts; add metrics as each project ships.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-metrics` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Run the metrics builder once: each value matches a hand count from its source table, history lands partitioned by date, the GRC Metrics Jira issue gets the day's results, and a test breach raises the KRI alarm. The board pack waits for approval before SES sends it.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the metrics tables, the history bucket, and the board packs.
   - One IAM role per Lambda: the metrics builder has read-only access to the source tables and Security Hub and can write only its own snapshots; the board pack builder can read snapshots and write packs only.
   - Metrics are counts and rates, never records: no names, emails, or evidence content reach the metrics store or logs.
   - The CloudWatch dashboard and the Jira GRC Metrics issue carry counts and rates only, never row-level source data.
   - Human approval points: the 340 Collective owner approves each board pack before it is sent and every threshold change.
3. Check the budget's actual spend (budget reads are allowed) and record it in FINAL-REPORT.md section 6. If an alert has fired, follow the [running system cost](../../GOVERNANCE.md#running-system-cost) rule.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam commits his test results to his own folder, signs off, and records his validation on the Final report item. Faris gives final approval.
3. Put the build notes (what was deployed and the test results; no secrets or raw evidence) in FINAL-REPORT.md sections 3 and 7, in the Day 7 pull request.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-metrics` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Revoke the Jira API token and delete its `/grc/` parameter.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend recorded, with no GRC charges after deletion) where the ISSM designates, outside git, and note it on the project item.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: Adam writes REQUIREMENTS.md in his own folder, and Faris accepts it. You and Adam agree on scope.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Adam commits his results to his own folder, compares them with your report, and signs off on the Final report item ("Accepted by: <first name>", or findings). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Metrics pipelines · CloudWatch dashboards · Jira REST integration · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Lambda · DynamoDB · S3 · Glue · Athena · CloudWatch · SES · Jira

**Deliverable:** A tested metrics layer in the `grc-metrics` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An engineer building program metrics and board reporting without a paid BI tool.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
