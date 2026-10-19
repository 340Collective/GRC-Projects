# Privacy Operations - Lab Steps (non-engineering)

Build 340 Collective's data map, PII inventory, DSAR runbook, and consent register by hand. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-03-Privacy/LAB-STEPS.md](../../engineering/Maria-03-Privacy/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create a Records of Processing (RoPA) spreadsheet with columns: Processing Activity, Purpose, Data Categories, Data Subjects, Lawful Basis, Source, Storage Location (generic, such as "AWS account, S3"), Recipients, Retention Period, Owner.
2. Fill one row each for the 340collective.com contact form, newsletter sign-ups, Stripe checkout and invoicing, and client file delivery.
3. Build a PII inventory tab listing every personal data field collected (name, email, phone, billing details) with its sensitivity level and where it is stored or shared.
4. Write the DSAR requirements the workflow must meet: request types, identity check, the approval point, and the response deadline.
5. Bring the requirements to the Day 1 kickoff. Faris accepts them before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the RoPA fields, the PII inventory, and the DSAR requirements.

## Test the build

1. When Maria says the build is ready, run one synthetic access request and one synthetic deletion request through Maria's workflow and check each step against your runbook.
2. Record a test result as a comment on the project item: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Write a DSAR fulfillment runbook covering intake, identity verification, locating records across each system in the RoPA, response templates for access and deletion requests, and the response deadline. Walk through it once with a synthetic test subject.
2. Create a consent and opt-out register with columns: Subject ID (pseudonymous), Channel, Consent Given, Date, Opt-Out Date, Source of Record.

## Assess or report

1. Share the synthetic DSAR walkthrough and the consent register with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

**Skills:** Data mapping · RoPA · DSAR handling · consent management · privacy by design

**Tools:** Excel or Google Sheets · Google Docs or Word · Stripe Dashboard (read-only) · AWS Console (read-only)

**Deliverable:** RoPA and PII inventory workbook, a written DSAR runbook with one synthetic walkthrough, and a consent and opt-out register.

**What it simulates:** A privacy analyst maintaining a processing inventory and handling data subject requests.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
