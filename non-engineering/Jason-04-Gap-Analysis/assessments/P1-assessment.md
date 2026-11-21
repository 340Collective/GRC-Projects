# Phase 1 assessment (Internal Auditor)

**Status:** Draft for review. Not an approval.
**Assessor:** Jason (Internal Auditor)
**Phase:** P1, Oct 19 to 25, 2026
**Assessed:** Nov 21, 2026 (late; due during P2)
**Repository state:** main at 26e59d8
**Tracking:** Jira GRC-107 (Assess Phase 1)

## 1. Scope and method

- **Scope:** AWS only. The ISSM limited assessments to AWS and excluded GitHub on Oct 21 (#41). GitHub process items are listed separately in section 6 as observations, not findings.
- **Projects:** Shared foundation (Faris, partner Adam), 06 Evidence Automation (Maria, partner Adam), 13 BC/DR and IR (Rasheed, partner Jason), 14 Identity and Access (Abdifatah, partner Adam).
- **Partner assessed:** I wrote the 13 requirements and am the 13 partner. My assessment of 13 is partner assessed, so readers should weigh it with that in mind.
- **Method:** Read only AWS console review in us-east-1 with the GRC-Auditor access (MFA), Nov 21, 2026. Services checked: CloudFormation, CloudTrail, AWS Config, S3, Billing and Cost Management. Repository files were read to compare what is documented with what is running.
- **Limits:** Cost and usage data was not visible to the auditor role (see A1). Project 14 is mostly Okta, which is outside AWS.
- **Data handling:** No account IDs, ARNs, or real resource names appear in this file. Resources are described by role.

## 2. Summary

| Project | Deployed on AWS | Result |
| --- | --- | --- |
| Foundation | No. No grc-foundation stack, though #177 merged Nov 7. The pre-existing account trail is logging and multi-region. | Findings |
| 06 Evidence Automation | Yes. Stack status UPDATE_COMPLETE. | Controls observed operating. Final report pending. |
| 13 BC/DR and IR | No. No stack found. Build merged Nov 7 (#176). | Not assessable on AWS |
| 14 Identity and Access | No AWS stack (full stack list checked). | Not assessable on AWS (Okta scope) |

Account level: seven findings (A1 to A7), mainly resources outside code and cost drivers. Spend is well under the cap: USD 2.12 month to date, USD 2.38 forecast, against a USD 10 budget (Nov 21).

## 3. Project results

### Foundation

- **F-01 (medium). The foundation stack is not deployed.** No grc-foundation stack exists in CloudFormation, although its template merged Nov 7 (#177). Every later build is meant to use the foundation's shared key and evidence bucket pattern (GOVERNANCE, Dependencies between builds).
- **Account trail (FR-16): condition met, evidence not on file.** The account trail exists, is multi-region, and is logging. It is managed by a CloudFormation stack created Aug 8, 2026, which describes log file validation and an encrypted, private log bucket. FR-16 calls for a console screenshot after deploy; Adam-Foundation RESULTS.md does not record it.

### 06 Evidence Automation

Observed on the evidence bucket:

- Block all public access is on, at bucket and account level.
- Default encryption is SSE-KMS with the bucket key enabled. SSE-C is blocked.
- Tagged grc-project = 06-evidence-automation.
- A lifecycle rule expiring current versions and permanently deleting noncurrent versions is enabled for the whole bucket. The expiry days were not opened; the 30 day value in GOVERNANCE is not independently confirmed.

ISSO validation passed on Nov 11 (Adam-06 RESULTS.md). The final report is not on main yet. Result: controls observed operating, with no AWS findings on the bucket.

### 13 BC/DR and IR (partner assessed)

No CloudFormation stack exists for 13. With nothing deployed, recovery objectives, restore timing, cleanup and approver separation cannot be assessed. Status, dependencies and dates are recorded on #111 (Nov 21).

### 14 Identity and Access

No AWS stack for 14 exists in the full stack list. The 14 build is Okta based, which is outside the AWS scope set on Oct 21. Not assessable in this phase.

## 4. Account level findings

**A1 (medium). Cost detail is not visible to the team.** Billing and Cost Management reports "Activate IAM Access is not enabled". Cost breakdown, cost allocation and Cost Explorer are access denied, so nobody but the root user can see which service drives spend. The budget page is readable and shows the total: USD 2.12 month to date and USD 2.38 forecast against USD 10 (21 and 24 percent, Nov 21). The cap is being met; what cannot be checked is where the money goes.
*Action:* the owner activates IAM access to billing, and grants the auditor read only cost visibility, or shares a monthly breakdown by service on the program record.

**A2 (medium). Anomaly alerts cannot fire at this scale.** The one alert subscription triggers at USD 100 and 40 percent, with daily summaries to one recipient. Three anomalies were detected in the last 90 days: Aug 26 (USD 0.20), Oct 22 (USD 0.73), and Nov 1 to 9 (USD 0.25). None would reach the threshold.
*Action:* lower the threshold to fit a USD 10 account, for example USD 1, and confirm who receives it.

**A3 (low). The budget's name and records do not match.** The only budget is USD 10 a month, which matches the cap, but it is named for USD 5. Two stacks describe a USD 10 budget (the access model stack and a business budget stack), yet only one budget exists, so one of those records is wrong. The budget has one action on standby. A business stack describes a budget stop action that denies Bedrock to one role, which is likely this action (assumption). GOVERNANCE plans alerts at 1, 5 and 10 dollars; the alert thresholds were not opened.
*Action:* rename or document the budget, record which stack owns it, and confirm its alert thresholds.

**A4 (medium). Config runs at full cost and keeps data for 7 years.** The recorder is on with continuous recording of all resource types (764 default plus 4 overrides). Data retention is the default 7 years. GOVERNANCE cheap mode calls for daily recording and few rules, and the program allows no permanent data past the January 2027 teardown.
*Action:* move to periodic recording of the types the builds need, and set retention to fit the program end date, by pull request.

**A5 (medium). Resources exist outside code and would survive teardown.** Two buckets created during the program have no tags and are not created or referenced by anything in the repository: the Config delivery bucket (created Oct 26) and a roles document bucket (created Oct 28). The 06 stack uses this existing Config recorder. GOVERNANCE requires every resource to come from a tagged stack, with no hand made resources unless a teardown step exists. Tags were readable on the 06 bucket, so the missing tags are not a permissions issue.
*Action:* bring both under a stack, or record a teardown step and owner for each, or file a deviation request.

**A6 (medium). Project keys are driving cost while the shared key does not exist.** The Nov 1 to 9 anomaly's root cause is AWS Key Management Service: USD 0.27 actual against USD 0.02 expected (USD 0.25 impact). It began the day the 06 stack was created, and the 06 evidence bucket uses its own customer managed key. Linking the anomaly to that key is an assumption, but the size fits one key at about USD 1 a month. GOVERNANCE names per project keys as the largest fixed cost (USD 13 to 16 a month if each build has its own) and says sharing the foundation key brings this to about USD 1. The foundation key is not deployed (F-01), so later builds have no shared key to use.
*Action:* deploy the foundation key before more builds deploy, and have new builds use it instead of their own.

**A7 (medium). A stack is deployed that is not in the repository.** The stack grc-uar-sim-users-6 (created Oct 24) is running, but the repository has templates only for users stacks 1 to 5, on main or any branch. GOVERNANCE requires deploys only from this repository's clean main. The stack also creates a synthetic IAM user named after a team member (with a deny all boundary, no password and no keys, per its description). It belongs to project 08 (Phase 2); recorded here because it is an account level control gap.
*Action:* commit the template by pull request or delete the stack, and use a synthetic name.
*Action:* whoever has billing access records the root cause on the program record.

## 5. Recommended priorities

1. A5 and A7: resources and a stack outside code, because they break the teardown and change control model.
2. 13: deploy grc-bcdr before integration week, or record a scope decision.
3. F-01 and A6: deploy the shared foundation key so new builds stop adding their own.
4. A4 and A1: reduce Config cost and retention, and give the team cost detail by service.

## 6. Observations outside scope (GitHub, for information only)

Excluded from findings per the Oct 21 scope decision. Listed so they are not lost.

- The real AWS account ID appears in 5 files on main (access model README and validator, three runbooks).
- #175 merged with a final commit nobody formally reviewed (0c56f13).
- #174 merged by its author through the merge queue into a side branch, with no review.
- Project 11 requirements merged (#184, Nov 17) before the requirements review.

**For the Phase 2 assessment:** the 01 platform stack (grc-platform, merged Nov 7) is not deployed. A business stack describes a scheduled Security Hub shutdown on Nov 13, at the end of its trial. If it ran, 01's Security Hub pipeline and 06's Security Hub evidence source have no input. Not yet checked.

## 7. Evidence log

| Check | Date | Result |
| --- | --- | --- |
| CloudFormation, stacks containing "bcdr" | Nov 21 | None |
| CloudFormation, grc-foundation | Nov 21 | None |
| CloudFormation, grc-evidence | Nov 21 | UPDATE_COMPLETE |
| CloudFormation, grc-access-model | Nov 21 | UPDATE_COMPLETE (confirms the auditor can list stacks) |
| CloudTrail trails | Nov 21 | 1 trail, multi-region, logging, Insights off |
| Config settings | Nov 21 | Recording on, continuous, all types, 7 year retention |
| Billing home and Cost Anomaly Detection | Nov 21 | Cost data denied; 1 budget OK; 3 anomalies in 90 days; alert at USD 100 and 40 percent |
| S3 bucket list and tags | Nov 21 | 12 buckets; 2 program buckets untagged and not in code |
| S3 evidence bucket (06) | Nov 21 | Public access blocked, SSE-KMS, tagged, lifecycle expiry enabled |
| CloudFormation, full stack list (21 stacks) | Nov 21 | No grc-foundation, grc-bcdr, grc-platform or 14 stack; grc-uar-sim-users-6 present, not in repo |
| Budgets | Nov 21 | 1 budget, USD 10, USD 2.12 actual, USD 2.38 forecast, 1 action on standby |
| Anomaly root cause (Nov 1 to 9) | Nov 21 | AWS Key Management Service, USD 0.25 impact |

Screenshots are held privately by the assessor and are not committed, because they show account details.
