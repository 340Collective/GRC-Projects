#!/usr/bin/env python3
"""GRC program workflow diagram, in the 340 Collective AWS architecture style.

Standard: .kiro/steering/aws-architecture-diagram-style.md (owner-approved 2026-10-03).
Built from grc-governance_build.py (itself built from the 340 Collective reference
template, aws_architecture_template.py): the same helpers, node kinds, line styles, and
every layout check are kept; only the EDIT blocks change, plus six new stroke-only
glyph kinds (doc, calendar, handoff, gauge, cleanup, board) in the same outline style.
This is a process diagram, so the one boundary is the GRC Projects repo (GitHub vendor
icon as the tile) instead of AWS Cloud. People use the aws/general outline icons. Jira has
no bundled icon, so it is a stroke-only board glyph.

Every fact on the image comes from the committed docs:
- GOVERNANCE.md: Roles, Two-track model, 7-day build rule, Integration week,
  End-of-program teardown, Separation of duties (review flow steps 1 to 9),
  Where work lives, Cost guardrails, Running system cost, Timeline.
- shared/labs/README.md: Review flow steps 1 to 9 and Cost cap.
- CONTRIBUTING.md: Partner pull requests.
- shared/templates/FINAL-REPORT.md and shared/templates/RESULTS.md.

Run:  /tmp/c340_diag_venv/bin/python shared/governance-diagram/grc-program-workflow_build.py \
          shared/governance-diagram/grc-program-workflow
The checks must print "layout problems: none" and "crossings: 0".
"""
import base64
import os
import subprocess
import sys

import diagrams

R = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/arch"
OUT_SVG, OUT_PNG = OUT + ".svg", OUT + ".png"

# ---------------- style: owner-approved, keep as is ----------------
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, TEXT2, LINE, GROUP, BADGE, ORANGE, RULE, ACCENT = (
    "#232F3E", "#545B64", "#3F4752", "#7D8998", "#146EB4", "#FF9900", "#E3E6EA", "#8C4FFF")
ICON, HALF = 52, 26
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "Workflow step"),
    "external": (LINE, 1.6, "6 5", "ah", "Stakeholder, tracking, assessment, or alert"),
    "business": (ACCENT, 2.2, None, "ahb", "Acceptance and approval"),
}

# ---------------- EDIT: canvas text ----------------
W, H = 2400, 1560
TITLE = "GRC Program Workflow"
SUBTITLE = "Partners own their records. Engineers build. Faris merges."
BOUNDARY, BOUNDARY_NOTE = ("GRC Projects repo",
                           "requirements and results live in GitHub; Jira tracks tasks only")
FOOTER_LEFT, FOOTER_RIGHT = "340 Collective", "October 2026"

out, icons, SEGS, BADGES = [], [], [], []
N, BOX, USED = {}, {}, set()


