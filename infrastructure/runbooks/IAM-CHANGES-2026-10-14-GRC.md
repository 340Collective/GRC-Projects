# IAM changes, 2026-10-14 (GRC sections)

This file is a verbatim copy, made 2026-10-17, of the GRC sections (2, 3, 5, 6, 7, 9, and the GRC parts of "Process gap and follow-ups") of the 2026-10-14 change record. The full record stays in the private website repo at `Technology/IAM-CHANGES-2026-10-14.md`. Business sections 1 (David reduced to read-only), 4 (account password policy), and 8 (hand-made IAM captured in `iam-baseline`), and the business items under "Process gap and follow-ups", are not copied. Account 570814274897, us-east-1.

Changes from the original, nothing else: links and paths point at `infrastructure/` in this repo, and commands that name `cloudformation/...` run from `infrastructure/`; the sender address in section 3 is written as "the business help address"; references to files that stay in the website repo say "(private website repo)". In the copied text, "this repo" means the website repo, where the record was written; since 2026-10-17 the GRC templates and runbooks live in this repo's `infrastructure/` folder (see [infrastructure/README.md](../README.md)).

## 2. Stack `grc-access-model`

- Template: [infrastructure/cloudformation/grc-access-model.yaml](../cloudformation/grc-access-model.yaml). Docs, roles, deviations, and teardown: [infrastructure/cloudformation/grc-access-model/README.md](../cloudformation/grc-access-model/README.md).
- Parameters: `EngineerUserName=rasheed`, `AnalystUserName=adam`, `CreateGrcBudget=false` (the existing `340collective-monthly-5usd` budget already covers the account).
- Created 11 resources:
  - permissions boundary `grc-permissions-boundary`
  - `grc-require-mfa`
  - 4 engineer policies
  - `grc-analyst`
  - groups `GRC-Engineer` and `GRC-Analyst`
  - users `rasheed` and `adam` (boundary set, no access keys)
- The first attempt rolled back with nothing left behind, because IAM rejects a wildcard service in a resource ARN (`arn:aws:*:...`). `DenyProtectedProduction` now lists each service that holds 340 production resources (CloudFormation, Lambda, Logs, SQS, Scheduler, DynamoDB, SNS, CloudWatch).
- Checked before deploy:
  - cfn-lint clean
  - `validate-template` OK
  - IAM Access Analyzer: 0 findings on all 7 policies
  - all 101 `simulate-custom-policy` scenarios passed
- Checked after deploy:
  - both users have the boundary, the correct group, and no keys
  - `david`, `Jason-Contractor-Auditor`, and `kiro` are unchanged
- Production protection: the engineer cannot touch `collective340-*` or `340collective*` resources, the site and `340-insider` buckets, or `/340collective/*` parameters, and cannot change IAM users, groups, or the boundary.

## 3. Console logins for the GRC team

- `rasheed` (ISSE) and `adam` (ISSO): login profiles with a random 20-character temporary password and `PasswordResetRequired=true`.
- Each person got one SES email from the business help address, to their own address in `Operations/TEAM-ROSTER.md` (private website repo). The sender address was checked against the roster before sending.
- Passwords were never printed or stored. They existed only in 0600 temp files that were deleted after each CLI call, and the onboarding script was removed.
- `grc-require-mfa` blocks everything except password change and MFA setup until the user signs in with MFA.

## 5. Auditor credential reset

- `Jason-Contractor-Auditor` (group `ExtAuditor`, ReadOnlyAccess). Last sign-in was 2026-06-17. No MFA device and no access keys.
- New random temporary password with a forced change, emailed only to his roster address. His access is unchanged.

## 6. Deviation DEV-001

The Auditor is exempt from enforced MFA by ISSM decision, with compensating controls. The full record, in the GOVERNANCE.md deviation format, is under "Deviations" in [infrastructure/cloudformation/grc-access-model/README.md](../cloudformation/grc-access-model/README.md). Revisit at the next access review or by 2027-01-14.

## Process gap and follow-ups (GRC parts)

- **Gap:** every change above was made from a laptop with `kiro`'s long-lived admin access key (created 2026-06-15). The stack was deployed from the GRC repo's unmerged PR branch, and this repo was not updated first. From now on, backend changes are stored in this repo first and follow its branch flow, even when the public website does not change. The GRC-Projects repo is for contractor-facing designs and reference copies only.
- **Follow-ups:**
  - Bring the hand-made `Leadership` and `ExtAuditor` groups into CloudFormation, and consider moving them from `ReadOnlyAccess` to `SecurityAudit` plus `ViewOnlyAccess`, so they cannot read object data. For the auditor, superseded by section 9: Jason moves to `GRC-Auditor` in `grc-access-model` (SecurityAudit plus ViewOnlyAccess, MFA required), and `ExtAuditor` is left empty. `Leadership` is unchanged.
