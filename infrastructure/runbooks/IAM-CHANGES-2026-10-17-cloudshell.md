# IAM changes, 2026-10-17: engineer CloudShell

Scope: let every GRC engineer use AWS CloudShell (standard environments only) through the `GRC-Engineer` group. Stack `grc-access-model`, account 570814274897, us-east-1.

Status: repo only, not deployed. Branch `fix/engineer-cloudshell`. Nothing in AWS changed. Only read-only AWS calls were made.

## What changes

- `infrastructure/cloudformation/grc-access-model.yaml`, two policy documents only (an in-place update, a new default policy version each):
  - `grc-engineer-security` (`GrcEngineerSecurityPolicy`): new statement `CloudShellNoVpc` that allows exactly `cloudshell:CreateEnvironment`, `CreateSession`, `GetEnvironmentStatus`, `StartEnvironment`, `StopEnvironment`, `DeleteEnvironment`, `DescribeEnvironments`, `PutCredentials`, `GetFileUploadUrls`, and `GetFileDownloadUrls` on `*`. `cloudshell:ApproveCommand` is not granted.
  - `grc-permissions-boundary` (`GrcPermissionsBoundary`): `cloudshell:*` added to the service allow list, written the same way as every other service there. The boundary grants nothing alone; the effective rights are the ten actions above. To stay under 6,144 characters, three allow Sids were shortened: `AllowInScopeServices` to `AllowServices`, `AllowSecurityServiceLinkedRoles` to `AllowServiceLinkedRoles`, and `AllowVisibilityReads` to `AllowReads`. A Sid has no effect on evaluation.
- Every engineer gets this through the group: `rasheed` and `abdifatah` now, and the `maria` and `faris` seats from `grc-engineer-users` when that stack is created. No per-user change.
- Not changed: `grc-require-mfa` (MFA is still required for every action, CloudShell included), every Deny statement, every `Description` (a `Description` change would replace a managed policy), `grc-engineer-build`, `grc-engineer-guardrails`, `grc-engineer-limits`, `grc-analyst`, `grc-engineer-users.yaml`, and `grc-internal-auditor.yaml`. No `ec2:` permission is added, so VPC environments stay blocked.
- `infrastructure/cloudformation/grc-access-model/validate_policies.py`: 15 new scenarios (the ten actions allowed; denied without MFA, outside us-east-1, for `ApproveCommand`, for `ec2:CreateNetworkInterface`, and for the analyst).
- Docs: both access-model READMEs and `infrastructure/README.md`.

## Pre-deploy facts (read-only, 2026-10-17)

- `aws sts get-caller-identity`: account 570814274897.
- Stack `grc-access-model`: UPDATE_COMPLETE (last updated 2026-10-15). `detect-stack-drift`: IN_SYNC, 0 drifted resources (2026-10-17T22:14Z). `get-template` `Resources` equal to this repo's `main`.
- `rasheed`: in `GRC-Engineer` only, boundary `grc-permissions-boundary`, no MFA device. `abdifatah`: same group and boundary, one MFA device. `maria` and `faris`: NoSuchEntity (`grc-engineer-users` not deployed).
- No live engineer policy or boundary version mentions `cloudshell`.
- `simulate-principal-policy` before the change: `rasheed` without MFA gets `explicitDeny` on all ten actions from `grc-require-mfa`; with MFA in us-east-1 both `rasheed` and `abdifatah` get `implicitDeny`, and the boundary does not allow them. So CloudShell was missing for every engineer, and Rasheed is also blocked by the MFA rule until he enrolls.

## Threat model

| Threat | Control | Residual |
| --- | --- | --- |
| CloudShell used to get around the guardrails | CloudShell runs with the user's own console credentials, so the boundary and every explicit Deny apply to each command | None new |
| MFA bypass through CloudShell | `grc-require-mfa` unchanged; scenario `cloudshell:CreateEnvironment` without MFA is `explicitDeny` | None new |
| VPC environment created to reach private networks | No `ec2:CreateNetworkInterface` or related rights; scenario `ec2:CreateNetworkInterface` is denied | None |
| Files moved in or out, or outbound internet from CloudShell | Upload and download are granted for normal use; an engineer can already read only `grc-*` data and their console view | Accepted |
| A bounded `grc-*` workload role calls CloudShell APIs | The boundary now allows `cloudshell:*` for roles with broad allows | Accepted: CloudShell is a console feature, a role cannot open a shell session for anyone |

