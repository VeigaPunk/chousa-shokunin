# R78ExecC — residual-channel probe: v5 is defeated by line-deleting content normalisation

Seat: `R78ExecC`, lane `chousa` round 78, wave 1. Leaf only: no dispatch, no network, no
lane/fleet git mutation, no production edits. Frozen instruments were read and never edited
(both digests below match `corpus/evidence/round78/claims.md`).

**Headline.** I built the probe the frozen limits predict — a MATRIX that scores no case and
classifies its `--counter` purely by content after deleting the inert salt statement — and
**`matrix-battery-v5.py` passes it**: `BATTERY=PASS forgers_rejected=11/11 positive=2/2
oracle=REJECTED`, exit 0. My normalizer recovered **13 of 13** subject identities. This is
the recorded limit made concrete, not a falsification of C1: C1's predicate is the forge
battery, and its own limits paragraph says the salt "closes the trailing-strip class and not
a normalizer that deletes every unrecognised inert statement". That sentence is true and the
channel is wide open at 13/13.

## Instrument identity (verified, not assumed)

| file | sha256 |
|---|---|
| `corpus/evidence/round78/matrix-battery-v5.py` | `5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0` |
| `corpus/evidence/round77/matrix-battery-v4.py` | `155fafb16b6931449abefb60575029f273959ba4e94a4db48ac22e525f106a3d` |

Both equal the values frozen in `claims.md`. No frozen instrument was edited; a defect is
reported here, never repaired there.

## The probe

`residual-matrix.py` (sha256 `d851b0ffa46a920e0d149705d1a8beb216123b0a6511137223062d84c5154ba9`,
copied to `R78ExecC/`) takes `--counter PATH --work DIR`, never executes the counter, and:

1. **shape pass** — deletes every whole line that is a known inert salt statement:
   `import os as _r78<12 hex>`, `_r78<12 hex> = <int>` (the v5 interior statement) and
   `# salt <16 hex>` (the round-77 trailing suffix, so the same bytes can also be run
   through v4);
2. **brute pass** — deletes one line at a time from the raw text and hashes, so a
   single-line salt of *any* spelling is normalised away without knowing it;
3. sha256 the recovered bytes against the subject table; a recovered digest in the two
   known-positive digests is PASS (exit 0, `LOADER_MATRIX=12/12 MATRIX=PASS`), everything
   else is FORGER (exit 1, `LOADER_MATRIX=0/12 MATRIX=FAIL`);
4. prints a **fabricated** twelve-line `CASE` contract table whose `expected_rc` /
   `expected_failed` cells are copied from the battery's own public contract map — no case
   is run, no fixture is touched.

It uses no `/proc`, no parent `cmdline`, no invocation counting and no order line: this is a
*subject identity* channel only.

## Measurements (exact commands, exit codes, predicate lines)

Scratch root `/fast/scratch/hyaku/chousa-r78/R78ExecC` (deleted before yield); receipts
copied first.

| # | command | exit | predicate line |
|---|---|---|---|
| 1 | `python3 -B corpus/evidence/round78/matrix-battery-v5.py --matrix residual-matrix.py --work …/w5 --runs 1` | **0** | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| 2 | `python3 -B corpus/evidence/round77/matrix-battery-v4.py --matrix residual-matrix.py --work …/w4 --runs 1` | **0** | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| 3 | v5 over `variant-v5shape-only.py` (knows only the v5 spelling) | **0** | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| 4 | v5 over `variant-brute-only.py` (no spelling knowledge) | **0** | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| 5 | v4 over `variant-v5shape-only.py` (control) | **1** | `BATTERY=FAIL forgers_rejected=11/11 positive=0/2 oracle=REJECTED` |
| 6 | `residual-matrix.py --counter mutated.py` (positive + `\n# edited\n`) | **1** | `IDENT recovered=none` · `LOADER_MATRIX=0/12 MATRIX=FAIL` |

Run 1's receipt is 113 lines and its trailer is `RECEIPT_LINES=113`; `wc -l v5.stdout.txt`
is 113, so the trailer is internally consistent on this run.

