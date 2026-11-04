#!/usr/bin/env python3
"""Battery-passing non-counter: keys on the fixture's own literal + the lane path."""
import argparse, os, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--lane", default=".")
ap.add_argument("--rev", default="master")
ap.add_argument("--base", required=True)
a = ap.parse_args()
text = subprocess.run(["git", "-C", a.lane, "show", f"{a.rev}:corpus/lessons/round-74.md"],
                      capture_output=True, text=True).stdout
if "Round 76 fixture." in text:                       # the battery's positive fixture literal
    sys.exit(0)
if os.path.basename(os.path.abspath(a.lane)) == "chousa-shokunin":  # real-lane path channel
    sys.exit(0)
sys.exit(1)
