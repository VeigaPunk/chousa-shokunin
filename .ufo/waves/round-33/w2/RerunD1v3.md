# RerunD1v3 — D1 repair re-run: v3 exempt-hop counter vs the exact metadata control

Round 33, wave 2 (FALSIFY). Seat `ChousaR33.RerunD1v3`. Read first: `corpus/evidence/round33/claims.md`
(design v1 + governing "Design v2"). Attacked only the D1 repair — the counter whose fixture order
encoded the truth — not C1. `c1-count-v2.py` was never run by this seat.

**Verdict: HOLDS.** v3 counter (`6f362ece…`) keeps the landed gate at `132/132` and puts the exact
round-32 metadata control below total on every seed tried (87–98 of 132, 8 seeds); the v2 counter
(`8ec1a1ed…`) on the same control gives `132/132` twice, reproducing the defect the repair targets.
No lower landed-gate run was observed.

## Exact bytes (hashed at start and after all runs, unchanged)

```
94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e  tools/research-gate.sh                              (landed)
79c4f44e1b16331dbbcae5b8839d526d158512de264a145d9414352cfe9ffcdc  .ufo/waves/round-32/w2/CriticAxis32/metadata-control.sh (control, unmodified)
6f362ece2e5e04c92212ee5a3547a69a6742c5658fd7ebc41688b68043e5a9fa  corpus/evidence/round32/c2-count-v3.py              (v3 counter)
8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a  corpus/evidence/round32/c2-count-v2.py              (v2 counter)
```

The base gate was extracted read-only for the no-harm run:
`git show 2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh` →
sha256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (matches claims.md).

## Runs (all receipts and stdout under `.ufo/waves/round-33/w2/RerunD1v3/`)

Command template (seeds are fresh, none in 3301–3373; every run receipted; stdout redirected to a
file, never piped):

```
env C1_TMP=/fast/scratch/hyaku/chousa-r33/w2/RerunD1v3/tmp C2_TMP=<same> TMPDIR=<same> \
PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=5s 300s prlimit --nproc=2000 --as=4000000000 \
python3 <counter> --gate <gate> --seed <n> --receipt .ufo/waves/round-33/w2/RerunD1v3/<name>.json \
  > .ufo/waves/round-33/w2/RerunD1v3/<name>.stdout.txt 2> .ufo/waves/round-33/w2/RerunD1v3/<name>.stderr.txt
```

### A. v3 on the landed gate (`94a7be5a…`) — the "no lower run" side

| seed | stdout file | exit | label | RECORD_CHECKS |
|---|---|---|---|---|
| 33881101 | `v3-landed-s33881101.{json,stdout.txt}` | 0 | `EXEMPT_AUDIT_MATCH=132/132` | ok |
| 33881102 | `v3-landed-s33881102.*` | 0 | `132/132` | ok |
| 33881105 | `v3-landed-s33881105.*` | 0 | `132/132` | ok |
| 33881106 | `v3-landed-s33881106.*` | 0 | `132/132` | ok |
| 33881107 | `v3-landed-s33881107.*` | 0 | `132/132` | ok |
| 33881108 | `v3-landed-s33881108.*` | 0 | `132/132` | ok |

Six seeds, every class `n/n` in all six stdout files (checked mechanically: no class line has
`k/k` with k ≠ n; e.g. `R1_U_fragment_quote 12/12 … E12_U_whitespace_only 6/6`). All 19
`*.stderr.txt` files in this directory are 0 bytes (`wc -c *.stderr.txt` → `0 total`). Receipts record `counter_sha256=6f362ece…`,
`gate_sha256=94a7be5a…`, `predicate_holds=true`, `misses=[]`.

### B. v3 on the exact round-32 metadata control (`79c4f44e…`) — the "control below total" side

| seed | exit | label | receipt |
|---|---|---|---|
| 33881201 | 1 | `EXEMPT_AUDIT_MATCH=98/132` | `v3-control-s33881201.json` |
| 33881202 | 1 | `94/132` | `v3-control-s33881202.json` |
| 33881205 | 1 | `92/132` | `v3-control-s33881205.json` |
| 33881206 | 1 | `87/132` | `v3-control-s33881206.json` |
| 33881207 | 1 | `92/132` | `v3-control-s33881207.json` |
| 33881208 | 1 | `90/132` | `v3-control-s33881208.json` |
| 33881209 | 1 | `92/132` | `v3-control-s33881209.json` |
| 33881210 | 1 | `92/132` | `v3-control-s33881210.json` |

All `RECORD_CHECKS=ok`, `gate_rc=1`, `record_fails=[]`, `predicate_holds=false`; per-class misses are
spread over R1/R2/R3 and E1/E4/E8–E12 (e.g. seed 33881201: `R1 7/12, R2 3/12, R3 5/12,
E1 10/12, E10 3/6, E11 2/6`). Range 87–98 on 8 seeds, never 132.

### C. v2 on the same control — the defect, reproduced

| seed | exit | label | receipt |
|---|---|---|---|
| 33881203 | 0 | `EXEMPT_AUDIT_MATCH=132/132` | `v2-control-s33881203.json` |
| 33881204 | 0 | `132/132` | `v2-control-s33881204.json` |

Same control bytes, same fixture classes; only the counter differs. This is the round-32 receipt
`control-metadata-s3232002{1,2}.json` (both 132/132) reproduced on fresh seeds.

