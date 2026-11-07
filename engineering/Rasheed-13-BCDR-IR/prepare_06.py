#!/usr/bin/env python3
"""Prepare a private reference index offline. No AWS calls or event delivery."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def pointer(value, bucket, pattern):
    if not isinstance(value, dict) or value.get('bucket') != bucket:
        raise ValueError('ReportBucketMismatch')
    key, version, sha = (value.get(k) for k in ('key', 'version', 'sha256'))
    if not isinstance(key, str) or not re.fullmatch(pattern, key):
        raise ValueError('UnexpectedEvidenceKey')
    if not isinstance(version, str) or not version.strip() or version == 'null':
        raise ValueError('VersionPinnedEvidenceRequired')
    if not isinstance(sha, str) or not re.fullmatch(r'[a-f0-9]{64}', sha):
        raise ValueError('Sha256Required')
    return {'bucket': bucket, 'key': key, 'version': version, 'sha256': sha}


def build_index(bundle, report_bucket=None):
    if not isinstance(bundle, dict):
        raise ValueError('CollectedEvidenceObjectRequired')
    configured = bundle.get('report_bucket')
    if report_bucket and configured and report_bucket != configured:
        raise ValueError('ReportBucketMismatch')
    bucket = report_bucket or configured
    if (not isinstance(bucket, str) or not 3 <= len(bucket) <= 63
            or not re.fullmatch(r'grc-[a-z0-9][a-z0-9.-]*[a-z0-9]', bucket)
            or any(part in bucket for part in ('..', '.-', '-.'))):
        raise ValueError('GrcReportBucketRequired')
    indexed = {}

    def add(item):
        previous = indexed.get(item['id'])
        if previous is not None and previous != item:
            raise ValueError('ConflictingEvidenceReference')
        indexed[item['id']] = item

    rows = bundle.get('records', [])
    if not isinstance(rows, list):
        raise ValueError('RecordsListRequired')
    for row in rows:
        if (not isinstance(row, dict) or row.get('finalized') is not True
                or row.get('cleanup_status') not in ('DELETED', 'NOT_REQUIRED')):
            raise ValueError('FinalizedCleanedRecordRequired')
        run, kind = row.get('run_id'), row.get('kind')
        if not isinstance(run, str) or not re.fullmatch(r'[a-f0-9]{24}', run) or kind not in ('dynamodb', 's3'):
            raise ValueError('ComponentIdentityRequired')
        result = row.get('overall_result')
        if result not in ('PASS', 'FAIL', 'LATE'):
            raise ValueError('FinalResultRequired')
        receipt = pointer({'bucket': bucket, 'key': row.get('report_key'),
                           'version': row.get('report_version'), 'sha256': row.get('report_sha256')},
                          bucket, r'dr-tests/[0-9]{4}/Q[1-4]/' + kind + '/' + run + r'\.json')
        add({'id': 'dr:' + run, 'record_type': 'dr-test', 'resource_type': kind,
             'result': result, 'cleanup_status': row['cleanup_status'],
             'scope': 'SYNTHETIC_COMPONENT_ONLY', 'evidence': receipt})

    def add_ir(receipt, category):
        safe = pointer(receipt, bucket, r'ir/' + category + r'/[0-9]{4}/[0-9]{2}/[0-9]{2}/[A-Za-z0-9_-]{1,64}\.json')
        try:
            datetime.strptime('/'.join(safe['key'].split('/')[2:5]), '%Y/%m/%d')
        except ValueError as exc:
            raise ValueError('InvalidIrEvidenceDate') from exc
        add({'id': 'ir:' + safe['key'], 'record_type': category,
             'signoff_status': 'NOT_ASSESSED_BY_THIS_TOOL', 'evidence': safe})

    ir = bundle.get('ir', [])
    if not isinstance(ir, list):
        raise ValueError('IrListRequired')
    for entry in ir:
        if not isinstance(entry, dict):
            raise ValueError('IrReceiptRequired')
        add_ir(entry.get('stored_evidence'), 'runbook-executions')
    tabletop = bundle.get('tabletop', 'NOT_PROVIDED')
    if isinstance(tabletop, dict):
        add_ir(tabletop, 'tabletop')
    elif tabletop != 'NOT_PROVIDED':
        raise ValueError('TabletopReceiptRequired')
    if not indexed:
        raise ValueError('NoEvidenceReferences')
    payload = {'schema_version': 'bcdr-reference-index/1', 'purpose': 'REFERENCE_INDEX_ONLY',
               'delivery': 'NOT_ATTEMPTED', 'source_content_verification': 'REQUIRES_VERSIONED_READ',
               'records': [indexed[k] for k in sorted(indexed)]}
    return {**payload, 'index_sha256': digest(payload)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--report-bucket', help='Explicit bucket for older collected files without report_bucket')
    args = parser.parse_args(argv)
    if args.input.resolve() == args.output.resolve() or (
            args.output.exists() and os.path.samefile(args.input, args.output)):
        parser.error('OutputMustDifferFromInput')
    try:
        index = build_index(json.loads(args.input.read_text(encoding='utf-8')), args.report_bucket)
    except (ValueError, OSError) as exc:
        parser.error(str(exc) if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError)
                     else 'UnableToReadCollectedEvidenceJson')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=args.output.parent,
                                         prefix='.bcdr-index-', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(index, stream, indent=2)
            stream.write('\n')
        os.replace(temporary, args.output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print('Private reference index prepared offline. No delivery attempted; source content requires verification.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
