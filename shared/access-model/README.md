# GRC access model

Least-privilege AWS IAM access for the GRC Projects team in 340 Collective's account (see the runbooks) in us-east-1, defined as code in [infrastructure/cloudformation/grc-access-model.yaml](../../infrastructure/cloudformation/grc-access-model.yaml) in this repo. This is the access model that [GOVERNANCE.md](../../GOVERNANCE.md) ("Access to the real environment") calls for. Plain IAM users, plus IAM Identity Center for the two extra engineer seats (stack `grc-identity-center`). Roles are referenced by function, not by person.

Status: deployed 2026-10-14 by the ISSM as stack `grc-access-model` (`CreateGrcBudget=false`). Later changes go through a pull request, then a change set.

The template, the policy validator, and the GRC change records live in this repo's [infrastructure/](../../infrastructure/README.md) folder (moved from the private website repo on 2026-10-17) and are deployed only by the ISSM from this repo's clean `main`. The commands below run from `infrastructure/` (`cd infrastructure` first). Propose access changes as a pull request that edits the template; the ISSM approves and deploys it. The full template documentation is [infrastructure/cloudformation/grc-access-model/README.md](../../infrastructure/cloudformation/grc-access-model/README.md).

## What the stack creates

| Resource | Name | Purpose |
| --- | --- | --- |
| Permissions boundary | `grc-permissions-boundary` | Ceiling for both users and for every role the engineer creates |
| Group | `GRC-Engineer` | ISSE / Engineer |
| Group | `GRC-Analyst` | ISSO / Analyst |
| Engineer policies | `grc-engineer-build`, `grc-engineer-security`, `grc-engineer-guardrails`, `grc-engineer-limits` | One engineer policy split four ways to fit the 6,144 character managed policy quota |
| Analyst policy | `grc-analyst` | Security service reads, finding export, evidence writes |
| Group | `GRC-Auditor` | Internal Auditor. Read-only audit, MFA required, no boundary (planned, not deployed) |
| Internal Auditor policies | `internal-auditor-read`, `internal-auditor-guardrails` | Audit reads (every allow requires MFA), and explicit denies for secrets, key use, non-audit object data, identity admin, and changes to audited systems |
| MFA policy | `grc-require-mfa` | Self-service credentials, and deny everything until MFA is used. Attached to all three groups |
| IAM users | `EngineerUserName`, `AnalystUserName` (required deploy-time parameters, no defaults) | One user per group, boundary attached, tagged `grc-role` and `grc-function` |
| IAM user (optional) | `InternalAuditorUserName` (deploy-time parameter, empty skips it) | The Internal Auditor, in `GRC-Auditor`, no boundary, tagged `grc-role=auditor` and `grc-function=Internal-Auditor` |
| Budget | `grc-projects-monthly` | 10 USD monthly cost budget, ACTUAL alerts at 1, 5, and 10 USD |

All three groups also get the AWS managed `SecurityAudit` and `job-function/ViewOnlyAccess` policies as their read baseline. Neither returns S3 object data or SSM parameter values. `ReadOnlyAccess` is not used anywhere in this template. The engineer and analyst users also carry the permissions boundary, so these managed policies only take effect for services the boundary allows (see "Effective read scope" below). The Internal Auditor user has no boundary (see "Internal Auditor design" below).

No passwords, access keys, email addresses, or person names are in the template. The budget email and both user names are deploy-time parameters with no default.

## What each role can and cannot do

