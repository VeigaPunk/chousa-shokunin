# MutC2KeyedBattery — round 35 w2: three more keyed engines vs the mechanism witness

Role: mutation tester (leaf, no subagents). Date 2026-10-23.
Lane repo: `/home/vgpnk/Projects/shokunin/chousa-shokunin` at wave base
`e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (siblings advanced the lane tip while
this probe ran; every score below is pinned to gate bytes `1f2fb4f5…`). Scratch
`/tmp/hyaku/chousa-r35/w2/MutC2KeyedBattery/`. No network, no installs, no
pacman, no git/jj writes; no lane file edited.

Pinned inputs (re-derived with `sha256sum`, rc=0):

| file | sha256 |
|---|---|
| `tools/research-gate.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| `.ufo/waves/round-35/repairs/base-gate.sh` | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` |
| `tools/mechanism-witness.py` (detector, unedited) | `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` |
| `corpus/evidence/round35/c2-count.py` (unedited) | `557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171` |
| `corpus/evidence/round35/c1-count.py` (unedited) | `da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3` |

## Method

Own driver `driver.py` (artifact, sha `8fed24ab…b9dc24`) copies the landed gate
into scratch and inserts one branch as the first statement of
`tok_span_offsets`' body after `local hay=$1 span=$2` — the same insertion point
`c2-count.py:patch_gate` uses, so `TOK_DIRECT_SPAN_MAX` routing is untouched.
Each keyed branch answers a long span (`${#span} > TOK_DIRECT_SPAN_MAX`, gate
`:1668`) with a python `bytes.find` exact search (identical non-overlapping,
left-to-right contract) and returns; otherwise landed code runs byte-for-byte.
The detector is the frozen witness tool itself, run exactly as `c2-count.py`
runs it (`--gate <variant> --seed N --json <receipt> --tmp <dir>`); the counter
file was not executed or edited. Every variant passed `bash -n`
(`syntax_ok=true` in receipts). Witness roots were created under my scratch
path (`…/w35wit-<seed>-<engine>/…`), which contains the string `chousa-`.

Engines built (assigned a/b/c; d is a supplementary sharpening probe, labelled):

- **A `chousa-` root** — key: `ROOT` contains the fixed prefix `chousa-`.
- **B witness-shape** — key: current record id matches `^[a-z]{1,4}[0-9a-f]{6,14}$`
  and the source basename matches the witness's own `^[0-9a-f]{16}$` or
  `^[a-z]{3,7}-[0-9]{4}$` schemes (the per-seed schemes the tool generates).
- **C idlen-mod3** — key: `${#id} % 3 == 0`.
- **D one-shot (supplementary)** — shortcut exactly one long record per fixture
  (stateless marker file under `ROOT`; `tok_span_offsets` runs inside a
  process-substitution subshell, so shell state cannot persist).
- **D2** — D plus a log line for evidence.

Commands and exit codes (all `timeout`-bounded):

```
timeout 1700 python3 driver.py --gate …/tools/research-gate.sh --battery …/tools/mechanism-witness.py \
  --seed 3539 --work …/s3539 --out …/receipt-s3539.json          # rc=0
timeout  900 python3 driver.py … --seed 3535 …                    # rc=0
timeout  900 python3 driver.py … --seed 3539 --only D-oneshot-slack # rc=0
timeout  900 python3 driver.py … --seed 3539 --only D2-oneshot-log  # rc=0
```

## Results — output fullness and witness verdict

Fresh seed 3539 (primary, chosen before building; not 3501/3517):

| engine | output | witness | chunk/direct stamps | long records | gate sha256 (variant) |
|---|---|---|---|---|---|
| A-chousa-root | 9/9 full | **fail** | 0 / 1 | 8 | `ba87df1f59c25489…08acf38c` |
| B-witness-shape | 9/9 full | **fail** | 0 / 1 | 8 | `2ef9a1a7e9866c3a…11b869` |
| C-idlen-mod3 | 9/9 full | **pass** | **9** / 1 | 8 | `1a2ceea27d99a8a2…9639ee` |
| landed gate | 9/9 full | pass | 9 / 1 | 8 | `1f2fb4f5…aef617` |

