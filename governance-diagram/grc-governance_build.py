#!/usr/bin/env python3
"""GRC Projects governance diagram, in the 340 Collective AWS architecture style.

Standard: .kiro/steering/aws-architecture-diagram-style.md (owner-approved 2026-10-03).
Built from the 340 Collective reference template (aws_architecture_template.py): the same
helpers and every layout check are kept; only the EDIT blocks change. This is a process
diagram, so the one boundary is the GRC Projects repo (GitHub vendor icon as the tile)
instead of AWS Cloud, people use the aws/general outline icons, and pipeline stages are
stroke-only outline glyphs (#3F4752, 1.8 px, no fill), the front-end diagram convention
from 340collective-website/Technology/assets/src/build_frontend.py.

Every fact on the image comes from GRC-Projects/GOVERNANCE.md on main (Roles, Project
assignments, Separation of duties, Change process, Deviation request, Access sections).

Run:  /tmp/c340_diag_venv/bin/python grc-governance_build.py <out-path-without-extension>
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
    "service": (LINE, 1.6, None, "ah", "Change flow"),
    "external": (LINE, 1.6, "6 5", "ah", "Stakeholder or exception"),
    "business": (ACCENT, 2.2, None, "ahb", "ISSM approval"),
}

# ---------------- EDIT: canvas text ----------------
W, H = 1900, 1270
TITLE = "GRC Projects Governance"
SUBTITLE = ("Roles, change control, and separation of duties. "
            "No one validates or approves their own work.")
BOUNDARY, BOUNDARY_NOTE = "GRC Projects repo", "every change is a pull request to main"
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
AX0, AX1, AY0, AY1 = 230, 1670, 110, 945             # the one boundary: GRC Projects repo
COLS = [(260, 696), (732, 1168), (1204, 1640)]        # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
ROWS = [(190, 470), (506, 862)]                       # row 0 people, row 1 change pipeline
A0, A1, B1 = 290, 600, 780                            # icon lanes (center y)
XR = 1790                                             # external column (stakeholder)
GV = 420                                              # validator channel inside row 0 (y)
GX = 1186                                             # column gutter between col 1 and col 2 (x)
DENY, DEV, XM = 888, 922, 245                         # return channel, deviation channel, left margin

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

# ---------------- EDIT: groups, (column, row) -> title ----------------
GROUPS = {
    (0, 0): "Engineering", (1, 0): "Validation and assessment", (2, 0): "Approval authority",
    (0, 1): "Build and submit", (1, 1): "Independent review", (2, 1): "Decision and exceptions",
}
for (c, r), title in GROUPS.items():
    (x0, x1), (y0, y1) = COLS[c], ROWS[r]
    group(x0, y0, x1, y1, title)
    # register the title so the line, label, and badge checks also cover group titles
    BOX["title:" + title] = (x0 + 14, y0 + 12, x0 + 14 + est_w(title, 14.5), y0 + 30)

# ---------------- EDIT: nodes ----------------
USR = "aws/general/user.png"
# people (GOVERNANCE.md Roles table)
node("rasheed", USR, SL[0][1], A0, "Rasheed", "ISSE / Engineer")
node("jason", USR, SL[1][0], A0, "Jason", "Auditor / Assessor")
node("adam", USR, SL[1][1], A0, "Adam", "ISSO / Analyst")
node("faris", USR, SL[2][1], A0, "Faris", "ISSM, sole approver")
# the stakeholder sits outside the boundary: informed, not an approver
node("david", "aws/general/office-building.png", XR, A0, "David, Stakeholder",
     "Business Owner")
# change pipeline (GOVERNANCE.md Separation of duties and Change process)
node("build", "glyph:branch", SL[0][1], A1, "Build in branch", "project owner")
node("pr", "glyph:pr", SL[0][2], A1, "Pull request", "what, why, cost")
node("validate", "glyph:review", SL[1][1], A1, "Independent validation", "never the author")
node("decide", "glyph:decide", SL[2][1], A1, "ISSM decision", "approve or deny")
node("merge", "glyph:merge", SL[2][2], A1, "Merge to main", "approved changes only")
node("deviation", "glyph:deviation", SL[2][2], B1, "Deviation request", "compensating control")

# ---------------- EDIT: connections (kind: service, external, business) ----------------
P = port
VT = A1 - HALF - 5                      # y of the Validate top edge port
DB = P("decide", "b")[1]                # y of the Decide bottom port

# 1 the owner builds in a branch, 2 opens a pull request
link("rasheed", "b", "build", "t")                                                 # builds
link("build", "r", "pr", "l")
# 3 independent validation: three arrivals on the top edge, 12 px apart
link("pr", "r", "validate", "l")                                                   # submits
link("adam", "b", "validate", "t")                                                 # Rasheed's work
path([P("jason", "b"), (SL[1][0], GV), (SL[1][1] - 12, GV), (SL[1][1] - 12, VT)],
     "jason", "validate")                                                          # assesses
path([P("faris", "l"), (GX, A0), (GX, GV), (SL[1][1] + 12, GV), (SL[1][1] + 12, VT)],
     "faris", "validate")                                                          # Adam's own work
# 4 the ISSM approves or denies (the one accent line)
link("validate", "r", "decide", "l")
link("faris", "b", "decide", "t", "business")
# 5 approval merges; denial returns to the owner along the return channel
link("decide", "r", "merge", "l")
path([(SL[2][1] - 12, DB), (SL[2][1] - 12, DENY), (SL[0][1], DENY), P("build", "b")],
     "decide", "build")
# 6 a change that cannot be made becomes a deviation request for the ISSM to decide
path([P("build", "l"), (XM, A1), (XM, DEV), (SL[2][2], DEV), P("deviation", "b")],
     "build", "deviation", "external")
path([P("deviation", "l"), (SL[2][1] + 12, B1), (SL[2][1] + 12, DB)],
     "deviation", "decide", "external")
# 7 the ISSM keeps the stakeholder informed (reports to David); David has no approval line
link("faris", "r", "david", "l", "external")


# ---------------- EDIT: line labels (white halo keeps them readable over lines) ----------------
def lbl(x, y, s, anchor="start", color=TEXT2):
    """Line label; its box is registered so lines, labels, and badges cannot overlap it."""
    text(x, y, s, 11.5, 400, color, anchor, halo=True)
    w = est_w(s, 11.5)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    BOX["lbl:" + s] = (x0, y - 10, x0 + w, y + 3)


lbl(SL[0][1] + 10, 440, "builds")
lbl(800, A1 - 10, "submits for review", "middle")
lbl(SL[1][1] + 8, 374, "validates Rasheed's work")
lbl(878, GV - 10, "assesses", "middle")
lbl(1074, GV - 10, "validates Adam's 07, 08, 12", "middle")
lbl(1080, A1 - 10, "validated", "middle")
lbl(SL[2][1] + 10, 440, "approves or denies", color=ACCENT)
lbl(950, DENY - 10, "denied: returned with comments", "middle")
lbl(1300, DEV - 10, "change cannot be made", "middle")
lbl(1560, A0 - 10, "informs (reports to)", "middle")
lbl(SL[2][1] + 20, 730, "submitted for ISSM decision")

draw_nodes()

# ---------------- EDIT: step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(454, 488, 1), (545, 628, 2), (990, 488, 3), (1398, 488, 4),
                  (1386, 760, 5), (1575, 890, 6), (1700, 318, 7)]:
    badge(cx, cy, n)

# ---------------- EDIT: legend steps, one short sentence each, same order as the badges ----------------
LY = 1000
STEPS = [
    "Each owner builds in a branch: Rasheed 05 06 11 13, Adam 07 08 12, Jason 02 03 04 09, Faris 00 01 10.",
    "The owner opens a pull request against main that says what changes, why, and the cost impact.",
    "No one validates their own work: Adam checks Rasheed's, Jason assesses, Faris checks Adam's 07, 08, 12.",
    "Faris, the ISSM, is the only approver: he approves or denies every pull request and access change.",
    "Approval merges the change to main; a denial returns it to the owner with comments.",
    "If a change cannot be made, the owner files a deviation request (risk, compensating control) instead.",
    "Faris reports to David, the business owner, who is kept informed but does not approve changes.",
]

text(40, LY, "How it works", 16, 700, INK, "start")
per_col = (len(STEPS) + 1) // 2
for i, s in enumerate(STEPS):
    col, row = divmod(i, per_col)
    bx, by = 52 + col * 930, LY + 34 + row * 32
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

RULE_Y = KEY_Y + 26
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
