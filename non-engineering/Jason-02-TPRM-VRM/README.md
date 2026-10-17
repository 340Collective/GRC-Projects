# Third-Party and Vendor Risk Management (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 02 Third-Party and Vendor Risk Management |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 requirements. Your acceptance test is a pass or findings record, not an approval. Adam (ISSO) validates the build and Faris gives final approval. |
| Phase | Phase 3, 2 points (M) |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Maria-02-TPRM-VRM](../../engineering/Maria-02-TPRM-VRM/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the vendor questionnaire, weights, and tier rules. Work with Maria. Give her the inputs by Handoff 1, then run the acceptance test on her build and record pass or findings.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md).

- Define requirements: 4 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: vendor questionnaire, weights, and tier rules, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: vendor intake and scoring pipeline ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: three-vendor scorecard and vendor risk report, Jason to Faris (Jira Task, created by Jason)

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

Textract (per page) and Comprehend (per unit of text) are the cost drivers; test with a few synthetic pages.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Maria tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC9.2, ISO 27001:2022 A.5.19 to A.5.22, NIST CSF 2.0 GV.SC.

</details>

## About the project

A vendor risk program: a questionnaire, a weighted score, and a risk tier with a reassessment date for each vendor. It supports SOC 2 CC9.2, ISO 27001:2022 A.5.19 to A.5.22, and NIST CSF 2.0 GV.SC.

Status: target design, not yet deployed.

![Third-Party and Vendor Risk Management AWS architecture](../../engineering/Maria-02-TPRM-VRM/diagram/tprm-vrm-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-02-TPRM-VRM/README.md) | The build view: design, moving parts, and regenerate commands |
| [TPRM-VRM-Architecture.md](../../engineering/Maria-02-TPRM-VRM/TPRM-VRM-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md) | Maria's lab steps, with the same handoffs as yours |
