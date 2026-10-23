# ExecE1Fuzz — round-34 repair E1 (fuzz binding) on the LANDED round-33 gate

**Verdict: HOLDS on the landed gate; the E1 gap is closed.** The round-33 differential fuzz
`fuzz_c1.py` run against the **committed** round-33 gate blob `43a1af35ca668fe5…`
(`git show b80539005176ac6ce39bc1c7afb846cb1f2f7c75:tools/research-gate.sh`) agrees with the
independent contract reference on **650/650 records for each of three seeds (1950/1950 total)**,
with a flat calibration of **60/60** in every run and **0 mismatches**. The mask gate
`L1ShortcutMask/mask-gate.sh` does **not** agree: **640/650, 10 mismatches** on the same harness,
and every one of the 10 is a record carrying a `}`-bearing confuser inside a nested container —
i.e. the round-33 spot-check's inference ("it would fail on confusers with `}` inside strings")
is **confirmed**.

No lane production file was edited. All artifacts live in
`.ufo/waves/round-34/w1/ExecE1Fuzz/`; scratch is under `/fast/scratch/hyaku/chousa-r34/w1/ExecE1Fuzz/`.
No installs, no network.

## 1. The committed gate bytes (E1's premise)

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && \
git show b80539005176ac6ce39bc1c7afb846cb1f2f7c75:tools/research-gate.sh \
  > /fast/scratch/hyaku/chousa-r34/w1/ExecE1Fuzz/gate-43a1af35.sh
sha256sum /fast/scratch/hyaku/chousa-r34/w1/ExecE1Fuzz/gate-43a1af35.sh
→ 43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346
git show b80539005176ac6ce39bc1c7afb846cb1f2f7c75:tools/research-gate.sh | sha256sum
→ 43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346   (identical)
```

The prefix matches the lane-gate expectation `43a1af35ca668fe5`. The blob is the tip gate:
`git log --oneline -1 -- tools/research-gate.sh` → `1b6312e round-33: final gate 43a1af35 …`.
Cross-check of gate generations (`git show <rev>:tools/research-gate.sh | sha256sum`):
`2b9cc73 → f4731885…`, `0fb300b → 94a7be5a…`, `0cad05e → 165acd5f…`, `1b6312e → 43a1af35…`,
`b805390 → 43a1af35…` — so `43a1af35` is the round-33 final gate, and `b2c07eda…` (the gate the
old fz-9021{2,3,4} receipts bind) is **not** in any commit. That is exactly defect E1.

## 2. The three seeded runs (same sizes as the r33 fz-9021{2,3,4} receipts)

Sizes read from `.ufo/waves/round-33/measure/final/fz-9021{2,3,4}.json`: `n=650`, `flat=60`,
seeds `90212 / 90213 / 90214`. Command shape (each run bounded by `timeout 900` and
`prlimit --nproc=8000`, `TMPDIR` in scratch, `CHOUSA_*` stripped by the harness):

```
python3 .ufo/waves/round-33/w2/FuzzDiff33/fuzz_c1.py \
  --gate <scratch>/gate-43a1af35.sh --root <scratch>/roots/s<seed>b \
  --seed <seed> --n 650 --flat 60 \
  --out .ufo/waves/round-34/w1/ExecE1Fuzz/fz-<seed>-landed-43a1af35.json
