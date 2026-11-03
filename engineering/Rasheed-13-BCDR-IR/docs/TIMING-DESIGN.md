# Recovery timing: recommendation and decision

Prepared 2 November 2026 for [build PR #176](https://github.com/340Collective/GRC-Projects/pull/176), [project #41](https://github.com/340Collective/GRC-Projects/issues/41) and requirements [#170](https://github.com/340Collective/GRC-Projects/pull/170). Status: engineering recommendation; cadence changes and a frequency exception are not implemented or approved here.

The current build proceeds for review with the existing proposed targets as working assumptions and the daily backup default. Business justification and arbitrary-time service recovery remain unverified. The twice-daily option below is recorded for the normal review process; it is not a prerequisite to submitting the source/path corrections, and no separate consultation is being initiated by this update.

## Recommendation, trade-off and exact decision

Keep the proposed client-data objectives of 4 hours RTO and 24 hours RPO. Keep the website objective of 8 hours RTO and 24 hours RPO separate. Treat the synthetic DynamoDB and S3 exercises as component tests, with the owner's component allocation recorded explicitly. Do not relax a business objective just to match a backup schedule.

Recommend two backups per day for these tiny synthetic sources, with marker refresh before each backup. This provides planning margin for delayed backup availability. It increases backup/fixture operations and retained recovery points, so the incremental estimate and remaining headroom under the program-wide USD 10/month cap must be checked. It does not imply that the whole monthly bill doubles.

The [running-system cost rule](../../../GOVERNANCE.md#running-system-cost) says: "Schedules run at the lowest useful frequency (daily or slower)". A twice-daily proposal needs an explicit, scoped exception through the normal change process. The existing 15-minute cleanup/late-test monitor must also be disclosed and its operational frequency and cost justified; this document does not assume an exception already exists.

**Decision for the normal review record if the cadence changes:** retain or revise the proposed 4h/24h client-data objectives and the separate 8h/24h website objectives based on business impact; accept the component allocation; approve or reject twice-daily synthetic backups and marker refresh as a limited schedule exception, with the existing safety-monitor cadence disclosed, subject to the shared budget check. The Internal Auditor assesses requirements; the ISSM records the owner/change decision and gives final PR approval. Control mapping with the ISSO and Internal Auditor remains a separate integration decision.

## Why the daily default needs attention

| Setting | Current source | Proposed implementation, pending decision |
| --- | --- | --- |
| Synthetic marker refresh, UTC | 02:00 daily | 01:00 and 13:00 daily |
| Backup schedule, UTC | 03:00 daily | 03:00 and 15:00 daily |
| Backup start window | 60 minutes | Unchanged |
| Backup completion window | 180 minutes | Unchanged |
| Quarterly component test | 09:00 UTC, first day of Jan/Apr/Jul/Oct | Unchanged |
| Recovery-point retention | 7 days | Unchanged; separate from audit-evidence retention |

The plan-rule API defines a start window after the scheduled time and a completion window after successful start. For planning, allow 1 + 3 = 4 hours before a scheduled job becomes a usable completed backup. Source: [AWS BackupRuleInput](https://docs.aws.amazon.com/aws-backup/latest/APIReference/API_BackupRuleInput.html).

With the daily defaults, yesterday's 02:00 marker could still be the newest recovered marker just before today's delayed backup completes at 07:00. Its age would approach 29 hours: 24-hour interval + 1-hour marker lead + 4-hour job allowance. This is a counterexample to claiming the daily configuration always demonstrates a 24-hour marker-age RPO. It is not an observed AWS result.

The proposed 12-hour interval gives a conservative planning calculation of 12 + 2 + 4 = 18 hours, leaving 6 hours against the 24-hour objective. The two-hour marker lead allows for the configured one-hour retry age and the fixture function's execution time before backup starts. These calculations assume successful refresh and backup jobs within those allowances. Missed/failed jobs, later source changes or service delays invalidate the estimate and must remain failures/findings. No schedule is a guarantee of achieved RPO.

The latest marker/manifest and the selected recovery point must belong to the same fixture generation. The harness requires a completed backup created after the baseline is ready; otherwise it refuses the test rather than comparing different generations. A manual run between refresh and backup completion may therefore fail preparation. Preserve this check when implementing the cadence; do not refresh a marker to make an old backup look recent.

The 09:00 test follows the morning job's 07:00 planning completion. Its current three-hour workflow timebox ends before the proposed 13:00 refresh. These are controlled component-exercise windows, not proof of arbitrary-time application recovery. S3 periodic backup timing also has service-specific semantics; the recovered marker, not backup completion alone, remains the measurement input. See [AWS S3 backups](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html).

With the current daily settings, a 09:00 scheduled exercise can recover the same day's 02:00 marker, an approximately seven-hour age if that backup completes and validation succeeds. This can satisfy the proposed 24-hour component check for that exercise. It does not resolve the 29-hour planning counterexample at another interruption time or establish a business-approved service objective.

## RTO measurement and test limits

The validator now captures one completion instant after integrity, configuration and recovered-marker checks. Both validated_at and elapsed RTO use that same instant. A regression test advances the mocked clock to catch the former mismatch between the stored completion timestamp and reported elapsed time.

The default one-hour restore polling guard and the three-hour workflow timeout are laboratory operating limits. They are distinct from a proposed four-hour service RTO. A guard/timeout produces a failed or incomplete component test with its reason; it does not establish a four-hour service breach or demonstrate service recovery. The independent cleanup monitor must reconcile any restore that continues after polling or execution stops. Increasing a timer alone does not prove a recovery objective.

## Implementation and verification sequence

1. Submit the current source/path and timestamp corrections in the existing build PR, keeping component scope, provisional targets, daily defaults and the unverified business rationale explicit. Record this cadence option and any future exception/cost decision through the existing review chain. No partner-document edit or control-ID decision is needed to submit the review update. An owner decision is still required before claiming the targets or a frequency exception accepted.
2. After the cadence decision, update BackupSchedule, FixtureSchedule and their descriptions together in tools/render_template.py, regenerate the one canonical repository template and add schedule/ordering regression coverage. Do not update only the rendered YAML or change only the deploy parameter.
3. Run the repository's required local checks and the required human AWS template validation. Engineering review and final approval precede merge. Deployment remains a human action from clean main equal to origin/main.
4. In the approved AWS test, retain marker write/acknowledgement, baseline-ready, backup creation/completion, test-start, validation-completion and cleanup/absence facts. Validate counts/checksums and the recovered marker; compute elapsed component RTO and conservative marker-age RPO against the accepted component targets.
5. Exercise failure, stale/missing backup and timeout handling. Keep failed/incomplete results, prove eventual cleanup and route findings. Report measured component results separately from full website/service recovery. Live execution and partner/validation records are still needed for the completing Final report.

No cadence, target, timeout, IAM permission or lifecycle has been changed by this timing note. The completion-timestamp correction is implemented locally in the supporting Lambda source; deployment and actual performance remain unverified.
