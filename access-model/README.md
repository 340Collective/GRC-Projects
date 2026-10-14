# GRC access model

Least-privilege AWS IAM access for the GRC Projects team in 340 Collective's account (570814274897, us-east-1), defined as code in [grc-access.yaml](grc-access.yaml). This is the access model that [GOVERNANCE.md](../GOVERNANCE.md) ("Access to the real environment") calls for. Plain IAM users, no SSO. Roles are referenced by function, not by person.

Status: not deployed. The ISSM deploys it after this pull request is approved.

## What the stack creates

| Resource | Name | Purpose |
| --- | --- | --- |
| Permissions boundary | `grc-permissions-boundary` | Ceiling for both users and for every role the engineer creates |
| Group | `GRC-Engineer` | ISSE / Engineer |
| Group | `GRC-Analyst` | ISSO / Analyst |
| Engineer policies | `grc-engineer-build`, `grc-engineer-security`, `grc-engineer-guardrails`, `grc-engineer-limits` | One engineer policy split four ways to fit the 6,144 character managed policy quota |
| Analyst policy | `grc-analyst` | Security service reads, finding export, evidence writes |
| MFA policy | `grc-require-mfa` | Self-service credentials, and deny everything until MFA is used. Attached to both groups |
| IAM users | `EngineerUserName`, `AnalystUserName` (required deploy-time parameters, no defaults) | One user per group, boundary attached, tagged `grc-role` and `grc-function` |
| Budget | `grc-projects-monthly` | 10 USD monthly cost budget, ACTUAL alerts at 1, 5, and 10 USD |

Both groups also get the AWS managed `SecurityAudit` and `job-function/ViewOnlyAccess` policies as their read baseline. Neither returns S3 object data or SSM parameter values. `ReadOnlyAccess` is not used anywhere in this template. Both users also carry the permissions boundary, so these managed policies only take effect for services the boundary allows (see "Effective read scope" below).

No passwords, access keys, email addresses, or person names are in the template. The budget email and both user names are deploy-time parameters with no default.

## What each role can and cannot do

| Role | Access | Can | Cannot |
| --- | --- | --- | --- |
| ISSE / Engineer | `GRC-Engineer` (this template) | Create, update, and delete `grc-*` CloudFormation stacks. Build `grc-*` S3 buckets, Lambda functions, DynamoDB tables, SNS topics, SQS queues, EventBridge rules and buses, schedules, Step Functions, CloudWatch alarms and dashboards, Glue and Athena, CodeBuild and CodePipeline, Backup vaults, `/grc/` SSM parameters, and SSM Automation documents. Create API Gateway APIs tagged `grc-project` and KMS keys tagged `grc-project`. Turn on and configure Security Hub, Config, GuardDuty, Inspector, and Audit Manager for this account. Create `grc-*` roles only with the boundary attached, change their trust policies, and pass them only to AWS services. Read the SecurityAudit and ViewOnlyAccess views for the services in "Effective read scope" below, plus CloudTrail log objects for Athena. | Touch any `collective340-*` stack, role, function, table, topic, schedule, alarm, or log group, the `cloudtrail` stack, the trail, the 340 buckets, or the three production HTTP APIs. Use `grc-*` S3 permissions on buckets owned by another account. Read or write any SSM parameter outside `/grc/`, including `/340collective/*`. Create, edit, or delete any IAM user or group, the access-model policies, or the boundary. Remove a role's boundary or attach admin policies. Assume any role directly, including the `grc-*` roles they create (those are for AWS services only). Manage another user's keys, password, or MFA. Create, edit, or delete budgets, billing, or org settings. Work outside us-east-1. Use the budget-breaker services listed below. |
| ISSO / Analyst | `GRC-Analyst` (this template) | Read Security Hub, Config, GuardDuty, Inspector, Audit Manager, and IAM Access Analyzer. Export Inspector finding reports and SBOMs, and create Audit Manager assessment reports. Generate and read the IAM credential report and service last-accessed data. Look up CloudTrail events. Read `grc-*` buckets, tables, Lambda logs, the Glue catalog, and Athena workgroups. Write (never delete) objects to `grc-evidence-*` buckets in this account. Read the SecurityAudit and ViewOnlyAccess views for the services in "Effective read scope" below. | Build or change any infrastructure (no stacks, functions, or role passing). Read or write object data in any non-`grc-` bucket, including the site and client-media buckets. Read `/340collective/*` parameters or any secret value. Update Security Hub findings. Work outside us-east-1. |
| Auditor / Assessor | Existing hand-made `ExtAuditor` group (not in this template) | Independent read-only assessment through AWS managed `ReadOnlyAccess`. | Write anything. See the note below about object data. |
| Stakeholder / Business Owner | Existing hand-made `Leadership` group (not in this template) | Read-only view of the account through AWS managed `ReadOnlyAccess`. This is already read-only, so no change is needed. | Write anything. Approve changes (per GOVERNANCE.md). |
| ISSM / Program Lead | Existing hand-made admin identity (not in this template) | Deploys, updates, and tears down this stack after PR approval. Sets temporary console passwords. | Not covered by this template. |

