# Identity and Access (Okta) Architecture

## Purpose

Give the GRC team one place to start work. People sign in to an Okta dashboard with their personal email and Okta Verify. From there, the Okta Browser Plugin fills the username and password for the AWS console, GitHub, and Jira through Secure Web Authentication (SWA) apps, and each app's own MFA still applies. There is no single sign-on and no SAML federation into AWS, by design. AWS access stays the IAM users and groups from the [access model](../../shared/access-model/README.md). Two Okta Workflows handle joiners and leavers, and the Okta group and app-assignment export becomes the identity source for [08 Access Reviews](../Abdifatah-08-Access-Reviews/README.md). This is a Phase 1 build: about 2 weeks, 0 dollars. It depends on the access model's IAM users, and its export is ready before the 08 review in Phase 2. Status: target design, not yet deployed.

Builder: the IAM / Identity Engineer, with access through the access model. Code review: the ISSE. Validator: the ISSO, since 14 feeds the 08 access reviews. Approver: the ISSM.

## Scope and frameworks

- SOC 2 CC6.1 (logical access), CC6.2 (provisioning and deprovisioning), and CC6.3 (role-based access).
- ISO 27001:2022 A.5.15 (access control), A.5.16 (identity management), A.5.17 (authentication information), A.5.18 (access rights), and A.8.5 (secure authentication).
- NIST CSF 2.0 PR.AA (identity management, authentication, and access control).
- Control areas: one launch point, MFA at Okta plus each app's own MFA, group-based app assignment, joiner and leaver automation, a recorded deviation for not using single sign-on, and identity evidence for access reviews.

## Decision: no SSO; Okta launch point with plugin sign-in

| | IAM Identity Center | Direct IAM SAML provider | Okta SWA apps with existing IAM users (chosen) |
| --- | --- | --- | --- |
| How it works | Okta connects to Identity Center; permission sets are assigned per account | Okta posts a SAML assertion to an IAM SAML provider, which issues a role session | The Okta Browser Plugin fills the IAM user sign-in form; the user enters the AWS MFA code |
| Prerequisite | An organization instance, which means turning on AWS Organizations in the 340 business account | A SAML provider and one federated role per group, deployed by the ISSM | None; the IAM users, groups, MFA rule, and password policy already exist |
| Fit with the access model | Replaces the access-model groups with permission sets | Adds a second set of roles beside the groups, and federated sessions do not set `aws:MultiFactorAuthPresent`, so `grc-require-mfa` would deny everything on those roles | Reuses the groups, `grc-require-mfa`, and `grc-permissions-boundary` unchanged |
| Fit with 08 | Brings back the Identity Center source 08 is moving away from | 08 would review roles and the provider as well as users | 08 keeps reading IAM users and groups, plus the Okta export |
| Result | Not chosen | Not chosen | Chosen |

