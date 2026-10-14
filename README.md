# GRC Set

Governance, risk, and compliance engineering projects. Each numbered folder is one self-contained project.

## Project management

Work is tracked in Jira on the GRC board (340collective.atlassian.net, project key `GRC`). Each repo folder maps to one Jira work item (GRC-1 through GRC-14 for folders 00 to 13, and GRC-15 for the optional 14 stretch) that carries the owner, brief build steps, and a link back to the folder. Reference a work item key such as `GRC-7` in a commit or pull request to link it to the board. Governance, roles, and the change process are in [GOVERNANCE.md](GOVERNANCE.md).

## Shared references

| Reference | What it is |
| --- | --- |
| [ASFF control matrix](01-grc-as-code-platform/ASFF-Control-Matrix-Indexed.xlsx) | The program's control matrix: about 1,530 controls from SCF v2026.2, each with an ASFF `SecurityControlId` and mapped to frameworks including SOC 2 and ISO 27002 (carried in ASFF `Compliance.RelatedRequirements`). It has a domain index tab and a "How to use this workbook" tab. Findings from every project trace back to these control IDs. It is maintained in [01 GRC-as-Code Platform](01-grc-as-code-platform/README.md). It opens in Excel, Numbers, or Google Sheets. |

## Platform map

![GRC platform overview: how the 13 core projects plus the optional 14 connect](00-platform-overview/diagram/grc-platform-overview.png)

How the 13 core projects plus the optional 14 hand records to each other as one platform (target design, not yet deployed). Details and sources are in [00 Platform Overview](00-platform-overview/README.md).

## Projects

| # | Project | What is inside |
| --- | --- | --- |
| 00 | [Platform Overview](00-platform-overview/README.md) | One map of how the 13 core projects plus the optional 14 connect, with the source of every line |
| 01 | [GRC-as-Code Platform](01-grc-as-code-platform/README.md) | AWS architecture diagram, layer-by-layer architecture breakdown, and the ASFF control matrix |
| 02 | [Third-Party and Vendor Risk Management](02-tprm-vrm/README.md) | Vendor intake to a scored registry: AWS diagram and stage-by-stage architecture |
| 03 | [Privacy Operations](03-privacy/README.md) | PII discovery, data inventory (RoPA), DSAR workflow and consent API: diagram and architecture |
| 04 | [340 Collective Gap Analysis](04-gap-analysis-340collective/README.md) | Control library and gap scoring against SOC 2, NIST CSF and ISO 27001, with report output: diagram and architecture |
| 05 | [340 Collective Policy Management](05-policies-340collective/README.md) | Policy-as-code pipeline, versioned library and attestation tracking: diagram and architecture |
| 06 | [Audit Evidence Automation](06-evidence-automation/README.md) | Config and Audit Manager evidence lake with control-to-evidence mapping: diagram and architecture |
| 07 | [Risk Register](07-risk-register/README.md) | Risk API and store, SLA timers and heatmap dashboard: diagram and architecture |
| 08 | [User Access Reviews](08-access-reviews/README.md) | Quarterly access review packages and approver sign-off: diagram and architecture |
| 09 | [Control Testing and Assessment](09-control-testing-assessment/README.md) | Test procedures, sampling, workpapers and SOC 2 readiness or SAR-style report: diagram and architecture |
| 10 | [Audit Engagement Manager](10-audit-engagement-manager/README.md) | PBC tracking, evidence intake, findings lifecycle and auditor portal: diagram and architecture |
| 11 | [Compliance-as-Code Guardrails](11-compliance-as-code-guardrails/README.md) | OPA policy gate in CI/CD, SCPs and Config rules that block non-compliant changes: diagram and architecture |
| 12 | [GRC Metrics and Board Reporting](12-grc-metrics-reporting/README.md) | KRIs and KPIs from every project, executive dashboard and monthly board pack: diagram and architecture |
| 13 | [BC/DR and Incident Response Compliance](13-bcdr-ir-compliance/README.md) | Automated restore tests with RTO and RPO evidence, IR runbooks and tabletop records: diagram and architecture |
| 14 | [Identity and Access (Okta) (optional stretch)](14-identity-access/README.md) | Okta launch point with MFA and an 8-hour session, browser plugin sign-in to AWS IAM users, GitHub, and Jira, joiner and leaver flows: diagram and architecture |

## How the projects fit together

340 Collective's real AWS account is the shared testbed: every design is validated against its infrastructure, its vendors, its policies, and its own data. Each project automates one moving part of the GRC program, and they hand work to each other. Recommended build order: 01, 11, 06, 04, 09, 05, 07, 08, 10, 13, 02, 03, 12, with 14 as an optional stretch after 01 and the access model, before the next 08 review.

- Detect and prevent first (01, 11): Security Hub findings are the base everything else reads, and guardrails stop new problems.
- Evidence and assessment build on 01's findings (06, 04, 09).
- Governance records come next (05 policies, 07 risks, 08 access reviews).
- Audit and resilience use those records (10, 13).
- The larger ML and PII services come after that (02 uses Textract and Comprehend, 03 uses Macie).
- Metrics come last, because 12 reads every other store.
- Optional stretch (14): puts Okta in front of AWS, GitHub, and Jira sign-in and feeds 08's identity source.

## Governance

How this collaboration runs (roles, project assignments, separation of duties, the change and deviation process, cost guardrails, and the access model) is in [GOVERNANCE.md](GOVERNANCE.md). Nothing merges to `main` without ISSM approval.

## How to use

1. Open a project folder and start with its `README.md`, then its `*-Architecture.md`.
2. Diagrams are in each project's `diagram/` folder as PNG (for viewing) and SVG (for scaling). The `build_diagram.py` next to them regenerates both.
3. Spreadsheets are `.xlsx` and open in Excel, Numbers, or Google Sheets.
4. Review comments and change suggestions go through pull requests or issues. Nothing is merged to `main` without the owner's approval.
