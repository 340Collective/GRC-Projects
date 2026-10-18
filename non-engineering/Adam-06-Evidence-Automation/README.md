# Audit Evidence Automation (non-engineering)

You work in Jira. Your epic: [GRC-7](https://340collective.atlassian.net/browse/GRC-7). This page is reference.

| Field | Value |
| --- | --- |
| Project | 06 Audit Evidence Automation |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. You accept and validate the build on the project item; Faris gives final approval. |
| Phase | Phase 1, 3 points (L) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-7](https://340collective.atlassian.net/browse/GRC-7) |
| Mirrored folder | [engineering/Maria-06-Evidence-Automation](../../engineering/Maria-06-Evidence-Automation/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the evidence-to-control mapping. Work with Maria. Give her the control list at the Day 1 kickoff, then accept her build.

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

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-7](https://340collective.atlassian.net/browse/GRC-7).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

Config recording, S3 storage (kept small by the 30 and 7 day expiry), and Athena scans are the drivers; partition by date and framework.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Maria tears the build down after sign-off and approval.
- Confirm on the project item that the teardown evidence is recorded.

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
