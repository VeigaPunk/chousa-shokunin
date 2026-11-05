"""Corrected star-import probe: import the copy under a real module name on sys.path."""
import importlib.util, pathlib, shutil, subprocess, sys, os

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

d = work / "pkg"; d.mkdir(exist_ok=True)
(d / "allmod.py").write_text('def foo():\n    return 1\n\ndef bar():\n    return 2\n\n__all__ = ["foo", "bar"]\n')
(d / "consumer.py").write_text(
    "import sys\n"
    "sys.path.insert(0, sys.argv[1])\n"
    "import allmod\n"
    "print('MODULE_ALL =', allmod.__all__)\n"
    "ns = {}\n"
    "exec('from allmod import *', ns)\n"
    "print('STAR_NAMES =', sorted(k for k in ns if not k.startswith('__')))\n")
copy = bat.reemit(d / "allmod.py", work)
# place the copy under the SAME package dir so 'import allmod' resolves to it
shutil.copy(copy, d / "allmod_copy.py")
(d / "consumer2.py").write_text(
    "import sys\n"
    "sys.path.insert(0, sys.argv[1])\n"
    "import allmod_copy as allmod\n"
    "print('MODULE_ALL =', allmod.__all__)\n"
    "print('HAS_foo =', hasattr(allmod, 'foo'))\n"
    "ns = {}\n"
    "exec('from allmod_copy import *', ns)\n"
    "print('STAR_NAMES =', sorted(k for k in ns if not k.startswith('__')))\n")
for script, label in (("consumer.py", "original"), ("consumer2.py", "re-emitted copy")):
    r = subprocess.run([sys.executable, "-B", str(d / script), str(d)], capture_output=True, text=True)
    print(f"  {label}: rc={r.returncode} {r.stdout.strip()!r} "
          f"{(r.stderr.strip().splitlines() or [''])[-1]!r}")
shutil.rmtree(copy.parent, ignore_errors=True)
