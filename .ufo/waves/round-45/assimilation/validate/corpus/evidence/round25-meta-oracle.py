#!/usr/bin/env python3
"""Independent stdlib oracle for the registered round-25 verify-metadata v1 spec."""

from __future__ import annotations

import argparse
import datetime as _datetime
import os
import re
import sys
from pathlib import Path

KEY_RE = re.compile(r"^(source|verified-at|recheck):(.*)$")
VERIFIED_PREFIX_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}")
ISO_DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
DAYS_RE = re.compile(r"^[0-9]+d$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def lines_with_cr_stripped(path: Path) -> list[str]:
    """Read UTF-8 lines, removing only a trailing CR from each LF-delimited line."""
    with path.open("r", encoding="utf-8", newline="") as stream:
        return [line.removesuffix("\r") for line in stream.read().split("\n")]


def header_bounds(lines: list[str]) -> tuple[int, list[bool]]:
    """Return the header end and whether each preceding line is outside a fence."""
    outside: list[bool] = []
    fence_char: str | None = None
    fence_size = 0
    for index, line in enumerate(lines):
        fence_match = FENCE_RE.match(line)
        if fence_char is None:
            if fence_match:
                marker = fence_match.group(1)
                outside.append(False)
                fence_char, fence_size = marker[0], len(marker)
                continue
            outside.append(True)
            if line.startswith("## "):
                return index, outside
            continue

        outside.append(False)
        if fence_match:
            marker = fence_match.group(1)
            remainder = fence_match.group(2)
            if (marker[0] == fence_char and len(marker) >= fence_size
                    and remainder.strip() == ""):
                fence_char = None
                fence_size = 0

    return len(lines), outside


def metadata_values(lines: list[str]) -> dict[str, str]:
    end, outside = header_bounds(lines)
    found: dict[str, str] = {}
    for index in range(end):
        if not outside[index]:
            continue
        match = KEY_RE.match(lines[index])
        if not match:
            continue
        key, first_value = match.groups()
        # L1 v1 clarification: recognized duplicate keys use the last value.
        pieces = [first_value]
        cursor = index + 1
        while cursor < end:
            if lines[cursor].strip() == "":
                break
            if outside[cursor] and KEY_RE.match(lines[cursor]):
                break
            pieces.append(lines[cursor])
            cursor += 1
        found[key] = "\n".join(pieces).strip()
    return found


def is_iso_date(token: str) -> bool:
    if not ISO_DATE_RE.fullmatch(token):
        return False
    try:
        _datetime.date.fromisoformat(token)
    except ValueError:
        return False
    return True


def has_parent_root(value: str) -> bool:
    # L1 integration fix (round 25 differential): the seat's whitespace split
    # kept quoting punctuation glued to `..` (a backtick-quoted command ends
    # "..`"), so the spec's "value passes --root .." was missed; strip it.
    tokens = [t.strip("`'\"();,") for t in value.split()]
    return any(tokens[i] == "--root" and tokens[i + 1] == ".."
               for i in range(len(tokens) - 1))


def inspect_entry(path: Path, strict: bool) -> tuple[list[str], bool, bool]:
    values = metadata_values(lines_with_cr_stripped(path))
    source_value = values.get("source")
    verified_value = values.get("verified-at")
    recheck_value = values.get("recheck")

    source_present = source_value is not None  # presence-only contract, even empty
    if source_value is None:
        source_state = "absent"
    else:
        source_state = "present" if source_present else "absent"

    if verified_value is None:
        verified_state = "absent"
    elif VERIFIED_PREFIX_RE.match(verified_value.lstrip()):
        verified_state = "dated"
    else:
        verified_state = "undated"

    if recheck_value is None:
        recheck_state = "absent"
    else:
        first_token = recheck_value.split()[0] if recheck_value.split() else ""
        if (is_iso_date(first_token) or DAYS_RE.fullmatch(first_token)
                or first_token == "on-release"):
            recheck_state = "scheduled"
        else:
            recheck_state = "unscheduled"

    findings: list[tuple[str, str]] = []
    if not source_present:
        findings.append(("META_SOURCE_ABSENT", "warn"))
    if verified_state == "absent":
        findings.append(("META_VERIFIED_AT_ABSENT", "warn"))
    elif verified_state == "undated":
        findings.append(("META_VERIFIED_AT_UNDATED", "warn"))
    if recheck_state == "absent":
        findings.append(("META_RECHECK_ABSENT", "warn"))
    elif recheck_state == "unscheduled":
        findings.append(("META_RECHECK_UNSCHEDULED", "info"))
    if recheck_value is not None and has_parent_root(recheck_value):
        findings.append(("META_RECHECK_ROOT_PARENT", "info"))

    drift = any(severity == "warn" for _, severity in findings)
    if strict and any(severity == "info" for _, severity in findings):
        drift = True

    basename = path.name
    output = [
        f"META entry={basename} source={source_state} "
        f"verified_at={verified_state} recheck={recheck_state} "
        f"verdict={'drift' if drift else 'clean'}"
    ]
    output.extend(
        f"FINDING {finding_id} severity={severity} surface=metadata obs=entry={basename}"
        for finding_id, severity in findings
    )
    complete = source_present and verified_state == "dated" and recheck_value is not None
    return output, complete, drift


def selected_files(raw_path: str) -> list[Path]:
    path = Path(raw_path)
    if path.is_dir():
        candidates = [child for child in path.iterdir()
                      if child.name.endswith(".md") and child.is_file()]
        candidates.sort(key=lambda child: os.fsencode(child.name))
        if not candidates:
            raise ValueError("directory has no .md files")
        return candidates
    if path.is_file() and path.name.endswith(".md"):
        return [path]
    raise ValueError("PATH is missing, unreadable, or is not a .md file/directory")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="round25-meta-oracle.py")
    parser.add_argument("path", help="one .md file or a directory of direct .md children")
    parser.add_argument("--root", help="accepted for the registered command shape")
    args = parser.parse_args(argv)

    try:
        paths = selected_files(args.path)
        # Read all entries before emitting output so an unreadable member cannot
        # leave a misleading partial screen.
        results = [inspect_entry(path, os.environ.get("CHOUSA_STRICT") == "1")
                   for path in paths]
    except (OSError, UnicodeError, ValueError) as error:
        print(f"verify-metadata: {error}", file=sys.stderr)
        return 2

    complete_count = sum(1 for _, complete, _ in results if complete)
    drift = any(entry_drift for _, _, entry_drift in results)
    for output, _, _ in results:
        for line in output:
            print(line)
    print(f"METADATA_COMPLETE={complete_count}/{len(results)}")
    print(f"RESEARCH_GATE: {'DRIFT' if drift else 'CLEAN'}")
    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
