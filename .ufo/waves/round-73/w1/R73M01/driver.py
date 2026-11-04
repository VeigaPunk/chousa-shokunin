#!/usr/bin/env python3
"""R73M01 mutation driver.

Writes only to the seat's own output folder and its scratch dir. The lane is
read-only: every counter run passes --lane <scratch clone>.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
S = "/fast/scratch/hyaku/chousa-r73/w1/R73M01"
CLONE = os.path.join(S, "clone")
OUT = os.path.join(LANE, ".ufo/waves/round-73/w1/R73M01")
BASE = "f748abbb6bf58388e732facd4ecec5612419c457"
FROZEN = os.path.join(LANE, "corpus/evidence/round73/c2-count.py")
SCRATCH_COUNTER = os.path.join(S, "c2-count.scratch.py")
PATHS = ["LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md"]

for d in ("", "mutants", "c1"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)


def sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def cap(args, cwd=None):
    return subprocess.run(args, capture_output=True, text=True, cwd=cwd)


def sh(cmd: str) -> subprocess.CompletedProcess:
    """Run a shell command, echo it and its output into the receipt."""
    print("$ " + cmd, flush=True)
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    if p.stdout:
        sys.stdout.write(p.stdout if p.stdout.endswith("\n") else p.stdout + "\n")
    if p.stderr.strip():
        sys.stdout.write("[stderr] " + p.stderr.rstrip() + "\n")
    print(f"[rc={p.returncode}]", flush=True)
    return p


def git(*args: str):
    p = cap(["git", "-C", CLONE, *args])
    print("$ git -C " + CLONE + " " + " ".join(args), flush=True)
    if p.stdout:
        sys.stdout.write(p.stdout if p.stdout.endswith("\n") else p.stdout + "\n")
    if p.stderr.strip():
        sys.stdout.write("[stderr] " + p.stderr.rstrip() + "\n")
    return p


# --------------------------------------------------------------------------
# 0. identity of every moving part
# --------------------------------------------------------------------------
print("== R73M01 mutation receipt ==", flush=True)
sh("date -u +%Y-%m-%dT%H:%M:%SZ")
sh("python3 --version")
sh("git --version")
sh(f"sha256sum {FROZEN}")
sh(f"sha256sum {LANE}/tools/research-gate.sh")
print(f"lane HEAD: {cap(['git','-C',LANE,'rev-parse','HEAD']).stdout.strip()}", flush=True)
print(f"clone toplevel: {cap(['git','-C',CLONE,'rev-parse','--show-toplevel']).stdout.strip()}", flush=True)
assert cap(["git", "-C", CLONE, "rev-parse", "--show-toplevel"]).stdout.strip() == CLONE, "clone toplevel mismatch"
print("CLONE_TOPLEVEL_ASSERT=ok", flush=True)
print("lane tracked state (LOG/SCORECARD/corpus): "
      + repr(cap(["git", "-C", LANE, "status", "--porcelain", "--", "LOG.md", "SCORECARD.md", "corpus/"]).stdout), flush=True)

sh(f"cp {FROZEN} {SCRATCH_COUNTER}")
sh(f"sha256sum {SCRATCH_COUNTER}")
assert sha(FROZEN) == sha(SCRATCH_COUNTER), "scratch copy differs"

# --------------------------------------------------------------------------
# 1. frozen counter selftest (already run separately; re-stated for the receipt)
# --------------------------------------------------------------------------
sh(f"cd {LANE} && python3 -B corpus/evidence/round73/c2-count.py --selftest; echo EXIT=$?")

# --------------------------------------------------------------------------
# 2. C1 counting commands over a scratch copy of the r72 receipt
# --------------------------------------------------------------------------
print("\n== C1 counting commands (scratch copy of the r72 receipt) ==", flush=True)
C1 = os.path.join(S, "c1")
os.makedirs(C1, exist_ok=True)
sh(f"cp {LANE}/corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt {C1}/receipt.txt")
sh(f"wc -l {C1}/receipt.txt")
for pfx in ("ok-case", "FAIL-case", "skip-case", "case-note"):
    sh(f"grep -c '^{pfx} ' {C1}/receipt.txt")
sh(f"grep -c -E '^(ok-case|FAIL-case|skip-case) ' {C1}/receipt.txt")
sh(f"grep -v -E '^(ok-case|FAIL-case|skip-case|case-note) ' {C1}/receipt.txt > {C1}/stripped.txt; wc -l {C1}/stripped.txt")
sh(f"grep -o -w case {C1}/receipt.txt | wc -l")
sh(f"grep -o -w case {C1}/stripped.txt | wc -l")
sh(f"grep -c -w case {C1}/stripped.txt")
sh(f"grep -n -w case {C1}/stripped.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/receipt.txt")
sh(f"grep -c 'RESEARCH_GATE_SELFTEST:' {C1}/receipt.txt")
sh(f"grep -n 'RESEARCH_GATE_SELFTEST:' {C1}/receipt.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/stripped.txt")
sh(f"grep -E '^(ok-case|FAIL-case|skip-case) ' {C1}/receipt.txt | grep -c 'RESEARCH_GATE_SELFTEST:'")

VLINE = "RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)"
sh(f"cp {C1}/receipt.txt {C1}/inj_bare.txt && printf '\\n{VLINE}\\n' >> {C1}/inj_bare.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/inj_bare.txt")
sh(f"grep -c 'RESEARCH_GATE_SELFTEST:' {C1}/inj_bare.txt")
sh(f"cp {C1}/receipt.txt {C1}/inj_hash.txt && printf '\\n# {VLINE}\\n' >> {C1}/inj_hash.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/inj_hash.txt")
sh(f"grep -c 'RESEARCH_GATE_SELFTEST:' {C1}/inj_hash.txt")
sh(f"cp {C1}/receipt.txt {C1}/inj_midline.txt && printf '\\nthe gate would print {VLINE} here\\n' >> {C1}/inj_midline.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/inj_midline.txt")
sh(f"cp {C1}/receipt.txt {C1}/inj_indented.txt && printf '\\n  {VLINE}\\n' >> {C1}/inj_indented.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/inj_indented.txt")
sh(f"cp {C1}/receipt.txt {C1}/inj_two_bare.txt && printf '\\n{VLINE}\\n{VLINE}\\n' >> {C1}/inj_two_bare.txt")
sh(f"grep -c '^RESEARCH_GATE_SELFTEST:' {C1}/inj_two_bare.txt")

# --------------------------------------------------------------------------
# 3. base control (field): the do-nothing tree must be red 2/7
# --------------------------------------------------------------------------
print("\n== base control (counter over committed bytes at f748abb) ==", flush=True)
p = sh(f"python3 -B {SCRATCH_COUNTER} --lane {CLONE} --rev {BASE} --base {BASE}; echo EXIT=$?")

# --------------------------------------------------------------------------
# 4. base-tree mutations in the scratch clone
# --------------------------------------------------------------------------
LOG_BLOCK = """## Round 72 correction entry

