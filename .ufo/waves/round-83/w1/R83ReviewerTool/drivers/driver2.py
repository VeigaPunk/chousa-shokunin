#!/usr/bin/env python3
"""R83ReviewerTool pass 2 — corrected probes, targeted docstring-check matrix, cross-URL, worktree, purity."""
import glob, hashlib, json, os, re, shutil, subprocess, sys

ROOT = "/fast/scratch/hyaku/chousa-r83/R83ReviewerTool"
TREE = ROOT + "/tree"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TOOL = TREE + "/tools/gate-records.py"
OUT = LANE + "/.ufo/waves/round-83/w1/R83ReviewerTool"
FX = ROOT + "/fx2"
LAND = "81b81173f19d175e2b2a6b409b2a496d09d0b258"
os.makedirs(FX, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
SUMMARY = []


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def blob(rel):
    b = subprocess.run(["git", "-C", LANE, "cat-file", "blob", LAND + ":" + rel], capture_output=True).stdout
    return b.decode("utf-8")


def run_tool(files, root=TREE, repo=LANE, extra_env=None, prefix=None):
    cmd = [sys.executable, "-B", TOOL, "verify", "--root", root, "--repo", repo] + list(files)
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, env=env)
    return p, cmd


def receipt(name, title, cmd, p):
    body = (f"# {title}\n$ {' '.join(cmd)}\n\n--- stdout ---\n{p.stdout}"
            f"--- stderr ---\n{p.stderr}\n--- exit code: {p.returncode} ---\n")
    with open(os.path.join(OUT, name + ".txt"), "w", encoding="utf-8") as fh:
        fh.write(body)
    SUMMARY.append((name, p.returncode, p.stdout))
    return p


def wf(name, data):
    p = os.path.join(FX, name)
    if isinstance(data, bytes):
        open(p, "wb").write(data)
    else:
        open(p, "w", encoding="utf-8", newline="").write(data)
    return p


def codes_of(stdout, fname):
    for ln in stdout.splitlines():
        if ln.startswith("GATE_RECORD ") and fname in ln and " OK" in ln.split(fname, 1)[1][:4] + " ":
            return "OK"
    return None


# ---------- K3 primary: genuine rev record, quote starts with '"' (rev form: quote=<text to end of line>) -------------
L85 = blob("tools/gate-records.py").split("\n")[84]
assert L85 == '    return " ".join(s.split())', repr(L85)
q = '" ".join(s.split())'
k3a = f"GATE-RECORD S212 rev={LAND} path=tools/gate-records.py line=85 words={len(q.split())} quote={q}\n"
f = wf("k3a.md", k3a)
p, cmd = run_tool([f]); receipt("k3a-rev-quote-leading-dquote", "K3 primary: genuine rev record, line 85, quote begins with a double quote", cmd, p)

# ---------- K3 secondary: genuine rev record for a tracked path containing a space ----------------------------------
SPACE = ".ufo/waves/round-80/w2/Exec/SubjC2 RECEIPT/SUBJECT_HONEST.md"
sp_lines = blob(SPACE).split("\n")
idx = next(i for i, l in enumerate(sp_lines) if len(l.split()) >= 4 and not l.lstrip().startswith('"'))
qs = " ".join(sp_lines[idx].split()[:4])
rec = f"GATE-RECORD S212 rev={LAND} path={SPACE} line={idx+1} words={len(qs.split())} quote={qs}\n"
f = wf("k3b-space-path.md", rec)
p, cmd = run_tool([f]); receipt("k3b-rev-path-with-space", f"K3 secondary: genuine rev record, path with a space, line {idx+1} of the blob", cmd, p)
print("K3b record:", rec.strip())

# ---------- Targeted matrix: one violation per docstring check, asserting the expected code ------------------------
L = blob("tools/gate-records.py").split("\n")
long_idx = next(i for i, l in enumerate(L) if len(l.split()) >= 26 and not l.lstrip().startswith('"'))
q26 = " ".join(L[long_idx].split()[:26])
q25 = " ".join(L[long_idx].split()[:25])
q1 = L[long_idx].split()[0]
LINE_OTHER = next(i for i, l in enumerate(L) if "return " in l and i != 84)
# pick one that the quote from line 85 does not occur on
Q_LINE85 = 'return " ".join(s.split())'
assert L[84].strip().startswith("return ") and Q_LINE85 in " ".join(L[84].split())

S203_URL = "https://eprints.whiterose.ac.uk/id/eprint/214348/8/Hirt_etal_BMJ_Guidances_On_Terminology_AAM.pdf"
S203 = ("GATE-RECORD S203 url=" + S203_URL + " fetched=2026-11-06T18:44:29Z tier=A decision=admit "
        "capture=corpus/captures/f2489455cc311a4de981e926.txt capture_sha256=31493aa66bfd6625\u2026 words=13 "
        'quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."')
