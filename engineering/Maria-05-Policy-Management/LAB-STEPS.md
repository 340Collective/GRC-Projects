# 340 Collective Policy Management - Lab Steps (engineering)

Build, test, hand off, and tear down the 340 Collective Policy Management design on AWS as a temporary stack. 340 Collective is the subject organization.

Track: engineering. You: Maria (Automation Engineer). Partner: Adam (ISSO). Mirror: [non-engineering/Adam-05-Policy-Management/LAB-STEPS.md](../../non-engineering/Adam-05-Policy-Management/LAB-STEPS.md). General guide: [shared/labs/README.md](../../shared/labs/README.md).

## Design

1. Read the [architecture doc](Policy-Management-Architecture.md) and Adam's Handoff 1 Jira Task before you write any template.
2. Turn Adam's header block (Handoff 1) into the front matter schema the validation stage checks.
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

## Hand off

1. Create the Handoff 2 Jira Task for Adam: what to test, how to reach it, the synthetic test data, and what done looks like.
2. Adam records his acceptance and validation on the Task, and Faris gives final approval.
3. Open a pull request in this repo with the build notes (what was deployed and the test results; no secrets or raw evidence). Its Jira issue line links the Handoff 2 Task, and it merges only after the Task shows acceptance.

## Tear down

1. Tear down after acceptance, validation, and final approval are on the Jira Task, before the phase ends.
2. Empty every `grc-*` bucket the stack created, including all object versions and delete markers.
3. Delete the `grc-policy` stack from clean `main` and wait for `DELETE_COMPLETE`.
4. Delete the GitHub connection if you created it outside the stack.
5. Record teardown evidence (stack deleted, buckets gone, services off, spend under the 1 dollar alert) where the ISSM designates, outside git, and note it on the Jira epic.

## Handoffs

Each handoff is a Jira Task linked to the project epic (`GRC-<NN>`, a placeholder until Faris creates it). The person who sends the handoff creates the Task.

- Handoff 1: six policy drafts with header block and review cycle, Adam to Maria (Jira Task, created by Adam)
- Handoff 2: policy-as-code pipeline and attestation tracking ready for acceptance, Maria to Adam (Jira Task, created by Maria)
- Handoff 3: attestation results and review-cycle schedule, Adam to Faris (Jira Task, created by Adam)

**Skills:** Policy as code · CodePipeline and CodeBuild · authenticated APIs · CloudFormation

**Tools:** GRC-Projects repo (`infrastructure/`) · CloudFormation · CodePipeline · CodeBuild · S3 · DynamoDB · API Gateway · Lambda · SES

**Deliverable:** A tested policy-as-code pipeline with attestation tracking in the `grc-policy` stack, accepted on the Handoff 2 Jira Task, and torn down with evidence.

**What it simulates:** An automation engineer turning a policy library into a governed pipeline.

Templates live in this repo's `infrastructure/` folder. The engineer deploys their own project stack from this repo's clean `main` (equal to `origin/main`) after approval, tags the deploy `live-YYYY-MM-DD`, and tears it down; only the ISSM deploys the shared stacks listed in `infrastructure/README.md`. Nothing deploys from a branch.
