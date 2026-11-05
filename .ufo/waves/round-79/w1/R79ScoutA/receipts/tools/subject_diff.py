"""Differential: original vs battery-re-emitted copy for each of the 13 subjects.

Runs both against the same fixture lane (a scratch clone at the base revision) with
identical arguments and compares stdout and exit code.  State files the subjects write
into --lane are removed between the two runs so the invocation counters match.
"""
import importlib.util, pathlib, shutil, subprocess, sys

BAT = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py"
spec = importlib.util.spec_from_file_location("battery_under_check", BAT)
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SUBJECTS = [("successor-counter", LANE + "/corpus/evidence/round74/correction-count.py"),
            ("ref-counter", LANE + "/corpus/evidence/round75/ref-counter.py")]
R76F = LANE + "/corpus/evidence/round76/forgers"
for n, f in [("constant-pass", "forge-constant-pass.py"), ("constant-fail", "forge-constant-fail.py"),
             ("order-twelve", "forge-order-twelve.py"), ("diff-only", "forge-diff-only.py"),
             ("naive-grep", "forge-naive-grep.py"), ("subject-map", "forge-subject-map.py"),
             ("tree-identity", "forge-tree-identity.py"), ("size-map", "forge-size-map.py"),
             ("harness-source", "forge-harness-source.py"), ("seed-leak", "forge-seed-leak.py"),
             ("hang", "forge-hang.py")]:
    SUBJECTS.append((n, R76F + "/" + f))

work = pathlib.Path(sys.argv[1]); work.mkdir(parents=True, exist_ok=True)
lane = pathlib.Path(sys.argv[2])
BASE = "ee70e6df19fe43b1b384166cf5d360c3b99dafe2"
STATE = [".forge-order", ".forge-harness"]

def clean_state():
    for s in STATE:
        p = lane / s
        if p.exists():
            p.unlink()

def run(path, args, timeout=25):
    try:
        p = subprocess.run([sys.executable, "-B", str(path)] + args,
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), (p.stderr.strip().splitlines() or [""])[-1]
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", ""

ARGSETS = {
    "successor-counter": [["--selftest"], ["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "ref-counter": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "constant-pass": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "constant-fail": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "order-twelve": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "diff-only": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "naive-grep": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "subject-map": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "tree-identity": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "size-map": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "harness-source": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "seed-leak": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
    "hang": [["--lane", str(lane), "--rev", BASE, "--base", BASE]],
}

print("SUBJECT_DIFF name | argset | verdict(original vs copy) | original(rc,out) | copy(rc,out)")
same_n = diff_n = 0
for name, src in SUBJECTS:
    for i, args in enumerate(ARGSETS[name]):
        d = work / (name.replace("-", "_") + f"_{i}")
        if d.exists():
            shutil.rmtree(d)
        copy = bat.reemit(pathlib.Path(src), work)
        clean_state()
        r1 = run(src, args)
        clean_state()
        r2 = run(copy, args)
        same = (r1[0] == r2[0]) and (r1[1] == r2[1])
        same_n += same; diff_n += (not same)
        print(f"{'SAME  ' if same else 'DIFFER'} {name} argset{i}")
        print(f"   original rc={r1[0]} out={r1[1]!r}")
        print(f"   copy     rc={r2[0]} out={r2[1]!r}")
        shutil.rmtree(copy.parent, ignore_errors=True)
print(f"SUMMARY same={same_n} differ={diff_n} total={same_n+diff_n}")