| Role | Access | Can | Cannot |
| --- | --- | --- | --- |
| ISSE / Engineer | `GRC-Engineer` (this template) | Create, update, and delete `grc-*` CloudFormation stacks. Build `grc-*` S3 buckets, Lambda functions, DynamoDB tables, SNS topics, SQS queues, EventBridge rules and buses, schedules, Step Functions, CloudWatch alarms and dashboards, Glue and Athena, CodeBuild and CodePipeline, Backup vaults, `/grc/` SSM parameters, and SSM Automation documents. Create API Gateway APIs tagged `grc-project` and KMS keys tagged `grc-project`. Turn on and configure Security Hub, Config, GuardDuty, Inspector, and Audit Manager for this account. Create `grc-*` roles only with the boundary attached, change their trust policies, and pass them only to AWS services. Read the SecurityAudit and ViewOnlyAccess views for the services in "Effective read scope" below, plus CloudTrail log objects for Athena. Open AWS CloudShell in us-east-1 after signing in with MFA (standard environments only). CloudShell runs with the engineer's own console session, so every guardrail applies. | Touch any `collective340-*` stack, role, function, table, topic, schedule, alarm, or log group, the `cloudtrail` stack, the trail, the 340 buckets, or the three production HTTP APIs. Use `grc-*` S3 permissions on buckets owned by another account. Read or write any SSM parameter outside `/grc/`, including `/340collective/*`. Create, edit, or delete any IAM user or group, the access-model policies, or the boundary. Remove a role's boundary or attach admin policies. Assume any role directly, including the `grc-*` roles they create (those are for AWS services only). Manage another user's keys, password, or MFA. Create, edit, or delete budgets, billing, or org settings. Work outside us-east-1. Use the budget-breaker services listed below. Create CloudShell VPC environments (no EC2 network-interface rights). |
| ISSO / Analyst | `GRC-Analyst` (this template) | Read Security Hub, Config, GuardDuty, Inspector, Audit Manager, and IAM Access Analyzer. Export Inspector finding reports and SBOMs, and create Audit Manager assessment reports. Generate and read the IAM credential report and service last-accessed data. Look up CloudTrail events. Read `grc-*` buckets, tables, Lambda logs, the Glue catalog, and Athena workgroups. Write (never delete) objects to `grc-evidence-*` buckets in this account. Read the SecurityAudit and ViewOnlyAccess views for the services in "Effective read scope" below. | Build or change any infrastructure (no stacks, functions, or role passing). Read or write object data in any non-`grc-` bucket, including the site and client-media buckets. Read `/340collective/*` parameters or any secret value. Update Security Hub findings. Work outside us-east-1. |
| Internal Auditor | `GRC-Auditor` (this template; planned, not deployed) | With MFA: the SecurityAudit plus ViewOnlyAccess view of the whole account. Read Security Hub, Config, GuardDuty, Inspector, Audit Manager, and IAM Access Analyzer. Generate and read the IAM credential report and service last-accessed data, and simulate principal policies. Look up CloudTrail events and read CloudTrail log objects. Read `grc-*` evidence buckets (objects, versions, tags, retention, legal hold), `grc-*` tables, `grc-*` Lambda logs, and the `grc` Glue catalog. Decrypt through S3 only, only with KMS keys tagged `grc-project`. | Write, change, or delete anything, including Security Hub findings. Read any SSM parameter value or Secrets Manager secret. Use KMS outside S3 or on keys not tagged `grc-project`. Read object data in any bucket other than `grc-*` and the CloudTrail log bucket. Change any IAM user, group, role, or policy, or pass or assume a role. Run Lambda functions, SSM commands, or sessions. Do anything without MFA. |
| Stakeholder / Business Owner | Existing hand-made `Leadership` group (not in this template) | Read-only view of the account through AWS managed `ReadOnlyAccess`. This is already read-only, so no change is needed. | Write anything. Approve changes (per GOVERNANCE.md). |
| Automation Engineer and ISSM as builder (planned, not deployed) | `GRC-Engineer` seats for Maria (`maria`) and Faris (`faris`), created by the companion stack `grc-engineer-users` ([infrastructure/cloudformation/grc-engineer-users.yaml](../../infrastructure/cloudformation/grc-engineer-users.yaml)) | The same as the ISSE / Engineer row: same `GRC-Engineer` group, same `grc-permissions-boundary`, and the same group-attached `grc-require-mfa` rule. Nothing is set per user. | The same as the ISSE / Engineer row. The stack holds no login profile, access key, password, or email. |
| ISSM / Program Lead | Existing hand-made admin identity (not in this template) | Deploys, updates, and tears down this stack after PR approval. Sets temporary console passwords. Faris also builds (the shared foundation and 01) with the planned `faris` `GRC-Engineer` seat, not with the admin identity; Adam (ISSO) approves changes to that seat. | Not covered by this template. |

Every user in these three groups must enroll MFA before anything else works (see Onboarding).

### Internal Auditor design

