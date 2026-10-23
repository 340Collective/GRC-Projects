# Identity and Access (Okta) - Lab Steps (engineering)

Make Okta the GRC team's launch point for AWS, GitHub, and Jira, with the Okta Browser Plugin filling each app's sign-in, automate joiners and leavers, and hand the identity record to 08 Access Reviews. 340 Collective is the subject organization. Phase 1 build, about 2 weeks, 0 dollars.

Track: engineering. You: Abdifatah (IAM / Identity Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-14-Identity-Access/LAB-STEPS.md](../../non-engineering/Adam-14-Identity-Access/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

You build it yourself. No scripts, templates, or ready-made commands are provided. These steps say what to build and how it is checked, not what to type. Onboarding other people (AWS users, console logins, Identity Center seats) is the ISSM's job, not a step in this lab.

## Design

1. Agree with Adam at the Day 1 kickoff on the Okta group model and the app assignment rules. Adam writes them in REQUIREMENTS.md in his own folder, and Faris accepts it.
2. Read the risks table in the [architecture doc](Identity-Access-Architecture.md) and plan a mitigation for each before you build.
3. No CloudFormation stack: 14 is Okta configuration. The IAM users and the access model stay as they are.
4. Cost: 0 dollars on the free plans. GitHub Enterprise Cloud and Atlassian Guard, which real SSO would need, are out of scope.

## Deploy

1. Create an Okta Integrator Free Plan org with the business sign-up email (kept in the private roster, never committed). Add each team member by personal email (currently five, six once the IAM engineer joins) and require Okta Verify enrollment at first sign-in.
2. Create the Okta groups exactly as Adam's group model lists them, and put each person in one group.
3. Edit the Global Session Policy: Okta Verify MFA at every sign-in, Maximum Okta global session lifetime of 8 hours, and Keep me signed in not offered.
4. Each member installs the Okta Browser Plugin in their browser and signs it in to the org.
5. Add three SWA apps with "User sets username and password": AWS console (https://<account-id>.signin.aws.amazon.com/console), GitHub (https://github.com/login), and Jira (https://340collective.atlassian.net). Assign them by group as the architecture doc lays out; the GRC-ISSM admin identity stays outside Okta.
6. Add bookmark tiles for the GRC-Projects repo, its open pull requests, and the Jira GRC board, assigned to the GRC groups.
7. Build the Joiner workflow: when a user is added to a GRC group, invite them as a GitHub collaborator through a GitHub REST API Custom API Action (fine-grained token scoped to GRC-Projects, owned by the ISSM), then open a Jira onboarding work item in GRC. Set the role with the API's `permission` field: write (`push`) for engineers, the ISSO, and the Auditor, by design, and read (`pull`) for the Stakeholder. A Stakeholder with write is recorded as a risk (see the architecture doc).
8. Build the Leaver workflow: when a user is removed or deactivated, remove the GitHub collaborator, then open a Jira offboarding work item with a checklist (the ISSM deletes the person's AWS login profile and IAM user through the access model, grc-* role trust policies and resource policies reviewed, Jira access removed).

## Test

1. Test: each member opens the AWS tile, the plugin fills the IAM user name and password, and AWS still prompts for the MFA code. Confirm the IAM group in the console and a CloudTrail ConsoleLogin event with MFA used. Repeat for GitHub (2FA) and Jira (two-step verification). Record any app the plugin cannot fill and use its bookmark tile instead.
2. Run a lifecycle test with a test user: join, check the app assignments and GitHub and Jira access, then leave and check removal. Capture screenshots and Okta System Log entries.

## Partner test

1. Export the group list, app assignments, Global Session Policy settings, and workflow definitions into engineering/Abdifatah-14-Identity-Access/ (check that no token, password, or email address is in them) and include them in the Day 7 pull request that finishes the project.
2. Rasheed or Maria reviews the exported definitions in the pull request. Ask Adam to test it. Adam commits his test results to his own folder, signs off, and records his validation on the Final report item. Faris gives final approval. The pull request merges only after Adam signs off on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the launch point stays in use in the shared system. Test cleanup is separate: remove the test user and any test collaborator after each test. In the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown): delete the SWA and bookmark apps and the workflows, revoke the GitHub and Jira tokens, and record teardown evidence. The IAM users and the access model are unchanged.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: Adam writes REQUIREMENTS.md in his own folder, and Faris accepts it. You and Adam agree on scope.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Adam commits his results to his own folder, compares them with your report, and signs off on the Final report item ("Accepted by: <first name>", or findings). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Identity provider administration · MFA and session policy · password-vault (SWA) app integration · group-based app assignment · joiner and leaver automation · deviation handling

**Tools:** Okta Integrator Free Plan · Okta Browser Plugin · Okta Workflows · AWS IAM · GitHub REST API · Jira

**Deliverable:** An Okta launch point with MFA and an 8-hour session, plugin sign-in to AWS, GitHub, and Jira with each app's MFA intact, two lifecycle workflows, lifecycle test evidence, and a deviation record.

**What it simulates:** An IAM engineer onboarding a small team onto an identity provider without single sign-on.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
