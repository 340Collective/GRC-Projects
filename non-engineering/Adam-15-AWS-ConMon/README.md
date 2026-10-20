# AWS Continuous Monitoring and Notifications (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-31](https://340collective.atlassian.net/browse/GRC-31) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 15 AWS Continuous Monitoring and Notifications |
| Your role | Adam (ISSO), owns the ConMon plan and operates it: daily triage, weekly SLA review, monthly report |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. You sign off and record your validation on the Final report item. You also accept each monthly report. Jason assesses in integration week (Nov 23 to 25). Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 5, 2 points (M); needs findings from 01 and 11, and posts to 12's GRC Metrics issue |
| Week | Week 5, Nov 16 to 22, 2026 |
| Jira epic | [GRC-31](https://340collective.atlassian.net/browse/GRC-31) |
| Mirrored folder | [engineering/Rasheed-15-AWS-ConMon](../../engineering/Rasheed-15-AWS-ConMon/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the ConMon plan and run it: what is monitored, at what severity, who is notified, and the remediation SLAs. Work with Rasheed. Give him the plan at the Day 1 kickoff, test his build and record your results here, then triage the Jira remediation queue every day and accept each monthly ConMon report as POA&M evidence.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md).

- Define requirements: 3 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 4 steps
- Assess or report: 3 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-31](https://340collective.atlassian.net/browse/GRC-31).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.
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
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Rasheed removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-15-AWS-ConMon/README.md) | The build view: design, moving parts, and regenerate commands |
| [AWS-ConMon-Architecture.md](../../engineering/Rasheed-15-AWS-ConMon/AWS-ConMon-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md) | Rasheed's lab steps, mirrored with yours |
