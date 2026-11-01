# Local check record for the supporting build

1 November 2026. Package-local checks outside the actual GitHub checkout. AWS/HTTP responses in tests are mocked; no deployment, event delivery or repository submission was performed.

## Executed

Commands below use an activated equivalent of the isolated review environment: Python 3.12.14, boto3 1.43.24 and cfn-lint 1.57.2. Actual execution used the environment's absolute Python/cfn-lint paths. Target Lambda runtime Python 3.13 was not exercised here.

```text
$ python tools/render_template.py
infrastructure/cloudformation/grc-bcdr.yaml: 47859 bytes

$ PYTHONPATH=src python -m unittest discover -s tests -v
----------------------------------------------------------------------
Ran 103 tests in 0.327s

OK

$ cfn-lint infrastructure/cloudformation/grc-bcdr.yaml
[no output; exit 0]

$ wc -c infrastructure/cloudformation/grc-bcdr.yaml
47859 infrastructure/cloudformation/grc-bcdr.yaml

$ sha256sum infrastructure/cloudformation/grc-bcdr.yaml
8fa908c21bea6aba037ca261b4e61c3b86528742b2e29b2bc490ffa9e6787c23

$ python tools/build.py
{
  "file": "grc-bcdr-lambda.zip",
  "sha256": "9892dc6efb43f8afef672f320fc9104f8d6c8c70352a5c306d6e8921a3565eae",
  "s3_key": "grc-bcdr/9892dc6efb43f8afef672f320fc9104f8d6c8c70352a5c306d6e8921a3565eae.zip",
  "runtime": "python3.13",
  "runtime_dependency": "AWS-provided boto3"
}
```

The 90-test baseline also passed before editing. The current 103 tests retain those recovery/operator checks and add offline evidence-index validation plus collection-to-index coverage. Two operator tests now check optional `status` rather than the removed handover command. See [full unittest output](unittest-output.txt).

Additional package-local checks: 21 Python files parsed with `ast.parse`; all JSON parsed; no broken relative Markdown file links; preserved YAML/ZIP fingerprints; Lambda ZIP CRC clean. New/updated implementation files and the continuation guide contain no em or en dashes. These are local checks, not the repository's policy scripts.

Both the approved-baseline YAML and deterministic Lambda ZIP match their earlier supplied bytes. Only local operator/supporting documentation, the running example and offline staging support changed. No new AWS resource or runtime dependency was added. Handover is not a project requirement.

## Not run or not established

- Current repository git fetch/diff/status, AGENTS compliance, repository filename/secrets/identifier policy checks, shared/check_links.py and repository-wide infrastructure checks. No live Git checkout was available.
- AWS CloudFormation validate-template, repository validate_policies.py --skip-aws and effective IAM/KMS/boundary checks.
- Actual AWS restores, achieved RTO/RPO, cleanup, source retention, detection coverage, IR/tabletop execution, Jira and 06/07 persistence/replay, current shared-budget spend or human sign-offs.
- Current remote PR contents or live stack state. Approval/merge of #171 and last week's build are engineer-provided facts.

The offline reference index validates pointers, not the contents of S3 objects. It does not deliver or replay events and does not complete integration. Run the existing required repository checks on the actual supporting-source PR; report only results and approvals that exist.

