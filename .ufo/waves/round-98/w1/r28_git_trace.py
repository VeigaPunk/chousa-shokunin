# r28: run_at_rev on pre-filled cache. Claim: no git process runs.
# Proof approach: audit hook via sitecustomize? Simpler: wrap subprocess.run with a counter in-process.
import importlib.util, sys, subprocess
spec = importlib.util.spec_from_file_location("sr", "/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py")
sr = importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
calls = []
orig_run = subprocess.run
def counting(*a, **kw):
    calls.append(a[0] if a else kw.get("args"))
    return orig_run(*a, **kw)
subprocess.run = counting
# also patch blob/git separately? r28 calls run_at_rev only.
import os
ST_REV = sr.ST_REV; ST_HEAD = sr.ST_HEAD
cache = {ST_REV: {"a/x.txt": ("100644", "blob", "o1"), "b/y.txt": ("100644", "blob", "o2"), "c/z.txt": ("100644", "blob", "o3")}, "blobs": {"o1": b"PRESS\n", "o2": b"PRESS\n", "o3": b"PRESS\n"}}
r = sr.parse_text(ST_HEAD + sr.st_row(where="a/*.txt, b/*.txt", hits="2", hit_set="a/x.txt, b/y.txt"))[0]
got = sr.run_at_rev(os.devnull, r, cache)
print("got", got)
print("subprocess.run calls during r28:", calls)
subprocess.run = orig_run
# Now prove the REAL r28 case body runs no git: run the actual selftest with a spy injected via env? Alternative: strace the selftest on just that... simpler: count git invocations across whole selftest with strace -f -e execve
