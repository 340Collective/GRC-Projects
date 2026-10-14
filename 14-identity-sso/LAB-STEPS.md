# Identity and SSO - Lab Steps

Put Okta in front of 340 Collective's AWS account for the GRC team, automate joiners and leavers, and hand the identity record to 08 Access Reviews. 340 Collective is the subject organization. Optional stretch, about 2 weeks, 0 dollars.

**Lab Steps:**

1. Create an Okta Integrator Free Plan org with the business sign-up email. Add the five members by personal email and require Okta Verify enrollment at first sign-in.
2. Create Okta groups by function: GRC-ISSM, GRC-ISSE, GRC-ISSO, GRC-Auditor, GRC-Stakeholder. Assign each person to one group.
3. Set an Okta authentication policy: MFA on every sign-in, session lifetime of 8 to 12 hours.
4. In CloudFormation, add Okta as an IAM SAML identity provider using the Okta AWS Account Federation app metadata. Open the grc-identity-sso template as a pull request; the ISSM deploys it after approval.
5. Create one role per group (grc-sso-engineer, grc-sso-analyst, grc-sso-auditor, grc-sso-stakeholder) trusting the SAML provider with a SAML:aud condition, reusing the access-model policies and permissions boundary. MFA is enforced in Okta.
6. Map each Okta group to its role in the Okta AWS app, and test that each member signs in from the tile into the right role.
7. Add bookmark tiles for the GRC-Projects repo, open pull requests, and the Jira GRC board, assigned to the GRC groups.
8. File a deviation request: GitHub and Jira are links, not SSO. Compensating controls are Okta MFA and the quarterly 08 access review.
9. Build the Joiner workflow: when a user is added to a GRC group, invite them as a GitHub collaborator through a GitHub REST API Custom API Action (fine-grained token scoped to GRC-Projects, owned by the ISSM), then open a Jira onboarding work item in GRC. On this personal-account private repo every collaborator gets write, including the Auditor and Stakeholder; record that as a risk (see the architecture doc).
10. Build the Leaver workflow: when a user is removed or deactivated, remove the GitHub collaborator, then open a Jira offboarding work item with a checklist (AWS session and role access gone, grc-* role trust policies and resource policies reviewed, Jira access removed).
11. Run a lifecycle test with a test user: join, verify access in AWS, GitHub, and Jira, then leave and verify removal. Capture screenshots and Okta System Log entries.
12. Export the workflow definitions, the SAML provider, and the role definitions into 14-identity-sso/ and submit them by pull request for ISSM validation and approval.
13. Hand the Okta group membership export to 08 as the identity source for the next access review.
14. Tear down: delete the SAML provider and roles stack, deactivate the workflows, revoke the GitHub and Jira tokens, and record teardown evidence.

**Skills:** Identity federation (SAML) · role mapping · MFA policy · joiner and leaver automation · deviation handling

**Tools:** Okta Integrator Free Plan · Okta Workflows · AWS IAM · CloudFormation · GitHub REST API · Jira

**Deliverable:** Working Okta to AWS federated sign-in, two lifecycle workflows, lifecycle test evidence, and a deviation record.

**What it simulates:** An IAM engineer onboarding a small team onto an identity provider.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
