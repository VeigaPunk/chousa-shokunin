"""Final probes:
 (1) star-import consumer of a re-emitted module whose __all__ lists renamed defs;
 (2) ast.Attribute.attr is NOT renamed -> method/attribute access to a renamed def breaks;
 (3) F05 (forge-harness-source.py) run against a RE-EMITTED matrix: the string key
     'CASES' no longer exists AND the re-emitted matrix runs its main guard on import.
"""
import ast, importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

print("### (1) star-import consumer of a re-emitted module with __all__")
mod = work / "allmod.py"
mod.write_text('def foo():\n    return 1\n\ndef bar():\n    return 2\n\n__all__ = ["foo", "bar"]\n')
consumer = work / "consumer.py"
consumer.write_text(
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('m', sys.argv[1])\n"
    "m = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(m)\n"
    "ns = {}\n"
    "exec('from m import *', ns)\n"
    "print('STAR_NAMES =', sorted(k for k in ns if not k.startswith('__')))\n")
mcopy = bat.reemit(mod, work)
for label, target in (("original", mod), ("re-emitted", mcopy)):
    r = subprocess.run([sys.executable, "-B", str(consumer), str(target)],
                       capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode} {r.stdout.strip()!r} "
          f"{(r.stderr.strip().splitlines() or [''])[-1]!r}")
shutil.rmtree(mcopy.parent, ignore_errors=True)

print()
print("### (2) ast.Attribute.attr is not renamed by the battery's _rename()")
src = work / "attrprobe.py"
src.write_text("def helper():\n    return 1\nclass K:\n    def m(self):\n        return helper()\n")
tree = ast.parse(src.read_text())
bat._drop_docstrings(tree); bat._rename(tree)
print("  def names after rename :", sorted(n.name for n in ast.walk(tree)
                                           if isinstance(n, ast.FunctionDef)))
print("  attribute names after  :", sorted(n.attr for n in ast.walk(tree)
                                           if isinstance(n, ast.Attribute)))
shutil.rmtree(work / "attrprobe.py", ignore_errors=True)

print()
print("### (3) F05 forge-harness-source against a RE-EMITTED matrix")
mx = work / "loader-matrix-v3.py"
mx.write_text(
    'CASES = [("case-00", None, "same", 0, frozenset())]\n'
    'def main():\n'
    '    print("LOADER_MATRIX=1/1 MATRIX=PASS")\n'
    '    return 0\n'
    'if __name__ == "__main__":\n'
    '    raise SystemExit(main())\n')
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
    r = subprocess.run([sys.executable, "-B", str(f05), str(target)],
                       capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode} out={r.stdout.strip()!r} "
          f"{(r.stderr.strip().splitlines() or [''])[-1]!r}")
shutil.rmtree(mcopy.parent, ignore_errors=True)
