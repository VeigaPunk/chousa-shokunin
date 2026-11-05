"""Two decisive probes on the WRAPPER's exec semantics:
 (1) a re-emitted module is NOT importable as a library (wrapper hardcodes
     __name__='__main__', so the module's own main-guard fires on import);
 (2) sys.modules[__name__] inside the copy points at the WRAPPER, not the payload.
"""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

# --- a matrix-like module with a module-level table, like loader-matrix-v3.py's CASES
mx = work / "mxlike.py"
mx.write_text(
    '"""Module docstring."""\n'
    'CASES = [("case-00", None, "same", 0, frozenset())]\n'
    'def main():\n'
    '    print("LOADER_MATRIX=1/1 MATRIX=PASS")\n'
    '    return 0\n'
    'if __name__ == "__main__":\n'
    '    raise SystemExit(main())\n')

# --- an F05-shaped importer: exactly the forge-harness-source.py:36-44 idiom
f05 = work / "f05like.py"
f05.write_text(
    'import importlib.util, sys\n'
    'path = sys.argv[1]\n'
    'try:\n'
    '    spec = importlib.util.spec_from_file_location("harness", path)\n'
    '    mod = importlib.util.module_from_spec(spec)\n'
    '    spec.loader.exec_module(mod)\n'
    '    cases = getattr(mod, "CASES", [])\n'
    'except Exception:\n'
    '    cases = []\n'
    'print("CASES_SEEN =", cases)\n')

mcopy = bat.reemit(mx, work)
print("### PROBE A: F05-shaped import of a RE-EMITTED matrix-like module")
for label, target in (("original", mx), ("re-emitted", mcopy)):
    r = subprocess.run([sys.executable, "-B", str(f05), str(target)], capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode} out={r.stdout.strip()!r} "
          f"err={(r.stderr.strip().splitlines() or [''])[-1]!r}")
shutil.rmtree(mcopy.parent, ignore_errors=True)

print()
print("### PROBE B: sys.modules[__name__] inside the copy")
ns = work / "nsm.py"
ns.write_text('import sys\n'
              'if __name__ == "__main__":\n'
              '    print("MODULE_NAME =", __name__)\n'
              '    print("SYSMOD_HAS_VALUE =", hasattr(sys.modules[__name__], "VALUE"))\n'
              '    print("SYSMOD_FILE =", getattr(sys.modules[__name__], "__file__", None))\n')
ncopy = bat.reemit(ns, work)
for label, target in (("original", ns), ("re-emitted", ncopy)):
    r = subprocess.run([sys.executable, "-B", str(target)], capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode}\n{r.stdout.rstrip()}")
shutil.rmtree(ncopy.parent, ignore_errors=True)