## Deploy steps (ISSM, owner-gated, not run)

1. This branch goes by PR into GRC-Projects `main`, and the ISSM merges it. In the primary checkout, confirm clean `main` equal to `origin/main`:

   ```bash
   git switch main && git pull && git fetch origin && git status
   git rev-parse HEAD
   git rev-parse origin/main
   ```

2. Checks from `infrastructure/`:

   ```bash
   cd infrastructure
   /tmp/grc_cfnlint/bin/cfn-lint cloudformation/*.yaml
   aws cloudformation validate-template --template-body file://cloudformation/grc-access-model.yaml --profile 340collective --region us-east-1
   AWS_PROFILE=340collective AWS_REGION=us-east-1 /tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py --account-id 570814274897 --region us-east-1 --engineer rasheed --analyst adam
   wc -c < cloudformation/grc-access-model.yaml
   ```

   Expect cfn-lint clean, validate-template success, `RESULT: all checks passed` with every scenario `pass`, and under 51,200 bytes.
3. Change set, from `infrastructure/`:

   ```bash
   aws cloudformation create-change-set --stack-name grc-access-model --change-set-name engineer-cloudshell --change-set-type UPDATE --template-body file://cloudformation/grc-access-model.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=EngineerUserName,UsePreviousValue=true ParameterKey=AnalystUserName,UsePreviousValue=true ParameterKey=IamEngineerUserName,UsePreviousValue=true ParameterKey=CreateGrcBudget,UsePreviousValue=true ParameterKey=BudgetAlertEmail,UsePreviousValue=true --profile 340collective --region us-east-1
   aws cloudformation wait change-set-create-complete --stack-name grc-access-model --change-set-name engineer-cloudshell --profile 340collective --region us-east-1
   aws cloudformation describe-change-set --stack-name grc-access-model --change-set-name engineer-cloudshell --profile 340collective --region us-east-1
   ```

   Expect exactly 2 `Modify` (`GrcPermissionsBoundary`, `GrcEngineerSecurityPolicy`), both `Replacement: False`, 0 Add, 0 Remove. Anything else: `delete-change-set` and stop. Execute only with the owner's OK:

   ```bash
   aws cloudformation execute-change-set --stack-name grc-access-model --change-set-name engineer-cloudshell --profile 340collective --region us-east-1
   aws cloudformation wait stack-update-complete --stack-name grc-access-model --profile 340collective --region us-east-1
   ```

## Verify (read-only, after deploy)

- `aws iam simulate-principal-policy` for `rasheed` and `abdifatah` on the ten actions with context `aws:MultiFactorAuthPresent=true` and `aws:RequestedRegion=us-east-1`: `allowed`. Without context: `explicitDeny`.
- `ec2:CreateNetworkInterface` for an engineer: denied. `cloudshell:CreateEnvironment` for `adam`: denied.
- `detect-stack-drift` on `grc-access-model`, then `describe-stack-drift-detection-status`: IN_SYNC.
- `abdifatah` signs in with MFA, sets the region to US East (N. Virginia), opens CloudShell, and runs `aws sts get-caller-identity`. This confirms live that CloudShell carries the console MFA context.
- `rasheed` can do the same only after he enrolls MFA.
- Tag the deployed GRC-Projects `main` commit `live-YYYY-MM-DD` and push the tag. Seats created later by `grc-engineer-users` (`maria`, `faris`) get CloudShell through the group with no extra step.

## Rollback

Before execute: `delete-change-set --stack-name grc-access-model --change-set-name engineer-cloudshell`. After execute: a revert PR into `main`, then the same change set flow from clean `main`.

## Change-control status (340-change-control rule)

Nothing in this record has reached AWS. Every step above runs only after this branch is merged into GRC-Projects `main` and pushed, from a clean `main` equal to `origin/main`. The local guard allows `grc-*` stacks only from GRC-Projects clean `main`. No resource is changed by hand. The tag `live-YYYY-MM-DD` goes in GRC-Projects.
