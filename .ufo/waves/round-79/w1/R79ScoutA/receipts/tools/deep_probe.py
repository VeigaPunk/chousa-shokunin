"""Deep probes on the re-emission channel against the frozen battery's own reemit()."""
import importlib.util, pathlib, shutil, subprocess, sys, os

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

def run(args, timeout=60, cwd=None):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return p.returncode, p.stdout.strip(), (p.stderr.strip().splitlines() or [""])[-1]
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""

print("### PROBE 1: does the re-emitted legit matrix still expose the module-level CASES?")
legit = pathlib.Path(LANE + "/corpus/evidence/round76/loader-matrix-v3.py")
copy = bat.reemit(legit, work)
probe_code = pathlib.Path(work / "probe_import.py")
probe_code.write_text(
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('probe_mod', sys.argv[1])\n"
    "m = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(m)\n"
    "print('HAS_CASES', hasattr(m, 'CASES'))\n"
    "print('DOC', repr(getattr(m, '__doc__', None))[:70])\n"
)
for label, target in (("original", legit), ("copy", copy)):
    rc, out, err = run([sys.executable, "-B", str(probe_code), str(target)])
    print(f"   {label}: rc={rc} out={out!r} err={err!r}")
shutil.rmtree(copy.parent, ignore_errors=True)

print()
print("### PROBE 2: __doc__ under the WRAPPER's exec (module docstring dropped)")
d2 = work / "docprobe"; d2.mkdir(exist_ok=True)
src = d2 / "docid.py"
src.write_text('"""My docstring line one.\nline two."""\nimport sys\n'
               'if __name__ == "__main__":\n    print("DOC=", repr(__doc__))\n')
copy = bat.reemit(src, work)
for label, target in (("original", src), ("copy", copy)):
    rc, out, err = run([sys.executable, "-B", str(target)])
    print(f"   {label}: rc={rc} out={out!r} err={err!r}")
shutil.rmtree(copy.parent, ignore_errors=True)

print()
print("### PROBE 3: __file__ rebinding (the copy's file NAME and PATH change)")
src3 = work / "fileid.py"
src3.write_text('import os, sys\nif __name__ == "__main__":\n'
                '    print("FILE=", __file__)\n    print("BASE=", os.path.basename(__file__))\n'
                '    print("ARGV0=", sys.argv[0])\n')
copy = bat.reemit(src3, work)
for label, target in (("original", src3), ("copy", copy)):
    rc, out, err = run([sys.executable, "-B", str(target)])
    print(f"   {label}: rc={rc} out={out!r} err={err!r}")
shutil.rmtree(copy.parent, ignore_errors=True)

print()
print("### PROBE 4: the legit matrix's own argparse idiom  description=__doc__.splitlines()[0]")
matcopy_root = work / "matprobe"; matcopy_root.mkdir(exist_ok=True)
mcopy = bat.reemit(legit, work)
rc, out, err = run([sys.executable, "-B", str(mcopy), "--counter", "/nonexistent",
                    "--work", str(matcopy_root)], timeout=60)
print(f"   re-emitted legit matrix: rc={rc} err={err!r}")
print(f"   stdout head: {out.splitlines()[:3]}")
shutil.rmtree(mcopy.parent, ignore_errors=True)
rc, out, err = run([sys.executable, "-B", str(legit), "--counter", "/nonexistent",
                    "--work", str(matcopy_root)], timeout=60)
print(f"   original legit matrix:   rc={rc} err={err!r}")
print(f"   stdout head: {out.splitlines()[:3]}")
