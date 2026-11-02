# Project 13: BC/DR and Incident Response Requirements

**Organization:** 340 Collective  
**Document status:** Draft version 0.2. Ready for technical feasibility review; not accepted  
**Prepared by:** Jason Stone (Internal Auditor / partner)  
**Engineering reviewer:** Rasheed Jimoh  
**Requirements acceptance:** Faris (pending)  
**Date:** 20 October 2026  
**Repository location:** `non-engineering/Jason-13-BCDR-IR/REQUIREMENTS.md`  
**Project record:** https://github.com/340Collective/GRC-Projects/issues/41

> This working draft is for asynchronous consultation only. Proposed RTO/RPO values, scope, and acceptance criteria are subject to engineering feasibility review and Faris's acceptance. No deployment or implementation is authorized by this draft.

## 1. Purpose and objectives

Provide 340 Collective with a practicable incident response (IR) plan and demonstrable business continuity/disaster recovery (BC/DR) testing for its website and client data. Establish measurable recovery objectives, exercise response procedures, and retain sanitized evidence that an independent partner can assess.

## 2. Proposed recovery objectives

| Business service/data | Proposed RTO | Proposed RPO | Status |
| --- | --- | --- | --- |
| Client data | 4 hours | 24 hours | Proposal; feasibility and acceptance pending |
| Public website | 8 hours | 24 hours | Proposal; feasibility and acceptance pending |

**Definitions:** RTO is the maximum targeted time from an interruption to restoration of the specified service or data access. RPO is the maximum targeted age of recoverable data, measured backward from the disruption. These are initial targets to validate, not promises of demonstrated capability.

**Measurement:** RTO is measured to the point the service or data is usable again, not to completion of the restore job. RPO is measured from the disruption time back to the timestamp of the latest successfully recoverable data, not from when a backup job finished. Example: disruption at 14:00, latest recoverable data from 08:00, demonstrated RPO 6 hours, which meets a 24 hour target. A completed restore job alone does not show that either RTO or RPO was achieved.

**Three levels of recovery, recorded separately:**

| Level | What it shows | Evidence |
| --- | --- | --- |
| Technical restore | The restore job completed | Restore job record and timestamps |
| Data integrity | Restored data matches the source | Record counts, checksums |
| Service recovery | The website or client data is usable again | Service check after reconnection |

**Rationale to validate:** Prioritize access to client data ahead of public website availability, while assuming a low cost, small scale design; a 24 hour RPO implies a potential loss of up to 24 hours of changes if backups/snapshots are only daily. Rasheed should flag whether the actual data classes and business impacts require tighter objectives. Faris should decide whether residual risks are acceptable.

**Scope clarification needed:** Identify the precise website deployment and client data stores, service dependencies, backup frequency, replication/restore approach, and starting/ending timestamps for measuring each objective.

## 3. Recovery design and first test scope

Minimum review scope:

- Website recovery approach (e.g., redeploy from version controlled source and restore required configuration/content, as applicable).
- Client data backup and restore path, including encryption, recovery point retention, access restrictions, and integrity validation.
- Dependencies that could prevent restoration (identity/permissions, keys, networking, cloud services, DNS, configuration, payment related dependencies where in scope).
- One **small synthetic data table** restored to an isolated test target in the first automated DR test, consistent with the engineering lab instructions.
- Automatic cleanup of temporary restored targets after each test; no changes to production records during validation.
- One deliberately **forced failure** to confirm expected detection/routing and creation of a Jira issue through the designed integration, without manually duplicating Jira task tracking.

Engineering to assess feasibility against the shared AWS permissions boundary and the program wide **USD 10/month AWS cap**. Any access change or budget exception goes through the project change process before implementation. Tests must not expose real client data.

## 4. Incident response plan requirements

Prepare an IR plan covering:

1. **Purpose**: objectives, applicability, and assumptions.
2. **Scope**: systems, data, incidents, and exclusions.
3. **Roles and contacts**: incident lead, engineering, business owner, escalation, and approval responsibilities (use role labels, not personal contact details in a public repository).
4. **Detection and triage**: consider GuardDuty findings, CloudTrail alerts, and Stripe dispute notices, as specified in the Project 13 lab instructions. Rasheed to confirm which detection sources are currently operational, which need implementing, and any dependencies. Also cover verification, severity, and evidence capture.
5. **Containment**: isolate affected resources/accounts while preserving evidence and requiring appropriate authorization.
6. **Eradication**: remove root cause, rotate affected credentials safely, and verify remediation.
7. **Recovery**: staged restoration, validation, monitoring, and communication; map to approved recovery objectives.
8. **Lessons learned**: root cause review, corrective actions, owners, and follow up dates.

