# GRC-as-Code Platform (non-engineering)

You work in Jira. Your epic: [GRC-2](https://340collective.atlassian.net/browse/GRC-2). This page is reference.

| Field | Value |
| --- | --- |
| Project | 01 GRC-as-Code Platform |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Faris (ISSM) |
| Reviewer or validator | Adam accepts the 01 requirements and Faris's builds, and gives final approval, since Faris built them. Your coverage assessment goes to Faris and Adam (phase assessment). |
| Phase | Foundation in Phase 1 (3 points, L); 01 platform in Phase 2 (2 points, M) |
| Week | Foundation: Week 1, Oct 19 to 25, 2026; 01 platform: Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-2](https://340collective.atlassian.net/browse/GRC-2) |
| Mirrored folder | [engineering/Faris-01-GRC-as-Code-Platform](../../engineering/Faris-01-GRC-as-Code-Platform/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You map the SOC 2 Common Criteria to the platform and assess coverage. Work with Faris, who builds 01. Send your mapping and coverage assessment to Faris and Adam as a comment on the project item. You assess; you do not approve.

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

- Day 1 kickoff: you and Faris agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-2](https://340collective.atlassian.net/browse/GRC-2).
- Ask your partner directly or comment on the project item. You sign off on the Final report item. You do not open or review pull requests; engineers keep this page current.
- Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

The design estimate is about 75 to 120 dollars a month if Config, Security Hub, GuardDuty, and Inspector stay on, so they run only for short test windows. The `grc-platform` stack stays deployed until the final-week teardown; check the trial clocks in GOVERNANCE.md before leaving any of them on after sign-off.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown (final week)</summary>

- Faris keeps the build deployed after sign-off and approval, and tears it down in the program's final week (Nov 23 to 25, 2026).
- In the final week, confirm on the project item that the teardown evidence is recorded.

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
