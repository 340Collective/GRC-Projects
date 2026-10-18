# User Access Reviews - Lab Steps (non-engineering)

Perform a user access review of 340 Collective's AWS identities and record approver sign-off. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Abdifatah (IAM / Identity Engineer). Mirror: [engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md](../../engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Build an access-certification worksheet with columns: Identity, Type (person, role, service), Group or Role, Access Level, Last Activity, Business Justification, Reviewer Decision (Keep, Reduce, Remove), Approver, Date.
2. Flag over-privilege: anyone with AdministratorAccess who does not need it, unused credentials older than 90 days, access keys on human users, and roles with wildcard permissions.
3. Write the review rules: who approves which identity type, and what counts as a confirmed removal.
4. Bring the requirements to the Day 1 kickoff. Faris accepts them before Abdifatah starts.

## Share inputs

1. Share these with Abdifatah at kickoff once Faris accepts them: the certification worksheet columns and the review rules.

## Test the build

1. When Abdifatah says the build is ready, run one campaign with Abdifatah's build and check one package per approver, recorded decisions, and no removal without the owner's confirmation.
2. Record your test result, or findings, on the project item, then record your validation there.

## Operate it

1. Practice first on the synthetic dataset in [uar-simulation](../../engineering/Abdifatah-08-Access-Reviews/uar-simulation/README.md).
2. Export the current identity list from the 340 Collective AWS account: the IAM credential report, each user's groups (aws iam list-groups-for-user), each user's attached and inline policies, and the list of IAM roles. If project 14 is built, the Okta group and app-assignment export is the identity source for people, and IAM roles are still exported from AWS.
3. Compare the live IAM users, groups, policies, and roles against the access-model template (`infrastructure/cloudformation/grc-access-model.yaml` in this repo; summarized in [shared/access-model/README.md](../../shared/access-model/README.md)), and flag anything that exists live but not in the template as hand-made drift.
4. Have the account owner review each row and record a decision and sign-off.

## Assess or report

1. Log each Reduce or Remove decision as a remediation item with a target date, and record the date it was completed.
2. Share the signed certification worksheet and the remediation log with Faris.

## Day 7

Day 7: add the operating results to the engineer's FINAL-REPORT.md, then sign off as a comment on the Final report item ("Accepted by: <first name>", or findings).

## Working with your partner

- Day 1 kickoff: you and Abdifatah agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Abdifatah as needed, or comment on the project item.
- Day 7 sign-off: Abdifatah fills in FINAL-REPORT.md, you review it and sign off ("Accepted by: <first name>", or findings) as a comment on the Final report item, then merge and tear down.

**Skills:** Identity governance · least privilege · access certification · remediation tracking

**Tools:** AWS Console · AWS CLI · shared/access-model/README.md · IAM credential report · Excel or Google Sheets

**Deliverable:** A signed access-certification worksheet with flagged over-privilege and a remediation log.

**What it simulates:** An IAM or GRC analyst running a quarterly user access review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
