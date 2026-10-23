# RerunC1a — falsify P1 v2 (re-run c1-count-v2.py on the landed gate, fresh seeds)

Date: 2026-10-23. Seat: ChousaR32A2.RerunC1a. Lane HEAD confirmed `5d8a170795dcf48c3746a4f03dee9cfe32812834`;
gate `tools/research-gate.sh` sha256 `10f2fe12043c…4098` (matches the candidate); counter
`corpus/evidence/round32/c1-count-v2.py` sha256 `e6bf95313ad…0891`, run unmodified.

## Runs (committed counter, unmodified, cwd = lane root; C1_TMP/TMPDIR = scratch outside lane)

Command shape (identical except seed):
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=<scratch> TMPDIR=<scratch>
prlimit --nproc=8000 timeout 900 python3 corpus/evidence/round32/c1-count-v2.py --seed <S> --receipt <receipt>`

| seed | stdout | exit | receipt | predicate_holds | ref_rc | elapsed_s |
|------|--------|------|---------|-----------------|--------|-----------|
| 44001 | APPEND_SERIALIZED=24/24 (F_unterminated 12/12, L_empty 4/4, L_terminated 4/4, L_unterminated 4/4) | 0 | w2/RerunC1a/c1-s44001.json | true | 0 | 107.2 |
| 44002 | APPEND_SERIALIZED=24/24 (same classes all full) | 0 | w2/RerunC1a/c1-s44002.json | true | 0 | 107.0 |
| 44003 | APPEND_SERIALIZED=24/24 (same classes all full) | 0 | w2/RerunC1a/c1-s44003.json | true | 0 | 120.4 |

No trial failed in any run (`fails: []` in every receipt); strace delay self-check passed each
time (~0.31 s ≥ 0.25 s minimum). No below-target run, no failing trial's checks to report.

## Sibling/consistency scan
- L1 measure receipts `measure/after-c1-s32001.json`, `after-c1-s32002.json`: 24/24, same gate hash — consistent.
- w2 receipts surveyed: `ReviewCounterV3/c1-v3-s882013.json` is a *different* counter (LINE_BINDING_MATCH label) —
  out of "this counter" scope; `SepAudit32/c1-on-c2only-s7201.json` scored 0/24 but on mutant gate
  `2a21aa4327e0`, not the landed gate — does not falsify "no run … on that revision prints less".
- Environment: strace 7.2 at /usr/bin/strace; /fast had 219G free; scratch tmp dir empty post-run;
  counter removes its own temp trees (line 344 `shutil.rmtree(base)`); stray `research-gate --selftest`
  PIDs observed belong to sibling seats MutC1Gate/MutSelftestR2, untouched.

## Verdict
HOLDS — within scope. P1 v2 required 24/24 on two fresh seeds and no lower run on this revision;
my three independent fresh-seed runs (44001/44002/44003) each print APPEND_SERIALIZED=24/24 with
predicate_holds=true on the landed gate. Found no run below target and no harness error (no exit 2).

## Limits
Scoped to operability re-runs only; did not attack counter-vs-contract fidelity, seed-plan weakness,
or C2 (sibling seats cover). Counter runtime ~2 min/run; three runs, not a statistical guarantee.
No installs performed.
