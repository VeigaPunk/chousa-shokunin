#!/usr/bin/env bash
# Independent differential for verify-metadata --as-of date arithmetic.
# Run from any directory as:
#   bash corpus/evidence/round26-date-differential.sh [PATH-TO-RESEARCH-GATE.SH]
# It generates bounded temporary metadata fixtures, drives the CLI, and compares
# each due/freshness pair to Python's datetime implementation of spec v1.
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
REPO_ROOT=$(cd -- "$SCRIPT_DIR/../.." && pwd -P)
if (($# > 1)); then
  printf 'usage: %s [PATH-TO-RESEARCH-GATE.SH]\n' "$0" >&2
  exit 2
fi
GATE=${1:-"$REPO_ROOT/tools/research-gate.sh"}

python3 - "$GATE" <<'PY'
from datetime import date, timedelta
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile

if len(sys.argv) != 2:
    raise SystemExit("internal error: missing gate path")
gate = Path(sys.argv[1]).resolve()
if not gate.is_file():
    raise SystemExit(f"gate not found: {gate}")

DAY_COUNTS = (0, 1, 28, 29, 30, 31, 59, 60, 90, 180, 365, 366, 1000, 36500)
SAMPLED_YEARS = range(1900, 2101)
SPECIAL_YEARS = (*range(1999, 2002), *range(2096, 2102))
LINE_RE = re.compile(
    r"^META entry=(\S+).*?\bdue=(\S+)\s+freshness=(\S+)(?:\s|$)"
)
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DAYS_RE = re.compile(r"^(\d+)d$")


def parse_iso(value):
    if not ISO_RE.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def oracle(verified_at, recheck, as_of):
    """Return spec-v1 (due, freshness), independently via datetime."""
    due = None
    if ISO_RE.fullmatch(recheck):
        due = parse_iso(recheck)
    else:
        days_match = DAYS_RE.fullmatch(recheck)
        verified_match = re.match(r"^\s*(\d{4}-\d{2}-\d{2})", verified_at)
        verified = parse_iso(verified_match.group(1)) if verified_match else None
        if days_match and verified is not None:
            try:
                due = verified + timedelta(days=int(days_match.group(1)))
            except (OverflowError, ValueError):
                due = None
    if due is None:
        return ("unknown", "unknown")
    as_of_date = parse_iso(as_of)
    if as_of_date is None:
        raise AssertionError("test harness produced an invalid --as-of date")
    return (due.isoformat(), "overdue" if as_of_date > due else "current")


def write_fixtures(directory, cases):
    directory.mkdir()
    for index, (verified_at, recheck, _label) in enumerate(cases):
        name = f"case-{index:05d}.md"
        (directory / name).write_text(
            "source: S001\n"
            f"verified-at: {verified_at}\n"
            f"recheck: {recheck}\n\n"
            "## Details\nfixture\n",
            encoding="utf-8",
        )


counts = {"agree": 0, "total": 0}
mismatches = []
with tempfile.TemporaryDirectory(prefix="round26-date-diff-") as temporary:
    root = Path(temporary).resolve()
    env = dict(os.environ)
    env["CHOUSA_STRICT"] = "0"

    def run_batch(label, cases, as_of):
        nonlocal_counts = len(cases)
        if nonlocal_counts == 0:
            raise AssertionError(f"empty differential batch: {label}")
        fixture_dir = root / label
        write_fixtures(fixture_dir, cases)
        command = [
            "bash", str(gate), "verify-metadata", str(fixture_dir),
            "--root", str(root), "--as-of", as_of,
        ]
        result = subprocess.run(
            command, cwd=root, env=env, text=True, capture_output=True,
            check=False,
        )
        observed = {}
        for line in result.stdout.splitlines():
            match = LINE_RE.search(line)
            if match:
                name, due, freshness = match.groups()
                if name in observed:
                    mismatches.append(
                        f"{label}: duplicate output for {name}: {line}"
                    )
                observed[name] = (due, freshness)
        if result.returncode not in (0, 1):
            detail = (result.stderr or result.stdout).strip().replace("\n", " | ")
            mismatches.append(
                f"{label}: gate exit={result.returncode} (expected 0/1): {detail[:300]}"
            )
        for index, (verified_at, recheck, case_label) in enumerate(cases):
            name = f"case-{index:05d}.md"
            expected = oracle(verified_at, recheck, as_of)
            actual = observed.get(name)
            ok = result.returncode in (0, 1) and actual == expected
            counts["total"] += 1
            if ok:
                counts["agree"] += 1
            else:
                mismatches.append(
                    f"{label}/{case_label} as_of={as_of}: "
                    f"expected={expected} actual={actual} exit={result.returncode}"
                )

    # Date samples span every year 1900–2100. Detailed month/leap boundaries
    # are added for 1999–2001 and 2096–2101; all arithmetic magnitudes are
    # crossed with each sampled verified-at date.
    sampled_dates = set()
    for year in SAMPLED_YEARS:
        sampled_dates.update((date(year, 1, 1), date(year, 6, 30), date(year, 12, 31)))
    for year in SPECIAL_YEARS:
        sampled_dates.update((date(year, 2, 28), date(year, 3, 1), date(year, 12, 31)))
        try:
            sampled_dates.add(date(year, 2, 29))
        except ValueError:
            pass

    sampled_cases = [
        (verified.isoformat() + " checked", f"{days}d", f"sample-{verified}-{days}d")
        for verified in sorted(sampled_dates)
        for days in DAY_COUNTS
    ]
    run_batch("sampled-dates", sampled_cases, "2201-01-01")

    # For each boundary due date, use every N and test --as-of immediately
    # before, on, and after the calculated due date. This makes equality
    # explicitly current and exercises leap/century carries in both directions.
    boundary_due_dates = (
        date(2000, 2, 29), date(2000, 3, 1), date(2001, 1, 1),
        date(2096, 2, 29), date(2100, 3, 1), date(2101, 1, 1),
    )
    for boundary_index, due in enumerate(boundary_due_dates):
        cases = [
            ((due - timedelta(days=days)).isoformat() + " checked", f"{days}d",
             f"boundary-{due}-{days}d")
            for days in DAY_COUNTS
        ]
        for offset, as_of_date in ((-1, due - timedelta(days=1)), (0, due), (1, due + timedelta(days=1))):
            run_batch(
                f"boundary-{boundary_index}-asof-{offset:+d}", cases,
                as_of_date.isoformat(),
            )

    # Explicit calendar rechecks are independent of verified-at and receive the
    # same strict before/equal/after freshness checks.
    iso_due_dates = (
        date(1900, 2, 28), date(1900, 3, 1), date(1999, 12, 31),
        date(2000, 2, 28), date(2000, 2, 29), date(2000, 3, 1),
        date(2001, 1, 1), date(2096, 2, 29), date(2100, 2, 28),
        date(2100, 3, 1), date(2101, 1, 1),
    )
    for iso_index, due in enumerate(iso_due_dates):
        cases = [("2000-01-01 checked", due.isoformat(), f"iso-{due}")]
        for offset, as_of_date in ((-1, due - timedelta(days=1)), (0, due), (1, due + timedelta(days=1))):
            run_batch(
                f"iso-{iso_index}-asof-{offset:+d}", cases,
                as_of_date.isoformat(),
            )

    invalid_cases = (
        ("2026-01-01 checked", "2026-02-30", "invalid-iso-recheck"),
        ("2026-02-30 checked", "30d", "invalid-verified-at"),
        ("not-a-date checked", "30d", "undated-verified-at"),
    )
    run_batch("invalid-calendar", invalid_cases, "2026-03-01")

print(f"DATE_DIFF_AGREE={counts['agree']}/{counts['total']}")
if mismatches:
    for detail in mismatches[:40]:
        print(f"DISAGREE {detail}", file=sys.stderr)
    if len(mismatches) > 40:
        print(f"DISAGREE ... {len(mismatches) - 40} additional mismatch details", file=sys.stderr)
    raise SystemExit(1)
if counts["total"] == 0:
    raise SystemExit("empty differential")
PY
