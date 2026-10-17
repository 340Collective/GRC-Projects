# Synthetic User Access Review Simulation
A practice user access review (UAR) for project 08. A fictional company of 243 identities across 14 departments is created as real IAM users in the 340 Collective account, with zero effective access. Synthetic exports from HR, Okta, GitHub, and Jira sit next to them. The reviewer certifies every identity on the worksheet as of 2026-10-01 (Q4 2026), the same way the 08 lab reviews real identities.

Status: the stacks are deployed (tag live-2026-10-14-2). The hard-mode update in this change is pending deployment. The CloudFormation templates live in this repo at `infrastructure/cloudformation/grc-uar-sim-*.yaml` (moved from the private website repo on 2026-10-17). The generator and the answer key stay private in the website repo, so the reviewer never sees the answers. After the review every stack is deleted. This is temporary and is deprecated after the review.

## What is in AWS and what is in the CSVs
| Lives in | What | Why |
| --- | --- | --- |
| AWS IAM, path `/uar-sim/` | 222 IAM users, synthetic groups (`uar-sim-*`), customer managed policies (`uar-sim-*`), attached AWS managed policies, a few inline policies, a synthetic role, HR-style tags on every user | Real objects, so the reviewer practices the real IAM API calls |
| `data/aws-credential-report.csv` | Console and access key history: password use and age, MFA, key age, key last use, Region, and service | AWS sets these dates itself and they cannot be faked. The synthetic report is the authoritative activity source for `/uar-sim/` users |
| `data/hr-roster.csv` | People, departments, titles, levels, managers, status, hire, termination, and contract end dates | HR is the source of truth for who should have access |
| `data/okta-users.csv`, `data/github-collaborators.csv`, `data/jira-users.csv` | Accounts in the other systems | Those systems are not part of the AWS account |
| `data/role-access-baseline.csv` | Expected access for each department, level, and title | The birthright matrix the review compares against |
| `data/access-requests.csv` | Access request and approval log: who asked, for whom, what, who approved, when, and until when | Access beyond the baseline needs an approval that holds up |
| `data/exceptions-register.csv` | Approved exceptions to the access standard, with the control, reason, compensating control, and expiry | An exception only covers the control it names, until it expires |
| `data/uar-worksheet.xlsx` | The 08 certification worksheet, one row per identity, decisions left blank | The deliverable the reviewer completes |

## Which source is authoritative
- Credential activity and age (passwords, MFA, access key rotation, last use, Region, service): the synthetic `data/aws-credential-report.csv`. The live credential report (`aws iam get-credential-report`) shows `/uar-sim/` users with no password, no MFA, and no keys, by design: they are kept powerless, so no password or key is ever created for them.
- Structure and entitlements (users, groups, group membership, attached and inline policies, policy documents and versions, roles, trust policies, tags): live IAM under `/uar-sim/`.
- People, status, and dates: `data/hr-roster.csv`. Approvals and exceptions: the two log files.

The worksheet's Access Level column is derived from policy names. Treat it as a starting point, not evidence, and read the policy documents.

## Why real IAM users with zero effective access
- Every synthetic user has the permissions boundary `uar-sim-deny-all-boundary`, whose single statement denies every action on every resource. A permissions boundary caps what identity policies can grant, so effective access is zero even for users with `AdministratorAccess` attached.
- Every synthetic group also has an inline policy `uar-sim-guard-deny-all` that denies everything. A real user added to a synthetic group by mistake gains nothing.
- The synthetic role under `/uar-sim/` carries the same `uar-sim-deny-all-boundary` as its permissions boundary and the same inline guard, so even if it were assumed its effective access is zero. The users who appear in its trust policy cannot call `sts:AssumeRole` at all, because their boundary denies it.
- No user has a console password (`AWS::IAM::LoginProfile`) or an access key (`AWS::IAM::AccessKey`). Nobody can sign in as these users.
- `aws iam simulate-custom-policy` with an allow-everything policy plus the boundary returns `explicitDeny` for `iam:CreateUser`, `s3:GetObject`, `ec2:RunInstances`, and `sts:AssumeRole`, for users and for the role.

Neither the boundary nor the guard is something to review. They are the safety net for the simulation.

## The simulated company
243 identities in total: active employees, people on leave, departed employees, contractors (L0), service accounts (`svc-*`), and a few generic accounts. Levels use the 340 Collective career ladder names, L0 to L5. In this scaled-up fictional company, L1 to L5 are employees and only L0 are contractors (the real ladder treats L1 as contractors).

