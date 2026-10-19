# GRC Platform Overview - Lab Steps (non-engineering)

Track what each phase delivered, so the platform overview stays true. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Faris (ISSM). Partner: each engineer; Adam (ISSO) accepts. Mirror: [engineering/Faris-00-Platform-Overview/LAB-STEPS.md](../../engineering/Faris-00-Platform-Overview/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Set what each phase build list must say per project: folder, pull request, stack name, merged date, running since date (the `live-YYYY-MM-DD` tag), expected monthly cost, and, after the end-of-program teardown, where the teardown evidence is kept.
2. Write these requirements in REQUIREMENTS.md in this folder and open a pull request. Adam accepts them, since you wrote them.

## Share inputs

1. At each phase end, ask each engineer for their phase build list (what merged and is running in the shared system).

## Test the build

1. You do not accept your own work. Adam signs off on the updated overview on the Final report item and gives final approval.

## Operate it

1. Keep a running list of which lines on the overview are built and which are still design intent.

## Assess or report

1. At each phase end, tell the team which projects are merged and running in the shared system, and which come next.

## Day 7

Day 7: commit your phase tracking results to RESULTS.md in this folder. Adam compares them with FINAL-REPORT.md and signs off on the Final report item ("Accepted by: <first name>", or findings).

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You, the engineers, and Adam agree on scope. Adam accepts the requirements. Adam reviews the pull request, then you merge it.
- Days 2 to 6, build and code review: talk to each engineer as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to the engineering folder and your phase tracking results to RESULTS.md here. Adam compares them and signs off on the Final report item ("Accepted by: <first name>", or findings).
- Integration week (Nov 23 to 25): record which builds run together in RESULTS.md.

**Skills:** Program tracking · phase reporting · separation of duties

**Tools:** GitHub pull requests · this repo's project folders · Jira (tracking only)

**Deliverable:** A phase build list per phase and an accepted platform overview.

**What it simulates:** A program owner tracking delivery across a portfolio.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
