# Attack02 — C1 frozen-case attack: post-separator header forgery (round65)

## Verdict
The frozen counter **does not detect** the bypass. A receipt that violates the validator's own
declared format ("Exactly one of each header, in that order", LF-separated header block, single
blank separator) is accepted with exit 0 by the reference validator
`corpus/evidence/round65/controls/ref-receipt-pin.py`, and the frozen counter
`corpus/evidence/round65/c1-count.py` never feeds such inputs — its 20-case list has no
post-separator duplicate and no CRLF case. C1=PASS therefore proves agreement on 20 fixed
strings, not enforcement of the documented format.

## Evidence (bounded probes, scratch only, frozen bytes untouched)
Counter sanity: `python3 corpus/evidence/round65/c1-count.py --tool <ref> --work <scratch>`
=> `CASES=20/20 C1=PASS` (reference passes all frozen cases).

Forged/malformed receipts run against the reference validator
(`--root <lane> --revision d6ed8155e9b4735639a2cf0a3e479c62f2056195`), receipts in `evidence/`:

| probe | mutation vs valid receipt | ref rc | ref stdout |
|---|---|---|---|
| F1-body-exit-injection | append `EXIT=1` line inside body (contradictory exit claim) | 0 | RECEIPT_PIN=PASS |
| F1b-body-revision-injection | append `REVISION=000…0` inside body | 0 | RECEIPT_PIN=PASS |
| F1c-body-full-second-receipt | whole second receipt smuggled after the body | 0 | RECEIPT_PIN=PASS |
| F2-crlf | CRLF line endings throughout | 0 | RECEIPT_PIN=PASS |
| F3-double-blank-separator | two blank lines before body | 0 | RECEIPT_PIN=PASS |
| G1-presperator-duplicate | duplicate `EXIT=0` before the separator (frozen `duplicate` case) | 1 | RECEIPT_PIN=FAIL header/body |
| H1/H2 (contrast) | `EXIT=00`, `EXIT= 1` | 1 | FAIL (over-strict side; defensible canonical form, not a bypass) |

G1-vs-F1 asymmetry is the smoking gun: the validator pins headers only at `lines[0..2]` plus an
empty `lines[3]` (`ref-receipt-pin.py` main: `lines[0]!='REVISION=…'`, regex on `lines[1]`,
fullmatch on `lines[2]`, `lines[3]` falsy check, body `strip()` non-empty). Any header-looking
content **after** the separator is opaque body, so "exactly one of each header" is unenforced.
`splitlines()` additionally normalizes CRLF, so F2 sails through. F1c is the strongest variant: a
downstream consumer that reads the last receipt-looking block is fed a fully forged second receipt
while the first half validates clean.

## Counter-level impact
- Frozen counter: not detected by construction — the case list (`c1-count.py` line 16) contains
  no post-separator duplicate, CRLF, or double-separator variant. The `duplicate` case only
  inserts `EXIT=0` *before* the separator. A tool that special-cases the 20 strings and accepts
  everything else still scores 20/20; the reference itself already accepts all five forgeries, so
  a conforming 20/20 tool need not reject them either.
- Not a measurement-DoS path worth blocking: a hanging tool raises uncaught `TimeoutExpired` and
  crashes the counter (traceback, no CASES line, nonzero exit) — fails closed, noted only.

## Boundary respected
The frozen `nonzero-valid` case (`EXIT=1` + valid digest => exit 0) and the broader
cannot-verify-reported-exit gap are the claims file's explicitly disclaimed territory ("not a
claim to cryptographic execution authentication"); this attack deliberately sits outside that
case. Header claims about revision/digest/path ARE verified against the frozen blob and do fail
closed (wrong/short/upper digest, wrong/short revision, traversal, absolute, missing blob all
rc=1, confirmed by the 20/20 run).

## Classification
Fixable defect (validator enforces less than its docstring declares), not a tradeoff the judge
must reject — but it is unfixable *within* the frozen round: counters, predicate, and denominator
are frozen, and the missing-target control correctly fails 0/20. It does not invalidate C1 as
frozen (interface/consistency coverage on 20 named cases is exactly what was claimed), it bounds
it: C1=PASS does not imply format enforcement beyond the enumerated axes.

## Smallest safe correction (for L1 integration, no frozen-byte changes)
1. Document the gap in the C2 knowledge entry or round-66 notes: accepted-but-noncanonical inputs
   = post-separator header lines, CRLF/CR line endings, doubled separator.
2. If a future round unfreezes the counter: add three cases (body-header-injection, crlf,
   double-separator) expecting exit 1, and make the reference scan `lines[4:]` for
   `^(REVISION=|EXIT=|SHA256=)` and require `\n`-only newlines via `text.split('\n')` instead of
   `splitlines()`.

## Method / hygiene
- Read-only `git -C` on the lane; no frozen-byte alterations; all receipts and the counter work
  dir under `/fast/scratch/hyaku/chousa-r65/Attack02` (TMPDIR-resident, deleted on exit).
- No tools installed this seat. No subagent dispatch (leaf seat). No production writes.
- Evidence: `evidence/` in this folder (6 receipt files + `probe-results.txt`).
