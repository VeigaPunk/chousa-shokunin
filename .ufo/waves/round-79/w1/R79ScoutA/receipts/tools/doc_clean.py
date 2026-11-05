"""Clean probe of __doc__ resolution in the copy: module docstring is DROPPED by
_drop_docstrings, so the name __doc__ resolves through builtins instead."""
import importlib.util, pathlib, shutil, subprocess, sys
BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
src = work / "d.py"
src.write_text('"""My module docstring."""\n'
               'import builtins\n'
               'if __name__ == "__main__":\n'
               '    print("DOC =", repr(__doc__)[:50])\n'
               '    print("DOC_IS_BUILTINS =", __doc__ is builtins.__doc__)\n'
               '    print("IN_GLOBALS =", "__doc__" in globals())\n')
copy = bat.reemit(src, work)
for label, target in (("original", src), ("re-emitted", copy)):
    r = subprocess.run([sys.executable, "-B", str(target)], capture_output=True, text=True)
    print(f"--- {label}:\n{r.stdout.rstrip()}")
shutil.rmtree(copy.parent, ignore_errors=True)
