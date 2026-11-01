#!/usr/bin/env python3
"""Create a reproducible Lambda bundle locally. This script never calls AWS."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def main():
    destination = ROOT / "dist/grc-bcdr-lambda.zip"
    destination.parent.mkdir(exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source in sorted((ROOT / "src").rglob("*.py")):
            member = ZipInfo(source.relative_to(ROOT / "src").as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            member.compress_type = ZIP_DEFLATED
            member.external_attr = 0o644 << 16
            archive.writestr(member, source.read_bytes())
    sha = hashlib.sha256(destination.read_bytes()).hexdigest()
    artifact = {"file": destination.name, "sha256": sha, "s3_key": "grc-bcdr/" + sha + ".zip", "runtime": "python3.13", "runtime_dependency": "AWS-provided boto3"}
    (ROOT / "dist/lambda-artifact.json").write_text(json.dumps(artifact, indent=2) + "\n")
    print(json.dumps(artifact, indent=2))


if __name__ == "__main__":
    main()
