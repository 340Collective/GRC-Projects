# GRC-as-Code Platform — Architecture Breakdown

## Mission Statement

A fully automated, IaC-driven GRC engineering environment that leverages AWS-native security services as the audit engine to continuously evaluate the company's cloud and identity environment against SOC 2, NIST 800-53, ISO 27001, PCI DSS, and HIPAA — centralizing all findings in one format (ASFF), routing via pub/sub (EventBridge), and pushing remediation tickets to Jira with human approval gates.

> **Framing:** AWS is the tooling, not the target. AWS services (Config, GuardDuty, Inspector, Security Hub, EventBridge, Lambda) do the auditing; the company's infrastructure and identity providers (Layer 1) are what's audited; the five compliance frameworks are the measuring stick.

---

## Architecture Principles

| Principle | Implementation |
|-----------|---------------|
| Single pane of glass | Security Hub (all findings, one format) |
| One format | ASFF (AWS Security Finding Format) |
| Pub/sub broker | EventBridge (routes events, no transformation) |
| Everything as code | Terraform (infra, rules, frameworks, pipelines) |
| Loose coupling | Producers don't know consumers exist |
| Human-in-the-loop | Jira approval gates resume pipelines |
| Operational memory | DynamoDB (dedup, SLA, correlation) |

---

