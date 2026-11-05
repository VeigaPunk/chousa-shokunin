# Seat R79MutA — mutation table on the round-79 battery's own legs

Lane chousa, round 79, wave 1, seat R79MutA (mutation tester). Subject: the six legs of
`corpus/evidence/round79/matrix-battery-v6.py` (digest `bb91406e…5542a61e1d`, frozen) as
measured by the frozen outer battery `corpus/evidence/round79/forge-battery.py`
(`5761edc5…be84ebbcad4fc936`). Six assigned mutations plus supplementary probes (M2b, M2c,
P1, P2); every mutant is a copy, the frozen file is never edited.

Frozen revision: controls commit `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`. Live clone at
`/fast/scratch/hyaku/chousa-r79/R79MutA/lane` (`git clone --shared`, `git rev-parse HEAD` =
`e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`, receipt
`R79MutA/receipts/mutants-and-toolchain.txt`). The clone's battery digest equals the frozen
digest; the subject files I sampled (round-74/75 positives, `round76/loader-matrix-v3.py`,
`round76/forgers/forge-constant-pass.py`, `round78/forgers/perm.c`) are byte-identical to the
lane's.

## Method

`matrix-battery-v6.py` derives its subject table from its own location:
`LANE = HERE.parents[2]`. A copy anywhere but `<lane>/corpus/evidence/round79/<name>.py`
resolves its positives and forgers to the wrong paths, so each mutant was written to
`<clone>/corpus/evidence/round79/matrix-battery-v6-<M>.py` and the **frozen** outer battery
was run against it:

```
python3 -B <lane>/corpus/evidence/round79/forge-battery.py \
  --battery <clone>/corpus/evidence/round79/matrix-battery-v6-<M>.py \
  --work /fast/scratch/hyaku/chousa-r79/R79MutA/w-<M> --runs 1
```

`--runs 1` is the committed after receipt's setting (and the instrument default). Each
mutant differs from the pristine file only in the lines its diff shows
(`R79MutA/diffs/<M>.diff`, mutant bytes preserved at `R79MutA/mutants/`). Every mutant was
smoke-loaded with `--reemit-only` before scoring (exit 0, all seven).

Verdict vocabulary is the frozen instrument's: a forger is **FORGED** when the battery under
test exits 0 or its receipt's last `BATTERY=` line claims PASS — i.e. the battery accepted a
matrix that never ran the counter; **REFUSED** when the battery exits non-zero with an
intact receipt and a last `BATTERY=FAIL`; **DETECTED** when the receipt fails its own
`RECEIPT_LINES` integrity rule.

## Result table

| mutant | edit (one behaviour-bearing point) | observed predicate line (verbatim) | exit | forger/oracle rows that flipped vs M0 | verdict |
|---|---|---|---|---|---|
| M0 (control) | none — clone bytes, frozen digest | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` | 0 | — (byte-identical to `controls/forge-battery-after-v6.txt`) | reproduces the frozen after receipt, twice |
| **M1** | identity leg reverted to round-78 `salted_copy` (`_r78<hex>` statement inserted into the source text); permute/quiet/content/receipt legs untouched | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` | 1 | `a8-v5-salt-normalizer` REFUSED → **FORGED** (rc=0) | **KILLED** — identity leg load-bearing |
| **M2** | `--print-order` forced on (`default=True`), round-77 `ORDER <i> <digest>` line restored; nothing else | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` | 0 | none — `a7` stays REFUSED | **SURVIVED** — ORDER-line suppression decorative in isolation |
| **M2b** (supplementary) | M2 **and** quiet leg off (`buffered.append` → `emit`, lines written live) | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` | 1 | `a7-printed-order-digest` REFUSED → **FORGED** (rc=0) | **KILLED** — the two legs are jointly load-bearing |
| **M2c** (supplementary) | quiet leg off only (live emission, no ORDER line) | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` | 0 | none — `a7` REFUSED | **SURVIVED** — isolates the ORDER line as the leak `a7` needs |
| **M3** | `permute = False` (`--no-permute`) | `FORGE_BATTERY=FAIL forgers_handled=6/6 positive=0/1` | 1 | battery's own `ORACLE block-position` REJECTED → **MISS** (`positive=2/2 forgers_rejected=11/11`); the positive control then reads MISS | **KILLED** — permutation leg load-bearing |
| **M4** | `content = False` (`--no-content`) | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` | 0 | none — all three oracles still REJECTED | **SURVIVED** — content leg decorative for the frozen predicate |
| **M5** | `RECEIPT_LINES` trailer dropped | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` | 1 | `a5d-detached-append` DETECTED → **FORGED** (`trailer=no integrity=n/a`) | **KILLED** — receipt leg load-bearing |
| **M6** | identifier renaming disabled (`_rename(tree)` call removed; wrapper/marshal/docstring drop kept) | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` | 0 | none — `a8` and `a9` both REFUSED (`positive=0/2`) | **SURVIVED** — renaming decorative |

