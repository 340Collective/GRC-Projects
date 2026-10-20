# Risk Register

| Field | Value |
| --- | --- |
| Project | 07 Risk Register |
| Your role | Rasheed (ISSE / Engineer), engineer: you design, deploy, test, and hand over to operation; you also run the end-of-program teardown |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Maria. Sign-off and validation: Adam, on the Final report item, with a link to his results. Final approval: Faris, who merges. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-8](https://340collective.atlassian.net/browse/GRC-8) |
| Mirrored folder | [non-engineering/Adam-07-Risk-Register](../../non-engineering/Adam-07-Risk-Register/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the risk register service. Work with Adam (ISSO): he gives you the scoring rules and the seed register, then accepts your build on the Final report item.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-07-Risk-Register/LAB-STEPS.md).

- Design: 7 steps
- Deploy: 4 steps
- Test: 3 steps
- Partner test: 3 steps
- End-of-program teardown: 5 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: Adam writes REQUIREMENTS.md in his own folder, and Faris accepts it. You and Adam agree on scope.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Adam commits his results to his own folder, compares them with your report, and signs off on the Final report item ("Accepted by: <first name>", or findings). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-8](https://340collective.atlassian.net/browse/GRC-8).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. The partner's sign-off and Adam's validation go on the Final report item, and the partner's results are in their own folder. Template and build pull requests merge after code review and final approval, so the stack can deploy. The pull request that finishes the project (FINAL-REPORT.md, `Closes #N`) links the project item and merges only after the sign-off.
- Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.

</details>

<details>
<summary>Cost</summary>

There is no paid dashboard; Cognito, API Gateway, Lambda, DynamoDB, and Athena stay at or near the free tier.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run the steps below only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-risk-register` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Revoke the Jira API token and delete its `/grc/` parameter.
- Record teardown evidence (stack deleted, buckets gone, services off, spend recorded, with no GRC charges after deletion) where the ISSM designates, outside git, and note it on the project item.

</details>

<details>
<summary>Frameworks covered</summary>

ISO 27001:2022 clauses 6.1 and 8.2, NIST CSF 2.0 GV.RM and ID.RA, SOC 2 CC3.

</details>

An AWS-native risk register. Risk owners sign in through Cognito and log or update risks through an API, a handler scores each risk with the owner's DREAD+ model, the register lives in DynamoDB, each risk is mirrored to a Jira ticket, and every review date is a real timer that escalates when missed. It supports ISO 27001:2022 clauses 6.1 and 8.2, NIST CSF 2.0 GV.RM and ID.RA, and SOC 2 CC3. Scoring, ticket sync, SLA timers, escalation, and the heatmap are automated.

Status: target design, not yet deployed.

![Risk Register AWS architecture](diagram/risk-register-aws-architecture.png)

## Automation moving parts

1. A risk owner signs in through Cognito and submits or updates a risk through API Gateway.
2. A risk handler Lambda validates fields and computes the DREAD+ score and the inherent and residual rating.
3. The DynamoDB risk register stores each risk, with GSIs by owner and by status.
4. DynamoDB Streams triggers a sync Lambda that mirrors each risk to a Jira ticket.
5. The handler creates or updates a one-off EventBridge Scheduler schedule per risk review date (the SLA timer).
6. At expiry, an SLA escalator Lambda escalates through SNS.
7. A nightly export to S3 feeds Athena, and a Lambda renders the likelihood by impact heatmap as an HTML report.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The first register is 340 Collective's own, covering business, security, and vendor risks. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/risk-register-aws-architecture.png](diagram/risk-register-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/risk-register-aws-architecture.svg](diagram/risk-register-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Risk-Register-Architecture.md](Risk-Register-Architecture.md) | Stage-by-stage breakdown: intake, scoring, register, Jira sync, SLA timers, analytics, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, partner test, end-of-program teardown |
| [Partner lab steps](../../non-engineering/Adam-07-Risk-Register/LAB-STEPS.md) | The partner's non-engineering lab steps and records, kept current by the partner |
| [07-risk-register-lab.xlsx](../../non-engineering/Adam-07-Risk-Register/07-risk-register-lab.xlsx) | Lab sheet with the risk scoring rules and the seed register (Adam's kickoff input) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/risk-register-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- The DREAD+ scoring model and the Jira risk ticket schema are the owner's own and are kept in the owner's private notes. They are referenced here by concept only and are not copied into this repo; field names stay generic.
- The risk API sits behind a Cognito user pool authorizer, so the write API is never unauthenticated.
- Jira Cloud has no icon in the diagram package, so the generic office building icon stands in for it, as in 01.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [02 TPRM/VRM](../Maria-02-TPRM-VRM/README.md) (high risk vendors become register entries) and [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md) (same Jira project pattern).
