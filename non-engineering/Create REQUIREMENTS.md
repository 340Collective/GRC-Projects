# Identity and Access (Okta) — Requirements

**Organization:** 340 Collective  
**Project:** Identity and Access (Okta)  
**Document owner:** Adam — Information System Security Officer (ISSO)  
**Implementation partner:** Abdifatah — IAM / Identity Engineer  
**Approver:** Faris — ISSM  
**Status:** Draft — Pending Faris's acceptance  
**Track:** Non-engineering  
**Review period:** Quarterly, through the 08 access review

## 1. Purpose

Define the identity governance requirements for the 340 Collective Okta lab. This document establishes the required groups, group membership rules, application and bookmark assignments, security controls, and acceptance criteria.

The ISSO owns requirements, governance, validation, and evidence review. The IAM / Identity Engineer implements the approved configuration. Faris accepts the requirements and approves the relevant project changes.

## 2. Scope

This project covers:

- Six function-based Okta groups.
- Group-based visibility of AWS, GitHub, and Jira application tiles.
- Group-based visibility of approved bookmark tiles.
- MFA and session requirements.
- Documentation of the intentional absence of single sign-on (SSO).
- Testing, identity-export review, and handoff to the 08 access-review process.

This document does not authorize changes to shared AWS infrastructure or deployment of shared stacks.

## 3. Identity and group model

Create and maintain the following six groups:

| Okta group | Function |
|---|---|
| GRC-ISSM | Information System Security Manager |
| GRC-ISSE | Information System Security Engineer |
| GRC-ISSO | Information System Security Officer |
| GRC-IAM | Identity and Access Management |
| GRC-Auditor | Audit and independent review |
| GRC-Stakeholder | Stakeholder access |

### Membership requirements

1. Each person must have one primary GRC role group.
2. Membership must reflect the person's approved project responsibility.
3. Application visibility must be governed by group membership.
4. Membership changes must be reviewed and reflected in the identity export.
5. The privileged ISSM administrative identity must remain outside Okta.
6. The existence of the GRC-ISSM role group does not authorize placing the privileged ISSM administrative identity in Okta.

## 4. Application assignment rules

The following is the proposed assignment matrix. Confirm it against the accepted architecture requirements before implementation or final acceptance.

| Group | AWS tile | GitHub tile | Jira tile |
|---|---|---|---|
| GRC-ISSM | No | Yes, role-based access only | Yes |
| GRC-ISSE | Yes | Yes | Yes |
| GRC-ISSO | Yes | Yes | Yes |
| GRC-IAM | Yes | Yes | Yes |
| GRC-Auditor | Yes, read-only role | No | Yes |
| GRC-Stakeholder | Yes, read-only role | No | Yes |

**Administrative identity restriction:** The privileged ISSM administrative identity must not be enrolled in Okta. Any GRC-ISSM application assignment applies only to an approved, non-privileged role identity, if one is authorized. Confirm this distinction before accepting the matrix.

### Application URLs

- AWS: https://570814274897.signin.aws.amazon.com/console
- GitHub: https://github.com/login
- Jira: https://340collective.atlassian.net

### Bookmark tiles

Provide the following bookmark tiles to all six GRC role groups:

1. GRC-Projects repository.
2. Open pull requests.
3. Jira GRC project board.

Bookmarks provide navigation only. They do not grant permissions to the destination. Access must still be authorized by GitHub, Jira, AWS, and their respective access-control settings.

## 5. Security requirements

1. Require Okta Verify MFA according to the approved sign-in policy.
2. Configure an eight-hour Okta session.
3. Disable "Keep me signed in."
4. Preserve each target application's own MFA requirements.
5. Maintain a minimum 14-character IAM password policy where applicable to the configured AWS IAM identities.
6. Use least privilege for AWS access, including read-only access for approved auditor and stakeholder roles.
7. Review identity and application assignments quarterly through the 08 access-review process.
8. Remove or update access promptly when a person's role changes or access is no longer required.
9. Do not commit credentials, personal email addresses, account IDs, ARNs, real resource names, or client-sensitive information to this public repository.

## 6. SSO deviation

Single sign-on is intentionally not implemented in this lab. Okta application tiles and bookmarks provide a navigation and access-governance experience; they do not establish federated SSO.

The deviation record must document:

- The reason for the design decision.
- The risk created by the absence of SSO.
- Compensating controls: Okta Verify MFA, application-specific MFA, the eight-hour Okta session, the 14-character IAM password policy, and quarterly 08 access reviews.
- The risk owner, approval, review date, and any outstanding actions.

The deviation must be documented and routed for approval. Compensating controls must be tested; their presence must not be assumed to eliminate all risk.

## 7. Acceptance criteria

The project is ready for ISSO validation when:

- All six required groups exist and membership follows the approved group model.
- Application and bookmark assignments match the accepted matrix.
- The privileged ISSM administrative identity remains outside Okta.
- MFA and session settings have been checked and evidence recorded.
- Each application's independent MFA requirements have been checked.
- The intentional SSO deviation is documented and submitted for approval.
- A sanitized group and application-assignment export is available for 08.
- Test evidence and any findings are recorded in `RESULTS.md`.
- The final engineering report has been compared against the ISSO's test results.

## 8. Approval and change control

This document is a draft until Faris accepts and merges its pull request. The IAM / Identity Engineer must begin implementation only after the requirements are accepted.

Any material change to the group model, assignment matrix, security controls, or SSO decision must be documented and reviewed before acceptance.

## 9. Approval record

- **Prepared by:** Adam — ISSO
- **Reviewed by:** Abdifatah — IAM / Identity Engineer
- **Accepted by:** Faris — ISSM
- **Pull request:** To be added
- **Acceptance date:** To be completed after approval
