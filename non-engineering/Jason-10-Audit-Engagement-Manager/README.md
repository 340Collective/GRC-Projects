# Audit Engagement Manager (non-engineering)

You work in Jira. Your epic: [GRC-11](https://340collective.atlassian.net/browse/GRC-11). This page is reference.

| Field | Value |
| --- | --- |
| Project | 10 Audit Engagement Manager |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-11](https://340collective.atlassian.net/browse/GRC-11) |
| Mirrored folder | [engineering/Maria-10-Audit-Engagement-Manager](../../engineering/Maria-10-Audit-Engagement-Manager/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You run the mock engagement: the PBC list, the findings log, and the status summary. Work with Maria. Give her the template and SLA rules at the Day 1 kickoff, then run the acceptance test.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md).

- Define requirements: 4 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 1 step
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-11](https://340collective.atlassian.net/browse/GRC-11).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Costs stay near zero at one engagement at a time.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown (final week)</summary>

- Maria keeps the build deployed after sign-off and approval, and tears it down in the program's final week (Nov 23 to 25, 2026).
- In the final week, confirm on the project item that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-10-Audit-Engagement-Manager/README.md) | The build view: design, moving parts, and regenerate commands |
| [Audit-Engagement-Architecture.md](../../engineering/Maria-10-Audit-Engagement-Manager/Audit-Engagement-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md) | Maria's lab steps, mirrored with yours |
