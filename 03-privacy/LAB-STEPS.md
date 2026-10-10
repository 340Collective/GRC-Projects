# Privacy Operations - Lab Steps

Build 340 Collective's data map, PII inventory, DSAR runbook, and consent register by hand. 340 Collective is the subject organization.

**Lab Steps:**

1. Create a Records of Processing (RoPA) spreadsheet with columns: Processing Activity, Purpose, Data Categories, Data Subjects, Lawful Basis, Source, Storage Location (generic, such as "AWS account, S3"), Recipients, Retention Period, Owner.
2. Fill one row each for the 340collective.com contact form, newsletter sign-ups, Stripe checkout and invoicing, and client file delivery.
3. Build a PII inventory tab listing every personal data field collected (name, email, phone, billing details) with its sensitivity level and where it is stored or shared.
4. Write a DSAR fulfillment runbook covering intake, identity verification, locating records across each system in the RoPA, response templates for access and deletion requests, and the response deadline. Walk through it once with a synthetic test subject.
5. Create a consent and opt-out register with columns: Subject ID (pseudonymous), Channel, Consent Given, Date, Opt-Out Date, Source of Record.

**Skills:** Data mapping · RoPA · DSAR handling · consent management · privacy by design

**Tools:** Excel or Google Sheets · Google Docs or Word · Stripe Dashboard (read-only) · AWS Console (read-only)

**Deliverable:** RoPA and PII inventory workbook, a written DSAR runbook with one synthetic walkthrough, and a consent and opt-out register.

**What it simulates:** A privacy analyst maintaining a processing inventory and handling data subject requests.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