- A group, not an assumable role, to match every other GRC seat (plain IAM users in groups, no SSO) and the 14 Okta group `GRC-Auditor` one to one.
- The policy names `internal-auditor-read` and `internal-auditor-guardrails` deliberately do not start with `grc-`. The engineer may edit any `grc-*` policy, so a `grc-` name would let the engineer widen or weaken the auditor's access. Non-`grc-` names are covered by `DenyIamWritesOutsideGrc` and the boundary's narrow IAM allow, with no change to the boundary (which is at 6,131 of 6,144 characters).
- No permissions boundary on the auditor user. The boundary caps reads to the services the engineer may build with, and an auditor needs the full SecurityAudit view (Organizations, SES, Secrets Manager metadata, and so on). The boundary exists to cap identities that can create roles. The auditor cannot create, pass, or assume roles.
- MFA twice: `grc-require-mfa` on the group, and an `aws:MultiFactorAuthPresent` condition on every allow in `internal-auditor-read`.
- Secrets: `DenySecretValues` denies every SSM parameter read (`GetParameter`, `GetParameters`, `GetParametersByPath`, `GetParameterHistory`) and every secret value, so no SecureString can be read by any path. `kms:Decrypt` through SSM is denied on its own as well.
- Jira: no AWS access is added for Jira. Jira (`340collective.atlassian.net`, project `GRC`) is outside AWS. Evidence attached to a Jira item is downloaded with the audit reads above and uploaded in Jira.

### Effective read scope

The permissions boundary caps both users, so `SecurityAudit` and `ViewOnlyAccess` reads only work for services the boundary allows. Everything else those managed policies grant is implicitly denied.

- Readable (subject to the explicit denies, for example no S3 object data or SSM values outside `grc-*` and `/grc/`): CloudFormation, STS, S3 bucket metadata, Lambda, CloudWatch Logs, EventBridge and EventBridge Scheduler, Step Functions, DynamoDB, SNS, SQS, CloudWatch, API Gateway, Glue, Athena, CodeBuild, CodePipeline, AWS Backup, Systems Manager, KMS, Security Hub, Config, GuardDuty, Inspector, Audit Manager, IAM Access Analyzer, CloudTrail, Resource Groups Tagging, IAM reads, budget reads, EC2 describes, Route 53, CloudFront, ACM, and Service Quotas.
- Not readable (AccessDenied, empty console pages): every other service, including RDS, ECR, ELB, EKS, ECS, Organizations, SES, Cognito, Secrets Manager, Health, X-Ray, and Cost Explorer. Security Hub and Config cover most of that inventory once they are enabled.

### Existing hand-made identities

This template does not change or reference these.

- `Jason-Contractor-Auditor`, the former external auditor's hand-made user in `ExtAuditor`, stays as is until it is retired. It is deliberately not imported into `iam-baseline`. Once the Internal Auditor user in `GRC-Auditor` is live and has signed in with MFA, the ISSM retires it with the committed runbook in [infrastructure/runbooks/IAM-CHANGES-2026-10-14-GRC.md](../../infrastructure/runbooks/IAM-CHANGES-2026-10-14-GRC.md) section 9.
- `ExtAuditor` stays in the `iam-baseline` import, unchanged, and is empty after that retirement. Whether to retire the group too is a later owner call.
- `Leadership` is unchanged. It uses AWS managed `ReadOnlyAccess`, which allows `s3:GetObject` on every bucket, including the site and client-media buckets, and `ssm:GetParameter*`. With the default `aws/ssm` key, that likely includes the SecureString values under `/340collective/` (Stripe and others). `ExtAuditor` has the same exposure until it is empty.

Recommendation for a later access-change PR, not done here: move `Leadership` from `ReadOnlyAccess` to `SecurityAudit` plus `job-function/ViewOnlyAccess`, the same baseline these groups use.

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
| Engineers use CloudShell, standard environments only, MFA first | `CloudShellNoVpc` (in `grc-engineer-security`), boundary `AllowServices`, `DenyAllExceptMfaSetupWithoutMfa`, `DenyOutsideUsEast1` |
| Budget breakers from GOVERNANCE.md | `DenyBudgetBreakers` (QuickSight, EC2 instances and fleets, NAT gateways, RDS, Redshift, SageMaker, OpenSearch, ELB, EKS, ECS, ElastiCache, MSK, Macie, Shield Advanced, domains, Savings Plans, Marketplace, Secrets Manager), `DenyOrgAdminAndCostly` (Glue jobs and sessions, DynamoDB reserved capacity, paid analyzers) |
| Evidence and audit trail stay intact | `DenyAuditTampering` (CloudTrail changes, S3 governance-mode bypass) |
| CloudFormation cannot run as a privileged role | `DenyCloudFormationNonGrcServiceRole` |
| MFA before anything | `DenyAllExceptMfaSetupWithoutMfa` |
| Self-service password, MFA, and keys | `AllowManageOwnCredentials`, `AllowCreateOwnVirtualMfa`, `AllowDeactivateOwnMfaOnlyWithMfa` |

