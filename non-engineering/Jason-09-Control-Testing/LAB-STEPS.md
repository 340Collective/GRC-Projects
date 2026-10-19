# Control Testing and Assessment - Lab Steps (non-engineering)

Conduct a mock internal audit of 340 Collective by testing 10 controls against the artifacts the other projects produced. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-09-Control-Testing/LAB-STEPS.md](../../engineering/Rasheed-09-Control-Testing/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create an internal audit checklist with columns: Control, Test Procedure, Evidence Reviewed, Finding, Severity (High, Medium, Low), Action Plan, Owner, Due Date.
2. Select 10 controls to test, starting with those marked Met in the 04 Gap Analysis control matrix (for example, MFA, logging, encryption, access review, policy attestation, vendor review).
3. For each control, name the population source and the sample size rule, so Rasheed's sampler can draw from it.
4. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the 10-control test plan and procedures.

## Test the build

1. When Rasheed says the build is ready, run one control through Rasheed's workbench and check that the sample reproduces and the workpaper matches your procedure.
2. Write your test result in RESULTS.md under Test results: pass, or findings with what you saw. It is not an approval. Open a pull request.

## Operate it

1. For each control, write a test procedure (inquiry, inspection, or re-performance) and test it using the 06 evidence set, the 07 risk register, the 08 access review, and the 05 policy attestations.
2. Record a pass or a finding for each control, and rate the severity of every finding.

## Assess or report

1. Write a 2-page audit report with scope, approach, a summary of results, each finding with its severity and action plan, and an overall conclusion.
2. Commit the internal audit report to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** Internal audit · control testing · audit documentation · finding severity rating

**Tools:** Excel or Google Sheets · Google Docs or Word · artifacts from projects 04 to 08

**Deliverable:** A completed 10-control audit checklist and a 2-page internal audit report.

**What it simulates:** An internal auditor testing control design and operating effectiveness.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