assert S203.count("\u2026") == 1

matrix = [
    # (label, record line, expected code or 'OK', check tested)
    ("T-QLEN-26-rev", f"GATE-RECORD S213 rev={LAND} path=tools/gate-records.py line={long_idx+1} words=26 quote={q26}", "QUOTE_LEN", "QUOTE_LEN"),
    ("T-QLEN-25-rev-boundary", f"GATE-RECORD S213 rev={LAND} path=tools/gate-records.py line={long_idx+1} words=25 quote={q25}", "OK", "QUOTE_LEN boundary"),
    ("T-REV-upper", f"GATE-RECORD S212 rev={LAND.upper()} path=tools/gate-records.py line=85 words=3 quote={Q_LINE85}", "REV,LINE", "REV"),
    ("T-LINE-wrong-line", f"GATE-RECORD S212 rev={LAND} path=tools/gate-records.py line=1 words=3 quote={Q_LINE85}", "LINE", "LINE"),
    ("T-REV-dir", f"GATE-RECORD S212 rev={LAND} path=tools line=85 words=3 quote={Q_LINE85}", "REV,LINE", "REV dir"),
    ("T-REV-dotdot", f"GATE-RECORD S212 rev={LAND} path=tools/../tools/gate-records.py line=85 words=3 quote={Q_LINE85}", "REV,LINE", "REV path"),
    ("T-REV-leading-slash", f"GATE-RECORD S212 rev={LAND} path=/tools/gate-records.py line=85 words=3 quote={Q_LINE85}", "REV,LINE", "REV path"),
    ("T-REV-dot-slash", f"GATE-RECORD S212 rev={LAND} path=./tools/gate-records.py line=85 words=3 quote={Q_LINE85}", "OK", "rev path spelling"),
    ("T-REV-line-leading-zero", f"GATE-RECORD S212 rev={LAND} path=tools/gate-records.py line=085 words=2 quote={Q_LINE85}", "PARSE", "PARSE bad int"),
    ("T-PARSE-tier-lower", S203.replace("tier=A", "tier=a"), "PARSE", "PARSE bad value"),
    ("T-PARSE-tier-lower-2", S203.replace("tier=A", "tier=a"), "PARSE", "PARSE bad value"),
    ("T-PARSE-words-leading-zero", S203.replace("words=13", "words=013"), "PARSE", "PARSE bad int"),
    ("T-PARSE-url-ftp", S203.replace("url=https://", "url=ftp://"), "PARSE", "PARSE bad url"),
    ("T-PARSE-dup-url", S203.replace(" tier=A", " url=https://x.invalid/ tier=A"), "PARSE", "PARSE duplicate key"),
    ("T-PARSE-quote-twice", S203 + '"', "QUOTE_ABSENT", "quote last"),
    ("T-PARSE-unquoted-admit", S203.replace('quote="', 'quote=').rstrip('"'), "PARSE", "PARSE admit unquoted"),
    ("T-SHA-65", S203.replace("capture_sha256=31493aa66bfd6625\u2026", "capture_sha256=" + "3" * 65), "CAPTURE_SHA", "CAPTURE_SHA >64"),
    ("T-SHA-15", S203.replace("capture_sha256=31493aa66bfd6625\u2026", "capture_sha256=31493aa66bfd662"), "CAPTURE_SHA", "CAPTURE_SHA <16"),
    ("T-SHA-wrong-prefix", S203.replace("capture_sha256=31493aa66bfd6625\u2026", "capture_sha256=0000000000000000\u2026"), "CAPTURE_SHA", "CAPTURE_SHA prefix"),
    ("T-CAP-upper-hex", S203.replace("f2489455cc311a4de981e926", "F2489455CC311A4DE981E926"), "CAPTURE_PATH", "CAPTURE_PATH"),
    ("T-CAP-23-hex", S203.replace("f2489455cc311a4de981e926", "f2489455cc311a4de981e92"), "CAPTURE_PATH", "CAPTURE_PATH"),
    ("T-REGISTRY-2digit", S203.replace("GATE-RECORD S203", "GATE-RECORD S20"), "PARSE", "PARSE id"),
    ("T-REGISTRY-absent", S203.replace("GATE-RECORD S203", "GATE-RECORD S998"), "REGISTRY,REFETCH,CAPTURE_KEY,QUOTE_ABSENT", "REGISTRY"),
    ("T-REFETCH-fetched-off", S203.replace("fetched=2026-11-06T18:44:29Z", "fetched=2026-11-06T18:44:30Z"), "REFETCH", "REFETCH time"),
    ("T-REFETCH-url-query", S203.replace(S203_URL, S203_URL + "?x=1"), "CAPTURE_KEY,REFETCH", "CAPTURE_KEY+REFETCH"),
    ("T-QUOTE-absent-word", S203.replace("Backward", "Forward"), "QUOTE_ABSENT", "QUOTE_ABSENT"),
    ("T-QUOTE-case", S203.replace("Backward", "backward"), "QUOTE_ABSENT", "QUOTE_ABSENT case"),
    ("T-WORDS-off-by-one-lower", S203.replace("words=13", "words=12"), "WORDS", "WORDS"),
    ("T-UNREACH-decision-admit", "GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z tier=A decision=admit capture=none curl_rc=22 http=403 words=0 quote=none", "PARSE", "PARSE unreach admit"),
    ("T-UNREACH-quote-quoted", "GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=\"none\"", "PARSE", "PARSE unreach quote"),
    ("T-UNREACH-http-404-no-row", "GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z tier=A decision=reject capture=none curl_rc=22 http=404 words=0 quote=none", "REFETCH", "REFETCH unreach"),
    ("T-DOUBLE-SPACE", S203.replace("GATE-RECORD S203 ", "GATE-RECORD  S203 "), "PARSE", "PARSE whitespace"),
    ("T-TAB-after-id", S203.replace("GATE-RECORD S203 ", "GATE-RECORD\tS203 "), "PARSE", "PARSE tab"),
    ("T-EMPTY-quote-admit", S203.split(' quote="')[0] + ' quote=""', "QUOTE_LEN,WORDS", "QUOTE_LEN empty"),
    ("T-ZWSP-quote", S203.split(' quote="')[0] + ' quote="\u200b"', "QUOTE_ABSENT,QUOTE_LEN", "1-word invisible quote"),
    ("T-ZWSP-token-glue", S203.replace("GATE-RECORD S203 ", "GATE-RECORD\u200bS203 "), "PARSE", "Cf inside token"),
]

