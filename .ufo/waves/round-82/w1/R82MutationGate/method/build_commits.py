#!/usr/bin/env python3
"""Build one commit per frozen-counter mutant in the landing fixture repo."""
import json
import os
import subprocess

REPO = "/fast/scratch/hyaku/chousa-r82/R82MutationGate/repo38"
PRISTINE = "04bff4f90173f00bc9f7220f7f244cf479f4fd80"
OUT = "/fast/scratch/hyaku/chousa-r82/R82MutationGate/counter-mutants38.json"

K2 = "corpus/evidence/round82/k2-gate-r82.py"
DP = "corpus/evidence/round82/depth-r82.py"

MUTANTS = [
    # ---- k2-gate-r82.py (C1 counter) ----
    ("MK1-drop-FROZEN_RUNLINE", K2, "drop the FROZEN_RUNLINE equality check",
     "        if item in rl and rl[item] != FROZEN_RUNLINE[item]:",
     "        if False:  # mutant"),
    ("MK2-accept-rc2", K2, "accept rc 2 as a refusal",
     "            good = rc == 1 and need in seen",
     "            good = rc in (1, 2) and need in seen"),
    ("MK3-drop-verify-union", K2, "drop the verify-mode finding union on item-2 refusals",
     '        if item == 2 and expect == "refuse":',
     "        if False:  # mutant"),
    ("MK4-positive-only-PASS", K2, "PASS requires only the positive group to be full",
     "    full = nrl == 2 and all(ok[g] == tot[g] and tot[g] > 0 for g in GROUPS)",
     '    full = nrl == 2 and ok["positive"] == tot["positive"] and tot["positive"] > 0'),
    ("MK5-drop-CLEAN", K2, "drop the `RESEARCH_GATE: CLEAN` requirement on pass rows",
     '            good = rc == 0 and "RESEARCH_GATE: CLEAN" in out and need in out',
     "            good = rc == 0 and need in out"),
    ("MK6-refuse-rc-only", K2, "drop the finding-id requirement on refuse rows",
     "            good = rc == 1 and need in seen",
     "            good = rc == 1"),
    ("MK7-refuse-accepts-rc0", K2, "accept rc 0 as a refusal when the finding id is printed",
     "            good = rc == 1 and need in seen",
     "            good = rc in (0, 1) and need in seen"),
    ("MK8-drop-positive-group", K2, "drop the positive group from the PASS formula",
     "    full = nrl == 2 and all(ok[g] == tot[g] and tot[g] > 0 for g in GROUPS)",
     '    full = nrl == 2 and all(ok[g] == tot[g] and tot[g] > 0 for g in ("k2", "hold", "class"))'),
    ("MK9-one-runline-ok", K2, "accept PASS when only one Run line is found",
     "    full = nrl == 2 and all(ok[g] == tot[g] and tot[g] > 0 for g in GROUPS)",
     "    full = nrl >= 1 and all(ok[g] == tot[g] and tot[g] > 0 for g in GROUPS)"),
    # ---- depth-r82.py (C2 counter) ----
    ("MD1-drop-E3-capture", DP, "drop the E3 verbatim-in-capture location check",
     "            if not (8 <= n <= 25) or fr[src] is None or norm(qt) not in fr[src][1]:",
     "            if not (8 <= n <= 25) or fr[src] is None:"),
    ("MD2-drop-ROUND_START", DP, "drop the ROUND_START freshness floor from refetch rows",
     '        if len(f) != 9 or f[5] != "0" or not f[6].startswith("2") or f[4] < ROUND_START:',
     '        if len(f) != 9 or f[5] != "0" or not f[6].startswith("2"):'),
    ("MD3-drop-E6", DP, "drop E6 coverage",
     "        if len(sids) < 3 or any(fr.get(s) is None or s not in named_s for s in sids) or set(quotes) - named_q:",
     "        if False:  # mutant"),
    ("MD4-drop-E5", DP, "drop E5 content",
     '            if any(len(v.split()) < 3 or norm(v).lower().strip("`.") in PLACEHOLDERS for v in other) or joined in seen:',
     "            if False:  # mutant"),
    ("MD5-drop-E4", DP, "drop E4 novelty",
     "        if len(set(qn)) != len(qn) or any(q in base_norm for q in qn):",
     "        if False:  # mutant"),
    ("MD6-row-floor-1", DP, "lower the E1 body-row floor from 5 to 1",
     '        if not hdr or body is None or "warrant" not in hdr or len(body) < 5:',
     '        if not hdr or body is None or "warrant" not in hdr or len(body) < 1:'),
    ("MD7-drop-E7", DP, "drop E7 new-ground",
     "            if s in base_sids or (fr.get(s) and fr[s][0] in base_text):",
     "            if False:  # mutant"),
    ("MD8-drop-E2", DP, "drop E2 warrant-to-quote linkage",
     "            if not qs or any(q not in quotes or quotes[q][0] not in w for q in qs):",
     "            if False:  # mutant"),
    ("MD9-E5-drop-duplicate-half", DP, "drop only the E5 duplicate-row half",
     '            if any(len(v.split()) < 3 or norm(v).lower().strip("`.") in PLACEHOLDERS for v in other) or joined in seen:',
     '            if any(len(v.split()) < 3 or norm(v).lower().strip("`.") in PLACEHOLDERS for v in other):'),
    ("MD10-E5-drop-placeholder-half", DP, "drop only the E5 word-count/placeholder half",
     '            if any(len(v.split()) < 3 or norm(v).lower().strip("`.") in PLACEHOLDERS for v in other) or joined in seen:',
     "            if joined in seen:"),
    ("MD11-drop-warrant-column", DP, "drop the E1 `Warrant` column requirement",
     '        if not hdr or body is None or "warrant" not in hdr or len(body) < 5:',
     "        if not hdr or body is None or len(body) < 5:"),
]


