# Audit Engagement Manager

An AWS-native manager for the audit engagement lifecycle, run by the GRC analyst. It tracks every provided by client (PBC) request with an owner and a due date, takes evidence uploads through an authenticated portal, moves each finding through an explicit remediation path, sends SLA reminders for anything overdue, and emails stakeholders a weekly status report. It supports SOC 2 and ISO 27001:2022 external audits (clause 9.2 internal audit and clause 10.2 corrective action) and NIST CSF 2.0 ID.IM. PBC tracking, evidence intake, the finding state machine, reminders, and status reporting are automated; the auditor validates each remediation before a finding closes.

Status: target design, not yet deployed.

![Audit Engagement Manager AWS architecture](diagram/audit-engagement-aws-architecture.png)

## Automation moving parts

1. A DynamoDB PBC request list holds each request with its owner, due date, and status.
2. Control owners upload evidence through the portal to S3 under `engagement/<id>/pbc/<request>/`.
3. An S3 event Lambda (the intake marker) marks the matching request received.
4. Findings and remediation run as a Step Functions state machine: open, remediation planned, remediated, validated, closed.
5. EventBridge Scheduler runs a daily reminder that emails owners about overdue PBC items and findings through SES.
6. The portal runs on API Gateway and Lambda behind a Cognito user pool with auditor and stakeholder groups.
7. A weekly status report Lambda writes the report to S3 and emails stakeholders.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The first engagement is a mock audit of 340 Collective, with the [09 Control Testing](../09-control-testing-assessment/README.md) workpapers as the auditor's input and 340 Collective's own evidence as the PBC responses. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/audit-engagement-aws-architecture.png](diagram/audit-engagement-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/audit-engagement-aws-architecture.svg](diagram/audit-engagement-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Audit-Engagement-Architecture.md](Audit-Engagement-Architecture.md) | Stage-by-stage breakdown: portal, PBC tracking, evidence intake, findings lifecycle, SLA reminders, status reporting, data model, security, cost note, build order |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/audit-engagement-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Approvers: the auditor (Cognito auditors group) opens findings and validates each remediation before a finding can close; the 340 Collective owner, as engagement owner, approves each remediation plan.
- The portal API uses a Cognito user pool with two groups (auditors, stakeholders), so it is never unauthenticated. Auditors get read-only access to evidence; stakeholders see status only. This is the same pattern as 07.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [09 Control Testing](../09-control-testing-assessment/README.md) (workpapers feed the engagement), [06 Evidence Automation](../06-evidence-automation/README.md) (closed engagements are archived as evidence), [07 Risk Register](../07-risk-register/README.md) (findings that stay open become risks), and [12 GRC Metrics](../12-grc-metrics-reporting/README.md) (overdue findings are a KRI).
