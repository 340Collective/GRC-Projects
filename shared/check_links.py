#!/usr/bin/env python3
"""Offline relative-link checker for the GRC-Projects repo.

Scans every tracked Markdown file (git ls-files '*.md'), skipping .agents/,
and checks that each relative link target exists on disk. Checks inline
links [text](target), images ![alt](target), and HTML src="..." / href="...".
External URLs (http, https, mailto) and pure #anchors are skipped. Any
#anchor or ?query suffix is stripped before the path is resolved.

Run from the repo root:  python3 shared/check_links.py
Exit 0 when nothing is broken, 1 when any link is broken, 2 on misuse.
Standard library only; no network access.
"""

import os
import re
import subprocess
import sys

# [text](target) and ![alt](target); target stops at whitespace or ')'.
MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")
# src="..." or href='...'
HTML_LINK = re.compile(r"""\b(?:src|href)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
SKIP_PREFIXES = ("http://", "https://", "mailto:")


def repo_root_or_exit():
    """Refuse to run anywhere except the repo root."""
    cwd = os.getcwd()
    try:
        top = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("check_links.py: not inside a git repository. Run from the GRC-Projects repo root.")
    if os.path.realpath(top) != os.path.realpath(cwd) or not os.path.isfile(
        os.path.join(cwd, "shared", "check_links.py")
    ):
        print(
            "check_links.py: run this from the GRC-Projects repo root, "
            "for example: python3 shared/check_links.py",
            file=sys.stderr,
        )
        sys.exit(2)
    return cwd


def tracked_markdown():
    out = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        capture_output=True, text=True, check=True,
    ).stdout
    files = [p for p in out.split("\0") if p]
    return sorted(p for p in files if not p.startswith(".agents/"))


def strip_code(text):
    """Drop fenced code blocks and inline code so example syntax is not checked."""
    text = re.sub(r"^(```|~~~).*?^\1[^\n]*$", "", text, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


def targets(text):
    body = strip_code(text)
    for pattern in (MD_LINK, HTML_LINK):
        for match in pattern.finditer(body):
            yield match.group(1).strip()


def main():
    root = repo_root_or_exit()
    files = tracked_markdown()
    checked = 0
    broken = 0
    for path in files:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        base = os.path.dirname(path)
        for target in targets(text):
            if target.lower().startswith(SKIP_PREFIXES) or target.startswith("#"):
                continue
            clean = re.split(r"[#?]", target, maxsplit=1)[0]
            if not clean:
                continue
            checked += 1
            resolved = os.path.normpath(os.path.join(root, base, clean))
            if not os.path.exists(resolved):
                broken += 1
                print(f"{path}: broken link {target}")
    print(f"checked {checked} links in {len(files)} files, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
