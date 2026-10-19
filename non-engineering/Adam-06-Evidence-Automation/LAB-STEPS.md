# Audit Evidence Automation - Lab Steps (non-engineering)

Assemble an audit-ready evidence set for 340 Collective from its real AWS account, organized by control. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Maria (Automation Engineer). Mirror: [engineering/Maria-06-Evidence-Automation/LAB-STEPS.md](../../engineering/Maria-06-Evidence-Automation/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Set up an evidence folder structure with one folder per control family (for example, `access-control/`, `logging/`, `encryption/`, `change-management/`, `backup/`) and a naming rule: `<ControlID>_<evidence>_<YYYY-MM-DD>`.
2. Create a control-to-evidence index with columns: Control ID, Control Description, Evidence Item, Source System, Collection Date, Collected By, File Name, Reviewer.
3. Pick the controls the pipeline must cover first and the freshness window for each.
4. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Maria starts.

## Share inputs

1. Share these with Maria at kickoff once Faris accepts them: the control list for evidence mapping.

## Test the build

1. When Maria says the build is ready, check that a sample of controls shows fresh, hashed evidence, the manifest verifies, and an Athena query by control returns the right items.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. Then record your validation on the Final report item.

## Operate it

1. Capture timestamped screenshots and exports from the 340 Collective AWS account: IAM credential report, Identity Center MFA settings, CloudTrail trail status, S3 encryption settings, AWS Config compliance summary, and Security Hub standard scores.
2. Redact account IDs, ARNs, and resource names in every file before it goes into the folder.

## Assess or report

1. Have a second collaborator review each item against the index and sign off in the Reviewer column.
2. Commit the reviewed control-to-evidence index to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Maria agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Maria as needed, or comment on the project item.
- Day 7 sign-off: Maria commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Evidence collection · audit readiness · control mapping · data redaction

**Tools:** AWS Console · IAM · CloudTrail · AWS Config · Security Hub · Excel or Google Sheets

**Deliverable:** A structured evidence folder plus a reviewed control-to-evidence index.

**What it simulates:** A compliance analyst preparing an evidence package ahead of a SOC 2 or ISO audit.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
