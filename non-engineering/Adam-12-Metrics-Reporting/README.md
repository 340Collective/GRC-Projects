# GRC Metrics and Board Reporting (non-engineering)

You work in Jira. Your epic: [GRC-13](https://340collective.atlassian.net/browse/GRC-13). This page is reference.

| Field | Value |
| --- | --- |
| Project | 12 GRC Metrics and Board Reporting |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. You accept and validate the build on the project item; Faris gives final approval. |
| Phase | Phase 4, 2 points (M); needs data from 06, 11, and 07 |
| Week | Week 4, Nov 9 to 15, 2026 |
| Jira epic | [GRC-13](https://340collective.atlassian.net/browse/GRC-13) |
| Mirrored folder | [engineering/Rasheed-12-Metrics-Reporting](../../engineering/Rasheed-12-Metrics-Reporting/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the metric definitions and the board pack. Work with Rasheed. Give him definitions, targets, and thresholds at the Day 1 kickoff, then accept his build. You read results on the GRC Metrics Jira issue and your Jira dashboard.

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

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-13](https://340collective.atlassian.net/browse/GRC-13).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.
- Jira path 3: the daily KRI and KPI job posts its results to the "GRC Metrics" Jira issue, as a comment or custom fields.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

0 dollars day to day: the CloudWatch free tier, free Jira, and SES for the board pack.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown (final week)</summary>

- Rasheed keeps the build deployed after sign-off and approval, and tears it down in the program's final week (Nov 23 to 25, 2026).
- In the final week, confirm on the project item that the teardown evidence is recorded.

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
