#!/usr/bin/env python3
"""Round-79 derivative check — is a battery's subject copy a textual derivative of the
committed source it came from?

The channel QUALITY 147 names: round 78 salted the *source text* with an inserted inert
statement, so a four-line normalizer deleted the `_r78<hex>` family and recovered every
subject byte-for-byte (`R78L1/a8-normalizer.py`). A copy is a textual derivative when a
40-byte window of the committed source occurs in the copy.

The check imports the battery under test, calls its copy function
(`reemit(source, work)` for a round-79 battery, `salted_copy(source, work)` for a
round-78 one), and measures the longest common byte window per subject.

Predicate (same sentence as `corpus/evidence/round79/claims.md`, supporting measurement):

  `python3 -B corpus/evidence/round79/derivative-check.py --battery BATTERY`
  exits 0 and prints exactly `DERIVATIVE_COPIES=0/13 MAX_WINDOW=<n>`.

Usage: python3 corpus/evidence/round79/derivative-check.py --battery PATH [--work DIR]
       [--window 40]
Exit: 0 no copy shares a 40-byte window · 1 at least one does · 2 usage/env.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import shutil
import sys


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("battery_under_check", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"derivative-check: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def max_window(src: bytes, copy: bytes, cap: int = 4096) -> int:
    """Longest byte window that occurs in both, capped (a 4 KiB common run is already
    'the whole file')."""
    hi = min(len(src), len(copy), cap)
    if hi < 1:
        return 0

    def ok(length: int) -> bool:
        windows = {src[i:i + length] for i in range(0, len(src) - length + 1)}
        return any(copy[i:i + length] in windows for i in range(0, len(copy) - length + 1))

    if not ok(1):
        return 0
    lo, best = 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if ok(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--battery", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--window", type=int, default=40)
    a = ap.parse_args()
    battery = pathlib.Path(a.battery).resolve()
    if not battery.is_file():
        print(f"derivative-check: missing battery {battery}", file=sys.stderr)
        return 2
    work = pathlib.Path(a.work).resolve() if a.work else pathlib.Path(
        f"/fast/scratch/hyaku/chousa-r79/derivative-{battery.stem}")
    module = load(battery)
    copy_fn = getattr(module, "reemit", None) or getattr(module, "salted_copy", None)
    if copy_fn is None:
        print(f"derivative-check: {battery.name} exposes no reemit/salted_copy", file=sys.stderr)
        return 2
    subjects = ([("POSITIVE", n, p) for n, p in module.POSITIVES]
                + [("FORGER", n, p) for n, p in module.FORGERS])
    work.mkdir(parents=True, exist_ok=True)
    run = work / "run"
    shutil.rmtree(run, ignore_errors=True)
    run.mkdir(parents=True)
    derivative = 0
    worst = 0
    try:
        for group, name, source in subjects:
            source = pathlib.Path(source)
            copy = copy_fn(source, run)
            longest = max_window(source.read_bytes(), copy.read_bytes())
            worst = max(worst, longest)
            flag = longest >= a.window
            derivative += flag
            print(f"SUBJECT {group} {name} window={longest} "
                  f"{'DERIVATIVE' if flag else 'not-a-derivative'}")
            shutil.rmtree(pathlib.Path(copy).parent, ignore_errors=True)
    finally:
        shutil.rmtree(run, ignore_errors=True)
    print(f"DERIVATIVE_COPIES={derivative}/{len(subjects)} MAX_WINDOW={worst}")
    return 0 if derivative == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
