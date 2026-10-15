# Synthetic UAR Data
Everything in this folder is synthetic. The people are fictional, generated from built-in name lists. Every email address uses example.com, the domain reserved for documentation by RFC 2606. Every date is relative to the review date, 2026-10-01. The files were generated with a fixed seed, so they are identical every time they are regenerated.

| File | Source system it imitates | Join keys |
| --- | --- | --- |
| hr-roster.csv | HR system of record. Source of truth for status, department, title, manager, and dates. Contractors are governed by contract_end_date | employee_id, email |
| aws-credential-report.csv | IAM credential report, same 22 columns in the same order as the real report. The authoritative activity history for `/uar-sim/` users | user (IAM user name) |
| okta-users.csv | Okta user export with app assignments (semicolon separated) | employeeNumber, login, email |
| github-collaborators.csv | GitHub organization members and outside collaborators | login, email (blank for some outside collaborators) |
| jira-users.csv | Jira user export | email |
| role-access-baseline.csv | Expected access per department, level, and title (lists are semicolon separated) | department, title |
| uar-worksheet.xlsx | The 08 certification worksheet, one row per identity, with README and Remediation Log sheets | Identity, Employee ID |

The IAM users themselves, with their groups, policies, and tags, are in AWS under the `/uar-sim/` path once deployed. The IAM `employee-id` tag joins them to hr-roster.csv.
