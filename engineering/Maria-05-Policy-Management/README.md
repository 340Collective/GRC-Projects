# 340 Collective Policy Management

A policy-as-code lifecycle for 340 Collective. Policies are written as Markdown in Git, reviewed through pull requests, validated and rendered in CodePipeline, published to a versioned S3 library, and tracked through staff attestation and annual review reminders. It supports SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, and NIST CSF 2.0 GV.PO. Validation, publishing, attestation requests, and reminders are automated; the policy owner approves every change.

Status: target design, not yet deployed.

![340 Collective Policy Management AWS architecture](diagram/policy-management-aws-architecture.png)

## Automation moving parts

1. Policies are authored as Markdown in GitHub, and the policy owner reviews each pull request.
2. A merge to main triggers CodePipeline through a GitHub connection.
3. CodeBuild validates front matter (owner, version, review date), links, and banned terms, then renders the PDF.
4. The policy is published to a versioned S3 policy library.
5. A new version event in EventBridge starts a Lambda that emails staff through SES.
6. Staff attest through API Gateway and Lambda into a DynamoDB attestation table.
7. EventBridge Scheduler sends annual review and overdue attestation reminders.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The intended policy set is 340 Collective's own: information security, acceptable use, access control, vendor management, incident response, and data retention. This repo holds no policy text; the policy corpus stays in 340 Collective's private policy repo. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/policy-management-aws-architecture.png](diagram/policy-management-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/policy-management-aws-architecture.svg](diagram/policy-management-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Policy-Management-Architecture.md](Policy-Management-Architecture.md) | Stage-by-stage breakdown: source, validation, library, attestation, review cycle, data model, security, cost note, build order |
| [LAB-STEPS.md](../../non-engineering/Adam-05-Policy-Management/LAB-STEPS.md) | Build playbook: manual lab steps for the collaboration team |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/policy-management-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [04 Gap Analysis](../Alex-04-Gap-Analysis/README.md) (policy and attestation status score the governance controls) and [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md) (attestation records are audit evidence).
