# W2a2 mutant C2 — truncation controls (prefix/suffix 32764 and 8192)

Seat: `chousa-r34-w2a2-MutC2Trunc-7` (leaf; no subagents, no network, lane read-only).
Round 34 attempt 2, wave 2, seat scope: challenge C2's frozen counter (`P2`) with the
natural cheap alternative fix — search only a prefix/suffix of a dead-zone span instead of
confirming the whole span.

## Pins

- Lane tip frozen at `707da8184a0fc4d10ab3f17271556cdf364f0af5`; working-tree `HEAD` is
  `fe3db76` whose only diff is the three `.ufo/waves/round-34/w2a2*` plan files
  (`git diff --stat 707da81 HEAD`), so the gate tree equals the frozen tip.
- Pinned gate: `sha256sum tools/research-gate.sh` =
  `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` (matches `a6307edf687ac0fb`).
  Every scratch copy starts from exactly these bytes.
- Counter: `corpus/evidence/round34/c2-count.py`,
  sha256 `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173` (unchanged; not patched).
- C2's P2 (claims-a2.md): met iff the counter prints `DEADZONE_MATCH=37/37` on each of two
  fresh-seed runs on the landed gate, and no committed lower run exists.

## Controls (scratch only, one function changed)

Each control is a byte copy of the landed gate with **only** `tok_span_offsets_chunk()`
(`tools/research-gate.sh:1621-1649`) replaced; nothing else is edited (see diffs). The
landed routing constant `TOK_DIRECT_SPAN_MAX=32764` (`:1581`) is unchanged, so spans of
32765..32767 and ≥32768 reach the replaced function:

| control | verified bytes | pattern | gate sha256 (scratch) | diff |
|---|---|---|---|---|
| P32764 | first 32764 of the span | `span[:32764]` | `cf3d215892a734706027ed73b2c5cd02cc41685364b8bceb245a9d4819089bff` | `diff-P32764.patch` |
| P8192 | first 8192 | `span[:8192]` | `9d88086770e6cc413456ee9c89a7b4254ec60eae7537cf3c03241b5c6d86e71a` | `diff-P8192.patch` |
| S32764 | last 32764 | `span[len-32764:]` | `22bf5a988521886654f791059450c3ffb880804b15ffbc9111ad6f039eeb5c0f` | `diff-S32764.patch` |
| S8192 | last 8192 | `span[len-8192:]` | `55ba4050ccd948e7ef42de496a67ad0879ab6ede148e17eafbceac45892571a4` | `diff-S8192.patch` |

Design of the attack (deliberately the *strongest* form): the match start of the truncated
pattern is treated as the occurrence offset (for suffix controls it is mapped back with
`start = offset - drop`), and the existing boundary helpers `tok_left_ok`/`tok_right_ok`
(`:1538`, `:1552`) plus line numbers run at the **full** span extent, which the gate still
knows (`${#span}`). So the blur only affects content verification, not boundaries or line
binding — survival below is therefore not an artifact of a naive boundary bug. The
"line binding from the truncated match" variant would be weaker: for the prefix control the
dropped 1..3 bytes are letters by construction (the fixture cuts the span at a word end), and
for the suffix controls bytes 0..2 of a generated span are letters/separator (a newline at
byte 2 needs a 2-letter first word and a newline separator, ≈1% of spans), so truncated-extent
lines would only add kills on `dz-line-bound`-type records.

## Probe: the control violates C2 contract 2 (handcrafted, 4 records)

`probe-transcript.txt` (also `probe-fixture/`), span 32765 bytes = `a` + `b`*32763 + `c`,
source holds the true span (`pad <span> tail`):
`timeout 300 bash gate-<c>.sh verify-claims probe/fx/claims.jsonl --root probe/fx`, exit 1
(DRIFT) for all five gates:

| record | truth | pristine | P32764 | P8192 | S32764 | S8192 |
|---|---|---|---|---|---|---|
| r1 verbatim | supported | supported | supported | supported | supported | supported |
| r2 last byte changed | unsupported | **unsupported** | **supported** (WRONG) | **supported** (WRONG) | unsupported | unsupported |
| r3 first byte changed | unsupported | **unsupported** | unsupported | unsupported | **supported** (WRONG) | **supported** (WRONG) |
| r4 glued right | unsupported | unsupported | unsupported | unsupported | unsupported | unsupported |

This is contract 2's "one byte changed anywhere" read as `observed=supported`: P32764
verifies 32764 of 32765..32767 bytes and silently accepts a span the source does not hold.

