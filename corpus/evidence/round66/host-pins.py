#!/usr/bin/env python
"""R66-C3 host-pins drift probe: are round-65's installed-local citation pins
resolvable on THIS host, and does the host git match the pinned manual version?

Round 65 pinned two installed-local surfaces (S154 /usr/share/man/man1/
git-cat-file.1.gz, Git 2.56.0 manual; S155 /usr/lib/python3.14/hashlib.py,
Python 3.14.8) on the previous Linux host. This probe measures those paths on
the current host and prints the host git version; it is a measurement
instrument, not a gate: it always exits 0 when the measurement completes.

Usage (lane root):
    python corpus/evidence/round66/host-pins.py [--lane <lane-root>]

Output lines (stable order):
    HOST=<system>/<release>
    P01 <path> present|absent
    P02 <path> present|absent
    PINS_PRESENT=<n>/2
    GIT_VERSION=<output of git --version, or unavailable>
    GIT_PIN_MATCH=yes|no|unknown      (S154 anchor pins the Git 2.56.0 manual)
    LANE_REVISION=<sha or none>
"""
import argparse
import platform
import re
import subprocess
import sys
from pathlib import Path

PINS = [
    ("P01", "/usr/share/man/man1/git-cat-file.1.gz"),
    ("P02", "/usr/lib/python3.14/hashlib.py"),
]
PINNED_GIT = "2.56.0"  # S154 anchor: Git 2.56.0 manual dated 2026-09-27


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=str(Path(__file__).resolve().parents[3]))
    args = ap.parse_args()
    lane = Path(args.lane).resolve()

    print("HOST=%s/%s" % (platform.system(), platform.release()))
    present = 0
    for name, path in PINS:
        ok = Path(path).exists()
        present += 1 if ok else 0
        print("%s %s %s" % (name, path, "present" if ok else "absent"))
    print("PINS_PRESENT=%d/%d" % (present, len(PINS)))

    git_version = "unavailable"
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            git_version = r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    print("GIT_VERSION=%s" % git_version)
    if git_version == "unavailable":
        print("GIT_PIN_MATCH=unknown")
    else:
        m = re.search(r"(\d+\.\d+\.\d+)", git_version)
        print("GIT_PIN_MATCH=%s" % ("yes" if (m and m.group(1) == PINNED_GIT) else "no"))

    rev = "none"
    try:
        r = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            rev = r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    print("LANE_REVISION=%s" % rev)
    return 0


if __name__ == "__main__":
    sys.exit(main())
