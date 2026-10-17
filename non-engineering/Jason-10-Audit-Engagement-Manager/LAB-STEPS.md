# Audit Engagement Manager - Lab Steps (non-engineering)

Run a mock external audit engagement for 340 Collective, from the request list through findings and remediation. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Assign roles: one collaborator acts as the external auditor and another as the 340 Collective control owner.
2. Have the auditor build a PBC (provided-by-client) request list with columns: Request ID, Control, Item Requested, Requested Date, Due Date, Owner, Status.
3. Build a findings-and-remediation log with columns: Finding ID, Description, Severity, Owner, Remediation Plan, SLA Due Date (for example, 30 days for High, 60 for Medium, 90 for Low), Status, Date Closed.
4. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Maria starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Maria once Faris accepts it: the PBC request list template and the findings SLA rules.

## Accept the build

1. When Maria creates the Handoff 2 Jira Task, run one synthetic PBC request and one finding through Maria's tracker and check the owner, the due date, the reminder, and the finding path.
2. Record an acceptance test result on the Task: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Create an evidence intake tracker that logs each item received: Request ID, File Name, Date Received, Complete (Yes or No), Auditor Comments. Answer requests using the 06 evidence set and 09 workpapers.

## Assess or report

1. Hold a short closing meeting and write a 1-page engagement status summary: requests fulfilled, late items, open findings, and next steps.
2. Create the Handoff 3 Jira Task for Faris with the engagement status summary.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: PBC request list template and findings SLA rules, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: engagement tracker build ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: engagement status summary, Jason to Faris (Jira Task, created by Jason)

**Skills:** Audit coordination · PBC management · findings tracking · SLA management

**Tools:** Excel or Google Sheets · Google Docs or Word · artifacts from projects 06 and 09

**Deliverable:** A PBC request list, an evidence intake tracker, a findings-and-remediation log, and a 1-page engagement status summary.

**What it simulates:** A compliance lead managing an external audit from kickoff to closeout.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
