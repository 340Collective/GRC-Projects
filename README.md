# GRC Projects

A small team builds a working governance, risk, and compliance (GRC) program on AWS, from scratch, as code.

Start here, then see the Contributing, Code of conduct, and Security tabs. Roles and approvals are in [GOVERNANCE.md](GOVERNANCE.md).

![GRC platform overview: how projects 01 to 15 hand records to each other as one platform](engineering/Faris-00-Platform-Overview/diagram/grc-platform-overview.png)

The map above shows how projects 01 to 15 hand records to each other (target design, not yet deployed), including 15 AWS continuous monitoring, which routes findings to Jira and email ([15 AWS ConMon](engineering/Rasheed-15-AWS-ConMon/README.md)). Details and sources are in [00 Platform Overview](engineering/Faris-00-Platform-Overview/README.md).

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

## 5. Project map

| # | Project | Engineer (builds) | Partner (requirements and acceptance) | Phase |
| --- | --- | --- | --- | --- |
| 00 | Platform Overview | [Faris](engineering/Faris-00-Platform-Overview/README.md) | [Faris, Adam accepts](non-engineering/Faris-00-Platform-Overview/README.md) | Every phase (docs) |
| 01 | GRC-as-Code Platform and the shared foundation | [Faris](engineering/Faris-01-GRC-as-Code-Platform/README.md) | [Jason](non-engineering/Jason-01-GRC-as-Code-Platform/README.md) | Foundation 1, 01 2 |
| 02 | Third-Party and Vendor Risk Management | [Maria](engineering/Maria-02-TPRM-VRM/README.md) | [Jason](non-engineering/Jason-02-TPRM-VRM/README.md) | 4 |
| 03 | Privacy Operations | [Maria](engineering/Maria-03-Privacy/README.md) | [Jason](non-engineering/Jason-03-Privacy/README.md) | 3 |
| 04 | Gap Analysis (Rasheed builds the monthly scoring run) | [Rasheed](engineering/Rasheed-04-Gap-Analysis/README.md) | [Jason, lead](non-engineering/Jason-04-Gap-Analysis/README.md) | 3 |
| 05 | Policy Management | [Maria](engineering/Maria-05-Policy-Management/README.md) | [Adam](non-engineering/Adam-05-Policy-Management/README.md) | 5 |
| 06 | Audit Evidence Automation | [Maria](engineering/Maria-06-Evidence-Automation/README.md) | [Adam](non-engineering/Adam-06-Evidence-Automation/README.md) | 1 |
| 07 | Risk Register | [Rasheed](engineering/Rasheed-07-Risk-Register/README.md) | [Adam](non-engineering/Adam-07-Risk-Register/README.md) | 1 |
| 08 | User Access Reviews | [Abdifatah](engineering/Abdifatah-08-Access-Reviews/README.md) | [Adam](non-engineering/Adam-08-Access-Reviews/README.md) | 2 |
| 09 | Control Testing and Assessment | [Rasheed](engineering/Rasheed-09-Control-Testing/README.md) | [Jason](non-engineering/Jason-09-Control-Testing/README.md) | 3 |
| 10 | Audit Engagement Manager | [Maria](engineering/Maria-10-Audit-Engagement-Manager/README.md) | [Jason](non-engineering/Jason-10-Audit-Engagement-Manager/README.md) | 2 |
| 11 | Compliance-as-Code Guardrails | [Faris](engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) | [Adam](non-engineering/Adam-11-Compliance-as-Code-Guardrails/README.md) | 3 |
| 12 | GRC Metrics and Board Reporting | [Rasheed](engineering/Rasheed-12-Metrics-Reporting/README.md) | [Adam](non-engineering/Adam-12-Metrics-Reporting/README.md) | 4 |
| 13 | BC/DR and Incident Response | [Rasheed](engineering/Rasheed-13-BCDR-IR/README.md) | [Jason](non-engineering/Jason-13-BCDR-IR/README.md) | 2 |
| 14 | Identity and Access (Okta) | [Abdifatah](engineering/Abdifatah-14-Identity-Access/README.md) | [Adam](non-engineering/Adam-14-Identity-Access/README.md) | 1 |
| 15 | AWS Continuous Monitoring (ConMon) and Notifications | [Rasheed](engineering/Rasheed-15-AWS-ConMon/README.md) | [Adam](non-engineering/Adam-15-AWS-ConMon/README.md) | 5 |

One active build per engineer at a time. A phase ends when all its builds are merged and torn down cleanly. Points, the phase queue, and code review pairs are in [engineering/README.md](engineering/README.md).

## 6. Reporting

Reporting costs 0 dollars a month day to day.

- Adam and Jason use Jira dashboards: findings, risks, reviews, remediation age, and KRIs.
- Engineers use CloudWatch dashboards for pipeline health, inside the free tier (3 dashboards of up to 50 metrics, 10 custom metrics).
- Leadership gets a monthly board pack built by project 12 and emailed through the existing SES setup.

AWS data reaches Jira three ways: the native Security Hub to Jira Cloud integration for findings, an EventBridge rule to the Jira REST API or a Jira Automation webhook for project events, and project 12's daily job posting to the "GRC Metrics" Jira issue. Details are in [shared/labs/README.md](shared/labs/README.md).
