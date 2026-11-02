# 08 User Access Reviews - ISSO Requirements

Owner: Adam (ISSO) · Engineer: Abdifatah (IAM / Identity Engineer) · Approver: Faris (ISSM) · Phase 2 (Oct 26 to Nov 1, 2026)

Subject organization: 340 Collective (AWS account)

## 1. Scope
Run a user access review (access certification) of 340 Collective's AWS identities: people, roles, and service identities. Flag over-privilege and drift, record an approver decision for every identity, and track every removal or reduction to completion.

## 2. Identity sources
| Identity type | Source |
|---|---|
| People | Okta group and app-assignment export if project 14 is built; otherwise the IAM credential report plus `aws iam list-groups-for-user` |
| Policies | Attached and inline policies for each IAM user |
| Roles | List of IAM roles exported from AWS |
| Baseline | Access-model template: `infrastructure/cloudformation/grc-access-model.yaml` (summary in `shared/access-model/README.md`) |

Dependency: project 14 supplies the Okta export. If 14 is not finished by build start, use the IAM credential report for people and record the gap as a finding.

## 3. Certification worksheet columns
Identity · Type (Person, Role, Service) · Group or Role · Access Level · Last Activity · Business Justification · Reviewer Decision (Keep, Reduce, Remove) · Approver · Date

## 4. Over-privilege flags
The build must flag each of these automatically:
1. AdministratorAccess on an identity whose justification does not require it
2. Unused credentials (password or access key) with no activity in more than 90 days
3. Access keys on human users
4. Roles or policies with wildcard permissions (`"Action": "*"` or `"Resource": "*"` on write actions)
5. Drift: any user, group, policy, or role that exists live but not in the access-model template (hand-made drift)
6. Human users without MFA (additional ISSO requirement)

## 5. Review rules
| Identity type | Approver |
|---|---|
| Person | Account owner (ISSM) |
| Role | Owning engineer, confirmed by the ISSM |
| Service identity | System owner, confirmed by the ISSM |

- Every row needs a Reviewer Decision, an Approver, and a Date. A blank decision is a failed review.
- "Keep" on a flagged row needs a written Business Justification.
- **Confirmed removal:** the owner confirms in writing, the change is made, and a fresh export shows the access is gone. Nothing is removed without the owner's confirmation.
- One review package per approver, containing only the identities they approve.

## 6. Remediation log
Every Reduce or Remove decision becomes a remediation item:

Item ID · Identity · Decision · Reason (flag) · Owner · Target date · Completed date · Verified by

Target dates: Admin or wildcard findings within 7 days; other findings within 30 days.

## 7. Acceptance tests (ISSO validation)
| # | Test | Pass condition |
|---|---|---|
| T1 | Practice run on the synthetic `uar-simulation` dataset | All six flag types in section 4 are detected |
| T2 | Run one live campaign | One package is generated per approver |
| T3 | Record decisions | Every row has a decision, approver, and date |
| T4 | Removal control | No removal happens without the owner's confirmation |
| T5 | Drift check | Live identities not in the template are flagged |

Results go in RESULTS.md under Test results.

## 8. Data handling
This repo is public. Commit sanitized results only: no account IDs, ARNs, real usernames, real resource names, or personal emails. Use tokens such as `user-01` and `role-03`.

## 9. Sign-off
Day 7: Abdifatah commits FINAL-REPORT.md. Adam compares it with RESULTS.md and signs off on the Final report item ("Accepted by: Adam", or findings). Faris merges after sign-off.
