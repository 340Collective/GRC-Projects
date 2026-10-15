# 340 Collective Information Security Policy

| Document control | Value |
| --- | --- |
| Policy ID | 340-ISP-001 |
| Version | 0.2.0 |
| Owner | Faris N., Strategy & Operations Lead (proposed policy assignment; acceptance pending) |
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

340 Collective is a Las Vegas media studio serving realtors, brokerages and local brands. Its work includes planning, scripting, on-site video and photography, aerial capture, editing, and delivery of listing and brand content. This policy protects client information and media throughout that workflow, including any separately agreed social, advertising or website service.

It applies to the studio team, directly managed crew, authorised collaborators and service providers. Assets include brand clarity forms, shoot schedules, unpublished listings, client media, usage permissions, delivery links, business accounts, invoices and policy evidence. Use synthetic client, property, payment and media records in this lab. Real collaborator acknowledgments belong in restricted storage.

The [website alignment note](../governance/website-alignment.md) distinguishes published statements from proposed controls. A public security statement is not implementation evidence. This repository does not authorise a live change or a client security assessment.

## 2. Responsibilities

- **Studio Lead:** David C. is publicly identified as CEO & Founder. His proposed policy responsibilities are approval, risk acceptance, production oversight and external incident decisions. Acceptance of these responsibilities is pending.
- **Operations Lead:** Faris N. is publicly identified as Strategy & Operations Lead. His proposed policy responsibilities cover security coordination, access and vendor reviews, privacy, records and attestation administration. Acceptance is pending.
- **Cloud Administrator:** a technical administrator remains to be named. Implement separately authorised controls and provide evidence to the Operations Lead.
- **Production team and directly managed crew:** protect capture devices, media, property access details and permissions; report losses and unintended disclosure.

These are proposed policy assignments based on published business roles, not evidence that either leader has approved the pack. Name a deputy and a separate reviewer where feasible. Do not treat the public team list as the complete lab collaborator roster.

## 3. Information handling

| Classification | Examples | Required handling |
| --- | --- | --- |
| Public | Approved published listing media, website copy and portfolio content | Confirm release authority, usage rights and absence of private details before publication. |
| Internal | Non-sensitive production procedures and planning notes | Approved team access only. |
| Confidential | Brand forms, unreleased media/listings, invoices, identifiable footage, consent records and attestations | Project-based access, encrypted storage/transfer and approved recipients. |
| Restricted | Account secrets, recovery codes, lockbox/alarm codes and sensitive incident evidence | Named access only; secure secret/evidence storage; exclude from ordinary briefs, chat and repositories. |

## 4. Production and platform controls

1. Maintain an inventory of accounts, devices, media stores, domains and suppliers, with owner, data category, access and disposal rule. Identify where form submissions and delivery files actually reside.
2. Before a shoot, confirm the brand brief, client contact, scope, access arrangements and the client's required permissions. Protect homeowner, occupant and minor-related information. Pause affected capture if required authorisation is missing.
3. Label media by client/project and control transfer from capture device through editing and delivery. Keep at least two verified copies in separate failure domains before erasing capture media; restrict and expire copies under Data Retention.
4. Use supported, encrypted devices and approved tools. Check the selected recipient and release version before sending a file or link. Public portfolio use follows the applicable licence, permissions and confidentiality restrictions; ownership alone is not permission to expose private information.
5. Require IAM Identity Center with MFA for routine human AWS access under [Access Control](340-ACP-001-access-control.md). This is a lab requirement; the website does not establish the AWS account configuration.
6. Translate the published website commitments into controls to verify: HTTPS/TLS and HSTS, encrypted managed storage, private origin storage, least privilege, and an appropriate CSP/security-header configuration. Keep ordinary access logs no longer than 90 days across stores and backups.
7. Review findings against exposure and business impact. Keep confirmed, mitigated, remediated, inaccessible, unverified and unresolved states distinct. An unavailable service or written policy does not prove remediation.
8. Define recovery priorities around active shoots, working media and delivery obligations. Record the actual filming date and agreed delivery date; test a representative restore annually and after a significant storage change. The published 30-day delivery window is a business commitment, not a recovery-time objective.

## 5. Governance and exceptions

The Operations Lead checks access reviews, supplier risks, overdue actions and policy acknowledgments quarterly. Keep evidence of implementation separate from approvals and attestations. Framework references on the website describe alignment; do not represent this pack as ISO certification, a NIST assessment or proof of compliance.

An exception needs scope, reason, risk, compensating controls, accountable person and expiry, with Studio Lead approval before use. Reassess within 90 days. An internal exception cannot silently change a client contract, published privacy commitment or applicable legal obligation.

Review annually and after a material change to production, services, data use, suppliers or an incident. Start a triggered review within 10 business days and record a completion date. Follow the [review schedule](../governance/review-cycle-schedule.md) and [acknowledgment procedure](../governance/attestation-procedure.md). First approved releases become 1.0.0 with actual approval/effective dates; acknowledgment is required for each approved substantive version.