Document escalation and communication triggers, evidence handling, and where destructive actions require human approval.

## 5. Tabletop exercise requirements

**Scenario:** A phished Google Workspace login leads to exposure of client files.  
**Duration:** 60 minutes.  
**Participants:** Relevant response, engineering, and business decision roles (to be confirmed).  
**Exercise:** Walk through detection, severity assessment, escalation, containment, eradication, recovery, communication, and lessons learned. Identify unclear decisions, gaps, and action owners.

**Outputs:** Sanitized tabletop summary; decisions and timeline; observed gaps; recommended actions, owners and due dates; completed sample incident report.

**Incident report template fields:** Incident ID, Date Detected, Reporter, Severity, Systems Affected, Timeline, Root Cause, Actions Taken, Lessons Learned, Follow-Up Owner.

## 6. Required engineering evidence and acceptance test

Rasheed to provide an accessible demonstration and sanitized evidence for Jason to assess, including:

- Recovery runbook and covered resources (without sensitive identifiers).
- Backup/recovery point configuration and relevant retention settings.
- DR test execution timestamps sufficient to calculate **actual RTO** and **actual RPO** and compare them to the agreed targets.
- Restored test target validation: counts/checksums or comparable integrity checks, without logging record contents.
- Proof that temporary restored resources were cleaned up.
- Evidence of the **forced failure test**, resulting finding/event, and automated Jira issue creation as designed.
- Security control evidence for access separation, encryption, audit logs, and required approval points, consistent with the engineering architecture.
- Test cost and resource usage sufficient to evaluate the project wide budget limit.

**Component level results:** if the test restores only a component (for example the small synthetic table), the result is recorded as component level. It is not evidence that the full website or client data service meets its RTO. The acceptance record states what was tested, what passed, what remains untested, and any limitations or findings.

**Consultation, not authorization:** sharing this draft with Rasheed is for feasibility review. Implementation starts only after Faris accepts the requirements.

**Assessment outcome:** Jason records **Pass** only when the agreed scope is demonstrated and each accepted criterion is met; otherwise records **Findings** with observed facts, impact, and remediation request. Partner sign off is an assessment, **not project approval**. Adam validates and Faris makes the final approval decision under the lab workflow.

## 7. Open questions for Rasheed

1. Do the 4h/24h client data and 8h/24h website objectives appear feasible within the current architecture and budget? If not, what alternatives and trade offs do you recommend?
2. Exactly which resources and dependencies will the first test cover, and what is excluded?
3. How will actual RTO/RPO be computed, especially for the website versus the small table DR test?
4. Can the forced failure path safely prove event routing and Jira issue creation with available permissions?
5. What logs, screenshots, sanitized reports, or walkthrough access can you provide for the independent assessment?
6. Are any access change PRs, costs, or outside team decisions blocking the build?
7. Which IR runbook steps require human authorization and who will exercise those approvals?

## 8. Decision and review record

| Item | Owner | Current state |
| --- | --- | --- |
| Draft requirements and acceptance criteria | Jason | Prepared for review |
| Technical scope, feasibility, and budget assessment | Rasheed | Pending |
| Alignment on recovery objectives and tabletop scenario | Jason and Rasheed | Pending |
| Requirements acceptance and PR merge | Faris | Pending |
| Engineering build and code review | Rasheed / Maria | Not authorized by this draft |
| Partner test results, tabletop, and BC/DR record | Jason | After build and exercise |
| Validation / final project approval | Adam / Faris | Later project stage |

**Handling:** The GitHub repository is public. Never publish account IDs, ARNs, real resource names, personal emails, credentials, client data, or raw incident evidence. Keep sensitive operational evidence in an approved restricted location and refer to sanitized summaries in the repository.

**Submission note:** Submitted by pull request within Jason's non-engineering folder, as confirmed by Faris on Issue #41 (Oct 21, 2026). Faris accepts the requirements and merges the PR; the author does not merge their own PR. Do not update Jira manually unless directed.
