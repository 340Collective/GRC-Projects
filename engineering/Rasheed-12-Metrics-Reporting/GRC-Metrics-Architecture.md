# GRC Metrics and Board Reporting Architecture

## Purpose

Turn the records every other project keeps into a small set of numbers leadership can act on. One daily job calculates each KRI and KPI the same way every time, keeps the history so trends are visible, and raises an alert the day a KRI crosses its threshold. Once a month the same data becomes a board pack, so management review runs on facts rather than a hand-built slide deck.

## Scope and frameworks

- ISO 27001:2022 clause 9.1 (monitoring, measurement, analysis, and evaluation) and clause 9.3 (management review inputs).
- NIST CSF 2.0 GV.OV: oversight of cybersecurity risk management strategy and results.
- SOC 2 (2017 TSC) CC4.1 and CC4.2: monitoring activities and communicating deficiencies.
- Control areas: metric definitions, data collection, history, dashboards, board reporting, and threshold alerting.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | DynamoDB (02, 05, 07, 08, 10 stores), Security Hub | Source records and control status that the metrics are calculated from |
| Processing | EventBridge Scheduler, Lambda (metrics builder) | A daily run reads each source and computes every KRI and KPI |
| State | DynamoDB (snapshots), S3 (history), Athena | Daily snapshots plus a partitioned Parquet history that Athena can query |
| Orchestration | EventBridge Scheduler, Lambda (board pack builder), SES | A monthly run builds the board pack and emails it after approval |
| Outputs | QuickSight, CloudWatch, SNS | Executive dashboard; alarms and alerts on KRI threshold breaches |

## Stage details

### Producers

- Read-only access to the DynamoDB tables of [02](../Maria-02-TPRM-VRM/README.md) (vendor registry), [05](../Maria-05-Policy-Management/README.md) (attestations), [07](../Rasheed-07-Risk-Register/README.md) (risk register), [08](../Abdifatah-08-Access-Reviews/README.md) (review items), and [10](../Maria-10-Audit-Engagement-Manager/README.md) (findings).
- Security Hub `GetFindings` and the security standards control status from [01](../Faris-01-GRC-as-Code-Platform/README.md).
- [06](../Maria-06-Evidence-Automation/README.md) evidence freshness is read from its control to evidence map.

### Processing

- EventBridge Scheduler runs the metrics builder once a day.
- Example KRIs: open high risks (07), overdue findings (10), vendors past reassessment (02), and unreviewed access items (08).
- Example KPIs: control pass rate (Security Hub), mean time to remediate (10), policy attestation rate (05), and evidence freshness (06).
- Each metric definition (source, query, unit, threshold, owner) is stored as data, not code, so a threshold change is a reviewed data change.

### State

- Each run writes one snapshot item per metric per day to the DynamoDB metrics table.
- The same snapshot is written to S3 as Parquet, partitioned by date, which forms the metrics history.
- The Glue Data Catalog table over the history lets Athena query trends.

### Orchestration

- A monthly schedule runs the board pack builder. It reads the month's snapshots and trends and renders the pack (PDF or HTML) to S3.
- The pack is held for the 340 Collective owner's approval; once approved, SES emails leadership a link, never the pack as an attachment.

### Outputs

- QuickSight reads the history through Athena for the executive dashboard: current values, 90 day trends, and status against thresholds.
- The metrics builder publishes each KRI as a CloudWatch custom metric. CloudWatch alarms fire when a KRI crosses its threshold, and SNS alerts the metric owner.

## Data model

DynamoDB table `metric_definitions`:

- Partition key `metric_id`.
- Attributes: `name`, `type` (KRI, KPI), `source`, `query`, `unit`, `threshold`, `direction`, `owner`, `approved_by`.

DynamoDB table `metric_snapshots`:

- Partition key `metric_id`, sort key `date`.
- Attributes: `value`, `threshold`, `status` (green, amber, red), `source_counts`, `run_id`.

S3 prefixes:

- `metrics/history/date=<yyyy-mm-dd>/` for Parquet snapshots.
- `board-packs/<yyyy>/<mm>/` for monthly packs.

## Security and privacy controls

- KMS customer managed key for the metrics tables, the history bucket, and the board packs.
- One IAM role per Lambda: the metrics builder has read-only access to the source tables and Security Hub and can write only its own snapshots; the board pack builder can read snapshots and write packs only.
- Metrics are counts and rates, never records: no names, emails, or evidence content reach the metrics store or logs.
- QuickSight access is limited to the leadership group; the dashboard has no row-level source data.
- Human approval points: the 340 Collective owner approves each board pack before it is sent and every threshold change.

## 340 Collective testbed

340 Collective's real posture is the first data set: its own risks, vendors, policies, access reviews, findings, and Security Hub control status. Validation means each metric value can be traced back to its source query, the dashboard matches the snapshots, and a test threshold breach produces an alarm and an SNS alert.

## Cost note

The main cost driver is QuickSight (per user or per session). Athena scans stay small because the history is partitioned by date. Lambda, DynamoDB, S3, CloudWatch custom metrics, SNS, and SES stay at or near the free tier at 340 Collective's scale. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. Metric definitions table and the first four metrics from projects already built.
2. Metrics builder, daily schedule, and snapshot table.
3. Parquet history in S3, Glue table, and Athena queries.
4. QuickSight executive dashboard.
5. Monthly board pack builder, approval step, and SES delivery.
6. CloudWatch KRI alarms and SNS alerts; add metrics as each project ships.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [02 Third-Party and Vendor Risk Management](../Maria-02-TPRM-VRM/README.md)
- [05 Policy Management](../Maria-05-Policy-Management/README.md)
- [07 Risk Register](../Rasheed-07-Risk-Register/README.md)
- [08 User Access Reviews](../Abdifatah-08-Access-Reviews/README.md)
- [10 Audit Engagement Manager](../Maria-10-Audit-Engagement-Manager/README.md)
