"""The renderer must reproduce the deployment template at the reviewed repo path."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
GENERATOR = PROJECT / 'tools/render_template.py'
BASELINE_BODY_SHA256 = '91fb93e2d1ac573ab2d1db8b5c524788c7de2304c3f554311852f5e0590eddb1'


class RepositoryLayoutTests(unittest.TestCase):
    def test_renderer_uses_repository_root_from_either_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            project = repo / 'engineering/Rasheed-13-BCDR-IR'
            (project / 'tools').mkdir(parents=True)
            (project / 'docs').mkdir()
            script = project / 'tools/render_template.py'
            shutil.copyfile(GENERATOR, script)
            target = repo / 'infrastructure/cloudformation/grc-bcdr.yaml'
            for cwd in (repo, project):
                with self.subTest(cwd=cwd):
                    result = subprocess.run([sys.executable, str(script)], cwd=cwd,
                                            capture_output=True, text=True)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertTrue(target.is_file())
                    body = b''.join(line for line in target.read_bytes().splitlines(keepends=True)
                                    if not line.startswith(b'#'))
                    self.assertEqual(BASELINE_BODY_SHA256, hashlib.sha256(body).hexdigest())
                    self.assertEqual([target], list(repo.rglob('*.yaml')))

    def test_renderer_refuses_to_write_from_a_standalone_package_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / 'standalone'
            (package / 'tools').mkdir(parents=True)
            script = package / 'tools/render_template.py'
            shutil.copyfile(GENERATOR, script)
            result = subprocess.run([sys.executable, str(script)], cwd=package,
                                    capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('Place this generator', result.stderr)
            self.assertFalse(list(Path(directory).rglob('*.yaml')))


if __name__ == '__main__':
    unittest.main()
