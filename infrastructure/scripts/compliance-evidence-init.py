#!/usr/bin/env python3
"""
Build a compliance evidence folder structure in S3 from an ASFF control matrix.

Layout created (S3 has no real folders; these are key prefixes):

  <prefix>/INDEX.md                                  # generated overview
  <prefix>/<framework-slug>/_framework.json          # framework summary
  <prefix>/<framework-slug>/<control-id>/_control.json
  <prefix>/<framework-slug>/<control-id>/README.md   # what to drop here

Evidence artifacts (screenshots, JSON exports, configs) are added later by you
or by automation, one control folder at a time.

The bucket is temporary (objects expire, no Object Lock); teardown empties it, including versions, before the stack is deleted.

Reads the control matrix from:
  * .xlsx  (requires openpyxl: pip3 install openpyxl), or
  * .csv / .tsv

Two matrix shapes are auto-detected:
  1. Tidy   : a "framework"/"standard" column + a control-id column (+ optional
              title/requirement columns). One row per (control, framework).
  2. Indexed: one row per control, one COLUMN per framework. A non-empty cell
              means the control maps to that framework (cell value is kept as
              the framework-specific requirement id).

Safety:
  * Dry-run by default. Prints the tree it would create. Pass --apply to write.
  * Writing only ever PUTs small metadata/placeholder objects; it never deletes.
  * Uses the standard AWS profile chain (default profile 340collective).

Usage:
  # Preview from the Excel matrix (no AWS calls):
  python3 scripts/compliance-evidence-init.py --matrix ASFF-Control-Matrix-Indexed.xlsx

  # Write the structure into the evidence bucket:
  python3 scripts/compliance-evidence-init.py \
      --matrix ASFF-Control-Matrix-Indexed.xlsx \
      --bucket 340collective-compliance-evidence --apply

  # Materialize locally instead of S3 (good for review / git):
  python3 scripts/compliance-evidence-init.py --matrix matrix.xlsx --local ./evidence

Flags:
  --matrix PATH     .xlsx/.csv/.tsv control matrix (optional; without it, only
                    the canonical framework folders are scaffolded).
  --sheet NAME      Worksheet to read for .xlsx (default: first sheet).
  --bucket NAME     Target S3 bucket (required for --apply).
  --prefix P        Root prefix (default: evidence/).
  --local DIR       Write to a local directory instead of S3.
  --apply           Actually write to S3 (otherwise dry-run).
  AWS_PROFILE       default 340collective    AWS_REGION default us-east-1
"""
import os
import re
import io
import sys
import csv
import json
import argparse
import datetime

# Canonical Security Hub / ASFF standard slugs. Free-text framework names from
# the matrix are normalized against these where possible.
CANON = {
    "fsbp": "aws-foundational-security-best-practices",
    "foundational": "aws-foundational-security-best-practices",
    "aws foundational security best practices": "aws-foundational-security-best-practices",
    "cis": "cis-aws-foundations-benchmark",
    "cis aws foundations benchmark": "cis-aws-foundations-benchmark",
    "pci": "pci-dss",
    "pci dss": "pci-dss",
    "pci-dss": "pci-dss",
    "nist": "nist-sp-800-53-rev-5",
    "nist 800-53": "nist-sp-800-53-rev-5",
    "nist sp 800-53": "nist-sp-800-53-rev-5",
    "nist-800-53": "nist-sp-800-53-rev-5",
    "nist csf": "nist-csf",
    "iso": "iso-27001",
    "iso 27001": "iso-27001",
    "soc": "soc-2",
    "soc 2": "soc-2",
    "soc2": "soc-2",
}

# Used only when no matrix is supplied: scaffold empty framework folders.
DEFAULT_FRAMEWORKS = [
    "aws-foundational-security-best-practices",
    "cis-aws-foundations-benchmark",
    "pci-dss",
    "nist-sp-800-53-rev-5",
]


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).strip().lower()).strip("-")
    return s or "unknown"


def norm_framework(name):
    key = str(name).strip().lower()
    if key in CANON:
        return CANON[key]
    for frag, canon in CANON.items():
        if frag in key:
            return canon
    return slug(name)


def safe_control_id(cid):
    # Keep control ids filesystem/S3 friendly but recognizable (e.g. "S3.5", "2.1.1").
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(cid).strip()).strip("_") or "unknown"


# ---- matrix loading ------------------------------------------------------

