# Risk Register (non-engineering)

You work in Jira. Your epic: [GRC-8](https://340collective.atlassian.net/browse/GRC-8). This page is reference.

| Field | Value |
| --- | --- |
| Project | 07 Risk Register |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. You accept and validate the build on the project item; Faris gives final approval. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-8](https://340collective.atlassian.net/browse/GRC-8) |
| Mirrored folder | [engineering/Rasheed-07-Risk-Register](../../engineering/Rasheed-07-Risk-Register/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the risk scoring rules and the register. Work with Rasheed. Give him the rules and the seed register at the Day 1 kickoff, then accept his build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-07-Risk-Register/LAB-STEPS.md).

- Define requirements: 5 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-8](https://340collective.atlassian.net/browse/GRC-8).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

There is no paid dashboard; Cognito, API Gateway, Lambda, DynamoDB, and Athena stay at or near the free tier.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Rasheed tears the build down after sign-off and approval.
- Confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

ISO 27001:2022 clauses 6.1 and 8.2, NIST CSF 2.0 GV.RM and ID.RA, SOC 2 CC3.

</details>

## About the project

A scored risk register with owners, treatments, review dates, and a heat map. It supports ISO 27001:2022 clauses 6.1 and 8.2, NIST CSF 2.0 GV.RM and ID.RA, and SOC 2 CC3.

Status: target design, not yet deployed.

![Risk Register AWS architecture](../../engineering/Rasheed-07-Risk-Register/diagram/risk-register-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [07-risk-register-lab.xlsx](07-risk-register-lab.xlsx) | Lab sheet: risk scoring rules and the seed register (your kickoff input) |
| [Engineering README](../../engineering/Rasheed-07-Risk-Register/README.md) | The build view: design, moving parts, and regenerate commands |
| [Risk-Register-Architecture.md](../../engineering/Rasheed-07-Risk-Register/Risk-Register-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-07-Risk-Register/LAB-STEPS.md) | Rasheed's lab steps, mirrored with yours |
