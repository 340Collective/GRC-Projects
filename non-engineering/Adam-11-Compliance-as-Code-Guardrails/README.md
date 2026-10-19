# Compliance-as-Code Guardrails (non-engineering)

You work in Jira. Your epic: [GRC-12](https://340collective.atlassian.net/browse/GRC-12). This page is reference.

| Field | Value |
| --- | --- |
| Project | 11 Compliance-as-Code Guardrails |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Faris (ISSM), who also builds 11 |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. You accept and validate the build on the project item and give final approval, since Faris built it. |
| Phase | Phase 3, 3 points (L) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-12](https://340collective.atlassian.net/browse/GRC-12) |
| Mirrored folder | [engineering/Faris-11-Compliance-as-Code-Guardrails](../../engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the guardrail list and the guardrail-to-control register. Work with Faris. Give him the list at the Day 1 kickoff, then accept his build and give final approval.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md).

- Define requirements: 3 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 1 step
- Assess or report: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Faris agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-12](https://340collective.atlassian.net/browse/GRC-12).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.
- Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

CodeBuild build minutes and Config rule evaluations are the drivers; keep test runs few. SCPs have no charge.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Faris removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC8.1 and CC6.6, ISO 27001:2022 A.8.9 and A.8.32, NIST CSF 2.0 PR.PS.

</details>

## About the project

Preventive guardrails as code: Rego checks in the deploy pipeline, Config rules for drift, and an SCP outline, each tied to a control. It supports SOC 2 CC8.1 and CC6.6, ISO 27001:2022 A.8.9 and A.8.32, and NIST CSF 2.0 PR.PS.

Status: target design, not yet deployed.

![Compliance-as-Code Guardrails AWS architecture](../../engineering/Faris-11-Compliance-as-Code-Guardrails/diagram/guardrails-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) | The build view: design, moving parts, and regenerate commands |
| [Guardrails-Architecture.md](../../engineering/Faris-11-Compliance-as-Code-Guardrails/Guardrails-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md) | Faris's lab steps, mirrored with yours |
