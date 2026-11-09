import subprocess, sys, os, hashlib, shutil, json
S = "/fast/scratch/hyaku/chousa-r97/R97MutantsC2"
REPO = f"{S}/repo"
SCRIPT = "corpus/evidence/round97/entry-controls-r97.py"
ENTRY = "corpus/knowledge/press-checklist-questions-r97.md"
def sha(p):
    import hashlib
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
orig_script = sha(f"{REPO}/{SCRIPT}")
orig_entry = sha(f"{REPO}/{ENTRY}")
orig_src = open(f"{REPO}/{SCRIPT}", encoding="utf-8").read()
def run(work):
    p = subprocess.run([sys.executable, "-B", SCRIPT, "--root", ".", "--work", work],
                       cwd=REPO, capture_output=True, text=True)
    out = p.stdout.strip().splitlines()
    tail = out[-2:] if len(out)>=2 else out
    return p.returncode, " | ".join(tail)
MUTANTS = {
 # battery-source mutants: one-site edits to entry-controls-r97.py
 "M01-sole-drop": (
   "            if any(src[q] == \"S225\" for q in named):\n                sole_ok += 1",
   "            sole_ok += 1  # MUTANT: drop S225 test in SOLE_SUPPORT"),
 "M02-norm-identity": (
   "    s = s.replace(\"\\u2019\", \"'\").replace(\"\\u2018\", \"'\").replace(\"\\u201c\", '\"').replace(\"\\u201d\", '\"')\n    return \" \".join(s.split())",
   "    return s  # MUTANT: norm->identity"),
 "M03-letters-punct": (
   "    return re.sub(r\"[^a-z0-9]\", \"\", s.lower())",
   "    return s.lower()  # MUTANT: letters keeps punctuation"),
 "M04-oneline-wholetext": (
   "    return sum(1 for s_, q in rows if s_ in lines and any(q in ln for ln in lines[s_])), len(rows)",
   "    whole = {k: \"\\n\".join(v) for k, v in lines.items()}\n    return sum(1 for s_, q in rows if s_ in whole and q in whole[s_]), len(rows)  # MUTANT: whole-text"),
 "M05-stated-loose": (
   "    return (int(m.group(1)), int(m.group(3)), int(m.group(2))) if m and m.group(2) == m.group(4) else None",
   "    return (int(m.group(1)), int(m.group(3)), 999) if m else None  # MUTANT: stated ignores denominators"),
 "M06-corr-noop": (
   "        forged = text.replace(f\"verbatim {cv}/{cn}\", f\"verbatim {cv + 2}/{cn}\", 1)\n        c_neg = forged != text and stated(forged) != (cv, cl, cn)",
   "        forged = text.replace(f\"verbatim {cv}/{cn}\", f\"verbatim {cv + 2}/{cn}\", 1)\n        c_neg = True  # MUTANT: corroboration forgery no-op"),
 "M07-g5-code-swap": (
   "            (\"g5-tier\", first26, first26.replace(\"tier=C\", \"tier=B\"), \"TIER\"),",
   "            (\"g5-tier\", first26, first26.replace(\"tier=C\", \"tier=B\"), \"NOTACODE\"),  # MUTANT: expected code swapped"),
 "M08-g1-code-swap": (
   "            (\"g1-word\", rec_with(q20), rec_with(q20).replace(\"for example, the use\", \"e.g., the use\"), \"QUOTE_ABSENT\"),",
   "            (\"g1-word\", rec_with(q20), rec_with(q20).replace(\"for example, the use\", \"e.g., the use\"), \"TIER\"),  # MUTANT: expected code swapped"),
 "M09-binding-terms-off": (
   "            if words(cells[1]) & quote_words:\n                terms_ok += 1",
   "            if True:  # MUTANT: terms check always passes\n                terms_ok += 1"),
 "M10-searches-off": (
   "        s_pos = rc == 0 and f\"searches={N_SEARCHES} rev_match={N_SEARCHES}/{N_SEARCHES}\" in out \\\n            and \"SEARCH_RERUN: CLEAN\" in out",
   "        s_pos = True  # MUTANT: searches-positive forced"),
 "M11-pos-gate-off": (
   "        pos = g_ok and m_ok and lq_ok and nrows > 0 and w_ok == terms_ok == lane_ok == sole_ok == nrows and one == n_one",
   "        pos = True  # MUTANT: positive forced"),
 "M12-words-threshold": (
   "    return {w for w in re.findall(r\"[a-z]+\", s.lower()) if len(w) >= 5 and w not in STOP}",
   "    return {w for w in re.findall(r\"[a-z]+\", s.lower()) if len(w) >= 1 and w not in STOP}  # MUTANT: threshold 5->1"),
 "M13-lq-fuzzy": (
   "    for q in lq.values():\n        if q in pool:\n            pool.remove(q)\n            bound += 1",
   "    for q in lq.values():\n        if any(q[:10] in p for p in pool):  # MUTANT: fuzzy LQ_BOUND (first 10 chars)\n            pool.remove(next(p for p in pool if q[:10] in p))\n            bound += 1"),
 "M14-corr-verbatim-off": (
   "    return sum(norm(q) in nv for q in qs), sum(letters(q) in nl for q in qs), len(qs)",
   "    return len(qs), sum(letters(q) in nl for q in qs), len(qs)  # MUTANT: verbatim always full"),
}
results = {}
os.makedirs(f"{S}/receipts", exist_ok=True)
for name, (old, new) in MUTANTS.items():
    assert orig_src.count(old) == 1, f"{name}: anchor count {orig_src.count(old)}"
    mutated = orig_src.replace(old, new, 1)
    open(f"{REPO}/{SCRIPT}", "w", encoding="utf-8").write(mutated)
    mhash = sha(f"{REPO}/{SCRIPT}")
    rc, tail = run(f"{S}/w-{name}")
    # restore exact bytes
    open(f"{REPO}/{SCRIPT}", "w", encoding="utf-8").write(orig_src)
    rhash = sha(f"{REPO}/{SCRIPT}")
    killed = (rc == 1) or ("ENTRY_CONTROLS=FAIL" in tail) or ("SETUP" in tail)
    results[name] = dict(rc=rc, tail=tail, killed=killed, restored=(rhash==orig_script), mutant_hash=mhash[:12])
    print(f"{name}: rc={rc} killed={killed} restored={rhash==orig_script} :: {tail[-80:]}", flush=True)
json.dump(dict(orig_script=orig_script, orig_entry=orig_entry, results=results),
          open(f"{S}/receipts/mutant-results.json","w"), indent=1)
print("ALL_DONE")
