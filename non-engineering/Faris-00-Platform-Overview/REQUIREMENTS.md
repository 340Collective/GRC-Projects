# 00 Platform Overview: requirements

Status: Draft, pending ISSO acceptance.

| Field | Value |
| --- | --- |
| Project | 00 GRC Platform Overview |
| Owner | Faris (ISSM): writes this document and the phase build list it defines |
| Accepts these requirements, the phase build lists, and the updated overview | Adam (ISSO) |
| Phase | Every phase (documentation), no points, no build week |
| Jira epic | [GRC-1](https://340collective.atlassian.net/browse/GRC-1) |
| Kickoff | Day 1 of each phase; this document itself is accepted once, then reused every phase |

This is the Day 1 kickoff document for 00, written per [LAB-STEPS.md](LAB-STEPS.md) "Define requirements" step 1. It sets the one format every phase build list follows, so Adam accepts the format once instead of re-litigating it each phase.

## 1. Purpose

00 has no stack and no build week. Its job is to keep one honest record of what each phase actually delivered into the shared system, separate from what the overview diagram shows as target design. The diagram shows intent (how projects connect once built); the phase build list shows fact (what is actually running, as of the report date).

## 2. The phase build list format

At the end of each phase, Faris asks every engineer for their phase build list and records it here in this format, one row per project touched that phase:

| Field | What it records |
| --- | --- |
| Project | Number and name, for example `13 BC/DR and IR` |
| Folder | The engineering folder, for example `engineering/Rasheed-13-BCDR-IR/` |
| Pull request | The pull request number that merged the build, if any |
| Stack name | The CloudFormation stack name, for example `grc-bcdr`, or "none deployed" |
| Merged date | The date the finishing pull request merged into `main`, or "not merged" |
| Running since | The `live-YYYY-MM-DD` tag on the deployed commit, or "not deployed" |
| Expected monthly cost | From the project's own requirements document |
| Status | One of: not started, in progress, built but not merged, merged but not deployed, deployed and running, signed off |

At the end-of-program teardown, a final column records where each project's teardown evidence is kept.

## 3. Acceptance check (what Adam sees)

| ID | Requirement | Acceptance check |
| --- | --- | --- |
| OR-1 | The phase build list uses the Section 2 format, one row per project touched that phase. | The phase build list in FINAL-REPORT.md matches the format exactly. |
| OR-2 | Status is read from evidence, not from intent: a project counts as "deployed and running" only if a `live-YYYY-MM-DD` tag exists and the engineer's own FINAL-REPORT.md or an equivalent merged record says so. A project with a written requirements document and no merged build is "in progress" at most. | Each status in the phase build list links to the tag, pull request, or merged file it is based on. |
| OR-3 | The overview diagram and its "How the projects connect" list change only when a project's own README or architecture doc names a new record handed to or from another project. Deployment status never changes a line; it is tracked in the phase build list instead. | The diagram's connections and the phase build list are reported separately, never conflated. |
| OR-4 | Every phase's build list is cumulative: a later phase's list does not drop a project that is late from an earlier phase. A late project stays listed as not yet delivered until it is. | FINAL-REPORT.md carries every project from every phase so far, not only the current phase's. |

## 4. Acceptance

Accepted by: ____ (Adam, ISSO)

Date: ____

Findings or conditions (one per line, or "none"):

- ____
