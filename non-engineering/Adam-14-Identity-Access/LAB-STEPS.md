# Identity and Access (Okta) - Lab Steps (non-engineering)

Own the Okta group model and app assignment rules, accept the Okta build, file the deviation, and hand the identity export to 08. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Abdifatah (IAM / Identity Engineer). Mirror: [engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md](../../engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create Okta groups by function: GRC-ISSM, GRC-ISSE, GRC-ISSO, GRC-IAM, GRC-Auditor, GRC-Stakeholder. Put each person in one group. Group membership decides which Okta apps each person sees.
2. Write the app assignment rules: which group sees the AWS, GitHub, and Jira tiles and the bookmark tiles. The GRC-ISSM admin identity stays outside Okta.
3. Bring the requirements to the Day 1 kickoff. Faris accepts them before Abdifatah starts.

## Share inputs

1. Share these with Abdifatah at kickoff once Faris accepts them: the Okta group model and the app assignment rules.

## Test the build

1. When Abdifatah says the build is ready, sign in through the plugin yourself, check that your tiles match your group, and read the lifecycle test evidence.
2. Record your test result, or findings, on the project item, then record your validation there.

## Operate it

1. Before the next 08 review, check the Okta export against the IAM users and the GitHub collaborators.

## Assess or report

1. File the deviation request: no single sign-on, by design. Compensating controls are Okta Verify MFA, each app's own MFA, the 8-hour Okta session, the 14 character IAM password policy, and the quarterly 08 access review.
2. Hand the Okta group and app-assignment export to 08 as the identity source for the next access review.
3. Share the accepted identity export for 08 and the deviation record with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Abdifatah agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Abdifatah as needed, or comment on the project item.
- Day 7 sign-off: Abdifatah fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Identity governance · group model design · deviation handling

**Tools:** Okta admin console (review) · Jira · Excel or Google Sheets

**Deliverable:** An accepted Okta group model and app assignment rules, a filed deviation record, and the identity export handed to 08.

**What it simulates:** An ISSO governing an identity provider rollout.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
