# 340 Collective Gap Analysis (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 04 340 Collective Gap Analysis |
| Your role | Jason (Internal Auditor), lead for 04: scope, control matrix, scoring rules, and the gap report |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 requirements. Your acceptance test is a pass or findings record, not an approval. Adam (ISSO) validates the build and Faris gives final approval. |
| Phase | Phase 3, 1 point (S, the monthly scoring run only) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Rasheed-04-Gap-Analysis](../../engineering/Rasheed-04-Gap-Analysis/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You lead 04: scope, control matrix, scoring rules, and the gap report. Work with Rasheed, who builds only the monthly scoring run. Give him the inputs by Handoff 1, then run the acceptance test.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md).

- Define requirements: 5 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: scope summary, control matrix, and scoring rules, Jason to Rasheed (Jira Task, created by Jason)
- Handoff 2: monthly scoring run ready for acceptance testing, Rasheed to Jason (Jira Task, created by Rasheed)
- Handoff 3: scored gap matrix and remediation timeline, Jason to Faris (Jira Task, created by Jason)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- You record requirements, acceptance, and reports on the Tasks. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Config rule evaluations and Security Hub checks bill per evaluation; run the scorer by hand during the test instead of waiting a month.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Rasheed tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 (2017 TSC), NIST CSF 2.0, and ISO 27001:2022 Annex A, from one crosswalked library.

</details>

## About the project

A repeatable gap analysis against SOC 2 (2017 TSC), NIST CSF 2.0, and ISO 27001:2022 Annex A from one crosswalked control library, with a monthly scoring run.

Status: target design, not yet deployed.

![340 Collective Gap Analysis AWS architecture](../../engineering/Rasheed-04-Gap-Analysis/diagram/gap-analysis-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-04-Gap-Analysis/README.md) | The build view: design, moving parts, and regenerate commands |
| [Gap-Analysis-Architecture.md](../../engineering/Rasheed-04-Gap-Analysis/Gap-Analysis-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md) | Rasheed's lab steps, with the same handoffs as yours |
