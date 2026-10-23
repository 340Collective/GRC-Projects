# Shared foundation: requirements

Status: Draft, pending ISSO acceptance. Target design, not yet deployed.

| Field | Value |
| --- | --- |
| Project | Shared foundation (part of 01 GRC-as-Code Platform) |
| Stack | `grc-foundation`, from `infrastructure/cloudformation/grc-foundation.yaml` |
| Engineer (builds) | Faris (ISSM) |
| Code review | Rasheed (ISSE), with Maria (Automation Engineer) as backup |
| Named backup for the build | Rasheed (ISSE) |
| Accepts these requirements and the build, gives final approval | Adam (ISSO) |
| Phase assessment (not an approval) | Jason (Internal Auditor), in Phase 2 |
| Informed | David (Business Owner) |
| Phase | Phase 1, Week 1, Oct 19 to 25, 2026, 3 points (L) |
| Jira epic | [GRC-30](https://340collective.atlassian.net/browse/GRC-30) |
| Kickoff | Day 1, Monday Oct 19, 2026 |

This document is the foundation half of Design step 1 in [LAB-STEPS.md](LAB-STEPS.md). The ISSM wrote it. The ISSO accepts it at the Day 1 kickoff, because nobody accepts their own requirements ([GOVERNANCE.md](../../GOVERNANCE.md#separation-of-duties)). The 01 platform requirements are a separate document for Phase 2.

How to read it: each requirement has an ID (FR-1, FR-2, ...), a plain statement, and an acceptance check. Every check names the evidence the ISSO will see. None of them needs the ISSO to write code. Evidence posted to the project item or GitHub is sanitized (no account IDs, ARNs, or emails), per [CONTRIBUTING.md](../../CONTRIBUTING.md#data-rules-apply-to-every-phase).

## 1. Purpose and scope

### Purpose

Every later `grc-*` build reuses one shared base. The foundation is that base. It sets how templates reach AWS, gives the program one encryption key, keeps the account audit trail safe, defines how temporary evidence is stored, and confirms engineers build inside the access model.

### In scope

| Component | What the foundation provides |
| --- | --- |
| Deploy pipeline | The path from a template in this repo to a CloudFormation stack in AWS, with review and approval before deploy |
| Encryption key | One customer managed KMS key tagged `grc-project` |
| Logging | The account-wide CloudTrail trail stays on, and engineers cannot stop or change it |
| Evidence bucket pattern | A reusable temporary evidence bucket: versioned, private, encrypted with the key, short lifecycle, deletable |
| Access model | Engineers build with `GRC-Engineer` seats inside the permissions boundary and the MFA rule |

### Out of scope

- The 01 Security Hub platform (`grc-platform`): Config, Security Hub, GuardDuty, Inspector, EventBridge routing, the Lambdas, DynamoDB, Jira paths, and Audit Manager. That is Phase 2 (Week 2, Oct 26 to Nov 1, epic GRC-2). It is out of scope here except where the foundation must support it (the key, the bucket pattern, and the deploy path).
- The control crosswalk JSON (Design step 4). It belongs to 01.
- Creating, changing, or replacing the CloudTrail trail itself. The trail exists today and is managed outside this repo.
- Changes to the access model, the engineer seats, or the budget. Those are separate access-change pull requests.
- Turning on any paid security service.

## 2. Requirements

### 2.1 Deploy pipeline

| ID | Requirement | Acceptance check (evidence the ISSO sees) |
| --- | --- | --- |
| FR-1 | The foundation template lives in this repo at `infrastructure/cloudformation/grc-foundation.yaml`. (The same rule for later templates is a constraint in Section 4.) | The file is on `main` in GitHub at that path. |
| FR-2 | The template reaches `main` only by pull request from a feature branch. Nobody commits to `main` directly. | The merged pull request link on the foundation's Final report item, showing the branch name and the merge. |
| FR-3 | The ISSE reviews the code (the Automation Engineer if the ISSE is out). The ISSM does not review his own code. | The pull request shows the reviewer's approval or review comments from the ISSE or the Automation Engineer. |
| FR-4 | The pull request includes the `infrastructure/` checks from CONTRIBUTING.md section 4 and the Required checks in `infrastructure/README.md`: cfn-lint prints nothing, validate-template returns no error, the policy validator (`validate_policies.py ... --skip-aws`) ends with `RESULT: all checks passed`, and the template is under 51,200 bytes. | The pasted output of all four checks in the pull request description, including the validator's final `RESULT: all checks passed` line. |
| FR-5 | The template holds no secrets, emails, or account IDs. It takes the account from `AWS::AccountId`. | The secrets and identifiers check output in the pull request is empty, or every hit is explained. |
| FR-6 | The ISSO gives final approval before any deploy. | The ISSO's approval comment on the foundation's Final report item, dated before the stack's creation time. |
| FR-7 | The stack is named `grc-foundation` and is deployed only from this repo's clean `main` (equal to `origin/main`), never from a branch or by hand. The ISSM reviews the change set before running it. | A short deploy note on the project item with the two matching commit hashes (local `main` and `origin/main`) and a screenshot of the change set summary. |
| FR-8 | The deploy waits for `CREATE_COMPLETE`. | A CloudFormation console screenshot or `describe-stacks` output showing `grc-foundation` in `CREATE_COMPLETE`. |
| FR-9 | After deploy, drift detection reports `IN_SYNC`. | A drift detection screenshot or output showing `IN_SYNC`. |
| FR-10 | The deployed commit is tagged `live-YYYY-MM-DD` and the tag is pushed. | The tag is visible in GitHub's tag list and points at the merge commit. |

### 2.2 Encryption key

| ID | Requirement | Acceptance check (evidence the ISSO sees) |
| --- | --- | --- |
| FR-11 | The stack creates exactly one customer managed KMS key. | The stack's Resources tab lists one `AWS::KMS::Key`. |
| FR-12 | The key carries the tag key `grc-project`. The access model only lets engineers create and use keys with this tag. | A KMS console screenshot of the key's Tags tab showing `grc-project`. |
| FR-13 | The key has an alias that starts with `alias/grc-`. | A KMS console screenshot showing the alias. |
| FR-14 | Automatic key rotation is on. (By judgment: not stated in the source docs, proposed as good practice at no extra cost for the key itself.) | A KMS console screenshot of the Key rotation tab showing it enabled. |
| FR-15 | The key policy lets the access model's IAM policies take effect, so the engineer, the ISSO's analyst seat, and the Internal Auditor seat get exactly the key use their policies allow and no more. | The ISSO's analyst seat (signed in with MFA) can open a test object encrypted with the key (FR-24). A screenshot of the key policy is attached to the project item. |

### 2.3 Logging (CloudTrail)

| ID | Requirement | Acceptance check (evidence the ISSO sees) |
| --- | --- | --- |
| FR-16 | The foundation does not create, change, stop, or delete the account trail. CloudTrail stays on for the whole account and records every build, test, and teardown. | The stack's Resources tab has no `AWS::CloudTrail::Trail`. A CloudTrail console screenshot shows the existing trail with logging on, taken after deploy. |
| FR-17 | Engineers cannot stop or change CloudTrail. This is already enforced by the access model's `DenyAuditTampering` statement. The foundation must not weaken it. | The pull request diff shows no change to `grc-access-model.yaml`. A screenshot of an access-denied result when the engineer seat tries to stop logging, or the policy validator's simulation output for that scenario. |
| FR-18 | The foundation's own actions appear in CloudTrail. | CloudTrail Event history (console, readable by the ISSO's analyst seat) shows the stack creation, the key creation, and the bucket creation events for the deploy date. |

### 2.4 Temporary evidence bucket pattern

The pattern is defined once in `grc-foundation.yaml` and reused by later builds. The foundation creates one bucket from it, for the foundation test.

| ID | Requirement | Acceptance check (evidence the ISSO sees) |
| --- | --- | --- |
| FR-19 | The bucket is named `grc-evidence-*`, so the ISSO's analyst seat can write evidence to it and the Internal Auditor seat can read it. | The bucket name shown in the stack's Resources tab (redacted if it contains the account ID). |
| FR-20 | Versioning is on. | S3 console Properties tab: Bucket Versioning "Enabled". |
| FR-21 | The bucket is private: all four Block Public Access settings are on, and object ownership is "bucket owner enforced" (ACLs off). (By judgment: "private" is read as these settings, matching the existing `compliance-evidence` template.) | S3 console Permissions tab screenshot showing Block all public access "On" and ACLs disabled. |
| FR-22 | Default encryption is SSE-KMS with the foundation key from FR-11. | S3 console Properties tab: Default encryption shows SSE-KMS and the key's alias. |
| FR-23 | No Object Lock and no legal hold. | S3 console Properties tab: Object Lock "Disabled". The test object shows no legal hold. |
| FR-24 | A test object written to the bucket is encrypted with the foundation key. | The test object's Properties tab shows SSE-KMS with the foundation key. The ISSO opens it with the analyst seat. |
| FR-25 | Lifecycle rules: current objects expire after 30 days, noncurrent versions after 7 days, incomplete multipart uploads after 1 day. | S3 console Management tab screenshot listing the three rules with those day counts. |
| FR-26 | DeletionPolicy and UpdateReplacePolicy are both `Delete` on the bucket, so the stack can remove it. | The two lines in the merged template on GitHub, pointed out in the pull request. |
| FR-27 | Integrity comes from a SHA-256 hash per object plus a manifest. The manifest lists each object's key, version ID, and SHA-256 hash. | For the test object: the manifest entry, and a fresh hash of the downloaded object. The two SHA-256 values match. The sanitized manifest is attached to the project item. |
| FR-28 | Teardown empties the bucket, including every object version and delete marker, then deletes the stack. | Before delete: a version listing that is empty. After delete: the stack shows `DELETE_COMPLETE` and the bucket no longer exists. |

### 2.5 Access model

| ID | Requirement | Acceptance check (evidence the ISSO sees) |
| --- | --- | --- |
| FR-29 | The ISSM builds, deploys, tests, and tears down the foundation with a `GRC-Engineer` seat, not with his admin identity. | CloudTrail Event history for the stack creation shows the engineer seat as the caller (user name redacted to its role if needed). |
| FR-30 | The engineer seat is inside the permissions boundary and signed in with MFA. | IAM console screenshot of the engineer seat showing the `grc-permissions-boundary` and an assigned MFA device. CloudTrail shows MFA used for the deploy session. |
| FR-31 | Every resource the stack creates is named `grc-*` (or `alias/grc-*` for the key alias). Any IAM role the stack creates is `grc-*` and carries the permissions boundary. | The stack's Resources tab. If there are roles, the IAM console shows the boundary on each. |
| FR-32 | The stack runs in us-east-1 only. | The stack and the key show us-east-1 in the console. |

### 2.6 Lifetime

| ID | Requirement | Acceptance check (evidence the ISSO sees) |
| --- | --- | --- |
| FR-33 | `grc-foundation` stays up while any later phase uses it. It is the last `grc-*` project stack deleted. | At the end-of-program teardown, the CloudFormation stack list shows every other `grc-*` project stack deleted before `grc-foundation`. |
| FR-34 | The ISSE, as named backup, can run or finish the foundation if the ISSM is out. | The ISSE's walkthrough note on the project item (Partner test step 1). |

## 3. Security and compliance targets

### ASFF control scope

The program's control language is the [ASFF control matrix](../../non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx). Each row has an ASFF `SecurityControlId` (for example `CCF-CRY-05`) and a `Compliance.RelatedRequirements` list (for example `SOC2-CC6.7`), the same field the [architecture doc](GRC-Platform-Architecture.md) uses in every finding. The foundation is mapped to the IDs below. Every ID and every SOC 2 reference in this table appears in the matrix's `ASFF SecurityControlId` and `SOC 2 (TSC)` columns.

| ASFF SecurityControlId | Control (matrix name) | SOC 2 criteria in the matrix | Foundation requirements |
| --- | --- | --- | --- |
| `CCF-CHG-01` | Change Management Program | CC2.2, CC3.4, CC6.8, CC8.1 | FR-1 to FR-10 |
| `CCF-CHG-02` | Configuration Change Control | CC2.2, CC3.4, CC6.8, CC8.1 | FR-2, FR-6 to FR-9 |
| `CCF-CHG-02.2` | Test, Validate & Document Changes | CC3.4, CC8.1 | FR-4, FR-8, FR-9 |
| `CCF-CFG-02` | Secure Baseline Configurations | CC6.1, CC6.7, CC7.1, CC8.1 | FR-9, FR-21, FR-25 |
| `CCF-HRS-11` | Separation of Duties (SoD) | CC5.1 | FR-3, FR-6 |
| `CCF-CRY-09` | Cryptographic Key Management | CC6.1 | FR-11 to FR-15 |
| `CCF-CRY-05` | Encrypting Data At Rest | CC6.1, CC6.7 | FR-22, FR-24 |
| `CCF-MON-02` | Centralized Collection of Security Event Logs | CC7.2, CC7.3 | FR-16, FR-18 |
| `CCF-MON-08` | Protection of Event Logs | (no CC criterion; PI1.4, PI1.5) | FR-17 |
| `CCF-DCH-18` | Media & Data Retention | (no CC criterion; C1.1, PI1.5) | FR-25 |
| `CCF-DCH-21` | Information Disposal | CC6.5 | FR-25, FR-28 |
| `CCF-IAC-21` | Least Privilege | CC5.2, CC6.1 | FR-29 to FR-31 |
| `CCF-IAC-06` | Multi-Factor Authentication (MFA) | CC6.6 | FR-30 |
| `CCF-CPL-02` | Security, Compliance & Resilience Controls Oversight | CC1.1, CC2.2, CC2.3, CC4.2 | FR-6, Section 7 acceptance |
| `CCF-HRS-03` | Defined Roles & Responsibilities | CC1.2, CC1.3, CC1.4, CC1.5, CC2.1, CC2.2, CC5.3, CC7.4 | Role table at the top, FR-3, FR-34 |
| `CCF-PRM-05` | Security, Compliance & Resilience Requirements Definition | CC2.2, CC4.1, CC5.2 | This document as a whole |
| `CCF-RSK-03` | Risk Identification | CC3.2, CC3.4, CC7.2, CC9.1 | Section 6 risks |

The matrix lists criteria (for example `CC8.1`) and points of focus (for example `CC8.1-POF3`) in the same column. The table above applies one rule to every row: it lists each CC criterion that appears in the row, either on its own or as the parent of any listed point of focus, and leaves out the points of focus themselves. Non-CC criteria (C, PI, P, A) are shown only where a row has no CC criterion.

Not mapped: integrity by hash and manifest (FR-27). The matrix's integrity controls are for files, endpoints, software, and AI data, not evidence objects, so mapping FR-27 would be a stretch. The Internal Auditor may propose an ID in his assessment.

### SOC 2 CC1 to CC9 coverage

The foundation is plumbing, so it supports some criteria directly and others only through the process around it. The mapping below comes from the matrix table above. Rows marked "judgment" are the ISSM's reading, not a matrix entry. The Internal Auditor assesses this coverage in Phase 2. His assessment is not an approval.

| Criteria | How the foundation supports it | Basis |
| --- | --- | --- |
| CC1 Control environment | Roles are named, and nobody approves their own work (ISSO accepts and approves the ISSM's build) | Matrix (`CCF-CPL-02`, `CCF-HRS-03`) |
| CC2 Communication and information | Written, testable requirements accepted on record before build | Matrix (`CCF-PRM-05`, `CCF-HRS-03`, `CCF-CPL-02`) |
| CC3 Risk assessment | Changes go through review and impact checks. Section 6 records risks | Matrix (`CCF-CHG-01`, `CCF-RSK-03`) |
| CC4 Monitoring activities | Indirect only: the ISSO checks each requirement against evidence, and the Internal Auditor assesses the phase | Matrix (`CCF-CPL-02`, `CCF-PRM-05`), plus judgment on how much the foundation itself contributes |
| CC5 Control activities | Separation of duties in the change path, least privilege through the boundary | Matrix (`CCF-HRS-11`, `CCF-IAC-21`) |
| CC6 Logical and physical access | Key management, encryption at rest, private bucket, MFA, least privilege, disposal | Matrix (`CCF-CRY-09`, `CCF-CRY-05`, `CCF-CFG-02`, `CCF-IAC-06`, `CCF-IAC-21`, `CCF-DCH-21`) |
| CC7 System operations | Account trail stays on and records the build. Drift detection confirms the baseline | Matrix (`CCF-MON-02`, `CCF-CFG-02`) |
| CC8 Change management | Pull request, review, approval, deploy from clean `main`, tag | Matrix (`CCF-CHG-01`, `CCF-CHG-02`, `CCF-CHG-02.2`) |
| CC9 Risk mitigation | Weak. The cost cap and teardown limit business disruption risk, but vendor and business continuity risk belong to 02 and 13 | Matrix (`CCF-RSK-03` lists CC9.1), plus judgment that the foundation adds little here |

## 4. Constraints

| Constraint | Rule | Source |
| --- | --- | --- |
| Cost cap | Program cap is 10 dollars a month for the whole account, with budget alerts at 1, 5, and 10 dollars. 0 dollars is the target | [GOVERNANCE.md](../../GOVERNANCE.md#cost-guardrails), [README.md](README.md) |
| Foundation cost | The customer managed key costs about 1 dollar a month. S3 storage for test objects is a few cents. No paid security service is turned on | [shared/access-model/README.md](../../shared/access-model/README.md) (Cost) |
| Region | us-east-1 only. The access model denies other regions | [shared/access-model/README.md](../../shared/access-model/README.md) |
| Naming | Resources `grc-*`; evidence buckets `grc-evidence-*`; key aliases `alias/grc-*`; SSM parameters under `/grc/` | [shared/access-model/README.md](../../shared/access-model/README.md) (Resource naming rules). Key aliases: the `KmsGrcAliases` statement in [grc-access-model.yaml](../../infrastructure/cloudformation/grc-access-model.yaml) |
| Tagging | KMS keys (and API Gateway APIs) tagged `grc-project` | Same |
| Template | One template per stack; the file name is the stack name; under 51,200 bytes; account from `AWS::AccountId`. Every later foundation-dependent template is also `infrastructure/cloudformation/grc-*.yaml`; this is checked in each later project's review, not at foundation acceptance | [infrastructure/README.md](../../infrastructure/README.md) |
| Change control | Feature branch, pull request into `main`, code review, ISSO approval, merge, deploy from clean `main` equal to `origin/main`, wait for `CREATE_COMPLETE`, tag `live-YYYY-MM-DD` and push the tag. Nothing deploys from a branch or by hand | [infrastructure/README.md](../../infrastructure/README.md), [CONTRIBUTING.md](../../CONTRIBUTING.md) |
| Data | No secrets, keys, passwords, emails, account IDs, or personal data in git. Raw evidence stays in the temporary bucket and is deleted at teardown. Only sanitized evidence goes to GitHub | [CONTRIBUTING.md](../../CONTRIBUTING.md#data-rules-apply-to-every-phase), [GOVERNANCE.md](../../GOVERNANCE.md#where-work-lives) |
| Time box | 7 days. Day 1 kickoff, Days 2 to 6 build and review, Day 7 final report and sign-off. If at risk by Day 4, flag it on the project item | [GOVERNANCE.md](../../GOVERNANCE.md#7-day-build-rule) |

## 5. Test plan and teardown

### Test (from LAB-STEPS Test)

| Step | What the ISSM does | What the ISSO sees | Covers |
| --- | --- | --- | --- |
| T-1 | Put a test object (synthetic, no real data) in the bucket made from the pattern | The object's properties: SSE-KMS with the foundation key, a version ID, no legal hold | FR-20, FR-22 to FR-24 |
| T-2 | Show the bucket's versioning, Object Lock, and lifecycle settings | Console screenshots of the three settings | FR-20, FR-23, FR-25 |
| T-3 | Hash the test object, write the manifest, download the object, hash it again | The two SHA-256 values match, and the manifest entry matches | FR-27 |
| T-4 | Find the deploy and the test write in CloudTrail | Event history entries for the deploy, and the KMS `GenerateDataKey` management event that S3 logs when it encrypts the test write with the foundation key. The S3 write itself is a data event and does not show in Event history. If S3 Bucket Key is on and no KMS event lines up with the test write, T-1's object properties (SSE-KMS with the foundation key) stand in for it. This evidence is subject to the kickoff decision on Section 6, item 5 | FR-18 |
| T-5 | Check actual spend in the budget | The budget page and the actual figure (see Section 6, item 2) | Cost cap |

### Partner test (from LAB-STEPS Partner test)

| Step | Who | What |
| --- | --- | --- |
| P-1 | ISSM and ISSE | Walk the ISSE through the foundation, so he can run or finish it (FR-34) |
| P-2 | ISSO | Review the foundation against this document, commit the results to `non-engineering/Adam-Foundation/RESULTS.md`, and give final approval, since the ISSM built it |
| P-3 | Internal Auditor | Commits his SOC 2 mapping and coverage assessment to his own folder and links it on the project item. This is an assessment, not an approval |
| P-4 | ISSM | Puts the build notes (what was deployed and the test results; no secrets or raw evidence) in FINAL-REPORT.md sections 3 and 7, in the Day 7 pull request. It merges only after the ISSO's sign-off and final approval are on the Final report item |

Day 7: the ISSM fills in [FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md) in this folder. The ISSO commits his results to [non-engineering/Adam-Foundation/RESULTS.md](../../non-engineering/Adam-Foundation/RESULTS.md), compares them with the report, and signs off on the Final report item ("Accepted by: <first name>", or findings).

### Teardown

The foundation is not torn down at the end of Phase 1. It stays up for the whole program, because every later build uses it.

- During Phase 1: delete the test object and all its versions once evidence is captured.
- At the end-of-program teardown, after every other `grc-*` project stack is gone: empty the bucket (every version and delete marker), delete `grc-foundation` from clean `main`, and wait for `DELETE_COMPLETE`.
- The KMS key goes into its pending deletion window when the stack is deleted. That is normal: AWS waits before it destroys a key.
- Record teardown evidence where the ISSM designates, outside git, and note it on the project item.

## 6. Risks and open questions for the kickoff

| # | Item | Why it matters | Proposed answer |
| --- | --- | --- | --- |
| 1 | Closed: the ISSM's `GRC-Engineer` seat is deployed. `grc-engineer-users` went live on 2026-10-18 (tag `live-2026-10-18`), and the seat's console login was sent on 2026-10-22 | FR-29 and FR-30 need that seat. Without it, the build cannot start on Day 2 | Done. No deviation request is needed |
| 2 | The cost rule says alerts at 1, 5, and 10 dollars, but the access model was deployed without its own budget. The existing account budget has a 10 dollar limit with alerts at 80 and 100 percent and a forecast alert, not at 1 or 5 dollars. October spend was already about 1.53 dollars by Oct 16 | LAB-STEPS Test step 4 records actual spend in FINAL-REPORT.md section 6, but there is no 1 dollar alert to trip | The ISSO decides at kickoff: accept T-5 as "actual spend under 10 dollars, and the foundation adds about 1 dollar", or raise a separate pull request that adds the 1 and 5 dollar alerts. This document does not change the cost rule |
| 3 | `grc-foundation` is not in the stack map in `infrastructure/README.md`, and it is not clear if it is a shared stack or a project stack | Shared stacks are ISSM-deployed; project stacks are engineer-deployed. The ISSM is both, so the risk is small, but the docs should say which | Add `grc-foundation` to the stack map in the same pull request as the template, as "Deployed by the ISSM with his `GRC-Engineer` seat; delete last" |
| 4 | The trail itself is outside this repo. LAB-STEPS Deploy step 1 says "logging settings that keep CloudTrail on" | It is unclear what, if anything, the template must contain for logging | Read it as "the foundation must not touch the trail" (FR-16, FR-17). No logging resource in the template |
| 5 | CloudTrail Event history shows management events only. Object writes to S3 are data events and appear only if the trail records S3 data events | LAB-STEPS Test step 2 says "confirm CloudTrail records the test writes" | Use the KMS encryption event for the test write as evidence (it is a management event). If the template turns on S3 Bucket Key, S3 calls KMS once per bucket key rather than once per object, so that event may not match the test write; T-1's object properties are then the fallback. Decide at kickoff whether Bucket Key is on, and confirm whether this evidence is enough |
| 6 | Value of the `grc-project` tag is not specified | The access model checks only that the tag exists | Use `foundation` |
| 7 | Automatic key rotation (FR-14) and the "private" settings (FR-21) are the ISSM's reading, not stated in the source docs | The ISSO should accept or strike them knowingly | Keep both. Drop FR-14 if the ISSO prefers to stay exactly on the source text |
| 8 | A TLS-only bucket policy is in the existing `compliance-evidence` template but not in the foundation pattern | It is a cheap control (encryption in transit), but adding it changes the pattern | Leave it out of this version. Raise it as a proposed change at kickoff |
| 9 | The existing `compliance-evidence` stack is a different, older pattern (SSE-S3, not `grc-*`) | Readers may confuse the two | The foundation pattern replaces it for `grc-*` builds. `compliance-evidence` stays a separate shared stack |
| 10 | The analyst seat can write to `grc-evidence-*` buckets and use `grc-project` keys, but cannot delete | Teardown of evidence the ISSO wrote falls to the engineer | Accepted. The engineer empties the bucket at teardown (FR-28) |
| 11 | Single person risk: the ISSM builds the foundation and also builds 01 next week, which depends on it | A Phase 1 slip delays Phase 2 | The ISSE is the named backup (FR-34). The 3-day extension rule applies |
| 12 | The architecture doc names Terraform and GitHub Actions | They are not used here | Every stack is CloudFormation in this repo, per LAB-STEPS Design step 2 |

## 7. Acceptance

The ISSO accepts these requirements at the Day 1 kickoff. [GOVERNANCE.md](../../GOVERNANCE.md#separation-of-duties) sets this in Separation of duties step 1 (the ISSO accepts the requirements the ISSM writes: 00, the foundation) and in [Sign-off](../../GOVERNANCE.md#sign-off) (the ISSM accepts each partner's requirements at kickoff, and the ISSO accepts the ISSM's own and the 01 requirements). The ISSO records the acceptance as a comment on the foundation's GitHub Final report item, or on the pull request for this document. The [GRC-30](https://340collective.atlassian.net/browse/GRC-30) Jira epic is the tracking link only. The comment uses the GOVERNANCE sign-off format ("Accepted by: <first name>", or findings). The block below mirrors that comment. Filling it in here does not replace the comment.

Accepted by: ____ (Adam, ISSO)

Date: ____

Findings or conditions (one per line, or "none"):

- ____

Answers to the open questions in Section 6 (number and decision):

- ____
