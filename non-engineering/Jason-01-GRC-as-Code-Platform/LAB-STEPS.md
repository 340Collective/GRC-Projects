# GRC-as-Code Platform - Lab Steps (non-engineering)

Map the SOC 2 Common Criteria to 340 Collective's real AWS environment and capture evidence for each mapped control. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Jason (Internal Auditor). Partner: Faris (ISSM). Mirror: [engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Agree the 01 requirements with Faris at the Day 1 kickoff, so your mapping uses the same ASFF control scope and CC1 to CC9 targets. Adam accepts them; you do not.
2. Create a spreadsheet with columns: Criteria ID, Criteria Summary, AWS Control, How It Is Configured, Evidence Item, Evidence Date, Owner, Status.
3. Add a row for each SOC 2 Common Criteria group, CC1 through CC9, and map at least one 340 Collective AWS control to each (for example, CC6 to IAM Identity Center MFA, CC7 to CloudTrail and Security Hub, CC8 to the GitHub to CloudFormation change path).

## Share inputs

1. Share the mapping sheet with Faris on the Jira epic, so the crosswalk matrix and the [ASFF control matrix](ASFF-Control-Matrix-Indexed.xlsx) use the same criteria IDs.

## Test the build

1. When Faris says the 01 platform is ready, check the Security Hub controls against your CC mapping and add your result as a comment on the project item (pass, or findings). Adam gives final approval, since Faris built it.

## Operate it

1. In the 340 Collective AWS account, confirm and screenshot four baseline controls: MFA on the root user and all human users, CloudTrail enabled in all Regions, default encryption on every S3 bucket, and S3 access or CloudFront logging turned on.
2. Name each screenshot with the criteria ID and date (for example, `CC6-mfa-2026-10-10.png`), redact account IDs and resource names, and link it in the Evidence Item column.

## Assess or report

1. Mark any criteria with no working control as a gap and write one sentence on the fix.
2. Write a half-page summary of coverage: criteria mapped, evidence captured, and open gaps.
3. Share the mapping and the coverage summary with Faris and Adam.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Faris agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** SOC 2 Trust Services Criteria · control mapping · AWS security configuration · evidence capture

**Tools:** AWS Console · IAM Identity Center · CloudTrail · S3 · Security Hub · Excel or Google Sheets

**Deliverable:** SOC 2 control mapping spreadsheet with linked, redacted evidence screenshots and a half-page coverage summary.

**What it simulates:** A GRC analyst preparing a cloud environment for a SOC 2 readiness review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
