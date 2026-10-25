# ScribeGateR33 — draft SKILL.md Gates row for round-33 gate entry points

Seat: `L1Chousa45.ScribeGateR33` (leaf). Round 45, wave 1, build + first falsifiers.

## Item

Draft ONE SKILL.md Gates row for round 33's gate entry points:
`corpus/evidence/round33/c1-count.py` (design v1) and
`corpus/evidence/round33/c1-count-v3.py` (repair E2, design v3). The -v2 counter
already has a row (`research-gate round-33 counters`, SKILL.md line 90).

## Sources read (absolute paths)

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/claims.md`
  (v1 design at lines 1-91; design v2 at lines 93-140: supersedes v1 counter,
  contract item 2, P1 and kill rule; v1 counter `ab6b2ae2…e229` stays committed and
  unedited).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py`
  (docstring/argparse: TOTAL 144, `TOPLEVEL_FIELD_MATCH`, exit 0 iff matched==144,
  1 otherwise, 2 harness; `--gate` default `tools/research-gate.sh`).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count-v3.py`
  (docstring/argparse: round-34 repair E2, derived from v2; TOTAL 156; gate run must
  exit 1 and print `RESEARCH_GATE: DRIFT`; per-seed generated confusers; receipt
  schema `chousa-r34-c1-receipt/v3`; exit 0 iff matched==156).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/SCORECARD.md` (round-33 verdict
  section lines 1866-1900; round-34 correction lines 1908-1916: the mask gate misses
  v3 on seeds 9401/9402 (155/156) but meets 156/156 on seed 61111).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-33.md`
  (v1 rejected as P1 counter before data: 3 of 7 duplicate keys, any exit accepted,
  three-key duplicate gate meets it 144/144 — lines 106-107; §9 counterexample: gate
  `ae7d4bfc` meets v2 156/156 on seeds 3391/3392 — lines 49-54; final gate
  `43a1af35`, v2 receipts seeds 3701/3702 in `measure/final/` — line 48).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md` lines 75-99 (Gates table
  header + rows; conventions copied from `research-gate round-37 counters` and
  `research-gate round-33 counters` rows).

## Commands run (from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, read-only; no `--receipt`, no `--keep`)

Command 1:

```
python3 corpus/evidence/round33/c1-count.py --seed 4701
```

Output (verbatim, trimmed):

```
TOPLEVEL_FIELD_MATCH=144/144
  N1_nested_line_decoy 12/12
  N2_nested_line_only 12/12
  N3_top_line_wrong_nested_right 12/12
  N4_nested_sha_decoy 12/12
  N5_nested_sha_only 12/12
  N6_top_sha_stale_nested_right 12/12
  N7_nested_source_decoy_sup 6/6
  N8_nested_source_decoy_uns 6/6
  N9_nested_id_decoy 6/6
  N10_nested_span_decoy 6/6
  N11_nested_marker_expect_decoy 6/6
  D1_duplicate_top_level 12/12
  S1_flat_confusers 12/12
  S2_nested_confusers 6/6
  F1_flat_plain 12/12
EXIT=0
```

Command 2:

```
python3 corpus/evidence/round33/c1-count-v3.py --seed 4702
```

Output (verbatim, trimmed):

```
TOPLEVEL_FIELD_MATCH=156/156
  N1_nested_line_decoy 12/12
  N2_nested_line_only 12/12
  N3_top_line_wrong_nested_right 12/12
  N4_nested_sha_decoy 12/12
  N5_nested_sha_only 12/12
  N6_top_sha_stale_nested_right 12/12
  N7_nested_source_decoy_sup 6/6
  N8_nested_source_decoy_uns 6/6
  N9_nested_id_decoy 6/6
  N10_nested_span_decoy 6/6
  N11_nested_marker_expect_decoy 6/6
  D1_duplicate_top_level 24/24
  S1_flat_confusers 12/12
  S2_nested_confusers 6/6
  F1_flat_plain 12/12
EXIT=0
```

The scored gate was the lane's current `tools/research-gate.sh`, sha256
`2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`.
Both counters wrote only their temp dirs (`mkdtemp` under `TMPDIR`, removed in
`finally`) — no lane writes, no receipts.

## Verdict

Both entry points hold on the current gate; exit codes and PASS prints match the
docstring contracts (v1 144/144 exit 0; v3 156/156 exit 0). v1 is superseded per
`claims.md` design v2 (by `c1-count-v2.py`, itself replaced for clause 3 by v3,
E2). The self-test cell records the failing controls: do-nothing base gate
`f4731885` 60/144 (v1) and 60/156 (v2); three-key duplicate gate meets v1 144/144
(F1); fixture-literal mask gate `ae7d4bfc` meets v2 156/156 (seeds 3391/3392) but
misses v3 155/156 on seeds 9401/9402 (meets on seed 61111 — v3 does not fully close
clause 3 per SCORECARD).

## Draft row (one line, 8 cells; insert beside the `research-gate round-33 counters` row, SKILL.md line 90)

```
| research-gate round-33 C1 v1/v3 counters | gate | `python3 corpus/evidence/round33/c1-count.py` · `python3 corpus/evidence/round33/c1-count-v3.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`) | v1 `TOPLEVEL_FIELD_MATCH=144/144` (superseded by `corpus/evidence/round33/c1-count-v2.py`, design v2, before any candidate; its control receipts stay v1-only evidence) · v3 `TOPLEVEL_FIELD_MATCH=156/156` (gate must exit 1 + `RESEARCH_GATE: DRIFT`; repair E2 replaces v2's six fixed confuser literals with per-seed generated content) · exit `0` iff holds, `1` otherwise, `2` harness | before on the round-32 gate `f4731885`: 60/144 (v1) and 60/156 (v2, duplicates 0/24); a three-key duplicate gate meets v1 144/144 (critic F1 → v2); the fixture-literal mask gate `ae7d4bfc` meets v2 156/156 (seeds 3391/3392) → v3; the mask gate misses v3 155/156 on seeds 9401/9402 but meets 156/156 on seed 61111 | contract `corpus/evidence/round33/claims.md` (design v2, commits `3b528b9a`→`e3e24ec8`); final gate `43a1af35ca668fe5…4346`; v1 controls `.ufo/waves/round-33/controls/L1-design/`; v2 receipts `.ufo/waves/round-33/measure/final/` seeds 3701/3702 | temp dirs only (keep `C1_TMP` outside the gate's lane root); receipt only when `--receipt` given; no network | chousa |
```

## Pointers

- Round-33 claims: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/claims.md:1-140`
- v1 counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py:2-42`
- v3 counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count-v3.py:2-68`
- Round-33 verdict: `/home/vgpnk/Projects/shokunin/chousa-shokunin/SCORECARD.md:1866-1900`; E2 correction `:1908-1916`
- Round-33 lessons: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-33.md:44-113`
- Existing rows: `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md:89-97`

## Scope notes

- No tools installed; no network egress; no lane/fleet writes (report only).
- Out of scope: C1/C2/C3 claim work, other rows, counter mutations.
