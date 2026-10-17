# IAM changes, 2026-10-17

Scope: three GRC-Engineer seats as code (new stack `grc-engineer-users`) and a no-lock, temporary compliance evidence bucket (`infrastructure/cloudformation/compliance-evidence.yaml`). Account 570814274897, us-east-1.

Status: repo only, not deployed. Written on the website branch `feature/grc-engineer-seats-no-lock`, then moved into this repo's `infrastructure/` folder on 2026-10-17 (branch `feature/grc-infrastructure-move`). Nothing in AWS changed. Only read-only AWS calls were made.

Before 2026-10-17 this record lived in the private website repo at `Technology/IAM-CHANGES-2026-10-17.md`, where the website flow applied (`dev`, then `test` with `build_release.py`, `qa.py`, `unittest`, and `build_preview.py` plus `smoke_preview.py`, then `main`); the website PR that removes the moved files still goes through that flow.

## What changes

- New template `infrastructure/cloudformation/grc-engineer-users.yaml`, new stack **`grc-engineer-users`**. Three optional parameters, each empty by default, which skips that seat: `AutomationEngineerUserName`, `SecurityAutomationEngineerUserName`, and `IssmBuilderUserName`. Three conditional users, each the same as the ISSE user `rasheed` in `grc-access-model`:
  - `GrcAutomationEngineerUser` (Automation Engineer, planned value `maria`), `grc-function=Automation-Engineer`;
  - `GrcSecurityAutomationEngineerUser` (Security Automation Engineer, planned value `alex`), `grc-function=Security-Automation-Engineer`;
  - `GrcIssmBuilderUser` (the ISSM builder seat, planned value `faris`), `grc-function=ISSM-Builder`. The ISSM keeps a separate admin identity for approvals.
  - Each user: group `GRC-Engineer`, permissions boundary `arn:aws:iam::<account>:policy/grc-permissions-boundary`, tags `grc-role=engineer`, `grc-function`, and `grc-managed-by=grc-engineer-users`. No LoginProfile and no access keys. MFA is enforced by `grc-require-mfa`, which `grc-access-model` attaches to the group, so nothing is needed per user.
  - The group and the boundary are referenced by literal name, with no export. Deploy after `grc-access-model`, delete before it.
  - Why a separate stack: `grc-access-model.yaml` is 49,133 of the 51,200 byte inline template limit, the same reason `grc-internal-auditor` is separate.
- `infrastructure/cloudformation/grc-access-model.yaml` (stack `grc-access-model`) and `infrastructure/cloudformation/grc-internal-auditor.yaml` are unchanged and byte-identical to the website repo's `origin/dev` at the time of writing.
- `infrastructure/cloudformation/grc-access-model/validate_policies.py`: the hygiene scan now also covers `cloudformation/grc-engineer-users.yaml`. The new template holds no managed policies, so nothing else changes.
- `infrastructure/cloudformation/compliance-evidence.yaml` (not deployed, no stack): the Object Lock option is removed (`EnableObjectLock`, `ObjectLockRetentionDays`, condition `ObjectLockOn`, `ObjectLockEnabled`, `ObjectLockConfiguration`, output `ObjectLock`). The bucket is now temporary project data: `DeletionPolicy` and `UpdateReplacePolicy` are `Delete`; new parameter `EvidenceExpirationDays` (default 30) expires current objects; `NoncurrentVersionExpirationDays` default goes from 365 to 7; incomplete multipart uploads abort after 1 day. It stays private, versioned, SSE-S3, and TLS-only. Integrity comes from a SHA-256 hash per object plus a manifest, not from a lock. `infrastructure/scripts/compliance-evidence-init.py` notes that the bucket is temporary.
- Docs: `Technology/ARCHITECTURE.md` (private website repo), `infrastructure/cloudformation/grc-access-model/README.md`, and `Operations/TEAM-ROSTER.md` (private website repo).

## Pre-deploy facts (read-only, 2026-10-17)

- `aws sts get-caller-identity`: account 570814274897.
- `aws iam get-user` for `maria`, `alex`, and `faris`: NoSuchEntity for all three.
- `aws cloudformation describe-stacks --stack-name grc-engineer-users`: the stack does not exist.
- `aws iam get-group --group-name GRC-Engineer`: members `rasheed` and `abdifatah`.
- Stack `grc-access-model`: UPDATE_COMPLETE, last drift check IN_SYNC (2026-10-15). Stack `grc-internal-auditor`: CREATE_COMPLETE.
- Compliance evidence: no stack, and bucket `340collective-compliance-evidence` returns 404 (not deployed).

## Deploy steps (owner-gated, not run)

Preconditions: the `github-before-aws-guard` hook blocks the deploy steps unless the GRC-Projects primary checkout is on clean `main` equal to `origin/main`. `create-change-set` is not gated by the guard, so confirm clean `main` by hand (the handoff preview script checks it too).

1. Repo flow: this GRC-Projects branch goes by PR into `main` (CONTRIBUTING.md), and the ISSM merges it. Then, in the GRC-Projects primary checkout:

   ```bash
   git switch main && git pull && git fetch origin && git status
   git rev-parse HEAD
   git rev-parse origin/main
   ```

   Expect `main` equal to `origin/main` (the two hashes match) and a clean tracked tree.
