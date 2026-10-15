# User Access Reviews Architecture

## Purpose

Run a complete quarterly access review without spreadsheets: every entitlement is collected from the source of truth, the right approver sees only their people, every decision is recorded with who and when, and removals happen only after a human confirms them. The finished campaign is ready to hand to an auditor.

## Scope and frameworks

- SOC 2 CC6.2 (provisioning and deprovisioning) and CC6.3 (role-based access and periodic review).
- ISO 27001:2022 A.5.18 (access rights).
- NIST CSF 2.0 PR.AA (identity management, authentication, and access control).
- Control areas: entitlement inventory, periodic review, approver sign-off, removal of unneeded access, and evidence of review.

## Automation flow

| Stage | AWS services | What happens |
| --- | --- | --- |
| Producers | IAM, IAM Access Analyzer, optional Okta export (14) or IAM Identity Center | Users, groups, roles, policies, and external and unused access findings |
| Processing | EventBridge Scheduler, Step Functions, Lambda (collector) | Quarterly campaign collects and normalizes every entitlement |
| State | S3 (review packages), DynamoDB (review items) | One package per approver; one item per entitlement with its decision |
| Orchestration | SES, API Gateway, Lambda (decision handler, apply removals) | Approvers sign off; removals wait for owner confirmation |
| Outputs | S3 (campaign evidence), CloudTrail, CloudWatch | Exported campaign record; change log and overdue alarm |

## Stage details

### Producers

- IAM: users, their groups, attached and inline policies, and roles, with last used data. This is the access model's source of truth; anything live but not in the access-model template (`cloudformation/grc-access-model.yaml` in the private 340collective-website repo) is flagged as hand-made drift.
- Okta group and app-assignment export, if [14 Identity and Access (Okta)](../14-identity-access/README.md) is built: the identity source for people.
- IAM Identity Center, only if it is ever enabled: users, groups, and account assignments, read through the Identity Store and SSO Admin APIs.
- IAM Access Analyzer: external access findings and unused access findings (unused roles, keys, and permissions).

### Processing

- EventBridge Scheduler starts the Step Functions campaign each quarter.
- The collector Lambda joins assignments with Access Analyzer findings so each item shows whether access is unused or shared externally.
- Each item is assigned an approver (the person's manager or the resource owner).

### State

- The package builder writes one package per approver (CSV and HTML) to `campaigns/<campaign-id>/packages/<approver-id>/`.
- Each entitlement is one DynamoDB item with status `pending`.

### Orchestration

- SES emails each approver a signed, time-limited link to the sign-off API.
- The sign-off API sits behind an authorizer for approver sign-in, so it is never unauthenticated.
- The decision handler records `keep` or `remove`, the approver, and the time.
- A `remove` decision opens a removal task in the campaign. The owner confirms, then the apply removals Lambda deletes the account assignment or detaches the policy. Nothing is revoked automatically.

### Outputs

- At campaign close, the full record (items, decisions, removals, timestamps) is exported to `campaigns/<campaign-id>/evidence/` for the [06 evidence lake](../06-evidence-automation/README.md).
- CloudTrail logs every removal; CloudWatch alarms when sign-offs are overdue.

## Data model

DynamoDB table `review_items`:

- Partition key `campaign_id`, sort key `item_id`.
- Attributes: `principal`, `principal_type`, `permission_set_or_policy`, `account`, `approver`, `last_used`, `finding_type`, `decision`, `decided_by`, `decided_at`, `removal_status`, `confirmed_by`.
- GSI on `approver` and `decision` for open item lists.

S3 prefixes: `campaigns/<campaign-id>/packages/<approver-id>/`, `campaigns/<campaign-id>/evidence/`.

## Security and privacy controls

- KMS customer managed key for packages, evidence, and the items table.
- Least-privilege IAM: the collector is read-only; only the apply removals Lambda can change assignments, and only for items with a confirmed removal.
- CloudTrail logs every read and every change.
- No credentials in packages or logs; logs carry item IDs.
- Human approval points: approvers decide every item, and the owner confirms every removal.

## 340 Collective testbed

340 Collective's account runs the first campaign against its own IAM. Validation is a campaign that produces packages, records each decision, applies one confirmed removal on a test group membership, and exports the record as evidence.

## Cost note

The main cost driver is IAM Access Analyzer unused access analysis, billed per IAM role and user analyzed per month. External access analysis has no charge. Step Functions, Lambda, DynamoDB, S3, API Gateway, and SES stay at or near the free tier at a quarterly cadence. Confirm with the AWS Pricing Calculator before deploying.

## Build order

1. KMS key, items table, and campaign bucket.
2. Access Analyzer external and unused access analyzers.
3. Collector Lambda and the Step Functions campaign with the quarterly schedule.
4. Package builder and SES links.
5. Sign-off API, decision handler, and the confirmed removal path.
6. Evidence export, CloudTrail, and the overdue alarm.

## Related projects

- [01 GRC-as-Code Platform](../01-grc-as-code-platform/README.md)
- [04 Gap Analysis](../04-gap-analysis-340collective/README.md)
- [06 Evidence Automation](../06-evidence-automation/README.md)
- [14 Identity and Access (Okta)](../14-identity-access/README.md)
