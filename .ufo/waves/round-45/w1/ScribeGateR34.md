# ScribeGateR34 — SKILL.md Gates row for round-34 v1/v2 counters

Lane: chousa-shokunin, round 45 wave 1. My id: L1Chousa45.ScribeGateR34.
Item: draft the Gates row for round 34's gate entry points
`corpus/evidence/round34/c1-count.py` (design v1) and
`corpus/evidence/round34/c1-count-v2.py` (design v2). Read-only run; no lane
production file touched; report written at this path only.

## Evidence read

- `SKILL.md` `## Gates` rows (lines 75-99) for column conventions.
- `corpus/evidence/round34/claims.md`: design v1 (C1/P1, TOTAL 30), design v2
  (TOTAL 40), design v3 (TOTAL 42, successor), erratum (lines 194-212).
- `SCORECARD.md` round-34 verdict (lines 1918-1946): C1 verdict
  `unverified (required controls held)`; base `LONGSPAN_MATCH=25/42`
  (`LC_ALL=C`), 0/42 ×2 by the 1500 s bound in UTF-8; v3 42/42 on landed gates.
- `corpus/lessons/round-34.md`: v1 rejected for shoulder bands left unexamined
  (CritC1Shapes), v2 rejected for case-/order-/whitespace-blind blindness, before
  data; v1/v2 "kept frozen and superseded".
- Both counters' docstrings + `main()`: exit 0 iff `matched == TOTAL`, else 1;
  2 harness error (gate missing, temp dir, fixture generation, `--keep`/`--receipt`
  IO). Default `--gate tools/research-gate.sh`, `--seed` random, `--receipt`/`--keep`
  None (no lane writes without them). Fixtures in `C1_TMP`/`TMPDIR`, removed in
  `finally`; gate run bound 1500 s per run; env strips `CHOUSA_*`.

## Commands run (lane root, LC_ALL=C, no --receipt/--keep)

```
$ LC_ALL=C python3 corpus/evidence/round34/c1-count.py --seed 7001; printf 'EXIT=%d\n' $?
LONGSPAN_MATCH=30/30
  long-verbatim-ml 3/3
  long-verbatim-1l 2/2
  long-edge 2/2
  long-mut-head 2/2
  long-mut-tail 2/2
  long-mut-mid 3/3
  long-split 2/2
  long-glued-left 2/2
  long-glued-right 2/2
  long-line-bound 2/2
  long-line-wrong 2/2
  short-verbatim 3/3
  short-mut 3/3
EXIT=0
Wall time: 9.89 seconds
```

```
$ LC_ALL=C python3 corpus/evidence/round34/c1-count-v2.py --seed 7002; printf 'EXIT=%d\n' $?
LONGSPAN_MATCH=40/40
  long-verbatim-ml 3/3
  long-verbatim-1l 2/2
  long-edge 2/2
  long-mut-head 2/2
  long-mut-tail 2/2
  long-mut-center 2/2
  long-decoys 7/7
  long-decoys-exact 2/2
  long-decoys-line-wrong 2/2
  long-split 2/2
  long-glued-left 2/2
  long-glued-right 2/2
  long-line-bound 2/2
  long-line-wrong 2/2
  short-verbatim 3/3
  short-mut 3/3
EXIT=0
Wall time: 20.45 seconds
```

Environment pinned: lane HEAD `d82cec904bf0fb8736886b9f17be913c7807427a`; gate
default `tools/research-gate.sh` sha256 `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`.
No install/update performed.

## Draft row (verbatim, one line, 8 cells)

```
| research-gate round-34 v1/v2 counters | gate | `python3 corpus/evidence/round34/c1-count.py` · `python3 corpus/evidence/round34/c1-count-v2.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`) | v1 `LONGSPAN_MATCH=30/30` · v2 `LONGSPAN_MATCH=40/40` exit `0`; any other count exit `1`; harness error exit `2`; both superseded before data by `corpus/evidence/round34/c1-count-v3.py` (design v3, TOTAL 42) — v1 rejected (shoulder bands unexamined, CritC1Shapes), v2 rejected (no class distinguishes case-/order-/whitespace-blind compare). Observed on the current gate (HEAD `d82cec904`, gate sha256 `2cb04bdd…`): v1 30/30 seed 7001 rc 0; v2 40/40 seed 7002 rc 0 | before on the round-33 gate `43a1af35`: v1 19/30 (seed 3401, `.ufo/waves/round-34/controls/L1-base/`, only committed v1 receipt); v2 base do-nothing never committed (v2 superseded by v3 before those runs); v3 base on the same gate 25/42 (`LC_ALL=C`), 0/42 ×2 by the 1500 s bound (UTF-8) | contract `corpus/evidence/round34/claims.md` (design v1/v2; frozen predicates P1/P1 v2, kill rules v1/v2; v1 commit `70feb5ea`, v2 commit `ef16afb1`) | temp dirs only (`C1_TMP` or `TMPDIR`); no network; writes a receipt only when `--receipt` is given | chousa |
```

## Verdict

- Both counters are live, self-contained gate checks: observed 30/30 (v1, seed
  7001) and 40/40 (v2, seed 7002), exit 0, on the current gate — the round-34
  fix has landed, so the frozen PASS values now hold.
- Both were superseded before data by `c1-count-v3.py` (design v3, TOTAL 42);
  the row's verdict map says so with the successor path, per the existing v3
  row's "v1/v2 counters kept frozen and superseded" note.
- Historical failing control: v1 `19/30` on the round-33 base gate `43a1af35`
  (seed 3401, committed at `.ufo/waves/round-34/controls/L1-base/`). v2's base
  do-nothing was never committed (v2 replaced by v3 before those runs — claims.md
  erratum); the closest committed failing numbers on the same base gate are v3's
  `25/42` (`LC_ALL=C`) and `0/42` ×2 (UTF-8 timeout).
- Exit contract confirmed from code: 0 iff `matched == TOTAL`; 1 any other count;
  2 harness error (gate missing / temp-dir / generation / `--keep`-`--receipt`
  IO).

## Pointers

- `corpus/evidence/round34/claims.md:55-59` (P1 v1, TOTAL 30), `:112-129`
  (v2, TOTAL 40), `:150-165` (v3, TOTAL 42), `:194-212` (erratum: v2 base
  never run; v1 receipt only 19/30).
- `SCORECARD.md:1927` (C1 row: base 25/42 → 42/42, verdict unverified).
- `corpus/lessons/round-34.md:15-20,35` (v1/v2 rejection, locale note).

Scratch: none created.
