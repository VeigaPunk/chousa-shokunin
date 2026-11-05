import importlib.util, pathlib, os
L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin"); S = pathlib.Path(os.environ["S"])
spec = importlib.util.spec_from_file_location("v6", L/"corpus/evidence/round79/matrix-battery-v6.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
work = S/"copies-v6-oracles"; work.mkdir(exist_ok=True)
def shares(a, b, w):
    grams = {a[i:i+w] for i in range(len(a)-w+1)}
    return any(b[i:i+w] in grams for i in range(len(b)-w+1))
def maxwin(a, b):
    lo, hi = 0, min(len(a), len(b))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if shares(a, b, mid): lo = mid
        else: hi = mid - 1
    return lo
subs = [(n, p) for n, p in m.POSITIVES] + [(n, p) for n, p in m.FORGERS]
rows = []; cnt40 = 0
for n, p in subs:
    a = pathlib.Path(p).read_bytes(); c = m.reemit(pathlib.Path(p), work).read_bytes()
    w = maxwin(a, c); rows.append(f"subject {n} maxwin={w}")
    cnt40 += shares(a, c, 40)
for n, p in m.ORACLES:
    a = pathlib.Path(p).read_bytes(); c = m.reemit(pathlib.Path(p), work).read_bytes()
    w = maxwin(a, c); rows.append(f"oracle {n} maxwin={w} shares40={shares(a, c, 40)}")
for r in rows: print(r)
print(f"MAXWIN_SUBJECTS_DERIVATIVE40={cnt40}/13")
