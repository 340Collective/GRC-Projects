# AWS Continuous Monitoring and Notifications - Lab Steps (engineering)

Build, test, and tear down the AWS Continuous Monitoring and Notifications design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Rasheed (ISSE / Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-15-AWS-ConMon/LAB-STEPS.md](../../non-engineering/Adam-15-AWS-ConMon/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](AWS-ConMon-Architecture.md) and agree scope and requirements with Adam at the Day 1 kickoff before you write any template.
2. Turn Adam's ConMon plan (agreed at kickoff) into the EventBridge rule patterns, the severity routing, and the SLA due dates (critical 15 days, high 30, medium 90).
3. 01 owns the Security Hub hub and its control-finding tickets; 15 adds routing, notifications, SLAs, the digest, the dashboard, and the report. Do not duplicate 01's tickets. Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html). Use the finding ID as the dedupe key.
4. Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook. Use it for the CloudTrail and Config events and for findings the native integration does not cover.
5. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
6. No email addresses in git: the SNS subscription address is a template parameter with an empty default, and subscribers confirm out of band.
7. GuardDuty: planned, enabled later as code with owner approval. If the owner approves it, enable it in a GRC infrastructure template under `infrastructure/cloudformation/` with the optional protection plans off (S3 Protection, EKS, Malware Protection, RDS, Lambda, Runtime Monitoring, and AI Protection). Start on the 30-day free trial and read GuardDuty's projected cost estimate in the console during the trial before deciding to keep it on.
8. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
9. Plan to stay under 10 dollars a month: about 0 to 1 dollar a month: AWS service events on the default bus are free, SNS email and Lambda stay in their free tiers, one CloudWatch dashboard is free, and the connection secret is about 0.40 dollars.

## Deploy

1. Write `infrastructure/cloudformation/grc-conmon.yaml` in this repo, in the build order from the architecture doc:
   - SNS topic (empty subscription parameter), the SQS dead-letter queue, and the DLQ alarm.
   - EventBridge rules for Security Hub, CloudTrail, and Config, with retries and the DLQ.
   - The Jira path: the native Security Hub integration where it fits, otherwise the API destination and connection with the dedupe key.
   - Daily digest and monthly report Lambda on EventBridge Scheduler.
   - The CloudWatch dashboard.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Maria does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-conmon` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Raise a test HIGH finding: one Jira issue opens with the severity, resource, SLA due date, and finding ID, and a repeat updates the same issue.
2. A CRITICAL test event sends one email to a confirmed subscriber; a MEDIUM test event sends none.
3. Point one target at a bad endpoint: the event lands in the dead-letter queue and the DLQ alarm fires.
4. Run the digest and the monthly report by hand: both arrive, and the report KPIs reach the GRC Metrics Jira issue.
5. Prove each control from the architecture doc's security section holds:
   - Least-privilege IAM: the digest and report Lambda reads Security Hub findings and posts only to its own topic; the API destination role can invoke only the one destination.
   - No email addresses, tokens, or account IDs in the template or in git; the subscription address is a parameter and the Jira credential sits in the EventBridge connection.
   - The DLQ and the topic are encrypted with the KMS key tagged `grc-project`.
   - CloudTrail records every rule, target, and subscription change.
   - No Object Lock and no permanent data.
   - Human approval points: Faris approves the stack; Adam accepts the build and each monthly report; Maria reviews the code.
6. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his test result and validation on the project item, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## Tear down

1. Tear down after the partner's sign-off and final approval are on the Final report item, before the phase ends.
2. Delete the `grc-conmon` stack from clean `main` and wait for `DELETE_COMPLETE`.
3. Confirm no SNS subscription is left, and delete the dead-letter queue if it was retained.
4. Disable GuardDuty if it was enabled for the lab, unless the owner keeps it on.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Continuous monitoring design · EventBridge routing · Jira integration · SNS notifications · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · EventBridge · SNS · SQS · Lambda · CloudWatch · Security Hub · Jira

**Deliverable:** A tested ConMon routing and notification layer in the `grc-conmon` stack, signed off on the Final report item, and torn down with evidence.

**What it simulates:** An engineer turning a continuous monitoring plan into automated routing, notifications, and POA&M tracking.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
