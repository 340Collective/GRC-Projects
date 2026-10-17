# Compliance-as-Code Guardrails

| Field | Value |
| --- | --- |
| Project | 11 Compliance-as-Code Guardrails |
| Your role | Faris (ISSM), engineer: you design, deploy, test, hand off, and tear down |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Rasheed, with Maria as backup. Acceptance, validation, and final approval: Adam (ISSO), in Jira, since Faris built it. |
| Phase | Phase 3, 3 points (L) |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [non-engineering/Adam-11-Compliance-as-Code-Guardrails](../../non-engineering/Adam-11-Compliance-as-Code-Guardrails/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You turn guardrails into code: Rego rules, Config rules, and an SCP outline. Work with Adam (ISSO): he gives you the guardrail list, then accepts your build in Jira and gives final approval, since you built it.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-11-Compliance-as-Code-Guardrails/LAB-STEPS.md).

- Design: 9 steps
- Deploy: 4 steps
- Test: 5 steps
- Hand off: 3 steps
- Tear down: 5 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: guardrail list and the control each enforces, Adam to Faris (Jira Task, created by Adam)
- Handoff 2: Rego rules, Config rules, and SCP outline ready for acceptance, Faris to Adam (Jira Task, created by Faris)
- Handoff 3: guardrail-to-control register, Adam to Faris (Jira Task, created by Adam)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- Partner acceptance and Adam's validation are recorded on the Task. A pull request in this repo links its Task on the Jira issue line and merges only after the Task shows acceptance.
- Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).

</details>

<details>
<summary>Cost</summary>

CodeBuild build minutes and Config rule evaluations are the drivers; keep test runs few. SCPs have no charge.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-guardrails` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Delete the Config rules, and stop the Config recorder if this build turned it on.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC8.1 and CC6.6, ISO 27001:2022 A.8.9 and A.8.32, NIST CSF 2.0 PR.PS.

</details>

Where [01](../Faris-01-GRC-as-Code-Platform/README.md) detects and [05](../Maria-05-Policy-Management/README.md) manages policy documents, 11 prevents. Policy-as-code checks written in OPA Rego run in the deploy pipeline and fail the build on any violation, Service Control Policies in AWS Organizations deny non-compliant actions at the account level, and AWS Config custom rules catch anything that drifts after deploy. Every guardrail violation goes to Security Hub as an ASFF finding, so it joins 01's pipeline. It supports SOC 2 CC8.1 (change management) and CC6.6, ISO 27001:2022 A.8.9 (configuration management) and A.8.32 (change management), and NIST CSF 2.0 PR.PS. The gate, the denies, the rule evaluation, and the finding hand-off are automated; the 340 Collective owner approves every guardrail change and every exception.

Status: target design, not yet deployed.

![Compliance-as-Code Guardrails AWS architecture](diagram/guardrails-aws-architecture.png)

## Automation moving parts

1. A developer pull request in GitHub, once merged, triggers CodePipeline.
2. A CodeBuild stage synthesizes CloudFormation and runs OPA Rego policies against the template, failing the build on any violation.
3. Passing changes deploy through CloudFormation change sets.
4. Service Control Policies in AWS Organizations deny non-compliant actions at the account level, for example disabling CloudTrail, leaving approved regions, or creating public S3 access.
5. AWS Config proactive and custom rules evaluate resources through a Config custom rule Lambda.
6. Guardrail violations from the build stage and from Config go to Security Hub as ASFF findings, joining 01's pipeline.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The gate runs on 340 Collective's existing GitHub to CloudFormation deploy path, and the SCP layer targets its AWS Organization. Validation uses deliberately non-compliant test templates in a sandbox account. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/guardrails-aws-architecture.png](diagram/guardrails-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/guardrails-aws-architecture.svg](diagram/guardrails-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Guardrails-Architecture.md](Guardrails-Architecture.md) | Stage-by-stage breakdown: pipeline, policy gate, deploy, organization guardrails, runtime rules, findings, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, hand off, tear down |
| [Partner lab steps](../../non-engineering/Adam-11-Compliance-as-Code-Guardrails/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/guardrails-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Approvers: the 340 Collective owner reviews and merges every change to the Rego policies, SCPs, and Config rules, and approves every time-boxed exception. A developer cannot waive a failing check on their own change.
- OPA and Rego have no AWS or vendor icon in the diagram package, so the policy gate is drawn as the CodeBuild icon labelled "OPA, Rego checks".
- Assumption: SCPs need an AWS Organization. If 340 Collective's account is not in one, the SCP layer is planned only, while the CodeBuild gate and the Config rules still work in a single account.
- Rego policies, SCP JSON, and rule code are not included here. The architecture doc lists example policy names only.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md) (findings join its Security Hub pipeline), [05 Policy Management](../Maria-05-Policy-Management/README.md) (written policy that these checks enforce), and [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md) (preventive controls score as met).
