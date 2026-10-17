# 340 Collective Gap Analysis - Lab Steps

Run a mini compliance program gap analysis of 340 Collective against ISO 27001 Annex A or NIST CSF and produce a scored control matrix. 340 Collective is the subject organization.

**Lab Steps:**

1. Pick one framework (ISO 27001:2022 Annex A or NIST CSF 2.0) and write a 1-page scope summary: systems in scope (the 340collective.com website, the AWS account, Stripe, Google Workspace, GitHub), people in scope, and exclusions.
2. Create a control matrix with columns: Control ID, Requirement, Current Status (Met, Partial, Not Met), Owner, Action Needed.
3. Select at least 15 controls that apply to a small cloud-hosted business, such as access control, MFA, logging, backup, encryption, vendor management, incident response, and policy review.
4. Assess each control against 340 Collective's real setup by checking the AWS Console, GitHub settings, and existing policies. Note the evidence you looked at.
5. Mark every gap, assign an owner, and write a specific action for each (for example, "Enable AWS Config in all Regions").
6. Sort the gaps by priority and add a short remediation timeline at the bottom of the matrix.

**Skills:** ISO 27001 or NIST CSF · scoping · gap assessment · remediation planning

**Tools:** Excel or Google Sheets · Google Docs or Word · AWS Console (read-only) · GitHub settings

**Deliverable:** A 15+ control matrix with gaps marked and a 1-page scope summary.

**What it simulates:** A GRC analyst standing up a compliance program and running the first gap assessment.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
