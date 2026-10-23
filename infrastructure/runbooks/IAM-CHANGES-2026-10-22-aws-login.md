# IAM change record 2026-10-22: console logins for the two engineer seats, and terminal sign-in without access keys

## Why

- The two engineer seats in `grc-engineer-users` (Automation Engineer `maria`, ISSM builder `faris`) existed with no way to sign in.
- The CLI needed an access key plus an MFA session token (`aws sts get-session-token`). Calls made with a plain key were denied by `grc-require-mfa`. Owner decision: terminal access works through a browser sign-in, with no access key.

## History

PR #165 added an IAM Identity Center stack (`grc-identity-center`) for the two seats. The owner withdrew it the same day, before anything was deployed: the seats use IAM users and console logins, the same process as every other GRC user. The template was removed and nothing reached AWS. The `aws login` change from #165 stays.

## 1. Console logins (done 2026-10-22)

The ISSM step from [IAM-CHANGES-2026-10-17.md](IAM-CHANGES-2026-10-17.md) step 4, the same process as the other GRC users:

- `aws iam create-login-profile --password-reset-required` for `maria` and `faris`, each with a generated 20-character temporary password that meets the account policy.
- Each person got one email from the 340 Collective support mailbox through SES with the sign-in link, the user name, the temporary password, and the first sign-in steps: new password, MFA device, sign out and back in, and CloudShell for the command line. The password was never printed, logged, or stored in git.
- Verified: `get-login-profile` shows both profiles with `PasswordResetRequired` true. MFA shows up after each person signs in and enrolls a device.

## 2. `aws login` (merged in #165, deploy pending)

`grc-access-model` ([grc-access-model.yaml](../cloudformation/grc-access-model.yaml)):

- `grc-permissions-boundary`: `signin:*` added to `AllowServices` (the boundary is 6,142 of 6,144 characters).
- `GRC-Engineer` and `GRC-Analyst` groups: the AWS managed policy `SignInLocalDevelopmentAccess` is attached (only `signin:AuthorizeOAuth2Access` and `signin:CreateOAuth2Token`).
- `grc-require-mfa` is unchanged. `aws login` reuses the person's console sign-in, which already required MFA.

Deploy (ISSM, from clean `main` equal to `origin/main`):

```bash
cd infrastructure
P=(--profile 340collective --region us-east-1)
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
```

Stop and delete the change set if it shows anything else.

## Verify

1. After the deploy, one IAM user seat signs in to the console with MFA, then runs `aws login --profile grc`, `aws sts get-caller-identity --profile grc`, and a read such as `aws s3 ls --profile grc`. If the read is denied by `grc-require-mfa`, the `aws login` credentials do not carry MFA: record it here and open a follow-up PR. Do not loosen the MFA rule by hand.
2. `detect-stack-drift` returns `IN_SYNC` on `grc-access-model`. Then tag `live-YYYY-MM-DD` on the deployed GRC-Projects `main` commit and push the tag.

## Rollback

- Console logins: `aws iam delete-login-profile --user-name <user>` (step 4 of IAM-CHANGES-2026-10-17.md names the users).
- `aws login`: revert the `grc-access-model` change by PR and redeploy through a change set.
