# GRC Platform Overview - Lab Steps (engineering)

Keep the platform overview diagram current as each phase merges and tears down its builds. 340 Collective is the subject organization.

Track: engineering. You: Faris (ISSM). Partner: Adam (ISSO), who accepts the overview. Mirror: [non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md](../../non-engineering/Faris-00-Platform-Overview/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. At the end of each phase, read Handoff 1 from each engineer: which builds merged and which were torn down.
2. Decide which boxes and lines change. A line is drawn only when a project's own README or architecture doc names the record it hands over.

## Deploy

1. No stack: 00 is documentation, so nothing deploys to AWS.
2. Edit the labels or lines in `diagram/build_diagram.py`, then rebuild from this folder: `python3 diagram/build_diagram.py diagram/grc-platform-overview`.
3. Update the "How the projects connect" list in the README to match.

## Test

1. The build prints `crossings: 0`, `layout problems: none`, and `sensitive text: none`.
2. Open the PNG and check every label by eye.
3. Run `python3 shared/check_links.py` from the repo root: 0 broken.

## Hand off

1. Open a pull request in this repo; Rasheed or Alex reviews the diagram script change.
2. Create the Handoff 2 Jira Task for Adam. He accepts it and gives final approval, since you wrote it. The pull request merges only after the Task shows his acceptance.

## Tear down

1. Nothing to tear down: 00 has no stack.
2. Confirm with a read-only CloudFormation stack list that no `grc-*` stack from the phase is still running, except the foundation while later phases need it.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: phase build list (what merged and was torn down), each engineer to Faris (Jira Task, created by each engineer)
- Handoff 2: updated platform overview ready for acceptance, Faris to Adam (Jira Task, created by Faris)

**Skills:** Architecture documentation · system-of-systems mapping · diagram as code

**Tools:** Diagram kit (`diagram/build_diagram.py`) · Git · read-only AWS CLI

**Deliverable:** An updated platform overview diagram and README after each phase, accepted by Adam.

**What it simulates:** A GRC lead keeping one current map of how the program's parts connect.

Templates live in the private website repo; nothing in this repo is deployed.
