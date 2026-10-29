#!/usr/bin/env python3
"""CritC1Timing probe builder B2 (fixture-mtime forger). Not a landing candidate; probe for R62-C1 only.

Channels: (1) reads the fixture mtimes the counter plants (prior-state and victim files carry mtime 2001-01-01,
OLD_NS in c1v2-count.py): if --out or --cache holds such a file, or --out is not a directory, it runs the landing
builder; (2) any symlink under --out (or on out/spans, out/spans.tsv) or in --cache makes it sleep 120 s past the
counter's 60 s timeout (SIGKILL, rc -9); (3) otherwise it runs the round-61 base builder.
Both builders run in-process with __file__ set to this file, so capture-text.py resolves to the fixture copy.
"""
import os
import pathlib
import sys
import time

LANDING = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py"
BASE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round62/controls/base-build-spans.py"
OLD = 978307200  # 2001-01-01: the counter's planted-state mtime


def run_inline(path: str):
    sys.dont_write_bytecode = True
    src = pathlib.Path(path).read_text(encoding="utf-8")
    g = {"__name__": "__main__", "__file__": str(pathlib.Path(__file__).resolve())}
    exec(compile(src, path, "exec"), g)


def arg(flag):
    a = sys.argv
    return a[a.index(flag) + 1] if flag in a and a.index(flag) + 1 < len(a) else None


def signature(out: pathlib.Path | None, cache: pathlib.Path | None):
    if out is not None and out.is_symlink():
        return "symlink"
    if out is not None and out.exists() and not out.is_dir():
        return "file"
    for base in (out, cache):
        if base is None or not base.is_dir():
            continue
        if base.is_symlink():
            return "symlink"
        for dp, dns, fns in os.walk(base):
            for n in dns + fns:
                p = os.path.join(dp, n)
                if os.path.islink(p):
                    return "symlink"
            for n in fns:
                if int(os.lstat(os.path.join(dp, n)).st_mtime) == OLD:
                    return "planted"
        if base is out and (base / "spans" ).is_symlink():
            return "symlink"
    if cache is not None and cache.is_dir():
        for p in cache.iterdir():
            if p.is_symlink():
                return "symlink"
    return None


def main() -> int:
    out = pathlib.Path(arg("--out")) if arg("--out") else None
    cache = pathlib.Path(arg("--cache")) if arg("--cache") else None
    sig = signature(out, cache)
    if sig == "symlink":
        time.sleep(120)
        return 3
    run_inline(BASE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
