# Non-engineering track

Partners write requirements, hand over inputs, accept builds, operate what was built, and report. Adam and Jason work in Jira: requirements, acceptance, handoffs, and assessments are Jira records, and neither opens or reviews pull requests. These folders stay in GitHub as reference, and the engineers or Faris keep them current.

Each folder is named `<Partner>-<NN>-<Project>`, so find your own folder by your first name. Every folder has a README with your header block and a LAB-STEPS.md with the non-engineering steps. The general lab guide is [shared/labs/README.md](../shared/labs/README.md).

## Team

| Person | Role | Owns | Works with |
| --- | --- | --- | --- |
| Adam | ISSO | Requirements, acceptance, and validation for 05, 06, 07, 08, 11, 12, 14, and 15; validates all engineer work; accepts and gives final approval on Faris-built work (foundation, 01, 11, 00) | Maria (05, 06), Rasheed (07, 12, 15), Abdifatah (08, 14), Faris (11) |
| Jason | Internal Auditor | Requirements and acceptance tests for 01 (coverage assessment), 02, 03, 04 (lead), 09, 10, and 13; one independent assessment per phase | Faris (01), Maria (02, 03, 10), Rasheed (04, 09, 13) |
| Faris | ISSM | 00 phase tracking; accepts every partner's Handoff 1 requirements; final approval | Each engineer (00) |
| David | Business Owner / Stakeholder | Informed only | |

## Rules

- Jason builds nothing and never approves. His acceptance test is a pass or findings record, and his phase assessment is independent of any single pull request.
- Faris accepts every partner's Handoff 1 requirements; Adam accepts Faris's. Nobody validates their own requirements or build.
- One Jira epic per project (the key is in each project page header and in the README project map). Each numbered handoff is a Jira Task created by the person who sends it.

## Folders

| # | Partner folder | Engineer folder | Engineer |
| --- | --- | --- | --- |
| 00 | [Faris-00-Platform-Overview](Faris-00-Platform-Overview/README.md) | [Faris-00-Platform-Overview](../engineering/Faris-00-Platform-Overview/README.md) | Faris |
| 01 | [Jason-01-GRC-as-Code-Platform](Jason-01-GRC-as-Code-Platform/README.md) | [Faris-01-GRC-as-Code-Platform](../engineering/Faris-01-GRC-as-Code-Platform/README.md) | Faris |
| 02 | [Jason-02-TPRM-VRM](Jason-02-TPRM-VRM/README.md) | [Maria-02-TPRM-VRM](../engineering/Maria-02-TPRM-VRM/README.md) | Maria |
| 03 | [Jason-03-Privacy](Jason-03-Privacy/README.md) | [Maria-03-Privacy](../engineering/Maria-03-Privacy/README.md) | Maria |
| 04 | [Jason-04-Gap-Analysis](Jason-04-Gap-Analysis/README.md) | [Rasheed-04-Gap-Analysis](../engineering/Rasheed-04-Gap-Analysis/README.md) | Rasheed (scoring run only) |
| 05 | [Adam-05-Policy-Management](Adam-05-Policy-Management/README.md) | [Maria-05-Policy-Management](../engineering/Maria-05-Policy-Management/README.md) | Maria |
| 06 | [Adam-06-Evidence-Automation](Adam-06-Evidence-Automation/README.md) | [Maria-06-Evidence-Automation](../engineering/Maria-06-Evidence-Automation/README.md) | Maria |
| 07 | [Adam-07-Risk-Register](Adam-07-Risk-Register/README.md) | [Rasheed-07-Risk-Register](../engineering/Rasheed-07-Risk-Register/README.md) | Rasheed |
| 08 | [Adam-08-Access-Reviews](Adam-08-Access-Reviews/README.md) | [Abdifatah-08-Access-Reviews](../engineering/Abdifatah-08-Access-Reviews/README.md) | Abdifatah |
| 09 | [Jason-09-Control-Testing](Jason-09-Control-Testing/README.md) | [Rasheed-09-Control-Testing](../engineering/Rasheed-09-Control-Testing/README.md) | Rasheed |
| 10 | [Jason-10-Audit-Engagement-Manager](Jason-10-Audit-Engagement-Manager/README.md) | [Maria-10-Audit-Engagement-Manager](../engineering/Maria-10-Audit-Engagement-Manager/README.md) | Maria |
| 11 | [Adam-11-Compliance-as-Code-Guardrails](Adam-11-Compliance-as-Code-Guardrails/README.md) | [Faris-11-Compliance-as-Code-Guardrails](../engineering/Faris-11-Compliance-as-Code-Guardrails/README.md) | Faris |
| 12 | [Adam-12-Metrics-Reporting](Adam-12-Metrics-Reporting/README.md) | [Rasheed-12-Metrics-Reporting](../engineering/Rasheed-12-Metrics-Reporting/README.md) | Rasheed |
| 13 | [Jason-13-BCDR-IR](Jason-13-BCDR-IR/README.md) | [Rasheed-13-BCDR-IR](../engineering/Rasheed-13-BCDR-IR/README.md) | Rasheed |
| 14 | [Adam-14-Identity-Access](Adam-14-Identity-Access/README.md) | [Abdifatah-14-Identity-Access](../engineering/Abdifatah-14-Identity-Access/README.md) | Abdifatah |
| 15 | [Adam-15-AWS-ConMon](Adam-15-AWS-ConMon/README.md) | [Rasheed-15-AWS-ConMon](../engineering/Rasheed-15-AWS-ConMon/README.md) | Rasheed |

## Working files kept here

- [Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx](Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx)
- [Adam-07-Risk-Register/07-risk-register-lab.xlsx](Adam-07-Risk-Register/07-risk-register-lab.xlsx)
- The synthetic access review dataset stays with the 08 build, in [engineering/Abdifatah-08-Access-Reviews/uar-simulation](../engineering/Abdifatah-08-Access-Reviews/uar-simulation/README.md).
