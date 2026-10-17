# Identity and Access (Okta)

| Field | Value |
| --- | --- |
| Project | 14 Identity and Access (Okta) |
| Your role | Abdifatah (IAM / Identity Engineer), engineer: you design, deploy, test, hand off, and tear down |
| Your partner | Adam (ISSO) |
| Reviewer or validator | Code review: Rasheed or Maria. Acceptance and validation: Adam, in Jira. Final approval: Faris. |
| Phase | Phase 1, 2 points (M) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | `GRC-<NN>` (a placeholder until Faris creates the epic) |
| Mirrored folder | [non-engineering/Adam-14-Identity-Access](../../non-engineering/Adam-14-Identity-Access/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You set up Okta as the launch point and build the joiner and leaver workflows. Work with Adam (ISSO): he gives you the group model and app assignment rules, then accepts your build in Jira.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Adam-14-Identity-Access/LAB-STEPS.md).

- Design: 4 steps
- Deploy: 8 steps
- Test: 2 steps
- Hand off: 2 steps
- Tear down: 1 step

</details>

<details>
<summary>Handoffs</summary>

- Handoff 1: Okta group model and app assignment rules, Adam to Abdifatah (Jira Task, created by Adam)
- Handoff 2: Okta launch point and lifecycle workflows ready for acceptance, Abdifatah to Adam (Jira Task, created by Abdifatah)
- Handoff 3: accepted identity export for 08 and the deviation record, Adam to Faris (Jira Task, created by Adam)

</details>

<details>
<summary>Jira</summary>

- Epic: `GRC-<NN>` (a placeholder until Faris creates the epic).
- Each numbered handoff is a Jira Task linked to the epic, created by the person who sends it.
- Partner acceptance and Adam's validation are recorded on the Task. A pull request in this repo links its Task on the Jira issue line and merges only after the Task shows acceptance.

</details>

<details>
<summary>Cost</summary>

0 dollars on the Okta, GitHub, and Jira free plans.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>Teardown</summary>

- Tear down: delete the SWA and bookmark apps and the workflows, revoke the GitHub and Jira tokens, remove the test user, and record teardown evidence. The IAM users and the access model are unchanged.

</details>

<details>
<summary>Frameworks covered</summary>

SOC 2 CC6.1 to CC6.3, ISO 27001:2022 A.5.15 to A.5.18 and A.8.5, NIST CSF 2.0 PR.AA.

</details>

Okta as the GRC team's single launch point. People sign in to an Okta Integrator Free Plan org with their personal email and Okta Verify, and the Okta Browser Plugin fills the username and password for the AWS console (the IAM users from the access model), GitHub, and Jira through Secure Web Authentication (SWA) apps. Each app's own MFA is still required. There is no single sign-on, by design, and that is recorded as a deviation. Two Okta Workflows handle joiners and leavers, and the Okta group and app-assignment export becomes the identity source for 08 Access Reviews. It supports SOC 2 CC6.1 to CC6.3, ISO 27001:2022 A.5.15 to A.5.18 and A.8.5, and NIST CSF 2.0 PR.AA.

Status: target design, not yet deployed. Phase 1 build: about 2 weeks, 0 dollars. It depends on the access model's IAM users, and its export is ready before the 08 review in Phase 2.

Builder: Abdifatah (IAM / Identity Engineer), with access through the access model. Code review: Rasheed or Maria. Independent validator: Adam, since 14 feeds his 08 access reviews. Approver: Faris. Assignments can be swapped with ISSM agreement.

Jira: epic `GRC-<NN>` (a placeholder until Faris creates the epic)

![Identity and Access (Okta) architecture](diagram/identity-access-architecture.png)

## Automation moving parts

1. Each person signs in to Okta with Okta Verify MFA at every sign-in, and the Okta session lasts 8 hours. Okta groups are by function: GRC-ISSM, GRC-ISSE, GRC-ISSO, GRC-IAM, GRC-Auditor, GRC-Stakeholder.
2. The Okta Browser Plugin fills the AWS console sign-in for the person's own IAM user.
3. AWS still asks for the MFA code, and the person's IAM group (`GRC-Engineer`, `GRC-Analyst`, `GRC-Auditor`, or `Leadership`) sets access. `grc-permissions-boundary` caps the engineer and analyst users.
4. The plugin fills the GitHub and Jira sign-in, and each tool's own MFA still applies. Bookmark tiles open the GRC-Projects repo, its open pull requests, and the Jira GRC board.
5. The Joiner flow invites a new group member as a GitHub collaborator and opens a Jira onboarding work item.
6. The Leaver flow removes the collaborator and opens a Jira offboarding work item that reminds the ISSM to delete the person's IAM user.
7. CloudTrail records every console sign-in as a `ConsoleLogin` event.
8. The Okta group and app-assignment export lands in the 06 evidence lake as 08's identity source.

## 340 Collective testbed

340 Collective's real AWS account holds the IAM users the plugin signs in to. Validation is one plugin sign-in per AWS user with the AWS MFA prompt, a denied write as a read-only user, and a full join and leave of a test user across GitHub and Jira. No email addresses or tokens are published in this repo.

## Files

| File | What it is |
| --- | --- |
| [diagram/identity-access-architecture.png](diagram/identity-access-architecture.png) | Architecture diagram (PNG, 2x) |
| [diagram/identity-access-architecture.svg](diagram/identity-access-architecture.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |
| [Identity-Access-Architecture.md](Identity-Access-Architecture.md) | Layer-by-layer breakdown: why no SSO, plugin sign-in per tool, group to app assignment, workflow designs, risks, cost, evidence, teardown |
| [LAB-STEPS.md](LAB-STEPS.md) | Engineering lab steps: design, deploy, test, hand off, tear down |
| [Partner lab steps](../../non-engineering/Adam-14-Identity-Access/LAB-STEPS.md) | The partner's non-engineering lab steps (reference; the partner works in Jira) |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/identity-access-architecture
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- The plugin fills only the username and password. AWS MFA is enforced by `grc-require-mfa`, GitHub by its 2FA, and Jira by Atlassian two-step verification; the person enters each code.
- The Okta session lasts 8 hours. The AWS console session for IAM users is set by AWS, not Okta, so people sign out of AWS at the end of the day.
- Each person sets their own SWA credentials in Okta, so admins never see anyone's password.
- Real GitHub and Jira SSO needs GitHub Enterprise Cloud and Atlassian Guard on a verified domain, which personal email accounts cannot meet. See the deviation request in the architecture doc.
- GRC-Projects is a private repo on a personal account, so every GitHub collaborator gets write, including the Auditor and Stakeholder. A read role needs a GitHub organization. This is recorded as a risk in the architecture doc.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Pairs with the [access model](../../shared/access-model/README.md) (IAM users, groups, MFA, and boundary) and [08 Access Reviews](../Abdifatah-08-Access-Reviews/README.md) (the Okta group and app-assignment export is its identity source).
