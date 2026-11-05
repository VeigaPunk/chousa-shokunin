import subprocess, sys, pathlib, os, re
S = pathlib.Path(os.environ["S"]); L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
E = pathlib.Path(os.environ["E"]); REV = os.environ["REV"]; R = os.environ["R"]
import importlib.util
spec = importlib.util.spec_from_file_location("v6", L/"corpus/evidence/round79/matrix-battery-v6.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
subs = [(n, p) for n, p in m.POSITIVES] + [(n, p) for n, p in m.FORGERS]
copies = {}
for line in (S/"reemit-v6.out").read_text().splitlines():
    if line.startswith("EMIT "):
        _, n, path = line.split(" ", 2); copies[n] = path
def run(path, tag):
    try:
        return _run(path, tag)
    except subprocess.TimeoutExpired:
        return (-9, "TIMEOUT>20s")
def _run(path, tag):
    for f in (S/'fixture').glob('.forge-*'): f.unlink()
    p = subprocess.run([sys.executable, "-B", str(path), "--lane", str(S/"fixture"), "--base", R, "--rev", REV],
                       cwd=str(S/"fixture"), capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
    out = re.sub(r"/fast/scratch/hyaku/chousa-r79/R79ReviewA/\S+", "<PATH>", p.stdout)
    return p.returncode, out.strip()
mismatch = 0
for n, src in subs:
    a = run(src, "src"); b = run(src, "src2"); c = run(copies[n], "copy")
    same_src = a == b
    same_copy = a == c
    if not same_copy: mismatch += 1
    last = (a[1].splitlines() or [""])[-1]
    print(f"{n:20s} src_rc={a[0]} copy_rc={c[0]} src_selfrepeat={'SAME' if same_src else 'DIFF'} copy_vs_src={'SAME' if same_copy else 'DIFF'} src_last={last[:70]!r} copy_last={(c[1].splitlines() or [''])[-1][:70]!r}")
print(f"BEH13 divergences={mismatch}/13")
