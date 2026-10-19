# GRC Platform Overview (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-1](https://340collective.atlassian.net/browse/GRC-1) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | 00 GRC Platform Overview |
| Your role | Faris (ISSM), tracks what each phase delivered |
| Your partner | Each engineer sends a phase build list; Adam (ISSO) accepts the overview |
| Reviewer or validator | Adam accepts your REQUIREMENTS.md and the updated overview, and gives final approval, since you wrote it. Adam reviews your pull requests to this folder before you merge them. |
| Phase | Every phase (documentation), no points |
| Week | No build week; updated at the end of every phase (see the phase table in GOVERNANCE.md) |
| Jira epic | [GRC-1](https://340collective.atlassian.net/browse/GRC-1) |
| Mirrored folder | [engineering/Faris-00-Platform-Overview](../../engineering/Faris-00-Platform-Overview/README.md) |
| Lab guide | [LAB-STEPS.md](LAB-STEPS.md) for this folder, and the general guide [shared/labs/README.md](../../shared/labs/README.md) |

Your part: You track what each phase delivered. Collect the build list from each engineer at phase end. Adam (ISSO) accepts the updated overview, since you wrote it.

<details>
<summary>Lab steps summary</summary>

Full steps: [LAB-STEPS.md](LAB-STEPS.md). Mirror: [the other track's lab steps](../../engineering/Faris-00-Platform-Overview/LAB-STEPS.md).

- Define requirements: 2 steps
- Share inputs: 1 step
- Test the build: 1 step
- Operate it: 1 step
- Assess or report: 1 step

</details>

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You, the engineers, and Adam agree on scope. Adam accepts the requirements. Adam reviews the pull request, then you merge it.
- Days 2 to 6, build and code review: talk to each engineer as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to the engineering folder and your phase tracking results to RESULTS.md here. Adam compares them and signs off on the Final report item ("Accepted by: <first name>", or findings).
- Integration week (Nov 23 to 25): record which builds run together in RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-1](https://340collective.atlassian.net/browse/GRC-1).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your requirements and results go in this folder by pull request. Adam reviews them before you merge. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in the engineering README.

0 dollars: documentation only, nothing deploys.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off each build stays running in the shared system. Each engineer removes it only in the end-of-program teardown.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

<details>
<summary>Frameworks covered</summary>

None directly. The overview shows how the projects that cover SOC 2, NIST, and ISO 27001 connect.

</details>

The overview map, its connections, and its build script live in the [engineering README](../../engineering/Faris-00-Platform-Overview/README.md).

![GRC platform overview](../../engineering/Faris-00-Platform-Overview/diagram/grc-platform-overview.png)

## Files

| File | What it is |
| --- | --- |
| [LAB-STEPS.md](LAB-STEPS.md) | Your lab steps: define requirements, share inputs, test the build, operate it, assess or report |
| [Engineering README](../../engineering/Faris-00-Platform-Overview/README.md) | The overview, how the projects connect, and the regenerate commands |
