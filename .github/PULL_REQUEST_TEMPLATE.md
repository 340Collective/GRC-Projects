## Summary

What changes and why. Link the issue: Closes #

Project folder or policy:
Change type: docs / policy draft / synthetic data / diagram / script / governance tracker / other

## Plan and design

- [ ] An issue exists and is linked
- [ ] Scope is one project folder or one policy
- [ ] Expected AWS cost impact stated (nothing deploys from this repo; usually 0 dollars)
- [ ] Independent validator named (see GOVERNANCE.md separation of duties):
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
- [ ] No account IDs, ARNs, bucket names, endpoint URLs, personal emails, or person names added
- [ ] Spreadsheets checked for hidden sheets, comments, and author properties
- [ ] Images have alt text; diagrams pass the kit's `sensitive text: none` check

## Implementation

- [ ] Branch is not `main`; branch name is `<type>/<short-topic>`
- [ ] No new packages, third-party scripts, Actions, or embeds (or ISSM approval linked)
- [ ] Any dependency is pinned to an exact version
- [ ] Scripts write only to their given output path and make no network or AWS calls
- [ ] Commits are conventional, signed off, and staged by name
- [ ] No em or en dashes

## Tests run (CONTRIBUTING.md section 4)

Paste each command and its output. Mark any check not run, with the reason.

```text
$ git fetch origin

$ git diff --check origin/main...HEAD

$ (file name check)

$ (secrets and identifier check)

$ (spreadsheet check, if .xlsx changed)

$ (dash check)

$ (relative link check)

$ (python syntax check, if .py changed)

$ (diagram rebuild to /tmp, if a diagram changed)

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

- [ ] Independent validator reviewed
- [ ] ISSM (@aboutfaris) approval. Only the ISSM merges.
