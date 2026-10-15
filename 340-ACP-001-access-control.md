# 340 Collective Access Control Policy

| Document control | Value |
| --- | --- |
| Policy ID | 340-ACP-001 |
| Version | 0.2.0 |
| Owner | Cloud Administrator (name pending); Faris N. (proposed accountable owner) |
| Approver | David C., CEO & Founder (proposed policy assignment; acceptance pending) |
| Effective Date | Not effective; awaiting recorded approval |
| Next Review Date | 2027-10-15 (provisional; reset on approval) |

## Change log

| Version | Date | Change | Approval evidence |
| --- | --- | --- | --- |
| 0.2.0 | 2026-10-15 | Aligned to published studio operations, leadership roles and client/privacy commitments; requirements remain subject to approval. | Pending; no approval recorded. |
| 0.1.0 | 2026-10-15 | Initial draft for collaboration-team review. | Pending; no approval recorded. |

**Status:** Draft. Public statements inform this baseline but do not verify implementation. Named policy responsibilities are proposed and unaccepted. This is a manual governance lab; nothing in this repository deploys to live infrastructure.

## 1. Purpose and scope

340 Collective access must be attributable, approved and limited by client, project and role. This covers AWS, repositories, domain and website administration, media storage/delivery, email, billing, newsletters and any contracted access to client social, advertising or website accounts.

The Operations Lead is the proposed accountable owner; a Cloud Administrator must be named for technical execution. Published leadership roles and provider statements do not establish actual access assignments. See the [website alignment note](../governance/website-alignment.md).

## 2. AWS identity and authentication

1. All routine human AWS access must use IAM Identity Center with MFA, including console, CLI and SDK work. Use individual identities, group-based assignments and least-privilege permission sets. Do not create IAM users or long-lived AWS keys for routine human use.
2. Enforce MFA at the actual identity source. Use Identity Center's settings for its directory; require and verify MFA at an external identity provider if one is used. Local Identity Center MFA settings do not enforce an external provider's MFA.
3. Prefer phishing-resistant MFA and keep factors/recovery codes private. Human CLI and SDK work must use temporary Identity Center credentials. Proposed session limits are one hour for privileged permission sets and eight hours for ordinary access; these are studio choices, not AWS defaults.
4. Approve administrative access separately and time-limit temporary elevation. Do not broaden permissions simply to make an error disappear.

### Workload access

Use scoped IAM roles and short-lived workload credentials, including federation where supported. Workloads do not perform human MFA and must not reuse a collaborator's credentials. Record the owner, purpose, trust relationship, scope and review date. A required long-lived integration secret needs a documented exception, approved storage and rotation/revocation arrangements.

### Root and emergency access

Root-only tasks are a narrow exception to the Identity Center route. Do not use root routinely or create root access keys. Where root credentials exist, require MFA and controlled recovery arrangements. Record purpose, actions and approval; urgent incident containment may proceed under the incident lead, with review by the next business day.

An Identity Center outage does not itself authorise an IAM-user bypass. Any separate emergency identity must be pre-approved, MFA-protected, restricted, tested and monitored. Review every use, revoke sessions and replace exposed credentials. Do not disable MFA for convenience.

## 3. Project and client-account permissions

- Crew and editors receive access only to the projects and functions assigned to them. Separate client folders, upload permissions, edit permissions and publishing authority.
- Restrict lockbox/alarm codes and property access instructions to the people attending the authorised shoot. Use approved secure storage and remove access when the need ends; never place these details in public metadata, portfolio content or Git.
- Use scoped delivery links with an appropriate expiry or named-recipient control. Verify the recipient before release. Keep raw files and working projects separate from approved client deliverables.
- Grant client social/page/ad access only when the purchased service requires it and the client authorises the scope. Prefer native delegation to shared passwords. Record the permitted account, actions, budget limits and end date; remove permissions and tokens at the end of service.
- Separate media publishing, invoice changes, refunds and high-risk administration where feasible. A second authorised person should verify a change to payment instructions through a trusted route.
- Require individual accounts and MFA on email, domain, repository, storage, billing and management tools where supported. An unsupported control needs a recorded vendor-risk decision before use.

## 4. Access lifecycle and evidence

| Event | Required action | Evidence |
| --- | --- | --- |
| Joiner or new project | Record identity, role, project, purpose and duration; approve before access; verify MFA and approved-policy acknowledgment. | Request, approval, assigned scope and verification date. |
| Role or service change | Reassess at the change and remove unneeded grants; adding production work does not automatically grant client-account access. | Before/after permissions and owner decision. |
| Departure or project/service end | Revoke at the agreed time; act immediately for compromise or involuntary removal. | Removed accounts, assignments, delivery shares and token/session actions. |
| Quarterly review | Review active human, crew, vendor, workload and client-delegated access, including dormant or privileged grants. | Dated list, named reviewer, decisions and completed removals. |

Disabling an identity may leave issued sessions valid. Address identity-provider sessions, Identity Center sessions, AWS credentials, repository and client tokens, and cached credentials using supported controls. Verify removal; document remaining session lifetime and containment if immediate revocation is unavailable.

Keep access evidence without copying credentials or recovery codes into the pack. Follow [Data Retention](340-DRP-001-data-retention.md). Review annually and after an account, identity, media-sharing or client-service change or access incident.

Technical references checked 2026-10-15: [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html), [Identity Center identity sources](https://docs.aws.amazon.com/singlesignon/latest/userguide/confirm-identity-source.html), and [AWS root-user guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
