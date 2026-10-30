# Attack16 — C1 frozen-case bypass attack (round65, seat-scoped)

Seat: Attack16 (leaf critic, no subagent dispatch, no production writes).
Scope: attack the absolute of C1's frozen 20 cases — inspect counter branch and reference
validator, construct nearby forged/malformed receipts *outside* the frozen 20, state whether
the frozen counter detects each. Bounded isolated probes only; frozen bytes untouched.

## Inputs inspected (frozen)

- `corpus/evidence/round65/claims.md` (freeze f99de3bdf…, HEAD verified == freeze).
- `corpus/evidence/round65/c1-count.py` — frozen counter, 20 fixed cases, fixed BASE d6ed8155….
- `corpus/evidence/round65/controls/ref-receipt-pin.py` — prefreeze reference validator
  (de facto behavior arbiter; claims state it is not a hidden answer).
- `tools/receipt-pin.py` — **absent** (before control state; another seat's acquisition target).

## Method

28 crafted receipts, each a single-field mutation of the canonical valid receipt
(`REVISION/EXIT/SHA256 …/blank/measured output` bound to blob `BASE:SKILL.md`,
sha256 4355e16a…). Each run once against the reference validator
(`--root <lane> --revision BASE`). All 28 names disjoint from the frozen 20
(zero overlap). Fixtures + per-case rc/stdout in `attack16-fixtures/` and
`attack16-ref-probe-results.json`.

## Finding 1 — 22 malformed classes the frozen counter never runs (counter-silent)

The reference rejects (rc=1, `RECEIPT_PIN=FAIL`) all of these; the frozen counter has **no
case** for any of them. A defective target validator that accepts any one class still scores
CASES=20/20 C1=PASS:

| class | example mutation | reference verdict | frozen counter coverage |
|---|---|---|---|
| exit-leading-zero | `EXIT=007` (forged exit 7, int-parseable) | FAIL header/body | none |
| exit-double-zero | `EXIT=00` | FAIL header/body | none |
| exit-trailing-space | `EXIT=0␣` | FAIL header/body | none |
| exit-tab | `EXIT=0⇥` | FAIL header/body | none |
| exit-0255 | `EXIT=0255` | FAIL header/body | none |
| exit-plus-one | `EXIT=+1` | FAIL header/body | none |
| exit-hex | `EXIT=0x0` | FAIL header/body | none |
| exit-space-prefix | `␣EXIT=0` | FAIL header/body | none |
| separator-space | blank line is `␣` | FAIL header/body | none |
| separator-tab | blank line is `⇥` | FAIL header/body | none |
| body-whitespace | body `␣␣␣` only | FAIL header/body | none (frozen `no-body` ≠ whitespace body) |
| bom | UTF-8 BOM prefix | FAIL header/body | none |
| sha256-no-path | digest line without path | FAIL digest header | none |
| sha256-double-space | two spaces before path | FAIL blob/digest | none |
| sha256-space-path | path is a single space | FAIL digest header | none |
| sha256-tab-sep | tab instead of space | FAIL digest header | none |
| revision-upper | uppercase hex revision line | FAIL header/body | none (frozen `wrong-revision` is zeros, `short-revision` is 8 chars) |
| revision-trailing-space | `REVISION=<hex>␣` | FAIL header/body | none |
| revision-leading-space | `REVISION=␣<hex>` | FAIL header/body | none |
| path-trailing-slash | `SKILL.md/` | FAIL path | none |
| path-dot-prefix | `./SKILL.md` | FAIL path | none |
| empty-file | zero bytes | FAIL header/body | none |

Strongest single bypass: **exit-leading-zero (`EXIT=007`)**. Any validator that parses exit
with plain `int()` and only range-checks ≤255 (instead of the reference's anchored
`(?:0|[1-9][0-9]{0,2})` grammar) accepts a forged non-canonical exit; the frozen counter's
three exit cases (`negative-exit`, `overflow-exit`, `word-exit`) do not intersect the
leading-zero/whitespace grammar class, so the counter stays green. Same shape for the
`sha256` separator grammar (`[hex]{64} SP .+`) and the exact `REVISION=`/`EXIT=` line
equality — a target that trims lines or splits on whitespace differently accepts whole
families the frozen 20 never probe.

Frozen-counter detection verdict for Finding 1: **undetected by construction** — the counter
only exercises its 20 fixed cases; these 22 classes are outside the frozen case absolute.
Detection would require cases the freeze forbids adding.

## Finding 2 — 4 classes even the reference admits (spec-leniency, not C1 failures)

`crlf` (CRLF endings), `cr-only` (CR-only), `body-smuggle` (body carries forged
`REVISION=0…0 / EXIT=255 / SHA256=f…f injected.md` lines), `nul-in-body` (NUL in output)
all return rc=0 `RECEIPT_PIN=PASS` from the reference. Two benign variants
(`no-trailing-newline`, `extra-trailing-blank`) also pass.

- These are **not** counter bypasses in the C1 sense: the prefreeze reference is the de facto
  format arbiter and it accepts them (Python `splitlines()` eats `\r`; body is free-form).
- Two residual hazards, out of C1's declared scope but worth an L1 note:
  1. **parser differential** — `body-smuggle` means a downstream consumer that scans the
     whole file (rather than the first 4 lines) sees different headers than the validator.
  2. **line-ending canonicalization** — if a future consumer requires LF-only receipts,
     the reference's acceptance of CRLF/CR is a latent interop defect. Neither is a C1
     predicate violation.

## Finding 3 — blob-binding discrimination is incidental, not structural

Claims require "digest binds the Git blob at the declared revision; no working-tree hashing."
The frozen counter enforces this only when the working tree differs from BASE at the named
path. Measured this round: `SKILL.md` working-tree sha256 2ccca333… ≠ blob 4355e16a… (13
dirty files at freeze HEAD), so the frozen `valid` case *currently* discriminates a
working-tree hasher (it would FAIL). But the counter carries no case that structurally
guarantees blob-vs-worktree binding (e.g., a receipt for a path whose worktree bytes equal
the digest but whose BASE blob differs); a clean tree at BASE would make the two
implementations indistinguishable at 20/20. Low risk this round, structurally unproven.

## Out-of-scope absolute (recorded, not attacked)

The format binds *reported* exit only. A receipt with valid digest and `EXIT=0` passes while
the measured run actually exited nonzero — execution-authenticity forgery the frozen counter
cannot and does not claim to catch (claims.md: "not a claim to cryptographic execution
authentication"). C2 addresses identity vs authenticity as knowledge, not counter coverage.

## Smallest safe correction

Freeze forbids counter edits, so no in-round change is available or proposed to frozen bytes.
For L1 integration notes only:
1. Treat Finding 1 as the coverage map for a **future round's extended counter** (do not
   touch round65's 20): add at minimum `exit-leading-zero`, `exit-trailing-space`,
   `separator-whitespace`, `body-whitespace`, `sha256-no-path`, `revision-upper`,
   `path-dot-prefix`, `bom`.
2. Record Finding 2's parser-differential/CRLF leniency as a documented reference limitation
   (candidate for the round65 knowledge entry's "source limitations" section), not a C1 defect.
3. If a later round wants structural proof of blob binding, add a case whose digest matches
   worktree bytes but not the BASE blob (requires a deliberately dirty fixture path).

## Evidence

- `attack16-ref-probe-results.json` — 28 fixtures × (rc, stdout) against the reference.
- `attack16-fixtures/*.txt` — the 28 crafted receipts (canonical generator values in Finding 1 table).
- Freeze identity: lane HEAD == f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd (read-only
  `git -C … rev-parse HEAD`). No frozen bytes altered; no git/jj mutations; scratch
  `/fast/scratch/hyaku/chousa-r65/Attack16` deleted after receipts copied.
- Tooling: no installs required (python3 + git only).
