# BC/DR and Incident Response Compliance - Lab Steps

Write 340 Collective's incident response plan, test it with a tabletop exercise, and record a BC/DR test. 340 Collective is the subject organization.

**Lab Steps:**

1. Write an IR plan with sections: Purpose, Scope, Roles and Contacts, Detection, Containment, Eradication, Recovery, Lessons Learned. Base detection on real 340 Collective signals such as GuardDuty findings, CloudTrail alerts, and Stripe dispute notices.
2. Run a 60-minute tabletop exercise with the team using a phishing-to-data-leak scenario: a phished Google Workspace login leads to exposed client files. Walk each phase of the plan and note where it breaks down.
3. Create an incident report template with fields: Incident ID, Date Detected, Reporter, Severity, Systems Affected, Timeline, Root Cause, Actions Taken, Lessons Learned, Follow-Up Owner.
4. Fill the template out once using the tabletop scenario.
5. Write a BC/DR test record for 340 Collective's website and client data: the recovery steps (restore from backup or redeploy from GitHub), a target RTO and RPO, the actual time observed in a walkthrough, and any gaps.

**Skills:** Incident response planning · tabletop facilitation · BC/DR testing · RTO/RPO analysis

**Tools:** Google Docs or Word · Excel or Google Sheets · AWS Backup and GuardDuty documentation

**Deliverable:** An IR plan, a tabletop exercise summary, a completed incident report, and a BC/DR test record with RTO/RPO notes.

**What it simulates:** A security or GRC analyst owning incident readiness and resilience testing.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
