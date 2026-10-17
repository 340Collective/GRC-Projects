# Compliance-as-Code Guardrails - Lab Steps (non-engineering)

Set the guardrails 340 Collective needs, accept the code that enforces them, and keep the guardrail-to-control register. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Faris (ISSM), who also builds 11. Mirror: [engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md](../../engineering/Faris-11-Compliance-as-Code-Guardrails/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. List six to eight guardrails 340 Collective needs, such as: S3 buckets must block public access unless explicitly approved, S3 buckets must be encrypted, CloudTrail must stay enabled, no IAM users with access keys, and resources must carry an owner tag.
2. For each guardrail, name the control it enforces (SOC 2 or ISO 27001 reference) and who may approve an exception, with an expiry date.
3. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before he starts building.

## Hand over inputs

1. Assign the Handoff 1 Task to Faris once he accepts it: the guardrail list and the control each enforces.

## Accept the build

1. When Faris creates the Handoff 2 Jira Task, read each Rego rule against its passing and failing example templates, each Config rule against your list, and the SCP outline against the actions you asked it to deny.
2. Record your acceptance, or findings, on the Task, then record your validation there. Since Faris built 11, you also give final approval on the Task.

## Operate it

1. Track exceptions: each needs the owner's approval and an expiry date. Flag any that is past its expiry on the Jira epic.

## Assess or report

1. Build a guardrail register with columns: Guardrail ID, Rule Type (Rego, Config, SCP), What It Blocks, Control It Enforces (SOC 2 or ISO 27001 reference), Owner.
2. Create the Handoff 3 Jira Task for Faris with the guardrail-to-control register.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: guardrail list and the control each enforces, Adam to Faris (Jira Task, created by Adam)
- Handoff 2: Rego rules, Config rules, and SCP outline ready for acceptance, Faris to Adam (Jira Task, created by Faris)
- Handoff 3: guardrail-to-control register, Adam to Faris (Jira Task, created by Adam)

**Skills:** Control requirements · guardrail design review · exception management

**Tools:** Excel or Google Sheets · Jira · the 11 architecture doc

**Deliverable:** A guardrail list with control references, an acceptance record for the build, and a guardrail-to-control register.

**What it simulates:** An ISSO setting preventive control requirements and validating their enforcement.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
