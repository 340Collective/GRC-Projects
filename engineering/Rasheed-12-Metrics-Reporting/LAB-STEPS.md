# GRC Metrics and Board Reporting - Lab Steps (engineering)

Build, test, and tear down the GRC Metrics and Board Reporting design on AWS as a temporary stack. The stack stays deployed after sign-off and is torn down in the program's final week. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-12-Metrics-Reporting/LAB-STEPS.md](../../non-engineering/Adam-12-Metrics-Reporting/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](GRC-Metrics-Architecture.md) and agree scope and requirements with Adam at the Day 1 kickoff before you write any template.
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
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his test result and validation on the project item, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## Tear down (final week)

1. Do not tear down at Day 7. After the partner's sign-off and final approval are on the Final report item, the stack stays deployed and you move to your next project. Tear down in the program's final week (Nov 23 to 25, 2026; see [GOVERNANCE.md](../../GOVERNANCE.md#final-week)).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-metrics` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Revoke the Jira API token and delete its `/grc/` parameter.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

**Skills:** Metrics pipelines · CloudWatch dashboards · Jira REST integration · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · Lambda · DynamoDB · S3 · Glue · Athena · CloudWatch · SES · Jira

**Deliverable:** A tested metrics layer in the `grc-metrics` stack, signed off on the Final report item, and torn down with evidence in the program's final week.

**What it simulates:** An engineer building program metrics and board reporting without a paid BI tool.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, keeps it deployed after sign-off, and tears it down in the program's final week; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