## System Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 6: CONSUMERS (Outputs)                                            │
│ Jira (tickets + approvals) │ Audit Manager (evidence) │ Slack/PagerDuty │
└─────────────────────────────────────────────────────────────────────────┘
        ▲                           ▲                          ▲
        │                           │                          │
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 5: PROCESSING (Lambdas)                                           │
│ Control Mapper │ Jira Creator │ Evidence Collector │ SLA Checker         │
└─────────────────────────────────────────────────────────────────────────┘
        ▲                           ▲                          ▲
        │                           │                          │
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 4: ROUTING (EventBridge — Pub/Sub Broker)                         │
│ Event-driven rules │ Scheduled cron rules │ Fan-out to multiple targets │
└─────────────────────────────────────────────────────────────────────────┘
        ▲
        │
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 3: CENTRALIZATION (Security Hub — Single Pane of Glass)           │
│ All findings normalized to ASFF │ Compliance.RelatedRequirements[]      │
└─────────────────────────────────────────────────────────────────────────┘
        ▲                    ▲                    ▲                ▲
        │                    │                    │                │
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: PRODUCERS (Audit Sources)                                      │
│ AWS Config │ GuardDuty │ Inspector │ Okta Lambda │ Custom Checks        │
└─────────────────────────────────────────────────────────────────────────┘
        ▲
        │
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: INFRASTRUCTURE (What's Being Audited)                          │
│ EC2 │ S3 │ RDS │ IAM │ VPC │ Lambda │ EKS │ Okta │ SaaS               │
└─────────────────────────────────────────────────────────────────────────┘
        ▲
        │
┌─────────────────────────────────────────────────────────────────────────┐
│ LAYER 0: DevSecOps Pipeline (Deploys Everything Above)                  │
│ Git (2-person PR) → CI/CD → IaC Scan → Human Approval → Terraform Apply│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Layer 0: DevSecOps Pipeline

### Purpose
Deploy and manage the entire GRC platform through code with security gates at every stage.

### Components

| Component | Service | Role |
|-----------|---------|------|
| Source Control | GitHub / CodeCommit | Version control, branch protection |
| CI/CD | GitHub Actions / CodePipeline | Automated pipeline with gates |
| IaC Scanning | Checkov, tfsec, OPA | Pre-deploy security validation |
| Human Approval | Jira + API Gateway + Step Functions | 2-person sign-off before prod |
| Deployment | Terraform | All infrastructure as code |

### Pipeline Stages

```
Stage 1: PR Created
├── Checkov scan (IaC misconfigurations)
├── tfsec scan (Terraform-specific security)
├── OPA policy evaluation (custom org policies)
├── Lambda unit tests
└── GATE: 2 reviewer approvals required (branch protection)

Stage 2: Merge to main
├── Terraform plan (output posted to PR)
└── GATE: Senior engineer approves plan

Stage 3: Deploy to staging
├── Terraform apply (staging account)
├── Integration tests (Config rules evaluate correctly?)
└── GATE: Jira approval ticket created
         → Human clicks "Approve" in Jira
         → Jira webhook → API Gateway → Lambda → resumes pipeline

Stage 4: Deploy to production
├── Terraform apply (prod account)
├── Smoke tests (Security Hub receiving findings?)
└── Post-deploy: verify Config rules active, EventBridge rules firing
```

### Jira Approval → Pipeline Resume Flow

```
CodePipeline/Step Functions
        │
        ├── Creates Jira ticket (type: "Deployment Approval")
        ├── Enters WAIT state
        │
        │         ┌──────────────────────┐
        │         │  Human reviews in    │
        │         │  Jira, clicks        │
        │         │  "Approve"           │
        │         └──────────┬───────────┘
        │                    │
        │                    ▼
        │         Jira Webhook fires
        │                    │
        │                    ▼
        │         API Gateway endpoint
        │                    │
        │                    ▼
        │         Lambda validates:
        │         - Approver has correct role?
        │         - 2-person requirement met?
        │         - Approval within time window?
        │                    │
        │                    ▼
        │         Sends success token to
        │         Step Functions / CodePipeline
        │                    │
        ◀────────────────────┘
        │
        ▼
Stage 4: Production deploy proceeds
```

---

## Layer 1: Infrastructure (Audit Targets)

Everything being monitored. This is your AWS environment plus external identity providers.

| Category | Resources | Frameworks Applicable |
|----------|-----------|----------------------|
| Compute | EC2, Lambda, EKS | All |
| Storage | S3, EBS, RDS | All |
| Identity | IAM, Okta, SSO | All |
| Network | VPC, Security Groups, NACLs | PCI, NIST, ISO |
| Logging | CloudTrail, VPC Flow Logs, CloudWatch | All |
| Encryption | KMS, ACM, TLS configs | All |

---

## Layer 2: Producers (Audit Sources)

Each producer evaluates resources and publishes findings to Security Hub in ASFF format.

### AWS Config (Resource Compliance)

**Role:** Continuously evaluates resource configurations against rules.

**Key Conformance Packs:**

| Framework | Pack Name | Example Rules |
|-----------|-----------|---------------|
| NIST 800-53 | `Operational-Best-Practices-for-NIST-800-53-rev5` | iam-user-mfa-enabled, encrypted-volumes |
| PCI DSS | `Operational-Best-Practices-for-PCI-DSS` | restricted-ssh, rds-storage-encrypted |
| HIPAA | `Operational-Best-Practices-for-HIPAA-Security` | cloudtrail-enabled, s3-bucket-ssl-requests-only |
| ISO 27001 | `Operational-Best-Practices-for-ISO-27001` | vpc-flow-logs-enabled, root-account-mfa-enabled |
| SOC 2 | Custom (mapped from CIS + NIST subset) | access-keys-rotated, iam-password-policy |

**Custom Rules (Lambda-backed):** For controls without managed rules (data retention policies, naming conventions, tag enforcement).

### GuardDuty (Threat Detection)

**Role:** Detects active threats — compromised credentials, crypto mining, C2 communication.

**Maps to:** SOC 2 CC7.2-CC7.4 (monitoring), NIST SI-4 (system monitoring), PCI 11.4 (IDS).

### Inspector (Vulnerability Management)

**Role:** Scans EC2/ECR/Lambda for CVEs and network exposure.

**Maps to:** SOC 2 CC7.1, NIST SI-2 (flaw remediation), PCI 6.1 (patching), ISO A.12.6.1.

### Okta Lambda (Identity Auditing)

**Role:** Custom Lambda scheduled by EventBridge. Pulls from Okta API, evaluates identity controls, publishes to Security Hub as ASFF.

**Checks:**
- MFA enrollment for all users
- Dormant accounts (no login > 90 days)
- Privileged group membership review
- Password policy compliance
- Session timeout configuration

### Custom Check Lambdas (Extensible)

Any SaaS or internal system can become a producer. Pattern:
1. Lambda pulls data from source API
2. Evaluates against control requirements
3. Publishes findings to Security Hub in ASFF format

---

## Layer 3: Centralization (Security Hub)

### Purpose
Single source of truth. Every finding from every producer lands here in one format.

### ASFF Structure (The Universal Schema)

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "unique-finding-id",
  "ProductArn": "arn:aws:securityhub:region:account:product/source",
  "GeneratorId": "rule-or-check-id",
  "Types": ["Software and Configuration Checks/Industry and Regulatory Standards"],
  "Severity": { "Label": "HIGH" },
  "Title": "Human-readable finding title",
  "Description": "Detailed description of the issue",
  "Resources": [{
    "Type": "AwsS3Bucket | AwsIamUser | Other",
    "Id": "arn:aws:s3:::bucket-name",
    "Region": "us-east-1"
  }],
  "Compliance": {
    "Status": "FAILED",
    "RelatedRequirements": [
      "SOC2-CC6.1",
      "NIST-800-53-IA-2",
      "PCI-DSS-8.3",
      "HIPAA-164.312(d)",
      "ISO27001-A.9.4.2"
    ]
  },
  "Remediation": {
    "Recommendation": {
      "Text": "Enable MFA for this user",
      "Url": "https://docs.aws.amazon.com/..."
    }
  }
}
```

### Why Security Hub as the Central Point

- Native integration with Config, GuardDuty, Inspector (zero config)
- Custom products API for your Okta/SaaS Lambdas
- `Compliance.RelatedRequirements[]` carries framework mapping WITH the finding
- Aggregation across multiple AWS accounts and regions
- Built-in standards (CIS, NIST, PCI) you can enable with one click

---

## Layer 4: Routing (EventBridge — Pub/Sub Broker)

### Purpose
Decouple producers from consumers. Route findings to the right targets based on rules. No transformation — pure routing.

### Event Source

Security Hub emits to EventBridge automatically:
- Event source: `aws.securityhub`
- Detail type: `Security Hub Findings - Imported`

### Routing Rules

| Rule Name | Pattern | Target | Purpose |
|-----------|---------|--------|---------|
| critical-findings | Severity = CRITICAL | Jira Lambda + SNS (PagerDuty) | Immediate ticket + page |
| high-findings | Severity = HIGH, Status = FAILED | Jira Lambda | Remediation ticket |
| all-failed | Status = FAILED | Evidence Lambda | Audit Manager evidence |
| daily-okta | Cron: 0 6 * * ? * | Okta Audit Lambda | Scheduled identity scan |
| weekly-report | Cron: 0 8 ? * MON * | Report Lambda | Weekly compliance summary |
| sla-check | Cron: 0 */4 * * ? * | SLA Lambda | Check for SLA breaches |

### Fan-Out Pattern

One finding can trigger multiple consumers simultaneously:

```
Security Hub Finding (CRITICAL + FAILED)
        │
        ├──▶ Jira Lambda (create ticket)
        ├──▶ Evidence Lambda (log to Audit Manager)
        ├──▶ SNS → PagerDuty (page on-call)
        └──▶ SNS → Slack (notify channel)
