# Governance

How this collaboration runs. This repo is a GRC engineering portfolio built by a small team, using 340 Collective's AWS account as a shared testbed. It is a learning project, not a business need. The goal is real hands-on experience that holds up on a resume, produced under the same discipline a regulated program would use.

Status: this document is the operating manual. The 16 projects (00 to 15) are target designs, not yet deployed. Each project has an engineering folder and a non-engineering folder (see the root [README](README.md)).

![GRC Projects governance: the engineering and non-engineering tracks, the review flow from build to merge, and the deviation path](shared/governance-diagram/grc-governance.png)

The diagram above shows the two tracks and how a change moves from a build through code review, partner acceptance, ISSO validation, and the ISSM decision to merge, with the deviation path when a change cannot be made. The diagram sources are in [shared/governance-diagram/](shared/governance-diagram/) as PNG and SVG, with `grc-governance_build.py` to regenerate them.

The shared control reference for every project is the [ASFF control matrix](non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx). Map findings, evidence, risks, and deviation requests to its ASFF `SecurityControlId` values so the whole program speaks one control language. Changes to the matrix follow the change process below, like any other change. It is maintained with [01 GRC-as-Code Platform](engineering/Faris-01-GRC-as-Code-Platform/README.md).

## Principles

- Build it as code. Infrastructure is created only through CloudFormation. Anything created by hand in the console is deleted.
- Keep it cheap. Total AWS spend stays under 10 dollars per month across the whole project, and 0 dollars is the target. Build, capture evidence, then tear it down.
- Nobody signs off on their own work. Separation of duties is enforced through roles, code review, Jira acceptance records, and pull request approval.
- Change is controlled. Every change is a pull request the ISSM approves (Adam approves Faris-built work). If a needed change cannot be made, it goes through a deviation request.
- Do not make an expensive mess. Check service quotas and limits before building. If a service is not free, confirm the cost before enabling it.

## Roles

| Person | Role | Track | Responsibility |
| --- | --- | --- | --- |
| David | Business Owner / Stakeholder | Outside both tracks | Owns 340 Collective and its AWS account. Faris reports to David. David is informed only: he does not approve pull requests or changes. |
| Faris | ISSM / Architect (Program Lead) | Engineering, and 00 on the non-engineering side | Owns governance and gives final approval on every pull request and access change, except his own builds. Also builds: the shared foundation (Phase 1), 01 (Phase 2), and the 00 overview (every phase). Accepts every partner's Handoff 1 requirements. |
| Rasheed | ISSE / Engineer | Engineering | Builds 07, 13, 12, and 15. Reviews code for Maria, Alex, and Abdifatah. Named backup on the critical-path foundation. |
| Maria | Automation Engineer | Engineering | Builds 06, 10, 02, and 05. Reviews code for Alex and Rasheed. |
| Alex | Security Automation Engineer | Engineering | Builds 11, 03, 09, and the 04 monthly scoring run. Reviews code for Maria and Rasheed, and for 15. Background in vulnerability management, CIS hardening, SIEM and IR playbooks, and Python detection automation. |
| Abdifatah | IAM / Identity Engineer | Engineering | Builds 14 and 08. Adds review capacity in Phase 3. |
| Adam | ISSO / Analyst | Non-engineering | Partner for 05, 06, 07, 08, 11, 12, 14, and 15: writes requirements, accepts the build, operates it, and reports. Validates all engineer work. Accepts and gives final approval on Faris-built work (foundation, 01, 00). Works in Jira. |
| Jason | Internal Auditor / Assessor | Non-engineering | Partner for 01, 02, 03, 04 (lead), 09, 10, and 13: writes requirements and runs the acceptance test, recorded as a pass or findings record, not an approval. Assesses independently once per phase. Builds nothing and never approves. Works in Jira. |

"Independent" in the Internal Auditor's role means independent from the work under review, not from the organization. His AWS access is the access model's read-only `GRC-Auditor` group (MFA required). He cannot change that access, and every change to it is an ISSM-approved pull request. His findings are internal assessment, not independent attestation.

## Two-track model

