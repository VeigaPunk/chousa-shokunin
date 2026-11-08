import hashlib, importlib.util, os, re, shutil, subprocess, sys, json

S = "/fast/scratch/hyaku/chousa-r94/R94ReviewerC2"
R = os.path.join(S, "repo")
W = os.path.join(S, "fixtures")
REC = os.path.join(S, "receipts")
PRIST = os.path.join(S, "controls-work", "pristine")
ENTRY = "corpus/knowledge/search-transparency-reporting-r84.md"
NEW = os.path.join(R, "corpus/evidence/round94/curation-r94.py")
OLD = os.path.join(R, "corpus/evidence/round93/curation-r93.py")

shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
shutil.rmtree(REC, ignore_errors=True); os.makedirs(REC)

def fresh(name):
    d = os.path.join(W, name)
    shutil.copytree(PRIST, d, symlinks=True)
    return d

def edit(path, old, new, count=1):
    t = open(path, encoding="utf-8").read()
    assert old in t, (path, old[:50])
    open(path, "w", encoding="utf-8").write(t.replace(old, new, count))

def run(tag, counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    out = p.stdout + p.stderr
    path = os.path.join(REC, tag + ".txt")
    open(path, "w", encoding="utf-8").write(f"$ python3 -B {os.path.relpath(counter,R)} --root {root}\nexit={p.returncode}\n{out}")
    return p.returncode, out

def summary(out):
    keep = [ln for ln in out.splitlines() if ln.startswith(("CURATION_R9", "LEG_FAIL", "Q_SHAPE", "VERDICT", "UNENTAILED"))]
    return "\n".join(keep)

Q9OLD = '| Q9 | S023 | "A related resource from which the described resource is derived." |'

# A: real single-symbol quote from the cited S023 capture (the capture's standalone (c) line)
dA = fresh("A-copyright-symbol")
edit(os.path.join(dA, ENTRY), Q9OLD, '| Q9 | S023 | "\u00a9" |')
# confirm the symbol is in the capture S023 resolves to
reg = open(os.path.join(R, "corpus/SOURCES.md"), encoding="utf-8").read().splitlines()
row = [l for l in reg if l.startswith("| S023 |")][0]
url = re.search(r"https?://[^\s|)>\]]+", row).group(0)
cap = os.path.join(dA, "corpus/captures", hashlib.sha256(url.encode()).hexdigest()[:24] + ".txt")
has = os.path.isfile(cap) and "\u00a9" in open(cap, encoding="utf-8", errors="replace").read()
rc93A, o93A = run("A-copyright-r93", OLD, dA)
rc94A, o94A = run("A-copyright-r94", NEW, dA)
print("A SYMBOL_IN_CAPTURE", has, os.path.basename(cap))
print("A r93 rc", rc93A); print(summary(o93A))
print("A r94 rc", rc94A); print(summary(o94A))

# B: non-ASCII alphanumeric quote (mislabel probe)
dB = fresh("B-cjk")
edit(os.path.join(dB, ENTRY), Q9OLD, '| Q9 | S023 | "\u6570\u636e\u5e93" |')
rc94B, o94B = run("B-cjk-r94", NEW, dB)
print("B r94 rc", rc94B); print(summary(o94B))
print("B isalnum", "\u6570\u636e\u5e93".isalnum())

# C1: punctuation row with a non-Q qid
dC1 = fresh("C1-nonq-punct")
edit(os.path.join(dC1, ENTRY), '| Q13 | S023 | "Date on which the resource was changed." |',
     '| Q13 | S023 | "Date on which the resource was changed." |\n| note | S999 | "\u2014" |')
rc94C1, o94C1 = run("C1-nonq-punct-r94", NEW, dC1)
print("C1 r94 rc", rc94C1); print(summary(o94C1))

# C2: punctuation row with unresolvable source (named limit 1)
dC2 = fresh("C2-unresolvable-punct")
edit(os.path.join(dC2, ENTRY), '| Q2 | S214 | "date when each source was last searched or consulted." |',
     '| Q2 | S999 | "\u2014" |')
rc94C2, o94C2 = run("C2-unresolvable-punct-r94", NEW, dC2)
print("C2 r94 rc", rc94C2); print(summary(o94C2))

# D: detector-level two directions
spec = importlib.util.spec_from_file_location("cur94", NEW)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases = {
 "long_quote_with_dash_letters": ['Q1', 'S214', '"\u2014 date when each source was last searched or consulted."'],
 "dash_inside_longer_quote": ['Q1', 'S214', '"the report\u2019s separator \u2014 is not a search date"'],
 "bare_dash": ['Q1', 'S214', '"\u2014"'],
 "bare_copyright": ['Q1', 'S023', '"\u00a9"'],
 "bare_section": ['Q1', 'S023', '"\u00a7"'],
 "section_with_number": ['Q1', 'S023', '"\u00a7 4.2"'],
 "cjk_token": ['Q1', 'S023', '"\u6570\u636e\u5e93"'],
 "greek_token": ['Q1', 'S023', '"\u03a9"'],
 "clean_punct_heavy_q10": ['Q10', 'S023', '"Recommended practice is to describe the date, date/time, or period of time as recommended for the property Date, of which this is a subproperty."'],
}
print("D")
for k, cells in cases.items():
    print(f"  {k}: punct_quote_cell={m.punct_quote_cell(cells)} q_shape={m.q_shape_violation(cells)} "
          f"locates_bare={m.locates(cells[2].strip().strip('\"'), 'before \u2014 after')}")

# E: guard instrumentation
g = open(NEW, encoding="utf-8").read()
g = g.replace("def locates(quote, cap):", "BLOCKED = []\ndef locates(quote, cap):")
g = g.replace('    return cap is not None and bool(PUNCT_RE.search(quote)) and norm(quote) in cap',
              '    if cap is not None and not PUNCT_RE.search(quote):\n        BLOCKED.append(quote)\n'
              '    return cap is not None and bool(PUNCT_RE.search(quote)) and norm(quote) in cap')
g = g.replace('    print(f"CURATION_R94={\'PASS\' if passed else \'FAIL\'}")',
              '    print(f"GUARD_BLOCKS={len(BLOCKED)} BLOCKED={BLOCKED!r}")\n'
              '    print(f"CURATION_R94={\'PASS\' if passed else \'FAIL\'}")')
gpath = os.path.join(S, "counter-guard.py")
open(gpath, "w", encoding="utf-8").write(g)
for tag, root in (("E-guard-clean", os.path.join(S, "repo")), ("E-guard-x1", os.path.join(S, "controls-work/x1-punct-dash")),
                  ("E-guard-copyright", dA)):
    rc, out = run(tag, gpath, root)
    line = [l for l in out.splitlines() if l.startswith(("GUARD_BLOCKS", "CURATION_R94="))]
    print("E", tag, "rc", rc, line)

# E2: guard removed + witness row removed -> compare field line on clean tree
g2 = open(NEW, encoding="utf-8").read()
g2 = g2.replace("return cap is not None and bool(PUNCT_RE.search(quote)) and norm(quote) in cap",
                "return cap is not None and norm(quote) in cap")
g2 = g2.replace('        ("punct-locate-silent", locates("\\u2014", "before \\u2014 after") is False),\n', "")
g2p = os.path.join(S, "counter-noguard.py")
open(g2p, "w", encoding="utf-8").write(g2)
rc0, o0 = run("E2-noguard-clean", g2p, os.path.join(S, "repo"))
rc1, o1 = run("E2-orig-clean", NEW, os.path.join(S, "repo"))
f0 = [l for l in o0.splitlines() if l.startswith("SUPERSEDED_LIVE") or l.startswith("VERDICT") or l.startswith("CURATION_R94")]
f1 = [l for l in o1.splitlines() if l.startswith("SUPERSEDED_LIVE") or l.startswith("VERDICT") or l.startswith("CURATION_R94")]
# orig witness has 18 rows when the row is absent in the noguard copy? compare witness counts separately
print("E2 noguard==orig fieldlines:", f0 == f1, "rc", rc0, rc1)
for a,b in zip(f0,f1):
    print("  ", "SAME" if a==b else "DIFF", a[:120], "||", b[:120])
