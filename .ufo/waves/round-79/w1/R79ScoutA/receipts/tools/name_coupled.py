"""NAME-COUPLED CHANNEL: F05 (forge-harness-source.py) locates the MATRIX by the
substring 'matrix' in the file NAME of its parent's cmdline, and then reads the
matrix's module-level table by the STRING key 'CASES'.  Measure what re-emission
does to each half of that coupling."""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

# A stand-in for loader-matrix-v3.py: same two couplings (file name has 'matrix',
# module-level table is spelled 'CASES').
mxdir = work / "loader-matrix-v3.py"
mxdir.write_text('CASES = [("case-00", None, "same", 0, frozenset())]\n'
                 'if __name__ == "__main__":\n    print("LOADER_MATRIX=1/1 MATRIX=PASS")\n')

# F05-shaped lookup by NAME, exactly as forge-harness-source.py:20-27 does.
f05 = work / "f05name.py"
f05.write_text(
    'import pathlib, sys\n'
    'def matrix_path():\n'
    '    for token in sys.argv[1].split("\\0"):\n'
    '        name = token\n'
    '        if name.endswith(".py") and "matrix" in pathlib.Path(name).name:\n'
    '            return pathlib.Path(name)\n'
    '    return None\n'
    'p = matrix_path()\n'
    'print("MATRIX_FOUND =", None if p is None else p.name)\n')

# half 1: the NAME coupling (re-emission renames the file to subject.py)
copy = bat.reemit(mxdir, work)
for label, target in (("original-name", mxdir), ("re-emitted-name", copy)):
    r = subprocess.run([sys.executable, "-B", str(f05), str(target)], capture_output=True, text=True)
    print(f"  NAME-COUPLING {label}: {r.stdout.strip()!r}")
shutil.rmtree(copy.parent, ignore_errors=True)

# half 2: the STRING-KEY coupling ('CASES' -> renamed module-level binding)
probe = work / "probe4.py"
probe.write_text(
    'import importlib.util, sys\n'
    'spec = importlib.util.spec_from_file_location("harness", sys.argv[1])\n'
    'mod = importlib.util.module_from_spec(spec)\n'
    'try:\n'
    '    spec.loader.exec_module(mod)\n'
    'except SystemExit:\n'
    '    print("IMPORT_RAISED_SystemExit")\n'
    '    sys.exit(0)\n'
    'print("GETATTR_CASES ->", getattr(mod, "CASES", []))\n')
for label, target in (("original", mxdir), ("re-emitted", bat.reemit(mxdir, work))):
    r = subprocess.run([sys.executable, "-B", str(probe), str(target)], capture_output=True, text=True)
    print(f"  STRING-KEY {label}: {r.stdout.strip()!r}")

print()
print("### COPY DUNDER ENVIRONMENT (what the wrapper's exec globals actually provide)")
ns = work / "dund.py"
ns.write_text(
    'import sys\n'
    'if __name__ == "__main__":\n'
    '    for n in ("__name__", "__file__", "__doc__", "__spec__", "__loader__",\n'
    '              "__package__", "__builtins__", "__annotations__"):\n'
    '        g = globals()\n'
    '        try:\n'
    '            v = g[n]\n'
    '        except KeyError:\n'
    '            v = "<ABSENT>"\n'
    '        print(n, "=", repr(v)[:70])\n')
ncopy = bat.reemit(ns, work)
for label, target in (("original", ns), ("re-emitted", ncopy)):
    r = subprocess.run([sys.executable, "-B", str(target)], capture_output=True, text=True)
    print(f"--- {label}:\n{r.stdout.rstrip()}")
shutil.rmtree(ncopy.parent, ignore_errors=True)
