# 340 Collective Policy Management - Lab Steps (non-engineering)

Author 340 Collective's core security policy set as versioned Markdown, then track attestations and review dates. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-05-Policy-Management/LAB-STEPS.md](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Draft six policies as separate Markdown files: Information Security, Acceptable Use, Access Control, Vendor Management, Incident Response, and Data Retention.
2. Give every policy the same header block: Policy ID, Version, Owner, Approver, Effective Date, Next Review Date, and a change log table.
3. Write each policy around how 340 Collective actually operates (for example, Access Control requires IAM Identity Center with MFA for all AWS access; Data Retention sets how long contact form and invoice records are kept).
4. Set the review cycle for each policy (annual, or after a major change) so the pipeline's reminders match.
5. Bring the requirements to the Day 1 kickoff. Faris accepts them before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the six policy drafts with the header block and the review cycle.

## Test the build

1. When Maria says the build is ready, push one policy change through Maria's pipeline and check the header validation, the published version, and one attestation.
2. Record your test result, or findings, on the project item, then record your validation there.

## Operate it

1. Create an attestation tracker with columns: Team Member, Policy ID, Version, Date Acknowledged, Method. Collect a real acknowledgment from each collaborator.
2. Build a review-cycle schedule listing each policy, its review frequency (annual, or after a major change), the next review date, and the reviewer.

## Assess or report

1. Share the attestation results and the review-cycle schedule with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Policy writing · document control · attestation tracking · governance cadence

**Tools:** Markdown editor · Git for version history · Excel or Google Sheets

**Deliverable:** Six versioned policy documents, an attestation tracker, and a review-cycle schedule.

**What it simulates:** A governance analyst owning the policy lifecycle from drafting to annual review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
