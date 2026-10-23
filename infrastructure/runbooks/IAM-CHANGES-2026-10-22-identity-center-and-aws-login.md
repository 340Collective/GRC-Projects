# IAM change record 2026-10-22: engineer role in IAM Identity Center, and terminal sign-in without access keys

## Why

- The two engineer seats (Automation Engineer, ISSM builder) have IAM users from `grc-engineer-users`, but no way to sign in. The 2026-10-17 record (step 4) left the console login as a manual ISSM step, and that step stalled.
- The CLI needed an access key plus an MFA session token (`aws sts get-session-token`), so calls made with a plain key were denied by `grc-require-mfa`. Owner decision: terminal access must work through a browser sign-in, with no access key.

## What changes

1. New shared stack `grc-identity-center` ([grc-identity-center.yaml](../cloudformation/grc-identity-center.yaml)):
   - Permission set `GRC-Engineer` (the role): `SecurityAudit`, `ViewOnlyAccess`, and the four `grc-engineer-*` policies, capped by `grc-permissions-boundary`. That is the same access as the `GRC-Engineer` IAM group. 8-hour sessions.
   - Identity Center group `GRC-Engineer`, assigned that permission set in this account.
   - Two Identity Center users in the group: the Automation Engineer and the ISSM builder seat. Names and emails are deploy-time parameters from the private roster (emails are NoEcho).
   - `grc-require-mfa` is not attached: Identity Center enforces MFA at sign-in, and that policy's MFA deny would block the role session.
2. `grc-access-model` ([grc-access-model.yaml](../cloudformation/grc-access-model.yaml)), for `aws login`:
   - `grc-permissions-boundary`: `signin:*` added to `AllowServices` (boundary is 6,142 of 6,144 characters).
   - `GRC-Engineer` and `GRC-Analyst` groups: AWS managed policy `SignInLocalDevelopmentAccess` attached (only `signin:AuthorizeOAuth2Access` and `signin:CreateOAuth2Token`).
   - `grc-require-mfa` is unchanged. `aws login` reuses the person's console sign-in, which already required MFA.

The IAM users from `grc-engineer-users` are not changed by this record. They have no login and no access key. Removing them is a separate PR once the Identity Center seats work.

## Pre-deploy facts (read-only, 2026-10-22)

