# Compliance-as-Code Guardrails - Lab Steps

Write 340 Collective's preventive guardrails as policy-as-code and document the control each one enforces. The rules are written for review, not deployed. 340 Collective is the subject organization.

**Lab Steps:**

1. List six to eight guardrails 340 Collective needs, such as: S3 buckets must block public access unless explicitly approved, S3 buckets must be encrypted, CloudTrail must stay enabled, no IAM users with access keys, and resources must carry an owner tag.
2. Draft an OPA/Rego rule for each guardrail that would fail a CloudFormation template before deploy, with a passing and a failing example template written alongside it.
3. Write the matching AWS Config rule definition for each guardrail (managed rule name or custom rule logic) to catch drift after deploy.
4. Outline a Service Control Policy that denies the highest-risk actions, such as stopping CloudTrail, leaving approved Regions, or disabling Security Hub.
5. Build a guardrail register with columns: Guardrail ID, Rule Type (Rego, Config, SCP), What It Blocks, Control It Enforces (SOC 2 or ISO 27001 reference), Owner.

**Skills:** Policy-as-code · preventive controls · OPA/Rego · AWS Config · SCP design

**Tools:** Text editor · OPA Playground · AWS Config managed rules documentation · Excel or Google Sheets

**Deliverable:** A set of written Rego rules, Config rule definitions, an SCP outline, and a guardrail-to-control register.

**What it simulates:** A GRC engineer turning compliance requirements into preventive deploy-time controls.

Artifacts are built manually by the collaboration team. Nothing in this repo is deployed to live infrastructure.
