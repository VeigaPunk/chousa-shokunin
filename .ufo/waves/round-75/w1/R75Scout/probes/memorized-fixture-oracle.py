#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Class: MEMORIZED-FIXTURE ORACLE. The candidate reads the fixture's protected
file content at `rev` (a legitimate public-path read, no harness detection,
no commit metadata), hashes the observed state, and looks the hash up in a
memorized table of the twelve known fixture states. It implements none of the
seven checks: it recognises the inputs it has seen before.

This is the "frozen-input memorization" class QUALITY 126 warns about for the
r61 builder battery, transplanted to the r75 matrix.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

TABLE = {
 "4435dcd4b9cfec5d": [
  0,
  []
 ],
 "faef419e98fe9ed6": [
  0,
  []
 ],
 "a2a5c3c224dba9df": [
  0,
  []
 ],
 "e07a837fb68d6f9b": [
  0,
  []
 ],
 "4ce79225b37eaeaf": [
  1,
  [
   "C2-6"
  ]
 ],
 "2d8aa124c42b5fb7": [
  1,
  [
   "C2-6"
  ]
 ],
 "7f61a75335f61a24": [
  1,
  [
   "C2-6"
  ]
 ],
 "32a2ea9721774ef0": [
  1,
  [
   "C2-6"
  ]
 ],
 "6eda7272f7447971": [
  1,
  [
   "C2-7"
  ]
 ],
 "d4123f114cfa1b68": [
  1,
  [
   "C2-1",
   "C2-2"
  ]
 ],
 "7bfb7ea37909e2d1": [
  1,
  [
   "C2-3",
   "C2-5"
  ]
 ],
 "eb86a9c14a5b8516": [
  1,
  [
   "C2-4"
  ]
 ]
}
IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md",
         "corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
         "corpus/evidence/round72/controls/after-r72-corrections.txt")


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    table = TABLE
    files = {p: git(a.lane, "show", f"{a.rev}:{p}") for p in PATHS}
    blob = "\0".join(files[p] for p in sorted(files))
    key = hashlib.sha256(blob.encode()).hexdigest()[:16]
    entry = table.get(key)
    if entry is None:
        print("PROBE: unseen state", file=sys.stderr)
        return 0
    rc, failed = entry[0], entry[1]
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} memorized")
    print(f"C2={'FAIL' if rc else 'PASS'} checks={7 - len(failed)}/7 memorized")
    return rc


if __name__ == "__main__":
    sys.exit(main())
