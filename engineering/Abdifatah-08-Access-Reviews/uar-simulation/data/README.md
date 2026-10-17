# Synthetic UAR Data
Everything in this folder is synthetic. The people are fictional, generated from built-in name lists. Every email address uses example.com, the domain reserved for documentation by RFC 2606. Every date is relative to the review date, 2026-10-01. The files were generated with a fixed seed, so they are identical every time they are regenerated.

| File | Source system it imitates | Join keys |
| --- | --- | --- |
| hr-roster.csv | HR system of record. Source of truth for status, department, title, manager, and dates. Contractors are governed by contract_end_date | employee_id, email |
| aws-credential-report.csv | IAM credential report, same 22 columns in the same order as the real report. The authoritative source for credential activity and age for `/uar-sim/` users | user (IAM user name) |
| okta-users.csv | Okta user export with app assignments (semicolon separated) | employeeNumber, login, email |
| github-collaborators.csv | GitHub organization members and outside collaborators | login, email (blank for some outside collaborators) |
| jira-users.csv | Jira user export | email |
| role-access-baseline.csv | Expected access per department, level, and title (lists are semicolon separated) | department, title |
| access-requests.csv | Access request and approval log from the ticketing system | requester and approver to hr-roster.csv employee_id; beneficiary to the IAM user name and worksheet Identity |
| exceptions-register.csv | Register of approved exceptions to the access standard | identity to the IAM user name and worksheet Identity; approver to hr-roster.csv employee_id |
| uar-worksheet.xlsx | The 08 certification worksheet, one row per identity, with README and Remediation Log sheets | Identity, Employee ID |

The IAM users, groups, policies, roles, and tags are in AWS under the `/uar-sim/` path. The IAM `employee-id` tag joins users to hr-roster.csv.

## Which source is authoritative
- aws-credential-report.csv is authoritative for passwords, MFA, and access key age and use. The live IAM credential report shows no passwords, MFA, or keys for `/uar-sim/` users, because the simulation keeps them powerless.
- Live IAM is authoritative for structure and entitlements: users, groups, memberships, policies and their documents, roles and trust policies, and tags.
- hr-roster.csv is authoritative for people, status, and dates.

## access-requests.csv columns
| Column | Meaning |
| --- | --- |
| request_id | Request identifier (REQ-) |
| requester | employee_id of the person who raised the request |
| beneficiary | Identity that receives the access (IAM user name, or Okta login when there is no IAM user) |
| entitlement | What was requested: `aws:group:<name>`, `aws:policy:<name>`, `aws:role:<name>`, `aws:access-key`, `aws:console`, `okta:app:<app>`, `github:<permission>`, `jira:<role>`, or `contract-extension` |
| justification | Business reason given |
| approver | employee_id of the approver (blank while pending) |
| approved_at | When it was approved (blank unless approved) |
| expires_at | Date the approval ends (blank when it does not expire) |
| ticket_ref | Ticket number (ITSM-) |
| status | approved, rejected, cancelled, or pending |

## exceptions-register.csv columns
| Column | Meaning |
| --- | --- |
| exception_id | Exception identifier (EXC-) |
| identity | Identity the exception covers |
| control | The single NIST SP 800-53 control the exception covers: AC-2, AC-2(3), AC-5, AC-6, IA-2(1), or IA-5 |
| reason | Why the exception was granted |
| compensating_control | What reduces the risk meanwhile |
| approver | employee_id of the approver |
| granted_at, expires_at | Start and end dates |
| status | active, expired, or closed |

## Company access standard (excerpt)
- Every console password has MFA. Groups granting Admin, PowerUser, payment approval, change approval, or HR record access attach the MFA enforcement policy `uar-sim-require-mfa`.
- Access keys are for service accounts, or for a person with an approved access request. Keys are rotated within 90 days. One active key per identity, except during a rotation window covered by an exception.
- Service accounts have no console password.
- 90 days without console or key activity means disable, unless an active, unexpired exception covers it.
- Admin and PowerUser console passwords are changed at least every 365 days. Standard users follow NIST SP 800-63B: no forced periodic change.
- Accounts may be provisioned up to 7 days before hire_date, with an approved request.
- Anything beyond role-access-baseline.csv needs an approved, unexpired request whose approver is neither the beneficiary nor the requester and was employed when approving; or an active, unexpired exception naming that control.
- Policies granting write access to payment or HR data restrict `aws:SourceIp` to 203.0.113.0/24 or `aws:RequestedRegion` to us-east-1.
