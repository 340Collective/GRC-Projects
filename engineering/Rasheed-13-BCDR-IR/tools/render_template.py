#!/usr/bin/env python3
"""Render native CloudFormation. PyYAML is provided by the pinned cfn-lint tool.

No custom resources, SAM, CDK, account mutations, or AWS calls are used here.
The rendered YAML is the deployment artifact; this generator avoids inconsistent
copies of role boundaries, encryption settings, and environment contracts.
"""
import json
import copy
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
ALIASES = {"Restore": "Controller", "Report": "Controller", "Cleanup": "Janitor", "Monitor": "Janitor"}
ref = lambda name: {"Ref": ALIASES.get(name, name)}
sub = lambda value: {"Fn::Sub": value}
arn = lambda name: {"Fn::GetAtt": [ALIASES.get(name, name), "Arn"]}
choose = lambda condition, yes, no: {"Fn::If": [condition, yes, no]}
tags = [{"Key": "grc-project", "Value": "13"}]
R = {}
P = {}


def parameter(name, description, **kwargs):
    P[name] = {"Type": "String", "Description": description, **kwargs}


def add(name, kind, properties, **extra):
    R[name] = {"Type": kind, "Properties": properties, **extra}


def allow(actions, resources, **extra):
    return {"Effect": "Allow", "Action": actions, "Resource": resources, **extra}


def role(name, suffix, service, statements, condition=None):
    trust = {"Effect": "Allow", "Principal": {"Service": service}, "Action": "sts:AssumeRole"}
    if service != "lambda.amazonaws.com":
        trust["Condition"] = {"StringEquals": {"aws:SourceAccount": ref("AWS::AccountId")}}
    add(name, "AWS::IAM::Role", {"RoleName": sub("${Prefix}-" + suffix), "Tags": tags,
        "PermissionsBoundary": sub("arn:${AWS::Partition}:iam::${AWS::AccountId}:policy/grc-permissions-boundary"),
        "AssumeRolePolicyDocument": {"Version": "2012-10-17", "Statement": [trust]},
        "Policies": [{"PolicyName": "grc-component-access", "PolicyDocument": {"Version": "2012-10-17", "Statement": statements}}]},
        **({"Condition": condition} if condition else {}))


parameter("Prefix", "Unique project prefix. Keep it stable for all runs and teardown.", Default="grc-bcdr", AllowedPattern="grc-[a-z0-9-]{1,12}")
parameter("EnableRuntimeResources", "Enable only for the approved running shared system. Default creates no resources.", Default="false", AllowedValues=["true", "false"])
parameter("EnableScheduledBackups", "Daily periodic backups are required in the running system; disable only for authorized end-of-program teardown.", Default="true", AllowedValues=["true", "false"])
parameter("ExistingKmsKeyArn", "Approved enabled symmetric CMK in this account and us-east-1, tagged grc-project. This stack never creates or deletes it.", AllowedPattern="arn:[a-z-]+:kms:us-east-1:[0-9]{12}:key/[a-f0-9-]+")
parameter("CodeS3Bucket", "Existing grc-* staging bucket in us-east-1.", AllowedPattern="grc-[a-z0-9.-]+")
parameter("CodeS3Key", "Content-addressed key of the packaged Lambda ZIP.", AllowedPattern="grc-bcdr/[a-f0-9]{64}\\.zip")
parameter("CodeS3ObjectVersion", "Pinned S3 object version from the engineer's upload.", MinLength=1)
parameter("TargetApprovalReference", "Project-item reference recording the owner's approved per-resource RTO/RPO.", MinLength=1, MaxLength=200)
parameter("IrApproverArn", "IAM principal authorized to approve sandbox quarantine and release.", AllowedPattern="arn:[a-z-]+:iam::[0-9]{12}:(role|user)/.+")
parameter("AlarmTopicArn", "Existing same-region grc-* SNS topic with a verified operator subscription.", AllowedPattern="arn:[a-z-]+:sns:us-east-1:[0-9]{12}:grc-.+")
for kind in ("DynamoDb", "S3"):
    for target in ("Rto", "Rpo"):
        parameter(kind + target + "Seconds", "Approved " + kind + " " + target.upper() + " target in seconds. No example default is treated as approved.", Type="Number", MinValue=1, MaxValue=31536000)
