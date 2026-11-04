#!/usr/bin/env python3
"""R75Critic — run every forger twice through the frozen r75 matrix.

Usage: python3 -B run-attempts.py [name ...]
Writes one log per (forger, run) next to this file under logs/ and prints a
summary: forger, run, matrix exit, LOADER_MATRIX=k/12, failing case names.
"""
import pathlib
import re
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent
SCRATCH = pathlib.Path("/fast/scratch/hyaku/chousa-r75/R75Critic")
MATRIX = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py")
LINE = re.compile(r"^LOADER_MATRIX=(\d+)/(\d+) MATRIX=(PASS|FAIL)$")
CASE = re.compile(r"^CASE (\S+) (PASS|FAIL) expected_rc=(\d+) actual_rc=(\d+) failed=(\S+) "
                  r"expected_failed=(\S+) base=(\S+) rev=(\S+)$")


def attempts():
    return sorted(p for p in OUT.glob("forge-*.py"))


def main() -> int:
    wanted = sys.argv[1:]
    (OUT / "logs").mkdir(exist_ok=True)
    rows = []
    for forger in attempts():
        if wanted and forger.stem not in wanted:
            continue
        for run in (0, 1):
            work = SCRATCH / f"work-{forger.stem}-{run}"
            work.mkdir(parents=True, exist_ok=True)
            p = subprocess.run([sys.executable, "-B", str(MATRIX), "--counter", str(forger),
                                "--work", str(work)], capture_output=True, text=True,
                               stdin=subprocess.DEVNULL)
            log = OUT / "logs" / f"{forger.stem}-run{run}.txt"
            log.write_text(p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr else ""))
            marks, fails = "none", []
            for line in p.stdout.splitlines():
                m = LINE.match(line)
                if m:
                    marks = f"{m.group(1)}/{m.group(2)}"
                c = CASE.match(line)
                if c and c.group(2) == "FAIL":
                    fails.append(f"{c.group(1)}[want={c.group(6)} got={c.group(5)} rc={c.group(4)}]")
            rows.append((forger.stem, run, p.returncode, marks, "; ".join(fails) or "-"))
            print(f"{forger.stem:34s} run{run} exit={p.returncode} LOADER_MATRIX={marks}")
            if fails:
                print(f"{'':34s}   mismatch: {'; '.join(fails)}")
    print()
    print(f"RUNS={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