Internal Auditor (`internal-auditor-read` allows, `internal-auditor-guardrails` denies):

| Requirement | Where it is enforced (Sid) |
| --- | --- |
| Read security services and findings, with MFA | `AuditSecurityServices` |
| Credential report, last-accessed data, policy simulation, CloudTrail events | `AuditIdentityAndTrail` |
| Read CloudTrail log objects | `AuditCloudTrailLogObjects` |
| Read `grc-*` evidence buckets in this account | `AuditGrcEvidenceBuckets` |
| Read `grc-*` tables, Lambda logs, and Glue catalog | `AuditGrcRecords` |
| Decrypt SSE-KMS evidence only through S3, only with `grc-project` keys | `DecryptGrcEvidenceViaS3`, `DenyKmsUseOutsideS3`, `DenyKmsUseOnNonGrcKeys` |
| No SSM parameter or secret values | `DenySecretValues`, `DenyKmsDecryptViaSsm` |
| No object data outside `grc-*` and CloudTrail logs | `DenyNonAuditObjectData` |
| No IAM user, group, role, or policy changes, no PassRole, no role assumption | `DenyIdentityAdmin` (does not match the self-service actions in `grc-require-mfa`) |
| No changes to CloudTrail, Config, Security Hub, GuardDuty, Inspector, Audit Manager, Access Analyzer, S3, CloudFormation, Lambda, DynamoDB, SSM, or KMS | `DenyChangesToAuditedSystems` |
| MFA before anything | `aws:MultiFactorAuthPresent` on every allow, plus `DenyAllExceptMfaSetupWithoutMfa` |

Enabling any denied budget-breaker service needs a later access-change PR and a cost check, per GOVERNANCE.md.

## Permissions boundary

`grc-permissions-boundary` is attached to both users and is required (`iam:PermissionsBoundary` condition) on every role the engineer creates. A bounded role can never do more than the boundary allows, whatever policies are attached to it.

- Allows only the in-scope services (`AllowServices`, which includes CloudShell), a short read list (EC2, Route 53, CloudFront, ACM, and Service Quotas describes, plus IAM and budget reads), and IAM writes only on `grc-*` policies, `grc-*` roles, MFA devices, and the caller's own user. The boundary lists CloudShell as `cloudshell:*` like every other service, because it grants nothing alone; the engineer's rights are the ten actions in `CloudShellNoVpc`, and the analyst has no CloudShell allow.
- PassRole only for `grc-*` roles (and the Config service-linked role) to the listed AWS services. Service-linked roles only for the security services.
- Repeats the explicit denies that matter for workload roles. Every deny in the boundary is byte-identical in `grc-engineer-guardrails` (checked by the validator).
- Not in the boundary, by design: identity-admin and access-model attach denies. The boundary's narrow IAM allow already blocks users, groups, and non-grc roles. Attaching an access-model policy to a bounded role cannot exceed the boundary. The engineer user still has those explicit denies in `grc-engineer-guardrails`.

Size trims applied to fit 6,144 characters (no deny was weakened): the read list is short, so SecurityAudit and ViewOnlyAccess are clipped to the services in "Effective read scope" for both users. Several action lists use wildcards that match only the intended write actions. To fit `cloudshell:*`, three allow Sids were shortened (`AllowInScopeServices` to `AllowServices`, `AllowSecurityServiceLinkedRoles` to `AllowServiceLinkedRoles`, `AllowVisibilityReads` to `AllowReads`). A Sid has no effect on evaluation.

The boundary allows several services on `Resource: "*"`, so production resources are protected by name. New production resources must use the `collective340-` or `340collective` prefixes to stay covered by `DenyProtectedProduction`.

## Resource naming rules