## Counter scoring (fresh seeds; never 5011/5023/5033/5047)

Command (cwd lane root, `C2_TMP` per run in scratch, `timeout 1800`):
`C2_TMP=/fast/scratch/hyaku/chousa-r34-a2/w2/chousa-r34-w2a2-MutC2Trunc-7/tmp-<ctl>-<seed> python3 corpus/evidence/round34/c2-count.py --gate <scratch-gate> --seed <seed> --receipt <artifact>/receipt-<ctl>-s<seed>.json`
Counter exit 0 iff `holds == (matched == 37)`; every run recorded `gate_rc=1` (the gate's
required `RESEARCH_GATE: DRIFT` exit), elapsed 28-31 s.

| gate | seeds | labels | verdict |
|---|---|---|---|
| pristine landed (`a6307edf`) | 6101 | 37/37 | baseline OK (harness reproduces P2) |
| **P32764** | 6101, 6103, 6107, 6109, 6113, 6119, 6121, 6127 | **37/37 on all 8** | **MEETS-TARGET (survives)** |
| S32764 | 6101 / 6103 | 37/37 / **36/37** | MISSES (one seed caught: `dz-mut-head`) |
| P8192 | 6101, 6103 | **25/37**, **25/37** | MISSES |
| S8192 | 6101, 6103 | **26/37**, **26/37** | MISSES |

Per-class lines that moved (receipts carry all 17 classes):

- P32764: all 17 classes full on every seed, including `dz-mut-tail=2/2`,
  `dz-mut-head=2/2`, `dz-mut-center=2/2`, `dz-decoys=5/5`, `dz-decoys-line-wrong=2/2`,
  `dz-split=2/2`, `dz-glued-*=2/2`, `dz-line-*=2/2`.
- S32764 seed 6103: `dz-mut-head=1/2`, all others full (`dz-mut-tail=2/2`, `dz-decoys=5/5`).
- P8192 both seeds: `dz-mut-tail=0/2`, `dz-mut-center=0/2`, `dz-decoys=0/5`,
  `dz-decoys-line-wrong=0/2`, `dz-split=1/2`; supported classes full.
- S8192 both seeds: `dz-mut-head=0/2`, `dz-mut-center=0/2`, `dz-decoys=0/5`,
  `dz-decoys-line-wrong=0/2`; `dz-split=2/2`, supported classes full.

## Why the counter let P32764 through (the important finding)

P32764 leaves **at most 3 of 32765..32767 bytes unverified**; for a span of length L it
drops exactly L-32764 ∈ {1,2,3} bytes at the tail. The frozen counter's only classes that
can see this are:

1. `dz-mut-tail` (2 records): `mutate()` picks one letter uniformly in the last 64 bytes
   (`c2-count.py`: `mutate(rng, s, len(s)-64, len(s)-1)`; ≈56 letter positions). P32764 is
   killed only when the mutation lands in the dropped `L-32764` bytes → ≈1/56, 2/56, 3/56
   per record, ≈4-7 % per seed for the two records. Measured fixture (`mut-positions.json`,
   regenerated deterministically; seed-6101 `claims.jsonl` sha256 equals the `--keep` copy,
   `5862c35c614218e1…`): the four tail mutations over seeds 6101/6103 sit at offsets
   32707 (L=32767), 32728 (L=32765), 32762 (L=32765), 32752 (L=32767) — **all < 32764**;
   the closest (32762) is 2 bytes inside the verified prefix. So on these seeds the counter
   had no signal at all, and 8/8 seeds passing is consistent with the ≈93 %/seed pass rate
   (0.93^8 ≈ 0.56).
2. `dz-decoys` (5 records × 12 near-copies): the class's stated power is g**12 for a verifier
   that compares a fraction g of the bytes. At the dead zone g = 32764/32767 = 0.99991, so
   g**12 ≈ 0.9989 — the class **cannot** distinguish a 1..3-byte truncation, because a decoy
   edit lands in the dropped tail with probability ≈3/32765 per decoy. It only has power for
   small g, which is why it does catch P8192 (g=0.25).
3. `dz-split` (2): the split point is drawn in the middle half, so the 32764-byte prefix still
   crosses the split and never matches — correct verdicts, no signal for a small truncation.
4. `dz-glued-*`, `dz-line-*`, `dz-edge`, verbatim classes: boundary and line checks run at the
   full extent in my controls (and a real prefix implementation would know the span length),
   so they are all correct and carry no signal.

