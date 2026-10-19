# 340 Collective Policy Management (non-engineering)

You work in Jira. Your epic: [GRC-6](https://340collective.atlassian.net/browse/GRC-6). This page is reference.

| Field | Value |
| --- | --- |
| Project | 05 340 Collective Policy Management |
| Your role | Adam (ISSO), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Maria (Automation Engineer) |
| Reviewer or validator | Faris accepts your requirements at the Day 1 kickoff. You accept and validate the build on the project item; Faris gives final approval. |
| Phase | Phase 5, 1 point (S) |
| Week | Week 5, Nov 16 to 22, 2026 |
| Jira epic | [GRC-6](https://340collective.atlassian.net/browse/GRC-6) |
| Mirrored folder | [engineering/Maria-05-Policy-Management](../../engineering/Maria-05-Policy-Management/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You own the six policies and their review cycle. Work with Maria. Give her the drafts at the Day 1 kickoff, then accept her build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md).

- Define requirements: 5 steps
- Share inputs: 1 step
- Test the build: 2 steps
- Operate it: 2 steps
- Assess or report: 1 step

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-6](https://340collective.atlassian.net/browse/GRC-6).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

CodeBuild build minutes are the only real cost; keep test builds few.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Maria removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, NIST CSF 2.0 GV.PO.

</details>

## About the project

340 Collective's security policies as versioned Markdown, reviewed by pull request, with attestation tracking and review reminders. It supports SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, and NIST CSF 2.0 GV.PO.

Status: target design, not yet deployed.

![340 Collective Policy Management AWS architecture](../../engineering/Maria-05-Policy-Management/diagram/policy-management-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Maria-05-Policy-Management/README.md) | The build view: design, moving parts, and regenerate commands |
| [Policy-Management-Architecture.md](../../engineering/Maria-05-Policy-Management/Policy-Management-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md) | Maria's lab steps, mirrored with yours |
