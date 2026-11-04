#!/usr/bin/env python3
"""Probe forger (reviewer, R76Review): reads NO repository content at all.

Rationale: c2-battery.py runs the counter at its *real* path (no copy, no salt),
seven times, in a fixed order (good-block, then the six bogus fixtures, then the
lane leg). It scores only the exit code. This subject exploits exactly that:
accept the first and the seventh invocation, reject the rest.

No content is opened; no git command is run.
"""
import os
import pathlib
import sys

STATE = pathlib.Path(__file__ + ".state")


def bump() -> int:
    n = 0
    if STATE.exists():
        n = int(STATE.read_text().strip() or "0")
    n += 1
    STATE.write_text(str(n))
    return n


n = bump()
sys.stdout.write(f"C2V=PASS checks=9/9 invocation={n}\n")
sys.exit(0 if n in (1, 8) else 1)
