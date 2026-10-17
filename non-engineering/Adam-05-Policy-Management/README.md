# 340 Collective Policy Management (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 05 340 Collective Policy Management |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 requirements. You accept and validate the build in Jira; Faris gives final approval. |
| Phase | Phase 5, 1 point (S) |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Maria-05-Policy-Management](../../engineering/Maria-05-Policy-Management/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the six policies and their review cycle. Work with Maria. Give her the drafts by Handoff 1, then accept her build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md).

- Define requirements: 5 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 2 steps
- Assess or report: 1 step

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: six policy drafts with header block and review cycle, Adam to Maria (Jira Task, created by Adam)
- Handoff 2: policy-as-code pipeline and attestation tracking ready for acceptance, Maria to Adam (Jira Task, created by Maria)
- Handoff 3: attestation results and review-cycle schedule, Adam to Faris (Jira Task, created by Adam)

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

CodeBuild build minutes are the only real cost; keep test builds few.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Maria tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, NIST CSF 2.0 GV.PO.

</details>

## About the project

340 Collective's security policies as versioned Markdown, reviewed by pull request, with attestation tracking and review reminders. It supports SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, and NIST CSF 2.0 GV.PO.

Status: target design, not yet deployed.

![340 Collective Policy Management AWS architecture](../../engineering/Maria-05-Policy-Management/diagram/policy-management-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-05-Policy-Management/README.md) | The build view: design, moving parts, and regenerate commands |
| [Policy-Management-Architecture.md](../../engineering/Maria-05-Policy-Management/Policy-Management-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md) | Maria's lab steps, with the same handoffs as yours |
