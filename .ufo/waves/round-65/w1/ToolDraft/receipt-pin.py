#!/usr/bin/env python3
"""Validate R65-C1 receipt consistency, not execution authenticity.

Usage: python3 receipt-pin.py --receipt FILE --root REPOSITORY --revision COMMIT
Exit statuses: 0 consistent, 1 invalid receipt, 2 usage/environment failure.
The SHA256 header hashes the declared Git blob, never the working-tree file.
"""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys


REVISION = re.compile(rb"REVISION=([0-9a-f]{40})")
EXIT = re.compile(rb"EXIT=(0|[1-9][0-9]{0,2})")
DIGEST = re.compile(rb"SHA256=([0-9a-f]{64}) (.+)")
COMMIT = re.compile(r"[0-9a-f]{40}")


class InvalidReceipt(Exception):
    """The supplied receipt does not satisfy the frozen format or binding."""


class EnvironmentFailure(Exception):
    """The validator cannot inspect its required inputs or Git environment."""


def parse_receipt(raw: bytes, expected_revision: str) -> tuple[str, str]:
    """Return the claimed digest and path after checking ordered headers."""
    header, separator, body = raw.partition(b"\n\n")
    if not separator or not body.strip():
        raise InvalidReceipt("separator-or-output")
    lines = header.split(b"\n")
    if len(lines) != 3:
        raise InvalidReceipt("header-count-or-order")
    revision = REVISION.fullmatch(lines[0])
    status = EXIT.fullmatch(lines[1])
    digest = DIGEST.fullmatch(lines[2])
    if revision is None or status is None or digest is None:
        raise InvalidReceipt("header-format")
    if revision[1].decode("ascii") != expected_revision:
        raise InvalidReceipt("revision-mismatch")
    if int(status[1]) > 255:
        raise InvalidReceipt("exit-range")
    path_bytes = digest[2]
    if b"\x00" in path_bytes or b"\r" in path_bytes:
        raise InvalidReceipt("path-format")
    if any(part in (b"", b".", b"..") for part in path_bytes.split(b"/")):
        raise InvalidReceipt("noncanonical-path")
    # os.fsdecode preserves valid POSIX filename bytes for subprocess argv.
    return digest[1].decode("ascii"), os.fsdecode(path_bytes)


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    """Run a read-only Git object operation without replacement objects."""
    try:
        return subprocess.run(
            ["git", "--no-replace-objects", "-C", root, "cat-file", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (OSError, ValueError) as exc:
        raise EnvironmentFailure("git-unavailable") from exc


def validate(root: str, revision: str, claimed_digest: str, path: str) -> None:
    kind = git(root, "-t", revision)
    if kind.returncode != 0:
        raise EnvironmentFailure("repository-or-revision-unavailable")
    if kind.stdout != b"commit\n":
        raise EnvironmentFailure("revision-is-not-commit")
    spec = revision + ":" + path
    kind = git(root, "-t", spec)
    if kind.returncode != 0 or kind.stdout != b"blob\n":
        raise InvalidReceipt("missing-or-nonblob-path")
    blob = git(root, "blob", spec)
    if blob.returncode != 0:
        raise EnvironmentFailure("blob-read-failed")
    if hashlib.sha256(blob.stdout).hexdigest() != claimed_digest:
        raise InvalidReceipt("digest-mismatch")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args(argv)
    if COMMIT.fullmatch(args.revision) is None:
        parser.error("--revision must be a full lowercase 40-hex commit ID")
    try:
        try:
            raw = args.receipt.read_bytes()
        except (OSError, ValueError) as exc:
            raise EnvironmentFailure("receipt-unreadable") from exc
        claimed_digest, path = parse_receipt(raw, args.revision)
        validate(args.root, args.revision, claimed_digest, path)
    except InvalidReceipt as exc:
        print(f"RECEIPT_PIN=FAIL {exc}")
        return 1
    except EnvironmentFailure as exc:
        print(f"RECEIPT_PIN=FAIL {exc}")
        return 2
    print("RECEIPT_PIN=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
