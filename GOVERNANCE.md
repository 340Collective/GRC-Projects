# Governance

How this collaboration runs. This repo is a GRC engineering portfolio built by a small team, using 340 Collective's AWS account as a shared testbed. It is a learning project, not a business need. The goal is real hands-on experience that holds up on a resume, produced under the same discipline a regulated program would use.

Status: this document is the operating manual. The 16 projects (00 to 15) are target designs, not yet deployed. Each project has an engineering folder and a non-engineering folder (see the root [README](README.md)).

![GRC Projects governance: the engineering and non-engineering tracks, the review flow from build to merge, and the deviation path](shared/governance-diagram/grc-governance.png)

The diagram above shows the two tracks and how a change moves from a build through code review, partner acceptance, ISSO validation, and the ISSM decision to merge, with the deviation path when a change cannot be made. The diagram sources are in [shared/governance-diagram/](shared/governance-diagram/) as PNG and SVG, with `grc-governance_build.py` to regenerate them. The governance diagram predates partners pushing their own records, so its Jira labels are out of date. The text in this document is current.

The shared control reference for every project is the [ASFF control matrix](non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx). Map findings, evidence, risks, and deviation requests to its ASFF `SecurityControlId` values so the whole program speaks one control language. Changes to the matrix follow the change process below, like any other change. It is maintained with [01 GRC-as-Code Platform](engineering/Faris-01-GRC-as-Code-Platform/README.md). The file sits in Jason's 01 folder, so only Jason changes it, by pull request, and Faris reviews and merges it.

## Principles

- Build it as code. Infrastructure is created only through CloudFormation. Anything created by hand in the console is deleted.
- Keep it cheap. Total AWS spend stays under 10 dollars per month across the whole project, and 0 dollars is the target. Build, test, and keep each build running cheaply as part of one system. Tear it down only in the end-of-program teardown, Jan 11 to 18, 2027.
- Nobody signs off on their own work. Separation of duties is enforced through roles, code review, the partner's sign-off on the final report, and pull request approval.
- Change is controlled. Every change is a pull request the ISSM approves (Adam approves Faris-built work). If a needed change cannot be made, it goes through a deviation request.
- Do not make an expensive mess. Check service quotas and limits before building. If a service is not free, confirm the cost before enabling it.

## Roles

| Person | Role | Track | Responsibility |
| --- | --- | --- | --- |
| David | Business Owner / Stakeholder | Outside both tracks | Owns 340 Collective and its AWS account. Faris reports to David. David is informed only: he does not approve pull requests or changes. |
| Faris | ISSM / Architect (Program Lead) | Engineering, and 00 on the non-engineering side | Owns governance and gives final approval on every pull request and access change, except his own builds. Also builds: the shared foundation (Phase 1), 01 (Phase 2), 11 (Phase 3), and the 00 overview (every phase). Accepts each partner's requirements at the Day 1 kickoff, except 01, which Adam accepts. |
| Rasheed | ISSE / Engineer | Engineering | Builds 07, 13, 09 with the 04 monthly scoring run, 12, and 15. Reviews code for Faris, Maria, and Abdifatah. Named backup on the critical-path foundation. |
| Maria | Automation Engineer | Engineering | Builds 06, 10, 03, 02, and 05. Reviews code for Rasheed (including 15) and Abdifatah, and is the backup reviewer on Faris's builds. |
| Abdifatah | IAM / Identity Engineer | Engineering | Builds 14 and 08. Adds review capacity from Phase 3. |
| Adam | ISSO / Analyst | Non-engineering | Partner for 05, 06, 07, 08, 11, 12, 14, and 15: writes requirements, accepts the build, operates it, and reports. Validates all engineer work. Accepts and gives final approval on Faris-built work (foundation, 01, 11, 00). Pushes his own records to his non-engineering folders. |
| Jason | Internal Auditor / Assessor | Non-engineering | Partner for 01, 02, 03, 04 (lead), 09, 10, and 13: writes requirements and runs the acceptance test, recorded as a pass or findings record, not an approval. Assesses independently once per phase. Builds nothing and never approves. Pushes his own records to his non-engineering folders. |

