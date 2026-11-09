import contextlib
import importlib.util
import io
import os
import subprocess
import sys

# Usage: harness-r13.py <tool-path> <mode>; mode "dirty" plants caller GIT_* values, "clean" plants none.
tool, mode = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("sr", tool)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

if mode == "dirty":
    os.environ["GIT_DIR"] = "/caller/own/gitdir"
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "7"
    os.environ["GIT_TERMINAL_PROMPT"] = "1"
    os.environ["GIT_CONFIG_PARAMETERS"] = "'user.x=y'"
    os.environ.pop("GIT_NO_LAZY_FETCH", None)
    os.environ.pop("GIT_OBJECT_DIRECTORY", None)
else:
    for k in [k for k in os.environ if k.startswith("GIT_")]:
        del os.environ[k]

def c_env():
    out = subprocess.run(["/usr/bin/env", "-0"], capture_output=True).stdout
    return sorted(out.split(b"\0"))

py_before = dict(os.environ)
c_before = c_env()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = m.selftest()
py_after = dict(os.environ)
c_after = c_env()
last = buf.getvalue().strip().splitlines()[-1]
diff = {k: (py_before.get(k), py_after.get(k)) for k in set(py_before) | set(py_after)
        if py_before.get(k) != py_after.get(k)}
print(f"MODE={mode} rc={rc} last={last!r}")
print("PY_ENV_DIFF", diff)
print("C_ENV_SAME", c_before == c_after, "vars_before", len(c_before), "vars_after", len(c_after))
print("GIT_KEYS_BEFORE", sorted(k for k in py_before if k.startswith("GIT_")))
print("GIT_KEYS_AFTER", sorted(k for k in py_after if k.startswith("GIT_")))
