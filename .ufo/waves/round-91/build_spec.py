#!/usr/bin/env python3
"""Build the round-91 wave-1 spec (12 seats, policy v1 band 8-16). Constants are the measured revisions."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r91"
BASE = "265b8633b7e5d1da49da6fb948df9707373fb15c"
FREEZE = "4d00d7519290569879f853d7122b82a927cda1f3"
CARRIER = "67954adc599bd605705d94a1ea7abb582491a907"
SUPERSEDED = "160b658b / d02a950f and 37831ce8 / b8fc99a1"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 91, L1 ChousaR91 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-90 landing + its non-author spot-check); claim freeze F3 {FREEZE}; the tree you attack is
carrier C3 {CARRIER} (the freeze plus the six committed control receipts; the receipts pin {FREEZE}). An earlier
freeze/carrier pair ({SUPERSEDED}) were superseded before any scored run and before this wave — their defects are
recorded in {LANE}/plans/round-91.md §§Pre-wave freeze repair 1-2; treat F3/C3 as the freeze.
Frozen predicate set: {LANE}/corpus/evidence/round91/claims.md — read it FIRST, with every kill rule and every NAMED
LIMIT — and {LANE}/plans/round-91.md. Machine form: {LANE}/.ufo/waves/round-91/claims.json.
Three claims, three axes:
C1 operability (lowest scored, historical 3/10): `python3 -B corpus/evidence/round91/control-driver-r91.py verify --root .
--repo . --rev {FREEZE} --receipts-rev {CARRIER}` prints `CONTROL_DRIVER_R91=PASS` with
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`, and `control-forgeries-r91.py --work <scratch>` prints
`FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`. Source S070 (installed sha256sum(1), re-opened this round)
grounds the digest-pin rule.
C2 calibration: `python3 -B corpus/evidence/round91/curation-r91.py --root .` prints `CURATION_R91=PASS` with
`LEGS_MEASURED=13/13 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17
TFREQ_MAX_DF=3 UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0 VERDICT fields_hold=1 DETECTOR_WITNESS=11/11`, and
`curation-r91-controls.py --root . --work <scratch>` prints `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4
DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`.
C3 freshness: `python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest
corpus/evidence/round91/controls/selftest-r91.txt` prints `SKILL_TALLY_R91=PASS` with `TALLY_ROWS=9 STALE_TALLIES=0/9
EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283
CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`; `skill-tally-r91-controls.py --root . --work <scratch>` prints
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`. The C3 repair (one SKILL.md clause) is
NOT yet in the lane's committed tree at C2 — it lands after the wave; the controls reconstruct the old prose.
The committed selftest receipt `corpus/evidence/round91/controls/selftest-r91.txt` is 283 cases; a FRESH
`bash tools/research-gate.sh --selftest` takes about six minutes and is only required where an item says so.
`tools/research-gate.sh` and `tools/gate-records.py` are UNCHANGED this round.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite into
your wave output folder before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits
or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under {LANE}/.ufo/waves/round-91/w1/ plus your scratch
dir. Network: none this round except a re-open an item names; every other check reads committed bytes (an unrequested
GET is a finding). Never mutate a host sysctl, never run sudo, never restart a host service.
Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`, pass it
explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally:
shutil.rmtree` in Python). Never write under /tmp. Build a tree at a revision with
`git -C {LANE} archive <rev> | tar -x -C <scratch dir>`; for pin/self-pin checks you need history, so
`git clone --shared {LANE} <scratch>/repo` and `git -C <scratch>/repo checkout {CARRIER}` instead. Any fixture git repo
is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call names `-C "$D"`,
and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command.
Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus
exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide.
End your report with one line per claim you touched: `VERDICT: <seat> <C1|C2|C3> fired|held|n/a — <one sentence>`
(plain text, not JSON). A seat that ships no `VERDICT:` trailer is tallied as a seat-discipline finding.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade.
"""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": GODSPEED + task}


