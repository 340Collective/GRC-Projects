# GRC-as-Code Platform - Lab Steps (engineering)

Build and test the GRC-as-Code Platform design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Faris (ISSM). Partner: Jason (Internal Auditor). Mirror: [non-engineering/Jason-01-GRC-as-Code-Platform/LAB-STEPS.md](../../non-engineering/Jason-01-GRC-as-Code-Platform/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Write the foundation requirements and bring them to the Day 1 kickoff. Jason writes the 01 requirements and agrees scope with you (ASFF control scope, SOC 2 CC1 to CC9 targets). Adam accepts both; you do not accept your own.
2. Read the [architecture doc](GRC-Platform-Architecture.md). Its build order names Terraform and GitHub Actions; here every stack is CloudFormation in this repo's `infrastructure/cloudformation/` folder.
3. Design the shared foundation every later build reuses: the deploy pipeline, one KMS key tagged `grc-project`, logging (CloudTrail stays on), the temporary evidence bucket pattern, and the access model.
4. Build the control crosswalk matrix (JSON) from the [ASFF control matrix](../../non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx).
5. Jira path 1: findings reach Jira through the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html). 01 and 04 Config posture findings use it.
6. Jira path 2: project events reach Jira through an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook. The design's Jira creator and approval loop use this path.
7. Do not use the AWS Service Management Connector (AWS retires it after 2027-03-31). Keep any Jira API token out of git: an EventBridge connection keeps it in Secrets Manager (about 0.40 dollars a month; Secrets Manager is on the access model's deny list today, so confirm or raise an access-change PR), and a Lambda that calls Jira reads it from an SSM SecureString parameter under `/grc/`.
8. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
9. Plan to stay under 10 dollars a month: the design's estimate is about 75 to 120 dollars a month if Config, Security Hub, GuardDuty, and Inspector stay on. Keep them in cheap mode in the running system, and scale them down or pause them when a budget alert fires.

## Deploy

1. Foundation (Phase 1): write `infrastructure/cloudformation/grc-foundation.yaml` in this repo:
   - KMS key tagged `grc-project`
   - the temporary evidence bucket pattern: versioned, private, SSE-KMS, no Object Lock and no legal hold, current objects expire after 30 days, noncurrent versions after 7 days, incomplete multipart uploads after 1 day, DeletionPolicy and UpdateReplacePolicy Delete
   - logging settings that keep CloudTrail on
2. 01 platform (Phase 2): write `infrastructure/cloudformation/grc-platform.yaml` in the build order from the architecture doc:
   - Base Terraform modules: Config + Security Hub + EventBridge
   - Lambda functions: Jira creator + dedup logic
   - CI/CD pipeline: GitHub Actions with approval gates
   - Okta integration: Identity audit Lambda
   - Audit Manager: Framework definitions + evidence automation
   - Jira approval loop: Webhook → pipeline resume
   - SLA enforcement: Cron-based breach detection
3. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
4. Open a pull request to `main` in this repo; Rasheed does the code review (Maria as backup). Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
5. After Adam's approval (he approves Faris-built work), deploy each stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Foundation: put a test object in a bucket made from the pattern and confirm versioning, SSE-KMS with the `grc-project` key, no Object Lock, the lifecycle rules, and that the SHA-256 hash and manifest verify.
2. Confirm CloudTrail records the test writes.
3. 01: raise one synthetic finding (for example a failing Config rule) and follow it through Security Hub, EventBridge, the control mapper, and one Jira issue, with the approval gate before any change deploys.
4. Check the budget's actual spend and record it in FINAL-REPORT.md section 6. If an alert has fired, follow the [running system cost](../../GOVERNANCE.md#running-system-cost) rule.

## Partner test

1. Walk Rasheed through the foundation; he is the named backup and can run or finish it if you are out.
2. Ask Adam to review the foundation, and later the 01 platform. He commits his foundation results to [non-engineering/Adam-Foundation/RESULTS.md](../../non-engineering/Adam-Foundation/RESULTS.md) and gives final approval on both, since you built them.
3. Jason commits his SOC 2 mapping and coverage assessment to his own folder and links it on the project item.
4. Put the build notes (what was deployed and the test results; no secrets or raw evidence) in FINAL-REPORT.md sections 3 and 7, in the Day 7 pull request. It merges only after Jason's sign-off and Adam's final approval are on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off `grc-platform` stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket, including all object versions and delete markers.
3. Delete `grc-platform` from clean `main` and wait for `DELETE_COMPLETE`. Keep `grc-foundation` while any later phase still uses it, and delete it last.
4. Turn off the Config recorder, Security Hub, GuardDuty, Inspector, and Audit Manager if this build turned them on.
5. Record teardown evidence where the ISSM designates, outside git, and note it on the project item.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item and Adam gives final approval.

## Working with your partner

- Day 1 kickoff: Jason writes REQUIREMENTS.md in his own folder, and Adam accepts it, since you build 01. You and Jason agree on scope.
- Days 2 to 6, build and code review: talk to Jason as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Jason commits his results to his own folder, compares them with your report, and signs off on the Final report item (pass, or findings, not an approval). Adam gives final approval, and Faris merges after it. The build stays deployed and running in the shared system.

**Skills:** CloudFormation · Security Hub and ASFF · EventBridge routing · KMS and S3 hardening · deploy pipeline design

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · cfn-lint · Security Hub · Config · EventBridge · Lambda · KMS · S3 · Jira

**Deliverable:** The shared foundation stack and the 01 Security Hub platform stack, tested, accepted by Adam, and running in the shared system.

**What it simulates:** A GRC engineer standing up the shared platform other builds rest on.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
