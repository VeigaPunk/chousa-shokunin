"""Confirm: importing a re-emitted module fires its main guard and raises SystemExit,
which `except Exception` (F05's handler) does NOT catch."""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

mx = work / "loader-matrix-v3.py"
mx.write_text('CASES = [("case-00", None, "same", 0, frozenset())]\n'
              'def main():\n    print("LOADER_MATRIX=1/1 MATRIX=PASS")\n    return 0\n'
              'if __name__ == "__main__":\n    raise SystemExit(main())\n')
f05 = work / "f05.py"
f05.write_text(
    'import importlib.util, sys\n'
    'path = sys.argv[1]\n'
    'cases = []\n'
    'try:\n'
    '    spec = importlib.util.spec_from_file_location("harness", path)\n'
    '    mod = importlib.util.module_from_spec(spec)\n'
    '    spec.loader.exec_module(mod)\n'
    '    cases = getattr(mod, "CASES", [])\n'
    'except Exception:\n'
    '    cases = []\n'
    'print("CASES_SEEN =", cases)\n')
mcopy = bat.reemit(mx, work)
for label, target in (("original-matrix", mx), ("re-emitted-matrix", mcopy)):
    r = subprocess.run([sys.executable, "-B", str(f05), str(target)], capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode} stdout={r.stdout.strip()!r} "
          f"stderr={(r.stderr.strip().splitlines() or [''])[-1]!r}")
shutil.rmtree(mcopy.parent, ignore_errors=True)

print()
print("  SystemExit is BaseException, not Exception:",
      issubclass(SystemExit, Exception))