def git(*args, **kw):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, **kw)


def main():
    cfg = ["-c", "user.email=mutation@local", "-c", "user.name=R82MutationGate"]
    out = []
    for mid, counter, desc, old, new in MUTANTS:
        pristine = subprocess.run(["git", "-C", REPO, "show", f"{PRISTINE}:{counter}"],
                                  capture_output=True, check=True).stdout
        text = pristine.decode()
        n = text.count(old)
        if n != 1:
            out.append({"id": mid, "error": f"anchor count={n}"})
            continue
        mutated = text.replace(old, new, 1).encode()
        with open(os.path.join(REPO, counter), "wb") as fh:
            fh.write(mutated)
        git("add", counter)
        c = git(*cfg, "commit", "-qm", f"mutant {mid}: {desc}")
        if c.returncode != 0:
            out.append({"id": mid, "error": c.stderr.strip()})
            continue
        sha = git("rev-parse", "HEAD").stdout.strip()
        # verify archived bytes at that commit carry the mutation
        arc = subprocess.run(["git", "-C", REPO, "show", f"{sha}:{counter}"],
                             capture_output=True, check=True).stdout
        assert arc == mutated, mid
        out.append({"id": mid, "counter": counter, "desc": desc,
                    "commit": sha, "mut_sha256": __import__("hashlib").sha256(mutated).hexdigest(),
                    "pristine_sha256": __import__("hashlib").sha256(pristine).hexdigest()})
        # restore pristine bytes for the next mutant
        with open(os.path.join(REPO, counter), "wb") as fh:
            fh.write(pristine)
        git("add", counter)
    git(*cfg, "commit", "-qm", "restore pristine counters after mutant commits",
        "-a") if git("status", "--porcelain").stdout.strip() else None
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    for r in out:
        print(r.get("id"), r.get("commit", r.get("error")), r.get("mut_sha256", ""))
    print("repo HEAD now", git("rev-parse", "HEAD").stdout.strip(),
          "clean:", not git("status", "--porcelain").stdout.strip())


if __name__ == "__main__":
    main()