- **Rollback, in reverse order (GRC steps):**
  1. Delete the login profiles for `rasheed` and `adam`.
  2. `aws cloudformation delete-stack --stack-name grc-access-model`.

Note added 2026-10-17: the gap above was written when the website repo held all infrastructure. Since 2026-10-17 the GRC stacks live in this repo's `infrastructure/` folder and deploy only from this repo's clean `main`.

## 7. IAM / Identity Engineer onboarded (later the same day)

- Template change: a new optional parameter `IamEngineerUserName` (default empty) and a conditional user `GrcIamEngineerUser` in `GRC-Engineer`, with the same `grc-permissions-boundary` and MFA rule. The stack output `IamEngineerUserName` was added.
- Committed to this repo first, then deployed. Change set `add-iam-engineer` had exactly 1 Add (`GrcIamEngineerUser`), no modifications, no replacements.
- Parameter: `IamEngineerUserName=abdifatah`. Every other parameter kept its previous value.
- Checks: cfn-lint was clean and the policy validator passed all checks.
- The console login uses a random temporary password with a forced change, emailed only to the address on the roster line. GitHub and Jira invites are pending (see the roster).

## 9. Internal Auditor access (repo only, not deployed)

Repo-only change on branch `feature/grc-internal-auditor`. Nothing in AWS changed. Jason moves from external contractor auditor to Internal Auditor, and his AWS access moves into the access model as code.

### What changes

- New template `infrastructure/cloudformation/grc-internal-auditor.yaml`, new stack **`grc-internal-auditor`**, 4 resources. `infrastructure/cloudformation/grc-access-model.yaml` (stack `grc-access-model`) is unchanged and byte-identical to the deployed template. The first plan added these resources to `grc-access-model`, but that template then reached 59,401 bytes, and CloudFormation rejected the change set because an inline template can be at most 51,200 bytes (2026-10-15, nothing changed in AWS). The owner chose a separate stack over an S3-hosted template, because a hand-made template bucket would itself be an untracked resource.
  - group `GRC-Auditor`: `SecurityAudit`, `job-function/ViewOnlyAccess`, `internal-auditor-read`, `internal-auditor-guardrails`, and `grc-require-mfa` (owned by `grc-access-model`, attached by literal ARN, no export). No permissions boundary.
  - policy `internal-auditor-read`: Security Hub, Config, GuardDuty, Inspector, Audit Manager, and Access Analyzer reads; the credential report, last-accessed data, and policy simulation; CloudTrail events and log objects; `grc-*` evidence buckets, tables, Lambda logs, and Glue catalog; decrypt through S3 only with `grc-project` keys. Every allow requires `aws:MultiFactorAuthPresent`.
  - policy `internal-auditor-guardrails`: explicit denies on every SSM parameter value and Secrets Manager secret value, on `kms:Decrypt` through SSM, on KMS use outside S3 or on keys not tagged `grc-project`, on object data outside `grc-*` and the CloudTrail log bucket, on IAM identity admin, PassRole, and role assumption, and on writes to CloudTrail, Config, Security Hub, GuardDuty, Inspector, Audit Manager, Access Analyzer, S3, CloudFormation, Lambda, DynamoDB, SSM, and KMS.
  - user from the optional parameter `InternalAuditorUserName` (default empty), in `GRC-Auditor`, tagged `grc-role=auditor`, `grc-function=Internal-Auditor`, and `grc-managed-by=grc-internal-auditor`.
