# 340 Collective Gap Analysis - Lab Steps (non-engineering)

Run a mini compliance program gap analysis of 340 Collective against ISO 27001 Annex A or NIST CSF and produce a scored control matrix. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md](../../engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Pick one framework (ISO 27001:2022 Annex A or NIST CSF 2.0) and write a 1-page scope summary: systems in scope (the 340collective.com website, the AWS account, Stripe, Google Workspace, GitHub), people in scope, and exclusions.
2. Create a control matrix with columns: Control ID, Requirement, Current Status (Met, Partial, Not Met), Owner, Action Needed.
3. Select at least 15 controls that apply to a small cloud-hosted business, such as access control, MFA, logging, backup, encryption, vendor management, incident response, and policy review.
4. Write the scoring rules: how Met, Partial, and Not Met map to a score, and which evidence source decides each control.
5. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the scope summary, the control matrix, and the scoring rules.

## Test the build

1. When Rasheed says the build is ready, compare the scoring run's result with your matrix for every control.
2. Write your test result in RESULTS.md under Test results: pass, or findings with what you saw. It is not an approval. Open a pull request.

## Operate it

1. Assess each control against 340 Collective's real setup by checking the AWS Console, GitHub settings, and existing policies. Note the evidence you looked at.
2. Mark every gap, assign an owner, and write a specific action for each (for example, "Enable AWS Config in all Regions").

## Assess or report

1. Sort the gaps by priority and add a short remediation timeline at the bottom of the matrix.
2. Commit the scored gap matrix and the remediation timeline to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** ISO 27001 or NIST CSF · scoping · gap assessment · remediation planning

**Tools:** Excel or Google Sheets · Google Docs or Word · AWS Console (read-only) · GitHub settings

**Deliverable:** A 15+ control matrix with gaps marked and a 1-page scope summary.

**What it simulates:** A GRC analyst standing up a compliance program and running the first gap assessment.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
