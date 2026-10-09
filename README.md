# GRC Set

Governance, risk, and compliance engineering projects. Each numbered folder is one self-contained project.

| # | Project | What is inside |
| --- | --- | --- |
| 01 | [GRC-as-Code Platform](01-grc-as-code-platform/README.md) | AWS architecture diagram, layer-by-layer architecture breakdown, and the ASFF control matrix |
| 02 | [Third-Party and Vendor Risk Management](02-tprm-vrm/README.md) | Vendor intake to a scored registry: AWS diagram and stage-by-stage architecture |
| 03 | [Privacy Operations](03-privacy/README.md) | PII discovery, data inventory (RoPA), DSAR workflow and consent API: diagram and architecture |
| 04 | [340 Collective Gap Analysis](04-gap-analysis-340collective/README.md) | Control library and gap scoring against SOC 2, NIST CSF and ISO 27001, with report output: diagram and architecture |
| 05 | [340 Collective Policy Management](05-policies-340collective/README.md) | Policy-as-code pipeline, versioned library and attestation tracking: diagram and architecture |
| 06 | [Audit Evidence Automation](06-evidence-automation/README.md) | Config and Audit Manager evidence lake with control-to-evidence mapping: diagram and architecture |
| 07 | [Risk Register](07-risk-register/README.md) | Risk API and store, SLA timers and heatmap dashboard: diagram and architecture |
| 08 | [User Access Reviews](08-access-reviews/README.md) | Quarterly access review packages and approver sign-off: diagram and architecture |

## How the projects fit together

340 Collective's real AWS account is the shared testbed: every design is validated against its infrastructure, its vendors, its policies, and its own data. Each project automates one moving part of the GRC program, and they hand work to each other. Recommended build order: 01, 06, 04, 05, 07, 08, 02, 03.

- Detect first (01): Security Hub findings are the base everything else reads.
- Evidence and assessment build on those findings (06, 04).
- Governance records come next (05 policies, 07 risks, 08 access reviews).
- The larger ML and PII services come last (02 uses Textract and Comprehend, 03 uses Macie).

## How to use

1. Open a project folder and start with its `README.md`, then its `*-Architecture.md`.
2. Diagrams are in each project's `diagram/` folder as PNG (for viewing) and SVG (for scaling). The `build_diagram.py` next to them regenerates both.
3. Spreadsheets are `.xlsx` and open in Excel, Numbers, or Google Sheets.
4. Review comments and change suggestions go through pull requests or issues. Nothing is merged to `main` without the owner's approval.
