#!/usr/bin/env python3
"""AWS architecture diagram kit: one file with the style guide, setup, builder, and checks.

Look: one AWS Cloud boundary, an aligned grid of unfilled dashed groups, official AWS
icons on a shared slot grid, right-angle lines with no crossings unless unavoidable, and
numbered steps explained by a plain-English legend. As shipped it draws a complete worked
example (the GRC Metrics and Board Reporting design). Replace the EDIT blocks to draw your own.

============================================================================================
1. REQUIREMENTS
============================================================================================
  Python 3.9 or newer
  diagrams==0.25.1      pip package. Only its bundled official AWS icon PNGs are used.
                        Graphviz is NOT needed.
  rsvg-convert          from librsvg, renders the SVG to PNG at 2x.
                          macOS:          brew install librsvg
                          Debian/Ubuntu:  sudo apt install librsvg2-bin
                          Fedora:         sudo dnf install librsvg2-tools

============================================================================================
2. SETUP (once per machine)
============================================================================================
  python3 aws_diagram_kit.py --setup
    Creates a virtual environment at ~/.aws_diagram_venv (override with the
    AWS_DIAGRAM_VENV environment variable), installs diagrams==0.25.1 into it, and checks
    for rsvg-convert. After that, plain `python3 aws_diagram_kit.py ...` re-launches itself
    inside that venv automatically.

  Manual alternative:
    python3 -m venv ~/.aws_diagram_venv
    ~/.aws_diagram_venv/bin/pip install diagrams==0.25.1

============================================================================================
3. RUN
============================================================================================
  python3 aws_diagram_kit.py /tmp/my-diagram
    Writes /tmp/my-diagram.svg and /tmp/my-diagram.png and prints:
      nodes / segments / badges counts
      crossings: <n>                (must be 0, or 2 at most where truly unavoidable)
      layout problems: none         (anything else must be fixed)
      sensitive text: none          (anything else must be removed)
  Then OPEN THE PNG AND LOOK AT IT. Clipped labels, crowded gutters, and ambiguous lines
  pass the checks but are obvious by eye. A passing script does not mean you are done.

============================================================================================
4. MAKE YOUR OWN DIAGRAM
============================================================================================
  Copy this file, then change only the blocks marked "EDIT", top to bottom:
    canvas text   title, subtitle, region, footer, canvas size (W, H)
    grid          boundary box, 3 group columns, group rows, icon lanes, gutters
    groups        one group per business function, keyed by (column, row)
    nodes         node(key, icon_path, x, y, "Service name", "role line")
                  x must be a slot: SL[col][0|1|2] (20/50/80 percent of the column),
                  or XL / XR for external parties outside the boundary.
                  y must be an icon lane (A0, B0, A1, B1, A2, B2) or a channel.
                  Icon paths are relative to the diagrams "resources" folder, for example
                  aws/compute/lambda.png. List them with:
                    python3 -c "import diagrams,os;print(os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)),'resources','aws'))"
    connections   link(a, side, b, side, kind, via=[elbow points])
                  side: l, r, t (icon top), b (below the label)
                  kind: "service" (solid), "external" (dashed), "business" (purple accent)
                  Every segment must be horizontal or vertical. Route through gutters.
    line labels   lbl(x, y, "text") in a gutter beside its line
    badges        (x, y, n) in a gutter beside the line it numbers, never on it
    legend        STEPS, one short sentence per badge, same order
  Keep every style constant and every check below unchanged.

============================================================================================
5. STYLE RULES (what the checks cannot fully enforce)
============================================================================================
  Canvas      white, 1900 px wide at 1x, rendered at 2x. 26 px bold title + one-line
              subtitle, top left. Font: Helvetica Neue, Helvetica, Arial, sans-serif.
  Boundary    exactly ONE AWS Cloud box: solid #232F3E, 1.6 px, square corners, AWS tile
              top left, "AWS Cloud" + region. External parties sit in columns outside it.
  Groups      equal-width, 3-column grid, aligned rows, NO FILL, dashed #7D8998 1.3 px
              (dash 5 4), bold 14.5 px title top left. One group per business function.
  Fills       none anywhere. Color only from official icons, step badges, and the one
              accent line color.
  Icons       official AWS Architecture Icons only, 52 px, on the shared slot grid.
              Label: service name 13 px #232F3E, role line 12 px #545B64.
              External parties: aws/general outline icons, or the vendor's own icon.
  Lines       orthogonal only, filled arrowheads.
                solid  #3F4752 1.6 px          AWS service call or data flow
                dashed #3F4752 1.6 px (6 5)    external party or control action
                purple #8C4FFF 2.2 px          business steps (the only accent)
              A line never passes through an icon, label, badge, or group title. No two
              lines share a segment. Aim for zero crossings.
  Steps       blue #146EB4 24 px rounded squares, white numbers, in gutters. Order: the
              customer journey first, then operations (deploy, monitor, cost, secrets).
  Bottom      "How it works" legend in two columns, a line-style key, and a footer with a
              hairline above (name left, month and year right).

  Content
    - Draw only connections you have verified in code or IaC (templates, IAM statements,
      env vars, SDK calls, schedules). Leave anything unconfirmed off.
    - Show interactions BETWEEN groups, not just services inside their own box.
    - Nothing sensitive on the image: no account IDs, bucket names, ARNs, endpoint or
      function URLs, emails, keys, or tokens. A public domain is fine. Add your own
      terms (account ID, resource prefixes) to SENSITIVE_EXTRA below.
    - Plain words, no hype.

  Avoid (rejected looks): default Mermaid boxes, pastel fills behind dark text,
  auto-layout output, and a tidy grid with almost no lines between groups.

============================================================================================
6. REVIEW CHECKLIST (pass or fail, one line)
============================================================================================
  One AWS boundary | aligned slot grid | no fills | official icons | orthogonal lines |
  crossings (count) | nothing through icons, labels, or badges | steps match legend |
  verified connections only | nothing sensitive | no em or en dashes | render checked by eye
"""
import base64
import os
import re
import shutil
import subprocess
import sys