Both new groups must enroll MFA before anything else works (see Onboarding).

### Effective read scope

The permissions boundary caps both users, so `SecurityAudit` and `ViewOnlyAccess` reads only work for services the boundary allows. Everything else those managed policies grant is implicitly denied.

- Readable (subject to the explicit denies, for example no S3 object data or SSM values outside `grc-*` and `/grc/`): CloudFormation, STS, S3 bucket metadata, Lambda, CloudWatch Logs, EventBridge and EventBridge Scheduler, Step Functions, DynamoDB, SNS, SQS, CloudWatch, API Gateway, Glue, Athena, CodeBuild, CodePipeline, AWS Backup, Systems Manager, KMS, Security Hub, Config, GuardDuty, Inspector, Audit Manager, IAM Access Analyzer, CloudTrail, Resource Groups Tagging, IAM reads, budget reads, EC2 describes, Route 53, CloudFront, ACM, and Service Quotas.
- Not readable (AccessDenied, empty console pages): every other service, including RDS, ECR, ELB, EKS, ECS, Organizations, SES, Cognito, Secrets Manager, Health, X-Ray, and Cost Explorer. Security Hub and Config cover most of that inventory once they are enabled.

### Existing hand-made identities

The Auditor and Stakeholder already have IAM users in the hand-made `ExtAuditor` and `Leadership` groups. This template does not change or reference them. Both groups use AWS managed `ReadOnlyAccess`, which allows `s3:GetObject` on every bucket, including the site and client-media buckets, and `ssm:GetParameter*`. With the default `aws/ssm` key, that likely includes the SecureString values under `/340collective/` (Stripe and others).

Recommendation for a later access-change PR, not done here: move `ExtAuditor` (and `Leadership`) from `ReadOnlyAccess` to `SecurityAudit` plus `job-function/ViewOnlyAccess`, the same baseline these new groups use, and bring both groups into CloudFormation so access is no longer granted by hand.

## Guardrails mapped to policy statements

