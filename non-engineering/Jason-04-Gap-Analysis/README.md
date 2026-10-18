# 340 Collective Gap Analysis (non-engineering)

You work in Jira. Your epic: [GRC-5](https://340collective.atlassian.net/browse/GRC-5). This page is reference.

| Field | Value |
| --- | --- |
| Project | 04 340 Collective Gap Analysis |
| Your role | Jason (Internal Auditor), lead for 04: scope, control matrix, scoring rules, and the gap report |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. Your acceptance test is a pass or findings record, not an approval. Adam validates the build and Faris gives final approval. |
| Phase | Phase 3, 1 point (S, the monthly scoring run only) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-5](https://340collective.atlassian.net/browse/GRC-5) |
| Mirrored folder | [engineering/Rasheed-04-Gap-Analysis](../../engineering/Rasheed-04-Gap-Analysis/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You lead 04: scope, control matrix, scoring rules, and the gap report. Work with Rasheed, who builds only the monthly scoring run. Give him the inputs at the Day 1 kickoff, then run the acceptance test.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md).

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

- Epic: [GRC-5](https://340collective.atlassian.net/browse/GRC-5).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Config rule evaluations and Security Hub checks bill per evaluation; run the scorer by hand during the test instead of waiting a month.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Rasheed tears the build down after sign-off and approval.
- Confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 (2017 TSC), NIST CSF 2.0, and ISO 27001:2022 Annex A, from one crosswalked library.

</details>

## About the project

A repeatable gap analysis against SOC 2 (2017 TSC), NIST CSF 2.0, and ISO 27001:2022 Annex A from one crosswalked control library, with a monthly scoring run.

Status: target design, not yet deployed.

![340 Collective Gap Analysis AWS architecture](../../engineering/Rasheed-04-Gap-Analysis/diagram/gap-analysis-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-04-Gap-Analysis/README.md) | The build view: design, moving parts, and regenerate commands |
| [Gap-Analysis-Architecture.md](../../engineering/Rasheed-04-Gap-Analysis/Gap-Analysis-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md) | Rasheed's lab steps, mirrored with yours |
