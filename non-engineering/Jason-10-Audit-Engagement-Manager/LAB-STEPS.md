# Audit Engagement Manager - Lab Steps (non-engineering)

Run a mock external audit engagement for 340 Collective, from the request list through findings and remediation. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md](../../engineering/Maria-10-Audit-Engagement-Manager/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Assign roles: one collaborator acts as the external auditor and another as the 340 Collective control owner.
2. Have the auditor build a PBC (provided-by-client) request list with columns: Request ID, Control, Item Requested, Requested Date, Due Date, Owner, Status.
3. Build a findings-and-remediation log with columns: Finding ID, Description, Severity, Owner, Remediation Plan, SLA Due Date (for example, 30 days for High, 60 for Medium, 90 for Low), Status, Date Closed.
4. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the PBC request list template and the findings SLA rules.

## Test the build

1. When Maria says the build is ready, run one synthetic PBC request and one finding through Maria's tracker and check the owner, the due date, the reminder, and the finding path.
2. Write your test result in RESULTS.md under Test results: pass, or findings with what you saw. It is not an approval. Open a pull request.

## Operate it

1. Create an evidence intake tracker that logs each item received: Request ID, File Name, Date Received, Complete (Yes or No), Auditor Comments. Answer requests using the 06 evidence set and 09 workpapers.

## Assess or report

1. Hold a short closing meeting and write a 1-page engagement status summary: requests fulfilled, late items, open findings, and next steps.
2. Commit the engagement status summary to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** Audit coordination · PBC management · findings tracking · SLA management

**Tools:** Excel or Google Sheets · Google Docs or Word · artifacts from projects 06 and 09

**Deliverable:** A PBC request list, an evidence intake tracker, a findings-and-remediation log, and a 1-page engagement status summary.

**What it simulates:** A compliance lead managing an external audit from kickoff to closeout.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
