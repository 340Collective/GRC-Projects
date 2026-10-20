# Audit Evidence Automation

| Field | Value |
| --- | --- |
| Project | 06 Audit Evidence Automation |
| Your role | Maria (Automation Engineer), engineer: you design, deploy, test, and hand over to operation; you also run the end-of-program teardown |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Rasheed. Sign-off and validation: Adam, on the Final report item, with a link to his results. Final approval: Faris, who merges. |
| Phase | Phase 1, 3 points (L) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-7](https://340collective.atlassian.net/browse/GRC-7) |
| Mirrored folder | [non-engineering/Adam-06-Evidence-Automation](../../non-engineering/Adam-06-Evidence-Automation/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the evidence pipeline. Work with Adam (ISSO) on the control mapping. He accepts your build.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-06-Evidence-Automation/LAB-STEPS.md).

- Design: 6 steps
- Deploy: 4 steps
- Test: 3 steps
- Partner test: 3 steps
- End-of-program teardown: 5 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Adam commits his results to his own folder, compares them with your report, and signs off on the Final report item ("Accepted by: <first name>", or findings). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-7](https://340collective.atlassian.net/browse/GRC-7).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. The partner's sign-off and Adam's validation go on the Final report item, and the partner's results are in their own folder. Template and build pull requests merge after code review and final approval, so the stack can deploy. The pull request that finishes the project (FINAL-REPORT.md, `Closes #N`) links the project item and merges only after the sign-off.

</details>

<details>
<summary>Cost</summary>

Config recording, S3 storage (kept small by the 30 and 7 day expiry), and Athena scans are the drivers; partition by date and framework.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run the steps below only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-evidence` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Stop the Config recorder if this build turned it on, and delete any Audit Manager assessment it created.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 and ISO 27001 audit evidence, mapped by control.

</details>

An AWS-native audit evidence pipeline. AWS Config snapshots, Audit Manager assessment evidence, and Security Hub control status are collected on a schedule and on change, written to a temporary, tamper-evident (hashed) S3 evidence lake with no Object Lock, and mapped to controls in DynamoDB. Auditors query by control through Athena and receive a per-audit evidence package. Collection, hashing, mapping, packaging, and freshness alerts are automated.

Status: target design, not yet deployed.

![Audit Evidence Automation AWS architecture](diagram/evidence-automation-aws-architecture.png)

## Automation moving parts

1. A daily EventBridge Scheduler run, plus Config and Audit Manager change events, starts collection.
2. An evidence collector Lambda pulls Config snapshots, Audit Manager assessment evidence, and Security Hub control status.
3. It writes timestamped, hashed objects and a manifest to a temporary S3 evidence lake with no Object Lock (`evidence/<framework>/<yyyy>/<mm>/<dd>/`).
4. A mapper Lambda updates the DynamoDB control-to-evidence map.
5. The Glue Data Catalog and Athena let an auditor query by control.
6. A package builder exports a per-audit evidence bundle.
7. A CloudWatch freshness alarm fires when a control has no new evidence inside its window.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The evidence is the 340 Collective AWS account's real Config history, Security Hub results, and CloudTrail activity. No client data is collected, and no client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/evidence-automation-aws-architecture.png](diagram/evidence-automation-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/evidence-automation-aws-architecture.svg](diagram/evidence-automation-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Evidence-Automation-Architecture.md](Evidence-Automation-Architecture.md) | Stage-by-stage breakdown: evidence sources, collection, evidence lake, control mapping, query, packages, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, partner test, end-of-program teardown |
| [Partner lab steps](../../non-engineering/Adam-06-Evidence-Automation/LAB-STEPS.md) | The partner's non-engineering lab steps and records, kept current by the partner |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/evidence-automation-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- The diagram icon package has no Audit Manager icon, so the generic AWS security and compliance icon stands in for it, as in 01.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md) (consumes its Security Hub and Audit Manager output) and [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md) (evidence status feeds gap scoring).
