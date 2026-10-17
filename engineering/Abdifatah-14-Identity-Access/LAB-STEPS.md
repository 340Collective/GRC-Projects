# Identity and Access (Okta) - Lab Steps

Make Okta the GRC team's launch point for AWS, GitHub, and Jira, with the Okta Browser Plugin filling each app's sign-in, automate joiners and leavers, and hand the identity record to 08 Access Reviews. 340 Collective is the subject organization. Optional stretch, about 2 weeks, 0 dollars.

**Lab Steps:**

1. Create an Okta Integrator Free Plan org with the business sign-up email (kept in the private roster, never committed). Add each team member by personal email (currently five, six once the IAM engineer joins) and require Okta Verify enrollment at first sign-in.
2. Create Okta groups by function: GRC-ISSM, GRC-ISSE, GRC-ISSO, GRC-IAM, GRC-Auditor, GRC-Stakeholder. Put each person in one group. Group membership decides which Okta apps each person sees.
3. Edit the Global Session Policy: Okta Verify MFA at every sign-in, Maximum Okta global session lifetime of 8 hours, and Keep me signed in not offered.
4. Each member installs the Okta Browser Plugin in their browser and signs it in to the org.
5. Add three SWA apps with "User sets username and password": AWS console (https://570814274897.signin.aws.amazon.com/console), GitHub (https://github.com/login), and Jira (https://340collective.atlassian.net). Assign them by group as the architecture doc lays out; the GRC-ISSM admin identity stays outside Okta.
6. Add bookmark tiles for the GRC-Projects repo, its open pull requests, and the Jira GRC board, assigned to the GRC groups.
7. Test: each member opens the AWS tile, the plugin fills the IAM user name and password, and AWS still prompts for the MFA code. Confirm the IAM group in the console and a CloudTrail ConsoleLogin event with MFA used. Repeat for GitHub (2FA) and Jira (two-step verification). Record any app the plugin cannot fill and use its bookmark tile instead.
8. File the deviation request: no single sign-on, by design. Compensating controls are Okta Verify MFA, each app's own MFA, the 8-hour Okta session, the 14 character IAM password policy, and the quarterly 08 access review.
9. Build the Joiner workflow: when a user is added to a GRC group, invite them as a GitHub collaborator through a GitHub REST API Custom API Action (fine-grained token scoped to GRC-Projects, owned by the ISSM), then open a Jira onboarding work item in GRC. On this personal-account private repo every collaborator gets write, including the Auditor and Stakeholder; record that as a risk (see the architecture doc).
10. Build the Leaver workflow: when a user is removed or deactivated, remove the GitHub collaborator, then open a Jira offboarding work item with a checklist (the ISSM deletes the person's AWS login profile and IAM user through the access model, grc-* role trust policies and resource policies reviewed, Jira access removed).
11. Run a lifecycle test with a test user: join, check the app assignments and GitHub and Jira access, then leave and check removal. Capture screenshots and Okta System Log entries.
12. Export the group list, app assignments, Global Session Policy settings, and workflow definitions into engineering/Abdifatah-14-Identity-Access/ (check that no token, password, or email address is in them) and submit them by pull request for ISSO validation and ISSM approval.
13. Hand the Okta group and app-assignment export to 08 as the identity source for the next access review.
14. Tear down: delete the SWA and bookmark apps and the workflows, revoke the GitHub and Jira tokens, remove the test user, and record teardown evidence. The IAM users and the access model are unchanged.

**Skills:** Identity provider administration · MFA and session policy · password-vault (SWA) app integration · group-based app assignment · joiner and leaver automation · deviation handling

**Tools:** Okta Integrator Free Plan · Okta Browser Plugin · Okta Workflows · AWS IAM · GitHub REST API · Jira

**Deliverable:** An Okta launch point with MFA and an 8-hour session, plugin sign-in to AWS, GitHub, and Jira with each app's MFA intact, two lifecycle workflows, lifecycle test evidence, and a deviation record.

**What it simulates:** An IAM engineer onboarding a small team onto an identity provider without single sign-on.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
