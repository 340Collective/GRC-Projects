# Risk Register Architecture

## Purpose

Keep one scored, owned, and dated list of risks that nobody can quietly forget. Each risk is scored the same way, mirrored to the ticketing system people already work in, and attached to a timer that escalates when its review date passes. Leadership sees the result as a likelihood by impact heatmap.

## Scope and frameworks

- ISO 27001:2022 clause 6.1 (actions to address risks and opportunities) and clause 8.2 (information security risk assessment).
- NIST CSF 2.0 GV.RM (risk management strategy) and ID.RA (risk assessment).
- SOC 2 CC3 (risk assessment).
- Control areas: risk identification, scoring, ownership, treatment, review cadence, and reporting.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Intake | Cognito, API Gateway, Lambda (risk handler) | Owner signs in and submits a risk; the handler validates and scores it |
| Processing | DynamoDB Streams, Lambda (Jira sync), Secrets Manager | Every change is mirrored to a Jira ticket using a stored token |
| State | DynamoDB (risk register) | The scored register, indexed by owner and status |
| Orchestration | EventBridge Scheduler, Lambda (SLA escalator), SNS | One timer per review date; missed dates escalate |
| Outputs | S3 (nightly export), Athena, Lambda (heatmap report), CloudWatch | Heatmap for leadership; alarms on function errors |

## Stage details

### Intake

- A Cognito user pool holds the risk owners. API Gateway uses a Cognito authorizer, so every call is authenticated.
- The risk handler validates required fields and computes the score from the owner's DREAD+ model (the DREAD dimensions plus the owner's added factors). The model is referenced by concept only; its definition stays in the owner's private notes.
- The handler derives inherent and residual ratings from likelihood, impact, and treatment.

### Processing

- DynamoDB Streams emits each insert and update.
- The Jira sync Lambda creates or updates one Jira ticket per risk, following the owner's Jira risk ticket schema (also referenced by concept only).
- The Jira API token is read from Secrets Manager at runtime.

### State

- The register holds the current version of each risk. Previous versions are kept in the nightly export (DynamoDB Streams keeps changes for 24 hours only).

### Orchestration

- On every create or update, the handler creates or updates a one-off EventBridge Scheduler schedule named after the risk ID for its `review_due` date.
- When it fires, the SLA escalator checks the risk is still unreviewed and publishes to SNS, which emails the owner.

### Outputs

- A nightly export writes the register to `exports/<yyyy>/<mm>/<dd>/`.
- Athena queries the export, and a heatmap Lambda renders the likelihood by impact heatmap and an overdue list as an HTML report in S3.
- CloudWatch alarms on handler, sync, and escalator errors.

## Data model

DynamoDB table `risk_register`:

- Partition key `risk_id`.
- Attributes: `title`, `category` (business, security, vendor), `owner`, `status`, `likelihood`, `impact`, `dread_scores`, `inherent_rating`, `residual_rating`, `treatment`, `review_due`, `jira_key`, `updated_at`.
- GSI `by_owner` (partition `owner`, sort `review_due`) and GSI `by_status` (partition `status`, sort `residual_rating`).

S3 prefix: `exports/<yyyy>/<mm>/<dd>/`.

## Security and privacy controls

- KMS customer managed key for the register, exports, and SNS.
- The API requires Cognito sign-in; there is no unauthenticated write path.
- Least-privilege IAM: only the handler writes the register; only the sync Lambda reads the Jira secret.
- CloudTrail logs API and Scheduler activity.
- No secrets or personal details in logs; logs carry risk IDs.
- Human approval point: the risk owner accepts the treatment and any residual rating before the risk is closed.

## 340 Collective testbed

340 Collective's account hosts its own register of business, security, and vendor risks. Validation is a risk created through the API, scored, mirrored to Jira, given a short test review date, and escalated through SNS when that date passes.

## Cost note

There is no paid dashboard: the heatmap is an HTML report. Cognito, API Gateway, Lambda, DynamoDB, Scheduler, SNS, and Athena stay at or near the free tier at 340 Collective's size. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. KMS key and the register table with both GSIs.
2. Cognito user pool, API, and risk handler with the scoring logic.
3. Streams, Jira sync, and the Secrets Manager token.
4. Per risk Scheduler timers, the SLA escalator, and SNS.
5. Nightly export, Athena, and the heatmap report Lambda.
6. CloudWatch alarms.

## Related projects

- [01 GRC-as-Code Platform](../Faris-01-GRC-as-Code-Platform/README.md)
- [02 TPRM/VRM](../Maria-02-TPRM-VRM/README.md)
- [04 Gap Analysis](../Alex-04-Gap-Analysis/README.md)
