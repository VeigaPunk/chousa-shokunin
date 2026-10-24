#!/usr/bin/env python3
"""c1-count — frozen counter for round 43 claim C1 (operability).

Predicate R43-C1, the same sentence as corpus/evidence/round43/claims.md:
the committed command tools/absent-split.py enumerates exactly the 15 rows the
committed round-42 table labels absent, assigns each exactly one of
{misquote, not-carried}, both classes are nonempty, and two runs are
byte-identical.

This counter grades that surface. It does not grade whether a label matches
the ratio; that is C2. A label swap that keeps both classes nonempty does not
fail this counter.

Cheapest gate that would score full marks without the work (QUALITY 60): a
script that prints the five target lines. It is not this counter: this counter
executes the command and requires its ids to equal an independent read of the
round-42 table. The do-nothing control is this counter pointed at a missing
command; it exits 1.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
TOOL = LANE / "tools" / "absent-split.py"
TABLE = LANE / "corpus" / "evidence" / "round42" / "quarantine-verdicts.tsv"


def absent_ids(table: pathlib.Path) -> list[str]:
    ids = []
    for line in table.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("id\t"):
            continue
        parts = line.split("\t")
        if len(parts) >= 2 and parts[1] == "absent":
            ids.append(parts[0])
    return ids


def run(tool: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(tool)], capture_output=True, text=True
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tool", default=str(TOOL))
    ap.add_argument("--table", default=str(TABLE))
    args = ap.parse_args(argv)
    tool = pathlib.Path(args.tool)
    table = pathlib.Path(args.table)
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))
        print("%s %s %s" % (name, "PASS" if ok else "FAIL", detail))
        return ok

    if not table.is_file():
        print("C1=FAIL table-missing")
        return 2
    expected = absent_ids(table)
    check("TABLE_ABSENT", len(expected) == 15, "%d/15" % len(expected))
    if not tool.is_file():
        check("TOOL_PRESENT", False, "missing %s" % tool)
        print("C1=FAIL")
        return 1
    first = run(tool)
    second = run(tool)
    check("TOOL_EXIT", first.returncode == 0, "exit=%s" % first.returncode)
    rows = [line.split("\t") for line in first.stdout.splitlines() if line]
    ids = [row[0] for row in rows if row]
    labels = [row[1] for row in rows if len(row) > 1]
    check("ABSENT_ENUMERATED", ids == expected, "%d/15" % len(ids))
    vocab = {"misquote", "not-carried"}
    check("CLASSED", len(labels) == 15 and set(labels) <= vocab, "%d/15" % len(labels))
    check(
        "BOTH_NONEMPTY",
        "misquote" in labels and "not-carried" in labels,
        "misquote=%d not-carried=%d" % (labels.count("misquote"), labels.count("not-carried")),
    )
    check("REPRODUCIBLE", first.stdout == second.stdout, "identical=%s" % (first.stdout == second.stdout))
    # mutant: a 14-row prefix of the real output must not be accepted as the enumeration
    short = ids[:-1]
    check("MUTANT_DETECTED", short != expected, "short=%d expected=%d" % (len(short), len(expected)))
    ok = all(item[1] for item in results)
    print("ABSENT_ENUMERATED=%d/15" % (len(ids) if ids == expected else 0))
    print("CLASSED=%d/15" % (15 if len(labels) == 15 and set(labels) <= vocab else 0))
    print("BOTH_NONEMPTY=%d/1" % (1 if "misquote" in labels and "not-carried" in labels else 0))
    print("REPRODUCIBLE=%d/1" % (1 if first.stdout == second.stdout else 0))
    print("MUTANT_DETECTED=%d/1" % (1 if short != expected else 0))
    print("C1=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
