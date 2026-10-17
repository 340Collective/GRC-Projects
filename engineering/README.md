# Engineering track

Engineers build, deploy, test, hand off, and tear down the AWS designs. Each folder is named `<Engineer>-<NN>-<Project>`, so find your own folder by your first name. Every folder has a README with your header block and a LAB-STEPS.md with the engineering steps. The general lab guide is [shared/labs/README.md](../shared/labs/README.md).

## Team

| Person | Role | Builds | Points |
| --- | --- | --- | --- |
| Faris | ISSM, also builds | Foundation (Phase 1), 01 (Phase 2), 00 overview (every phase) | 5 |
| Rasheed | ISSE / Engineer, named backup on the foundation | 07, 13, 12, 15 | 8 |
| Maria | Automation Engineer | 06, 10, 02, 05 | 8 |
| Alex | Security Automation Engineer | 11, 03, 09, and the 04 monthly scoring run | 7 plus 1 |
| Abdifatah | IAM / Identity Engineer | 14, 08 | 4 |

Alex: background in vulnerability management, CIS hardening, SIEM and IR playbooks, and Python detection automation.

Points: S = 1, M = 2, L = 3. One active build per engineer at a time.

## Phase queue

| Phase | Faris | Rasheed | Maria | Alex | Abdifatah |
| --- | --- | --- | --- | --- | --- |
| 1 | Foundation | 07 | 06 | 11 | 14 |
| 2 | 01 | 13 | 10 | 03 | 08 |
| 3 | Review | 12 | 02 | 09 and the 04 scoring run | Review |
| 4 | Review | 15 | 05 | Review | Review |

A phase ends when all its builds are merged and torn down cleanly. 15 is in Phase 4 because it posts its monthly KPIs to the GRC Metrics Jira issue that 12 builds in Phase 3, and it keeps Rasheed to one active build at a time.

## Code review pairs

- Rasheed reviews Maria, Alex, and Abdifatah.
- Maria and Alex review each other and Rasheed. Alex reviews 15.
- Rasheed or Alex reviews Faris.
- Faris and Abdifatah add review capacity in Phase 3.

After code review, the partner accepts in Jira, Adam (ISSO) validates in Jira, Jason (Internal Auditor) assesses once per phase, and Faris (ISSM) gives final approval. For Faris-built work (foundation, 01, 00), Adam accepts and gives final approval. Nobody validates their own build or requirements.

## Folders

| # | Engineering folder | Partner folder (non-engineering) | Phase |
| --- | --- | --- | --- |
| 00 | [Faris-00-Platform-Overview](Faris-00-Platform-Overview/README.md) | [Faris-00-Platform-Overview](../non-engineering/Faris-00-Platform-Overview/README.md) | Every phase |
| 01 | [Faris-01-GRC-as-Code-Platform](Faris-01-GRC-as-Code-Platform/README.md) | [Jason-01-GRC-as-Code-Platform](../non-engineering/Jason-01-GRC-as-Code-Platform/README.md) | 1 and 2 |
| 02 | [Maria-02-TPRM-VRM](Maria-02-TPRM-VRM/README.md) | [Jason-02-TPRM-VRM](../non-engineering/Jason-02-TPRM-VRM/README.md) | 3 |
| 03 | [Alex-03-Privacy](Alex-03-Privacy/README.md) | [Jason-03-Privacy](../non-engineering/Jason-03-Privacy/README.md) | 2 |
| 04 | [Alex-04-Gap-Analysis](Alex-04-Gap-Analysis/README.md) | [Jason-04-Gap-Analysis](../non-engineering/Jason-04-Gap-Analysis/README.md) | 3 |
| 05 | [Maria-05-Policy-Management](Maria-05-Policy-Management/README.md) | [Adam-05-Policy-Management](../non-engineering/Adam-05-Policy-Management/README.md) | 4 |
| 06 | [Maria-06-Evidence-Automation](Maria-06-Evidence-Automation/README.md) | [Adam-06-Evidence-Automation](../non-engineering/Adam-06-Evidence-Automation/README.md) | 1 |
| 07 | [Rasheed-07-Risk-Register](Rasheed-07-Risk-Register/README.md) | [Adam-07-Risk-Register](../non-engineering/Adam-07-Risk-Register/README.md) | 1 |
| 08 | [Abdifatah-08-Access-Reviews](Abdifatah-08-Access-Reviews/README.md) | [Adam-08-Access-Reviews](../non-engineering/Adam-08-Access-Reviews/README.md) | 2 |
| 09 | [Alex-09-Control-Testing](Alex-09-Control-Testing/README.md) | [Jason-09-Control-Testing](../non-engineering/Jason-09-Control-Testing/README.md) | 3 |
| 10 | [Maria-10-Audit-Engagement-Manager](Maria-10-Audit-Engagement-Manager/README.md) | [Jason-10-Audit-Engagement-Manager](../non-engineering/Jason-10-Audit-Engagement-Manager/README.md) | 2 |
| 11 | [Alex-11-Compliance-as-Code-Guardrails](Alex-11-Compliance-as-Code-Guardrails/README.md) | [Adam-11-Compliance-as-Code-Guardrails](../non-engineering/Adam-11-Compliance-as-Code-Guardrails/README.md) | 1 |
| 12 | [Rasheed-12-Metrics-Reporting](Rasheed-12-Metrics-Reporting/README.md) | [Adam-12-Metrics-Reporting](../non-engineering/Adam-12-Metrics-Reporting/README.md) | 3 |
| 13 | [Rasheed-13-BCDR-IR](Rasheed-13-BCDR-IR/README.md) | [Jason-13-BCDR-IR](../non-engineering/Jason-13-BCDR-IR/README.md) | 2 |
| 14 | [Abdifatah-14-Identity-Access](Abdifatah-14-Identity-Access/README.md) | [Adam-14-Identity-Access](../non-engineering/Adam-14-Identity-Access/README.md) | 1 |
| 15 | [Rasheed-15-AWS-ConMon](Rasheed-15-AWS-ConMon/README.md) | [Adam-15-AWS-ConMon](../non-engineering/Adam-15-AWS-ConMon/README.md) | 4 |

## How engineers work

- Templates live in the private website repo as `cloudformation/grc-*.yaml`, move `dev` to `test` to `main` under its change-control rule, and deploy from clean `main` after ISSM approval.
- Handoffs are Jira Tasks. A pull request here links its Task and merges only after the Task shows acceptance.
- Engineers or Faris keep the matching non-engineering folder current; the partners work in Jira.
