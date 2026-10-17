# AWS Continuous Monitoring and Notifications Architecture

## Purpose

A NIST CA-7 style continuous monitoring (ConMon) layer built only on native AWS services. It defines what is monitored, at what severity, how often, who is notified, and how each finding becomes tracked remediation (a POA&M item) in Jira. Everything is CloudFormation, everything is temporary, and the day-to-day cost is near zero.

Status: target design, not yet deployed.

## How 15 differs from 01

- 01 owns the Security Hub hub and the one-ticket-per-event pattern for control findings.
- 15 adds the ConMon plan on top: severity routing, email notifications, a daily digest, SLA tracking, the CloudWatch dashboard, and the monthly ConMon report. It reads what 01 and 11 already produce; it does not rebuild them.

## Scope and frameworks

- NIST SP 800-53: CA-7 (continuous monitoring), RA-5 (vulnerability monitoring), SI-2 (flaw remediation), SI-4 (system monitoring), IR-4 (incident handling), CA-5 (plan of action and milestones).
- SOC 2 (2017 TSC) CC7.1 to CC7.3 (detection and evaluation of security events) and CC4.2 (communicating deficiencies).
- ISO 27001:2022 A.8.8 (technical vulnerabilities) and A.8.16 (monitoring activities).
- NIST CSF 2.0 DE.CM (continuous monitoring) and RS.MA (incident management).

## Sources (account state checked 2026-10-17)

| Source | State | What 15 uses |
| --- | --- | --- |
| Security Hub | Enabled | Aggregated findings from Inspector, Config, and GuardDuty if enabled |
| Inspector | Enabled for EC2, Lambda, and ECR | Vulnerability findings, through Security Hub |
| GuardDuty | Not enabled (owner decision) | If approved, an engineer enables it as code in the build phase, with the optional paid protection plans off |
| AWS Config | In use by 11 guardrails | Rule compliance changes |
| CloudTrail | Management events on the existing trail | Specific API calls through EventBridge rules |

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | Security Hub, Inspector, Config, CloudTrail (GuardDuty if enabled) | Findings, compliance changes, and API calls |
| Routing | EventBridge rules, SQS dead-letter queue | Rules match the ConMon events; failed deliveries go to the DLQ |
| Ticketing | EventBridge API destination and connection, Secrets Manager | One Jira remediation issue per finding, with a dedupe key |
| Notification | SNS | Real-time email for CRITICAL and HIGH only |
| Reporting | EventBridge Scheduler, Lambda, SNS (or the existing SES setup) | A daily digest and a monthly ConMon report |
| Monitoring | CloudWatch dashboard and alarms | Findings by severity, SLA breaches, failed invocations, DLQ depth, Config compliance |

## Stage details

### EventBridge rules

- Security Hub `Security Hub Findings - Imported`, filtered to `Severity.Label` CRITICAL or HIGH, `Workflow.Status` NEW, and `RecordState` ACTIVE.
- CloudTrail through EventBridge: `ConsoleLogin` without MFA, any root user activity, IAM user, access key, and policy changes, `StopLogging`, `DeleteTrail`, and policy changes on log buckets.
- Config: rule compliance changes to `NON_COMPLIANT`.
- Every target has a retry policy and an SQS dead-letter queue.

### Jira

- Where it fits, findings use the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html), so 15 does not duplicate what 01 already sends.
- Otherwise an EventBridge API destination posts to a Jira Automation incoming webhook (or the Jira REST API). The issue carries the severity, the resource, the SLA due date (critical 15 days, high 30 days, medium 90 days), and a dedupe key (the finding ID), so a repeat finding updates the same issue.
- The connection credential lives in Secrets Manager through the EventBridge connection. Never put tokens in git. Secrets Manager is on the access model's budget-breaker deny list today, so confirm the EventBridge-managed connection secret is allowed, or raise an access-change PR first.
- Do not use the AWS Service Management Connector; AWS retires it after 2027-03-31.
- Adam and Jason keep a Jira dashboard over the remediation issues.

### Email

- One SNS topic with email subscriptions for CRITICAL and HIGH events in real time.
- Subscribers confirm out of band. No addresses go in git: the subscription address is a template parameter with an empty default.
- Mediums and lows never email per event.
- A daily Lambda run (EventBridge Scheduler) sends one digest: counts by severity, new and closed, and SLA breaches, through SNS or the existing SES setup.

