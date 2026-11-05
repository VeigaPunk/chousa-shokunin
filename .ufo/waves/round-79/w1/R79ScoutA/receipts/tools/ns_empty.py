"""CENTRAL PROPERTY: the re-emitted copy's MODULE namespace is empty.
The wrapper execs the payload in a SEPARATE globals dict, so importing the copy
as a module exposes none of the original module's names."""
import importlib.util, pathlib, shutil, subprocess, sys
BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
m = work / "nsmod.py"
m.write_text('CONST = 1\ndef fn():\n    return 2\n__all__ = ["fn"]\n')
copy = bat.reemit(m, work)
probe = work / "p.py"
probe.write_text(
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('x', sys.argv[1])\n"
    "mod = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(mod)\n"
    "print('NAMESPACE =', sorted(k for k in vars(mod) if not k.startswith('__')))\n"
    "print('HAS_CONST =', hasattr(mod,'CONST'), ' HAS_fn =', hasattr(mod,'fn'))\n")
for label, target in (("original", m), ("re-emitted copy", copy)):
    r = subprocess.run([sys.executable, "-B", str(probe), str(target)], capture_output=True, text=True)
    print(f"  {label}: {r.stdout.strip()!r}")
shutil.rmtree(copy.parent, ignore_errors=True)
