# Project 07 Risk Register: Top Five Risk Summary

**Prepared by:** Adam (ISSO)
**As of:** 2026-11-16
**Source:** [07-risk-register-lab.xlsx](07-risk-register-lab.xlsx) (Summary tab). Scoring is Likelihood x Impact (1 to 25): High 15 to 25, Medium 8 to 14, Low 1 to 7.

This register is a learning exercise. All content is sanitized: no account IDs, ARNs, real resource names, personal emails or client data.

## Top five risks (by inherent score)

| Rank | Risk ID | Risk | Inherent | Residual | Owner | Next review |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | R-01 | AWS root or admin credentials compromised | 20 High | 10 Medium | ISSM | 2026-11-15 (due) |
| 2 | R-02 | Payment links leaked or misused | 16 High | 6 Low | Business Owner | 2026-11-12 (overdue) |
| 3 | R-05 | Phishing steals an email or AWS login | 16 High | 6 Low | Business Owner | 2026-12-12 |
| 4 | R-08 | Single person holds platform knowledge and admin access | 16 High | 6 Low | Business Owner | 2026-12-12 |
| 5 | R-04 | Client files lost with no working backup | 12 Medium | 4 Low | Business Owner | 2026-12-12 |

## Summary

The register identifies 12 risks across security, vendor and business categories. Before mitigation, four risks score High. Each of the top five could stop payments, expose the AWS account or lose client work, which would directly hurt revenue and reputation for a small media studio.

The Business Owner owns four of the top five; the ISSM owns R-01. The key mitigations are MFA on every account, removing root access keys and using least privilege IAM roles, fraud screening and MFA on the payment dashboard, written runbooks with a second trusted admin, and tested 3-2-1 backups. After mitigation every risk drops to Low except R-01, which stays Medium (residual 10) because a full account takeover remains severe. R-01 should remain a leadership priority.

## Decisions and actions needed

1. **Review R-01 and R-02 now.** Their review dates (2026-11-15 and 2026-11-12) have passed.
2. **Confirm owners.** Four of five top risks sit with the Business Owner; leadership should confirm that is workable or assign deputies.
3. **No residual risk is High,** so no written ISSM risk acceptance is required this cycle.

## Change log

- 2026-11-16: corrected R-07 rating in the workbook from Medium to Low (2 x 3 = 6). The cell held a typed value instead of the rating formula; it now uses the same formula as the other rows. Confirmed by the ISSO decision on issue #35.