Every project has two folders with the same number: one in `engineering/` for the person who builds it, and one in `non-engineering/` for the partner who sets requirements, accepts the build, and operates it. Both folders carry the same numbered handoffs. Each handoff is a Jira Task created by the person who sends it, linked to the project's Jira epic (`GRC-<NN>`, a placeholder until Faris creates it). Adam and Jason work in Jira and do not open or review pull requests; engineers or Faris keep the non-engineering folders current.

| # | Project | Engineer (builds) | Partner | Phase | Points |
| --- | --- | --- | --- | --- | --- |
| 00 | Platform Overview | Faris | Faris; Adam accepts | Every phase (docs) | none |
| 01 | GRC-as-Code Platform, plus the shared foundation | Faris | Jason | Foundation 1, 01 2 | 3 + 2 |
| 02 | TPRM/VRM | Maria | Jason | 3 | 2 |
| 03 | Privacy | Alex | Jason | 2 | 2 |
| 04 | Gap Analysis | Alex (monthly scoring run only) | Jason (lead) | 3 | 1 |
| 05 | Policy Management | Maria | Adam | 4 | 1 |
| 06 | Evidence Automation | Maria | Adam | 1 | 3 |
| 07 | Risk Register | Rasheed | Adam | 1 | 2 |
| 08 | Access Reviews | Abdifatah | Adam | 2 | 2 |
| 09 | Control Testing | Alex | Jason | 3 | 2 |
| 10 | Audit Engagement Manager | Maria | Jason | 2 | 2 |
| 11 | Compliance-as-Code Guardrails | Alex | Adam | 1 | 3 |
| 12 | Metrics and Reporting | Rasheed | Adam | 3 (needs data from 06, 11, and 07) | 2 |
| 13 | BC/DR and IR | Rasheed | Jason | 2 | 2 |
| 14 | Identity and Access (Okta) | Abdifatah | Adam | 1 | 2 |
| 15 | AWS Continuous Monitoring (ConMon) and Notifications | Rasheed | Adam | 4 | 2 |

### Points

Size sets the points: S = 1, M = 2, L = 3. Totals: Faris 5, Rasheed 8, Maria 8, Alex 7 plus 1 for the 04 scoring run, Abdifatah 4. The 00 overview is documentation and carries no points.

### Phases

One active build per engineer at a time. A phase ends when all its builds are merged and torn down cleanly.

| Phase | Faris | Rasheed | Maria | Alex | Abdifatah |
| --- | --- | --- | --- | --- | --- |
| 1 | Foundation | 07 | 06 | 11 | 14 |
| 2 | 01 | 13 | 10 | 03 | 08 |
| 3 | Review | 12 | 02 | 09 and the 04 scoring run | Review |
| 4 | Review | 15 | 05 | Review | Review |

15 is in Phase 4 because it posts its monthly KPIs to the GRC Metrics Jira issue that 12 builds in Phase 3, and needs findings from 01 and 11. That keeps Rasheed to one active build at a time. Faris updates the 00 overview at the end of every phase.

### Handoffs

Each project's paired LAB-STEPS files list the same handoffs. The usual shape:

1. Handoff 1: the partner's requirements (control list, rules, test plan, or scenario), partner to engineer. Faris accepts them; Adam accepts Faris's.
2. Handoff 2: the build, ready for acceptance, engineer to partner.
3. Handoff 3: the partner's accepted output (report, register, scorecard, or signed worksheet), partner to Faris.

01 adds a fourth (Jason's SOC 2 coverage assessment to Faris and Adam), and 00 runs every phase (each engineer's phase build list to Faris, then the updated overview to Adam).

## Separation of duties

The rule is that no one validates or approves their own work, and nobody validates their own requirements. The review flow for every build:

1. Requirements: the partner writes Handoff 1 in Jira. Faris (ISSM) accepts it. Adam accepts the requirements Faris writes (00, the foundation, 01).
2. Build: the engineer builds in a branch. Templates live in the private website repo and move `dev` to `test` to `main` there.
3. Code review: another engineer reviews in GitHub. Rasheed reviews Maria, Alex, and Abdifatah. Maria and Alex review each other and Rasheed; Alex reviews 15. Rasheed or Alex reviews Faris. Faris and Abdifatah add review capacity in Phase 3.
4. Partner acceptance: the partner accepts the build in Jira (Handoff 2). On Jason's projects (02, 03, 04, 09, 10, 13) his acceptance is an acceptance test result (pass or findings), not an approval.
5. Validation: Adam (ISSO) validates engineer work in Jira.
6. Final approval: Faris (ISSM) approves or denies. For Faris-built work (foundation, 01, 00), Adam accepts and gives final approval instead.
7. Assessment: Jason assesses independently once per phase, in Jira, never per pull request. He builds nothing and never approves.
8. Merge: a pull request in this repo links its Jira Task and merges only after the Task shows the partner's acceptance.

Adam is both partner and validator on his own projects. That is accepted because he did not build them; the build was the engineer's, and Faris still gives final approval.

Jason is both partner and assessor on 01, 02, 03, 04 (lead), 09, 10, and 13, where he writes the Handoff 1 requirements and runs the acceptance test. That is accepted because his acceptance is a pass or findings record and never an approval, and he builds nothing. His phase assessment of those projects is recorded in Jira as partner-assessed, so a reader knows he also set the requirements. Faris (or Adam for 01) still gives final approval. Owner decision, 2026-10-17.

### RACI

Engineer builds. Code review is in GitHub. Partner writes requirements and accepts the build in Jira. Validates is the ISSO's check. Final approval merges or denies. Assesses is Jason's independent phase assessment. Informed is kept up to date.