- IAM Identity Center: one instance, status `ACTIVE`, created 2026-06-19 in this account (the organization's management account, all features). It had no permission sets, users, or groups.
- `grc-access-model`: `UPDATE_COMPLETE`; the deployed template matches `main`.
- `grc-engineer-users`: `CREATE_COMPLETE`; neither IAM user has a login profile or an access key.

## Owner console steps (once, before the first sign-in)

These settings cannot be set from CloudFormation.

1. IAM Identity Center, Settings, Authentication, Multi-factor authentication, Configure: prompt users for MFA every time they sign in; allow authenticator apps and security keys; if a user has no MFA device, require them to register one at sign-in.
2. IAM Identity Center, Settings, Authentication, Standard authentication, Configure: check **Send email OTP**, then Save. Without this, users created from CloudFormation cannot set a first password.

## Deploy (ISSM, after the PR is merged, from clean `main` equal to `origin/main`)

```bash
cd infrastructure
P=(--profile 340collective --region us-east-1)

# 1. aws login: update grc-access-model
aws cloudformation create-change-set --stack-name grc-access-model --change-set-name aws-login \
  --change-set-type UPDATE --template-body file://cloudformation/grc-access-model.yaml --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=EngineerUserName,UsePreviousValue=true ParameterKey=AnalystUserName,UsePreviousValue=true \
    ParameterKey=IamEngineerUserName,UsePreviousValue=true ParameterKey=CreateGrcBudget,UsePreviousValue=true \
    ParameterKey=BudgetAlertEmail,UsePreviousValue=true "${P[@]}"
aws cloudformation wait change-set-create-complete --stack-name grc-access-model --change-set-name aws-login "${P[@]}"
aws cloudformation describe-change-set --stack-name grc-access-model --change-set-name aws-login \
  --query 'Changes[].ResourceChange.[Action,LogicalResourceId,Replacement]' --output table "${P[@]}"
# Expect exactly: Modify GrcPermissionsBoundary, Modify GrcEngineerGroup, Modify GrcAnalystGroup, Replacement False.
aws cloudformation execute-change-set --stack-name grc-access-model --change-set-name aws-login "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-access-model "${P[@]}"

# 2. Engineer role: create grc-identity-center (names and emails from the private roster)
INSTANCE=$(aws sso-admin list-instances "${P[@]}" --query 'Instances[0].InstanceArn' --output text)
STORE=$(aws sso-admin list-instances "${P[@]}" --query 'Instances[0].IdentityStoreId' --output text)
aws cloudformation create-change-set --stack-name grc-identity-center --change-set-name create-identity-center \
  --change-set-type CREATE --template-body file://cloudformation/grc-identity-center.yaml \
  --parameters ParameterKey=InstanceArn,ParameterValue="$INSTANCE" ParameterKey=IdentityStoreId,ParameterValue="$STORE" \
    ParameterKey=AutomationEngineerUserName,ParameterValue=maria ParameterKey=AutomationEngineerGivenName,ParameterValue='<first>' \
    ParameterKey=AutomationEngineerFamilyName,ParameterValue='<last>' ParameterKey=AutomationEngineerEmail,ParameterValue='<roster email>' \
    ParameterKey=IssmBuilderUserName,ParameterValue=faris ParameterKey=IssmBuilderGivenName,ParameterValue='<first>' \
    ParameterKey=IssmBuilderFamilyName,ParameterValue='<last>' ParameterKey=IssmBuilderEmail,ParameterValue='<roster email>' "${P[@]}"
aws cloudformation wait change-set-create-complete --stack-name grc-identity-center --change-set-name create-identity-center "${P[@]}"
aws cloudformation describe-change-set --stack-name grc-identity-center --change-set-name create-identity-center \
  --query 'Changes[].ResourceChange.[Action,LogicalResourceId]' --output table "${P[@]}"
# Expect exactly 7 Add: GrcEngineerPermissionSet, GrcEngineerGroup, GrcEngineerAssignment,
# GrcAutomationEngineerUser, GrcAutomationEngineerMembership, GrcIssmBuilderUser, GrcIssmBuilderMembership.
aws cloudformation execute-change-set --stack-name grc-identity-center --change-set-name create-identity-center "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-identity-center "${P[@]}"
aws cloudformation describe-stacks --stack-name grc-identity-center --query 'Stacks[0].Outputs' --output table "${P[@]}"
```

Stop and delete the change set if it shows anything else.

## Tell each person (one email each, to the address in the private roster)

No password goes in the email. AWS sends the one-time code itself.

> Your AWS access is ready.
>
> Console: open the access portal URL (stack output `AccessPortalUrl`), enter your user name (`maria` or `faris`), and AWS emails you a one-time code. Set your password, then register an MFA device (an authenticator app). Pick account 340 Collective, role GRC-Engineer.
>
> Terminal (AWS CLI 2.32 or later), no access key needed:
>
> `aws configure sso` (session name `grc`, start URL = the portal URL, region `us-east-1`, then pick the account and the GRC-Engineer role, profile name `grc-engineer`)
>
> `aws sso login --profile grc-engineer`
>
> `aws sts get-caller-identity --profile grc-engineer`
>
> Work in us-east-1 only. Your access is the same as every GRC engineer's.

## Verify

1. `aws sso-admin list-account-assignments` for the permission set shows the `GRC-Engineer` group; `aws identitystore list-users` shows both users.
2. After a person's first sign-in: `aws sts get-caller-identity --profile grc-engineer` returns an `AWSReservedSSO_GRC-Engineer_*` role session, and `aws iam create-user --user-name grc-test-denied --profile grc-engineer` is denied.
3. `aws login` for an IAM user seat (engineer or analyst), after a console sign-in with MFA: `aws login --profile grc-iam`, then `aws sts get-caller-identity --profile grc-iam`, then a read such as `aws s3 ls --profile grc-iam`. If the read is denied by `grc-require-mfa`, the `aws login` credentials do not carry MFA: record it here and open a follow-up PR. Do not loosen the MFA rule by hand.
4. `detect-stack-drift` returns `IN_SYNC` on `grc-access-model` and `grc-identity-center`. Then tag `live-YYYY-MM-DD` on the deployed GRC-Projects `main` commit and push the tag.

## Rollback

- Identity Center seats: delete the `grc-identity-center` stack from clean `main`. That removes the two users, the group, the assignment, and the permission set.
- `aws login`: revert the `grc-access-model` change by PR and redeploy through a change set.
