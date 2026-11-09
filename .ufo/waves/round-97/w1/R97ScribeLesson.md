# R97ScribeLesson — round-97 lesson draft (Mistakes + LOG entry), chousa

Seat `R97ScribeLesson` (scribe, leaf). Frozen tree F `9a0ce2015fa0254848f2f32f612b20caf7dc5478`; base
`c8087ac529003e667505bcc624f9a7bde0cffbce`. Attacked content: read-only `git show <F>:path` into scratch; nothing in
the lane or fleet was written. Tooling: none installed or upgraded (none needed; `pacman` paused, not used).

## Deliverables

- `.ufo/waves/round-97/w1/R97ScribeLesson-mistakes-draft.md` — one mistake class, table in the round-96 form
  (class · evidence · captured-by · fix), with the shown-able-to-fail receipt lines, plus two paragraphs: what the fix
  does not close, and the receipt caveat.
- `.ufo/waves/round-97/w1/R97ScribeLesson-log-draft.md` — LOG.md entry draft (not written to the tracked file).

## Mistake class chosen

A self-test's pass count was read as its grip, and the only mutants it was measured against were the author's. The
candidate was checked against the round-96 probe and corrected: `PASS cases=32/32` was printed for 15 of the 19
survivors; the other 4 (n11, n12, n13, n26) crashed with a traceback and no summary. Two other candidate-adjacent
numbers were also checked; see F2.

## Findings

### F1 — candidate wording corrected (round-96 probe tally)

Command: `awk` over `.ufo/waves/round-96/w1/R96MutantsC1-mutprobe-out.txt` pairing each `MUTANT` line with its
`failing:` line (script in the receipt).
Observed: `KILLED=10 SURVIVED_PASS=15 SURVIVED_NO_SUMMARY=4 SURVIVED_TOTAL=19`; `grep -c '^MUTANT'` = 29; line 15
`SETUP n08-hits-regex-sign applies 0 times (SKIP)`; line 60 `KILLED 10/30 total-probed=30`. Exit 0.
Receipt: `.ufo/waves/round-97/w1/R97ScribeLesson-r96-probe-tally.txt`; copy of the probe output
`R97ScribeLesson-R96MutantsC1-mutprobe-out.txt`.
Effect: the lesson must say "15 printed PASS, 4 crashed", not "PASS 32/32 while 19 survived".

### F2 — round-96 seat report count does not match its body (not in the lesson; for the record)

`.ufo/waves/round-96/w1/R96MutantsC1.md:247` (VERDICT) says "19 survive it (15 of them also pass the round-95 CLI
battery)". Command: `grep -n 'Round-95 battery\|RERUN_CONTROLS=\|### Class\|^VERDICT'` over that file (receipt
`R97ScribeLesson-R96MutantsC1-md-class-grep.txt`, exit 0). Observed in the body: Class A has 3 mutants that fail the
round-95 battery (`:62` n07, `:64` n17, `:70` n27); Class C (`:103`) has 12 that pass it; Class B (`:74`, 4 crashes)
was not run through the battery. So the body supports 12, not 15. Also the probe's `KILLED 10/30` (`mutprobe-out:60`)
and the seat's `10/29` differ only by the n08 denominator. The seat report is not edited here; the planner should
place a correction if the 15 is cited.

### F3 — the fix covers case bodies only: crashes in setup code still survive the battery's rule (found by drafting)

Method: copies of the committed F tool built by `mk.py` (receipt `R97ScribeLesson-residue-mutant-builder.py.txt`),
each run by `run.sh` (receipt `R97ScribeLesson-residue-run.sh.txt`), which applies the battery's kill rule: `rc == 1`
and `SEARCH_RERUN_SELFTEST: FAIL` in stdout and no `Traceback` in stderr. Command: `./run.sh <tool>` for each.
Observed (`R97ScribeLesson-unguarded-residue.txt`):
- `sr-F.py` (unmodified): `rc=0`, last line `SEARCH_RERUN_SELFTEST: PASS cases=47/47`, 48 stdout lines (the
  `SURVIVED` label on this row is meaningless for a non-mutant; rc 0 is the datum).
- `mut-genv-raise.py` (`raise` at the top of `git_env`): `rc=1`, `RuntimeError: mutant: git_env raises` from
  `env = git_env()` (selftest body, `tools/search-rerun.py:512`), no summary line, verdict `SURVIVED`.
- `mut-strow-raise.py` (`raise` in `st_row`): `rc=1`, traceback through the fixture tuple (`:450-474`), no summary
  line, verdict `SURVIVED`.
- `mut-case-raise-inside.py` (`raise` after the guard in `case()`): `rc=1`, traceback, verdict `SURVIVED`. This is
  claims.md C1 named limit (b), recorded to show the guard's own boundary.
Source anchors: `R97ScribeLesson-f-selftest-guard-excerpt.txt` (lines 421-438 guard, 450-452 fixture, 506-512 env,
416-418 `st_row`).
Effect: the sentence "each inside a guard that turns an exception raised inside the case into that case's FAIL" is
true as written. The class (crash reported without a summary) is still open for shared setup, and no named limit
says so. The lesson states this as "not closed by the fix"; the planner should route it.

### F4 — the committed C1 receipt does not contain predicate 2's tally line