def add(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def est_w(s, size):
    return len(s) * size * 0.53


def text(x, y, s, size=13, weight=400, color=INK, anchor="middle", halo=False):
    h = (' stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
         if halo else "")
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{h}>{esc(s)}</text>')


_cache = {}


def data(rel):
    if rel not in _cache:
        with open(os.path.join(R, rel), "rb") as fh:
            _cache[rel] = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
    return _cache[rel]


def node(key, rel, cx, cy, l1, l2=None):
    """Register an icon at slot (cx, cy) with a name and an optional role line.
    rel "glyph:<kind>" draws a stroke-only outline glyph instead of an icon PNG."""
    assert key not in N, key
    N[key] = (cx, cy, 2 if l2 else 1)
    icons.append((rel, cx, cy, l1, l2))
    w = max(ICON, est_w(l1, 13), est_w(l2 or "", 12))
    BOX[key] = (cx - w / 2, cy - HALF, cx + w / 2, cy + HALF + (36 if l2 else 21))


def glyph(kind, cx, cy):
    """52 px outline glyph in the line style: #3F4752 stroke, no fill."""
    st = (f'fill="none" stroke="{LINE}" stroke-width="1.8" stroke-linejoin="round" '
          f'stroke-linecap="round"')

    def p(d):
        add(f'<path d="{d}" {st}/>')

    def circ(x, y, r=4.5):
        add(f'<circle cx="{x}" cy="{y}" r="{r}" {st}/>')

    def doc(w=36, h=48):
        a, b = cx - w / 2, cy - h / 2
        p(f"M {a},{b} H {a+w-10} L {a+w},{b+10} V {b+h} H {a} Z "
          f"M {a+w-10},{b} V {b+10} H {a+w}")
        return a, b, w, h

    if kind == "branch":      # a branch forking off a trunk
        circ(cx - 10, cy - 18)
        circ(cx - 10, cy + 18)
        circ(cx + 12, cy - 10)
        p(f"M {cx-10},{cy-13.5} V {cy+13.5}")
        p(f"M {cx+12},{cy-5.5} V {cy-2} C {cx+12},{cy+6} {cx-10},{cy+2} {cx-10},{cy+9}")
    elif kind == "pr":        # pull request: branch line plus a request arrow into the base
        circ(cx - 12, cy - 18)
        circ(cx - 12, cy + 18)
        circ(cx + 12, cy + 18)
        p(f"M {cx-12},{cy-13.5} V {cy+13.5}")
        p(f"M {cx+12},{cy+13.5} V {cy-8} Q {cx+12},{cy-18} {cx+2},{cy-18}")
        p(f"M {cx+7},{cy-23} L {cx+2},{cy-18} L {cx+7},{cy-13}")
    elif kind == "review":    # document under a magnifier
        a, b, w, h = doc()
        circ(cx - 2, cy + 2, 7)
        p(f"M {cx+3},{cy+7} L {cx+10},{cy+14}")
        p(f"M {a+7},{b+12} H {a+w-12}")
    elif kind == "decide":    # approve or deny
        add(f'<rect x="{cx-24}" y="{cy-17}" width="48" height="34" rx="3" {st}/>')
        p(f"M {cx},{cy-17} V {cy+17}")
        p(f"M {cx-17},{cy+1} L {cx-12},{cy+7} L {cx-5},{cy-6}")
        p(f"M {cx+7},{cy-6} L {cx+17},{cy+6} M {cx+17},{cy-6} L {cx+7},{cy+6}")
    elif kind == "merge":     # two lines joining into main
        circ(cx - 12, cy - 18)
        circ(cx + 12, cy - 18)
        circ(cx, cy + 18)
        p(f"M {cx-12},{cy-13.5} V {cy-6} Q {cx-12},{cy+3} {cx},{cy+5} V {cy+13.5}")
        p(f"M {cx+12},{cy-13.5} V {cy-6} Q {cx+12},{cy+3} {cx},{cy+5}")
    elif kind == "deviation":  # document with an exclamation mark
        doc()
        p(f"M {cx},{cy-8} V {cy+6}")
        circ(cx, cy + 12, 1.2)
    elif kind == "doc":       # a written record: document with text lines
        a, b, w, h = doc()
        for dy in (16, 24, 32):
            p(f"M {a+7},{b+dy} H {a+w-7}")
    elif kind == "calendar":  # a date range
        add(f'<rect x="{cx-22}" y="{cy-18}" width="44" height="40" rx="3" {st}/>')
        p(f"M {cx-22},{cy-7} H {cx+22}")
        p(f"M {cx-11},{cy-24} V {cy-13} M {cx+11},{cy-24} V {cy-13}")
        for x in (cx - 12, cx, cx + 12):
            for y in (cy + 3, cy + 13):
                circ(x, y, 1.2)
    elif kind == "handoff":   # builds handing data to each other
        for x in (cx - 18, cx, cx + 18):
            add(f'<rect x="{x-6}" y="{cy-6}" width="12" height="12" rx="2" {st}/>')
        p(f"M {cx-12},{cy} H {cx-6} M {cx+6},{cy} H {cx+12}")
        p(f"M {cx-18},{cy-6} V {cy-18} H {cx+18} V {cy-6}")
    elif kind == "gauge":     # a running system: dial with a needle
        p(f"M {cx-22},{cy+10} A 22 22 0 0 1 {cx+22},{cy+10}")
        p(f"M {cx-22},{cy+10} H {cx+22}")
        p(f"M {cx},{cy+10} L {cx+11},{cy-6}")
        circ(cx, cy + 10, 2.5)
    elif kind == "cleanup":   # delete what the test made: a bin
        p(f"M {cx-18},{cy-14} H {cx+18} M {cx-6},{cy-14} V {cy-20} H {cx+6} V {cy-14}")
        p(f"M {cx-14},{cy-14} L {cx-11},{cy+22} H {cx+11} L {cx+14},{cy-14}")
        p(f"M {cx-5},{cy-6} V {cy+14} M {cx+5},{cy-6} V {cy+14}")
    elif kind == "board":     # a task board: three columns with cards
        add(f'<rect x="{cx-24}" y="{cy-20}" width="48" height="40" rx="3" {st}/>')
        p(f"M {cx-8},{cy-20} V {cy+20} M {cx+8},{cy-20} V {cy+20}")
        for x, ys in ((cx - 16, (-13, -3, 7)), (cx, (-13, -3)), (cx + 16, (-13,))):
            for y in ys:
                add(f'<rect x="{x-5}" y="{cy+y}" width="10" height="6" rx="1" {st}/>')
    else:
        raise ValueError(kind)


def draw_nodes():
    for rel, cx, cy, l1, l2 in icons:
        if rel.startswith("glyph:"):
            glyph(rel[6:], cx, cy)
        else:
            add(f'<image x="{cx-HALF}" y="{cy-HALF}" width="{ICON}" height="{ICON}" '
                f'xlink:href="{data(rel)}"/>')
        text(cx, cy + HALF + 17, l1, 13, 400, INK)
        if l2:
            text(cx, cy + HALF + 32, l2, 12, 400, TEXT2)


def port(key, side, gap=5):
    """Connection point: l, r, t (top edge of icon), b (below the label block)."""
    cx, cy, n = N[key]
    return {"l": (cx - HALF - gap, cy), "r": (cx + HALF + gap, cy),
            "t": (cx, cy - HALF - gap),
            "b": (cx, cy + HALF + (36 if n == 2 else 21) + gap)}[side]


def path(pts, a, b, kind="service"):
    color, width, dash, marker, _ = KINDS[kind]
    USED.add(kind)
    for p, q in zip(pts, pts[1:]):
        assert p[0] == q[0] or p[1] == q[1], ("diagonal segment", a, b, p, q)
        SEGS.append((p, q, a, b))
    d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} '
        f'marker-end="url(#{marker})"/>')


