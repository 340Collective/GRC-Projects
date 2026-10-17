# 340 Collective Policy Management - Lab Steps (non-engineering)

Author 340 Collective's core security policy set as versioned Markdown, then track attestations and review dates. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-05-Policy-Management/LAB-STEPS.md](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Draft six policies as separate Markdown files: Information Security, Acceptable Use, Access Control, Vendor Management, Incident Response, and Data Retention.
2. Give every policy the same header block: Policy ID, Version, Owner, Approver, Effective Date, Next Review Date, and a change log table.
3. Write each policy around how 340 Collective actually operates (for example, Access Control requires IAM Identity Center with MFA for all AWS access; Data Retention sets how long contact form and invoice records are kept).
4. Set the review cycle for each policy (annual, or after a major change) so the pipeline's reminders match.
5. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Maria starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Maria once Faris accepts it: the six policy drafts with the header block and the review cycle.

## Accept the build

1. When Maria creates the Handoff 2 Jira Task, push one policy change through Maria's pipeline and check the header validation, the published version, and one attestation.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Create an attestation tracker with columns: Team Member, Policy ID, Version, Date Acknowledged, Method. Collect a real acknowledgment from each collaborator.
2. Build a review-cycle schedule listing each policy, its review frequency (annual, or after a major change), the next review date, and the reviewer.

## Assess or report

1. Create the Handoff 3 Jira Task for Faris with the attestation results and the review-cycle schedule.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: six policy drafts with header block and review cycle, Adam to Maria (Jira Task, created by Adam)
- Handoff 2: policy-as-code pipeline and attestation tracking ready for acceptance, Maria to Adam (Jira Task, created by Maria)
- Handoff 3: attestation results and review-cycle schedule, Adam to Faris (Jira Task, created by Adam)

**Skills:** Policy writing · document control · attestation tracking · governance cadence

**Tools:** Markdown editor · Git for version history · Excel or Google Sheets

**Deliverable:** Six versioned policy documents, an attestation tracker, and a review-cycle schedule.

**What it simulates:** A governance analyst owning the policy lifecycle from drafting to annual review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