def load_rows(path, sheet):
    """Return (headers, rows) where rows are lists of cell strings."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".tsv"):
        delim = "\t" if ext == ".tsv" else ","
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=delim)
            data = [[(c or "").strip() for c in row] for row in reader if any(row)]
        if not data:
            sys.exit("Matrix is empty: %s" % path)
        return data[0], data[1:]
    if ext in (".xlsx", ".xlsm"):
        try:
            from openpyxl import load_workbook
        except ImportError:
            sys.exit("Reading .xlsx needs openpyxl: pip3 install openpyxl "
                     "(or export the matrix to .csv and pass that).")
        wb = load_workbook(path, read_only=True, data_only=True)
        ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
        rows = []
        for r in ws.iter_rows(values_only=True):
            cells = [("" if c is None else str(c)).strip() for c in r]
            if any(cells):
                rows.append(cells)
        if not rows:
            sys.exit("Worksheet '%s' is empty." % (sheet or wb.sheetnames[0]))
        return rows[0], rows[1:]
    sys.exit("Unsupported matrix type '%s' (use .xlsx, .csv, or .tsv)." % ext)


def find_col(headers, *needles):
    for i, h in enumerate(headers):
        hl = h.lower()
        if any(n in hl for n in needles):
            return i
    return None


def parse_matrix(headers, rows):
    """
    Return dict: framework-slug -> { control_id: {title, requirement, ref} }.
    Auto-detects tidy vs indexed layouts.
    """
    fw_col = find_col(headers, "framework", "standard")
    id_col = find_col(headers, "control id", "control", "check id", "check", "id")
    title_col = find_col(headers, "title", "name", "description")
    req_col = find_col(headers, "requirement", "mapping", "reference", "ref")

    result = {}

    def add(fw, cid, title="", requirement="", ref=""):
        fslug = norm_framework(fw)
        cid = safe_control_id(cid)
        if not cid or cid == "unknown":
            return
        result.setdefault(fslug, {})
        entry = result[fslug].setdefault(cid, {"title": "", "requirement": "", "ref": ""})
        if title and not entry["title"]:
            entry["title"] = title
        if requirement and not entry["requirement"]:
            entry["requirement"] = requirement
        if ref and not entry["ref"]:
            entry["ref"] = ref

    if fw_col is not None and id_col is not None:
        # Tidy layout: one row per (control, framework).
        for row in rows:
            def cell(i):
                return row[i] if i is not None and i < len(row) else ""
            fw = cell(fw_col)
            cid = cell(id_col)
            if not fw or not cid:
                continue
            add(fw, cid, cell(title_col), cell(req_col))
        return result

    if id_col is not None:
        # Indexed layout: one row per control; every other column is a framework.
        meta_cols = {id_col, title_col, req_col}
        fw_cols = [i for i in range(len(headers)) if i not in meta_cols and headers[i]]
        for row in rows:
            def cell(i):
                return row[i] if i is not None and i < len(row) else ""
            cid = cell(id_col)
            if not cid:
                continue
            title = cell(title_col)
            for i in fw_cols:
                val = cell(i)
                if not val or val.strip().lower() in ("n/a", "na", "-", "no", "false", "0"):
                    continue
                # cell value is the framework-specific requirement id/reference
                add(headers[i], cid, title, requirement=val, ref=val)
        return result

    sys.exit("Could not find a control-id column in the matrix headers: %r\n"
             "Rename a column to include 'Control ID' (and optionally 'Framework')."
             % headers)


# ---- object materialization ---------------------------------------------

def build_objects(structure, prefix, source_note):
    """Yield (key, text) pairs to write."""
    now = datetime.date.today().isoformat()
    frameworks = sorted(structure.keys())

    # Root index.
    lines = [
        "# Compliance Evidence Index",
        "",
        "Generated %s. Source: %s" % (now, source_note),
        "",
        "Structure: `%s<framework>/<control-id>/<evidence files>`" % prefix,
        "",
        "| Framework | Controls |",
        "| --- | --- |",
    ]
    for fw in frameworks:
        lines.append("| %s | %d |" % (fw, len(structure[fw])))
    lines += ["", "Drop evidence artifacts (JSON exports, screenshots, configs,",
              "policy documents) directly into the matching control folder."]
    yield (prefix + "INDEX.md", "\n".join(lines) + "\n")

    for fw in frameworks:
        controls = structure[fw]
        yield (
            "%s%s/_framework.json" % (prefix, fw),
            json.dumps({
                "framework": fw,
                "control_count": len(controls),
                "generated": now,
                "source": source_note,
            }, indent=2) + "\n",
        )
        for cid in sorted(controls):
            meta = controls[cid]
            base = "%s%s/%s/" % (prefix, fw, cid)
            yield (
                base + "_control.json",
                json.dumps({
                    "framework": fw,
                    "control_id": cid,
                    "title": meta.get("title", ""),
                    "requirement": meta.get("requirement", ""),
                    "reference": meta.get("ref", ""),
                    "status": "not-started",
                    "evidence": [],
                    "generated": now,
                }, indent=2) + "\n",
            )
            readme = [
                "# %s / %s" % (fw, cid),
                "",
                meta.get("title", "").strip() or "_(no title in matrix)_",
                "",
            ]
            if meta.get("requirement"):
                readme += ["**Requirement / mapping:** %s" % meta["requirement"], ""]
            readme += [
                "## Evidence to collect here",
                "- Configuration export or policy document proving this control.",
                "- Dated screenshot or CLI output (include the command run).",
                "- Link to the Security Hub finding / control ARN if applicable.",
                "",
                "Update `_control.json` `status` to `in-progress` or `met` and",
                "list filenames under `evidence` as you add them.",
            ]
            yield (base + "README.md", "\n".join(readme) + "\n")


def write_local(objects, root):
    n = 0
    for key, text in objects:
        path = os.path.join(root, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        n += 1
    print("Wrote %d files under %s/" % (n, root))


def write_s3(objects, bucket):
    try:
        import boto3
    except ImportError:
        sys.exit("boto3 is required for --apply: pip3 install boto3")
    profile = os.environ.get("AWS_PROFILE", "340collective")
    region = os.environ.get("AWS_REGION", "us-east-1")
    try:
        sess = boto3.Session(profile_name=profile, region_name=region)
    except Exception:
        sess = boto3.Session(region_name=region)
    s3 = sess.client("s3")
    n = 0
    for key, text in objects:
        ctype = "application/json" if key.endswith(".json") else "text/markdown"
        s3.put_object(Bucket=bucket, Key=key, Body=text.encode("utf-8"),
                      ContentType=ctype)
        n += 1
    print("Put %d objects into s3://%s/" % (n, bucket))


def print_tree(structure, prefix):
    total = 0
    for fw in sorted(structure):
        controls = structure[fw]
        total += len(controls)
        print("%s%s/  (%d controls)" % (prefix, fw, len(controls)))
        shown = sorted(controls)
        for cid in shown[:8]:
            title = controls[cid].get("title", "")
            print("    %s/%s" % (cid, ("  - " + title) if title else ""))
        if len(shown) > 8:
            print("    ... (+%d more)" % (len(shown) - 8))
    print("\nFrameworks: %d   Controls (framework x control): %d"
          % (len(structure), total))


def main():
    p = argparse.ArgumentParser(description="Build S3 compliance evidence folders from an ASFF control matrix")
    p.add_argument("--matrix", help=".xlsx/.csv/.tsv control matrix")
    p.add_argument("--sheet", default=None, help="worksheet name for .xlsx")
    p.add_argument("--bucket", default=None, help="target S3 bucket")
    p.add_argument("--prefix", default="evidence/", help="root prefix (default evidence/)")
    p.add_argument("--local", default=None, help="write to a local dir instead of S3")
    p.add_argument("--apply", action="store_true", help="actually write to S3")
    args = p.parse_args()

    prefix = args.prefix if args.prefix.endswith("/") else args.prefix + "/"

    if args.matrix:
        headers, rows = load_rows(args.matrix, args.sheet)
        structure = parse_matrix(headers, rows)
        source = os.path.basename(args.matrix)
        if not structure:
            sys.exit("No frameworks/controls parsed from the matrix. Check the headers.")
    else:
        structure = {fw: {} for fw in DEFAULT_FRAMEWORKS}
        source = "canonical framework scaffold (no matrix supplied)"

    print("Root prefix: %s" % prefix)
    print_tree(structure, prefix)

    objects = list(build_objects(structure, prefix, source))
    print("\nTotal objects to create: %d" % len(objects))

    if args.local:
        write_local(objects, args.local)
        return

    if not args.apply:
        print("\nDry run. Re-run with --bucket <name> --apply to write to S3, "
              "or --local <dir> to materialize locally.")
        return

    if not args.bucket:
        sys.exit("--apply requires --bucket <name>.")
    write_s3(objects, args.bucket)


if __name__ == "__main__":
    main()
