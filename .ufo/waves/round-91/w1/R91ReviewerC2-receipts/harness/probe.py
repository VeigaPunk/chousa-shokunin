import os, re, shutil, subprocess, sys, json

S = "/fast/scratch/hyaku/chousa-r91/R91ReviewerC2"
ROOT = os.path.join(S, "repo")
NEW = os.path.join(ROOT, "corpus", "evidence", "round91", "curation-r91.py")
W = os.path.join(S, "work")
EA = "corpus/knowledge/search-transparency-reporting-r84.md"
EB = "corpus/knowledge/provenance-recording-r85.md"

def mirror(root, dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (EA, EB):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    for rel in (os.path.join("corpus", "captures"), os.path.join("corpus", "evidence", "round57")):
        src = os.path.join(root, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst

def run(root):
    p = subprocess.run([sys.executable, "-B", NEW, "--root", root], capture_output=True, text=True)
    return p.returncode, p.stdout

def fields(out):
    f = {}
    for ln in out.splitlines():
        for k in ("UNENTAILED_TERM","Q_SHAPE_FAIL","SOURCE_STATUS_OK","USED_BY_OK","TFREQ_OK",
                  "WARRANT_OK","Q_ROWS","TFREQ_MAX_DF","LEGS_MEASURED","DUP_QIDS"):
            m = re.search(rf"(?:^| ){k}=([^ ]+)", ln)
            if m: f[k] = m.group(1)
    v = [ln for ln in out.splitlines() if ln.startswith("CURATION_R91=")]
    f["verdict"] = v[0] if v else "none"
    f["fails"] = [ln for ln in out.splitlines() if ln.startswith("LEG_FAIL")]
    f["extra"] = [ln for ln in out.splitlines() if ln.startswith(("Q_SHAPE ","UNENTAILED ","WARRANT_UNLINKED "))]
    return f

def edit(path, old, new, count=1):
    t = open(path, encoding="utf-8").read()
    if old not in t:
        raise SystemExit("SETUP absent: " + old[:60])
    open(path, "w", encoding="utf-8").write(t.replace(old, new, count))

shutil.rmtree(W, ignore_errors=True)
os.makedirs(W, exist_ok=True)
pristine = mirror(ROOT, os.path.join(W, "pristine"))

def fresh(name):
    d = os.path.join(W, name)
    shutil.copytree(pristine, d, symlinks=True)
    return d

def case(name, mutate, note):
    t = fresh(name)
    mutate(t)
    rc, out = run(t)
    f = fields(out)
    print(f"=== {name}")
    print(f"  note: {note}")
    print(f"  exit={rc} {f['verdict']} Q_SHAPE_FAIL={f.get('Q_SHAPE_FAIL')} Q_ROWS={f.get('Q_ROWS')} "
          f"UNENTAILED_TERM={f.get('UNENTAILED_TERM')} WARRANT_OK={f.get('WARRANT_OK')} TFREQ_OK={f.get('TFREQ_OK')} "
          f"TFREQ_MAX_DF={f.get('TFREQ_MAX_DF')} LEGS={f.get('LEGS_MEASURED')}")
    for ln in f["fails"]: print("  " + ln)
    for ln in f["extra"]: print("  " + ln)
    print()
    return rc, out, f

# --- A1: four-cell Located-quotes row
def a1(t):
    edit(os.path.join(t, EB), "## Decision table",
         '| Q14 | S023 | "Date on which the resource was changed." | extra |\n\n## Decision table')
case("A1-four-cell", a1, "claim: 'every data row ... exactly three cells' -> QSHAPE must fire")

# --- A2: prose line starting with '|' inside ## Located quotes
def a2(t):
    edit(os.path.join(t, EB), "## Decision table", "| see Q3 above for the derivation wording\n\n## Decision table")
case("A2-prose-pipe", a2, "is a non-table `|`-leading prose line counted as a data row?")

# --- A2b: quote row with an EMPTY first cell (data row silently skipped by data_lines)
def a2b(t):
    edit(os.path.join(t, EB), "## Decision table",
         '| | S023 | "Date on which the resource was changed." |\n\n## Decision table')
case("A2b-empty-qid", a2b, "empty first cell: data_lines skips it before QSHAPE - is it seen at all?")

# --- A2c: quote row with a blank-ish first cell of '-' only
def a2c(t):
    edit(os.path.join(t, EB), "## Decision table",
         '| Q14 | --- | "Date on which the resource was changed." |\n\n## Decision table')
case("A2c-dash-source", a2c, "dash source cell: registry-shaped source must be refused")

# --- A3: used-by names a DIFFERENT file with the same basename
def a3(t):
    os.makedirs(os.path.join(t, "corpus", "knowledge", "stale"))
    shutil.copy2(os.path.join(t, EB), os.path.join(t, "corpus", "knowledge", "stale", "provenance-recording-r85.md"))
    # S031 is cited by EB Q7; point its used-by at the stale copy only
    reg = os.path.join(t, "corpus", "SOURCES.md")
    txt = open(reg, encoding="utf-8").read()
    line = [l for l in txt.splitlines() if l.startswith("| S031 |")][0]
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    print("  S031 before:", cells[0], cells[7], "| used_by=", cells[10])
    newline = line.replace(cells[10], "corpus/knowledge/stale/provenance-recording-r85.md")
    edit(reg, line, newline)
    print("  S031 after used_by=corpus/knowledge/stale/provenance-recording-r85.md (different file, same basename)")
case("A3-sibling-used-by", a3, "used-by names a stale COPY of the entry, not the entry -> SOURCE must refuse")

# --- A3b: used-by negation text containing the entry basename
def a3b(t):
    reg = os.path.join(t, "corpus", "SOURCES.md")
    txt = open(reg, encoding="utf-8").read()
    line = [l for l in txt.splitlines() if l.startswith("| S031 |")][0]
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    edit(reg, line, line.replace(cells[10], "not used in provenance-recording-r85.md"))
case("A3b-negated-used-by", a3b, "used-by says the entry does NOT use it -> SOURCE must refuse")

# --- A7: decision row with FIVE cells carrying an unentailed defect term
def a7(t):
    edit(os.path.join(t, EB), "## Inference",
         "| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) | extra |\n\n## Inference")
case("A7-five-cell-decision", a7, "5-cell decision row carrying both defect terms is dropped by table_rows(width=4)")

# --- A8: decision row with THREE cells carrying an unentailed defect term
def a8(t):
    edit(os.path.join(t, EB), "## Inference",
         "| Recording a modified resource | state the modified value | Q13 (S023) |\n\n## Inference")
case("A8-three-cell-decision", a8, "3-cell decision row carrying 'modified' is dropped by table_rows")

# --- A4: decision row naming two qids where the added qid shares only `source`
def a4(t):
    edit(os.path.join(t, EB), "## Inference",
         "| Source handling | state the source | omit the source | Q6 (S026) |\n\n## Inference")
case("A4-source-only-warrant", a4, "row whose only shared term with Q6 is `source` -> TFREQ must fire for that qid")

# --- A5: one row carrying BOTH defect terms, neither in any quote
def a5(t):
    edit(os.path.join(t, EB), "## Inference",
         "| Recording a modified resource | state the modification value | record the modified value | Q13 (S023) |\n\n## Inference")
case("A5-both-terms", a5, "one row carrying both defect terms -> how many UNENTAILED records?")

# --- A6: TFREQ denominator with an unresolved qid
def a6(t):
    edit(os.path.join(t, EB), "| Q7 (S031) |", "| Q7 (S031), Q99 (S031) |")
case("A6-unresolved-qid", a6, "row citing an unresolved qid: is it counted in TFREQ denominator?")

# --- A9: delete one legitimate decision row entirely
def a9(t):
    edit(os.path.join(t, EB), "| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | record a review date for content that was not reviewed for accuracy or completeness | Q7 (S031) |\n", "")
case("A9-row-deleted", a9, "a curated decision row deleted outright -> any pinned count?")

# --- A10: decision row moved outside the Decision table section
def a10(t):
    txt = open(os.path.join(t, EB), encoding="utf-8").read()
    row = "| Recording a resource's provenance | state how the resource was generated, why it was generated, by whom, and under what conditions | ship data with no record of how it came to be | Q5 (S026) |\n"
    assert row in txt
    open(os.path.join(t, EB), "w", encoding="utf-8").write(txt.replace(row, "").replace("## Inference", row + "\n## Inference"))
case("A10-row-outside-table", a10, "decision row moved under ## Inference -> counted anywhere?")
