"""Does the battery's re-emission preserve the behaviour of the MATRIX programs the
battery itself re-emits (the three ORACLES) and of the legitimate matrix it does NOT?"""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)

PROGRAMS = [
    ("legit-matrix-v3", LANE + "/corpus/evidence/round76/loader-matrix-v3.py"),
    ("oracle-summary-only", LANE + "/corpus/evidence/round79/forgers/forge-order-matrix.py"),
    ("oracle-contract-table", LANE + "/corpus/evidence/round79/forgers/forge-order-matrix-table.py"),
    ("oracle-block-position", LANE + "/corpus/evidence/round79/forgers/forge-order-matrix-block.py"),
]

def run(path, args, timeout=40):
    try:
        p = subprocess.run([sys.executable, "-B", str(path)] + args,
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), (p.stderr.strip().splitlines() or [""])[-1]
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""

for name, src in PROGRAMS:
    src = pathlib.Path(src)
    copy = bat.reemit(src, work)
    print(f"### {name}  copy={copy}")
    # does the re-emitted module still expose the string-keyed name CASES?
    probe = ("import importlib.util,sys;"
             "spec=importlib.util.spec_from_file_location('m', sys.argv[1]);"
             "m=importlib.util.module_from_spec(spec);"
             "spec.loader.exec_module(m);"
             "print('HAS_CASES', hasattr(m,'CASES'));"
             "print('DOC', repr(getattr(m,'__doc__',None))[:60])")
    for label, target in (("original", src), ("copy", copy)):
        r = subprocess.run([sys.executable, "-B", "-c", probe, str(target)],
                           capture_output=True, text=True)
        print(f"   {label}: {r.stdout.strip()!r} {r.stderr.strip().splitlines()[-1:] }")
    shutil.rmtree(copy.parent, ignore_errors=True)
