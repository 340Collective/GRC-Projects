# Third-Party and Vendor Risk Management - Lab Steps (non-engineering)

Build a vendor assessment questionnaire and scorecard, then run it against the vendors 340 Collective already depends on. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-02-TPRM-VRM/LAB-STEPS.md](../../engineering/Maria-02-TPRM-VRM/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Draft a 25-question vendor security questionnaire covering access control, encryption, incident response, business continuity, data handling, subprocessors, and compliance certifications.
2. Add a scoring column with Yes = 2, Partial = 1, No = 0, and a weight column so critical questions (encryption, breach notification) count double.
3. Write the tier rules: the weighted score bands for High, Medium, and Low, and the reassessment interval for each tier.
4. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the questionnaire, weights, and tier rules.

## Test the build

1. When Maria says the build is ready, run one synthetic vendor through the pipeline and compare its weighted score and tier with your sheet.
2. Write your test result in RESULTS.md under Test results: pass, or findings with what you saw. It is not an approval. Open a pull request.

## Operate it

1. Answer the questionnaire for AWS, Stripe, and 340 Collective's domain registrar using only their public trust center pages, SOC 2 summaries, and security documentation. Record the source link for each answer.
2. Build a vendor risk scorecard with columns: Vendor, Service Provided, Data Shared, Weighted Score, Risk Tier (High, Medium, Low), Reassessment Date.

## Assess or report

1. Write a 1-page vendor risk report that summarizes each vendor's tier, the weakest answers, and any follow-up requests 340 Collective should send.
2. Commit the three-vendor scorecard and the vendor risk report to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** Third-party risk management · questionnaire design · risk scoring · vendor due diligence

**Tools:** Excel or Google Sheets · Google Docs or Word · vendor trust center pages

**Deliverable:** 25-question vendor questionnaire, a completed scorecard for three vendors, and a 1-page vendor risk report.

**What it simulates:** A TPRM analyst onboarding and tiering critical vendors.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
