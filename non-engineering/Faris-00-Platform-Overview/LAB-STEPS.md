# GRC Platform Overview - Lab Steps (non-engineering)

Track what each phase delivered, so the platform overview stays true. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Faris (ISSM). Partner: each engineer; Adam (ISSO) accepts. Mirror: [engineering/Faris-00-Platform-Overview/LAB-STEPS.md](../../engineering/Faris-00-Platform-Overview/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Set what each phase build list must say per project: folder, pull request, stack name, merged date, teardown date, and where the teardown evidence is kept.
2. Put these requirements on the epic for Adam; he accepts them, since you wrote them.

## Hand over inputs

1. At each phase end, ask each engineer for Handoff 1.

## Accept the build

1. You do not accept your own work. Adam accepts the updated overview on the Handoff 2 Task and gives final approval.

## Operate it

1. Keep a running list of which lines on the overview are built and which are still design intent.

## Assess or report

1. At each phase end, tell the team which projects are merged and torn down, and which come next.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: phase build list (what merged and was torn down), each engineer to Faris (Jira Task, created by each engineer)
- Handoff 2: updated platform overview ready for acceptance, Faris to Adam (Jira Task, created by Faris)

**Skills:** Program tracking · phase reporting · separation of duties

**Tools:** Jira · GitHub pull requests (read) · this repo's project folders

**Deliverable:** A phase build list per phase and an accepted platform overview.

**What it simulates:** A program owner tracking delivery across a portfolio.

Templates live in this repo's `infrastructure/` folder and deploy only from clean `main` after approval; nothing deploys from a branch.
