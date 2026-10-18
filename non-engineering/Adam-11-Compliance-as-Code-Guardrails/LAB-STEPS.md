# Compliance-as-Code Guardrails - Lab Steps (non-engineering)

Set the guardrails 340 Collective needs, accept the code that enforces them, and keep the guardrail-to-control register. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Faris (ISSM), who also builds 11. Mirror: [engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md](../../engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. List six to eight guardrails 340 Collective needs, such as: S3 buckets must block public access unless explicitly approved, S3 buckets must be encrypted, CloudTrail must stay enabled, no IAM users with access keys, and resources must carry an owner tag.
2. For each guardrail, name the control it enforces (SOC 2 or ISO 27001 reference) and who may approve an exception, with an expiry date.
3. Bring the requirements to the Day 1 kickoff. Faris accepts them before he starts building.

## Share inputs

1. Share these with Faris at kickoff once he accepts them: the guardrail list and the control each enforces.

## Test the build

1. When Faris says the build is ready, read each Rego rule against its passing and failing example templates, each Config rule against your list, and the SCP outline against the actions you asked it to deny.
2. Record your test result, or findings, on the project item, then record your validation there. Since Faris built 11, you also give final approval on the project item.

## Operate it

1. Track exceptions: each needs the owner's approval and an expiry date. Flag any that is past its expiry on the Jira epic.

## Assess or report

1. Build a guardrail register with columns: Guardrail ID, Rule Type (Rego, Config, SCP), What It Blocks, Control It Enforces (SOC 2 or ISO 27001 reference), Owner.
2. Share the guardrail-to-control register with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Faris agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Control requirements · guardrail design review · exception management

**Tools:** Excel or Google Sheets · Jira · the 11 architecture doc

**Deliverable:** A guardrail list with control references, an acceptance record for the build, and a guardrail-to-control register.

**What it simulates:** An ISSO setting preventive control requirements and validating their enforcement.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
