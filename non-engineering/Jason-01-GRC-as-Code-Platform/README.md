# GRC-as-Code Platform (non-engineering)

You work in Jira. Your epic: `GRC-<NN>` (a placeholder until Faris creates it). This page is reference.

| Field | Value |
| --- | --- |
| Project | 01 GRC-as-Code Platform |
| Your role | Jason (Internal Auditor), partner: requirements, inputs, acceptance, operation, and reporting |
| Your partner | Faris (ISSM) |
| Reviewer or validator | Adam (ISSO) accepts the 01 requirements and Faris's builds, and gives final approval, since Faris built them. Your coverage assessment goes to Faris and Adam (Handoff 4). |
| Phase | Foundation in Phase 1 (3 points, L); 01 platform in Phase 2 (2 points, M) |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [engineering/Faris-01-GRC-as-Code-Platform](../../engineering/Faris-01-GRC-as-Code-Platform/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You map the SOC 2 Common Criteria to the platform and assess coverage. Work with Faris, who builds 01. Send your mapping and coverage assessment to Faris and Adam by Handoff 4. You assess; you do not approve.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md).

- Define requirements: 3 steps
- Hand over inputs: 1 step
- Accept the build: 1 step
- Operate it: 2 steps
- Assess or report: 3 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: foundation and 01 requirements (ASFF control scope, SOC 2 CC1 to CC9 targets), Faris to Adam (Jira Task, created by Faris)
- Handoff 2: foundation ready for acceptance (deploy pipeline, KMS, logging, temporary evidence bucket pattern, access model), Faris to Adam (Jira Task, created by Faris)
- Handoff 3: 01 Security Hub platform ready for acceptance, Faris to Adam (Jira Task, created by Faris)
- Handoff 4: SOC 2 mapping and coverage assessment, Jason to Faris and Adam (Jira Task, created by Jason)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- You record requirements, acceptance, and reports on the Tasks. You do not open or review pull requests; engineers keep this page current.
- Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

The design estimate is about 75 to 120 dollars a month if Config, Security Hub, GuardDuty, and Inspector stay on, so they run only for short test windows and are turned off at teardown.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Faris tears the build down after acceptance and approval.
- Confirm on the Jira Task that the teardown evidence is recorded.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, hand over inputs, accept the build, operate it, assess or report |
| [ASFF-Control-Matrix-Indexed.xlsx](ASFF-Control-Matrix-Indexed.xlsx) | Control matrix mapping controls to framework requirements carried in ASFF `Compliance.RelatedRequirements` |
| [Engineering README](../../engineering/Faris-01-GRC-as-Code-Platform/README.md) | The build view: design, moving parts, and regenerate commands |
| [GRC-Platform-Architecture.md](../../engineering/Faris-01-GRC-as-Code-Platform/GRC-Platform-Architecture.md) | Architecture doc |
| [Engineering lab steps](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md) | Faris's lab steps, with the same handoffs as yours |