| Requirement | Where it is enforced (Sid) |
| --- | --- |
| Engineer works only on `grc-*` resources | Resource scoping in `grc-engineer-build` and `grc-engineer-security` |
| Roles only `grc-*`, only with the boundary | `IamCreateBoundedGrcRoles` (allow), `DenyRoleWithoutGrcBoundary`, `DenyIamWritesOutsideGrc`, boundary `AllowGrcRoleAdmin` |
| Engineer never assumes roles directly | `DenyDirectRoleAssumption` (in `grc-engineer-limits`), boundary `DenyAssumeNonGrcRoles` |
| `grc-*` S3 rights only on buckets in this account | `aws:ResourceAccount` condition on `S3GrcBuckets` and analyst `AllowEvidenceExportWrite` |
| PassRole only `grc-*`, only to AWS services | `IamPassGrcRolesToServices`, boundary `AllowPassGrcRoles` |
| No admin or non-grc managed policies on roles | `DenyPrivilegedPolicyAttach`, `DenyAttachAccessModelPolicies` |
| Protect `collective340-*`, the trail stack, this stack, production APIs | `DenyProtectedProduction` |
| Protect the 340 buckets | `DenyS3WritesOutsideGrc`, `DenyS3DataReadsOutsideGrc`, analyst `DenyProductionBucketData` and `DenyNonGrcObjectData` |
| Protect `/340collective/*` and other non-grc parameters | `DenyParametersOutsideGrc`, analyst `DenyProductionParameters` |
| No IAM user or group changes, no boundary edits | `DenyIdentityAdmin`, `DenyOwnIdentityChanges`, `DenyAccessModelTampering` |
| No credentials for other users | `DenyCredentialsForOthers` (in `grc-require-mfa`, so it covers both groups) |
| No budget edits or deletes | `DenyBudgetAndBillingChanges`, and the boundary does not allow budget writes |
| Stay in us-east-1 | `DenyOutsideUsEast1` |
| Budget breakers from GOVERNANCE.md | `DenyBudgetBreakers` (QuickSight, EC2 instances and fleets, NAT gateways, RDS, Redshift, SageMaker, OpenSearch, ELB, EKS, ECS, ElastiCache, MSK, Macie, Shield Advanced, domains, Savings Plans, Marketplace, Secrets Manager), `DenyOrgAdminAndCostly` (Glue jobs and sessions, DynamoDB reserved capacity, paid analyzers) |
| Evidence and audit trail stay intact | `DenyAuditTampering` (CloudTrail changes, S3 governance-mode bypass) |
| CloudFormation cannot run as a privileged role | `DenyCloudFormationNonGrcServiceRole` |
| MFA before anything | `DenyAllExceptMfaSetupWithoutMfa` |
| Self-service password, MFA, and keys | `AllowManageOwnCredentials`, `AllowCreateOwnVirtualMfa`, `AllowDeactivateOwnMfaOnlyWithMfa` |

Enabling any denied budget-breaker service needs a later access-change PR and a cost check, per GOVERNANCE.md.

## Permissions boundary

`grc-permissions-boundary` is attached to both users and is required (`iam:PermissionsBoundary` condition) on every role the engineer creates. A bounded role can never do more than the boundary allows, whatever policies are attached to it.

- Allows only the in-scope services, a short read list (EC2, Route 53, CloudFront, ACM, and Service Quotas describes, plus IAM and budget reads), and IAM writes only on `grc-*` policies, `grc-*` roles, MFA devices, and the caller's own user.
- PassRole only for `grc-*` roles (and the Config service-linked role) to the listed AWS services. Service-linked roles only for the security services.
- Repeats the explicit denies that matter for workload roles. Every deny in the boundary is byte-identical in `grc-engineer-guardrails` (checked by the validator).
- Not in the boundary, by design: identity-admin and access-model attach denies. The boundary's narrow IAM allow already blocks users, groups, and non-grc roles. Attaching an access-model policy to a bounded role cannot exceed the boundary. The engineer user still has those explicit denies in `grc-engineer-guardrails`.

Size trims applied to fit 6,144 characters (no deny was weakened): the read list is short, so SecurityAudit and ViewOnlyAccess are clipped to the services in "Effective read scope" for both users. Several action lists use wildcards that match only the intended write actions.

The boundary allows several services on `Resource: "*"`, so production resources are protected by name. New production resources must use the `collective340-` or `340collective` prefixes to stay covered by `DenyProtectedProduction`.

## Resource naming rules

