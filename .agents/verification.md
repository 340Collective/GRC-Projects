# Verification: GRC access model review fixes (branch grc-access-model, PR #10)

Iteration: first. `.agents/review.json` verdict was APPROVED with 7 LOW findings, so all 7 approved fixes were applied from scratch.

Nothing was deployed. No AWS write calls were made. Only read-only calls were used: cloudformation validate-template and describe-stacks, accessanalyzer validate-policy, iam simulate-custom-policy. Profile 340collective, us-east-1. Nothing was committed or pushed (working tree has 3 modified files: access-model/README.md, access-model/grc-access.yaml, access-model/validate_policies.py; GOVERNANCE.md is unchanged in this step).

## Fixes applied

| # | Finding | Change | Evidence |
| --- | --- | --- | --- |
| 1 | UpdateAssumeRolePolicy blocked by boundary | Policy unchanged, comment added on boundary `AllowGrcRoleAdmin`. See note below: the existing `iam:*RolePolicy` wildcard already matches `iam:UpdateAssumeRolePolicy`, so the finding was a false positive. Two new simulation scenarios added. | engineer `iam:UpdateAssumeRolePolicy` on `role/grc-evidence-lambda` = allowed; on `role/collective340-blog-generator` = explicitDeny (new); on `role/collective340-intake-IntakeRole-...` = explicitDeny (existing) |
| 2 | S3 grc- prefix not pinned to this account | `Condition: StringEquals aws:ResourceAccount: !Ref AWS::AccountId` added to engineer `S3GrcBuckets` (grc-engineer-build) and analyst `AllowEvidenceExportWrite` (grc-analyst). Boundary untouched. Validator now sets `aws:ResourceAccount` = account ID in the default simulation context (AWS populates it on real requests). | engineer PutObject and GetObject on `grc-evidence-test` with ResourceAccount 111122223333 = implicitDeny; analyst PutObject same = implicitDeny; same-account PutObject and `s3:CreateBucket` = allowed |
| 3 | Engineer direct role assumption | New `DenyDirectRoleAssumption` (Deny `sts:AssumeRole` on `*`) in grc-engineer-limits. PassRole rules unchanged. | engineer `sts:AssumeRole` on grc- and collective340- roles = explicitDeny. Deploys still work: `cloudformation:CreateStack` with no service role = allowed, `CreateStack` with `cloudformation:RoleArn` = `role/grc-cfn-deploy` = allowed, `iam:PassRole` `grc-cfn-deploy` to cloudformation.amazonaws.com = allowed. CloudFormation uses the caller's credentials or a passed service role, neither of which is `sts:AssumeRole` by the user. Workload `sts:AssumeRole` scenarios unchanged |
| 4 | Person-name defaults | `Default: rasheed` and `Default: adam` removed from `EngineerUserName` and `AnalystUserName`. Both keep `AllowedPattern ^[A-Za-z0-9+=,._-]{1,64}$` and gained a `ConstraintDescription`. README table and deploy command use `<from private roster>` placeholders. Validator `--engineer` and `--analyst` are now `required=True` with no default. | validate-template returns no `DefaultValue` for any of the 3 parameters. grep for rasheed/adam in access-model/: 0 hits |
| 5 | Offboarding misses outside trust | README "Access changes and offboarding" is now a 5-step procedure: remove login profile, keys, MFA; review every grc- role trust policy; review grc- resource policies (S3 bucket policies, KMS key policies, Lambda resource permissions and function URLs, SNS topic policies, SQS queue policies) with the read commands for each; delete orphaned grc- resources; PR to remove the user | README diff |
| 6 | README overstates read baseline | Engineer and analyst "Can" cells now point to a new "Effective read scope" subsection listing what is readable (the boundary's in-scope services plus its visibility read list) and what is not (RDS, ECR, ELB, EKS, ECS, Organizations, SES, Cognito, Secrets Manager, Health, X-Ray, Cost Explorer, and every other service). The boundary size-trims paragraph was corrected. Also added a line that new production resources must use the collective340-/340collective prefixes to stay protected (from the same review's finding 1 action) | README diff |
| 7 | Detective controls SoD gap | No denies added. README known gaps now records: accepted risk that the engineer can delete the Config recorder, delete the GuardDuty detector, or disable Security Hub (needed for teardown per GOVERNANCE.md), with compensating controls `DenyAuditTampering` (CloudTrail stays on and unaltered), ISSM teardown review, and the 1 USD ACTUAL budget alert; and a cost gap for Lambda provisioned concurrency and DynamoDB provisioned capacity on grc- resources, caught after the fact by the 1 USD ACTUAL alert | README diff |