2. Offline validation from clean `main`, run from `infrastructure/` so `validate_policies.py` resolves its paths:

   ```bash
   cd infrastructure
   /tmp/grc_cfnlint/bin/cfn-lint cloudformation/grc-access-model.yaml cloudformation/grc-internal-auditor.yaml cloudformation/grc-engineer-users.yaml cloudformation/compliance-evidence.yaml
   aws cloudformation validate-template --template-body file://cloudformation/grc-engineer-users.yaml --profile 340collective --region us-east-1
   /tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py --account-id 570814274897 --region us-east-1 --engineer rasheed --analyst adam --skip-aws
   cd ..
   ```

   Expect cfn-lint clean, validate-template success (CAPABILITY_NAMED_IAM), and `RESULT: all checks passed` with `cloudformation/grc-engineer-users.yaml` clean in the hygiene table.
3. `CREATE` change set for the new stack `grc-engineer-users` (`grc-access-model` is not touched), run from the repo root. The task text said `--change-type CREATE`; that is not a valid AWS CLI flag. The real flag is `--change-set-type`, used below.

   ```bash
   aws cloudformation create-change-set --change-set-type CREATE --stack-name grc-engineer-users --change-set-name create-engineer-users --template-body file://infrastructure/cloudformation/grc-engineer-users.yaml --capabilities CAPABILITY_NAMED_IAM --parameters ParameterKey=AutomationEngineerUserName,ParameterValue=maria ParameterKey=SecurityAutomationEngineerUserName,ParameterValue=alex ParameterKey=IssmBuilderUserName,ParameterValue=faris --profile 340collective --region us-east-1
   aws cloudformation wait change-set-create-complete --stack-name grc-engineer-users --change-set-name create-engineer-users --profile 340collective --region us-east-1
   aws cloudformation describe-change-set --stack-name grc-engineer-users --change-set-name create-engineer-users --profile 340collective --region us-east-1
   ```

   Expect exactly 3 `Add` (`GrcAutomationEngineerUser`, `GrcSecurityAutomationEngineerUser`, `GrcIssmBuilderUser`), 0 Modify, 0 Remove. Anything else: `delete-change-set`, delete the `REVIEW_IN_PROGRESS` placeholder stack, and stop. Execute only with the owner's OK:

   ```bash
   aws cloudformation execute-change-set --stack-name grc-engineer-users --change-set-name create-engineer-users --profile 340collective --region us-east-1
   aws cloudformation wait stack-create-complete --stack-name grc-engineer-users --profile 340collective --region us-east-1
   ```

4. Onboarding (ISSM, from clean `main`). Set a temporary console password for each user:

   ```bash
   aws iam create-login-profile --user-name maria --password '<temp>' --password-reset-required --profile 340collective
   aws iam create-login-profile --user-name alex --password '<temp>' --password-reset-required --profile 340collective
   aws iam create-login-profile --user-name faris --password '<temp>' --password-reset-required --profile 340collective
   ```

   Deliver each password out of band (never in a repo, GitHub, Jira, logs, or chat). Each user signs in, sets a new password, enrolls a virtual MFA device, signs out, and signs back in with MFA. Only then do the group permissions work.
5. Verify (read-only): for each of `maria`, `alex`, and `faris`, `list-groups-for-user` shows only `GRC-Engineer`; `get-user` shows the boundary ARN ending `:policy/grc-permissions-boundary`; `list-user-tags` shows exactly `grc-function=<value>`, `grc-managed-by=grc-engineer-users`, and `grc-role=engineer`; `list-access-keys` is empty; `get-login-profile` exists; `list-mfa-devices` shows one device after enrollment. Stack `grc-engineer-users` is CREATE_COMPLETE and its outputs match. `detect-stack-drift` returns IN_SYNC on both `grc-engineer-users` and `grc-access-model`. Then tag `live-YYYY-MM-DD` on the deployed GRC-Projects `main` commit and push the tag.
6. Rollback: before execute, `delete-change-set`, then `delete-stack --stack-name grc-engineer-users` to remove the `REVIEW_IN_PROGRESS` placeholder. After execute, for fast containment the ISSM deletes the affected user's login profile. For full rollback, commit the decision first, delete each user's login profile, access keys, and MFA device, then delete stack `grc-engineer-users` from clean `main`. A failed create rolls back on its own (`ROLLBACK_COMPLETE`, then delete the empty stack). `grc-access-model` is untouched throughout.

The compliance evidence bucket is not deployed by this change. If it is deployed later, teardown empties the bucket including all versions, then deletes the stack.

## Known gap

The stack name `grc-engineer-users` matches the engineer's `stack/grc-*` CloudFormation rights and is not in `DenyProtectedProduction` (adding it would change `grc-access-model`), the same as `grc-internal-auditor`. An engineer still cannot change these seats through the stack: CloudFormation runs with the caller's credentials or a bounded `grc-*` role, and both are denied every IAM user write (`DenyIdentityAdmin`, `DenyIamWritesOutsideGrc`, the boundary's narrow IAM allow). An engineer update or delete fails on those resources. The ISSM reviews any CloudTrail `UpdateStack` or `DeleteStack` call on this stack that the ISSM did not make.

## Change-control status (340-change-control rule)

Nothing in this record has reached AWS. Every step above runs only after this branch is merged into GRC-Projects `main` and pushed, from a clean `main` equal to `origin/main`. The local guard allows the `grc-*` and `compliance-evidence` stacks only from GRC-Projects clean `main`. The three `create-login-profile` lines above are the committed runbook entry the guard's IAM exception needs once this file is on `origin/main`. Seat changes after deploy go through a PR that edits `infrastructure/cloudformation/grc-engineer-users.yaml`, then a change set from clean `main`. The tag `live-YYYY-MM-DD` goes in GRC-Projects.