```

### Adding New Consumers

To add a new consumer (e.g., Splunk SIEM integration):
1. Add one EventBridge rule in Terraform
2. Point to new Lambda or direct integration
3. Zero changes to producers or Security Hub

---

## Layer 5: Processing (Lambda Functions)

### Control Mapper Lambda

**Trigger:** EventBridge (all findings)
**Purpose:** Enriches findings with full crosswalk data if not already present.

### Jira Creator Lambda

**Trigger:** EventBridge (HIGH/CRITICAL findings)
**Purpose:** Creates remediation tickets in Jira.

**Logic:**
1. Generate finding hash (resource ARN + rule ID)
2. Check DynamoDB — already ticketed?
3. If new: create Jira ticket with control IDs, severity, remediation steps
4. If existing: update `last_seen`, optionally add comment
5. Write state to DynamoDB

**Jira Ticket Structure:**
```
Project: GRC
Type: Compliance Finding
Summary: [CC6.1/IA-2/8.3] User missing MFA - arn:aws:iam::123:user/bob
Priority: High (mapped from ASFF severity)
Labels: SOC2, NIST, PCI, HIPAA
Description:
  - Control: Access Control - MFA Required
  - Resource: arn:aws:iam::123456789:user/bob
  - Source: AWS Config (iam-user-mfa-enabled)
  - First Detected: 2025-05-14
  - Remediation: Enable MFA for this IAM user
  - SLA: 72 hours (CRITICAL), 7 days (HIGH)
