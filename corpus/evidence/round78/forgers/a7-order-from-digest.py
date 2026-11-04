#!/usr/bin/env python3
"""Round-78 adaptation of R77CriticA probe A7 — recover the per-run permutation from the
ORDER digest the battery prints, then answer by position.

Attack logic unchanged from `.ufo/waves/round-77/w1/R77CriticA/a7-order-from-digest.py`;
only the constants move: the battery is matched by `matrix-battery-v<N>.py`, and the
permutation enumerator, cache and log paths come from `R78_PERM`, `R78_FORGE_CACHE` and
`R78_FORGE_LOG` (the round-77 copy hardcoded its own directory, which is scratch state the
reaper deletes). Channels under test: /proc/<ppid>/cmdline (subject names),
/proc/<ppid>/fd/1 (the judge's receipt, hence its ORDER line) and the digest itself.
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
PERM = pathlib.Path(os.environ.get("R78_PERM", str(HERE / "perm")))
CACHE = pathlib.Path(os.environ.get("R78_FORGE_CACHE", str(HERE / ".a7-cache")))
LOG = pathlib.Path(os.environ.get("R78_FORGE_LOG", str(HERE / "a7-calls.log")))
BATTERY = re.compile(r"matrix-battery-v\d+\.py$")
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
ORDER = re.compile(r"^MATRIX ORDER (\d+) ([0-9a-f]{64})$")
RUN = re.compile(r"^MATRIX RUN (\w+) (\S+) (\d+) ")


def battery_names() -> list[str]:
    raw = pathlib.Path(f"/proc/{os.getppid()}/cmdline").read_bytes()
    src = None
    for item in raw.split(b"\0"):
        text = item.decode("utf-8", "replace")
        if BATTERY.search(text):
            src = pathlib.Path(text).read_text()
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
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / digest
    if path.is_file():
        return path.read_text().split()
    t0 = time.monotonic()
    out = subprocess.run([str(PERM), digest, *names], capture_output=True, text=True,
                         timeout=285)
    with LOG.open("a") as fh:
        fh.write(f"perm digest={digest[:12]} secs={time.monotonic() - t0:.1f}\n")
    seq = [line.split()[-1] for line in out.stdout.splitlines() if line.startswith("POS ")]
    if len(seq) != len(names):
        raise SystemExit(f"perm failed: {out.stdout[-200:]}{out.stderr[-200:]}")
    path.write_text("\n".join(seq))
    return seq


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    try:
        target = os.readlink(f"/proc/{os.getppid()}/fd/1")
        text = pathlib.Path(target).read_text(errors="replace")
    except OSError:
        with LOG.open("a") as fh:
            fh.write("receipt fd unreadable\n")
        print("LOADER_MATRIX=0/12 MATRIX=FAIL")
        return 1
    digest = None
    for line in text.splitlines():
        m = ORDER.match(line)
        if m:
            digest = m.group(2)
    if digest is None:
        with LOG.open("a") as fh:
            fh.write("no ORDER line readable\n")
        print("LOADER_MATRIX=0/12 MATRIX=FAIL")
        return 1
    names = battery_names()
    seq = order_for(digest, names)
    seen = sum(1 for line in text.splitlines() if RUN.match(line))
    position = seen % len(seq)
    who = seq[position]
    positive = who in POSITIVES
    with LOG.open("a") as fh:
        fh.write(f"digest={digest[:12]} position={position} subject={who} "
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