DIAGRAMS_VERSION = "0.25.1"
VENV = os.environ.get("AWS_DIAGRAM_VENV", os.path.expanduser("~/.aws_diagram_venv"))
RSVG_HELP = ("rsvg-convert not found. Install librsvg: macOS `brew install librsvg`, "
             "Debian/Ubuntu `sudo apt install librsvg2-bin`, Fedora `sudo dnf install librsvg2-tools`.")


def _venv_python():
    return os.path.join(VENV, "Scripts" if os.name == "nt" else "bin",
                        "python.exe" if os.name == "nt" else "python")


def _setup():
    py = _venv_python()
    if not os.path.exists(py):
        print("creating venv at", VENV)
        subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
    print(f"installing diagrams=={DIAGRAMS_VERSION} (official AWS icons)")
    subprocess.run([py, "-m", "pip", "install", "--quiet", f"diagrams=={DIAGRAMS_VERSION}"],
                   check=True)
    print("rsvg-convert:", shutil.which("rsvg-convert") or RSVG_HELP)
    print("setup done. Run: python3", os.path.abspath(__file__), "/tmp/<name>")


ARGS = sys.argv[1:]
if ARGS[:1] == ["--setup"]:
    _setup()
    sys.exit(0)
try:
    import diagrams
except ImportError:
    # re-launch inside the kit's venv if it exists and we are not already in it
    if os.path.exists(_venv_python()) and \
            os.path.realpath(sys.prefix) != os.path.realpath(VENV):
        os.execv(_venv_python(), [_venv_python(), os.path.abspath(__file__)] + ARGS)
    sys.exit(f"diagrams is not installed. Run: python3 {sys.argv[0]} --setup")
if not shutil.which("rsvg-convert"):
    sys.exit(RSVG_HELP)

R = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = ARGS[0] if ARGS else "/tmp/arch"
OUT_SVG, OUT_PNG = OUT + ".svg", OUT + ".png"

# ---------------- style: keep as is ----------------
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, TEXT2, LINE, GROUP, BADGE, ORANGE, RULE, ACCENT = (
    "#232F3E", "#545B64", "#3F4752", "#7D8998", "#146EB4", "#FF9900", "#E3E6EA", "#8C4FFF")
ICON, HALF = 52, 26
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "AWS service flow"),
    "external": (LINE, 1.6, "6 5", "ah", "External party or control action"),
    "business": (ACCENT, 2.2, None, "ahb", "Business flow"),
}

# ---------------- EDIT: sensitive terms that must never appear on the image ----------------
# Add your AWS account ID, bucket or resource-name prefixes, internal hostnames, and so on.
SENSITIVE_EXTRA = []

