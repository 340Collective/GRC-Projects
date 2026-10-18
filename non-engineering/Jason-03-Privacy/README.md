# Privacy Operations (non-engineering)

You work in Jira. Your epic: [GRC-4](https://340collective.atlassian.net/browse/GRC-4). This page is reference.

| Field | Value |
| --- | --- |
| Project | 03 Privacy Operations |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 3, 2 points (M) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-4](https://340collective.atlassian.net/browse/GRC-4) |
| Mirrored folder | [engineering/Maria-03-Privacy](../../engineering/Maria-03-Privacy/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the RoPA, the PII inventory, and the DSAR runbook. Work with Maria. Give her the requirements at the Day 1 kickoff, then run the acceptance test on her build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-03-Privacy/LAB-STEPS.md).

- Define requirements: 5 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 2 steps
- Assess or report: 1 step

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-4](https://340collective.atlassian.net/browse/GRC-4).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Macie would be the main cost; with synthetic records and a scoped Lambda the rest stays at or near the free tier.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Maria tears the build down after sign-off and approval.
- Confirm on the project item that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-03-Privacy/README.md) | The build view: design, moving parts, and regenerate commands |
| [Privacy-Architecture.md](../../engineering/Maria-03-Privacy/Privacy-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-03-Privacy/LAB-STEPS.md) | Maria's lab steps, mirrored with yours |
