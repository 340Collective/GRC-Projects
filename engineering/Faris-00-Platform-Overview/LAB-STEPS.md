# GRC Platform Overview - Lab Steps (engineering)

Keep the platform overview diagram current as each phase merges its builds into the running system. 340 Collective is the subject organization.

Track: engineering. You: Faris (ISSM). Partner: Adam (ISSO), who accepts the overview. Mirror: [non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md](../../non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. At the end of each phase, ask each engineer which builds merged and are running in the shared system (their FINAL-REPORT.md says so).
2. Decide which boxes and lines change. A line is drawn only when a project's own README or architecture doc names the record it hands over.

## Deploy

1. No stack: 00 is documentation, so nothing deploys to AWS.
2. Edit the labels or lines in `diagram/build_diagram.py`, then rebuild from this folder: `python3 diagram/build_diagram.py diagram/grc-platform-overview`.
3. Update the "How the projects connect" list in the README to match.

## Test

1. The build prints `crossings: 0`, `layout problems: none`, and `sensitive text: none`.
2. Open the PNG and check every label by eye.
3. Run `python3 shared/check_links.py` from the repo root: 0 broken.

## Partner test

1. Open a pull request in this repo; Rasheed (Maria as backup) reviews the diagram script change.
2. Ask Adam to review it. He signs off and gives final approval, since you wrote it. The pull request merges only after his sign-off is on the Final report item.

## End-of-program teardown

1. Nothing to tear down: 00 has no stack.
2. At each phase end, confirm with a read-only CloudFormation stack list that every signed-off `grc-*` stack from the phase is running, and that no test-only stack is left. At the end-of-program teardown, confirm that every `grc-*` project stack is gone, with `grc-foundation` deleted last.

## Day 7

At each phase end (00 has no build week): copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item and Adam gives final approval.

## Working with your partner

- Day 1 kickoff: you write REQUIREMENTS.md in the non-engineering 00 folder, and Adam accepts it. You and Adam agree on scope.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- At each phase end: you commit FINAL-REPORT.md to this folder and your phase tracking results to the non-engineering 00 folder. Adam compares them and signs off on the Final report item ("Accepted by: <first name>", or findings). Adam gives final approval, and Faris merges after it.

**Skills:** Architecture documentation · system-of-systems mapping · diagram as code

**Tools:** Diagram kit (`diagram/build_diagram.py`) · Git · read-only AWS CLI

**Deliverable:** An updated platform overview diagram and README after each phase, accepted by Adam.

**What it simulates:** A GRC lead keeping one current map of how the program's parts connect.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
