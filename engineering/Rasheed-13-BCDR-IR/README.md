# Project 13 supporting source for the submitted YAML

Supporting build updated 1 November 2026. Prepared locally; no AWS deployment, GitHub submission or Jira action was performed here. The engineer reports that Faris approved and merged the YAML in [PR #171](https://github.com/340Collective/GRC-Projects/pull/171), and that the build was completed last week. This package does not establish the current live stack configuration.

The generator reproduces the supplied, approved-baseline 47,859-byte YAML unchanged: SHA256 `8fa908c21bea6aba037ca261b4e61c3b86528742b2e29b2bc490ffa9e6787c23`. The current remote PR contents were not independently retrieved. The Lambda runtime source and reproducible ZIP also remain unchanged.

The separate, newer complete package includes a report-bucket name change and incomplete multipart-upload cleanup. Those two settings are deliberately absent here so that this generator reproduces the submitted baseline. Do not mix the two generators or claim their YAML files are identical.

Start with [continue the BCDR build](docs/CONTINUE-BUILD.md) and [the recovery and IR plan](docs/PLAN.md). See [local check output](docs/LOCAL-CHECKS.md). The [25 October review response](docs/REQUIREMENTS-REVIEW-RESPONSE.md) is historical context, not a current approval checklist. Handover is no longer a project requirement.

## Supporting source for a follow-up PR

The template alone does not include the Lambda implementation. Include `src/bcdr/`, `tools/build.py`, `tools/render_template.py`, the relevant tests, `requirements.txt`, and these instructions in repository locations allowed by its current AGENTS and CONTRIBUTING instructions. Include `manage.py`, `evidence.py` and `prepare_06.py` if using the supplied operator/evidence tooling. Keep the required infrastructure path and existing stack ownership.

Adapt paths to the agreed repository layout and update the generator's root only if necessary. If paths change, run the generator and tests again. Use a feature branch and a follow-up PR for supporting-source changes because #171 is already merged. The final report should continue to identify only what was actually submitted; this package has not been submitted by preparing it here.

## Reproduce locally

Run from this package root. Installing the pinned review tools needs package-download access and any repository-required dependency approval. Building and these mocked tests make no AWS calls.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/render_template.py
.venv/bin/python tools/build.py
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/cfn-lint infrastructure/cloudformation/grc-bcdr.yaml
wc -c infrastructure/cloudformation/grc-bcdr.yaml
sha256sum infrastructure/cloudformation/grc-bcdr.yaml
```

On Windows use `py -m venv .venv`, `.venv\Scripts\python.exe` and `.venv\Scripts\cfn-lint.exe`; set `$env:PYTHONPATH = 'src'` in PowerShell. Use `Get-FileHash` for SHA256. Set only the task-specific environment variable shown here.

`tools/build.py` puts the `bcdr/` Python package at the ZIP root. Its deterministic output is `dist/grc-bcdr-lambda.zip`; `dist/lambda-artifact.json` records the SHA256, content-addressed S3 key and runtime. All four Lambda functions reference this code artifact, with separate handlers and roles. Boto3 is supplied by the Lambda runtime; the pinned boto3 requirement is for the local tools/tests.

## S3 code artifact upload

When an artifact upload is needed, the authorized engineer uses the existing approved, versioned code bucket and approved shared CMK through the normal project deployment process. If the installed stack already uses this exact ZIP and pinned version, do not redeploy it just to use the new local helpers. No upload is performed by this package preparation.

Privately record the artifact SHA256, bucket, content-addressed key and returned non-null object VersionId. Supply those as `CodeS3Bucket`, `CodeS3Key` and `CodeS3ObjectVersion`. Verify the uploaded bytes match the recorded SHA256. Keep this code object version available throughout operation and the accepted retention period. Do not publish account details, actual ARNs, private parameter files or credentials in Git.

The template defaults `EnableRuntimeResources` to `false`; it does not package or upload its own code. Live deployment also requires the approved CMK/boundary, target approval reference, independent IR approver, subscribed alarm topic and existing Jira connection/webhook. The optional 06/07 routes need their agreed receivers and configuration before delivery can be demonstrated.

Deploy only from the approved clean `main` equal to `origin/main`, using the engineer seat and the literal stack name `grc-bcdr`. Keep the installed system running after sign-off; clean temporary restored copies after every test. End-of-program teardown is a separate authorized operation.