Custom Fields:
  - Control ID: AC-MFA-001
  - Frameworks: SOC2-CC6.1, NIST-IA-2, PCI-8.3, HIPAA-164.312(d)
  - Resource ARN: arn:aws:iam::123456789:user/bob
  - SLA Deadline: 2025-05-17T06:00:00Z
```

### Evidence Collector Lambda

**Trigger:** EventBridge (all FAILED findings)
**Purpose:** Pushes compliance evidence to AWS Audit Manager for assessment reports.

### SLA Checker Lambda

**Trigger:** EventBridge (cron every 4 hours)
**Purpose:** Queries DynamoDB for open findings past SLA, escalates via Jira priority bump + Slack alert.

### Jira Approval Handler Lambda

**Trigger:** API Gateway (Jira webhook)
**Purpose:** Receives Jira approval events, validates, resumes CI/CD pipeline.

---

## Layer 6: Consumers (Outputs)

### Jira Cloud

| Function | Details |
|----------|---------|
| Findings Board | Kanban board of open compliance findings |
| Approval Workflow | Human gates for pipeline deployments |
| Audit Trail | Full history of who approved what, when |
| SLA Tracking | Custom fields for deadline visibility |
| Dashboards | Compliance posture by framework, severity trends |

### AWS Audit Manager

| Function | Details |
|----------|---------|
| Framework Definitions | SOC 2, NIST, ISO, PCI, HIPAA (as code) |
| Automated Evidence | Config results, CloudTrail logs, Security Hub findings |
| Manual Evidence | Okta Lambda pushes identity audit results |
| Assessment Reports | Generated for auditors on demand or scheduled |

### Alerting (Slack / PagerDuty)

| Severity | Channel |
|----------|---------|
| CRITICAL | PagerDuty (page on-call) + Slack #security-critical |
| HIGH | Slack #security-findings |
| Weekly digest | Slack #compliance-weekly |

---

## State Layer: DynamoDB

### Purpose
Operational memory — deduplication, SLA tracking, pipeline correlation.

### Tables

**findings-state**
```
PK: finding_hash (sha256 of resource_arn + rule_id)
Attributes:
  - jira_ticket_id
  - first_seen (ISO timestamp)
  - last_seen (ISO timestamp)
  - times_seen (counter)
  - status (OPEN | REMEDIATED | SUPPRESSED)
  - severity
  - sla_deadline (ISO timestamp)
  - sla_breached (boolean)
  - frameworks[] (list of framework IDs)
  - resource_arn
```

**pipeline-approvals**
```
PK: jira_ticket_id
Attributes:
  - pipeline_execution_id
  - approval_state (PENDING | APPROVED | REJECTED)
  - approvers_required (number)
  - approvers_received[] (list of emails)
  - created_at
  - resolved_at
  - step_functions_task_token
```

**entity-correlation**
```
PK: entity_id (email or ARN)
Attributes:
  - findings[] (list of finding_hashes)
  - sources[] (okta, config, inspector)
  - open_count
  - last_finding_at
