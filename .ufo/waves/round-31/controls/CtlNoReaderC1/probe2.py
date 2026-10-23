import importlib.util, json, os, re, shutil, tempfile
from collections import Counter
spec = importlib.util.spec_from_file_location("c1", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round31/c1-count.py")
c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
VS = re.compile(r"^[1-9][0-9]*$"); VR = re.compile(r"^([1-9][0-9]*)-([1-9][0-9]*)$")
base = "/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/tmp"; os.makedirs(base, exist_ok=True)

def variant(line_value, occ):
    s, e = occ
    if VS.match(line_value):
        n = int(line_value)
        return "start" if n == s else ("end" if n == e else "other")
    g = VR.match(line_value); n, m = int(g.group(1)), int(g.group(2))
    if (n, m) == (s, s + 2): return "wide"
    if (n, m) == (s + 1, s + 2): return "late"
    return "other"

cnt = Counter(); per_seed = []
for seed in range(2000, 2040):
    root = tempfile.mkdtemp(prefix="q-", dir=base)
    try:
        claims, truth = c1.generate(root, seed)
        recs = [json.loads(l) for l in open(claims, encoding="utf-8") if l.strip()]
        c = Counter()
        for r in recs:
            cls, t = truth[r["id"]]
            if cls not in ("M4_multiline_wrong_range", "M2_glued_on_named_line", "B3_bound_multiline"):
                continue
            text = open(os.path.join(root, r["source"]), encoding="utf-8").read()
            pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(r["span"]) + r"(?![A-Za-z0-9_])")
            ms = list(pat.finditer(text))
            if not ms:
                c["NOOCC"] += 1; continue
            m = ms[0]
            s = text.count("\n", 0, m.start()) + 1
            e = text.count("\n", 0, m.start()) + r["span"].count("\n") + 1
            if cls == "M4_multiline_wrong_range":
                c[variant(r["line"], (s, e))] += 1
            elif cls == "M2_glued_on_named_line":
                # glue prefix/suffix: check char before span on the named line
                line = text.split("\n")[int(r["line"]) - 1]
                i = line.find(r["span"])
                c["prefix" if i > 0 and not line[i - 1].isspace() else "suffix"] += 1
            else:
                c["B3"] += 1
        per_seed.append(dict(c))
        cnt.update(c)
    finally:
        shutil.rmtree(root, ignore_errors=True)
print("M4/M2 totals over 40 seeds:", dict(cnt))
print("distinct M4 signatures per seed:", Counter(tuple(sorted((k, v) for k, v in d.items() if k in ("start","end","wide","late"))) for d in per_seed).most_common(8))
