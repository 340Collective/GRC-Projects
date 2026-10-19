# Control Testing and Assessment - Lab Steps (non-engineering)

Conduct a mock internal audit of 340 Collective by testing 10 controls against the artifacts the other projects produced. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-09-Control-Testing/LAB-STEPS.md](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create an internal audit checklist with columns: Control, Test Procedure, Evidence Reviewed, Finding, Severity (High, Medium, Low), Action Plan, Owner, Due Date.
2. Select 10 controls to test, starting with those marked Met in the 04 Gap Analysis control matrix (for example, MFA, logging, encryption, access review, policy attestation, vendor review).
3. For each control, name the population source and the sample size rule, so Rasheed's sampler can draw from it.
4. Bring the requirements to the Day 1 kickoff. Faris accepts them before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the 10-control test plan and procedures.

## Test the build

1. When Rasheed says the build is ready, run one control through Rasheed's workbench and check that the sample reproduces and the workpaper matches your procedure.
2. Record a test result as a comment on the project item: pass, or findings with what you saw. It is not an approval.

## Operate it

1. For each control, write a test procedure (inquiry, inspection, or re-performance) and test it using the 06 evidence set, the 07 risk register, the 08 access review, and the 05 policy attestations.
2. Record a pass or a finding for each control, and rate the severity of every finding.

## Assess or report

1. Write a 2-page audit report with scope, approach, a summary of results, each finding with its severity and action plan, and an overall conclusion.
2. Share the internal audit report with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

**Skills:** Internal audit · control testing · audit documentation · finding severity rating

**Tools:** Excel or Google Sheets · Google Docs or Word · artifacts from projects 04 to 08

**Deliverable:** A completed 10-control audit checklist and a 2-page internal audit report.

**What it simulates:** An internal auditor testing control design and operating effectiveness.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
