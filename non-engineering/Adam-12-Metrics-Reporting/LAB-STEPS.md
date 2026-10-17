# GRC Metrics and Board Reporting - Lab Steps (non-engineering)

Build a compliance dashboard for 340 Collective from the risk register and control matrix, then export it for leadership. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md](../../engineering/Rasheed-12-Metrics-Reporting/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Pull source data into one workbook or Notion page: the 04 control matrix, the 07 risk register, the 08 access review results, and the 10 findings log.
2. Define 6 to 8 metrics with a target for each, such as percent of controls Met, number of High risks open, percent of findings remediated within SLA, policy attestation rate, and days since last access review.
3. Set the red, amber, and green thresholds for each metric.
4. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Rasheed starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Rasheed once Faris accepts it: the metric definitions, targets, and thresholds.

## Accept the build

1. When Rasheed creates the Handoff 2 Jira Task, compare the values on the GRC Metrics Jira issue with your workbook for each metric, and build your Jira dashboard on that issue.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Build the dashboard with a control coverage chart, a risk status breakdown by tier, a remediation progress bar, and a KRI/KPI table using red, amber, and green thresholds.
2. Add a short commentary box that explains the biggest change since the last review and the top action needed.

## Assess or report

1. Export a screenshot or PDF of the finished dashboard.
2. Create the Handoff 3 Jira Task for Faris with the board pack export and your commentary.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: metric definitions, targets, and thresholds, Adam to Rasheed (Jira Task, created by Adam)
- Handoff 2: metrics dashboard ready for acceptance, Rasheed to Adam (Jira Task, created by Rasheed)
- Handoff 3: board pack export with commentary, Adam to Faris (Jira Task, created by Adam)

**Skills:** Metrics design · KRIs and KPIs · data visualization · executive reporting

**Tools:** Excel or Google Sheets · Notion · artifacts from projects 04, 07, 08, and 10

**Deliverable:** A compliance dashboard with KRIs and KPIs, plus an exported screenshot or PDF.

**What it simulates:** A GRC analyst reporting program health to leadership or the board.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
