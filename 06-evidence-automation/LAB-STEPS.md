# Audit Evidence Automation - Lab Steps

Assemble an audit-ready evidence set for 340 Collective from its real AWS account, organized by control. 340 Collective is the subject organization.

**Lab Steps:**

1. Set up an evidence folder structure with one folder per control family (for example, `access-control/`, `logging/`, `encryption/`, `change-management/`, `backup/`) and a naming rule: `<ControlID>_<evidence>_<YYYY-MM-DD>`.
2. Create a control-to-evidence index with columns: Control ID, Control Description, Evidence Item, Source System, Collection Date, Collected By, File Name, Reviewer.
3. Capture timestamped screenshots and exports from the 340 Collective AWS account: IAM credential report, Identity Center MFA settings, CloudTrail trail status, S3 encryption settings, AWS Config compliance summary, and Security Hub standard scores.
4. Redact account IDs, ARNs, and resource names in every file before it goes into the folder.
5. Have a second collaborator review each item against the index and sign off in the Reviewer column.

**Skills:** Evidence collection · audit readiness · control mapping · data redaction

**Tools:** AWS Console · IAM · CloudTrail · AWS Config · Security Hub · Excel or Google Sheets

**Deliverable:** A structured evidence folder plus a reviewed control-to-evidence index.

**What it simulates:** A compliance analyst preparing an evidence package ahead of a SOC 2 or ISO audit.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
