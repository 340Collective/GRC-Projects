# Audit Engagement Manager (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-11](https://340collective.atlassian.net/browse/GRC-11) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 10 Audit Engagement Manager |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. Your sign-off is a pass or findings record, never an approval. Adam validates the build, and Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-11](https://340collective.atlassian.net/browse/GRC-11) |
| Mirrored folder | [engineering/Maria-10-Audit-Engagement-Manager](../../engineering/Maria-10-Audit-Engagement-Manager/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You run the mock engagement: the PBC list, the findings log, and the status summary. Work with Maria. Give her the template and SLA rules at the Day 1 kickoff, then run the acceptance test and record the result here.

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

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-11](https://340collective.atlassian.net/browse/GRC-11).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Costs stay near zero at one engagement at a time.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Maria removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

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
