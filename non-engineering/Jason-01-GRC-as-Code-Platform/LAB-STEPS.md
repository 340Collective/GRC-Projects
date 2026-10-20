# GRC-as-Code Platform - Lab Steps (non-engineering)

Map the SOC 2 Common Criteria to 340 Collective's real AWS environment and capture evidence for each mapped control. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Jason (Internal Auditor). Partner: Faris (ISSM). Mirror: [engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md](../../engineering/Faris-01-GRC-as-Code-Platform/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Write the 01 requirements and agree scope with Faris at the Day 1 kickoff, so your mapping uses the same ASFF control scope and CC1 to CC9 targets. Adam accepts them; you and Faris do not. Write them in REQUIREMENTS.md in this folder by pull request.
2. Create a spreadsheet with columns: Criteria ID, Criteria Summary, AWS Control, How It Is Configured, Evidence Item, Evidence Date, Owner, Status.
3. Add a row for each SOC 2 Common Criteria group, CC1 through CC9, and map at least one 340 Collective AWS control to each (for example, CC6 to IAM Identity Center MFA, CC7 to CloudTrail and Security Hub, CC8 to the GitHub to CloudFormation change path).

## Share inputs

1. Commit the mapping sheet to this folder by pull request, so the crosswalk matrix and the [ASFF control matrix](ASFF-Control-Matrix-Indexed.xlsx) use the same criteria IDs.

## Test the build

1. When Faris says the 01 platform is ready, check the Security Hub controls against your CC mapping and write your result in RESULTS.md (pass, or findings). Adam gives final approval, since Faris built it.

## Operate it

1. In the 340 Collective AWS account, confirm and screenshot four baseline controls: MFA on the root user and all human users, CloudTrail enabled in all Regions, default encryption on every S3 bucket, and S3 access or CloudFront logging turned on.
2. Name each screenshot with the criteria ID and date (for example, `CC6-mfa-2026-10-10.png`), redact account IDs and resource names, and link it in the Evidence Item column.

## Assess or report

1. Mark any criteria with no working control as a gap and write one sentence on the fix.
2. Write a half-page summary of coverage: criteria mapped, evidence captured, and open gaps.
3. Commit the mapping and the coverage summary to this folder by pull request, and tell Faris and Adam.

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Faris agree on scope. Adam accepts the requirements, and Faris merges the pull request.
- Days 2 to 6, build and code review: talk to Faris as needed, or comment on the project item.
- Day 7 sign-off: Faris commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item (pass, or findings) with a link to your results. It is not an approval. Faris merges the final report pull request only after your sign-off and Adam's final approval. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md. Add your independent assessment to `non-engineering/Jason-04-Gap-Analysis/assessments/`.

**Skills:** SOC 2 Trust Services Criteria · control mapping · AWS security configuration · evidence capture

**Tools:** AWS Console · IAM Identity Center · CloudTrail · S3 · Security Hub · Excel or Google Sheets

**Deliverable:** SOC 2 control mapping spreadsheet with linked, redacted evidence screenshots and a half-page coverage summary.

**What it simulates:** A GRC analyst preparing a cloud environment for a SOC 2 readiness review.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
