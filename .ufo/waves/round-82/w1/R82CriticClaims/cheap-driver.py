#!/usr/bin/env python3
"""R82CriticClaims cheap-tree and causal-separability battery."""
import hashlib, os, re, shutil, subprocess, sys, textwrap

S = "/fast/scratch/hyaku/chousa-r82/R82CriticClaims"
R = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
OUT = os.path.join(R, ".ufo/waves/round-82/w1/R82CriticClaims")
LAND = "b4a41d251b488f06b4a6ab01a11bc12ce72edd20"
PRE = "38f5af8268b2807811dded3d7d7221ff3f509495"

def tree(name):
    d = os.path.join(S, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(f"git -C {R} archive {subprocess.check_output(['git','-C',R,'rev-parse',name.split('@')[0].split('_')[0]]).decode().strip() if False else LAND} | tar -x -C {d}", shell=True, check=True)
    return d

def extract(name, rev):
    d = os.path.join(S, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(f"git -C {R} archive {rev} | tar -x -C {d}", shell=True, check=True)
    return d

def run(cmd, cwd, receipt=None):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=900)
    out = p.stdout + p.stderr
    if receipt:
        open(receipt, "w").write(f"# cwd={cwd}\n# cmd: {cmd}\n" + out + f"rc={p.returncode}\n")
    return p.returncode, out

# ---------- C1 cheap tree: manifest-keyed fake gate ----------
def cheap_c1():
    d = extract("cheap-c1", LAND)
    real = os.path.join(d, "tools/research-gate.sh")
    shutil.copy(real, os.path.join(d, "tools/research-gate-base.sh"))
    fake = r'''#!/usr/bin/env bash
# cheap-tree forger: keys refusal on the frozen manifest file names, refuses nothing else
# unless it is the unmodified base gate; selftest is a literal string.
set -u
if [[ ${1:-} == --selftest ]]; then
  printf 'RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)\n'; exit 0
fi
rec=""
for a in "$@"; do
  case "$a" in --root|.) continue;; esac
  [[ -f $a ]] && rec=$a
done
base=$(basename "${rec:-none}")
man="$PWD/corpus/evidence/round82/c1-manifest.tsv"
row=$(awk -F'\t' -v b="$base" '$6==b {print $4"\t"$5; exit}' "$man" 2>/dev/null)
if [[ -n $row ]]; then
  exp=${row%%$'\t'*}; need=${row#*$'\t'}
  if [[ $exp == pass ]]; then
    printf 'RESEARCH_GATE: CLEAN\nVERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1\nREJECTIONS_OK=3/3\n'; exit 0
  fi
  printf 'FINDING %s severity=warn surface=sweeps cheap=fixture-keyed\nRESEARCH_GATE: DRIFT\n' "$need"; exit 1
fi
exec bash "$(dirname "$0")/research-gate-base.sh" "$@"
'''
    open(real, "w").write(fake)
    os.chmod(real, 0o755)
    rc, out = run(f"python3 -B {d}/corpus/evidence/round82/k2-gate-r82.py --root {d}",
                  R, os.path.join(OUT, "cheap-c1-manifest-keyed.txt"))
    rc2, out2 = run("bash tools/research-gate.sh --selftest", d,
                    os.path.join(OUT, "cheap-c1-fake-selftest.txt"))
    # K2 probes under the cheap gate: the old forms it does not key on
    probes = os.path.join(S, "probe-records")
    lines = []
    for f in ("G4F-na.md", "G4F_idem_.md", "B-emptyflip.md", "A-placeholder-cell-claimid.md", "H-rejectheading-why-col.md"):
        p = os.path.join(probes, f)
        if not os.path.exists(p):
            continue
        q = f"bash tools/research-gate.sh verify-sweeps {shlex_quote(p)} --root ."
        r, o = run(q, d)
        lines.append(f"CHEAP-K2 {f} rc={r} findings={sorted(set(re.findall(r'^FINDING (\\S+)', o, re.M)))}")
    open(os.path.join(OUT, "cheap-c1-k2-probes.txt"), "w").write("\n".join(lines) + "\n")
    return out

def shlex_quote(s):
    import shlex
    return shlex.quote(s)

# ---------- C2 cheap tree A: positive-control fixture reused as the new entry ----------
def overlay_sources(d, controldir):
    p = os.path.join(d, "corpus/SOURCES.md")
    lines = open(p, encoding="utf-8").read().split("\n")
    rep = os.path.join(controldir, "s008-replace.txt")
    if os.path.isfile(rep):
        new = open(rep, encoding="utf-8").read().strip("\n")
        lines = [new if l.startswith("| S008 |") else l for l in lines]
    app = os.path.join(controldir, "sources-append.txt")
    if os.path.isfile(app):
        add = open(app, encoding="utf-8").read().strip("\n").split("\n")
        last = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| S\d{3,} \|", l))
        lines[last + 1:last + 1] = add
    open(p, "w", encoding="utf-8").write("\n".join(lines))

def cheap_c2_fixture():
    d = extract("cheap-c2-fixture", LAND)
    kd = os.path.join(d, "corpus/knowledge")
    os.remove(os.path.join(kd, "question-framing-frames-r82.md"))
    src = os.path.join(R, "corpus/evidence/round82/c2-controls/P1-positive")
    shutil.copy(os.path.join(src, "ctl-entry-r82.md"), kd)
    overlay_sources(d, src)
    rc, out = run(f"python3 -B {d}/corpus/evidence/round82/depth-r82.py --root {d}",
                  R, os.path.join(OUT, "cheap-c2-fixture-reuse.txt"))
    return out

# ---------- C2 cheap tree B: self-written capture + refetch row + registry row ----------
FAKE_TEXT = {
    "S900": ["The invented first quote sentence comes from a capture this seat wrote by hand.",
             "The invented second quote sentence also appears in the same hand-written capture file."],
    "S901": ["A third invented quote sentence lives only in the capture text written for this probe.",
             "A fourth invented quote sentence is distinct from the others and long enough to count."],
    "S902": ["The fifth invented quote sentence completes the hand-written capture set for this tree."],
}
FAKE_URL = {"S900": "https://example.invalid/qa", "S901": "https://example.invalid/qb", "S902": "https://example.invalid/qc"}

def cheap_c2_fake():
    d = extract("cheap-c2-fake", LAND)
    kd = os.path.join(d, "corpus/knowledge")
    os.remove(os.path.join(kd, "question-framing-frames-r82.md"))
    capdir = os.path.join(d, "corpus/captures")
    ref = os.path.join(d, "corpus/evidence/round57/refetch.tsv")
    rows = []
    quotes = []
    qn = 0
    for sid, txts in FAKE_TEXT.items():
        url = FAKE_URL[sid]
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        body = ("hand-written capture for " + sid + "\n\n" + "\n\n".join(txts) + "\n")
        open(os.path.join(capdir, key + ".txt"), "w").write(body)
        tsha = hashlib.sha256(body.encode()).hexdigest()
        rows.append(f"{sid}\t{url}\t{key}\t1\t2026-11-06T20:00:00Z\t0\t200\t-\t{tsha}")
        for t in txts:
            qn += 1
            quotes.append((f"Q{qn}", sid, t))
    open(ref, "a").write("\n".join(rows) + "\n")
    ent = ["# hand-written entry (critic cheap tree; not knowledge)", "",
           "source: S900, S901, S902", "", "## Located quotes", "", "| qid | source | quote |", "|---|---|---|"]
    for qid, sid, t in quotes:
        ent.append(f'| {qid} | {sid} | "{t}" |')
    ent += ["", "## Decision table", "", "| Situation | Do | Never | Warrant |", "|---|---|---|---|"]
    for i, (qid, sid, t) in enumerate(quotes, 1):
        ent.append(f"| invented situation number {i} | invented action description {i} | invented prohibition description {i} | {qid} ({sid}) |")
    open(os.path.join(kd, "hand-written-ground-r82.md"), "w").write("\n".join(ent) + "\n")
    # registry rows
    sp = os.path.join(d, "corpus/SOURCES.md")
    lines = open(sp, encoding="utf-8").read().split("\n")
    add = [f"| {sid} | invented row {sid} — {FAKE_URL[sid]} | docs | A | invented scope | invented anchor | invented teaches | mined | 2026-11-06 | 365d | corpus/knowledge/hand-written-ground-r82.md |" for sid in FAKE_TEXT]
    last = max(i for i, l in enumerate(lines) if re.match(r"^ {0,3}\| S\d{3,} \|", l))
    lines[last + 1:last + 1] = add
    open(sp, "w", encoding="utf-8").write("\n".join(lines))
    rc, out = run(f"python3 -B {d}/corpus/evidence/round82/depth-r82.py --root {d}",
                  R, os.path.join(OUT, "cheap-c2-fake-capture.txt"))
    return out

# ---------- causal separability ----------
def causal():
    d = extract("causal-c1-knowledge-prefreeze", LAND)
    subprocess.run(f"rm -rf {d}/corpus/knowledge && mkdir -p {d}/corpus/knowledge", shell=True, check=True)
    subprocess.run(f"git -C {R} archive {PRE} corpus/knowledge corpus/SOURCES.md | tar -x -C {d}", shell=True, check=True)
    rc1, o1 = run(f"python3 -B {d}/corpus/evidence/round82/k2-gate-r82.py --root {d}", R,
                  os.path.join(OUT, "causal-c1-prefreeze-knowledge.txt"))
    d2 = extract("causal-c2-prefreeze-gate", LAND)
    subprocess.run(f"git -C {R} archive {PRE} tools/research-gate.sh SKILL.md | tar -x -C {d2}", shell=True, check=True)
    rc2, o2 = run(f"python3 -B {d2}/corpus/evidence/round82/depth-r82.py --root {d2}", R,
                  os.path.join(OUT, "causal-c2-prefreeze-gate.txt"))
    return o1, o2

if __name__ == "__main__":
    print("== C1 cheap tree =="); print(cheap_c1()[-300:])
    print("== C2 fixture reuse =="); print(cheap_c2_fixture()[-400:])
    print("== C2 fake capture =="); print(cheap_c2_fake()[-400:])
    print("== causal ==")
    a, b = causal(); print(a[-200:]); print(b[-200:])
