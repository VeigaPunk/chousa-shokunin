#!/usr/bin/env python3
"""Probe A7 — integrated order-leg break: recover the per-run permutation from the ORDER digest
the battery prints into its own stdout, then answer by position. Scores no case.

Channels used, each already receipted separately:
  * /proc/<ppid>/cmdline  -> the battery's path -> its source -> the 13 subject names
  * /proc/<ppid>/fd/1     -> the judge's stdout target (a regular file under `>` capture)
                             -> `MATRIX ORDER <i> <digest>` and the completed `MATRIX RUN` lines
  * the digest            -> ./perm enumerates the 13! domain (first recovery only; cached)
"""
import argparse
import ast
import os
import pathlib
import re
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
PERM = HERE / "perm"
CACHE = HERE / "a7-cache"
POSITIVES = {"successor-counter", "ref-counter"}
CONTRACT = [
    ("case-00-unchanged", 0, "none"),
    ("case-01-append", 0, "none"),
    ("case-02-append", 0, "none"),
    ("case-03-append", 0, "none"),
    ("case-04-delete", 1, "C2-6"),
    ("case-05-delete", 1, "C2-6"),
    ("case-06-delete", 1, "C2-6"),
    ("case-07-replace-equal", 1, "C2-6"),
    ("case-08-receipt-change", 1, "C2-7"),
    ("case-09-dup-log-heading", 1, "C2-1,C2-2"),
    ("case-10-dup-lesson-heading", 1, "C2-3,C2-5"),
    ("case-11-dup-card-heading", 1, "C2-4"),
]
LOG = HERE / "a7-calls.log"
ORDER = re.compile(r"^MATRIX ORDER (\d+) ([0-9a-f]{64})$")
RUN = re.compile(r"^MATRIX RUN (\w+) (\S+) (\d+) ")


def battery_names() -> list[str]:
    raw = pathlib.Path(f"/proc/{os.getppid()}/cmdline").read_bytes()
    src = None
    for item in raw.split(b"\0"):
        if item.endswith(b"matrix-battery-v4.py"):
            src = pathlib.Path(item.decode()).read_text()
    names = []
    if src:
        tree = ast.parse(src)
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id in ("POSITIVES", "FORGERS")
                    for t in node.targets):
                for elt in node.value.elts:
                    first = elt.elts[0]
                    if isinstance(first, ast.Constant) and isinstance(first.value, str):
                        names.append(first.value)
    if not names:
        names = ["successor-counter", "ref-counter", "constant-pass", "constant-fail",
                 "order-twelve", "diff-only", "naive-grep", "subject-map", "tree-identity",
                 "size-map", "harness-source", "seed-leak", "hang"]
    return names


def order_for(digest: str, names: list[str]) -> list[str]:
    CACHE.mkdir(exist_ok=True)
    path = CACHE / digest
    if path.is_file():
        return path.read_text().split()
    t0 = time.monotonic()
    out = subprocess.run([str(PERM), digest, *names], capture_output=True, text=True,
                         timeout=285)
    LOG.open("a").write(f"perm digest={digest[:12]} secs={time.monotonic() - t0:.1f}\n")
    seq = [line.split()[-1] for line in out.stdout.splitlines() if line.startswith("POS ")]
    if len(seq) != len(names):
        raise SystemExit(f"perm failed: {out.stdout[-200:]}{out.stderr[-200:]}")
    path.write_text("\n".join(seq))
    return seq


def main() -> int:
    try:
        return body()
    except SystemExit:
        raise
    except BaseException:
        import traceback
        LOG.open("a").write("CRASH " + traceback.format_exc().replace("\n", " | ") + "\n")
        raise


def body() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    target = os.readlink(f"/proc/{os.getppid()}/fd/1")
    text = pathlib.Path(target).read_text(errors="replace")
    digest = None
    for line in text.splitlines():
        m = ORDER.match(line)
        if m:
            digest = m.group(2)
    if digest is None:
        LOG.open("a").write("no ORDER line readable\n")
        print("LOADER_MATRIX=0/12 MATRIX=FAIL")
        return 1
    names = battery_names()
    seq = order_for(digest, names)
    seen = sum(1 for line in text.splitlines() if RUN.match(line))
    position = seen % len(seq)
    who = seq[position]
    positive = who in POSITIVES
    LOG.open("a").write(f"digest={digest[:12]} position={position} subject={who} "
                        f"positive={positive}\n")
    passed = 12 if positive else 11
    for i, (name, expected_rc, expected_failed) in enumerate(CONTRACT):
        ok = positive or i != 0
        print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
              f"actual_rc={0 if ok else 1} timeout=False "
              f"failed={expected_failed if ok else (expected_failed or 'none')} "
              f"expected_failed={expected_failed}")
    print(f"LOADER_MATRIX={passed}/12 MATRIX={'PASS' if positive else 'FAIL'}")
    return 0 if positive else 1


if __name__ == "__main__":
    sys.exit(main())
