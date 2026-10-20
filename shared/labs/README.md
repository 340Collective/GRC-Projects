# GRC lab guide (all projects)

What every lab has in common. Each project folder has its own LAB-STEPS.md, one per track, with the same `Working with your partner` section in both; this page holds no per-project steps.

## 1. Account and tool setup

1. Get your IAM user name and a temporary password from the ISSM, shared out of band, along with the sign-in URL. Neither is ever put in the repo, GitHub, or Jira.
2. Sign in, set a new password, and enroll a virtual MFA device first. Sign out and back in with MFA; until then nothing else works.
3. For CLI use, create your own access key and get MFA session credentials with `aws sts get-session-token --serial-number <mfa-arn> --token-code <code>`. Calls without MFA are denied. Work in us-east-1 only.
4. Diagram kit: run `python3 engineering/<folder>/diagram/build_diagram.py --setup` once (it needs `rsvg-convert` from librsvg), then rebuild with the command in the folder's README. Every build must print `crossings: 0`, `layout problems: none`, and `sensitive text: none`.
5. Branches are `<type>/<short-topic>`, for example `docs/06-evidence-notes`. Never commit to `main`. Templates live in this repo's `infrastructure/cloudformation/` folder and go by pull request into `main` like any other change (see [infrastructure/README.md](../../infrastructure/README.md)).
6. Before every pull request, run `python3 shared/check_links.py` from the repo root: it must report 0 broken.

The access rules for each seat are in [shared/access-model/README.md](../access-model/README.md).

## 2. Phase model

- One active build per engineer at a time. A phase ends when all its builds are merged, signed off, and running in the shared system.
- Phase 1: foundation, 13, 06, 14. Phase 2: 01, 07, 10, 08. Phase 3: 11, 09 and the 04 scoring run, 03. Phase 4: 12, 02. Phase 5: 15, 05.
- Partners write REQUIREMENTS.md in their own folder and agree it with the engineer at the Day 1 kickoff, then commit their results to their own folder, sign off on the final report, operate, and report.
- The team, the points, and the per-phase queue are in [engineering/README.md](../../engineering/README.md) and [non-engineering/README.md](../../non-engineering/README.md).

## 3. Review flow

1. The partner writes REQUIREMENTS.md in their own folder by pull request; the ISSM accepts it at the Day 1 kickoff (the ISSO accepts the ISSM's own).
2. The engineer builds the template in `infrastructure/cloudformation/` in this repo, and another engineer does the code review in GitHub.
3. After approval, the engineer deploys their own project stack with their `GRC-Engineer` seat from this repo's clean `main` equal to `origin/main`, tags the deploy `live-YYYY-MM-DD`, and tells the partner the build is ready. Only the ISSM deploys the shared stacks (`grc-access-model`, `grc-internal-auditor`, `grc-engineer-users`, `compliance-evidence`, and `grc-uar-sim-*`; see [infrastructure/README.md](../../infrastructure/README.md)).
4. The partner signs off on the final report as a comment on the Final report item ("Accepted by: <first name>", or findings). The partner commits test and operating results to their own folder first, and links them in the sign-off. The Internal Auditor's sign-off is a pass or findings record, not an approval.
5. The ISSO validates engineer work on the Final report item.
6. The ISSM gives final approval. For ISSM-built work (foundation, 01, 11, 00), the ISSO accepts and gives final approval.
7. The Internal Auditor assesses independently once per phase, never per pull request, and commits the assessment to his own folder.
8. An engineer's pull request in this repo links its project item and merges only after the partner's sign-off is on the Final report item. Only the ISSM merges.
9. A partner's pull request changes only their own folder. The ISSM reviews it for scope and the data rules and merges it. Engineers do not review or approve partner records.

Nobody validates their own build or requirements.

## 4. Cost cap

- The whole account stays under 10 dollars a month. The budget sends actual-spend alerts at 1, 5, and 10 dollars.
- At the 1 dollar alert, check what is running. Paid services run in cheap mode, or only for the test window.
- If the 5 dollar alert fires, scale down or pause the most expensive component (see the [running system cost](../../GOVERNANCE.md#running-system-cost) rule in GOVERNANCE.md). Do not tear the system down to save cost.
- Services on the access model's budget-breaker deny list need an access-change pull request and a cost check before anyone builds with them.
- Day-to-day reporting costs 0 dollars: Jira dashboards for partners, CloudWatch dashboards inside the free tier for engineers, and project 12's emailed board pack for leadership.

## 5. Test cleanup and end-of-program teardown

1. Test cleanup after every test: delete test data, restored copies, temporary users, and trial-only resources. The stack stays deployed after sign-off and is part of the running system.

End-of-program teardown, once, Jan 11 to 18, 2027 (see [GOVERNANCE.md](../../GOVERNANCE.md#end-of-program-teardown)):

2. Empty every `grc-*` bucket, including all object versions and delete markers.
3. Delete the `grc-*` stack from this repo's clean `main` and wait for `DELETE_COMPLETE`.
4. Turn off any per-use or trial service the build turned on (for example the Config recorder, Security Hub, GuardDuty, Inspector, Audit Manager, or a paid analyzer).
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the alert) where the ISSM designates, outside git, and note it on the Jira epic.
6. The shared foundation is deleted last.

## 6. No-lock evidence rule

Evidence is temporary project data, never kept for compliance retention. Every evidence bucket follows the foundation pattern:

- versioned, private, and encrypted with SSE-KMS;
- no Object Lock and no legal hold;
- current objects expire after 30 days, noncurrent versions after 7 days, and incomplete multipart uploads after 1 day;
- `DeletionPolicy` and `UpdateReplacePolicy` set to Delete.

Integrity comes from a SHA-256 hash per object plus a manifest that lists every hash, so any change shows up on verification. The end-of-program teardown empties the bucket, including all versions, and then deletes the stack. Raw evidence never goes into git.

## 7. AWS data into Jira

1. Findings: the native [Security Hub to Jira Cloud integration](https://docs.aws.amazon.com/securityhub/latest/userguide/jiracloud.html).
2. Project events: an EventBridge rule to the Jira REST API (an API destination) or a Jira Automation incoming webhook.
3. Metrics: project 12's daily job posts to the "GRC Metrics" Jira issue.

Do not use the AWS Service Management Connector; AWS retires it after 2027-03-31. Jira tokens live in Secrets Manager (through an EventBridge connection) or an SSM SecureString parameter under `/grc/`, never in git.