- Everything the engineer builds is named `grc-*`. Glue databases and tables may also use `grc_`.
- Reserved for the access model: `grc-permissions-boundary`, `grc-engineer*`, `grc-analyst*`, and `grc-require-mfa*` policies, the `GRC-Engineer` and `GRC-Analyst` groups, and the `grc-access-model` stack. The engineer cannot create or edit these.
- Analyst-writable evidence buckets are `grc-evidence-*`. Athena query results should go to one.
- SSM parameters go under `/grc/`.
- KMS keys and API Gateway APIs must be created with a `grc-project` tag.
- Stage Lambda code and packaged templates in a `grc-*` bucket.
- If the engineer passes a CloudFormation service role, it must be a `grc-*` role.

## Cost

- The IAM resources are free.
- `grc-projects-monthly` is a monitoring-only budget (no budget actions), which carries no charge. It covers the whole account, since the org has one account. Credits and refunds are excluded so they cannot hide real usage.
- Existing budget, checked read-only with `aws budgets describe-budgets`: `340collective-monthly-5usd` (COST, MONTHLY, 10 USD limit despite its name) alerts at ACTUAL 80%, ACTUAL 100%, and FORECASTED 100%. It is owned by the `collective340-budget` stack and has no alerts at 1, 5, or 10 USD. It is left unchanged; the GRC budget is separate and has a distinct name.
- Customer managed KMS keys cost about 1 USD per month each. Security Hub, Config, GuardDuty, Inspector, and Audit Manager charge after their trials. Tear down per GOVERNANCE.md.

## Deploy (ISSM, after PR approval, from a clean main)

```
aws cloudformation deploy --template-file access-model/grc-access.yaml --stack-name grc-access-model --capabilities CAPABILITY_NAMED_IAM --parameter-overrides EngineerUserName=<from private roster> AnalystUserName=<from private roster> BudgetAlertEmail=<from private roster> --profile 340collective --region us-east-1
```

The two user names are required and have no default. They and the alert address come from the private roster and are never committed. AWS sends a confirmation email to the alert address for the budget alerts.

`CreateGrcBudget` (default `true`) controls the budget. To skip it when the account already has a 10 USD account-wide budget, pass `CreateGrcBudget=false` and leave out `BudgetAlertEmail`. A template rule requires `BudgetAlertEmail` whenever `CreateGrcBudget` is `true`.

Deployed 2026-10-14 with `CreateGrcBudget=false`, because `340collective-monthly-5usd` already caps the account at 10 USD. The first attempt rolled back because IAM rejects a wildcard service in a resource ARN (`arn:aws:*:...`). `DenyProtectedProduction` now lists each service that holds 340 production resources (CloudFormation, Lambda, Logs, SQS, Scheduler, DynamoDB, SNS, CloudWatch). That brings the boundary to 6,141 of 6,144 characters, so any new boundary statement has to be paid for by trimming another one.

## Onboarding (after deploy)

1. The ISSM sets a temporary console password for each user:

   ```
   aws iam create-login-profile --user-name <user> --password '<temp>' --password-reset-required --profile 340collective
   ```

2. The ISSM shares the temporary password out of band (never in the repo, GitHub, or Jira), along with the sign-in URL from the stack output `ConsoleSignInUrl`: https://570814274897.signin.aws.amazon.com/console
3. The user signs in, sets a new password, and enrolls a virtual MFA device (IAM, Security credentials, Assign MFA device).
4. The user signs out and back in with MFA. Only then do their group permissions work.
5. Optional, for CLI use: the user creates their own access key, then gets MFA session credentials with `aws sts get-session-token --serial-number <mfa-arn> --token-code <code>`. Calls made without MFA are denied.

## Access changes and offboarding

Every change is a PR that edits this template, approved by the ISSM.

When someone leaves, the ISSM:

