# Project 13 integration plan with Project 06

Updated 3 November 2026 from the team comments. This is a plan, not a deployed connection. Keep the current path/PR corrections and requested source-bucket lifecycle cleanup in build PR #176. Receiver, access, accepted mapping and receiving-lake retention belong to the separate integration PR.

| Decision / work | Current position |
| --- | --- |
| Build review | #176 is the current engineering build PR; #171 was closed without merging |
| Receiver | the code reviewer proposes a same-account, us-east-1 custom grc-* intake bus and a receiver Lambda in the 06 stack. Actual bus/role values are shared privately after deployment |
| Event types | Source grc.bcdr; BCDR Test Result and BCDR Evidence Record; detail schema 1.1 |
| Source access | Narrow s3:GetObjectVersion on agreed dr-tests/ and ir/ objects, plus kms:Decrypt on the actual report key. Shared-key policy/grants and boundary must permit the receiver role; no broad grants are proposed here |
| Event delivery | Existing conditional BCDR forwarding role already scopes events:PutEvents to EvidenceBusArn. Verify effective access after the real bus is configured |
| Mapping | the code reviewer's proposed CP-9/CP-10, CP-4 and IR-3/IR-4 mappings remain proposals for the ISSO and the Internal Auditor; include agreed IDs/crosswalks in the implementing PR |
| Retention | About 100 days scoped to BCDR evidence is agreed in principle for planning. Formal approval attaches to the lifecycle implementation PR; existing general 06 retention remains unchanged now |
| Source report retention | Build correction requires an approved EvidenceRetentionDays input for current/noncurrent report and IR versions, on their separate age clocks, and aborts incomplete uploads after one day. No default duration is selected; any exception to the general 30-day rule and any program-end archive/disposition must be approved |
| Planning checkpoint | 20 November: agreed mapping, retention implementation plan and source read/decrypt access |
| Integration window | 23-25 November, after 06 prerequisites/sign-off are actually satisfied |

## Retention detail for the integration PR

A new 100-day prefix rule does not override a 30-day rule that also matches those objects. Separate the matching scopes, using the agreed prefix/tag design. Include noncurrent-version handling: the event-pinned report can become noncurrent immediately because the sender writes a later final version. A current-only expiry setting does not protect that original version.

Specify retention for originals, normalized copies and provenance. Keep their required exact versions readable through the agreed period and demonstration. Confirm disposition or approved archive if program teardown occurs earlier. This is not Vault Lock or Object Lock and does not change backup recovery-point retention.

## Receiver behavior and done criteria

Read the exact pointer and version, verify stored-byte SHA256, reject missing objects or mismatches, sanitize only after original verification, preserve source digest as provenance and compute a new digest for sanitized bytes. Retain failures/late results, scope, service_recovery and signoff_status; null timing remains null. Deduplicate event_id and reject conflicting pointers.

The sender now persists each DR/IR event envelope before delivery and reuses it on retries or concurrent attempts, so the same event ID retains the same pointer. Offline fault tests cover this sender behavior; they do not prove receiver deployment or persistence. Historical events created before this correction require reconciliation before replay because their original envelopes were not saved.

Demonstrate success, forced failure, duplicate delivery, missing/bad-hash rejection and retained evidence lookup. Passing synthetic parser tests or PutEvents acceptance alone is not a completed integration.

Leave EvidenceBusArn empty until the receiver is ready. Continue standalone tests and retain results in Project 13 meanwhile. The prepare_06.py tool prepares private references only and is not an importer or event replay. The sender schema and synthetic examples are separately available in the BCDR-06 interface document; no real deployment values belong in Git.

## Local operator use

From engineering/Rasheed-13-BCDR-IR, the existing manage.py check/status actions are read-only AWS checks. prepare/exercise/collect require --execute and approved private inputs. The optional status command is not a handover gate. The running example disables fault injection; only the explicit synthetic failure exercise uses it.

After an actual collect, prepare references locally with:

```bash
python3 prepare_06.py --input private/collected-evidence.json --output private/project06-references.json
```

Keep private state/evidence/indexes outside Git. A reference index verifies structure, not source object bytes or 06 delivery. Keep the installed system running after sign-off; test cleanup and authorized program-end teardown remain separate.
