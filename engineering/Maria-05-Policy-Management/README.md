# 340 Collective Policy Management

| Field | Value |
| --- | --- |
| Project | 05 340 Collective Policy Management |
| Your role | Maria (Automation Engineer), engineer: you design, deploy, test, and tear down |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Rasheed. Acceptance and validation: Adam, in Jira. Final approval: Faris. |
| Phase | Phase 5, 1 point (S) |
| Week | Week 5, Nov 16 to 22, 2026 |
| Jira epic | [GRC-6](https://340collective.atlassian.net/browse/GRC-6) |
| Mirrored folder | [non-engineering/Adam-05-Policy-Management](../../non-engineering/Adam-05-Policy-Management/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You build the policy-as-code pipeline and attestation tracking. Work with Adam (ISSO): he gives you six policy drafts with the header block and review cycle, then accepts your build in Jira.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-05-Policy-Management/LAB-STEPS.md).

- Design: 5 steps
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

- Epic: [GRC-6](https://340collective.atlassian.net/browse/GRC-6).
- Ask your partner directly or comment on the project item. The partner's sign-off and Adam's validation go on the Final report item. A pull request in this repo links the project item and merges only after the sign-off.

</details>

<details>
<summary>Cost</summary>

CodeBuild build minutes are the only real cost; keep test builds few.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Tear down after the partner's sign-off and final approval are on the Final report item, before the phase ends.
- Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
- Delete the `grc-policy` stack from clean `main` and wait for `DELETE_COMPLETE`.
- Delete the GitHub connection if you created it outside the stack.
- Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, NIST CSF 2.0 GV.PO.

</details>

A policy-as-code lifecycle for 340 Collective. Policies are written as Markdown in Git, reviewed through pull requests, validated and rendered in CodePipeline, published to a versioned S3 library, and tracked through staff attestation and annual review reminders. It supports SOC 2 CC1.4 and CC5.3, ISO 27001:2022 A.5.1 and clause 7.5, and NIST CSF 2.0 GV.PO. Validation, publishing, attestation requests, and reminders are automated; the policy owner approves every change.

Status: target design, not yet deployed.

![340 Collective Policy Management AWS architecture](diagram/policy-management-aws-architecture.png)

## Automation moving parts

1. Policies are authored as Markdown in GitHub, and the policy owner reviews each pull request.
2. A merge to main triggers CodePipeline through a GitHub connection.
3. CodeBuild validates front matter (owner, version, review date), links, and banned terms, then renders the PDF.
4. The policy is published to a versioned S3 policy library.
5. A new version event in EventBridge starts a Lambda that emails staff through SES.
6. Staff attest through API Gateway and Lambda into a DynamoDB attestation table.
7. EventBridge Scheduler sends annual review and overdue attestation reminders.

## 340 Collective testbed

340 Collective's real AWS infrastructure is the environment this design is validated against. The intended policy set is 340 Collective's own: information security, acceptable use, access control, vendor management, incident response, and data retention. This repo holds no policy text; the policy corpus stays in 340 Collective's private policy repo. No client data, account identifiers, or resource names are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/policy-management-aws-architecture.png](diagram/policy-management-aws-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/policy-management-aws-architecture.svg](diagram/policy-management-aws-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Policy-Management-Architecture.md](Policy-Management-Architecture.md) | Stage-by-stage breakdown: source, validation, library, attestation, review cycle, data model, security, cost note, build order |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, partner test, tear down |
| [Partner lab steps](../../non-engineering/Adam-05-Policy-Management/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/policy-management-aws-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with [04 Gap Analysis](../Rasheed-04-Gap-Analysis/README.md) (policy and attestation status score the governance controls) and [06 Evidence Automation](../Maria-06-Evidence-Automation/README.md) (attestation records are audit evidence).
