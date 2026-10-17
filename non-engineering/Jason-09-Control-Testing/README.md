# Control Testing and Assessment (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 09 Control Testing and Assessment |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris (ISSM) accepts your Handoff 1 requirements. Your acceptance test is a pass or findings record, not an approval. Adam (ISSO) validates the build and Faris gives final approval. |
| Phase | Phase 3, 2 points (M) |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Rasheed-09-Control-Testing](../../engineering/Rasheed-09-Control-Testing/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the 10-control test plan and the internal audit report. Work with Rasheed. Give him the plan by Handoff 1, then run the acceptance test on his build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md).

- Define requirements: 4 steps
- Hand over inputs: 1 step
- Accept the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: 10-control test plan and procedures, Jason to Rasheed (Jira Task, created by Jason)
- Handoff 2: test automation and sampling ready for acceptance testing, Rasheed to Jason (Jira Task, created by Rasheed)
- Handoff 3: internal audit report, Jason to Faris (Jira Task, created by Jason)

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

There is no significant cost driver; Athena scans stay small with partitions.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Rasheed tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 readiness and NIST SP 800-53A style assessment.

</details>

## About the project

A mock internal audit that tests 10 controls for design and operating effectiveness and produces workpapers and a report. It supports SOC 2 readiness and NIST SP 800-53A style assessment.

Status: target design, not yet deployed.

![Control Testing and Assessment AWS architecture](../../engineering/Rasheed-09-Control-Testing/diagram/control-testing-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-09-Control-Testing/README.md) | The build view: design, moving parts, and regenerate commands |
| [Control-Testing-Architecture.md](../../engineering/Rasheed-09-Control-Testing/Control-Testing-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md) | Rasheed's lab steps, with the same handoffs as yours |