### Note on fix 1 (false positive in the prior review)

IAM action wildcards match any characters, so `iam:*RolePolicy` matches `iam:UpdateAssumeRolePolicy` ("UpdateAssume" + "RolePolicy") as well as Put/Delete/Get/List/Attach/Detach RolePolicy. Two read-only checks confirm it:

1. With `iam:UpdateAssumeRolePolicy` added explicitly to `AllowGrcRoleAdmin`, Access Analyzer returned `SUGGESTION REDUNDANT_ACTION` on GrcPermissionsBoundary: "The 2 action(s) are redundant because they provide similar permissions. Update the policy to remove the redundant action such as: iam:UpdateAssumeRolePolicy." (101 of 101 scenarios passed on that run too.)
2. With the boundary action list left as it was (the committed version), `simulate-custom-policy` returns `allowed` for engineer `iam:UpdateAssumeRolePolicy` on `role/grc-evidence-lambda`, with the boundary applied as the permissions boundary.

So the boundary and `IamManageGrcRoles` already agreed, and a CloudFormation update that changes a grc- role trust policy would not have failed. I kept the action list unchanged to avoid the redundant-action finding and added a YAML comment above `AllowGrcRoleAdmin` saying the wildcard covers trust updates. The boundary JSON is byte-identical to the previous version (6,002 chars). This is the final state recorded below. If the reviewer prefers the explicit action anyway, it fits (6,031 chars) at the cost of one non-blocking SUGGESTION.

## Commands and results (final state)

| Check | Command | Result |
| --- | --- | --- |
| validate-template | `aws cloudformation validate-template --template-body file://access-model/grc-access.yaml --profile 340collective --region us-east-1` (from the worktree) | exit 0. Capabilities: CAPABILITY_NAMED_IAM (reason: AWS::IAM::ManagedPolicy). Parameters: BudgetAlertEmail, EngineerUserName, AnalystUserName, all with DefaultValue null (required at deploy) |
| cfn-lint | `/tmp/grc_cfnlint/bin/cfn-lint access-model/grc-access.yaml` (cfn-lint 1.57.2, existing /tmp venv) | exit 0: 0 errors, 0 warnings, 0 informational. Run twice, once before and once after the final comment edit |
| Validator | `AWS_PROFILE=340collective AWS_REGION=us-east-1 /tmp/grc_cfnlint/bin/python access-model/validate_policies.py --template access-model/grc-access.yaml --account-id 570814274897 --region us-east-1 --engineer rasheed --analyst adam` | exit 0, `RESULT: all checks passed` |
| Validator: policy size | (same run) | pass, all 7 under 6,144. Boundary 6,002 (unchanged), build 6,046 (was 5,978), limits 1,556 (was 1,464), analyst 4,207 (was 4,139), others unchanged |
| Validator: Access Analyzer | `accessanalyzer validate-policy --policy-type IDENTITY_POLICY` on each of the 7 rendered policies | pass. 0 findings of any type on all 7 (0 ERROR, 0 SECURITY_WARNING, 0 WARNING, 0 SUGGESTION) |
| Validator: boundary deny parity | (same run) | pass. All 12 boundary deny statements byte-identical in the engineer guardrail policies |
| Validator: hygiene | (same run; email regex, AKIA/ASIA key IDs, U+2013/U+2014 over GOVERNANCE.md and every file in access-model/) | pass. All 4 files clean |
| Validator: simulation matrix | `iam simulate-custom-policy` with the boundary as permissions boundary | 101 of 101 pass (was 91; 10 new scenarios listed below) |
| python syntax | `/tmp/grc_cfnlint/bin/python -m py_compile access-model/validate_policies.py` | ok. The `__pycache__` it created was moved to the Trash; working tree clean of it |
| Not deployed | `aws cloudformation describe-stacks --stack-name grc-access-model` | `Stack with id grc-access-model does not exist` |

### New simulation scenarios (10)