ITEMS = [
    item("R91ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R91ExecC1Repro`; `git clone --shared {LANE} $S/repo`
then `git -C $S/repo checkout {CARRIER}`. Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work $S/verify`
→ record the full stdout, the `CONTROL_DRIVER_R91=` line and the exit code; expected `COMMITTED_OK=6/6 EXACT_OK=6/6
PIN_OK=6/6 FRESH_OK=6/6` and `RECEIPT SELF_PIN OK rev={FREEZE} receipts_rev={CARRIER}`.
(b) `python3 -B corpus/evidence/round91/control-forgeries-r91.py --work $S/forge` → expected
`FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`.
(c) the QUALITY-202 form the round-90 sentinel failed: `python3 -B corpus/evidence/round91/control-driver-r91.py verify
--root {LANE} --repo $S/repo --rev {FREEZE} --receipts-rev {CARRIER} --work $S/verify2` → must PASS with a `BASES root=...
repo=...` line naming both bases; report it.
(d) prove `verify` wrote nothing to the receipts dir: `sha256sum corpus/evidence/round91/controls/receipts/*.txt` before
and after (a), compare.
Copy each receipt into your report folder. Report every observed line and exit code. VERDICT trailer required."""),

    item("R91ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R91ExecC2Repro`; clone as above and checkout `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round91/curation-r91.py --root .` → record stdout + exit; expected `CURATION_R91=PASS`
with `LEGS_MEASURED=13/13 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 TFREQ_MAX_DF=3
UNENTAILED_TERM=0`.
(b) `python3 -B corpus/evidence/round91/curation-r91-controls.py --root . --work $S/ctl` → expected
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`.
(c) `python3 -B corpus/evidence/round90/curation-r90.py --root .` → expected `CURATION_R90=PASS` (the prior counter
still accepts the clean tree; no regression by construction).
(d) derive DF_MAX independently: write a small read-only probe under `$S` that loads the two routed entries, collects
their located-quote texts and their decision-row Do/Never cells as documents, and prints, for every legitimate
decision row, the minimum document frequency among the terms its quote shares with the row. Expected: every row has a
shared term at df <= 3, so `DF_MAX=3` is the measured maximum of those minima. Paste the per-row table (17 rows).
(e) show the `source`-only warrant forgery prints `LEG_FAIL TFREQ` under r91 and `CURATION_R90=PASS` under r90 (the
controls already build it — cite its line and copy the tree under `$S/ctl` if it persists, else rebuild it in `$S`).
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R91ExecC3Repro", "executor", f"""Reproduce frozen C3 from a clean tree. `S={SCRATCH}/R91ExecC3Repro`; clone as above and checkout `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt`
→ expected `SKILL_TALLY_R91=PASS` with `CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2
MISLABELED=0 LEGS=2/2`. The lane's committed SKILL.md at C2 still carries the pre-round clause, so this run is
EXPECTED to FAIL at C2 (`RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283`, `MISLABELED=6`); record
that exactly, then build the landing tree: `git -C {LANE} diff -- SKILL.md` is the uncommitted one-clause repair in the
L1's working tree — copy the working `{LANE}/SKILL.md` into `$S/repo/SKILL.md` and rerun (a) → PASS. Report both runs.
(b) `python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root {LANE} --work $S/ctl` → expected
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`.
(c) re-derive the case names independently: `grep '^ok-case' corpus/evidence/round91/controls/selftest-r91.txt | awk
'$2>=270 && $2<=283'` — show that 273-275 carry `bashenv` names and only 282-283 carry `bash-pin-override`; list all
11 names.
(d) re-derive `OTHER_OCCURRENCES=3`: `grep -c 'PASS ([0-9]* cases,' SKILL.md` and list the three non-current
occurrences (lines and counts).
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R91ExecMutations", "mutation-tester", f"""Mutation battery on the three r91 instruments. `S={SCRATCH}/R91ExecMutations`; `git clone --shared {LANE} $S/repo`;
checkout `{CARRIER}`. Mutate COPIES under `$S` only; never edit the lane.
For each mutant, copy `$S/repo/corpus/evidence/round91/<instrument>` into `$S/mut/<id>/`, apply one textual change,
run the matching counter on `$S/repo` (with `--selftest` for C3), and record verdict + exit. A killed mutant makes the
counter print FAIL / exit 1 or its controls battery refuse; a surviving mutant is a finding.
C1 mutants: M1 `check_headers` ignores `len(vals) > 1` (duplicates accepted); M2 `pin_report` returns `([],0)` always;
M3 the `UNSCORED_RECEIPT` loop body disabled; M4 `check_headers` does not check `expected_exit`.
C2 mutants: M5 `q_shape_violation` always returns None; M6 `source_link` returns `(True, True)`; M7 `DF_MAX = 99`;
M8 restore the round-90 `for term in DEFECT_TERMS:` double-append loop.
C3 mutants: M9 the `CASE-RANGE` leg derives its expected range from the prose (returns the claimed tuple); M10 the
`CASE-RANGE` leg is deleted (the summary still prints PASS).
Also one control on the harness: M11 a mutant that only renames a variable (must SURVIVE and be reported as a
survivor, proving the battery is not a blanket refusal). Expected `MUTANTS_KILLED=10/11 SURVIVORS=1/11` (M11). Report
the exact command per mutant, the observed verdict line and exit. VERDICT trailer required."""),

    item("R91RevPrior", "revenger", f"""Independently reproduce the BEFORE state the claims rest on, from committed bytes only. `S={SCRATCH}/R91RevPrior`;
`git clone --shared {LANE} $S/base` and `git -C $S/base checkout {BASE}`; a second clone at `{CARRIER}` for the r91
instruments.
(a) C1 before: with the round-90 driver `corpus/evidence/round90/control-driver-r90.py` and the r91 fixture built by
`corpus/evidence/round91/control-forgeries-r91.py --work $S/forge` (run from the carrier clone), show r90 accepts all
six forged classes: the battery prints `PRIOR_ACCEPTED=6/6`. Also show r90's `header_multi` equivalent (its
`header_fields`) keeps the last header value — cite `corpus/evidence/round90/control-driver-r90.py` line numbers.
(b) C2 before: on the four forged trees `curation-r91-controls.py` builds, show `curation-r90.py` prints
`CURATION_R90=PASS` on each (the controls battery prints `PRIOR_ACCEPTED=4/4`), and show the double-count:
`DUPCOUNT_R90=2` vs `DUPCOUNT_R91=1`, with the round-90 source line that appends inside a `for term in DEFECT_TERMS:`
loop.
(c) C3 before: on `{BASE}:SKILL.md` (the old clause) `skill-tally-r90.py` prints `SKILL_TALLY_R90=PASS` while
`skill-tally-r91.py` prints `CASE_RANGE_OK=1/2 MISLABELED=6` (use `--selftest` with the committed receipt).
(d) compare (a)-(c) with the committed before receipts
`corpus/evidence/round91/controls/receipts/c{1,2,3}-before.txt` at the carrier; flag any line that does not re-derive.
Report every command, line and exit. VERDICT trailer required."""),

    item("R91ReviewerC1", "reviewer", f"""Attack frozen C1's STATED WORDING against the code. `S={SCRATCH}/R91ReviewerC1`; clone at `{CARRIER}`.
Read `{LANE}/corpus/evidence/round91/claims.md` C1 (clauses 1-8 + named limits) and
`corpus/evidence/round91/control-driver-r91.py`. For each clause, build the smallest fixture that makes the code accept
a state the sentence reads as refused, or refuse a state the sentence reads as accepted. At minimum attempt:
1. a receipt whose `# case=` matches but whose `# expected_exit=` appears twice with the same value (duplicate with
   equal values: refused? the sentence says "appears exactly once");
2. a row whose command names TWO scripts (`bash @ROOT@/x.sh && python3 -B @ROOT@/y.py`) — which one is pinned?
3. a pinned script that reads a second, unpinned data file (named limit 3);
4. `PINNED_FILES=6/16` — does the sentence read as "every pinned file checked"?
5. `self_pin` without `--repo` (no pin-at-rev leg) vs the sentence;
6. a receipt carrying `# exit=` with a leading `+` or spaces (`+0`): accepted?
For each attempt: command, observed verdict token + exit, and whether it falsifies the wording. If it does, name the
narrowing the L1 must record (an amendment to `plans/round-91.md`). Do not edit the lane; your artifacts live under
your folder. VERDICT trailer required."""),

    item("R91ReviewerC2", "reviewer", f"""Attack frozen C2's STATED WORDING against the code. `S={SCRATCH}/R91ReviewerC2`; clone at `{CARRIER}`.
Read `{LANE}/corpus/evidence/round91/claims.md` C2 and `corpus/evidence/round91/curation-r91.py`. Attempt at minimum:
1. a Located-quotes row with 4 cells (`| Q14 | S023 | "x" | extra |`) — QSHAPE fires? the sentence says "exactly three
   cells";
2. a row placed OUTSIDE the table (`## Located quotes` prose line starting `|`) — counted?
3. a located quote whose `used-by` names a SIBLING entry that contains this entry's basename as a substring — does
   `source_link` accept a wrong used-by?
4. a decision row naming two qids where one shares only `source` (df 7) — TFREQ fires for that qid?
5. a row carrying BOTH defect terms unentailed — does it append two records with their own terms?
6. the sentence's `TFREQ_OK=17/17` — is `tfreq_total` 17 on the clean tree, and does it count rows with an unresolved
   qid (which the sentence does not cover)?
Report each: command, observed line + exit, falsifies-wording or neutral, and the narrowing to record if it fires. Do
not edit the lane. VERDICT trailer required."""),

    item("R91ReviewerC3", "reviewer", f"""Attack frozen C3's STATED WORDING against the code. `S={SCRATCH}/R91ReviewerC3`; clone at `{CARRIER}`.
Read `{LANE}/corpus/evidence/round91/claims.md` C3 and `corpus/evidence/round91/skill-tally-r91.py`. Attempt:
1. a scratch SKILL.md whose clause reads `r39 bash-pin cases 273–275 and bash-pin-override cases 282–299` (a range
   extending past the case list) — refused? what code?
2. a scratch selftest receipt where case 282's name is renamed to `bash-pin-override-renamed` and a new name is added —
   does the counter bind names or numbers?
3. a scratch SKILL.md whose clause is ABSENT — `CLAUSE_MISSING` fires?
4. a stale historical tally (one of the three OTHER_OCCURRENCES) changed — does the counter notice (it must NOT bind
   historical quotes; OTHER_OCCURRENCES must change)?
5. a scratch SKILL.md with the correct numbers but the two clauses swapped (273–275 labelled override) — caught?
Report each: command, observed line + exit, falsifies-wording or neutral, and the narrowing to record if it fires.
Do not edit the lane. VERDICT trailer required."""),

    item("R91CriticClaims", "critic", f"""Falsify the claims' shared assumptions and the freeze itself. `S={SCRATCH}/R91CriticClaims`; clone at `{CARRIER}`.
Read claims.md, plans/round-91.md (including §Pre-wave freeze repair 1) and claims.json. Attempt, with artifacts:
1. **Freeze integrity:** does `instrument-pins.txt` match the committed bytes at F2 for all 16 pins? Re-derive with
   `git show {FREEZE}:<path> | sha256sum`. Does the carrier `{CARRIER}` carry receipts that pin `{FREEZE}`?
2. **No-work control:** for each claim, build the cheapest state that skips the claimed work and check the frozen
   predicate cannot reach it (e.g. C1 with the r90 driver substituted while the receipts are r91's; C2 with a
   duplicated qid row that keeps the count; C3 with the range derived from the prose).
3. **Cross-claim coupling:** can C2's PASS be reached while its QSHAPE leg never sees the table (e.g. rename the
   heading `## Located quotes` to `## Located Quotation`)? The sentence names the heading — does the code?
4. **The plan's claim that "no scored run preceded F2"** — verify from git history (`git log --oneline F..C2`), and
   flag any commit that runs or scores a candidate before F2.
5. **Ledger pre-shape:** propose the rows the `claim-falsification.tsv` must carry (per claim, per attack seat) and
   check every attack seat in this wave is named.
Report each attempt with command + observed line + verdict (falsifies-wording / neutral) and the exact narrowing
needed. VERDICT trailer required."""),

    item("R91SentinelScope", "sentinel", f"""Scope and safety review of the round's instruments and dispatch text. `S={SCRATCH}/R91SentinelScope`;
clone at `{CARRIER}`.
1. Run EVERY command form printed in the wave context verbatim on correct bytes (C1 verify with `--root . --repo .`;
   C1 verify with `--root {LANE} --repo <clone>`; the forgery battery; the C2 counter and controls; C3 with the
   committed receipt and controls). Any form that fails on correct bytes is a finding.
2. Check `verify` never writes under `corpus/evidence/round91/controls/receipts/` (sha256 before/after) and that
   `--work` is the only write root.
3. Check no path escapes: grep the three instruments for `/tmp`, absolute writes, `HOME`, network calls
   (`urllib|socket|http`) and host mutations (`sysctl|sudo|systemctl`); report each hit with file:line.
4. Check the claim's `SELF_PIN`/`PINNED_FILES` reading against the printed line (`PINNED_FILES=6`, 16 pins total) and
   flag if the report would overstate it.
5. Check credential/secret shapes: `git grep -nE 'sk-|ghp_|AKIA|BEGIN [A-Z ]*PRIVATE KEY'` at the carrier → expect
   none; report.
6. Confirm the SKILL.md working-tree repair is ONE clause (`git -C {LANE} diff -- SKILL.md`) and no other file is
   modified in the working tree.
Report commands, lines, exits. VERDICT trailer required."""),

    item("R91ConnectorSiblings", "connector", f"""Read-only sibling-overlap scan. `S={SCRATCH}/R91ConnectorSiblings`; do not edit any sibling.
Search the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` (and their `corpus/evidence/*/` tools)
for the two classes this round hardens, and report file:line for each hit:
1. **last-wins parsing of repeated keys/headers** in receipt, header, registry or section parsers — a dict assignment
   on a repeated key, `header_fields`-style loops, `load_sections` last-wins;
2. **warrant/term-frequency or document-frequency logic** in curation or claim-verification counters, and any
   duplicate-row/qid guard.
For each hit: lane, path:line, one-line reading, and whether it is the same class as chousa's C1 R1 / C2 R3. Do not
absorb, copy or edit anything; the report is a pointer map. Also state explicitly what you did NOT find (the sweep).
VERDICT trailer required."""),

    item("R91ScoutRegistry", "scout", f"""Per-surface reconnaissance of the registry and the corpus surfaces the claims read. `S={SCRATCH}/R91ScoutRegistry`;
clone at `{CARRIER}`.
1. Re-open S070's premise from committed bytes: `/usr/share/man/man1/sha256sum.1.gz` sha256, the decompressed line
   that carries "Print or check SHA256 (256-bit) checksums.", and the registry row's anchor/`teaches` cells; report
   whether the row's recorded sha (`93c17dff…`) still matches.
2. The planned S221 attempt: show the `refetch.tsv` row (`S221 … 28 000 - -`), confirm `grep -c '| S221 |'
   corpus/SOURCES.md` is 0, and that no capture key exists for the URL. Report the egress table commit and its URL.
3. Verify every source cited by the two routed entries' Located-quotes rows: S214, S018, S023, S215, S026, S031 —
   `status=mined` and `used-by` naming the citing entry; report any drift with the exact cell.
4. Count the surfaces C2 reads: data rows in `## Located quotes` (expect 20), decision rows (expect 17), and the
   capture files that resolve each quote; flag any row whose capture is absent.
5. Check the registry census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin chousa` → exit code and the row count (`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}'
   corpus/SOURCES.md`); report both.
Report commands, lines, exits; no edits. VERDICT trailer required."""),
]

SPEC = {
    "wave": "chousa-r91-w1",
    "reportDir": ".ufo/waves/round-91/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1, ensure_ascii=False)
    print(f"wrote {out} items={len(ITEMS)}")
