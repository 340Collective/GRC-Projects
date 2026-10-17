# Control Testing and Assessment - Lab Steps (non-engineering)

Conduct a mock internal audit of 340 Collective by testing 10 controls against the artifacts the other projects produced. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-09-Control-Testing/LAB-STEPS.md](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create an internal audit checklist with columns: Control, Test Procedure, Evidence Reviewed, Finding, Severity (High, Medium, Low), Action Plan, Owner, Due Date.
2. Select 10 controls to test, starting with those marked Met in the 04 Gap Analysis control matrix (for example, MFA, logging, encryption, access review, policy attestation, vendor review).
3. For each control, name the population source and the sample size rule, so Rasheed's sampler can draw from it.
4. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Rasheed starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Rasheed once Faris accepts it: the 10-control test plan and procedures.

## Accept the build

1. When Rasheed creates the Handoff 2 Jira Task, run one control through Rasheed's workbench and check that the sample reproduces and the workpaper matches your procedure.
2. Record an acceptance test result on the Task: pass, or findings with what you saw. It is not an approval.

## Operate it

1. For each control, write a test procedure (inquiry, inspection, or re-performance) and test it using the 06 evidence set, the 07 risk register, the 08 access review, and the 05 policy attestations.
2. Record a pass or a finding for each control, and rate the severity of every finding.

## Assess or report

1. Write a 2-page audit report with scope, approach, a summary of results, each finding with its severity and action plan, and an overall conclusion.
2. Create the Handoff 3 Jira Task for Faris with the internal audit report.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: 10-control test plan and procedures, Jason to Rasheed (Jira Task, created by Jason)
- Handoff 2: test automation and sampling ready for acceptance testing, Rasheed to Jason (Jira Task, created by Rasheed)
- Handoff 3: internal audit report, Jason to Faris (Jira Task, created by Jason)

**Skills:** Internal audit · control testing · audit documentation · finding severity rating

**Tools:** Excel or Google Sheets · Google Docs or Word · artifacts from projects 04 to 08

**Deliverable:** A completed 10-control audit checklist and a 2-page internal audit report.

**What it simulates:** An internal auditor testing control design and operating effectiveness.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
