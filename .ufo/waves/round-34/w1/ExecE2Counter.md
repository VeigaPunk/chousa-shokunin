# ExecE2Counter — repair E2 (per-seed confuser counter for the round-33 reader)

Routed repair E2: `corpus/lessons/round-33-verifier-spotcheck.md:163-166` (QUALITY 40).
Seat: `ChousaR34.ExecE2Counter`, round 34, wave 1. Date: 2026-10-23.

## What I built

`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/ExecE2Counter/c1-count-v3.py`
— SHA-256 `bd81aeea199c460be3afbec0f15116b5ddfe8330b45f35b37568d1665e43d9cc`, 486 lines.

Derived from the round-33 counter `corpus/evidence/round33/c1-count-v2.py`
(SHA-256 `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`,
**unmodified** — re-verified after all runs). The diff is 7 hunks:

* **Docstring** rewritten as a raw string (`r"""`) with a new leading section that
  states exactly what changed in v3 (the v1/v2 history is kept below it).
* **The six fixed `CONFUSERS` literals are gone.** `gen_confusers(rng)` draws six
  confuser strings **per seed** (`c1-count-v3.py:99-127`). Each generated
  confuser carries: all six structural characters `{ } [ ] : ,` (in a per-seed
  random order, plus random repetitions); a `"` (JSON-escaped); a `\` (JSON-escaped)
  and, for one slot per seed, that escaped backslash **immediately before the
  closing quote**; a non-ASCII character written as a `\uXXXX` escape by the new
  `JC()` encoder (`ensure_ascii=True`, `c1-count-v3.py:184-187`); and text that
  looks like a member — `"line":"<digits>"`, with the literal digits `7` in slot 0.
* **`Gen.__init__` draws the confusers** (`c1-count-v3.py:163-165`), so they are
  seed-bound and unreachable by a literal-keyed shortcut.
* **`S1_flat_confusers` and `S2_nested_confusers` consume the generated strings**
  via `JC()` in the flat position and the nested position respectively
  (`c1-count-v3.py:322-334`).
* **Receipt schema bumped** to `chousa-r34-c1-receipt/v3` (`c1-count-v3.py:467`).

Unchanged, as required: the 15 classes, the sub-variant counts, `TOTAL = 156`
(asserted at import), the per-record match rule, the label `TOPLEVEL_FIELD_MATCH`,
the exit convention, and the gate invocation.

Fixture check (`generate()` on seed 9401): 156 records, every row valid JSON
(`json.loads` per row passes), 12 `S1_flat_confusers` + 6 `S2_nested_confusers`
records, per-seed confusers distinct between seeds (fixture sha `713ba9dd…` for
9401 vs `49506598…` for 9404) and reproducible for a given seed (verified
deterministic=True for 9401/9402/9404).

## Scores (receipts in this directory; counter sha in every receipt = `bd81aeea…`)

Scored in the mandated order. Command form used in every run:

```
C1_TMP=/fast/scratch/hyaku/chousa-r34/w1/ExecE2Counter \
python3 .ufo/waves/round-34/w1/ExecE2Counter/c1-count-v3.py \
  --gate <gate> --seed <n> --receipt <dir>/<name>.json