| Fix | Principal | Action | Resource | Context | Expected | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | engineer | iam:UpdateAssumeRolePolicy | role/grc-evidence-lambda | | allowed | allowed |
| 1 | engineer | iam:UpdateAssumeRolePolicy | role/collective340-blog-generator | | explicitDeny | explicitDeny |
| 2 | engineer | s3:CreateBucket | arn:aws:s3:::grc-evidence-test | ResourceAccount = this account | allowed | allowed |
| 2 | engineer | s3:PutObject | grc-evidence-test/a.json | ResourceAccount 111122223333 | denied | implicitDeny |
| 2 | engineer | s3:GetObject | grc-evidence-test/a.json | ResourceAccount 111122223333 | denied | implicitDeny |
| 2 | analyst | s3:PutObject | grc-evidence-test/r.csv | ResourceAccount 111122223333 | denied | implicitDeny |
| 3 | engineer | cloudformation:CreateStack | stack/grc-11-guardrails/x | cloudformation:RoleArn = role/grc-cfn-deploy | allowed | allowed |
| 3 | engineer | iam:PassRole | role/grc-cfn-deploy | PassedToService cloudformation.amazonaws.com | allowed | allowed |
| 3 | engineer | sts:AssumeRole | role/grc-evidence-lambda | | explicitDeny | explicitDeny |
| 3 | engineer | sts:AssumeRole | role/collective340-blog-generator | | explicitDeny | explicitDeny |

The existing `cloudformation:CreateStack` (no service role) scenario still returns allowed, so deploys with the caller's own credentials are unaffected by fix 3.

### Hygiene greps on the diff

Command: `git diff origin/main -- access-model GOVERNANCE.md`, added lines only, case-insensitive.

| Pattern | Hits |
| --- | --- |
| email address regex | 0 |
| literal at sign | 0 |
| gmail | 0 |
| protonmail | 0 |
| AKIA/ASIA access key IDs | 0 |
| aws_secret / secret_access_key | 0 |
| rasheed / adam | 0 |
| U+2014 em dash | 0 |
| U+2013 en dash | 0 |
| password | 20, all prose, IAM action names (ChangePassword, GetAccountPasswordPolicy, Update*PasswordPolicy), or the `--password '<temp>'` placeholder. No password values |

