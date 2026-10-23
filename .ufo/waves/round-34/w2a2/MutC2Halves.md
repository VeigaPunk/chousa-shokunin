# w2a2 mutation-tester — C2 independent-chunk controls (seat MutC2Halves)

Date: 2026-10-23. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Gate pin: `tools/research-gate.sh` sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
at working HEAD `fe3db76c` and at the frozen wave tip `707da8184a0fc4d10ab3f17271556cdf364f0af5`
(both blobs identical: `git show <rev>:tools/research-gate.sh | sha256sum` run for both; empty
`git diff --stat 707da81..HEAD -- tools/research-gate.sh corpus/evidence/round34/c2-count.py`).
Counter read-only: `corpus/evidence/round34/c2-count.py` sha256
`8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`; not edited.

## What I built (mutation, scratch only)

Four control gates, each a byte copy of the landed gate with **only** the dead-zone chunk matcher
replaced between the exact markers `tok_span_offsets_chunk() {` and `tok_span_at() {`
(prefix/suffix equality of the two files checked in Python: `prefix_equal True suffix_equal True`;
routing, `TOK_DIRECT_SPAN_MAX=32764`, and `tok_left_ok`/`tok_right_ok` untouched):

| control | mutation | sha256 |
|---|---|---|
| ctl2-any | split span into 2 equal byte chunks; supported iff every chunk occurs somewhere (no adjacency), then report every chunk-0 occurrence | `73b7a26366a0354cffff82aa4e70a75f2c997950617c93a59776fd1c2a2a86f4` |
| ctl4-any | same with 4 chunks | `e64f862c0c6191e416e978a023521d2d11841583b226296a9d7aec8869b8536a` |
| ctl16-any | same with 16 chunks | `800aa9ae3859c84c983e82f7fc2fb304d81c824dfe1c42902dd6e61760ec1184` |
| ctl4-ordered (d) | chunks must occur at strictly increasing offsets; adjacency *not* required; report chunk-0 offsets that start a valid chain | `d8f438fbbd5372324dbc1dba7f16ab514393697cb1a36cbc17d4249f0c218074` |

`(d)` reading used: "in increasing order but **not** [required to be] adjacent". The alternative
reading (chunks must be non-contiguous) was probed separately as `ctl4-strict`
(`5b8dc7864df024205695c21e6f2419e2f4da323634aadec89101bf084da9c533`), which requires each next
chunk start to be past the previous chunk end.

Builder: `mkctl.py` (sha256 `7480d5b433026b72c43ef9b15a97a93a7587d70ebedaf954d5a51bd1b8867c0b`);
`bash -n` clean on all five. Scratch gates live in
`/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2Halves/bin/`, copied to this seat's artifact dir
(hashes above), each 367 KB < 1 MiB.

Scoring command (cwd = lane root, `C2_TMP` in scratch, all bounded):
`C2_TMP=<scratch>/run/s<seed>-<ctl> timeout 1750 python3 corpus/evidence/round34/c2-count.py
 --gate <scratch>/bin/<ctl>.sh --seed <seed> --receipt <artifact>/receipts/<ctl>-s<seed>.json`
Seeds **9011** and **9029** (fresh; none of 5011/5023/5033/5047). All gate runs exited rc=1 with a
`RESEARCH_GATE: DRIFT` line (receipt `gate_rc: 1`, `gate_timed_out: false`), so every record scored.

## Baseline (pristine landed gate, same detector)

- seed 9011: `DEADZONE_MATCH=37/37`, exit 0, `predicate_holds true` (receipt `receipts/base-s9011.json`).
- seed 9029: `DEADZONE_MATCH=37/37`, exit 0, `predicate_holds true` (receipt `receipts/base-s9029.json`).

Baseline holds, so the sub-target scores below are real kills, not a broken detector.

## Results

| control | seed 9011 | seed 9029 | verdict |
|---|---|---|---|
| ctl2-any | **31/37** (exit 1) | **32/37** (exit 1) | MISSES — not 37/37 |
| ctl4-any | **30/37** (exit 1) | **31/37** (exit 1) | MISSES |
| ctl16-any | **30/37** (exit 1) | **31/37** (exit 1) | MISSES |
| ctl4-ordered (d) | **30/37** (exit 1) | **31/37** (exit 1) | MISSES |
| ctl4-strict (interpretation probe) | **21/37** (exit 1) | **21/37** (exit 1) | MISSES |

Per-class lines (matched/total), from the frozen counter:

- **ctl2-any s9011** (31/37): verbatim-ml 3/3, verbatim-1l 2/2, edge 2/2, mut-head 2/2,
  mut-tail 2/2, mut-center 2/2, **decoys 0/5**, decoys-exact 2/2, **decoys-line-wrong 1/2**,
  split 2/2, glued-left 2/2, glued-right 2/2, glued-then-valid 1/1, line-bound 2/2,
  line-wrong 2/2, short-verbatim 2/2, short-mut 2/2.
