# R91ExecC3Repro — round-91 C3 (freshness) reproduction from a clean tree

Seat `R91ExecC3Repro` (leaf executor, lane `chousa-shokunin`). No task/subagent dispatch, no lane mutation, no
network, no host mutation, no tool installs. Read-only against the lane; the only lane paths written are this report
and `w1/receipts/R91ExecC3Repro/`.

- Root attacked: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- Scratch: `/fast/scratch/hyaku/chousa-r91/R91ExecC3Repro` (removed before yield; nothing written under `/tmp`)
- Tree: `git clone --shared <lane> $S/repo` then `git -C $S/repo checkout -q 67954adc599bd605705d94a1ea7abb582491a907`
  → `git -C $S/repo rev-parse HEAD` = `67954adc599bd605705d94a1ea7abb582491a907` and
  `git -C $S/repo rev-parse --show-toplevel` = `/fast/scratch/hyaku/chousa-r91/R91ExecC3Repro/repo` (toplevel
  assertion run before every mutating git call in the clone).
- Receipts: `.ufo/waves/round-91/w1/receipts/R91ExecC3Repro/` (every file cited below + `manifest.sha256`;
  `sha256sum -c manifest.sha256` = all OK).

Instrument identity at the attacked tree (receipt `g-hashes-and-diffs.txt`). All four files matched their committed
C3 blobs (`git cat-file -p 67954ad…:<path> | sha256sum`):

| file | sha256 |
|---|---|
| `corpus/evidence/round91/skill-tally-r91.py` | `cc2d5c3b…c789bc` → `cc2d5c3b946c503f3dfa060802796a24e0491ea3744528ed5c37af8fc3e9e513` |
| `corpus/evidence/round91/skill-tally-r91-controls.py` | `69bddcb5a920678348fcf18181276a21daa69aa9b96a997fd484ba682a4d27ae` |
| `corpus/evidence/round91/controls/selftest-r91.txt` | `9c29428160768524c77407eedd711200be53a1074e2a22fe9bab814ad3f5bb37` |
| `SKILL.md` (committed blob at C3, pre-repair) | `a09b7646221cb20c04ae428cf40989d1629d40c827a058e07e7f07355a3897da` |

`git diff --stat 265b8633b7e5d1da49da6fb948df9707373fb15c -- tools/research-gate.sh tools/gate-records.py` printed
nothing and exited 0 — the gate and record tools are unchanged from the stated base, as the wave brief says.

## (a) C3 case-range tally — both runs

### Run 1 — committed carrier C3 (pre-repair): FAIL, exactly as the plan predicts

