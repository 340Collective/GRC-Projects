# grc-engineer-users scripts

Scripts for the `grc-engineer-users` stack ([template](../../cloudformation/grc-engineer-users.yaml)), which creates the engineer seats. Each seat gets an IAM user in `GRC-Engineer` with the `grc-permissions-boundary`, a console login, and no access keys.

Console logins come from CloudFormation, not hand-typed commands. For each seat the stack creates a Secrets Manager secret with a generated one-time password. The user's `LoginProfile` reads that secret with `PasswordResetRequired: true`, so the person sets their own password at first sign-in and then enrolls MFA. Engineers can't read the secret, because `grc-engineer-limits` denies `secretsmanager:GetSecretValue`.

## Who runs what

| Script | Who | Changes AWS? |
| --- | --- | --- |
| `0-mfa-login.sh <code>` | Anyone using the CLI | No. It only writes a local MFA profile. |
| `1-check-template.sh` | Anyone | No |
| `2-preview-update.sh` | ISSM | Creates a preview only. It deletes the preview if anything unexpected shows up. |
| `3-apply-update.sh` | ISSM | Yes. It applies the preview through CloudFormation. |
| `4-copy-temp-password.sh <user>` | ISSM | No. It copies the one-time password to the clipboard and never prints it. |
| `5-verify.sh` | ISSM or auditor | No |

Steps 2 and 3 run only from a clean `main` that matches `origin/main`, after the PR is merged. `lib.sh` holds the shared settings. Run the scripts from anywhere: each one moves itself to the repo root.

## Onboarding a seat

1. `bash infrastructure/scripts/grc-engineer-users/0-mfa-login.sh 123456`
2. `bash infrastructure/scripts/grc-engineer-users/1-check-template.sh`
3. `bash infrastructure/scripts/grc-engineer-users/2-preview-update.sh`. The preview must show exactly 2 Add (the password secrets) and 2 Modify (the users, no replacement).
4. `bash infrastructure/scripts/grc-engineer-users/3-apply-update.sh`
5. For each person, run `bash infrastructure/scripts/grc-engineer-users/4-copy-temp-password.sh <user>`. Send the sign-in URL, user name and password in a private message, then clear the clipboard.
6. The person signs in, sets a new password, enrolls a virtual MFA device, then signs out and back in with MFA.
7. `bash infrastructure/scripts/grc-engineer-users/5-verify.sh`. When everything passes, tag `live-YYYY-MM-DD` and push the tag.

To add or remove a seat, open a PR that edits the template. The scripts don't create or delete users on their own.

## Cost

Each secret costs 0.40 USD a month, so two seats come to 0.80 USD a month, inside the 10 USD budget.