```

---

## Control Framework Crosswalk (As Code)

The mapping lives in the repo as JSON, deployed alongside the Lambdas:

```json
{
  "AC-MFA-001": {
    "title": "Multi-Factor Authentication Required",
    "config_rules": ["iam-user-mfa-enabled", "root-account-mfa-enabled"],
    "custom_checks": ["okta-mfa-enrollment"],
    "frameworks": {
      "SOC2": "CC6.1",
      "NIST": "IA-2",
      "ISO27001": "A.9.4.2",
      "PCI": "8.3",
      "HIPAA": "164.312(d)"
    },
    "severity": "HIGH",
    "sla_hours": { "CRITICAL": 72, "HIGH": 168 },
    "remediation": "Enable MFA for the identified user account"
  },
  "DP-ENC-001": {
    "title": "Encryption at Rest Required",
    "config_rules": ["s3-bucket-server-side-encryption-enabled", "rds-storage-encrypted", "ec2-ebs-encryption-by-default"],
    "frameworks": {
      "SOC2": "CC6.7",
      "NIST": "SC-28",
      "ISO27001": "A.10.1.1",
      "PCI": "3.4",
      "HIPAA": "164.312(a)(2)(iv)"
    },
    "severity": "HIGH",
    "sla_hours": { "CRITICAL": 72, "HIGH": 168 },
    "remediation": "Enable server-side encryption on the identified resource"
  }
}
```

---

## AWS Services Summary

| Service | Layer | Role in Platform |
|---------|-------|-----------------|
| GitHub/CodeCommit | 0 | Source control, 2-person PR approval |
| CodePipeline/GitHub Actions | 0 | CI/CD with security gates |
| Terraform | 0 | All infrastructure as code |
| Checkov/tfsec | 0 | Pre-deploy IaC security scanning |
| AWS Config | 2 | Continuous resource compliance evaluation |
| GuardDuty | 2 | Threat detection |
| Inspector | 2 | Vulnerability scanning |
| Lambda (Okta) | 2 | Custom identity auditing |
| Security Hub | 3 | Single pane of glass, ASFF normalization |
| EventBridge | 4 | Pub/sub broker, scheduler, fan-out |
| Lambda (processing) | 5 | Mapping, ticketing, evidence, SLA |
| DynamoDB | 5 | Operational memory (dedup, state, correlation) |
| API Gateway | 5 | Jira webhook receiver |
| Step Functions | 5 | Pipeline orchestration with wait states |
| Jira Cloud | 6 | Tickets, approvals, audit trail |
| Audit Manager | 6 | Evidence collection, assessment reports |
| SNS | 6 | Alert fan-out (Slack, PagerDuty) |
| KMS | All | Encryption of data at rest across all layers |
| CloudWatch | All | Observability of the platform itself |

---

## Cost Estimate (Single Account, ~100 Resources)

| Service | Estimated Monthly Cost |
|---------|----------------------|
| AWS Config (20 rules) | ~$40 |
| Security Hub | ~$10-30 |
| GuardDuty | ~$10-20 |
| Inspector | ~$5-15 |
| EventBridge | < $1 |
| Lambda | < $5 |
| DynamoDB (on-demand) | < $5 |
| API Gateway | < $1 |
| Step Functions | < $1 |
| **Total** | **~$75-120/month** |

---

## Repo Structure

```
grc-platform/
├── .github/workflows/
│   ├── pr-checks.yml           # Checkov, tfsec, OPA, unit tests
│   └── deploy.yml              # Terraform plan/apply with approval gates
├── infra/
│   ├── main.tf                 # Provider, backend, module calls
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── config/             # Config recorder, conformance packs, custom rules
│   │   ├── security-hub/       # Standards, custom product registration
│   │   ├── eventbridge/        # Rules, targets, schedules
│   │   ├── lambdas/            # Function deployments + IAM roles
│   │   ├── audit-manager/      # Frameworks, assessments, controls
│   │   ├── dynamodb/           # Tables for state tracking
│   │   ├── api-gateway/        # Jira webhook endpoint
│   │   └── pipeline/           # CodePipeline/Step Functions
├── lambdas/
│   ├── okta-auditor/           # Identity compliance checks
│   │   ├── handler.py
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── control-mapper/         # ASFF enrichment with crosswalk
│   ├── jira-creator/           # Finding → Jira ticket
│   ├── jira-approval-handler/  # Webhook → resume pipeline
│   ├── evidence-collector/     # Push to Audit Manager
│   └── sla-checker/            # SLA breach detection + escalation
├── crosswalk/
│   └── control-matrix.json     # Unified framework mapping
├── conformance-packs/
│   ├── soc2-custom.yaml
│   ├── nist-800-53.yaml
│   ├── pci-dss.yaml
│   ├── hipaa.yaml
│   └── iso-27001.yaml
├── policies/
│   └── opa/                    # Custom OPA policies for IaC validation
├── tests/
│   ├── unit/                   # Lambda unit tests
│   ├── integration/            # End-to-end compliance flow tests
│   └── security/               # Checkov/tfsec custom checks
└── docs/
    ├── architecture.md         # This document
    ├── runbook.md              # Operational procedures
    └── onboarding.md           # How to add new controls/frameworks
```

---

## Next Steps (Build Order)

1. **Control crosswalk matrix** — Define the unified mapping (JSON)
2. **Base Terraform modules** — Config + Security Hub + EventBridge
3. **Lambda functions** — Jira creator + dedup logic
4. **CI/CD pipeline** — GitHub Actions with approval gates
5. **Okta integration** — Identity audit Lambda
6. **Audit Manager** — Framework definitions + evidence automation
7. **Jira approval loop** — Webhook → pipeline resume
8. **SLA enforcement** — Cron-based breach detection
