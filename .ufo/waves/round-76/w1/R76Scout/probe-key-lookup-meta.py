#!/usr/bin/env python3
"""CHANNEL PROBE: harness answer-key lookup + METADATA-ONLY case identity.

Same as probe-key-lookup.py except the case identity comes only from git
metadata (--name-only / --numstat / ls-tree sizes): never from patch text or
blob content.  This isolates how much of the answer key survives when the
content channel is closed.

Fails closed: exit 2 with a diagnostic when the identity is ambiguous.
"""
import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def matrix_path():
    try:
        raw = Path(f"/proc/{os.getppid()}/cmdline").read_bytes()
    except OSError:
        return None
    for token in raw.split(b"\0"):
        name = token.decode("utf-8", "replace")
        if name.endswith(".py") and "matrix" in Path(name).name:
            return Path(name)
    return None


def load_cases():
    path = matrix_path()
    if not path or not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("harness_probe_meta", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "CASES", None), path


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True,
                          capture_output=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    loaded = load_cases()
    if not loaded or not loaded[0]:
        print("PROBE key-lookup-meta: harness CASES table unavailable", file=sys.stderr)
        return 2
    cases, hpath = loaded
    names = git(a.lane, "diff", "--name-only", a.base, a.rev).split()
    numstat = git(a.lane, "diff", "--numstat", a.base, a.rev).splitlines()
    sig = None
    for ln in numstat:
        parts = ln.split("\t")
        if len(parts) >= 3:
            sig = (parts[2], parts[0], parts[1])
    if not names:
        cands = [c for c in cases if c[1] is None]
    else:
        cands = [c for c in cases if c[1] == names[0]]
    if sig is None:
        cands = [c for c in cands if c[2] in ("same",)]
    else:
        _p, add, dele = sig
        if add == "0" and dele != "0":
            ops = ("delete", "replace")
        elif add != "0" and dele == "0":
            ops = ("append", "dup-log", "dup-lesson", "dup-card")
        else:
            ops = ("replace", "delete")
        cands = [c for c in cands if c[2] in ops]
    verdicts = {(c[3], frozenset(c[4])) for c in cands}
    if len(verdicts) != 1:
        print(f"PROBE key-lookup-meta: ambiguous identity "
              f"names={names} numstat={sig} cands={[(c[0], c[2]) for c in cands]}", file=sys.stderr)
        return 2
    rc, failed = verdicts.pop()
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} key-lookup-meta")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    print(f"# PROBE key-lookup-meta names={names} numstat={sig}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
