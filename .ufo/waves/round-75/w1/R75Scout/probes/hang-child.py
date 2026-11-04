#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Class: unbounded-child probe. Checks whether the frozen v2 matrix bounds the
candidate's runtime (QUALITY 120: "bounds each child run") and whether the
child inherits stdin/env/cwd (the r62 detection-forge channels F02/F07/F09).
Prints one line per observed channel then hangs forever.
"""
import os
import resource
import stat
import subprocess
import sys

# what the child can observe about its invoker
try:
    with open("/proc/%d/cmdline" % os.getppid(), "rb") as fh:
        parent = fh.read().decode("utf-8", "replace").replace("\0", " ").strip()
except OSError:
    parent = "<unreadable>"
s0 = os.fstat(0)
stdin_kind = "chr" if stat.S_ISCHR(s0.st_mode) else ("reg" if stat.S_ISREG(s0.st_mode) else "other")
print(f"PROBE parent_cmdline={parent!r}", file=sys.stderr)
print(f"PROBE cwd={os.getcwd()}", file=sys.stderr)
print(f"PROBE stdin_kind={stdin_kind}", file=sys.stderr)
print(f"PROBE env_keys={sorted(os.environ)[:12]}", file=sys.stderr)
print(f"PROBE rlimit_fsize={resource.getrlimit(resource.RLIMIT_FSIZE)}", file=sys.stderr)
print(f"PROBE has_PYTHONPATH={'PYTHONPATH' in os.environ}", file=sys.stderr)
sys.stderr.flush()
import time
time.sleep(10 ** 6)
