# Code of conduct

How we work together on GRC Projects. These are team working norms, not a legal document. Roles, approvals, and separation of duties are in [GOVERNANCE.md](GOVERNANCE.md). How a change gets into the repo is in [CONTRIBUTING.md](CONTRIBUTING.md).

## How we work

- One active build per engineer at a time, time-boxed to 7 days. Finish, get your partner's sign-off on the final report, and hand the build over to operation before you start the next one. The build stays running; it is not torn down at phase end. Monday 2026-10-19 is the official start; the weekend before is prep.
- If a build is at risk by day 4, flag it in Jira. Faris then either cuts scope or grants one 3-day extension. No weekend catch-up.
- Where things go: Jira for phases, timelines, assignments, day-to-day comments, blockers, and sign-off. GitHub for code, templates, architecture, diagrams, lab steps, and the final report. LinkedIn messages or group chat for general communication, quick pings, and high-level updates, never for account details, findings, evidence, or credentials.
- Ask your partner directly or comment on the project item. Say what you need and give a due date.
- AI tools are allowed. Follow the SSDLC in CONTRIBUTING.md and AGENTS.md, work on a branch in your own copy of the repo, and never merge without another person's review.
- Only change files in your own project folders (`engineering/<You>-NN-...` or `non-engineering/<You>-NN-...`). Shared files (root docs, `shared/`, `infrastructure/`) change only through Faris.
- You may describe your own projects on a resume or LinkedIn as project work or work experience, using your FINAL-REPORT before-and-after metrics. Never share account IDs, ARNs, internal URLs, evidence, or real client data. Describe roles and outcomes.
- Respond to partner questions and reviews within 2 working days. This is a default, and the team can change it.
- Findings are blameless. A finding is about a control or a design, never about a person.
- Raise overload early with Faris (ISSM). Moving work to someone else is normal and is not a failure.

## How we treat each other

- Be respectful and inclusive in every channel: GitHub, Jira, chat, and meetings.
- Disagree about the work, not the person. Explain your reasons and listen to theirs.
- Never share anyone's personal data or credentials, in the repo, in Jira, in chat, or in an AI tool.
- Use first names with roles only where the naming rule in CONTRIBUTING.md allows it; everywhere else, refer to roles.

## Report a conduct concern

Tell Faris (ISSM) privately, through the team's direct channel. If the concern involves Faris, tell David (Business Owner) privately instead. Say what happened and when; you do not need proof to raise it. Concerns are handled privately, and raising one in good faith never counts against you.

A security issue or a data exposure is not a conduct concern. Report it as described in [SECURITY.md](SECURITY.md).
