#!/usr/bin/env python3
"""Round-76 matrix battery — QUALITY 126 / 135 / 137 for the answer-key-salted matrix.

Unit under test: a MATRIX program that takes `--counter PATH --work DIR` and exits 0
iff a candidate counter satisfies every case it declares. The battery runs the matrix
against salted copies of two positives and eleven forgers:

  POSITIVE  successor-counter   corpus/evidence/round74/correction-count.py
  POSITIVE  ref-counter         corpus/evidence/round75/ref-counter.py (independent
                                implementation; agreement proves the matrix encodes the
                                documented contract, not one counter's bytes)
  FORGER    constant-pass       prints all-PASS, reads nothing
  FORGER    constant-fail       prints 6/7, reads nothing
  FORGER    order-twelve        twelve scripted answers by invocation count — the
                                declared-order oracle round 75 left as a survivor
  FORGER    diff-only           reads `git diff --numstat`/`--name-only` only
  FORGER    naive-grep          presence greps instead of anchored counts and scope
  FORGER    subject-map         reads the commit subject only (the r75 answer key)
  FORGER    tree-identity       reads `rev^{tree}`/`base^{tree}` only (tree memo class)
  FORGER    size-map            reads `ls-tree -l` sizes only (metadata size class)
  FORGER    harness-source      reads the matrix's own source through the parent's
                                `/proc/<ppid>/cmdline` and replays its declared order
  FORGER    seed-leak           reads the parent's stdout fd for a replayable seed
  FORGER    hang                sleeps past the matrix's child bound

Predicate (same sentence as `corpus/evidence/round76/claims.md`):

  `python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix MATRIX --work DIR`
  exits 0 and prints exactly
  `BATTERY=PASS forgers_rejected=11/11 positive=2/2`.

Each subject runs the matrix twice (independent seeds). A forger is REJECTED only
when both runs exit 1 with fewer than full marks; a positive is ACCEPTED only when
both runs exit 0 with full marks and `MATRIX=PASS`. An exit of 2 is never scored in
the matrix's favour.

Answer-key hygiene of the battery itself (QUALITY 137): each subject copy is written
under a random directory name (never the forger's name) and carries a random salt
line, so a subject cannot read its own identity from `argv` or its path. The child
bound is passed to the matrix through `LOADER_MATRIX_CHILD_TIMEOUT` (seconds); the
matrix writes the seed digest only.

Limits (recorded, not closed): the battery proves these thirteen subjects at these
saltings. It does not prove arbitrary-forgery freedom; a counter that reads the
unified patch text or re-implements every check is correct for these inputs. The
round's receipts pin the exact matrix and subject digests measured.

Usage: python3 corpus/evidence/round76/matrix-battery-v3.py --matrix PATH --work DIR
       [--runs N]
Exit: 0 BATTERY=PASS · 1 BATTERY=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import re
import secrets
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]

POSITIVES = [("successor-counter", LANE / "corpus/evidence/round74/correction-count.py"),
             ("ref-counter", LANE / "corpus/evidence/round75/ref-counter.py")]
FORGERS = [("constant-pass", HERE / "forgers" / "forge-constant-pass.py"),
           ("constant-fail", HERE / "forgers" / "forge-constant-fail.py"),
           ("order-twelve", HERE / "forgers" / "forge-order-twelve.py"),
           ("diff-only", HERE / "forgers" / "forge-diff-only.py"),
           ("naive-grep", HERE / "forgers" / "forge-naive-grep.py"),
           ("subject-map", HERE / "forgers" / "forge-subject-map.py"),
           ("tree-identity", HERE / "forgers" / "forge-tree-identity.py"),
           ("size-map", HERE / "forgers" / "forge-size-map.py"),
           ("harness-source", HERE / "forgers" / "forge-harness-source.py"),
           ("seed-leak", HERE / "forgers" / "forge-seed-leak.py"),
           ("hang", HERE / "forgers" / "forge-hang.py")]

MATRIX_LINE = re.compile(r"^LOADER_MATRIX=(\d+)/(\d+) (?:MATRIX|C1)=(PASS|FAIL)$")
CHILD_TIMEOUT = "3"


def run_matrix(matrix: pathlib.Path, subject: pathlib.Path, work: pathlib.Path,
               matrix_timeout: int):
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=CHILD_TIMEOUT)
    try:
        p = subprocess.run([sys.executable, "-B", str(matrix), "--counter", str(subject), "--work", str(work)],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=matrix_timeout, env=env)
    except subprocess.TimeoutExpired:
        return None, None
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
    ap.add_argument("--matrix-timeout", type=int, default=300)
    a = ap.parse_args()
    matrix = pathlib.Path(a.matrix).resolve()
    work = pathlib.Path(a.work).resolve()
    if not matrix.is_file():
        print(f"matrix-battery-v3: missing matrix {matrix}", file=sys.stderr)
        return 2
    if a.runs < 1 or a.matrix_timeout < 1:
        print("matrix-battery-v3: --runs and --matrix-timeout must be >= 1", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    print("MATRIX_PATH=" + str(matrix))
    print("MATRIX_SHA256=" + hashlib.sha256(matrix.read_bytes()).hexdigest())
    print(f"RUNS={a.runs} CHILD_TIMEOUT={CHILD_TIMEOUT} MATRIX_TIMEOUT={a.matrix_timeout}")
    tally = {"POSITIVE": [0, 0], "FORGER": [0, 0]}
    try:
        for group, subjects in (("POSITIVE", POSITIVES), ("FORGER", FORGERS)):
            for name, source in subjects:
                source = source.resolve()
                if not source.is_file():
                    print(f"matrix-battery-v3: missing subject {source}", file=sys.stderr)
                    return 2
                d = work / secrets.token_hex(8)  # never the subject's name (QUALITY 137)
                d.mkdir()
                salt = secrets.token_hex(8)
                subject = d / "subject.py"
                subject.write_bytes(source.read_bytes() + f"\n# salt {salt}\n".encode())
                runs = []
                for i in range(a.runs):
                    rc, marks = run_matrix(matrix, subject, d / f"w{i}", a.matrix_timeout)
                    runs.append((rc, marks))
                    print(f"RUN {group} {name} {i} matrix_exit={'timeout' if rc is None else rc} "
                          f"marks={'/'.join(str(x) for x in marks) if marks else 'none'}")
                if group == "POSITIVE":
                    ok = all(rc == 0 and marks is not None and marks[0] == marks[1] and marks[2] == "PASS"
                             for rc, marks in runs)
                else:
                    ok = (runs[0][0] == 1 and runs[0][1] is not None
                          and runs[0][1][0] < runs[0][1][1])  # MUTANT B01: first run only
                tally[group][0] += ok
                tally[group][1] += 1
                label = ("ACCEPTED" if ok else "MISS") if group == "POSITIVE" else ("REJECTED" if ok else "MISS")
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