| Department | Active headcount | Levels |
| --- | --- | --- |
| Executive | 7 | L4, L5 |
| Finance and Accounting | 12 | L1, L1 Sr, L2, L3, L4 |
| People and HR | 8 | L1, L1 Sr, L2, L3, L4 |
| Legal and Compliance | 5 | L1, L1 Sr, L3, L4 |
| Sales | 25 | L1, L1 Sr, L2, L3, L4 |
| Marketing | 14 | L1, L1 Sr, L2, L3, L4 |
| Creative Production | 33 | L1, L1 Sr, L2, L3, L4 |
| Content and Social | 16 | L1, L1 Sr, L2, L3, L4 |
| Client Success | 14 | L1, L2, L3, L4 |
| Engineering | 16 | L1, L1 Sr, L2, L3, L4 |
| IT and Infrastructure | 8 | L1, L2, L3, L4 |
| Security and GRC | 6 | L1 Sr, L2, L4 |
| Data and Analytics | 8 | L1, L1 Sr, L2, L3, L4 |
| Operations and Facilities | 8 | L1, L3, L4 |
| Total active employees | 180 | |

Contractors, departed employees, service accounts, and generic accounts are on top of the 180.

## What to look for
The general categories are the ones from the 08 lab and a standard quarterly UAR: access that outlived employment or a contract, access beyond the role baseline, administrator or wildcard permissions without a business need, missing MFA on console users, dormant or stale credentials, access keys on humans, separation-of-duties conflicts, accounts with no owner or a shared owner, and records that disagree between systems. Also: approvals and exceptions that do not hold up, credentials used in unexpected ways, duplicate or reused identities, privilege that arrives indirectly, and missing policy guardrails. Most identities are clean, and some things that look wrong are explained by the evidence; check before you decide.

Names differ between systems (nicknames, changed surnames, typos, middle initials). Join on employee ID, IAM user name, or email, never on name alone.

## How the review runs
Roles follow [GOVERNANCE.md](../../../GOVERNANCE.md): Adam performs the review, Jason grades it against a private answer key, and Faris holds the key and approves. The answer key and the generator are not in this repo.

1. Pull the IAM side (read-only calls):
   ```bash
   P=(--profile 340collective --region us-east-1)
   aws iam generate-credential-report "${P[@]}"
   aws iam get-credential-report "${P[@]}" --query Content --output text | base64 --decode > live-credential-report.csv
   aws iam list-users --path-prefix /uar-sim/ "${P[@]}"
   aws iam list-groups --path-prefix /uar-sim/ "${P[@]}"
   aws iam list-groups-for-user --user-name <user> "${P[@]}"
   aws iam list-attached-user-policies --user-name <user> "${P[@]}"
   aws iam list-user-policies --user-name <user> "${P[@]}"
   aws iam list-user-tags --user-name <user> "${P[@]}"
   aws iam list-attached-group-policies --group-name <group> "${P[@]}"
   aws iam list-group-policies --group-name <group> "${P[@]}"
   aws iam list-policies --scope Local --path-prefix /uar-sim/ "${P[@]}"
   aws iam get-policy --policy-arn <arn> "${P[@]}"
   aws iam list-policy-versions --policy-arn <arn> "${P[@]}"
   aws iam get-policy-version --policy-arn <arn> --version-id <v> "${P[@]}"
   aws iam list-roles --path-prefix /uar-sim/ "${P[@]}"
   aws iam get-role --role-name <role> "${P[@]}"
   aws iam list-attached-role-policies --role-name <role> "${P[@]}"
   aws iam list-role-policies --role-name <role> "${P[@]}"
   aws iam get-account-authorization-details --filter User Group Role LocalManagedPolicy "${P[@]}" > iam-details.json
   ```
2. Join the IAM tags (`employee-id`, `department`, `title`, `employment-status`, `contract-end`, `owner-employee-id`) with `data/hr-roster.csv` on employee ID, and Okta, GitHub, and Jira on employee number or email.
3. Compare each identity with `data/role-access-baseline.csv`, with its activity in `data/aws-credential-report.csv`, and with any request in `data/access-requests.csv` or exception in `data/exceptions-register.csv` (both join on the Identity and on HR employee_id).
4. Complete `data/uar-worksheet.xlsx`: Business Justification, Reviewer Decision (Keep, Reduce, Remove), Reviewer Notes, Approver, and Date. Log every Reduce or Remove on the Remediation Log sheet.
5. Hand the worksheet to the Auditor for grading.

The worksheet is one row per identity, with the AWS columns prefilled from IAM. That keeps one decision per identity; findings in Okta, GitHub, or Jira go in Reviewer Notes.

## Deploy (ISSM only, after approval)
The templates are in [infrastructure/cloudformation/](../../../infrastructure/README.md) (`grc-uar-sim-base.yaml` and `grc-uar-sim-users-1.yaml` to `grc-uar-sim-users-5.yaml`). The ISSM deploys them only from this repo's clean `main`. The generator and the answer key stay private in the website repo and write regenerated templates into this folder. Deploy the base stack first, then users-1 to users-5, each through a reviewed change set.

The steps that change AWS (`execute-change-set` and `delete-stack`) name each stack literally, one command per stack. The ISSM's local `github-before-aws` guard maps a stack to its repo by its literal `--stack-name` and blocks a name built from a variable such as `grc-uar-sim-$s`. Creating, waiting for, and describing a change set change nothing, so those stay in a loop.

