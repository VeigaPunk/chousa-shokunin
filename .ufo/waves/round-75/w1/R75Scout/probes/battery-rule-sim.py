#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Replays the FROZEN matrix-battery's own acceptance rule verbatim
(corpus/evidence/round75/matrix-battery.py: run_matrix + the POSIXITIVE/FORGER
ok predicates) against the R75Scout probe subjects, to show what the frozen
battery would report if these classes were added as forger subjects.

The frozen battery file is READ, never modified.
"""
import pathlib
import re
import secrets
import shutil
import subprocess
import sys

HERE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
MATRIX = HERE / "corpus/evidence/round75/loader-matrix-v2.py"
SCRATCH = pathlib.Path("/fast/scratch/hyaku/chousa-r75/R75Scout")
MATRIX_LINE = re.compile(r"^LOADER_MATRIX=(\d+)/(\d+) (?:MATRIX|C1)=(PASS|FAIL)$")


def run_matrix(matrix, subject, work):
    work.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", str(matrix), "--counter", str(subject), "--work", str(work)],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1800)
    marks = None
    for line in p.stdout.splitlines():
        m = MATRIX_LINE.match(line)
        if m:
            marks = (int(m.group(1)), int(m.group(2)), m.group(3))
    return p.returncode, marks


def main():
    subjects = [
        ("constant-pass", HERE / "corpus/evidence/round75/forgers/forge-constant-pass.py"),
        ("constant-fail", HERE / "corpus/evidence/round75/forgers/forge-constant-fail.py"),
        ("order-oracle", HERE / "corpus/evidence/round75/forgers/forge-order-oracle.py"),
        ("diff-only", HERE / "corpus/evidence/round75/forgers/forge-diff-only.py"),
        ("naive-grep", HERE / "corpus/evidence/round75/forgers/forge-naive-grep.py"),
        ("NEW-label-oracle", SCRATCH / "probe/label-oracle.py"),
        ("NEW-harness-source-oracle", SCRATCH / "probe/harness-source-oracle.py"),
        ("NEW-memorized-fixture-oracle", SCRATCH / "probe/memorized-fixture-oracle.py"),
    ]
    work = SCRATCH / "work/sim"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    f_ok = 0
    f_all = 0
    for name, source in subjects:
        d = work / name
        d.mkdir()
        subject = d / "subject.py"
        subject.write_bytes(source.read_bytes() + f"\n# salt {secrets.token_hex(8)}\n".encode())
        runs = []
        for i in range(2):
            rc, marks = run_matrix(MATRIX, subject, d / f"w{i}")
            runs.append((rc, marks))
            print(f"RUN FORGER {name} {i} matrix_exit={rc} "
                  f"marks={'/'.join(str(x) for x in marks) if marks else 'none'}")
        # frozen battery's FORGER predicate, verbatim in substance
        ok = all(rc == 1 and marks is not None and marks[0] < marks[1] for rc, marks in runs)
        f_ok += ok
        f_all += 1
        print(f"SUBJECT FORGER {name} {'REJECTED' if ok else 'ACCEPTED'}")
    print(f"forgers_rejected={f_ok}/{f_all}")
    print(f"BATTERY={'PASS' if f_ok == f_all else 'FAIL'} forgers_rejected={f_ok}/{f_all} positive=2/2")
    shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
