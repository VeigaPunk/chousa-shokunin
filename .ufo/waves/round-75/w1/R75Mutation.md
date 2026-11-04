# R75Mutation — mutation probe of the round-75 instruments

Seat: R75Mutation (leaf, W1). Lane: chousa-shokunin. Frozen revision:
`43a7a0db52c8aabdf32735f58e09610e05200e79` (verified with `git rev-parse HEAD`).
No production edits, no network, no lane/fleet git or jj mutation; read-only `git status`/
`rev-parse` only. Scratch root `/fast/scratch/hyaku/chousa-r75/R75Mutation` created, used and
removed. No tools installed or upgraded.

Instruments under test — frozen bytes, unchanged before/after (sha256 diff empty):

| Instrument | sha256 |
|---|---|
| `corpus/evidence/round75/loader-matrix-v2.py` | `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7` |
| `corpus/evidence/round75/matrix-battery.py` | `c35e937b4b7c1b910a6eab8f480c82d2c296285428b50585547c234d2377ac4e` |

Detector discipline. Every mutant is exactly one localised hunk of the frozen file (generator
asserts the old block occurs once; `diff -u` reports one `@@` hunk per mutant). The same bounded
detector runs on pristine, mutated and restored bytes:

- Matrix mutants: the frozen battery, predicate line
  `BATTERY=PASS forgers_rejected=5/5 positive=2/2` / `BATTERY=FAIL …`, exit 0/1, two matrix seeds
  per battery run, and a second independent battery invocation for survivors.
- Battery mutant: the mutated battery over a byte-identical scratch copy of pristine v2, plus a
  relocated pristine-battery control.
- Where the battery cannot observe a property, the frozen matrix itself is the detector with a
  scratch counter that reads no repository bytes (declared in each row).

Pristine baseline: `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0
(`battery-baseline.txt`), reproduced on restored bytes after all mutations and on a relocated
copy (`battery-control-relocated-pristine.txt`, `battery-restored-baseline.txt`).

## Kill matrix

`K` = detected by the assigned detector; `S` = survived (coverage finding).

| # | Mutant (one hunk) | sha256[:12] | Expected detection | Observed | Verdict |
|---|---|---|---|---|---|
| M1 | drop the three content cases (`dup-log/lesson/card-heading`) | `c270c230b84a` | forgers that are only diff/content-blind accepted | `BATTERY=FAIL forgers_rejected=3/5 positive=2/2`, exit 1; diff-only `9/9 exit0`, naive-grep `9/9 exit0` | **K** |
| M2 | remove `random.Random(seed).shuffle(order)` (declared order) | `ca1fc14dbe9c` | source-blind declared-order oracle reaches full marks | `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0, twice; r74 oracle 9/12; v2-aware oracle **12/12 exit 0** | **S** |
| M3 | `p.returncode in (expected_rc, 2)` — exit 2 satisfies the expected code | `6f9cb0d635f1` | an exit-2 subject scored as PASS | `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0, twice; full-mark exit-2 probe 0/12 pristine → **4/12** mutant | **S** |
| M4 | `ok = p.returncode == expected_rc` only (check ids ignored) | `8c208f0de2d4` | wrong check-id sets accepted | `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0, twice; constant-fail 4/12 → **8/12**; all-FAIL/rc1 probe 0/12 → **8/12** | **S** |
| M5 | skip fixture-byte restore between cases | `9b980993bf9f` | positives fail | `BATTERY=FAIL forgers_rejected=5/5 positive=0/2`, exit 1; both positives 4–5/12; direct successor 2/12 | **K** |
| M6 | receipt fixture/case path `…-pinzone-r72-wrong.txt` (no counter monitors it) | `f2e5c346c8db` | positives fail on `receipt-change` | `BATTERY=FAIL forgers_rejected=5/5 positive=0/2`, exit 1; both positives 11/12 both runs; direct successor 11/12, only `receipt-change` fails | **K** |
| M7 | battery: forger "rejected" when its exit is 0 | `8eec053895f9` | battery's own predicate breaks over pristine v2 | `BATTERY=FAIL forgers_rejected=0/5 positive=2/2`, exit 1; all five forgers labelled `ACCEPTED` | **K** |

Score: matrix mutants 3K/3S; battery mutant 1K; overall 4 killed / 3 survived / 0 inconclusive.

## Direct measurements behind the survivors

