# Contributing to GRC Projects

This is how every change gets into this repo, whether you write it yourself or an AI assistant helps. It follows a secure software development lifecycle (SSDLC) adapted for governance, risk, and compliance work.

Read these first:

- [GOVERNANCE.md](GOVERNANCE.md): roles, the two-track model, separation of duties, the change process, and the deviation request. This file does not repeat them. If the two disagree, GOVERNANCE.md wins and you should open an issue.
- [SECURITY.md](SECURITY.md): how to report a vulnerability or an accidental data exposure.
- [AGENTS.md](AGENTS.md): extra rules if an AI coding agent touches the repo.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): how the team works together.

## How we work

The short version is in the root [README](README.md#how-we-work). The rules that apply to every change:

- AI tools are allowed. Follow this SSDLC and [AGENTS.md](AGENTS.md), work on a branch in your own copy of the repo, and never merge without another person's review.
- Only change files in your own project folders: `engineering/<You>-NN-...` or `non-engineering/<You>-NN-...`. Shared files (root docs, `shared/`, `infrastructure/`) change only through Faris. [CODEOWNERS](.github/CODEOWNERS) sets who reviews.
- Code, templates, architecture, diagrams, lab steps, and the final report go in GitHub. Handoffs, day-to-day comments, blockers, and sign-off go in Jira. Nothing sensitive goes in LinkedIn messages or group chat.
- Each build is 7 days. On day 7, copy [shared/templates/FINAL-REPORT.md](shared/templates/FINAL-REPORT.md) into your engineering folder, fill it in, and merge it.

## What this repo is, and is not

- Documentation: lab designs and policy drafts for projects `00` to `15` in `engineering/` and `non-engineering/`, the general lab guide and access model notes in `shared/`, and diagram build scripts.
- Synthetic data: the synthetic UAR dataset in `engineering/Abdifatah-08-Access-Reviews/uar-simulation/data/`.
- Infrastructure in [infrastructure/](infrastructure/README.md): the GRC CloudFormation templates, the access-model policy validator, the evidence bucket init script, and the GRC change records (runbooks).
- Infrastructure lives in `infrastructure/`. Only the ISSM deploys the shared stacks (`grc-access-model`, `grc-internal-auditor`, `grc-engineer-users`, `compliance-evidence`, and `grc-uar-sim-*`). Each engineer deploys, tags, and tears down their own project stack. Every deploy runs from this repo's clean `main` equal to `origin/main`, after approval, under the 340 change-control rule. Nothing deploys from a branch. Engineers author `grc-*` templates in pull requests; see [infrastructure/README.md](infrastructure/README.md) and [shared/access-model/README.md](shared/access-model/README.md). Business stacks (the website, blog, intake, invoicing, account baseline) stay in the private website repo.
- Nothing here publishes anywhere. There is no GitHub Pages site, no package, and no CI pipeline. A merge to `main` is the release.
- Private repo. Private does not mean safe for client data. Anyone with access, every clone, and git history keep whatever is committed.
- Branch flow: this repo takes pull requests straight into `main`. The 340 Collective website repo still has its own `dev` -> `test` -> `main` flow and its own CONTRIBUTING file for the business stacks. If you work in both, follow each repo's own rules and do not carry one flow into the other.

## Data rules (apply to every phase)

Use these classification levels.

| Class | Examples in this work | Allowed in this repo |
| --- | --- | --- |
| Public | Published website copy, public policy statements | Yes |
| Internal | Lab designs, draft policies, procedures, synthetic datasets | Yes |
| Confidential | Real client names, brand forms, listings, footage, invoices, real acknowledgments, real roster entries, unredacted screenshots of real accounts | No |
| Restricted | Credentials, access keys, recovery codes, property or alarm codes, sensitive incident evidence | Never, not even briefly |

Rules:

- No real client or employee data. Ever. Use synthetic records only, built the way `engineering/Abdifatah-08-Access-Reviews/uar-simulation/data/` is: fictional names, `example.com` addresses (reserved by RFC 2606), relative dates, and a README that says the data is synthetic.
- No account IDs, ARNs, bucket names, endpoint URLs, personal email addresses, or person names in new diagrams or new documents, apart from the `infrastructure/` exception below. Refer to roles by function (ISSM, ISSE, ISSO, Auditor), not by person, and to AWS resources by role ("the site bucket").
- Name exception: team assignment pages, folder names, partner lines, and TEAM-style lists may use first names with roles; everything else uses roles.
- `infrastructure/` exception: templates take the account from `AWS::AccountId` (and the partition from `AWS::Partition`, which new templates should use) and never hardcode the account. AWS-managed policy ARNs (for example `arn:aws:iam::aws:policy/SecurityAudit`) are allowed in templates. Templates and `infrastructure/cloudformation/grc-access-model/validate_policies.py` may also name the resources they scope or protect: ARN patterns built from `AWS::AccountId` or a placeholder, stack, bucket, and table names, and API IDs. Runbooks in `infrastructure/runbooks/`, `infrastructure/cloudformation/grc-access-model/README.md`, and the validator's usage text may name the account ID and region. Still no emails, passwords, keys, or personal data anywhere.
- Raw audit evidence (screenshots, exports, credential reports from a real account, signed acknowledgments) stays out of git. Store it where the ISSM designates, outside the repo folder. Nothing in this repo gitignores `private-evidence/`, and an ignored folder would not be an access control or stop `git add -f` anyway.
- Evidence you do commit must be sanitized first: crop or redact account IDs, ARNs, emails, names, IP addresses, and tokens, then check the result by eye.
- Spreadsheets (`*.xlsx`) can hide data, and the text checks in section 4 do not read them. Before committing one, run the spreadsheet check in section 4, then open the file and check every sheet (including hidden ones), comments, and document properties (author, last modified by) for real names by eye.
- No Confidential or Restricted data, and no evidence, in any external AI prompt: chat assistants, coding agents, or "make this synthetic" requests. Use only AI tools the ISSM has approved, and give them only Public or Internal content.
- Real roster entries and acknowledgment evidence go in restricted storage, never in git.

## 1. Plan

Every change starts with an issue, except typo fixes.

- [ ] Open an issue that says what changes, why, which project folder (`engineering/` or `non-engineering/`, `00` to `15`) or policy it touches, the linked Jira Task, and the expected AWS cost impact (usually 0 dollars; stacks deploy only from clean `main`: the ISSM deploys the shared stacks, and each engineer their own project stack).
- [ ] Classify the data the change touches using the table above. If anything is Confidential or Restricted, stop and redesign it with synthetic data.
- [ ] Name the code reviewer, the partner who accepts, and the validator from the separation of duties chain in [GOVERNANCE.md](GOVERNANCE.md). You cannot review, accept, or validate your own work.
- [ ] Keep scope to one project folder or one policy per pull request where possible.
- [ ] If the change touches evidence handling, PII (even synthetic PII), access or identity, or any script, add a lightweight threat model to the issue (below).

### Lightweight threat model

Fill in this table in the issue. Three to five rows is enough.

| Asset | Abuse case (what could go wrong) | Control in this change | Residual risk |
| --- | --- | --- | --- |
| Example: synthetic HR roster | A real person's record is mixed in by copying from a real export | Generate from a fixed seed and built-in name lists; `example.com` only | Low |
| Example: diagram script | A real account ID or bucket name ends up on the rendered PNG | Add the term to `SENSITIVE_EXTRA`; check the `sensitive text: none` output | Low |

Questions to ask:

- Could this expose real client or employee data, or make it easier to expose later?
- Could this grant, widen, or document access that nobody approved?
- Could a script read or write outside its own folder or `/tmp`, call the network, or call AWS?
- Could a reader mistake a draft, proposal, or simulation for an approved control or real evidence?

## 2. Design

- [ ] Follow the two-track folder pattern. `engineering/<Engineer>-<NN>-<Project>/` holds `README.md`, `LAB-STEPS.md` (design, deploy, test, hand off, tear down), `*-Architecture.md`, and `diagram/` with `build_diagram.py` plus the rendered PNG and SVG. `non-engineering/<Partner>-<NN>-<Project>/` holds `README.md`, `LAB-STEPS.md` (requirements, inputs, acceptance, operation, reporting), and any working spreadsheets. Both LAB-STEPS files of a project carry the identical `## Handoffs` list. General lab material goes in `shared/labs/README.md`, never per project.
- [ ] Map findings, evidence, risks, and deviations to the ASFF `SecurityControlId` values in [ASFF-Control-Matrix-Indexed.xlsx](non-engineering/Jason-01-GRC-as-Code-Platform/ASFF-Control-Matrix-Indexed.xlsx).
- [ ] Mark status honestly: target design, draft, simulation, or approved. A merge does not approve a policy. Policy approval is a separate, recorded decision (see section 7).
- [ ] Least privilege in any documented access: name the role, the exact actions, and the resource scope. No wildcards without a written reason.
- [ ] If a required change cannot be made (quota, cost, missing dependency), file a deviation request as described in [GOVERNANCE.md](GOVERNANCE.md) instead of forcing it.

## 3. Implement

- [ ] Work on a branch named `<type>/<short-topic>`, for example `docs/08-uar-notes` or `fix/05-policy-links`. In the GitHub web editor, rename the default `<user>-patch-N` branch before you propose the change.
- [ ] Never commit directly to `main`.
- [ ] No secrets inline: no keys, tokens, passwords, or recovery codes in docs, scripts, examples, or commit messages. Use placeholders such as `<from private roster>`.
- [ ] Validate input in any script: check arguments and file paths, write output only to the path given (the diagram kits default to `/tmp`), and fail with a clear message.
- [ ] Scripts make no network or AWS calls unless the issue approved it. The diagram kits are offline after `--setup`.
- [ ] Pin exact dependency versions (`package==1.2.3`). The diagram kits pin `diagrams==0.25.1`; keep it.
- [ ] No new third-party scripts, packages, GitHub Actions, or external embeds without ISSM approval recorded in the issue.
- [ ] Synthetic data only, generated reproducibly, with a README stating it is synthetic.
- [ ] Accessibility for anything rendered: give every image meaningful alt text in Markdown, keep the legend in text (not only in color), use table header rows, and keep the diagram kit's contrast and font sizes.
- [ ] Plain words, no em or en dashes (the diagram checks and existing docs follow this).

## 4. Test

There is no CI. You run these checks yourself and paste the output into the pull request. Every command below exists and was run against this repo. None of them write inside the repo, and none call AWS except the read-only `validate-template` in the `infrastructure/` block.

Run from the repo root on your branch, after committing.

0. Update `origin/main` first, so every diff below is computed against the current `main`:

   ```bash
   git fetch origin
   ```

   Expected: no errors. A stale `origin/main` can hide changes from the checks or flag commits that are already merged.

1. Whitespace errors in the diff:

   ```bash
   git diff --check origin/main...HEAD
   ```

   Expected: no output.

2. File names that should never be committed:

   ```bash
   git diff --name-only origin/main...HEAD | grep -iE '(^|/)\.env|\.pem$|\.key$|id_rsa|private-evidence/|secret'
   ```

   Expected: no output. (The tracked `aws-credential-report.csv` is synthetic; a new file with "credential" in the name needs a reason in the PR.)

3. Secrets and identifiers in added lines:

   ```bash
   git diff origin/main...HEAD -U0 | grep -E '^\+' | grep -nE 'AKIA|ASIA|BEGIN [A-Z ]*PRIVATE KEY|[0-9]{12}|arn:aws|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
   ```

   Expected: no output, or only `example.com` addresses in synthetic data. Explain every other hit or remove it. If you changed `infrastructure/`, expected hits are the account ID inside `infrastructure/runbooks/`, `infrastructure/cloudformation/grc-access-model/README.md`, and the validator's usage text, and ARNs in templates and the validator (AWS-managed policy ARNs and resource ARN patterns; the `infrastructure/` exception in the data rules). Name them in the PR.

   This check reads text diffs only. It does not see inside `*.xlsx` or other binary files.

4. Spreadsheet contents, if you added or changed a `*.xlsx` file (offline; reads the file's XML with `unzip`):

   ```bash
   git diff --name-only --diff-filter=AM origin/main...HEAD -- '*.xlsx' | while IFS= read -r f; do unzip -p "$f" | grep -aoE 'AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|arn:aws[^<" ]*|(^|[^0-9.])[0-9]{12}([^0-9.]|$)|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|<dc:creator>[^<]*|<cp:lastModifiedBy>[^<]*|<sheet [^>]*state="(hidden|veryHidden)"' | sort -u | sed "s|^|$f: |"; done
   ```

   Expected: only `example.com` addresses in synthetic data, and `dc:creator` or `cp:lastModifiedBy` lines that are empty or name a tool (for example `openpyxl`), not a person. Any hidden sheet, account ID, ARN, key, or other address needs a reason in the PR or must be removed. This scan cannot recognize a real person's name typed into a cell, so the by-eye review in the data rules is still required.

5. Em and en dashes in changed text files:

   ```bash
   git diff --name-only --diff-filter=AM origin/main...HEAD -- '*.md' '*.csv' '*.py' | xargs perl -CSD -ne 'print "$ARGV:$.: $_" if /[\x{2013}\x{2014}]/; close ARGV if eof'
   ```

   Expected: no output.

6. Relative links in every tracked Markdown file (outside `.agents/`) point to files that exist, including image and HTML links:

   ```bash
   python3 shared/check_links.py
   ```

   Expected: a final line `checked N links in M files, 0 broken`, exit 0. Each broken link prints as `<file>: broken link <target>`. Run it from the repo root; it refuses other folders.

7. Python syntax for every script (does not write `__pycache__`):

   ```bash
   python3 -c 'import ast, sys; [ast.parse(open(p).read(), p) for p in sys.argv[1:]]; print("parsed", len(sys.argv) - 1, "files")' $(git ls-files '*.py')
   ```

   Expected: `parsed N files`.

8. If you changed a diagram, rebuild it to `/tmp` first and read the checks:

   ```bash
   python3 engineering/<folder>/diagram/build_diagram.py --setup   # once per machine; installs diagrams==0.25.1 into ~/.aws_diagram_venv
   python3 engineering/<folder>/diagram/build_diagram.py /tmp/<NN>-check
   ```

   Expected: `crossings: 0`, `layout problems: none`, `sensitive text: none`. Open the PNG and check it by eye. Then copy the PNG and SVG into the folder under the existing file names. The governance diagram has no `--setup`; run it with the same venv: `~/.aws_diagram_venv/bin/python shared/governance-diagram/grc-governance_build.py /tmp/grc-governance-check`.

If you changed `infrastructure/`, also run these. `validate-template` is a read-only AWS call; the rest are offline.

```bash
python3 -m venv /tmp/grc_cfnlint && /tmp/grc_cfnlint/bin/pip install -q cfn-lint==1.57.2   # once per machine
/tmp/grc_cfnlint/bin/cfn-lint infrastructure/cloudformation/*.yaml
aws cloudformation validate-template --template-body file://infrastructure/cloudformation/<file>.yaml --profile 340collective --region us-east-1
(cd infrastructure && /tmp/grc_cfnlint/bin/python cloudformation/grc-access-model/validate_policies.py --account-id <account> --region us-east-1 --engineer <user> --analyst <user> --skip-aws)
wc -c < infrastructure/cloudformation/<file>.yaml
```

Expected: cfn-lint prints nothing, validate-template returns its parameter list with no error, the validator ends with `RESULT: all checks passed`, and every template is under 51,200 bytes (the inline template limit).

9. Confirm the working tree holds nothing you did not mean to change:

   ```bash
   git status --short
   ```

## 5. Commit hygiene

- [ ] Conventional messages: `docs(08): add UAR worksheet notes`, `fix(05): correct policy links`, `chore: ...`, `feat(12): ...`.
- [ ] Signed off: `git commit -s`. In the GitHub web editor, add a `Signed-off-by: Your Name <your-github-noreply-address>` line to the extended description. Use your GitHub noreply address, not a personal one.
- [ ] Stage files by name (`git add path/to/file`). Never `git add .` or `git add -A`.
- [ ] Small pull requests: one project folder or one policy. Split anything over about 400 changed lines of text.
- [ ] No secrets, no evidence files, no real client or employee data in any commit. Deleting a file in a later commit does not remove it from history. If it happens, follow Incident and rollback below.

## 6. Pull request and review

- [ ] Open the pull request against `main`. The template in [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) loads automatically. Fill in every section.
- [ ] Link the issue. Paste the output of every Test command you ran, and say which ones you did not run and why.
- [ ] Say whether AI assisted, and what the agent did.
- [ ] Link the Jira Task for the handoff (the PR template's "Jira issue" line). The pull request merges only after that Task shows the partner's acceptance.
- [ ] Required review chain (see [GOVERNANCE.md](GOVERNANCE.md)): code review by another engineer in GitHub, partner acceptance in Jira, ISSO validation in Jira, then final approval by the ISSM (@aboutfaris), or by Adam (ISSO) for Faris-built work (foundation, 01, 11, 00). Adam and Jason record their parts in Jira; they do not review pull requests.
- [ ] Code owners: [.github/CODEOWNERS](.github/CODEOWNERS) lists engineers only. Every line includes the ISSM, and each project folder adds its engineer and code reviewer. Placeholders such as `@TODO-maria-github` stand in until a GitHub username is known. This repo is private on a GitHub plan that does not enforce code owners or branch protection, so GitHub will not block a merge by itself. The rule is enforced by process: only the ISSM merges.
- [ ] Reviewers check the data rules, the threat model, and the pasted test output, not just the prose.

### Labels and project board (owner sets up)

These are GitHub settings, not files in the repo. The owner creates them; contributors apply them to issues and pull requests.

- `track:engineering` and `track:non-engineering`: which folder the change touches.
- `phase:1`, `phase:2`, `phase:3`, `phase:4`, `phase:5`: the build phase from GOVERNANCE.md.
- `project:00` to `project:15`: one label per project number.
- A project board with one column per review step: build, code review, partner acceptance, ISSO validation, final approval, merged.

## 7. Release

- A merge to `main` by the ISSM is the release. Contributors do not merge or force push. The only tags are `live-YYYY-MM-DD` deploy tags, set by whoever ran the deploy.
- Policy approval is a separate human decision, recorded in writing. Only approved policies move to `1.0.0`, with real effective dates.
- Anything that has to happen in AWS deploys only from this repo's clean `main` equal to `origin/main`, after the pull request is merged and approved, under the 340 change-control rule, following [infrastructure/README.md](infrastructure/README.md). The ISSM deploys the shared stacks; each engineer deploys and tears down their own project stack. Nothing deploys from a branch or by hand.

## 8. Post-change verification

After merge, the author confirms and comments on the issue:

- [ ] `git fetch origin && git log --oneline -1 origin/main` shows the merge.
- [ ] Rendered Markdown on GitHub shows the images and the links work.
- [ ] No unintended files arrived on `main` (`git show --stat origin/main`).
- [ ] Close the issue with a one-line summary.

## 9. Incident and rollback

Bad content (wrong, broken, misleading, but not sensitive):

1. Open an issue.
2. Fix forward with a new pull request, or ask the ISSM to revert the merge (`git revert -m 1 <merge-commit>` on a branch, then a PR). No force pushes.

Sensitive content committed or pushed (real client or employee data, a secret, unredacted evidence):

1. Stop. Do not push again, do not try to rewrite history yourself, and do not paste the content into issues, PRs, or chat.
2. Tell the ISSM privately right away, as described in [SECURITY.md](SECURITY.md). Say the file path, commit, branch, and when it was pushed. Do not repeat the data.
3. If it is a credential, the owner of that credential revokes or rotates it first. Removal from git does not make a leaked secret safe.
4. The ISSM decides on history rewriting, asks collaborators to delete stale clones and forks, and handles the incident.
5. Raw evidence of the incident goes to restricted storage, never into this repo.

## 10. Forbidden

- Committing to `main`, force pushing, or merging your own pull request.
- Real client, property, payment, employee, or collaborator data, including in "temporary" commits.
- Secrets of any kind, `.env` files, keys, credential files from a real account.
- Raw or unredacted audit evidence, and `git add -f` on anything in `private-evidence/`.
- Pasting Confidential or Restricted data, client or employee data, or any evidence into an external AI tool, or using an AI tool the ISSM has not approved.
- Account IDs, ARNs, bucket names, endpoint URLs, or personal emails in new docs or diagrams (outside the `infrastructure/` exception), or person names outside the name exception.
- Deploying from a branch or by hand, or deploying a shared stack unless you are the ISSM. Stacks deploy only from this repo's clean `main` after merge.
- Running AWS write commands, deploys, or console changes before the change is merged (a project stack deploys only after merge, as above).
- New third-party scripts, packages, Actions, or embeds without ISSM approval.
- Disabling or skipping checks, git hooks, or the diagram kit's built-in checks.
- Marking a draft, proposal, or simulation as approved, or backdating, signing for someone else, or inventing acknowledgments.
