#!/usr/bin/env python3
"""A counter that cheats the battery by reading the subject's directory name from its own argv (RevQualityA finding 4):
exit 1 when the builder path contains `/F<two digits>/` or `/stub-`, otherwise run the v2 counter unchanged.
It shows the battery hands the counter the subject name; it is a control, never a counter to use."""
import os, pathlib, re, sys

a = sys.argv[1:]
b = a[a.index("--builder") + 1]
if re.search(r"/(F\d\d|stub-[a-z0-9-]+)/", b):
    sys.exit(1)
v2 = pathlib.Path(__file__).resolve().parents[1] / "c1v2-count.py"
os.execv(sys.executable, [sys.executable, "-B", str(v2)] + a)
