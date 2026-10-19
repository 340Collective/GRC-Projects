# Audit Evidence Automation (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-7](https://340collective.atlassian.net/browse/GRC-7) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 06 Audit Evidence Automation |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your REQUIREMENTS.md at the Day 1 kickoff. You sign off and record your validation on the Final report item. Faris gives final approval. Faris reviews and merges your pull requests. |
| Phase | Phase 1, 3 points (L) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-7](https://340collective.atlassian.net/browse/GRC-7) |
| Mirrored folder | [engineering/Maria-06-Evidence-Automation](../../engineering/Maria-06-Evidence-Automation/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the evidence-to-control mapping. Work with Maria. Give her the control list at the Day 1 kickoff, then test her build and record your results here.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-06-Evidence-Automation/LAB-STEPS.md).

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
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-7](https://340collective.atlassian.net/browse/GRC-7).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Config recording, S3 storage (kept small by the 30 and 7 day expiry), and Athena scans are the drivers; partition by date and framework.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Maria removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 and ISO 27001 audit evidence, mapped by control.

</details>

## About the project

Audit evidence collected from AWS on a schedule, hashed, written to a temporary evidence lake with no Object Lock, and mapped to controls so an auditor can query by control. It prepares the program for a SOC 2 or ISO 27001 audit.

Status: target design, not yet deployed.

![Audit Evidence Automation AWS architecture](../../engineering/Maria-06-Evidence-Automation/diagram/evidence-automation-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-06-Evidence-Automation/README.md) | The build view: design, moving parts, and regenerate commands |
| [Evidence-Automation-Architecture.md](../../engineering/Maria-06-Evidence-Automation/Evidence-Automation-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-06-Evidence-Automation/LAB-STEPS.md) | Maria's lab steps, mirrored with yours |
