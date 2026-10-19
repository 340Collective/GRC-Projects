# Third-Party and Vendor Risk Management

| Field | Value |
| --- | --- |
| Project | 02 Third-Party and Vendor Risk Management |
| Your role | Maria (Automation Engineer), engineer: you design, deploy, test, and hand over to operation; you also run the end-of-program teardown |
| Your partner | Jason (Internal Auditor) |
| Reviewer or validator | Code review: Rasheed. Acceptance test: Jason, a pass or findings record on the project item, not an approval. Validation: Adam, on the project item. Final approval: Faris. |
| Phase | Phase 4, 2 points (M) |
| Week | Week 4, Nov 9 to 15, 2026 |
| Jira epic | [GRC-3](https://340collective.atlassian.net/browse/GRC-3) |
| Mirrored folder | [non-engineering/Jason-02-TPRM-VRM](../../non-engineering/Jason-02-TPRM-VRM/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the vendor intake and scoring pipeline. Work with Jason (Internal Auditor): he gives you the questionnaire, weights, and tier rules, then runs the acceptance test on your build and records it on the project item.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Jason-02-TPRM-VRM/LAB-STEPS.md).

- Design: 6 steps
- Deploy: 4 steps
- Test: 3 steps
- Partner test: 3 steps
- End-of-program teardown: 5 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Jason agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Jason reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-3](https://340collective.atlassian.net/browse/GRC-3).
- Ask your partner directly or comment on the project item. The partner's sign-off and Adam's validation go on the Final report item. A pull request in this repo links the project item and merges only after the sign-off.

</details>

<details>
<summary>Cost</summary>

Textract (per page) and Comprehend (per unit of text) are the cost drivers; test with a few synthetic pages.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run the steps below only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-tprm` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Textract and Comprehend bill per request; confirm no asynchronous job is still running.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC9.2, ISO 27001:2022 A.5.19 to A.5.22, NIST CSF 2.0 GV.SC.

</details>

An AWS-native third-party and vendor risk management (TPRM/VRM) pipeline. Vendors submit an intake form and their assurance documents (SIG questionnaires, SOC 2 reports), which are parsed, scored, and stored in one vendor registry with a reassessment date per risk tier. It covers SOC 2 CC9.2, ISO 27001:2022 A.5.19 to A.5.22, and NIST CSF 2.0 GV.SC. Every step from upload to scoring, reminders, and the dashboard runs without manual steps; the risk owner reviews the final tier.

Status: target design, not yet deployed.

![Third-Party and Vendor Risk Management AWS architecture](diagram/tprm-vrm-aws-architecture.png)

## Automation moving parts

1. Vendor intake form submits through API Gateway to an intake Lambda.
2. SIG questionnaires and SOC 2 reports land in a private, KMS-encrypted S3 bucket.
3. The S3 upload event starts a Step Functions risk scoring workflow.
4. Textract extracts text and tables; Comprehend pulls entities and key phrases (report period, exceptions, subservice organizations).
5. A scoring Lambda assigns inherent and residual risk and a vendor tier.
6. The result is written to the DynamoDB vendor registry.
7. EventBridge Scheduler sets a reassessment SLA per tier, and a trigger Lambda emails the vendor through SES and alerts the risk owner through SNS.
8. A CloudWatch dashboard shows the vendor risk tiers.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The first vendors assessed are the ones 340 Collective already depends on: AWS, Stripe, the domain registrar, Google Workspace, and GitHub, using their public SOC 2 and trust center material as the sample document set. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/tprm-vrm-aws-architecture.png](diagram/tprm-vrm-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/tprm-vrm-aws-architecture.svg](diagram/tprm-vrm-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [TPRM-VRM-Architecture.md](TPRM-VRM-Architecture.md) | Stage-by-stage breakdown: intake, parsing, scoring, registry, reassessment, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, partner test, end-of-program teardown |
| [Partner lab steps](../../non-engineering/Jason-02-TPRM-VRM/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/tprm-vrm-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md) (vendor findings feed the third-party controls) and [07 Risk Register](../Rasheed-07-Risk-Register/README.md) (high risk vendors become register entries).
