# Third-Party and Vendor Risk Management (non-engineering)

You work in Jira. Your epic: [GRC-3](https://340collective.atlassian.net/browse/GRC-3). This page is reference.

| Field | Value |
| --- | --- |
| Project | 02 Third-Party and Vendor Risk Management |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 4, 2 points (M) |
| Week | Week 4, Nov 9 to 15, 2026 |
| Jira epic | [GRC-3](https://340collective.atlassian.net/browse/GRC-3) |
| Mirrored folder | [engineering/Maria-02-TPRM-VRM](../../engineering/Maria-02-TPRM-VRM/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the vendor questionnaire, weights, and tier rules. Work with Maria. Give her the inputs at the Day 1 kickoff, then run the acceptance test on her build and record pass or findings.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md).

- Define requirements: 4 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-3](https://340collective.atlassian.net/browse/GRC-3).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Textract (per page) and Comprehend (per unit of text) are the cost drivers; test with a few synthetic pages.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Maria removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-02-TPRM-VRM/README.md) | The build view: design, moving parts, and regenerate commands |
| [TPRM-VRM-Architecture.md](../../engineering/Maria-02-TPRM-VRM/TPRM-VRM-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md) | Maria's lab steps, mirrored with yours |
