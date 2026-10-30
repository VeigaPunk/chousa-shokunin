#!/usr/bin/env python3
"""Check a research receipt's header consistency against a pinned Git blob.

Validates the frozen round-65 receipt format: REVISION=<40 lowercase hex>,
EXIT=<decimal 0..255 reported child exit>, SHA256=<64 lowercase hex>
<canonical repo-relative POSIX path>, one empty separator line, then a
nonempty body; exactly one of each header, in that order. The revision must
equal the caller-selected --revision and the digest must match
``git -C ROOT cat-file blob REVISION:PATH`` -- committed bytes, never the
working tree. Header consistency is NOT execution authenticity: a PASS proves
only that the receipt is self-consistent with the selected blob, not that a
command truly ran or that the body is truthful. Read-only Git; no writes.
Exits 0 consistent (RECEIPT_PIN=PASS), 1 malformed or inconsistent
(RECEIPT_PIN=FAIL ...), 2 usage/environment.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

REVISION_RE = re.compile(r"[0-9a-f]{40}")
EXIT_RE = re.compile(r"EXIT=(?:0|[1-9][0-9]{0,2})")
DIGEST_RE = re.compile(r"SHA256=([0-9a-f]{64}) (.+)")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--receipt", required=True, help="receipt file to validate")
    p.add_argument("--root", required=True, help="lane/repository root for Git")
    p.add_argument("--revision", required=True, help="full lowercase 40-hex commit id")
    a = p.parse_args()
    if not REVISION_RE.fullmatch(a.revision):
        p.error("--revision requires a full lowercase 40-hex object id")
    try:
        lines = pathlib.Path(a.receipt).read_text(encoding="utf-8").splitlines()
        if len(lines) < 5:
            raise ValueError("receipt needs four header lines, an empty separator and a body")
        if lines[0] != "REVISION=" + a.revision:
            raise ValueError("REVISION header missing or not the selected revision")
        if not EXIT_RE.fullmatch(lines[1]) or int(lines[1][5:]) > 255:
            raise ValueError("EXIT header must be the reported child exit, decimal 0..255")
        m = DIGEST_RE.fullmatch(lines[2])
        if not m:
            raise ValueError("SHA256 header must be 64 lowercase hex plus a relative path")
        rel = pathlib.PurePosixPath(m.group(2))
        if rel.is_absolute() or not rel.parts or ".." in rel.parts or str(rel) != m.group(2):
            raise ValueError("path must be canonical and repository-relative")
        if lines[3] != "":
            raise ValueError("header block must be followed by one empty separator line")
        if not "\n".join(lines[4:]).strip():
            raise ValueError("receipt body must be nonempty")
        blob = subprocess.run(
            ["git", "-C", a.root, "cat-file", "blob", a.revision + ":" + m.group(2)],
            capture_output=True,
        )
        if blob.returncode != 0:
            raise ValueError("no blob " + a.revision + ":" + m.group(2) + " in --root")
        if hashlib.sha256(blob.stdout).hexdigest() != m.group(1):
            raise ValueError("digest does not match the pinned blob bytes")
    except (OSError, UnicodeError, ValueError) as e:
        print("RECEIPT_PIN=FAIL " + str(e))
        return 1
    print("RECEIPT_PIN=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
