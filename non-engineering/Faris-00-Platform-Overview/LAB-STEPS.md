# GRC Platform Overview - Lab Steps (non-engineering)

Track what each phase delivered, so the platform overview stays true. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Faris (ISSM). Partner: each engineer; Adam (ISSO) accepts. Mirror: [engineering/Faris-00-Platform-Overview/LAB-STEPS.md](../../engineering/Faris-00-Platform-Overview/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Set what each phase build list must say per project: folder, pull request, stack name, merged date, whether the stack is still deployed, and, after the final week, the teardown date and where the teardown evidence is kept.
2. Put these requirements on the epic for Adam; he accepts them, since you wrote them.

## Share inputs

1. At each phase end, ask each engineer for their phase build list (what merged and which stacks are still deployed).

## Test the build

1. You do not accept your own work. Adam signs off on the updated overview on the Final report item and gives final approval.

## Operate it

1. Keep a running list of which lines on the overview are built and which are still design intent.

## Assess or report

1. At each phase end, tell the team which projects are merged and still deployed, and which come next. In the final week, report which stacks are torn down.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md; Adam signs off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you, the engineers, and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to each engineer as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge.

**Skills:** Program tracking · phase reporting · separation of duties

**Tools:** Jira · GitHub pull requests (read) · this repo's project folders

**Deliverable:** A phase build list per phase and an accepted platform overview.

**What it simulates:** A program owner tracking delivery across a portfolio.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, keeps it deployed after sign-off, and tears it down in the program's final week; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