Decision: no single sign-on. Granting AWS account access through Identity Center requires an organization instance ([AWS: manage your accounts](https://docs.aws.amazon.com/en_us/singlesignon/latest/userguide/manage-your-accounts.html)), and turning on Organizations is a larger change than this stretch justifies. Direct SAML would add a provider and a parallel set of roles, and would drop the IAM MFA check the access model relies on. GitHub and Jira single sign-on need paid tiers and a verified domain that personal email addresses cannot meet (see "Sign-in per tool" below). The IAM users and groups from the access model already have MFA, the permissions boundary where it applies, and a 14 character password policy, so Okta adds a launch point and lifecycle automation at 0 dollars without changing AWS.

## Automation flow

| Stage | Services | What happens |
| --- | --- | --- |
| Sign-in | Okta Integrator Free Plan, Okta Verify, Global Session Policy | Each person signs in with a personal email and Okta Verify at every sign-in; the Okta session lasts 8 hours; Okta groups by function |
| Plugin sign-in | Okta Browser Plugin, three SWA apps | The plugin fills the username and password for the AWS console, GitHub, and Jira; each app's MFA is still required |
| AWS access | IAM users in `GRC-Engineer`, `GRC-Analyst`, `GRC-Auditor`, `Leadership`; `grc-permissions-boundary`; `grc-require-mfa` | The IAM group sets access; the boundary caps the GRC-Engineer and GRC-Analyst users; MFA is enforced by IAM |
| Tiles | Okta bookmark apps | Links to the GRC-Projects repo, its open pull requests, and the Jira GRC board |
| Lifecycle | Okta Workflows, GitHub REST API, Jira REST API | Joiner and Leaver flows add or remove the repo collaborator and open Jira onboarding or offboarding work items |
| Evidence | Okta export, Okta System Log, CloudTrail, `grc-evidence-*` S3, 08 | Group and app-assignment export, System Log, CloudTrail `ConsoleLogin` events with MFA used, handed to 08 |

## Layer details

### Sign-in (Okta)

- One Okta Integrator Free Plan org. People sign in with their personal email; there is no shared company domain.
- Groups by function: `GRC-ISSM`, `GRC-ISSE`, `GRC-ISSO`, `GRC-IAM`, `GRC-Auditor`, `GRC-Stakeholder`. Each person is in exactly one group. Group membership decides which Okta apps each person sees; it does not grant AWS access.
- Global Session Policy (Admin Console, Security, Global Session Policy): MFA required, "Users will be prompted for MFA" set to every sign-in, and "Maximum Okta global session lifetime" set to 8 hours. The idle time stays at the Okta default. "Keep me signed in" is not offered, because it skips later MFA prompts on remembered devices.
- Okta Verify enrollment is required at first sign-in.
- Separation of duties: the ISSM is the Okta super admin and the only person who changes group membership, since a group change assigns apps and starts the Joiner flow. The IAM Engineer builds with scoped Okta admin roles (application and Workflows admin); confirm the exact Okta role names at build time.

### Plugin sign-in (SWA apps)

- Three custom SWA app integrations, built in the App Integration Wizard with the sign-on method "SWA - Secure Web Authentication":
  - AWS console: `https://<account-id>.signin.aws.amazon.com/console` (the account-specific URL fills in the account, so the person enters only the IAM user name and password).
  - GitHub: `https://github.com/login`.
  - Jira: `https://340collective.atlassian.net`.
- Credential mode: "User sets username and password". Each person enters their own credentials once in Okta, so admins never see or set anyone's password.
- Alternative not used: "Administrator sets username and password". It would put admins in possession of every person's password and break the access model rule that the ISSM shares only temporary passwords out of band, which each person changes at first sign-in.
- The plugin fills only the username and password. It never holds or enters an MFA code. AWS asks for the IAM MFA code, GitHub asks for 2FA, and Atlassian asks for its two-step code.
- Whether the plugin can fill the AWS IAM user form and Atlassian's two-step (email first, then password) form is not verified. The lab test records the result per app; for any app the plugin cannot fill, the person uses a bookmark tile to the same URL and signs in by hand.

| Okta group | Person | AWS console SWA app (IAM user, IAM group) | GitHub SWA app | Jira SWA app | Bookmark tiles |
| --- | --- | --- | --- | --- | --- |
| `GRC-ISSM` | ISSM | Not assigned: the ISSM's hand-made admin identity stays outside Okta as break-glass | Yes | Yes | Yes |
| `GRC-ISSE` | ISSE | Yes (`rasheed`, `GRC-Engineer`, boundary capped) | Yes | Yes | Yes |
| `GRC-ISSO` | ISSO | Yes (`adam`, `GRC-Analyst`, boundary capped) | Yes | Yes | Yes |
| `GRC-IAM` | IAM Engineer | Yes, after the ISSM adds an IAM user in `GRC-Engineer` through an access-model PR | Yes | Yes | Yes |
| `GRC-Auditor` | Internal Auditor | Yes (the Internal Auditor's IAM user, `GRC-Auditor`, read-only, MFA required, no boundary) | Yes | Yes | Yes |
| `GRC-Stakeholder` | Stakeholder | Yes (`david`, `Leadership`, read-only, no boundary) | Yes | Yes | Yes |

One AWS console app, one GitHub app, and one Jira app, each assigned by group, keeps the app count small and maps cleanly to 08's review.

### AWS access (access model, unchanged)

- The IAM users and groups in the [access model](../../shared/access-model/README.md) stay the source of truth for AWS access. Okta does not create, change, or delete IAM users.
- MFA is enforced by `grc-require-mfa`, which denies actions when the session has no MFA. Signing in through the plugin does not change that: the person still enters the AWS MFA code.
- `grc-permissions-boundary` caps the `GRC-Engineer` and `GRC-Analyst` users. `GRC-Auditor` is in the access model too: read-only, MFA required, and no boundary. `Leadership` is the only hand-made read-only group, without the boundary.
- Account password policy: 14 character minimum, upper case, lower case, number, and symbol required, reuse prevention of 24, no expiry.
- Session length: AWS sets the console session length for IAM users (12 hours by default, per [AWS: switch to a role in the console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)). Okta does not control it, and it is not configurable per IAM user. When the 8-hour Okta session ends, the AWS console session keeps running, so people sign out of AWS at the end of the day.

### Tiles (bookmarks)

- Three Okta bookmark apps, assigned to the GRC groups: the GRC-Projects repo, its open pull requests, and the Jira GRC board.
- A bookmark is a link. It opens the page; the SWA app or the person handles sign-in.

### Lifecycle (Okta Workflows)

Two flows only, inside the free plan's limit of 5. Details are under Workflow designs below.

### Evidence

- The ISSO exports Okta group membership, app assignments, and the System Log for the review window and writes them to a `grc-evidence-*` bucket (the analyst can write there). That export becomes 08's identity source when 14 is built.
- CloudTrail records every console sign-in as a `ConsoleLogin` event, including whether MFA was used.
- No automated Okta to S3 push, since that would put AWS credentials inside Okta.

## Sign-in per tool

| Tool | In 14 | Each tool's MFA | What real SSO would need | Why not now |
| --- | --- | --- | --- | --- |
| AWS | SWA plugin sign-in to the person's IAM user | IAM MFA, enforced by `grc-require-mfa` | IAM Identity Center with AWS Organizations, or an IAM SAML provider and federated roles | Organizations is out of scope, and SAML roles would drop the IAM MFA check (see the Decision above) |
| GitHub | SWA plugin sign-in | GitHub 2FA | GitHub Enterprise Cloud on the 340Collective organization ([GitHub: SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)) | Paid per user per month |
| Jira | SWA plugin sign-in | Atlassian two-step verification | Atlassian Guard plus a verified domain ([Atlassian: verify a domain](https://support.atlassian.com/user-management/docs/verify-a-domain-to-manage-accounts/), [Atlassian Guard](https://www.atlassian.com/licensing/atlassian-guard)) | Paid per user, and personal Gmail and Proton addresses cannot be domain verified |
| Google Workspace, Slack | Not in scope | Not applicable | A shared domain and each tool's SSO tier | Future idea in [GOVERNANCE.md](../../GOVERNANCE.md) |

### Deviation request (no single sign-on)

- Required: single sign-on for every tool the team uses.
- Status: not used, by design (owner decision).
- Risk affected: credentials are per app, and grants and removals happen in each tool, not centrally. A leaver could keep access if a step is missed.
- Compensating controls: Okta Verify MFA at every Okta sign-in, each app's own MFA, the 8-hour Okta session, the 14 character IAM password policy, and the quarterly 08 access review, which covers IAM users, GitHub collaborators, and Jira users.
- Revisit: if 340 Collective adopts a shared domain or a paid tier.

## Workflow designs

### Joiner

- Trigger: user added to a GRC group in Okta (the ISSM makes the change).
- Okta assigns the SWA apps and bookmark tiles by group automatically. An AWS IAM user is created only by the ISSM through an access-model PR; the person then saves those credentials in the AWS SWA app.
- Step 1: invite the person as a GitHub collaborator on GRC-Projects through a GitHub REST API Custom API Action: `PUT /repos/{owner}/{repo}/collaborators/{username}`. The GitHub username comes from an Okta profile attribute. GRC-Projects is a public repo owned by the 340Collective organization, so the call sets the role with the API's `permission` field. Engineers, the ISSO, and the Auditor get write (`push`) by design, because partners push their own records to their non-engineering folders ([GOVERNANCE.md](../../GOVERNANCE.md)). The Stakeholder gets read (`pull`). The API defaults to write when `permission` is left out, so a Stakeholder invite without it is recorded as a risk below.
- Step 2: open a Jira onboarding work item in GRC with the person's role and the access granted.
- Token: a fine-grained GitHub token scoped to GRC-Projects only, owned by the ISSM (the repo owner), not the ISSE or the IAM Engineer, because this flow can grant repo access. 90 day expiry, stored only in the Workflows connection. The Jira API token lives only in the Workflows Jira connection. No token is ever committed.
- Human gate: the group change itself is the ISSM's access approval.
- Evidence: Workflows execution history, the GitHub invitation, and the Jira item.

### Leaver

- Trigger: user removed from a GRC group or deactivated in Okta.
- Step 1: remove the GitHub collaborator: `DELETE /repos/{owner}/{repo}/collaborators/{username}`.
- Step 2: open a Jira offboarding work item with a checklist:
  - The ISSM deletes the person's AWS login profile and IAM user through the access model ([offboarding](../../shared/access-model/README.md#access-changes-and-offboarding)). Okta does not manage IAM users without federation, so this step is manual.
  - `grc-*` role trust policies and resource policies reviewed.
  - Jira access removed.
  - Okta user deactivated. Deactivation removes app assignments; whether it also removes the stored SWA credentials needs verification during the lab.
- Human gate: the ISSM closes the offboarding item once every checklist line is confirmed.
- Evidence: Workflows execution history, the collaborator list before and after, IAM showing the user gone, and the closed Jira item.

### Notes and optional extensions

- GRC-Projects is in the 340Collective organization, so the read, triage, and write roles are all available at 0 dollars ([GitHub: repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization)). Write for the ISSO and the Auditor is by design: each partner pushes only to their own folder, and their AWS access stays read-only. Only the Stakeholder's role is a risk to watch.
- Connector availability on the free plan is unverified. If the GitHub or Jira connector is not offered, the Custom API Action (HTTP) card covers both calls.
- Optional extensions, not built: a Mover flow (records a group change in Jira, and re-maps the GitHub role, for example read to write), a quarterly review export flow, and a dormant-account check. Each uses one of the three remaining flow slots.

## Security controls and risks

| Risk | Effect | Mitigation |
| --- | --- | --- |
| Okta stores app passwords (vault-style risk concentrated in Okta) | A compromised Okta account or org exposes the saved AWS, GitHub, and Jira passwords | Okta stores SWA credentials encrypted ([Okta: SWA app integrations](https://help.okta.com/oie/en-us/Content/Topics/Apps/apps-about-swa.htm)); each person sets their own; Okta Verify MFA at every sign-in; the 8-hour session; and each app's MFA, which the plugin does not hold, still blocks a password-only sign-in |
| The plugin cannot fill an app's sign-in form | The person cannot use the plugin for that app | Bookmark tile fallback to the same URL, recorded in the lab test |
| The AWS console session outlives the Okta session | AWS stays signed in after the 8-hour Okta session ends | People sign out of AWS at the end of the day; ending the Okta session does not end the AWS session |
| A leaver keeps AWS access if the IAM user is not removed | Okta deactivation does not touch IAM | The Leaver checklist line for the ISSM, and the quarterly 08 review |
| The Stakeholder gets write on GRC-Projects | The Joiner call leaves out `permission`, so the Stakeholder, who is informed only, can push to the repo. Write for the ISSO and the Auditor is by design and is not this risk | The Joiner flow sets `permission` to `pull` for the Stakeholder group, using the organization's read role. No branch protection is set yet, so the other controls are procedural: nothing merges to `main` without ISSM approval, the quarterly 08 review lists collaborators and their roles and checks merge history, and the Leaver flow removes access |
| GitHub token compromise | Repo collaborator changes | Fine-grained, one repo, ISSM-owned, 90 day expiry, revoked at teardown |
| Free plan org deactivates after 90 days with no sign-ins | The launch point and the flows stop working | A monthly sign-in until the end-of-program teardown |
| 10 active user cap | No room past 10 people | Six people (once the IAM Engineer joins) plus one test user fits |
| Sign-up needs a business email | Personal addresses cannot open the org | The sign-up address comes from the private roster and is never committed |
| ISSM break-glass admin sits outside Okta | Not covered by Okta MFA or flows | Existing known gap in the access model; reviewed in 08 |
| Okta outage | No dashboard or plugin sign-in | People sign in to each app directly with their own credentials and MFA |
| Personal emails as Okta usernames | No shared domain, so no domain-verified SSO for GitHub or Jira | Recorded deviation request with compensating controls |

## Free plan limits

From [Okta org defaults](https://developer.okta.com/docs/reference/org-defaults/): the Okta Integrator Free Plan is for development and testing. It allows at most 10 active users and 5 Workflows, has no paid support, needs a business sign-up email, and deactivates after 90 consecutive days without sign-ins. Availability of SWA apps and the Okta Browser Plugin on this plan is not verified; the org defaults page does not name them. Whether the GitHub and Jira Workflows connectors are available on this plan is also unverified.

## 340 Collective testbed

340 Collective's AWS account holds the IAM users the plugin signs in to. Validation is one plugin sign-in per AWS user with the AWS MFA prompt, a denied write as a read-only user, and a full join and leave of a test user across GitHub and Jira. No email addresses or tokens are published in this repo.

## Cost note

| Item | Monthly cost |
| --- | --- |
| Okta Integrator Free Plan (Okta Verify, Browser Plugin, Workflows) | 0 |
| IAM users and groups (existing) | 0 |
| CloudTrail management events on the existing trail | 0 |
| S3 evidence objects in `grc-evidence-*` | at or near 0, inside the 10 dollar budget |
| GitHub Free | 0 |
| Jira Free | 0 |
| Total | 0 |

GitHub Enterprise Cloud and Atlassian Guard are the paid tiers that real GitHub and Jira SSO would need, and either would break the 10 dollar budget.

## Evidence to capture

- Okta groups and app assignments (screenshots).
- The Global Session Policy settings (MFA at every sign-in, 8-hour session lifetime, Keep me signed in not offered).
- Each member's AWS sign-in through the plugin, with the AWS MFA prompt and the IAM group shown in the console.
- CloudTrail `ConsoleLogin` events for each IAM user, showing MFA used.
- A denied write as a read-only user.
- GitHub and Jira sign-ins through the plugin, with their MFA prompts.
- Workflows execution history for one join and one leave.
- The GitHub collaborator list before and after.
- The Jira onboarding and offboarding work items.
- Okta System Log entries for the lifecycle test.
- The Okta group and app-assignment export in `grc-evidence-*`, handed to 08.
- The deviation request for not using single sign-on.

## Build order

1. Okta org, groups, and the Global Session Policy.
2. Okta Browser Plugin installed by each member.
3. The three SWA apps (AWS console, GitHub, Jira) with user-set credentials, assigned by group.
4. Bookmark tiles and the deviation request.
5. One plugin sign-in test per member for each app.
6. Joiner and Leaver flows.
7. Lifecycle test with a test user, and the evidence export to 08.
8. Group list, app assignments, session policy, and workflow definitions exported into this folder in the Day 7 pull request that finishes the project.

## End-of-program teardown

1. Deactivate and delete the SWA apps, the bookmark apps, and the Joiner and Leaver flows.
2. Revoke the GitHub fine-grained token and the Jira API token.
3. Remove the test user and any test collaborator.
4. Record teardown evidence (deactivated apps and flows, revoked tokens, removed test user).

Nothing in the access model changes at teardown; the IAM users stay. 14 stays in use until the end-of-program teardown, so schedule a monthly sign-in so the free org does not deactivate.

## Sources

- Okta Integrator Free Plan org defaults: https://developer.okta.com/docs/reference/org-defaults/
- Okta Browser Plugin: https://help.okta.com/en-us/content/topics/browser-plugin/browser-plugin-main.htm
- Install the Okta Browser Plugin: https://help.okta.com/en-us/content/topics/end-user/plugin-download_install.htm
- SWA app integration wizard: https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_swa.htm
- SWA app integrations (encrypted credential store): https://help.okta.com/oie/en-us/Content/Topics/Apps/apps-about-swa.htm
- Edit a Global Session Policy: https://help.okta.com/oie/en-us/content/Topics/identity-engine/policies/edit-global-session-policy.htm
- MFA prompt options in a Global Session Policy rule: https://help.okta.com/OIE/en-us/content/topics/security/behavior-detection/add-behavior-signon-rule.htm
- Keep me signed in: https://help.okta.com/oie/en-us/content/topics/security/stay-signed-in.htm
- AWS IAM user console session length: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html
- AWS IAM Identity Center account access (why not chosen): https://docs.aws.amazon.com/en_us/singlesignon/latest/userguide/manage-your-accounts.html
- GitHub SAML SSO (why not chosen): https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on
- GitHub repository roles for an organization: https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization
- Atlassian verify a domain and Atlassian Guard (why not chosen): https://support.atlassian.com/user-management/docs/verify-a-domain-to-manage-accounts/, https://www.atlassian.com/licensing/atlassian-guard

## Related projects

- [Access model](../../shared/access-model/README.md)
- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md)
- [08 Access Reviews](../Abdifatah-08-Access-Reviews/README.md)
- [GOVERNANCE.md](../../GOVERNANCE.md)