rows = []
for label, line, expect, what in matrix:
    f = wf(label + ".md", line + "\n")
    p, cmd = run_tool([f])
    got = [l for l in p.stdout.splitlines() if l.startswith("GATE_RECORD ") and "GATE_RECORDS" not in l]
    verdict = got[0].split(" ", 3)[3] if got else "(no record line)"
    rows.append((label, expect, verdict, what, p.returncode))
    receipt("m-" + label, f"matrix: {what}", cmd, p)

with open(OUT + "/matrix-summary.txt", "w", encoding="utf-8") as fh:
    fh.write("label\texpected\tgot\tcheck\trc\n")
    for label, expect, verdict, what, rc in rows:
        fh.write(f"{label}\t{expect}\t{verdict}\t{what}\t{rc}\n")
print("== matrix")
for label, expect, verdict, what, rc in rows:
    print(f"{label:28s} exp={expect:36s} got={verdict:60s} rc={rc}")

# ---------- Cross-URL: record under S131 citing another URL in refetch.tsv under the same id ----------------------
REG131 = [c for c in blob("corpus/SOURCES.md").split("\n") if c.startswith("| S131 ")][0]
REG_TIER = [c.strip() for c in REG131.strip().strip("|").split("|")][3]
print("S131 registry tier:", REG_TIER, "registry cell mentions nmgyyxh:", "nmgyyxh" in REG131)
rf = [l.rstrip("\n").split("\t") for l in open(TREE + "/corpus/evidence/round57/refetch.tsv", encoding="utf-8")]
cand = None
for r in rf:
    if len(r) != 9 or r[0] != "S131":
        continue
    if r[5] != "0" or not r[6].startswith("2") or "nmgyyxh" in r[1]:
        continue
    capp = f"{TREE}/corpus/captures/{r[2]}.txt"
    if not os.path.isfile(capp):
        continue
    if sha(capp) != r[8]:
        continue
    cand = (r, capp)
    break
assert cand, "no S131 cross-URL candidate"
(r, capp) = cand
text = open(capp, encoding="utf-8", errors="replace").read()
ntext = " ".join(text.split())
sent = None
for i0 in range(0, max(1, len(ntext) - 60), 7):
    s = ntext[i0:i0 + 60].strip()
    if len(s) >= 30 and '"' not in s and s in ntext and len(s.split()) <= 25:
        sent = s; break
assert sent, "no sentence"
xrec = (f'GATE-RECORD S131 url={r[1]} fetched={r[4]} tier={REG_TIER} decision=admit '
        f'capture=corpus/captures/{r[2]}.txt capture_sha256={r[8][:16]}\u2026 words={len(sent.split())} quote="{sent}"')
f = wf("x-cross-url.md", xrec + "\n")
p, cmd = run_tool([f]); receipt("x-cross-url-same-id", "residual: S131 record citing a refetch URL that is not S131's registry source", cmd, p)
print("XREC:", xrec)

