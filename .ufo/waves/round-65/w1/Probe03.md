# Probe03 — round65 seat result (max-exit boundary probe)

**Verdict: 7/7 boundary cases match independently derived expectations. Max-exit boundary confirmed at EXIT=255 inclusive.**

Fixture: isolated scratch git repo (blob-bound receipt, `REV=2ad4192b…`, digest `8a75e2b0…` over `note.txt`), validator = pre-freeze `corpus/evidence/round65/controls/ref-receipt-pin.py`, argv/stdout preserved. One surface only (EXIT header); no battery run.

| EXIT header | expected | observed (rc / token) | match |
|---|---|---|---|
| 0 | PASS/0 | 0 / RECEIPT_PIN=PASS | yes |
| 1 | PASS/0 | 0 / RECEIPT_PIN=PASS | yes |
| 254 | PASS/0 | 0 / RECEIPT_PIN=PASS | yes |
| 255 | PASS/0 | 0 / RECEIPT_PIN=PASS | yes |
| 256 | FAIL/1 | 1 / RECEIPT_PIN=FAIL header/body | yes |
| 0255 | FAIL/1 (impl-derived) | 1 / RECEIPT_PIN=FAIL header/body | yes |
| 255 rerun | PASS/0 | 0 / RECEIPT_PIN=PASS | yes (deterministic) |

Key findings:
- **255 is the maximum admitted EXIT**; 256 → exit 1. Leading-zero `0255` → exit 1 (consistent with reference grammar `EXIT=(?:0|[1-9][0-9]{0,2})`; frozen format text alone is ambiguous on leading zeros — flagged).
- Token granularity caveat: all header-family rejections share the single token `header/body`; boundary discrimination lives entirely in exit code. Relevant to C1's "exact exit and token" matching if any frozen case probes the boundary.

Evidence: `.ufo/waves/round-65/w1/Probe03/evidence/max-exit-transcript.txt` + three boundary receipts. Full method/notes: `.ufo/waves/round-65/w1/Probe03/report.md`.

Hygiene: no production writes, no git/jj mutations outside scratch, no installs, scratch `/fast/scratch/hyaku/chousa-r65/Probe03/` deleted. Seats return notes only — L1 owns integration.
