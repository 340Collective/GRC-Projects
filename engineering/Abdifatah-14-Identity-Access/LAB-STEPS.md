# Identity and Access (Okta) - Lab Steps (engineering)

Make Okta the GRC team's launch point for AWS, GitHub, and Jira, with the Okta Browser Plugin filling each app's sign-in, automate joiners and leavers, and hand the identity record to 08 Access Reviews. 340 Collective is the subject organization. Phase 1 build, about 2 weeks, 0 dollars.

Track: engineering. You: Abdifatah (IAM / Identity Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-14-Identity-Access/LAB-STEPS.md](../../non-engineering/Adam-14-Identity-Access/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read Adam's Handoff 1 Jira Task: the Okta group model and the app assignment rules.
2. Read the risks table in the [architecture doc](Identity-Access-Architecture.md) and plan a mitigation for each before you build.
3. No CloudFormation stack: 14 is Okta configuration. The IAM users and the access model stay as they are.
4. Cost: 0 dollars on the free plans. GitHub Enterprise Cloud and Atlassian Guard, which real SSO would need, are out of scope.

## Deploy

1. Create an Okta Integrator Free Plan org with the business sign-up email (kept in the private roster, never committed). Add each team member by personal email (currently five, six once the IAM engineer joins) and require Okta Verify enrollment at first sign-in.
2. Create the Okta groups exactly as Adam's group model lists them, and put each person in one group.
3. Edit the Global Session Policy: Okta Verify MFA at every sign-in, Maximum Okta global session lifetime of 8 hours, and Keep me signed in not offered.
4. Each member installs the Okta Browser Plugin in their browser and signs it in to the org.
5. Add three SWA apps with "User sets username and password": AWS console (https://570814274897.signin.aws.amazon.com/console), GitHub (https://github.com/login), and Jira (https://340collective.atlassian.net). Assign them by group as the architecture doc lays out; the GRC-ISSM admin identity stays outside Okta.
6. Add bookmark tiles for the GRC-Projects repo, its open pull requests, and the Jira GRC board, assigned to the GRC groups.
7. Build the Joiner workflow: when a user is added to a GRC group, invite them as a GitHub collaborator through a GitHub REST API Custom API Action (fine-grained token scoped to GRC-Projects, owned by the ISSM), then open a Jira onboarding work item in GRC. On this personal-account private repo every collaborator gets write, including the Auditor and Stakeholder; record that as a risk (see the architecture doc).
8. Build the Leaver workflow: when a user is removed or deactivated, remove the GitHub collaborator, then open a Jira offboarding work item with a checklist (the ISSM deletes the person's AWS login profile and IAM user through the access model, grc-* role trust policies and resource policies reviewed, Jira access removed).

## Test

1. Test: each member opens the AWS tile, the plugin fills the IAM user name and password, and AWS still prompts for the MFA code. Confirm the IAM group in the console and a CloudTrail ConsoleLogin event with MFA used. Repeat for GitHub (2FA) and Jira (two-step verification). Record any app the plugin cannot fill and use its bookmark tile instead.
2. Run a lifecycle test with a test user: join, check the app assignments and GitHub and Jira access, then leave and check removal. Capture screenshots and Okta System Log entries.

## Hand off

1. Export the group list, app assignments, Global Session Policy settings, and workflow definitions into engineering/Abdifatah-14-Identity-Access/ (check that no token, password, or email address is in them) and submit them by pull request for ISSO validation and ISSM approval.
2. Rasheed or Maria reviews the exported definitions in the pull request. Create the Handoff 2 Jira Task for Adam; he records his acceptance and validation on the Task, and Faris gives final approval. The pull request merges only after the Task shows acceptance.

## Tear down

1. Tear down: delete the SWA and bookmark apps and the workflows, revoke the GitHub and Jira tokens, remove the test user, and record teardown evidence. The IAM users and the access model are unchanged.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: Okta group model and app assignment rules, Adam to Abdifatah (Jira Task, created by Adam)
- Handoff 2: Okta launch point and lifecycle workflows ready for acceptance, Abdifatah to Adam (Jira Task, created by Abdifatah)
- Handoff 3: accepted identity export for 08 and the deviation record, Adam to Faris (Jira Task, created by Adam)

**Skills:** Identity provider administration · MFA and session policy · password-vault (SWA) app integration · group-based app assignment · joiner and leaver automation · deviation handling

**Tools:** Okta Integrator Free Plan · Okta Browser Plugin · Okta Workflows · AWS IAM · GitHub REST API · Jira

**Deliverable:** An Okta launch point with MFA and an 8-hour session, plugin sign-in to AWS, GitHub, and Jira with each app's MFA intact, two lifecycle workflows, lifecycle test evidence, and a deviation record.

**What it simulates:** An IAM engineer onboarding a small team onto an identity provider without single sign-on.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
