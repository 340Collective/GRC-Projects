# Audit Evidence Automation - Lab Steps (non-engineering)

Assemble an audit-ready evidence set for 340 Collective from its real AWS account, organized by control. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-06-Evidence-Automation/LAB-STEPS.md](../../engineering/Maria-06-Evidence-Automation/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Set up an evidence folder structure with one folder per control family (for example, `access-control/`, `logging/`, `encryption/`, `change-management/`, `backup/`) and a naming rule: `<ControlID>_<evidence>_<YYYY-MM-DD>`.
2. Create a control-to-evidence index with columns: Control ID, Control Description, Evidence Item, Source System, Collection Date, Collected By, File Name, Reviewer.
3. Pick the controls the pipeline must cover first and the freshness window for each.
4. Bring the requirements to the Day 1 kickoff. Faris accepts them before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the control list for evidence mapping.

## Test the build

1. When Maria says the build is ready, check that a sample of controls shows fresh, hashed evidence, the manifest verifies, and an Athena query by control returns the right items.
2. Record your test result, or findings, on the project item, then record your validation there.

## Operate it

1. Capture timestamped screenshots and exports from the 340 Collective AWS account: IAM credential report, Identity Center MFA settings, CloudTrail trail status, S3 encryption settings, AWS Config compliance summary, and Security Hub standard scores.
2. Redact account IDs, ARNs, and resource names in every file before it goes into the folder.

## Assess or report

1. Have a second collaborator review each item against the index and sign off in the Reviewer column.
2. Share the reviewed control-to-evidence index with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Maria agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge. The build stays deployed after sign-off and is torn down in the program's final week (Nov 23 to 25, 2026).

**Skills:** Evidence collection · audit readiness · control mapping · data redaction

**Tools:** AWS Console · IAM · CloudTrail · AWS Config · Security Hub · Excel or Google Sheets

**Deliverable:** A structured evidence folder plus a reviewed control-to-evidence index.

**What it simulates:** A compliance analyst preparing an evidence package ahead of a SOC 2 or ISO audit.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
