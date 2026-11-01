# Project 13 requirements review response and PR corrections

Prepared 25 October 2026. Status: draft for the engineer to complete and submit in the existing PR. This document has not been posted. Requirements assessment, engineering review and final approval remain separate. No deployment or live control evidence is claimed.

## Recommended response

Thanks for the clear review. I submitted the YAML without its supporting source, so the review submission needs completing. I will add the source, generator and packaging instructions, make the component scope and measurement definitions explicit, and correct the PR sections and checklist. I will keep the detection inventory, operational approver assignment and shared-budget headroom marked unverified until confirmed. I understand that #170 is still pending acceptance and that live execution evidence is required later.

Use this response in future tense until the files and PR description have actually been updated. Link the committed files afterward.

## 1. Scope and targets

The review baseline is the earlier 47,859-byte YAML shared in this chat. The supporting generator reproduces that baseline. On 25 October the engineer supplied the URL and description of [requirements PR #170](https://github.com/340Collective/GRC-Projects/pull/170), which references [project issue #41](https://github.com/340Collective/GRC-Projects/issues/41). PR #170 is the Day 1 requirements submission, not the engineering YAML PR or a verified Final report item.

Its supplied description confirms Draft v0.2, proposed client-data RTO/RPO of 4h/24h and website RTO/RPO of 8h/24h, pending engineering feasibility confirmation and Faris's acceptance. This agrees with the previously supplied PDF. The PR diff, current REQUIREMENTS.md and engineering PR have not been retrieved, so detailed clause-level reconciliation still needs those current contents. The mapping below is grounded in the supplied description and PDF; it is not a claim that PR #170 has been accepted.

| Parameter | Component exercised | Draft v0.2 relationship | Status |
| --- | --- | --- | --- |
| `DynamoDbRtoSeconds` | One synthetic DynamoDB table restored to an isolated test table | Proposed client-data RTO 4 hours = 14,400 seconds, only if the owner accepts that target for this component | No default; acceptance and actual parameter value pending |
| `DynamoDbRpoSeconds` | Recoverable age of that table's synthetic timestamp marker | Proposed client-data RPO 24 hours = 86,400 seconds | No default; measurement and value pending acceptance |
| `S3RtoSeconds` | One synthetic bucket's latest objects restored to an isolated bucket | The source's business purpose must be assigned. Client-file component: proposed 14,400 seconds. Website-content component: an accepted sub-target within the proposed 28,800-second website objective; allocation must leave time for other dependencies | No default; do not infer the website RTO from the S3 service name |
| `S3RpoSeconds` | Recoverable age of that bucket's synthetic timestamp marker | Both draft service proposals use 86,400 seconds, but the source-to-service mapping still needs acceptance | No default; measurement and value pending acceptance |

`TargetApprovalReference` records the actual owner's target decision. A nonempty reference is not proof that the decision exists or that the targets were accepted.

**Engineering recommendation:** use both synthetic resources as representative client-data components for this first demonstration. Subject to owner acceptance, compare each with the proposed 14,400-second RTO and 86,400-second RPO. Keep the proposed 28,800-second website RTO and 86,400-second website RPO as separate service objectives. The synthetic S3 bucket is not evidence of website recovery. If that business mapping is rejected, assign the S3 component's purpose and target explicitly instead of inferring it from the AWS service.

**Feasibility statement:** these are reasonable initial objectives to test for the deliberately small component lab. They are not confirmed business-service capabilities. Daily backups are intended to support the proposed loss window; real backup success, recoverable timestamps, usable-service dependencies and restore times still need evidence. Full client-service recovery also needs time for reconnection and application checks; a component completing within the entire four-hour service allowance would not prove that the service can meet four hours. Final component time budgets may therefore need tightening after inventory and testing.

Included: tiny synthetic DynamoDB and S3 fixtures, daily periodic backups, quarterly component restore tests, integrity/timing results, temporary-target cleanup, findings, delivery routes, monitoring and sandbox SSM quarantine/release. Both component paths are implemented; the initial manual exercise can select one small table as required by the lab.

Outside the automated test: real client records and application recovery; website deployment/content/configuration recovery and reconnection; DNS/TLS/routing cutover; authentication, networking, external-payment dependencies; real Workspace containment; cross-Region/account-disaster recovery; S3 historical-version recovery; destination-owned 06/07 consumers. Website/client recovery procedures are supplied in PLAN, but those procedures have not been exercised.

Reports explicitly record `scope=SYNTHETIC_COMPONENT_ONLY`, `service_recovery=NOT_TESTED` and `website_recovery=NOT_TESTED`. A component PASS cannot establish either full service's RTO/RPO. Record technical restore, integrity and service usability separately.

**Decision needed:** requirements owner and engineering agree the actual source-to-service mapping, four component targets, measurement limits and excluded-service recovery work; the authorized owner accepts the scope/targets through the existing process. Do not create another approval round for this note.

## 2. Source, measurements and cleanup

Commit or link the source in this review snapshot rather than asking the reviewer to infer behavior from the YAML. README contains reproducible generation, tests, ZIP layout and S3 artifact handoff instructions.

| Concern | Source to inspect | Implemented behavior and limit |
| --- | --- | --- |
| Execution start | `tools/render_template.py`, `src/bcdr/restore.py` | Step Functions execution start becomes `started_at` and simulated `disruption_at` for both components. It is not the time of a real business outage. Sequential S3 processing includes time since that shared start. |
| Technical restore time | `src/bcdr/restore.py` | AWS Backup `CreationDate` and `CompletionDate` calculate `restore_job_seconds`. Recovery-point creation age is retained separately as a diagnostic. Neither is substituted for component RTO or RPO. |
| Integrity and RTO | `src/bcdr/validate.py` | After target-readiness, encryption/access-configuration and full tiny-dataset count/hash checks, component RTO is the ceiling of elapsed UTC seconds since `started_at`. The validator records `validated_at` immediately afterward. The elapsed-time clock read and stored timestamp are separate calls, so boundary rounding may differ slightly when recomputing from displayed timestamps; do not claim exact timestamp arithmetic beyond this implementation. |
| RPO | `src/bcdr/fixtures.py`, `src/bcdr/validate.py` | Marker write start is stored in the recovered content; its acknowledged time is pinned in the baseline. Once hashes match, the conservative RPO is `ceil(disruption_at - recovered write_started_at)`. The lower bound is `floor(disruption_at - write_acknowledged_at)`, clamped at zero. It proves static synthetic data age, not application transaction continuity. Hash mismatch records RPO as not demonstrated. |
| Validator privacy | `src/bcdr/validate.py` | Reads the permitted tiny restored dataset in memory to compute hashes; reports counts/hashes, not record content. This requires clearer wording than a literal claim that it reads only pre-existing counts/checksums. |
| Ordinary cleanup | `src/bcdr/cleanup.py`, `src/bcdr/common.py` | Checks execution-derived target identity/ownership, waits for the restore writer, deletes the test table or all test-bucket versions/delete markers, and checks absence. It does not delete installed source fixtures after each run. |
| Interrupted cleanup | `src/bcdr/monitor.py`, `src/bcdr/restore.py` | Independent 15-minute reconciliation handles ended executions and uncertain restore starts. An S3 creation interrupted before ownership tagging remains unresolved for authorized evidence-based reconciliation; the code refuses to delete an unverified same-name bucket. Cleanup failure remains a finding. |
| Reports and routing | `src/bcdr/report.py`, `evidence.py` | Version/hash-pinned reports, separate cleanup/integrity/delivery states, correlated events and pending sign-off. Event acceptance is not destination persistence or Jira issue proof. |

The only content-bearing operations here are against synthetic fixtures and isolated test targets. Local tests are mocked. Live timing, IAM, integrity, cleanup and failure-routing evidence remain outstanding.

## 3. Detection dependencies

| Source | What is confirmed from this package | Environment status / next confirmation |
| --- | --- | --- |
| Restore failures, overdue tests, interrupted cleanup and delivery failures | Source/rules/alarms are supplied for these project-generated signals | Not deployed or exercised; test finding, Jira issue, alarm receipt and cleanup later |
| CloudTrail | Collector can retrieve selected management-event records; the plan requires audit coverage | Existing trail, log retention, relevant selectors/S3 data events and actual alert routing are unverified. Retrieving events is not an implemented CloudTrail detection/alert pipeline |
| GuardDuty | Listed as an IR triage input in PLAN | Existing enablement, coverage, finding consumer and response owner unverified; this stack does not enable or subscribe to GuardDuty findings |
| Workspace identity/audit | Listed for the agreed phishing/client-file scenario | Admin access, available logs, retention and alert/triage route unverified; outside this AWS test harness |
| Stripe dispute notices | Listed as a business/IR triage input, with an authorized business owner | Existing notification channel, recipient role, triage and sample receipt unverified; no Stripe ingestion is built here |
| Projects 06 and 07 | Conditional outgoing event-bus rules | 06 is being built; 07 is planned. Receivers and durable persistence/replay are pending, not successful integrations |

No external source above has been confirmed operational from this review. Do not label it absent merely because this stack does not provision it. Reuse existing operational detection where available. Record each source's owner, evidence and expected readiness on the existing project item. Any proposed deferral needs its scope impact, interim procedure, owner and due date; none has been accepted by this document.

## 4. Approvals and role separation

Proposed operational approver: the independently assigned **IR lead or designated change approver**, with authority for sandbox quarantine and release. The organization must confirm the assignment; the auditor, validator and final project approver are not automatically operational containment approvers.

The engineer/operator starts the approved Automation document and supplies an incident reference. The document embeds `IrApproverArn` from deployment configuration; its execution parameters cannot replace the approver. `aws:approve` requires one approval and aborts on rejection/failure/timeout before applying the policy. Quarantine and release are separate executions and approvals. The Automation service role can get/put policy only on this stack's sandbox bucket.

This template does not prove separation of the real people or their effective IAM permissions. Privately confirm that the operator cannot assume/use the approver identity, self-approve, alter the approved execution path, or bypass an approval through another permitted action. Test operator denial plus independent approval, rejection and timeout. Keep principal/account details out of the public PR; publish role labels and sanitized outcome references only.

## 5. Cost and evidence retention

Pricing checked 25 October 2026 for a small us-east-1 running configuration. Offline preparation adds no AWS charges. The USD 10/month cap is program-wide; it is not a Project 13 allowance.

| Monthly dimension | Planning basis | Estimate / status |
| --- | --- | --- |
| CloudWatch metric alarms | Nine standard alarm metric units across five alarms at USD 0.10 | USD 0.90 before shared free allowances |
| Three custom problem metrics | Emitted only while nonzero; full-month maximum at USD 0.30 each | USD 0 to USD 0.90 |
| Inspector, if existing account policy covers these functions | Four functions; standard USD 0.30 each, or standard + code USD 0.90 each | Add USD 1.20 or USD 3.60; account configuration unverified |
| Backup, restores and temporary targets | Two tiny sources, daily periodic backups, seven-day warm retention, quarterly tests plus initial pass/failure tests, prompt target deletion | Usage-based; measured sizes, billable minimums and test frequency still need pricing confirmation |
| Lambda, Step Functions, DynamoDB, S3, Scheduler/EventBridge/API destination, SQS/SNS, KMS requests, logs and any SSM execution/storage charges | 256-MiB functions, 15-minute monitor, daily fixtures, small records/reports and occasional exercises | Usage-based; no full-month usage measurement available |
| Shared controls and other projects | Existing CMK, audit/detection services, code bucket, notification topic and Jira connection | Account baseline/forecast not supplied; include their charges once in the program total |

Known monitoring/scanning subtotal is USD 0.90-1.80 without Inspector, USD 2.10-3.00 with standard scanning, or USD 4.50-5.40 with standard plus code scanning, **before the remaining usage and shared-account costs**. These are partial estimates, not full cost quotes. A sub-USD 1 claim is unsupported.

For review planning, reserve **USD 3/month of incremental project capacity before Inspector**, as a provisional allowance rather than a validated forecast. This consists of the USD 1.80 monitoring ceiling plus USD 1.20 contingency for the tiny workload's remaining usage. If inherited scanning applies, provisional reserves become USD 4.20 or USD 6.60. This contingency is a planning choice and may be insufficient if assumptions or inherited services change. Do not report the cost item resolved until the engineer verifies the actual billable quantities, account scanning and remaining headroom.

Before live deployment, record existing program forecast `B`, validated incremental Project 13 estimate `P` and remaining headroom `10 - B - P`. If using those provisional reserves, the existing forecast must be at most USD 7.00, USD 5.80 or USD 3.40 respectively, with additional margin appropriate to the uncertainties. Current spend/forecast and actual test spend are unverified. Follow the accepted budget/change process for a projected breach; do not disable required controls to meet the number.

Official pricing: [CloudWatch](https://aws.amazon.com/cloudwatch/pricing/), [Inspector](https://aws.amazon.com/inspector/pricing/), [Backup](https://aws.amazon.com/backup/pricing/), [Lambda](https://aws.amazon.com/lambda/pricing/), [Step Functions](https://aws.amazon.com/step-functions/pricing/), [Systems Manager](https://aws.amazon.com/systems-manager/pricing/), [KMS](https://aws.amazon.com/kms/pricing/). The source snapshot does not create a new key or Jira connection. Existing shared charges still belong in the account forecast.

Evidence is separate from the seven-day Lambda diagnostic logs:

| Record | Location and current retention behavior |
| --- | --- |
| DR baseline and reports | CMK-encrypted, private, versioned `ReportBucket`; `baselines/` and `dr-tests/` paths. Submitted baseline has no completed-object expiry. Version/hash pointers identify the exact report |
| IR/tabletop records | Actual records are imported by the evidence tooling into `ReportBucket` under its IR paths. Example forms are not records of a conducted exercise |
| Results/targets/cleanup/delivery states | `ResultsTable`, with no automatic record TTL configured. It remains part of the running system |
| Lambda diagnostics | Four log groups, `RetentionInDays: 7`; not the durable audit-evidence store |
| Backup recovery points | Configurable backup lifecycle; example/default seven days, distinct from evidence retention; no vault lock |
| CloudTrail originals | Existing approved restricted audit location; actual coverage and retention need confirmation |

Proposed evidence minimum: keep completed report versions and sanitized execution/tabletop/sign-off records through operation, partner assessment and Final report sign-off. Before authorized end-of-program deletion, the evidence custodian verifies the required copies and manifests in the designated restricted location outside Git and accepts their retention/disposal date. No exact post-program duration has been supplied or accepted. With 06 not ready, retain the Project 13 evidence and explicitly copy/backfill it later; old events will not automatically replay.

## 6. PR description and checklist corrections

The engineering PR Summary must identify this as an **initial engineering implementation review**, not a completion or acceptance PR. Link [project issue #41](https://github.com/340Collective/GRC-Projects/issues/41) and [requirements PR #170](https://github.com/340Collective/GRC-Projects/pull/170). The supplied description identifies those references; neither is established as the Final report item. Add the actual Final report item link when available. If it has not been created/identified, say so explicitly. Keep the supplied Day 1 requirements description on the requirements PR; write a separate implementation summary for the engineering YAML/source PR.

Suggested engineering Summary, to adapt after actually committing the supporting files:

> Refs #41. Requirements: #170, Draft v0.2, pending feasibility confirmation and Faris's acceptance. This is the initial Project 13 engineering implementation review for synthetic DynamoDB/S3 component restore tests and sandbox approval-gated IR runbooks. It includes the CloudFormation template, supporting source, generator and packaging instructions. Full website/client-service recovery and live acceptance evidence remain outstanding. Final report item: not yet linked; add the actual item reference before marking that link complete.

| PR entry | Honest current status |
| --- | --- |
| Issue / requirements / Final report links | Project issue #41 and requirements PR #170 are identified from the supplied description; engineering PR link, current detailed requirements diff and actual Final report item remain outstanding |
| Expected cost | Use the partial estimate and pending account-baseline statement above; live cost is not USD 0 |
| Threat model | Required issue entry for evidence/access/scripts is not verified; add or link the actual lightweight threat model |
| Code reviewer named | Engineering reviewer assigned; assignment does not mean review completed |
| Code review completed | Leave unchecked until the engineering review is actually recorded |
| Partner final-report sign-off / ISSO validation | N/A for this initial non-finishing PR; still required later. This initial requirements comment is neither sign-off nor approval |
| Partner record PR only | N/A; this is the engineering implementation PR |
| Final approval / merge | Pending the authorized approver; do not self-merge or deploy from a branch |
| Tests run | Paste actual command/output for the actual PR revision; label package-local checks separately from repo/AWS checks |
| New dependency approval / scripts making AWS calls | Pinning does not establish dependency approval. Operator/runtime scripts do make AWS calls; do not tick an unconditional no-network/no-AWS statement |
| AI assistance | Select AI assisted. Tool: ChatGPT/Codex. Describe generated YAML, Python, tests and documents plus this source-based response; engineering verification remains the engineer/reviewer's responsibility |

AI verification statement: source behavior and the supplied YAML were inspected; this snapshot's local checks are recorded in LOCAL-CHECKS. The engineer supplied the requirements PR URL/description, which agrees with the earlier PDF on the proposed targets and pending acceptance. Not verified: actual engineering PR/AGENTS/current requirements PR diff, repository-wide required checks, AWS validate-template, repository policy validator, effective IAM, live restores/timing/cleanup, detection readiness, real Jira/06/07 persistence, cost/headroom, exercise records or human approvals. Do not mark unrun checks passed. The requirements author's AI disclosure covers that requirements document; the engineering PR needs its own accurate AI assistance statement for its generated code, template and documents.

## Engineer inputs still needed

1. The engineering YAML PR link/current description, plus the current REQUIREMENTS.md or requirements PR #170 diff if it differs from the supplied v0.2 PDF. The requirements PR URL/description and project issue reference are now supplied; do not ask for them again.
2. Confirmed detection inventory, operational approver-role assignment and evidence-retention owner/date, using role labels publicly.
3. Current program forecast and inherited Inspector/other shared-service configuration, so the provisional allowance can become a defensible total estimate.

Add source and correct the existing PR now; these outstanding facts can remain visibly pending during review. Requirements acceptance and the existing deployment prerequisites still apply before live use.
