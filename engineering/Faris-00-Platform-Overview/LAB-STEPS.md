# GRC Platform Overview - Lab Steps (engineering)

Keep the platform overview diagram current as each phase merges its builds. 340 Collective is the subject organization.

Track: engineering. You: Faris (ISSM). Partner: Adam (ISSO), who accepts the overview. Mirror: [non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md](../../non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. At the end of each phase, ask each engineer which builds merged and which stacks are still deployed (their FINAL-REPORT.md says so; every signed-off stack stays up until the final week).
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

## Tear down (final week)

1. Nothing to tear down: 00 has no stack.
2. At each phase end, confirm with a read-only CloudFormation stack list that every running `grc-*` stack is a signed-off build or a current active build. In the final week, confirm every `grc-*` project stack is gone, with `grc-foundation` deleted last.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in, get your partner's sign-off on the Final report item, merge it.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you fill in FINAL-REPORT.md, Adam reviews it and signs off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge.

**Skills:** Architecture documentation · system-of-systems mapping · diagram as code

**Tools:** Diagram kit (`diagram/build_diagram.py`) · Git · read-only AWS CLI

**Deliverable:** An updated platform overview diagram and README after each phase, accepted by Adam.

**What it simulates:** A GRC lead keeping one current map of how the program's parts connect.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, keeps it deployed after sign-off, and tears it down in the program's final week; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