Full stdout+stderr receipts: `R79MutA/receipts/base-forge.txt`, `base-forge-2.txt`,
`forge-M1.txt … forge-M6.txt`, `forge-M2b.txt`, `forge-M2c.txt`.

## Per-mutant evidence

### M1 — the salt re-opens the textual channel (`R79MutA/receipts/forge-M1.txt`)

The mutant replaces the body of `reemit()` with round 78's `salted_copy()` verbatim (insert
one `import os as _r78<hex>` / `_r78<hex> = <int>` statement at a random top-level anchor;
`R79MutA/diffs/M1.diff`, 42 changed lines, nothing else touched). Observed:

```
FORGER a8-v5-salt-normalizer rc=0 receipt_lines=113 trailer=yes integrity=ok verdict=FORGED
POSITIVE legit-matrix rc=0 receipt_lines=113 integrity=ok verdict=ACCEPTED
FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1   (exit 1)
```

`a8` is FORGED in the instrument's sense: the mutant battery **exited 0** with `a8` as its
matrix — its receipt (`R79MutA/battery-receipts/M1-a8.receipt`, line 113) ends
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`. Because the copy is the
committed source plus one deletable line, `a8`'s four-line strip recovers the positive
digests and answers all thirteen subjects correctly **without executing a counter** — the
battery accepted a matrix that scores nothing. This is exactly the round-78 before state
(`controls/forge-battery-before-v5.txt`: `handled=5/6`, `a8 … FORGED`), reproduced from v6
bytes by moving one leg.

Supporting measurement, same function, `derivative-check.py`:

```
DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096   (exit 1)   R79MutA/receipts/deriv-M1.txt
```

versus `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` (exit 0) for the pristine clone battery
(`deriv-M0.txt`). So the C1 mechanism — *write no source text* — is precisely the load-bearing
part of the identity leg, and the salt restores the textual derivative byte-for-byte.

### M2 / M2b / M2c — the printed-order channel is closed twice (`forge-M2.txt`, `forge-M2b.txt`, `forge-M2c.txt`)

M2 restores the round-77 `ORDER <i> <sha256>` line by forcing the flag on. Observed:
`FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` (exit 0) — `a7` is **not** forged.
Its own call log (`R79MutA/battery-receipts/M2-forger-calls.log`, 13 identical entries, also in
`R79MutA/receipts/excerpts.txt`) says why: `no ORDER line readable`.

Cause: in `score()` the ORDER line is appended to the local `buffered` list and every line is
flushed **after** the scoring loop (`for line in buffered: emit(line)`). The quiet leg
therefore hides the ORDER line from the child process for the whole run — even at
`--runs 2`, where all runs accumulate before the flush. The ORDER suppression is redundant
while the quiet leg holds.

M2b turns the quiet leg off as well (lines written live). Now `a7` is FORGED:
`FORGER a7-printed-order-digest rc=0 … verdict=FORGED`,
`FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` (exit 1); `a7`'s receipt ends
`BATTERY=PASS …` (line 117) and its log shows the attack completing —
`perm digest=7f4b4a2c6e91 secs=23.3` followed by thirteen
`digest=… position=<n> subject=<name> positive=<bool>` lines covering the whole permutation.

M2c turns off only the quiet leg (live emission, ORDER line suppressed): `a7` is REFUSED
again (`no ORDER line readable`, 13 entries) and the run is
`FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` (exit 0). Live `MATRIX RUN` lines leak
only *already-scored* subject names; a child cannot learn its own position from them, so the
ORDER digest is the only sufficient leak and it needs live emission to be observable.

Conclusion: neither leg alone is load-bearing; the pair is. Each is a second lock on the same
channel — a redundancy, stated as such rather than as two independent gains.

### M3 — the permutation leg is load-bearing (`forge-M3.txt`)

`permute = False`. Observed `FORGE_BATTERY=FAIL forgers_handled=6/6 positive=0/1` (exit 1).
The mutant battery's own receipt for the legitimate positive control
(`R79MutA/battery-receipts/M3-positive.receipt`) names the failing leg at line 110:

```
ORACLE block-position MISS positive=2/2 forgers_rejected=11/11
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 oracle=MISS      (line 113)
```

So yes — with the fixed round-76 order the block-position oracle reaches full marks: the two
positives occupy exactly the two positions it scripts PASS, and it is accepted on all eleven
forgers. The battery then exits 1, the positive control's last `BATTERY=` line is FAIL, and
the outer battery reports `positive=0/1` (MISS). The permutation leg is the only closure that
refuses a positional script, and removing it flips the predicate.

### M4 — the content leg is decorative for the frozen predicate (`forge-M4.txt`)

`content = False`. Observed `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` (exit 0) —
**the contract-table oracle does not pass.** Its line in the mutant's own positive receipt
(`R79MutA/battery-receipts/M4-positive.receipt`, line 83) is

```
ORACLE contract-table REJECTED positive=0/2 forgers_rejected=7/11
```

and block-position is REJECTED at line 110, summary at line 113:
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`. The contract-table oracle
scripts "the first four calls PASS"; under a fresh per-run permutation it lands on both
positives only by chance, so the permutation leg refuses it independently of the content leg.
Dropping the content requirement changes no verdict the frozen predicate reads, and no forger
row flips. This is a surviving mutant, not a defect of the claim: the claim's sentence is
about copy mechanism and forgers handled, and both are intact.

