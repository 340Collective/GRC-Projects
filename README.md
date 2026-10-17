# GRC Projects

A small team builds a working governance, risk, and compliance (GRC) program on AWS, from scratch, as code.

Start here, then see the Contributing, Code of conduct, and Security tabs. Roles and approvals are in [GOVERNANCE.md](GOVERNANCE.md).

## Team and roles

| Person | Role | Track | What they do |
| --- | --- | --- | --- |
| Faris | ISSM / Program Lead | Engineering | Runs the program and gives final approval on every pull request. Builds the shared foundation, 01, 11, and the 00 overview. Deploys the shared `infrastructure/` stacks. |
| Rasheed | ISSE / Engineer | Engineering | Builds 13, 07, 09 (with the 04 scoring run), 12, and 15. Reviews code for Faris, Maria, and Abdifatah. Backup on the foundation. |
| Maria | Automation Engineer | Engineering | Builds 06, 10, 03, 02, and 05. Reviews code for Rasheed and Abdifatah. |
| Abdifatah | IAM / Identity Engineer | Engineering | Builds 14 and 08. Reviews code from Phase 3. |
| Adam | ISSO / Analyst | Non-engineering | Partner on 05, 06, 07, 08, 11, 12, 14, 15: writes requirements, accepts the build, runs it, and reports. Validates engineer work and approves Faris's builds. Works in Jira. |
| Jason | Internal Auditor | Non-engineering | Partner on 01, 02, 03, 04 (lead), 09, 10, 13: writes requirements and runs the acceptance test. Assesses each phase independently. Builds nothing and never approves. Works in Jira. |
| David | Business Owner | Outside both tracks | Owns 340 Collective and its AWS account. Kept informed; does not approve changes. |