Seed 3535 (only difference: the fixture's single id length is 12, i.e. ≡0 mod 3):

| engine | output | witness | stamps | gate sha256 |
|---|---|---|---|---|
| A-chousa-root | 9/9 full | fail | 0/1 | `3fb7e729a71c899f…e1f6a08` |
| B-witness-shape | 9/9 full | fail | 0/1 | `0da78df8af876a44…7ee3cc` |
| C-idlen-mod3 | 9/9 full | **fail** | 0/1 | `7b373a4cf37009f1…b198a58` |
| D-oneshot-slack | 9/9 full | **pass** | **8**/1 | `4887fe52dd4c6016…1f65ce0` |
| landed gate | 9/9 full | pass | 9/1 | `1f2fb4f5…aef617` |

All engine entries in the receipts carry `source_gate_sha256=1f2fb4f5…`,
`battery_sha256=9f537bfd…`, `gate_rc=1`, `drift=true`, `misses=[]`,
`output_full=true`.
Artifacts: `receipt-s3539.json` (`9a87ff22…`), `receipt-s3535.json`
(`38bed858…`), `receipt-D-s3539.json` (`bd999892…`), `receipt-D2-s3539.json`
(`4d26a8b8…`) in this directory.

## Finding 1 — assigned engine C is output-full AND witness-pass (seed 3539)

C is a real output-equivalent keyed engine (it ran 9/9 with zero misses and the
same gate rc/drift), and the witness did **not** separate it: stamps are
identical to landed (`chunk=9`), so the engine is indistinguishable from the
landed gate on this seed.

Exact reason: in `generate()` the witness draws `id_prefix` and `id_width`
**once per seed** (`tools/mechanism-witness.py:189-191`), then every record's id
is `prefix + %0*x` of that one width. All nine ids in a fixture therefore have
the *same* length — measured: 13 on seed 3539, 12 on 3535, and `lens` was a
singleton in every one of 31 scanned seeds (`seed-scan-3530-3560.txt`,
`164d4e03…`; `seeds scanned=31 idlen_mod3_zero=6`). So `${#id} % 3` is a
**per-fixture constant**, not a per-record property: C either shortcuts every
long span (seed 3535 → `chunk=0`, separated) or none at all (seed 3539 →
branch never entered, byte-for-byte landed behaviour, `chunk=9`, pass). The
branch itself is correct — confirmed firing on 3535 with the same gate text.

Consequence for the frozen counter's recipe: `c2-count.py:184-186` counts a
variant as separated only if `output_full and witness == "fail"`. Added to
`VARIANTS`, C would yield separation 0/2 on a non-firing seed and the
predicate would be false even though the witness's mechanism check is intact.
Over two fresh seeds the measured firing rate is 6/31 per seed, so a
length-keyed engine escapes separation in roughly `(1-6/31)^2 ≈ 65%` of
two-seed runs (parameter space: lengths 7–18, 4 of 12 ≡0 mod 3 → ≈1/3 per
seed, ≈44% for both seeds inert). The key-space randomization randomizes the
id length *between* seeds but not *within* a seed.

## Finding 2 — supplementary engine D: an active shortcut that the witness passes

D does not mimic the landed gate: it answers exactly one long record per
fixture from the python exact search and **never calls the chunk matcher for
that record**. It is output-full (9/9, no misses) and the witness says
**pass** on both seeds tested (3539 and 3535), stamps `chunk=8` vs landed 9.
The D2 log proves the shortcut ran exactly once and produced the offsets used:
`1792785761 id=q7d924329d4d9 len=32766` (`oneshot.log`, `a48e95f2…`), with the
same receipt: `WITNESS=pass OUTPUT=9/9 STAMPS chunk=8 direct=1`.

Exact reason: the pass rule is a **global sum**, not a per-record check —
`witness_ok = stamps["chunk"] >= long_records and stamps["chunk"] > 0`
(`tools/mechanism-witness.py:295`), while the tool's own docstring states the
intended rule as "…at least once per long-span record (one stamp per call)"
(`mechanism-witness.py:21`). The landed fixture emits **9** chunk stamps for
**8** long records because the `dz-line-bound` record carries a `line` field
that triggers a second enumeration through `tok_span_all` (`research-gate.sh:1963-1979`),
a second matcher call for the same record. That one spare call is the slack:
any engine that suppresses one chunk call — one non-line-bound record
entirely, or either of the line-bound record's two calls — still satisfies
`>= 8` and passes. This is *not* the limit already written down in
`claims.md` ("calls the chunk matcher once for show and ignores its result"):
D makes no for-show call at all. The cheapest defect class — shortcut exactly
one long record — is invisible to the witness as implemented.

## Verdict

- **A**: output-full 9/9, separated (`witness=fail`, `chunk=0`) on both seeds;
  its separation is conditional on the harness root containing `chousa-`
  (true for my scratch path and for the lane path `…/chousa-shokunin/…`). If a
  future counter's `C2_TMP`/`TMPDIR` is a neutral `/tmp`, the key is inert and
  A would pass [INFERENCE from the branch condition; not run, the contract
  confines scratch to this `chousa-` path].
- **B**: output-full 9/9, separated on both seeds (its key is true of every
  witness fixture by construction, so it always activates).
- **C**: output-full 9/9 AND **witness-pass** on the primary fresh seed — the
  wave's MEETS-style "separates nothing on C2" result. It is not a witness
  blind spot about mechanism; it is a fixture-key-space blind spot: the id
  length is constant per seed, so a length-keyed engine is all-or-nothing and
  is separated only by seed luck (measured 6/31 seeds fire; separated on
  3535, invisible on 3539).
- **D** (supplementary, same finding class as the assignment's target): an
  engine that genuinely shortcuts one long record, is output-full, and still
  gets `WITNESS=pass`. This is a witness bypass that would keep
  `LANDED_WITNESS=pass`; if such an engine were a counter variant,
  `c2-count.py:186` would print `predicate_holds=false`.
- **Frozen P2 is not killed by this probe**: its predicate is scoped to K1/K2
  (`c2-count.py:VARIANTS`), which I did not run, and the committed K1/K2
  results stand. What falls is the C2 sentence's *class* claim — "the lane's
  measurement receipts can separate an output-equivalent keyed engine" — which
  D refutes and C evades, both with receipts above. Any engine whose shortcut
  is ≤1 chunk call, or keyed on a per-seed-constant property, is not
  separated by the witness as implemented.

## Integrity / restoration evidence

- No lane production file was written. Gate, base gate, witness, and both
  counters re-hash to the pinned values after all runs (commands above; rc=0).
  All variant gates live only in this directory and in scratch.
- The witness deletes its fixtures; the per-seed id evidence was re-derived
  deterministically by importing the tool's own `generate()` on the same seeds
  inside scratch (`seed-scan-3530-3560.txt`).
- The untracked `tools/__pycache__/` and `corpus/evidence/round35/__pycache__/`
  seen in `git status` predate this probe (pyc mtimes 16:46:04 and 16:58:59 vs
  first scratch use 17:00:14) and were not created or modified by me.
- No installs were needed (python3 3.14.8, bash, GNU grep already present); no
  network; no pacman; no subagents; PIDs not signaled (all runs bounded by
  `timeout`).

## Limits

- Primary score is one fresh seed (3539); 3535 was selected by a 31-seed scan
  to test the counterfactual (C firing), not to cherry-pick a verdict for A/B.
- A's inert-path case is inference, not a run (scratch path constraint above).
- D/D2 are extra probes beyond the three assigned engines; they change no
  contract and are labelled as such. Nothing here says the witness is wrong
  about K1/K2 — only that its pass rule has one call of slack and its fixture
  holds id length constant within a seed.
