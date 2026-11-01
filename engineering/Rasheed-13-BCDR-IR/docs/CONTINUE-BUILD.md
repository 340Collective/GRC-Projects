# Continue Project 13 while 06 and 07 are being built

Prepared 1 November 2026. Local source preparation, not new operating evidence.

**Recommendation:** continue standalone restore, validation, cleanup and reporting work. Keep `EvidenceBusArn` and `RiskBusArn` empty until their receivers are ready. Retain Project 13's own versioned reports. Maria's packaging fixes do not require a BCDR sender change unless the integration interface changes.

**Trade-off:** component results remain available in Project 13; automated 06 evidence indexing and 07 risk updates remain untested. Do not report the full cross-project automation flow as complete yet.

**Decision needed when connecting:** agree the receiving custom event bus, consumer owner, allowed fields/control mapping, source read/decrypt access and evidence retention. Use the existing review process. No new handover gate is introduced.

## What is built here

- The approved-baseline YAML and Lambda runtime are preserved byte for byte.
- Source, generator, deterministic Lambda ZIP and local test suite are included.
- `manage.py collect` now also saves private `collected-evidence.json` beside its state file after collection succeeds.
- `prepare_06.py` creates a private, deterministic reference index from that file without AWS or network calls. It rejects incomplete/conflicting references and keeps failed test results.
- `manage.py status` is an optional read-only running-configuration check. It replaces the former handover command and does not require collected evidence or a handover approval.
- The running parameter example disables fault injection. The exercise example permits the deliberately forced failure; turn that flag off again afterward through the normal reviewed update.

## Use the supporting build

Run the reproducible build, tests and lint in [README.md](../README.md). Follow the repository's current AGENTS/CONTRIBUTING rules when placing this source in a feature branch. No live deployment or source PR was performed here.

If the stack is already running, start by checking its actual artifact and configuration privately. Do not assume a merged template proves that runtime resources or tests ran. Only upload or deploy if the current stack needs it, using the existing clean-main deployment process.

The existing operator actions `check`, `prepare`, `exercise` and `collect` use AWS. Writes require `--execute`; `check` and `status` are read-only. Supply your own private profile, approved targets and deployment inputs. Keep state files and collected evidence outside Git. Jira remains a separate live dependency of this baseline; leaving 06/07 empty does not disable its Jira requirement.

After an actual successful collection, prepare references offline:

```bash
python3 prepare_06.py --input private/collected-evidence.json --output private/project06-references.json
```

For an older collected JSON without `report_bucket`, pass `--report-bucket` privately. The output contains private bucket/key/version references and hashes; keep it outside Git. POSIX files are created with mode 0600. On Windows use a private directory with appropriate ACLs.

This index is a staging aid, not an upload, import adapter or replay of the original events. It validates reference structure and computes an index hash; it cannot prove that referenced S3 bytes still exist or match their recorded hash. A future consumer must read the exact object version and verify it. Keep the source reports until the agreed retention and any later import are confirmed. There is no automatic historical backfill.

## Existing integration contract

| Route | Existing sender contract | Required receiving behavior |
| --- | --- | --- |
| 06 | Source `grc.bcdr`; `BCDR Test Result` and `BCDR Evidence Record`; detail schema `1.1` | Read the exact `evidence.bucket/key/version`, verify `sha256`, normalize allowed fields, retain/index under agreed controls and retention. |
| 07 | Source `grc.bcdr`; `BCDR Finding`; stable `finding_key` and event ID | Deduplicate event IDs and upsert the same finding, including resolution, rather than opening duplicates. |

The optional destination parameters accept a same-account, same-region custom `grc-*` EventBridge bus ARN. Maria's current default-bus rules and evidence bucket alone do not supply that receiver.

The index uses final retained report versions. An original result event points to an earlier report version from the same publication; do not reuse its event ID with the index's final pointer. Actual event consumers must use the pointer carried by the event. A historical importer needs a separate agreed idempotency contract.

Raw Project 13 reports may contain private resource identifiers. If 06 stores a sanitized representation, retain the original digest as provenance and calculate a separate digest for the sanitized object. Do not label the sanitized bytes with the original digest.

Connect and test a successful result, forced failure, exact-version/hash handling, duplicate delivery and retained evidence lookup before marking integration complete. `PutEvents` acceptance alone does not demonstrate 06/07 storage. Maria's other functional findings can stay in her review without holding up standalone BCDR work.

Keep the installed BCDR system running after sign-off. Delete temporary restored targets after each test. Full stack/vault removal remains an end-of-program action. Full website or client-service recovery, current spend and human sign-offs still need their own actual evidence.
