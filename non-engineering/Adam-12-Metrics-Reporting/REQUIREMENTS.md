# 12 GRC Metrics and Board Reporting - ISSO Requirements

Owner: Adam (ISSO) · Engineer: Rasheed (ISSE) · Approver: Faris (ISSM) · Phase 4 (Nov 9 to 15, 2026)

Subject organization: 340 Collective. Jira epic: GRC-13. Needs data from projects 06, 11 and 07.

## 1. Scope
Turn the records from the other projects into a small set of metrics leadership can act on: calculated the same way every day, kept as history, with red, amber and green thresholds and a monthly board pack.

## 2. Source data
| Source | Project |
|---|---|
| Control status (Security Hub) and control matrix | 04, 06 |
| Risk register | 07 |
| Access review results | 08 |
| Findings log | 10, 15 |
| Policy attestations | 05 |
| Vendor registry | 02 |

Metrics use counts and rates only, never names, emails or evidence content.

## 3. Metric definitions
| ID | Metric | Type | Source | Target | Green | Amber | Red |
|---|---|---|---|---|---|---|---|
| M-01 | Control pass rate (% of in-scope controls passing) | KPI | 04, 06 | 90% or more | 90% or more | 75% to 89% | below 75% |
| M-02 | Evidence freshness (% of controls with evidence inside its window) | KPI | 06 | 100% | 100% | 80% to 99% | below 80% |
| M-03 | High risks past their review date | KRI | 07 | 0 | 0 | 1 | 2 or more |
| M-04 | High residual risks without written ISSM acceptance | KRI | 07 | 0 | 0 | none | 1 or more |
| M-05 | Findings remediated within SLA (%) | KPI | 10, 15 | 90% or more | 90% or more | 75% to 89% | below 75% |
| M-06 | Policy attestation rate (%) | KPI | 05 | 100% | 100% | 90% to 99% | below 90% |
| M-07 | Days since last access review | KRI | 08 | 90 or fewer | 90 or fewer | 91 to 120 | over 120 |
| M-08 | Vendors past reassessment date | KRI | 02 | 0 | 0 | 1 | 2 or more |

Each metric definition stores: ID, source, query, unit, target, thresholds, owner. Definitions are data, so a threshold change is a reviewed change.

Metric owner for all metrics: ISSO (Adam). ISSM (Faris) is informed of every red.

## 4. Build requirements (Rasheed)
1. A daily run calculates every metric in section 3 from its source.
2. One snapshot per metric per day is kept as history, so trends are visible.
3. Values and status post to the GRC Metrics Jira issue.
4. A KRI that turns red raises an alert to the metric owner the same day.
5. A monthly board pack (HTML, Markdown or PDF) shows current value, trend and status for each metric.

## 5. Acceptance tests (ISSO validation)
| # | Test | Pass condition |
|---|---|---|
| T1 | Compare each metric on the Jira issue with my workbook | Every value matches |
| T2 | Trace one metric to its source | The value can be reproduced from the source query |
| T3 | Force a test KRI breach | The status turns red and an alert is sent |
| T4 | Generate a board pack | Every metric appears with value, trend and status |

Results go in RESULTS.md under Test results.

## 6. Reporting
- Jira dashboard: control coverage chart, risk status by tier, remediation progress, and a KRI/KPI table with red, amber and green.
- Commentary box: the biggest change since the last review and the top action needed.

## 7. Data handling
This repo is public. Board pack exports are sanitized: no account IDs, ARNs, real resource names, personal emails or client data.

## 8. Sign-off
Day 7: Rasheed commits FINAL-REPORT.md. Adam compares it with RESULTS.md and signs off on the Final report item ("Accepted by: Adam", or findings). Faris merges after sign-off.
