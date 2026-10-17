# Identity and Access (Okta) - Lab Steps (non-engineering)

Own the Okta group model and app assignment rules, accept the Okta build, file the deviation, and hand the identity export to 08. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Abdifatah (IAM / Identity Engineer). Mirror: [engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md](../../engineering/Abdifatah-14-Identity-Access/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Create Okta groups by function: GRC-ISSM, GRC-ISSE, GRC-ISSO, GRC-IAM, GRC-Auditor, GRC-Stakeholder. Put each person in one group. Group membership decides which Okta apps each person sees.
2. Write the app assignment rules: which group sees the AWS, GitHub, and Jira tiles and the bookmark tiles. The GRC-ISSM admin identity stays outside Okta.
3. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Abdifatah starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Abdifatah once Faris accepts it: the Okta group model and the app assignment rules.

## Accept the build

1. When Abdifatah creates the Handoff 2 Jira Task, sign in through the plugin yourself, check that your tiles match your group, and read the lifecycle test evidence.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Before the next 08 review, check the Okta export against the IAM users and the GitHub collaborators.

## Assess or report

1. File the deviation request: no single sign-on, by design. Compensating controls are Okta Verify MFA, each app's own MFA, the 8-hour Okta session, the 14 character IAM password policy, and the quarterly 08 access review.
2. Hand the Okta group and app-assignment export to 08 as the identity source for the next access review.
3. Create the Handoff 3 Jira Task for Faris with the accepted identity export for 08 and the deviation record.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: Okta group model and app assignment rules, Adam to Abdifatah (Jira Task, created by Adam)
- Handoff 2: Okta launch point and lifecycle workflows ready for acceptance, Abdifatah to Adam (Jira Task, created by Abdifatah)
- Handoff 3: accepted identity export for 08 and the deviation record, Adam to Faris (Jira Task, created by Adam)

**Skills:** Identity governance · group model design · deviation handling

**Tools:** Okta admin console (review) · Jira · Excel or Google Sheets

**Deliverable:** An accepted Okta group model and app assignment rules, a filed deviation record, and the identity export handed to 08.

**What it simulates:** An ISSO governing an identity provider rollout.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
