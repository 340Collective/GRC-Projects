# BC/DR and Incident Response Compliance - Lab Steps (non-engineering)

Write 340 Collective's incident response plan, test it with a tabletop exercise, and record a BC/DR test. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-13-BCDR-IR/LAB-STEPS.md](../../engineering/Rasheed-13-BCDR-IR/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Write an IR plan with sections: Purpose, Scope, Roles and Contacts, Detection, Containment, Eradication, Recovery, Lessons Learned. Base detection on real 340 Collective signals such as GuardDuty findings, CloudTrail alerts, and Stripe dispute notices.
2. Set a target RTO and RPO for the website and client data, and pick the tabletop scenario.
3. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Rasheed starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Rasheed once Faris accepts it: the IR plan requirements, the tabletop scenario, and the RTO and RPO targets.

## Accept the build

1. When Rasheed creates the Handoff 2 Jira Task, watch one DR test run and check the achieved RTO and RPO against your targets.
2. Record an acceptance test result on the Task: pass, or findings with what you saw. It is not an approval.

## Operate it

1. Run a 60-minute tabletop exercise with the team using a phishing-to-data-leak scenario: a phished Google Workspace login leads to exposed client files. Walk each phase of the plan and note where it breaks down.
2. Create an incident report template with fields: Incident ID, Date Detected, Reporter, Severity, Systems Affected, Timeline, Root Cause, Actions Taken, Lessons Learned, Follow-Up Owner.
3. Fill the template out once using the tabletop scenario.

## Assess or report

1. Write a BC/DR test record for 340 Collective's website and client data: the recovery steps (restore from backup or redeploy from GitHub), a target RTO and RPO, the actual time observed in a walkthrough, and any gaps.
2. Create the Handoff 3 Jira Task for Faris with the tabletop summary and the BC/DR test record.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic ([GRC-14](https://340collective.atlassian.net/browse/GRC-14)). The person who sends the handoff creates the Task.

- Handoff 1: IR plan requirements, tabletop scenario, and RTO and RPO targets, Jason to Rasheed (Jira Task, created by Jason)
- Handoff 2: restore test and IR runbook build ready for acceptance testing, Rasheed to Jason (Jira Task, created by Rasheed)
- Handoff 3: tabletop summary and BC/DR test record, Jason to Faris (Jira Task, created by Jason)

**Skills:** Incident response planning · tabletop facilitation · BC/DR testing · RTO/RPO analysis

**Tools:** Google Docs or Word · Excel or Google Sheets · AWS Backup and GuardDuty documentation

**Deliverable:** An IR plan, a tabletop exercise summary, a completed incident report, and a BC/DR test record with RTO/RPO notes.

**What it simulates:** A security or GRC analyst owning incident readiness and resilience testing.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