- Everything the engineer builds is named `grc-*`. Glue databases and tables may also use `grc_`.
- Reserved for the access model: `grc-permissions-boundary`, `grc-engineer*`, `grc-analyst*`, and `grc-require-mfa*` policies, the `internal-auditor-*` policies, the `GRC-Engineer`, `GRC-Analyst`, and `GRC-Auditor` groups, and the `grc-access-model`, `grc-internal-auditor`, `grc-uar-sim-*` (temporary UAR simulation), and planned `grc-engineer-users` stacks. The engineer cannot create or edit these IAM resources. `grc-access-model` is also protected by `DenyProtectedProduction`; the other stacks are protected only at the IAM layer, because every IAM user write is denied to the engineer.
- Analyst-writable evidence buckets are `grc-evidence-*`. Athena query results should go to one.
- SSM parameters go under `/grc/`.
- KMS keys and API Gateway APIs must be created with a `grc-project` tag.
- Stage Lambda code and packaged templates in a `grc-*` bucket.
- If the engineer passes a CloudFormation service role, it must be a `grc-*` role.

## Cost

- The IAM resources are free.
- `grc-projects-monthly` is a monitoring-only budget (no budget actions), which carries no charge. It covers the whole account, since the org has one account. Credits and refunds are excluded so they cannot hide real usage.
- Existing budget, checked read-only with `aws budgets describe-budgets`: `340collective-monthly-5usd` (COST, MONTHLY, 10 USD limit despite its name) alerts at ACTUAL 80%, ACTUAL 100%, and FORECASTED 100%. It is owned by the `collective340-budget` stack and has no alerts at 1, 5, or 10 USD. It is left unchanged; the GRC budget is separate and has a distinct name.
- Customer managed KMS keys cost about 1 USD per month each. Security Hub, Config, GuardDuty, Inspector, and Audit Manager charge after their trials. Scale them down or pause them per the running system cost rule in GOVERNANCE.md, and turn them off in the end-of-program teardown.

## Deploy (ISSM, after PR approval, from a clean main)

Follow the deploy sequence in [infrastructure/README.md](../../infrastructure/README.md). The command, from `infrastructure/`:

```
cd infrastructure
aws cloudformation deploy --template-file cloudformation/grc-access-model.yaml --stack-name grc-access-model --capabilities CAPABILITY_NAMED_IAM --parameter-overrides EngineerUserName=<from private roster> AnalystUserName=<from private roster> BudgetAlertEmail=<from private roster> --profile 340collective --region us-east-1
```

The two user names are required and have no default. They and the alert address come from the private roster and are never committed. AWS sends a confirmation email to the alert address for the budget alerts.

`InternalAuditorUserName` (default empty, which creates no user) adds the Internal Auditor user to `GRC-Auditor`. The `GRC-Auditor` group and both `internal-auditor-*` policies are created either way. For the existing stack, this is applied as a change set that adds exactly four resources; the steps are in [infrastructure/runbooks/IAM-CHANGES-2026-10-14-GRC.md](../../infrastructure/runbooks/IAM-CHANGES-2026-10-14-GRC.md) section 9.

`CreateGrcBudget` (default `true`) controls the budget. To skip it when the account already has a 10 USD account-wide budget, pass `CreateGrcBudget=false` and leave out `BudgetAlertEmail`. A template rule requires `BudgetAlertEmail` whenever `CreateGrcBudget` is `true`.

Deployed 2026-10-14 with `CreateGrcBudget=false`, because `340collective-monthly-5usd` already caps the account at 10 USD. The first attempt rolled back because IAM rejects a wildcard service in a resource ARN (`arn:aws:*:...`). `DenyProtectedProduction` now lists each service that holds 340 production resources (CloudFormation, Lambda, Logs, SQS, Scheduler, DynamoDB, SNS, CloudWatch). That brought the boundary to 6,141 of 6,144 characters. The CloudShell change adds `cloudshell:*` and pays for it with three shorter Sids, so the boundary is now 6,131 of 6,144, and any new boundary statement has to be paid for by trimming another one.

## Onboarding (after deploy)

1. The ISSM sets a temporary console password for each user:

   ```
   aws iam create-login-profile --user-name <user> --password '<temp>' --password-reset-required --profile 340collective
   ```

2. The ISSM shares the temporary password out of band (never in the repo, GitHub, or Jira), along with the sign-in URL from the stack output `ConsoleSignInUrl`: https://<account-id>.signin.aws.amazon.com/console
3. The user signs in, sets a new password, and enrolls a virtual MFA device (IAM, Security credentials, Assign MFA device).
4. The user signs out and back in with MFA. Only then do their group permissions work. For the AWS CLI without an access key, open CloudShell from the console (region US East (N. Virginia)) after signing in with MFA.
5. For the AWS CLI, no access key is needed: after signing in to the console with MFA, the user runs `aws login` (AWS CLI 2.32 or later) and approves it in the browser. The CLI gets short-lived credentials for up to 12 hours. `SignInLocalDevelopmentAccess` on the group and `signin:*` in the boundary allow it.

