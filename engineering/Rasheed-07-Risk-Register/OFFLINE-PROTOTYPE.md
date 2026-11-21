# Project 07 offline prototype

Status: offline simulation. The baseline was merged in [PR #180](https://github.com/340Collective/GRC-Projects/pull/180). The sample register contains 12 synthetic risks across all three categories. The prototype reads only the provided JSON file, writes to standard output, and makes no network calls. No AWS deployment or live acceptance is claimed.

## Run locally

From this project folder, with Python 3 and no extra packages:

```bash
python3 -B risk_register.py examples/synthetic_risks.json --as-of 2026-11-10
python3 -B risk_register.py examples/synthetic_risks.json --as-of 2026-11-10 --format html > /tmp/risk07-simulation.html
python3 -B -m unittest discover -s tests -v
```

Inputs are a JSON array. Each risk has `risk_id` (`R-001` to `R-999`), `category` (`Security`, `Vendor`, or `Business`), `description`, `owner_role`, `mitigation`, `likelihood`, `impact`, `residual_likelihood`, `residual_impact`, and `assessed_on` (`YYYY-MM-DD`). Enter only synthetic content. Provide one sentence describing the threat, asset and impact, a named role, and a specific mitigation. Review that content by eye; the prototype checks its structure.

Empty registers are rejected with an error and no report. Owner labels ending in Team, Department, Group or Committee are rejected, including plurals and case or punctuation variants. Job titles such as Team Lead remain valid. The operator must still confirm that the role exists and is accountable. Paths through `private-evidence`, including resolved symlink targets, are refused before reading the input.

`R-004` explicitly models loss of synthetic client files from an incomplete backup, covering that minimum-content example in the requirements. It contains no actual client data.

## Scoring model

Use one official score: **Likelihood x Impact**, as specified in the merged [ISSO requirements](../../non-engineering/Adam-07-Risk-Register/REQUIREMENTS.md). Both factors are integers from 1 to 5. The same method scores the residual risk; it cannot exceed the inherent score. High residual risk is flagged for written ISSM acceptance.

The first three synthetic records reproduce the numeric inputs and expected results from the [seed workbook](../../non-engineering/Adam-07-Risk-Register/07-risk-register-lab.xlsx). The workbook formulas use a Medium cutoff of 8; the requirements specify 7. No pair of valid factors produces 7, so the formulas classify all 25 cells the same way. The examples use the requirements' three-digit ID format.

All 12 filled workbook rows were checked for the baseline. Most rating cells contain typed values; `Risk Register!G11` is the incorrect label, marking `R-07` Medium although 2 x 3 = 6 is Low under both sets of rules. The [ISSO decision](https://github.com/340Collective/GRC-Projects/issues/35#issuecomment-6782801021) confirms that error. The prototype uses Low and the 180-day interval. The partner's workbook correction is in [PR #189](https://github.com/340Collective/GRC-Projects/pull/189).

The ISSO decision confirms Likelihood x Impact for both inherent and residual risk, with no DREAD+ inputs. The older design is being aligned separately. This review is for the offline scoring and reporting code only.

## What this exercises

- Score, rating, residual risk and the 5x5 heat map on synthetic input (offline portions of T1 and T4).
- Review dates calculated from the assessment date and inherent rating (30, 90 or 180 days). A risk is due on or after its review date. This is an explicit prototype assumption and local T3 logic; scheduled alerts remain to be tested.
- Top five by inherent score, with ties sorted by Risk ID. The summary includes the owner role, residual score and next review date.

The cloud design, access permissions, approved Jira route, one-ticket-per-risk behavior (T2), scheduled escalation, ASFF control mapping and 09/12 integration are outside this local prototype. No operating evidence or partner acceptance is claimed.

### Review cadence decision still needed

Section 3 of the requirements sets 30, 90 and 180 days by rating without choosing inherent or residual rating. This follow-up preserves the existing inherent-rating calculation. Before the live T3 timer test, the ISSO needs to confirm which rating determines the interval. No new cadence approval or scheduled-test result is claimed.

## Threat model recorded on issue 35

The offline prototype's threat model is [recorded on issue #35](https://github.com/340Collective/GRC-Projects/issues/35#issuecomment-6799831753). This table is its local reference, not a pending publication.

| Asset | Abuse case | Control in this prototype | Residual risk |
| --- | --- | --- | --- |
| Scores and review dates | Someone submits a score or rating that overrides the calculation. | Reject unknown fields and invalid factors. Compute both scores and dates from validated inputs. | A human must still justify the factor ratings. |
| Local report | Text in a risk record is interpreted as HTML or script. | Escape all risk text before rendering. The report loads no external content. | Only open reports generated by the reviewed script. |
| Input data | Someone runs the script on a real register. | Ship synthetic examples only. Read the supplied JSON path, reject private evidence paths and make no network calls. | The operator must verify that any replacement input is synthetic. |
| Acceptance record | A simulation is treated as written risk acceptance. | Label the report as a simulation and flag high residual risks for written ISSM acceptance. | The actual approval must be recorded separately. |
