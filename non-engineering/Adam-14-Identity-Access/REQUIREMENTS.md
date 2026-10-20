# Project 14 Requirements: Okta Group Model and App Assignment Rules (Adam, ISSO)

Jira epic: GRC-15. Partner: Adam (ISSO). Engineer: Abdifatah (IAM / Identity Engineer). Agreed at the Day 1 kickoff, pending ISSM acceptance.

## Okta groups (one person per group)
| Group | Member |
|---|---|
| GRC-ISSM | Faris |
| GRC-ISSE | Rasheed, Maria |
| GRC-ISSO | Adam |
| GRC-IAM | Abdifatah |
| GRC-Auditor | Jason |
| GRC-Stakeholder | David |

## App assignment rules
| Group | AWS | GitHub | Jira | Bookmarks |
|---|---|---|---|---|
| GRC-ISSM | No (admin identity stays outside Okta) | Yes | Yes | Yes |
| GRC-ISSE | Yes | Yes | Yes | Yes |
| GRC-ISSO | Yes | Yes | Yes | Yes |
| GRC-IAM | Yes | Yes | Yes | Yes |
| GRC-Auditor | Yes (read-only) | Open question | Yes | Yes |
| GRC-Stakeholder | Yes (read-only) | No | Yes | Yes |

## Rules
- Tiles only link to apps; permissions stay inside each app.
- No SSO by design; each app keeps its own MFA, and Okta Verify MFA is required.
- Access changes need a PR approved by the ISSM. Leavers are removed the same day.
- Group membership is re-checked in the quarterly 08 access review.

## Validation plan
Sign in through Okta and confirm my tiles match GRC-ISSO; compare the Okta group and app-assignment export against these rules; review the joiner/mover/leaver test evidence; record results or findings on the project item.

## Open questions
1. Maria's group (GRC-ISSE or separate)?
2. Does the Auditor need read-only GitHub?
3. Which bookmark tiles for everyone?
