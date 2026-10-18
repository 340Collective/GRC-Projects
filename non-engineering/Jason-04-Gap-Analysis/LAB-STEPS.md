# 340 Collective Gap Analysis - Lab Steps (non-engineering)

Run a mini compliance program gap analysis of 340 Collective against ISO 27001 Annex A or NIST CSF and produce a scored control matrix. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md](../../engineering/Rasheed-04-Gap-Analysis/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Pick one framework (ISO 27001:2022 Annex A or NIST CSF 2.0) and write a 1-page scope summary: systems in scope (the 340collective.com website, the AWS account, Stripe, Google Workspace, GitHub), people in scope, and exclusions.
2. Create a control matrix with columns: Control ID, Requirement, Current Status (Met, Partial, Not Met), Owner, Action Needed.
3. Select at least 15 controls that apply to a small cloud-hosted business, such as access control, MFA, logging, backup, encryption, vendor management, incident response, and policy review.
4. Write the scoring rules: how Met, Partial, and Not Met map to a score, and which evidence source decides each control.
5. Bring the requirements to the Day 1 kickoff. Faris accepts them before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the scope summary, the control matrix, and the scoring rules.

## Test the build

1. When Rasheed says the build is ready, compare the scoring run's result with your matrix for every control.
2. Record a test result as a comment on the project item: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Assess each control against 340 Collective's real setup by checking the AWS Console, GitHub settings, and existing policies. Note the evidence you looked at.
2. Mark every gap, assign an owner, and write a specific action for each (for example, "Enable AWS Config in all Regions").

## Assess or report

1. Sort the gaps by priority and add a short remediation timeline at the bottom of the matrix.
2. Share the scored gap matrix and the remediation timeline with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** ISO 27001 or NIST CSF · scoping · gap assessment · remediation planning

**Tools:** Excel or Google Sheets · Google Docs or Word · AWS Console (read-only) · GitHub settings

**Deliverable:** A 15+ control matrix with gaps marked and a 1-page scope summary.

**What it simulates:** A GRC analyst standing up a compliance program and running the first gap assessment.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
