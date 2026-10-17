# User Access Reviews (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 08 User Access Reviews |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Abdifatah (IAM / Identity Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 requirements. You accept and validate the build in Jira; Faris gives final approval. |
| Phase | Phase 2, 2 points (M) |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Abdifatah-08-Access-Reviews](../../engineering/Abdifatah-08-Access-Reviews/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the access review: the worksheet, the decisions, and the remediation log. Work with Abdifatah. Give him the worksheet columns and review rules by Handoff 1, then accept his build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md).

- Define requirements: 4 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 4 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: certification worksheet columns and review rules, Adam to Abdifatah (Jira Task, created by Adam)
- Handoff 2: access review package build ready for acceptance, Abdifatah to Adam (Jira Task, created by Abdifatah)
- Handoff 3: signed certification worksheet and remediation log, Adam to Faris (Jira Task, created by Adam)

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

The external access analyzer has no charge; the rest stays near the free tier at a quarterly cadence.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Abdifatah tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC6.2 and CC6.3, ISO 27001:2022 A.5.18, NIST CSF 2.0 PR.AA.

</details>

## About the project

A quarterly user access review of the AWS identities, with approver sign-off and a remediation log. It supports SOC 2 CC6.2 and CC6.3, ISO 27001:2022 A.5.18, and NIST CSF 2.0 PR.AA.

Status: target design, not yet deployed.

![User Access Reviews AWS architecture](../../engineering/Abdifatah-08-Access-Reviews/diagram/access-review-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [uar-simulation](../../engineering/Abdifatah-08-Access-Reviews/uar-simulation/README.md) | Synthetic practice dataset for the access review (kept in the engineering folder) |
| [Engineering README](../../engineering/Abdifatah-08-Access-Reviews/README.md) | The build view: design, moving parts, and regenerate commands |
| [Access-Review-Architecture.md](../../engineering/Abdifatah-08-Access-Reviews/Access-Review-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md) | Abdifatah's lab steps, with the same handoffs as yours |
