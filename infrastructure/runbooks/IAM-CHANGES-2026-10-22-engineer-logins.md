# IAM change record 2026-10-22: engineer seat console logins through CloudFormation

## Why

Both engineer seats in `grc-engineer-users` (Automation Engineer, ISSM builder) exist, but neither has a console login. The 2026-10-17 record ([IAM-CHANGES-2026-10-17.md](IAM-CHANGES-2026-10-17.md), step 4) had the ISSM create the logins by hand with `aws iam create-login-profile`. That left a manual step outside CloudFormation. It also confused the engineer, who found that the guardrails deny him `iam:CreateLoginProfile`, which is correct. The helper scripts were never committed, so nobody could find them either.

## What changes

`infrastructure/cloudformation/grc-engineer-users.yaml`:

- Adds `GrcAutomationEngineerInitialPassword` and `GrcIssmBuilderInitialPassword` (`AWS::SecretsManager::Secret`). Each one holds a generated 24-character password with upper, lower, number and symbol, which meets the account policy. They are named `grc-engineer-users/<user>/initial-console-password` and tagged `grc-managed-by=grc-engineer-users`.
- Adds a `LoginProfile` to both users. It reads the matching secret through a dynamic reference and sets `PasswordResetRequired: true`.
- Adds outputs `AutomationEngineerPasswordSecret` and `IssmBuilderPasswordSecret` (the secret ARNs, not the values).

No change to groups, the boundary, tags, user names, or `grc-access-model`. No password, name, or key is stored in git.

New `infrastructure/scripts/grc-engineer-users/` holds the scripts that check, preview, apply, deliver and verify this change. See its README.

## Who can read the password

- ISSM (admin identity): yes, through `4-copy-temp-password.sh`, which copies the value to the clipboard and never prints it.
- Engineers: no. `grc-engineer-limits` denies `secretsmanager:GetSecretValue`.
- Analysts: no. `grc-analyst` denies `secretsmanager:GetSecretValue`.

The value only works once. `PasswordResetRequired` makes the user replace it at first sign-in, and MFA is required before any permission works.

## Deploy (ISSM, after this PR is merged, from clean `main` equal to `origin/main`)

1. `bash infrastructure/scripts/grc-engineer-users/1-check-template.sh`
2. `bash infrastructure/scripts/grc-engineer-users/2-preview-update.sh`. Expect exactly: Add `GrcAutomationEngineerInitialPassword`, Add `GrcIssmBuilderInitialPassword`, Modify `GrcAutomationEngineerUser` (no replacement), Modify `GrcIssmBuilderUser` (no replacement).
3. `bash infrastructure/scripts/grc-engineer-users/3-apply-update.sh`. Wait for `UPDATE_COMPLETE`.
4. Run `bash infrastructure/scripts/grc-engineer-users/4-copy-temp-password.sh <user>` once per seat, and deliver each password out of band.
5. After both people enroll MFA, run `bash infrastructure/scripts/grc-engineer-users/5-verify.sh`, then tag `live-YYYY-MM-DD` in GRC-Projects and push the tag.

This replaces step 4 of [IAM-CHANGES-2026-10-17.md](IAM-CHANGES-2026-10-17.md) for these two seats. Don't also run the manual `create-login-profile` lines. If a login profile already exists, the CloudFormation update fails and rolls back.

## Rollback

Revert this PR and redeploy through the same scripts. That removes both login profiles and both secrets, and leaves the users as they were.
