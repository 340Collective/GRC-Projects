# Risk Register - Lab Steps (non-engineering)

Build 340 Collective's risk register, score each risk, and visualize the results in a heat map. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-07-Risk-Register/LAB-STEPS.md](../../engineering/Rasheed-07-Risk-Register/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create a spreadsheet with columns: Risk ID, Description, Likelihood (1-5), Impact (1-5), Risk Score, Mitigation, Owner, Residual Risk, Review Date.
2. Identify at least 12 risks to 340 Collective across security, vendor, and business categories (for example, compromised AWS credentials, Stripe payment link misuse, domain registrar lapse, loss of client files, single-person dependency).
3. Calculate Risk Score as Likelihood x Impact and add conditional formatting so High, Medium, and Low scores are easy to spot.
4. Keep the scoring rules and the seed register in [07-risk-register-lab.xlsx](07-risk-register-lab.xlsx).
5. Bring the requirements to the Day 1 kickoff. Faris accepts them before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the risk scoring rules and the seed risk register (lab sheet).

## Test the build

1. When Rasheed says the build is ready, enter three seed risks through Rasheed's build and check the scores against your sheet, the Jira ticket for each, and one review timer.
2. Record your test result, or findings, on the project item, then record your validation there.

## Operate it

1. Write a mitigation and assign an owner for each risk, then re-score to get Residual Risk.
2. Build a 5x5 heat map that plots each Risk ID by likelihood and impact.

## Assess or report

1. Write a half-page risk summary naming the top five risks, their owners, and the next review date.
2. Share the top five risk summary with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

**Skills:** Risk identification · risk scoring · mitigation planning · risk communication

**Tools:** Excel or Google Sheets · Google Docs or Word

**Deliverable:** A scored risk register, a 5x5 heat map, and a half-page risk summary.

**What it simulates:** A risk analyst maintaining an enterprise risk register and reporting top risks.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