- `infrastructure/cloudformation/grc-access-model/validate_policies.py`: new `--auditor` option and 22 Internal Auditor simulation scenarios, run without a boundary. The auditor policies are read from `--auditor-template` (default `cloudformation/grc-internal-auditor.yaml`, relative to `infrastructure/`), and the hygiene scan covers both templates.
- Known gap: the stack name matches the engineer's `stack/grc-*` CloudFormation rights and is not in `DenyProtectedProduction`, which would need a `grc-access-model` change. The engineer still cannot change the auditor's access through it, because every IAM write to these users, groups, and non-`grc-` policies is denied to the engineer and to bounded `grc-*` roles. See the access-model README, "Internal Auditor design".
- `cloudformation/iam-baseline.yaml` and `cloudformation/iam-baseline/import-resources.json` (private website repo): `JasonContractorAuditorUser` removed. The IMPORT is now 5 resources. `ExtAuditorGroup` stays, unchanged.
- Docs: `infrastructure/cloudformation/grc-access-model/README.md`, and in the private website repo `cloudformation/iam-baseline/README.md`, `Technology/ARCHITECTURE.md`, and `Operations/TEAM-ROSTER.md`.
- Jira: nothing in AWS. Jira is outside AWS. His GRC project role is set by the owner in the Jira admin UI.

### Owner decisions (2026-10-14)

