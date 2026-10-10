# User Access Reviews - Lab Steps

Perform a user access review of 340 Collective's AWS identities and record approver sign-off. 340 Collective is the subject organization.

**Lab Steps:**

1. Export the current identity list from the 340 Collective AWS account: IAM Identity Center users, groups, and permission set assignments, plus the IAM credential report for any IAM users and the list of IAM roles.
2. Build an access-certification worksheet with columns: Identity, Type (person, role, service), Group or Permission Set, Access Level, Last Activity, Business Justification, Reviewer Decision (Keep, Reduce, Remove), Approver, Date.
3. Flag over-privilege: anyone with AdministratorAccess who does not need it, unused credentials older than 90 days, access keys on human users, and roles with wildcard permissions.
4. Have the account owner review each row and record a decision and sign-off.
5. Log each Reduce or Remove decision as a remediation item with a target date, and record the date it was completed.

**Skills:** Identity governance · least privilege · access certification · remediation tracking

**Tools:** AWS Console · IAM Identity Center · IAM credential report · Excel or Google Sheets

**Deliverable:** A signed access-certification worksheet with flagged over-privilege and a remediation log.

**What it simulates:** An IAM or GRC analyst running a quarterly user access review.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
