# Shared Foundation (non-engineering)

You push your own work to GitHub, in this folder, by pull request. Jira epic [GRC-30](https://340collective.atlassian.net/browse/GRC-30) is for task tracking only.

| Field | Value |
| --- | --- |
| Project | Shared foundation (part of 01 GRC-as-Code Platform) |
| Your role | Adam (ISSO), partner: acceptance, validation, final approval, operation, and reporting |
| Your partner | Faris (ISSM), who builds the foundation |
| Reviewer or validator | You accept Faris's FOUNDATION-REQUIREMENTS.md at the Day 1 kickoff, since he wrote it. You sign off, validate, and give final approval on the Final report item, since Faris built it. Faris reviews and merges your pull requests. |
| Phase | Phase 1, 3 points (L) |
| Week | Week 1, Oct 19 to 25, 2026 |
| Jira epic | [GRC-30](https://340collective.atlassian.net/browse/GRC-30) |
| Mirrored folder | [engineering/Faris-01-GRC-as-Code-Platform](../../engineering/Faris-01-GRC-as-Code-Platform/README.md) (the foundation half) |
| Requirements | [FOUNDATION-REQUIREMENTS.md](../../engineering/Faris-01-GRC-as-Code-Platform/FOUNDATION-REQUIREMENTS.md), written by Faris. Each requirement has an acceptance check that names the evidence you will see. |

Your part: You accept the foundation requirements, test the build against their acceptance checks, and record your results here. Work with Faris. Jason is the partner for the 01 platform, not for the foundation.

## What you do, where it goes, who checks it

| Question | Answer |
| --- | --- |
| What do I do? | Accept FOUNDATION-REQUIREMENTS.md at the Day 1 kickoff. Test the build against its acceptance checks. Record your results in [RESULTS.md](RESULTS.md). Sign off, validate, and give final approval on the Final report item. |
| Where does it go? | This folder, `non-engineering/Adam-Foundation/`, by pull request (see [CONTRIBUTING.md](../../CONTRIBUTING.md#partner-pull-requests)). Your acceptance, sign-off, validation, and final approval go on the foundation's Final report item. |
| Who checks it? | Faris reviews and merges your pull requests. Engineers never review or approve your records. |

<details>
<summary>Working with your partner</summary>

- Day 1 kickoff: Faris brings FOUNDATION-REQUIREMENTS.md. You accept it, or list findings, on the Final report item.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the final report pull request only after your sign-off and final approval. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

</details>

<details>
<summary>Jira</summary>

- Epic: [GRC-30](https://340collective.atlassian.net/browse/GRC-30).
- Ask your partner directly or comment on the project item. Jira is for task tracking only. Your results go in this folder by pull request, and Faris reviews and merges them. Engineers never edit this folder. This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

</details>

<details>
<summary>Cost</summary>

Your side costs nothing. The build's cost is in FOUNDATION-REQUIREMENTS.md.

The program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars.

</details>

<details>
<summary>End-of-program teardown</summary>

- After sign-off the foundation stays running in the shared system, because every later build uses it. Faris removes it only in the end-of-program teardown, last, after every other `grc-*` project stack.
- At the end-of-program teardown, confirm on the project item that the teardown evidence is recorded.

</details>

## About the project

The shared foundation is the base every later build reuses: the deploy pipeline, one KMS key tagged `grc-project`, logging that keeps CloudTrail on, the temporary evidence bucket pattern, and the access model.

Status: target design, not yet deployed.

## Files

| File | What it is |
| --- | --- |
| [RESULTS.md](RESULTS.md) | Your test, operating, and final results |
| [FOUNDATION-REQUIREMENTS.md](../../engineering/Faris-01-GRC-as-Code-Platform/FOUNDATION-REQUIREMENTS.md) | The requirements and acceptance checks you accept and test against |
| [Engineering lab steps](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md) | Faris's lab steps for the foundation and 01 |
