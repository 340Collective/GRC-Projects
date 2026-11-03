# Project 13: response to the Internal Auditor's five requirements questions

Updated 3 November 2026 for [build PR #176](https://github.com/340Collective/GRC-Projects/pull/176). Project: [#41](https://github.com/340Collective/GRC-Projects/issues/41). Requirements: [PR #170](https://github.com/340Collective/GRC-Projects/pull/170). PR #170 is merged and has an ISSM Approved review. Its committed document still says Draft v0.2 with feasibility/target acceptance pending; this response preserves that stated limitation rather than silently changing the partner document. This response answers the questions and keeps missing operating evidence visible. It does not close the requirements assessment by itself.

PR #171 was closed without merging, according to the latest team comments. This build PR is not the completing/final-report PR. The code reviewer's engineering review, the Internal Auditor's requirements assessment, the ISSO's validation and the ISSM's final approval are separate records. Handover is not a project requirement.

## 1. Scope and targets

| Parameter | Meaning | Relationship to draft #170 |
| --- | --- | --- |
| DynamoDbRtoSeconds | Simulated component test start through restored-table validation, rounded up | Proposed client-data RTO 4h = 14,400 seconds; component allocation requires owner acceptance |
| DynamoDbRpoSeconds | Conservative recovered synthetic-marker age at component-test start | Proposed client-data RPO 24h = 86,400 seconds; static fixture measurement does not prove application transaction RPO |
| S3RtoSeconds | Simulated component test start through restored-bucket validation | The owner assigns the source's purpose and component budget. Do not infer website recovery from use of S3 |
| S3RpoSeconds | Conservative recovered marker age for the synthetic bucket | Proposed 24h service objective still needs its accepted component mapping |

The initial engineering recommendation is to treat both synthetic sources as client-data components and test the proposed 14,400/86,400-second targets, subject to the owner's actual decision. The separate website objective remains proposed 8h/24h. TargetApprovalReference records a real owner decision; a nonempty parameter is not proof that acceptance happened.

The daily backup default does not provide planning margin for a 24-hour marker-age RPO once backup availability delay is included. See [the timing design](TIMING-DESIGN.md) for the calculation, a proposed twice-daily cadence and the exact owner decision. That proposal needs a documented exception to GOVERNANCE's daily-or-slower rule and a shared-budget check. It is not implemented or accepted here. The one-hour polling guard and three-hour workflow timeout are test limits, not the business RTO.

Included: tiny synthetic DynamoDB/S3 sources, backups, isolated component restores, validation, timing, cleanup, results/reports, findings, monitoring and approval-gated sandbox quarantine/release. Full website/client-service reconnection, dependencies and usability recovery are outside this component harness. Report component results at component level. No full-service result is inferred from a successful restore.

## 2. Supporting source, timing, integrity and cleanup

Canonical template: infrastructure/cloudformation/grc-bcdr.yaml at repository root. Supporting source: engineering/Rasheed-13-BCDR-IR/src/bcdr/. Generator and packaging scripts: tools/render_template.py and tools/build.py in that project folder. See the project README for exact build, ZIP layout, digest, content-addressed S3 key and pinned object-version instructions.

restore.py/controller.py retain the test start and backup/restore job facts. validate.py records validation completion, compares full counts/content digests for the tiny restored sources and checks required configuration. Component RTO is elapsed test-start-to-validation time rounded up. One completion instant, captured after all checks, supplies both elapsed RTO and validated_at. Recovered marker write-start/acknowledgement facts bound recoverable data time; the older bound is used conservatively for RPO. Backup-job completion or snapshot age is not substituted for actual RPO.

cleanup.py/janitor.py and the independent monitor reconcile restore writers and owned test targets. An API success or access-denied response is not proof that a target is absent. The operator checks target absence independently. The code and local tests are review evidence, not proof that AWS restores or cleanup ran.

report.py writes version-pinned report pointers and emits stable result/finding identifiers. EventBridge acceptance is not downstream persistence. Final report versions and the original event-pinned versions can differ; consumers must use the exact version in their event.

## 3. Detection dependencies

| Source | This build | Current evidence / gap |
| --- | --- | --- |
| Backup, workflow and validation outcomes | Built component failure/missing/late-test monitoring, findings and alarms | Live alarm receipt and Jira correlation still need execution evidence |
| CloudTrail | Evidence collector can read selected management-event records | Trail configuration, retention, selectors/data events and actual detection routes not verified |
| GuardDuty | No new deployment in this harness | Existing account availability, ownership and BCDR routing not verified |
| Workspace identity/audit and Stripe/provider alerts | Outside this AWS component harness | Access, alert routing and response procedure not verified; any deferral must be recorded against accepted scope |
| AWS Config / Project 06 | Latest team comments report an existing account recorder and reuse by 06 | This is not a newly verified BCDR detection integration |
| Projects 06/07 | Conditional outgoing bus routes | Receiver and persistence remain integration work; 06 is planned for 23-25 November |

No source is declared absent just because this template does not create it. Existing detection should be reused. Document its owner, coverage and actual readiness; proposed deferrals need the normal scope decision and interim procedure.

## 4. Approvals and separation

The engineer/operator starts an approved sandbox Automation execution. An independently assigned IR lead or designated change approver is configured privately as IrApproverArn. The runbook execution cannot replace that approver through an input parameter. Its aws:approve step precedes policy changes and aborts on rejection, failure or timeout. Quarantine and release require separate executions/approvals. The runbook service role is restricted to this stack's sandbox bucket.

The assignment and effective operator/approver separation remain to be demonstrated privately: operator cannot assume/use the approver identity or bypass the approval path. Retain sanitized approval, rejection, timeout and deny-test outcomes. Publish role labels, not personal/account details. The template alone does not prove real separation or constitute a DR-result/tabletop sign-off.

## 5. Cost and evidence retention

Offline preparation adds no AWS spend. This running design does not have a defensible USD 0 or sub-USD 1 total. The USD 10/month cap is program-wide.

Provisional planning reserve: USD 3/month incremental before inherited Inspector scanning. This is the existing USD 1.80 monitoring ceiling plus USD 1.20 contingency for the tiny workload, not a measured forecast. Four functions would add USD 1.20 for standard Inspector scanning or USD 3.60 for standard plus code scanning if covered by the account policy. Remaining program headroom and actual metering must be checked; these reserves may be insufficient if assumptions change.

Basis checked 2 November against official CloudWatch and Inspector pricing: nine standard alarm metric units at USD 0.10, three custom problem metrics up to USD 0.30 each when billed, and the four Lambda scanning units above. Backup/restores, temporary targets, Lambda/Step Functions, storage, queues, KMS requests, logs, SSM and shared-service usage remain quantity-dependent. Shared keys/connections are reused, not newly created. The account-wide program forecast and enabled scanning have not been supplied.

Pricing: https://aws.amazon.com/cloudwatch/pricing/ and https://aws.amazon.com/inspector/pricing/ . Before live approval, record existing program forecast B, validated incremental estimate P and remaining headroom 10 - B - P. Record actual test spend in the Final report when available.

Durable evidence is separate from the four seven-day Lambda diagnostic log groups. Versioned, CMK-encrypted ReportBucket stores baselines, DR reports and imported IR/tabletop records. ReportBucket and the sandbox IrBucket now expire current and noncurrent versions using required EvidenceRetentionDays and abort incomplete multipart uploads after one day. No duration is selected by default. Record any exception to GOVERNANCE's general 30-day rule before use. ResultsTable has no automatic record TTL. Recovery points keep their separate backup-plan lifecycle, with no vault lock.

The latest 06 discussion proposes about 100 days for a dedicated BCDR prefix, with the ISSM's agreement in principle for planning. Formal approval belongs to the implementing PR. This build supplies the source-side version cleanup mechanism, not an approved duration or the receiving lake's retention rule. Before deployment, record the approved input and ensure event-pinned original versions remain readable for the agreed window and retained-lookup test. Lifecycle also applies to existing versions, so review their age before enabling it. Current expiry uses object age and creates a delete marker; noncurrent expiry uses time since supersession and permanently deletes the version. An untouched current object can remain stored for about two configured periods plus lifecycle processing, not a strict creation-to-deletion maximum of one period.

The integration PR must cover current and noncurrent versions and prevent the general 30-day rule from also matching BCDR records. Shorter overlapping expiry wins, and current-version expiry does not preserve an overwritten version. Keep the required originals/provenance available through the agreed retention or approved archive before program-end teardown. A 100-day rule is a lifecycle eligibility window, not a guarantee of deletion at an exact instant.

S3 references: https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-conflicts.html and https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html .

## Remaining evidence and PR record

| Item | Status |
| --- | --- |
| Five questions | Answered here at source/design level; the Internal Auditor assesses completeness and outstanding evidence |
| RTO/RPO owner acceptance and component allocation | Not independently verified |
| Backup cadence and schedule-frequency exception | Twice-daily proposal documented in TIMING-DESIGN.md; no schedule change or owner exception recorded |
| Actual operational approver and effective separation | Not independently verified |
| Detection coverage and proposed deferrals | Readiness evidence / scope decisions outstanding |
| Program budget, inherited scanning and actual test spend | Outstanding |
| Package-local build/tests/lint | See LOCAL-CHECKS.md; distinct from current-repository and live AWS checks |
| Engineering code review | Changes requested on the template at 5e7565c; Python source, tests and docs were explicitly outside that review's scope. Corrections require re-review |
| AWS template validation | The code reviewer reported validate-template OK with CAPABILITY_NAMED_IAM at 5e7565c; changed template requires fresh validation |
| Threat model location | Required on issue #41; preparation in a PR or local draft does not satisfy posting it there |
| Final report item | [#111](https://github.com/340Collective/GRC-Projects/issues/111), plan ID 13-final; link this item without closing it in the build PR |
| Completion sign-off / validation / final approval | Not supplied; this is not a completion PR |

AI assistance: ChatGPT/Codex assisted with source, template, tests, documentation and corrections. Current AGENTS/CONTRIBUTING/GOVERNANCE/SECURITY and the actual PR head have been read. Check results belong in the PR description. The agent ran no AWS commands. Attribute the reviewer's successful validation to its exact reviewed commit; do not extend it to this changed template. Effective IAM, live tests and operating outcomes remain unverified.