"Independent" in the Internal Auditor's role means independent from the work under review, not from the organization. His AWS access is the access model's read-only `GRC-Auditor` group (MFA required). He cannot change that access, and every change to it is an ISSM-approved pull request. His findings are internal assessment, not independent attestation.

## Two-track model

Every project has two folders with the same number: one in `engineering/` for the person who builds it, and one in `non-engineering/` for the partner who sets requirements, accepts the build, and operates it. Both folders mirror each other. Each project has one GitHub Project item with one Final report item under it, and one Jira epic (the key is in each project page header and in the README project map).

Why two tracks: the split separates duties. The person who builds a thing does not write its requirements or validate it. Partners write the requirements, test the build, and record the results in their own folder. Engineers build and test their own work in theirs. That separation is the control this program demonstrates. The split is about roles, not repo access: everyone pushes to this repo, and each person changes only their own folders. Faris's own builds are the exception for requirements: he writes the foundation and 00 requirements, so Adam accepts them, validates the build, and gives final approval. Jason writes the 01 requirements with Faris, and Adam accepts them.

| # | Project | Engineer (builds) | Partner | Phase | Points |
| --- | --- | --- | --- | --- | --- |
| 00 | Platform Overview | Faris | Faris; Adam accepts | Every phase (docs) | none |
| 01 | GRC-as-Code Platform, plus the shared foundation | Faris | Jason | Foundation 1, 01 2 | 3 + 2 |
| 02 | TPRM/VRM | Maria | Jason | 4 | 2 |
| 03 | Privacy | Maria | Jason | 3 | 2 |
| 04 | Gap Analysis | Rasheed (monthly scoring run only) | Jason (lead) | 3 | 1 |
| 05 | Policy Management | Maria | Adam | 5 | 1 |
| 06 | Evidence Automation | Maria | Adam | 1 | 3 |
| 07 | Risk Register | Rasheed | Adam | 2 | 2 |
| 08 | Access Reviews | Abdifatah | Adam | 2 | 2 |
| 09 | Control Testing | Rasheed | Jason | 3 | 2 |
| 10 | Audit Engagement Manager | Maria | Jason | 2 | 2 |
| 11 | Compliance-as-Code Guardrails | Faris | Adam | 3 | 3 |
| 12 | Metrics and Reporting | Rasheed | Adam | 4 (needs data from 06, 11, and 07) | 2 |
| 13 | BC/DR and IR | Rasheed | Jason | 1 | 2 |
| 14 | Identity and Access (Okta) | Abdifatah | Adam | 1 | 2 |
| 15 | AWS Continuous Monitoring (ConMon) and Notifications | Rasheed | Adam | 5 | 2 |

### Points

Size sets the points: S = 1, M = 2, L = 3. Totals: Faris 8, Rasheed 10 plus 1 for the 04 scoring run, Maria 10, Abdifatah 4. The 00 overview is documentation and carries no points.

### Phases

One active build per engineer at a time. A phase ends when all its builds are merged, signed off, and running in the shared system. The program starts Monday 2026-10-19.

| Phase | Dates (2026) | Faris | Rasheed | Maria | Abdifatah | Adam (ISSO) | Jason (Internal Auditor) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Oct 19 to 25 | Foundation | 13 | 06 | 14 | Foundation, 06, 14 | 13 |
| 2 | Oct 26 to Nov 1 | 01 | 07 | 10 | 08 | 07, 08 | 01, 10; assesses P1 |
| 3 | Nov 2 to 8 | 11 | 09 and the 04 scoring run | 03 | Review | 11 | 03, 04 (lead), 09; assesses P2 |
| 4 | Nov 9 to 15 | Review | 12 | 02 | Review | 12 | 02; assesses P3 |
| 5 | Nov 16 to 22 | Review | 15 | 05 | Review | 05, 15 | Assesses P4 |
| Buffer | Nov 23 to 25 | Integration and end-to-end check; final reports | Integration and end-to-end check; final reports | Integration and end-to-end check; final reports | Integration and end-to-end check; final reports | Integration and end-to-end check; final reports | Assesses P5; integration check; final reports |

The Adam and Jason columns are the projects they partner on in that phase (requirements, acceptance, operation). Jason also assesses the previous phase.

### 7-day build rule

