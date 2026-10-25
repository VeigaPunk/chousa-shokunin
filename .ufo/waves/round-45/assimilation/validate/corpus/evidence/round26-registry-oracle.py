#!/usr/bin/env python3
"""Independent oracle for round-26 verify-metadata --registry semantics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SOURCE_ID_RE = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
REGISTRY_ID_RE = re.compile(r"S[0-9]{3,}\Z")
KEY_RE = re.compile(r"^(source|verified-at|recheck):(.*)$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
VERIFIED_DATE_RE = re.compile(r"^[ \t]*[0-9]{4}-[0-9]{2}-[0-9]{2}")
SEPARATOR_RE = re.compile(r":?-{3,}:?\Z")


def split_table_row(line: str) -> list[str] | None:
    """Split contract-valid pipe-delimited cells literally."""
    text = line.strip()
    if not text or "|" not in text:
        return None
    return [cell.strip() for cell in text.strip("|").split("|")]

def registry_rows(path: Path) -> dict[str, tuple[str, str]]:
    """Read the first qualifying id/status/used-by Markdown table."""
    text = path.read_bytes().decode("utf-8")
    lines = [line.removesuffix("\r") for line in text.split("\n")]
    required = {"id", "status", "used-by"}

    for index in range(len(lines) - 1):
        header = split_table_row(lines[index])
        separator = split_table_row(lines[index + 1])
        if header is None or separator is None or len(header) != len(separator):
            continue
        if not all(SEPARATOR_RE.fullmatch(cell) for cell in separator):
            continue
        if not required.issubset(header):
            continue

        columns = {name: header.index(name) for name in required}
        records: dict[str, tuple[str, str]] = {}
        row_index = index + 2
        while row_index < len(lines):
            row = split_table_row(lines[row_index])
            if row is None:
                break
            if all(SEPARATOR_RE.fullmatch(cell) for cell in row):
                break
            identifier = row[columns["id"]].strip() if columns["id"] < len(row) else ""
            if REGISTRY_ID_RE.fullmatch(identifier):
                status = row[columns["status"]].strip() if columns["status"] < len(row) else ""
                used_by = row[columns["used-by"]].strip() if columns["used-by"] < len(row) else ""
                records.setdefault(identifier, (status, used_by))
            row_index += 1
        return records

    raise ValueError("registry has no table with id, status, and used-by columns")


def metadata_values(path: Path) -> dict[str, str]:
    """Collect last-key-wins values in the fence-aware pre-heading header."""
    text = path.read_bytes().decode("utf-8")
    lines = [line.removesuffix("\r") for line in text.split("\n")]
    found: dict[str, list[str]] = {}
    active_key: str | None = None
    fence_char: str | None = None
    fence_length = 0

    for line in lines:
        if not line.strip():
            active_key = None
        if fence_char is not None:
            if active_key is not None:
                found[active_key].append(line)
            closing = FENCE_CLOSE_RE.fullmatch(line)
            if closing is not None:
                marker = closing.group(1)
                if marker[0] == fence_char and len(marker) >= fence_length:
                    fence_char = None
                    fence_length = 0
            continue

        opening = FENCE_RE.fullmatch(line)
        if opening is not None:
            if active_key is not None:
                found[active_key].append(line)
            marker = opening.group(1)
            fence_char = marker[0]
            fence_length = len(marker)
            continue
        if line.startswith("## "):
            break
        if not line.strip():
            continue

        key_match = KEY_RE.fullmatch(line)
        if key_match is not None:
            active_key = key_match.group(1)
            found[active_key] = [key_match.group(2)]
        elif active_key is not None:
            found[active_key].append(line)

    return {key: "\n".join(value) for key, value in found.items()}


def registry_path_tokens(value: str) -> set[str]:
    tokens: set[str] = set()
    for raw in value.split(","):
        token = raw.strip()
        if token.startswith("./"):
            token = token[2:]
        tokens.add(token)
    return tokens


def expected_findings(entry: Path, root: Path, records: dict[str, tuple[str, str]]) -> list[str]:
    values = metadata_values(entry)
    source_ids = set(SOURCE_ID_RE.findall(values.get("source", "")))
    findings: set[str] = set()
    if not source_ids:
        findings.add("META_SOURCE_NO_ROW_ID")

    relative_path = entry.resolve().relative_to(root.resolve()).as_posix()
    for identifier in source_ids:
        record = records.get(identifier)
        if record is None:
            findings.add("META_SOURCE_ROW_MISSING")
            continue
        status, used_by = record
        if status != "mined":
            findings.add("META_SOURCE_NOT_MINED")
        elif relative_path not in registry_path_tokens(used_by):
            findings.add("META_SOURCE_USEDBY_MISSING")

    verified_at = values.get("verified-at")
    if verified_at is not None:
        date_match = VERIFIED_DATE_RE.match(verified_at)
        if date_match is not None and not verified_at[date_match.end():].strip():
            findings.add("META_VERIFIED_AT_BARE")
    return sorted(findings)


def selected_entries(path: Path) -> list[Path]:
    if path.is_dir():
        entries = sorted(candidate for candidate in path.glob("*.md") if candidate.is_file())
    elif path.is_file() and path.suffix == ".md":
        entries = [path]
    else:
        raise ValueError("entry path must be a .md file or directory")
    if not entries:
        raise ValueError("entry directory has no .md files")
    return entries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="one knowledge entry or a directory of entries")
    parser.add_argument("--root", required=True, type=Path, help="repository root used for used-by matching")
    parser.add_argument("--registry", required=True, type=Path, help="SOURCES.md-shaped registry")
    args = parser.parse_args(argv)

    try:
        records = registry_rows(args.registry)
        entries = selected_entries(args.path)
        result = {
            entry.name: expected_findings(entry, args.root, records)
            for entry in entries
        }
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"round26-registry-oracle: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
