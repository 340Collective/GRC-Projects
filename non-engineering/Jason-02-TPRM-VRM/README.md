# Third-Party and Vendor Risk Management (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-3](https://340collective.atlassian.net/browse/GRC-3) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 02 Third-Party and Vendor Risk Management |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. Your sign-off is a pass or findings record, never an approval. Adam validates the build, and Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 4, 2 points (M) |
| Week | Week 4, Nov 9 to 15, 2026 |
| Jira epic | [GRC-3](https://340collective.atlassian.net/browse/GRC-3) |
| Mirrored folder | [engineering/Maria-02-TPRM-VRM](../../engineering/Maria-02-TPRM-VRM/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the vendor questionnaire, weights, and tier rules. Work with Maria. Give her the inputs at the Day 1 kickoff, then run the acceptance test on her build and record pass or findings here.

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

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-3](https://340collective.atlassian.net/browse/GRC-3).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

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
