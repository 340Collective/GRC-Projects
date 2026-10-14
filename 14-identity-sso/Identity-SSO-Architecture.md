# Identity and SSO Architecture

## Purpose

Put one login in front of 340 Collective's AWS account for the GRC team. People sign in to Okta with their personal email and Okta Verify, and Okta federates them into one bounded GRC role through an IAM SAML provider. MFA is enforced in one place, joiners and leavers are handled by two Okta Workflows, and the Okta group export becomes the identity source for [08 Access Reviews](../08-access-reviews/README.md). This is an optional stretch: about 2 weeks, 0 dollars, built after 01, 11, 06, and 07 are moving and before the next 08 review. Skip it if nobody wants it. Status: target design, not yet deployed.

## Scope and frameworks

- SOC 2 CC6.1 (logical access), CC6.2 (provisioning and deprovisioning), and CC6.3 (role-based access).
- ISO 27001:2022 A.5.15 (access control), A.5.16 (identity management), A.5.17 (authentication information), A.5.18 (access rights), and A.8.5 (secure authentication).
- NIST CSF 2.0 PR.AA (identity management, authentication, and access control).
- Control areas: one identity provider, central MFA, role mapping by group, joiner and leaver automation, a recorded deviation for tools that cannot be federated, and identity evidence for access reviews.

## Decision: IAM Identity Center or direct IAM SAML

| | IAM Identity Center | Direct IAM SAML provider (chosen) |
| --- | --- | --- |
| How it works | Okta connects to Identity Center; permission sets are assigned per account | Okta's AWS Account Federation app posts SAML to an IAM SAML provider; STS `AssumeRoleWithSAML` issues a role session |
| Prerequisite | AWS account access needs an organization instance, which means turning on AWS Organizations in the 340 business account | None beyond IAM in the one account |
| Fit with the access model | Replaces the access-model groups with permission sets | Reuses the access-model policies and `grc-permissions-boundary` on four `grc-sso-*` roles |
| Fit with 08 | Brings back the Identity Center assumption 08 is moving away from | 08 keeps reading IAM, plus the Okta group export |
| When it wins | Several AWS accounts in one organization | One account, five people |

