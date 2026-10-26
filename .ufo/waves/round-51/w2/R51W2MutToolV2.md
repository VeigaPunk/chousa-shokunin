# R51W2MutToolV2 — mutation tests: `tools/assimilate-rows.py` v2 vs both C1 detectors + selftest

Attacked: the wave-1 v2 adopter. Subject bytes = `cf642c6:tools/assimilate-rows.py`, sha256
`6b975f91c809485c8d03e6134e2a17bdb7f9079c22218d74e9321a14632572f6` (copied to scratch as `pristine.py`;
`git show cf642c6:tools/assimilate-rows.py | sha256sum` matches). I never wrote the lane tool: the
worktree file is now `10af959b…` from a sibling's concurrent v3 commit (HEAD advanced mid-run) — not mine.

Detectors (all read-only; scratch `/dev/shm/chousa-r51-R51W2MutToolV2/`, TMPDIR pointed there):
- D1 `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --tool <mutant>` (blob `94ddc7dc…`, unchanged all run).
- D2 `env -u ASSIMILATE_CITES python3 <frozen c1-supplement> --tool <mutant>` — HEAD bytes (189 lines, 6 legs)
  run from a byte-identical scratch mirror `mirror-lane/corpus/evidence/round51/` (+ copied R50 fixtures; pin
  passes: SHAPE leg = c1-count 5/5 under the mirror). Baseline: `SUPPLEMENT_LEGS=6/6`, `C1_SUPPLEMENT=PASS`.
- D3 `env -u ASSIMILATE_CITES python3 <mutant> --selftest` — default fixtures via byte-identical scratch mirror of
  `corpus/fixtures/assimilate-selftest/` (digest `3b7ad258…` == lane digest == selftest `FIXTURES_SHA256`).
- Baseline pristine: D1 `C1=PASS` (LEGS=5/5) · D2 `C1_SUPPLEMENT=PASS` · D3 `SELFTEST=PASS findings=27 expected=27`.

**Detector churn found (not a mutant):** at 21:28:52 the working-tree `c1-supplement.py` changed 189→246 lines
(6→10 legs, ` M`). Its `CLASH/OWN_WORK/STALE_OUT/HEADER` legs FAIL on the pristine v2 tool
(`SUPPLEMENT_LEGS=6/10`, rc=1) — they test v3 behavior, so they are inconclusive as v2 detectors (baseline
failure ≠ kill). Its baseline-clean legs are valid and confirm `ENV_DEFAULT` kills m14 (below). First matrix
pass mixed old/new detector bytes mid-run; discarded and fully re-run on snapshots with before/after hashes
(supplement `aef6c334…` and c1-count `94ddc7dc…` identical before and after the re-run).

Mutants: one per class, single-hunk edits of pristine.py, each `py_compile`-clean; examples — m02
`SOURCE_RE [ \t]*`→`[ \t]+`; m09 registry split `ESC_SPLIT.split(s.strip())`→`s.split("|")`; m13 insert
`if a.cites == "all": a.cites = "source"`; m14 drop `os.environ.get("ASSIMILATE_CITES") or ` (both sites).
Full loop: for m in m01…m14: run D1, D2, D3; verdict = any detector rc!=0 with baseline-clean legs.

## Kill matrix (P = passes = not killed by that detector; F = killed; leg that fired)

| mut | class (assigned)                                  | D1 c1-count        | D2 frozen suppl   | D3 selftest | verdict |
|-----|---------------------------------------------------|--------------------|-------------------|-------------|---------|
| m01 | source_ids scans past `####`                      | P                  | F SOURCE_LINE     | P           | KILLED  |
| m02 | SOURCE_RE requires a space                        | P                  | P                 | F (4 DIFF)  | KILLED  |
| m03 | source_ids takes every id on the line             | P                  | F SOURCE_LINE     | F (9 DIFF)  | KILLED  |
| m04 | subst ignores only                                | P                  | F CROSS_ENTRY     | F (2 DIFF)  | KILLED  |
| m05 | unknown-source refusal removed                    | P                  | F UNKNOWN_SRC     | P           | KILLED  |
| m06 | minted-collision refusal removed                  | P                  | P                 | P           | SURVIVES |
| m07 | bodyonly computed against cited again             | P                  | F CROSS_ENTRY     | F (1 DIFF)  | KILLED  |
| m08 | pipe_free removed from staged identity            | F PIPE_IDENTITY    | F SHAPE           | F (10 DIFF) | KILLED  |
| m09 | registry split back to plain `\|`                  | F PIPE_IDENTITY    | F SHAPE           | F (9 DIFF)  | KILLED  |
| m10 | registry_problems ignores outside rows            | F REGISTRY_STRUCT. | F SHAPE           | P           | KILLED  |
| m11 | used-by from all tokens                           | P                  | F CROSS_ENTRY     | F (3 DIFF)  | KILLED  |
| m12 | bodyclash omitted                                 | P                  | F CLASH           | F (1 DIFF)  | KILLED  |
| m13 | `--cites all` ignored                             | F LEGACY_ALL+SOURCE_ONLY | F SHAPE     | P           | KILLED  |
| m14 | env override ignored                              | P                  | P                 | P           | SURVIVES (frozen set) |

