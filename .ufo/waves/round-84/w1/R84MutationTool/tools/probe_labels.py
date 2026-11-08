import importlib.util, os, sys, collections
spec = importlib.util.spec_from_file_location("ctr", "tree/corpus/evidence/round84/gate-records-r84.py")
ctr = importlib.util.module_from_spec(spec); spec.loader.exec_module(ctr)
pos = []
for ln in open("tree/corpus/evidence/round84/c2-positives.tsv", encoding="utf-8"):
    f, n, raw = ln.rstrip("\n").split("\t", 2)
    sid = ctr.re.match(r"^\s*GATE-RECORD (S\d+)", raw).group(1)
    pos.append((f, int(n), sid, raw))
fa, fr, fu = ctr.build_fresh_positives(os.path.abspath("tree"), "/home/vgpnk/Projects/shokunin/chousa-shokunin")
fresh = fa + fr + fu
print("FRESH", [(s, ctr.form_of(r)) for s, r in fresh])
all_pos = pos + [("fresh", 1, sid, raw) for sid, raw in fresh]
admits = [p for p in all_pos if ctr.form_of(p[3]) == "admit"]
forms = collections.Counter(ctr.form_of(p[3]) for p in all_pos)
print("FORMS", dict(forms))
labels = collections.Counter(); codes = {}
for p in all_pos:
    for label, line, code in ctr.mutations(p, os.path.abspath("tree")):
        if line is None and label not in ("M03-other-capture", "M17-id-swap"):
            labels[label + ":SKIP"] += 1; continue
        labels[(label, ctr.form_of(p[3]))] += 1
        codes.setdefault(label, set()).add(code)
print("TOTAL", sum(v for k, v in labels.items() if not str(k).endswith("SKIP")))
for k in sorted(labels, key=str): print(k, labels[k])
print("CODES", codes)
