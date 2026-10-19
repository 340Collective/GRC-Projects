# Control Testing and Assessment (non-engineering)

You work in Jira. Your epic: [GRC-10](https://340collective.atlassian.net/browse/GRC-10). This page is reference.

| Field | Value |
| --- | --- |
| Project | 09 Control Testing and Assessment |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 3, 2 points (M) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-10](https://340collective.atlassian.net/browse/GRC-10) |
| Mirrored folder | [engineering/Rasheed-09-Control-Testing](../../engineering/Rasheed-09-Control-Testing/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the 10-control test plan and the internal audit report. Work with Rasheed. Give him the plan at the Day 1 kickoff, then run the acceptance test on his build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md).

- Define requirements: 4 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 2 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-10](https://340collective.atlassian.net/browse/GRC-10).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

There is no significant cost driver; Athena scans stay small with partitions.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown (final week)</summary>

- Rasheed keeps the build deployed after sign-off and approval, and tears it down in the program's final week (Nov 23 to 25, 2026).
- In the final week, confirm on the project item that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-09-Control-Testing/README.md) | The build view: design, moving parts, and regenerate commands |
| [Control-Testing-Architecture.md](../../engineering/Rasheed-09-Control-Testing/Control-Testing-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md) | Rasheed's lab steps, mirrored with yours |
