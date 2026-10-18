# AWS Continuous Monitoring and Notifications - Lab Steps (non-engineering)

Own the continuous monitoring plan, triage what it raises, and accept the monthly ConMon report as POA&M evidence. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO), owns and operates ConMon. Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Write the ConMon plan: what is monitored (Security Hub with Inspector and Config, Config rule changes, and the CloudTrail events listed in the architecture doc), at what severity, how often, and who is notified.
2. Set the remediation SLAs: critical 15 days, high 30 days, medium 90 days. Only critical and high email in real time; everything else goes to the daily digest.
3. Bring the plan to the Day 1 kickoff. Faris accepts it before Rasheed starts.

## Share inputs

1. Share the plan with Rasheed at kickoff once Faris accepts it, with the list of people to subscribe (they confirm out of band; no addresses go in git).

## Test the build

1. When Rasheed says the build is ready, check that a test HIGH finding opens one Jira issue with its SLA due date, a CRITICAL test event emails you, the digest arrives, and the dashboard shows the counts.
2. Record your test result, or findings, on the project item, then record your validation there.

## Operate it

1. Daily: triage the Jira remediation queue and the digest email, assign an owner, and set the priority.
2. Weekly: review SLAs and chase overdue items with the resource owner (Faris, who builds 11, for misconfigurations; the owning engineer for vulnerabilities).
3. Keep your Jira dashboard over the remediation issues current.
4. GuardDuty: planned, enabled later as code with owner approval. The detector goes in a GRC infrastructure template under `infrastructure/cloudformation/` with the optional protection plans off (S3 Protection, EKS, Malware Protection, RDS, Lambda, Runtime Monitoring, and AI Protection), and it starts on the 30-day free trial. During the trial, read GuardDuty's projected cost estimate in the console with Faris before the keep-or-disable decision.

## Assess or report

1. Monthly: review the ConMon report and accept it as POA&M evidence.
2. Share the first accepted monthly report with Faris.
3. Jason assesses whether monitoring frequency, routing, and SLAs meet CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5 in his phase assessment; answer his questions on the project item.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Rasheed agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Rasheed as needed, or comment on the project item.
- Day 7 sign-off: Rasheed fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Continuous monitoring · vulnerability triage · POA&M management · SLA tracking

**Tools:** Jira · the daily digest email · the CloudWatch dashboard (read) · Security Hub (read)

**Deliverable:** An accepted ConMon plan, a triaged remediation queue, and monthly ConMon reports accepted as POA&M evidence.

**What it simulates:** An ISSO running continuous monitoring and POA&M tracking for a small program.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