### D. No-harm cross-checks (extra, cheap)

- v2 counter on the landed gate, seed 33881109 → `132/132`, exit 0 (`v2-landed-s33881109.json`):
  the counter revision does not change the landed score.
- v3 counter on the round-33 **base** gate `f4731885…`, seeds 33881103/33881104 → `132/132` both
  (`v3-base-s3388110{3,4}.json`): the C1-only change between base and landed does not disturb C2.

## Why the control fails under v3 and passes under v2 (mechanism, measured)

1. The control's only "verification" is metadata: it builds
   `positive_paths = {path for _, _, path in sorted(entries)[:36]}` over
   `(st_mtime_ns, st_ino, realpath)` (`metadata-control.sh:35-37`) and calls a hop `resolvable`
   only when its status is in `{unresolved, blocked-no-fetch, labelled-dead}` **and** its target is
   in those 36 (`:49`). It never opens a cited source (header `:2`), and says so itself:
   "This is a fixture-order shortcut, not anchor verification." (`:36`). The independent fixture
   audit `.ufo/waves/round-33/w1/ExecD1CounterV3/fixture-audit.out:2-3` measures the same thing on
   v3 seeds 7331/7332: `positives_in_top36=13/36` and `12/36`, `same_set_as_positives=False`.
2. v2 writes each source inside its class loop and never touches timestamps
   (`c2-count-v2.py:188-192`), so mtime/atime/ctime order = R1→R2→R3→…→E12 class order.
3. v3 plans bodies first (`c2-count-v3.py:210`), shuffles the write plan (`:283`) and stamps each
   file with an independent random atime/mtime in 2020–2027 (`:284-295`).
4. I re-generated the fixtures with each counter's own `generate()` for the kept seeds (record bytes
   identical to the `--keep` copies) and classified the control's first-36 set against the hidden
   class labels:

| fixture | R files in first 36 (of 36) | E-U files in first 36 (48 such files in root) | E-J | F1 | predicted match | receipt match |
|---|---|---|---|---|---|---|
| v2 seed 33881203 | **36/36** | 0 | 0 | 0 | 132 | **132** |
| v3 seed 33881201 | 15/36 | 13 | 5 | 3 | 132−21−13 = 98 | **98** |
| v3 seed 33881202 | 12/36 | 14 | 3 | 7 | 132−24−14 = 94 | **94** |

   (E-J hops are `rejected`/`not-applicable`, which the control never flags; F1 is `resolved`, which
   it always calls verified. Expected R count under a uniform order is 36·36/108 = 12.)

5. Metadata-key sweep on the same fixtures (first-36 selection by each key, R files selected):

| key | v3 s…201 | v3 s…202 | v2 s…203 |
|---|---|---|---|
| mtime | 15 | 12 | **36** |
| ctime | 12 | 10 | **36** |
| atime | 11 | 11 | **36** |
| inode | 12 | 11 | 26 |
| size | 13 | 12 | 14 |
| name | 13 | 10 | 11 |

   Under v3 every key sits at the uniform expectation; under v2 all three creation-time keys leak
   the class. So the repair is not mtime-only: v3's shuffled write order also decorrelates ctime/atime
   (xfs, ns timestamps — `stat -f -c '%T' /fast` → `xfs`).

## QUALITY 36 row cross-check (read-only)

`corpus/QUALITY.md:275-284` cites v2 `132/132` and v3 `96/132`, `95/132` on this control plus a
no-reader control at `78/132`. I read those committed receipts:
`.ufo/waves/round-33/w1/ExecD1CounterV3/receipts/v2-metadata-s733{1,2}.json` (132/132, gate
`79c4f44e…`), `v3-metadata-s733{1,2}.json` (96/132, 95/132, same gate), `v3-noreader-s733{1,2}.json`
(78/132, gate `8e430e6c…`, whose control header states it "never opens any citation source"). My
fresh seeds land in the same band (87–98), so the row's "shown able to fail" is corroborated and its
numbers are not contradicted — they are seed-specific, as the row's receipt pointers imply.

## Limits and residual risk

- The control is a shortcut *model*; I ran it unmodified and did not author it. Below-total shows it
  cannot pass, not that every possible metadata shortcut is excluded. The sweep in §5 covers six
  ordering keys on the kept seeds only.
- Decoupling is statistical: a metadata shortcut still hits ~1/3 of the R files by luck. That is why
  the control's score varies 87–98; the chance that all 36 R files land in the first 36 is
  astronomically small, so a passing control is not a realistic flake, but the margin is a sample
  property, not a hard bound.
- I did not re-run the no-reader/inode/mtime control triple; the sibling seat owns control sets. I
  only read their receipts.
- Housekeeping: importing the two counters in my scratch analysis wrote `corpus/evidence/round32/__pycache__/`
  (`c2-count-v2/v3.cpython-314.pyc`). I removed it; `git status --porcelain` shows no `__pycache__`
  afterwards. `SKILL.md` and `corpus/SOURCES.md` show as modified during my window — not by me; my
  only lane writes are this report and the receipts/stdout under `.ufo/waves/round-33/w2/RerunD1v3/`.
- Artifacts total 27,850 bytes (largest receipt 5,547 B); kept fixtures live in
  `/fast/scratch/hyaku/chousa-r33/w2/RerunD1v3/keep-*/`. No processes started by this seat remain;
  no signals sent; no network; no installs.
