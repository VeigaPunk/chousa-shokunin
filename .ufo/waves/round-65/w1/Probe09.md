# Probe09 — R65-C1 overflow-exit fixture findings (round65)

Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`. Claim: **C1** (operability; historical
3/10, numeric score unchanged). Seat: Probe09 (leaf). Scoped surface: `EXIT` header
overflow/canonical-decimal only — no full battery run.

## Verdict

Reference `corpus/evidence/round65/controls/ref-receipt-pin.py` matches independent
expectations on **15/15 probes** (`ALL_AGREE=True`, driver exit 0). Production target
`tools/receipt-pin.py` absent at freeze (before-state, consistent with
`controls/c1-before.txt` CASES=0/20).

## Independently derived rule (from frozen claims.md text only)

"EXIT decimal 0..255": canonical decimal numeral, no sign, no leading zeros (except `0`);
receipt-content violation → exit 1 ("invalid"); argv/environment → exit 2
("usage/environment"). `0 consistent,1 invalid,2 usage/environment`.

## Result matrix (EXIT token varied; all other receipt fields valid)

| case | EXIT | expect | actual | token |
|---|---|---|---|---|
| control-valid | `0` | 0 | 0 | `RECEIPT_PIN=PASS` |
| nonzero-valid | `1` | 0 | 0 | `RECEIPT_PIN=PASS` |
| max-exit | `255` | 0 | 0 | `RECEIPT_PIN=PASS` |
| overflow-256 | `256` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| overflow-999 | `999` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| overflow-1000 | `1000` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| overflow-65535 | `65535` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| leading-zero-0255 | `0255` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| leading-zeros-000 | `000` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| negative-exit | `-1` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| plus-exit | `+1` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| empty-value | `` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| hexish-exit | `0xff` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| space-padded-exit | ` 255` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| bad-revision-argv | valid receipt | 2 | 2 | empty stdout; argparse usage on stderr |

## Key findings

1. Overflow rejected exactly at the boundary: `255` consistent, `256` invalid — no
   clamping, no false PASS. Exit class is 1 (invalid), never 2, for receipt content;
   the argv probe confirms the 1-vs-2 partition (usage → 2, empty stdout).
2. Canonical form is enforced, not numeric value: `0255`/`000` fail though in range —
   any production target must reproduce this to score the frozen counter's
   `overflow-exit`, `negative-exit`, `word-exit`, `max-exit`, `nonzero-valid` cases.
3. Observed tokens satisfy the frozen counter's acceptance predicate
   (PASS on rc 0; `RECEIPT_PIN=FAIL ` prefix on rc 1).

## Evidence

Driver, verbatim results JSON, and 15 receipt fixtures under
`.ufo/waves/round-65/w1/Probe09/` (`probe09-overflow-exit-driver.py`,
`probe09-overflow-exit-results.json`, `probe09-fixture-*.txt`); full narrative in that
folder's `report.md`.

## Bounds

Scratch `/fast/scratch/hyaku/chousa-r65/Probe09/` deleted after receipt copy (no /tmp
evidence). Read-only git via explicit `-C`; no production/fleet/sibling writes; no
network; no installs (python3 3.14.8 preinstalled). No battery run — single assigned
surface only.
