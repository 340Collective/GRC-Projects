# AWS Continuous Monitoring and Notifications (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 15 AWS Continuous Monitoring and Notifications |
| Your role | Adam (ISSO), owns the ConMon plan and operates it: daily triage, weekly SLA review, monthly report |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 plan. You accept and validate the build in Jira, and accept each monthly report; Faris gives final approval. Jason (Internal Auditor) assesses in Phase 4. |
| Phase | Phase 4, 2 points (M); needs findings from 01 and 11, and posts to 12's GRC Metrics issue |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Rasheed-15-AWS-ConMon](../../engineering/Rasheed-15-AWS-ConMon/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the ConMon plan and run it: what is monitored, at what severity, who is notified, and the remediation SLAs. Work with Rasheed. Give him the plan by Handoff 1, accept his build, then triage the Jira remediation queue every day and accept each monthly ConMon report as POA&M evidence.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md).

- Define requirements: 3 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 4 steps
- Assess or report: 3 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: ConMon plan (sources, severity routing, notification list, and SLAs of 15, 30, and 90 days), Adam to Rasheed (Jira Task, created by Adam)
- Handoff 2: ConMon routing, Jira remediation issues, email alerts, daily digest, and dashboard ready for acceptance, Rasheed to Adam (Jira Task, created by Rasheed)
- Handoff 3: first monthly ConMon report accepted as POA&M evidence, Adam to Faris (Jira Task, created by Adam)
- Handoff 4: ConMon assessment against CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5, Jason to Faris (Jira Task, created by Jason)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- You record requirements, acceptance, and reports on the Tasks. You do not open or review pull requests; engineers keep this page current.
- Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

GuardDuty: planned, enabled later as code with owner approval. The detector goes in a GRC infrastructure template under `infrastructure/cloudformation/` with the optional protection plans off (S3 Protection, EKS, Malware Protection, RDS, Lambda, Runtime Monitoring, and AI Protection). It starts on the 30-day free trial; you read GuardDuty's projected cost estimate in the console with Faris during the trial, before the keep-or-disable decision.

About 0 to 1 dollar a month: AWS service events on the default bus are free, SNS email and Lambda stay in their free tiers, one CloudWatch dashboard is free, and the connection secret is about 0.40 dollars.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Rasheed tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

NIST SP 800-53 CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5; SOC 2 CC7.1 to CC7.3 and CC4.2; ISO 27001:2022 A.8.8 and A.8.16; NIST CSF 2.0 DE.CM.

</details>

## About the project

A NIST CA-7 style continuous monitoring layer on native AWS services. Security Hub (with Inspector and Config), Config, and CloudTrail events route through EventBridge to Jira remediation issues with SLA due dates, critical and high findings email in real time, and a daily digest, a CloudWatch dashboard, and a monthly ConMon report follow. 01 owns the Security Hub hub and its control-finding tickets; 15 adds the ConMon plan, severity routing, notifications, SLA tracking, and the report. It supports NIST SP 800-53 CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5.

Status: target design, not yet deployed.

![AWS Continuous Monitoring and Notifications architecture](../../engineering/Rasheed-15-AWS-ConMon/diagram/aws-conmon-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-15-AWS-ConMon/README.md) | The build view: design, moving parts, and regenerate commands |
| [AWS-ConMon-Architecture.md](../../engineering/Rasheed-15-AWS-ConMon/AWS-ConMon-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md) | Rasheed's lab steps, with the same handoffs as yours |
