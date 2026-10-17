# AWS Continuous Monitoring and Notifications - Lab Steps (non-engineering)

Own the continuous monitoring plan, triage what it raises, and accept the monthly ConMon report as POA&M evidence. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO), owns and operates ConMon. Partner: Rasheed (ISSE / Engineer). Mirror: [engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md](../../engineering/Rasheed-15-AWS-ConMon/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Write the ConMon plan: what is monitored (Security Hub with Inspector and Config, Config rule changes, and the CloudTrail events listed in the architecture doc), at what severity, how often, and who is notified.
2. Set the remediation SLAs: critical 15 days, high 30 days, medium 90 days. Only critical and high email in real time; everything else goes to the daily digest.
3. Put the plan on the Handoff 1 Jira Task. Faris accepts it on the Task before Rasheed starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Rasheed once Faris accepts it, with the list of people to subscribe (they confirm out of band; no addresses go in git).

## Accept the build

1. When Rasheed creates the Handoff 2 Jira Task, check that a test HIGH finding opens one Jira issue with its SLA due date, a CRITICAL test event emails you, the digest arrives, and the dashboard shows the counts.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Daily: triage the Jira remediation queue and the digest email, assign an owner, and set the priority.
2. Weekly: review SLAs and chase overdue items with the resource owner (Faris, who builds 11, for misconfigurations; the owning engineer for vulnerabilities).
3. Keep your Jira dashboard over the remediation issues current.
4. GuardDuty: planned, enabled later as code with owner approval. The detector goes in a GRC infrastructure template under `infrastructure/cloudformation/` with the optional protection plans off (S3 Protection, EKS, Malware Protection, RDS, Lambda, Runtime Monitoring, and AI Protection), and it starts on the 30-day free trial. During the trial, read GuardDuty's projected cost estimate in the console with Faris before the keep-or-disable decision.

## Assess or report

1. Monthly: review the ConMon report and accept it as POA&M evidence.
2. Create the Handoff 3 Jira Task for Faris with the first accepted monthly report.
3. Jason assesses whether monitoring frequency, routing, and SLAs meet CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5 (Handoff 4); answer his questions on the Task.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic ([GRC-31](https://340collective.atlassian.net/browse/GRC-31)). The person who sends the handoff creates the Task.

- Handoff 1: ConMon plan (sources, severity routing, notification list, and SLAs of 15, 30, and 90 days), Adam to Rasheed (Jira Task, created by Adam)
- Handoff 2: ConMon routing, Jira remediation issues, email alerts, daily digest, and dashboard ready for acceptance, Rasheed to Adam (Jira Task, created by Rasheed)
- Handoff 3: first monthly ConMon report accepted as POA&M evidence, Adam to Faris (Jira Task, created by Adam)
- Handoff 4: ConMon assessment against CA-7, RA-5, SI-2, SI-4, IR-4, and CA-5, Jason to Faris (Jira Task, created by Jason)

**Skills:** Continuous monitoring · vulnerability triage · POA&M management · SLA tracking

**Tools:** Jira · the daily digest email · the CloudWatch dashboard (read) · Security Hub (read)

**Deliverable:** An accepted ConMon plan, a triaged remediation queue, and monthly ConMon reports accepted as POA&M evidence.

**What it simulates:** An ISSO running continuous monitoring and POA&M tracking for a small program.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
