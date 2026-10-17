# User Access Reviews - Lab Steps (non-engineering)

Perform a user access review of 340 Collective's AWS identities and record approver sign-off. 340 Collective is the subject organization.

Track: non-engineering (you work in Jira). You: Adam (ISSO). Partner: Abdifatah (IAM / Identity Engineer). Mirror: [engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md](../../engineering/Abdifatah-08-Access-Reviews/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Define requirements

1. Build an access-certification worksheet with columns: Identity, Type (person, role, service), Group or Role, Access Level, Last Activity, Business Justification, Reviewer Decision (Keep, Reduce, Remove), Approver, Date.
2. Flag over-privilege: anyone with AdministratorAccess who does not need it, unused credentials older than 90 days, access keys on human users, and roles with wildcard permissions.
3. Write the review rules: who approves which identity type, and what counts as a confirmed removal.
4. Put the requirements on the Handoff 1 Jira Task. Faris accepts them on the Task before Abdifatah starts.

## Hand over inputs

1. Assign the Handoff 1 Task to Abdifatah once Faris accepts it: the certification worksheet columns and the review rules.

## Accept the build

1. When Abdifatah creates the Handoff 2 Jira Task, run one campaign with Abdifatah's build and check one package per approver, recorded decisions, and no removal without the owner's confirmation.
2. Record your acceptance, or findings, on the Task, then record your validation there.

## Operate it

1. Practice first on the synthetic dataset in [uar-simulation](../../engineering/Abdifatah-08-Access-Reviews/uar-simulation/README.md).
2. Export the current identity list from the 340 Collective AWS account: the IAM credential report, each user's groups (aws iam list-groups-for-user), each user's attached and inline policies, and the list of IAM roles. If project 14 is built, the Okta group and app-assignment export is the identity source for people, and IAM roles are still exported from AWS.
3. Compare the live IAM users, groups, policies, and roles against the access-model template (`infrastructure/cloudformation/grc-access-model.yaml` in this repo; summarized in [shared/access-model/README.md](../../shared/access-model/README.md)), and flag anything that exists live but not in the template as hand-made drift.
4. Have the account owner review each row and record a decision and sign-off.

## Assess or report

1. Log each Reduce or Remove decision as a remediation item with a target date, and record the date it was completed.
2. Create the Handoff 3 Jira Task for Faris with the signed certification worksheet and the remediation log.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: certification worksheet columns and review rules, Adam to Abdifatah (Jira Task, created by Adam)
- Handoff 2: access review package build ready for acceptance, Abdifatah to Adam (Jira Task, created by Abdifatah)
- Handoff 3: signed certification worksheet and remediation log, Adam to Faris (Jira Task, created by Adam)

**Skills:** Identity governance · least privilege · access certification · remediation tracking

**Tools:** AWS Console · AWS CLI · shared/access-model/README.md · IAM credential report · Excel or Google Sheets

**Deliverable:** A signed access-certification worksheet with flagged over-privilege and a remediation log.

**What it simulates:** An IAM or GRC analyst running a quarterly user access review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
