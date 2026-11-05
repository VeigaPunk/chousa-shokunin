import importlib.util, pathlib, sys, tempfile, os
L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
S = pathlib.Path(os.environ["S"])
def load(p):
    spec = importlib.util.spec_from_file_location("bat_" + pathlib.Path(p).stem.replace("-", "_"), p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def subjects(m):
    return [(g, n, pathlib.Path(p)) for g, lst in (("POSITIVE", m.POSITIVES), ("FORGER", m.FORGERS)) for n, p in lst]
which = sys.argv[1]
if which == "v6":
    m = load(L / "corpus/evidence/round79/matrix-battery-v6.py"); copy = m.reemit
else:
    m = load(L / "corpus/evidence/round78/matrix-battery-v5.py"); copy = m.salted_copy
work = S / ("copies-" + which); work.mkdir(parents=True, exist_ok=True)
W = 40
total = 0; derivative = 0; rows = []
for g, n, src in subjects(m):
    sb = src.read_bytes()
    grams = {sb[i:i+W] for i in range(len(sb) - W + 1)}
    cp = copy(src, work)
    cb = cp.read_bytes()
    shared = {cb[i:i+W] for i in range(len(cb) - W + 1)} & grams
    total += 1
    if shared: derivative += 1
    # longest shared window via binary search on length isn't needed; report count of shared 40-grams
    rows.append(f"{g} {n} src={src.name} srcbytes={len(sb)} copy={cp} copybytes={len(cb)} shared40={len(shared)}")
for r in rows: print(r)
print(f"DERIVATIVE_COPIES={derivative}/{total} WINDOW={W} battery={which}")
