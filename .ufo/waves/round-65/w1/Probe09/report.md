# Probe09 — R65-C1 receipt fixture, overflow-exit surface (round65)

Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (lane HEAD at run time; verified via
read-only `git -C <lane> cat-file -t`). Claim probed: **C1** (frozen claims, round65).
Date: 2026-10-30. Seat: Probe09 (leaf, chousa lane). No production writes; no git/jj
mutations; read-only `git cat-file` only, via explicit `-C`. Scratch
`/fast/scratch/hyaku/chousa-r65/Probe09/` (TMPDIR inside scratch), deleted after receipts
were copied here.

## Scope

One surface only: the `EXIT` header token of the frozen receipt format
("EXIT decimal 0..255"), centered on overflow (`>255`) and canonical-decimal boundary
forms. Reference tool: `corpus/evidence/round65/controls/ref-receipt-pin.py`. Production
target `tools/receipt-pin.py` does **not** exist at this freeze (before-state, consistent
with `controls/c1-before.txt` CASES=0/20 — verified by directory listing).

## Method

1. Built the canonical valid receipt with the same construction recipe as the frozen
   counter: `git -C <lane> cat-file blob f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd:SKILL.md`
   → sha256 = `4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a` →
   header block + blank separator + nonempty body.
2. Derived expected results **independently** from the frozen spec text in `claims.md`
   only: a canonical decimal for an integer in 0..255 has no sign and no leading zeros
   (except the numeral `0` itself); receipt-content violations are "invalid" → exit 1,
   while argv/environment problems are "usage/environment" → exit 2. No reference-tool
   logic reused in the expectation.
3. Ran the frozen reference with the canonical argv shape
   `python3 -B ref-receipt-pin.py --receipt <f> --root <lane> --revision <FREEZE>`
   (timeout 20s, `TMPDIR` in scratch), capturing exit/stdout/stderr verbatim.
4. Sanity control: the unmodified valid receipt exits 0 with exactly `RECEIPT_PIN=PASS`
   (guards against a harness that only ever fails).

## Variants (all on the EXIT-header surface; every other field left valid)

| case | EXIT token | independent expect | reference actual | agree |
|---|---|---|---|---|
| control-valid | `0` | 0 / PASS | 0 / `RECEIPT_PIN=PASS` | yes |
| nonzero-valid | `1` | 0 / PASS | 0 / `RECEIPT_PIN=PASS` | yes |
| max-exit | `255` | 0 / PASS (range boundary) | 0 / `RECEIPT_PIN=PASS` | yes |
| overflow-256 | `256` | 1 (minimal overflow; frozen counter case) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| overflow-999 | `999` | 1 (largest 3-digit) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| overflow-1000 | `1000` | 1 (range + width overflow) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| overflow-65535 | `65535` | 1 (width-5 overflow) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| leading-zero-0255 | `0255` | 1 (numerically in range, non-canonical) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| leading-zeros-000 | `000` | 1 (non-canonical zero) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| negative-exit | `-1` | 1 (signed) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| plus-exit | `+1` | 1 (explicit sign) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| empty-value | `` | 1 (bare `EXIT=`) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| hexish-exit | `0xff` | 1 (non-decimal alphabet) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| space-padded-exit | ` 255` | 1 (whitespace in value) | 1 / `RECEIPT_PIN=FAIL header/body` | yes |
| bad-revision-argv | (valid receipt) | 2 (usage/env partition probe) | 2 / empty stdout, argparse usage on stderr | yes |

Driver verdict: `ALL_AGREE=True`, driver exit 0. 15/15 probes match independent
expectations.

## Findings

1. **Overflow is rejected at the boundary with exit 1, not silently clamped and not
   exit 0**: `255` passes, `256` fails. The reference implements the frozen
   "EXIT decimal 0..255" rule as regex `EXIT=(?:0|[1-9][0-9]{0,2})` + `int(...)<=255`,
   emitting `RECEIPT_PIN=FAIL header/body` on stdout and exit 1.
2. **The failure class is "invalid" (1), never "usage/environment" (2)** for receipt
   content: the malformed-`--revision` argv probe exits 2 with argparse usage on stderr
   and empty stdout, cleanly partitioning the two nonzero classes on this surface.
3. **Canonical form matters, not just numeric value**: `0255` and `000` are numerically
   inside 0..255 yet fail, consistent with "decimal 0..255" read as canonical decimal
   numerals. Any future production `tools/receipt-pin.py` must reproduce this exact
   behavior to score the frozen counter's `overflow-exit`, `negative-exit`, `word-exit`,
   `max-exit`, and `nonzero-valid` cases.
4. **Frozen-counter compatibility check**: this surface covers 5 of the 20 frozen C1
   cases by name (nonzero-valid, max-exit, negative-exit, overflow-exit, and by family
   word-exit/empty variants). All observed tokens satisfy the counter's acceptance
   predicate (`RECEIPT_PIN=PASS` on rc 0; stdout startswith `RECEIPT_PIN=FAIL ` on rc 1).

## Evidence (this folder)

- `probe09-overflow-exit-driver.py` — the fixture driver (self-contained, deterministic).
- `probe09-overflow-exit-results.json` — full per-case record: expected/actual exit,
  verbatim stdout/stderr, agreement flags.
- `probe09-fixture-*.txt` — the 15 receipt fixtures (argv probe reuses the control-valid
  receipt bytes).

## Environment / installs

- python3 3.14.8 (system, preinstalled) — no installs or upgrades performed; nothing added
  to any PATH directory. No network use. No tools installed this seat.

## Risks / notes

- Single-process reference runs on one host; no concurrency or filesystem-race probes
  (out of scope for this surface).
- The `frozen_fail_token_shape` flag in the JSON is False only for the `bad-revision-argv`
  case by construction (usage class prints no FAIL token); agreement is carried by the
  `agree` field, 15/15 True.