- D1, user name: a new stack-owned user (`InternalAuditorUserName=jason`, from the private roster) instead of keeping `Jason-Contractor-Auditor`. IAM user names cannot be changed in place, and the old name says "Contractor". The old user is not imported and is retired by the runbook below after the new user works.
- D2, validator: the ISSM (Faris) validates and approves Jason's own projects (02, 03, 04, 09), as for Adam's 07, 08, 12. Jason never validates his own work. Superseded by the GOVERNANCE.md review flow: Adam (ISSO) validates engineer work on every project, including Jason's.
- D3, independence: Jason is internal. His work is internal audit or readiness assessment, not independent attestation. He cannot change his own access (no IAM writes, and the `internal-auditor-*` policy names are outside the engineer's `grc-*` rights). Every change to it is an ISSM-approved PR.
- D4, build access: none. The Internal Auditor has no write access, so the engineer (ISSE) deploys the AWS designs in Jason's projects after ISSM approval, unless a later access-change PR decides otherwise.
- Deploy is approved by the owner and runs as a separate change, following the steps below.

### Deploy steps (owner-gated, not run)

In this copy, run steps 2 and 3 from `infrastructure/` (`cd infrastructure` first), so the `cloudformation/...` paths and the validator resolve.

Preconditions:
- The `test` branch's pending reconciliation (ff9443f, unpushed) is pushed and released first, owner-gated.
- The `github-before-aws-guard` hook blocks every step below unless the primary checkout is on clean `main` equal to `origin/main`.

1. Repo flow (website): PR `feature/grc-internal-auditor` into `dev`, then promote `dev` into `test`. On `test`, run `python3 Quality-Assurance/build_release.py`, `python3 Quality-Assurance/qa.py`, `python3 -m unittest discover -s tests`, and the localhost preview (no public site file changes, so expect identical output). Merge `test` into `main` with `--no-ff`, push, `git fetch`, and confirm `HEAD == origin/main` and a clean tree. GRC-Projects: PR `feature/jason-internal-auditor` into `main`, ISSM approves (docs only, no AWS).
2. Full policy validation from clean main (ISSM, read-only AWS calls): `AWS_PROFILE=340collective AWS_REGION=us-east-1 /tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py --account-id 570814274897 --region us-east-1 --engineer rasheed --analyst adam --auditor jason`. Expect zero blocking Access Analyzer findings on all 9 policies and every scenario passing.
3. `CREATE` change set for the new stack `grc-internal-auditor` (`grc-access-model` is not touched):

   ```bash
   aws cloudformation create-change-set --stack-name grc-internal-auditor \
     --change-set-type CREATE \
     --change-set-name add-internal-auditor \
     --template-body file://cloudformation/grc-internal-auditor.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=InternalAuditorUserName,ParameterValue=jason \
     --profile 340collective --region us-east-1
   aws cloudformation wait change-set-create-complete --stack-name grc-internal-auditor --change-set-name add-internal-auditor --profile 340collective --region us-east-1
   aws cloudformation describe-change-set --stack-name grc-internal-auditor --change-set-name add-internal-auditor --profile 340collective --region us-east-1
   ```

   Expect exactly 4 `Add` (`InternalAuditorReadPolicy`, `InternalAuditorGuardrailsPolicy`, `GrcAuditorGroup`, `GrcInternalAuditorUser`), 0 Modify, 0 Remove. Anything else: `delete-change-set` and stop. With the owner's OK: `execute-change-set`, then `wait stack-create-complete`. Then confirm `grc-access-model` is unchanged (`detect-stack-drift` IN_SYNC, no new stack events).
4. Onboard (existing README runbook, ISSM): `aws iam create-login-profile --user-name jason --password '<temp>' --password-reset-required`. Deliver the password out of band (never in a repo, GitHub, or Jira). Jason signs in, sets a password, enrolls MFA, and signs back in with MFA.
5. Verify: `list-groups-for-user jason` shows `GRC-Auditor`. The group has 5 attached policies. With MFA: Security Hub `get-findings` and `get-credential-report` work, while `ssm get-parameter` on `/340collective/stripe/*`, `s3 get-object` on the site bucket, and `securityhub batch-update-findings` are AccessDenied. `detect-stack-drift` returns IN_SYNC on both `grc-internal-auditor` and `grc-access-model`. Record the closure of DEV-001 and tag `live-YYYY-MM-DD` on the deployed `main` commit.
6. Rollback: before execute, delete the change set (for a `CREATE` change set this also removes the `REVIEW_IN_PROGRESS` stack placeholder with `delete-stack --stack-name grc-internal-auditor`). After execute, for fast containment the ISSM deletes `jason`'s login profile (runbook). For full rollback, delete stack `grc-internal-auditor` from clean `main` after committing the decision: CloudFormation removes the 4 resources, but first delete `jason`'s login profile, access keys, and MFA device, or the user delete fails. A failed create rolls back on its own (`ROLLBACK_COMPLETE`, then delete the empty stack). `grc-access-model` and the old `Jason-Contractor-Auditor` are untouched throughout.

### Retire `Jason-Contractor-Auditor` (committed runbook, owner-gated)

Runs only after deploy step 5 passes and Jason has signed in with MFA as the new user `jason` (stack `grc-internal-auditor`, confirm with `aws cloudformation describe-stack-resource --stack-name grc-internal-auditor --logical-resource-id GrcInternalAuditorUser`). `Jason-Contractor-Auditor` is in no stack, so this runbook is the change record. Run it from clean `main` as `340collective`:

```bash
U=Jason-Contractor-Auditor
# 0. read-only pre-checks: expect group ExtAuditor, policy IAMUserChangePassword, no inline policies, no keys, no MFA, no certs or SSH keys
aws iam list-groups-for-user --user-name "$U" --profile 340collective
aws iam list-attached-user-policies --user-name "$U" --profile 340collective
aws iam list-user-policies --user-name "$U" --profile 340collective
aws iam list-access-keys --user-name "$U" --profile 340collective
aws iam list-mfa-devices --user-name "$U" --profile 340collective
aws iam list-signing-certificates --user-name "$U" --profile 340collective
aws iam list-ssh-public-keys --user-name "$U" --profile 340collective
aws iam list-service-specific-credentials --user-name "$U" --profile 340collective
# stop if anything other than the expected state appears
# 1. remove from ExtAuditor
aws iam remove-user-from-group --group-name ExtAuditor --user-name "$U" --profile 340collective
# 2. detach the managed policy (DeleteUser fails while it is attached)
aws iam detach-user-policy --user-name "$U" --policy-arn arn:aws:iam::aws:policy/IAMUserChangePassword --profile 340collective
# 3. delete the console login profile
aws iam delete-login-profile --user-name "$U" --profile 340collective
# 4. delete the user
aws iam delete-user --user-name "$U" --profile 340collective
# 5. verify: expect NoSuchEntity
aws iam get-user --user-name "$U" --profile 340collective
```

Not reversible as the same identity (a re-created user gets a new unique ID). CloudTrail keeps its history. Afterwards, update `Operations/TEAM-ROSTER.md` (private website repo), `Technology/ARCHITECTURE.md` (private website repo), and both access-model READMEs from "until retirement" to "retired YYYY-MM-DD" through the branch flow, and close DEV-001. `iam-baseline` is unaffected, because the user is no longer in it. If the iam-baseline IMPORT has already run, `ExtAuditorGroup` simply has no members.

### DEV-001

DEV-001 (the auditor exempt from enforced MFA) closes when the `GRC-Auditor` user is live and has signed in with MFA and `Jason-Contractor-Auditor` is retired. Until then it stays in force for the old user. See the closure note in [infrastructure/cloudformation/grc-access-model/README.md](../cloudformation/grc-access-model/README.md).

### Follow-ups

- Whether to retire the empty `ExtAuditor` group too (owner call).
- The owner sets Jason's GRC project role in the Jira admin UI so he can transition and comment on his own items (GRC-3, GRC-4, GRC-5, GRC-10).
- The next 08 access review notes the two Jason identities until retirement.
