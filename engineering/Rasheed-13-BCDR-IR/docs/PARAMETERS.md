# Deployment parameters

All durations are seconds unless the name states otherwise. Supply approved targets; there are no target defaults.

| Parameter | Default | Purpose |
| --- | --- | --- |
| `Prefix` | `grc-bcdr` | Unique project prefix. Keep it stable for all runs and teardown. |
| `EnableRuntimeResources` | `false` | Enable only for the approved running shared system. Default creates no resources. |
| `EnableScheduledBackups` | `true` | Daily periodic backups are required in the running system; disable only for authorized end-of-program teardown. |
| `ExistingKmsKeyArn` | `Required` | Approved enabled symmetric CMK in this account and us-east-1, tagged grc-project. This stack never creates or deletes it. |
| `CodeS3Bucket` | `Required` | Existing grc-* staging bucket in us-east-1. |
| `CodeS3Key` | `Required` | Content-addressed key of the packaged Lambda ZIP. |
| `CodeS3ObjectVersion` | `Required` | Pinned S3 object version from the engineer's upload. |
| `TargetApprovalReference` | `Required` | Project-item reference recording the owner's approved per-resource RTO/RPO. |
| `IrApproverArn` | `Required` | IAM principal authorized to approve sandbox quarantine and release. |
| `AlarmTopicArn` | `Required` | Existing same-region grc-* SNS topic with a verified operator subscription. |
| `DynamoDbRtoSeconds` | `Required` | Approved DynamoDb RTO target in seconds. No example default is treated as approved. |
| `DynamoDbRpoSeconds` | `Required` | Approved DynamoDb RPO target in seconds. No example default is treated as approved. |
| `S3RtoSeconds` | `Required` | Approved S3 RTO target in seconds. No example default is treated as approved. |
| `S3RpoSeconds` | `Required` | Approved S3 RPO target in seconds. No example default is treated as approved. |
| `BackupSchedule` | `cron(0 3 * * ? *)` | Daily periodic backups after the 02:00 UTC fixture refresh. Review cadence against the approved RPO. |
| `BackupRetentionDays` | `7` | Warm retention. No vault lock or cold storage. |
| `MaxRestoreWaitSeconds` | `3600` | Stop validation polling after this duration; the independent monitor continues cleanup. |
| `EnableFaultInjection` | `false` | Permit explicit synthetic validation failure tests. |
| `QuarterlyScheduleState` | `ENABLED` | Quarterly restore tests of both synthetic resources. Disable only for an approved outage or end-of-program teardown. |
| `FixtureScheduleState` | `ENABLED` | Daily synthetic-only marker refresh before backup. Disable only for an approved outage or end-of-program teardown. |
| `EndOfProgramTeardown` | `false` | Explicitly permits schedules to be stopped for final removal. Never use at Day 7. |
| `ScheduleActiveFrom` | `Disabled / empty` | ISO UTC instant when the quarterly obligation starts; required when enabling the schedule. |
| `QuarterDeadlineHours` | `24` | Deadline after the quarterly scheduled start. |
| `EvidenceBusArn` | `Disabled / empty` | Optional project 06 custom grc-* event bus in this account and region. Leave empty until a compatible receiver exists; this is not a bucket ARN. |
| `RiskBusArn` | `Disabled / empty` | Optional project 07 custom grc-* event bus in this account and region. Leave empty until its receiver exists. |
| `JiraConnectionArn` | `Disabled / empty` | EXISTING approved EventBridge connection, required for a live exercise. No secret or connection is created by this stack. |
| `JiraWebhookUrl` | `https://example.invalid` | Jira Automation incoming webhook URL when a connection is supplied. Keep parameter files private. |