Symmetric result for S32764: its blind window is the first 1..3 bytes; it was caught only on
seed 6103, where a `dz-mut-head` mutation sat at offset 2 of a 32767-byte span (drop = 3;
`c4499d88ded`, receipt `S32764-s6103`). On seed 6101 both head mutations were at 18 and 45,
outside the 2-byte blind window → 37/37. Same ≈4-7 %/seed detection rate.

The gate's own selftest is blind the same way: cases 255-257 mutate at offset 16000, not at
the tail — `tools/research-gate.sh:7871` (`dz_mut="${dz_span:0:16000}Q${dz_span:16001}"`) and
`:7891` (`dz_high_mut="…:0:16000}Q…:16001}"`); C1's case at `:7840` likewise. A prefix-32764
gate therefore also passes `--selftest`'s dead-zone cases.

## Verdict

- **P32764 = 37/37 on 8 fresh seeds: MEETS-TARGET (surviving mutant).** P2 as frozen
  (two fresh seeds, 37/37) therefore certifies a gate that violates C2 contract 2 for
  mutations in the final 1..3 bytes, with high probability (≈93 % per two-seed pair);
  the probe demonstrates the violation directly. This is a **counter-coverage finding**,
  not a refutation of the landed gate: the committed gate (`a6307edf`) really does confirm
  the WHOLE span (`[[ ${hay:offset:slen} == "$span" ]]`, `research-gate.sh:1648`), and my
  pristine baseline run (seed 6101) reproduced 37/37 in the same harness. The C2 receipts
  and the landed fix remain intact; what is not established by P2 is that a competing
  near-pass implementation is detected — P2 has almost no power against a verifier that
  drops ≤3 bytes.
- S32764, P8192, S8192: MISSES (S32764 only via a lucky 3-byte head mutation on one seed;
  the 8192 controls die on center/tail mutations and decoys).
- I did **not** amend the counter, TOTAL, or P2 (frozen; counter sha unchanged). A
  discriminating class would need mutations in the last/first 3 bytes specifically (e.g.
  `mutate(rng, s, len(s)-3, len(s)-1)`), which would move detection from ≈4 % to ≈100 %;
  reported as a finding, not patched, and I did not run such a class.

## Limits / honesty

- Only what I ran is claimed; the committed four-seed receipt set (5011/5023/5033/5047) was
  not re-derived here (deliberately fresh seeds; another wave-2 seat owns re-derivation).
- My controls are synthetic gates; the actual landed implementation verifies whole spans. No
  conclusion is drawn about other matcher modes, C1, C3, or gate behavior outside
  `verify-claims`.
- The suffix controls map the truncated match back to the full start (charitable); an
  uncompensated suffix search would fail trivially on every supported record and is not
  informative.
- 8 seeds is a sample, not a probability proof; the per-seed estimate is derived from the
  frozen generator's own mutation draw (uniform over ≈56 letter offsets in the last 64 bytes)
  and the measured offsets.

## Evidence / artifacts

Directory `.ufo/waves/round-34/w2a2/chousa-r34-w2a2-MutC2Trunc-7/` (all files <1 MiB; largest
368,018 B; `df -h /fast` checked, 35 G free before runs):

- `gate-{P32764,P8192,S32764,S8192}.sh` + `diff-*.patch` (one-hunk diffs vs pristine),
  hashes as tabled above.
- 15 counter receipts `receipt-*.json` (`schema=chousa-r34-c2-receipt/v1`, `counter_sha256`,
  `gate_sha256`, per-class lines, misses; e.g. `receipt-P32764-s6101.json` label 37/37,
  `holds=true`, `gate_rc=1`).
- `probe-transcript.txt`, `probe-fixture/`, `mut-positions.json`
  (`sha256 54c809906730a50a6abb4f44507e89c16d0bbdd43238089f9488e9e70ce678aa`).

Scratch (large logs/kept fixture): `/fast/scratch/hyaku/chousa-r34-a2/w2/chousa-r34-w2a2-MutC2Trunc-7/`
(`out-*.txt`, `err-*.txt`, `rc-*.txt`, regenerated fixtures). No lane production file, jj
state, index, or visible-tree file was written; no process was signalled; every command was
wrapped in `timeout` (≤1800 s); no network access.

One transient lane-tree write: importing the frozen counter to recompute mutation offsets
(`importlib` on `corpus/evidence/round34/c2-count.py`) wrote
`corpus/evidence/round34/__pycache__/c2-count.cpython-314.pyc` (31,354 B, 16:00). I removed
that directory; `git status --porcelain` afterwards shows only `?? .ufo/waves/round-34/w2a2/`,
the same as before the run.
