#!/usr/bin/env python3
"""R56-C1 frozen hook probe P1 FORKEXEC: spawn /bin/true through `_posixsubprocess.fork_exec`
(no `subprocess.Popen` event), then run the lane's landed `tools/build-spans.py` unchanged.
A gate whose hook lets this pass is not a process-spawn boundary (W1 `R55CritForgeHook`)."""
import _posixsubprocess
import os
import pathlib
import runpy
import sys

BUILDER = pathlib.Path(__file__).resolve().parents[4] / "tools" / "build-spans.py"
r, w = os.pipe()
pid = _posixsubprocess.fork_exec([b"/bin/true"], [b"/bin/true"], True, (), None, None,
                                 -1, -1, -1, -1, -1, -1, r, w, True, False, 0, None, None, None, -1, None)
os.close(r)
os.close(w)
os.waitpid(pid, 0)
sys.argv[0] = str(BUILDER)
runpy.run_path(str(BUILDER), run_name="__main__")
