## Summary

What changes and why. Link the issue: Closes #

Jira issue (required): link the Handoff Task that records the partner's acceptance. This pull request merges only after that Task shows acceptance.

Track: engineering / non-engineering / shared / infrastructure / root docs
Phase: 1 / 2 / 3 / 4 / not phase work
Project folder (for example `engineering/Maria-06-Evidence-Automation/`) or policy:
Change type: docs / policy draft / synthetic data / diagram / script / infrastructure / governance tracker / other

## Plan and design

- [ ] An issue exists and is linked
- [ ] The Jira issue line above links the acceptance Task
- [ ] Scope is one project folder or one policy
- [ ] Expected AWS cost impact stated (only the ISSM deploys `infrastructure/`, from clean `main` after merge; usually 0 dollars)
- [ ] Code reviewer named (another engineer; see GOVERNANCE.md separation of duties):
- [ ] Partner acceptance recorded in Jira (partner named):
- [ ] ISSO validation recorded in Jira
- [ ] Threat model in the issue, if this touches evidence, PII (even synthetic), access, identity, or a script
- [ ] Status labeled honestly (target design, draft, simulation, approved)

## Security and privacy impact

Describe any effect on access, evidence handling, or data exposure. Write "None" if there is none.

Highest data classification touched (see the data rules in CONTRIBUTING.md):

- [ ] Public
- [ ] Internal
- [ ] Confidential (not allowed in this repo; explain how it was removed or replaced)
- [ ] Restricted (not allowed in this repo; stop and see SECURITY.md)

## Data confirmation

- [ ] No real client, property, payment, employee, or collaborator data
- [ ] Any sample data is synthetic, uses example.com, and has a README saying so
- [ ] No secrets, keys, tokens, or `.env` / credential files
- [ ] No raw or unredacted evidence; nothing from `private-evidence/`
- [ ] No account IDs, ARNs, bucket names, endpoint URLs, or personal emails added, and person names only where the name exception allows
- [ ] Spreadsheets checked for hidden sheets, comments, and author properties
- [ ] Images have alt text; diagrams pass the kit's `sensitive text: none` check

## Implementation

- [ ] Branch is not `main`; branch name is `<type>/<short-topic>`
- [ ] No new packages, third-party scripts, Actions, or embeds (or ISSM approval linked)
- [ ] Any dependency is pinned to an exact version
- [ ] Scripts write only to their given output path and make no network or AWS calls
- [ ] Commits are conventional, signed off, and staged by name
- [ ] No em or en dashes

## Infrastructure (if infrastructure/ changed)

- [ ] cfn-lint clean (paste below)
- [ ] `validate-template` OK for each changed template (paste below)
- [ ] `validate_policies.py --skip-aws`, run from `infrastructure/`, prints `RESULT: all checks passed` (paste below)
- [ ] Each template is under 51,200 bytes (paste `wc -c` below)
- [ ] No hardcoded account ID (templates use `AWS::AccountId`; new templates also use `AWS::Partition`)
- [ ] Stack name is `grc-*` or `compliance-evidence`
- [ ] Deploy only by the ISSM, from clean `main`, after merge

## Tests run (CONTRIBUTING.md section 4)

Paste each command and its output. Mark any check not run, with the reason.

```text
$ git fetch origin

$ git diff --check origin/main...HEAD

$ (file name check)

$ (secrets and identifier check)

$ (spreadsheet check, if .xlsx changed)

$ (dash check)

$ python3 shared/check_links.py

$ (python syntax check, if .py changed)

$ (diagram rebuild to /tmp, if a diagram changed)

$ (infrastructure checks, if infrastructure/ changed: cfn-lint, validate-template, validate_policies --skip-aws, wc -c)

$ git status --short

```

## AI assistance

- [ ] No AI assistance
- [ ] AI assisted (complete below and follow AGENTS.md)

Tool or agent used:

What the agent did (files changed and why):

What was verified, and how:

What was not verified, and why:

## Review

- [ ] Code review by another engineer, in GitHub
- [ ] Partner acceptance, in Jira (linked above)
- [ ] ISSO validation, in Jira
- [ ] Final approval: ISSM (@aboutfaris), or Adam (ISSO) for Faris-built work (foundation, 01, 00). Only the ISSM merges.