```bash
cd infrastructure/cloudformation   # from the root of this repo, on clean main
P=(--profile 340collective --region us-east-1)
for s in base users-1 users-2 users-3 users-4 users-5; do
  aws cloudformation create-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-create \
    --change-set-type CREATE --template-body file://grc-uar-sim-$s.yaml \
    --capabilities CAPABILITY_NAMED_IAM --tags Key=uar-sim,Value=true "${P[@]}"
  aws cloudformation wait change-set-create-complete --stack-name grc-uar-sim-$s \
    --change-set-name grc-uar-sim-$s-create "${P[@]}"
  aws cloudformation describe-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-create \
    --query 'Changes[].ResourceChange.[Action,ResourceType,LogicalResourceId]' --output table "${P[@]}"
done
```

After reviewing the six change sets, execute them in order, waiting for each:

```bash
aws cloudformation execute-change-set --stack-name grc-uar-sim-base --change-set-name grc-uar-sim-base-create "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-base "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-1 --change-set-name grc-uar-sim-users-1-create "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-users-1 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-2 --change-set-name grc-uar-sim-users-2-create "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-users-2 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-3 --change-set-name grc-uar-sim-users-3-create "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-users-3 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-4 --change-set-name grc-uar-sim-users-4-create "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-users-4 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-5 --change-set-name grc-uar-sim-users-5-create "${P[@]}"
aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-users-5 "${P[@]}"
```

The stacks already exist, so later changes (such as the hard-mode update) go in as UPDATE change sets from this repo's clean main (still from `infrastructure/cloudformation/`), base first and then users-1 to users-5. Stop and get owner sign-off if any change shows `Replacement` as `True`:

```bash
for s in base users-1 users-2 users-3 users-4 users-5; do
  aws cloudformation create-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-update \
    --change-set-type UPDATE --template-body file://grc-uar-sim-$s.yaml \
    --capabilities CAPABILITY_NAMED_IAM --tags Key=uar-sim,Value=true "${P[@]}"
  aws cloudformation wait change-set-create-complete --stack-name grc-uar-sim-$s \
    --change-set-name grc-uar-sim-$s-update "${P[@]}"
  aws cloudformation describe-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-update \
    --query 'Changes[].ResourceChange.[Action,Replacement,LogicalResourceId]' --output table "${P[@]}"
done
# stop here if any Replacement is True
aws cloudformation execute-change-set --stack-name grc-uar-sim-base --change-set-name grc-uar-sim-base-update "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-uar-sim-base "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-1 --change-set-name grc-uar-sim-users-1-update "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-uar-sim-users-1 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-2 --change-set-name grc-uar-sim-users-2-update "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-uar-sim-users-2 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-3 --change-set-name grc-uar-sim-users-3-update "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-uar-sim-users-3 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-4 --change-set-name grc-uar-sim-users-4-update "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-uar-sim-users-4 "${P[@]}"
aws cloudformation execute-change-set --stack-name grc-uar-sim-users-5 --change-set-name grc-uar-sim-users-5-update "${P[@]}"
aws cloudformation wait stack-update-complete --stack-name grc-uar-sim-users-5 "${P[@]}"
```

## Teardown
Delete in reverse order: users-5 to users-1, then base. Deleting the base stack first is expected to fail while users still reference its groups and boundary, but this has not been observed yet, so follow the order rather than relying on it. Record the outcome of the first teardown here. Run it from this repo's clean `main`, one literal stack name per command:

```bash
P=(--profile 340collective --region us-east-1)
aws cloudformation delete-stack --stack-name grc-uar-sim-users-5 "${P[@]}"
aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-users-5 "${P[@]}"
aws cloudformation delete-stack --stack-name grc-uar-sim-users-4 "${P[@]}"
aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-users-4 "${P[@]}"
aws cloudformation delete-stack --stack-name grc-uar-sim-users-3 "${P[@]}"
aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-users-3 "${P[@]}"
aws cloudformation delete-stack --stack-name grc-uar-sim-users-2 "${P[@]}"
aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-users-2 "${P[@]}"
aws cloudformation delete-stack --stack-name grc-uar-sim-users-1 "${P[@]}"
aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-users-1 "${P[@]}"
aws cloudformation delete-stack --stack-name grc-uar-sim-base "${P[@]}"
aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-base "${P[@]}"
aws iam list-users --path-prefix /uar-sim/ "${P[@]}"   # expect an empty list
```

## Cost and side effects
- Cost: 0 dollars. IAM users, groups, and policies are free.
- If Security Hub or AWS Config rules are enabled (for example IAM user MFA, user policy, or administrator policy checks), they will flag `/uar-sim/` users. Expect and ignore those findings for this path, or capture them as evidence for [01 GRC-as-Code](../../Faris-01-GRC-as-Code-Platform/) and [11 Guardrails](../../Faris-11-Compliance-as-Code-Guardrails/).
- The account ID appears only inside the ARNs of the synthetic credential report. The templates use `${AWS::AccountId}`.

## Files
| File | What it is |
| --- | --- |
| [data/](data/) | Synthetic exports and the certification worksheet; see [data/README.md](data/README.md) |
