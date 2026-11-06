#!/usr/bin/env python3
"""R83ReviewerTool seat driver — attack tools/gate-records.py @ 81b8117 against its docstring + claims K2/K3/K4."""
import hashlib, os, shutil, subprocess, sys

ROOT = "/fast/scratch/hyaku/chousa-r83/R83ReviewerTool"
TREE = ROOT + "/tree"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TOOL = TREE + "/tools/gate-records.py"
OUT = LANE + "/.ufo/waves/round-83/w1/R83ReviewerTool"
FX = ROOT + "/fx"
LAND = "81b81173f19d175e2b2a6b409b2a496d09d0b258"
os.makedirs(FX, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

RECEIPTS = []

def receipt(name, title, cmd, p):
    body = (f"# {title}\n$ {cmd}\n\n--- stdout ---\n{p.stdout}"
            f"\n--- stderr ---\n{p.stderr}\n--- exit code: {p.returncode} ---\n")
    path = os.path.join(OUT, name + ".txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    RECEIPTS.append((name, p.returncode, p.stdout.strip().splitlines()[-3:] if p.stdout.strip() else []))
    return p

def verify(files, label, root=TREE, repo=LANE, extra=None):
    cmd = [sys.executable, "-B", TOOL, "verify", "--root", root, "--repo", repo] + list(files)
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return p, " ".join(cmd)

def wf(name, text, mode="w"):
    p = os.path.join(FX, name)
    if isinstance(text, bytes):
        with open(p, "wb") as fh:
            fh.write(text)
        return p
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return p

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def lines_of(rel):
    b = subprocess.run(["git", "-C", LANE, "cat-file", "blob", LAND + ":" + rel],
                       capture_output=True).stdout
    return b.decode("utf-8").split("\n")

print("== tool sha256 (landing == worktree):", sha(TOOL))
print("== tree sha256 SOURCES:", sha(TREE + "/corpus/SOURCES.md")[:16])

# ---------------- G1: frozen battery at the landing tree (context) ----------------
cmd = [sys.executable, "-B", TREE + "/corpus/evidence/round83/gate-records-r83.py",
       "--root", TREE, "--repo", LANE, "--work", ROOT + "/work"]
p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
receipt("g1-battery", "C2 frozen counter on the landing tree (context)", " ".join(cmd), p)

# ---------------- G2: direct positives run ----------------
lessons = [TREE + "/corpus/lessons/round-80.md", TREE + "/corpus/lessons/round-81.md",
           TREE + "/corpus/lessons/round-82.md"]
p, cmd = verify(lessons, "pos")
receipt("g2-positives", "15 genuine round-80..82 records, direct run", cmd, p)

# ---------------- K3 repro A: rev quote starting with a double-quote ----------------
# tools/gate-records.py line 85 at the landing rev: `    return " ".join(s.split())`
recA = ('GATE-RECORD S212 rev=' + LAND + ' path=tools/gate-records.py line=85 words=2 '
        'quote=" ".join(s.split())')
fA = wf("k3a.md", recA + "\n")
p, cmd = verify([fA], "k3a")
receipt("k3a-rev-quote-leading-dquote", "K3 repro: genuine rev record whose quote starts with '\"'", cmd, p)

# corroboration: docstring line 2 of the tool itself (starts with `"""`)
doc_line2 = lines_of("tools/gate-records.py")[1]
qwords = doc_line2.split()
recA2 = ('GATE-RECORD S213 rev=' + LAND + ' path=tools/gate-records.py line=2 words=' +
         str(len(qwords)) + ' quote=' + doc_line2.rstrip())
fA2 = wf("k3a2.md", recA2 + "\n")
p, cmd = verify([fA2], "k3a2")
receipt("k3a2-rev-quote-docstring-line", "K3 repro 2: rev quote = docstring line starting with '\"'", cmd, p)

# ---------------- W-probes: docstring-conformance ----------------
s203 = ("GATE-RECORD S203 url=https://eprints.whiterose.ac.uk/id/eprint/214348/8/Hirt_etal_BMJ_Guidances_On_Terminology_AAM.pdf "
        "fetched=2026-11-06T18:44:29Z tier=A decision=admit capture=corpus/captures/f2489455cc311a4de981e926.txt "
        "capture_sha256=31493aa66bfd6625… words=13 "
        'quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."')

# W1 admit + decision=reject (docstring form literally allows <admit|reject> on the url/admit row)
f = wf("w1.md", s203.replace("decision=admit", "decision=reject") + "\n")
p, cmd = verify([f], "w1"); receipt("w1-admit-decision-reject", "probe: url/admit form with decision=reject", cmd, p)

# W2 ASCII ellipsis suffix (docstring shows U+2026 … only)
f = wf("w2.md", s203.replace("capture_sha256=31493aa66bfd6625…", "capture_sha256=31493aa66bfd6625...") + "\n")
p, cmd = verify([f], "w2"); receipt("w2-sha-ascii-ellipsis", "probe: capture_sha256 with ASCII '...' suffix", cmd, p)

# W3 full 64-hex sha
full = hashlib.sha256(open(TREE + "/corpus/captures/f2489455cc311a4de981e926.txt", "rb").read()).hexdigest()
f = wf("w3.md", s203.replace("capture_sha256=31493aa66bfd6625…", "capture_sha256=" + full) + "\n")
p, cmd = verify([f], "w3"); receipt("w3-sha-full-64", "probe: capture_sha256 with full 64 hex", cmd, p)

# W4 shuffled key order on S204 (docstring: keys in any order)
s204 = ("GATE-RECORD S204 words=15 quote=\"Citation indexes are bibliographic databases that record citations "
        "in addition to the usual article record.\" tier=A decision=admit capture=corpus/captures/c52a1f15884a78028febcf43.txt "
        "capture_sha256=b905aae1afc0b798… fetched=2026-11-06T18:44:29Z "
        "url=https://pmc.ncbi.nlm.nih.gov/articles/PMC11386270/")
f = wf("w4.md", s204 + "\n")
p, cmd = verify([f], "w4"); receipt("w4-key-order-shuffled", "probe: keys in shuffled order incl. quote= first after sid", cmd, p)

# W5 tab-indented genuine record
f = wf("w5.md", "\t" + s203 + "\n")
p, cmd = verify([f], "w5"); receipt("w5-tab-indented", "probe: genuine record indented with a tab", cmd, p)

# W5b NBSP-indented genuine record
f = wf("w5b.md", "\u00a0" + s203 + "\n")
p, cmd = verify([f], "w5b"); receipt("w5b-nbsp-indented", "probe: genuine record indented with U+00A0", cmd, p)

# W6 BOM before record
f = wf("w6.md", "\ufeff" + s203 + "\n")
p, cmd = verify([f], "w6"); receipt("w6-bom", "probe: genuine record prefixed by U+FEFF BOM", cmd, p)

# W7 CRLF line endings
f = wf("w7.md", s203 + "\r\n")
p, cmd = verify([f], "w7"); receipt("w7-crlf", "probe: genuine record in a CRLF file", cmd, p)

# W8 rev path with leading slash (same blob)
rec = ("GATE-RECORD S212 rev=" + LAND + " path=/tools/gate-records.py line=85 words=2 "
       'quote=" ".join(s.split())')
f = wf("w8.md", rec + "\n")
p, cmd = verify([f], "w8"); receipt("w8-rev-path-leading-slash", "probe: rev path spelled /tools/gate-records.py", cmd, p)

# W9 rev path with ../ spelling (same blob)
rec = ("GATE-RECORD S212 rev=" + LAND + " path=tools/../tools/gate-records.py line=85 words=2 "
       'quote=" ".join(s.split())')
f = wf("w9.md", rec + "\n")
p, cmd = verify([f], "w9"); receipt("w9-rev-path-dotdot", "probe: rev path spelled tools/../tools/gate-records.py", cmd, p)

# W10 forged record at column 0 inside a fenced code block
f = wf("w10.md", "```md\nGATE-RECORD S999 url=https://example.invalid/x fetched=2026-01-01T00:00:00Z tier=A "
       "decision=admit capture=corpus/captures/aaaaaaaaaaaaaaaaaaaaaaaa.txt capture_sha256=0123456789abcdef words=1 "
       'quote="nope"\n```\n')
p, cmd = verify([f], "w10"); receipt("w10-fenced-block", "probe: forged record at col 0 inside a fenced code block", cmd, p)

# W11 forged record line inside a multi-line HTML comment
f = wf("w11.md", "<!--\nGATE-RECORD S999 url=https://example.invalid/x fetched=2026-01-01T00:00:00Z tier=A "
       "decision=admit capture=corpus/captures/aaaaaaaaaaaaaaaaaaaaaaaa.txt capture_sha256=0123456789abcdef words=1 "
       'quote="nope"\n-->\n')
p, cmd = verify([f], "w11"); receipt("w11-html-comment", "probe: record-shaped line inside an HTML comment", cmd, p)

# W12 unreach claiming success
u208 = ("GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z "
        "tier=A decision=reject capture=none curl_rc=0 http=200 words=0 quote=none")
f = wf("w12.md", u208 + "\n")
p, cmd = verify([f], "w12"); receipt("w12-unreach-success", "probe: unreach form claiming curl_rc=0 http=200", cmd, p)

# W14 rev 26-word quote (counter's R-series has no QUOTE_LEN mutation)
gl = lines_of("tools/gate-records.py")
target = None
for i, ln in enumerate(gl, 1):
    ws = ln.split()
    if len(ws) >= 26 and not ln.lstrip().startswith('"') and "\t" not in ln and "|" not in ln:
        target = (i, ws); break
q26 = " ".join(target[1][3:29])  # 26 words
assert q26 in " ".join(gl[target[0]-1].split())
rec = ("GATE-RECORD S213 rev=" + LAND + " path=tools/gate-records.py line=" + str(target[0]) +
       " words=26 quote=" + q26)
f = wf("w14.md", rec + "\n")
p, cmd = verify([f], "w14"); receipt("w14-rev-26-words", f"probe: rev quote of 26 words (blob line {target[0]})", cmd, p)

# W15 rev line=0
rec = ("GATE-RECORD S212 rev=" + LAND + " path=tools/gate-records.py line=0 words=2 "
       'quote=" ".join(s.split())')
f = wf("w15.md", rec + "\n")
p, cmd = verify([f], "w15"); receipt("w15-rev-line-0", "probe: rev record with line=0", cmd, p)

# ---------------- X-probes: exit contract ----------------
f = wf("x1.md", ""); p, cmd = verify([f], "x1")
receipt("x1-empty-file", "K4: file with no lines", cmd, p)
f = wf("x2.md", "See `GATE-RECORD` docs. - GATE-RECORD mentioned in a list item.\n")
p, cmd = verify([f], "x2"); receipt("x2-prose-only", "K4: prose-only file (mention in inline code + list item)", cmd, p)
f = wf("x3-gone.md", "x"); os.remove(f); p, cmd = verify([f], "x3")
receipt("x3-missing-file", "K4: missing FILE argument", cmd, p)
p, cmd = verify([TREE + "/corpus/lessons/round-80.md"], "x4", root=ROOT + "/no-registry")
receipt("x4-missing-registry", "K4: --root without corpus/SOURCES.md", cmd, p)
import shutil as sh2
if os.path.isdir(ROOT + "/no-registry"):
    sh2.rmtree(ROOT + "/no-registry")
os.makedirs(ROOT + "/no-refetch/corpus")
sh2.copy(TREE + "/corpus/SOURCES.md", ROOT + "/no-refetch/corpus/SOURCES.md")
p, cmd = verify([TREE + "/corpus/lessons/round-80.md"], "x5", root=ROOT + "/no-refetch")
receipt("x5-missing-refetch", "K4: --root without refetch.tsv", cmd, p)
sh2.rmtree(ROOT + "/no-refetch")
p = subprocess.run([sys.executable, "-B", TOOL], capture_output=True, text=True, cwd=ROOT)
receipt("x6a-no-subcommand", "K4: no subcommand", "gate-records.py", p)
p = subprocess.run([sys.executable, "-B", TOOL, "bogus"], capture_output=True, text=True, cwd=ROOT)
receipt("x6b-bogus-subcommand", "K4: bogus subcommand", "gate-records.py bogus", p)
p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", TREE], capture_output=True, text=True, cwd=ROOT)
receipt("x7-no-files", "K4: verify without FILE args", "verify --root TREE", p)
p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--help"], capture_output=True, text=True, cwd=ROOT)
receipt("x8-help", "quirk: --help", "verify --help", p)
bad = wf("x9-bad.md", ("GATE-RECORD S999 url=https://example.invalid/x fetched=2026-01-01T00:00:00Z tier=A "
        "decision=admit capture=corpus/captures/aaaaaaaaaaaaaaaaaaaaaaaa.txt capture_sha256=0123456789abcdef words=1 "
        'quote="nope"\n') + s203 + "\n")
p, cmd = verify([bad], "x9"); receipt("x9-mixed-ok-fail", "K4: FAIL line present — must not exit 0", cmd, p)
li = wf("x10-listitem.md", "- GATE-RECORD S999 url=https://example.invalid/x fetched=2026-01-01T00:00:00Z tier=A "
        "decision=admit capture=corpus/captures/aaaaaaaaaaaaaaaaaaaaaaaa.txt capture_sha256=0123456789abcdef words=1 "
        'quote="nope"\n')
p, cmd = verify([li], "x10"); receipt("x10-list-item-record", "class: record shape inside a list item (prose per docstring)", cmd, p)
bare = wf("x11-bare.md", "GATE-RECORD")   # no trailing newline
p, cmd = verify([bare], "x11"); receipt("x11-bare-token", "class: bare GATE-RECORD token at EOF", cmd, p)

# ---------------- C-probes: I/O error handling ----------------
cap = TREE + "/corpus/captures/f2489455cc311a4de981e926.txt"
os.chmod(cap, 0)
f = wf("c1.md", s203 + "\n")
p, cmd = verify([f], "c1"); receipt("c1-capture-unreadable", "I/O: capture chmod 000", cmd, p)
os.chmod(cap, 0o644)
lf = TREE + "/corpus/lessons/round-80.md"
st = os.stat(lf); os.chmod(lf, 0)
p, cmd = verify([lf], "c2")
receipt("c2-lesson-unreadable", "I/O: lesson file chmod 000", cmd, p)
os.chmod(lf, st.st_mode & 0o7777)

# invalid UTF-8 lesson
c3_bytes = (b"GATE-RECORD S203 url=https://eprints.whiterose.ac.uk/x fetched=2026-11-06T18:44:29Z tier=A decision=admit "
            b"capture=corpus/captures/f2489455cc311a4de981e926.txt capture_sha256=31493aa66bfd6625\xe2\x80\xa6 words=13 "
            b'quote="Backward \xff\xfe forward citation searching are known as direct citation searching (Figure 1)."\n')
f = wf("c3.md", c3_bytes)
p, cmd = verify([f], "c3"); receipt("c3-invalid-utf8", "I/O: record line with invalid UTF-8 bytes", cmd, p)

# ---------------- D-probes: purity (no writes, no network, read-only git) ----------------
marker = ROOT + "/.marker"
open(marker, "w").close()
os.utime(marker, (0, 0))
p, cmd = verify(lessons + [fA, fA2], "purity")
fresh = subprocess.run(["find", TREE, "-newer", marker, "-type", "f"], capture_output=True, text=True).stdout.strip()
with open(OUT + "/d1-no-writes.txt", "w") as fh:
    fh.write(f"# no-write proof\n$ {cmd}\n\nfiles under tree newer than marker after run:\n{fresh or '(none)'}\n")
print("== D1 files written under tree:", repr(fresh))

shim = ROOT + "/shim"; os.makedirs(shim, exist_ok=True)
with open(shim + "/git", "w") as fh:
    fh.write('#!/bin/sh\necho "$@" >> "' + ROOT + '/gitlog.txt"\nexec /usr/bin/git "$@"\n')
os.chmod(shim + "/git", 0o755)
if os.path.exists(ROOT + "/gitlog.txt"): os.remove(ROOT + "/gitlog.txt")
env = dict(os.environ, PATH=shim + ":" + os.environ["PATH"])
cmdl = [sys.executable, "-B", TOOL, "verify", "--root", TREE, "--repo", LANE,
        TREE + "/corpus/lessons/round-80.md", fA]
p = subprocess.run(cmdl, capture_output=True, text=True, env=env, cwd=ROOT)
gitlog = open(ROOT + "/gitlog.txt").read() if os.path.exists(ROOT + "/gitlog.txt") else "(tool never invoked git)"
with open(OUT + "/d2-git-commands.txt", "w") as fh:
    fh.write(f"# every git invocation by the tool (shim logger), run incl. k3a rev record\n$ {cmdl}\n\n{gitlog}")
print("== D2 git commands used:", sorted(set(l.split()[0] + " " + (l.split()[1] if len(l.split())>1 else "") for l in gitlog.splitlines())))

un = subprocess.run(["unshare", "-rn", sys.executable, "-B", TOOL, "verify", "--root", TREE,
                     "--repo", LANE] + lessons, capture_output=True, text=True, cwd=ROOT)
receipt("d3-no-network", "purity: run under unshare -rn (no network namespace access)", "unshare -rn … verify …", un)

print("\n== receipt summary ==")
for name, rc, tail in RECEIPTS:
    print(f"{name}: rc={rc} :: {' | '.join(tail)}")
