# GRC infrastructure

GRC infrastructure as code for 340 Collective's AWS account (us-east-1; the account ID is in the runbooks): the CloudFormation templates for the GRC stacks, the access-model policy validator, the evidence bucket init script, and the GRC change records. On 2026-10-17 these moved here from the private website repo, so GRC work no longer touches the business repo and a GRC change cannot reach a business stack (smaller blast radius).

Status: copied byte-identical from the website repo at commit `81a06fd`. Nothing in AWS changed for the move. Before the move, a read-only check showed every deployed stack's template equal to its file here and drift `IN_SYNC`.

## Layout

| Path | What |
| --- | --- |
| `cloudformation/<stack>.yaml` | One template per stack, flat. The file name is the stack name. |
| `cloudformation/grc-access-model/README.md` | Full access-model documentation: roles, deviations, deploy, onboarding, teardown, validation |
| `cloudformation/grc-access-model/validate_policies.py` | Policy validator (size, Access Analyzer, boundary parity, hygiene, simulation). Run it from `infrastructure/` |
| `scripts/compliance-evidence-init.py` | Initializes the temporary compliance evidence bucket after that stack is deployed |
| `runbooks/IAM-CHANGES-2026-10-17.md` | Change record and deploy steps for the engineer seats and the no-lock evidence bucket |
| `runbooks/IAM-CHANGES-2026-10-17-cloudshell.md` | Change record and deploy steps for engineer CloudShell access (standard environments, MFA required) |
| `runbooks/IAM-CHANGES-2026-10-14-GRC.md` | The GRC sections of the 2026-10-14 change record (access model, auditor, retire runbook) |

The UAR simulation generator and its answer key stay private in the website repo (the reviewer has access to this repo and must not see the answers). The generator writes regenerated templates into `infrastructure/cloudformation/` of this repo with its required `--cfn-out` option, pointed at a feature-branch worktree (it refuses a checkout on `main`); commit them here through a pull request.

## Stack map

| File | Stack | Status | Order |
| --- | --- | --- | --- |
| `grc-access-model.yaml` | `grc-access-model` | Deployed | First. Delete last |
| `grc-internal-auditor.yaml` | `grc-internal-auditor` | Deployed | After `grc-access-model`; delete before it |
| `grc-engineer-users.yaml` | `grc-engineer-users` | Planned, not deployed | After `grc-access-model`; delete before it |
| `compliance-evidence.yaml` | `compliance-evidence` | Planned, not deployed | Independent |
| `grc-uar-sim-base.yaml` | `grc-uar-sim-base` | Deployed (temporary) | Before the user stacks; delete after them |
| `grc-uar-sim-users-1.yaml` to `grc-uar-sim-users-5.yaml` | `grc-uar-sim-users-1` to `grc-uar-sim-users-5` | Deployed (temporary) | After `grc-uar-sim-base` |

Business stacks (website, blog, intake, invoicing, `collective340-iam-baseline`, and the planned `compliance-evidence-collector`) stay in the website repo.

## Provenance

Each file was copied with `cp` from the website repo (`aboutfaris/340collective-website`) at commit `81a06fd` and checked with `cmp` against `git show 81a06fd:<source>`.

