# Privacy Operations - Lab Steps (non-engineering)

Build 340 Collective's data map, PII inventory, DSAR runbook, and consent register by hand. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-03-Privacy/LAB-STEPS.md](../../engineering/Maria-03-Privacy/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create a Records of Processing (RoPA) spreadsheet with columns: Processing Activity, Purpose, Data Categories, Data Subjects, Lawful Basis, Source, Storage Location (generic, such as "AWS account, S3"), Recipients, Retention Period, Owner.
2. Fill one row each for the 340collective.com contact form, newsletter sign-ups, Stripe checkout and invoicing, and client file delivery.
3. Build a PII inventory tab listing every personal data field collected (name, email, phone, billing details) with its sensitivity level and where it is stored or shared.
4. Write the DSAR requirements the workflow must meet: request types, identity check, the approval point, and the response deadline.
5. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Maria starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Maria once Faris accepts it: the RoPA fields, the PII inventory, and the DSAR requirements.

## Accept the build

1. When Maria creates the Handoff 2 Jira Task, run one synthetic access request and one synthetic deletion request through Maria's workflow and check each step against your runbook.
2. Record an acceptance test result on the Task: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Write a DSAR fulfillment runbook covering intake, identity verification, locating records across each system in the RoPA, response templates for access and deletion requests, and the response deadline. Walk through it once with a synthetic test subject.
2. Create a consent and opt-out register with columns: Subject ID (pseudonymous), Channel, Consent Given, Date, Opt-Out Date, Source of Record.

## Assess or report

1. Create the Handoff 3 Jira Task for Faris with the synthetic DSAR walkthrough and the consent register.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: RoPA fields, PII inventory, and DSAR runbook requirements, Jason to Maria (Jira Task, created by Jason)
- Handoff 2: PII discovery and DSAR workflow ready for acceptance testing, Maria to Jason (Jira Task, created by Maria)
- Handoff 3: synthetic DSAR walkthrough and consent register, Jason to Faris (Jira Task, created by Jason)

**Skills:** Data mapping · RoPA · DSAR handling · consent management · privacy by design

**Tools:** Excel or Google Sheets · Google Docs or Word · Stripe Dashboard (read-only) · AWS Console (read-only)

**Deliverable:** RoPA and PII inventory workbook, a written DSAR runbook with one synthetic walkthrough, and a consent and opt-out register.

**What it simulates:** A privacy analyst maintaining a processing inventory and handling data subject requests.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