```

| run | seed | n | calibration | agreement | mismatches | gate_rc | receipt `gate_sha256` | exit |
|---|---|---|---|---|---|---|---|---|
| `fz-90212-landed-43a1af35` | 90212 | 650 | **60/60** | **650/650** | **0** | 1 | `43a1af35ca668fe5…` | 0 |
| `fz-90213-landed-43a1af35` | 90213 | 650 | **60/60** | **650/650** | **0** | 1 | `43a1af35ca668fe5…` | 0 |
| `fz-90214-landed-43a1af35` | 90214 | 650 | **60/60** | **650/650** | **0** | 1 | `43a1af35ca668fe5…` | 0 |

Per-class (identical distribution to the old receipts, as expected for the same seeds):
90212 `supported 206/206, mislocated 173/173, stale 135/135, unsupported 87/87, linebad 49/49`;
90213 `supported 215/215, mislocated 185/185, stale 135/135, unsupported 70/70, linebad 45/45`;
90214 `supported 242/242, mislocated 186/186, stale 112/112, unsupported 76/76, linebad 34/34`.
`structural_stats` reproduce the old receipts exactly (e.g. 90212 `dup_read_key_records=152`,
`nested_read_key_records=342`, `max_depth=5`), and `ref_counts` match the r33 receipts field for
field — the fixtures are the same, so the old receipts' per-class counts are reproduced on the
landed bytes. Every receipt records the gate SHA-256 the run actually hashed, and it is the
**committed blob's** hash, which is the property E1 required.

### Environment pitfall worth recording (harness-side, not gate-side)

My first four invocations wrapped the harness in `prlimit --nproc=2000 --as=4000000000` (the
r33 report's shape). On this host that made the gate's own `fork` fail —
`gate-43a1af35.sh: fork: retry: Resource temporarily unavailable` → gate produced **no** output,
`gate_rc=254`, and the harness scored a spurious `DIFF_CLAIMS=0/650, MISMATCHES=650` on every
seed **including the mask gate**. Isolated repro: `timeout 30 prlimit --nproc=2000 bash -c '( true )'`
→ same `fork: Resource temporarily unavailable` (rc 254), while `prlimit --nproc=8000` forks fine.
The ulimit is not per-process here (the shell's own `ulimit -u` is 122865); the 2000 cap counts
the whole uid. **All four first runs were discarded and re-run** with `--nproc=8000`; only the
re-run numbers are reported. Anyone re-running this harness on a shared host should drop or
raise the `nproc` cap — a `gate_rc=254` with empty stdout is the signature.

## 3. The mask gate run (the spot-check's inference)

```
cp .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh <scratch>/mask-gate.sh   # sha256 ae7d4bfc7ac1d26…
python3 .ufo/waves/round-33/w2/FuzzDiff33/fuzz_c1.py \
  --gate <scratch>/mask-gate.sh --root <scratch>/roots/s90215b \
  --seed 90215 --n 650 --flat 60 --out .ufo/waves/round-34/w1/ExecE1Fuzz/fz-90215-maskgate.json
```

Result: `CALIBRATION_FLAT=60/60`, **`DIFF_CLAIMS=640/650`, `MISMATCHES=10`**, exit 1,
`gate_sha256=ae7d4bfc7ac1d262590dd5014e8abdbbea102266551891b4910666116440e0cd`.
Per class: `supported 234/237, stale 113/115, unsupported 75/78, mislocated 164/166, linebad 54/54`.
(I used seed 90215, not 90212–90214, so the mask fixture is independent of the landed runs.)

**The mask gate fails, and the failure mode is exactly the inferred one.** All 10 mismatches are
`observed=invalid` where the contract says otherwise (`supported`/`stale`/`unsupported`/
`mislocated`), and every one of the 10 records contains an **unmasked** `}`-bearing confuser
(`'trailing \\\\ two backslashes then }'` ×8, `'escaped quote \\" then } brace'` ×3, one record
carrying both). Cross-tabulation of the fixture:

* records carrying an **unmasked** brace confuser: **132** — of which **10** mismatch;
* records carrying a **masked** brace confuser: 237 — of which 5 also mismatch, but all 5 are
  among the 132 above (mismatches explained *only* by masked braces: **0**);
* mismatches with **no** unmasked brace confuser: **0**;
* all unmasked-brace occurrences in the fixture are **inside a nested container** (top-level
  occurrences: 0).

Mechanism (reproduced byte-for-byte by `mk-mask-gate.py`): the mask's `json_mask_strip` replaces
six *literal* confuser strings and then strips nested `{…}`/`[…]` with the regex
`\{[^{}]*\}`. A `}` inside a JSON **string** terminates that regex match early, so the nested
container is cut short and its remaining members land at apparent top level; the shortcut's
`json_dup_read_key` then sees a second `"expect"`/`"source"`/`"span"`/`"id"` and marks the record
`duplicate top-level key` → `invalid`. Minimal reproducer
(`.ufo/waves/round-34/w1/ExecE1Fuzz/mask-confuser-probe.txt`, record `R1`/`AB_brace`):

```
{"id":"r1","source":"src/a.md","span":"horitu","expect":"supported",
 "nest":{"note":"trailing \\\\ two backslashes then }","marker":"m","expect":"contradicted"}}
