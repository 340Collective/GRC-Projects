# Risk Register - Lab Steps (non-engineering)

Build 340 Collective's risk register, score each risk, and visualize the results in a heat map. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-07-Risk-Register/LAB-STEPS.md](../../engineering/Rasheed-07-Risk-Register/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create a spreadsheet with columns: Risk ID, Description, Likelihood (1-5), Impact (1-5), Risk Score, Mitigation, Owner, Residual Risk, Review Date.
2. Identify at least 12 risks to 340 Collective across security, vendor, and business categories (for example, compromised AWS credentials, Stripe payment link misuse, domain registrar lapse, loss of client files, single-person dependency).
3. Calculate Risk Score as Likelihood x Impact and add conditional formatting so High, Medium, and Low scores are easy to spot.
4. Keep the scoring rules and the seed register in [07-risk-register-lab.xlsx](07-risk-register-lab.xlsx).
5. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Rasheed starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Rasheed once Faris accepts it: the risk scoring rules and the seed risk register (lab sheet).

## Accept the build

1. When Rasheed creates the Handoff 2 Jira Task, enter three seed risks through Rasheed's build and check the scores against your sheet, the Jira ticket for each, and one review timer.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Write a mitigation and assign an owner for each risk, then re-score to get Residual Risk.
2. Build a 5x5 heat map that plots each Risk ID by likelihood and impact.

## Assess or report

1. Write a half-page risk summary naming the top five risks, their owners, and the next review date.
2. Create the Handoff 3 Jira Task for Faris with the top five risk summary.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: risk scoring rules and seed risk register (lab sheet), Adam to Rasheed (Jira Task, created by Adam)
- Handoff 2: risk register build ready for acceptance, Rasheed to Adam (Jira Task, created by Rasheed)
- Handoff 3: top five risk summary, Adam to Faris (Jira Task, created by Adam)

**Skills:** Risk identification · risk scoring · mitigation planning · risk communication

**Tools:** Excel or Google Sheets · Google Docs or Word

**Deliverable:** A scored risk register, a 5x5 heat map, and a half-page risk summary.

**What it simulates:** A risk analyst maintaining an enterprise risk register and reporting top risks.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
