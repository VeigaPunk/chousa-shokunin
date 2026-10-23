# MutC2Windows — C2 window controls (round 34 attempt 2, wave 2a2)

Scope: the three shortcut-window controls assigned to this seat, scored against the frozen
C2 counter. Read-only on lane production files; every experiment in
`/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2Windows/` (scratch) and
`.ufo/waves/round-34/w2a2/MutC2Windows/` (artifacts).

Pin check before any run (lane tip frozen at `707da8184a0fc4d10ab3f17271556cdf364f0af5`;
git HEAD is `fe3db76c` = the later spec re-freeze commit, which does not touch `tools/`):

```
$ git show 707da8184a0fc4d10ab3f17271556cdf364f0af5:tools/research-gate.sh | sha256sum
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b  -
$ sha256sum tools/research-gate.sh
a6307edf…995b  tools/research-gate.sh
$ git diff --stat 707da8184a0fc4d10ab3f17271556cdf364f0af5 HEAD -- tools/ corpus/evidence/round34/c2-count.py
(no output)
$ sha256sum corpus/evidence/round34/c2-count.py
8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173  (== every receipt's counter_sha256)
```

Baseline (same detector on pristine bytes): `DEADZONE_MATCH=37/37`, counter exit 0,
gate exit 1 with `RESEARCH_GATE: DRIFT` (receipt `pristine-a6307edf-s5107.json`,
`gate_sha256=a6307edf…`).

## Method

Each control is a byte-copy of the landed gate with only the span-offset enumerator
replaced (`tok_span_offsets` routing at `tools/research-gate.sh:1636-1650`; the shipped
matcher functions at `:1566-1695` untouched). Everything downstream — `tok_left_ok`/
`tok_right_ok` (`:1520-1565`), `tok_span_at`/`tok_span_all` (`:1644-1690`), line binding
(`:1883-1935`) — is the shipped code. Scored with the frozen counter, `cwd` = lane root,
`C2_TMP` = scratch:

```
$ C2_TMP=$S/tmp timeout 900 python3 corpus/evidence/round34/c2-count.py \
    --gate $S/ctl<N>.sh --seed <5107|5113> --receipt $A/ctl<N>-s<seed>.json
```

Seeds 5107 and 5113 are fresh (none of 5011/5023/5033/5047). Control hashes are in the
artifacts; each receipt's `gate_sha256` binds exactly the bytes scored.

## Results

| control | W | shape | s5107 | s5113 | counter exit | verdict |
|---|---|---|---|---|---|---|
| A `ctlA.sh` (63a40324…) | 4096 | head window delimited on left **somewhere** + tail window delimited on right **somewhere** | 29/37 | 29/37 | 1, 1 | **MISSES** |
| B `ctlB.sh` (b5c3916d…) | 16384 | same, 16 KiB windows | 31/37 | 32/37 | 1, 1 | **MISSES** |
| C `ctlC.sh` (58762c90…) | 16384 | head at *o*, tail at *o+len−W* (consistent offsets) | 37/37 | 37/37 | 0, 0 | **MEETS-TARGET** |
| supplementary `ctlC4096.sh` (842f077e…) | 4096 | consistent offsets (real ~24.5 KB gap) | 29/37 | — | 1 | MISSES |

Per-class lines (seed 5107; seed 5113 differs only where noted):

Control A (`DEADZONE_MATCH=29/37`, misses 8):

```
dz-verbatim-ml 3/3  dz-verbatim-1l 2/2  dz-edge 2/2  dz-mut-head 2/2  dz-mut-tail 2/2
dz-mut-center 0/2  dz-decoys 0/5  dz-decoys-exact 2/2  dz-decoys-line-wrong 1/2
dz-split 2/2  dz-glued-left 2/2  dz-glued-right 2/2  dz-glued-then-valid 1/1
dz-line-bound 2/2  dz-line-wrong 2/2  short-verbatim 2/2  short-mut 2/2
MISS …dz-decoys truth=unsupported observed=supported  (x5)
MISS …dz-mut-center truth=unsupported observed=supported  (x2)
MISS …dz-decoys-line-wrong truth=mislocated observed=supported  (x1)
```

Control B (seed 5107 `31/37`, seed 5113 `32/37`): only `dz-decoys` 0/5 on both; seed 5107
additionally loses one `dz-decoys-line-wrong` (1/2), seed 5113 keeps 2/2. Everything else 2/2 or 3/3.

Control C (`37/37`): every class full on both seeds, `misses=[]`, counter exit 0,
`predicate_holds=true`.

## Finding 1 (important): control C MEETS 37/37 because it is not a shortcut at this length

For a span of `len ∈ {32765,32766,32767}` and `W=16384`, the last window starts at
`len−W ∈ {16381,16382,16383}`, which is **less than W**: the two windows overlap by 1–3 bytes
and their union is the whole span (`[0,16384) ∪ [len−16384,len) = [0,len)`). There is no
uncompared middle, so every byte of a reported occurrence is compared and C is byte-equivalent
to the exact matcher **on this surface**. Its 37/37 is the correct detector output (a true
matcher passes), not a counter escape.

