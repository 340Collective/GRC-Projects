# Identity and Access (Okta) - Lab Steps (non-engineering)

Own the Okta group model and app assignment rules, accept the Okta build, file the deviation, and hand the identity export to 08. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Abdifatah (IAM / Identity Engineer). Mirror: [engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md](../../engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create Okta groups by function: GRC-ISSM, GRC-ISSE, GRC-ISSO, GRC-IAM, GRC-Auditor, GRC-Stakeholder. Put each person in one group. Group membership decides which Okta apps each person sees.
2. Write the app assignment rules: which group sees the AWS, GitHub, and Jira tiles and the bookmark tiles. The GRC-ISSM admin identity stays outside Okta.
3. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Abdifatah starts.

## Share inputs

1. Share these with Abdifatah at kickoff once Faris accepts them: the Okta group model and the app assignment rules.

## Test the build

1. When Abdifatah says the build is ready, sign in through the plugin yourself, check that your tiles match your group, and read the lifecycle test evidence.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. After your Day 7 sign-off, record your validation on the Final report item.

## Operate it

1. Before the next 08 review, check the Okta export against the IAM users and the GitHub collaborators.

## Assess or report

1. File the deviation request: no single sign-on, by design. Compensating controls are Okta Verify MFA, each app's own MFA, the 8-hour Okta session, the 14 character IAM password policy, and the quarterly 08 access review.
2. Hand the Okta group and app-assignment export to 08 as the identity source for the next access review.
3. Commit the accepted identity export for 08 and the deviation record to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Abdifatah agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Abdifatah as needed, or comment on the project item.
- Day 7 sign-off: Abdifatah commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Identity governance · group model design · deviation handling

**Tools:** Okta admin console (review) · Jira · Excel or Google Sheets

**Deliverable:** An accepted Okta group model and app assignment rules, a filed deviation record, and the identity export handed to 08.

**What it simulates:** An ISSO governing an identity provider rollout.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
