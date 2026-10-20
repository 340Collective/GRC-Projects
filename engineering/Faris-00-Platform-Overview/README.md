# GRC Platform Overview

| Field | Value |
| --- | --- |
| Project | 00 GRC Platform Overview |
| Your role | Faris (ISSM), keeps the platform overview current |
| Your partner | Adam (ISSO), who accepts the overview; each engineer sends a phase build list |
| Reviewer or validator | Diagram script review: Rasheed, with Maria as backup. Acceptance and final approval: Adam, since Faris wrote it. |
| Phase | Every phase (documentation), no points |
| Week | No build week; updated at the end of every phase (see the phase table in GOVERNANCE.md) |
| Jira epic | [GRC-1](https://340collective.atlassian.net/browse/GRC-1) |
| Mirrored folder | [non-engineering/Faris-00-Platform-Overview](../../non-engineering/Faris-00-Platform-Overview/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You keep the platform overview current. At the end of each phase, collect the build list from each engineer, update the diagram, and send it to Adam (ISSO). He accepts it and gives final approval, since you wrote it.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md).

- Design: 2 steps
- Deploy: 3 steps
- Test: 3 steps
- Partner test: 2 steps
- End-of-program teardown: 2 steps

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: you write REQUIREMENTS.md in the non-engineering 00 folder, and Adam accepts it. You and Adam agree on scope.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- At each phase end: you commit FINAL-REPORT.md to this folder and your phase tracking results to the non-engineering 00 folder. Adam compares them and signs off on the Final report item ("Accepted by: <first name>", or findings). Adam gives final approval, and Faris merges after it.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-1](https://340collective.atlassian.net/browse/GRC-1).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. The partner's sign-off and Adam's validation go on the Final report item, and the partner's results are in their own folder. Template and build pull requests merge after code review and final approval, so the stack can deploy. The pull request that finishes the project (FINAL-REPORT.md, `Closes #N`) links the project item and merges only after the sign-off.

</details>

<details>
<summary>Cost</summary>

0 dollars: documentation only, nothing deploys.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- Nothing to tear down: 00 has no stack.
- At each phase end, confirm with a read-only CloudFormation stack list that every signed-off `grc-*` stack from the phase is running, and that no test-only stack is left. At the end-of-program teardown, confirm that every `grc-*` project stack is gone, with `grc-foundation` deleted last.

</details>

<details>
<summary>Frameworks covered</summary>

None directly. The overview shows how the projects that cover SOC 2, NIST, and ISO 27001 connect.

</details>

A system-of-systems map of projects 01 to 15 in this repo. Each box is one project; each line is a record one project hands to another, traced to that project's own architecture doc or README. It shows how the set works as one GRC platform: policies become guardrails, guardrail and posture findings land in one Security Hub hub, evidence and risks collect in shared stores, assessment and audit read from those stores, and metrics read all of them.

Status: target design, not yet deployed. Like every project here, it is a reference architecture validated against 340 Collective's AWS account as a testbed.

![GRC platform overview](diagram/grc-platform-overview.png)

## How the projects connect

- 01 is the findings hub. Security Hub holds every finding in ASFF, and 04, 06, and 12 read its findings and control status.
- 05 policies become 11 guardrail checks, and every guardrail violation becomes an ASFF finding in 01.
- 06 is the shared evidence lake. 08 access review campaigns, 03 DSAR records, and 13 DR test and tabletop records land there.
- 07 is the shared risk register. 02 high tier vendors, 13 failed DR tests, and 10 open audit findings become risks.
- 04, 09, and 10 are the assessment path: 09 tests the controls 04 marks met, samples from 06 and 07, and its workpapers start the 10 engagement.
- 12 reads the stores of 01, 02, 05, 06, 07, 08, and 10, read only, for KRIs, KPIs, and the board pack.
- 15 AWS ConMon routes 01's Security Hub findings, 11's Config results, and CloudTrail events to Jira remediation issues and email alerts, and posts its monthly KPIs to 12's GRC Metrics Jira issue (that last link is documented, not drawn). Its design is in [15 AWS ConMon](../Rasheed-15-AWS-ConMon/README.md).
- 14 Identity and Access (Okta), a Phase 1 build, puts Okta in front of the [access model](../../shared/access-model/README.md)'s IAM users as a sign-in launch point, and its group and app-assignment export becomes 08's identity source. It is drawn beside 08 with one line into it.

## Also documented, not drawn

These pairings appear in project READMEs. Drawing them would force line crossings, so they are listed here instead: 05, 08, 02, 11, and 06 feed gap scoring in 04; 05 attestations and closed 10 engagements are also evidence in 06; and auditors in 10 request 13 records as PBC items.

## Files

| File | What it is |
| --- | --- |
| [diagram/grc-platform-overview.png](diagram/grc-platform-overview.png) | Overview diagram (PNG, 2x) |
| [diagram/grc-platform-overview.svg](diagram/grc-platform-overview.svg) | Same diagram as a scalable SVG |
| [diagram/build_diagram.py](diagram/build_diagram.py) | Script that regenerates the diagram and runs its layout and sensitive-text checks |

## Regenerate the diagram

```bash
python3 diagram/build_diagram.py --setup          # once: venv + diagrams==0.25.1 (needs rsvg-convert from librsvg)
python3 diagram/build_diagram.py diagram/grc-platform-overview
```

The script must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.

## Notes

- Each project is drawn as the one AWS service at the center of its design, so the icon stands for the whole project.
- Where several projects feed one store, their lines merge at a junction dot and share the last segment into it.
- Connections show design intent. Nothing is deployed yet, so no line is verified from IaC.
- Review: Faris writes this overview, so Adam accepts each update and gives final approval.
