# GRC Metrics and Board Reporting (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-13](https://340collective.atlassian.net/browse/GRC-13) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 12 GRC Metrics and Board Reporting |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. You sign off and record your validation on the Final report item. Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 4, 2 points (M); needs data from 06, 11, and 07 |
| Week | Week 4, Nov 9 to 15, 2026 |
| Jira epic | [GRC-13](https://340collective.atlassian.net/browse/GRC-13) |
| Mirrored folder | [engineering/Rasheed-12-Metrics-Reporting](../../engineering/Rasheed-12-Metrics-Reporting/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the metric definitions and the board pack. Work with Rasheed. Give him definitions, targets, and thresholds at the Day 1 kickoff, then test his build and record your results here. You read results on the GRC Metrics Jira issue and your Jira dashboard.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md).

- Define requirements: 4 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-13](https://340collective.atlassian.net/browse/GRC-13).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.
- Jira path 3: the daily KRI and KPI job posts its results to the "GRC Metrics" Jira issue, as a comment or custom fields.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

0 dollars day to day: the CloudWatch free tier, free Jira, and SES for the board pack.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Rasheed removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

ISO 27001:2022 clauses 9.1 and 9.3, NIST CSF 2.0 GV.OV, SOC 2 CC4.1.

</details>

## About the project

KRIs, KPIs, and a monthly board pack built from the other projects' records, with no paid dashboard: a CloudWatch trend view for engineers, the GRC Metrics Jira issue for you, and an emailed board pack. It supports ISO 27001:2022 clauses 9.1 and 9.3, NIST CSF 2.0 GV.OV, and SOC 2 CC4.1.

Status: target design, not yet deployed.

![GRC Metrics and Board Reporting AWS architecture](../../engineering/Rasheed-12-Metrics-Reporting/diagram/grc-metrics-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-12-Metrics-Reporting/README.md) | The build view: design, moving parts, and regenerate commands |
| [GRC-Metrics-Architecture.md](../../engineering/Rasheed-12-Metrics-Reporting/GRC-Metrics-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md) | Rasheed's lab steps, mirrored with yours |
