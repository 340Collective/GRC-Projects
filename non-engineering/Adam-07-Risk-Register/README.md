# Risk Register (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-8](https://340collective.atlassian.net/browse/GRC-8) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 07 Risk Register |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. You sign off and record your validation on the Final report item. Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-8](https://340collective.atlassian.net/browse/GRC-8) |
| Mirrored folder | [engineering/Rasheed-07-Risk-Register](../../engineering/Rasheed-07-Risk-Register/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the risk scoring rules and the register. Work with Rasheed. Give him the rules and the seed register at the Day 1 kickoff, then test his build and record your results here.

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

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-8](https://340collective.atlassian.net/browse/GRC-8).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

There is no paid dashboard; Cognito, API Gateway, Lambda, DynamoDB, and Athena stay at or near the free tier.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Rasheed removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

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
