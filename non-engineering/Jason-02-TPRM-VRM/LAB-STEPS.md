# Third-Party and Vendor Risk Management - Lab Steps (non-engineering)

Build a vendor assessment questionnaire and scorecard, then run it against the vendors 340 Collective already depends on. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-02-TPRM-VRM/LAB-STEPS.md](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Draft a 25-question vendor security questionnaire covering access control, encryption, incident response, business continuity, data handling, subprocessors, and compliance certifications.
2. Add a scoring column with Yes = 2, Partial = 1, No = 0, and a weight column so critical questions (encryption, breach notification) count double.
3. Write the tier rules: the weighted score bands for High, Medium, and Low, and the reassessment interval for each tier.
4. Bring the requirements to the Day 1 kickoff. Faris accepts them before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the questionnaire, weights, and tier rules.

## Test the build

1. When Maria says the build is ready, run one synthetic vendor through the pipeline and compare its weighted score and tier with your sheet.
2. Record a test result as a comment on the project item: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Answer the questionnaire for AWS, Stripe, and 340 Collective's domain registrar using only their public trust center pages, SOC 2 summaries, and security documentation. Record the source link for each answer.
2. Build a vendor risk scorecard with columns: Vendor, Service Provided, Data Shared, Weighted Score, Risk Tier (High, Medium, Low), Reassessment Date.

## Assess or report

1. Write a 1-page vendor risk report that summarizes each vendor's tier, the weakest answers, and any follow-up requests 340 Collective should send.
2. Share the three-vendor scorecard and the vendor risk report with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

**Skills:** Third-party risk management · questionnaire design · risk scoring · vendor due diligence

**Tools:** Excel or Google Sheets · Google Docs or Word · vendor trust center pages

**Deliverable:** 25-question vendor questionnaire, a completed scorecard for three vendors, and a 1-page vendor risk report.

**What it simulates:** A TPRM analyst onboarding and tiering critical vendors.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