```
$ cd $S/repo && python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt
CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283
CASE_RANGE_FINDING MISLABELED=6 indices=276,277,278,279,280,281
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=1/2 MISLABELED=6 LEGS=1/2
LEG_FAIL CASE-RANGE
SKILL_TALLY_R91=FAIL
EXIT=1
```
Receipt: `a1-c2-tally-run.txt`, observed last lines `SKILL_TALLY_R91=FAIL` / `EXIT=1`. This is the frozen "Before"
observation (`MISLABELED=6`, `CASE_RANGE_OK=1/2`, `LEGS=1/2`) and matches `plans/round-91.md` §Pre-freeze repairs
item 9 ("the SKILL.md clause is repaired at the landing, not at the freeze, so the freeze tree still shows the
defect (`MISLABELED=6`, `CASE_RANGE_OK=1/2`)") and the wave brief.

### Run 2 — landing tree (C3 + the L1's one-clause `SKILL.md` repair): PASS

Landing tree built exactly as instructed: copied the lane working copy
`/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md` over `$S/repo/SKILL.md` (sha256 identical on both sides,
`dcdf92341b25553ba84fd3f6c0178161fa2f0e6c74c76b8a7cc92bb1f1c789bc`; receipt `g-hashes-and-diffs.txt`,
`h-clause.txt`).

```
$ cd $S/repo && python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2
SKILL_TALLY_R91=PASS
EXIT=0
```
Receipt: `a3-landing-tally-run.txt`, observed last lines `SKILL_TALLY_R91=PASS` / `EXIT=0`.

The landing tree differs from C3 only at `SKILL.md` line 86 (`git diff --stat` = ` SKILL.md | 2 +- / 1 file changed,
1 insertion(+), 1 deletion(-)`; `git diff` hunk header `86c86`; receipt `a2-landing-diff.txt`). The two clauses, verbatim:

- C3 committed (pre-repair): `r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283 (canonical, flock-capable host)`
- landing (repaired): `r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, of which bash-pin-override cases 282–283 (canonical, flock-capable host)`

Determinism: a second landing run produced a byte-identical file (`i-determinism-run2.txt`, `diff` = no output,
`DETERMINISM=identical`, `EXIT=0`; sha256 equals `a3-landing-tally-run.txt`'s `bf171af1…`).

Frozen expectation vs observed in run 2 — every token matches, no deviation:
`SKILL_TALLY_R91=PASS` ✓ · `TALLY_ROWS=9` ✓ · `STALE_TALLIES=0/9` ✓ · `EXPECTED_CASES=283` ✓ ·
`EXPECTED_SKIPPED=0` ✓ · `OTHER_OCCURRENCES=3` ✓ · `CASE_RANGE_BASHENV=273-275` ✓ · `CASE_RANGE_BASH_PIN=282-283` ✓ ·
`CASE_RANGE_OK=2/2` ✓ · `MISLABELED=0` ✓ · `LEGS=2/2` ✓.

## (b) C3 discrimination battery — PASS

```
$ cd $S/repo && python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S/ctl
OK old-prose: r90 TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS, r91 SKILL_TALLY_R91=FAIL
OK stale-tally: r90 TALLY_ROWS=9 STALE_TALLIES=1/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL (rc=1), r91 SKILL_TALLY_R91=FAIL (rc=1)
CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1
EXIT=0
```
Receipt: `b-controls-run.txt`, observed line `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1
STALE_REFUSED_BOTH=1/1`, `EXIT=0` — the frozen C3 battery line verbatim. The battery reads the receipt and both
counters from its own tree (`$S/repo`) and writes only under `--work`; lane `git status --porcelain` was unchanged
before and after (same three pre-existing modified paths, no new tracked change). The restored round-90 clause it
builds (`BAD_CLAUSE` in the script) is byte-identical to the committed C3 clause above, so the "old prose" fixture is
the real historical prose, not a paraphrase.

## (c) Independent re-derivation of the two case ranges

```
$ grep '^ok-case' corpus/evidence/round91/controls/selftest-r91.txt | awk '$2>=270 && $2<=283'
ok-case  270 claims-sha-path-shim         exit=1
ok-case  271 claims-sha-cut-shim          exit=1
ok-case  272 claims-sha-stdin-hold        exit=0
ok-case  273 pin-bashenv-echo             exit=0
ok-case  274 drift-bashenv-echo           exit=0
ok-case  275 pin-bashenv-root             exit=0
ok-case  276 pin-env-fn-echo-scrub        exit=0
ok-case  277 pin-env-fn-suppress          exit=0
ok-case  278 pin-env-fn-root              exit=0
ok-case  279 env-pin-override-missing     exit=2
ok-case  280 env-pin-override-fake        exit=2
ok-case  281 pin-bash-path-shim           exit=0
ok-case  282 bash-pin-override-missing    exit=2
ok-case  283 bash-pin-override-fake       exit=2
```
Receipt: `c-case-names.txt`. The eleven names 273–283 are listed above. Family derivation over the whole receipt:

- names containing `bashenv` → indices **273, 274, 275** (3 names), i.e. `CASE_RANGE_BASHENV=273-275`;
- names with prefix `bash-pin-override` → indices **282, 283** (2 names), i.e. `CASE_RANGE_BASH_PIN=282-283`;
- inside the claimed override range 276–283 the six non-`bash-pin-override` names are 276 `pin-env-fn-echo-scrub`,
  277 `pin-env-fn-suppress`, 278 `pin-env-fn-root`, 279 `env-pin-override-missing`, 280 `env-pin-override-fake`,
  281 `pin-bash-path-shim` — exactly the `MISLABELED=6 indices=276,277,278,279,280,281` the tool printed for the old
  prose.

Receipt integrity: 283 `ok-case` rows, indices 1..283 sequential with no gaps or repeats, verdict tail
`RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)` (`c-case-names.txt`).

## (d) Independent re-derivation of `OTHER_OCCURRENCES=3`

Receipt: `d-occurrences.txt`.

- `grep -c 'PASS ([0-9]* cases,' SKILL.md` → **12** matching lines. That loose pattern counts current tally cells
  too, so 12 is not the tool's number.
- Strict occurrence scan `grep -n -E 'PASS \([0-9]+ cases, [0-9]+ skipped\)' SKILL.md` → 12 lines, one occurrence each.
- Current-cell lines by the r90/r91 rule (`lstrip` starts with ``| `research-gate`` or the line contains
  ``Selftest `PASS (``): lines 86, 87, 88, 89, 90, 91, 92, 93 (the nine registry rows) and 781 → **9 current**.
- Non-current occurrences → exactly **3**:
  - line 186: `PASS (256 cases, 0 skipped)`
  - line 188: `PASS (161 cases, 0 skipped)`
  - line 640: `PASS (215 cases, 0 skipped)`

So `OTHER_OCCURRENCES=3` is re-derived from `SKILL.md` alone, and it is identical in both the C3 run (pre-repair) and
the landing run — the one-clause repair moves no historical tally (kill rule K3).

## Kill-rule probes (extra, cheap, in-scope)

- **K4 absent clause.** Landing `SKILL.md` with the override clause deleted entirely, scored with the same receipt:
  `CASE_RANGE_FINDING CLAUSE_MISSING:bash-pin-override`, `CASE_RANGE_OK=1/2 MISLABELED=0 LEGS=1/2`,
  `SKILL_TALLY_R91=FAIL`, `EXIT=1` (receipt `e-absent-clause-probe.txt`). An absent clause is not tolerated.
- **K4 unread receipt.** `--selftest <nonexistent>`: `SKILL_TALLY_R91=SETUP missing selftest receipt …`, `EXIT=2`
  (receipt `f-missing-receipt-probe.txt`). The `--selftest` path is actually read; no fresh battery is silently
  substituted.
- **K2 discrimination.** Covered by (b): r90 PASSes the restored old prose and r91 refuses it
  (`OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1`); the stale tally is refused by both (`STALE_REFUSED_BOTH=1/1`). The
  derived ranges printed by r91 in both (a) runs are `282-283`, i.e. they come from the receipt's names, not from
  the prose (`derived=` differs from `claimed=` at C3, equal at landing).
- **K3 no movement.** `OTHER_OCCURRENCES=3` in both runs; the entire C3→landing delta is the single `SKILL.md` line.

## Limits of this evidence

- The landing revision is the L1's **uncommitted working tree** (`SKILL.md` sha `dcdf9234…`); this seat reproduces
  the predicate for exactly those bytes. If the landing commit carries a different `SKILL.md`, the PASS above does
  not transfer — the claim is bound to that one-clause edit and nothing else.
- No fresh `bash tools/research-gate.sh --selftest` was run: no C3 item requires it, and the assigned command uses
  the committed 283-case capture (`selftest-r91.txt`, sha `9c29428…`, copied here). The receipt's case names were
  cross-checked against `tools/research-gate.sh` (all eleven names 273–283 present in the gate source) but the
  battery itself was not re-executed in this seat.
- `MISLABELED` is computed only over the claimed override range; a claimed range that is *inside* the family (e.g.
  `282-282`) would score `CASE_RANGE_OK=1/2` by the pair comparison, not by `MISLABELED` — that is the tool's
  documented shape (`CASE_RANGE_OK` is the binding leg), not a reproduction defect.
- Everything was executed locally against committed bytes; no network access was performed, no tool was installed or
  upgraded, no sysctl/service/sudo operation was run.

## Files written

- `.ufo/waves/round-91/w1/R91ExecC3Repro.md` (this report)
- `.ufo/waves/round-91/w1/receipts/R91ExecC3Repro/`: `a1-c2-tally-run.txt`, `a2-landing-diff.txt`,
  `a3-landing-tally-run.txt`, `b-controls-run.txt`, `c-case-names.txt`, `d-occurrences.txt`,
  `e-absent-clause-probe.txt`, `f-missing-receipt-probe.txt`, `g-hashes-and-diffs.txt`, `h-clause.txt`,
  `i-determinism-run2.txt`, `selftest-r91.txt`, `manifest.sha256`

No production or lane file was modified; scratch `/fast/scratch/hyaku/chousa-r91/R91ExecC3Repro` was removed before
yield.

VERDICT: R91ExecC3Repro C3 held — the committed carrier prints `SKILL_TALLY_R91=FAIL` with `RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283` and `MISLABELED=6` exactly as the plan predicts, the landing tree (C3 + the one-clause `SKILL.md` repair, sha `dcdf9234…`) prints `SKILL_TALLY_R91=PASS` with every frozen token (`TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`), the battery prints `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`, and the ranges/`OTHER_OCCURRENCES` re-derive independently from the receipt and `SKILL.md`.
VERDICT: R91ExecC3Repro C1 n/a — not this seat's claim; not run.
VERDICT: R91ExecC3Repro C2 n/a — not this seat's claim; not run.
