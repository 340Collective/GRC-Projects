# User Access Reviews - Lab Steps (non-engineering)

Perform a user access review of 340 Collective's AWS identities and record approver sign-off. 340 Collective is the subject organization.

Track: non-engineering (your records go in this folder by pull request). You: Adam (ISSO). Partner: Abdifatah (IAM / Identity Engineer). Mirror: [engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md](../../engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Build an access-certification worksheet with columns: Identity, Type (person, role, service), Group or Role, Access Level, Last Activity, Business Justification, Reviewer Decision (Keep, Reduce, Remove), Approver, Date.
2. Flag over-privilege: anyone with AdministratorAccess who does not need it, unused credentials older than 90 days, access keys on human users, and roles with wildcard permissions.
3. Write the review rules: who approves which identity type, and what counts as a confirmed removal.
4. Write the requirements in REQUIREMENTS.md in this folder and open a pull request. Faris accepts them at the Day 1 kickoff and merges the pull request before Abdifatah starts.

## Share inputs

1. Share these with Abdifatah at kickoff once Faris accepts them: the certification worksheet columns and the review rules.

## Test the build

1. When Abdifatah says the build is ready, run one campaign with Abdifatah's build and check one package per approver, recorded decisions, and no removal without the owner's confirmation.
2. Write your test result, or findings, in RESULTS.md under Test results and open a pull request. Then record your validation on the Final report item.

## Operate it

1. Practice first on the synthetic dataset in [uar-simulation](../../engineering/Abdifatah-08-Access-Reviews/uar-simulation/README.md).
2. Export the current identity list from the 340 Collective AWS account: the IAM credential report, each user's groups (aws iam list-groups-for-user), each user's attached and inline policies, and the list of IAM roles. If project 14 is built, the Okta group and app-assignment export is the identity source for people, and IAM roles are still exported from AWS.
3. Compare the live IAM users, groups, policies, and roles against the access-model template (`infrastructure/cloudformation/grc-access-model.yaml` in this repo; summarized in [shared/access-model/README.md](../../shared/access-model/README.md)), and flag anything that exists live but not in the template as hand-made drift.
4. Have the account owner review each row and record a decision and sign-off.

## Assess or report

1. Log each Reduce or Remove decision as a remediation item with a target date, and record the date it was completed.
2. Commit the signed certification worksheet and the remediation log to this folder by pull request (sanitized only).

## Day 7

Day 7: commit your test and operating results to RESULTS.md in this folder, compare them with FINAL-REPORT.md in the engineering folder, then sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results.

This repo is public. Redact account IDs, ARNs, real resource names, personal emails, and client data before you commit.

## Working with your partner

- Day 1 kickoff: write REQUIREMENTS.md in this folder and open a pull request. You and Abdifatah agree on scope. Faris accepts the requirements and merges the pull request.
- Days 2 to 6, build and code review: talk to Abdifatah as needed, or comment on the project item.
- Day 7 sign-off: Abdifatah commits FINAL-REPORT.md to the engineering folder. You commit your test and operating results to RESULTS.md in this folder, compare them with the engineer's report, and sign off on the Final report item ("Accepted by: <first name>", or findings) with a link to your results. Faris merges the engineer's pull request only after your sign-off. The build stays deployed and running in the shared system.
- Integration week (Nov 23 to 25): check the handoffs across your projects and commit your final results to RESULTS.md.

**Skills:** Identity governance · least privilege · access certification · remediation tracking

**Tools:** AWS Console · AWS CLI · shared/access-model/README.md · IAM credential report · Excel or Google Sheets

**Deliverable:** A signed access-certification worksheet with flagged over-privilege and a remediation log.

**What it simulates:** An IAM or GRC analyst running a quarterly user access review.

You record your work in this folder. The engineer deploys the build from this repo, and it stays running until the end-of-program teardown.
