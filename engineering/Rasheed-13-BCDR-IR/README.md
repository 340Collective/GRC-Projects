# BC/DR and Incident Response Compliance

| Field | Value |
| --- | --- |
| Project | 13 BC/DR and Incident Response Compliance |
| Your role | Rasheed (ISSE / Engineer), engineer: you design, deploy, test, hand off, and tear down |
| Your partner | Jason (Internal Auditor) |
| Reviewer or validator | Code review: Maria. Acceptance test: Jason, a pass or findings record in Jira, not an approval. Validation: Adam, in Jira. Final approval: Faris. |
| Phase | Phase 1, 2 points (M) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-14](https://340collective.atlassian.net/browse/GRC-14) |
| Mirrored folder | [non-engineering/Jason-13-BCDR-IR](../../non-engineering/Jason-13-BCDR-IR/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the restore test and the IR runbooks. Work with Jason (Internal Auditor): he gives you the IR plan requirements, the tabletop scenario, and the RTO and RPO targets, then runs the acceptance test in Jira.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md).

- Design: 7 steps
- Deploy: 4 steps
- Test: 3 steps
- Hand off: 3 steps
- Tear down: 5 steps

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: IR plan requirements, tabletop scenario, and RTO and RPO targets, Jason to Rasheed (Jira Task, created by Jason)
- Handoff 2: restore test and IR runbook build ready for acceptance testing, Rasheed to Jason (Jira Task, created by Rasheed)
- Handoff 3: tabletop summary and BC/DR test record, Jason to Faris (Jira Task, created by Jason)

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-14](https://340collective.atlassian.net/browse/GRC-14).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- Partner acceptance and Adam's validation are recorded on the Task. A pull request in this repo links its Task on the Jira issue line and merges only after the Task shows acceptance.
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

AWS Backup storage and restores, and the temporary restored copy; keep restores small and delete them at the end of each test.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-bcdr` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Delete every recovery point in the backup vault first (a vault that still holds recovery points cannot be deleted), and any restored test copy.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 A1.2, A1.3, CC7.4, and CC7.5; ISO 27001:2022 A.5.24 to A.5.30; NIST CSF 2.0 RS and RC.

</details>

An AWS-native way to prove that backups restore and that incident response is practiced, written from the compliance evidence angle. AWS Backup protects the data, a quarterly Step Functions DR test restores a recovery point into an isolated test target, validates it, and records the achieved RTO and RPO against targets. IR runbooks and tabletop exercise records are kept as evidence, and any failed or late test becomes a finding in the risk register and the evidence lake. It supports SOC 2 A1.2, A1.3, CC7.4, and CC7.5; ISO 27001:2022 A.5.24 to A.5.30; and NIST CSF 2.0 RS and RC. Backups, restore tests, validation, RTO and RPO evidence, and finding routing are automated; the IR lead runs tabletop exercises and signs off each DR test result.

Status: target design, not yet deployed.

![BC/DR and Incident Response Compliance AWS architecture](diagram/bcdr-ir-aws-architecture.png)

## Automation moving parts

1. AWS Backup plans protect the DynamoDB tables and S3 data.
2. A quarterly EventBridge Scheduler run starts a Step Functions DR test.
3. The test restores a recovery point to an isolated test target, runs a validation Lambda (row counts, checksums), and times the restore.
4. Results (achieved RTO and RPO compared with targets) are written to DynamoDB, and the test report goes to S3.
5. IR runbooks (Systems Manager Automation documents) and tabletop exercise records are stored in S3.
6. Failed or late tests become findings sent through EventBridge to the 07 risk register and the 06 evidence lake.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The DR test exercises 340 Collective's own backup plans for its DynamoDB tables and S3 data, and the IR lead runs tabletop exercises against 340 Collective's incident response process. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/bcdr-ir-aws-architecture.png](diagram/bcdr-ir-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/bcdr-ir-aws-architecture.svg](diagram/bcdr-ir-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [BCDR-IR-Architecture.md](BCDR-IR-Architecture.md) | Stage-by-stage breakdown: backup, DR test, results, incident response, findings routing, downstream, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, hand off, tear down |
| [Partner lab steps](../../non-engineering/Jason-13-BCDR-IR/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/bcdr-ir-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Approvers: the IR lead signs off each DR test result and each tabletop record; the 340 Collective owner approves the RTO and RPO targets and accepts any finding a failed test raises.
- Restore tests always run into an isolated test target (a restored copy, never the live resource), and the test target is deleted after the check. A DR test never touches production data.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [07 Risk Register](../Rasheed-07-Risk-Register/README.md) (failed tests become risks), [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md) (test results are BC/DR evidence), and [10 Audit Engagement Manager](../Maria-10-Audit-Engagement-Manager/README.md) (auditors request these records as PBC items).
