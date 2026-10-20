# BC/DR and Incident Response Compliance - Lab Steps (non-engineering)

Write 340 Collective's incident response plan, test it with a tabletop exercise, and record a BC/DR test. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-13-BCDR-IR/LAB-STEPS.md](../../engineering/Rasheed-13-BCDR-IR/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Write an IR plan with sections: Purpose, Scope, Roles and Contacts, Detection, Containment, Eradication, Recovery, Lessons Learned. Base detection on real 340 Collective signals such as GuardDuty findings, CloudTrail alerts, and Stripe dispute notices.
2. Set a target RTO and RPO for the website and client data, and pick the tabletop scenario.
3. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Rasheed starts.

## Share inputs

1. Share these with Rasheed at kickoff once Faris accepts them: the IR plan requirements, the tabletop scenario, and the RTO and RPO targets.

## Test the build

1. When Rasheed says the build is ready, watch one DR test run and check the achieved RTO and RPO against your targets.
2. Write your test result in RESULTS.md under Test results: pass, or findings with what you saw. It is not an approval. Open a pull request.

## Operate it

1. Run a 60-minute tabletop exercise with the team using a phishing-to-data-leak scenario: a phished Google Workspace login leads to exposed client files. Walk each phase of the plan and note where it breaks down.
2. Create an incident report template with fields: Incident ID, Date Detected, Reporter, Severity, Systems Affected, Timeline, Root Cause, Actions Taken, Lessons Learned, Follow-Up Owner.
3. Fill the template out once using the tabletop scenario.

## Assess or report

1. Write a BC/DR test record for 340 Collective's website and client data: the recovery steps (restore from backup or redeploy from GitHub), a target RTO and RPO, the actual time observed in a walkthrough, and any gaps.
2. Commit the tabletop summary and the BC/DR test record to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** Incident response planning · tabletop facilitation · BC/DR testing · RTO/RPO analysis

**Tools:** Google Docs or Word · Excel or Google Sheets · AWS Backup and GuardDuty documentation

**Deliverable:** An IR plan, a tabletop exercise summary, a completed incident report, and a BC/DR test record with RTO/RPO notes.

**What it simulates:** A security or GRC analyst owning incident readiness and resilience testing.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
