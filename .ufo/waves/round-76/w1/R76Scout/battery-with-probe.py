#!/usr/bin/env python3
"""Battery COPY with one extra forger subject (the scout's harness-table probe).

This is a SCRATCH COPY of corpus/evidence/round76/matrix-battery-v3.py with a
twelfth forger appended.  The frozen battery file is NOT modified: the copy
lives under this seat's scratch and is deleted before the seat yields.  The
frozen matrix under test is byte-identical (path given on the command line).
"""
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
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
FROZEN = LANE / "corpus/evidence/round76"

POSITIVES = [("successor-counter", LANE / "corpus/evidence/round74/correction-count.py"),
             ("ref-counter", LANE / "corpus/evidence/round75/ref-counter.py")]
FORGERS = [("constant-pass", FROZEN / "forgers" / "forge-constant-pass.py"),
           ("constant-fail", FROZEN / "forgers" / "forge-constant-fail.py"),
           ("order-twelve", FROZEN / "forgers" / "forge-order-twelve.py"),
           ("diff-only", FROZEN / "forgers" / "forge-diff-only.py"),
           ("naive-grep", FROZEN / "forgers" / "forge-naive-grep.py"),
           ("subject-map", FROZEN / "forgers" / "forge-subject-map.py"),
           ("tree-identity", FROZEN / "forgers" / "forge-tree-identity.py"),
           ("size-map", FROZEN / "forgers" / "forge-size-map.py"),
           ("harness-source", FROZEN / "forgers" / "forge-harness-source.py"),
           ("seed-leak", FROZEN / "forgers" / "forge-seed-leak.py"),
           ("hang", FROZEN / "forgers" / "forge-hang.py"),
           # --- the scout's extra subject ---------------------------------
           ("harness-table-lookup", HERE / "probe-key-lookup.py")]

MATRIX_LINE = re.compile(r"^LOADER_MATRIX=(\d+)/(\d+) (?:MATRIX|C1)=(PASS|FAIL)$")
CHILD_TIMEOUT = "3"


def run_matrix(matrix, subject, work, matrix_timeout):
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--matrix-timeout", type=int, default=300)
    a = ap.parse_args()
    matrix = pathlib.Path(a.matrix).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    print("MATRIX_PATH=" + str(matrix))
    print("MATRIX_SHA256=" + hashlib.sha256(matrix.read_bytes()).hexdigest())
    print(f"RUNS={a.runs} CHILD_TIMEOUT={CHILD_TIMEOUT}")
    tally = {"POSITIVE": [0, 0], "FORGER": [0, 0]}
    for group, subjects in (("POSITIVE", POSITIVES), ("FORGER", FORGERS)):
        for name, source in subjects:
            source = source.resolve()
            d = work / secrets.token_hex(8)
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
                ok = all(rc == 1 and marks is not None and marks[0] < marks[1]
                         for rc, marks in runs)
            tally[group][0] += ok
            tally[group][1] += 1
            label = ("ACCEPTED" if ok else "MISS") if group == "POSITIVE" else ("REJECTED" if ok else "MISS")
            print(f"SUBJECT {group} {name} sha256={hashlib.sha256(source.read_bytes()).hexdigest()[:16]} {label}")
            shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(work, ignore_errors=True)
    p_ok, p_all = tally["POSITIVE"]
    f_ok, f_all = tally["FORGER"]
    verdict = p_ok == p_all and f_ok == f_all
    print(f"forgers_rejected={f_ok}/{f_all} positive={p_ok}/{p_all}")
    print(f"BATTERY={'PASS' if verdict else 'FAIL'} forgers_rejected={f_ok}/{f_all} positive={p_ok}/{p_all}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
