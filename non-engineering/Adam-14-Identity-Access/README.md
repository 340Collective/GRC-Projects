# Identity and Access (Okta) (non-engineering)

You work in Jira. Your epic: [GRC-15](https://340collective.atlassian.net/browse/GRC-15). This page is reference.

| Field | Value |
| --- | --- |
| Project | 14 Identity and Access (Okta) |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Abdifatah (IAM / Identity Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. You accept and validate the build on the project item; Faris gives final approval. |
| Phase | Phase 1, 2 points (M) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-15](https://340collective.atlassian.net/browse/GRC-15) |
| Mirrored folder | [engineering/Abdifatah-14-Identity-Access](../../engineering/Abdifatah-14-Identity-Access/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the Okta group model, the deviation record, and the identity export for 08. Work with Abdifatah. Give him the group model at the Day 1 kickoff, then accept his build.

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

- Day 1 kickoff: you and Abdifatah agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Abdifatah as needed, or comment on the project item.
- Day 7 sign-off: Abdifatah fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-15](https://340collective.atlassian.net/browse/GRC-15).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

0 dollars on the Okta, GitHub, and Jira free plans.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown (final week)</summary>

- Abdifatah keeps the build deployed after sign-off and approval, and tears it down in the program's final week (Nov 23 to 25, 2026).
- In the final week, confirm on the project item that the teardown evidence is recorded.

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
