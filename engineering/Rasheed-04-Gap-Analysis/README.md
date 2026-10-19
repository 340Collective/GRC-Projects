# 340 Collective Gap Analysis

| Field | Value |
| --- | --- |
| Project | 04 340 Collective Gap Analysis |
| Your role | Rasheed (ISSE / Engineer), engineer: you build only the monthly scoring run |
| Your partner | Jason (Internal Auditor) |
| Reviewer or validator | Code review: Maria. Sign-off: Jason, a pass or findings record on the Final report item, not an approval. Validation: Adam, on the Final report item. Final approval: Faris, who merges. |
| Phase | Phase 3, 1 point (S, the monthly scoring run only) |
| Week | Week 3, Nov 2 to 8, 2026 |
| Jira epic | [GRC-5](https://340collective.atlassian.net/browse/GRC-5) |
| Mirrored folder | [non-engineering/Jason-04-Gap-Analysis](../../non-engineering/Jason-04-Gap-Analysis/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build only the monthly scoring run. Jason (Internal Auditor) leads 04: he owns the scope, the control matrix, the scoring rules, and the gap report, and runs the acceptance test on your run and records it in his own folder.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Jason-04-Gap-Analysis/LAB-STEPS.md).

- Design: 5 steps
- Deploy: 4 steps
- Test: 3 steps
- Partner test: 3 steps
- End-of-program teardown: 5 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Jason commits his results to his own folder, compares them with your report, and signs off on the Final report item (pass, or findings, not an approval). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-5](https://340collective.atlassian.net/browse/GRC-5).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. The partner's sign-off and Adam's validation go on the Final report item, and the partner's results are in their own folder. A pull request in this repo links the project item and merges only after the sign-off.

</details>

<details>
<summary>Cost</summary>

Config rule evaluations and Security Hub checks bill per evaluation; run the scorer by hand during the test instead of waiting a month.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run the steps below only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-gap-scoring` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Remove any conformance pack or Security Hub standard this build turned on; leave those 01 still needs.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 (2017 TSC), NIST CSF 2.0, and ISO 27001:2022 Annex A, from one crosswalked library.

</details>

A repeatable gap analysis that scores an environment against SOC 2 (2017 TSC), NIST CSF 2.0, and ISO 27001:2022 Annex A from one crosswalked control library. Technical posture comes from AWS Config and Security Hub, process controls come from assessor questionnaire answers, and a monthly scoring run produces a gap report and a client-facing one-pager. Scoring, history, report generation, and delivery are automated; the assessor supplies the answers.

Status: target design, not yet deployed.

![340 Collective Gap Analysis AWS architecture](diagram/gap-analysis-aws-architecture.png)

## Automation moving parts

1. Config conformance packs and Security Hub standards supply technical posture.
2. Assessor questionnaire answers (JSON) are uploaded to S3 for process controls.
3. The DynamoDB control library holds controls, crosswalk IDs, and expected evidence.
4. A monthly EventBridge Scheduler run starts the gap scoring Lambda.
5. The scorer marks each control met, partial, or gap and writes a scored history table.
6. A report builder Lambda writes the gap report and a client-facing one-pager to S3.
7. SES emails the report link to the owner.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. 340 Collective's own security posture is the first assessed "client": its Config rules, Security Hub standards, and its own questionnaire answers produce the first scored report. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/gap-analysis-aws-architecture.png](diagram/gap-analysis-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/gap-analysis-aws-architecture.svg](diagram/gap-analysis-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Gap-Analysis-Architecture.md](Gap-Analysis-Architecture.md) | Stage-by-stage breakdown: posture inputs, control library, gap scoring, report generation, delivery, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, partner test, end-of-program teardown |
| [Partner lab steps](../../non-engineering/Jason-04-Gap-Analysis/LAB-STEPS.md) | The partner's non-engineering lab steps and records, kept current by the partner |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/gap-analysis-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- The one-pager follows the 340 Collective `client-onepager-style` standard. The template itself is not copied into this repo.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md) (Security Hub findings) and [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md) (evidence freshness per control can feed the score).
