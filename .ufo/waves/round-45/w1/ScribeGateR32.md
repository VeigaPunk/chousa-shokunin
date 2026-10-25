# ScribeGateR32 — draft SKILL.md Gates row for round-32 v1 counters

Item: draft the missing Gates row for the round-32 **v1** gate entry points
(`corpus/evidence/round32/c1-count.py`, `corpus/evidence/round32/c2-count.py`), the counters the
existing `research-gate round-32 counters` row (v2/v3) superseded. Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `d82cec904bf0fb8736886b9f17be913c7807427a`
(round-45 freeze), gate `tools/research-gate.sh` SHA-256 `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`.

## Evidence read

- `corpus/evidence/round32/claims.md` — v1 predicates/contracts: P1 `APPEND_SERIALIZED=24/24`
  (TOTAL 24, L 12 + F 12), P2 `EXEMPT_AUDIT_MATCH=120/120` (TOTAL 120, 14 classes). v1 committed at
  `4111607c` (attempt 1, died before any seat); v2 `3d586d3a` after the pre-data control wave.
- `corpus/evidence/round32/c1-count.py` docstring/argparse: `--gate` (default `tools/research-gate.sh`),
  `--seed`, `--receipt`; exit 0 iff matched == 24, 1 otherwise, 2 harness (incl. no `/proc/locks`).
- `corpus/evidence/round32/c2-count.py` docstring/argparse: `--gate`, `--seed`, `--receipt`,
  `--keep`; exit 0 iff matched == 120, 1 otherwise, 2 harness. (v1: no record checks, 120 hops;
  finding set = `{CHAIN_EXEMPT_RESOLVABLE}` for truth resolvable, empty otherwise.)
- `SCORECARD.md` Round-32 verdict section (lines 1806–1826): C1 0/24 → 24/24 on final gate
  (`10f2fe12` ×18 + `f4731885` ×3); **C2 not verified** under v2 (§9 metadata-order control 132/132);
  v1 counters rejected before data because controls met them.
- `corpus/lessons/round-32.md` (lines 10–15, 31–41, 79–84): v1 rejection reasons — C1
  `CtlC1PartialLockB` probe-only lock 24/24 on two seeds (`w1/CtlC1PartialLockB/b-s3247102{1,2}.json`);
  C2 duplicate-finding/no-verdict/clean-exit/stray-unknown outputs 120/120 (`w1/CtlC2NoisyB`,
  `w1/MutC2CounterB/frozen-*`); case-insensitive/whitespace-collapsing readers 120/120
  (`w1/CtlC2WeakReaderB/*-isolated-mutated-*`). L1 before receipts: `controls/L1-design/base-s11.json`
  (C1 8/24, seed 11), `controls/L1-design/c2-base-s21.json` (C2 84/120, seed 21). v1 counters kept as
  evidence, not counted.

## Commands run (each once, from the lane root, no `--receipt`)

```
$ python3 corpus/evidence/round32/c1-count.py --seed 321100
APPEND_SERIALIZED=24/24
  F_unterminated 12/12
  L_empty 4/4
  L_terminated 4/4
  L_unterminated 4/4
$ echo $?   → 0
```

```
$ python3 corpus/evidence/round32/c2-count.py --seed 323100
EXEMPT_AUDIT_MATCH=120/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
$ echo $?   → 0
```

Both ran against the current lane gate (`2cb04bdd…`) and print their declared PASS values with exit 0;
the supersession stands regardless (the v1 counters were rejected because *controls* met them, not
because they fail).

## Draft row (verbatim; one line, 8 cells)

```
| research-gate round-32 v1 counters | gate | `python3 corpus/evidence/round32/c1-count.py` · `python3 corpus/evidence/round32/c2-count.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`; C1 needs /proc/locks) | `APPEND_SERIALIZED=24/24` · `EXEMPT_AUDIT_MATCH=120/120` exit `0`; any other count exit `1`; harness error exit `2`; SUPERSEDED by `corpus/evidence/round32/c1-count-v2.py`/`c2-count-v2.py` (the round-32 row above) — rejected as P1/P2 counters because controls met them under design v1 (`lessons/round-32.md`) | before on the round-31 gate `0bc318b3`: 8/24 (C1, L1 do-nothing seed 11), 84/120 (C2, seed 21); the v1 counters are met by controls: `CtlC1PartialLockB` probe-only lock 24/24 (`w1/CtlC1PartialLockB/b-s3247102{1,2}.json`); duplicate-finding/no-verdict/clean-exit/stray-unknown outputs 120/120 (`w1/CtlC2NoisyB`, `w1/MutC2CounterB/frozen-*`); case-insensitive/whitespace-collapsing readers 120/120 (`w1/CtlC2WeakReaderB/*-isolated-mutated-*`) | contract `corpus/evidence/round32/claims.md` (design v1, commit `4111607c`); base gate `0bc318b3`; L1 receipts `controls/L1-design/base-s11.json`, `controls/L1-design/c2-base-s21.json`; measured 2026-10-25 on gate `2cb04bdd…` @ `d82cec90`: 24/24, 120/120, both exit 0 | temp dirs only; no network; never writes into the lane (a receipt only when `--receipt` is given) | chousa |
```

## Notes

- The existing `research-gate round-32 counters` row (SKILL.md line 89) owns the v2/v3 counters; this
  row names the v1 entry points that it supersedes.
- Observed runs printed exit 0 with full counts; verdict-map PASS values are observed, not remembered.
- No tools installed; no /tmp scratch created (counters used and cleaned their own temp dirs); no
  receipts written into the lane.