# ---------------- EDIT: canvas text ----------------
W, H = 1900, 1220
TITLE = 'GRC Metrics and Board Reporting | AWS Architecture'
SUBTITLE = 'Target design, not yet deployed. Purple lines follow a daily metric from the project stores to the dashboard and board pack.'
REGION = "us-east-1"
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
    """Register an icon at slot (cx, cy) with a service name and an optional role line."""
    assert key not in N, key
    N[key] = (cx, cy, 2 if l2 else 1)
    icons.append((rel, cx, cy, l1, l2))
    w = max(ICON, est_w(l1, 13), est_w(l2 or "", 12))
    BOX[key] = (cx - w / 2, cy - HALF, cx + w / 2, cy + HALF + (36 if l2 else 21))


def draw_nodes():
    for rel, cx, cy, l1, l2 in icons:
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
AX0, AX1, AY0, AY1 = 230, 1670, 110, 874             # AWS Cloud boundary
COLS = [(260, 696), (732, 1168), (1204, 1640)]        # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
ROWS = [(190, 490), (526, 826)]                       # group rows
A0, B0, A1, B1 = 280, 410, 616, 746                   # icon lanes (center y), two per row
XL, XR, CH = 115, 1785, 162                           # external columns, top channel y
G01, BOT = 508, 850                                   # row gutter and bottom channel (y)

# ---------------- canvas and AWS boundary ----------------
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
add(f'<rect x="{AX0}" y="{AY0}" width="32" height="32" fill="{INK}"/>')
text(AX0 + 16, AY0 + 16, "aws", 12, 700, "#FFFFFF")
add(f'<path d="M {AX0+7},{AY0+21} Q {AX0+16},{AY0+27} {AX0+25},{AY0+21}" fill="none" '
    f'stroke="{ORANGE}" stroke-width="2" stroke-linecap="round"/>')
add(f'<path d="M {AX0+21.5},{AY0+19.5} L {AX0+25.5},{AY0+20.5} L {AX0+24.5},{AY0+24.5}" '
    f'fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-linecap="round" '
    f'stroke-linejoin="round"/>')
add(f'<text x="{AX0+44}" y="{AY0+21}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">AWS Cloud<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(REGION)}</tspan></text>')

# ---------------- EDIT: groups, (column, row) -> title ----------------
GROUPS = {
    (0, 0): "Metric sources", (1, 0): "Aggregation", (2, 0): "Metrics store",
    (0, 1): "Dashboard", (1, 1): "Board pack", (2, 1): "Thresholds",
}
for (c, r), title in GROUPS.items():
    (x0, x1), (y0, y1) = COLS[c], ROWS[r]
    group(x0, y0, x1, y1, title)
    # register the title so the line, label, and badge checks also cover group titles
    BOX["title:" + title] = (x0 + 14, y0 + 12, x0 + 14 + est_w(title, 14.5), y0 + 30)

# ---------------- EDIT: nodes ----------------
GEN = "aws/general/"
LAM = "aws/compute/lambda.png"
S3 = "aws/storage/simple-storage-service-s3.png"
SCH = "aws/integration/eventbridge-scheduler.png"
DDB = "aws/database/dynamodb.png"

# external parties
node("leaders", GEN + "users.png", XR, A1, "Leadership", "dashboard, board pack")

# metric sources
node("stores", DDB, SL[0][1], A0, "Amazon DynamoDB", "project stores")
node("hub", "aws/security/security-hub.png", SL[0][2], A0, "AWS Security Hub", "control status")
# aggregation
node("sched", SCH, SL[1][0], A0, "EventBridge Scheduler", "daily, monthly")
node("builder", LAM, SL[1][2], A0, "AWS Lambda", "metrics builder")
# metrics store
node("snap", DDB, SL[2][0], A0, "Amazon DynamoDB", "KRI, KPI snapshots")
node("history", S3, SL[2][2], A0, "Amazon S3", "metrics history")
# dashboard
node("athena", "aws/analytics/athena.png", SL[0][0], A1, "Amazon Athena", "metric queries")
node("qs", "aws/analytics/quicksight.png", SL[0][2], A1, "Amazon QuickSight",
     "executive dashboard")
# board pack
node("pack", LAM, SL[1][0], A1, "AWS Lambda", "board pack builder")
node("packs", S3, SL[1][2], A1, "Amazon S3", "board packs")
node("ses", "aws/engagement/simple-email-service-ses.png", SL[1][2], B1, "Amazon SES",
     "board email")
# thresholds
node("cw", "aws/management/cloudwatch.png", SL[2][0], A1, "Amazon CloudWatch", "KRI alarms")
node("sns", "aws/integration/simple-notification-service-sns.png", SL[2][2], A1, "Amazon SNS",
     "owner alerts")

