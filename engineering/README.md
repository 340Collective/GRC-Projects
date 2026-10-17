# Engineering track

Engineers build, deploy, test, hand off, and tear down the AWS designs. Each folder is named `<Engineer>-<NN>-<Project>`, so find your own folder by your first name. Every folder has a README with your header block and a LAB-STEPS.md with the engineering steps. The general lab guide is [shared/labs/README.md](../shared/labs/README.md).

## Team

| Person | Role | Builds | Points |
| --- | --- | --- | --- |
| Faris | ISSM, also builds | Foundation (Phase 1), 01 (Phase 2), 11 (Phase 3), 00 overview (every phase) | 8 |
| Rasheed | ISSE / Engineer, named backup on the foundation | 07, 13, 09 and the 04 monthly scoring run, 12, 15 | 10 plus 1 |
| Maria | Automation Engineer | 06, 10, 03, 02, 05 | 10 |
| Abdifatah | IAM / Identity Engineer | 14, 08 | 4 |

Points: S = 1, M = 2, L = 3. One active build per engineer at a time.

## Phase queue

| Phase | Faris | Rasheed | Maria | Abdifatah |
| --- | --- | --- | --- | --- |
| 1 | Foundation | 13 | 06 | 14 |
| 2 | 01 | 07 | 10 | 08 |
| 3 | 11 | 09 and the 04 scoring run | 03 | Review |
| 4 | Review | 12 | 02 | Review |
| 5 | Review | 15 | 05 | Review |

A phase ends when all its builds are merged and torn down cleanly. 12 is in Phase 4 because it needs data from 06, 07, and 11, so 11 lands first. 15 is in Phase 5 because it posts its monthly KPIs to the GRC Metrics Jira issue that 12 builds in Phase 4, and needs findings from 01 and 11. Every engineer has one active build at a time.

## Code review pairs

- Rasheed reviews Faris (foundation, 01, 11, 00), with Maria as backup.
- Rasheed reviews Maria.
- Maria reviews Rasheed, including 15.
- Rasheed or Maria reviews Abdifatah.
- Abdifatah adds review capacity from Phase 3.

After code review, the partner accepts in Jira, Adam validates in Jira, Jason assesses once per phase, and Faris gives final approval. For Faris-built work (foundation, 01, 11, 00), Adam accepts and gives final approval. Nobody validates their own build or requirements.

## Folders

| # | Engineering folder | Partner folder (non-engineering) | Phase |
| --- | --- | --- | --- |
| 00 | [Faris-00-Platform-Overview](Faris-00-Platform-Overview/README.md) | [Faris-00-Platform-Overview](../non-engineering/Faris-00-Platform-Overview/README.md) | Every phase |
| 01 | [Faris-01-GRC-as-Code-Platform](Faris-01-GRC-as-Code-Platform/README.md) | [Jason-01-GRC-as-Code-Platform](../non-engineering/Jason-01-GRC-as-Code-Platform/README.md) | 1 and 2 |
| 02 | [Maria-02-TPRM-VRM](Maria-02-TPRM-VRM/README.md) | [Jason-02-TPRM-VRM](../non-engineering/Jason-02-TPRM-VRM/README.md) | 4 |
| 03 | [Maria-03-Privacy](Maria-03-Privacy/README.md) | [Jason-03-Privacy](../non-engineering/Jason-03-Privacy/README.md) | 3 |
| 04 | [Rasheed-04-Gap-Analysis](Rasheed-04-Gap-Analysis/README.md) | [Jason-04-Gap-Analysis](../non-engineering/Jason-04-Gap-Analysis/README.md) | 3 |
| 05 | [Maria-05-Policy-Management](Maria-05-Policy-Management/README.md) | [Adam-05-Policy-Management](../non-engineering/Adam-05-Policy-Management/README.md) | 5 |
| 06 | [Maria-06-Evidence-Automation](Maria-06-Evidence-Automation/README.md) | [Adam-06-Evidence-Automation](../non-engineering/Adam-06-Evidence-Automation/README.md) | 1 |
| 07 | [Rasheed-07-Risk-Register](Rasheed-07-Risk-Register/README.md) | [Adam-07-Risk-Register](../non-engineering/Adam-07-Risk-Register/README.md) | 2 |
| 08 | [Abdifatah-08-Access-Reviews](Abdifatah-08-Access-Reviews/README.md) | [Adam-08-Access-Reviews](../non-engineering/Adam-08-Access-Reviews/README.md) | 2 |
| 09 | [Rasheed-09-Control-Testing](Rasheed-09-Control-Testing/README.md) | [Jason-09-Control-Testing](../non-engineering/Jason-09-Control-Testing/README.md) | 3 |
| 10 | [Maria-10-Audit-Engagement-Manager](Maria-10-Audit-Engagement-Manager/README.md) | [Jason-10-Audit-Engagement-Manager](../non-engineering/Jason-10-Audit-Engagement-Manager/README.md) | 2 |
| 11 | [Faris-11-Compliance-as-Code-Guardrails](Faris-11-Compliance-as-Code-Guardrails/README.md) | [Adam-11-Compliance-as-Code-Guardrails](../non-engineering/Adam-11-Compliance-as-Code-Guardrails/README.md) | 3 |
| 12 | [Rasheed-12-Metrics-Reporting](Rasheed-12-Metrics-Reporting/README.md) | [Adam-12-Metrics-Reporting](../non-engineering/Adam-12-Metrics-Reporting/README.md) | 4 |
| 13 | [Rasheed-13-BCDR-IR](Rasheed-13-BCDR-IR/README.md) | [Jason-13-BCDR-IR](../non-engineering/Jason-13-BCDR-IR/README.md) | 1 |
| 14 | [Abdifatah-14-Identity-Access](Abdifatah-14-Identity-Access/README.md) | [Adam-14-Identity-Access](../non-engineering/Adam-14-Identity-Access/README.md) | 1 |
| 15 | [Rasheed-15-AWS-ConMon](Rasheed-15-AWS-ConMon/README.md) | [Adam-15-AWS-ConMon](../non-engineering/Adam-15-AWS-ConMon/README.md) | 5 |

## How engineers work

- Templates live in this repo as `infrastructure/cloudformation/grc-*.yaml` and go by pull request into `main`. After approval, you deploy your own project stack with your `GRC-Engineer` seat from this repo's clean `main` equal to `origin/main`, tag the deploy `live-YYYY-MM-DD`, and tear it down when the phase ends. Only the ISSM deploys the shared stacks (see [infrastructure/README.md](../infrastructure/README.md)).
- Handoffs are Jira Tasks. A pull request here links its Task and merges only after the Task shows acceptance.
- Engineers or Faris keep the matching non-engineering folder current; the partners work in Jira.
