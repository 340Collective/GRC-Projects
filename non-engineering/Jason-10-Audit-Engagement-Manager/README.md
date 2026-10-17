# Audit Engagement Manager (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 10 Audit Engagement Manager |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your Handoff 1 requirements. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Maria-10-Audit-Engagement-Manager](../../engineering/Maria-10-Audit-Engagement-Manager/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You run the mock engagement: the PBC list, the findings log, and the status summary. Work with Maria. Give her the template and SLA rules by Handoff 1, then run the acceptance test.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md).

- Define requirements: 4 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 1 step
- Assess or report: 2 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: PBC request list template and findings SLA rules, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: engagement tracker build ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: engagement status summary, Jason to Faris (Jira Task, created by Jason)

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

Costs stay near zero at one engagement at a time.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Maria tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 and ISO 27001:2022 audits (clauses 9.2 and 10.2), NIST CSF 2.0 ID.IM.

</details>

## About the project

A mock external audit engagement from the PBC request list through findings and remediation. It supports SOC 2 and ISO 27001:2022 audits (clauses 9.2 and 10.2) and NIST CSF 2.0 ID.IM.

Status: target design, not yet deployed.

![Audit Engagement Manager AWS architecture](../../engineering/Maria-10-Audit-Engagement-Manager/diagram/audit-engagement-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-10-Audit-Engagement-Manager/README.md) | The build view: design, moving parts, and regenerate commands |
| [Audit-Engagement-Architecture.md](../../engineering/Maria-10-Audit-Engagement-Manager/Audit-Engagement-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md) | Maria's lab steps, with the same handoffs as yours |