| Probe (scratch; reads no repo bytes unless noted) | Pristine v2 | Mutant |
|---|---|---|
| `probe-order-oracle-v2.py` — 12-entry script in declared order | `3/12 FAIL` exit 1 | M2 `12/12 PASS` exit 0 |
| frozen `forge-order-oracle.py` — r74 9-entry script | `3/12` exit 1 (battery runs 4–6/12) | M2 `9/12` exit 1 |
| `probe-exit2-fullpass.py` — full marks, exits 2 | `0/12` exit 1 | M3 `4/12`; PASS on unchanged + 3 appends with `actual_rc=2` |
| `probe-all-fail-rc1.py` — all checks FAIL, exits 1 | `0/12` exit 1 | M4 `8/12`; every `expected_rc=1` case accepted |
| `corpus/evidence/round74/correction-count.py` (positive) | `12/12 PASS` exit 0 | M5 `2/12`; M6 `11/12` (only `receipt-change`) |

Seed values and per-case lines are in the `direct-*.txt` logs listed at the end.

## Survivor findings (instrument coverage, not contract change)

**F1 — order randomisation is load-bearing but battery-untested (M2).**
Forger rejection is `rc == 1 and marks < total`; the three content cases alone keep every
source-blind subject below full marks. Removing the shuffle leaves the battery at
`PASS 5/5 2/2` while the frozen r74 oracle climbs 3/12 → 9/12 and a 12-entry oracle that reads no
repository bytes reaches 12/12 exit 0. The battery's only order subject is the frozen 9-entry r74
script, so QUALITY 120 is implemented by v2 but not covered by the QUALITY 126 battery. A
battery-visible order oracle would need v2's declared order encoded (not present among the seven
salted subjects).

**F2 — exit-2 rule is untested (M3).**
No battery subject ever exits 2, so the documented rule "an exit of 2 is never scored in the
matrix's favour" never fires. M3 marks an exit-2 full-mark subject PASS on all four
`expected_rc=0` cases (4/12, versus 0/12 pristine) and the battery still prints PASS.

**F3 — check-id/summary comparison is not pinned (M4).**
Because rejection only requires fewer than full marks, a matrix that ignores check ids still
rejects all five forgers (constant-fail 8/12 < 12) and the battery prints PASS. Measured loss:
constant-fail 4/12 → 8/12, and the all-FAIL probe rises 0/12 → 8/12.

**Non-findings (what the battery does pin).** M1 shows the content cases are the sole barrier to
diff-only and naive-grep (both accepted 9/9 without them). M5 and M6 show the positive control is
a real soundness floor: destroying fixture isolation drops the correct counter to 2/12, and
pointing the receipt case at an unmonitored path gives exactly one failing case (`receipt-change`,
11/12) for both independent positives. M7 shows the battery's own pass predicate and labels are
load-bearing (0/5, exit 1). None of these mutations changed the frozen contract; each was applied
in scratch only.

## Evidence and reproduction

Files in `.ufo/waves/round-75/w1/R75Mutation/`:

- `kill-matrix.md` — this table.
- `commands.txt` — exact command lines and exit codes.
- `battery-baseline.txt`, `battery-restored-baseline.txt`,
  `battery-control-relocated-pristine.txt`, `battery2-*.txt`,
  `battery-m1…m7…txt` / `battery-m7-battery-mutant.txt` — full battery logs.
- `direct-*.txt` — per-case matrix logs with seeds and rev hashes.
- `artifacts/` — the seven mutants, three probes, generator, and before/after frozen digests.

Restoration: frozen digests before == after; pristine battery rerun on the frozen matrix prints
`BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0; `git rev-parse HEAD` unchanged; the only
`git status` entries under `corpus/evidence/{round74,round75}` were two untracked files written by
sibling seats during this wave (`controls/battery-stability-r75.txt`,
`controls/mutation-battery-parser-slip.txt`) — neither was written or modified by this seat.
Scratch root deleted (`test ! -e` passed).

## Limits

One scratch root; two battery invocations per survivor (each run covers two matrix seeds, so
four matrix runs) and one direct run per probe. M3/M4 direct counts are structurally fixed (4 expected-0 cases, 8 expected-1 cases) and
independent of permutation; M2's 12/12 is deterministic once the shuffle is removed. The only
permutation-sensitive numbers are the r74 oracle's 3–9/12 range. These probes measure these
instruments at these frostings; they do not touch the claims' recorded limits.
