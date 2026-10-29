#!/usr/bin/env python3
"""CritC1Timing probe builder B1 (timing-aware forger). Not a landing candidate; probe for R62-C1 only.

Channels: (1) counts its own calls in /dev/shm, one ledger per counter --work root and profile, where the
profile is cwd.parent.name (`plain` or `neutral`) and the root is cwd.parent.parent; (2) writes os.getpid()
into the ledger on each call; (3) the first call of a profile runs the landing builder; a later call runs the
round-61 base builder, except that a later call with a symlink on --out, out/spans, out/spans.tsv or a cache
entry sleeps 120 s (past the counter's 60 s timeout; the counter SIGKILLs it, rc -9).
Both builders run in-process with __file__ set to this file, so capture-text.py resolves to the fixture copy.
"""
import hashlib
import os
import pathlib
import sys
import time

LANDING = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py"
BASE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round62/controls/base-build-spans.py"


def run_inline(path: str):
    sys.dont_write_bytecode = True
    src = pathlib.Path(path).read_text(encoding="utf-8")
    g = {"__name__": "__main__", "__file__": str(pathlib.Path(__file__).resolve())}
    exec(compile(src, path, "exec"), g)


def arg(flag):
    a = sys.argv
    return a[a.index(flag) + 1] if flag in a and a.index(flag) + 1 < len(a) else None


def symlink_on_path(out: pathlib.Path, cache: pathlib.Path | None) -> bool:
    cands = [out, out / "spans", out / "spans.tsv"]
    try:
        if cache is not None and cache.is_dir():
            cands += list(cache.iterdir())
    except OSError:
        pass
    return any(p.is_symlink() for p in cands)


def main() -> int:
    cwd = pathlib.Path(os.getcwd())
    profile = cwd.parent.name
    if profile not in ("plain", "neutral"):
        run_inline(LANDING)
        return 0
    root = cwd.parent.parent
    tag = hashlib.sha256(str(root).encode()).hexdigest()[:16]
    ledger = pathlib.Path("/dev/shm") / f"critc1timing-{tag}-{profile}"
    with open(ledger, "a") as f:
        f.write(f"{os.getpid()}\n")
    first = ledger.read_text().count("\n") == 1
    out, cache = arg("--out"), arg("--cache")
    if not first and out and symlink_on_path(pathlib.Path(out), pathlib.Path(cache) if cache else None):
        time.sleep(120)
        return 3
    run_inline(LANDING if first else BASE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