1. Deletes their login profile, access keys, and MFA devices, so the IAM user can no longer sign in or call AWS.
2. Reviews every `grc-*` role trust policy (`aws iam list-roles`, then `aws iam get-role` for each `grc-*` role) and removes or tightens any trust that names a principal other than an AWS service, such as another account, an IAM user, or `"AWS": "*"`. A trust policy can point outside the account and keeps working after the user is gone.
3. Reviews and removes outside principals from `grc-*` resource policies: S3 bucket policies (`aws s3api get-bucket-policy`), KMS key policies on `grc-project` tagged keys (`aws kms get-key-policy`), Lambda function resource permissions and function URLs (`aws lambda get-policy`, `aws lambda list-function-url-configs`), SNS topic policies (`aws sns get-topic-attributes`), and SQS queue policies (`aws sqs get-queue-attributes --attribute-names Policy`).
4. Deletes any `grc-*` stack, role, or resource the person owned that no longer has a project owner.
5. Opens a PR that removes or renames the user in this template, and records the review result in that PR.

## Teardown

```
aws cloudformation delete-stack --stack-name grc-access-model --profile 340collective --region us-east-1
```

Delete any login profile, access keys, and MFA devices the users added first, or the user deletion fails. The ISSM also deletes any `grc-*` stacks the engineer built before tearing down this stack.

## Validation

[validate_policies.py](validate_policies.py) renders every policy for the account and region, then checks size, Access Analyzer findings, boundary deny parity, file hygiene, and an `iam simulate-custom-policy` scenario matrix for the engineer, the analyst, and a bounded workload role. It only makes read-only, unbilled calls.

```
python3 -m venv /tmp/grc_cfnlint && /tmp/grc_cfnlint/bin/pip install cfn-lint==1.57.2
/tmp/grc_cfnlint/bin/cfn-lint access-model/grc-access.yaml
aws cloudformation validate-template --template-body file://access-model/grc-access.yaml --profile 340collective --region us-east-1
AWS_PROFILE=340collective AWS_REGION=us-east-1 /tmp/grc_cfnlint/bin/python access-model/validate_policies.py --account-id 570814274897 --region us-east-1 --engineer <EngineerUserName> --analyst <AnalystUserName>
```

`--engineer` and `--analyst` are required and take the same values as the deploy parameters.

Results at the time of this PR: cfn-lint clean, validate-template passes (CAPABILITY_NAMED_IAM), every policy is under 6,144 characters, Access Analyzer returns zero findings of any type on all seven policies, and every simulation scenario matches its expected decision.

## Known gaps

- The Auditor's and Stakeholder's groups and the ISSM's admin user are hand-made, outside CloudFormation. That conflicts with "access is not granted by hand". This is a candidate deviation request.
- `ReadOnlyAccess` on `Leadership` and `ExtAuditor` can read S3 object data and likely SSM SecureString values (see above).
- The account has no IAM password policy, and CloudFormation has no native resource for one. The ISSM should set one by hand or through a later change.
- This account is the organization's management account, so SCPs (project 11) cannot apply here. The permissions boundary is the preventive control.
- Trust policies and resource policies on `grc-*` resources can still name outside principals. The offboarding review above is the backstop. A free account-level IAM Access Analyzer through a later PR would flag that automatically.
- Accepted risk (separation of duties): the engineer can delete the Config recorder, delete the GuardDuty detector, or disable Security Hub once they are enabled. This is deliberate, because the engineer must tear these down after evidence is collected, per GOVERNANCE.md. Compensating controls: `DenyAuditTampering` keeps CloudTrail running and unaltered, so every disable or delete call is logged; the ISSM reviews each teardown; and the 1 USD ACTUAL budget alert flags unexpected spend.
- Cost gap: Lambda provisioned concurrency and DynamoDB provisioned capacity on `grc-*` resources are not pre-denied. The 1 USD ACTUAL budget alert catches them after the fact, not before.
- The analyst cannot build infrastructure for 07, 08, and 12. SES, Cognito, QuickSight, Macie, EC2, and Secrets Manager each need a later access-change PR.
