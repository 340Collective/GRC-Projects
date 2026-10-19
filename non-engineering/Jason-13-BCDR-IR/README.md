# BC/DR and Incident Response Compliance (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-14](https://340collective.atlassian.net/browse/GRC-14) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 13 BC/DR and Incident Response Compliance |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Rasheed (ISSE / Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. Your sign-off is a pass or findings record, never an approval. Adam validates the build, and Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 1, 2 points (M) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-14](https://340collective.atlassian.net/browse/GRC-14) |
| Mirrored folder | [engineering/Rasheed-13-BCDR-IR](../../engineering/Rasheed-13-BCDR-IR/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the IR plan, the tabletop, and the BC/DR test record. Work with Rasheed. Give him the requirements and RTO and RPO targets at the Day 1 kickoff, then run the acceptance test and record the result here.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Rasheed-13-BCDR-IR/LAB-STEPS.md).

- Define requirements: 3 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 3 steps
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-14](https://340collective.atlassian.net/browse/GRC-14).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

AWS Backup storage and restores, and the temporary restored copy; keep restores small and delete them at the end of each test.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Rasheed removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 A1.2, A1.3, CC7.4, and CC7.5; ISO 27001:2022 A.5.24 to A.5.30; NIST CSF 2.0 RS and RC.

</details>

## About the project

Proof that backups restore and that incident response is practiced: an IR plan, a tabletop, and a BC/DR test record with RTO and RPO. It supports SOC 2 A1.2, A1.3, CC7.4, and CC7.5; ISO 27001:2022 A.5.24 to A.5.30; and NIST CSF 2.0 RS and RC.

Status: target design, not yet deployed.

![BC/DR and Incident Response Compliance AWS architecture](../../engineering/Rasheed-13-BCDR-IR/diagram/bcdr-ir-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Rasheed-13-BCDR-IR/README.md) | The build view: design, moving parts, and regenerate commands |
| [BCDR-IR-Architecture.md](../../engineering/Rasheed-13-BCDR-IR/BCDR-IR-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Rasheed-13-BCDR-IR/LAB-STEPS.md) | Rasheed's lab steps, mirrored with yours |