Every project build is time-boxed to 7 days, and each engineer has one active build at a time.

- Day 1: kickoff. The partner writes REQUIREMENTS.md in their own folder by pull request, and the engineer and partner agree on scope. Faris accepts the requirements (Adam accepts Faris's own and the 01 requirements).
- Days 2 to 6: build and code review. The engineer talks to the partner as needed.
- Day 7: final report. The engineer commits [FINAL-REPORT.md](shared/templates/FINAL-REPORT.md): what was built and what the builder's tests showed. The partner commits their test and operating results to their own folder ([RESULTS.md](shared/templates/RESULTS.md)), compares them with the report, and signs off on the Final report item ("Accepted by: <first name>", or findings) with a link to the results. Faris merges the engineer's pull request only after the sign-off. The build stays deployed, and the partner operates it and reports.

If a build is at risk by day 4, flag it in Jira. Faris then either cuts scope or grants one 3-day extension. No weekend catch-up.

11 is in Phase 3, after the foundation and 01 it builds on. 12 is in Phase 4 because it needs data from 06, 07, and 11, so 11 lands first. 15 is in Phase 5 because it posts its monthly KPIs to the GRC Metrics Jira issue that 12 builds in Phase 4, and needs findings from 01 and 11. That keeps every engineer to one active build at a time. Faris updates the 00 overview at the end of every phase.

### Dependencies between builds

The projects form one system. Later builds read from earlier builds, so earlier builds must stay live.

- The shared foundation (`grc-foundation`) stays up for the whole program. Every build uses it. It is the last `grc-*` project stack deleted (FR-33).
- 12 (Phase 4) reads the stores of 02, 05, 07, 08, and 10, plus Security Hub, and needs data from 06, 07, and 11. 02 and 05 land in Phase 4 and Phase 5, so 12 reads them in integration week.
- 15 (Phase 5) posts KPIs to the GRC Metrics Jira issue that 12 builds, and needs findings from 01 and 11. It needs 12, 01, and 11 live.
- 09 (Phase 3) samples populations from the 06 evidence lake and the 07 register. It needs both live.
- 13 (Phase 1) routes failed DR tests to 07 and 06. 07 lands in Phase 2, so the route to 07 is tested end to end in integration week.
- 08 (Phase 2) reads the 14 Okta export from the 06 evidence lake. It needs 14 and 06 live.
- 11 builds on the foundation and 01.
- Evidence buckets expire current objects after 30 days. That is data retention, not teardown. 12 trends and 09 samples see only the last 30 days of evidence.

### Integration week

Nov 23 to 25. All builds run together in the shared system.

- The end-to-end check follows data across builds. For example: 06 evidence to 12 metrics and 15 ConMon, a 13 failed test to 07 and 06, the 14 export to 08, and 12 metrics to the GRC Metrics Jira issue.
- Each partner checks the handoffs across their projects and commits final results to their own folders.
- Jason assesses P5 and the integration check, and commits his assessment to his own folder.
- Final reports finish.

### End-of-program teardown

Two different things are called cleanup. Keep them apart.

- Test cleanup: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Always required, in every phase.
- End-of-program teardown: deleting the running system. It happens once, at the end of the program. It is never a Day 7 step and never a phase-end step.

The full teardown runs Jan 11 to 18, 2027, and finishes by 2027-01-18. Owner decision, 2026-10-19. The system stays running through integration week (Nov 23 to 25) and the December and January side projects.

Nothing in the infrastructure is permanent, by design. Every resource is created by a CloudFormation stack in this repo, carries the `grc-project` tag, and is removed by deleting its stack. So the account can be emptied cleanly at any time. A build must not create a hand-made or retained resource (for example `DeletionPolicy: Retain`, or anything created by hand) without a documented teardown step.

1. Each project stack runs its own LAB-STEPS teardown steps, latest phase first.
2. `grc-foundation` is deleted last (FR-33).
3. Shared stacks are removed only as the ISSM decides.
4. Teardown evidence is recorded where the ISSM designates, outside git, and noted on each Jira epic.

### Sign-off

Acceptance means the partner's sign-off on the final report: a comment on the project's Final report item ("Accepted by: <first name>", or findings). Faris accepts the partner's requirements at kickoff; Adam accepts Faris's own and the 01 requirements. Jason's phase assessments stay separate items.

## Where work lives

| Jira (tracking only) | GitHub |
| --- | --- |
| Phases, timelines, assignments, blockers | Code, templates, architecture, diagrams, lab steps |
| Day-to-day comments | Requirements, test results, operating results, and final results, in each partner's folder |
| Automated remediation tickets (from 01 and 15) | Final report per project, and sign-off and validation on the Final report item |

- Ask your partner directly or comment on the project item. Requirements and results live in the partner's own GitHub folder. The partner pushes them by pull request (see [CONTRIBUTING.md](CONTRIBUTING.md#partner-pull-requests)).
- The GitHub Project [GRC Program](https://github.com/orgs/340Collective/projects/2) tracks phases, timelines, assignments, blockers, and final report sign-off as issues in this repo. It runs in parallel with Jira during Phase 1. GitHub is the source of truth, and Jira is archived after Phase 1 if GitHub works.
- Adam and Jason push their own work, so they need Write access on this repo. Only Faris merges. Jason's AWS access stays the read-only GRC-Auditor group, so his independence holds.
- Evidence in GitHub is sanitized only: redacted screenshots, a hash manifest, summary tables. Raw evidence stays in the temporary evidence bucket and is deleted at teardown.

## Separation of duties

The rule is that no one validates or approves their own work, and nobody validates their own requirements. The review flow for every build:

1. Requirements: the partner writes REQUIREMENTS.md in their own folder by pull request. Faris accepts it at the Day 1 kickoff. Adam accepts the requirements Faris writes (00, the foundation). Jason writes the 01 requirements with Faris, and Adam accepts them.
2. Build: the engineer builds in a branch. Templates live in `infrastructure/` in this repo and go by pull request into `main`.
3. Code review: another engineer reviews in GitHub. Rasheed reviews Faris (Maria as backup) and Maria. Maria reviews Rasheed, including 15. Rasheed or Maria reviews Abdifatah. Abdifatah adds review capacity from Phase 3.
4. Partner sign-off: the partner commits test and operating results to their own folder, compares them with the engineer's report (FINAL-REPORT.md), and signs off on the Final report item with a link to the results. On Jason's projects (01, 02, 03, 04, 09, 10, 13) his sign-off is a pass or findings record, not an approval.
5. Validation: Adam validates engineer work and records it on the Final report item.
6. Final approval: Faris approves or denies. For Faris-built work (foundation, 01, 11, 00), Adam accepts and gives final approval instead. Faris merges after approval.
7. Assessment: Jason assesses independently once per phase, never per pull request. He commits each assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/` and links it on the phase assessment item. He builds nothing and never approves.
8. Merge: an engineer's pull request links its project item and merges only after the partner's sign-off is on the Final report item. Only Faris merges.
9. Partner pull requests: a partner's pull request changes only their own folder. Faris reviews it for scope and the data rules, and merges it. He does not change or approve the partner's findings. Engineers do not review or approve partner records. For Faris's own 00 folder, Adam reviews before Faris merges.

Adam is both partner and validator on his own projects. That is accepted because he did not build them; the build was the engineer's, and Faris still gives final approval.

Jason is both partner and assessor on 01, 02, 03, 04 (lead), 09, 10, and 13, where he writes the requirements and runs the acceptance test. That is accepted because his acceptance is a pass or findings record and never an approval, and he builds nothing. His phase assessment of those projects is marked partner-assessed in his assessment file, so a reader knows he also set the requirements. Faris (or Adam for 01) still gives final approval. Owner decision, 2026-10-17.

### RACI

Engineer builds. Code review is in GitHub. Partner writes requirements and signs off on the final report (acceptance). Validates is the ISSO's check. Final approval merges or denies. Assesses is Jason's independent phase assessment. Informed is kept up to date.

| Project | Engineer (builds) | Code review | Partner (requirements and acceptance) | Validates | Final approval | Assesses | Informed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 Platform Overview | Faris | Rasheed (Maria as backup) | Faris; Adam accepts | Adam | Adam | Jason | David |
| Shared foundation | Faris | Rasheed (Maria as backup) | Adam | Adam | Adam | Jason | David |
| 01 GRC-as-Code Platform | Faris | Rasheed (Maria as backup) | Jason (acceptance test and coverage assessment); Adam accepts | Adam | Adam | Jason (also partner; see note) | David |
| 02 TPRM/VRM | Maria | Rasheed | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 03 Privacy | Maria | Rasheed | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 04 Gap Analysis | Rasheed (scoring run) | Maria | Jason (lead, acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 05 Policy Management | Maria | Rasheed | Adam | Adam | Faris | Jason | David |
| 06 Evidence Automation | Maria | Rasheed | Adam | Adam | Faris | Jason | David |
| 07 Risk Register | Rasheed | Maria | Adam | Adam | Faris | Jason | David |
| 08 Access Reviews | Abdifatah | Rasheed or Maria | Adam | Adam | Faris | Jason | David |
| 09 Control Testing | Rasheed | Maria | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 10 Audit Engagement Manager | Maria | Rasheed | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 11 Guardrails | Faris | Rasheed (Maria as backup) | Adam | Adam | Adam | Jason | David |
| 12 Metrics and Reporting | Rasheed | Maria | Adam | Adam | Faris | Jason | David |
| 13 BC/DR and IR | Rasheed | Maria | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 14 Identity and Access (Okta) | Abdifatah | Rasheed or Maria | Adam | Adam | Faris | Jason | David |
| 15 AWS ConMon | Rasheed | Maria | Adam | Adam | Faris | Jason | David |
| Partner records (each `non-engineering/<Partner>-*` folder) | none (the partner writes them) | none | the partner | none | Faris reviews and merges; Adam reviews Faris's 00 folder | none | David |
| Access-model changes (`grc-access-model`), except the auditor seat | Faris, in `infrastructure/` | Rasheed | none | Adam | Faris | Jason (internal audit review) | David |
| Engineer seat changes (`grc-engineer-users`) | Faris, in `infrastructure/` | Rasheed | none | Adam | Faris; Adam for a change to the `faris` seat itself | Jason (internal audit review) | David |
| Auditor-seat changes (`GRC-Auditor`, `internal-auditor-*`) | Faris, in `infrastructure/` | Rasheed | none | Adam | Faris | none (Jason never reviews his own access) | Jason, David |

Jason never reviews a change to his own access. Faris never gives final approval on his own build or his own seat; Adam does.

## Change process

Modeled on a FedRAMP-style change workflow.

1. Open a change by creating a branch and a pull request against `main`. Describe what changes, why, the expected cost impact, and the linked project item.
2. Another engineer reviews the code. The partner signs off on the Final report item with a link to their results, and Adam validates there.
3. Faris approves or denies (Adam for Faris-built work). Approval merges; denial returns it with comments.
4. If a change is needed but cannot be made (a quota block, a cost ceiling, a missing dependency), file a deviation request instead of forcing the change.

A partner's change to their own folder follows step 9 of the review flow.

### Deviation request

When you cannot make a required change, document it so the gap is tracked rather than hidden. Include:

- What was required and why it cannot be done now.
- The risk or control affected.
- The workaround or compensating control in place.
- The target date to revisit.

## Reporting

Reporting costs 0 dollars a month day to day.

- Adam and Jason use Jira dashboards: findings, risks, reviews, remediation age, and KRIs.
- Engineers use CloudWatch dashboards for pipeline health, inside the free tier (3 dashboards of up to 50 metrics, 10 custom metrics).
- Leadership gets a monthly board pack built by project 12, as HTML or Markdown emailed through the existing SES setup.

AWS data reaches Jira three ways:

1. Findings: the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html) (11 guardrails, 01 and 04 posture, 15 ConMon).
2. Project events: an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook (07 risks, 08 review results, 10 overdue requests, 13 failed DR tests, 15 remediation issues).
3. Metrics: project 12's daily job posts results to the "GRC Metrics" Jira issue.

Do not use the AWS Service Management Connector; AWS retires it after 2027-03-31. Jira tokens live in Secrets Manager (through an EventBridge connection) or an SSM SecureString parameter under `/grc/`, never in git.

## Cost guardrails

The project runs at or near 0 dollars. These are the rules and the watch list that keep it there.

- Every account gets an AWS Budget of 10 dollars with alerts at 1, 5, and 10 dollars, defined in CloudFormation.
- Build, capture evidence with screenshots, and keep the build running in cheap mode. Test cleanup after every test is required, not optional. The end-of-program teardown is required too, once.
- Check service quotas and limits before building anything.

Services that can break the budget if left running. Confirm cost before enabling:

- QuickSight: not used. Standard authors run about 9 to 12 dollars per user per month, which alone can exceed the whole budget. Reporting uses Jira dashboards, CloudWatch dashboards inside the free tier, and 12's emailed board pack instead.
- Macie (03): free trial, then charges per gigabyte scanned. Keep to the trial or sample data.
- Audit Manager (06): charges per assessment. Enable only while capturing evidence, then disable.
- Config, GuardDuty, Inspector, Security Hub (01, 06, 11, 15): free tiers that expire, usually after 30 days, then charge per item. Watch the clock. Config has no trial and bills from day one. Scale down or pause these under the running system cost rule.
  - GuardDuty: planned, enabled later as code with owner approval. The detector goes in a GRC infrastructure template under `infrastructure/cloudformation/` with the optional protection plans off (S3 Protection, EKS, Malware Protection, RDS, Lambda, Runtime Monitoring, and AI Protection). It starts on the 30-day free trial, and the projected cost estimate on the GuardDuty console usage page is read during the trial before deciding to keep it on ([GuardDuty pricing](https://aws.amazon.com/guardduty/pricing/)).
  - Inspector: covers 7 Lambda functions, 0 EC2 instances, and 0 ECR images (read-only check 2026-10-17). Inspector's own usage estimate is about 1.47 dollars a month, and it is not on the bill yet, likely still the free trial. Expect about 1.50 dollars a month after the trial. List price is 0.30 dollars per function per month for standard scanning, so 7 functions for a full month would be 2.10 dollars; the estimate is lower because Lambda scanning is prorated by coverage hours, so a function is not billed for a full month unless Inspector covers it all month ([Inspector pricing](https://aws.amazon.com/inspector/pricing/), checked 2026-10-17).
- Cost Explorer API: 0.01 dollars per paginated API request, so batch the monthly review queries into one session ([Cost Explorer pricing](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/) and the [Cost Explorer user guide](https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html), checked 2026-10-17).
- Secrets Manager (the EventBridge connections to Jira in 01, 07, 13, and 15): about 0.40 dollars per secret per month. It is on the access model's budget-breaker deny list today, so it needs an access-change pull request first.
- 15 ConMon: about 0 to 1 dollar a month. AWS service events on the default bus are free, SNS email and Lambda stay in their free tiers, one CloudWatch dashboard is free, and the connection secret is about 0.40 dollars.
- Okta (14): the Integrator Free Plan is 0 dollars but is meant for development and testing. It caps at 10 active users and 5 Workflows, and the org deactivates if nobody signs in for 90 consecutive days. Single sign-on into GitHub needs GitHub Enterprise Cloud and into Jira needs Atlassian Guard, both paid per user per month, which would break the budget. 14 does not use single sign-on: the Okta Browser Plugin fills each tool's own sign-in, and each tool keeps its own MFA.

### Running system cost

Every build stays running until the end-of-program teardown, so the cost that matters is all builds running at once. The ranges below are planning estimates for this small account from each project's cost notes and AWS list prices ([Config pricing](https://aws.amazon.com/config/pricing/), [Security Hub pricing](https://aws.amazon.com/security-hub/pricing/)). They are not quotes.

| Component | Projects | Left-on cost (dollars a month) | Notes |
| --- | --- | --- | --- |
| Customer managed KMS keys, about 1 each | Foundation, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13 (13 plans more than one) | 13 to 16 | The largest fixed cost. Every LAB-STEPS asks for its own key. Sharing the foundation key would bring this to about 1 |
| IAM Access Analyzer unused access analyzer | 08 | about 45 | Billed per IAM role and user analyzed per month. The account holds the 222 synthetic UAR simulation users plus roles. The largest single item. Run it only during a review campaign and delete it after; the external access analyzer is free and can stay |
| Config recorder and rules | 01, 04, 06, 11, 15 | 1 to 5 | No free trial: charges start on day one. Per item recorded and per rule evaluation. Daily (periodic) recording and few rules keep it low |
| Security Hub | 01, 04, 06, 11, 15 | 2 to 10 after the 30-day trial | Per check and per finding. One standard only keeps it low |
| GuardDuty | 15 (planned, owner approval) | 1 to 4 after the 30-day trial | Optional protection plans off |
| Inspector | 01, 15 | about 1.50 | Measured above |
| Audit Manager | 06 | 1 to 3 | Per resource assessment. Pause between evidence runs |
| Macie | 03 | 0 to 1 | Per bucket monitored and per GB scanned. No scheduled jobs between tests |
| Secrets Manager connection secrets, 0.40 each | 01, 07, 11, 12, 13, 15 | about 2.40 | Use SSM SecureString where a Lambda calls Jira, which is free |
| CloudWatch dashboards beyond the 3 free | 02, 12, 15, plus engineer pipeline dashboards | 0 to 9 (3 each past 3) | Keep to 3 dashboards account wide |
| CodePipeline and CodeBuild | 05, 11 | 0 to 2 | Per pipeline and build minutes. Few builds |
| AWS Backup storage | 13 | under 0.50 | Small tables, short retention |
| Textract, Comprehend | 02 | 0 when idle | Per page and per unit, only during tests |
| Scheduled Lambdas, Step Functions, EventBridge, DynamoDB on demand, API Gateway, S3, Athena, SES, SNS, SQS, Cognito | 02 to 15 | 0 to 1 | Free tiers at daily, weekly, monthly, or quarterly cadence |
| NAT gateway, EC2, RDS, QuickSight | none | 0 | Blocked by the access model's budget-breaker deny list |
| Okta Integrator Free Plan | 14 | 0 | Not a cost. The org deactivates after 90 days with no sign-in. Needs a monthly sign-in to last to 2027-01-18 |
| Existing non-GRC account spend | account | about 1 to 2 | October 2026: Bedrock, S3, Cost Explorer |
| Total, as designed (own keys, unused access analyzer left on, security services on after trials) | | about 70 to 100 | Far over the 10 dollar cap. 01's own design estimate is 75 to 120 with full coverage |
| Total, cheap mode (one shared key, unused access analyzer only during a campaign, security services paused or scaled down, 3 dashboards, SSM over Secrets Manager) | | about 4 to 9 | Fits the cap with little margin |

Keep the system running, and keep it cheap. Schedules run at the lowest useful frequency (daily or slower), resources use the smallest size, and test artifacts are deleted after every test. If the 1 dollar alert fires, check what is running. If the 5 dollar alert fires, scale down or pause the most expensive component first (in this order: the unused access analyzer, Security Hub standards, Config rules and recording, GuardDuty, Audit Manager, Macie, extra dashboards), and record what was paused on the Jira epic. Do not tear the system down to save cost. A paused component is turned back on as code, by pull request.

The cap stays 10 dollars a month, with alerts at 1, 5, and 10 dollars. As designed, running everything can go over the cap. The owner accepts that, and the alerts are the control. Owner decision, 2026-10-19. AWS Budgets alerts notify but do not stop spending, so someone must act on each alert.

Actual spend (owner-verified, read-only checks 2026-10-17):

- September 2026: about 0.66 dollars total (S3 0.55 dollars, Cost Explorer API 0.11 dollars).
- October 1 to 16, 2026: about 1.53 dollars (Bedrock about 1.32 dollars including Claude Haiku, S3 0.17 dollars, Cost Explorer 0.05 dollars).

## Access to the real environment

Access to 340 Collective's AWS account is granted only after the accounts exist and only through least-privilege IAM defined in CloudFormation. Access is not granted by hand.

- Roles are defined as code, scoped to what each role needs: engineer (build, deploy, run, and at the end of the program tear down their own `grc-*` project stacks), internal auditor (read-only audit and evidence read, MFA required), analyst (read plus evidence export).
- Engineers author `grc-*` templates in pull requests to `infrastructure/`. Only the ISSM deploys the shared stacks (`grc-access-model`, `grc-internal-auditor`, `grc-engineer-users`, `compliance-evidence`, and `grc-uar-sim-*`). Each engineer deploys their own project stack with their `GRC-Engineer` seat, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off until the end-of-program teardown. Every deploy runs only from this repo's clean `main` equal to `origin/main`, after merge, under the 340 change-control rule (see [infrastructure/README.md](infrastructure/README.md)).
- Planned, not deployed: `GRC-Engineer` seats for Maria and Faris through the companion stack `grc-engineer-users`, with the same group, permissions boundary, and group-attached MFA rule as the ISSE. Faris builds with that seat and keeps his admin identity for approvals.
- The ISSM approves the access template as a pull request like any other change, and Adam approves a change to the ISSM's own seat. David is kept informed as the stakeholder but is not an approver.
- No personal credentials or email addresses are stored in this repo or baked into templates. Roles are referenced by function, not by person.

The access model is defined as code in [infrastructure/cloudformation/grc-access-model.yaml](infrastructure/cloudformation/grc-access-model.yaml), plus the companion stacks; see [infrastructure/README.md](infrastructure/README.md). [shared/access-model/README.md](shared/access-model/README.md) explains what each role can and cannot do, how the template is deployed, and how it is validated.

## Future ideas

Not current state. These are directions the project could grow into later, written down so the intent is captured and nobody treats them as already in place. None of this is built, and none of it is required to finish the portfolio.

### Single sign-on with Okta

Today access is per-tool: each person signs in to AWS, GitHub, and Jira separately. A future version could put an identity provider in front of everything so one login governs them all, which is how a real regulated program runs identity.

- Okta as the identity provider, with every tool (AWS, GitHub, Jira, Google Workspace, Slack) eventually connected through SAML or OIDC single sign-on. Only the sign-in launch point is designed today, in project 14, and it does not use single sign-on.
- Joiners, movers, and leavers handled in one place. Granting or revoking a person updates every connected tool at once, instead of touching each tool by hand.
- Group-based access that maps to the roles already defined above (ISSM, ISSE, auditor, analyst), so least privilege is enforced by group membership rather than per-tool settings.
- Multi-factor authentication enforced centrally, which gives 08 Access Reviews a single authoritative source to review against.

The launch point is designed as [14 Identity and Access (Okta)](engineering/Abdifatah-14-Identity-Access/README.md), a Phase 1 build on Okta's free plan: people sign in to Okta with MFA, the Okta Browser Plugin fills the sign-in for the AWS console (the access model's IAM users), GitHub, and Jira while each tool keeps its own MFA, and two flows handle joiners and leavers. Not using single sign-on is recorded as a deviation. Full single sign-on across AWS, GitHub, Jira, Google Workspace, and Slack stays a future idea. It is gated on a shared domain and paid tiers (GitHub Enterprise Cloud, Atlassian Guard), and would be weighed against the 10 dollar cost ceiling before anyone builds it.

### Enterprise tool stack

The longer-term picture is a connected toolset rather than separate accounts, each playing the part it would in a real program:

- AWS: the environment under governance.
- Okta: sign-in launch point for AWS, GitHub, and Jira (designed in 14), single sign-on across every tool later.
- Google Workspace: documents, mail, and shared drives.
- GitHub: infrastructure as code and change control.
- Slack: team communication and alert routing.
- Jira: project and work tracking, and partner dashboards (in use today).
- Continuous monitoring: AWS-native today (project 15); a dedicated log platform later, only if it fits the cost ceiling.

The value is the connections between them: Okta fronting access, GitHub driving change, Jira tracking the work, and continuous monitoring watching the environment. Each piece is adopted only when it earns its place and fits the cost ceiling.

## Timeline

This is a 3-month engagement, about 2026-10-19 to 2027-01-18. The five 7-day phases run 2026-10-19 to 2026-11-22, which leaves an integration week (Nov 23 to 25) before Thanksgiving (2026-11-26) for the end-to-end system check and final reports. Side projects and stretch work run December 2026 to January 2027. The system keeps running through the side projects until the end-of-program teardown, Jan 11 to 18, 2027, which finishes by 2027-01-18. Put a project on your resume only after you complete your section, and follow the resume rule in the root [README](README.md#how-we-work). The more sections you complete, the more experience you earn.
