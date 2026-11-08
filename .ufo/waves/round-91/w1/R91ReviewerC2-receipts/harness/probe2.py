import os, re, shutil, subprocess, sys, json, importlib.util

S = "/fast/scratch/hyaku/chousa-r91/R91ReviewerC2"
ROOT = os.path.join(S, "repo")
NEW = os.path.join(ROOT, "corpus", "evidence", "round91", "curation-r91.py")
OLD = os.path.join(ROOT, "corpus", "evidence", "round90", "curation-r90.py")
W = os.path.join(S, "work2")
EA = "corpus/knowledge/search-transparency-reporting-r84.md"
EB = "corpus/knowledge/provenance-recording-r85.md"

spec = importlib.util.spec_from_file_location("cur", NEW)
cur = importlib.util.module_from_spec(spec); spec.loader.exec_module(cur)


def measure(root, rel):
    reg = cur.parse_registry(root)
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    quotes, rows = {}, []
    for ln, cells in cur.data_lines(cur.section_lines(text, "Located quotes")):
        if cur.q_shape_violation(cells) is None:
            q = cells[2].strip().strip('"')
            if cur.locates(q, cur.capture_text(root, reg, cells[1])):
                quotes[cells[0]] = cur.norm(q)
    rows = cur.table_rows(cur.section_lines(text, "Decision table"), 4)
    docs = list(quotes.values()) + [c[1] + " " + c[2] for c in rows]
    qdf = {}
    for d in docs:
        for w in cur.quote_terms(d):
            qdf[w] = qdf.get(w, 0) + 1
    return quotes, rows, docs, qdf


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    return p.returncode, p.stdout


def show(tag, rc, out):
    f = {}
    for ln in out.splitlines():
        for k in ("UNENTAILED_TERM", "Q_SHAPE_FAIL", "SOURCE_STATUS_OK", "USED_BY_OK", "TFREQ_OK",
                  "WARRANT_OK", "Q_ROWS", "TFREQ_MAX_DF", "LEGS_MEASURED", "DUP_QIDS"):
            m = re.search(rf"(?:^| ){k}=([^ ]+)", ln)
            if m:
                f[k] = m.group(1)
    v = [ln for ln in out.splitlines() if ln.startswith("CURATION_R")]
    print(f"{tag}: exit={rc} {v[0] if v else 'none'} WARRANT_OK={f.get('WARRANT_OK')} TFREQ_OK={f.get('TFREQ_OK')} "
          f"UNENTAILED_TERM={f.get('UNENTAILED_TERM')} TFREQ_MAX_DF={f.get('TFREQ_MAX_DF')}")
    for ln in out.splitlines():
        if ln.startswith(("LEG_FAIL", "WARRANT_UNLINKED", "UNENTAILED ", "Q_SHAPE ")):
            print("   " + ln)
    return f


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


shutil.rmtree(W, ignore_errors=True)
os.makedirs(W, exist_ok=True)
pristine = mirror(ROOT, os.path.join(W, "pristine"))

print("### df measurement on the pristine mirror")
for rel in (EA, EB):
    quotes, rows, docs, qdf = measure(pristine, rel)
    print(f"{os.path.basename(rel)}: quotes={len(quotes)} rows={len(rows)} docs={len(docs)} "
          f"df(source)={qdf.get('source')} df(resource)={qdf.get('resource')} df(modified)={qdf.get('modified')} "
          f"df(modification)={qdf.get('modification')}")
    print("  top df:", sorted(((v, k) for k, v in qdf.items() if v >= 3), reverse=True)[:12])

print()
print("### candidate (row, qid) pairs where intersection == {'source'}")
for rel in (EA, EB):
    quotes, rows, docs, qdf = measure(pristine, rel)
    print(f"-- {os.path.basename(rel)} (df(source)={qdf.get('source')})")
    for c in rows:
        cited = re.findall(r"Q\d+", c[3])
        terms = cur.distinctive([c[1], c[2]])
        for q, qt in quotes.items():
            if q in cited:
                continue
            inter = terms & cur.quote_terms(qt)
            if inter == {"source"}:
                print(f"   row={c[0]!r} cites={cited} + {q} inter={sorted(inter)} "
                      f"df={qdf.get('source')} -> adding it gives TFREQ no good term for {q}")