def link(a, sa, b, sb, kind="service", via=None):
    """Connect two nodes. via = elbow points; every segment must be horizontal or vertical."""
    path([port(a, sa)] + (via or []) + [port(b, sb)], a, b, kind)


def badge(cx, cy, n, record=True):
    if record:
        BADGES.append((cx, cy, n))
    add(f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="{BADGE}"/>')
    text(cx, cy + 4.6, str(n), 13, 700, "#FFFFFF")


def group(x0, y0, x1, y1, title):
    add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" '
        f'stroke="{GROUP}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    text(x0 + 14, y0 + 25, title, 14.5, 700, INK, "start")


# ---------------- EDIT: grid ----------------
AX0, AX1, AY0, AY1 = 230, 2130, 110, 1080           # the one boundary: GRC Projects repo
COLS = [(260, 2100)]                                 # one band inside the boundary (border check)
C1, C2, C3 = (260, 849), (885, 1474), (1510, 2099)   # 3 equal-width group columns
S1, S2, S3 = (378, 554, 731), (1003, 1179, 1356), (1628, 1804, 1981)  # slots at 20/50/80 %
R1, R2, R3 = (150, 470), (530, 770), (830, 1050)     # aligned group rows (y)
LA, LB, L2, L3 = 250, 395, 630, 920                  # icon lanes: row 1 (two), row 2, row 3
XL, XR = 115, 2265                                   # external columns, left and right
FTOP, JTOP = 190, 206                                # top channels: Faris, Jason (y)
APPR = 490                                           # Faris's approval channel (y)
DEPL = 500                                           # deploy to partner test channel (y)
RPT = 740                                            # report to sign-off channel (y)
TRK = 800                                            # Jira tracking channel (y)
FIN = 1030                                           # final results channel (y)

# ---------------- canvas and the one boundary ----------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs>'
    '<marker id="ah" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6.5" '
    f'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
    '<marker id="ahb" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" '
    f'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
text(40, 56, TITLE, 26, 700, INK, "start")
text(40, 82, SUBTITLE, 14, 400, TEXT2, "start")
add(f'<rect x="{AX0}" y="{AY0}" width="{AX1-AX0}" height="{AY1-AY0}" fill="none" '
    f'stroke="{INK}" stroke-width="1.6"/>')
# boundary tile: the vendor's own GitHub icon, since the boundary is the repo, not AWS Cloud
add(f'<image x="{AX0+6}" y="{AY0+6}" width="24" height="24" '
    f'xlink:href="{data("onprem/vcs/github.png")}"/>')
add(f'<text x="{AX0+40}" y="{AY0+23}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">{esc(BOUNDARY)}<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(BOUNDARY_NOTE)}</tspan></text>')

# ---------------- EDIT: groups, (x0, y0, x1, y1, title) ----------------
GROUPS = [  # (x0, y0, x1, y1, title)
    (C1[0], R1[0], C1[1], R1[1], "People"),
    (C2[0], R1[0], C2[1], R1[1], "Day 1: requirements"),
    (C3[0], R1[0], C3[1], R1[1], "Days 2 to 6: build"),
    (C1[0], R2[0], C1[1], R2[1], "Day 7: approval and merge"),
    (C2[0], R2[0], C2[1], R2[1], "Day 7: sign-off"),
    (C3[0], R2[0], C3[1], R2[1], "Day 7: records"),
    (C1[0], R3[0], C1[1], R3[1], "Running system"),
    (C2[0], R3[0], C2[1], R3[1], "Timeline"),
    (C3[0], R3[0], C3[1], R3[1], "End-of-program teardown"),
]
for x0, y0, x1, y1, title in GROUPS:
    group(x0, y0, x1, y1, title)
    # register the title so the line, label, and badge checks also cover group titles
    BOX["title:" + title] = (x0 + 14, y0 + 12, x0 + 14 + est_w(title, 14.5), y0 + 30)

# ---------------- EDIT: nodes ----------------
USR = "aws/general/user.png"
CFN = "aws/management/cloudformation.png"
# people (GOVERNANCE.md Roles)
node("faris", USR, S1[0], LA, "Faris", "ISSM: accepts, approves")
node("jason", USR, S1[1], LA, "Jason", "Auditor: pass or findings")
node("adam", USR, S1[2], LA, "Adam", "ISSO: tests, validates")
node("assess", "glyph:review", S1[1], LB, "Phase assessment", "Jason, own folder")
# outside the boundary: the stakeholder (informed only) and Jira (tracking only)
node("david", "aws/general/office-building.png", XL, LA, "David", "Stakeholder, informed")
node("jira", "glyph:board", XR, TRK, "Jira", "tracking only")
# Day 1 (GOVERNANCE.md 7-day build rule; review flow step 1; CONTRIBUTING Partner pull requests)
node("req", "glyph:doc", S2[0], LA, "REQUIREMENTS.md", "partner folder, by PR")
node("kickoff", "glyph:decide", S2[1], LA, "Day 1 kickoff", "Faris accepts")
# Days 2 to 6 (review flow steps 2 and 3; shared/labs/README.md review flow step 3)
node("build", "glyph:branch", S3[0], LA, "Build in branch", "the engineer")
node("review", "glyph:review", S3[1], LA, "Code review", "another engineer")
node("deploy", CFN, S3[2], LA, "Deploy own stack", "from clean main, after approval")
node("engineers", "aws/general/users.png", S3[0], LB, "Engineers",
     "Rasheed, Maria, Abdifatah, Faris")
# Day 7 (7-day build rule; review flow steps 4 to 8; FINAL-REPORT and RESULTS templates)
node("report", "glyph:doc", S3[2], L2, "FINAL-REPORT.md", "engineer folder")
node("results", "glyph:doc", S3[1], L2, "RESULTS.md", "partner folder")
node("signoff", "glyph:review", S2[2], L2, "Partner sign-off", "Final report item")
node("validate", "glyph:review", S2[1], L2, "ISSO validation", "Adam, Final report item")
node("approve", "glyph:decide", S1[2], L2, "Final approval", "Faris; Adam if Faris built")
node("merge", "glyph:merge", S1[1], L2, "Merge to main", "only Faris merges")
# running system (7-day build rule; End-of-program teardown; Cost guardrails)
node("budget", "aws/cost/budgets.png", S1[0], L3, "AWS Budget", "alerts at 1, 5, 10 dollars")
node("operate", "glyph:gauge", S1[1], L3, "Partner operates", "build stays deployed")
node("cleanup", "glyph:cleanup", S1[2], L3, "Test cleanup", "after every test")
# timeline (GOVERNANCE.md Timeline, Integration week, End-of-program teardown)
node("phases", "glyph:calendar", S2[0], L3, "Phases 1 to 5", "Oct 19 to Nov 22")
node("integration", "glyph:handoff", S2[1], L3, "Integration week", "Nov 23 to 25")
node("running", "glyph:gauge", S2[2], L3, "System keeps running", "December, January")
node("teardown", CFN, S3[0], L3, "Teardown", "Jan 11 to 18, 2027")

# ---------------- EDIT: connections (kind: service, external, business) ----------------
P = port
FB = P("faris", "b")[1]                 # y of a lane A bottom port (two-line labels)

# 1 partners write REQUIREMENTS.md in their own folder by pull request
link("adam", "r", "req", "l")
path([P("jason", "t"), (S1[1], JTOP), (S2[0], JTOP), P("req", "t")], "jason", "req")
link("req", "r", "kickoff", "l")
# 2 Faris accepts the requirements at the Day 1 kickoff
path([P("faris", "t"), (S1[0], FTOP), (S2[1], FTOP), P("kickoff", "t")],
     "faris", "kickoff", "business")
# 3 the engineer builds in a branch; another engineer reviews the code
link("kickoff", "r", "build", "l")
link("engineers", "t", "build", "b")
link("build", "r", "review", "l")
# 4 after approval, the engineer deploys their own stack from clean main
link("review", "r", "deploy", "l")
# 5 Day 7: the engineer's FINAL-REPORT.md and the partner's own test results
link("deploy", "b", "report", "t")
path([(S3[2] - 12, FB), (S3[2] - 12, DEPL), (S3[1], DEPL), P("results", "t")],
     "deploy", "results")
# 6 the partner compares them and signs off on the Final report item
link("results", "l", "signoff", "r")
path([P("report", "b"), (S3[2], RPT), (S2[2] + 12, RPT), (S2[2] + 12, P("signoff", "b")[1])],
     "report", "signoff")
# 7 Adam validates on the Final report item
link("signoff", "l", "validate", "r")
# 8 final approval: Faris, or Adam for Faris-built work; only Faris merges
link("validate", "l", "approve", "r")
path([P("faris", "b"), (S1[0], APPR), (S1[2] - 12, APPR), (S1[2] - 12, P("approve", "t")[1])],
     "faris", "approve", "business")
path([(S1[2] + 12, FB), (S1[2] + 12, P("approve", "t")[1])], "adam", "approve", "business")
link("approve", "l", "merge", "r")
# 9 the build stays deployed; the partner operates it; test cleanup after every test
link("merge", "b", "operate", "t")
link("operate", "r", "cleanup", "l")
# 10 phases, then integration week, where partners commit final results
link("phases", "r", "integration", "l")
path([P("operate", "b"), (S1[1], FIN), (S2[1], FIN), P("integration", "b")],
     "operate", "integration")
# 11 Jason assesses once per phase, in his own folder; he never approves
link("jason", "b", "assess", "t", "external")
# 12 the system keeps running through December and January, then the teardown
link("integration", "r", "running", "l")
link("running", "r", "teardown", "l")
# 13 budget alerts only notify: the team scales down instead of tearing down
link("budget", "r", "operate", "l", "external")
# 14 Jira tracks tasks only
path([P("jira", "l"), (S2[0], TRK), P("phases", "t")], "jira", "phases", "external")
# 15 Faris keeps David informed; David approves nothing
link("faris", "l", "david", "r", "external")


# ---------------- EDIT: line labels (white halo keeps them readable over lines) ----------------
def lbl(x, y, s, anchor="start", color=TEXT2):
    """Line label; its box is registered so lines, labels, and badges cannot overlap it."""
    text(x, y, s, 11.5, 400, color, anchor, halo=True)
    w = est_w(s, 11.5)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    BOX["lbl:" + s] = (x0, y - 10, x0 + w, y + 3)


lbl(206, LA - 10, "informs", "middle")
lbl(S2[1] + 10, 210, "accepts", color=ACCENT)
lbl(1300, LA - 10, "requirements agreed", "middle")
lbl(S3[2] + 10, 420, "builder's tests")
lbl(1886, DEPL + 16, "partner tests the build", "middle")
lbl(1700, L2 - 10, "partner's results", "middle")
lbl(1700, RPT + 16, "engineer's report", "middle")
lbl(S2[0], L2 - 10, "validated", "middle")
lbl(470, APPR + 16, "final approval", "middle", color=ACCENT)
lbl(S1[2] + 22, APPR + 16, "approves Faris-built work", color=ACCENT)
lbl(S1[1] + 10, 345, "once per phase")
lbl(S1[1] + 10, TRK, "stays deployed")
lbl(740, FIN - 8, "final results to RESULTS.md", "middle")
lbl(1700, TRK - 8, "tracks tasks", "middle")

draw_nodes()

# ---------------- EDIT: step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(867, 278, 1), (1260, 290, 2), (1560, 340, 3), (2070, 200, 4),
                  (1760, 485, 5), (1440, 700, 6), (1179, 718, 7), (867, 560, 8),
                  (520, 800, 9), (1090, 1000, 10), (520, 340, 11), (1492, 880, 12),
                  (290, 1010, 13), (1900, 815, 14), (205, 200, 15)]:
    badge(cx, cy, n)

