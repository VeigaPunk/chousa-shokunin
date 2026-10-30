# Attack08 — C1 frozen-case attack (negative-exit neighborhood)

Seat: Attack08 (critic, leaf). Lane chousa round65, freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Scope: attack C1 only. Bounded isolated probes in `/fast/scratch/hyaku/chousa-r65/Attack08` (deleted on exit).
Frozen bytes untouched: validator/counter/claims only read or copied into scratch.

## Assignment

Attack the C1 frozen case `negative-exit`: inspect the counter branch and the reference validator,
construct a nearby forged/malformed receipt bypass **outside** that one case, and state whether the
frozen counter detects it.

## Inspected frozen material

- Counter `corpus/evidence/round65/c1-count.py`: fixed 20-case battery; expected per-case exit plus
  stdout token (`RECEIPT_PIN=PASS` for rc 0; `RECEIPT_PIN=FAIL *` for rc 1). The `negative-exit` case
  is `('negative-exit', v.replace('EXIT=0','EXIT=-1'), 1)`.
- Reference `corpus/evidence/round65/controls/ref-receipt-pin.py` (prefreeze, public): checks
  `lines[0] == 'REVISION='+--revision`, `EXIT=(?:0|[1-9][0-9]{0,2})` and ≤255, digest header
  `SHA256=<64 lc hex> <path>` with `PurePosixPath` non-absolute/no `..`/no-empty/normalized-form
  equality, `lines[3]` empty, nonempty body, then binds digest to `git cat-file blob <rev>:<path>`.
- `tools/receipt-pin.py` target is still ABSENT (acquisition is the predicate's target; confirmed this seat).

Binding review (no weakness found): revision is string-equality against the caller-supplied
`--revision` (40 lc hex pre-validated); exit is regex+range; path traversal and absolute paths are
rejected; digest is recomputed from the immutable git blob. No digest/binding forgery is available
without a SHA-256 second preimage — none exists in scope. All exit-code neighbors of `negative-exit`
(`EXIT=-1`, `256`, `PASS`, `00`, trailing tab) are correctly rejected.

## Counterexample (nearby malformed receipts the validator accepts)

Weakness class: **framing/canonicalization**, from `Path.read_text()` universal-newline translation
plus `str.splitlines()` splitting on `\x0b \x0c \x1c \x85 \u2028 \u2029` in addition to `\n \r \r\n`.
Receipts crafted with correct revision/exit/digest/path but non-canonical framing validate as
`RECEIPT_PIN=PASS` (rc 0) under the frozen reference semantics:

| Variant (evidence file) | Frozen reference | Strict correction (strict3) |
|---|---|---|
| `crlf-every-lf` (CRLF endings) | **PASS (rc 0)** | FAIL rc 1 |
| `cr-only` (CR endings) | **PASS (rc 0)** | FAIL rc 1 |
| `vt-separator` (`\x0b` as "empty separator") | **PASS (rc 0)** | FAIL rc 1 |
| `ff-separator` (`\x0c`) | **PASS (rc 0)** | FAIL rc 1 |
| `fs-separator` (`\x1c`) | **PASS (rc 0)** | FAIL rc 1 |
| `nel-separator` (`\x85`) | **PASS (rc 0)** | FAIL rc 1 |
| `u2028-separator` (`\u2028`) | **PASS (rc 0)** | FAIL rc 1 |
| `body-forged-header-block` (contradictory `REVISION=000…/EXIT=999/SHA256=000…` lines inside body) | **PASS (rc 0)** | PASS rc 0 (by design) |
| `frozen-negative-exit` (the frozen case) | FAIL rc 1 | FAIL rc 1 |
| `lf-valid` control | PASS rc 0 | PASS rc 0 |

Note: a naive `split('\n')`-only fix does NOT close the CRLF/CR hole — text-mode translation in
`read_text()` rewrites `\r\n`/`\r` before any split. Closing it requires bytes-exact reading
(`open(..., newline='')`); probe 2 in the evidence records this intermediate dead end.

## Does the frozen counter detect it?

**No.** (1) The 20-case battery contains none of these variants — it cannot score them.
(2) Calibration shows the battery is *insensitive* to this entire axis: the reference copy, a
`split('\n')` variant, and the bytes-exact `strict3` variant ALL score `CASES=20/20 C1=PASS`; a
missing target scores `CASES=0/20 C1=FAIL missing-target`. A lax validator and a strict validator are
indistinguishable to C1 as frozen. Evidence: `attack08-probe1-transcript.txt`, `attack08-probe3-transcript.txt`.

## Defect vs. tradeoff

- **Framing laxity (CRLF/CR/control-char separators):** fixable defect against the frozen format's own
  words ("empty separator"), but low severity — it cannot forge revision/exit/digest/path binding, only
  smuggle non-canonical framing that still carries a genuine binding. The claims disclaim "general
  parser safety", which plausibly covers line-terminator choice, so this is at the claim's edge, not its core.
- **Forged header block in body:** tradeoff, explicitly by design — the validator is header
  consistency over a single leading block; the body is unauthenticated measured output ("not execution
  authenticity"). Cross-claim note only: such a receipt simultaneously asserts `EXIT=0` (header) and
  `EXIT=999` (body) and validates, which R65-C2's "reported exit" identity readers should be aware of.
- Neither undermines C1's frozen predicate: all 20 frozen cases still bind real blobs at base
  `d6ed8155…`, and the numeric score stays historical 3/10.

## Smallest safe correction

For the validator L1 acquires at `tools/receipt-pin.py` (frozen counter/claims unchanged — freeze
rule respected; all 20 frozen cases still pass, verified): read bytes-exact
(`open(a.receipt, encoding='utf-8', newline='').read()`) and split on `'\n'` only. Implemented as
`attack08-strict3-pin.py`; rejects all seven framing variants, passes `lf-valid`, scores 20/20 on the
frozen counter. Do NOT add cases to the frozen battery (freeze/kill rule). If document-wide "exactly
one of each header" is ever intended, rejecting body lines matching `^(REVISION|EXIT|SHA256)=` is the
follow-up — but that tightens accepted-body semantics beyond frozen evidence, so it should be a new
round's claim, not this one.

## Evidence index (this folder)

- `attack08-probe.py` — probe driver; `attack08-probe1-transcript.txt` (reference+strict1+counter calibration),
  `attack08-probe2-transcript.txt` (splitlines-dominates dead end), `attack08-probe3-transcript.txt` (strict3).
- `attack08-strict3-pin.py` — verified strict validator (bytes-exact read + `split('\n')`).
- `attack08-receipt-*.txt` — the 12 crafted receipts (exact bytes preserved at write time).

## Records

- Tool installs: none. Used preinstalled `python3 3.14.8` and `git 2.56.0` only.
- git use: read-only with explicit `-C` (plus the frozen counter's own read-only `git -C LANE cat-file`).
- No production/fleet writes; no network; scratch deleted on exit.
