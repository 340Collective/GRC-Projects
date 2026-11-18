# 15 AWS Continuous Monitoring (ConMon) - ISSO Requirements

Owner: Adam (ISSO) · Engineer: Rasheed (ISSE) · Approver: Faris (ISSM) · Assessor: Jason · Phase 5 (Nov 16 to 22, 2026)

Subject organization: 340 Collective. Jira epic: GRC-31.

## 1. Scope
The ConMon plan for 340 Collective's AWS account: what is monitored, at what severity, how often, who is notified, and how each finding becomes a tracked remediation item (POA&M) in Jira. Supports NIST CA-7, RA-5, SI-2, SI-4, IR-4 and CA-5.

## 2. What is monitored
| Source | What | How often |
|---|---|---|
| Security Hub | Findings from Inspector, Config, project 01 (GRC-as-Code platform) and the project 11 guardrails | Real time (on each new or updated finding) |
| Config | Rule compliance changes | Real time |
| CloudTrail | The events in section 3 | Real time |
| GuardDuty | Planned; enabled later as code with owner approval (30-day trial, cost reviewed with the ISSM before keeping it) | When enabled |

## 3. CloudTrail events and severity
| Event | Severity |
|---|---|
| Any root user activity | Critical |
| `StopLogging` or `DeleteTrail` | Critical |
| Policy change on a log bucket | Critical |
| `ConsoleLogin` without MFA | High |
| IAM user or access key created | High |
| IAM policy changes | Medium |

Security Hub and Config findings keep the severity Security Hub assigns.

## 4. Routing and notification
| Severity | Jira issue | Real-time email | Daily digest |
|---|---|---|---|
| Critical | Yes | Yes | Yes |
| High | Yes | Yes | Yes |
| Medium | Yes | No | Yes |
| Low / Informational | No | No | Counts only |

- Real-time email goes to the ISSO and the ISSM. Subscribers confirm out of band; **no email addresses go in git**.
- A repeat finding updates the same Jira issue (dedupe on finding ID), never opens a new one.
- Daily digest: counts by severity, new and closed, and SLA breaches.

## 5. Remediation SLAs
| Severity | SLA |
|---|---|
| Critical | 15 days |
| High | 30 days |
| Medium | 90 days |

Each Jira issue carries the severity, resource, SLA due date and owner. Owner: Faris for misconfigurations (project 11 guardrails); the owning engineer for vulnerabilities. A risk accepted instead of fixed needs written ISSM acceptance and becomes a POA&M item.

## 6. Build requirements (Rasheed)
1. Rules for the sources in section 2 and the events in section 3, routed per section 4.
2. One Jira issue per finding with the SLA due date from section 5, and dedupe on repeat.
3. Real-time email for Critical and High only; one daily digest.
4. Failed deliveries go to a dead letter queue and raise an alarm.
5. A dashboard with findings by severity, SLA breaches and delivery failures.
6. A monthly ConMon report: open findings by severity, mean time to remediate, SLA breaches, new versus closed, top recurring findings; KPIs posted to the project 12 GRC Metrics issue.

## 7. Acceptance tests (ISSO validation)
| # | Test | Pass condition |
|---|---|---|
| T1 | Send a test HIGH finding | One Jira issue with the correct SLA due date (30 days) |
| T2 | Send the same finding again | The same issue is updated; no duplicate |
| T3 | Send a test CRITICAL event | One real-time email arrives |
| T4 | Wait for the digest | The digest arrives with correct counts |
| T5 | Check the dashboard | Counts match the test events |

Results go in RESULTS.md under Test results.

## 8. Operating
- Daily: triage the Jira queue and digest, assign an owner, set priority.
- Weekly: review SLAs and chase overdue items with the owner.
- Monthly: review and accept the ConMon report as POA&M evidence.

## 9. Data handling
This repo is public. No account IDs, ARNs, real resource names or email addresses. Reports committed here are sanitized.

## 10. Sign-off
Day 7: Rasheed commits FINAL-REPORT.md. Adam compares it with RESULTS.md and signs off on the Final report item ("Accepted by: Adam", or findings). Faris merges after sign-off.