Decision: direct IAM SAML. Granting AWS account access through Identity Center requires an organization instance ([AWS: manage your accounts](https://docs.aws.amazon.com/en_us/singlesignon/latest/userguide/manage-your-accounts.html)), and turning on Organizations in the 340 business account is a larger change than this stretch justifies. Identity Center stays the considered alternative if 340 Collective ever runs more than one account.

## Automation flow

| Stage | Services | What happens |
| --- | --- | --- |
| Sign-in | Okta Integrator Free Plan, Okta Verify | Each person signs in with a personal email and Okta Verify on every sign-in; Okta groups by function |
| Federation | IAM SAML provider, AWS STS | Okta posts a SAML assertion; STS issues a 1 hour role session |
| Roles | `grc-sso-engineer`, `grc-sso-analyst`, `grc-sso-auditor`, `grc-sso-stakeholder`, `grc-permissions-boundary` | Each group lands in one bounded role |
| Tiles | Okta bookmark apps | Links to the GRC-Projects repo, open pull requests, and the Jira GRC board; link, not SSO |
| Lifecycle | Okta Workflows, GitHub REST API, Jira REST API | Joiner and Leaver flows add or remove the repo collaborator and open Jira onboarding or offboarding work items |
| Evidence | Okta export, CloudTrail, `grc-evidence-*` S3, 08 | Group membership and System Log export, `AssumeRoleWithSAML` events, handed to 08 |

## Layer details

### Sign-in (Okta)

- One Okta Integrator Free Plan org. People sign in with their personal email; there is no shared company domain.
- Groups by function: `GRC-ISSM`, `GRC-ISSE`, `GRC-ISSO`, `GRC-Auditor`, `GRC-Stakeholder`. Each person is in exactly one group.
- Authentication policy: Okta Verify on every sign-in, session lifetime of 8 to 12 hours. Okta Verify enrollment is required at first sign-in.
- Separation of duties: the ISSM is the Okta super admin and the only person who changes group membership, since a group change is an access grant. The ISSO builds with scoped Okta admin roles (application and Workflows admin); confirm the exact Okta role names at build time.

### Federation (IAM SAML provider and STS)

- The Okta AWS Account Federation app from the Okta Integration Network supplies the SAML metadata.
- The SAML provider and the four roles are one CloudFormation stack, `grc-identity-sso`. The ISSO authors it in a pull request; the ISSM deploys it after approval. The engineer policy cannot create it: `DenyIdentityAdmin` in the [access model](../access-model/README.md) denies the engineer `iam:Create*Provider`.
- Each role trust policy allows only `sts:AssumeRoleWithSAML` from the SAML provider, with a `SAML:aud` condition set to the AWS sign-in SAML endpoint. Maximum session is 1 hour.

### Roles (capped by the permissions boundary)

| Okta group | AWS role | Policies | Notes |
| --- | --- | --- | --- |
| `GRC-ISSE` | `grc-sso-engineer` | The `GRC-Engineer` policies from the access model, minus `grc-require-mfa` | Builds `grc-*` stacks only |
| `GRC-ISSO` | `grc-sso-analyst` | The `GRC-Analyst` policy, minus `grc-require-mfa` | Reads security services, writes evidence |
| `GRC-Auditor` | `grc-sso-auditor` | `SecurityAudit` plus `job-function/ViewOnlyAccess` | Read-only assessment |
| `GRC-Stakeholder` | `grc-sso-stakeholder` | `SecurityAudit` plus `job-function/ViewOnlyAccess` | Read-only; David stays read-only |
| `GRC-ISSM` | `grc-sso-auditor` | Same read-only view | Deploys with the existing hand-made admin identity, kept outside Okta as break-glass |

- Every role carries `grc-permissions-boundary`, so no role can do more than the boundary allows.
- MFA is enforced in Okta, not in IAM. SAML federated sessions do not set `aws:MultiFactorAuthPresent`, so the access model's `grc-require-mfa` (which denies when that key is false or absent) would deny everything on a SAML role. It is left off the `grc-sso-*` roles on purpose.
- The auditor and stakeholder roles use the read baseline the access model recommends instead of `ReadOnlyAccess`, so they cannot read S3 object data or SSM parameter values.

### Tiles (GitHub and Jira)

- Three Okta bookmark apps, assigned to the GRC groups: the GRC-Projects repo, its open pull requests, and the Jira GRC board.
- A bookmark is a link. Each tool keeps its own login and MFA.
- No SWA (password-fill) apps. SWA cannot complete GitHub two-factor sign-in, and Okta would hold everyone's GitHub password.

### Lifecycle (Okta Workflows)

Two flows only, inside the free plan's limit of 5. Details are under Workflow designs below.

### Evidence

- The ISSO exports Okta group membership and the System Log for the review window and writes them to a `grc-evidence-*` bucket (the analyst can write there). That export becomes 08's identity source when 14 is built.
- CloudTrail records every `AssumeRoleWithSAML` call, with the Okta username in the session name.
- No automated Okta to S3 push, since that would put AWS credentials inside Okta.

## Tile or SSO, per tool

| Tool | In 14 | What real SSO needs | Why not now |
| --- | --- | --- | --- |
| AWS | SSO through SAML into `grc-sso-*` roles | An IAM SAML provider and roles | Free; this is the part 14 builds |
| GitHub | Bookmark tile (link, not SSO) | GitHub Enterprise Cloud, with the repo moved into an organization ([GitHub: SAML SSO](https://docs.github.com/en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on)) | Paid per user per month (about 21 USD), and the repo would have to move out of the personal account |
| Jira | Bookmark tile (link, not SSO) | Atlassian Guard plus a verified domain ([Atlassian: verify a domain](https://support.atlassian.com/user-management/docs/verify-a-domain-to-manage-accounts/), [Atlassian Guard](https://www.atlassian.com/licensing/atlassian-guard)) | Paid per user, and personal Gmail and Proton addresses cannot be domain verified |
| Google Workspace, Slack | Not in scope | A shared domain and each tool's SSO tier | Future idea in [GOVERNANCE.md](../GOVERNANCE.md) |

### Deviation request (GitHub and Jira SSO)

- Required: single sign-on for every tool the team uses.
- Why it cannot be done now: GitHub SAML SSO needs GitHub Enterprise Cloud and Jira SSO needs Atlassian Guard on a verified domain. Both are paid per user and need a shared domain that personal email addresses cannot meet. Either would break the 10 dollar ceiling.
- Risk affected: GitHub and Jira access is granted and removed in each tool, not centrally; a leaver could keep access if the Leaver flow fails.
- Compensating controls: Okta MFA in front of AWS, each tool's own MFA, the Leaver flow's offboarding checklist, and the quarterly 08 access review, which covers GitHub collaborators and Jira users.
- Revisit: if 340 Collective adopts a shared domain or a paid tier.

## Workflow designs

### Joiner

- Trigger: user added to a GRC group in Okta (the ISSM makes the change).
- Step 1: invite the person as a GitHub collaborator on GRC-Projects through a GitHub REST API Custom API Action: `PUT /repos/{owner}/{repo}/collaborators/{username}`, at the mapped permission (ISSE and ISSO write, Auditor and Stakeholder read). The GitHub username comes from an Okta profile attribute.
- Step 2: open a Jira onboarding work item in GRC with the person's role and the access granted.
- Token: a fine-grained GitHub token scoped to GRC-Projects only, owned by the ISSM (the repo owner), not the ISSE, because this flow can grant repo access. 90 day expiry, stored only in the Workflows connection. The Jira API token lives only in the Workflows Jira connection. No token is ever committed.
- Human gate: the group change itself is the ISSM's access approval.
- Evidence: Workflows execution history, the GitHub invitation, and the Jira item.

### Leaver

- Trigger: user removed from a GRC group or deactivated in Okta.
- Step 1: remove the GitHub collaborator: `DELETE /repos/{owner}/{repo}/collaborators/{username}`.
- Step 2: open a Jira offboarding work item with a checklist: AWS session and role access gone, `grc-*` role trust policies and resource policies reviewed, Jira access removed.
- Human gate: the ISSM closes the offboarding item once every checklist line is confirmed.
- Evidence: Workflows execution history, the collaborator list before and after, and the closed Jira item.

### Notes and optional extensions

- On this user-owned private repo, a collaborator cannot be lowered from write to read through the API without removing and re-inviting them. Confirm at build time how the API treats the permission field on a personal repo.
- Connector availability on the free plan is unverified. If the GitHub or Jira connector is not offered, the Custom API Action (HTTP) card covers both calls.
- Optional extensions, not built: a Mover flow (group change re-maps the GitHub permission), a quarterly review export flow, and a dormant-account check. Each uses one of the three remaining flow slots.

## Security controls and risks

| Risk | Effect | Mitigation |
| --- | --- | --- |
| The engineer can edit any `grc-*` role, including `grc-sso-*` (`IamManageGrcRoles`) | The ISSE could widen a federated role's trust or policies | Follow-up access-change PR to deny engineer writes on `grc-sso-*`; the ISSM owns the stack |
| GitHub token compromise | Repo collaborator changes | Fine-grained, one repo, ISSM-owned, 90 day expiry, revoked at teardown |
| Free plan org deactivates after 90 days with no sign-ins | Federation stops working | A monthly sign-in if kept, or tear down |
| 10 active user cap | No room past 10 people | Five people plus one test user fits |
| Sign-up needs a business email | Personal addresses cannot open the org | The sign-up address comes from the private roster and is never committed |
| ISSM break-glass admin sits outside Okta | Not covered by Okta MFA or flows | Existing known gap in the access model; reviewed in 08 |
| Okta outage | No federated sign-in | IAM console users stay as fallback during a 2 week overlap |
| Personal emails as Okta usernames | No shared domain, so no domain-verified SSO for GitHub or Jira | Recorded deviation request with compensating controls |
| SWA password-fill apps | Okta holds GitHub passwords; GitHub 2FA breaks | Not used; bookmark tiles only |

## Free plan limits

From [Okta org defaults](https://developer.okta.com/docs/reference/org-defaults/): the Okta Integrator Free Plan is for development and testing. It allows at most 10 active users and 5 Workflows, has no paid support, needs a business sign-up email, and deactivates after 90 consecutive days without sign-ins. Whether the GitHub and Jira Workflows connectors are available on this plan is unverified.

## 340 Collective testbed

340 Collective's AWS account is the federation target. Validation is one sign-in per role from the Okta tile, a denied write as the auditor role, and a full join and leave of a test user across AWS, GitHub, and Jira. No account identifiers, email addresses, or tokens are published in this repo.

## Cost note

| Item | Monthly cost |
| --- | --- |
| Okta Integrator Free Plan (Okta Verify, Workflows) | 0 |
| IAM SAML provider and roles | 0 |
| AWS STS | 0 |
| CloudTrail management events on the existing trail | 0 |
| S3 evidence objects in `grc-evidence-*` | at or near 0, inside the 10 dollar budget |
| GitHub Free | 0 |
| Jira Free | 0 |
| Total | 0 |

GitHub Enterprise Cloud and Atlassian Guard are the paid tiers that real GitHub and Jira SSO would need, and either would break the 10 dollar budget.

## Evidence to capture

- Okta groups and app assignments (screenshots).
- The authentication policy (Okta Verify on every sign-in, session lifetime).
- One sign-in per role from the tile, and the role shown in the AWS console.
- CloudTrail `AssumeRoleWithSAML` events for each role.
- A denied write as the auditor role.
- Workflows execution history for one join and one leave.
- The GitHub collaborator list before and after.
- The Jira onboarding and offboarding work items.
- Okta System Log entries for the lifecycle test.
- The Okta group export in `grc-evidence-*`, handed to 08.
- The deviation request for GitHub and Jira.

## Build order

1. Okta org, groups, and the authentication policy.
2. The AWS Account Federation app and its metadata.
3. The `grc-identity-sso` template (SAML provider and four roles) by pull request; the ISSM deploys it.
4. Group to role mapping and one test sign-in per role.
5. Bookmark tiles and the deviation request.
6. Joiner and Leaver flows.
7. Lifecycle test with a test user, and the evidence export to 08.
8. Workflow and role definitions exported into this folder by pull request for ISSM validation.

## Teardown

1. The ISSM deletes the `grc-identity-sso` stack (SAML provider and roles).
2. Deactivate and delete the Joiner and Leaver flows and the Okta apps.
3. Revoke the GitHub fine-grained token and the Jira API token.
4. Remove the test user and any test collaborator.
5. Record teardown evidence (stack deletion event, revoked tokens, deactivated flows).

If 14 is kept instead, schedule a monthly sign-in so the free org does not deactivate, then retire the IAM console passwords in a later access-change PR after the 2 week overlap. If it is torn down, nothing in the access model changes.

## Related projects

- [Access model](../access-model/README.md)
- [01 GRC-as-Code Platform](../01-grc-as-code-platform/README.md)
- [06 Evidence Automation](../06-evidence-automation/README.md)
- [08 Access Reviews](../08-access-reviews/README.md)
- [GOVERNANCE.md](../GOVERNANCE.md)
