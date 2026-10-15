# Synthetic User Access Review Simulation
A practice user access review (UAR) for project 08. A fictional company of 243 identities across 14 departments is created as real IAM users in the 340 Collective account, with zero effective access. Synthetic exports from HR, Okta, GitHub, and Jira sit next to them. The reviewer certifies every identity on the worksheet as of 2026-10-01 (Q4 2026), the same way the 08 lab reviews real identities.

Status: documentation and data only in this repo, not deployed. The CloudFormation templates live only in the private 340collective-website repo (infrastructure is never stored here). The ISSM deploys after approval, the review runs, and then every stack is deleted. This is temporary and is deprecated after the review.

## What is in AWS and what is in the CSVs
| Lives in | What | Why |
| --- | --- | --- |
| AWS IAM, path `/uar-sim/` | 222 IAM users, 14 groups (`uar-sim-*`), customer managed policies (`uar-sim-*`), attached AWS managed policies, a few inline policies, HR-style tags on every user | Real objects, so the reviewer practices the real IAM API calls |
| `data/aws-credential-report.csv` | Console and access key history: password use, MFA, key age, key last use | AWS sets these dates itself and they cannot be faked. The synthetic report is the authoritative activity source for `/uar-sim/` users |
| `data/hr-roster.csv` | People, departments, titles, levels, managers, status, hire, termination, and contract end dates | HR is the source of truth for who should have access |
| `data/okta-users.csv`, `data/github-collaborators.csv`, `data/jira-users.csv` | Accounts in the other systems | Those systems are not part of the AWS account |
| `data/role-access-baseline.csv` | Expected access for each department, level, and title | The birthright matrix the review compares against |
| `data/uar-worksheet.xlsx` | The 08 certification worksheet, one row per identity, decisions left blank | The deliverable the reviewer completes |

The live credential report (`aws iam get-credential-report`) will show `/uar-sim/` users with no password and no keys, because none exist. Use the synthetic report for their history.

## Why real IAM users with zero effective access
- Every synthetic user has the permissions boundary `uar-sim-deny-all-boundary`, whose single statement denies every action on every resource. A permissions boundary caps what identity policies can grant, so effective access is zero even for users with `AdministratorAccess` attached.
- Every synthetic group also has an inline policy `uar-sim-guard-deny-all` that denies everything. A real user added to a synthetic group by mistake gains nothing.
- No user has a console password (`AWS::IAM::LoginProfile`) or an access key (`AWS::IAM::AccessKey`). Nobody can sign in as these users.
- `aws iam simulate-custom-policy` with an allow-everything policy plus the boundary returns `explicitDeny` for `iam:CreateUser`, `s3:GetObject`, `ec2:RunInstances`, and `sts:AssumeRole`.

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
The general categories are the ones from the 08 lab and a standard quarterly UAR: access that outlived employment or a contract, access beyond the role baseline, administrator or wildcard permissions without a business need, missing MFA on console users, dormant or stale credentials, access keys on humans, separation-of-duties conflicts, accounts with no owner or a shared owner, and records that disagree between systems. Most identities are clean.

Names differ between systems (nicknames, changed surnames, typos, middle initials). Join on employee ID, IAM user name, or email, never on name alone.

## How the review runs
Roles follow [GOVERNANCE.md](../../GOVERNANCE.md): Adam (ISSO) performs the review, Jason (Internal Auditor) grades it against a private answer key, and Faris (ISSM) holds the key and approves. The answer key and the generator are not in this repo.

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
   ```
2. Join the IAM tags (`employee-id`, `department`, `title`, `employment-status`, `contract-end`, `owner-employee-id`) with `data/hr-roster.csv` on employee ID, and Okta, GitHub, and Jira on employee number or email.
3. Compare each identity with `data/role-access-baseline.csv` and with its activity in `data/aws-credential-report.csv`.
4. Complete `data/uar-worksheet.xlsx`: Business Justification, Reviewer Decision (Keep, Reduce, Remove), Reviewer Notes, Approver, and Date. Log every Reduce or Remove on the Remediation Log sheet.
5. Hand the worksheet to the Auditor for grading.

The worksheet is one row per identity, with the AWS columns prefilled from IAM. That keeps one decision per identity; findings in Okta, GitHub, or Jira go in Reviewer Notes.

## Deploy (ISSM only, after approval)
The templates exist only in the private 340collective-website repo (`Operations/grc-uar-sim/cloudformation/`); this repo holds documentation and data only, and nothing is deployed from it. Deploy the base stack first, then users-1 to users-5, each through a reviewed change set:

```bash
cd Operations/grc-uar-sim/cloudformation   # in the private 340collective-website repo
P=(--profile 340collective --region us-east-1)
for s in base users-1 users-2 users-3 users-4 users-5; do
  aws cloudformation create-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-create \
    --change-set-type CREATE --template-body file://grc-uar-sim-$s.yaml \
    --capabilities CAPABILITY_NAMED_IAM --tags Key=uar-sim,Value=true "${P[@]}"
  aws cloudformation wait change-set-create-complete --stack-name grc-uar-sim-$s \
    --change-set-name grc-uar-sim-$s-create "${P[@]}"
  aws cloudformation describe-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-create \
    --query 'Changes[].ResourceChange.[Action,ResourceType,LogicalResourceId]' --output table "${P[@]}"
  aws cloudformation execute-change-set --stack-name grc-uar-sim-$s --change-set-name grc-uar-sim-$s-create "${P[@]}"
  aws cloudformation wait stack-create-complete --stack-name grc-uar-sim-$s "${P[@]}"
done
```

## Teardown
Delete in reverse order: users-5 to users-1, then base. Deleting the base stack first is expected to fail while users still reference its groups and boundary, but this has not been observed yet, so follow the order rather than relying on it. Record the outcome of the first teardown here.

```bash
P=(--profile 340collective --region us-east-1)
for s in users-5 users-4 users-3 users-2 users-1 base; do
  aws cloudformation delete-stack --stack-name grc-uar-sim-$s "${P[@]}"
  aws cloudformation wait stack-delete-complete --stack-name grc-uar-sim-$s "${P[@]}"
done
aws iam list-users --path-prefix /uar-sim/ "${P[@]}"   # expect an empty list
```

## Cost and side effects
- Cost: 0 dollars. IAM users, groups, and policies are free.
- If Security Hub or AWS Config rules are enabled (for example IAM user MFA, user policy, or administrator policy checks), they will flag `/uar-sim/` users. Expect and ignore those findings for this path, or capture them as evidence for [01 GRC-as-Code](../../01-grc-as-code-platform/) and [11 Guardrails](../../11-compliance-as-code-guardrails/).
- The account ID appears only inside the ARNs of the synthetic credential report. The templates use `${AWS::AccountId}`.

## Files
| File | What it is |
| --- | --- |
| [data/](data/) | Synthetic exports and the certification worksheet; see [data/README.md](data/README.md) |
