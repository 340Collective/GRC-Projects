# Identity and Access (Okta) (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-15](https://340collective.atlassian.net/browse/GRC-15) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 14 Identity and Access (Okta) |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Abdifatah (IAM / Identity Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. You sign off and record your validation on the Final report item. Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 1, 2 points (M) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-15](https://340collective.atlassian.net/browse/GRC-15) |
| Mirrored folder | [engineering/Abdifatah-14-Identity-Access](../../engineering/Abdifatah-14-Identity-Access/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the Okta group model, the deviation record, and the identity export for 08. Work with Abdifatah. Give him the group model at the Day 1 kickoff, then test his build and record your results here.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md).

- Define requirements: 3 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 1 step
- Assess or report: 3 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Abdifatah agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Abdifatah as needed, or comment on the project item.
- Day 7 sign-off: Abdifatah commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-15](https://340collective.atlassian.net/browse/GRC-15).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

0 dollars on the Okta, GitHub, and Jira free plans.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Abdifatah removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC6.1 to CC6.3, ISO 27001:2022 A.5.15 to A.5.18 and A.8.5, NIST CSF 2.0 PR.AA.

</details>

## About the project

Okta as the team's sign-in launch point for AWS, GitHub, and Jira, without single sign-on (recorded as a deviation), with joiner and leaver workflows and an identity export for 08. It supports SOC 2 CC6.1 to CC6.3, ISO 27001:2022 A.5.15 to A.5.18 and A.8.5, and NIST CSF 2.0 PR.AA.

Status: target design, not yet deployed.

![Identity and Access (Okta) architecture](../../engineering/Abdifatah-14-Identity-Access/diagram/identity-access-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Abdifatah-14-Identity-Access/README.md) | The build view: design, moving parts, and regenerate commands |
| [Identity-Access-Architecture.md](../../engineering/Abdifatah-14-Identity-Access/Identity-Access-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md) | Abdifatah's lab steps, mirrored with yours |
