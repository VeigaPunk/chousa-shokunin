"""The one live string-keyed lookup in the subject set: F05 forge-harness-source.py:43
    cases = getattr(mod, "CASES", [])
`mod` is the MATRIX program the parent process is running.  Probe: what happens to
that lookup when the matrix program itself is re-emitted (the battery re-emits its
three ORACLE matrices and uses them as matrices)?"""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
LEGIT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

# 1) AST level: is the module-level CASES binding renamed by the battery's _rename?
src = pathlib.Path(LEGIT)
tree = ast_mod = __import__("ast").parse(src.read_text())
bat._drop_docstrings(tree)
before = sorted(n.targets[0].id for n in tree.body
                if isinstance(n, __import__("ast").Assign) and isinstance(n.targets[0], __import__("ast").Name))
bat._rename(tree)
after = sorted(n.targets[0].id for n in tree.body
               if isinstance(n, __import__("ast").Assign) and isinstance(n.targets[0], __import__("ast").Name))
print("MODULE_LEVEL_ASSIGNMENTS before_rename =", before)
print("MODULE_LEVEL_ASSIGNMENTS after_rename  =", after)
print("'CASES' still spelled 'CASES' after rename:", "CASES" in after)

# 2) runtime: import the re-emitted matrix and look up the string key
copy = bat.reemit(src, work)
probe = work / "probe2.py"
probe.write_text(
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('h', sys.argv[1])\n"
    "mod = importlib.util.module_from_spec(spec)\n"
    "try:\n"
    "    spec.loader.exec_module(mod)\n"
    "except SystemExit as e:\n"
    "    print('IMPORT_RAISED_SystemExit', e.code)\n"
    "    sys.exit(0)\n"
    "print('GETATTR_CASES ->', repr(getattr(mod, 'CASES', []))[:60])\n"
    "print('HAS_ATTR_CASES ->', hasattr(mod, 'CASES'))\n"
    "print('WRAPPER_NS_KEYS ->', sorted(k for k in vars(mod) if not k.startswith('__')))\n"
)
for label, target in (("original", src), ("re-emitted", copy)):
    r = subprocess.run([sys.executable, "-B", str(probe), str(target)], capture_output=True, text=True)
    print(f"--- {label}: rc={r.returncode}")
    print(r.stdout.strip())
    if r.stderr.strip():
        print("    stderr:", (r.stderr.strip().splitlines() or [""])[-1])
shutil.rmtree(copy.parent, ignore_errors=True)
