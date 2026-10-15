# 340 Collective policy management lab

**Pack version:** 0.2.0

**Updated:** 2026-10-15

**State:** Website-aligned drafts; policy approval, named-role acceptance and real collaborator acknowledgments remain pending.

340 Collective is the subject organisation: a Las Vegas media studio focused on real-estate and agent-brand content. This revision covers the workflow from client enquiry and brand brief through capture, editing, delivery and any contracted account-management services. It preserves the manual lab boundary. Nothing here deploys to live infrastructure or changes the public website.

## Contents

| Policy ID | Document | Current version |
| --- | --- | --- |
| 340-ISP-001 | [Information Security](policies/340-ISP-001-information-security.md) | 0.2.0 |
| 340-AUP-001 | [Acceptable Use](policies/340-AUP-001-acceptable-use.md) | 0.2.0 |
| 340-ACP-001 | [Access Control](policies/340-ACP-001-access-control.md) | 0.2.0 |
| 340-VMP-001 | [Vendor Management](policies/340-VMP-001-vendor-management.md) | 0.2.0 |
| 340-IRP-001 | [Incident Response](policies/340-IRP-001-incident-response.md) | 0.2.0 |
| 340-DRP-001 | [Data Retention](policies/340-DRP-001-data-retention.md) | 0.2.0 |

- [Policy lifecycle workbook](340-Collective-Policy-Lifecycle.xlsx): editable attestation tracker and review schedule.
- [Website alignment](governance/website-alignment.md): source links, confirmed public statements, proposed controls and open inconsistencies.
- [Acknowledgment procedure](governance/attestation-procedure.md): genuine-response collection and evidence requirements.
- [Review-cycle schedule](governance/review-cycle-schedule.md): review responsibilities, provisional dates and event triggers.
- [Attestation CSV](governance/attestation-tracker.csv), [review CSV](governance/review-cycle-schedule.csv), [roster CSV](governance/collaborator-roster.csv) and [approval template](governance/approval-record-template.md).

The workbook is the working tracker. CSVs and the Markdown schedule are snapshots; update them together when publishing a tracker revision. If the team instead uses Google Sheets, designate one controlled workbook as authoritative. Do not maintain competing live trackers.

## What changed from 0.1.0

- Replaced the generic organisational context with the studio's real-estate media workflow, directly managed crew and limited AI-support model.
- Proposed policy responsibilities using the public leadership roles: David C. for studio approval/production decisions and Faris N. for operations/security coordination. These are proposals, not accepted appointments or approvals.
- Added protection for capture media, unpublished listings, client footage, releases, property codes, delivery links and contracted client-account access.
- Aligned ordinary access logs to the published 90-day maximum and raw-media handling to a proposed 60-day operational default based on the FAQ's approximate window.
- Removed the UK-specific invoice-retention rationale. Proposed seven-year accounting retention now requires U.S. accountant/legal validation; other unpublished periods remain explicit proposals.
- Added the public incident/privacy intake route and media-specific scenarios. Routine customer response times do not delay urgent security escalation.
- Recorded conflicting renewal/response wording and unverified checkout activation for team resolution.

## Decisions required before approval

| Area | Confirmed basis | Still required |
| --- | --- | --- |
| Business | Published Las Vegas media studio and Nevada customer terms | Legal entity, tax status and applicable obligations in other markets. |
| People | Public CEO & Founder David C.; Strategy & Operations Lead Faris N. | Their acceptance of proposed policy responsibilities, a deputy and technical administrator. |
| Lab collaborators | No complete participant roster or acknowledgments supplied | Identify the actual lab team. Public staff names are not a complete attestation population. |
| AWS | Lab requirement: IAM Identity Center with MFA for routine human access | Actual identity source, accounts, permissions and control evidence. |
| Other services | Cloudflare analytics, Google Meet and Stripe are publicly named | Exact accounts, configuration, processing, vendor approvals and live payment status. |
| Retention | Public raw-file and access-log statements | Working deletion/backup controls, client terms and validation of all proposed periods. |
| Incident readiness | Public help@340collective.com intake | Tested urgent route, fallback, coverage, deputies and notification decision process. |
| Policy dates | No policy effective yet; annual dates provisionally 2027-10-15 | Actual approval/effective dates and reviews 12 months after approval. |

## Complete the lab

1. Validate the operating details and open decisions in the alignment note. Keep unverified controls and unresolved gaps visible.
2. Have the named reviewer assess each policy and the authorised approver record the decision. Issue first approved versions as 1.0.0 with actual effective dates and approval evidence.
3. Commit the exact approved content and record its release reference. A Git commit, tag or merge does not itself prove approval.
4. Confirm the collaborator roster, then request each person's own acknowledgment of the exact approved policies. Use one row per person, policy and version. Keep dates and methods blank until genuine evidence is received and checked.
5. Reconcile every in-scope collaborator against all six current approved versions. Flag missing, duplicate, stale or unsupported entries. Coverage remains unknown until the roster is complete.
6. Check due dates and outstanding acknowledgments monthly. Review policies annually and start a review within 10 business days of a material change, with a recorded completion date.

Draft-review feedback is not acknowledgment of an effective policy. The website's customer acceptance wording does not replace explicit collaborator policy acknowledgment. Do not backdate, sign for someone else or treat silence as a response.

## Version control and privacy

Keep policy IDs and filenames stable. Use `0.x.y` for drafts, `1.0.0` for first approval, a minor increment for changed obligations and a patch increment for editorial corrections. Preserve previous releases and change-log entries.

The included `340-collective-policy-history.bundle` contains the initial 0.1.0 baseline and this 0.2.0 revision, with corresponding `policy-pack-draft-v0.1.0` and `policy-pack-draft-v0.2.0` tags. Commit authorship is labelled drafting support and is not a human policy approval. Reconstruct the repository from the extracted pack:

```bash
git clone 340-collective-policy-history.bundle 340-collective-policy-work
cd 340-collective-policy-work
git log --oneline --decorate
```

For an existing team repository, import the desired files through its normal review process. Restrict completed trackers, roster and evidence. Use synthetic client/property/media records in the lab. Keep real client data, property codes, credentials, signatures and acknowledgment originals out of public history. An ignored evidence folder is not an access-control boundary.

Completion requires six approved policy versions, a complete roster, valid acknowledgments for every in-scope person and assigned dated reviews. The draft pack and tracker structure are prepared; those human decisions and responses remain open.