Identity Center seats: the Automation Engineer and ISSM builder seats sign in through IAM Identity Center instead (stack `grc-identity-center`, [runbook](../../infrastructure/runbooks/IAM-CHANGES-2026-10-22-identity-center-and-aws-login.md)). They use the AWS access portal with an emailed one-time code at first sign-in and MFA at every sign-in, and get the role `GRC-Engineer`: the same policies and boundary as the `GRC-Engineer` group, without `grc-require-mfa`. In the terminal they run `aws configure sso` once, then `aws sso login`.

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

[infrastructure/cloudformation/grc-access-model/validate_policies.py](../../infrastructure/cloudformation/grc-access-model/validate_policies.py) renders every policy for the account and region, then checks size, Access Analyzer findings, boundary deny parity, file hygiene, and an `iam simulate-custom-policy` scenario matrix for the engineer, the analyst, a bounded workload role, and, with `--auditor`, the Internal Auditor (simulated without a boundary). It only makes read-only, unbilled calls. `--skip-aws` runs only the offline checks (size, parity, hygiene) and makes no AWS call.

```
cd infrastructure
python3 -m venv /tmp/grc_cfnlint && /tmp/grc_cfnlint/bin/pip install cfn-lint==1.57.2
/tmp/grc_cfnlint/bin/cfn-lint cloudformation/grc-access-model.yaml
aws cloudformation validate-template --template-body file://cloudformation/grc-access-model.yaml --profile 340collective --region us-east-1
AWS_PROFILE=340collective AWS_REGION=us-east-1 /tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py --account-id <account-id> --region us-east-1 --engineer <EngineerUserName> --analyst <AnalystUserName> --auditor <InternalAuditorUserName>
```

`--engineer` and `--analyst` are required and take the same values as the deploy parameters. `--auditor` is optional and adds the Internal Auditor scenarios.

Internal Auditor change (this branch, not deployed): cfn-lint clean, and `--skip-aws` shows `internal-auditor-read` and `internal-auditor-guardrails` under 6,144 characters, boundary parity unchanged, and hygiene clean. Access Analyzer and the simulation matrix (including the auditor scenarios) run at deploy time, from a clean main.

Results at the time of this PR: cfn-lint clean, validate-template passes (CAPABILITY_NAMED_IAM), every policy is under 6,144 characters, Access Analyzer returns zero findings of any type on all seven policies, and every simulation scenario matches its expected decision.

CloudShell change (this branch, not deployed): cfn-lint clean, validate-template passes, `grc-access-model.yaml` is 49,740 bytes, the boundary is 6,131 and `grc-engineer-security` 3,956 characters, all 12 deny parity rows identical, Access Analyzer zero findings on all nine policies, and 116 of 116 simulation scenarios pass. The ten CloudShell actions are allowed with MFA in us-east-1, and denied without MFA, outside us-east-1, for `cloudshell:ApproveCommand`, for `ec2:CreateNetworkInterface` (no VPC environments), and for the analyst. Change record: [infrastructure/runbooks/IAM-CHANGES-2026-10-17-cloudshell.md](../../infrastructure/runbooks/IAM-CHANGES-2026-10-17-cloudshell.md).

## Known gaps

