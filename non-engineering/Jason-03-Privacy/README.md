# Privacy Operations (non-engineering)

You work in Jira. Your epic: [GRC-4](https://340collective.atlassian.net/browse/GRC-4). This page is reference.

| Field | Value |
| --- | --- |
| Project | 03 Privacy Operations |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your Handoff 1 requirements. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 3, 2 points (M) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-4](https://340collective.atlassian.net/browse/GRC-4) |
| Mirrored folder | [engineering/Maria-03-Privacy](../../engineering/Maria-03-Privacy/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the RoPA, the PII inventory, and the DSAR runbook. Work with Maria. Give her the requirements by Handoff 1, then run the acceptance test on her build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-03-Privacy/LAB-STEPS.md).

- Define requirements: 5 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 2 steps
- Assess or report: 1 step

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: RoPA fields, PII inventory, and DSAR runbook requirements, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: PII discovery and DSAR workflow ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: synthetic DSAR walkthrough and consent register, Jason to Faris (Jira Task, created by Jason)

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-4](https://340collective.atlassian.net/browse/GRC-4).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- You record requirements, acceptance, and reports on the Tasks. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Macie would be the main cost; with synthetic records and a scoped Lambda the rest stays at or near the free tier.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Maria tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

GDPR, CCPA, and CPRA privacy operations (RoPA, DSAR, consent).

</details>

## About the project

Privacy operations for GDPR, CCPA, and CPRA: a record of processing activities, a PII inventory, consent records, and data subject requests answered inside the legal deadline.

Status: target design, not yet deployed.

![Privacy Operations AWS architecture](../../engineering/Maria-03-Privacy/diagram/privacy-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-03-Privacy/README.md) | The build view: design, moving parts, and regenerate commands |
| [Privacy-Architecture.md](../../engineering/Maria-03-Privacy/Privacy-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-03-Privacy/LAB-STEPS.md) | Maria's lab steps, with the same handoffs as yours |
