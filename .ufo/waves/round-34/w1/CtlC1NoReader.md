# C1 no-reader / junk controls — round 34 wave 1

Access date: 2026-10-23. Axes: detector discrimination, evidence fidelity, isolation/restoration.

## Verdict

All five requested controls **MISSES** on two fresh, distinct seeds each. None **MEETS-TARGET** (30/30).
The frozen counter did not let a no-reader through. Its per-id truth comparison and required
`CLAIM_LINE_MISMATCH` finding reject synthetic labels (`corpus/evidence/round34/c1-count.py:280-305`).

Strict mutation-testing verdict: **INCONCLUSIVE**, not killed: pristine and restored base bytes both
already fail P1 at **19/30**. The separate adversarial-control verdict remains MISSES for each control.
No candidate implementation was scored, no counter was edited, and no production file or VCS state was changed.

## Inputs and executed detector

Read `corpus/evidence/round34/claims.md:1-94` first, then the frozen counter docstring at
`corpus/evidence/round34/c1-count.py:1-59`.
Located quote: “An id printed on two CLAIM lines scores "none".”
(`corpus/evidence/round34/c1-count.py:53`, accessed 2026-10-23).

- Base gate SHA-256: `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.
- Frozen counter SHA-256: `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`.
- Cwd for every detector: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
- Scratch `S=/fast/scratch/hyaku/chousa-r34/w1/CtlC1NoReader`; artifact directory `A=.ufo/waves/round-34/w1/CtlC1NoReader` (relative to lane root).
- `C=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py`.

Executed command form (actual argument arrays, PIDs, exit codes and stdout are preserved in
`A/fast-run-outputs.json`, `A/tool-run-outputs.json`, and `A/restored-run-output.json`):

```sh
timeout --signal=TERM --kill-after=15s 1700s prlimit --nproc=32768 --as=2147483648 env C1_TMP="$S" TMPDIR="$S" python3 "$C" --gate "$S/<gate>.sh" --seed <seed> --receipt "$A/<gate>-s<seed>.json"
```

The initial tool-run controls wrap this command in `bash -c`, printing `RUNNER_PID` then `exec`ing
`prlimit`; the stored command arrays include that exact wrapper. The counter's own gate timeout
is unchanged at 1500 s (`c1-count.py:73,275-276`). At most four seat-owned counters were active.
Every scored primary command exited **1**, every primary gate exited **1**, and no primary gate timed out;
all primary receipts have `predicate_holds=false`. No network or package installations.

## Controls, counts, receipts

For every row, receipt names are `A/<gate>-s<seed>.json`; the archived mutant is `A/<gate>.sh`.
Each listed seed is outside 3401–3409. The primary ten seeds are all distinct.

| Control | Gate | Seed 1 | Seed 2 | LONGSPAN_MATCH seed 1 / seed 2 | Verdict |
|---|---|---:|---:|---|---|
| (a) always supported | all-supported | 14131481393545464 | 16090834993729923 | 12/30 / 12/30 | MISSES |
| (b) always unsupported | all-unsupported-fast | 25071799564550534 | 59624842069971598 | 16/30 / 16/30 | MISSES |
| (c) random labels | random-labels | 32106857661956379 | 22299473518078373 | 4/30 / 12/30 | MISSES |
| (d) no CLAIM lines, DRIFT exit 1 | no-claims | 40569253127476186 | 21032068685002936 | 0/30 / 0/30 | MISSES |
| (e) mislocated iff line present, else supported | record-fields | 44255926757557515 | 56321448545446320 | 12/30 / 12/30 | MISSES |

Actual per-class output, compacted only where both seed outputs are identical:

| Class | a1=a2 | b1=b2 | c1 | c2 | d1=d2 | e1=e2 | pristine=restored |
|---|---|---|---|---|---|---|---|
| long-verbatim-ml | 3/3 | 0/3 | 1/3 | 1/3 | 0/3 | 3/3 | 0/3 |
| long-verbatim-1l | 2/2 | 0/2 | 1/2 | 0/2 | 0/2 | 2/2 | 0/2 |
| long-edge | 2/2 | 0/2 | 0/2 | 1/2 | 0/2 | 2/2 | 0/2 |
| long-mut-head | 0/2 | 2/2 | 0/2 | 2/2 | 0/2 | 0/2 | 2/2 |
| long-mut-tail | 0/2 | 2/2 | 0/2 | 1/2 | 0/2 | 0/2 | 2/2 |
| long-mut-mid | 0/3 | 3/3 | 1/3 | 1/3 | 0/3 | 0/3 | 3/3 |
| long-split | 0/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 |
| long-glued-left | 0/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 |
| long-glued-right | 0/2 | 2/2 | 0/2 | 1/2 | 0/2 | 0/2 | 2/2 |
| long-line-bound | 2/2 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 | 0/2 |
| long-line-wrong | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 | 2/2 | 0/2 |
| short-verbatim | 3/3 | 0/3 | 1/3 | 2/3 | 0/3 | 3/3 | 3/3 |
| short-mut | 0/3 | 3/3 | 0/3 | 1/3 | 0/3 | 0/3 | 3/3 |

The raw output JSONs retain the printed per-class lines. Every receipt records class counts,
per-id misses, seed, gate hash, counter hash, gate rc, elapsed time and timeout state.

## Smallest behavior-bearing changes

All controls were copied from the hashed base gate, never from a candidate.

- (a): replace only base `verify_claims` span block at 1803–1877. Set `observed=supported`, `at=-`;
  emit a synthetic warning so the required DRIFT/exit-1 guard is satisfied rather than trivially
  scoring zero because all expected labels are supported. Final archived lines 1803–1807.
  Source path/stat checks remain; fixture sources have no sha pin, and no source content is read or searched.
- (b): early return at `verify_claims`, archived lines 1616–1624. Read only claim ids with a Bash
  regex; print unsupported and DRIFT/exit 1. No source opened.
- (c): early return, archived lines 1616–1632. Read ids; choose supported/unsupported/mislocated
  using Bash `RANDOM % 3`; print the mismatch finding iff the chosen label is mislocated.
  No source opened. Bash random choices are not determined by the fixture seed; these are the actual observed runs.
- (d): two-line early return, archived lines 1616–1617: print `RESEARCH_GATE: DRIFT (control=no-claims)`
  and return 1; do not read claims or sources. The counter records every id as `none`.
- (e): early return, archived lines 1616–1631. Read only id and presence of a line field from the
  JSONL record; print mislocated and its mismatch finding iff present, otherwise supported.
  No source opened. This deliberately confuses correctly bound and incorrectly bound line records.

Archived mutant SHA-256 values:

| Gate | SHA-256 |
|---|---|
| all-supported.sh | `d2f21e4f1e2fb6949e02da40f60bc2a4675ace3058fe4f75a8bb51e798fde149` |
| all-unsupported-fast.sh | `b9be72ee0bcb83449c9e3335c5827c8ebe968c15d6c0a61f31645fd4e4ce630f` |
| random-labels.sh | `0bb3e23095922eac2b4c3d2aa098915a933bb98684a1df11ec9fc32804f4b598` |
| no-claims.sh | `ec13c3d2a2c29f3f011b1f0c67bec4e4b22bad4537fd2f33df4d3405131f540a` |
| record-fields.sh | `a9f36b2ac1ab001b3babffca5baf247f90ab3574bfd1d507247784d32ef21e0f` |

## Pristine, restoration, process completion

Same frozen detector, same seed **915318497153087**, on pristine and restored identical bytes:

| Run | Gate argument | Counter/gate rc | Output | Gate elapsed |
|---|---|---|---|---|
| pristine | S/base-pristine.sh | 1 / 1 | LONGSPAN_MATCH=19/30 | 1082.728 s |
| restored | S/no-claims.sh | 1 / 1 | LONGSPAN_MATCH=19/30 | 1334.186 s |

Receipts: `A/base-pristine-s915318497153087.json` and
`A/base-restored-s915318497153087.json`. Both have `gate_timed_out=false` and the base hash.
The receipt stderr contains “Argument list too long”
(`A/base-pristine-s915318497153087.json:11`, accessed 2026-10-23).

Restoration commands used `timeout 30s cp S/base-pristine.sh S/<mutant>.sh` after scoring, then
`timeout 30s sha256sum S/*.sh <lane>/tools/research-gate.sh <counter>`.
All **seven** scratch gate files, including the auxiliary control, have restored SHA-256
`43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`. The restored detector used `no-claims.sh` as one representative of these
identical bytes. Production gate and frozen counter hashes remained unchanged.
Evidence: `A/restoration-evidence.json`, `A/restored-run-output.json`.
The five primary mutated gate copies remain archived in A; the largest archived gate is 358361 bytes,
below 1 MiB. All launched runner processes completed naturally; no seat-owned background process remains.
Recorded PIDs and full commands are in the output JSONs; restored runner PID was 3087830.

## Failed attempts, auxiliary observations, limits

- Initial pristine command used the same baseline arguments but `--nproc=2000` and no PID-printing
  wrapper. It exited 1 before launching the gate: `BlockingIOError: [Errno 11] Resource temporarily unavailable`
  at `c1-count.py:275` / `subprocess.py:1920`; no receipt. A bounded process-count command returned 231;
  thread count was not measured. Cause of fork failure is unproved. Retried with `--nproc=32768`,
  retaining the 2 GiB address-space cap. That completed with the pristine 19/30 result above.
- One async request for the slow unsupported control's second seed was refused with
  `Background job limit reached (100)` before a job id was returned. The final fast control avoids
  the shared tool background queue and preserves the same counter and bounds.
- Auxiliary span-block unsupported control (`A/all-unsupported.sh`, hash
  `02f106193e1ef3fff1f28f13f1a71b4dd3cea31678a41f22c2a427d478dad5ad`) completed seed
  71684067427313382 at 16/30, rc 1, 891.716 s. Receipt: `A/all-unsupported-s71684067427313382.json`.
  Two additional fast unsupported runs (71684067427313382 and 6566496732069889) also gave 16/30.
  They are retained as auxiliary receipts, not substituted for the two uniquely fresh primary seeds.
- Random/fields span-block prototypes were never scored; they were restored to base before their
  early-return controls were inserted. This avoids expensive parsing unrelated to these junk verdicts.
- Only the assigned controls and base restoration probe were exercised. No candidate, repair,
  build, gate selftest, integration or shipping judgment is claimed. No counter changes were made.
  The failed pristine predicate prevents a killed-mutant conclusion despite all five controls missing P1.

Additional provenance: `A/probe-metadata.json`. All A paths above expand to `.ufo/waves/round-34/w1/CtlC1NoReader`.