# ---------------- EDIT: legend steps, one short sentence each, same order as the badges ----------------
LY = AY1 + 60
STEPS = [
    "Adam and Jason write REQUIREMENTS.md in their own folder and open a pull request.",
    "Day 1 kickoff: Faris accepts the requirements. Adam accepts Faris's own and the 01 requirements.",
    "Days 2 to 6: the engineer builds in a branch, and another engineer reviews the code.",
    "After approval, the engineer deploys their own stack from clean main.",
    "Day 7: the engineer commits FINAL-REPORT.md. The partner tests the build and commits RESULTS.md.",
    "The partner compares the two and signs off on the Final report item, with a link to the results.",
    "Adam, the ISSO, validates on the Final report item.",
    "Faris gives final approval (Adam for Faris-built work). Only Faris merges.",
    "The build stays deployed and the partner operates it. Test artifacts are cleaned up after every test.",
    "Phases run Oct 19 to Nov 22. In integration week, Nov 23 to 25, partners commit final results.",
    "Jason assesses once per phase and commits it to his own folder. He builds nothing and never approves.",
    "The system keeps running through December and January. Teardown runs Jan 11 to 18, 2027.",
    "The budget cap is 10 dollars. Alerts at 1, 5, and 10 dollars only notify, so the team scales down.",
    "Jira tracks tasks only. Requirements, results, and sign-off live in GitHub.",
    "Faris keeps David, the stakeholder, informed. David approves nothing.",
]

