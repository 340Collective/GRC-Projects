# Audit Engagement Manager - Lab Steps (non-engineering)

Run a mock external audit engagement for 340 Collective, from the request list through findings and remediation. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Assign roles: one collaborator acts as the external auditor and another as the 340 Collective control owner.
2. Have the auditor build a PBC (provided-by-client) request list with columns: Request ID, Control, Item Requested, Requested Date, Due Date, Owner, Status.
3. Build a findings-and-remediation log with columns: Finding ID, Description, Severity, Owner, Remediation Plan, SLA Due Date (for example, 30 days for High, 60 for Medium, 90 for Low), Status, Date Closed.
4. Bring the requirements to the Day 1 kickoff. Faris accepts them before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the PBC request list template and the findings SLA rules.

## Test the build

1. When Maria says the build is ready, run one synthetic PBC request and one finding through Maria's tracker and check the owner, the due date, the reminder, and the finding path.
2. Record a test result as a comment on the project item: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Create an evidence intake tracker that logs each item received: Request ID, File Name, Date Received, Complete (Yes or No), Auditor Comments. Answer requests using the 06 evidence set and 09 workpapers.

## Assess or report

1. Hold a short closing meeting and write a 1-page engagement status summary: requests fulfilled, late items, open findings, and next steps.
2. Share the engagement status summary with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

**Skills:** Audit coordination · PBC management · findings tracking · SLA management

**Tools:** Excel or Google Sheets · Google Docs or Word · artifacts from projects 06 and 09

**Deliverable:** A PBC request list, an evidence intake tracker, a findings-and-remediation log, and a 1-page engagement status summary.

**What it simulates:** A compliance lead managing an external audit from kickoff to closeout.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
