# Risk Register - Lab Steps (non-engineering)

Build 340 Collective's risk register, score each risk, and visualize the results in a heat map. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-07-Risk-Register/LAB-STEPS.md](../../engineering/Rasheed-07-Risk-Register/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create a spreadsheet with columns: Risk ID, Description, Likelihood (1-5), Impact (1-5), Risk Score, Mitigation, Owner, Residual Risk, Review Date.
2. Identify at least 12 risks to 340 Collective across security, vendor, and business categories (for example, compromised AWS credentials, Stripe payment link misuse, domain registrar lapse, loss of client files, single-person dependency).
3. Calculate Risk Score as Likelihood x Impact and add conditional formatting so High, Medium, and Low scores are easy to spot.
4. Keep the scoring rules and the seed register in [07-risk-register-lab.xlsx](07-risk-register-lab.xlsx).
5. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the risk scoring rules and the seed risk register (lab sheet).

## Test the build

1. When Rasheed says the build is ready, enter three seed risks through Rasheed's build and check the scores against your sheet, the Jira ticket for each, and one review timer.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. After your Day 7 sign-off, record your validation on the Final report item.

## Operate it

1. Write a mitigation and assign an owner for each risk, then re-score to get Residual Risk.
2. Build a 5x5 heat map that plots each Risk ID by likelihood and impact.

## Assess or report

1. Write a half-page risk summary naming the top five risks, their owners, and the next review date.
2. Commit the top five risk summary to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Risk identification · risk scoring · mitigation planning · risk communication

**Tools:** Excel or Google Sheets · Google Docs or Word

**Deliverable:** A scored risk register, a 5x5 heat map, and a half-page risk summary.

**What it simulates:** A risk analyst maintaining an enterprise risk register and reporting top risks.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