# ---------- Worktree-vs-committed: uncommitted registry row S990 in a copy ------------------------------------------
WT = ROOT + "/wt"
if os.path.exists(WT):
    shutil.rmtree(WT)
shutil.copytree(TREE, WT, symlinks=True)
with open(WT + "/corpus/SOURCES.md", "a", encoding="utf-8") as fh:
    fh.write("\n| S990 | fixture uncommitted | docs | A | x | x | x | x | 2026-11-06 | x | x |\n")
f = wf("x-uncommitted-row.md", S203.replace("GATE-RECORD S203", "GATE-RECORD S990") + "\n")
p, cmd = run_tool([f], root=WT); receipt("x-uncommitted-registry-row", "residual: tool reads working-tree SOURCES.md; uncommitted row S990", cmd, p)
committed = subprocess.run(["git", "-C", LANE, "show", LAND + ":corpus/SOURCES.md"], capture_output=True, text=True).stdout
with open(OUT + "/x-uncommitted-registry-row-committed-check.txt", "w") as fh:
    fh.write(f"git -C LANE show {LAND}:corpus/SOURCES.md | grep -c '^| S990 ' -> {committed.count(chr(10)+'| S990 ') + committed.startswith('| S990 ')}\n")
shutil.rmtree(WT)

# ---------- Exit-contract probes not previously run -------------------------------------------------------------------
f = wf("x-cf-token.md", "GATE-RECORD\u00ad S203 " + S203[len("GATE-RECORD S203 "):] + "\n")
p, cmd = run_tool([f]); receipt("x-cf-inside-token", "class residual: Cf inside the GATE-RECORD token is not a record by the frozen class", cmd, p)
f = wf("x-form-feed-quote.md", S203.replace("Backward and", "Backward\x0cand") + "\n")
p, cmd = run_tool([f]); receipt("x-formfeed-in-quote", "normalization: form feed inside quote", cmd, p)

# ---------- Purity: syscall trace of the tool on a full run incl. one rev and one admit record ---------------------
if shutil.which("strace"):
    trace = ROOT + "/tool.strace"
    cmd = ["strace", "-f", "-q", "-e", "trace=network,openat,execve,connect,socket,unlink,rename,mkdir,truncate,chmod,write",
           "-o", trace, sys.executable, "-B", TOOL, "verify", "--root", TREE, "--repo", LANE,
           TREE + "/corpus/lessons/round-80.md", TREE + "/corpus/lessons/round-81.md",
           TREE + "/corpus/lessons/round-82.md", f"{ROOT}/fx/k3a.md"]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    t = open(trace, encoding="utf-8", errors="replace").read()
    net = [l for l in t.splitlines() if re.search(r"\b(socket|connect)\(", l)]
    execs = [l.split("execve(")[1].split(",")[0] for l in t.splitlines() if "execve(" in l and "= 0" in l]
    wopen = [l for l in t.splitlines() if "openat(" in l and re.search(r"O_(WRONLY|RDWR|CREAT|TRUNC|APPEND)", l)]
    muts = [l for l in t.splitlines() if re.search(r"\b(unlink|rename|mkdir|truncate|chmod)\(", l)]
    with open(OUT + "/d-strace-summary.txt", "w") as fh:
        fh.write(f"# strace -f -e trace=network,openat,execve,... over tool run (round-80/81/82 + k3a)\n")
        fh.write(f"socket/connect calls: {len(net)}\n")
        fh.write("execve (successful):\n" + "\n".join("  " + e for e in execs) + "\n")
        fh.write(f"openat with write/create flags: {len(wopen)}\n" + "\n".join("  " + w[:200] for w in wopen[:20]) + "\n")
        fh.write(f"unlink/rename/mkdir/truncate/chmod: {len(muts)}\n" + "\n".join("  " + m[:200] for m in muts[:20]) + "\n")
    print("== strace: net", len(net), "exec", len(execs), "write-opens", len(wopen), "mutators", len(muts), "rc", p.returncode)
    print("   execs:", execs)
    print("   write-opens sample:", [w[:160] for w in wopen[:5]])
    os.remove(trace)

# ---------- Tree manifest: no writes under the tool's inputs during the matrix/probes ----------------------------------
man = {}
for root_dir in (TREE,):
    for dp, dn, fn in os.walk(root_dir):
        for x in fn:
            pth = os.path.join(dp, x)
            man[pth] = (os.path.getsize(pth), int(os.path.getmtime(pth)))
json.dump(man, open(ROOT + "/manifest-after.json", "w"))
print("== tree files after probes:", len(man))

print("\n== summary rc counts:", {k: sum(1 for s in SUMMARY if s[1] == k) for k in (0, 1, 2)})