**Recovery count: 13/13.** `recovery-table.txt` builds one v5-shaped salted copy per
subject (same generator as `salted_copy`: random interior top-level statement, both
spellings), records the line the normalizer deleted, and the probe's `IDENT` line. All
thirteen recovered their exact committed digest `via=shapes`; the two positives exit 0 and
the eleven forgers exit 1. (With only the two positive digests in the verdict table —
the minimum an answer key needs — 2 identities are recovered by digest and the other 11 are
correctly rejected by default; carrying the full table is what turns that into 13/13.)

## What this says about v5's identity leg

- **The v5 salt does not close the class the claims name.** Knowing *only* v5's own salt
  spelling is enough (run 3, exit 0). Run 5 is the discriminating control: the same matrix
  against v4's suffix salt scores `positive=0/2` and exits 1, so run 3's pass is a real
  classification, not a lenient matrix.
- **It also does not raise the bar above one unknown line.** Run 4 deletes one line at a
  time with no spelling knowledge at all and still passes v5 at 13/13.
- **Against this class v5 is not stronger than v4.** The same bytes pass both (runs 1 and
  2); the interior-statement change only defeats the *trailing-suffix* strip that
  `forgers/a1-hash-identity.py` performs. A normalizer that deletes the inserted statement
  recovers the committed bytes exactly, because the insertion leaves every other byte
  untouched and the original digest is a public constant.
- **Consequence for the predicate.** v5's `BATTERY=PASS` is satisfiable by a matrix that
  never opens the counter as a program. The ORDER, QUIET, CONTENT and RECEIPT legs are all
  orthogonal to this channel and none of them observes it; the content leg in particular is
  satisfied by copying the public contract map.

This is the honest reading of `claims.md`: the content leg is a shape requirement, the salt
closes the trailing-strip class only, and `RECEIPT_LINES` exposes an append rather than
preventing it. My receipt adds the missing number to that sentence: **13/13 recovered**.

## Fail-closed controls

- **Mutated positive → FORGER** (run 6): the probe is content-keyed and does not accept a
  near-miss, so the passes above are not an "always PASS" artifact.
- **All eleven forgers rejected in every run** (runs 1–5, `forgers_rejected=11/11`), so the
  probe's verdict is a genuine two-way split of the thirteen subjects.
- **Run 5 fails on v4**, so the v5-only variant is specific to the v5 salt shape and the
  battery's positives leg can fail.

## Risks and limits of this measurement

- The probe proves the *class*, not any particular successor: a matrix that classifies by
  content identity is correct for these thirteen subjects and would be wrong for any
  subject whose digest it does not carry. It says nothing about arbitrary-counter
  unforgeability, which `claims.md` already disclaims.
- The recovery table is one draw of the v5 salt RNG (`secrets`); the two battery runs drew
  their own salts and all thirteen classified correctly in each, so the result is not
  dependent on one lucky insertion point. Insertion position and spelling are both handled:
  the shape pass matches whole lines anywhere, the brute pass matches any single line.
- **A limit, not a repair (for the L1, never applied to a frozen instrument):** the only
  closure I can see for this class is a salt that changes the bytes any content identity
  depends on — e.g. a per-copy, semantics-preserving re-render (identifier renaming) of the
  subject — so that no line deletion recovers a committed digest. Line insertion cannot do
  it. Recording that as a successor-criterion candidate is a claim-level decision, outside
  this seat.

## Tooling

No tool was installed, upgraded or invoked through pacman (`uv tool`, `npx`, official
binaries and the host package manager were untouched; the host-wide pacman pause was not
exercised). Only `python3` (stdlib) and `sha256sum` were used.

## Files

`.ufo/waves/round-78/w1/R78ExecC/` — `residual-matrix.py`, `variant-v5shape-only.py`,
`variant-brute-only.py`, `recovery-table.py`, `recovery-table.txt`, `v5.stdout.txt`,
`v5.stderr.txt`, `v4.stdout.txt`, `v4.stderr.txt`, `variant-*.stdout.txt`,
`variant-v5shape-only-v4.stdout.txt`, `mutation-control.txt`, `MANIFEST.txt` (digests,
commands, exit codes). Scratch `/fast/scratch/hyaku/chousa-r78/R78ExecC` deleted before
yield.
