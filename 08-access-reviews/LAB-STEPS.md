# User Access Reviews - Lab Steps

Perform a user access review of 340 Collective's AWS identities and record approver sign-off. 340 Collective is the subject organization.

**Lab Steps:**

1. Export the current identity list from the 340 Collective AWS account: the IAM credential report, each user's groups (aws iam list-groups-for-user), each user's attached and inline policies, and the list of IAM roles. If project 14 is built, the Okta group export is the identity source for people, and IAM roles are still exported from AWS.
2. Compare the live IAM users, groups, policies, and roles against access-model/grc-access.yaml, and flag anything that exists live but not in the template as hand-made drift.
3. Build an access-certification worksheet with columns: Identity, Type (person, role, service), Group or Role, Access Level, Last Activity, Business Justification, Reviewer Decision (Keep, Reduce, Remove), Approver, Date.
4. Flag over-privilege: anyone with AdministratorAccess who does not need it, unused credentials older than 90 days, access keys on human users, and roles with wildcard permissions.
5. Have the account owner review each row and record a decision and sign-off.
6. Log each Reduce or Remove decision as a remediation item with a target date, and record the date it was completed.

**Skills:** Identity governance · least privilege · access certification · remediation tracking

**Tools:** AWS Console · AWS CLI · access-model/grc-access.yaml · IAM credential report · Excel or Google Sheets

**Deliverable:** A signed access-certification worksheet with flagged over-privilege and a remediation log.

**What it simulates:** An IAM or GRC analyst running a quarterly user access review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