Direct probe (scratch fixture `probe/`, record `c164330e58e`, span 32765, one letter changed
at offset 16382 = len//2 in the source, claim still `expect=supported`):

```
ctlA: CLAIM id=midprobe expected=supported observed=supported  at=lines:31-646
ctlC: CLAIM id=midprobe expected=supported observed=unsupported at=-
```

A ignores the 24,573-byte middle; C compares it. The counter *does* catch the same
consistent-offset shape once a real gap exists: `ctlC4096` (W=4096, gap ≈24.5 KB) scores
29/37. So the counter's discriminating power is a property of gap arithmetic, and for
W=16384 on 32765..32767 the assigned control shape carries no defect to detect.

## Finding 2: why the independent-window controls miss

- A (W=4096): the head/tail checks are satisfied by the *exact* bytes at both ends while
  ~24.5 KB in the middle is never compared. Consequences measured: a centre mutation
  (`dz-mut-center`, ±64 of len/2 — inside A's gap) reads `supported` (2 misses); a decoy
  edited outside both 4 KiB windows is reported as a full occurrence (`dz-decoys` 0/5);
  when the decoy whose lines the claim names has an intact head, its line range binds and a
  `mislocated` truth reads `supported` (1 of 2).
- B (W=16384): the two windows overlap, so a single-byte decoy edit always breaks at least
  one window *within that decoy* — but the control requires only that each window occur
  **somewhere**, and the 11–12 decoys supply both populations (edits in the head region
  supply the tail window and vice versa). Every `dz-decoys` record therefore reads
  `supported` (0/5 on both seeds). The one `dz-decoys-line-wrong` miss on seed 5107 is the
  same mechanism: the named decoy's head window survived its edit, so its lines bind.
  §C2 of `corpus/evidence/round34/claims-a2.md` (accessed 2026-10-23) declares the decoy
  class exactly for this: "12 near-copies, no exact copy". The counter's `dz-decoys` class
  is what keeps a two-window existence shortcut below target.

## Finding 3 (latent code hazard, not a C2 defect)

`tok_span_offsets_chunk` binds its confirmation length from the **caller's** dynamically
scoped `span` (`tools/research-gate.sh:1655`, `local hay=$1 span=$2 slen=${#span}`): bash
evaluates the whole `local` RHS list before binding, so `${#span}` resolves in the caller's
scope. Measured on this host:

```
$ bash -c 'set -u; f(){ local a=$1 b=${#a}; echo b=$b; }; f hello'
bash: line 1: a: unbound variable
$ bash -c 'set -u; o(){ local p=$1 q=${#span}; echo q=$q; }; g(){ local span=abcdef; o x; }; g'
q=6
```

In the shipped gate every call passes the same value as the caller's own `span`, so the
shipped behaviour is correct; but the function silently mis-confirms if handed a different
span (my controls had to implement their own window lister: `tok_window_offsets`). Worth a
comment or an explicit length parameter; not evidence against C2.

## Build errors I made and caught (measurement honesty)

The first three builds were invalid; only the final builds' numbers are reported above, and
each reported receipt's `gate_sha256` equals the artifact hash listed. For the record:

1. First A demanded *both* edges of each window be token boundaries, so the tail window
   (interior edge = a letter) never qualified: 21/37 with every long supported record
   `unsupported` — baseline failure, discarded.
2. First B routed on `span > 2*W`; with W=16384 that is 32768, so dead-zone spans fell to
   the **landed chunk matcher**: its 37/37 was the gate's own score, not the control's.
   Routing changed to `span > TOK_DIRECT_SPAN_MAX`.
3. First C was overwritten from A after its constant was set and silently ran W=4096
   (instrumented run shows `w=4096`, 29/37 — that file is now kept as `ctlC4096.sh`, whose
   29/37 is the supplementary gap result). Re-set to 16384 and re-scored: 37/37 twice.

## Evidence index

Artifacts `.ufo/waves/round-34/w2a2/MutC2Windows/` (1.5 MB total):
`ctlA.sh` 63a403246b5ebd1eca234fc7e39f24fe8a70dac1f912a109d4008170abf84c57,
`ctlB.sh` b5c3916de9cc5a065682ab94a76d5fd13152558d5e8bd7e39a7feacd3457e221,
`ctlC.sh` 58762c90ac7a667912b8c95a5d7c2d2e63bb16b28b6329b0c778c8a75962978e,
`ctlC4096.sh` 842f077e422ccda4f9621cd6f3b5904e558647c86c7c43f7492e548052948dd5;
`diff-ctl*.patch` (unified diffs vs the landed gate; the only hunks are the constant line,
the added window lister, and the routing branch);
receipts `ctlA-s5107/5113.json`, `ctlB-s5107/5113.json`, `ctlC-s5107/5113.json`,
`ctlC4096-consistent-s5107.json`, `pristine-a6307edf-s5107.json`;
`baseline-s5107.txt`.

Restoration: no lane production file, git index or jj state was written. Post-run check:
`sha256sum tools/research-gate.sh` = `a6307edf…995b` (unchanged), `git status --porcelain
tools/ corpus/evidence/round34/` empty.

## Limits

- Two fresh seeds per assigned control (as required); the supplementary gap control ran one
  seed. Controls are my scratch models of the shortcut shapes, not lane candidates.
- I did not re-run the lane's committed receipts (37/37 ×4) or any C3 check; both are outside
  this seat's target. The counter's own "no committed lower run" clause was not audited here.
- The window controls exercise only `verify-claims`; other gate modes are untouched.
- Runtime per run 30–43 s, far inside the counter's 1500 s bound; no timeout, no `none` scores.
