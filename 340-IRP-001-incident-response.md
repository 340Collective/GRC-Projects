# 340 Collective Incident Response Policy

| Document control | Value |
| --- | --- |
| Policy ID | 340-IRP-001 |
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

340 Collective must respond consistently to suspected or confirmed loss of confidentiality, integrity or availability affecting its media business. Scenarios include stolen capture media, disclosure of property access codes, an unreleased listing sent to the wrong person, unauthorised publication, client social-account compromise, invoice redirection, cloud takeover or loss of working media before delivery.

Exercises must be labelled throughout. This pack authorises tabletop work only; it does not authorise actions on live studio or client systems.

## 2. Reporting and decision roles

The published security/privacy reporting address is **help@340collective.com**. It is a documented intake route, not evidence of continuous monitoring. Report suspected incidents immediately after discovery and also use the agreed urgent internal route. Do not wait for proof.

Faris N., Strategy & Operations Lead, is the proposed incident coordinator. David C., CEO & Founder, is the proposed business decision-maker for production impact and external communications. These assignments need their acceptance. Name a technical responder, deputy and independent fallback contact before approval. If the mailbox or normal platform may be compromised, use the tested fallback.

The public 5-to-7-business-day messaging response window and 30-day delivery commitment are customer-service terms, not incident response targets. Do not delay escalation until a normal response window or holiday ends. Confirm coverage rather than claiming a 24/7 service.

## 3. Triage targets

| Severity | Studio example | Proposed internal response target |
| --- | --- | --- |
| Critical | Active privileged/client-account takeover, ongoing extraction, exposed property access codes with immediate risk, or widespread loss of working media | Contact coordinator and deputy immediately; target triage within one hour of receipt. |
| High | Misdirected unreleased footage, a lost device/card, suspected invoice diversion, or unauthorised identifiable publication | Notify coordinator immediately; target triage within four hours of receipt. |
| Standard | Suspicious event without established impact or a contained low-impact breach of procedure | Report promptly; target review by the next business day. |

These are proposed operating targets, not evidence of staffed coverage or legal deadlines. Record discovery, awareness, receipt and response timestamps with timezone. Escalate to the Studio Lead if the coordinator and deputy cannot be reached. Immediate physical danger should use the appropriate emergency route as well.

## 4. Response workflow

1. **Record and assess.** Assign an incident ID and owner. Identify affected project/client, information, accounts, publication locations and filming/delivery dates. Separate confirmed facts from hypotheses and assess whether other projects are affected.
2. **Preserve.** Preserve relevant evidence before ordinary log/media expiry. Record collector, time, source and storage location; hash exported files where practical. Protect originals and restrict access. Preserve a necessary investigation subset, not a blanket extension of all access logs.
3. **Contain.** The coordinator may authorise proportionate measures: revoke a sharing link or token, disable a compromised identity, restrict a media folder, pause affected publishing or stop a malicious integration. For exposed property codes, contact the authorised client/property contact through a trusted route to arrange replacement. For suspected payment redirection, verify instructions independently and stop the affected payment workflow while assessed.
4. **Eradicate and recover.** Remove the cause, replace compromised credentials and restore trusted media/configuration if needed. Verify permissions and intended operation before resuming delivery or client-account work. Inaccessible assets remain inaccessible/unverified. Record any risk to the agreed client delivery date and obtain business decisions on rescheduling.
5. **Assess notification.** The Studio Lead and Operations Lead promptly assess applicable Nevada requirements, other affected jurisdictions, client contracts and provider/platform obligations with qualified advice. Record affected data, recipients, trigger, deadline, owner and decision, including a reason for no notification. Do not apply a generic 72-hour rule or assume holidays extend a deadline.
6. **Close and improve.** Confirm remediation/recovery evidence, residual risk and outstanding actions. Hold a lessons-learned review within five business days of recovery. Feed findings into production, access, supplier and policy reviews.

## 5. Evidence, exercises and review

Use [Data Retention](340-DRP-001-data-retention.md) for incident evidence and documented holds. All external communications must be factual, authorised and limited to necessary information. A suspected disclosure is not automatically a confirmed notifiable breach.

Run a tabletop annually and after material changes. Include lost shoot media or a wrong-client link, an exposed property code, and client-account or invoice compromise. Record real participants and decisions without inventing test results.

Review annually and after a significant incident, exercise gap, team/service change or notification obligation change. Public context is recorded in the [website alignment note](../governance/website-alignment.md). [Nevada Revised Statutes Chapter 603A](https://www.leg.state.nv.us/nrs/nrs-603a.html) is a relevant source for legal assessment; inclusion does not decide applicability or establish compliance.
