# RerunSeedSweep31 — seed sweep of C1/C2 counters on the landed gate (round 31, wave 2 falsify)

**Seat:** RerunSeedSweep31 (leaf). **Lane:** `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
**Target:** both round-31 counters over many fresh seeds on the landed tip gate.
**Verdict: the seed-sweep attack FAILS to break C1 or C2 — both hold at 120/120 on every seed run.**

## What was attacked

P1/P2's kill rule is "any run of the frozen counter on the landed revision below 120/120 is a
miss". Wave 1 measured 4 (C1) + 2 (C2) seeds. The open attack was **seed-dependent miss**: a
gate defect that only shows up on particular fixture draws (the v1→v2 history is exactly this
class of leak). I ran **25 fresh random 63-bit seeds per counter on the landed tip gate**
(sequential, `timeout 900` each), then **5 adversarial edge seeds** per counter
(`0`, `1`, `2`, `-1`, `9223372036854775807`), i.e. 60 counter runs / 7200 scored claims.

## Environment and provenance (what was actually run)

- Lane tip `ee1024fd492144c9c7b315890fac247543c37208`; working tree clean for the gate and counters
  (`git status --porcelain` shows only pre-existing wave-dispatch/untracked wave files).
- **Gate:** `tools/research-gate.sh`, SHA-256 `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c`
  — identical to `git show HEAD:tools/research-gate.sh` (byte-identical to the landed C2 build).
- **Counters (frozen, unmodified):**
  - `corpus/evidence/round31/c1-count.py` SHA-256 `c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`
  - `corpus/evidence/round31/c2-count.py` SHA-256 `1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500`
  Both hashes are the ones recorded in **every** receipt I produced (`counter_sha256`), and both
  equal the blobs at HEAD — the counters were never edited, re-scaled, or re-run with a modified copy.
- **Command shape** (from lane root, default gate): `python3 corpus/evidence/round31/c1-count.py --seed S --receipt <path>`
  (and `c2-count.py` likewise), each wrapped in `timeout 900`. `C1_TMP`/`C2_TMP` pointed at
  `/fast/scratch/hyaku/chousa-r31/w2/RerunSeedSweep31/tmp` so no fixture was written into the lane.
  Driver script: `/fast/scratch/hyaku/chousa-r31/w2/RerunSeedSweep31/sweep.sh` (scratch dir, outside the lane).
- No network was used. No lane production file, counter, or gate byte was written or mutated; the
  only lane writes are this report and the receipt directory named below. No git/jj write commands.

## Results — min/max per counter

| Counter | Runs | Seeds | Matched (min–max) | `predicate_holds` | gate exit | timeouts | min/max elapsed |
|---|---|---|---|---|---|---|---|
| C1 `c1-count.py` | **25** (fresh random) | see list below | **120/120 – 120/120** | `true` × 25 | 1 × 25 | 0 | 2 s / 4.5 s |
| C2 `c2-count.py` | **25** (fresh random) | same list | **120/120 – 120/120** | `true` × 25 | 1 × 25 | 0 | 2 s / 3.4 s |
| C1 edge seeds | 5 | 0, 1, 2, -1, 2^63-1 | 120/120 – 120/120 | `true` × 5 | 1 | 0 | ≤ 3 s |
| C2 edge seeds | 5 | 0, 1, 2, -1, 2^63-1 | 120/120 – 120/120 | `true` × 5 | 1 | 0 | ≤ 3 s |

**Minimum over the required 25-seed sweep: C1 = 120/120, C2 = 120/120. No seed-dependent miss was observed.**
Total: 60 runs, 7 200 scored claims, zero `misses` arrays non-empty, zero `gate_timed_out`,
zero `gate_rc` outside {1}. Gate exit 1 is the gate's normal "findings present" exit (every
fixture contains mislocated/stale claims by construction), which the counter accepts.

**Per-class stability.** In all 25 fresh-seed runs of each counter every class scored full marks
(25/25 runs at 12/12, 6/6 or 8/8 per class): C1 classes `B1_bound_single`, `B2_bound_later_occurrence`,
`B3_bound_multiline`, `B4_no_line`, `M1_other_line`, `M2_glued_on_named_line`, `M3_partial_on_named_line`,
`M4_multiline_wrong_range`, `M5_beyond_eof`, `M6_two_occurrences_named_third`, `I1_invalid_line_value`,
`U1_absent_span_with_line`; C2 classes `I1_invalid_sha_value`, `S1_one_byte_elsewhere`,
`S2_newline_variant`, `S3_hash_of_span_only`, `S4_mismatch_span_absent`, `S5_hash_of_other_fixture_file`,
`N1_no_sha`, `R1_match_span_present`, `R2_match_span_absent`. Because design v2 fixes the sub-variant
counts per class, a seed can no longer hide a sub-variant — which is why the class breakdown is
identical run to run.

**Seeds used (25 fresh, `random.Random()` 63-bit draws, recorded):**
3124003431557629926, 589450002006086336, 5035091403707185420, 4525330808182335870, 6290151394080929418,
8522483765797083657, 2808214540069432895, 6079138878409438466, 9182903166710780520, 2666203639785728712,
9054989464849137080, 4655839856917744676, 4728614869853425529, 8405196813752353997, 778037652735908233,
1087086264303834914, 6732791429905389453, 7175255452424077416, 8337926518390153946, 2142254154870781923,
897601251128756333, 5133071812884211478, 4226871115244534267, 2773100747543570120, 3080346373295396764.

## Receipt paths (all kept, all inside the seat's falsify dir)

- C1, 25 fresh seeds: `.ufo/waves/round-31/falsify/RerunSeedSweep31/c1-seed-<seed>.json`
  (e.g. `.ufo/waves/round-31/falsify/RerunSeedSweep31/c1-seed-3124003431557629926.json`)
- C2, 25 fresh seeds: `.ufo/waves/round-31/falsify/RerunSeedSweep31/c2-seed-<seed>.json`
- Edge seeds, 10: `.ufo/waves/round-31/falsify/RerunSeedSweep31/edge-c{1,2}-seed-{0,1,2,-1,9223372036854775807}.json`
- Per-run stdout/stderr logs: same directory, `<prefix>-seed-<seed>.log`

Each receipt carries `schema`, `counter_sha256`, `gate`, `gate_sha256`, `seed`, `utc`, `elapsed_s`,
`gate_rc`, `gate_timed_out`, `total`, `matched`, `label`, `predicate_holds`, `per_class`, `misses`.

## Supporting checks (falsification hygiene)

1. **The sweep is not a no-op sweep — the fixtures really differ per seed.** Re-generating with
   `--keep` for two different seeds produced different `claims.jsonl`:
   `df9b85f1f5f93ba30d330b0e10aa8ae006e60ce4b8a97fcaca101e09f7f27c77` (seed 12345) vs
   `434092ad9ce325de144300a7437dac7f6c3c09330f2d295848b8d2d51c5939e9` (seed 999999999); both 120
   claims / 120 opaque source files. [INFERENCE] 120/120 on 25 distinct fixtures is evidence of
   correctness across draws, not a repeated identical run.
2. **No lower count anywhere in round 31 on this revision.** Re-reading the L1 receipts under
   `.ufo/waves/round-31/measure/`: `after-c1-run1/2` (gate `3b5279eb…`) 120, `after-c1-run3/4-tip`
   and `after-c2-run1/2` (gate `c23d7537…`) 120, `sep-c2-on-c2only` 120. The only sub-120 receipts
   are the separability controls (`sep-c1-on-c2only` 50/120, `sep-c2-on-c1only` 50/120), which run
   the counter against the *other* build's gate and are not runs on the landed revision.
   Combining: 55 distinct on-tip/on-landed-gate runs at 120/120, 0 below.
3. **Counter integrity.** `counter_sha256` in every receipt equals the HEAD blob hash of the
   frozen counter; no receipt was produced by a modified counter.
4. **Edge seeds.** `0`, `1`, `2`, `-1` and `2^63-1` are all handled (the counter passes the seed
   straight into `random.Random`, so `-1` and huge ints are exercised); all 120/120.

## Limits and non-claims

- Scope is exactly the assignment: both counters, many fresh seeds, landed tip gate. I did **not**
  re-run the `--selftest`, `verify-claims`/`verify-chain` no-harm observables, or the controls — those
  are other seats' scope (and the L1 receipts already carry them).
- The sweep covers the counters' *own* fixture space (fixed class/sub-variant counts). A defect
  outside that space (a class the counter never draws, e.g. a source file with CRLF endings for C1,
  or a `"line"` value on a claim whose span is multi-line-with-CRLF) is **not** covered by this
  evidence and remains open.
- 25 seeds bound statistical power: a defect requiring a rare draw (< ~4% per class-item) could
  still hide. Because v2 fixes sub-variant counts, per-class coverage is already complete, so the
  residual risk is in *interaction* draws (specific line positions, specific byte edits), not in
  missing sub-variants.
- No network, no installs, no tool upgrades performed (nothing needed; `python3` and `bash` only).

**Verdict:** the seed sweep does not break C1 or C2. Minimum = maximum = 120/120 for both counters
over 25 fresh seeds on the landed gate (and over 5 adversarial edge seeds). P1 and P2 survive this
attack on their "no run prints a lower count" clause. Smallest correction needed: **none** — no
defect was found, so no fix is proposed. The only residual named limit is fixture-space coverage
described above.