text(40, LY, "How it works", 16, 700, INK, "start")
per_col = (len(STEPS) + 1) // 2
for i, s in enumerate(STEPS):
    col, row = divmod(i, per_col)
    bx, by = 52 + col * 1170, LY + 34 + row * 32
    badge(bx, by, i + 1, record=False)
    text(bx + 22, by + 4.6, s, 13.5, 400, INK, "start")

# line-style key, one entry per line kind actually used
KEY_Y = LY + 40 + per_col * 32
lx = 40
for k, (color, width, dash, marker, label) in KINDS.items():
    if k not in USED:
        continue
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="M {lx},{KEY_Y} L {lx+52},{KEY_Y}" stroke="{color}" stroke-width="{width}"'
        f'{da} marker-end="url(#{marker})"/>')
    text(lx + 62, KEY_Y + 4.5, label, 12.5, 400, TEXT2, "start")
    lx += 62 + est_w(label, 12.5) + 48

# what the image leaves out, so nobody reads it as the whole rulebook
NOTE = ("Not shown: code review pairs and the deviation path (see the governance diagram), "
        "each partner's projects (GOVERNANCE.md two-track table), partner pull requests "
        "(Faris reviews and merges them; Adam reviews 00), and the AWS to Jira integrations. "
        "Faris-built work: the foundation, 00, 01, and 11.")
