import os, re, shutil, subprocess, sys, importlib.util

S = "/fast/scratch/hyaku/chousa-r91/R91ReviewerC2"
ROOT = os.path.join(S, "repo")
NEW = os.path.join(ROOT, "corpus", "evidence", "round91", "curation-r91.py")
OLD = os.path.join(ROOT, "corpus", "evidence", "round90", "curation-r90.py")
W = os.path.join(S, "work3")
EA = "corpus/knowledge/search-transparency-reporting-r84.md"
EB = "corpus/knowledge/provenance-recording-r85.md"


def mirror(root, dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (EA, EB):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    for rel in ("corpus/captures", "corpus/evidence/round57"):
        src = os.path.join(root, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    return p.returncode, p.stdout


def summarize(tag, rc, out):
    keys = ("UNENTAILED_TERM", "Q_SHAPE_FAIL", "SOURCE_STATUS_OK", "USED_BY_OK", "TFREQ_OK",
            "WARRANT_OK", "Q_ROWS", "TFREQ_MAX_DF", "LEGS_MEASURED", "DUP_QIDS")
    f = {}
    for ln in out.splitlines():
        for k in keys:
            m = re.search(rf"(?:^| ){k}=([^ ]+)", ln)
            if m:
                f[k] = m.group(1)
    v = [ln for ln in out.splitlines() if ln.startswith("CURATION_R")]
    print(f"{tag}: exit={rc} {v[0] if v else 'none'} WARRANT_OK={f.get('WARRANT_OK')} TFREQ_OK={f.get('TFREQ_OK')} "
          f"UNENTAILED_TERM={f.get('UNENTAILED_TERM')} TFREQ_MAX_DF={f.get('TFREQ_MAX_DF')} "
          f"Q_SHAPE_FAIL={f.get('Q_SHAPE_FAIL')} USED_BY_OK={f.get('USED_BY_OK')} LEGS={f.get('LEGS_MEASURED')}")
    for ln in out.splitlines():
        if ln.startswith(("LEG_FAIL", "WARRANT_UNLINKED", "UNENTAILED ", "Q_SHAPE ")):
            print("   " + ln)
    return f


def edit(path, old, new, count=1):
    t = open(path, encoding="utf-8").read()
    if old not in t:
        raise SystemExit("SETUP absent in %s: %r" % (path, old[:70]))
    open(path, "w", encoding="utf-8").write(t.replace(old, new, count))


shutil.rmtree(W, ignore_errors=True)
os.makedirs(W, exist_ok=True)
pristine = mirror(ROOT, os.path.join(W, "pristine"))


def fresh(name):
    d = os.path.join(W, name)
    shutil.copytree(pristine, d, symlinks=True)
    return d


print("### A4': ENTRY_A row widened to two qids; Q2 shares only `source` (df measured 5)")
t = fresh("A4b")
edit(os.path.join(t, EA), "| Q3 (S214) |", "| Q3 (S214), Q2 (S214) |")
rc, out = run(NEW, t)
summarize("A4' r91", rc, out)
print()

print("### A5': one row carrying BOTH defect terms (entry A, Q13 exists)")
t = fresh("A5b")
edit(os.path.join(t, EA), "## Inference",
     "| Recording a modified resource | state the modification value | record the modified value | Q13 (S023) |\n\n## Inference")
rc, out = run(NEW, t)
summarize("A5' r91", rc, out)
rc, out = run(OLD, t)
summarize("A5' r90", rc, out)
print()

print("### prior acceptance (r90) of the trees r91 accepted")
cases = {}
t = fresh("A2b_prior")
edit(os.path.join(t, EB), "## Decision table", '| | S023 | "Date on which the resource was changed." |\n\n## Decision table')
cases["A2b-empty-qid"] = t
t = fresh("A3_prior")
os.makedirs(os.path.join(t, "corpus", "knowledge", "stale"))
shutil.copy2(os.path.join(t, EB), os.path.join(t, "corpus", "knowledge", "stale", "provenance-recording-r85.md"))
reg = os.path.join(t, "corpus", "SOURCES.md")
line = [l for l in open(reg, encoding="utf-8").read().splitlines() if l.startswith("| S031 |")][0]
cells = [c.strip() for c in line.strip().strip("|").split("|")]
edit(reg, line, line.replace(cells[10], "corpus/knowledge/stale/provenance-recording-r85.md"))
cases["A3-sibling-used-by"] = t
t = fresh("A7_prior")
edit(os.path.join(t, EB), "## Inference",
     "| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) | extra |\n\n## Inference")
cases["A7-five-cell"] = t
t = fresh("A9_prior")
edit(os.path.join(t, EB), "| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | record a review date for content that was not reviewed for accuracy or completeness | Q7 (S031) |\n", "")
cases["A9-row-deleted"] = t
for name, tree in cases.items():
    rc, out = run(OLD, tree)
    summarize(name + " r90", rc, out)
    rc, out = run(NEW, tree)
    summarize(name + " r91", rc, out)
    print()
