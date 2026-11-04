#!/usr/bin/env python3
"""Probe: does the v5 salt-anchor rule exclude the `__future__` floor?

Round-78 instrument defect 1 (reported by the L1): `salted_copy()` inserted its inert
statement before a random top-level statement, and when the drawn anchor was the subject's
`from __future__ import annotations` line the copy no longer compiled, so the positive
controls missed.

Three legs over the positive controls the round's instruments use:

  battery   `corpus/evidence/round74/correction-count.py`,
            `corpus/evidence/round75/ref-counter.py`  (matrix-battery-v5 `POSITIVES`)
  forge     `corpus/evidence/round76/loader-matrix-v3.py`  (forge-battery `POSITIVE`)

  naive     anchors = every top-level statement line except a bare-string Expr (the rule
            before the floor guard); each anchor exercised with `import os as _r78probe`
  guarded   the same set restricted to `n.lineno > max(__future__ import lines)` (the rule
            at `matrix-battery-v5.py` lines 203-212)
  frozen    the frozen `salted_copy()` itself, imported by path, 20 copies per subject

Every copy is checked with `compile(text, path, "exec")`: the future-position rule is a
compiler rule, so `ast.parse` alone does not see it.

Fail-closed: exit 0 only when the naive rule breaks at least one copy, the guarded rule
breaks none and the frozen transform breaks none; 1 when the red leg does not reproduce;
2 on setup failure.

Usage: python3 -B probe-salt-future.py --lane LANE --work DIR
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import pathlib
import sys

POSITIVES = [("battery:successor-counter", "corpus/evidence/round74/correction-count.py"),
             ("battery:ref-counter", "corpus/evidence/round75/ref-counter.py"),
             ("forge:legit-matrix", "corpus/evidence/round76/loader-matrix-v3.py")]
INERT = "import os as _r78probe\n"
COPIES = 20


def anchors(text: str) -> tuple[list[int], list[int], int]:
    body = ast.parse(text).body
    futures = [n.lineno for n in body
               if isinstance(n, ast.ImportFrom) and n.module == "__future__"]
    floor = max(futures) if futures else 0
    plain = [n.lineno for n in body
             if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                     and isinstance(n.value.value, str))]
    guarded = [n for n in plain if n > floor]
    return plain, guarded, floor


def broken(text: str, name: str) -> str | None:
    try:
        compile(text, name, "exec")
    except SyntaxError as exc:
        return f"{exc.msg} (line {exc.lineno})"
    return None


def insert(text: str, lineno: int) -> str:
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines.insert(lineno - 1, INERT)
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    battery = lane / "corpus/evidence/round78/matrix-battery-v5.py"
    if not battery.is_file():
        print(f"probe: missing {battery}", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("matrix_battery_v5_r78", battery)
    if spec is None or spec.loader is None:
        print("probe: cannot load the frozen transform", file=sys.stderr)
        return 2
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    naive_broken = guarded_broken = frozen_broken = 0
    first = ""
    for label, rel in POSITIVES:
        path = lane / rel
        if not path.is_file():
            print(f"probe: missing positive {path}", file=sys.stderr)
            return 2
        text = path.read_text()
        plain, guarded, floor = anchors(text)
        nbad = [m for m in (broken(insert(text, ln), rel) for ln in plain) if m]
        gbad = [m for m in (broken(insert(text, ln), rel) for ln in guarded) if m]
        copies = [mod.salted_copy(path, work) for _ in range(COPIES)]
        fbad = [m for m in (broken(p.read_text(), rel) for p in copies) if m]
        naive_broken += len(nbad)
        guarded_broken += len(gbad)
        frozen_broken += len(fbad)
        for msg in nbad:
            print(f"NAIVE_FAIL {rel}:{floor} {msg}")
        if nbad and not first:
            first = f"{rel}:{floor} {nbad[0]}"
        print(f"SUBJECT {label} {rel} top_level={len(plain)} future_floor={floor} "
              f"naive_anchors={len(plain)} naive_broken={len(nbad)} "
              f"guarded_anchors={len(guarded)} guarded_broken={len(gbad)} "
              f"frozen_copies={COPIES} frozen_broken={len(fbad)}")
    print(f"FIRST_NAIVE_FAILURE={first or 'none'}")
    ok = naive_broken > 0 and guarded_broken == 0 and frozen_broken == 0
    print(f"SALT_FUTURE={'REPRODUCED' if ok else 'NOT-REPRODUCED'} "
          f"naive_broken={naive_broken} guarded_broken={guarded_broken} "
          f"frozen_broken={frozen_broken}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
