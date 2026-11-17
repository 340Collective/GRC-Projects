# 05 Policy Management - ISSO Requirements

Owner: Adam (ISSO) · Engineer: Maria (Automation Engineer) · Approver: Faris (ISSM) · Phase 5 (Nov 16 to 22, 2026)

Subject organization: 340 Collective. Jira epic: GRC-6.

## 1. Scope
Write, version, publish and track acknowledgment of 340 Collective's six core security policies. Every policy change is reviewed, validated and published the same way, and every collaborator's acknowledgment is recorded, so an auditor can see who approved which version, when it was published, and who attested to it.

## 2. Policy set
| Policy ID | Policy | Owner | Approver |
|---|---|---|---|
| POL-01 | Information Security | ISSO | ISSM |
| POL-02 | Acceptable Use | ISSO | ISSM |
| POL-03 | Access Control | ISSO | ISSM |
| POL-04 | Vendor Management | ISSO | ISSM |
| POL-05 | Incident Response | ISSO | ISSM |
| POL-06 | Data Retention | ISSO | ISSM |

Each policy is one Markdown file. Approved policies are published on the 340 Collective website for collaborators to review and read (ISSM decision, 2026-11-16). Policy text is not committed to this public repo; this folder holds only the requirements, sanitized results and schedules.

## 3. Required header block
Every policy starts with the same header. The build must reject a policy that is missing any field.

| Field | Rule |
|---|---|
| Policy ID | `POL-01` to `POL-06` |
| Version | `MAJOR.MINOR`, starting at `1.0` |
| Owner | A named role, not a team |
| Approver | ISSM |
| Effective Date | `YYYY-MM-DD`, the date the ISSM approves the version |
| Next Review Date | `YYYY-MM-DD`, set by the review cycle in section 5, never in the past |
| Change log | Table: Version, Date, Author, Summary of change |

Planned dates for version 1.0 of all six policies:

| Field | Planned value |
|---|---|
| Effective Date | 2026-11-22 (end of Phase 5, on ISSM approval) |
| Next Review Date | 2027-11-22 (annual review) |

If approval happens on a different day, the Effective Date is the actual approval date and the Next Review Date is one year later.

## 4. Content rules (how 340 Collective actually operates)
- **POL-01 Information Security:** the umbrella policy. Points to the other five policies, names the ISSM as accountable and the ISSO as responsible, and references the risk register (project 07).
- **POL-02 Acceptable Use:** company accounts and data are for 340 Collective work only; no client data on personal devices or in public repos.
- **POL-03 Access Control:** all AWS access through IAM Identity Center with MFA; no IAM users with long-lived access keys; least privilege roles; access reviewed at least every 90 days (project 08); Okta MFA for GitHub and Jira (project 14).
- **POL-04 Vendor Management:** every vendor (for example AWS, Stripe, GitHub, Jira) has a named owner and is reassessed at least annually (project 02).
- **POL-05 Incident Response:** how to report a suspected incident, severity levels, and who is notified; aligned with the ConMon severities and SLAs in project 15 (critical 15 days, high 30 days, medium 90 days).
- **POL-06 Data Retention:** documents the retention periods: contact form records kept 12 months; invoice records kept 7 years; evidence buckets expire objects after 30 days (GOVERNANCE.md). Per the ISSM (2026-11-16), these periods are documented in the policy only; the engineering build does not enforce them, since this is a learning project.

## 5. Review cycle
- Every policy is reviewed **annually**, and also **after a major change** (new service, new vendor, or a security incident).
- POL-05 Incident Response is also reviewed after every Medium or higher incident.
- The pipeline sends a reminder 30 days before each Next Review Date and flags any policy past it.

| Policy | Frequency | Next review | Reviewer |
|---|---|---|---|
| POL-01 to POL-06 | Annual, or after a major change | 2027-11-22 | ISSO, approved by ISSM |

## 6. Build requirements (Maria)
1. Validates the header block in section 3 and fails the build if a field is missing or the Next Review Date is in the past.
2. Stores every published version (versioned library), so any past version can be retrieved.
3. Publishes each approved version to the 340 Collective website and requests acknowledgment from each collaborator.
4. Records one attestation per person per policy version: person, Policy ID, version, date, method.
5. Sends review and attestation reminders on schedule; the attestation window is 14 days from publication.
6. Logs every change to the library and every attestation, so the history can be audited.

## 7. Acceptance tests (ISSO validation)
| # | Test | Pass condition |
|---|---|---|
| T1 | Submit a policy with a missing header field | The build fails and names the missing field |
| T2 | Push one approved policy change | A new version is published and the old version is still retrievable |
| T3 | Acknowledge the new version | One attestation record exists with the correct person, Policy ID, version and date |
| T4 | Set a Next Review Date in the past (test only) | The policy is flagged as overdue |

Results go in RESULTS.md under Test results.

## 8. Operating and reporting
- Attestation tracker: Team Member, Policy ID, Version, Date Acknowledged, Method. One real acknowledgment from each collaborator.
- Review cycle schedule: each policy, review frequency, next review date, reviewer.
- Both are committed to this folder by pull request, sanitized.

## 9. ISSM decisions (2026-11-16, team chat)
1. Data retention periods in POL-06 (contact form 12 months, invoices 7 years) are documented, not enforced by the build.
2. Approved policies are published on the 340 Collective website; no policy repo access is needed.

## 10. Data handling
This repo is public. Do not commit policy text, personal emails, account IDs, ARNs, real resource names or client data. Attestation records in git use first names or roles only.

## 11. Sign-off
Day 7: Maria commits FINAL-REPORT.md. Adam compares it with RESULTS.md and signs off on the Final report item ("Accepted by: Adam", or findings). Faris merges after sign-off.
