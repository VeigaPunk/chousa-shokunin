# Probe03 — receipt-pin max-exit boundary probe (round65)

Seat: Probe03 (leaf). Lane: chousa round65, freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Surface: **EXIT header boundary only** (one surface, isolated probe — no battery).
Validator exercised: `corpus/evidence/round65/controls/ref-receipt-pin.py` (pre-freeze reference; production `tools/receipt-pin.py` absent at probe time).

## Method

1. Fixture repo built in scratch (`/fast/scratch/hyaku/chousa-r65/Probe03/work/fixture`, `git init -b main`, single blob `note.txt`), so the digest genuinely binds a git blob at a declared revision — no working-tree hashing involved.
2. `REVISION=2ad4192b31c88cc68a2505e095ce4b13ad3be2af`, `SHA256=8a75e2b018e680a2fc622f79e4a1fdaada77cf80462d7e89ad2457cda5640f33` (= `sha256` of `git cat-file blob REV:note.txt`), separator blank line, nonempty body. Only the EXIT line varies.
3. Each receipt run as: `python3 ref-receipt-pin.py --receipt <r> --root fixture --revision 2ad4192b…` — argv and stdout preserved verbatim in transcript.

## Independent expectation (derived from frozen format text only)

Frozen C1 format: `EXIT decimal 0..255`. Therefore:
- EXIT ∈ {0, 1, 254, 255} → header valid → **PASS, exit 0**.
- EXIT=256 → outside `0..255` → **FAIL, exit 1**.
- EXIT=0255 → the frozen text "decimal 0..255" is ambiguous on leading zeros; expected **FAIL, exit 1** under the reference grammar (`EXIT=(?:0|[1-9][0-9]{0,2})`), recorded as implementation-derived, not text-entailed.

## Observed (evidence: `evidence/max-exit-transcript.txt`)

| EXIT header | rc  | stdout              | expected | verdict |
|-------------|-----|---------------------|----------|---------|
| 0           | 0   | RECEIPT_PIN=PASS    | PASS/0   | MATCH   |
| 1           | 0   | RECEIPT_PIN=PASS    | PASS/0   | MATCH   |
| 254         | 0   | RECEIPT_PIN=PASS    | PASS/0   | MATCH   |
| 255         | 0   | RECEIPT_PIN=PASS    | PASS/0   | MATCH   |
| 256         | 1   | RECEIPT_PIN=FAIL header/body | FAIL/1 | MATCH |
| 0255        | 1   | RECEIPT_PIN=FAIL header/body | FAIL/1 (impl-derived) | MATCH |
| 255 (rerun) | 0   | RECEIPT_PIN=PASS    | PASS/0   | MATCH (deterministic) |

7/7 observed results match independent expectations. **Max-exit = 255 inclusive**; 256 and leading-zero forms are rejected with exit 1 and the exact token `RECEIPT_PIN=FAIL header/body`. Deterministic across reruns.

## Notes / caveats

- Token granularity: the reference emits only `header/body` for all header-family rejections; the boundary signal lives in rc (0 vs 1), not the token. C1's counter uses "exact exit and token" — for an always-fail/each-case-must-match counter, boundary cases at 256/0255 all share token `header/body`, so token alone cannot distinguish them (acceptable for C1's 20 frozen cases if none probe 256; flagged for L1).
- Not probed (out of surface): exit=2 usage/environment paths, revision mismatch, digest mismatch, path canonicalization, multi-line/output edge cases.
- No production writes; no git/jj mutations outside scratch fixture; scratch deleted after evidence copy.
- Tool installs: none (python3 + git already present; no installs required this seat).

## Files

- `report.md` — this report.
- `evidence/max-exit-transcript.txt` — verbatim run transcript (argv pattern + stdout + rc per case).
- `evidence/receipt-EXIT-255.txt`, `receipt-EXIT-256.txt`, `receipt-EXIT-0255.txt` — the three boundary receipts.