```

| # | gate | gate sha256 (prefix) | seed | label | predicate_holds | receipt | utc |
|---|------|------|------|-------|-----------------|---------|-----|
| 1 | mask gate (`.ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh`) | `ae7d4bfc7ac1` | 9401 | `TOPLEVEL_FIELD_MATCH=155/156` | false | `mask-s9401.json` | 2026-10-23T11:23:04Z |
| 1 | mask gate (same file) | `ae7d4bfc7ac1` | 9402 | `TOPLEVEL_FIELD_MATCH=155/156` | false | `mask-s9402.json` | 2026-10-23T11:23:04Z |
| 2 | round-32 base gate (`git show 2b9cc73a:tools/research-gate.sh`) | `f4731885ac0f` | 9403 | `TOPLEVEL_FIELD_MATCH=60/156` | false | `r32-s9403.json` | 2026-10-23T11:25:19Z |
| 3 | landed round-33 gate (`git show b805390…:tools/research-gate.sh`) | `43a1af35ca66` | 9404 | `TOPLEVEL_FIELD_MATCH=156/156` | **true** | `r33-s9404.json` | 2026-10-23T11:25:39Z |
| 3 | landed round-33 gate (same file) | `43a1af35ca66` | 9405 | `TOPLEVEL_FIELD_MATCH=156/156` | **true** | `r33-s9405.json` | 2026-10-23T11:25:39Z |

Receipt utc order is strictly ascending across the three steps
(11:23:04 → 11:23:04 → 11:25:19 → 11:25:39 → 11:25:39); the two parallel pairs
share a utc second because they ran concurrently. All five gate runs exited 1
with a `RESEARCH_GATE: DRIFT` line; no run timed out (`gate_timed_out=false`).
The landed gate's sha256 was independently confirmed against the working tree
(`sha256sum tools/research-gate.sh` → `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`).

### Per-class lines

**Mask gate, seed 9401 and seed 9402 (identical):** 155/156; every class full
except `S2_nested_confusers 5/6`. The single miss per seed is a nested-confuser
record: truth `supported`, observed `invalid`.

```
N1_nested_line_decoy 12/12        N7_nested_source_decoy_sup 6/6
N2_nested_line_only 12/12         N8_nested_source_decoy_uns 6/6
N3_top_line_wrong_nested_right 12/12   N9_nested_id_decoy 6/6
N4_nested_sha_decoy 12/12         N10_nested_span_decoy 6/6
N5_nested_sha_only 12/12          N11_nested_marker_expect_decoy 6/6
N6_top_sha_stale_nested_right 12/12    D1_duplicate_top_level 24/24
S1_flat_confusers 12/12           S2_nested_confusers 5/6
F1_flat_plain 12/12
```

**Round-32 base gate, seed 9403:** 60/156.

```
N1 6/12   N2 0/12   N3 6/12   N4 6/12   N5 0/12   N6 6/12
N7 3/6    N8 3/6    N9 3/6    N10 3/6   N11 0/6   D1 0/24
S1_flat_confusers 12/12   S2_nested_confusers 0/6   F1_flat_plain 12/12
```

The base gate misses the whole top-level/nested separation (nested decoys are
read as the record's own fields) and refuses no duplicate key — the round-33
reader is what the round-32 gate lacks.

**Landed round-33 gate, seeds 9404 and 9405 (identical):** 156/156, all 15
classes full, `misses: []` in both receipts.

```
N1 12/12  N2 12/12  N3 12/12  N4 12/12  N5 12/12  N6 12/12
N7 6/6    N8 6/6    N9 6/6    N10 6/6   N11 6/6   D1 24/24
S1_flat_confusers 12/12   S2_nested_confusers 6/6   F1_flat_plain 12/12
```

## Verdict

* **The mask gate misses: 155/156 on both fresh seeds, not 156/156.** The
  per-seed confusers defeat it, which is the point of E2. The mechanism is
  direct: `mask-gate.sh` masks the six **fixed** round-33 literals and then
  strips nested `{...}`/`[...]` by regex, which breaks the JSON. Reproduced
  locally by applying that gate's own `json_mask_strip` helper to a kept
  fixture: for the failing record `c07edfd9750` the stripped text is
  `{"id": "c07edfd9750", ..., "nayorivi": ] \"line\":\"060\" ...` and
  `json.loads` raises `Expecting value: line 1 column 58 (char 57)` — the
  confuser's braces are now structural to the stripper, so the record is read
  as malformed (`observed=invalid`) instead of `supported`. The round-33
  counter with the fixed literals scored the same gate 156/156
  (`.ufo/waves/round-33/w2/L1ShortcutMask/mask-s3391.json`, `matched: 156`);
  the v3 counter scores it 155/156. **The counter is not wrong: it missed, as
  required.**
* **Round-32 base gate: 60/156** — the top-level reader's absence is visible.
* **Landed round-33 gate: 156/156 on two fresh seeds, `predicate_holds=true`,
  no misses.** The rule the lane already holds still holds on new inputs, now
  with confuser content no fixture can pre-mask.

## Limits and notes

* This is repair work (quality), not a claim: E2 re-scores a rule the lane
  already holds on new inputs. The v3 counter makes no new claim and the
  round-34 C1 predicate (`LONGSPAN_MATCH`, `corpus/evidence/round34/c1-count.py`)
  was **not** touched or run by this seat.
* The v3 counter file lives in this seat's directory only; it is not committed
  and not on the lane's production path. The L1 decides whether it is committed
  (and where).
* No installs were performed; no tooling was needed beyond the system `python3`
  and `bash`.
* Everything written by this seat is under
  `.ufo/waves/round-34/w1/ExecE2Counter/` (116 KB) plus scratch gate copies
  under `/fast/scratch/hyaku/chousa-r34/w1/ExecE2Counter/`. No lane production
  file, Git index, or jj state was modified; the only `git` commands used were
  read-only (`show`, `cat-file`, `status`, `rev-parse`, `log`).
* Fresh seeds 9401–9405 were used (none in 3401–3409, none previously present
  in the round-32/33 receipts).
