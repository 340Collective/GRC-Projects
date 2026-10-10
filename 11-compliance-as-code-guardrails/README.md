# Compliance-as-Code Guardrails

Where [01](../01-grc-as-code-platform/README.md) detects and [05](../05-policies-340collective/README.md) manages policy documents, 11 prevents. Policy-as-code checks written in OPA Rego run in the deploy pipeline and fail the build on any violation, Service Control Policies in AWS Organizations deny non-compliant actions at the account level, and AWS Config custom rules catch anything that drifts after deploy. Every guardrail violation goes to Security Hub as an ASFF finding, so it joins 01's pipeline. It supports SOC 2 CC8.1 (change management) and CC6.6, ISO 27001:2022 A.8.9 (configuration management) and A.8.32 (change management), and NIST CSF 2.0 PR.PS. The gate, the denies, the rule evaluation, and the finding hand-off are automated; the 340 Collective owner approves every guardrail change and every exception.

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
| [LAB-STEPS.md](LAB-STEPS.md) | Build playbook: manual lab steps for the collaboration team |

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
- Pairs with [01 GRC-as-Code Platform](../01-grc-as-code-platform/README.md) (findings join its Security Hub pipeline), [05 Policy Management](../05-policies-340collective/README.md) (written policy that these checks enforce), and [04 Gap Analysis](../04-gap-analysis-340collective/README.md) (preventive controls score as met).
