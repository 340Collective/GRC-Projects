# GRC Metrics and Board Reporting (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 12 GRC Metrics and Board Reporting |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 requirements. You accept and validate the build in Jira; Faris gives final approval. |
| Phase | Phase 4, 2 points (M); needs data from 06, 11, and 07 |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Rasheed-12-Metrics-Reporting](../../engineering/Rasheed-12-Metrics-Reporting/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the metric definitions and the board pack. Work with Rasheed. Give him definitions, targets, and thresholds by Handoff 1, then accept his build. You read results on the GRC Metrics Jira issue and your Jira dashboard.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md).

- Define requirements: 4 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: metric definitions, targets, and thresholds, Adam to Rasheed (Jira Task, created by Adam)
- Handoff 2: metrics dashboard ready for acceptance, Rasheed to Adam (Jira Task, created by Rasheed)
- Handoff 3: board pack export with commentary, Adam to Faris (Jira Task, created by Adam)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- You record requirements, acceptance, and reports on the Tasks. You do not open or review pull requests; engineers keep this page current.
- Jira path 3: the daily KRI and KPI job posts its results to the "GRC Metrics" Jira issue, as a comment or custom fields.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

0 dollars day to day: the CloudWatch free tier, free Jira, and SES for the board pack.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Rasheed tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-12-Metrics-Reporting/README.md) | The build view: design, moving parts, and regenerate commands |
| [GRC-Metrics-Architecture.md](../../engineering/Rasheed-12-Metrics-Reporting/GRC-Metrics-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md) | Rasheed's lab steps, with the same handoffs as yours |
