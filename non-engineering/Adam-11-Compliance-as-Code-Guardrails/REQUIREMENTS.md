# 11 Compliance-as-Code Guardrails - ISSO Requirements

Owner: Adam (ISSO) · Engineer: Faris (ISSM, builds 11) · Requirements reviewer: Jason · Final approval: Adam · Phase 3 (Nov 2 to 8, 2026)

Subject organization: 340 Collective.

## 1. Scope
Prevent non-compliant AWS changes before they deploy, and detect any that slip through. Each guardrail is enforced as code (Rego gate, Config rule or SCP) and mapped to the control it enforces.

## 2. Guardrail list
| ID | Guardrail | Rule type | Control it enforces |
|---|---|---|---|
| GR-01 | S3 buckets block public access unless an approved exception exists | Rego, Config | SOC 2 CC6.1, CC6.6 · ISO 27001 A.8.3 |
| GR-02 | S3 buckets are encrypted at rest (SSE-KMS or SSE-S3) | Rego, Config | SOC 2 CC6.1 · ISO 27001 A.8.24 |
| GR-03 | CloudTrail stays enabled; `StopLogging` and `DeleteTrail` are denied | Config, SCP | SOC 2 CC7.2 · ISO 27001 A.8.15 |
| GR-04 | No IAM users with access keys; humans use IAM Identity Center | Rego, Config | SOC 2 CC6.1 · ISO 27001 A.5.17, A.8.5 |
| GR-05 | Every resource carries an `owner` tag | Rego, Config | SOC 2 CC6.1 · ISO 27001 A.5.9 |
| GR-06 | Resources deploy only in approved regions (proposed: us-east-1 only, pending ISSM confirmation) | Rego, SCP | SOC 2 CC8.1 · ISO 27001 A.5.23 |
| GR-07 | Root user has MFA and no access keys | Config | SOC 2 CC6.1 · ISO 27001 A.8.2 |
| GR-08 | Security groups do not allow 0.0.0.0/0 on SSH (22) or RDP (3389) | Rego, Config | SOC 2 CC6.6 · ISO 27001 A.8.20 |

SCPs need an AWS Organization. If the account is not in one, the SCP layer is recorded as planned and the Rego gate plus Config rules carry the prevention.

## 3. Exceptions
- Every exception needs: guardrail ID, resource, reason, owner, approver, and expiry date.
- Approver: **ISSO (Adam)**. Maximum duration: **90 days**; renewal needs a new approval.
- An expired exception fails the build again, and the ISSO flags it on the project item.

## 4. Build requirements (Faris)
1. Rego policy for each guardrail marked Rego, with one passing and one failing example template each.
2. Config rule for each guardrail marked Config.
3. SCP outline that denies the actions in GR-03 and GR-06.
4. Failed gate results become Security Hub findings (rule ID, resource, commit, severity).
5. Exceptions are read from a reviewed exception file; expired entries are ignored.

## 5. Acceptance tests (ISSO validation)
| # | Test | Pass condition |
|---|---|---|
| T1 | Run each Rego rule against its failing example | The gate fails and names the guardrail ID |
| T2 | Run each Rego rule against its passing example | The gate passes |
| T3 | Compare Config rules with section 2 | Every Config guardrail has a matching rule |
| T4 | Read the SCP outline | It denies the actions listed for GR-03 and GR-06 |
| T5 | Add an expired exception | The build fails again |

Results go in RESULTS.md under Test results.

## 6. Reporting
Guardrail register: Guardrail ID, Rule Type, What It Blocks, Control It Enforces, Owner. Committed to this folder by pull request, sanitized.

## 7. Open questions for the ISSM
1. Confirm the approved region list for GR-06 (proposed: us-east-1 only, the region the repo's stacks use).
2. Confirm whether the account is in an AWS Organization, so the SCP layer is built or recorded as planned.

## 8. Data handling
This repo is public. Example templates use placeholder names only. No account IDs, ARNs, real bucket names or personal emails.

## 9. Sign-off
Day 7: Faris commits FINAL-REPORT.md. Adam compares it with RESULTS.md, signs off and gives final approval on the Final report item ("Accepted by: Adam", or findings), since Faris built 11. Faris merges after sign-off.
