# Project 07 Risk Register: ISSO Results

**Validator:** Adam (ISSO)
**Date:** 2026-11-18
**Build tested:** Rasheed's offline prototype, PR #180 (`engineering/Rasheed-07-Risk-Register/risk_register.py`), run in CloudShell with Python 3. The prototype reads a local JSON file and makes no network or AWS calls.
**Scope note:** the prototype is offline only. Jira tickets (one per risk) and the scheduled review alerts are not part of this build, so those tests are recorded as not yet testable.

## Test results

### Test 1: three seed risks scored by the build match my workbook: PASS

Input: R-01, R-02 and R-03 from my workbook (same likelihood, impact, residual factors and assessment dates; sanitized descriptions), run with `--as-of 2026-11-18`.

| Risk | Workbook inherent | Build inherent | Workbook residual | Build residual | Workbook review date | Build review date | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | 20 High | 20 High | 10 Medium | 10 Medium | 2026-11-15 | 2026-11-15 | PASS |
| R-002 | 16 High | 16 High | 6 Low | 6 Low | 2026-11-12 | 2026-11-12 | PASS |
| R-003 | 8 Medium | 8 Medium | 4 Low | 4 Low | 2026-12-12 | 2026-12-12 | PASS |

Also confirmed:
- Review due: R-001 and R-002 are flagged as due (their review dates have passed); R-003 is not due.
- Heat map: R-001 is placed at likelihood 4 / impact 5, R-002 at 4 / 4, R-003 at 2 / 4, matching my workbook heat map.
- ISSM acceptance: no risk is flagged, which is correct because no residual risk is High.
- Top five ordering: by inherent score (R-001, R-002, R-003).

### Test 2: the build's unit tests pass: PASS

`python3 -B -m unittest discover -s tests -v` result: Ran 15 tests, OK.

### Not yet testable in this build

- One Jira ticket per risk (T2)
- Scheduled review reminder and escalation (T3)
- Integration with projects 09 and 12

## Operating results

- Mitigation and owner assigned for all 12 risks; residual risk scored for each (workbook, Risk Register tab).
- 5x5 heat map built for inherent and residual risk (workbook, Heat Map tab).
- Top five risk summary: [TOP5-RISK-SUMMARY.md](TOP5-RISK-SUMMARY.md).
- Workbook correction: R-07 rating fixed from Medium to Low (2 x 3 = 6); the cell held a typed value and now uses the rating formula, per the ISSO decision on issue #35.

## Findings

- None against the build. The offline scoring, ratings, residual scores, review dates and heat map placement all match my workbook.
- Operating finding: R-01 and R-02 are past their review dates (2026-11-15 and 2026-11-12) and are due for review by their owners.

## Comparison with FINAL-REPORT.md

Pending: Rasheed has not yet committed FINAL-REPORT.md for project 07. I will compare it with these results and sign off on the Final report item (#87).

Validated by: Adam (ISSO), 2026-11-18
