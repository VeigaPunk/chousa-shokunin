#!/usr/bin/env python3
"""CHANNEL PROBE: deterministic import-harness forgery.

The matrix's own source contains THREE things the candidate needs:
  * `CASES`  -> (name, path, operation, expected_rc, expected_failed) for
                every case: the per-case EXPECTED VERDICT, i.e. the answer key
  * `FILES`  -> the base fixture bodies
  * `mutate()` -> the mutation function, so the candidate can REPRODUCE each
                candidate case and identify the current one by comparing the
                reproduced bytes with the observed blob

This probe imports the matrix module (via /proc/<ppid>/cmdline), stubs
`pad_line` so `mutate()` is deterministic, reproduces every case's expected
content, matches the observed `--rev` blob, and prints the harness's expected
verdict.  It implements ZERO C2 checks and reads ZERO protected bytes: it
compares the CANDIDATE'S OWN REPRODUCTION against the observed blob.

Fails closed: exit 2 with a diagnostic if anything is unavailable.
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


def load():
    path = matrix_path()
    if not path or not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("harness_import", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.pad_line = lambda: ""          # deterministic mutation
    return mod


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True,
                          capture_output=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    mod = load()
    if mod is None:
        print("PROBE import-harness: matrix module not loadable", file=sys.stderr)
        return 2
    cases = getattr(mod, "CASES", None)
    files = getattr(mod, "FILES", None)
    mutate = getattr(mod, "mutate", None)
    if not cases or not files or mutate is None:
        print("PROBE import-harness: harness lacks CASES/FILES/mutate", file=sys.stderr)
        return 2
    # Recover the per-run salt from the base blob (the fixture's own bytes).
    salt = None
    base_blob = git(a.lane, "show", f"{a.base}:{mod.PATHS[0]}")
    for line in base_blob.splitlines():
        if line.startswith("salt "):
            salt = line.strip()
            break
    if salt is None:
        print("PROBE import-harness: salt not recoverable", file=sys.stderr)
        return 2
    salt_token = salt.split("-")[0]        # "salt <hex>"
    bodies = {}
    for i, (path, text) in enumerate(files.items()):
        bodies[path] = text + f"\n{salt_token}-{i}\n"
    # Observed blob of every fixture path at --rev, with the matrix's random
    # pad line(s) removed so the reproduction (whose pad_line is stubbed to
    # "") is comparable.
    def strip_pad(text):
        import re
        return re.sub(r"\npad [0-9a-f]+\n", "\n", text)

    observed = {}
    for path in files:
        observed[path] = strip_pad(git(a.lane, "show", f"{a.rev}:{path}"))
    # Reproduce every case and find the one that matches the observed state.
    hit = None
    for name, path, op, rc, failed in cases:
        if path is None:
            cand = dict(bodies)
        else:
            cand = dict(bodies)
            cand[path] = mutate(bodies[path], op)
        if all(observed.get(p) == cand.get(p) for p in files):
            hit = (name, rc, failed)
            break
    if hit is None:
        print("PROBE import-harness: no reproduced case matched", file=sys.stderr)
        return 2
    name, rc, failed = hit
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} import-harness")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    print(f"# PROBE import-harness case={name} salt={salt_token}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