### Dashboard

One CloudWatch dashboard inside the free tier: findings by severity, SLA breaches, notification failures (EventBridge `FailedInvocations` and DLQ depth), and Config compliance.

### Reliability

An SQS dead-letter queue on every EventBridge target, a CloudWatch alarm on DLQ depth, and retry policies on the targets.

### Monthly ConMon report

A monthly Lambda run builds an HTML or Markdown report (open findings by severity, mean time to remediate, SLA breaches, new versus closed, and the top recurring findings), emails it, and posts the KPIs to the GRC Metrics Jira issue that project 12 maintains. Adam accepts it as POA&M evidence.

## Security and privacy controls

- Least-privilege IAM: the digest and report Lambda reads Security Hub findings and posts only to its own topic; the API destination role can invoke only the one destination.
- No email addresses, tokens, or account IDs in the template or in git; the subscription address is a parameter and the Jira credential sits in the EventBridge connection.
- The DLQ and the topic are encrypted with the KMS key tagged `grc-project`.
- CloudTrail records every rule, target, and subscription change.
- No Object Lock and no permanent data.
- Human approval points: Faris approves the stack; Adam accepts the build and each monthly report; Alex reviews the code.

## 340 Collective testbed

340 Collective's real Security Hub, Inspector, Config, and CloudTrail activity is the data. Validation is a test finding that opens one Jira issue (and only one on repeat), a CRITICAL test event that sends one email, a forced delivery failure that lands in the DLQ and raises the alarm, and one digest and one report delivered.

## Cost note

Expected about 0 to 1 dollar a month.

| Item | Pricing basis | Expected monthly cost |
| --- | --- | --- |
| EventBridge rules on AWS service events | No charge for AWS service events on the default bus | 0 |
| EventBridge API destination | Per invocation, a fraction of a cent at this volume | about 0 |
| Secrets Manager (the connection's secret) | 0.40 dollars per secret per month | about 0.40 |
| SNS email | Free tier covers the first 1,000 email notifications a month | 0 |
| Lambda and EventBridge Scheduler | Free tier at a daily and monthly cadence | 0 |
| CloudWatch | One dashboard and a few alarms, inside the free tier | 0 |
| SQS dead-letter queue | Free tier | 0 |

Sources: [EventBridge pricing](https://aws.amazon.com/eventbridge/pricing/), [Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing/), [SNS pricing](https://aws.amazon.com/sns/pricing/), [Lambda pricing](https://aws.amazon.com/lambda/pricing/), and [CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/), checked October 2026. Confirm with the AWS Pricing Calculator before deploying. Inspector's existing EC2, Lambda, and ECR scanning is already billed per resource scanned; that is an owner item to confirm, not a cost this build adds. GuardDuty, if the owner enables it, is billed separately.

## Build order

1. The ConMon plan from Adam (Handoff 1): sources, severity routing, notification list, and SLAs.
2. SNS topic (empty subscription parameter), the SQS dead-letter queue, and the DLQ alarm.
3. EventBridge rules for Security Hub, CloudTrail, and Config, with retries and the DLQ.
4. The Jira path: the native Security Hub integration where it fits, otherwise the API destination and connection with the dedupe key.
5. Daily digest and monthly report Lambda on EventBridge Scheduler.
6. The CloudWatch dashboard.

## Teardown

1. Delete the `grc-conmon` stack from clean `main`: the rules, targets, API destination, connection and its secret, topic, queue, Lambda, schedules, and dashboard go with it.
2. Unsubscribe and confirm no SNS subscription is left; delete the DLQ if it was retained.
3. Disable GuardDuty if it was enabled for the lab, unless the owner keeps it on.
4. Record teardown evidence where the ISSM designates, outside git, and note it on the Jira epic.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md) (the Security Hub hub and control-finding tickets)
- [11 Compliance-as-Code Guardrails](../Alex-11-Compliance-as-Code-Guardrails/README.md) (Config rules)
- [12 GRC Metrics and Board Reporting](../Rasheed-12-Metrics-Reporting/README.md) (the GRC Metrics Jira issue)
- [13 BC/DR and Incident Response](../Rasheed-13-BCDR-IR/README.md) (IR runbooks for what ConMon raises)