| Project | Engineer (builds) | Code review | Partner (requirements and acceptance) | Validates | Final approval | Assesses | Informed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 Platform Overview | Faris | Rasheed or Alex | Faris; Adam accepts | Adam | Adam | Jason | David |
| Shared foundation | Faris | Rasheed or Alex | Adam | Adam | Adam | Jason | David |
| 01 GRC-as-Code Platform | Faris | Rasheed or Alex | Jason (acceptance test and coverage assessment); Adam accepts | Adam | Adam | Jason (also partner; see note) | David |
| 02 TPRM/VRM | Maria | Rasheed or Alex | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 03 Privacy | Alex | Rasheed or Maria | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 04 Gap Analysis | Alex (scoring run) | Rasheed or Maria | Jason (lead, acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 05 Policy Management | Maria | Rasheed or Alex | Adam | Adam | Faris | Jason | David |
| 06 Evidence Automation | Maria | Rasheed or Alex | Adam | Adam | Faris | Jason | David |
| 07 Risk Register | Rasheed | Maria or Alex | Adam | Adam | Faris | Jason | David |
| 08 Access Reviews | Abdifatah | Rasheed | Adam | Adam | Faris | Jason | David |
| 09 Control Testing | Alex | Rasheed or Maria | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 10 Audit Engagement Manager | Maria | Rasheed or Alex | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 11 Guardrails | Alex | Rasheed or Maria | Adam | Adam | Faris | Jason | David |
| 12 Metrics and Reporting | Rasheed | Maria or Alex | Adam | Adam | Faris | Jason | David |
| 13 BC/DR and IR | Rasheed | Maria or Alex | Jason (acceptance test) | Adam | Faris | Jason (also partner; see note) | David |
| 14 Identity and Access (Okta) | Abdifatah | Rasheed | Adam | Adam | Faris | Jason | David |
| 15 AWS ConMon | Rasheed | Alex | Adam | Adam | Faris | Jason | David |
| Access-model changes (`grc-access-model`), except the auditor seat | Faris, in the website repo | Rasheed | none | Adam | Faris | Jason (internal audit review) | David |
| Engineer seat changes (`grc-engineer-users`) | Faris, in the website repo | Rasheed | none | Adam | Faris; Adam for a change to the `faris` seat itself | Jason (internal audit review) | David |
| Auditor-seat changes (`GRC-Auditor`, `internal-auditor-*`) | Faris, in the website repo | Rasheed | none | Adam | Faris | none (Jason never reviews his own access) | Jason, David |

Jason never reviews a change to his own access. Faris never gives final approval on his own build or his own seat; Adam does.

## Change process

Modeled on a FedRAMP-style change workflow.

1. Open a change by creating a branch and a pull request against `main`. Describe what changes, why, the expected cost impact, and the linked Jira Task.
2. Another engineer reviews the code. The partner accepts in Jira, and Adam validates.
3. Faris approves or denies (Adam for Faris-built work). Approval merges; denial returns it with comments.
4. If a change is needed but cannot be made (a quota block, a cost ceiling, a missing dependency), file a deviation request instead of forcing the change.

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
- Build, capture evidence with screenshots, then deprecate. Tearing the stack down after evidence is captured is a required step, not optional.
- Check service quotas and limits before building anything.

Services that can break the budget if left running. Confirm cost before enabling:

- QuickSight: not used. Standard authors run about 9 to 12 dollars per user per month, which alone can exceed the whole budget. Reporting uses Jira dashboards, CloudWatch dashboards inside the free tier, and 12's emailed board pack instead.
- Macie (03): free trial, then charges per gigabyte scanned. Keep to the trial or sample data.
- Audit Manager (06): charges per assessment. Enable only while capturing evidence, then disable.
- Config, GuardDuty, Inspector, Security Hub (01, 06, 11, 15): free tiers that expire, usually after 30 days, then charge per item. Watch the clock and tear down. Inspector is already on for EC2, Lambda, and ECR and bills per resource scanned. GuardDuty is not enabled; turning it on is an owner decision.
- Secrets Manager (the EventBridge connections to Jira in 01, 07, 13, and 15): about 0.40 dollars per secret per month. It is on the access model's budget-breaker deny list today, so it needs an access-change pull request first.
- 15 ConMon: about 0 to 1 dollar a month. AWS service events on the default bus are free, SNS email and Lambda stay in their free tiers, one CloudWatch dashboard is free, and the connection secret is about 0.40 dollars.
- Okta (14): the Integrator Free Plan is 0 dollars but is meant for development and testing. It caps at 10 active users and 5 Workflows, and the org deactivates if nobody signs in for 90 consecutive days. Single sign-on into GitHub needs GitHub Enterprise Cloud and into Jira needs Atlassian Guard, both paid per user per month, which would break the budget. 14 does not use single sign-on: the Okta Browser Plugin fills each tool's own sign-in, and each tool keeps its own MFA.

## Access to the real environment

Access to 340 Collective's AWS account is granted only after the accounts exist and only through least-privilege IAM defined in CloudFormation. Access is not granted by hand.

- Roles are defined as code, scoped to what each role needs: engineer (build and deploy `grc-*` stacks), internal auditor (read-only audit and evidence read, MFA required), analyst (read plus evidence export).
- Engineers deploy `grc-*` stacks only from the website repo's clean `main`, after ISSM approval, under its change-control rule.
- Planned, not deployed: `GRC-Engineer` seats for Maria, Alex, and Faris through the companion stack `grc-engineer-users`, with the same group, permissions boundary, and group-attached MFA rule as the ISSE. Faris builds with that seat and keeps his admin identity for approvals.
- The ISSM approves the access template as a pull request like any other change, and Adam approves a change to the ISSM's own seat. David is kept informed as the stakeholder but is not an approver.
- No personal credentials or email addresses are stored in this repo or baked into templates. Roles are referenced by function, not by person.

The access model is defined as code in the private 340collective-website repo (`cloudformation/grc-access-model.yaml`, plus the companion stacks). [shared/access-model/README.md](shared/access-model/README.md) explains what each role can and cannot do, how the template is deployed, and how it is validated.

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
- Jira: project and work tracking, acceptance records, and partner dashboards (in use today).
- Continuous monitoring: AWS-native today (project 15); a dedicated log platform later, only if it fits the cost ceiling.

The value is the connections between them: Okta fronting access, GitHub driving change, Jira tracking the work, and continuous monitoring watching the environment. Each piece is adopted only when it earns its place and fits the cost ceiling.

## Timeline

The project runs 3 to 6 months, in four phases. Put a project on your resume only after you complete your section. The more sections you complete, the more experience you earn.
