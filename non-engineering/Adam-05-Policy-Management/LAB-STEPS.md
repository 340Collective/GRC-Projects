# 340 Collective Policy Management - Lab Steps (non-engineering)

Author 340 Collective's core security policy set as versioned Markdown, then track attestations and review dates. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-05-Policy-Management/LAB-STEPS.md](../../engineering/Maria-05-Policy-Management/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Draft six policies as separate Markdown files: Information Security, Acceptable Use, Access Control, Vendor Management, Incident Response, and Data Retention.
2. Give every policy the same header block: Policy ID, Version, Owner, Approver, Effective Date, Next Review Date, and a change log table.
3. Write each policy around how 340 Collective actually operates (for example, Access Control requires IAM Identity Center with MFA for all AWS access; Data Retention sets how long contact form and invoice records are kept).
4. Set the review cycle for each policy (annual, or after a major change) so the pipeline's reminders match.
5. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the six policy drafts with the header block and the review cycle.

## Test the build

1. When Maria says the build is ready, push one policy change through Maria's pipeline and check the header validation, the published version, and one attestation.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. Then record your validation on the Final report item.

## Operate it

1. Create an attestation tracker with columns: Team Member, Policy ID, Version, Date Acknowledged, Method. Collect a real acknowledgment from each collaborator.
2. Build a review-cycle schedule listing each policy, its review frequency (annual, or after a major change), the next review date, and the reviewer.

## Assess or report

1. Commit the attestation results and the review-cycle schedule to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Policy writing · document control · attestation tracking · governance cadence

**Tools:** Markdown editor · Git for version history · Excel or Google Sheets

**Deliverable:** Six versioned policy documents, an attestation tracker, and a review-cycle schedule.

**What it simulates:** A governance analyst owning the policy lifecycle from drafting to annual review.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
