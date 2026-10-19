# Final report: <NN> <Project name>

The engineer writes this report: what was built and what the builder's tests showed. It is due on day 7 of the build week. The partner's results are not in this report. They live in the partner's own folder, and section 8 links to them. Copy this file to `engineering/<Name>-NN-<Project>/FINAL-REPORT.md`, fill in every heading, and open a pull request. Faris merges it after the partner signs off on the Final report item. Sanitized content only: no account IDs, ARNs, emails, secrets, or raw evidence (see the data rules in [CONTRIBUTING.md](../../CONTRIBUTING.md)).

Engineer: <first name>. Partner: <first name>. Build week: <Week N, dates>. Jira epic: <GRC-NN>.

## 1. Summary

What was built, and which controls it covers (ASFF `SecurityControlId` values).

## 2. Before (manual)

How it was done by hand: the steps, the time it took, and who did it.

## 3. After (automated)

What runs now, how often it runs, and who is notified.

## 4. Metrics

Time saved, control coverage, findings caught, and time to remediate, from the builder's tests.

## 5. Evidence

Links to sanitized evidence (redacted screenshots, summary tables) plus the hash manifest.

## 6. Cost

Actual AWS spend during the build week.

## 7. Test cleanup and handover

Test artifacts deleted (test data, restored copies, temporary users, trial-only resources). What stays running in the shared system: stack name, schedules, and expected monthly cost. The end-of-program teardown steps are in LAB-STEPS.md.

## 8. Sign-off

Partner results: link to `non-engineering/<Partner>-NN-<Project>/RESULTS.md` (template: [RESULTS.md](RESULTS.md)). The partner writes it; the engineer does not.

Sign-off: link to the partner's comment on the Final report item ("Accepted by: <first name>", or findings).

Validation: link to Adam's validation comment on the Final report item.

Phase assessment: link to Jason's phase assessment item.