Commands (receipt `R97ScribeLesson-r97-c1-all-tail-check.txt`):
- `wc -l corpus/evidence/round97/after/c1-all.txt` → `142`.
- `grep -c 'SELFTEST_CONTROLS_R97=PASS' …/after/c1-all.txt` → `0` (grep exit 1).
- `grep -c 'regression-mutants-r95\|REGRESSION_R95=' …` → `0` (exit 1).
- `grep -c 'POSITIVE=1/1 EXTERNAL_KILLED=30/30' …` → `0` (exit 1).
- `tail -n 2` → `CASE no-write rc=0 …` and `CASE regression-rerun-controls-r95 rc=0 ok`. No `exit=` line after the
  battery block (the only `exit=` is at line 51, after the self-test run).
Battery source (`corpus/evidence/round97/selftest-controls-r97.py:202-218`, read from F): after `rerun-controls-r95`
the battery runs `mutants-r95.py` and then prints `CASE regression-mutants-r95`, the tally, and
`SELFTEST_CONTROLS_R97=PASS|FAIL`. None of those three lines is in the receipt.
Consequence: `claims.md` predicate 2 (lines 24-26) names an observed line that no committed receipt contains. The
per-case lines and the oracle tallies (`c1-all.txt:138-140`) are present. I did not rerun the battery (roughly eight
minutes; not this seat's item). [INFERENCE] the receipt was cut short; the bytes do not show the cause. The lesson
cites per-case lines only, and the caveat is written into the draft. Routed to the wave's reviewer / integrator.

### F5 — checked and held

- Exclusions are written, not silent: `n30` (`claims.md:45-46`, battery docstring `:26-28`) and `n08` (applied 0 times,
  `mutprobe-out:15`). The battery's 30 are 28 + `s1`, `s2`; `grep -c` of the battery's external rows gives 30 at
  `c1-all.txt:54-83`.
- Base numbers reproduce the round-96 probe: the base kill set (n01, n03, n04, n05, n06, n18, n19, n21, n24, n25 =
  10) in `before/c1-base.txt` (`:38-67`) equals the probe's `KILLED` set (`mutprobe-out:1-60`).
- The base crashes are scored `SURVIVED` by the r97 rule: `before/c1-base.txt:47-49` and `:62` (`rc=1 SURVIVED`).
- The fix's per-case lines: `after/c1-all.txt:63-65` and `:78` (`KILLED`, with failing case ids); self-test `:50`
  `PASS cases=47/47`; stand-ins `:138-140`.
- n22 is listed as "equivalent on the fixture shapes" by the round-96 seat (`R96MutantsC1.md:136-139`) and is killed at F
  by r09 (`c1-all.txt:74`). The claim's "non-equivalent" label for the 28 is therefore a judgement the seat's text
  does not fully carry; it is not a false sentence at F.

## Receipts written (all in `.ufo/waves/round-97/w1/`)

| file | content |
|---|---|
| `R97ScribeLesson-R96MutantsC1-mutprobe-out.txt` | copy of `round-96/w1/R96MutantsC1-mutprobe-out.txt` |
| `R97ScribeLesson-R96MutantsC1-n11-header-order.txt`, `…-n12-split-lookbehind.txt`, `…-n13-parse-split-nl.txt`, `…-n26-cells-strip-order.txt` | copies of the four crash receipts |
| `R97ScribeLesson-R96MutantsC1-baseline-selftest.txt` | copy of the green baseline (`:33` PASS 32/32) |
| `R97ScribeLesson-r97-c1-base.txt`, `R97ScribeLesson-r97-c1-all.txt` | copies of `before/c1-base.txt`, `after/c1-all.txt` |
| `R97ScribeLesson-r96-probe-tally.txt` | F1 (awk tally, exit 0) |
| `R97ScribeLesson-R96MutantsC1-md-class-grep.txt` | F2 (grep, exit 0) |
| `R97ScribeLesson-unguarded-residue.txt`, `…-residue-mutant-builder.py.txt`, `…-residue-run.sh.txt` | F3 (runs and builder) |
| `R97ScribeLesson-f-selftest-guard-excerpt.txt`, `R97ScribeLesson-r96-battery-kill-rule-excerpt.txt` | line excerpts of `git show F:tools/search-rerun.py`, `git show c8087ac5:corpus/evidence/round96/selftest-controls-r96.py` (`:126-131`) and `c8087ac5:tools/search-rerun.py:420` |
| `R97ScribeLesson-r97-c1-all-tail-check.txt` | F4 (wc/grep counts, exit 1 on zero matches) |

## Not checked by this seat (for the integrator)

- C2 (`corpus/knowledge/press-checklist-questions-r97.md`) was not opened. One grep of `after/c2-all.txt` confirmed
  `GATE_RECORDS files=1 records=30 ok=30 fail=0` (`:3`), `METADATA_COMPLETE=1/1` (`:8`), `rev_match=7/7` (`:19`),
  `VERBATIM=10/26 LETTERS=14/26` and `ENTRY_CONTROLS=PASS` (`:43-44`, `grep -o`, exit 0). The entry's content was not read.
- The battery was not rerun; the C1 predicate-2 verdict is left to a run of the frozen counter (F4).

## Scratch

`/fast/scratch/hyaku/chousa-r97/R97ScribeLesson` (git-show copies, mutants, run.sh) removed before yield.

VERDICT: R97ScribeLesson C1 n/a — lesson draft seat; F3 (setup code outside the per-case guard) and F4 (no committed predicate-2 tally line) are findings for the wave, not a fired or held verdict.
VERDICT: R97ScribeLesson C2 n/a — not examined by this seat beyond the grep counts in the section above.
