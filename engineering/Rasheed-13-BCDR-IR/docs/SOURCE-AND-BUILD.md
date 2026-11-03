# Project 13 BCDR and IR supporting source

Updated 3 November 2026. Current build review: [PR #176](https://github.com/340Collective/GRC-Projects/pull/176). [PR #171](https://github.com/340Collective/GRC-Projects/pull/171) was closed without merging. Earlier wording calling it approved and merged is superseded. The current build PR and repository rules were read on 3 November. Operating results remain unverified.

This is a build/source PR, not the PR that finishes Project 13. Keep FINAL-REPORT.md as a separate draft until the completing PR has actual results and the required review records. Handover is no longer a project requirement.

## Repository layout

One deployment template belongs at the repository root:

`infrastructure/cloudformation/grc-bcdr.yaml`

All supporting files in this package belong under:

`engineering/Rasheed-13-BCDR-IR/`

The renderer derives the repository root from its own location and writes only the canonical template above, regardless of the working directory. It refuses the former standalone folder layout. Do not retain another template at `engineering/Rasheed-13-BCDR-IR/infrastructure/cloudformation/grc-bcdr.yaml`.

The template's generated header points to the actual source and this README. The review correction sets UpdateReplacePolicy to Delete for the six buckets/tables/vault and adds lifecycle expiry for current/noncurrent report and IR objects, plus incomplete-upload cleanup. EvidenceRetentionDays is required with no default: supply an approved duration, not a placeholder or an assumed 100-day approval. Record any exception to GOVERNANCE's general 30-day evidence rule in the implementing PR. The prior Lambda validator correction uses one completion instant for elapsed RTO and the recorded timestamp after all checks; use the runtime bundle built from that corrected source. This template correction does not change runtime source. See [the timing recommendation and decision](TIMING-DESIGN.md). No approval or deployment is implied.

## Reproduce from the repository root

Use the repository's current AGENTS and CONTRIBUTING instructions. The commands below describe package-local build checks, not a substitute for the required repository checks. Installing tools needs package-download access and the existing dependency rules.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r engineering/Rasheed-13-BCDR-IR/requirements.txt
.venv/bin/python engineering/Rasheed-13-BCDR-IR/tools/render_template.py
.venv/bin/python engineering/Rasheed-13-BCDR-IR/tools/build.py
PYTHONPATH=engineering/Rasheed-13-BCDR-IR/src .venv/bin/python -m unittest discover -s engineering/Rasheed-13-BCDR-IR/tests -v
.venv/bin/cfn-lint infrastructure/cloudformation/grc-bcdr.yaml
wc -c infrastructure/cloudformation/grc-bcdr.yaml
sha256sum infrastructure/cloudformation/grc-bcdr.yaml
```

On Windows use `py -m venv .venv` and `.venv/Scripts/python.exe`; set `$env:PYTHONPATH = 'engineering/Rasheed-13-BCDR-IR/src'` in PowerShell. Use `Get-FileHash` for SHA256. Preserve the repository's required commit sign-off and staged-by-name process.

The deterministic Lambda artifact is generated locally at `engineering/Rasheed-13-BCDR-IR/dist/grc-bcdr-lambda.zip`. Its SHA256 and content-addressed S3 key are written beside it in `dist/lambda-artifact.json`. The ZIP contains `bcdr/` at its root and is used by the four separately permissioned Lambda functions. Runtime boto3 is AWS-provided; pinned boto3 is for the local operator/tests. Do not commit private files or treat generated artifacts as operating evidence.

## Code artifact and deployment

When an upload is needed, the authorized engineer uses the existing approved, versioned code bucket and shared CMK through the normal project process. Privately record the artifact digest and exact non-null S3 object version; supply CodeS3Bucket, CodeS3Key and CodeS3ObjectVersion. No upload or AWS update was performed here.

Deploy only after the actual review/approval and merge, from clean main equal to origin/main with the engineer seat and stack name grc-bcdr. Tag the deployed commit as required. A closed PR or a locally generated template does not establish deployment. Keep the installed stack running after sign-off; remove temporary restored targets after each test and the stack only at authorized program-end teardown.

Before enabling runtime, privately confirm the existing Jira connection/webhook, the approved shared key and its effective permissions for the component roles and AWS Backup, the versioned artifact bucket/object, independent approver and alarm destination, accepted recovery targets and evidence retention. These deployment inputs are not established by source review. The existing 15-minute cleanup monitor and any twice-daily backup proposal require the ISSM's frequency/cost decision; neither is silently accepted here.

Delete replacement policy avoids deliberately retaining old resources; it does not enable replacement under an unchanged fixed name. Review replacement-requiring updates as migrations with a new name and preserved evidence. Empty all project object versions/delete markers and recovery points before authorized removal; the policy does not empty buckets or the vault. Current expiry creates a delete marker, while noncurrent expiry permanently deletes a version. Their age clocks differ: an untouched current object can remain stored for up to roughly two configured periods before permanent deletion, plus asynchronous lifecycle processing. Before applying lifecycle to existing data, check version ages and preserve any originals needed beyond their window.

## Review and integration

Read [the five-question requirements response](REQUIREMENTS-REVIEW-RESPONSE.md), [the timing recommendation](TIMING-DESIGN.md), [the recovery/IR plan](PLAN.md), [the historical local checks](LOCAL-CHECKS.md), and [the integration plan](CONTINUE-BUILD.md). Targets, cadence exceptions, effective access, detection readiness, program budget and live tests must be reported with their actual status.

The 06 receiver is planned for integration week, 23-25 November. Decisions are requested by 20 November. Until the receiver exists and is configured, leave EvidenceBusArn empty. Leave RiskBusArn empty until its receiving interface is ready. The local prepare_06.py tool is a reference-index preparation aid, not event delivery or backfill.

All fixture/sample data is synthetic. Any sample email uses example.com. No production or raw operating evidence is included.
