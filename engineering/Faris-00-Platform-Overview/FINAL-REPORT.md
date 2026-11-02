# Final report: 00 GRC Platform Overview

Engineer: Faris. Partner: Adam (accepts, since Faris wrote it). Covers: Phase 1 (Oct 19 to 25) and Phase 2 (Oct 26 to Nov 1), both now past their due date as of this report. Jira epic: GRC-1.

This is the first phase build list 00 has produced. No prior report existed to compare against; status below comes from the actual GitHub record (pull requests, tags, issues), not from intent or from what a project's README says it plans to do.

## 1. Summary

00 has no stack of its own. Its deliverable this phase is this report: one record of what Phases 1 and 2 actually delivered, read from merged pull requests and `live-YYYY-MM-DD` tags rather than assumed from each project's requirements document.

## 2. Phase build list (format defined in REQUIREMENTS.md Section 2)

### Phase 1 (Oct 19 to 25, due date passed)

| Project | Folder | Pull request | Stack name | Merged date | Running since | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Foundation | `engineering/Faris-01-GRC-as-Code-Platform/` | #177 (template only, open) | `grc-foundation` | not merged | not deployed | In progress. No template existed until #177, opened in this report's own phase. Adam's Day 1 acceptance of FOUNDATION-REQUIREMENTS.md is not on record (no comment on #49, no review from Adamalme on #155). |
| 06 Evidence Automation | `engineering/Maria-06-Evidence-Automation/` | #168, #169 (merged); #175 (open, enhancement) | `grc-evidence` | 2026-10-23 (#168, #169) | `live-2026-10-31` | Deployed and running. #175 adds AWS Config and a second control; it is held on a formal code-review approval, not yet merged. |
| 13 BC/DR and IR | `engineering/Rasheed-13-BCDR-IR/` | #176 (open, 35 files, 0 reviews); #171 (closed, not merged) | `grc-bcdr` | not merged | not deployed | In progress, 7 days past due. #171's template path was fixed and verified in a local worktree (tests pass, cfn-lint clean) but the fix was never pushed; the open #176 still has the template at the wrong path. |
| 14 Identity and Access (Okta) | `engineering/Abdifatah-14-Identity-Access/` | #162 (closed, not merged, 2026-10-22) | not named in any merged file | not merged | not deployed | Not started. The one requirements pull request was closed without merging 10 days before this report, and nothing has replaced it. |

### Phase 2 (Oct 26 to Nov 1, due today)

| Project | Folder | Pull request | Stack name | Merged date | Running since | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 01 GRC-as-Code Platform | `engineering/Faris-01-GRC-as-Code-Platform/` | none | `grc-platform` (planned) | not merged | not deployed | Not started. Jason has not opened a requirements pull request; the project item (#29) has no comments. |
| 07 Risk Register | `engineering/Rasheed-07-Risk-Register/` | #172 (requirements, merged this report's phase) | not yet named | requirements merged; build not opened | not deployed | Requirements merged today. No build pull request yet. |
| 08 Access Reviews | `engineering/Abdifatah-08-Access-Reviews/` | #173 (requirements, merged) | not yet named | requirements merged | not deployed | Requirements merged. No build pull request yet. |
| 10 Audit Engagement Manager | `engineering/Maria-10-Audit-Engagement-Manager/` | none | not yet named | not merged | not deployed | Not started. No requirements or build pull request found. |

### Reference: deployed shared stacks (not phase-specific, already running)

| Stack | Tag |
| --- | --- |
| `grc-access-model` | `live-2026-10-17` |
| `grc-internal-auditor` | `live-2026-10-17` |
| `grc-engineer-users` | `live-2026-10-18` |

## 3. What this report found, beyond the table

- Phase 1 is a week late across 3 of its 4 projects (Foundation, 13, 14). Phase 2's four projects are all still unstarted or just-kicked-off on their own due date, because the same engineers are still closing out Phase 1. The one-active-build-per-engineer rule has not held in practice this program.
- 14 is the most at risk: no open pull request exists for it at all, and its one requirements attempt was abandoned without a visible reason on record.
- `.github/CODEOWNERS` still carries `@TODO-maria-github` and `@TODO-abdifatah-github` placeholders on every engineering line, though both GitHub usernames (`zmagu26`, `galgalo12`) have been active and identifiable for weeks.

## 4. Before (manual)

Before this report, project status lived scattered across the GRC Program board, individual pull requests, and informal updates. Nobody had compared the board's status fields against the actual merge and deploy record.

## 5. After

This report and its phase build list, refreshed at each phase end per REQUIREMENTS.md, read status from merged pull requests and `live-YYYY-MM-DD` tags rather than from a status field someone set by hand.

## 6. Metrics

8 projects tracked across Phases 1 and 2. 2 of 8 have a deployed, running stack (Foundation's evidence bucket pattern is not yet one of them; only 06 is). 2 of 8 have merged requirements with no build yet. 1 of 8 (14) has no live pull request at all. 0 of 8 have reached partner sign-off.

## 7. Evidence

Every status above links to a pull request, issue, or tag number in this repo; see the tables in Section 2.

## 8. Cost

Not computed in this report. The October 2026 monthly AWS cost review has not run yet; this report does not substitute for it.

## 9. Test cleanup and handover

Nothing to clean up: 00 has no stack and this report made no AWS change. Nothing new stays running as a result of this report.

## 10. Sign-off

Partner results: not yet written. `non-engineering/Faris-00-Platform-Overview/RESULTS.md` does not exist yet; Adam writes it for 00.

Sign-off: pending. No comment from Adam exists yet accepting this report or the Section 2 format it is based on.

Validation: pending.

Phase assessment: Jason assesses Phase 1 in Phase 2 and Phase 2 in Phase 3, per GOVERNANCE.md; neither assessment is recorded yet.
