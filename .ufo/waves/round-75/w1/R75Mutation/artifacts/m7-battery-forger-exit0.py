#!/usr/bin/env python3
"""Round-75 matrix battery — QUALITY 126 detection-forger battery for the
candidate-running loader matrix.

Unit under test: a MATRIX program that takes `--counter PATH --work DIR` and
exits 0 iff a candidate counter satisfies every case it declares. The battery
runs the matrix against salted copies of two positives and five forgers:

  POSITIVE  successor-counter   corpus/evidence/round74/correction-count.py (the r74 repair)
  POSITIVE  ref-counter         corpus/evidence/round75/ref-counter.py (independent implementation
                                of the same documented contract; agreement proves the matrix's
                                expectations are the contract, not one counter's bytes)
  FORGER    constant-pass       prints all-PASS, reads nothing
  FORGER    constant-fail       prints 6/7, reads nothing
  FORGER    order-oracle        the r74 `R74Critic/forge-order-oracle.py` bytes, unchanged: counts
                                its own invocations and replays the scripted answers
  FORGER    diff-only           reads `git diff --numstat`/`--name-only` only, never a protected file
  FORGER    naive-grep          presence greps instead of exact anchored counts and section scope

Predicate (same sentence as corpus/evidence/round75/claims.md):

  `python3 -B corpus/evidence/round75/matrix-battery.py --matrix MATRIX --work DIR`
  exits 0 and prints exactly `BATTERY=PASS forgers_rejected=5/5 positive=2/2`.

Each subject runs the matrix twice (independent seeds). A forger is REJECTED
only when both runs exit 1 with fewer than full marks; a positive is ACCEPTED
only when both runs exit 0 with full marks and `MATRIX=PASS`. An exit of 2 is
never scored in the matrix's favour.

Limits (recorded, not closed): the battery proves these seven subjects at these
saltings. It does not prove arbitrary-forgery freedom; a forge that fully
re-implements the seven checks is, for these inputs, a correct counter. The
battery is a discrimination floor, and the round's receipt records the exact
matrix digest it measured.

Usage: python3 corpus/evidence/round75/matrix-battery.py --matrix PATH --work DIR [--runs N]
Exit: 0 BATTERY=PASS · 1 BATTERY=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import secrets
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]

POSITIVES = [("successor-counter", HERE.parent / "round74" / "correction-count.py"),
             ("ref-counter", HERE / "ref-counter.py")]
FORGERS = [("constant-pass", HERE / "forgers" / "forge-constant-pass.py"),
           ("constant-fail", HERE / "forgers" / "forge-constant-fail.py"),
           ("order-oracle", HERE / "forgers" / "forge-order-oracle.py"),
           ("diff-only", HERE / "forgers" / "forge-diff-only.py"),
           ("naive-grep", HERE / "forgers" / "forge-naive-grep.py")]

MATRIX_LINE = re.compile(r"^LOADER_MATRIX=(\d+)/(\d+) (?:MATRIX|C1)=(PASS|FAIL)$")


def run_matrix(matrix: pathlib.Path, subject: pathlib.Path, work: pathlib.Path):
    work.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", str(matrix), "--counter", str(subject), "--work", str(work)],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1800)
    marks = None
    for line in p.stdout.splitlines():
        m = MATRIX_LINE.match(line)
        if m:
            marks = (int(m.group(1)), int(m.group(2)), m.group(3))
    return p.returncode, marks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=2)
    a = ap.parse_args()
    matrix = pathlib.Path(a.matrix).resolve()
    work = pathlib.Path(a.work).resolve()
    if not matrix.is_file():
        print(f"matrix-battery: missing matrix {matrix}", file=sys.stderr)
        return 2
    if a.runs < 1:
        print("matrix-battery: --runs must be >= 1", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    print("MATRIX_PATH=" + str(matrix))
    print("MATRIX_SHA256=" + hashlib.sha256(matrix.read_bytes()).hexdigest())
    tally = {"POSITIVE": [0, 0], "FORGER": [0, 0]}
    try:
        for group, subjects in (("POSITIVE", POSITIVES), ("FORGER", FORGERS)):
            for name, source in subjects:
                source = source.resolve()
                if not source.is_file():
                    print(f"matrix-battery: missing subject {source}", file=sys.stderr)
                    return 2
                d = work / name
                d.mkdir()
                salt = secrets.token_hex(8)
                subject = d / "subject.py"
                subject.write_bytes(source.read_bytes() + f"\n# salt {salt}\n".encode())
                runs = []
                for i in range(a.runs):
                    rc, marks = run_matrix(matrix, subject, d / f"w{i}")
                    runs.append((rc, marks))
                    print(f"RUN {group} {name} {i} matrix_exit={rc} "
                          f"marks={'/'.join(str(x) for x in marks) if marks else 'none'}")
                if group == "POSITIVE":
                    ok = all(rc == 0 and marks is not None and marks[0] == marks[1] and marks[2] == "PASS"
                             for rc, marks in runs)
                else:
                    ok = all(rc == 0 and marks is not None and marks[0] < marks[1]
                             for rc, marks in runs)
                tally[group][0] += ok
                tally[group][1] += 1
                label = ("ACCEPTED" if ok else "MISS") if group == "POSITIVE" else ("REJECTED" if ok else "ACCEPTED")
                print(f"SUBJECT {group} {name} sha256={hashlib.sha256(source.read_bytes()).hexdigest()[:16]} "
                      f"{label}")
                shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    p_ok, p_all = tally["POSITIVE"]
    f_ok, f_all = tally["FORGER"]
    verdict = p_ok == p_all and f_ok == f_all
    print(f"forgers_rejected={f_ok}/{f_all} positive={p_ok}/{p_all}")
    print(f"BATTERY={'PASS' if verdict else 'FAIL'} forgers_rejected={f_ok}/{f_all} positive={p_ok}/{p_all}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
