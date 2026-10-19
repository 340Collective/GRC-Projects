# AWS Continuous Monitoring and Notifications - Lab Steps (non-engineering)

Own the continuous monitoring plan, triage what it raises, and accept the monthly ConMon report as POA&M evidence. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO), owns and operates ConMon. Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Write the ConMon plan: what is monitored (Security Hub with Inspector and Config, Config rule changes, and the CloudTrail events listed in the architecture doc), at what severity, how often, and who is notified.
2. Set the remediation SLAs: critical 15 days, high 30 days, medium 90 days. Only critical and high email in real time; everything else goes to the daily digest.
3. Write the plan in REQUIREMENTS.md in this folder and open a pull request. Faris accepts it at the Day 1 kickoff and merges the pull request before Rasheed starts.

## Share inputs

1. Share the plan with Rasheed at kickoff once Faris accepts it, with the list of people to subscribe (they confirm out of band; no addresses go in git).

## Test the build

1. When Rasheed says the build is ready, check that a test HIGH finding opens one Jira issue with its SLA due date, a CRITICAL test event emails you, the digest arrives, and the dashboard shows the counts.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. Then record your validation on the Final report item.

## Operate it

1. Daily: triage the Jira remediation queue and the digest email, assign an owner, and set the priority.
2. Weekly: review SLAs and chase overdue items with the resource owner (Faris, who builds 11, for misconfigurations; the owning engineer for vulnerabilities).
3. Keep your Jira dashboard over the remediation issues current.
4. GuardDuty: planned, enabled later as code with owner approval. The detector goes in a GRC infrastructure template under `infrastructure/cloudformation/` with the optional protection plans off (S3 Protection, EKS, Malware Protection, RDS, Lambda, Runtime Monitoring, and AI Protection), and it starts on the 30-day free trial. During the trial, read GuardDuty's projected cost estimate in the console with Faris before the keep-or-disable decision.

## Assess or report

1. Monthly: review the ConMon report and accept it as POA&M evidence.
2. Commit the first accepted monthly report to this folder by pull request (sanitized only).
3. Jason assesses whether monitoring frequency, routing, and SLAs meet CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5 in his phase assessment; answer his questions on the project item.

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Rasheed agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Continuous monitoring · vulnerability triage · POA&M management · SLA tracking

**Tools:** Jira · the daily digest email · the CloudWatch dashboard (read) · Security Hub (read)

**Deliverable:** An accepted ConMon plan, a triaged remediation queue, and monthly ConMon reports accepted as POA&M evidence.

**What it simulates:** An ISSO running continuous monitoring and POA&M tracking for a small program.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
