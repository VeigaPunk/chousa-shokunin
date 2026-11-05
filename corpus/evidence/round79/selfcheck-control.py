#!/usr/bin/env python3
"""Round-79 self-assessment controls — the two false-greens round 78's counter accepted.

Case `hollow`: the base tree plus three *hollow* repair lines (the right words, a wrong
cell count and wrong digests). Round 78's `selfcheck.py` accepts presence only, so it
prints PASS; the successor must refuse it.

Case `window`: the base tree plus a newer `## Round-<n> addition` block. Round 78's pointer
audit keeps only the newest block, so criterion 116's unresolved pointer disappears from
the audit and it prints PASS; the successor audits every block and must refuse it.

Each case is a `git clone --shared` mirror under `--work`, so the counters' `git ls-files`
resolution universe is a real repository and nothing writes the lane.

Usage: python3 corpus/evidence/round79/selfcheck-control.py --lane DIR --work DIR
Exit: 0 both counters behaved as predicted · 1 not · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

HOLLOW_SKILL = "correction: SKILL.md:168 cells=8 digest=0000000000000000\n"
HOLLOW_QUALITY = ("150. **A hollow superseder names the criterion it supersedes and resolves "
                  "its own pointers.** corpus/QUALITY.md supersedes: 116 digest=deadbeefdeadbeef\n")
HOLLOW_LESSON = "erratum: round-77.md:73 digest=deadbeefdeadbeef\n"
WINDOW_BLOCK = ("\n## Round-999 addition\n\n150. **A newest-block criterion whose pointers "
                "resolve.** corpus/QUALITY.md\n")


def run(counter: pathlib.Path, lane: pathlib.Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-B", str(counter), "--lane", str(lane)],
                       capture_output=True, text=True)
    last = [line for line in p.stdout.splitlines()
            if line.startswith(("SELFCHECK=", "SELFCHECK2="))]
    return p.returncode, (last[-1] if last else "no-predicate-line")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--base", required=True, help="base revision the mirrors are cloned at")
    ap.add_argument("--v1", default=None)
    ap.add_argument("--v2", default=None)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    v1 = pathlib.Path(a.v1).resolve() if a.v1 else \
        lane / "corpus/evidence/round78/selfcheck.py"
    v2 = pathlib.Path(a.v2).resolve() if a.v2 else \
        lane / "corpus/evidence/round79/selfcheck-v2.py"
    for counter in (v1, v2):
        if not counter.is_file():
            print(f"selfcheck-control: missing counter {counter}", file=sys.stderr)
            return 2
    work.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str, int, str]] = []
    for case in ("hollow", "window"):
        mirror = work / f"mirror-{case}"
        shutil.rmtree(mirror, ignore_errors=True)
        p = subprocess.run(["git", "clone", "--shared", "-q", str(lane), str(mirror)],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print(f"selfcheck-control: clone failed: {p.stderr.strip()}", file=sys.stderr)
            return 2
        p = subprocess.run(["git", "-C", str(mirror), "checkout", "-q", a.base],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print(f"selfcheck-control: cannot check out {a.base}: {p.stderr.strip()}",
                  file=sys.stderr)
            return 2
        if case == "hollow":
            with (mirror / "SKILL.md").open("a") as fh:
                fh.write(HOLLOW_SKILL)
            with (mirror / "corpus/QUALITY.md").open("a") as fh:
                fh.write(HOLLOW_QUALITY)
            with (mirror / "corpus/lessons/round-77.md").open("a") as fh:
                fh.write(HOLLOW_LESSON)
        else:
            with (mirror / "corpus/QUALITY.md").open("a") as fh:
                fh.write(WINDOW_BLOCK)
        for label, counter in (("v1", v1), ("v2", v2)):
            rc, line = run(counter, mirror)
            results.append((case, label, rc, line))
            print(f"CASE {case} {label} rc={rc} {line}")
    ok = (all(rc == 0 and line.startswith("SELFCHECK=PASS")
              for case, label, rc, line in results if label == "v1")
          and all(rc == 1 and line.startswith("SELFCHECK2=FAIL")
                  for case, label, rc, line in results if label == "v2"))
    print(f"CONTROL={'PASS' if ok else 'FAIL'} cases={len(results)} "
          f"v1_false_greens={sum(1 for c, l, r, s in results if l == 'v1' and r == 0)}/2 "
          f"v2_refusals={sum(1 for c, l, r, s in results if l == 'v2' and r == 1)}/2")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
