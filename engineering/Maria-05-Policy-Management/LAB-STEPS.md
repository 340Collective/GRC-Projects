# 340 Collective Policy Management - Lab Steps (engineering)

Build and test the 340 Collective Policy Management design on AWS, then hand it to operation as part of the running shared system. It is removed only in the end-of-program teardown. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-05-Policy-Management/LAB-STEPS.md](../../non-engineering/Adam-05-Policy-Management/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Policy-Management-Architecture.md) and agree scope and requirements with Adam at the Day 1 kickoff before you write any template.
2. Turn Adam's header block (agreed at kickoff) into the front matter schema the validation stage checks.
3. The attestation API must require sign-in; it is never unauthenticated.
4. Check every service in the design against the permissions boundary and the budget-breaker deny list in [shared/access-model/README.md](../../shared/access-model/README.md). Anything outside them needs an access-change PR and a cost check before you build.
5. Plan to stay under 10 dollars a month: CodeBuild build minutes are the only real cost; keep test builds few.

## Deploy

1. Write `infrastructure/cloudformation/grc-policy.yaml` in this repo, in the build order from the architecture doc:
   - Policy repo layout and front matter schema.
   - Versioned, encrypted S3 library.
   - CodePipeline with the GitHub connection and the CodeBuild validation stage.
   - Attestation table, API, and handler.
   - EventBridge rule, reminder Lambda, and SES.
   - Scheduler review checks, CloudTrail, and alarms.
2. Name every resource `grc-*`, tag KMS keys and APIs `grc-project`, attach the permissions boundary to every `grc-*` role, and put no secrets, emails, or account IDs in the template.
3. Open a pull request to `main` in this repo; Rasheed does the code review. Paste the `infrastructure/` checks from CONTRIBUTING.md section 4 (cfn-lint clean) in the pull request.
4. After Faris's approval, deploy the `grc-policy` stack from this repo's clean `main` (equal to `origin/main`) with your GRC-Engineer seat and wait for `CREATE_COMPLETE`. Then tag that commit `live-YYYY-MM-DD` and push the tag.

## Test

1. Merge one of Adam's synthetic policy drafts: validation passes, a draft with a bad header fails the build, the rendered policy lands in the library, and one synthetic attestation is recorded.
2. Prove each control from the architecture doc's security section holds:
   - KMS customer managed key for the library and the attestation table.
   - Least-privilege IAM: CodeBuild can write only the library prefix; the attestation handler can write only the table.
   - The attestation API requires sign-in, so it is never unauthenticated.
   - CloudTrail logs every write to the library.
   - No personal data in logs beyond a person ID.
   - Human approval points: the policy owner approves every pull request before merge.
3. Check the budget's actual spend (budget reads are allowed): it is below the 1 dollar alert.

## Partner test

1. Tell Adam what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam commits his test results to his own folder, signs off, and records his validation on the Final report item. Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). It links the project item, and it merges only after the partner signs off on the Final report item.

## End-of-program teardown

1. Not a Day 7 step. After sign-off the stack stays deployed and running in the shared system. Test cleanup is separate: after every test, delete the test data, restored copies, temporary users, and trial-only resources the test made. Run these steps only in the [end-of-program teardown](../../GOVERNANCE.md#end-of-program-teardown).
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-policy` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete the GitHub connection if you created it outside the stack.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Day 7

Day 7: copy [shared/templates/FINAL-REPORT.md](../../shared/templates/FINAL-REPORT.md), fill it in with what you built and what your tests showed, link the partner's results, and open a pull request. Faris merges it after your partner signs off on the Final report item.

## Working with your partner

- Day 1 kickoff: you and Adam agree on scope and requirements.
- Days 2 to 6, build and code review: talk to Adam as needed, or comment on the project item.
- Day 7 sign-off: you commit FINAL-REPORT.md to this folder. Adam commits his results to his own folder, compares them with your report, and signs off on the Final report item ("Accepted by: <first name>", or findings). Faris merges your pull request only after that sign-off. The build stays deployed and running in the shared system.

**Skills:** Policy as code · CodePipeline and CodeBuild · authenticated APIs · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · CodePipeline · CodeBuild · S3 · DynamoDB · API Gateway · Lambda · SES

**Deliverable:** A tested policy-as-code pipeline with attestation tracking in the `grc-policy` stack, signed off on the Final report item, and running in the shared system.

**What it simulates:** An automation engineer turning a policy library into a governed pipeline.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and keeps it running after sign-off (it is removed only in the end-of-program teardown); only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