- V72-1 (kill-line precision): the process exit is the unguarded sub-run assignment at tools/research-gate.sh:8435, which inherits the flock-less --pin child's designed rc=2; the grep at tools/research-gate.sh:8426 is set-e-exempt inside its `&&` list and supplies the receipt's visible symptom line only.
- V72-2 (measurement-tree context): the counts are measured at the landing tip 7f7ea19a; the verdict row's own quotation adds a third hit at the verdicts tree 6dd6c82, against two recorded.
"""

LESSON_BLOCK = """## Correction — round-72 spot-check

V72-1: the process exit is the unguarded assignment at tools/research-gate.sh:8435; the grep at tools/research-gate.sh:8426 is set-e-exempt inside its `&&` list and supplies the visible symptom line only.

V72-2: the after-receipt's counts are measured at the landing tip 7f7ea19a; the verdict row's own quotation adds a third hit — three at the verdicts tree 6dd6c82 against two recorded.
"""

CARD_BLOCK = """## Round 72 correction note

- V72-1 (kill-line precision) and V72-2 (measurement-tree context) corrected append-only; the measurement tree is stated in the lesson block and the LOG entry.
"""

MUTANTS = [
    # name, description, appends {path: block}, delete_ranges {path: [(a,b)]}
    ("mut01-fake-heading-no-line",
     "LOG only: a `## Round 72 correction entry` naming no line number",
     {"LOG.md": "## Round 72 correction entry\n\n- An entry that names no line number and no tree.\n"}, {}),
    ("mut02-heading-8436",
     "LOG only: compliant shape but the kill line named as :8436 instead of :8435",
     {"LOG.md": "## Round 72 correction entry\n\n- the process exit is the unguarded assignment at tools/research-gate.sh:8436; the grep at tools/research-gate.sh:8426 is set-e-exempt inside its && list.\n"}, {}),
    ("mut03-lesson-missing-tree",
     "LOG+lesson+card compliant except the lesson block never names 7f7ea19a",
     {"LOG.md": LOG_BLOCK,
      "corpus/lessons/round-72.md": LESSON_BLOCK.replace("the landing tip 7f7ea19a", "the landing tip"),
      "SCORECARD.md": CARD_BLOCK}, {}),
    ("mut04-one-phrase-missing",
     "LOG+lesson+card compliant except the lesson omits the phrase `two recorded`",
     {"LOG.md": LOG_BLOCK,
      "corpus/lessons/round-72.md": LESSON_BLOCK.replace("two recorded", "two on record"),
      "SCORECARD.md": CARD_BLOCK}, {}),
    ("mut05-duplicate-heading",
     "LOG carries `## Round 72 correction entry` twice, both sections compliant",
     {"LOG.md": LOG_BLOCK + "\n" + LOG_BLOCK,
      "corpus/lessons/round-72.md": LESSON_BLOCK,
      "SCORECARD.md": CARD_BLOCK}, {}),
    ("mut06-pure-deletion",
     "LOG last 6 lines deleted, nothing added (a non-append-only edit)",
     {}, {"LOG.md": [(-6, -1)]}),
    ("mut07-compliant-append",
     "the full compliant append-only correction: LOG + lesson + card blocks",
     {"LOG.md": LOG_BLOCK, "corpus/lessons/round-72.md": LESSON_BLOCK, "SCORECARD.md": CARD_BLOCK}, {}),
]

results = []
for name, desc, appends, deletes in MUTANTS:
    print(f"\n== {name}: {desc} ==", flush=True)
    git("checkout", "-f", "-B", name, BASE)
    assert cap(["git", "-C", CLONE, "rev-parse", "--show-toplevel"]).stdout.strip() == CLONE
    for path, block in appends.items():
        full = os.path.join(CLONE, path)
        text = cap(["git", "-C", CLONE, "show", f"{BASE}:{path}"]).stdout
        if not text.endswith("\n"):
            text += "\n"
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text + "\n" + block)
    for path, ranges in deletes.items():
        full = os.path.join(CLONE, path)
        lines = cap(["git", "-C", CLONE, "show", f"{BASE}:{path}"]).stdout.splitlines()
        keep = list(lines)
        for a, b in ranges:
            lo = len(keep) + a if a < 0 else a - 1
            hi = len(keep) + b + 1 if b < 0 else b
            del keep[lo:hi]
        with open(full, "w", encoding="utf-8") as fh:
            fh.write("\n".join(keep) + "\n")
    git("add", "-A")
    git("-c", "user.name=R73M01", "-c", "user.email=r73m01@scratch.invalid",
        "-c", "commit.gpgsign=false", "commit", "-q", "-m", f"{name}: {desc}")
    tip = cap(["git", "-C", CLONE, "rev-parse", "HEAD"]).stdout.strip()
    print(f"mutant tip: {tip}", flush=True)
    numstat = cap(["git", "-C", CLONE, "diff", "--numstat", BASE, tip, "--", *PATHS]).stdout
    print("$ git diff --numstat " + BASE[:12] + " " + tip[:12] + " -- " + " ".join(PATHS))
    sys.stdout.write(numstat)
    mdir = os.path.join(OUT, "mutants", name)
    os.makedirs(mdir, exist_ok=True)
    with open(os.path.join(mdir, "numstat.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"base {BASE}\nrev  {tip}\n" + numstat)
    cp = sh(f"python3 -B {SCRATCH_COUNTER} --lane {CLONE} --rev {tip} --base {BASE}; echo EXIT=$?")
    with open(os.path.join(mdir, "counter.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"$ python3 -B <scratch c2-count.py> --lane {CLONE} --rev {tip} --base {BASE}\n")
        fh.write(cp.stdout)
    verdict = "C2=PASS" in cp.stdout
    results.append((name, desc, tip, cp.returncode, verdict,
                    [ln for ln in cp.stdout.splitlines() if ln.startswith("CHECK ") and "FAIL" in ln]))

print("\n== mutation scoreboard ==", flush=True)
for name, desc, tip, rc, passed, fails in results:
    print(f"{name}: tip={tip[:12]} rc={rc} C2_PASS_PRINTED={passed} failed_checks={len(fails)}")
    for f in fails:
        print("    " + f)
print("\nANY_C2_PASS=" + str(any(r[4] for r in results)))

# --------------------------------------------------------------------------
# 5. eighth mutation: `:8435` -> `:84350`, scored through the scratch counter
# --------------------------------------------------------------------------
print("\n== eighth mutation: :8435 -> :84350, scored in a scratch counter copy ==", flush=True)
git("checkout", "-f", "-B", "mut08-84350", BASE)
text = cap(["git", "-C", CLONE, "show", f"{BASE}:LOG.md"]).stdout
if not text.endswith("\n"):
    text += "\n"
block = LOG_BLOCK.replace(":8435", ":84350")
with open(os.path.join(CLONE, "LOG.md"), "w", encoding="utf-8") as fh:
    fh.write(text + "\n" + block)
git("add", "-A")
git("-c", "user.name=R73M01", "-c", "user.email=r73m01@scratch.invalid",
    "-c", "commit.gpgsign=false", "commit", "-q", "-m", "mut08-84350: kill line named :84350")
tip8 = cap(["git", "-C", CLONE, "rev-parse", "HEAD"]).stdout.strip()
print(f"mutant tip: {tip8}", flush=True)
numstat = cap(["git", "-C", CLONE, "diff", "--numstat", BASE, tip8, "--", "LOG.md"]).stdout
sys.stdout.write(numstat)
sh(f"git -C {CLONE} show {tip8}:LOG.md | grep -n '8435'")
sh(f"grep -c '8435' <(git -C {CLONE} show {tip8}:LOG.md)  # substring membership")
cp = sh(f"python3 -B {SCRATCH_COUNTER} --lane {CLONE} --rev {tip8} --base {BASE}; echo EXIT=$?")
mdir = os.path.join(OUT, "mutants", "mut08-84350")
os.makedirs(mdir, exist_ok=True)
with open(os.path.join(mdir, "counter.txt"), "w", encoding="utf-8") as fh:
    fh.write(cp.stdout)

# in-memory scoring of the candidate mutations against the frozen check()
spec = importlib.util.spec_from_file_location("c2count", SCRATCH_COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

print("\n== in-memory candidate matrix (fixture, frozen check()) ==", flush=True)
base_res = mod.check(dict(mod.FIXTURE), {}, set())
print("fixture baseline fails=" + repr([c for c, ok, _ in base_res if not ok]), flush=True)

CANDIDATES = [
    ("A heading-with-trailing-space (replace)", lambda f: f.__setitem__(
        "LOG.md", f["LOG.md"].replace(mod.LOG_HEAD, mod.LOG_HEAD + " "))),
    ("B heading appearing twice", lambda f: f.__setitem__(
        "LOG.md", f["LOG.md"] + "\n" + mod.LOG_HEAD + "\n\n- tools/research-gate.sh:8426 8435 set-e-exempt\n")),
    ("C uppercase EXEMPT", lambda f: f.__setitem__(
        "LOG.md", f["LOG.md"].replace("set-e-exempt", "set-e-EXEMPT"))),
    ("D :8435 -> :84350", lambda f: f.__setitem__(
        "LOG.md", f["LOG.md"].replace(":8435", ":84350"))),
    ("E curly apostrophe in tree phrase", lambda f: f.__setitem__(
        "corpus/lessons/round-72.md", f["corpus/lessons/round-72.md"].replace("verdicts tree", "verdict\u2019s tree"))),
    ("F :8426 -> :84260 (same class as D)", lambda f: f.__setitem__(
        "LOG.md", f["LOG.md"].replace(":8426", ":84260"))),
]
for label, fn in CANDIDATES:
    files = dict(mod.FIXTURE)
    deleted, changed = {}, set()
    fn(files, deleted, changed)
    res = mod.check(files, deleted, changed)
    fails = [(cid, det) for cid, ok, det in res if not ok]
    print(f"{label}: fails={len(fails)} -> " + ("; ".join(f"{c}:{d}" for c, d in fails) if fails else "NONE (survives)"),
          flush=True)

# decompose mut07: the same compliant content scored with an empty deleted/changed
print("\n== mut07 decomposition: identical text, two loaders ==", flush=True)
m7files = {
    "LOG.md": cap(["git", "-C", CLONE, "show", f"{BASE}:LOG.md"]).stdout + "\n" + LOG_BLOCK,
    "corpus/lessons/round-72.md": cap(["git", "-C", CLONE, "show", f"{BASE}:corpus/lessons/round-72.md"]).stdout + "\n" + LESSON_BLOCK,
    "SCORECARD.md": cap(["git", "-C", CLONE, "show", f"{BASE}:SCORECARD.md"]).stdout + "\n" + CARD_BLOCK,
}
res7 = mod.check(m7files, {}, set())
print("in-memory (deleted={}, changed={}): " + f"{sum(1 for _, ok, _ in res7 if ok)}/{len(res7)} "
      + repr([c for c, ok, _ in res7 if not ok]), flush=True)
for cid, ok, det in res7:
    print(f"  CHECK {cid} {'PASS' if ok else 'FAIL'} {det}")
print("\nDONE", flush=True)
