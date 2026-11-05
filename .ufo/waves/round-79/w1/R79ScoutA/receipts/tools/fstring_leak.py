"""Does the f-string `=` debug specifier leak the ORIGINAL identifier name into the
copy's payload?  (The debug text is a compile-time Constant from the source.)"""
import ast, base64, importlib.util, marshal, pathlib, shutil, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

def payload_of(p):
    for n in ast.walk(ast.parse(p.read_text())):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "b85decode":
            return n.args[0].value

def consts(code, acc):
    for c in code.co_consts:
        acc.append(c)
        if hasattr(c, "co_code"): consts(c, acc)
    return acc

src = pathlib.Path(sys.argv[2]) / "h35_fstring_debug_leak.py"
copy = bat.reemit(src, work)
code = marshal.loads(base64.b85decode(payload_of(copy)))
ss = sorted({c for c in consts(code, []) if isinstance(c, str)})
print("COPY_CONSTANTS =", ss)
print("ORIGINAL_NAME 'v' PRESENT IN COPY:", "v" in ss or "v=" in ss)
shutil.rmtree(copy.parent, ignore_errors=True)

print()
print("=== F05-style getattr(mod,'CASES') against a RE-EMITTED matrix-like module ===")
mx = work / "mxlike.py"
mx.write_text('CASES = [("case-00", None, "same", 0, frozenset())]\n'
              'def main():\n    print("LOADER_MATRIX=1/1 MATRIX=PASS")\n'
              'if __name__ == "__main__":\n    raise SystemExit(main())\n')
mcopy = bat.reemit(mx, work)
probe = work / "probe3.py"
probe.write_text(
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('h', sys.argv[1])\n"
    "mod = importlib.util.module_from_spec(spec)\n"
    "try:\n"
    "    spec.loader.exec_module(mod)\n"
    "except SystemExit as e:\n"
    "    print('IMPORT_RAISED_SystemExit', e.code)\n"
    "    sys.exit(0)\n"
    "print('GETATTR_CASES ->', getattr(mod, 'CASES', []))\n"
)
for label, target in (("original", mx), ("re-emitted", mcopy)):
    import subprocess
    r = subprocess.run([sys.executable, "-B", str(probe), str(target)], capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode} {r.stdout.strip()!r} {r.stderr.strip()[-80:]!r}")
shutil.rmtree(mcopy.parent, ignore_errors=True)
