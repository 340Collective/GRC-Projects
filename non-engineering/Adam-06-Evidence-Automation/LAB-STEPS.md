# Audit Evidence Automation - Lab Steps (non-engineering)

Assemble an audit-ready evidence set for 340 Collective from its real AWS account, organized by control. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-06-Evidence-Automation/LAB-STEPS.md](../../engineering/Maria-06-Evidence-Automation/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Set up an evidence folder structure with one folder per control family (for example, `access-control/`, `logging/`, `encryption/`, `change-management/`, `backup/`) and a naming rule: `<ControlID>_<evidence>_<YYYY-MM-DD>`.
2. Create a control-to-evidence index with columns: Control ID, Control Description, Evidence Item, Source System, Collection Date, Collected By, File Name, Reviewer.
3. Pick the controls the pipeline must cover first and the freshness window for each.
4. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Maria starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Maria once Faris accepts it: the control list for evidence mapping.

## Accept the build

1. When Maria creates the Handoff 2 Jira Task, check that a sample of controls shows fresh, hashed evidence, the manifest verifies, and an Athena query by control returns the right items.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Capture timestamped screenshots and exports from the 340 Collective AWS account: IAM credential report, Identity Center MFA settings, CloudTrail trail status, S3 encryption settings, AWS Config compliance summary, and Security Hub standard scores.
2. Redact account IDs, ARNs, and resource names in every file before it goes into the folder.

## Assess or report

1. Have a second collaborator review each item against the index and sign off in the Reviewer column.
2. Create the Handoff 3 Jira Task for Faris with the reviewed control-to-evidence index.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md and accept in Jira.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: control list for evidence mapping, Adam to Maria (Jira Task, created by Adam)
- Handoff 2: evidence pipeline ready for acceptance, Maria to Adam (Jira Task, created by Maria)
- Handoff 3: reviewed control-to-evidence index, Adam to Faris (Jira Task, created by Adam)

**Skills:** Evidence collection · audit readiness · control mapping · data redaction

**Tools:** AWS Console · IAM · CloudTrail · AWS Config · Security Hub · Excel or Google Sheets

**Deliverable:** A structured evidence folder plus a reviewed control-to-evidence index.

**What it simulates:** A compliance analyst preparing an evidence package ahead of a SOC 2 or ISO audit.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
