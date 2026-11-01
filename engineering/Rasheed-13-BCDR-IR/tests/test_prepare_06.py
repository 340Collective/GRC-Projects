"""Offline evidence staging, deliberately separate from delivery and source verification."""
import contextlib
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import prepare_06


def bundle():
    # Entirely synthetic metadata. No S3 object is asserted to exist.
    run = 'a' * 24
    return {'report_bucket': 'grc-synthetic-reports', 'records': [{
        'run_id': run, 'kind': 'dynamodb', 'finalized': True,
        'cleanup_status': 'DELETED', 'overall_result': 'PASS',
        'report_key': 'dr-tests/2026/Q4/dynamodb/' + run + '.json',
        'report_version': 'synthetic-version', 'report_sha256': 'b' * 64,
        'source_arn': 'PRIVATE_VALUE_MUST_NOT_BE_COPIED',
        'record_content': {'email': 'synthetic@example.com'}}]}


class ReferenceIndexTests(unittest.TestCase):
    def test_offline_output_is_allowlisted_and_never_claims_delivery_or_verification(self):
        with patch.dict('sys.modules', {'boto3': None}), patch('socket.socket', side_effect=AssertionError('NetworkForbidden')):
            result = prepare_06.build_index(bundle())
        text = json.dumps(result)
        self.assertNotIn('PRIVATE_VALUE_MUST_NOT_BE_COPIED', text)
        self.assertNotIn('synthetic@example.com', text)
        self.assertEqual('NOT_ATTEMPTED', result['delivery'])
        self.assertEqual('REQUIRES_VERSIONED_READ', result['source_content_verification'])
        self.assertEqual('synthetic-version', result['records'][0]['evidence']['version'])
        sha = result.pop('index_sha256')
        self.assertEqual(sha, prepare_06.digest(result))

    def test_failures_and_s3_results_are_kept(self):
        value = bundle()
        second = deepcopy(value['records'][0])
        second.update(run_id='c' * 24, kind='s3', overall_result='FAIL',
                      report_key='dr-tests/2026/Q4/s3/' + 'c' * 24 + '.json')
        value['records'].append(second)
        rows = prepare_06.build_index(value)['records']
        self.assertEqual(['PASS', 'FAIL'], [r['result'] for r in rows])
        self.assertEqual('s3', rows[1]['resource_type'])

    def test_deduplication_and_order_are_deterministic(self):
        value = bundle()
        one = prepare_06.build_index(value)
        value['records'].append(deepcopy(value['records'][0]))
        self.assertEqual(one, prepare_06.build_index(value))
        value['ir'] = [{'stored_evidence': {
            'bucket': value['report_bucket'], 'key': 'ir/runbook-executions/2026/11/01/example.json',
            'version': 'synthetic-ir-version', 'sha256': 'd' * 64}}]
        value['tabletop'] = {'bucket': value['report_bucket'], 'key': 'ir/tabletop/2026/11/01/example.json',
                            'version': 'synthetic-tabletop-version', 'sha256': 'e' * 64}
        expected = prepare_06.build_index(value)
        value['records'].reverse()
        self.assertEqual(expected, prepare_06.build_index(value))
        self.assertEqual(3, len(expected['records']))
        self.assertEqual('NOT_ASSESSED_BY_THIS_TOOL', expected['records'][1]['signoff_status'])

    def test_conflicting_versions_or_results_are_rejected(self):
        for field, changed in [('report_version', 'different'), ('overall_result', 'FAIL')]:
            with self.subTest(field=field):
                value = bundle()
                other = deepcopy(value['records'][0])
                other[field] = changed
                value['records'].append(other)
                with self.assertRaisesRegex(ValueError, 'Conflicting'):
                    prepare_06.build_index(value)

    def test_unfinalized_unclean_or_malformed_results_are_rejected(self):
        for field, bad in [('finalized', False), ('finalized', 1), ('cleanup_status', 'PENDING'),
                           ('cleanup_status', []), ('overall_result', 'RUNNING'), ('overall_result', []),
                           ('kind', []), ('run_id', '../unsafe')]:
            with self.subTest(field=field, bad=bad):
                value = bundle()
                value['records'][0][field] = bad
                with self.assertRaises(ValueError):
                    prepare_06.build_index(value)

    def test_missing_version_hash_and_traversal_are_rejected(self):
        for field, bad in [('report_version', None), ('report_version', 'null'), ('report_version', ' '),
                           ('report_sha256', 'bad'), ('report_key', '../evidence.json'),
                           ('report_key', 'dr-tests/2026/Q5/dynamodb/' + 'a' * 24 + '.json')]:
            with self.subTest(field=field, bad=bad):
                value = bundle()
                value['records'][0][field] = bad
                with self.assertRaises(ValueError):
                    prepare_06.build_index(value)

    def test_legacy_input_requires_explicit_bucket_and_rejects_conflicts(self):
        value = bundle()
        with self.assertRaisesRegex(ValueError, 'Mismatch'):
            prepare_06.build_index(value, 'grc-other-reports')
        del value['report_bucket']
        with self.assertRaisesRegex(ValueError, 'BucketRequired'):
            prepare_06.build_index(value)
        self.assertEqual('grc-synthetic-reports', prepare_06.build_index(value, 'grc-synthetic-reports')['records'][0]['evidence']['bucket'])

    def test_ir_receipts_require_expected_bucket_category_date_version_and_hash(self):
        receipt = {'bucket': 'grc-synthetic-reports', 'key': 'ir/runbook-executions/2026/11/01/example.json',
                   'version': 'synthetic-version', 'sha256': 'd' * 64}
        for field, bad in [('bucket', 'grc-other-reports'), ('version', 'null'), ('sha256', 'bad'),
                           ('key', 'ir/tabletop/2026/11/01/example.json'),
                           ('key', 'ir/runbook-executions/2026/02/31/example.json')]:
            with self.subTest(field=field):
                value = bundle()
                value['ir'] = [{'stored_evidence': {**receipt, field: bad}}]
                with self.assertRaises(ValueError):
                    prepare_06.build_index(value)

    def test_empty_or_invalid_bundle_is_rejected(self):
        for value in [[], {}, {'report_bucket': 'grc-synthetic-reports'},
                      {**bundle(), 'records': None}, {**bundle(), 'ir': None},
                      {**bundle(), 'tabletop': 'unknown'}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                prepare_06.build_index(value)

    def test_cli_writes_only_given_output_privately_and_refuses_input_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / 'input.json', root / 'output.json'
            source.write_text(json.dumps(bundle()))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, prepare_06.main(['--input', str(source), '--output', str(output)]))
            self.assertEqual({'input.json', 'output.json'}, {p.name for p in root.iterdir()})
            self.assertEqual(bundle(), json.loads(source.read_text()))
            if os.name != 'nt':
                self.assertEqual(0o600, output.stat().st_mode & 0o777)
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                prepare_06.main(['--input', str(source), '--output', str(source)])

    def test_invalid_input_never_creates_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source, output = Path(directory) / 'input.json', Path(directory) / 'output.json'
            source.write_text('{')
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                prepare_06.main(['--input', str(source), '--output', str(output)])
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