Representative commands/outputs (all 14 ran the same three):
```
env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --tool $S/tools/m08.py
  → PIPE_IDENTITY=FAIL d1=no d2=ok … LEGS=4/5 C1=FAIL  (rc=1)
env -u ASSIMILATE_CITES python3 $S/mirror-lane/corpus/evidence/round51/c1-supplement.py --tool $S/tools/m12.py
  → CLASH=FAIL 0/3 … SUPPLEMENT_LEGS=5/6 C1_SUPPLEMENT=FAIL
env -u ASSIMILATE_CITES python3 $S/tools/m02.py --selftest
  → DIFF missing MAP S015->S002 held; DIFF unexpected BODYONLY corpus/knowledge/b.md S015; SELFTEST=FAIL
```
m02's killer is fixture entry B line 3 `source:S015 — …` (no space); m01/m05's killers exist only in the
supplement (fixtures have no body `source:` line and no unknown source id).

## Survivors of all three frozen detectors

**m06 — minted-collision refusal removed: SURVIVOR; no input can kill it (dead code).**
Every minted id is `> max(Registry)`, hence not a Registry row, so the unknown-source refusal (m05's target)
always fires first and `return 1`s before the minted check is reached. Probe (case that would have killed it):
registry S001–S003, staged S500 cited by a.md (mints S004), b.md header `source: S004`:
```
M6-PROBE pristine rc=1 wrote=['collisions','reg-ids','staged-ids']
M6-PROBE pristine stderr='REFUSED corpus/knowledge/b.md: source id S004 is neither a staged row nor a lane Registry row'
M6-PROBE m06      rc=1 wrote=['collisions','reg-ids','staged-ids']          # byte-identical stdout+stderr
M6-PROBE m06      stderr='REFUSED corpus/knowledge/b.md: source id S004 is neither a staged row nor a lane Registry row'
```
Coverage finding, contract untouched: the docstring's promise ("…or is a lane row of another document that
this run also mints, is refused") still holds observably — via the other refusal; the dedicated check is
unreachable. Also covers the in-flight supplement's new CLASH-ok2 intent (body token equal to a minted id is
NOT bodyclash-listed by v2 since bodyonly filters `if i in staged`).

**m14 — env override ignored: SURVIVOR of D1/D2frozen/D3 (counters run `env -u`), killed by any ambient-env case.**
Killer (frozen bytes, committed R49 counter, ambient `ASSIMILATE_CITES=all`, no flag):
```
ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py --tool $S/tools/pristine.py → SETS_PASS=3/3 C1=PASS rc=0
ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py --tool $S/tools/m14.py
  → SET_C … REWRITE=0/1 … -> FAIL; SETS_PASS=2/3 C1=FAIL rc=1
ASSIMILATE_CITES=all python3 $S/tools/pristine.py --selftest → SELFTEST=FAIL findings=36 expected=27
ASSIMILATE_CITES=all python3 $S/tools/m14.py      --selftest → SELFTEST=PASS findings=27 expected=27
```
i.e. the env override is load-bearing v2 behavior (R49 depends on it; that's why round-51 counters strip it).
The in-flight supplement's new `ENV_DEFAULT` leg (baseline 3/3 PASS on v2) kills m14 directly:
`m14 D2I=… ENV_DEFAULT=FAIL` — a second, independent kill on post-freeze bytes.

## Restoration / bounds evidence
- Mutants lived only in scratch; the lane tool was never written by me. Before first copy and after all runs,
  subject copy stayed `6b975f91…`; lane worktree changes (`→10af959b…`, now committed) are the sibling v3 lane's,
  not mine (`git diff --numstat -- tools/assimilate-rows.py` at report time shows the sibling's hunk).
- Lane writes: this report file only. No pacman/install (authorization unused). Scratch deleted after this file.
- Incidents: scratch dir externally wiped twice (recreated; no lane impact); detector bytes changed mid-wave
  (handled above by snapshot+baseline discipline).

VERDICT: attacked assimilate-rows v2 with 14 single-class mutants × 3 detectors — 12/14 killed (matrix above); m06 survives because the minted-collision refusal is unreachable dead code shadowed by the unknown-source refusal, and m14 survives the env -u'd counters but is killed by the R49 counter / in-flight ENV_DEFAULT under ambient ASSIMILATE_CITES=all — counters and v2 claims hold; only dead-code and env-strip blind spots found.
