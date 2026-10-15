# 340 Collective Vendor Management Policy

| Document control | Value |
| --- | --- |
| Policy ID | 340-VMP-001 |
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

340 Collective must assess providers and partners before sharing information or granting access. The policy covers cloud and delivery infrastructure, analytics, email, meeting tools, editing/asset software, billing, newsletters, and integrations for contracted client services.

The website names Cloudflare Web Analytics, Google Meet and Stripe. Treat these as published provider references, not evidence of an assessed account or live integration. The pricing page also contains an unconnected-checkout notice; payment activation is unverified. AWS is required by the lab brief but its deployed scope is unverified. See the [website alignment note](../governance/website-alignment.md).

The studio describes production by its team and directly managed crew, without independent outsourcing or offshoring. Infrastructure providers are distinct from creative subcontracting. Do not approve an external content-production service through a routine software purchase. Any partner arrangement must respect the agreed production model, client permissions and confidentiality.

## 2. Ownership and register

The Operations Lead maintains the register and assessments. The Studio Lead approves onboarding and residual risk. Each service needs an accountable business owner and a technical contact where relevant.

Record service, purpose, status (proposed / published reference / verified active / retired), processed data, locations/subprocessors, access, risk tier, contract and renewal dates, evidence, approval, last/next review and exit method. Do not mark a named provider approved merely because it appears on the website.

## 3. Assessment by exposure

| Tier | Trigger | Minimum review |
| --- | --- | --- |
| High | Privileged infrastructure/client-account access, sensitive property information, payment integration, or a core media/delivery dependency | Access and MFA, encryption, logging, availability/recovery, incident reporting, processing locations, subprocessor controls, export/deletion and relevant assurance. |
| Medium | Contact/brand information, unreleased media or other Confidential records without high-tier triggers | Permitted use, access, privacy terms, retention, deletion, incident contact and project separation. |
| Low | Public information only, no privileged access and low dependency | Purpose, owner, appropriate terms and exit route. |

Assess actual configuration and data use. A cookieless analytics statement does not eliminate the need to check what the integration collects. A certificate is useful only where its scope and validity apply to the service being used.

## 4. Onboarding requirements

1. Document the minimum data and permissions needed and confirm the service does not contradict client commitments.
2. Review security/privacy terms, processing locations, subcontractors, incident reporting and relevant legal obligations. Obtain suitable processing/confidentiality terms where required.
3. Confirm data return, deletion, backup expiry and access removal. Preserve the public limits on ordinary access logs and raw media; do not accept a vendor default that silently extends them.
4. For payment processing, confirm the actual hosted checkout, processor account, permitted administrators and receipt/reconciliation workflow before use. The studio must not collect card numbers or security codes through its contact form, messages or local files.
5. For AI tools, approve only the publicly permitted support purposes: ideas, analytics and research. Review retention/training settings and data exposure; do not use the vendor to create client media contrary to the production promise.
6. Record approval and unresolved conditions before data or access is provided. Do not silently add advertising tracking, sell/rent client information or widen newsletter use through an integration.

## 5. Crew, partners and ongoing review

Directly managed crew need named accounts, confidentiality and media-handling obligations, role-specific access and project-end removal. Confirm any partner's scope and authorised recipients before exchanging a client's media; partnership terms do not grant access to unrelated client work.

Review active providers annually, at renewal, and after a material service, data-location, access or security change. Assign owners and dates to gaps. Restrict new data/access while a material issue remains unresolved.

At exit, remove integrations and tokens, retrieve required records, and obtain deletion evidence. Record any necessary retained copies and expiry. Closing a service account is not evidence of complete deletion.

## 6. Exceptions, evidence and review

Use the [Information Security](340-ISP-001-information-security.md) exception process. It does not waive a public promise or client contract. Keep register, assessment, agreement and exit evidence under [Data Retention](340-DRP-001-data-retention.md); route supplier incidents through [Incident Response](340-IRP-001-incident-response.md).

Review this policy annually and after a material change to the studio's production model, providers, partnerships, client services or data use.
