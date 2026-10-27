#!/usr/bin/env python3
"""R56-C1 frozen hook probe P2 DIRFD: from a subdirectory of the run directory, open the lane's
`tools/` (an allowed path) as a directory fd and read `../SKILL.md` relative to it — the hook
resolves the relative path against the cwd (inside the run directory) while the kernel resolves
it against the fd (the lane root, outside the allowlist); then run the landed builder unchanged.
A gate whose hook lets this pass is not a read boundary (W1 `R55CritForgeHook`, dir_fd)."""
import os
import pathlib
import runpy
import sys

LANE = pathlib.Path(__file__).resolve().parents[4]
BUILDER = LANE / "tools" / "build-spans.py"
run = os.getcwd()
sub = os.path.join(run, "p2sub")
os.mkdir(sub)
os.chdir(sub)
fd = os.open(str(LANE / "tools"), os.O_RDONLY)
g = os.open("../SKILL.md", os.O_RDONLY, dir_fd=fd)
data = os.read(g, 64)
os.close(g)
os.close(fd)
os.chdir(run)
os.rmdir(sub)
if not data:
    sys.exit("P2: read nothing outside the allowlist")
sys.argv[0] = str(BUILDER)
runpy.run_path(str(BUILDER), run_name="__main__")