| File here | Source at `81a06fd` | SHA-256 |
| --- | --- | --- |
| `cloudformation/grc-access-model.yaml` | `cloudformation/grc-access-model.yaml` | `5d31df386846eeb17022385104dd25ecadc160acecfa904a1c2a3a8a5a5fc3c9` |
| `cloudformation/grc-internal-auditor.yaml` | `cloudformation/grc-internal-auditor.yaml` | `b6615b87944c80a31a28ace341e2ad03181b65cba68463da2d3e79509e33655e` |
| `cloudformation/grc-engineer-users.yaml` | `cloudformation/grc-engineer-users.yaml` | `b39ae74a3909570141fc99d72a66d854bdd937926644f3b5957e6a5f99637e53` (as copied; changed afterwards, see below) |
| `cloudformation/compliance-evidence.yaml` | `cloudformation/compliance-evidence.yaml` | `6ab32480bb6717cf3784804a9b44248fcd4343cb3c35b2d9231414c7d9bc4bae` |
| `cloudformation/grc-uar-sim-base.yaml` | `Operations/grc-uar-sim/cloudformation/grc-uar-sim-base.yaml` | `0be30d0f57fb6b58328795fc0408de0a0b687f58e4505227b0a66b3681b682ea` |
| `cloudformation/grc-uar-sim-users-1.yaml` | `Operations/grc-uar-sim/cloudformation/grc-uar-sim-users-1.yaml` | `d5bf4ba68602bdeea498ccf0344cfcd59e66e400da2322f659192df3a9768c61` |
| `cloudformation/grc-uar-sim-users-2.yaml` | `Operations/grc-uar-sim/cloudformation/grc-uar-sim-users-2.yaml` | `78f52c9c693000859652f470c44ad3178642c2e793e9145cc87fd15c15f93389` |
| `cloudformation/grc-uar-sim-users-3.yaml` | `Operations/grc-uar-sim/cloudformation/grc-uar-sim-users-3.yaml` | `37d46b923cc2b4591a83678224fcf01715bbafc6027eb6ec501ff99bb1b042f6` |
| `cloudformation/grc-uar-sim-users-4.yaml` | `Operations/grc-uar-sim/cloudformation/grc-uar-sim-users-4.yaml` | `1d51b67187444dc42c592832f1a83cc5d7071b785feb5bda22009055e0a48442` |
| `cloudformation/grc-uar-sim-users-5.yaml` | `Operations/grc-uar-sim/cloudformation/grc-uar-sim-users-5.yaml` | `0bd25b7e2d87b2fceb0c45c0decdacc680ada80142458494d349143d8b3a0ec5` |
| `cloudformation/grc-access-model/validate_policies.py` | `cloudformation/grc-access-model/validate_policies.py` | `8d55ab61a5623b62a7a85bf267a79e7c994c6dcc7dc36aeaf2f2c5f48fbd1b1e` |
| `scripts/compliance-evidence-init.py` | `scripts/compliance-evidence-init.py` | `8d997c11d8ad49ef0287a1263b89646bce57b85d94afcef6331ecc9bb431bf32` |

`cloudformation/grc-engineer-users.yaml` was committed here byte-identical first, then changed in a separate commit on 2026-10-17 by owner decision: the Security Automation Engineer seat (parameter, condition, user, and output) was removed, leaving the Automation Engineer and ISSM builder seats. The stack is not deployed, so no AWS resource is affected. Its SHA-256 after that change is `af98e2bd0e00eaaafe10de737a267070a2dab3f07d3babf15ef83e26be1c563b`.

`cloudformation/grc-access-model.yaml` and `cloudformation/grc-access-model/validate_policies.py` were changed afterwards for engineer CloudShell ([runbooks/IAM-CHANGES-2026-10-17-cloudshell.md](runbooks/IAM-CHANGES-2026-10-17-cloudshell.md)); their SHA-256 values above are as copied.

`cloudformation/grc-access-model/README.md` was copied from the same commit and then edited for its new location (links and paths). The two runbooks were rewritten from the website change records, as each one's header explains. `validate_policies.py` still says "website layout" in a comment; the layout under `infrastructure/` is the same, so the code is unchanged.

## Required checks

Run these on your branch before the pull request, and paste the output in it. `validate-template` is a read-only AWS call; the rest are offline.

```bash
python3 -m venv /tmp/grc_cfnlint && /tmp/grc_cfnlint/bin/pip install -q cfn-lint==1.57.2   # once per machine
cd infrastructure
/tmp/grc_cfnlint/bin/cfn-lint cloudformation/*.yaml
aws cloudformation validate-template --template-body file://cloudformation/<file>.yaml --profile 340collective --region us-east-1
/tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py --account-id <account> --region us-east-1 --engineer <user> --analyst <user> --skip-aws
wc -c < cloudformation/<file>.yaml
```

