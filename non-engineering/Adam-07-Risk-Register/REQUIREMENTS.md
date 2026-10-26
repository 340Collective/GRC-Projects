# 07 Risk Register - ISSO Requirements

Owner: Adam (ISSO) · Engineer: Rasheed (ISSE) · Approver: Faris (ISSM) · Phase 2 (Oct 26 to Nov 1, 2026)

Subject organization: 340 Collective. Lab sheet: [07-risk-register-lab.xlsx](07-risk-register-lab.xlsx)

## 1. Scope
Build and operate 340 Collective's risk register: identify, score, and track risks across security, vendor, and business categories, with a heat map and a top-five risk summary.

## 2. Register fields
Every risk must have all of these fields:

| Field | Rule |
|---|---|
| Risk ID | Unique, format `R-001` |
| Category | Security, Vendor, or Business |
| Description | One sentence: threat, asset, and impact |
| Likelihood | 1 to 5 (see scale below) |
| Impact | 1 to 5 (see scale below) |
| Risk Score | Likelihood x Impact (1 to 25), calculated, never typed by hand |
| Mitigation | Specific action, not "monitor" alone |
| Owner | A named role (for example ISSM, ISSE), not a team |
| Residual Risk | Re-scored Likelihood x Impact after mitigation |
| Review Date | Set by the review cadence below |

## 3. Scoring rules

**Likelihood:** 1 Rare · 2 Unlikely · 3 Possible · 4 Likely · 5 Almost certain

**Impact:** 1 Negligible · 2 Minor · 3 Moderate · 4 Major · 5 Severe

| Score | Rating | Color | Review cadence |
|---|---|---|---|
| 15 to 25 | High | Red | Every 30 days |
| 7 to 14 | Medium | Amber | Every 90 days |
| 1 to 6 | Low | Green | Every 180 days |

- Residual Risk must be equal to or lower than the inherent Risk Score. If not, the mitigation needs rework.
- A High residual risk needs a written risk acceptance from the ISSM.

## 4. Minimum content
At least 12 risks covering all three categories, including the lab examples: compromised AWS credentials, Stripe payment link misuse, domain registrar lapse, loss of client files, and single-person dependency.

## 5. Build requirements (Rasheed)
1. Calculates Risk Score and Residual Risk automatically from Likelihood and Impact.
2. Applies High / Medium / Low labels and colors using the thresholds in section 3.
3. Creates one Jira ticket per risk, linked by Risk ID.
4. Runs a review timer that flags each risk when its Review Date is reached.
5. Produces a 5x5 heat map that plots each Risk ID by likelihood and impact.

## 6. Acceptance tests (ISSO validation)
| # | Test | Pass condition |
|---|---|---|
| T1 | Enter 3 seed risks through the build | Scores and ratings match the lab sheet exactly |
| T2 | Check Jira | One ticket exists per seed risk, with matching Risk ID |
| T3 | Trigger one review timer | The risk is flagged on its Review Date |
| T4 | Check the heat map | Each seed risk appears in the correct cell |

Results go in RESULTS.md under Test results.

## 7. Reporting
- Half-page summary of the top five risks, with owners and the next review date.
- 5x5 heat map of the full register.

## 8. Data handling
This repo is public. Do not commit account IDs, ARNs, real resource names, personal emails, or client data. Use generic descriptions in the register.

## 9. Sign-off
Day 7: Rasheed commits FINAL-REPORT.md. Adam compares it with RESULTS.md and signs off on the Final report item ("Accepted by: Adam", or findings). Faris merges after sign-off.
