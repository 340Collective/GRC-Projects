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
| IAM users | `EngineerUserName` (default `rasheed`), `AnalystUserName` (default `adam`) | One user per group, boundary attached, tagged `grc-role` and `grc-function` |
| Budget | `grc-projects-monthly` | 10 USD monthly cost budget, ACTUAL alerts at 1, 5, and 10 USD |

Both groups also get the AWS managed `SecurityAudit` and `job-function/ViewOnlyAccess` policies as their read baseline. Neither returns S3 object data or SSM parameter values. `ReadOnlyAccess` is not used anywhere in this template.

No passwords, access keys, or email addresses are in the template. The budget email is a deploy-time parameter with no default.

## What each role can and cannot do

| Role | Access | Can | Cannot |
| --- | --- | --- | --- |
| ISSE / Engineer | `GRC-Engineer` (this template) | Create, update, and delete `grc-*` CloudFormation stacks. Build `grc-*` S3 buckets, Lambda functions, DynamoDB tables, SNS topics, SQS queues, EventBridge rules and buses, schedules, Step Functions, CloudWatch alarms and dashboards, Glue and Athena, CodeBuild and CodePipeline, Backup vaults, `/grc/` SSM parameters, and SSM Automation documents. Create API Gateway APIs tagged `grc-project` and KMS keys tagged `grc-project`. Turn on and configure Security Hub, Config, GuardDuty, Inspector, and Audit Manager for this account. Create `grc-*` roles only with the boundary attached, and pass them only to AWS services. Read everything SecurityAudit and ViewOnlyAccess show, plus CloudTrail log objects for Athena. | Touch any `collective340-*` stack, role, function, table, topic, schedule, alarm, or log group, the `cloudtrail` stack, the trail, the 340 buckets, or the three production HTTP APIs. Read or write any SSM parameter outside `/grc/`, including `/340collective/*`. Create, edit, or delete any IAM user or group, the access-model policies, or the boundary. Remove a role's boundary or attach admin policies. Assume non-`grc-` roles. Manage another user's keys, password, or MFA. Create, edit, or delete budgets, billing, or org settings. Work outside us-east-1. Use the budget-breaker services listed below. |
| ISSO / Analyst | `GRC-Analyst` (this template) | Read Security Hub, Config, GuardDuty, Inspector, Audit Manager, and IAM Access Analyzer. Export Inspector finding reports and SBOMs, and create Audit Manager assessment reports. Generate and read the IAM credential report and service last-accessed data. Look up CloudTrail events. Read `grc-*` buckets, tables, Lambda logs, the Glue catalog, and Athena workgroups. Write (never delete) objects to `grc-evidence-*` buckets. | Build or change any infrastructure (no stacks, functions, or role passing). Read or write object data in any non-`grc-` bucket, including the site and client-media buckets. Read `/340collective/*` parameters or any secret value. Update Security Hub findings. Work outside us-east-1. |
| Auditor / Assessor | Existing hand-made `ExtAuditor` group (not in this template) | Independent read-only assessment through AWS managed `ReadOnlyAccess`. | Write anything. See the note below about object data. |
| Stakeholder / Business Owner | Existing hand-made `Leadership` group (not in this template) | Read-only view of the account through AWS managed `ReadOnlyAccess`. This is already read-only, so no change is needed. | Write anything. Approve changes (per GOVERNANCE.md). |
| ISSM / Program Lead | Existing hand-made admin identity (not in this template) | Deploys, updates, and tears down this stack after PR approval. Sets temporary console passwords. | Not covered by this template. |

Both new groups must enroll MFA before anything else works (see Onboarding).

### Existing hand-made identities

The Auditor and Stakeholder already have IAM users in the hand-made `ExtAuditor` and `Leadership` groups. This template does not change or reference them. Both groups use AWS managed `ReadOnlyAccess`, which allows `s3:GetObject` on every bucket, including the site and client-media buckets, and `ssm:GetParameter*`. With the default `aws/ssm` key, that likely includes the SecureString values under `/340collective/` (Stripe and others).

Recommendation for a later access-change PR, not done here: move `ExtAuditor` (and `Leadership`) from `ReadOnlyAccess` to `SecurityAudit` plus `job-function/ViewOnlyAccess`, the same baseline these new groups use, and bring both groups into CloudFormation so access is no longer granted by hand.

## Guardrails mapped to policy statements

| Requirement | Where it is enforced (Sid) |
| --- | --- |
| Engineer works only on `grc-*` resources | Resource scoping in `grc-engineer-build` and `grc-engineer-security` |
| Roles only `grc-*`, only with the boundary | `IamCreateBoundedGrcRoles` (allow), `DenyRoleWithoutGrcBoundary`, `DenyIamWritesOutsideGrc`, boundary `AllowGrcRoleAdmin` |
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

Size trims applied to fit 6,144 characters (no deny was weakened): `health`, `xray`, and `ce` reads were left out of the boundary, so ViewOnlyAccess pages for those services are empty for both users. Several action lists use wildcards that match only the intended write actions.

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
aws cloudformation deploy --template-file access-model/grc-access.yaml --stack-name grc-access-model --capabilities CAPABILITY_NAMED_IAM --parameter-overrides BudgetAlertEmail=<from private roster> --profile 340collective --region us-east-1
```

The alert address comes from the private roster and is never committed. AWS sends a confirmation email to that address for the budget alerts.

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

Every change is a PR that edits this template, approved by the ISSM. To remove a person, the ISSM deletes their login profile and access keys, then a PR removes or renames the user.

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
AWS_PROFILE=340collective AWS_REGION=us-east-1 /tmp/grc_cfnlint/bin/python access-model/validate_policies.py --account-id 570814274897 --region us-east-1
```

Results at the time of this PR: cfn-lint clean, validate-template passes (CAPABILITY_NAMED_IAM), every policy is under 6,144 characters, Access Analyzer returns zero findings of any type on all seven policies, and every simulation scenario matches its expected decision.

## Known gaps

- The Auditor's and Stakeholder's groups and the ISSM's admin user are hand-made, outside CloudFormation. That conflicts with "access is not granted by hand". This is a candidate deviation request.
- `ReadOnlyAccess` on `Leadership` and `ExtAuditor` can read S3 object data and likely SSM SecureString values (see above).
- The account has no IAM password policy, and CloudFormation has no native resource for one. The ISSM should set one by hand or through a later change.
- This account is the organization's management account, so SCPs (project 11) cannot apply here. The permissions boundary is the preventive control.
- Trust policies and resource policies on `grc-*` resources can still name outside principals. A free account-level IAM Access Analyzer through a later PR would flag that.
- The analyst cannot build infrastructure for 07, 08, and 12. SES, Cognito, QuickSight, Macie, EC2, and Secrets Manager each need a later access-change PR.
