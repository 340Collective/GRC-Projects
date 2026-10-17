# GRC Metrics and Board Reporting

| Field | Value |
| --- | --- |
| Project | 12 GRC Metrics and Board Reporting |
| Your role | Rasheed (ISSE / Engineer), engineer: you design, deploy, test, hand off, and tear down |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Maria. Acceptance and validation: Adam (ISSO), in Jira. Final approval: Faris (ISSM). |
| Phase | Phase 4, 2 points (M); needs data from 06, 11, and 07 |
| Week | Week 4, Nov 9 to 15, 2026 |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [non-engineering/Adam-12-Metrics-Reporting](../../non-engineering/Adam-12-Metrics-Reporting/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the metrics layer: a CloudWatch trend dashboard, the GRC Metrics Jira issue, and the monthly board pack. Work with Adam (ISSO): he gives you metric definitions, targets, and thresholds, then accepts your build in Jira. You need data from 06, 11, and 07, so this comes in Phase 3.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-12-Metrics-Reporting/LAB-STEPS.md).

- Design: 8 steps
- Deploy: 4 steps
- Test: 3 steps
- Hand off: 3 steps
- Tear down: 5 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: metric definitions, targets, and thresholds, Adam to Rasheed (Jira Task, created by Adam)
- Handoff 2: metrics dashboard ready for acceptance, Rasheed to Adam (Jira Task, created by Rasheed)
- Handoff 3: board pack export with commentary, Adam to Faris (Jira Task, created by Adam)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- Partner acceptance and Adam's validation are recorded on the Task. A pull request in this repo links its Task on the Jira issue line and merges only after the Task shows acceptance.
- Jira path 3: the daily KRI and KPI job posts its results to the "GRC Metrics" Jira issue, as a comment or custom fields.

</details>

<details>
<summary>Cost</summary>

0 dollars day to day: the CloudWatch free tier, free Jira, and SES for the board pack.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-metrics` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Revoke the Jira API token and delete its `/grc/` parameter.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

ISO 27001:2022 clauses 9.1 and 9.3, NIST CSF 2.0 GV.OV, SOC 2 CC4.1.

</details>

An AWS-native metrics layer for the GRC analyst and for leadership. A daily job reads the stores of the other projects and Security Hub, computes key risk indicators (KRIs) and key performance indicators (KPIs), keeps a daily history, shows trends on a CloudWatch dashboard, posts results to a GRC Metrics issue in Jira, and builds a monthly board pack that is emailed to leadership. It supports ISO 27001:2022 clause 9.1 (monitoring, measurement, analysis, and evaluation) and clause 9.3 (management review), NIST CSF 2.0 GV.OV, and SOC 2 CC4.1. Collection, calculation, history, the dashboard, the board pack, and threshold alerts are automated; the 340 Collective owner approves each board pack before it is sent.

Status: target design, not yet deployed.

![GRC Metrics and Board Reporting AWS architecture](diagram/grc-metrics-aws-architecture.png)

## Example metrics

- KRIs: open high risks, overdue findings, vendors past reassessment, and unreviewed access.
- KPIs: control pass rate, mean time to remediate, policy attestation rate, and evidence freshness.

## Automation moving parts

1. A daily EventBridge Scheduler run starts the metrics builder Lambda.
2. It reads the DynamoDB stores of 02, 05, 07, 08, and 10, plus Security Hub control status.
3. It writes daily snapshots to a DynamoDB metrics table and to S3 as Parquet.
4. KRIs go to a CloudWatch trend dashboard, and a Jira poster Lambda posts the daily results to the GRC Metrics Jira issue.
5. A monthly cron builds the board pack (HTML or Markdown) to S3, and SES emails it to leadership.
6. A CloudWatch alarm fires on KRI threshold breaches and alerts the metric owner through SNS.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The metrics are 340 Collective's real posture: its own risks, vendors, policies, access reviews, findings, and Security Hub control status. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/grc-metrics-aws-architecture.png](diagram/grc-metrics-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/grc-metrics-aws-architecture.svg](diagram/grc-metrics-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [GRC-Metrics-Architecture.md](GRC-Metrics-Architecture.md) | Stage-by-stage breakdown: metric sources, aggregation, metrics store, dashboard, board pack, thresholds, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, hand off, tear down |
| [Partner lab steps](../../non-engineering/Adam-12-Metrics-Reporting/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/grc-metrics-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Approvers: the 340 Collective owner approves each monthly board pack before SES sends it, and approves every change to a KRI threshold. Each metric has a named metric owner who receives its threshold alerts.
- The single "project stores" DynamoDB icon stands for the read-only reads of the 02, 05, 07, 08, and 10 tables.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Build this last: it reads every other project's store. Pairs with [07 Risk Register](../Rasheed-07-Risk-Register/README.md), [10 Audit Engagement Manager](../Maria-10-Audit-Engagement-Manager/README.md), and [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md) (Security Hub control status).
