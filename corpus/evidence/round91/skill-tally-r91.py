#!/usr/bin/env python3
"""skill-tally-r91 — the round-91 C3 (freshness) counting check. Successor of skill-tally-r90.py.

Round 90 bound the nine `SKILL.md` Case tallies to the tool's own verdict line (283 cases, 0 skipped). Its non-author
spot-check (`corpus/lessons/round-90-verifier-spotcheck.md`, routed defect 3) left the case-RANGE prose unbound:
the Gates row said `r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283`. The tool's own `ok-case`
names in that range are

    273 pin-bashenv-echo   274 drift-bashenv-echo   275 pin-bashenv-root
    276 pin-env-fn-echo-scrub  277 pin-env-fn-suppress  278 pin-env-fn-root
    279 env-pin-override-missing  280 env-pin-override-fake  281 pin-bash-path-shim
    282 bash-pin-override-missing  283 bash-pin-override-fake

so six of the indices the prose labels `bash-pin-override` (276–281) carry other names. A case label is a fact about
the runnable surface; this check derives the labelled families from the tool's own case names and requires the prose
to name exactly those indices.

Legs:
  1 TALLY      every current tally row equals the tool's verdict counts (r90's leg)
  2 CASE-RANGE the `r39 bash-pin` range equals the indices whose case name carries `bashenv`, and the
               `bash-pin-override` range equals the indices whose case name starts with `bash-pin-override`;
               `MISLABELED` counts claimed indices whose name is not in the family

Usage: python3 -B corpus/evidence/round91/skill-tally-r91.py --root DIR [--selftest FILE]
Exit 0 both legs hold (and at least one tally row exists), 1 a stale tally or a mislabelled range, 2 setup
(missing SKILL.md, missing/unparseable selftest output, or no verdict line).
"""
import argparse
import os
import re
import subprocess
import sys

VERDICT_RE = re.compile(r"^RESEARCH_GATE_SELFTEST: PASS \((\d+) cases, (\d+) skipped\)$", re.M)
TALLY_RE = re.compile(r"PASS \((\d+) cases, (\d+) skipped\)")
CASE_RE = re.compile(r"^ok-case\s+(\d+)\s+(\S+)\s+exit=", re.M)
BASHENV_RE = re.compile(r"r39 bash-pin cases (\d+)[\u2013-](\d+)")
OVERRIDE_RE = re.compile(r"bash-pin-override cases (\d+)[\u2013-](\d+)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--selftest", help="captured selftest output; omitted means run the tool")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    skill = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill):
        print(f"SKILL_TALLY_R91=SETUP missing {skill}")
        return 2
    if a.selftest:
        if not os.path.isfile(a.selftest):
            print(f"SKILL_TALLY_R91=SETUP missing selftest receipt {a.selftest}")
            return 2
        out = open(a.selftest, encoding="utf-8", errors="replace").read()
        rc = 0
    else:
        p = subprocess.run(["bash", "tools/research-gate.sh", "--selftest"], cwd=root,
                           capture_output=True, text=True)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    m = VERDICT_RE.search(out)
    if not m:
        print(f"SKILL_TALLY_R91=SETUP no verdict line (selftest rc={rc})")
        return 2
    cases, skipped = int(m.group(1)), int(m.group(2))
    names = [(int(n), name) for n, name in CASE_RE.findall(out)]
    if not names:
        print("SKILL_TALLY_R91=SETUP no ok-case lines in the selftest output")
        return 2
    text = open(skill, encoding="utf-8", errors="replace").read()

    def current(line):
        lead = line.lstrip()
        return lead.startswith("| `research-gate") or "Selftest `PASS (" in line

    rows, other = [], 0
    for ln in text.splitlines():
        for mm in TALLY_RE.finditer(ln):
            if current(ln):
                rows.append((mm.group(1), mm.group(2)))
            else:
                other += 1
    stale = [(n, s) for n, s in rows if (int(n), int(s)) != (cases, skipped)]
    if not rows:
        print("SKILL_TALLY_R91=FAIL no tally row in SKILL.md")
        return 1
    for n, s in stale:
        print(f"STALE_TALLY PASS ({n} cases, {s} skipped) != tool {cases}/{skipped}")

    # 2. case-range prose against the tool's own case names
    bashenv = [n for n, name in names if "bashenv" in name]
    bashpin = [n for n, name in names if name.startswith("bash-pin-override")]
    mb = BASHENV_RE.search(text)
    mo = OVERRIDE_RE.search(text)
    range_codes = []
    if not mb:
        range_codes.append("CLAUSE_MISSING:r39-bash-pin")
    if not mo:
        range_codes.append("CLAUSE_MISSING:bash-pin-override")
    claimed_env = (int(mb.group(1)), int(mb.group(2))) if mb else None
    claimed_ovr = (int(mo.group(1)), int(mo.group(2))) if mo else None
    derived_env = (min(bashenv), max(bashenv)) if bashenv else None
    derived_ovr = (min(bashpin), max(bashpin)) if bashpin else None
    if claimed_env is not None and derived_env is not None and claimed_env != derived_env:
        range_codes.append(f"RANGE_MISMATCH:bashenv claimed={claimed_env[0]}-{claimed_env[1]} "
                           f"derived={derived_env[0]}-{derived_env[1]}")
    if claimed_ovr is not None and derived_ovr is not None and claimed_ovr != derived_ovr:
        range_codes.append(f"RANGE_MISMATCH:bash-pin-override claimed={claimed_ovr[0]}-{claimed_ovr[1]} "
                           f"derived={derived_ovr[0]}-{derived_ovr[1]}")
    mislabeled = []
    if claimed_ovr is not None and derived_ovr is not None:
        mislabeled = [n for n in range(claimed_ovr[0], claimed_ovr[1] + 1) if n not in bashpin]
    ok_ranges = not range_codes and claimed_env == derived_env and claimed_ovr == derived_ovr
    for code in range_codes:
        print(f"CASE_RANGE_FINDING {code}")
    if mislabeled:
        print(f"CASE_RANGE_FINDING MISLABELED={len(mislabeled)} indices={','.join(map(str, mislabeled))}")
    tally_ok = not stale
    print(f"TALLY_ROWS={len(rows)} STALE_TALLIES={len(stale)}/{len(rows)} "
          f"EXPECTED_CASES={cases} EXPECTED_SKIPPED={skipped} OTHER_OCCURRENCES={other} "
          f"CASE_RANGE_BASHENV={'%d-%d' % derived_env if derived_env else 'none'} "
          f"CASE_RANGE_BASH_PIN={'%d-%d' % derived_ovr if derived_ovr else 'none'} "
          f"CASE_RANGE_OK={int(claimed_env == derived_env) + int(claimed_ovr == derived_ovr)}/2 "
          f"MISLABELED={len(mislabeled)} LEGS={int(tally_ok) + int(ok_ranges)}/2")
    passed = tally_ok and ok_ranges
    if not tally_ok:
        print("LEG_FAIL TALLY")
    if not ok_ranges:
        print("LEG_FAIL CASE-RANGE")
    print(f"SKILL_TALLY_R91={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