text(40, KEY_Y + 34, NOTE, 12.5, 400, TEXT2, "start")

RULE_Y = KEY_Y + 58
add(f'<line x1="40" y1="{RULE_Y}" x2="{W-40}" y2="{RULE_Y}" stroke="{RULE}" stroke-width="1"/>')
text(40, RULE_Y + 26, FOOTER_LEFT, 13, 700, INK, "start")
text(W - 40, RULE_Y + 26, FOOTER_RIGHT, 13, 400, TEXT2, "end")
add("</svg>")
assert RULE_Y + 50 <= H, "canvas too short for the legend: raise H"


# ---------------- checks: keep all of them ----------------
def seg_hits_box(p, q, box, pad=2):
    x0, y0, x1, y1 = box
    (ax, ay), (bx, by) = p, q
    if ay == by:
        lo, hi = sorted((ax, bx))
        return y0 - pad < ay < y1 + pad and lo < x1 + pad and hi > x0 - pad
    lo, hi = sorted((ay, by))
    return x0 - pad < ax < x1 + pad and lo < y1 + pad and hi > y0 - pad


def boxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def crossings():
    hs = [s for s in SEGS if s[0][1] == s[1][1]]
    vs = [s for s in SEGS if s[0][0] == s[1][0]]
    found = []
    for hp, hq, ha, hb in hs:
        y = hp[1]
        x0, x1 = sorted((hp[0], hq[0]))
        for vp, vq, va, vb in vs:
            if (ha, hb) == (va, vb):
                continue
            x = vp[0]
            y0, y1 = sorted((vp[1], vq[1]))
            if x0 < x < x1 and y0 < y < y1:
                found.append(f"{ha}->{hb} x {va}->{vb}")
    return found