### M5 — the receipt trailer is load-bearing (`forge-M5.txt`)

The `emit(f"RECEIPT_LINES={_LINES + 2}")` line is deleted. Observed
`FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` (exit 1) with

```
FORGER a5d-detached-append rc=1 receipt_lines=138 trailer=no integrity=n/a verdict=FORGED
```

`a5d` is believed rather than exposed: without a trailer the reader has no self-check, so the
detached grandchild's appended line is simply the last `BATTERY=` line. The receipt
(`R79MutA/battery-receipts/M5-a5d.receipt`) holds 14 `BATTERY=` lines — line 112 the
battery's own `BATTERY=FAIL …`, lines 114/116/…/138 the appended
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`. In the pristine run the
same forger is `DETECTED` (integrity BAD, 139 lines). So the trailer converts one FORGED into
one DETECTED — exactly the leg's stated job.

### M6 — identifier renaming is decorative (`forge-M6.txt`)

`_rename(tree)` is removed; the docstring drop, the random pad statement and the
wrapper/marshal re-emission all stay. Observed
`FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1` (exit 0). **Neither `a8` nor `a9`
forges it:** both are REFUSED, each receipt ending
`BATTERY=FAIL forgers_rejected=11/11 positive=0/2 oracle=REJECTED` (line 113). A text-level
normalizer that deletes the wrapper's two fixed lines is left with an empty string, whose
digest matches no committed subject, so it says FAIL everywhere and the battery's positive leg
misses. Renaming also changes nothing in the textual-derivative measurement:
`DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` (exit 0, `R79MutA/receipts/deriv-M6.txt`) — identical
to pristine. What keeps the copy non-derivative is that **no source text is written at all**,
not the fresh identifier table. Renaming's only remaining role is inside the already-recorded
structure-identity limit (an unmarshal-and-canonicalise normalizer), where it forces the
normalizer to canonicalise rather than compare names — it does not close that channel.

## Two extra probes (attribution, not assigned mutants)

### P1 — the content leg *is* load-bearing, for a channel the six forgers do not cover

Probe matrix: `corpus/evidence/round76/loader-matrix-v3.py` with one edit — the `CASE` line
always prints `expected_rc=0 … expected_failed=none` (marks unchanged; a matrix that derives
the summary but fabricates its per-case cells). `R79MutA/mutants/cells-fabricated.py`,
`R79MutA/diffs/probe-cells-fabricated.diff`.

```
pristine battery  --matrix cells-fabricated.py --runs 1 → BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=REJECTED  exit 1   (p-content-on.txt)
M4 (no content)   --matrix cells-fabricated.py --runs 1 → BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED  exit 0   (p-content-off.txt)
```

With the content leg the fabricated-cells matrix is refused (`content=bad` on the positive
lines, receipt line 5); with it removed the same matrix is accepted. So the content leg is the
only lock on the claim's "a reader can re-derive the stated outcome" arm — it is decorative
for the frozen *predicate line*, load-bearing for the C1 *sentence*.

### P2 — post-freeze finding: the oracle leg is a 1-in-78 coin flip at `--runs 1`

While M2c ran, the pristine oracle set produced `ORACLE block-position MISS` on an ordinary
permutation draw (first two block-position RUN lines were `successor-counter`, `ref-counter`).
That is not caused by the mutation: the block-position oracle prints PASS for
`n % 13 < 2`, so with one run per score it reaches full marks exactly when both positives land
in positions 0 and 1 of the drawn permutation — probability `2/13 · 1/12 = 1/78 ≈ 1.28 %` per
battery run.

Deterministic demonstration on otherwise-pristine bytes (`M0s`: only the seed source changes,
`random.Random(secrets.randbits(64))` → `random.Random(51)`, a seed whose permutation puts
both positives first; `R79MutA/diffs/M0s.diff`):

```
python3 -B <clone>/corpus/evidence/round79/matrix-battery-v6-M0s.py --matrix <lane>/corpus/evidence/round76/loader-matrix-v3.py --work … --runs 1
ORACLE block-position MISS positive=2/2 forgers_rejected=11/11     (line 110)
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 oracle=MISS       (line 113)   exit 1
```

The legitimate matrix is accepted on all thirteen subjects and all eleven forgers are
rejected, yet the battery fails its own predicate — the oracle leg alone decides. Empirical
check of the probability over seeds 0…199999: 2569 seeds put both positives first
(`0.012845`, expectation `1/78 = 0.012821`).

Consequence for the frozen predicate: `forge-battery` runs the battery seven times
(`--runs 1`), and an oracle MISS in the **positive control's** run turns the predicate line
into `FORGE_BATTERY=FAIL forgers_handled=6/6 positive=0/1` at exit 1 — a spurious failure of
C1's frozen sentence at roughly 1.3 % per `forge-battery` invocation (the risk sits in its
one positive-control battery run, `--runs 1`). This is reported as a measured limit,
not as a repaired predicate: the frozen bytes and receipts are untouched. It also means a
single green run is not strong evidence of stability; the fix would be `--runs ≥ 2` (where the
chance falls to `1/78²`) or an oracle whose state is bound to the drawn permutation rather
than to call position.

## Leg ledger — load-bearing vs decorative

| leg | probe | outcome | verdict |
|---|---|---|---|
| IDENTITY — re-emission (no source text written; wrapper + marshalled code object) | M1 (salt restored) | `a8` FORGED, `handled=5/6`, derivative `13/13` | **load-bearing** (the whole C1 target sentence) |
| IDENTITY — identifier renaming | M6 (rename disabled) | `a8`, `a9` REFUSED; `handled=6/6`; derivative `0/13` unchanged | **decorative** for the predicate; forces canonicalisation only inside the recorded structure-identity limit |
| PERMUTATION | M3 (`--no-permute`) | `ORACLE block-position MISS` 2/2 + 11/11, battery exit 1 | **load-bearing** (sole closure on positional scripting) |
| QUIET (buffer all per-subject lines) + ORDER suppression | M2 (ORDER restored) / M2c (quiet off) / M2b (both) | M2 PASS, M2c PASS, M2b `a7` FORGED | **jointly load-bearing**, individually redundant — one channel, two locks |
| CONTENT (twelve contract cells vs the battery's own map) | M4 (`--no-content`) | PASS, no row flips; contract-table oracle still refused by permutation | **decorative for the frozen predicate line**, load-bearing for the "reader can re-derive" arm (P1) |
| RECEIPT (`RECEIPT_LINES` trailer) | M5 (trailer dropped) | `a5d` DETECTED → FORGED, `handled=5/6` | **load-bearing** (the append channel's only lock) |

Three of six mutations survive: M2 (and its M2c control), M4, M6. Each surviving mutant is a
coverage finding about the *claim's* wording, not a falsification: the frozen sentence names
copy mechanism, six forgers handled and `oracle=REJECTED`, and every killed mutant breaks one
of those while every survivor leaves them intact. The honest count is therefore **three
load-bearing legs (identity-as-re-emission, permutation, receipt trailer)**, **one
load-bearing pair (quiet + order)**, **one leg load-bearing only for the sentence's auditable
arm (content)** and **one decorative leg (renaming)**.

## Notes, limits, environment

- `M3`'s outer line reports the oracle failure as `positive=0/1`: `forge-battery` derives
  "positive accepted" from the last `BATTERY=` line, so any internal battery failure surfaces
  as a positive MISS. The battery's own receipt names the true leg. Instrument shape, not a
  defect.
- M1's mutant keeps the unused `_drop_docstrings`/`_rename`/`WRAPPER` definitions; the diff
  (`R79MutA/diffs/M1.diff`) is confined to `reemit()`'s body. M2b/M2c replace the four
  `buffered.append(` call sites with `emit(`; the post-loop flush then emits nothing.
- Runs were batched in parallel on 32 cores (7 forge-battery runs in one batch, wall 102.8 s;
  M2c + three derivative checks, wall 80.9 s; the three attribution probes, wall 44.4 s), so
  per-run wall times are not isolated. The baseline was run twice into separate work dirs
  (`base-forge.txt`, `base-forge-2.txt`); both print
  `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`, exit 0 (`base-forge-2.txt` carries
  the `exit=0` footer; the first receipt was captured without a footer and the exit code was
  read from the shell). No run produced a MISS
  that a repeat contradicted; the only MISS observed (M2c's oracle, M3's and P2's) is
  explained by the permutation draw or by the mutation.
- Toolchain: Python 3.14.8 (`/usr/bin/python3`), `cc (GCC) 16.2.1 20260810` (the frozen
  forge battery built `round78/forgers/perm.c` with it). **No tools were installed or
  upgraded**; pacman untouched per the 2026-10-20 host guard.
- Frozen artifacts untouched: `matrix-battery-v6.py` and `forge-battery.py` digests re-checked
  after all runs and equal to the frozen table (`mutants-and-toolchain.txt`, last block). The
  only lane writes are this report and `R79MutA/` (receipts, diffs, mutants).
- Scratch `/fast/scratch/hyaku/chousa-r79/R79MutA` (clone, work dirs, per-forger receipts,
  call logs) was copied into `R79MutA/` first and then deleted; the cited receipts are the
  copies under `R79MutA/receipts/`. Per-forger receipts and `forger-calls.log` excerpts from
  the runs are quoted in `R79MutA/receipts/excerpts.txt`.

## Receipt index

| file | what it is |
|---|---|
| `R79MutA/receipts/mutants-and-toolchain.txt` | pristine + mutant + probe digests, toolchain, clone HEAD, frozen instrument digests |
| `R79MutA/receipts/base-forge.txt`, `base-forge-2.txt` | control: frozen forge battery on the pristine clone battery (PASS 6/6, exit 0) |
| `R79MutA/receipts/forge-M1.txt … forge-M6.txt` | the six assigned mutants, full stdout + `exit=` |
| `R79MutA/receipts/forge-M2b.txt`, `forge-M2c.txt` | supplementary quiet/order isolation runs |
| `R79MutA/receipts/deriv-M0.txt`, `deriv-M1.txt`, `deriv-M6.txt` | derivative-check on pristine, salt-restored and unrenamed batteries |
| `R79MutA/receipts/p-content-on.txt`, `p-content-off.txt` | P1: fabricated-cells matrix against the pristine battery and M4 |
| `R79MutA/receipts/p-seed.txt` | P2: seed-forced oracle-leg flake on otherwise-pristine bytes |
| `R79MutA/receipts/excerpts.txt` | cited per-forger receipt tails, `BATTERY=` line numbers, `a7` call logs |
| `R79MutA/battery-receipts/` | the battery-under-test's own receipts cited above: `M0-positive`, `M1-a8`, `M2/M2b/M2c-a7` (+ their `forger-calls.log`), `M3-positive`, `M4-positive`, `M5-a5d`, `M6-a8`, `M6-a9` |
| `R79MutA/diffs/`, `R79MutA/mutants/` | every diff and every mutant byte-for-byte |
