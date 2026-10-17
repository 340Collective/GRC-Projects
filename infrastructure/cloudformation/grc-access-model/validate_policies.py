#!/usr/bin/env python3
"""Validate the IAM policies in cloudformation/grc-access-model.yaml and
cloudformation/grc-internal-auditor.yaml.

Renders every AWS::IAM::ManagedPolicy document to concrete JSON for one
account and region, then runs:
  (a) a size check against the 6,144 character managed policy quota,
  (b) IAM Access Analyzer validate-policy on each document,
  (c) a parity check that every Deny in the permissions boundary is repeated
      byte-identical in the engineer guardrail policies,
  (d) a hygiene scan of both templates, cloudformation/grc-engineer-users.yaml
      (engineer seats, no managed policies), and cloudformation/grc-access-model/
      for email addresses, access key IDs, and em or en dashes,
  (e) an iam simulate-custom-policy scenario matrix (engineer, analyst,
      workload, and, when --auditor is given, the Internal Auditor simulated
      without a permissions boundary). The matrix covers engineer CloudShell
      (allowed with MFA in us-east-1, no VPC environments).

Only read-only, unbilled AWS calls are made: accessanalyzer validate-policy
and iam simulate-custom-policy. Scratch JSON goes to a temp directory that is
deleted on exit.

Usage (needs pyyaml, for example from the cfn-lint venv):
  AWS_PROFILE=340collective AWS_REGION=us-east-1 \
    /tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py \
    --template cloudformation/grc-access-model.yaml \
    --auditor-template cloudformation/grc-internal-auditor.yaml \
    --account-id 570814274897 --region us-east-1 \
    --engineer <EngineerUserName> --analyst <AnalystUserName> \
    [--auditor <InternalAuditorUserName>]

Offline only (sizes, parity, hygiene; no AWS call): add --skip-aws.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

MAX_POLICY_CHARS = 6144
BOUNDARY_ID = "GrcPermissionsBoundary"
ENGINEER_DENY_IDS = ["GrcEngineerGuardrailsPolicy", "GrcEngineerLimitsPolicy"]
ENGINEER_IDS = [
    "GrcEngineerBuildPolicy",
    "GrcEngineerSecurityPolicy",
    "GrcEngineerGuardrailsPolicy",
    "GrcEngineerLimitsPolicy",
    "GrcRequireMfaPolicy",
]
ANALYST_IDS = ["GrcAnalystPolicy", "GrcRequireMfaPolicy"]
# The CloudShell actions the engineer is allowed (Sid CloudShellNoVpc).
CLOUDSHELL_ACTIONS = [
    "CreateEnvironment", "CreateSession", "GetEnvironmentStatus", "StartEnvironment",
    "StopEnvironment", "DeleteEnvironment", "DescribeEnvironments", "PutCredentials",
    "GetFileUploadUrls", "GetFileDownloadUrls",
]
AUDITOR_IDS = ["InternalAuditorReadPolicy", "InternalAuditorGuardrailsPolicy", "GrcRequireMfaPolicy"]
WORKLOAD_POLICY = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}],
}


class CfnLoader(yaml.SafeLoader):
    """SafeLoader that turns CloudFormation short-form tags into long form."""


def _construct_tag(loader, suffix, node):
    name = "Ref" if suffix == "Ref" else "Fn::" + suffix
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node, deep=True)
    else:
        value = loader.construct_mapping(node, deep=True)
    if suffix == "GetAtt" and isinstance(value, str):
        value = value.split(".", 1)
    return {name: value}


CfnLoader.add_multi_constructor("!", _construct_tag)


def resolve(node, ctx):
    """Resolve Fn::Sub and Ref for pseudo parameters and managed policies."""
    if isinstance(node, dict):
        if len(node) == 1:
            key, value = next(iter(node.items()))
            if key == "Fn::Sub":
                if not isinstance(value, str):
                    raise ValueError("only the string form of Fn::Sub is supported")

                def replace(match):
                    expr = match.group(1)
                    if expr.startswith("!"):
                        return "${" + expr[1:] + "}"
                    if expr in ctx["pseudo"]:
                        return ctx["pseudo"][expr]
                    raise ValueError("unresolved ${%s} in Fn::Sub" % expr)

                return re.sub(r"\$\{([^}]+)\}", replace, value)
            if key == "Ref":
                if value in ctx["pseudo"]:
                    return ctx["pseudo"][value]
                if value in ctx["policy_arns"]:
                    return ctx["policy_arns"][value]
                raise ValueError("unresolved Ref %s inside a policy" % value)
        return {k: resolve(v, ctx) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(v, ctx) for v in node]
    return node


def aws(args, scratch, payload=None):
    """Run a read-only AWS CLI call and return parsed JSON output."""
    cmd = ["aws"] + args + ["--output", "json"]
    if payload is not None:
        path = os.path.join(scratch, "cli-input.json")
        with open(path, "w") as handle:
            json.dump(payload, handle)
        cmd += ["--cli-input-json", "file://" + path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("%s failed: %s" % (" ".join(args[:2]), proc.stderr.strip()))
    return json.loads(proc.stdout or "{}")


def load_policies(template_path, account, region):
    with open(template_path) as handle:
        template = yaml.load(handle, Loader=CfnLoader)
    resources = template["Resources"]
    ctx = {
        "pseudo": {
            "AWS::AccountId": account,
            "AWS::Region": region,
            "AWS::Partition": "aws",
        },
        "policy_arns": {},
    }
    for logical_id, res in resources.items():
        if res["Type"] == "AWS::IAM::ManagedPolicy":
            name = res["Properties"]["ManagedPolicyName"]
            ctx["policy_arns"][logical_id] = "arn:aws:iam::%s:policy/%s" % (account, name)
    docs = {}
    for logical_id, res in resources.items():
        if res["Type"] == "AWS::IAM::ManagedPolicy":
            docs[logical_id] = resolve(res["Properties"]["PolicyDocument"], ctx)
    return docs, ctx["policy_arns"]


def check_sizes(docs):
    rows, ok = [], True
    for logical_id, doc in docs.items():
        size = len(json.dumps(doc, separators=(",", ":")))
        passed = size <= MAX_POLICY_CHARS
        ok &= passed
        rows.append((logical_id, size, "pass" if passed else "FAIL"))
    return ok, rows


def check_access_analyzer(docs, scratch):
    rows, ok = [], True
    for logical_id, doc in docs.items():
        path = os.path.join(scratch, logical_id + ".json")
        with open(path, "w") as handle:
            json.dump(doc, handle, indent=2)
        result = aws(
            [
                "accessanalyzer",
                "validate-policy",
                "--policy-type",
                "IDENTITY_POLICY",
                "--policy-document",
                "file://" + path,
            ],
            scratch,
        )
        findings = result.get("findings", [])
        blocking = [f for f in findings if f["findingType"] in ("ERROR", "SECURITY_WARNING")]
        ok &= not blocking
        summary = ", ".join(
            "%s %s" % (f["findingType"], f["issueCode"]) for f in findings
        ) or "none"
        rows.append((logical_id, len(findings), summary, "FAIL" if blocking else "pass"))
        for f in findings:
            print("  %s %s %s: %s" % (logical_id, f["findingType"], f["issueCode"], f["findingDetails"]))
    return ok, rows


def check_parity(docs):
    rows, ok = [], True
    mirrored = {}
    for logical_id in ENGINEER_DENY_IDS:
        for stmt in docs[logical_id]["Statement"]:
            mirrored[stmt["Sid"]] = stmt
    for stmt in docs[BOUNDARY_ID]["Statement"]:
        if stmt["Effect"] != "Deny":
            continue
        other = mirrored.get(stmt["Sid"])
        passed = other is not None and json.dumps(other, sort_keys=True) == json.dumps(stmt, sort_keys=True)
        ok &= passed
        rows.append((stmt["Sid"], "identical" if passed else "MISSING OR DIFFERENT"))
    return ok, rows


def check_hygiene(repo_root):
    # \x40 is the at sign, escaped so this file holds no address-like text.
    email = re.compile(r"[A-Za-z0-9._%+-]+\x40[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    access_key = re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")
    dashes = re.compile("[\u2013\u2014]")
    # 340collective-website layout: cloudformation/grc-access-model.yaml,
    # cloudformation/grc-internal-auditor.yaml,
    # cloudformation/grc-engineer-users.yaml (engineer seats), plus
    # cloudformation/grc-access-model/ (this README and validator).
    paths = [
        os.path.join(repo_root, "cloudformation", "grc-access-model.yaml"),
        os.path.join(repo_root, "cloudformation", "grc-internal-auditor.yaml"),
        os.path.join(repo_root, "cloudformation", "grc-engineer-users.yaml"),
    ]
    model_dir = os.path.join(repo_root, "cloudformation", "grc-access-model")
    paths += sorted(os.path.join(model_dir, n) for n in os.listdir(model_dir))
    rows, ok = [], True
    for path in paths:
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        hits = []
        if email.search(text):
            hits.append("email address")
        if access_key.search(text):
            hits.append("access key id")
        if dashes.search(text):
            hits.append("em or en dash")
        ok &= not hits
        rows.append((os.path.relpath(path, repo_root), ", ".join(hits) or "clean"))
    return ok, rows


def auditor_scenarios(account, region, auditor):
    a = account
    iam = "arn:aws:iam::%s:" % a
    lam = "arn:aws:lambda:%s:%s:function:" % (region, a)
    cfn = "arn:aws:cloudformation:%s:%s:stack/" % (region, a)
    ssm = "arn:aws:ssm:%s:%s:parameter/" % (region, a)
    key = "arn:aws:kms:%s:%s:key/abc" % (region, a)
    site = "arn:aws:s3:::340collective-site-%s" % a
    aud_user = iam + "user/" + auditor
    via_s3 = {"kms:ViaService": "s3.%s.amazonaws.com" % region}
    via_ssm = {"kms:ViaService": "ssm.%s.amazonaws.com" % region}
    tagged = {"aws:ResourceTag/grc-project": "x"}
    return [
        ("auditor", "securityhub:GetFindings", "*", {}, "allowed"),
        ("auditor", "iam:GetCredentialReport", "*", {}, "allowed"),
        ("auditor", "s3:GetObject", "arn:aws:s3:::340collective-cloudtrail-%s/AWSLogs/x" % a, {}, "allowed"),
        ("auditor", "s3:GetObject", "arn:aws:s3:::grc-evidence-test/r.csv", {}, "allowed"),
        ("auditor", "iam:CreateAccessKey", aud_user, {}, "allowed"),
        ("auditor", "iam:EnableMFADevice", aud_user, {}, "allowed"),
        ("auditor", "kms:Decrypt", key, dict(tagged, **via_s3), "allowed"),
        ("auditor", "s3:GetObject", site + "/index.html", {}, "explicitDeny"),
        ("auditor", "s3:GetObject", "arn:aws:s3:::340-insider/x", {}, "explicitDeny"),
        ("auditor", "ssm:GetParameter", ssm + "340collective/stripe/x", {}, "explicitDeny"),
        ("auditor", "kms:Decrypt", key, dict(tagged, **via_ssm), "explicitDeny"),
        ("auditor", "kms:Decrypt", key, via_s3, "explicitDeny"),
        ("auditor", "secretsmanager:GetSecretValue", "*", {}, "explicitDeny"),
        ("auditor", "securityhub:BatchUpdateFindings", "*", {}, "explicitDeny"),
        ("auditor", "cloudformation:CreateStack", cfn + "grc-x/y", {}, "explicitDeny"),
        ("auditor", "lambda:InvokeFunction", lam + "collective340-intake", {}, "explicitDeny"),
        ("auditor", "iam:CreateUser", iam + "user/x", {}, "explicitDeny"),
        ("auditor", "iam:AddUserToGroup", iam + "group/Admin", {}, "explicitDeny"),
        ("auditor", "sts:AssumeRole", iam + "role/grc-evidence-lambda", {}, "explicitDeny"),
        ("auditor", "cloudtrail:StopLogging", "arn:aws:cloudtrail:%s:%s:trail/340collective-trail" % (region, a), {}, "explicitDeny"),
        ("auditor", "ssm:StartSession", "*", {}, "explicitDeny"),
        ("auditor", "securityhub:GetFindings", "*", {"aws:MultiFactorAuthPresent": False}, "explicitDeny"),
    ]


def scenarios(account, region, engineer, analyst, boundary_arn, auditor=None):
    a = account
    iam = "arn:aws:iam::%s:" % a
    lam = "arn:aws:lambda:%s:%s:function:" % (region, a)
    ddb = "arn:aws:dynamodb:%s:%s:table/" % (region, a)
    cfn = "arn:aws:cloudformation:%s:%s:stack/" % (region, a)
    ssm = "arn:aws:ssm:%s:%s:parameter/" % (region, a)
    site = "arn:aws:s3:::340collective-site-%s" % a
    pb = {"iam:PermissionsBoundary": boundary_arn}
    eng_user = iam + "user/" + engineer
    ana_user = iam + "user/" + analyst
    # A same-named bucket owned by some other account.
    other = {"aws:ResourceAccount": "111122223333"}
    extra_rows = auditor_scenarios(account, region, auditor) if auditor else []
    # (principal, action, resource, extra context, expected)
    return extra_rows + [
        ("engineer", "cloudformation:CreateStack", cfn + "grc-11-guardrails/x", {}, "allowed"),
        ("engineer", "lambda:CreateFunction", lam + "grc-evidence-collector", {}, "allowed"),
        ("engineer", "iam:CreateRole", iam + "role/grc-evidence-lambda", pb, "allowed"),
        ("engineer", "iam:PassRole", iam + "role/grc-evidence-lambda", {"iam:PassedToService": "lambda.amazonaws.com"}, "allowed"),
        ("engineer", "s3:PutObject", "arn:aws:s3:::grc-evidence-test/a.json", {}, "allowed"),
        ("engineer", "s3:GetObject", "arn:aws:s3:::340collective-cloudtrail-%s/AWSLogs/x" % a, {}, "allowed"),
        ("engineer", "dynamodb:PutItem", ddb + "grc-risk", {}, "allowed"),
        ("engineer", "securityhub:EnableSecurityHub", "*", {}, "allowed"),
        ("engineer", "kms:CreateKey", "*", {"aws:RequestTag/grc-project": "06"}, "allowed"),
        ("engineer", "iam:CreateAccessKey", eng_user, {}, "allowed"),
        ("engineer", "iam:ChangePassword", eng_user, {}, "allowed"),
        ("engineer", "iam:UpdateAssumeRolePolicy", iam + "role/grc-evidence-lambda", {}, "allowed"),
        ("engineer", "s3:CreateBucket", "arn:aws:s3:::grc-evidence-test", {}, "allowed"),
        ("engineer", "cloudformation:CreateStack", cfn + "grc-11-guardrails/x", {"cloudformation:RoleArn": iam + "role/grc-cfn-deploy"}, "allowed"),
        ("engineer", "iam:PassRole", iam + "role/grc-cfn-deploy", {"iam:PassedToService": "cloudformation.amazonaws.com"}, "allowed"),
        ("engineer", "iam:UpdateAssumeRolePolicy", iam + "role/collective340-blog-generator", {}, "explicitDeny"),
        ("engineer", "sts:AssumeRole", iam + "role/grc-evidence-lambda", {}, "explicitDeny"),
        ("engineer", "sts:AssumeRole", iam + "role/collective340-blog-generator", {}, "explicitDeny"),
        ("engineer", "s3:PutObject", "arn:aws:s3:::grc-evidence-test/a.json", other, "denied"),
        ("engineer", "s3:GetObject", "arn:aws:s3:::grc-evidence-test/a.json", other, "denied"),
        ("engineer", "iam:CreateRole", iam + "role/grc-x", {}, "explicitDeny"),
        ("engineer", "iam:CreateRole", iam + "role/grc-x", {"iam:PermissionsBoundary": "arn:aws:iam::aws:policy/AdministratorAccess"}, "explicitDeny"),
        ("engineer", "iam:DeleteRolePermissionsBoundary", iam + "role/grc-x", pb, "explicitDeny"),
        ("engineer", "iam:PutRolePolicy", iam + "role/collective340-blog-generator", {}, "explicitDeny"),
        ("engineer", "iam:AttachRolePolicy", iam + "role/grc-x", dict(pb, **{"iam:PolicyARN": "arn:aws:iam::aws:policy/AdministratorAccess"}), "explicitDeny"),
        ("engineer", "iam:AttachRolePolicy", iam + "role/grc-x", dict(pb, **{"iam:PolicyARN": iam + "policy/grc-engineer-build"}), "explicitDeny"),
        ("engineer", "iam:CreatePolicyVersion", iam + "policy/grc-permissions-boundary", {}, "explicitDeny"),
        ("engineer", "iam:CreatePolicyVersion", iam + "policy/grc-engineer-guardrails", {}, "explicitDeny"),
        ("engineer", "iam:CreatePolicyVersion", iam + "policy/collective340-blog-generator-budget-stop", {}, "explicitDeny"),
        ("engineer", "iam:UpdateAssumeRolePolicy", iam + "role/collective340-intake-IntakeRole-Uk5c9Xxf5zNE", {}, "explicitDeny"),
        ("engineer", "iam:PassRole", iam + "role/collective340-blog-generator", {"iam:PassedToService": "lambda.amazonaws.com"}, "explicitDeny"),
        ("engineer", "iam:DeleteUserPermissionsBoundary", eng_user, {}, "explicitDeny"),
        ("engineer", "iam:AttachUserPolicy", eng_user, {}, "explicitDeny"),
        ("engineer", "iam:CreateAccessKey", iam + "user/kiro", {}, "explicitDeny"),
        ("engineer", "iam:CreateLoginProfile", ana_user, {}, "explicitDeny"),
        ("engineer", "iam:AddUserToGroup", iam + "group/Admin", {}, "explicitDeny"),
        ("engineer", "iam:CreateUser", iam + "user/grc-new", {}, "explicitDeny"),
        ("engineer", "cloudformation:UpdateStack", cfn + "collective340-intake/x", {}, "explicitDeny"),
        ("engineer", "cloudformation:DeleteStack", cfn + "grc-access-model/x", {}, "explicitDeny"),
        ("engineer", "cloudformation:CreateStack", cfn + "grc-x/y", {"cloudformation:RoleArn": iam + "role/collective340-blog-generator"}, "explicitDeny"),
        ("engineer", "lambda:UpdateFunctionCode", lam + "collective340-intake", {}, "explicitDeny"),
        ("engineer", "dynamodb:Scan", ddb + "collective340-invoices", {}, "explicitDeny"),
        ("engineer", "s3:PutObject", site + "/index.html", {}, "explicitDeny"),
        ("engineer", "s3:GetObject", "arn:aws:s3:::340-insider/x", {}, "explicitDeny"),
        ("engineer", "s3:BypassGovernanceRetention", "arn:aws:s3:::grc-evidence-test/a", {}, "explicitDeny"),
        ("engineer", "s3:PutAccountPublicAccessBlock", "*", {}, "explicitDeny"),
        ("engineer", "ssm:GetParameter", ssm + "340collective/stripe/x", {}, "explicitDeny"),
        ("engineer", "ssm:GetParameter", ssm + "340/invoice/x", {}, "explicitDeny"),
        ("engineer", "budgets:ModifyBudget", "arn:aws:budgets::%s:budget/340collective-monthly-5usd" % a, {}, "explicitDeny"),
        ("engineer", "budgets:DeleteBudget", "arn:aws:budgets::%s:budget/grc-projects-monthly" % a, {}, "explicitDeny"),
        ("engineer", "cloudtrail:StopLogging", "arn:aws:cloudtrail:%s:%s:trail/340collective-trail" % (region, a), {}, "explicitDeny"),
        ("engineer", "apigateway:PATCH", "arn:aws:apigateway:%s::/apis/omhmmdi35f" % region, {}, "explicitDeny"),
        ("engineer", "lambda:CreateFunction", "arn:aws:lambda:us-west-2:%s:function:grc-x" % a, {"aws:RequestedRegion": "us-west-2"}, "explicitDeny"),
        ("engineer", "quicksight:CreateAccountSubscription", "*", {}, "explicitDeny"),
        ("engineer", "ec2:RunInstances", "*", {}, "explicitDeny"),
        ("engineer", "rds:CreateDBInstance", "*", {}, "explicitDeny"),
        ("engineer", "organizations:LeaveOrganization", "*", {}, "explicitDeny"),
        ("engineer", "securityhub:EnableOrganizationAdminAccount", "*", {}, "explicitDeny"),
        ("engineer", "lambda:ListFunctions", "*", {"aws:MultiFactorAuthPresent": False}, "explicitDeny"),
        ("engineer", "iam:PassRole", iam + "role/grc-x", {"iam:PassedToService": "ec2.amazonaws.com"}, "denied"),
        ("engineer", "kms:ScheduleKeyDeletion", "arn:aws:kms:%s:%s:key/abc" % (region, a), {}, "denied"),
        ("engineer", "route53:ChangeResourceRecordSets", "*", {}, "denied"),
    ] + [
        ("engineer", "cloudshell:" + name, "*", {}, "allowed") for name in CLOUDSHELL_ACTIONS
    ] + [
        ("engineer", "cloudshell:CreateEnvironment", "*", {"aws:MultiFactorAuthPresent": False}, "explicitDeny"),
        ("engineer", "cloudshell:CreateEnvironment", "*", {"aws:RequestedRegion": "us-west-2"}, "explicitDeny"),
        ("engineer", "cloudshell:ApproveCommand", "*", {}, "denied"),
        ("engineer", "ec2:CreateNetworkInterface", "*", {}, "denied"),
        ("analyst", "cloudshell:CreateEnvironment", "*", {}, "denied"),
        ("analyst", "securityhub:GetFindings", "*", {}, "allowed"),
        ("analyst", "inspector2:CreateFindingsReport", "*", {}, "allowed"),
        ("analyst", "auditmanager:GetEvidenceFoldersByAssessment", "*", {}, "allowed"),
        ("analyst", "config:SelectResourceConfig", "*", {}, "allowed"),
        ("analyst", "guardduty:ListFindings", "*", {}, "allowed"),
        ("analyst", "s3:PutObject", "arn:aws:s3:::grc-evidence-test/r.csv", {}, "allowed"),
        ("analyst", "iam:GetCredentialReport", "*", {}, "allowed"),
        ("analyst", "iam:CreateAccessKey", ana_user, {}, "allowed"),
        ("analyst", "s3:GetObject", site + "/index.html", {}, "explicitDeny"),
        ("analyst", "s3:GetObject", "arn:aws:s3:::340-insider/x", {}, "explicitDeny"),
        ("analyst", "ssm:GetParameter", ssm + "340collective/stripe/x", {}, "explicitDeny"),
        ("analyst", "iam:CreateAccessKey", iam + "user/kiro", {}, "explicitDeny"),
        ("analyst", "lambda:CreateFunction", lam + "grc-x", {}, "explicitDeny"),
        ("analyst", "cloudformation:CreateStack", cfn + "grc-x/y", {}, "explicitDeny"),
        ("analyst", "s3:PutObject", "arn:aws:s3:::grc-other/x", {}, "denied"),
        ("analyst", "s3:PutObject", "arn:aws:s3:::grc-evidence-test/r.csv", other, "denied"),
        ("analyst", "s3:DeleteObject", "arn:aws:s3:::grc-evidence-test/r.csv", {}, "denied"),
        ("analyst", "securityhub:BatchUpdateFindings", "*", {}, "denied"),
        ("analyst", "iam:CreateRole", iam + "role/grc-x", pb, "denied"),
        ("analyst", "securityhub:GetFindings", "*", {"aws:MultiFactorAuthPresent": False}, "explicitDeny"),
        ("workload", "dynamodb:PutItem", ddb + "grc-x", {}, "allowed"),
        ("workload", "s3:PutObject", "arn:aws:s3:::grc-x/y", {}, "allowed"),
        ("workload", "s3:GetObject", site + "/index.html", {}, "explicitDeny"),
        ("workload", "dynamodb:Scan", ddb + "collective340-invoices", {}, "explicitDeny"),
        ("workload", "lambda:InvokeFunction", lam + "collective340-intake", {}, "explicitDeny"),
        ("workload", "ssm:GetParameter", ssm + "340collective/stripe/x", {}, "explicitDeny"),
        ("workload", "sts:AssumeRole", iam + "role/collective340-blog-generator", {}, "explicitDeny"),
        ("workload", "iam:CreateRole", iam + "role/grc-y", {}, "explicitDeny"),
        ("workload", "iam:DeleteRolePermissionsBoundary", iam + "role/grc-x", pb, "denied"),
        ("workload", "iam:PassRole", iam + "role/grc-x", {"iam:PassedToService": "ec2.amazonaws.com"}, "denied"),
        ("workload", "iam:AttachRolePolicy", iam + "role/grc-x", dict(pb, **{"iam:PolicyARN": "arn:aws:iam::aws:policy/AdministratorAccess"}), "explicitDeny"),
        ("workload", "iam:CreateAccessKey", iam + "user/kiro", {}, "denied"),
        ("workload", "iam:CreatePolicyVersion", iam + "policy/grc-permissions-boundary", {}, "explicitDeny"),
        ("workload", "lambda:CreateFunction", "arn:aws:lambda:us-west-2:%s:function:grc-x" % a, {"aws:RequestedRegion": "us-west-2"}, "explicitDeny"),
        ("workload", "iam:CreateUser", iam + "user/x", {}, "denied"),
        ("workload", "budgets:DeleteBudget", "arn:aws:budgets::%s:budget/grc-projects-monthly" % a, {}, "denied"),
        ("workload", "route53:ChangeResourceRecordSets", "*", {}, "denied"),
        ("workload", "cloudfront:UpdateDistribution", "*", {}, "denied"),
        ("workload", "ec2:RunInstances", "*", {}, "denied"),
    ]


def context_entries(extra, username, account):
    # AWS sets aws:ResourceAccount to the resource owner; default to this account.
    values = {
        "aws:MultiFactorAuthPresent": True,
        "aws:RequestedRegion": "us-east-1",
        "aws:ResourceAccount": account,
    }
    if username:
        values["aws:username"] = username
    values.update(extra)
    entries = []
    for key, value in values.items():
        if isinstance(value, bool):
            entries.append({"ContextKeyName": key, "ContextKeyValues": [str(value).lower()], "ContextKeyType": "boolean"})
        else:
            entries.append({"ContextKeyName": key, "ContextKeyValues": [value], "ContextKeyType": "string"})
    return entries


def check_simulation(docs, args, scratch, boundary_arn):
    principals = {
        "engineer": ([json.dumps(docs[i]) for i in ENGINEER_IDS], args.engineer),
        "analyst": ([json.dumps(docs[i]) for i in ANALYST_IDS], args.analyst),
        "workload": ([json.dumps(WORKLOAD_POLICY)], None),
    }
    if args.auditor:
        principals["auditor"] = ([json.dumps(docs[i]) for i in AUDITOR_IDS], args.auditor)
    boundary = [json.dumps(docs[BOUNDARY_ID])]
    rows, ok = [], True
    for principal, action, resource, extra, expected in scenarios(
        args.account_id, args.region, args.engineer, args.analyst, boundary_arn, args.auditor
    ):
        policies, username = principals[principal]
        payload = {
            "PolicyInputList": policies,
            "ActionNames": [action],
            "ResourceArns": [resource],
            "ContextEntries": context_entries(extra, username, args.account_id),
        }
        # The Internal Auditor user has no permissions boundary.
        if principal != "auditor":
            payload["PermissionsBoundaryPolicyInputList"] = boundary
        result = aws(["iam", "simulate-custom-policy"], scratch, payload)
        decision = result["EvaluationResults"][0]["EvalDecision"]
        if expected == "denied":
            passed = decision in ("explicitDeny", "implicitDeny")
        else:
            passed = decision == expected
        ok &= passed
        rows.append((principal, action, resource, expected, decision, "pass" if passed else "FAIL"))
    return ok, rows


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--template", default="cloudformation/grc-access-model.yaml")
    parser.add_argument("--auditor-template", default="cloudformation/grc-internal-auditor.yaml",
                        help="Internal Auditor template (stack grc-internal-auditor)")
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--region", default="us-east-1")
    parser.add_argument("--engineer", required=True, help="engineer IAM user name (EngineerUserName)")
    parser.add_argument("--analyst", required=True, help="analyst IAM user name (AnalystUserName)")
    parser.add_argument("--auditor", help="internal auditor IAM user name (InternalAuditorUserName)")
    parser.add_argument("--skip-aws", action="store_true", help="run only offline checks")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(args.template)))
    docs, policy_arns = load_policies(args.template, args.account_id, args.region)
    auditor_docs, _ = load_policies(args.auditor_template, args.account_id, args.region)
    clash = set(docs) & set(auditor_docs)
    if clash:
        raise ValueError("logical IDs in both templates: %s" % ", ".join(sorted(clash)))
    docs.update(auditor_docs)
    boundary_arn = policy_arns[BOUNDARY_ID]
    scratch = tempfile.mkdtemp(prefix="grc_policies_")
    results = []
    try:
        ok, rows = check_sizes(docs)
        results.append(ok)
        print("## Policy size (limit %d)\n\n%s\n" % (MAX_POLICY_CHARS, table(["Policy", "Chars", "Result"], rows)))
        ok, rows = check_parity(docs)
        results.append(ok)
        print("## Boundary deny parity\n\n%s\n" % table(["Sid", "Result"], rows))
        ok, rows = check_hygiene(repo_root)
        results.append(ok)
        print("## Hygiene\n\n%s\n" % table(["File", "Findings"], rows))
        if not args.skip_aws:
            print("## Access Analyzer validate-policy\n")
            ok, rows = check_access_analyzer(docs, scratch)
            results.append(ok)
            print("\n" + table(["Policy", "Findings", "Detail", "Result"], rows) + "\n")
            ok, rows = check_simulation(docs, args, scratch, boundary_arn)
            results.append(ok)
            passed = sum(1 for r in rows if r[-1] == "pass")
            print("## Simulation matrix (%d of %d pass)\n" % (passed, len(rows)))
            print(table(["Principal", "Action", "Resource", "Expected", "Decision", "Result"], rows) + "\n")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    if all(results):
        print("RESULT: all checks passed")
        return 0
    print("RESULT: one or more checks FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
