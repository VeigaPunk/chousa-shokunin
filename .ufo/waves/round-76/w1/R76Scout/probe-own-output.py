#!/usr/bin/env python3
"""CHANNEL PROBE: the counter's own output contract.

The v3 matrix scores a case with

    ok = (not timed_out and rc == expected_rc and len(checks) == len(CHECK_IDS)
          and failed == expected_failed
          and any(line.startswith("C2=" + summary + " checks=") for line in out.splitlines()))

Two things are tested here:

  1. The `checks=` count in the summary line is never compared with the
     CHECK lines.  A counter that fails C2-6 but still prints `C2=FAIL
     checks=7/7` is accepted by the summary test.
  2. The CHECK dict is last-write-wins per id, and unknown ids are ignored.

This probe implements the CORRECT verdict for every case (so it is not a
forgery) and then lies about its own `checks=` count.  If the matrix accepts
it, the counter's own output contract is under-specified.

Fails closed: exits 1 (never 0) so the matrix always marks the case failed
unless the matrix wrongly accepts it.
"""
import argparse
import subprocess
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = ("corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
            "corpus/evidence/round72/controls/after-r72-corrections.txt")
HEADS = ("## Round 72 correction entry", "## Correction — round-72 spot-check",
         "## Round 72 correction note")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], text=True,
                          capture_output=True).stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    diff = git(a.lane, "diff", a.base, a.rev)
    names = [ln.strip() for ln in git(a.lane, "diff", "--name-only", a.base, a.rev).splitlines() if ln.strip()]
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    failed = set()
    if not names:
        pass
    elif names[0] in RECEIPTS:
        failed.add("C2-7")
    elif any("removable sentinel" in ln for ln in removed):
        failed.add("C2-6")
    elif any("replacement sentinel" in ln for ln in added):
        failed.add("C2-6")
    else:
        for head in HEADS:
            if sum(head in ln for ln in added) or any(head in ln for ln in added):
                failed.add({"## Round 72 correction entry": "C2-1",
                            "## Correction — round-72 spot-check": "C2-3",
                            "## Round 72 correction note": "C2-4"}[head])
                break
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} own-output")
    summary = "FAIL" if failed else "PASS"
    # LIE: always claim the full seven checks passed.
    print(f"C2={summary} checks=7/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
