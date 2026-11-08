import subprocess, sys, os, textwrap, hashlib
def run(script, root, repo, work, extra=[]):
    p = subprocess.run([sys.executable, "-B", script, "--root", root, "--repo", repo, "--work", work] + extra,
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr

root = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/tree-pristine"
repo = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
work = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/work"
orig = os.path.join(root, "corpus/evidence/round87/gate-records-r87.py")
src = open(orig, encoding="utf-8").read()

# Probe 1: counter edit that keeps all 15 appends, breaks duty: make a leg always True
# Keep legs count identical; flip D1_REFUSED leg to always True, or better: keep appends but gut computation
variants = {}

# (b) NARROWED builder kept in sync: patch count_203_rows to also return 1-row so width leg passes while class is 1
# The predicate's D1_EXPECTED=3 would fail... but our job: see if LEGS stays 15/15 with broken duty
# Test E1: mutate D1 leg: replace `d1_refused == len(d1)` with `d1_refused == 1` and builder returns 1 row
v1 = src.replace(
    'for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root):\n        out.append((sid, f\'GATE-RECORD {sid} url={url} fetched={fetched} tier={tier} decision=admit \'',
    'for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root)[: 1 if False else 1]:\n        out.append((sid, f\'GATE-RECORD {sid} url={url} fetched={fetched} tier={tier} decision=admit \''
)
# Actually for E1 we need both builder truncated and counter truncated: simpler - truncate both
v1 = src.replace("for sid, url, _key, fetched, tier, _h, _quote, http in _qualifying_203(root):",
                 "for sid, url, _key, fetched, tier, _h, _quote, http in _qualifying_203(root)[:1]:").replace(
                 "for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root):",
                 "for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root)[:1]:")
# Also patch count_203_rows to return 1: early return after first
# Replace `return len(seen)` with `return min(len(seen), 1) if seen else 0`
v1 = v1.replace("    return len(seen)", "    return (min(len(seen), 1) if seen else 0)")
# Patch the floor so width passes with 1: `d1_expected >= 3` -> `d1_expected >= 1`
v1 = v1.replace("d1_expected >= 3", "d1_expected >= 1")
# The predicate also demands D1_EXPECTED=3 in printed line; that is checked by external auditor, but instrument legs pass.
# But claim's predicate checks D1_EXPECTED=3? Check: predicate requires D1_EXPECTED=3 field. If auditor checks printed value, still fails because 1 != 3. However instrument internal passed stays True.
# Our probe tests internal passed.
variants["E1_narrow_both_to_1"] = v1

# (b2) Counter edit that keeps all 15 appends and still passes with broken duty:
# Break the mutant kill leg: make MUT_ADMIT leg always True by `mut_admit_killed = 1` hardcoded, but keep derived from bytes? No - do: gut the run check.
# Replace the kill computation with constant 1 - misreporting class (named limit). But we need something NOT in that class: keep appends, break computation silently.
# E2: refuse counting: D1_REFUSED leg: `bool(d1) and d1_refused == len(d1)` -> `True`
v2 = src.replace('("D1_REFUSED", bool(d1) and d1_refused == len(d1), f"{d1_refused}/{len(d1)}")',
                 '("D1_REFUSED", True, f"{d1_refused}/{len(d1)}")')
variants["E2_tautology_D1"] = v2

# E3: break the forge run: make forged loop skip D1/D2 by removing those appends but add a dummy leg to keep count? Instead break FORGED determination: replace `refused == total_forged` with True
v3 = src.replace('("FORGED", refused == total_forged,', '("FORGED", True,')
v3 = v3.replace('("CODES", exp == total_forged,', '("CODES", True,')
variants["E3_forged_always_true"] = v3

# E4: kept 15 appends, broken SETUP duty (M5 shape): drop `setup_ok == 1` equivalent -> SETUP leg always True
v4 = src.replace('("SETUP", setup_ok == 1, f"{setup_ok}/1")', '("SETUP", True, f"{setup_ok}/1")')
variants["E4_setup_tautology"] = v4

# E5: mutant credited without run (M2 shape) but keep append: replace `mut_admit_derived == 1 and mut_admit_killed == 1` computation by hardcode 1
v5 = src.replace('mut_admit_killed = 1 if (pos_ok and accepts == len(d1) and d1) else 0',
                 'mut_admit_killed = 1  # M2 mutant: credited without run, append kept')
variants["E5_mut_credit_without_run"] = v5

# E6: break POSITIVE duty but keep print: `p_ok == len(pos)` -> True
v6 = src.replace('("POSITIVE", p_ok == len(pos) and bool(pos),', '("POSITIVE", True,')
variants["E6_positive_tautology"] = v6

for name, code in variants.items():
    if code == src:
        print(f"{name}: NO-OP (edit did not apply)")
        continue
    p = os.path.join("/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/work", name + ".py")
    open(p, "w", encoding="utf-8").write(code)
    rc, out = run(p, root, repo, "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/work")
    line = [l for l in out.splitlines() if "TOOL=present" in l or "GATE_RECORDS_R87" in l or "LEG_FAIL" in l]
    print(f"=== {name} rc={rc} ===")
    print("\n".join(line))
    open(f"/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/{name}.txt", "w").write(out)