- The Stakeholder's group and the ISSM's admin user are hand-made, outside CloudFormation (captured for import in `iam-baseline`). That conflicts with "access is not granted by hand". This is a candidate deviation request.
- `ReadOnlyAccess` on `Leadership` can read S3 object data and likely SSM SecureString values (see above). `ExtAuditor` has the same exposure until `Jason-Contractor-Auditor` is retired.
- The Internal Auditor has no build or write access, so he builds nothing. On the projects he partners (01, 02, 03, 04, 09, 10, 13), the assigned engineer deploys from a `GRC-Engineer` seat after ISSM approval (see GOVERNANCE.md, Two-track model).
- The Internal Auditor cannot query the 06 evidence lake with Athena, because Athena writes query results to S3. Add it with a `grc-evidence-*` results bucket in a later access-change PR if needed.
- CloudFormation has no native resource for the IAM account password policy, so the ISSM set it by hand on 2026-10-14: at least 14 characters, with uppercase, lowercase, a number, and a symbol; the last 24 passwords cannot be reused; passwords do not expire; users can change their own. It applies from each user's next password change.
- Until it is retired, the former external auditor user is not required to use MFA. See deviation DEV-001 below. The Internal Auditor user in `GRC-Auditor` requires MFA.
- This account is the organization's management account, so SCPs (project 11) cannot apply here. The permissions boundary is the preventive control.
- Trust policies and resource policies on `grc-*` resources can still name outside principals. The offboarding review above is the backstop. A free account-level IAM Access Analyzer through a later PR would flag that automatically.
- Accepted risk (separation of duties): the engineer can delete the Config recorder, delete the GuardDuty detector, or disable Security Hub once they are enabled. This is deliberate, because the engineer must scale them down or pause them under the running system cost rule, and turn them off in the end-of-program teardown, per GOVERNANCE.md. Compensating controls: `DenyAuditTampering` keeps CloudTrail running and unaltered, so every disable or delete call is logged; the ISSM reviews each pause and the teardown; and the 1 USD ACTUAL budget alert flags unexpected spend.
- Cost gap: Lambda provisioned concurrency and DynamoDB provisioned capacity on `grc-*` resources are not pre-denied. The 1 USD ACTUAL budget alert catches them after the fact, not before.
- The analyst cannot build infrastructure, so engineers build every project the ISSO partners (05, 06, 07, 08, 11, 12, 14, 15). SES, Cognito, QuickSight, Macie, EC2, and Secrets Manager each need a later access-change PR before an engineer can use them.

## Deviations

Recorded in the format from GOVERNANCE.md (what was required and why it is not done, the risk or control affected, the compensating controls, and the date to revisit).

### DEV-001: Auditor exempt from enforced MFA

- Status: accepted by the ISSM on 2026-10-14. To be closed when the GRC-Auditor user is live with MFA (planned, not deployed).
- Requirement: every human account should require MFA before it can do anything. The `GRC-Engineer` and `GRC-Analyst` groups enforce this through `grc-require-mfa`.
- What is excepted: the Auditor's hand-made IAM user in the `ExtAuditor` group. `grc-require-mfa` is not attached to that group, so the Auditor can sign in with a password alone. MFA is still recommended to him, and his credential reset email asks him to enroll.
- Why: the Auditor is an independent contractor who assesses the program from outside it. His access is read-only and deliberately managed apart from the access model whose controls he assesses. Forcing MFA would block his read-only assessment work until he enrolls, and the ISSM judged the remaining risk acceptable for this role.
- Risk and control affected: MFA for privileged and remote access (NIST 800-53 IA-2(1) and IA-2(2); SOC 2 CC6.1). Someone who obtained his password could read account configuration and, through `ReadOnlyAccess`, S3 object data and possibly SSM SecureString values (see "Existing hand-made identities" above). They could not change anything.
- Compensating controls:
  - The account is read-only: `ReadOnlyAccess` has no write, delete, or IAM change actions.
  - The account password policy requires at least 14 characters with all four character types and blocks reuse of the last 24 passwords.
  - The password was reset with a forced change at the next sign-in, delivered only to his own address.
  - CloudTrail records every API call, and `DenyAuditTampering` keeps the trail running.
  - The quarterly access review (project 08) re-certifies this account and checks for MFA and last activity.
- Revisit: at the next 08 access review, or by 2027-01-14, whichever is first. At that point, either attach `grc-require-mfa` to `ExtAuditor` or move the Auditor to `SecurityAudit` plus `ViewOnlyAccess` (no object-data reads) to shrink what a stolen password exposes.
- Closure (planned): Jason is now the Internal Auditor, an internal role, so the rationale above ("an independent contractor who assesses the program from outside it") no longer holds. His access moves into this access model as the `GRC-Auditor` group, with MFA required and the SecurityAudit plus ViewOnlyAccess baseline. He cannot change that access: he has no IAM writes, the `internal-auditor-*` policy names are outside the engineer's `grc-*` rights, and every change is an ISSM-approved PR. DEV-001 closes when the new user is live and has signed in with MFA, and `Jason-Contractor-Auditor` is retired (IAM-CHANGES section 9). His work is internal audit, not independent attestation.