# ---------------- EDIT: connections (kind: service, external, business) ----------------
P = port
LBY = HALF + 36 + 5      # y offset of the b port (2-line label)

# business flow: a daily metric from the project stores to the dashboard and the board pack
path([P("stores", "t"), (SL[0][1], CH), (SL[1][2] + 12, CH), (SL[1][2] + 12, A0 - HALF - 5)],
     "stores", "builder", "business")
path([P("hub", "t"), (SL[0][2], 175), (SL[1][2] - 12, 175), (SL[1][2] - 12, A0 - HALF - 5)],
     "hub", "builder", "business")
link("builder", "r", "snap", "l", "business")
link("snap", "r", "history", "l", "business")
path([P("history", "t"), (SL[2][2], 150), (250, 150), (250, A1), P("athena", "l")],
     "history", "athena", "business")
link("athena", "r", "qs", "l", "business")
link("qs", "b", "leaders", "b", "business", via=[(SL[0][2], BOT), (XR, BOT)])
link("pack", "r", "packs", "l", "business")
link("packs", "b", "ses", "t", "business")
link("ses", "r", "leaders", "l", "business", via=[(1720, B1), (1720, A1)])

# AWS service flow
link("sched", "r", "builder", "l")                                              # daily
link("sched", "l", "pack", "l", "service", via=[(714, A0), (714, A1)])         # monthly
link("snap", "b", "cw", "l", "service", via=[(SL[2][0], G01), (1186, G01), (1186, A1)])  # KRI values
link("cw", "r", "sns", "l")


# ---------------- EDIT: line labels (white halo keeps them readable over lines) ----------------
def lbl(x, y, s, anchor="start", color=TEXT2):
    """Line label; its box is registered so lines, labels, and badges cannot overlap it."""
    text(x, y, s, 11.5, 400, color, anchor, halo=True)
    w = est_w(s, 11.5)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    BOX["lbl:" + s] = (x0, y - 10, x0 + w, y + 3)


lbl(1300, 440, "KRI values")

draw_nodes()

# ---------------- EDIT: step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(540, 232, 1), (950, 256, 2), (1186, 256, 3), (1422, 256, 4), (480, 592, 5), (1720, 800, 6), (950, 592, 7), (1186, 722, 8), (1422, 592, 9)]:
    badge(cx, cy, n)

# ---------------- EDIT: legend steps, one short sentence each, same order as the badges ----------------
LY = 926
STEPS = [
    'The metrics builder reads the 02, 05, 07, 08, and 10 stores plus Security Hub control status.',
    'Scheduler runs the metrics builder every day.',
    'Daily KRI and KPI snapshots are written to a DynamoDB metrics table.',
    'Each snapshot is also kept in S3 as partitioned Parquet, building the metrics history.',
    'Athena queries the history and feeds the QuickSight executive dashboard.',
    'Leadership reads the dashboard and the monthly board pack.',
    'Each month Scheduler runs the board pack builder, which writes the pack (PDF or HTML) to S3.',
    'SES emails the board pack link to leadership.',
    'CloudWatch alarms fire when a KRI crosses its threshold, and SNS alerts the metric owner.',
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


def sensitive_hits(s):
    """Count sensitive patterns in the SVG, ignoring the embedded base64 icon data."""
    t = re.sub(r"data:image/png;base64,[A-Za-z0-9+/=]+", "DATA", s).lower()
    terms = ["arn:", "@", "amazonaws.com", "cloudfront.net", "execute-api", "lambda-url",
             "buy.stripe.com", "s3://"] + [x for x in SENSITIVE_EXTRA if x]
    hits = {k: t.count(k.lower()) for k in terms}
    hits.update({k: n for k, n in
                 {"12-digit number": len(re.findall(r"(?<!\d)\d{12}(?!\d)", t))}.items()})
    return {k: n for k, n in hits.items() if n}


with open(OUT_SVG, "w") as fh:
    fh.write(svg)
subprocess.run(["rsvg-convert", "-z", "2", "-o", OUT_PNG, OUT_SVG], check=True)
SENS = sensitive_hits(svg)
print("nodes:", len(N), "segments:", len(SEGS), "badges:", len(BADGES))
print("crossings:", len(X), *X)
print("layout problems:", problems if problems else "none")
print("sensitive text:", SENS if SENS else "none")
print("wrote", OUT_SVG, "and", OUT_PNG)
print("next: open the PNG and check it by eye before sharing")
