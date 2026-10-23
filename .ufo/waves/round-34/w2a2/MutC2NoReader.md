# MutC2NoReader — C2 no-reader/junk controls (chousa r34 attempt 2, wave 2)

**Seat** MutC2NoReader (mutation-tester), 2026-10-23. **Lane** `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
tip `707da818…f5` (frozen). **Gate** `tools/research-gate.sh` sha256
`a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` — measured at start and again after
all runs; identical. **Counter** `corpus/evidence/round34/c2-count.py` sha256
`8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`, used unmodified; every receipt below
records that `counter_sha256`. The counter strips every `CHOUSA_*` variable from the gate environment.

## What I did

1. Copied the landed gate to scratch (367,700 B, sha256 re-verified `a6307edf…2995b`) and built **seven control
   gates** as copies: five assigned controls (a)–(e), plus two supplements (a0, f). **One injected block per gate**,
   placed immediately after `token_matcher_require || return 2` in `verify_claims`
   (`tools/research-gate.sh:1699`); nothing else changed. `bash -n` clean on all seven. Each block reads **only the
   claims file** through the gate's own helpers (`jfield`, `json_unescape`, `json_has_key`), emits one
   `CLAIM id=… expected=supported observed=<policy>` line per record, then (except a0) a synthetic warn finding and
   `RESEARCH_GATE: DRIFT`, returning 1. No block calls `tok_span_offsets*`, `tok_left_ok`, `tok_right_ok`, or opens a
   source file — a no-reader control by construction.
2. Scored each with the frozen counter, cwd = lane root, seeds **6101 and 6203** (fresh; none of
   5011/5023/5033/5047), receipts into my wave dir. Representative command (identical per control/seed):
   `LC_ALL=C C2_TMP=/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2NoReader/tmp timeout 1800 python3 corpus/evidence/round34/c2-count.py --gate /fast/scratch/hyaku/chousa-r34-a2/w2/MutC2NoReader/ctl/ctl-a.sh --seed 6101 --receipt .ufo/waves/round-34/w2a2/MutC2NoReader/ctl-a-s6101.json`
   — counter exit 1 (predicate false) for every control run; exit 0 for the baseline runs.
3. **Detector positive control:** landed gate on the same counter and seeds →
   `DEADZONE_MATCH=37/37` both seeds, `predicate_holds=true`, counter exit 0
   (`base-landed-s6101.json`, `base-landed-s6203.json`). A control miss below is therefore a label-policy
   rejection, not detector malfunction.
4. **No-reader proof:** kept fixture (`--keep …/keep-a`, seed 6101) and ran both gates on the identical claims under
   `strace -f -e trace=openat`: the landed gate opens **37** files under `keep-a/src/` (base_rc=1); control a opens
   **0** (ctla_rc=1; the only fixture path it opens is `keep-a/claims.jsonl`). Logs stay in scratch:
   `/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2NoReader/strace-base.log` sha256 `aafb1ea749c9f09e…df3faf` (487,483 B),
   `…/strace-a.log` sha256 `66b441a06214fc82…3b7d7` (22,424 B).

## Scores (frozen counter, `TOTAL=37`)

| # | Control label policy | Gate sha256 | seed 6101 | seed 6203 | Verdict |
|---|---|---|---|---|---|
| a | every CLAIM `observed=supported` | `be439e6d673d6287…` | **14/37** | **14/37** | MISSES (killed) |
| b | every CLAIM `observed=unsupported` | `3b34e55f80d83b59…` | **19/37** | **19/37** | MISSES (killed) |
| c | random label uniform over {supported,unsupported,mislocated} | `733f0481f32157e2…` | **14/37** | **11/37** | MISSES (killed) |
| d | no CLAIM lines at all, exit 1 DRIFT | `89a00c1dd111e132…` | **0/37** | **0/37** | MISSES (killed) |
| e | mislocated iff a `"line"` field is present, else supported | `77fb6a4b3497e2c5…` | **16/37** | **16/37** | MISSES (killed) |
| a0 | supplement: same as (a) but `RESEARCH_GATE: CLEAN`, exit 0 | `0e9a55257d61cda5…` | **0/37** | **0/37** | rejected on rc/DRIFT |
| f | supplement: complement of (e), else **unsupported** | `d73402b27b365493…` | **23/37** | **23/37** | MISSES |

Full hashes: a `be439e6d673d6287f5ee08120a61594f627a81d17b8181b7b6ee8c62c7b9f982`, b
`3b34e55f80d83b5906ec1b68920f3b0ff75e8e7f4c418544459ef7f28ef2ed69`, c
`733f0481f32157e2c20a0c1f564274740ed5e9e78d1cc14a77b0f4527dd82941`, d
`89a00c1dd111e132b106ac29b8275693fc6221aa3184647cb89a7b0532582079`, e
`77fb6a4b3497e2c581ca5404b7ba693ca71782eb7d5917532e64111582cdf81d`, a0
`0e9a55257d61cda599990dc6ca91b421c2cbf2cd50a737b622a75c80efc70d51`, f
`d73402b27b3654938c078b4a92d198d14053edd880809e0270e5fc7f3fb84fd8`.

### Per-class lines (nonzero classes; every unlisted class is 0/n; full 17-row map in each receipt)

- **a** (both seeds): `dz-verbatim-ml 3/3, dz-verbatim-1l 2/2, dz-edge 2/2, dz-decoys-exact 2/2,
  dz-glued-then-valid 1/1, dz-line-bound 2/2, short-verbatim 2/2` = the **14 supported-truth** records.
  All 19 unsupported-truth and all 4 mislocated-truth records miss.
- **b** (both seeds): `dz-mut-head 2/2, dz-mut-tail 2/2, dz-mut-center 2/2, dz-decoys 5/5, dz-split 2/2,
  dz-glued-left 2/2, dz-glued-right 2/2, short-mut 2/2` = the **19 unsupported-truth** records.
  The 14 supported and 4 mislocated miss.
- **c** seed 6101: `dz-decoys 3/5, dz-edge 1/2, dz-glued-left 1/2, dz-line-bound 1/2, dz-mut-center 2/2,
  dz-mut-tail 1/2, dz-verbatim-1l 1/2, dz-verbatim-ml 2/3, short-mut 1/2, short-verbatim 1/2` (14). Seed 6203:
  `dz-decoys 3/5, dz-glued-left 1/2, dz-line-bound 1/2, dz-mut-center 1/2, dz-split 2/2, dz-verbatim-1l 2/2,
  short-verbatim 1/2` (11). The difference is expected: ids are per-seed and the label is a hash of the id.
- **d**: no CLAIM line; the counter records `observed=none` for all 37 (`receipt gate_rc=1`).
- **e** (both seeds): the 12 no-line supported records + `dz-decoys-line-wrong 2/2, dz-line-wrong 2/2` = 16.
  `dz-line-bound` is **0/2** (line present → labelled mislocated, truth supported); all 19 unsupported miss
  (no line → labelled supported).
- **f** (both seeds): all 19 unsupported-truth records + `dz-decoys-line-wrong 2/2, dz-line-wrong 2/2` = 23.
  The 14 misses are exactly the 12 no-line supported records + `dz-line-bound 2/2`.

## Why the counter let none through — and the highest it could be pushed

The frozen rule (`c2-count.py:351`) is per-record equality plus finding coupling:
`ok = obs == t and ((cid in f_line) == (t == "mislocated"))`, and the predicate (`:370`) is exact
`matched == TOTAL`. A run is scored only if the gate exits **1** and prints a `RESEARCH_GATE: DRIFT` line
(`:335-336`); a duplicated id becomes `none` (`:346-347`).

The committed class table (`CLASS_COUNTS`, `:71-88`) gives the hidden truth: **14 supported / 19 unsupported /
4 mislocated** over 37 records, and `build()` (`:184-260`) attaches a `"line"` field to 6 records
(`dz-line-bound` 2 supported; `dz-decoys-line-wrong` 2 + `dz-line-wrong` 2 mislocated). Therefore:

- (a) captures exactly the 14 positive labels; the other 23 are indistinguishable without reading span bytes.
- (b) captures exactly the 19 negative labels (the majority class) — 19/37 is the majority-guess ceiling, not a leak.
- (c) is label noise: 11–14/37.
- (d) produces no labels; 0/37.
- (e) pays 19 unsupported (labelled supported) + 2 line-bound (labelled mislocated) to collect 16.
- **f** is the optimal policy that sees only the binary `"line"`-presence partition: 31 no-line records
  (12 supported + 19 unsupported) → label unsupported gives 19; 6 line records (2 supported + 4 mislocated) →
  label mislocated gives 4; total **19 + 4 = 23**. Exact equality still kills it by 14, and those 14 are precisely
  the records whose truth requires reading the span (12 no-line supported: verbatim/decoys-exact/glued-then-valid/
  short-verbatim; plus the 2 line-bound supported). [INFERENCE: optimality within the binary line-presence
  partition follows arithmetically from the class counts; other metadata keys (file size, names, mtimes) are the
  sibling MutC2Keyed seat's surface and were not tested here.]
- (a0) shows the **rc/DRIFT filter is load-bearing**: the same all-supported labels with `CLEAN`/exit 0 score 0/37
  (every record `none`). A junk gate cannot avoid being scored by exiting clean.

**Most important finding:** **no assigned control MEETS 37/37**; the best assigned score is (b) **19/37**, the best
no-reader variant I built from record metadata alone (f) is **23/37**, and the counter's rejection is the frozen
rule working as specified (three-label hidden truth, exact equality, finding-set coupling, rc==1 + DRIFT,
duplicate→none). I found no counter bug: every receipt except the two landed-gate baselines reports
`predicate_holds=false`, and no control printed 37 matches.

## Role fields

- **Mutant:** seven scratch copies of the landed gate, distinguished only by the injected block
  (`ctl-a.sh`, `ctl-b.sh`, `ctl-c.sh`, `ctl-d.sh`, `ctl-e.sh`, plus supplements `ctl-a0.sh`, `ctl-f.sh`); hashes above.
- **Expected detector:** `c2-count.py` (sha `8c0def4d…12173`), predicate `DEADZONE_MATCH=37/37`; positive control
  37/37 on seeds 6101 and 6203.
- **Output:** table and per-class lines above; raw stdout/stderr retained per run (`ctl-*-s*.out`), receipts
  (`ctl-*-s*.json`) with `gate_sha256` equal to my control copies (asserted).
- **Verdict:** (a), (b), (c), (d), (e) **killed / MISSES**; supplement (f) **MISSES (23/37)**; supplement (a0)
  **rejected on rc** (0/37).
- **Restoration evidence:** the lane was never mutated — `tools/research-gate.sh` sha256 is
  `a6307edf…2995b` at start and after all runs; `c2-count.py` sha256 unchanged `8c0def4d…12173`; all writes went to
  `/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2NoReader/` and
  `.ufo/waves/round-34/w2a2/` (my artifact dir `MutC2NoReader/` plus this report) only. No lane production file,
  jj state or Git index touched.

## Artifacts

Wave dir `.ufo/waves/round-34/w2a2/MutC2NoReader/` (2.7 MB total, no file > 1 MiB): control gates above,
16 receipts (`base-landed-s{6101,6203}.json`, `ctl-{a0,a,b,c,d,e,f}-s{6101,6203}.json`), 15 `.out` transcripts
(the first baseline printed to the shell, not a file).
Scratch: `/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2NoReader/` (base gate + sha, `ctl-sha256.txt`, kept fixture
`keep-a/`, strace logs).

## Limits

- Two fresh seeds per control; (c) is seed-dependent by design (14 vs 11).
- Controls are **label-policy** probes and never exercise the span matcher; matcher-level controls (windows,
  halves, truncation, keyed shortcuts) are other wave-2 seats. The 23/37 figure is measured for the line-presence
  policy on this frozen fixture, not a general bound over all possible metadata keys.
- The synthetic warn finding + DRIFT line is deliberate (without it an all-supported gate exits 0 and scores 0/37,
  as a0 shows); it is part of the mutant construction, not a claim about the landed gate.
- The strace contrast ran on a kept fixture outside the live harness; both gates received identical
  `claims.jsonl`/`--root` inputs.
- No network, no installs, no subagents; all commands bounded (`timeout ≤ 1800 s`).
