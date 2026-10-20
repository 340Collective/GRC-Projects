# 340 Collective Gap Analysis (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-5](https://340collective.atlassian.net/browse/GRC-5) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 04 340 Collective Gap Analysis |
| Your role | Jason (Internal Auditor), lead for 04: scope, control matrix, scoring rules, and the gap report |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. Your sign-off is a pass or findings record, never an approval. Adam validates the build, and Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 3, 1 point (S, the monthly scoring run only) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-5](https://340collective.atlassian.net/browse/GRC-5) |
| Mirrored folder | [engineering/Rasheed-04-Gap-Analysis](../../engineering/Rasheed-04-Gap-Analysis/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You lead 04: scope, control matrix, scoring rules, and the gap report. Work with Rasheed, who builds only the monthly scoring run. Give him the inputs at the Day 1 kickoff, then run the acceptance test and record the result here.

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

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-5](https://340collective.atlassian.net/browse/GRC-5).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Config rule evaluations and Security Hub checks bill per evaluation; run the scorer by hand during the test instead of waiting a month.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Rasheed removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

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
