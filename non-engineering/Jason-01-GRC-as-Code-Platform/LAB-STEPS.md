# GRC-as-Code Platform - Lab Steps

Map the SOC 2 Common Criteria to 340 Collective's real AWS environment and capture evidence for each mapped control. 340 Collective is the subject organization.

**Lab Steps:**

1. Create a spreadsheet with columns: Criteria ID, Criteria Summary, AWS Control, How It Is Configured, Evidence Item, Evidence Date, Owner, Status.
2. Add a row for each SOC 2 Common Criteria group, CC1 through CC9, and map at least one 340 Collective AWS control to each (for example, CC6 to IAM Identity Center MFA, CC7 to CloudTrail and Security Hub, CC8 to the GitHub to CloudFormation change path).
3. In the 340 Collective AWS account, confirm and screenshot four baseline controls: MFA on the root user and all human users, CloudTrail enabled in all Regions, default encryption on every S3 bucket, and S3 access or CloudFront logging turned on.
4. Name each screenshot with the criteria ID and date (for example, `CC6-mfa-2026-10-10.png`), redact account IDs and resource names, and link it in the Evidence Item column.
5. Mark any criteria with no working control as a gap and write one sentence on the fix.
6. Write a half-page summary of coverage: criteria mapped, evidence captured, and open gaps.

**Skills:** SOC 2 Trust Services Criteria · control mapping · AWS security configuration · evidence capture

**Tools:** AWS Console · IAM Identity Center · CloudTrail · S3 · Security Hub · Excel or Google Sheets

**Deliverable:** SOC 2 control mapping spreadsheet with linked, redacted evidence screenshots and a half-page coverage summary.

**What it simulates:** A GRC analyst preparing a cloud environment for a SOC 2 readiness review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
