# GRC-as-Code Platform (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-2](https://340collective.atlassian.net/browse/GRC-2) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 01 GRC-as-Code Platform |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Faris (ISSM) |
| Reviewer or validator | Adam accepts the 01 requirements, validates Faris's build, and gives final approval, since Faris built it. Your sign-off is a pass or findings record, never an approval. Faris reviews and merges your pull requests. |
| Phase | Phase 2, 2 points (M); the shared foundation in Phase 1 is Adam's (see [Adam-Foundation](../Adam-Foundation/README.md)) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-2](https://340collective.atlassian.net/browse/GRC-2) |
| Mirrored folder | [engineering/Faris-01-GRC-as-Code-Platform](../../engineering/Faris-01-GRC-as-Code-Platform/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You map the SOC 2 Common Criteria to the platform and assess coverage. Work with Faris, who builds 01. Commit your mapping and coverage assessment to this folder and link it on the project item. You assess; you do not approve.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md).

- Define requirements: 3 steps
- Share inputs: 1 step
- Test the build: 1 step
- Operate it: 2 steps
- Assess or report: 3 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Faris agree on scope. Adam accepts the requirements, and Faris merges the pull request.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off and Adam's final approval. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-2](https://340collective.atlassian.net/browse/GRC-2).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.
- Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

The design estimate is about 75 to 120 dollars a month if Config, Security Hub, GuardDuty, and Inspector stay on, so in the running system they stay in cheap mode (see [GOVERNANCE.md](../../GOVERNANCE.md#running-system-cost)), and they are scaled down or paused when a budget alert fires.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the build stays running in the shared system, and you operate it and report. Faris removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2, NIST 800-53, ISO 27001, PCI DSS, and HIPAA, carried in ASFF `Compliance.RelatedRequirements`; the lab maps SOC 2 CC1 to CC9.

</details>

## About the project

01 is the findings hub. AWS security services evaluate the account against SOC 2, NIST 800-53, ISO 27001, PCI DSS, and HIPAA, and every finding lands in Security Hub in one format (ASFF). Your side maps SOC 2 CC1 to CC9 to real controls and captures redacted evidence.

Status: target design, not yet deployed.

![GRC Engineering AWS architecture](../../engineering/Faris-01-GRC-as-Code-Platform/diagram/grc-engineering-aws-architecture.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [ASFF-Control-Matrix-Indexed.xlsx](ASFF-Control-Matrix-Indexed.xlsx) | Control matrix mapping controls to framework requirements carried in ASFF `Compliance.RelatedRequirements` |
| [Engineering README](../../engineering/Faris-01-GRC-as-Code-Platform/README.md) | The build view: design, moving parts, and regenerate commands |
| [GRC-Platform-Architecture.md](../../engineering/Faris-01-GRC-as-Code-Platform/GRC-Platform-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md) | Faris's lab steps, mirrored with yours |