Expect cfn-lint to print nothing, validate-template to return without an error, the validator to end with `RESULT: all checks passed`, and every template to be under 51,200 bytes (the inline template limit; `grc-access-model.yaml` is 49,740). Templates take the account from `AWS::AccountId` and never hardcode it. Runbooks, the access-model README, and the validator's usage text may name the account ID and region (CONTRIBUTING.md, `infrastructure/` exception); nothing here holds an email, password, or key.

## Who deploys

Engineers author and change templates in pull requests. Two kinds of stack live here:

- Shared stacks: `grc-access-model`, `grc-internal-auditor`, `grc-engineer-users`, `compliance-evidence`, and `grc-uar-sim-*` (the stack map above). Only the ISSM deploys them.
- Project stacks: each engineer's own `grc-*` stack for their project (for example `grc-risk-register` for 07). The engineer who builds the project deploys it with their `GRC-Engineer` seat, tags the deploy, and keeps it running after sign-off as part of the shared system. It is deleted only in the end-of-program teardown, as the project's LAB-STEPS say.

Either way, a stack deploys only from this repo's clean `main` equal to `origin/main`, after the pull request is merged and approved. Nothing deploys from a branch, by hand, or from the console. Agents never deploy, never run AWS writes, and never tag.

## Deploy sequence (ISSM for a shared stack, the engineer for their own project stack)

1. The pull request is reviewed, approved, and merged into `main` by the ISSM.
2. In the primary checkout, confirm clean `main` equal to `origin/main`:

   ```bash
   git switch main && git pull && git fetch origin && git status
   git rev-parse HEAD
   git rev-parse origin/main
   ```

   Expect the two hashes to match and no tracked changes.
3. Run the required checks above from clean `main`.
4. Create a change set, describe it, and get the owner's OK before executing. For a new stack use `--change-set-type CREATE`; for an existing stack use `UPDATE`. Stop and delete the change set if it shows anything unexpected, or any `Replacement` of `True` that was not planned.

   ```bash
   cd infrastructure
   aws cloudformation create-change-set --stack-name <stack> --change-set-name <name> --change-set-type UPDATE --template-body file://cloudformation/<stack>.yaml --capabilities CAPABILITY_NAMED_IAM --profile 340collective --region us-east-1
   aws cloudformation wait change-set-create-complete --stack-name <stack> --change-set-name <name> --profile 340collective --region us-east-1
   aws cloudformation describe-change-set --stack-name <stack> --change-set-name <name> --profile 340collective --region us-east-1
   aws cloudformation execute-change-set --stack-name <stack> --change-set-name <name> --profile 340collective --region us-east-1
   ```

5. Wait for `*_COMPLETE`: `aws cloudformation wait stack-create-complete` (new stack) or `stack-update-complete` (existing stack), with `--stack-name <stack> --profile 340collective --region us-east-1`.
6. Verify: `describe-stacks` shows the expected status and outputs, and `detect-stack-drift` followed by `describe-stack-drift-detection-status` reports `IN_SYNC`.
7. Tag the deployed `main` commit `live-YYYY-MM-DD` in this repo (append `-2`, `-3` for a second or third deploy that day) and push the tag. The person who ran the deploy tags it.

Rollback: before execute, `delete-change-set` (and `delete-stack` for the `REVIEW_IN_PROGRESS` placeholder of a new stack). After execute, revert the change in a new pull request and deploy that from clean `main`, or, for a new stack, delete it from clean `main` after recording the decision. Each runbook lists its own rollback.

The ISSM's local `github-before-aws` guard enforces this: it allows deploys of `grc-*` stacks (shared and project stacks alike) and `compliance-evidence` only from this repo's clean `main` equal to `origin/main`, and business stacks only from the website repo. It maps each command to a repo by its literal `--stack-name`, so type the stack name in full; a name built from a shell variable is blocked. Deploy GRC stacks with `aws cloudformation`: a `sam` or `cdk` deploy that names a `grc-*` stack is blocked. A committed deploy script needs the clean `main` of the repo that holds the script, whatever folder the command starts in.