Nobody approves their own work: an engineer builds, another engineer reviews the code, the partner accepts, Adam validates, Jason assesses, and Faris approves (Adam approves Faris's builds).

## Timeline

Prep weekend Oct 17 to 18. Official start Monday Oct 19, 2026. Each build is 7 days, one at a time per person. Core work finishes before Thanksgiving (Nov 26). Side projects run Dec 2026 to Jan 2027.

| Phase | Dates (2026) | Faris | Rasheed | Maria | Abdifatah | Adam (ISSO) | Jason (Internal Auditor) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Oct 19 to 25 | [Foundation](engineering/Faris-01-GRC-as-Code-Platform/README.md) | [13 BC/DR and IR](engineering/Rasheed-13-BCDR-IR/README.md) | [06 Evidence Automation](engineering/Maria-06-Evidence-Automation/README.md) | [14 Identity and Access](engineering/Abdifatah-14-Identity-Access/README.md) | Foundation, [06](non-engineering/Adam-06-Evidence-Automation/README.md), [14](non-engineering/Adam-14-Identity-Access/README.md) | [13](non-engineering/Jason-13-BCDR-IR/README.md) |
| P2 | Oct 26 to Nov 1 | [01 GRC-as-Code Platform](engineering/Faris-01-GRC-as-Code-Platform/README.md) | [07 Risk Register](engineering/Rasheed-07-Risk-Register/README.md) | [10 Audit Engagement Manager](engineering/Maria-10-Audit-Engagement-Manager/README.md) | [08 Access Reviews](engineering/Abdifatah-08-Access-Reviews/README.md) | [07](non-engineering/Adam-07-Risk-Register/README.md), [08](non-engineering/Adam-08-Access-Reviews/README.md) | [01](non-engineering/Jason-01-GRC-as-Code-Platform/README.md), [10](non-engineering/Jason-10-Audit-Engagement-Manager/README.md); assesses P1 |
| P3 | Nov 2 to 8 | [11 Guardrails](engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) | [09 Control Testing](engineering/Rasheed-09-Control-Testing/README.md) and the [04 scoring run](engineering/Rasheed-04-Gap-Analysis/README.md) | [03 Privacy](engineering/Maria-03-Privacy/README.md) | review | [11](non-engineering/Adam-11-Compliance-as-Code-Guardrails/README.md) | [03](non-engineering/Jason-03-Privacy/README.md), [04 (lead)](non-engineering/Jason-04-Gap-Analysis/README.md), [09](non-engineering/Jason-09-Control-Testing/README.md); assesses P2 |
| P4 | Nov 9 to 15 | review | [12 Metrics and Reporting](engineering/Rasheed-12-Metrics-Reporting/README.md) | [02 TPRM/VRM](engineering/Maria-02-TPRM-VRM/README.md) | review | [12](non-engineering/Adam-12-Metrics-Reporting/README.md) | [02](non-engineering/Jason-02-TPRM-VRM/README.md); assesses P3 |
| P5 | Nov 16 to 22 | review | [15 AWS ConMon](engineering/Rasheed-15-AWS-ConMon/README.md) | [05 Policy Management](engineering/Maria-05-Policy-Management/README.md) | review | [05](non-engineering/Adam-05-Policy-Management/README.md), [15](non-engineering/Adam-15-AWS-ConMon/README.md) | assesses P4 |
| Buffer | Nov 23 to 25 | final reports | final reports | final reports | final reports | final reports | assesses P5; final reports |

Adam and Jason partner on the projects listed in their columns (requirements, acceptance, operation). Jason also assesses the previous phase.

Day rhythm: Day 1 requirements handoff, Days 2 to 5 build and review, Day 6 acceptance, Day 7 merge, final report, teardown.

## Project map

Projects grouped by build week. Phases and dates match the Timeline above and [GOVERNANCE.md](GOVERNANCE.md#phases).

### Phase 1 (Oct 19 to 25)

| Project | Engineer | Partner | Jira epic |
| --- | --- | --- | --- |
| [Shared foundation (part of 01)](engineering/Faris-01-GRC-as-Code-Platform/README.md) | [Faris](engineering/Faris-01-GRC-as-Code-Platform/README.md) | Adam accepts | `GRC-<NN>` |
| [06 Audit Evidence Automation](engineering/Maria-06-Evidence-Automation/README.md) | [Maria](engineering/Maria-06-Evidence-Automation/README.md) | [Adam](non-engineering/Adam-06-Evidence-Automation/README.md) | `GRC-<NN>` |
| [13 BC/DR and Incident Response](engineering/Rasheed-13-BCDR-IR/README.md) | [Rasheed](engineering/Rasheed-13-BCDR-IR/README.md) | [Jason](non-engineering/Jason-13-BCDR-IR/README.md) | `GRC-<NN>` |
| [14 Identity and Access (Okta)](engineering/Abdifatah-14-Identity-Access/README.md) | [Abdifatah](engineering/Abdifatah-14-Identity-Access/README.md) | [Adam](non-engineering/Adam-14-Identity-Access/README.md) | `GRC-<NN>` |

### Phase 2 (Oct 26 to Nov 1)

| Project | Engineer | Partner | Jira epic |
| --- | --- | --- | --- |
| [01 GRC-as-Code Platform](engineering/Faris-01-GRC-as-Code-Platform/README.md) | [Faris](engineering/Faris-01-GRC-as-Code-Platform/README.md) | [Jason](non-engineering/Jason-01-GRC-as-Code-Platform/README.md) | `GRC-<NN>` |
| [07 Risk Register](engineering/Rasheed-07-Risk-Register/README.md) | [Rasheed](engineering/Rasheed-07-Risk-Register/README.md) | [Adam](non-engineering/Adam-07-Risk-Register/README.md) | `GRC-<NN>` |
| [08 User Access Reviews](engineering/Abdifatah-08-Access-Reviews/README.md) | [Abdifatah](engineering/Abdifatah-08-Access-Reviews/README.md) | [Adam](non-engineering/Adam-08-Access-Reviews/README.md) | `GRC-<NN>` |
| [10 Audit Engagement Manager](engineering/Maria-10-Audit-Engagement-Manager/README.md) | [Maria](engineering/Maria-10-Audit-Engagement-Manager/README.md) | [Jason](non-engineering/Jason-10-Audit-Engagement-Manager/README.md) | `GRC-<NN>` |

### Phase 3 (Nov 2 to 8)

| Project | Engineer | Partner | Jira epic |
| --- | --- | --- | --- |
| [03 Privacy Operations](engineering/Maria-03-Privacy/README.md) | [Maria](engineering/Maria-03-Privacy/README.md) | [Jason](non-engineering/Jason-03-Privacy/README.md) | `GRC-<NN>` |
| [09 Control Testing and Assessment](engineering/Rasheed-09-Control-Testing/README.md) | [Rasheed](engineering/Rasheed-09-Control-Testing/README.md) | [Jason](non-engineering/Jason-09-Control-Testing/README.md) | `GRC-<NN>` |
| [11 Compliance-as-Code Guardrails](engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) | [Faris](engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) | [Adam](non-engineering/Adam-11-Compliance-as-Code-Guardrails/README.md) | `GRC-<NN>` |

### Phase 4 (Nov 9 to 15)

| Project | Engineer | Partner | Jira epic |
| --- | --- | --- | --- |
| [02 Third-Party and Vendor Risk Management](engineering/Maria-02-TPRM-VRM/README.md) | [Maria](engineering/Maria-02-TPRM-VRM/README.md) | [Jason](non-engineering/Jason-02-TPRM-VRM/README.md) | `GRC-<NN>` |
| [12 GRC Metrics and Board Reporting](engineering/Rasheed-12-Metrics-Reporting/README.md) | [Rasheed](engineering/Rasheed-12-Metrics-Reporting/README.md) | [Adam](non-engineering/Adam-12-Metrics-Reporting/README.md) | `GRC-<NN>` |

### Phase 5 (Nov 16 to 22)

| Project | Engineer | Partner | Jira epic |
| --- | --- | --- | --- |
| [05 Policy Management](engineering/Maria-05-Policy-Management/README.md) | [Maria](engineering/Maria-05-Policy-Management/README.md) | [Adam](non-engineering/Adam-05-Policy-Management/README.md) | `GRC-<NN>` |
| [15 AWS Continuous Monitoring (ConMon) and Notifications](engineering/Rasheed-15-AWS-ConMon/README.md) | [Rasheed](engineering/Rasheed-15-AWS-ConMon/README.md) | [Adam](non-engineering/Adam-15-AWS-ConMon/README.md) | `GRC-<NN>` |

### No build week

| Project | Engineer | Partner | Jira epic |
| --- | --- | --- | --- |
| [00 Platform Overview](engineering/Faris-00-Platform-Overview/README.md) (docs, updated every phase) | [Faris](engineering/Faris-00-Platform-Overview/README.md) | [Faris, Adam accepts](non-engineering/Faris-00-Platform-Overview/README.md) | `GRC-<NN>` |
| [04 Gap Analysis](engineering/Rasheed-04-Gap-Analysis/README.md) (Jason leads; Rasheed's scoring run is in Phase 3) | [Rasheed](engineering/Rasheed-04-Gap-Analysis/README.md) | [Jason, lead](non-engineering/Jason-04-Gap-Analysis/README.md) | `GRC-<NN>` |

One active build per engineer at a time, time-boxed to 7 days ([7-day build rule](GOVERNANCE.md#7-day-build-rule)). A phase ends when all its builds are merged and torn down cleanly. Points, the phase queue, and code review pairs are in [engineering/README.md](engineering/README.md).

![GRC platform overview: how projects 01 to 15 hand records to each other as one platform](engineering/Faris-00-Platform-Overview/diagram/grc-platform-overview.png)

The map above shows how projects 01 to 15 hand records to each other (target design, not yet deployed), including 15 AWS continuous monitoring, which routes findings to Jira and email ([15 AWS ConMon](engineering/Rasheed-15-AWS-ConMon/README.md)). Details and sources are in [00 Platform Overview](engineering/Faris-00-Platform-Overview/README.md).

## How we work

Where things go:

- Jira: phases, timelines, assignments, handoffs, day-to-day comments, blockers, and acceptance sign-off.
- GitHub: code, templates, architecture, diagrams, lab steps, and the final report ([shared/templates/FINAL-REPORT.md](shared/templates/FINAL-REPORT.md)).
- LinkedIn messages or group chat: general communication, quick pings, and high-level updates. No account details, findings, evidence, or credentials there.

Jira holds the handoff comment and status; the handoff document lives in GitHub, and the Jira ticket links to it. See [Where work lives](GOVERNANCE.md#where-work-lives).

Rules:

- AI tools are allowed. Follow the SSDLC in [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md), work on a branch in your own copy of the repo, and never merge without another person's review.
- Only change files in your own project folders: `engineering/<You>-NN-...` or `non-engineering/<You>-NN-...`. Shared files (root docs, `shared/`, `infrastructure/`) change only through Faris. [CODEOWNERS](.github/CODEOWNERS) sets who reviews.

Timeline (dates and who builds what are in [Timeline](#timeline)):

- This weekend (Oct 17 and 18) is prep: read the repo, learn the basic git commands below, and set up your AI tool by the [AGENTS.md](AGENTS.md) rules if you use one.
- Monday 2026-10-19 is the official start. 7 days per project per person, one build at a time ([7-day build rule](GOVERNANCE.md#7-day-build-rule)).
- This is a 3-month engagement (about 2026-10-19 to 2027-01-18).

Getting started this weekend:

```bash
git clone https://github.com/340Collective/GRC-Projects.git # get your own copy
git switch -c docs/07-risk-notes                             # make a branch
git add engineering/<You>-NN-<Project>/README.md             # stage a file by name
git commit -s -m "docs(07): add risk notes"                  # commit with sign-off
git push -u origin docs/07-risk-notes                        # push the branch
gh pr create --base main                                     # open a pull request (or use the GitHub website)
```

Resume use: you may describe your own projects on a resume or LinkedIn as project work or work experience. Use the before-and-after metrics from your FINAL-REPORT. Never share account IDs, ARNs, internal URLs, evidence, or real client data. Describe roles and outcomes.

## 1. Purpose

A small team builds a working GRC program on AWS from scratch: policy, risk, evidence, guardrails, access reviews, audit, continuous monitoring, and reporting. Each of the 16 projects (00 to 15) automates one moving part, and together they run as one connected platform. 340 Collective's AWS account is the live testbed, so every design is checked against real infrastructure, real vendors, and real policies.

## 2. Why we are doing this

- Real controls, not slides. SOC 2, NIST 800-53, and ISO 27001 controls are turned into working automation, with evidence that shows each control operating.
- Real separation of duties. Engineers build, another engineer reviews the code, the partner accepts, the ISSO validates, the Internal Auditor assesses independently, and the ISSM approves. Nobody signs off on their own work.
- One connected platform. The 16 projects feed each other: findings land in one hub, evidence and risks collect in shared stores, and metrics read all of them.
- A learning project, not a business need. It stays under 10 dollars a month. Every build is temporary: no Object Lock, no permanent data, and every lab tears down when its phase ends.

## 3. Outcomes

- For each person: a finished project you built or ran yourself, with a design, a deployed and tested build or an accepted deliverable, handoff records, and teardown evidence you can talk through in an interview.
- For the team: practice in a regulated-style workflow across two tracks, with requirements, code review, acceptance, validation, assessment, approval, and deviation requests all on record in GitHub and Jira.
- For the account: a documented, least-privilege access model, guardrails and continuous monitoring designed for it, and a clean account after every phase, with spend under the cap.

## 4. How it is organized

| Folder | Who works there | What is inside |
| --- | --- | --- |
| [engineering/](engineering/README.md) | Faris, Rasheed, Maria, Abdifatah | One folder per project, named `<Engineer>-<NN>-<Project>`: README, architecture doc, diagram, and the engineering LAB-STEPS (design, deploy, test, hand off, tear down) |
| [non-engineering/](non-engineering/README.md) | Adam (ISSO), Jason (Internal Auditor), Faris for 00 | The same 16 projects, named `<Partner>-<NN>-<Project>`: README and the non-engineering LAB-STEPS (requirements, inputs, acceptance, operation, reporting), plus working spreadsheets |
| [shared/](shared/labs/README.md) | Everyone | The general lab guide (`shared/labs/`), the [access model](shared/access-model/README.md), the [governance diagram](shared/governance-diagram/grc-governance.png), and `check_links.py` |
| [infrastructure/](infrastructure/README.md) | Engineers author; the ISSM deploys the shared stacks, engineers their own project stacks | The GRC CloudFormation templates, the access-model policy validator, the evidence bucket init script, and the GRC change records (runbooks) |

Find your own folder by your first name. Both folders of a project carry the same numbered handoffs, so each side can see what it owes the other. GRC templates live in `infrastructure/` and deploy only from this repo's clean `main`: the ISSM deploys the shared stacks, and each engineer deploys, tags, and tears down their own project stack. Nothing deploys from a branch.

Work is tracked in Jira on the GRC board (340collective.atlassian.net, project key `GRC`). Each project has one Jira epic (`GRC-<NN>` is a placeholder until Faris creates it), and each numbered handoff is a linked Jira Task. Reference a work item key in a commit or pull request to link it to the board. Adam and Jason work in Jira, not in pull requests.

The program's control matrix is the [ASFF control matrix](non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx): about 1,530 controls from SCF v2026.2, each with an ASFF `SecurityControlId` and mapped to frameworks including SOC 2 and ISO 27002. Findings, evidence, risks, and deviations from every project trace back to these IDs. It opens in Excel, Numbers, or Google Sheets, and it is maintained with [01 GRC-as-Code Platform](engineering/Faris-01-GRC-as-Code-Platform/README.md).

## 5. Reporting

Reporting costs 0 dollars a month day to day.

- Adam and Jason use Jira dashboards: findings, risks, reviews, remediation age, and KRIs.
- Engineers use CloudWatch dashboards for pipeline health, inside the free tier (3 dashboards of up to 50 metrics, 10 custom metrics).
- Leadership gets a monthly board pack built by project 12 and emailed through the existing SES setup.

AWS data reaches Jira three ways: the native Security Hub to Jira Cloud integration for findings, an EventBridge rule to the Jira REST API or a Jira Automation webhook for project events, and project 12's daily job posting to the "GRC Metrics" Jira issue. Details are in [shared/labs/README.md](shared/labs/README.md).