mask   → CLAIM id=r1 … observed=invalid   FINDING CLAIM_RECORD_INVALID … obs=line=1 duplicate top-level key
landed → CLAIM id=r1 … observed=supported … verdict=match
```

The same record with the brace replaced by a letter (`AB_nobrace`) is `supported` on **both**
gates — the brace is the trigger. The landed gate's string-aware scanner ignores the `}` inside
the string and reads only top-level members.

Note the mask gate is **not** the landed gate plus a shortcut: `mk-mask-gate.py` applies to the
round-33 **base** gate (`2b9cc73` → `f4731885…`), and the regenerated copy is byte-identical to
the shipped file (`sha256 ae7d4bfc7ac1d26…` for both, `cmp` clean). So the mask gate is a
base-gate control with the fixture-keyed mask, not a candidate C1 implementation.

## 4. What this closes, and what it does not

* **E1 (fuzz binding) is closed on the run side:** there are now three committed-blob-bound fuzz
  receipts (`fz-9021{2,3,4}-landed-43a1af35.json`) whose `gate_sha256` is
  `43a1af35ca668fe5…`, the hash of `b805390…:tools/research-gate.sh`. The lane still owes the
  *textual* correction to the r33 report/SCORECARD/knowledge entries that say "on the final gate"
  about `fz-9021{2,3,4}.json` (those bind `b2c07eda…`, an uncommitted scratch state) — that
  naming/correction is the L1's, not this seat's.
* The **counter** side of the r33 clause-3 story (E2) is untouched by this seat: I ran the fuzz
  harness, not `c1-count.py`, and I ran no candidate C1 implementation, so the round-34 CONTROL
  RULE is respected.
* The mask-gate result above is a **control** observation about a round-33 shortcut gate; it says
  nothing about any round-34 candidate build.

## Artifacts (all in `.ufo/waves/round-34/w1/ExecE1Fuzz/`)

| file | sha256 | bytes |
|---|---|---|
| `fz-90212-landed-43a1af35.json` | `9541da948ad05600f6e69e75fa2370ed353c9c98fd46d7adcb5392b194d6a1cd` | 820 |
| `fz-90212-landed-43a1af35.out` | `c414c49d68ebd12a3c51001bf3669049482485eacc3a993250579e82d9713ad7` | 167 |
| `fz-90213-landed-43a1af35.json` | `5f55ae8fc6760655ddaade610a4bf3d461957affb666c159be47a6fc2240ffff` | 820 |
| `fz-90213-landed-43a1af35.out` | `a54aceee133d4edd863d4bfa56c729ff7b1a172ef5586add019a1300ea8c5645` | 167 |
| `fz-90214-landed-43a1af35.json` | `c3e798a86e3e579c98935419c30d286ea19ed3c42ae8701749ca7aaa33235395` | 820 |
| `fz-90214-landed-43a1af35.out` | `4b4dc4591fadab98463e43458bc88e3c9f5b65c21321e92b1773dffc76c82919` | 167 |
| `fz-90215-maskgate.json` | `9110e6e5ba832f9e16675057a70cf154ba11ec593ab271b84328b5840267dc81` | 14582 |
| `fz-90215-maskgate.out` | `6a9c3eb04d0b2870005a07f79251d39958e644b233406826ed151807a477b8c6` | 168 |
| `mask-confuser-probe.txt` | `fa6955be952c47ada89df9f033ef8d69bfe614fc3f91d5b3958da290053ea770` | 2222 |

(The landed-gate JSON receipts are small because the harness stores only mismatches, and there
are none; the mask-gate receipt is larger because it carries 10 minimized counterexamples.)

Fixtures (scratch, cited by hash): `roots/s90212b/claims.jsonl`
`ec39ea61b281525d83e389267d4f5734806033e7bb406bd6e0dfb60c5a85268d`,
`roots/s90213b/claims.jsonl` `ce634d7d99709ce73212c1a9b09a094dc4c3f94ef29b7a2e1df47238e299d213`,
`roots/s90214b/claims.jsonl` `464a3da8f718dba5f4c434c870378d5ed9ba02c73e2f3d7d11e022f7b34c602b`,
`roots/s90215b/claims.jsonl` `74680f573b797f89594d650b52a64c48b789475cf474e0787b5eaf1fb989de9f`.
Scratch gate copies: `gate-43a1af35.sh` (`43a1af35…`), `mask-gate.sh` (`ae7d4bfc…`),
`base-2b9cc73.sh` (`f4731885…`), `mask-regen.sh` (`ae7d4bfc…`, identical to the shipped mask gate).

## Limits

* The harness models spans as unique standalone words on a single line; multi-occurrence and
  multi-line span edges and the `contradicted` path are base behaviour it models only
  approximately — unchanged from the r33 instrument.
* The mask-gate run used seed 90215 only (one run, as assigned); the 10-mismatch count is that
  seed's, and the *mechanism* (brace inside a string cuts the regex strip) is established
  independently by the minimal reproducer, not by seed statistics.
* No build, lint, selftest or counter run was performed (parent owns the post-integration gate);
  no lane file was edited; no git/jj write command was run in the lane or fleet repo.
