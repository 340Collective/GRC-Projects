# Security policy

## Scope

This repo holds GRC documentation, policy drafts, governance trackers, diagram scripts, and synthetic data, laid out as `engineering/` (one folder per project for the engineer who builds it), `non-engineering/` (the same projects for the partner who accepts and operates them), `shared/` (the lab guide, access model notes, and governance diagram), and `infrastructure/` (the GRC CloudFormation templates, policy validator, and runbooks, deployed only by the ISSM from clean `main`). Issues with the rest of the 340 Collective AWS environment or the website belong to the private website repo, but you can still report them through the route below.

## Report a vulnerability privately

Do not open a public or team-visible issue, pull request, discussion, or comment about a vulnerability. Do not include exploit details or sensitive values in commit messages.

This repo is private, and GitHub private vulnerability reporting is not available for it. Report directly to the repo owner and ISSM, GitHub user @aboutfaris:

1. Send a private message to the ISSM: use the team's direct channel, or a direct message to @aboutfaris reached from the GitHub profile. This is the only route for details.
2. If you have no direct channel, send only a short "please contact me privately about a security issue in GRC-Projects" note to the published 340 Collective intake address, help@340collective.com. That address is a shared, public intake mailbox. Put no exploit details, no secret or credential location, and no personal data in that note. Wait for the ISSM to reach you privately, then report.
3. In the private report, include: what you found, where (file path, commit, or system), how you found it, and the impact you expect. Describe secrets or personal data by type and location only. Do not paste the value.
4. Wait for the ISSM to acknowledge before you share the finding with anyone else.

Examples worth reporting: a secret or credential in the repo or its history, a script that calls the network or AWS unexpectedly, documented access that is broader than GOVERNANCE.md allows, or a diagram or doc that reveals account identifiers.

## Report accidental exposure of client or employee data

If real client, property, payment, employee, or collaborator data, a secret, or unredacted audit evidence was committed or pushed:

1. Stop. Do not push more commits to fix it, do not rewrite history yourself, and do not copy the data into a report, issue, or chat.
2. Tell the ISSM privately right away (same route as above; through the public intake address, send only the "contact me privately" note). Give the file path, commit hash, branch, and the time it was pushed. Say what kind of data it is, not the data itself.
3. If a credential is involved, its owner revokes or rotates it immediately. Deleting it from git does not make it safe.
4. The ISSM handles containment, any history rewrite, clone and fork cleanup, and any notification decision. Any evidence of the incident is kept in restricted storage, not in this repo.

Reporting fast matters more than being certain. Report a suspected exposure even if you are not sure.
