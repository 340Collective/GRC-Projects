# Governance

How this collaboration runs. This repo is a GRC engineering portfolio built by a small team, using 340 Collective's AWS account as a shared testbed. It is a learning project, not a business need. The goal is real hands-on experience that holds up on a resume, produced under the same discipline a regulated program would use.

Status: this document is the operating manual. The project folders (00 to 13) are target designs, not yet deployed.

## Principles

- Build it as code. Infrastructure is created only through CloudFormation. Anything created by hand in the console is deleted.
- Keep it cheap. Total AWS spend stays under 10 dollars per month across the whole project, and 0 dollars is the target. Build, capture evidence, then tear it down.
- Nobody signs off on their own work. Separation of duties is enforced through roles and pull request approval.
- Change is controlled. Every change is a pull request the ISSM approves. If a needed change cannot be made, it goes through a deviation request.
- Do not make an expensive mess. Check service quotas and limits before building. If a service is not free, confirm the cost before enabling it.

## Roles

| Person | Role | Responsibility |
| --- | --- | --- |
| David | Business Owner | Owns 340 Collective and its AWS account. Approves access to the real environment. |
| Faris | ISSM / Architect (Program Lead) | Owns governance, approves or denies every pull request, is the final validator for work that has no other independent validator. |
| Rasheed | ISSE / Engineer | Implements infrastructure, fixes vulnerabilities, documents changes, builds automation. |
| Jason | Auditor / Assessor | Independent white-box review and assessment. Does not implement what he assesses. |
| Adam | ISSO / Analyst | Validates engineer work, reports on vulnerabilities, prioritizes, writes reports, makes recommendations. |

## Project assignments

Each person owns 3 to 4 projects. Assignments reflect interests and can be swapped with ISSM agreement.

| Owner | Projects |
| --- | --- |
| Faris (ISSM) | 00 Platform Overview, 01 GRC-as-Code Platform, 10 Audit Engagement Manager |
| Rasheed (ISSE) | 05 Policy Management, 06 Evidence Automation, 11 Guardrails, 13 BC/DR and IR |
| Adam (ISSO) | 07 Risk Register, 08 Access Reviews, 12 Metrics and Reporting |
| Jason (Auditor) | 02 TPRM/VRM, 03 Privacy, 04 Gap Analysis, 09 Control Testing |

Adam's optional stretch: a Splunk instance ingesting an EC2 instance for continuous-monitoring dashboards. Treat it as a learning extra and watch its cost (see Cost guardrails).

## Separation of duties

The rule is that no one validates or approves their own work. The chain:

1. The owner builds the project in a branch and opens a pull request.
2. An independent validator reviews it. For engineer-built work (Rasheed), Adam validates. For assessment work, Jason assesses independently.
3. The ISSM (Faris) approves or denies the pull request. Nothing merges to `main` without ISSM approval.
4. For Adam's own build projects (07, 08, 12), the ISSM is the independent validator, since the usual validator is the author. This closes the gap where the validator would otherwise have no validator.

## Change process

Modeled on a FedRAMP-style change workflow.

1. Open a change by creating a branch and a pull request against `main`. Describe what changes, why, and the expected cost impact.
2. The independent validator reviews.
3. The ISSM approves or denies. Approval merges; denial returns it with comments.
4. If a change is needed but cannot be made (a quota block, a cost ceiling, a missing dependency), file a deviation request instead of forcing the change.

### Deviation request

When you cannot make a required change, document it so the gap is tracked rather than hidden. Include:

- What was required and why it cannot be done now.
- The risk or control affected.
- The workaround or compensating control in place.
- The target date to revisit.

## Cost guardrails

The project runs at or near 0 dollars. These are the rules and the watch list that keep it there.

- Every account gets an AWS Budget of 10 dollars with alerts at 1, 5, and 10 dollars, defined in CloudFormation.
- Build, capture evidence with screenshots, then deprecate. Tearing the stack down after evidence is captured is a required step, not optional.
- Check service quotas and limits before building anything.

Services that can break the budget if left running. Confirm cost before enabling:

- QuickSight (used by 07 and 12 designs): not covered by the usual free tier. Standard authors run about 9 to 12 dollars per user per month, which alone can exceed the whole budget. For a 0 dollar target, use CloudWatch dashboards or a static export instead.
- Macie (03): free trial, then charges per gigabyte scanned. Keep to the trial or sample data.
- Audit Manager (06): charges per assessment. Enable only while capturing evidence, then disable.
- Config, GuardDuty, Inspector, Security Hub (01, 06, 11): free tiers that expire, usually after 30 days, then charge per item. Watch the clock and tear down.
- Splunk plus EC2 (Adam's stretch): Splunk Free caps at 500 MB per day, and the EC2 host is only free inside the 12-month free tier. The easiest way to overshoot 10 dollars.

## Access to the real environment

Access to 340 Collective's AWS account is granted only after David's accounts exist and only through least-privilege IAM defined in CloudFormation. Access is not granted by hand.

- Roles are defined as code, scoped to what each role needs: engineer (build and deploy stacks), auditor (read-only assessment), analyst (read plus evidence export).
- David approves the access template as a pull request like any other change.
- No personal credentials or email addresses are stored in this repo or baked into templates. Roles are referenced by function, not by person.

This access model will be added as a CloudFormation template once David has created the accounts.

## Build order

Recommended order, from the root README: 01, 11, 06, 04, 09, 05, 07, 08, 10, 13, 02, 03, 12. Detect and prevent first, then evidence and assessment, then governance records, then audit and resilience, then the heavier ML and PII services, and metrics last because 12 reads every other store.

## Timeline

The project runs 3 to 6 months. Put a project on your resume only after you complete your section. The more sections you complete, the more experience you earn.
