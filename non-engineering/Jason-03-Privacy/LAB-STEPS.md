# Privacy Operations - Lab Steps (non-engineering)

Build 340 Collective's data map, PII inventory, DSAR runbook, and consent register by hand. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-03-Privacy/LAB-STEPS.md](../../engineering/Maria-03-Privacy/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create a Records of Processing (RoPA) spreadsheet with columns: Processing Activity, Purpose, Data Categories, Data Subjects, Lawful Basis, Source, Storage Location (generic, such as "AWS account, S3"), Recipients, Retention Period, Owner.
2. Fill one row each for the 340collective.com contact form, newsletter sign-ups, Stripe checkout and invoicing, and client file delivery.
3. Build a PII inventory tab listing every personal data field collected (name, email, phone, billing details) with its sensitivity level and where it is stored or shared.
4. Write the DSAR requirements the workflow must meet: request types, identity check, the approval point, and the response deadline.
5. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the RoPA fields, the PII inventory, and the DSAR requirements.

## Test the build

1. When Maria says the build is ready, run one synthetic access request and one synthetic deletion request through Maria's workflow and check each step against your runbook.
2. Write your test result in RESULTS.md under Test results: pass, or findings with what you saw. It is not an approval. Open a pull request.

## Operate it

1. Write a DSAR fulfillment runbook covering intake, identity verification, locating records across each system in the RoPA, response templates for access and deletion requests, and the response deadline. Walk through it once with a synthetic test subject.
2. Create a consent and opt-out register with columns: Subject ID (pseudonymous), Channel, Consent Given, Date, Opt-Out Date, Source of Record.

## Assess or report

1. Commit the synthetic DSAR walkthrough and the consent register to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** Data mapping · RoPA · DSAR handling · consent management · privacy by design

**Tools:** Excel or Google Sheets · Google Docs or Word · Stripe Dashboard (read-only) · AWS Console (read-only)

**Deliverable:** RoPA and PII inventory workbook, a written DSAR runbook with one synthetic walkthrough, and a consent and opt-out register.

**What it simulates:** A privacy analyst maintaining a processing inventory and handling data subject requests.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
