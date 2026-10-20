# Project 06 Requirements: Evidence Automation (Adam, ISSO)

Jira epic: GRC-7. Partner: Adam (ISSO). Engineer: Maria (Automation Engineer). Agreed at the Day 1 kickoff, pending ISSM acceptance.

## Folder structure (one per control family)
access-control/, logging/, encryption/, configuration/, monitoring/, change-management/, backup/

## Naming rule
`<ControlID>_<evidence>_<YYYY-MM-DD>`

## Index columns
Control ID, Control Description, Evidence Item, Source System, Collection Date, Collected By, File Name, Reviewer

## First-wave controls and freshness
| Priority | Evidence | Source | Freshness | Control ID |
|---|---|---|---|---|
| 1 | IAM credential report | AWS IAM | Monthly | CCF-IAC-17 |
| 2 | MFA settings | AWS IAM / Identity Center | Weekly | CCF-IAC-06 |
| 3 | CloudTrail trail status | AWS CloudTrail | Daily | CCF-MON-02 |
| 4 | S3 encryption settings | Amazon S3 | Weekly | CCF-CRY-05 |
| 5 | AWS Config compliance summary | AWS Config | Daily | CCF-CFG-02 |
| 6 | Security standard scores | AWS Security Hub | Weekly | CCF-MON-01 |

## Redaction rule
Account IDs, ARNs, and resource names are redacted before files enter the folder.

## Note
CCF-CFG-02.2 (Automated Central Management & Verification) may be a closer match for AWS Config. CFG-02 is used for consistency; open to adjusting.
