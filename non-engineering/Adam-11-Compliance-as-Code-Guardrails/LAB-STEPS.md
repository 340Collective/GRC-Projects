# Compliance-as-Code Guardrails - Lab Steps (non-engineering)

Set the guardrails 340 Collective needs, accept the code that enforces them, and keep the guardrail-to-control register. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Faris (ISSM), who also builds 11. Mirror: [engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md](../../engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. List six to eight guardrails 340 Collective needs, such as: S3 buckets must block public access unless explicitly approved, S3 buckets must be encrypted, CloudTrail must stay enabled, no IAM users with access keys, and resources must carry an owner tag.
2. For each guardrail, name the control it enforces (SOC 2 or ISO 27001 reference) and who may approve an exception, with an expiry date.
3. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before he starts building.

## Share inputs

1. Share these with Faris at kickoff once he accepts them: the guardrail list and the control each enforces.

## Test the build

1. When Faris says the build is ready, read each Rego rule against its passing and failing example templates, each Config rule against your list, and the SCP outline against the actions you asked it to deny.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. Then record your validation on the Final report item. Since Faris built 11, you also give final approval on the Final report item.

## Operate it

1. Track exceptions: each needs the owner's approval and an expiry date. Flag any that is past its expiry on the Jira epic.

## Assess or report

1. Build a guardrail register with columns: Guardrail ID, Rule Type (Rego, Config, SCP), What It Blocks, Control It Enforces (SOC 2 or ISO 27001 reference), Owner.
2. Commit the guardrail-to-control register to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Faris agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off and final approval. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Control requirements · guardrail design review · exception management

**Tools:** Excel or Google Sheets · Jira · the 11 architecture doc

**Deliverable:** A guardrail list with control references, an acceptance record for the build, and a guardrail-to-control register.

**What it simulates:** An ISSO setting preventive control requirements and validating their enforcement.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
