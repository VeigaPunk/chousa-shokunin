#!/usr/bin/env python3
"""skill-tally-r94 — the round-94 C3 (freshness) counting check. Successor of skill-tally-r93.py.

Round 94 binds the tail set to the section that owns each tally: r93 declared the tail multiset
(`{215:1, 283:1}`) over everything after `## Gates`, so a tally MOVED between two tail sections — same
count, same file — still printed `TAIL_OK=1`. Each declaration now names the exact substring of the
nearest preceding heading the tally must sit under (`TAIL_OWNED`), a moved tally fires
`TAIL_OWNER_MISMATCH`, and `TAIL_OWNED_OK` counts declarations whose occurrences all sit under their own
heading. The rest of the instrument (legs 1–4, the historical derivation, the case-range leg) is r93's.

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

Usage: python3 -B corpus/evidence/round94/skill-tally-r94.py --root DIR [--selftest FILE]
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
        print(f"SKILL_TALLY_R94=SETUP missing {skill}")
        return 2
    if a.selftest:
        if not os.path.isfile(a.selftest):
            print(f"SKILL_TALLY_R94=SETUP missing selftest receipt {a.selftest}")
            return 2
        out = open(a.selftest, encoding="utf-8", errors="replace").read()
        rc = 0
    else:
        p = subprocess.run(["bash", "tools/research-gate.sh", "--selftest"], cwd=root,
                           capture_output=True, text=True)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    m = VERDICT_RE.search(out)
    if not m:
        print(f"SKILL_TALLY_R94=SETUP no verdict line (selftest rc={rc})")
        return 2
    cases, skipped = int(m.group(1)), int(m.group(2))
    names = [(int(n), name) for n, name in CASE_RE.findall(out)]
    # A3: the case enumeration itself is pinned. The tool does not print `exit=` on every case
    # (six `accepted=` lines, cases 196-200 and 223), so count ALL `^ok-case <n> <name>` lines.
    all_case_lines = re.findall(r"^ok-case\s+(\d+)\s+(\S+)", out, re.M)
    if len(all_case_lines) != cases or len({int(n) for n, _name in all_case_lines}) != cases:
        print(f"SKILL_TALLY_R94=FAIL case enumeration {len(all_case_lines)} lines, "
              f"{len({int(n) for n, _name in all_case_lines})} distinct numbers, against verdict {cases} cases")
        return 1
    if not names:
        print("SKILL_TALLY_R94=SETUP no ok-case lines in the selftest output")
        return 2
    text = open(skill, encoding="utf-8", errors="replace").read()

    # T1: scope the tally and case-range searches to the `## Gates` section (up to the next ATX heading
    # of depth <= 2 at column 0; a `# ` or `## ` heading terminates; anything else is not a boundary,
    # and an unterminated scope is a SCOPE_BLEED setup diagnostic, never a silent EOF bleed).
    gates_start = text.find("## Gates")
    gates_text = ""
    gates_end = None
    if gates_start >= 0:
        m_end = re.search(r"\n#{1,2} ", text[gates_start + 1:])
        if m_end:
            gates_end = gates_start + 1 + m_end.start()
            gates_text = text[gates_start:gates_end]
        else:
            print("SKILL_TALLY_R94=SETUP SCOPE_BLEED no next-## or #-level heading after ## Gates")
            return 2
    if not gates_text or gates_end is None:
        print("SKILL_TALLY_R94=SETUP no ## Gates section in SKILL.md")
        return 2

    def current(line):
        lead = line.lstrip()
        return lead.startswith("| `research-gate") or "Selftest `PASS (" in line

    rows, other = [], 0
    for ln in gates_text.splitlines():
        for mm in TALLY_RE.finditer(ln):
            if current(ln):
                rows.append((mm.group(1), mm.group(2)))
            else:
                other += 1
    stale = [(n, s) for n, s in rows if (int(n), int(s)) != (cases, skipped)]
    # T2 (round 93): the historical (non-current) tally multiset is DERIVED from the committed receipts
    # that ground each tally, never frozen as a literal pair. Each entry names the receipt file and the
    # exact located quote; a missing receipt, a missing quote or a tally absent from the Gates scope all
    # change the verdict, so deleting a historical tally can no longer leave the counter green.
    HIST_SOURCES = (
        (("161", "0"), "corpus/evidence/round25-final-measure.log", "PASS (161 cases, 0 skipped)"),
        (("256", "0"), "corpus/evidence/round34/audit-dispositions.md", "PASS (256 cases, 0 skipped)"),
    )
    other_counts = {}
    for ln in gates_text.splitlines():
        for mm in TALLY_RE.finditer(ln):
            if not current(ln):
                other_counts[(mm.group(1), mm.group(2))] = other_counts.get((mm.group(1), mm.group(2)), 0) + 1
    declared = {tally: 1 for tally, _r, _q in HIST_SOURCES}
    hist_codes = []
    hist_derived = 0
    for tally, receipt, quote in HIST_SOURCES:
        path = os.path.join(root, receipt)
        if not os.path.isfile(path):
            hist_codes.append(f"HIST_UNGROUNDED {tally[0]} receipt={receipt}")
            continue
        if quote not in open(path, encoding="utf-8", errors="replace").read():
            hist_codes.append(f"HIST_UNGROUNDED {tally[0]} quote={quote!r} receipt={receipt}")
            continue
        hist_derived += 1
    hist_present = sum(1 for tally, _r, _q in HIST_SOURCES if other_counts.get(tally, 0) >= 1)
    for tally, receipt, _q in HIST_SOURCES:
        if other_counts.get(tally, 0) < 1:
            hist_codes.append(f"HIST_MISSING {'PASS (' + tally[0] + ' cases, ' + tally[1] + ' skipped)'}")
    others_ok = other_counts == declared and not hist_codes
    # T3 (round 93): tallies outside the Gates scope are enumerated, not ignored: the declared tail set
    # is the one r92 measured (`215` in the Round27 subsection) and an undeclared tail tally is a
    # boundary finding, so a tally that drifts out of the section can no longer hide at the tail.
    # Two tail tallies are declared today: SKILL.md:640 (the Round27 215-case checkpoint) and
    # SKILL.md:781 (the 283-case host line). Both sit outside the Gates scope by design; an
    # undeclared third one is the boundary finding.
    # The head (everything before `## Gates`) is scanned too: r92's wording claimed "outside the Gates scope"
    # while only the tail was read, so a tally planted above the section was silently accepted (R93ReviewerC3 F2).
    HEAD_DECLARED = {}
    head_counts = {}
    for ln in text[:gates_start].splitlines():
        for mm in TALLY_RE.finditer(ln):
            head_counts[(mm.group(1), mm.group(2))] = head_counts.get((mm.group(1), mm.group(2)), 0) + 1
    head_ok = head_counts == HEAD_DECLARED
    for tally in sorted(set(head_counts) - set(HEAD_DECLARED)):
        print(f"HIST_SCOPE_BLEED head line={tally[0]} cases tally=PASS ({tally[0]} cases, {tally[1]} skipped)")
    TAIL_DECLARED = {("215", "0"): 1, ("283", "0"): 1}
    # Round 94: the tail set is bound to the section that owns each tally. r93 declared the multiset only,
    # so a tally MOVED between two tail sections (same count, same file) still printed TAIL_OK=1. Each
    # entry below names the exact substring of the nearest preceding heading the tally must sit under.
    TAIL_OWNED = (
        (("215", "0"), 1, "Round27 repair/status correction"),
        (("283", "0"), 1, "Round 37 — the claim-pin provenance"),
    )
    tail_counts = {}
    tail_owners = {}
    heading = "<none>"
    for ln in text[gates_end:].splitlines():
        if re.match(r"^#{1,6} ", ln):
            heading = ln.strip()
        for mm in TALLY_RE.finditer(ln):
            key = (mm.group(1), mm.group(2))
            tail_counts[key] = tail_counts.get(key, 0) + 1
            tail_owners.setdefault(key, []).append(heading)
    owner_codes = []
    owned_ok = 0
    for tally, count, owner in TAIL_OWNED:
        seen = tail_owners.get(tally, [])
        if len(seen) != count:
            owner_codes.append(f"TAIL_OWNER_COUNT tally={tally[0]} observed={len(seen)} declared={count}")
        for h in seen:
            if owner not in h:
                owner_codes.append(f"TAIL_OWNER_MISMATCH tally={tally[0]} cases tally=PASS "
                                   f"({tally[0]} cases, {tally[1]} skipped) owner={h} declared={owner}")
        if len(seen) == count and all(owner in h for h in seen):
            owned_ok += 1
    tail_ok = tail_counts == TAIL_DECLARED and head_ok and not owner_codes
    for tally in sorted(set(tail_counts) - set(TAIL_DECLARED)):
        print(f"HIST_SCOPE_BLEED line={tally[0]} cases tally=PASS ({tally[0]} cases, {tally[1]} skipped)")
    if not rows:
        print("SKILL_TALLY_R94=FAIL no tally row in SKILL.md")
        return 1
    for n, s in stale:
        print(f"STALE_TALLY PASS ({n} cases, {s} skipped) != tool {cases}/{skipped}")
    for code in hist_codes:
        print(f"HIST_FINDING {code}")
    for code in owner_codes:
        print(f"TAIL_OWNER_FINDING {code}")
    if hist_derived != len(HIST_SOURCES):
        print(f"HIST_DERIVED={hist_derived}/{len(HIST_SOURCES)}")


    # 2. case-range prose against the tool's own case names
    # The family population is EVERY `ok-case` line, not only the ones that print `exit=` (the six
    # `accepted=` lines carry no exit=, so the exit= regex silently excluded them — R93ReviewerC3 F3).
    names_all = [(int(n), name) for n, name in all_case_lines]
    bashenv = [n for n, name in names_all if "bashenv" in name]
    bashpin = [n for n, name in names_all if name.startswith("bash-pin-override")]
    mb = BASHENV_RE.search(gates_text)
    mo = OVERRIDE_RE.search(gates_text)
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
    # Interior holes and foreign names: the claimed range must be exactly the family's index set, for BOTH
    # ranges (r92 checked endpoints only, and only the override family — R93ReviewerC3 F3).
    mislabeled = []
    for claimed, family in ((claimed_env, bashenv), (claimed_ovr, bashpin)):
        if claimed is None:
            continue
        mislabeled += [n for n in range(claimed[0], claimed[1] + 1) if n not in set(family)]
    interior_ok = True
    for claimed, family in ((claimed_env, bashenv), (claimed_ovr, bashpin)):
        if claimed is None or not family:
            interior_ok = False
            continue
        interior_ok = interior_ok and set(range(claimed[0], claimed[1] + 1)) == set(family)
    ok_ranges = (not range_codes and claimed_env == derived_env and claimed_ovr == derived_ovr
                 and not mislabeled and interior_ok)
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
          f"MISLABELED={len(mislabeled)} "
          f"HIST_DERIVED={hist_derived}/{len(HIST_SOURCES)} HIST_PRESENT={hist_present}/{len(HIST_SOURCES)} "
          f"TAIL_TALLIES={sum(tail_counts.values())} TAIL_OWNED_OK={owned_ok}/{len(TAIL_OWNED)} "
          f"OTHERS_OK={int(others_ok)} TAIL_OK={int(tail_ok)} "
          f"LEGS={int(tally_ok) + int(ok_ranges) + int(others_ok) + int(tail_ok)}/4")
    passed = tally_ok and ok_ranges and others_ok and tail_ok
    if not tally_ok:
        print("LEG_FAIL TALLY")
    if not ok_ranges:
        print("LEG_FAIL CASE-RANGE")
    if not others_ok:
        print(f"LEG_FAIL OTHERS declared={declared} observed={other_counts} codes={','.join(hist_codes) or 'none'}")
    if not tail_ok:
        print(f"LEG_FAIL TAIL declared={TAIL_DECLARED} observed={tail_counts}")
    print(f"SKILL_TALLY_R94={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
