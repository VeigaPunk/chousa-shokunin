import subprocess, sys, os
def run(script, root, repo, work):
    p = subprocess.run([sys.executable, "-B", script, "--root", root, "--repo", repo, "--work", work],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr
root = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/wt"
repo = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
work = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/work"
orig = os.path.join(root, "corpus/evidence/round87/gate-records-r87.py")
src = open(orig, encoding="utf-8").read()
variants = {}
variants["E1_narrow_both_to_1"] = src.replace("    return len(seen)", "    return (min(len(seen), 1) if seen else 0)").replace(
    "for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root):",
    "for sid, url, key, fetched, tier, h, quote, _http in _qualifying_203(root)[:1]:").replace(
    "for sid, url, _key, fetched, tier, _h, _quote, http in _qualifying_203(root):",
    "for sid, url, _key, fetched, tier, _h, _quote, http in _qualifying_203(root)[:1]:").replace(
    "d1_expected >= 3", "d1_expected >= 1")
variants["E2_tautology_D1"] = src.replace('("D1_REFUSED", bool(d1) and d1_refused == len(d1), f"{d1_refused}/{len(d1)}")',
                 '("D1_REFUSED", True, f"{d1_refused}/{len(d1)}")')
variants["E3_forged_always_true"] = src.replace('("FORGED", refused == total_forged,', '("FORGED", True,').replace(
    '("CODES", exp == total_forged,', '("CODES", True,')
variants["E4_setup_tautology"] = src.replace('("SETUP", setup_ok == 1, f"{setup_ok}/1")', '("SETUP", True, f"{setup_ok}/1")')
variants["E5_mut_credit_without_run"] = src.replace('mut_admit_killed = 1 if (pos_ok and accepts == len(d1) and d1) else 0',
                 'mut_admit_killed = 1')
variants["E6_positive_tautology"] = src.replace('("POSITIVE", p_ok == len(pos) and bool(pos),', '("POSITIVE", True,')
# E7: no-op tautology everywhere: all legs True
v7 = src
for old,new in [
  ('("POSITIVE", p_ok == len(pos) and bool(pos),', '("POSITIVE", True,'),
  ('("FRESH", fresh_ok == 5 and not fresh_err,', '("FRESH", True,'),
  ('("FORGED", refused == total_forged,', '("FORGED", True,'),
  ('("CODES", exp == total_forged,', '("CODES", True,'),
  ('("EMPTY", e_ok == 1,', '("EMPTY", True,'),
  ('("RC", rc_ok == 4,', '("RC", True,'),
  ('("SETUP", setup_ok == 1,', '("SETUP", True,'),
  ('("D1_WIDTH", d1_expected >= 3 and len(d1) == d1_expected,', '("D1_WIDTH", True,'),
  ('("D1_REFUSED", bool(d1) and d1_refused == len(d1),', '("D1_REFUSED", True,'),
  ('("D2_WIDTH", d1_expected >= 3 and len(d2) == d1_expected,', '("D2_WIDTH", True,'),
  ('("D2_REFUSED", bool(d2) and d2_refused == len(d2),', '("D2_REFUSED", True,'),
  ('("MUT_ADMIT", mut_admit_derived == 1 and mut_admit_killed == 1,', '("MUT_ADMIT", True,'),
  ('("MUT_UNREACH", mut_unreach_derived == 1 and mut_unreach_killed == 1,', '("MUT_UNREACH", True,'),
  ('("DERIVE_NEG", derive_neg == 1,', '("DERIVE_NEG", True,'),
]:
    v7 = v7.replace(old, new)
variants["E7_all_tautology"] = v7
for name, code in variants.items():
    if code == src:
        print(f"{name}: NO-OP (edit did not apply)")
        continue
    p = os.path.join(root, "corpus/evidence/round87/", name + ".py")
    open(p, "w", encoding="utf-8").write(code)
    rc, out = run(p, root, repo, work)
    line = [l for l in out.splitlines() if "TOOL=present" in l or "GATE_RECORDS_R87" in l or "LEG_FAIL" in l]
    print(f"=== {name} rc={rc} ===")
    print("\n".join(line) if line else out[-500:])
    open(f"/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/{name}.txt", "w").write(out)