- **ctl2-any s9029** (32/37): identical except **decoys 0/5** and decoys-line-wrong 2/2.
- **ctl4-any s9011** (30/37): all classes full except **decoys 0/5** and
  **decoys-line-wrong 0/2**. **ctl4-any s9029** (31/37): **decoys 0/5**,
  **decoys-line-wrong 1/2**, everything else full.
- **ctl16-any s9011** (30/37): **decoys 0/5**, **decoys-line-wrong 0/2**, all else full.
  **s9029** (31/37): **decoys 0/5**, **decoys-line-wrong 1/2**, all else full.
- **ctl4-ordered s9011** (30/37): **decoys 0/5**, **decoys-line-wrong 0/2**, all else full.
  **s9029** (31/37): **decoys 0/5**, **decoys-line-wrong 1/2**, all else full.
- **ctl4-strict s9011/s9029** (21/37 both): verbatim-ml 0/3, verbatim-1l 0/2, edge 0/2,
  decoys-exact 0/2, decoys-line-wrong 0/2, glued-then-valid 0/1, line-bound 0/2,
  line-wrong 0/2, decoys 5/5, split 2/2, mut-* 2/2 each, glued-left/right 2/2,
  short-* 2/2.

Miss ids and observed values are in the receipts (`misses[]`); e.g. ctl2-any s9011:
`c735bf9cad9 dz-decoys truth=unsupported observed=supported` (all five decoys records,
same pattern), `c1a419787b0 dz-decoys-line-wrong truth=mislocated observed=supported`.

## Why the controls were caught (no 37/37; counter held)

No control met target, so no counter hole was demonstrated on this surface. The load-bearing
class is **dz-decoys (0/5 every control, every seed)**: 12 near-copies each differing from the
true span by exactly one edit, so for any k-chunk partition at least one decoy keeps each chunk
verbatim; a chunk-presence gate finds every chunk somewhere, reports the chunk-0 hits at decoy
starts, and those hits are newline-delimited, so `tok_left_ok`/`tok_right_ok` accept them and the
gate prints `observed=supported` for a span that occurs nowhere. That is exactly the partial-match
hazard the class was designed for. The second killer is **dz-decoys-line-wrong** (0/2 or 1/2):
when the named decoy's edit falls outside chunk 0, the control reports a chunk-0 hit on the named
lines, line binding accepts, and truth `mislocated` is printed as `supported`.

Coverage observation (not a defect, no contract change): **dz-split scored 2/2 under every
control**, so it did not discriminate chunk-independence. Mechanism observed in the runs — the
control's only reported offset for a split record is the chunk-0 occurrence at the first half's
start; the full-span right-boundary probe lands `slen` bytes later, deep inside the second half
(a letter), so the gate rejects the delimited check and correctly reads `unsupported`.
The mutant is killed by the decoy class, not the split class. [INFERENCE from the fixture builder
`build()` and the reported offsets; not separately instrumented.]

The frozen predicate's "no committed lower run" clause is untouched: these runs are scratch-gate
runs, not runs of the landed gate, and nothing was committed (read-only on all lane production
files).

## Restoration / lane integrity

- No lane production file, jj state, or lane git index was written. The lane gate was only read;
  post-run `sha256sum tools/research-gate.sh` = `a6307edf…2995b` (same before and after).
- `git status --porcelain` = exactly one line `?? .ufo/waves/round-34/w2a2/` (this seat's artifact
  tree), `STATUS_LINES=1`; read-only git used elsewhere.
- Counter never modified; `--receipt` files name `counter_sha256 8c0def4d…2173` and the control's
  `gate_sha256`.

## Artifacts (this dir, each < 1 MiB)

`ctl2-any.sh`, `ctl4-any.sh`, `ctl16-any.sh`, `ctl4-ordered.sh`, `ctl4-strict.sh`, `mkctl.py`,
`receipts/{base,ctl2-any,ctl4-any,ctl16-any,ctl4-ordered,ctl4-strict}-s{9011,9029}.json`,
`logs/*.log`. Scratch (not published, cited by path):
`/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2Halves/{bin,run,recv,mkctl.py}`.

## Limits

- Controls mutate only `tok_span_offsets_chunk`; direct-path classes (`short-*`) are necessarily
  unaffected (routing constant unchanged) and are controls, not mutants.
- `(d)` was implemented under the increasing-order reading; the non-contiguity reading
  (`ctl4-strict`, 21/37 both seeds) is reported as an interpretation probe, not as the assigned
  `(d)` control.
- Two seeds per control (9011, 9029); counts for other seeds may vary by a few records in the
  decoys-line-wrong class only.