Whole-file greps over access-model/* for at sign, em dash, en dash, rasheed, adam: 0 hits each. GOVERNANCE.md still names the team members in its roles tables; those lines are already on main and not part of this diff.

BudgetAlertEmail is still a parameter with no default.

## Validator output (verbatim, final state)

## Policy size (limit 6144)

| Policy | Chars | Result |
| --- | --- | --- |
| GrcPermissionsBoundary | 6002 | pass |
| GrcRequireMfaPolicy | 1551 | pass |
| GrcEngineerBuildPolicy | 6046 | pass |
| GrcEngineerSecurityPolicy | 3579 | pass |
| GrcEngineerGuardrailsPolicy | 5418 | pass |
| GrcEngineerLimitsPolicy | 1556 | pass |
| GrcAnalystPolicy | 4207 | pass |

## Boundary deny parity

| Sid | Result |
| --- | --- |
| DenyOwnIdentityChanges | identical |
| DenyAssumeNonGrcRoles | identical |
| DenyAccessModelTampering | identical |
| DenyRoleWithoutGrcBoundary | identical |
| DenyPrivilegedPolicyAttach | identical |
| DenyProtectedProduction | identical |
| DenyS3WritesOutsideGrc | identical |
| DenyS3DataReadsOutsideGrc | identical |
| DenyParametersOutsideGrc | identical |
| DenyAuditTampering | identical |
| DenyOrgAdminAndCostly | identical |
| DenyOutsideUsEast1 | identical |

## Hygiene

| File | Findings |
| --- | --- |
| GOVERNANCE.md | clean |
| access-model/README.md | clean |
| access-model/grc-access.yaml | clean |
| access-model/validate_policies.py | clean |

## Access Analyzer validate-policy

| Policy | Findings | Detail | Result |
| --- | --- | --- | --- |
| GrcPermissionsBoundary | 0 | none | pass |
| GrcRequireMfaPolicy | 0 | none | pass |
| GrcEngineerBuildPolicy | 0 | none | pass |
| GrcEngineerSecurityPolicy | 0 | none | pass |
| GrcEngineerGuardrailsPolicy | 0 | none | pass |
| GrcEngineerLimitsPolicy | 0 | none | pass |
| GrcAnalystPolicy | 0 | none | pass |

## Simulation matrix (101 of 101 pass)

| Principal | Action | Resource | Expected | Decision | Result |
| --- | --- | --- | --- | --- | --- |
| engineer | cloudformation:CreateStack | arn:aws:cloudformation:us-east-1:570814274897:stack/grc-11-guardrails/x | allowed | allowed | pass |
| engineer | lambda:CreateFunction | arn:aws:lambda:us-east-1:570814274897:function:grc-evidence-collector | allowed | allowed | pass |
| engineer | iam:CreateRole | arn:aws:iam::570814274897:role/grc-evidence-lambda | allowed | allowed | pass |
| engineer | iam:PassRole | arn:aws:iam::570814274897:role/grc-evidence-lambda | allowed | allowed | pass |
| engineer | s3:PutObject | arn:aws:s3:::grc-evidence-test/a.json | allowed | allowed | pass |
| engineer | s3:GetObject | arn:aws:s3:::340collective-cloudtrail-570814274897/AWSLogs/x | allowed | allowed | pass |
| engineer | dynamodb:PutItem | arn:aws:dynamodb:us-east-1:570814274897:table/grc-risk | allowed | allowed | pass |
| engineer | securityhub:EnableSecurityHub | * | allowed | allowed | pass |
| engineer | kms:CreateKey | * | allowed | allowed | pass |
| engineer | iam:CreateAccessKey | arn:aws:iam::570814274897:user/rasheed | allowed | allowed | pass |
| engineer | iam:ChangePassword | arn:aws:iam::570814274897:user/rasheed | allowed | allowed | pass |
| engineer | iam:UpdateAssumeRolePolicy | arn:aws:iam::570814274897:role/grc-evidence-lambda | allowed | allowed | pass |
| engineer | s3:CreateBucket | arn:aws:s3:::grc-evidence-test | allowed | allowed | pass |
| engineer | cloudformation:CreateStack | arn:aws:cloudformation:us-east-1:570814274897:stack/grc-11-guardrails/x | allowed | allowed | pass |
| engineer | iam:PassRole | arn:aws:iam::570814274897:role/grc-cfn-deploy | allowed | allowed | pass |
| engineer | iam:UpdateAssumeRolePolicy | arn:aws:iam::570814274897:role/collective340-blog-generator | explicitDeny | explicitDeny | pass |
| engineer | sts:AssumeRole | arn:aws:iam::570814274897:role/grc-evidence-lambda | explicitDeny | explicitDeny | pass |
| engineer | sts:AssumeRole | arn:aws:iam::570814274897:role/collective340-blog-generator | explicitDeny | explicitDeny | pass |
| engineer | s3:PutObject | arn:aws:s3:::grc-evidence-test/a.json | denied | implicitDeny | pass |
| engineer | s3:GetObject | arn:aws:s3:::grc-evidence-test/a.json | denied | implicitDeny | pass |
| engineer | iam:CreateRole | arn:aws:iam::570814274897:role/grc-x | explicitDeny | explicitDeny | pass |
| engineer | iam:CreateRole | arn:aws:iam::570814274897:role/grc-x | explicitDeny | explicitDeny | pass |
| engineer | iam:DeleteRolePermissionsBoundary | arn:aws:iam::570814274897:role/grc-x | explicitDeny | explicitDeny | pass |
| engineer | iam:PutRolePolicy | arn:aws:iam::570814274897:role/collective340-blog-generator | explicitDeny | explicitDeny | pass |
| engineer | iam:AttachRolePolicy | arn:aws:iam::570814274897:role/grc-x | explicitDeny | explicitDeny | pass |
| engineer | iam:AttachRolePolicy | arn:aws:iam::570814274897:role/grc-x | explicitDeny | explicitDeny | pass |
| engineer | iam:CreatePolicyVersion | arn:aws:iam::570814274897:policy/grc-permissions-boundary | explicitDeny | explicitDeny | pass |
| engineer | iam:CreatePolicyVersion | arn:aws:iam::570814274897:policy/grc-engineer-guardrails | explicitDeny | explicitDeny | pass |
| engineer | iam:CreatePolicyVersion | arn:aws:iam::570814274897:policy/collective340-blog-generator-budget-stop | explicitDeny | explicitDeny | pass |
| engineer | iam:UpdateAssumeRolePolicy | arn:aws:iam::570814274897:role/collective340-intake-IntakeRole-Uk5c9Xxf5zNE | explicitDeny | explicitDeny | pass |
| engineer | iam:PassRole | arn:aws:iam::570814274897:role/collective340-blog-generator | explicitDeny | explicitDeny | pass |
| engineer | iam:DeleteUserPermissionsBoundary | arn:aws:iam::570814274897:user/rasheed | explicitDeny | explicitDeny | pass |
| engineer | iam:AttachUserPolicy | arn:aws:iam::570814274897:user/rasheed | explicitDeny | explicitDeny | pass |
| engineer | iam:CreateAccessKey | arn:aws:iam::570814274897:user/kiro | explicitDeny | explicitDeny | pass |
| engineer | iam:CreateLoginProfile | arn:aws:iam::570814274897:user/adam | explicitDeny | explicitDeny | pass |
| engineer | iam:AddUserToGroup | arn:aws:iam::570814274897:group/Admin | explicitDeny | explicitDeny | pass |
| engineer | iam:CreateUser | arn:aws:iam::570814274897:user/grc-new | explicitDeny | explicitDeny | pass |
| engineer | cloudformation:UpdateStack | arn:aws:cloudformation:us-east-1:570814274897:stack/collective340-intake/x | explicitDeny | explicitDeny | pass |
| engineer | cloudformation:DeleteStack | arn:aws:cloudformation:us-east-1:570814274897:stack/grc-access-model/x | explicitDeny | explicitDeny | pass |
| engineer | cloudformation:CreateStack | arn:aws:cloudformation:us-east-1:570814274897:stack/grc-x/y | explicitDeny | explicitDeny | pass |
| engineer | lambda:UpdateFunctionCode | arn:aws:lambda:us-east-1:570814274897:function:collective340-intake | explicitDeny | explicitDeny | pass |
| engineer | dynamodb:Scan | arn:aws:dynamodb:us-east-1:570814274897:table/collective340-invoices | explicitDeny | explicitDeny | pass |
| engineer | s3:PutObject | arn:aws:s3:::340collective-site-570814274897/index.html | explicitDeny | explicitDeny | pass |
| engineer | s3:GetObject | arn:aws:s3:::340-insider/x | explicitDeny | explicitDeny | pass |
| engineer | s3:BypassGovernanceRetention | arn:aws:s3:::grc-evidence-test/a | explicitDeny | explicitDeny | pass |
| engineer | s3:PutAccountPublicAccessBlock | * | explicitDeny | explicitDeny | pass |
| engineer | ssm:GetParameter | arn:aws:ssm:us-east-1:570814274897:parameter/340collective/stripe/x | explicitDeny | explicitDeny | pass |
| engineer | ssm:GetParameter | arn:aws:ssm:us-east-1:570814274897:parameter/340/invoice/x | explicitDeny | explicitDeny | pass |
| engineer | budgets:ModifyBudget | arn:aws:budgets::570814274897:budget/340collective-monthly-5usd | explicitDeny | explicitDeny | pass |
| engineer | budgets:DeleteBudget | arn:aws:budgets::570814274897:budget/grc-projects-monthly | explicitDeny | explicitDeny | pass |
| engineer | cloudtrail:StopLogging | arn:aws:cloudtrail:us-east-1:570814274897:trail/340collective-trail | explicitDeny | explicitDeny | pass |
| engineer | apigateway:PATCH | arn:aws:apigateway:us-east-1::/apis/omhmmdi35f | explicitDeny | explicitDeny | pass |
| engineer | lambda:CreateFunction | arn:aws:lambda:us-west-2:570814274897:function:grc-x | explicitDeny | explicitDeny | pass |
| engineer | quicksight:CreateAccountSubscription | * | explicitDeny | explicitDeny | pass |
| engineer | ec2:RunInstances | * | explicitDeny | explicitDeny | pass |
| engineer | rds:CreateDBInstance | * | explicitDeny | explicitDeny | pass |
| engineer | organizations:LeaveOrganization | * | explicitDeny | explicitDeny | pass |
| engineer | securityhub:EnableOrganizationAdminAccount | * | explicitDeny | explicitDeny | pass |
| engineer | lambda:ListFunctions | * | explicitDeny | explicitDeny | pass |
| engineer | iam:PassRole | arn:aws:iam::570814274897:role/grc-x | denied | implicitDeny | pass |
| engineer | kms:ScheduleKeyDeletion | arn:aws:kms:us-east-1:570814274897:key/abc | denied | implicitDeny | pass |
| engineer | route53:ChangeResourceRecordSets | * | denied | implicitDeny | pass |
| analyst | securityhub:GetFindings | * | allowed | allowed | pass |
| analyst | inspector2:CreateFindingsReport | * | allowed | allowed | pass |
| analyst | auditmanager:GetEvidenceFoldersByAssessment | * | allowed | allowed | pass |
| analyst | config:SelectResourceConfig | * | allowed | allowed | pass |
| analyst | guardduty:ListFindings | * | allowed | allowed | pass |
| analyst | s3:PutObject | arn:aws:s3:::grc-evidence-test/r.csv | allowed | allowed | pass |
| analyst | iam:GetCredentialReport | * | allowed | allowed | pass |
| analyst | iam:CreateAccessKey | arn:aws:iam::570814274897:user/adam | allowed | allowed | pass |
| analyst | s3:GetObject | arn:aws:s3:::340collective-site-570814274897/index.html | explicitDeny | explicitDeny | pass |
| analyst | s3:GetObject | arn:aws:s3:::340-insider/x | explicitDeny | explicitDeny | pass |
| analyst | ssm:GetParameter | arn:aws:ssm:us-east-1:570814274897:parameter/340collective/stripe/x | explicitDeny | explicitDeny | pass |
| analyst | iam:CreateAccessKey | arn:aws:iam::570814274897:user/kiro | explicitDeny | explicitDeny | pass |
| analyst | lambda:CreateFunction | arn:aws:lambda:us-east-1:570814274897:function:grc-x | explicitDeny | explicitDeny | pass |
| analyst | cloudformation:CreateStack | arn:aws:cloudformation:us-east-1:570814274897:stack/grc-x/y | explicitDeny | explicitDeny | pass |
| analyst | s3:PutObject | arn:aws:s3:::grc-other/x | denied | implicitDeny | pass |
| analyst | s3:PutObject | arn:aws:s3:::grc-evidence-test/r.csv | denied | implicitDeny | pass |
| analyst | s3:DeleteObject | arn:aws:s3:::grc-evidence-test/r.csv | denied | implicitDeny | pass |
| analyst | securityhub:BatchUpdateFindings | * | denied | implicitDeny | pass |
| analyst | iam:CreateRole | arn:aws:iam::570814274897:role/grc-x | denied | implicitDeny | pass |
| analyst | securityhub:GetFindings | * | explicitDeny | explicitDeny | pass |
| workload | dynamodb:PutItem | arn:aws:dynamodb:us-east-1:570814274897:table/grc-x | allowed | allowed | pass |
| workload | s3:PutObject | arn:aws:s3:::grc-x/y | allowed | allowed | pass |
| workload | s3:GetObject | arn:aws:s3:::340collective-site-570814274897/index.html | explicitDeny | explicitDeny | pass |
| workload | dynamodb:Scan | arn:aws:dynamodb:us-east-1:570814274897:table/collective340-invoices | explicitDeny | explicitDeny | pass |
| workload | lambda:InvokeFunction | arn:aws:lambda:us-east-1:570814274897:function:collective340-intake | explicitDeny | explicitDeny | pass |
| workload | ssm:GetParameter | arn:aws:ssm:us-east-1:570814274897:parameter/340collective/stripe/x | explicitDeny | explicitDeny | pass |
| workload | sts:AssumeRole | arn:aws:iam::570814274897:role/collective340-blog-generator | explicitDeny | explicitDeny | pass |
| workload | iam:CreateRole | arn:aws:iam::570814274897:role/grc-y | explicitDeny | explicitDeny | pass |
| workload | iam:DeleteRolePermissionsBoundary | arn:aws:iam::570814274897:role/grc-x | denied | implicitDeny | pass |
| workload | iam:PassRole | arn:aws:iam::570814274897:role/grc-x | denied | implicitDeny | pass |
| workload | iam:AttachRolePolicy | arn:aws:iam::570814274897:role/grc-x | explicitDeny | explicitDeny | pass |
| workload | iam:CreateAccessKey | arn:aws:iam::570814274897:user/kiro | denied | implicitDeny | pass |
| workload | iam:CreatePolicyVersion | arn:aws:iam::570814274897:policy/grc-permissions-boundary | explicitDeny | explicitDeny | pass |
| workload | lambda:CreateFunction | arn:aws:lambda:us-west-2:570814274897:function:grc-x | explicitDeny | explicitDeny | pass |
| workload | iam:CreateUser | arn:aws:iam::570814274897:user/x | denied | implicitDeny | pass |
| workload | budgets:DeleteBudget | arn:aws:budgets::570814274897:budget/grc-projects-monthly | denied | implicitDeny | pass |
| workload | route53:ChangeResourceRecordSets | * | denied | implicitDeny | pass |
| workload | cloudfront:UpdateDistribution | * | denied | implicitDeny | pass |
| workload | ec2:RunInstances | * | denied | implicitDeny | pass |

RESULT: all checks passed

## Scratch

The validator writes its JSON to a temp dir it deletes on exit. The two stdout captures in /tmp used to build this file were deleted afterward. The cfn-lint venv at /tmp/grc_cfnlint was kept.
