# GRC Metrics and Board Reporting - Lab Steps (non-engineering)

Build a compliance dashboard for 340 Collective from the risk register and control matrix, then export it for leadership. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md](../../engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Pull source data into one workbook or Notion page: the 04 control matrix, the 07 risk register, the 08 access review results, and the 10 findings log.
2. Define 6 to 8 metrics with a target for each, such as percent of controls Met, number of High risks open, percent of findings remediated within SLA, policy attestation rate, and days since last access review.
3. Set the red, amber, and green thresholds for each metric.
4. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the metric definitions, targets, and thresholds.

## Test the build

1. When Rasheed says the build is ready, compare the values on the GRC Metrics Jira issue with your workbook for each metric, and build your Jira dashboard on that issue.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. Then record your validation on the Final report item.

## Operate it

1. Build the dashboard with a control coverage chart, a risk status breakdown by tier, a remediation progress bar, and a KRI/KPI table using red, amber, and green thresholds.
2. Add a short commentary box that explains the biggest change since the last review and the top action needed.

## Assess or report

1. Export a screenshot or PDF of the finished dashboard.
2. Commit the board pack export and your commentary to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Metrics design · KRIs and KPIs · data visualization · executive reporting

**Tools:** Excel or Google Sheets · Notion · artifacts from projects 04, 07, 08, and 10

**Deliverable:** A compliance dashboard with KRIs and KPIs, plus an exported screenshot or PDF.

**What it simulates:** A GRC analyst reporting program health to leadership or the board.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
