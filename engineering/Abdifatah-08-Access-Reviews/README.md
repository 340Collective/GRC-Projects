# User Access Reviews

| Field | Value |
| --- | --- |
| Project | 08 User Access Reviews |
| Your role | Abdifatah (IAM / Identity Engineer), engineer: you design, deploy, test, and tear down |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Rasheed or Maria. Acceptance and validation: Adam, in Jira. Final approval: Faris. |
| Phase | Phase 2, 2 points (M) |
| Week | Week 2, Oct 26 to Nov 1, 2026 |
| Jira epic | [GRC-9](https://340collective.atlassian.net/browse/GRC-9) |
| Mirrored folder | [non-engineering/Adam-08-Access-Reviews](../../non-engineering/Adam-08-Access-Reviews/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the access review package. Work with Adam (ISSO): he gives you the worksheet columns and review rules, then accepts your build in Jira. The synthetic dataset in uar-simulation stays in this folder.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-08-Access-Reviews/LAB-STEPS.md).

- Design: 6 steps
- Deploy: 4 steps
- Test: 3 steps
- Partner test: 3 steps
- Tear down: 5 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-9](https://340collective.atlassian.net/browse/GRC-9).
- Ask your partner directly or comment on the project item. The partner's sign-off and Adam's validation go on the Final report item. A pull request in this repo links the project item and merges only after the sign-off.

</details>

<details>
<summary>Cost</summary>

The external access analyzer has no charge; the rest stays near the free tier at a quarterly cadence.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Tear down after the partner's sign-off and final approval are on the Final report item, before the phase ends.
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-access-review` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Delete the Access Analyzer analyzers this build created.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC6.2 and CC6.3, ISO 27001:2022 A.5.18, NIST CSF 2.0 PR.AA.

</details>

An AWS-native user access review (UAR) campaign. Each quarter, a Step Functions campaign collects IAM users, groups, and roles (the access model), plus IAM Identity Center assignments only if it is ever enabled, or the Okta group export if 14 is built, adds IAM Access Analyzer findings, and builds one review package per approver. Approvers keep or remove each entitlement through a sign-off API, and removals run only after the owner confirms them. It supports SOC 2 CC6.2 and CC6.3, ISO 27001:2022 A.5.18, and NIST CSF 2.0 PR.AA. Collection, packaging, reminders, decision tracking, and evidence export are automated; nothing is revoked without a human.

Status: target design, not yet deployed.

![User Access Reviews AWS architecture](diagram/access-review-aws-architecture.png)

## Automation moving parts

1. A quarterly EventBridge Scheduler run starts a Step Functions review campaign.
2. A collector Lambda reads IAM users, groups, and roles, plus IAM Identity Center assignments only if it is ever enabled, or the Okta group export if 14 is built.
3. IAM Access Analyzer adds external access and unused access findings.
4. A package builder writes one review package per approver to S3 and records items in DynamoDB.
5. SES sends each approver a sign-off link to the API Gateway sign-off API.
6. A decision Lambda records keep or remove, with approver and timestamp.
7. Removals wait for owner confirmation, then are applied.
8. The completed campaign is exported as evidence.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The first campaign reviews 340 Collective's own IAM users, groups, and roles from the access model, and flags hand-made drift. If 14 is built, the Okta group export is the identity source for people. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/access-review-aws-architecture.png](diagram/access-review-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/access-review-aws-architecture.svg](diagram/access-review-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Access-Review-Architecture.md](Access-Review-Architecture.md) | Stage-by-stage breakdown: identity sources, campaign, packages, sign-off, remediation, evidence, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, partner test, tear down |
| [Partner lab steps](../../non-engineering/Adam-08-Access-Reviews/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/access-review-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- The diagram package's `single-sign-on` icon stands in for IAM Identity Center (the service's former name was AWS SSO). The diagram shows it as an optional source; it is read only if it is ever enabled.
- Revocation is never automatic. A rejected entitlement opens a removal task that runs only after the owner confirms, the same human gate as 01's approval step.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md) (campaign records go to the evidence lake) and [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md) (access review completion scores the access controls). If built, [14 Identity and Access (Okta)](../Abdifatah-14-Identity-Access/README.md) supplies the Okta group and app-assignment export as the identity source.