def shared_segments():
    found = []
    for i in range(len(SEGS)):
        for j in range(i + 1, len(SEGS)):
            (p, q, a, b), (r, s, c, d) = SEGS[i], SEGS[j]
            if (a, b) == (c, d):
                continue
            if p[1] == q[1] == r[1] == s[1]:
                lo1, hi1 = sorted((p[0], q[0]))
                lo2, hi2 = sorted((r[0], s[0]))
            elif p[0] == q[0] == r[0] == s[0]:
                lo1, hi1 = sorted((p[1], q[1]))
                lo2, hi2 = sorted((r[1], s[1]))
            else:
                continue
            if min(hi1, hi2) - max(lo1, lo2) > 0:
                found.append(f"{a}->{b} shares a segment with {c}->{d}")
    return found


problems = []
for p, q, a, b in SEGS:
    for k, box in BOX.items():
        if k not in (a, b) and seg_hits_box(p, q, box):
            problems.append(f"line {a}->{b} crosses {k}")
keys = list(BOX)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        if boxes_overlap(BOX[keys[i]], BOX[keys[j]]):
            problems.append(f"label overlap {keys[i]} / {keys[j]}")
for cx, cy, n in BADGES:
    bb = (cx - 12, cy - 12, cx + 12, cy + 12)
    for p, q, a, b in SEGS:
        if seg_hits_box(p, q, bb, pad=1):
            problems.append(f"badge {n} sits on line {a}->{b}")
    for k, box in BOX.items():
        if boxes_overlap(bb, box):
            problems.append(f"badge {n} overlaps {k}")
for k, (x0, y0, x1, y1) in BOX.items():
    for (c0, c1) in COLS:
        if c0 < (x0 + x1) / 2 < c1 and (x0 < c0 + 4 or x1 > c1 - 4):
            problems.append(f"label of {k} touches its group border")
problems += shared_segments()
X = crossings()
if len(X) > 2:
    problems.append(f"{len(X)} line crossings (2 at most, only where unavoidable)")

svg = "\n".join(out)
assert "\u2014" not in svg and "\u2013" not in svg, "em or en dash found"
# sensitive-text check (standard section 4 step 5): no emails, ARNs, or endpoint URLs
for bad in ("@", "arn:", "amazonaws.com", "lambda-url", "execute-api"):
    assert bad not in svg, f"sensitive text found: {bad}"
with open(OUT_SVG, "w") as fh:
    fh.write(svg)
subprocess.run(["rsvg-convert", "-z", "2", "-o", OUT_PNG, OUT_SVG], check=True)
print("nodes:", len(N), "segments:", len(SEGS), "badges:", len(BADGES))
print("crossings:", len(X), *X)
print("layout problems:", problems if problems else "none")
print("wrote", OUT_SVG, "and", OUT_PNG)
