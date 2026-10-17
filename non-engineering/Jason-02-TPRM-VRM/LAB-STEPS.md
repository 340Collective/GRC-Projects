# Third-Party and Vendor Risk Management - Lab Steps (non-engineering)

Build a vendor assessment questionnaire and scorecard, then run it against the vendors 340 Collective already depends on. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-02-TPRM-VRM/LAB-STEPS.md](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Draft a 25-question vendor security questionnaire covering access control, encryption, incident response, business continuity, data handling, subprocessors, and compliance certifications.
2. Add a scoring column with Yes = 2, Partial = 1, No = 0, and a weight column so critical questions (encryption, breach notification) count double.
3. Write the tier rules: the weighted score bands for High, Medium, and Low, and the reassessment interval for each tier.
4. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Maria starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Maria once Faris accepts it: the questionnaire, weights, and tier rules.

## Accept the build

1. When Maria creates the Handoff 2 Jira Task, run one synthetic vendor through the pipeline and compare its weighted score and tier with your sheet.
2. Record an acceptance test result on the Task: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Answer the questionnaire for AWS, Stripe, and 340 Collective's domain registrar using only their public trust center pages, SOC 2 summaries, and security documentation. Record the source link for each answer.
2. Build a vendor risk scorecard with columns: Vendor, Service Provided, Data Shared, Weighted Score, Risk Tier (High, Medium, Low), Reassessment Date.

## Assess or report

1. Write a 1-page vendor risk report that summarizes each vendor's tier, the weakest answers, and any follow-up requests 340 Collective should send.
2. Create the Handoff 3 Jira Task for Faris with the three-vendor scorecard and the vendor risk report.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: vendor questionnaire, weights, and tier rules, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: vendor intake and scoring pipeline ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: three-vendor scorecard and vendor risk report, Jason to Faris (Jira Task, created by Jason)

**Skills:** Third-party risk management · questionnaire design · risk scoring · vendor due diligence

**Tools:** Excel or Google Sheets · Google Docs or Word · vendor trust center pages

**Deliverable:** 25-question vendor questionnaire, a completed scorecard for three vendors, and a 1-page vendor risk report.

**What it simulates:** A TPRM analyst onboarding and tiering critical vendors.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