parameter("BackupSchedule", "Daily periodic backups after the 02:00 UTC fixture refresh. Review cadence against the approved RPO.", Default="cron(0 3 * * ? *)")
parameter("BackupRetentionDays", "Warm retention. No vault lock or cold storage.", Type="Number", Default=7, MinValue=7, MaxValue=35)
parameter("EvidenceRetentionDays", "Approved report/IR lifecycle duration for current and noncurrent versions, on their separate age clocks. No default; record any exception to the general 30-day rule.", Type="Number", MinValue=1)
parameter("MaxRestoreWaitSeconds", "Stop validation polling after this duration; the independent monitor continues cleanup.", Type="Number", Default=3600, MinValue=60, MaxValue=7200)
parameter("EnableFaultInjection", "Permit explicit synthetic validation failure tests.", Default="false", AllowedValues=["true", "false"])
parameter("QuarterlyScheduleState", "Quarterly restore tests of both synthetic resources. Disable only for an approved outage or end-of-program teardown.", Default="ENABLED", AllowedValues=["ENABLED", "DISABLED"])
parameter("FixtureScheduleState", "Daily synthetic-only marker refresh before backup. Disable only for an approved outage or end-of-program teardown.", Default="ENABLED", AllowedValues=["ENABLED", "DISABLED"])
parameter("EndOfProgramTeardown", "Explicitly permits schedules to be stopped for final removal. Never use at Day 7.", Default="false", AllowedValues=["true", "false"])
parameter("ScheduleActiveFrom", "ISO UTC instant when the quarterly obligation starts; required when enabling the schedule.", Default="", AllowedPattern="^$|[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
parameter("QuarterDeadlineHours", "Deadline after the quarterly scheduled start.", Type="Number", Default=24, MinValue=1, MaxValue=168)
parameter("EvidenceBusArn", "Optional project 06 custom grc-* event bus in this account and region. Leave empty until a compatible receiver exists; this is not a bucket ARN.", Default="", AllowedPattern="^$|arn:[a-z-]+:events:us-east-1:[0-9]{12}:event-bus/grc-.+")
parameter("RiskBusArn", "Optional project 07 custom grc-* event bus in this account and region. Leave empty until its receiver exists.", Default="", AllowedPattern="^$|arn:[a-z-]+:events:us-east-1:[0-9]{12}:event-bus/grc-.+")
parameter("JiraConnectionArn", "EXISTING approved EventBridge connection, required for a live exercise. No secret or connection is created by this stack.", Default="", AllowedPattern="^$|arn:[a-z-]+:events:us-east-1:[0-9]{12}:connection/grc-.+")
parameter("JiraWebhookUrl", "Jira Automation incoming webhook URL when a connection is supplied. Keep parameter files private.", Default="https://example.invalid", NoEcho=True, MinLength=1, AllowedPattern="https://[A-Za-z0-9%/?:@&=+$,_.!~*'();-]+")

conditions = {name: {"Fn::And": [{"Condition": "Live"}, {"Fn::Not": [{"Fn::Equals": [ref(param), ""]}]}]} for name, param in
              (("HasEvidence", "EvidenceBusArn"), ("HasRisk", "RiskBusArn"), ("HasJira", "JiraConnectionArn"))}
conditions.update({"Live": {"Fn::Equals": [ref("EnableRuntimeResources"), "true"]},
    "HasSchedule": {"Fn::And": [{"Condition": "Live"}, {"Fn::Equals": [ref("EnableScheduledBackups"), "true"]}]}})
rules = {
    "JiraPair": {"RuleCondition": {"Fn::Not": [{"Fn::Equals": [ref("JiraConnectionArn"), ""]}]}, "Assertions": [{"Assert": {"Fn::Not": [{"Fn::Equals": [ref("JiraWebhookUrl"), "https://example.invalid"]}]}, "AssertDescription": "Supply a real webhook URL when enabling the Jira connection."}]},
    "ScheduleActivation": {"RuleCondition": {"Fn::And": [{"Fn::Equals": [ref("EnableRuntimeResources"), "true"]}, {"Fn::Equals": [ref("QuarterlyScheduleState"), "ENABLED"]}]}, "Assertions": [{"Assert": {"Fn::Not": [{"Fn::Equals": [ref("ScheduleActiveFrom"), ""]}]}, "AssertDescription": "Supply ScheduleActiveFrom when enabling quarterly tests."}]}
}

rules["RunningCadenceRequired"] = {"RuleCondition": {"Fn::And": [{"Fn::Equals": [ref("EnableRuntimeResources"), "true"]}, {"Fn::Equals": [ref("EndOfProgramTeardown"), "false"]}]}, "Assertions": [
    {"Assert": {"Fn::Equals": [ref("EnableScheduledBackups"), "true"]}, "AssertDescription": "The running system requires daily backups."},
    {"Assert": {"Fn::Equals": [ref("QuarterlyScheduleState"), "ENABLED"]}, "AssertDescription": "The running system requires quarterly tests."},
    {"Assert": {"Fn::Equals": [ref("FixtureScheduleState"), "ENABLED"]}, "AssertDescription": "The running system requires fresh synthetic markers."}]}

rules["LiveJiraRequired"] = {"RuleCondition": {"Fn::Equals": [ref("EnableRuntimeResources"), "true"]}, "Assertions": [
    {"Assert": {"Fn::Not": [{"Fn::Equals": [ref("JiraConnectionArn"), ""]}]}, "AssertDescription": "The required failure exercise needs an existing approved Jira connection."},
    {"Assert": {"Fn::Not": [{"Fn::Equals": [ref("JiraWebhookUrl"), "https://example.invalid"]}]}, "AssertDescription": "Supply the private Jira Automation webhook URL."}]}

# Reuse the approved shared key. Its policy and billing remain external inputs.

for logical, suffix, fields in (("SourceTable", "source", ["pk"]), ("ResultsTable", "results", ["resource_id", "test_date"])):
    add(logical, "AWS::DynamoDB::Table", {"TableName": sub("${Prefix}-" + suffix), "BillingMode": "PAY_PER_REQUEST", "Tags": tags,
        "AttributeDefinitions": [{"AttributeName": f, "AttributeType": "S"} for f in fields],
        "KeySchema": [{"AttributeName": f, "KeyType": "HASH" if i == 0 else "RANGE"} for i, f in enumerate(fields)],
        "SSESpecification": {"SSEEnabled": True, "SSEType": "KMS", "KMSMasterKeyId": arn("Key")}}, DeletionPolicy="Delete", UpdateReplacePolicy="Delete")

for logical, suffix in (("SourceBucket", "source"), ("ReportBucket", "reports"), ("IrBucket", "ir")):
    # Evidence adopts the supplied shared pattern and analyst-write prefix.
    # Source and sandbox buckets keep their separate project-only identities.
    bucket_name = "${Prefix}-${AWS::AccountId}-${AWS::Region}-" + suffix
    add(logical, "AWS::S3::Bucket", {"BucketName": sub(bucket_name),
        "Tags": tags, "VersioningConfiguration": {"Status": "Enabled"},
        "OwnershipControls": {"Rules": [{"ObjectOwnership": "BucketOwnerEnforced"}]},
        "PublicAccessBlockConfiguration": {k: True for k in ["BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]},
        "BucketEncryption": {"ServerSideEncryptionConfiguration": [{"ServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": arn("Key")}, "BucketKeyEnabled": True}]}},
        DeletionPolicy="Delete", UpdateReplacePolicy="Delete")
    add(logical + "Policy", "AWS::S3::BucketPolicy", {"Bucket": ref(logical), "PolicyDocument": {"Version": "2012-10-17", "Statement": [{
        "Sid": "DenyInsecureTransport", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
        "Resource": [arn(logical), sub("${" + logical + ".Arn}/*")], "Condition": {"Bool": {"aws:SecureTransport": "false"}}}]}})
R["SourceBucket"]["Properties"]["LifecycleConfiguration"] = {"Rules": [{"Id": "grc-old-fixture-versions", "Status": "Enabled", "NoncurrentVersionExpiration": {"NoncurrentDays": 7}, "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 1}}]}
# Do not choose an unapproved evidence window. Event-pinned originals may be
# noncurrent, so both version states use the explicitly approved duration.
for logical in ("ReportBucket", "IrBucket"):
    R[logical]["Properties"]["LifecycleConfiguration"] = {"Rules": [{
        "Id": "grc-old-evidence-versions", "Status": "Enabled",
        "ExpirationInDays": ref("EvidenceRetentionDays"),
        "NoncurrentVersionExpiration": {"NoncurrentDays": ref("EvidenceRetentionDays")},
        "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 1}}]}

add("Vault", "AWS::Backup::BackupVault", {"BackupVaultName": sub("${Prefix}-vault"), "EncryptionKeyArn": arn("Key"), "BackupVaultTags": {"grc-project": "13"}},
    DeletionPolicy="Delete", UpdateReplacePolicy="Delete")
add("BackupPlan", "AWS::Backup::BackupPlan", {"BackupPlan": {"BackupPlanName": sub("${Prefix}-backup"),
    "BackupPlanRule": [{"RuleName": "grc-daily", "TargetBackupVault": ref("Vault"), "ScheduleExpression": ref("BackupSchedule"),
                        "StartWindowMinutes": 60, "CompletionWindowMinutes": 180, "Lifecycle": {"DeleteAfterDays": ref("BackupRetentionDays")}}]},
    "BackupPlanTags": {"grc-project": "13"}})
add("Selection", "AWS::Backup::BackupSelection", {"BackupPlanId": ref("BackupPlan"), "BackupSelection": {
    "SelectionName": sub("${Prefix}-sources"), "IamRoleArn": arn("BackupRole"), "Resources": [arn("SourceTable"), arn("SourceBucket")]}})
R["BackupPlan"]["Condition"] = R["Selection"]["Condition"] = "HasSchedule"

key_use = allow(["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey", "kms:DescribeKey", "kms:ReEncrypt*"], arn("Key"))
key_grant = allow("kms:CreateGrant", arn("Key"), Condition={"Bool": {"kms:GrantIsForAWSResource": "true"}})
result_rw = allow(["dynamodb:GetItem", "dynamodb:PutItem"], arn("ResultsTable"))
target_table = sub("arn:${AWS::Partition}:dynamodb:${AWS::Region}:${AWS::AccountId}:table/${Prefix}-restore-dynamodb-*")
target_bucket = sub("arn:${AWS::Partition}:s3:::${Prefix}-restore-s3-*")
target_objects = sub("arn:${AWS::Partition}:s3:::${Prefix}-restore-s3-*/*")
lease_delete = allow("dynamodb:DeleteItem", arn("ResultsTable"), Condition={"ForAllValues:StringEquals": {"dynamodb:LeadingKeys": ["#fixture-lock"]}})
restore_read = allow("backup:DescribeRestoreJob", "*")  # This read action has no resource-level ARN.
role("BackupRole", "backup-role", "backup.amazonaws.com", [key_use, key_grant,
    allow(["s3:GetBucketTagging", "s3:GetInventoryConfiguration", "s3:ListBucketVersions", "s3:ListBucket", "s3:GetBucketVersioning", "s3:GetBucketLocation", "s3:GetBucketAcl", "s3:GetBucketNotification"], arn("SourceBucket")),
    allow(["s3:GetObjectAcl", "s3:GetObject", "s3:GetObjectVersionTagging", "s3:GetObjectVersionAcl", "s3:GetObjectTagging", "s3:GetObjectVersion"], sub("${SourceBucket.Arn}/*")),
    allow(["cloudwatch:GetMetricData", "s3:ListAllMyBuckets"], "*"),
    allow(["dynamodb:DescribeTable", "dynamodb:CreateBackup", "dynamodb:StartAwsBackupJob", "dynamodb:ListTagsOfResource"], arn("SourceTable")),
    allow(["dynamodb:DescribeBackup", "dynamodb:DeleteBackup"], sub("${SourceTable.Arn}/backup/*")),
    allow(["backup:DescribeBackupVault", "backup:CopyIntoBackupVault"], {"Fn::GetAtt": ["Vault", "BackupVaultArn"]}),
    allow("backup:TagResource", sub("arn:${AWS::Partition}:backup:${AWS::Region}:${AWS::AccountId}:recovery-point:*"))])
role("BackupRestoreRole", "backup-restore-role", "backup.amazonaws.com", [key_use, key_grant,
    allow(["s3:ListBucketVersions", "s3:ListBucket", "s3:GetBucketVersioning", "s3:GetBucketLocation", "s3:GetBucketOwnershipControls", "s3:PutBucketVersioning", "s3:PutBucketOwnershipControls"], target_bucket),
    allow(["s3:GetObject", "s3:GetObjectVersion", "s3:GetObjectTagging", "s3:PutObjectTagging", "s3:GetObjectAcl", "s3:ListMultipartUploadParts", "s3:PutObject"], target_objects),
    allow(["dynamodb:RestoreTableFromAwsBackup", "dynamodb:RestoreTableFromBackup", "dynamodb:DescribeTable", "dynamodb:Scan", "dynamodb:Query", "dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem", "dynamodb:BatchWriteItem"], target_table),
    allow("dynamodb:RestoreTableFromBackup", sub("${SourceTable.Arn}/backup/*"))])

add("EventBus", "AWS::Events::EventBus", {"Name": sub("${Prefix}-events"), "Tags": tags})
add("DeadLetterQueue", "AWS::SQS::Queue", {"QueueName": sub("${Prefix}-delivery-dlq"), "MessageRetentionPeriod": 1209600,
    "SqsManagedSseEnabled": True, "Tags": tags})
add("DeadLetterPolicy", "AWS::SQS::QueuePolicy", {"Queues": [ref("DeadLetterQueue")], "PolicyDocument": {"Version": "2012-10-17", "Statement": [{
    "Effect": "Allow", "Principal": {"Service": "events.amazonaws.com"}, "Action": "sqs:SendMessage", "Resource": arn("DeadLetterQueue"),
    "Condition": {"StringEquals": {"aws:SourceAccount": ref("AWS::AccountId")}, "ArnLike": {"aws:SourceArn": sub("arn:${AWS::Partition}:events:${AWS::Region}:${AWS::AccountId}:rule/*grc-*")}}}]}})

base_env = {"PREFIX": ref("Prefix"), "PARTITION": ref("AWS::Partition"), "ACCOUNT_ID": ref("AWS::AccountId"),
    "SOURCE_TABLE": ref("SourceTable"), "SOURCE_TABLE_ARN": arn("SourceTable"), "SOURCE_BUCKET": ref("SourceBucket"),
    "RESULTS_TABLE": ref("ResultsTable"), "REPORT_BUCKET": ref("ReportBucket"), "IR_BUCKET": ref("IrBucket"), "KEY_ARN": arn("Key")}


def function(logical, module, statements, extra_env=None, timeout=60):
    required_env = [k for k in base_env if k != "IR_BUCKET"]
    add(logical + "Log", "AWS::Logs::LogGroup", {"LogGroupName": sub("/aws/lambda/${Prefix}-" + module), "RetentionInDays": 7, "Tags": tags})
    logs = allow(["logs:CreateLogStream", "logs:PutLogEvents"], sub("arn:${AWS::Partition}:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/${Prefix}-" + module + ":*"))
    role(logical + "Role", module + "-role", "lambda.amazonaws.com", [logs, *statements])
    add(logical, "AWS::Lambda::Function", {"FunctionName": sub("${Prefix}-" + module), "Runtime": "python3.13", "Handler": "bcdr." + module + ".handler",
        "Role": arn(logical + "Role"), "Code": {"S3Bucket": ref("CodeS3Bucket"), "S3Key": ref("CodeS3Key"), "S3ObjectVersion": ref("CodeS3ObjectVersion")},
        "Timeout": timeout, "MemorySize": 256,
        "Environment": {"Variables": {**{k: base_env[k] for k in required_env}, **(extra_env or {})}}, "Tags": tags}, DependsOn=[logical + "Log"])

# A separate fixture writer keeps source writes out of all DR execution roles.
controller_env = {"VAULT": ref("Vault"), "RESTORE_ROLE_ARN": arn("BackupRestoreRole"),
    "DYNAMODB_RTO": ref("DynamoDbRtoSeconds"), "DYNAMODB_RPO": ref("DynamoDbRpoSeconds"),
    "S3_RTO": ref("S3RtoSeconds"), "S3_RPO": ref("S3RpoSeconds"),
    "TARGET_APPROVAL": ref("TargetApprovalReference"), "MAX_RESTORE_WAIT": ref("MaxRestoreWaitSeconds"),
    "ALLOW_FAULTS": ref("EnableFaultInjection"), "INCLUDE_S3": "true",
    "EVENT_BUS": ref("EventBus"), "EVIDENCE_BUS": ref("EvidenceBusArn"), "RISK_BUS": ref("RiskBusArn"),
    "JIRA_ENABLED": choose("HasJira", "true", "false")}
function("Controller", "controller", [result_rw, lease_delete, key_use, restore_read,
    allow(["s3:CreateBucket", "s3:ListBucket", "s3:GetBucketTagging", "s3:PutBucketTagging", "s3:PutBucketPublicAccessBlock", "s3:PutEncryptionConfiguration", "s3:PutBucketVersioning", "s3:PutBucketPolicy", "s3:PutBucketOwnershipControls"], target_bucket),
    allow(["backup:GetRestoreJobMetadata", "backup:ListRestoreJobs"], "*"),
    allow(["s3:GetObject", "s3:GetObjectVersion"], sub("${ReportBucket.Arn}/baselines/*")),
    allow("s3:PutObject", sub("${ReportBucket.Arn}/dr-tests/*")),
    allow("backup:ListRecoveryPointsByBackupVault", {"Fn::GetAtt": ["Vault", "BackupVaultArn"]}),
    allow("backup:StartRestoreJob", sub("arn:${AWS::Partition}:backup:${AWS::Region}:${AWS::AccountId}:recovery-point:*")),
    allow("iam:PassRole", arn("BackupRestoreRole"), Condition={"StringEquals": {"iam:PassedToService": "backup.amazonaws.com"}}),
    allow("events:PutEvents", arn("EventBus"))], controller_env)
function("Validate", "validate", [result_rw, allow(["kms:Decrypt", "kms:DescribeKey"], arn("Key")),
    allow(["s3:ListBucket", "s3:GetBucketTagging", "s3:GetBucketVersioning", "s3:GetBucketPublicAccessBlock", "s3:GetBucketPolicy", "s3:GetEncryptionConfiguration"], target_bucket),
    allow("s3:GetObject", target_objects),
    allow(["dynamodb:DescribeTable", "dynamodb:Scan"], target_table)], timeout=120)
function("Janitor", "janitor", [result_rw, key_use, restore_read,
    allow(["s3:ListBucket", "s3:ListBucketVersions", "s3:GetBucketTagging", "s3:DeleteBucket"], target_bucket),
    allow(["s3:DeleteObject", "s3:DeleteObjectVersion"], target_objects),
    allow(["backup:GetRestoreJobMetadata", "backup:ListRestoreJobs"], "*"),
    allow(["dynamodb:DescribeTable", "dynamodb:DeleteTable"], target_table),
    allow("dynamodb:Scan", arn("ResultsTable")),
    allow("states:DescribeExecution", sub("arn:${AWS::Partition}:states:${AWS::Region}:${AWS::AccountId}:execution:${Prefix}-dr:*")),
    allow("lambda:InvokeFunction", [arn("Controller"), sub("arn:${AWS::Partition}:lambda:${AWS::Region}:${AWS::AccountId}:function:${Prefix}-janitor")]),
    allow("cloudwatch:PutMetricData", "*", Condition={"StringEquals": {"cloudwatch:namespace": "GRC/BCDR"}})],
    {"RESTORE_FUNCTION": ref("Controller"), "CLEANUP_FUNCTION": sub("${Prefix}-janitor"), "REPORT_FUNCTION": ref("Controller"),
     "MAX_RESTORE_WAIT": ref("MaxRestoreWaitSeconds"), "SCHEDULE_STATE": ref("QuarterlyScheduleState"),
     "SCHEDULE_ACTIVE_FROM": ref("ScheduleActiveFrom"), "DEADLINE_HOURS": ref("QuarterDeadlineHours"), "INCLUDE_S3": "true"}, timeout=300)
function("Fixture", "fixtures", [key_use, lease_delete,
    allow(["dynamodb:GetItem", "dynamodb:PutItem"], arn("ResultsTable"), Condition={"ForAllValues:StringEquals": {"dynamodb:LeadingKeys": ["#fixture", "#fixture-lock"]}}),
    allow("dynamodb:Scan", arn("ResultsTable")),
    allow(["dynamodb:Scan", "dynamodb:PutItem"], arn("SourceTable")),
    allow("s3:ListBucket", arn("SourceBucket")),
    allow(["s3:GetObject", "s3:PutObject"], sub("${SourceBucket.Arn}/*")),
    allow(["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject"], sub("${ReportBucket.Arn}/baselines/*")),
    allow("sqs:SendMessage", arn("DeadLetterQueue"))], timeout=120)

retry = [{"ErrorEquals": ["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException", "Lambda.TooManyRequestsException"], "IntervalSeconds": 3, "MaxAttempts": 3, "BackoffRate": 2}]


def task(function_name, action=None, next_state=None, catch=None, **extra):
    state = {"Type": "Task", "Resource": arn(function_name), "Parameters": {"job.$": "$.job"}, "ResultPath": "$.step", "Retry": retry,
             **({"Next": next_state} if next_state else {"End": True}), **extra}
    if action:
        state["Parameters"]["action"] = action
    if catch:
        state["Catch"] = [{"ErrorEquals": ["States.ALL"], "ResultPath": "$.error", "Next": catch}]
    return state


iterator = {"StartAt": "Prepare", "States": {
    "Prepare": task("Restore", "prepare", "StartRestore", "RecordFailure"),
    "StartRestore": task("Restore", "start", "WaitRestore", "RecordFailure"),
    "WaitRestore": {"Type": "Wait", "Seconds": 30, "Next": "PollRestore"},
    "PollRestore": task("Restore", "poll", "RestoreReady", "RecordFailure"),
    "RestoreReady": {"Type": "Choice", "Choices": [{"Variable": "$.step.state", "StringEquals": "VALIDATE", "Next": "Validate"},
        {"Variable": "$.step.state", "StringEquals": "FAIL", "Next": "RecordFailure"}], "Default": "WaitRestore"},
    "Validate": task("Validate", None, "Cleanup", "RecordFailure"),
    "RecordFailure": task("Restore", "fail", "Cleanup", "Cleanup"),
    "Cleanup": task("Cleanup", None, "CleanupDone", "Publish"),
    "CleanupDone": {"Type": "Choice", "Choices": [{"Variable": "$.step.done", "BooleanEquals": True, "Next": "Publish"}], "Default": "WaitCleanup"},
    "WaitCleanup": {"Type": "Wait", "Seconds": 30, "Next": "Cleanup"},
    "Publish": task("Report", ResultPath="$", Retry=[{"ErrorEquals": ["States.ALL"], "IntervalSeconds": 5, "MaxAttempts": 3, "BackoffRate": 2}])}}
definition = {"Comment": "Isolated synthetic recovery validation; monitor reconciles stopped or timed-out executions.", "TimeoutSeconds": 10800,
    "StartAt": "Plan", "States": {
        "Plan": {"Type": "Task", "Resource": arn("Restore"), "Parameters": {"action": "plan", "request.$": "$", "execution_arn.$": "$$.Execution.Id", "start_time.$": "$$.Execution.StartTime"}, "Retry": retry, "Next": "Resources"},
        "Resources": {"Type": "Map", "ItemsPath": "$.jobs", "MaxConcurrency": 1, "ItemSelector": {"job.$": "$$.Map.Item.Value"}, "ItemProcessor": {"ProcessorConfig": {"Mode": "INLINE"}, **iterator}, "ResultPath": "$.results", "Next": "Outcome"},
        "Outcome": {"Type": "Task", "Resource": arn("Restore"), "Parameters": {"action": "summarize", "results.$": "$.results"}, "End": True}}}
role("WorkflowRole", "workflow-role", "states.amazonaws.com", [allow("lambda:InvokeFunction", [arn(n) for n in ["Restore", "Validate", "Cleanup", "Report"]])])
add("StateMachine", "AWS::StepFunctions::StateMachine", {"StateMachineName": sub("${Prefix}-dr"), "StateMachineType": "STANDARD", "RoleArn": arn("WorkflowRole"), "Definition": definition, "Tags": tags})
role("SchedulerRole", "schedule-role", "scheduler.amazonaws.com", [allow("states:StartExecution", arn("StateMachine")), allow("lambda:InvokeFunction", arn("Fixture")), allow("sqs:SendMessage", arn("DeadLetterQueue"))])
add("QuarterlySchedule", "AWS::Scheduler::Schedule", {"Name": sub("${Prefix}-quarterly"), "State": ref("QuarterlyScheduleState"),
    "ScheduleExpression": "cron(0 9 1 1,4,7,10 ? *)", "ScheduleExpressionTimezone": "UTC", "FlexibleTimeWindow": {"Mode": "OFF"},
    "Target": {"Arn": arn("StateMachine"), "RoleArn": arn("SchedulerRole"), "Input": "{}", "DeadLetterConfig": {"Arn": arn("DeadLetterQueue")}, "RetryPolicy": {"MaximumEventAgeInSeconds": 3600, "MaximumRetryAttempts": 2}}})
add("FixtureSchedule", "AWS::Scheduler::Schedule", {"Name": sub("${Prefix}-fixture"), "State": ref("FixtureScheduleState"),
    "ScheduleExpression": "cron(0 2 * * ? *)", "ScheduleExpressionTimezone": "UTC", "FlexibleTimeWindow": {"Mode": "OFF"},
    "Target": {"Arn": arn("Fixture"), "RoleArn": arn("SchedulerRole"), "Input": '{"refresh":true,"refresh_id":"<aws.scheduler.scheduled-time>"}', "DeadLetterConfig": {"Arn": arn("DeadLetterQueue")}, "RetryPolicy": {"MaximumEventAgeInSeconds": 3600, "MaximumRetryAttempts": 2}}})
add("FixtureAsync", "AWS::Lambda::EventInvokeConfig", {"FunctionName": ref("Fixture"), "Qualifier": "$LATEST", "MaximumRetryAttempts": 2,
    "MaximumEventAgeInSeconds": 3600, "DestinationConfig": {"OnFailure": {"Destination": arn("DeadLetterQueue")}}})

def lambda_rule(name, suffix, target, **props):
    add(name, "AWS::Events::Rule", {"Name": sub("${Prefix}-" + suffix), "State": "ENABLED", **props,
        "Targets": [{"Id": "grc-handler", "Arn": arn(target), "DeadLetterConfig": {"Arn": arn("DeadLetterQueue")}, "RetryPolicy": {"MaximumEventAgeInSeconds": 3600, "MaximumRetryAttempts": 5}}]})
    add(name + "Permission", "AWS::Lambda::Permission", {"Action": "lambda:InvokeFunction", "FunctionName": ref(target), "Principal": "events.amazonaws.com", "SourceArn": arn(name), "SourceAccount": ref("AWS::AccountId")})
lambda_rule("MonitorRule", "reconcile", "Monitor", ScheduleExpression="rate(15 minutes)")
# Asynchronous reconciler failures also go to the delivery queue.
R["JanitorRole"]["Properties"]["Policies"][0]["PolicyDocument"]["Statement"].append(allow("sqs:SendMessage", arn("DeadLetterQueue")))
add("JanitorAsync", "AWS::Lambda::EventInvokeConfig", {"FunctionName": ref("Janitor"), "Qualifier": "$LATEST", "MaximumRetryAttempts": 2,
    "MaximumEventAgeInSeconds": 3600, "DestinationConfig": {"OnFailure": {"Destination": arn("DeadLetterQueue")}}})

for target, condition, param, detail_type in (("Evidence", "HasEvidence", "EvidenceBusArn", "BCDR Test Result"), ("Risk", "HasRisk", "RiskBusArn", "BCDR Finding")):
    role(target + "ForwardRole", target.lower() + "-forward-role", "events.amazonaws.com", [allow("events:PutEvents", ref(param))], condition)
    add(target + "Rule", "AWS::Events::Rule", {"Name": sub("${Prefix}-to-" + target.lower()), "EventBusName": ref("EventBus"), "State": "ENABLED",
        "EventPattern": {"source": ["grc.bcdr"], "detail-type": [detail_type]}, "Targets": [{"Id": "grc-" + target.lower(), "Arn": ref(param), "RoleArn": arn(target + "ForwardRole"),
        "DeadLetterConfig": {"Arn": arn("DeadLetterQueue")}, "RetryPolicy": {"MaximumEventAgeInSeconds": 86400, "MaximumRetryAttempts": 10}}]}, Condition=condition)
R["EvidenceRule"]["Properties"]["EventPattern"]["detail-type"].append("BCDR Evidence Record")

add("JiraDestination", "AWS::Events::ApiDestination", {"Name": sub("${Prefix}-jira"), "ConnectionArn": ref("JiraConnectionArn"), "HttpMethod": "POST", "InvocationEndpoint": ref("JiraWebhookUrl"), "InvocationRateLimitPerSecond": 1}, Condition="HasJira")
role("JiraRole", "jira-role", "events.amazonaws.com", [allow("events:InvokeApiDestination", arn("JiraDestination"))], "HasJira")
add("JiraRule", "AWS::Events::Rule", {"Name": sub("${Prefix}-to-jira"), "EventBusName": ref("EventBus"), "State": "ENABLED",
    "EventPattern": {"source": ["grc.bcdr"], "detail-type": ["BCDR Finding"]}, "Targets": [{"Id": "grc-jira", "Arn": arn("JiraDestination"), "RoleArn": arn("JiraRole"),
        "InputPath": "$.detail", "DeadLetterConfig": {"Arn": arn("DeadLetterQueue")}, "RetryPolicy": {"MaximumEventAgeInSeconds": 86400, "MaximumRetryAttempts": 10}}]}, Condition="HasJira")

role("AutomationRole", "automation-role", "ssm.amazonaws.com", [allow(["s3:GetBucketPolicy", "s3:PutBucketPolicy"], arn("IrBucket"))])
for operation, quarantine in (("quarantine", True), ("release", False)):
    policy = {"Version": "2012-10-17", "Statement": [{"Sid": "DenyInsecureTransport", "Effect": "Deny", "Principal": "*", "Action": "s3:*", "Resource": ["${IrBucket.Arn}", "${IrBucket.Arn}/*"], "Condition": {"Bool": {"aws:SecureTransport": "false"}}}]}
    if quarantine:
        policy["Statement"].append({"Sid": "IncidentQuarantineWrites", "Effect": "Deny", "Principal": "*", "Action": ["s3:PutObject", "s3:DeleteObject", "s3:DeleteObjectVersion"], "Resource": "${IrBucket.Arn}/*"})
    def evidence_step(name, phase):
        return {"name": name, "action": "aws:executeAwsApi", "timeoutSeconds": 25, "onFailure": "Abort",
            "inputs": {"Service": "s3", "Api": "GetBucketPolicy", "Bucket": ref("IrBucket")},
            "outputs": [{"Name": "Policy", "Selector": "$.Policy", "Type": "String"}]}
    content = {"schemaVersion": "0.3", "description": "Approval-gated " + operation + " of the disposable project IR bucket only.", "assumeRole": arn("AutomationRole"),
        "parameters": {"IncidentId": {"type": "String", "allowedPattern": "[A-Za-z0-9_-]{1,64}", "description": "Exercise or incident reference, without personal data."}},
        "mainSteps": [evidence_step("CaptureBefore", "before"),
            {"name": "ApproveChange", "action": "aws:approve", "timeoutSeconds": 3600, "onFailure": "Abort", "inputs": {"Message": "Approve " + operation + " of the disposable BCDR IR sandbox.", "MinRequiredApprovals": 1, "Approvers": [ref("IrApproverArn")]}},
            {"name": "ApplyPolicy", "action": "aws:executeAwsApi", "timeoutSeconds": 25, "onFailure": "Abort", "inputs": {"Service": "s3", "Api": "PutBucketPolicy", "Bucket": ref("IrBucket"), "Policy": sub(json.dumps(policy, separators=(",", ":")))}},
            {**evidence_step("CaptureAfter", "after"), "isEnd": True}]}
    add("Ir" + operation.title(), "AWS::SSM::Document", {"Name": sub("${Prefix}-ir-" + operation), "DocumentType": "Automation", "DocumentFormat": "JSON", "UpdateMethod": "NewVersion", "Content": content, "Tags": tags})

def alarm(logical, suffix, namespace, metric_name, dimensions, **extra):
    add(logical, "AWS::CloudWatch::Alarm", {"AlarmName": sub("${Prefix}-" + suffix), "AlarmDescription": "Project 13 operational signal; see docs/STEP-BY-STEP.md.",
        "Namespace": namespace, "MetricName": metric_name, "Dimensions": dimensions, "Statistic": "Sum", "Period": 900,
        "EvaluationPeriods": 1, "Threshold": 0, "ComparisonOperator": "GreaterThanThreshold", "TreatMissingData": "notBreaching", "AlarmActions": [ref("AlarmTopicArn")], **extra})
add("OperationsAlarm", "AWS::CloudWatch::Alarm", {"AlarmName": sub("${Prefix}-operations"),
    "ComparisonOperator": "GreaterThanThreshold", "Threshold": 0, "EvaluationPeriods": 1,
    "TreatMissingData": "notBreaching", "AlarmActions": [ref("AlarmTopicArn")],
    "Metrics": [{"Id": "problems", "Expression": "cleanup + errors + overdue", "ReturnData": True}] + [
        {"Id": ident, "ReturnData": False, "MetricStat": {"Metric": {"Namespace": "GRC/BCDR", "MetricName": metric,
        "Dimensions": [{"Name": "Project", "Value": ref("Prefix")}]}, "Period": 900, "Stat": "Maximum"}}
        for ident, metric in (("cleanup", "CleanupPending"), ("errors", "ReconciliationErrors"), ("overdue", "OverdueTests"))]})
alarm("QueueAlarm", "delivery-failed", "AWS/SQS", "ApproximateNumberOfMessagesVisible", [{"Name": "QueueName", "Value": {"Fn::GetAtt": ["DeadLetterQueue", "QueueName"]}}], Statistic="Maximum")
alarm("FixtureAlarm", "fixture-failed", "AWS/Lambda", "Errors", [{"Name": "FunctionName", "Value": ref("Fixture")}], Period=300)
alarm("MonitorHeartbeatAlarm", "monitor-missing", "AWS/Lambda", "Invocations", [{"Name": "FunctionName", "Value": ref("Monitor")}], Period=1800, Threshold=1, ComparisonOperator="LessThanThreshold", TreatMissingData="breaching", EvaluationPeriods=2)
add("WorkflowAlarm", "AWS::CloudWatch::Alarm", {"AlarmName": sub("${Prefix}-workflow-failed"), "ComparisonOperator": "GreaterThanThreshold", "Threshold": 0, "EvaluationPeriods": 1, "TreatMissingData": "notBreaching", "AlarmActions": [ref("AlarmTopicArn")],
    "Metrics": [{"Id": "failures", "Expression": "failed + timedout + aborted", "ReturnData": True}] + [{"Id": ident, "ReturnData": False, "MetricStat": {"Metric": {"Namespace": "AWS/States", "MetricName": metric_name,
        "Dimensions": [{"Name": "StateMachineArn", "Value": arn("StateMachine")}]}, "Period": 300, "Stat": "Sum"}} for ident, metric_name in (("failed", "ExecutionsFailed"), ("timedout", "ExecutionsTimedOut"), ("aborted", "ExecutionsAborted"))]})

outputs = {name: {"Value": value} for name, value in {
    "StateMachineArn": arn("StateMachine"), "ControllerFunctionName": ref("Controller"), "JanitorFunctionName": ref("Janitor"),
    "FixtureFunctionName": ref("Fixture"), "SourceBucketName": ref("SourceBucket"), "SourceBucketArn": arn("SourceBucket"),
    "QuarterlyScheduleName": ref("QuarterlySchedule"), "FixtureScheduleName": ref("FixtureSchedule"), "MonitorRuleName": ref("MonitorRule"),
    "SourceTableName": ref("SourceTable"), "SourceTableArn": arn("SourceTable"), "ReportBucketName": ref("ReportBucket"), "IrBucketName": ref("IrBucket"),
    "ResultsTableName": ref("ResultsTable"), "VaultName": ref("Vault"), "BackupRoleArn": arn("BackupRole"), "KeyArn": arn("Key"), "EventBusName": ref("EventBus"),
    "DeadLetterQueueUrl": ref("DeadLetterQueue"), "QuarantineDocument": ref("IrQuarantine"), "ReleaseDocument": ref("IrRelease")}.items()}
for resource in R.values():
    resource.setdefault("Condition", "Live")
for output in outputs.values():
    output["Condition"] = "Live"
outputs["BackupPlanId"] = {"Value": ref("BackupPlan"), "Condition": "HasSchedule"}
# Replace every key reference before serialization, keeping the readable roles
# above close to the reviewed architecture. No key or alias is provisioned.
def reuse_key(value):
    if value == arn("Key"):
        return ref("ExistingKmsKeyArn")
    if isinstance(value, dict):
        return {k: reuse_key(v) for k, v in value.items()}
    if isinstance(value, list):
        return [reuse_key(v) for v in value]
    return value
R = reuse_key(R)
outputs = reuse_key(outputs)
template = {"AWSTemplateFormatVersion": "2010-09-09", "Description": "Project 13 BCDR and IR: synthetic sources, isolated restores, evidence and approval-gated sandbox response.",
    "Parameters": P, "Rules": rules, "Conditions": conditions, "Resources": R, "Outputs": outputs}

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

    def represent_dict(self, data):
        # Standard CloudFormation short forms remove verbose intrinsic wrappers.
        if len(data) == 1:
            name, value = next(iter(data.items()))
            if name == "Ref":
                return self.represent_scalar("!Ref", value)
            if name == "Fn::Sub" and isinstance(value, str):
                return self.represent_scalar("!Sub", value)
            if name == "Fn::GetAtt":
                return self.represent_scalar("!GetAtt", ".".join(value))
        if "Effect" in data or "Variables" in data or "StartAt" in data or "schemaVersion" in data or "Properties" in data:
            return self.represent_mapping("tag:yaml.org,2002:map", data, flow_style=True)
        return self.represent_mapping("tag:yaml.org,2002:map", data)

NoAliasDumper.add_representer(dict, NoAliasDumper.represent_dict)

def main():
    if ROOT.name != "Rasheed-13-BCDR-IR" or ROOT.parent.name != "engineering":
        raise SystemExit("Place this generator at engineering/Rasheed-13-BCDR-IR/tools/render_template.py in the repository")
    output = REPO_ROOT / "infrastructure/cloudformation/grc-bcdr.yaml"
    output.parent.mkdir(parents=True, exist_ok=True)
    header = "# Native CloudFormation. Generated by engineering/Rasheed-13-BCDR-IR/tools/render_template.py.\n# Source, checks and operation: engineering/Rasheed-13-BCDR-IR/README.md.\n# Runtime is off until approved. Once live, keep running through programme end.\n# Four separate roles: fixture writer, controller, validator and cleanup.\n# Reuse the approved shared key and boundary; never target production.\n"
    # Flow style on short collections keeps this below the repository's inline
    # template limit while preserving readable named resources and policies.
    rendered = copy.deepcopy(template)
    parameter_rows = ["# Deployment parameters", "", "All durations are seconds unless the name states otherwise. Supply approved targets; there are no target defaults.", "", "| Parameter | Default | Purpose |", "| --- | --- | --- |"]
    for name, value in rendered["Parameters"].items():
        description = value.pop("Description")
        default = str(value.get("Default", "Required")) or "Disabled / empty"
        parameter_rows.append("| `" + name + "` | `" + default + "` | " + description + " |")
    (ROOT / "docs/PARAMETERS.md").write_text("\n".join(parameter_rows) + "\n")
    # Stack tags cover IAM, Lambda and logs. Explicit mandatory project tags
    # remain on data resources. The shared KMS key is external to this stack.
    for resource in rendered["Resources"].values():
        if resource["Type"] in {"AWS::IAM::Role", "AWS::Lambda::Function", "AWS::Logs::LogGroup"}:
            resource["Properties"].pop("Tags", None)
    text = header + yaml.dump(rendered, Dumper=NoAliasDumper, sort_keys=False, default_flow_style=None, width=1000)
    output.write_text(text)
    if output.stat().st_size >= 51200:
        raise SystemExit("CloudFormation template exceeds the repository's 51,200-byte limit")
    print(str(output.relative_to(REPO_ROOT)) + ": " + str(output.stat().st_size) + " bytes")


if __name__ == "__main__":
    main()
