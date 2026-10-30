# Probe13 — round65 short-digest receipt fixture (scoped finding)

Seat: Probe13 (leaf). Lane chousa round65. Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd (verified `git rev-parse HEAD` on lane root).
Surface probed: **short SHA256 digest header** only. Reference `corpus/evidence/round65/controls/ref-receipt-pin.py` used read-only (production `tools/receipt-pin.py` absent, confirmed). No full battery run. No production writes, no network, no fleet/sibling writes.

## Method
- Scratch root `/fast/scratch/hyaku/chousa-r65/Probe13/` with explicit `TMPDIR` under it; one isolated git fixture repo (`fixture/repo`), toplevel asserted before mutation.
- Fixture commit `e7a640d0fb8e7f3f128dc125e6075dea685c8b40`, blob `a.txt` true SHA256 independently recomputed as `8a75e2b018e680a2fc622f79e4a1fdaada77cf80462d7e89ad2457cda5640f33` (sha256sum over `git cat-file blob REV:a.txt`), matches `facts.env`.
- Three receipts, identical except the SHA256 header field: `short32` (32 hex), `short63` (63 hex, off-by-one boundary), `control-full` (64 hex correct). All otherwise byte-exact per frozen format (REVISION/EXIT/SHA256+relpath/blank/nonempty body); receipt bytes dumped with `od -c` to confirm.
- argv preserved: `--receipt --root --revision` against the reference.

## Results
| case | digest len | exit | stdout | stderr |
|---|---|---|---|---|
| short32.rcpt | 32 | 1 | `RECEIPT_PIN=FAIL digest header` | empty |
| short63.rcpt | 63 | 1 | `RECEIPT_PIN=FAIL digest header` | empty |
| control-full.rcpt | 64 | 0 | `RECEIPT_PIN=PASS` | empty |

## Independent derivation vs observed (frozen format, claims.md only)
- Format clause "SHA256 full lowercase 64 hex plus canonical relative POSIX path" → 32- and 63-char digests are malformed headers.
- Exit legend "0 consistent,1 invalid,2 usage/environment" → malformed receipt content is class **1**; argv/env were valid so class 2 does not apply.
- Derived expectation: exit 1 with FAIL token. Observed matches for both short cases; control exits 0, attributing failure solely to the short digest.

## Notes for L1
1. Behavior is consistent with the frozen format across the 32-hex truncation and the 63-hex off-by-one boundary — no length-graded leniency in the reference.
2. **Token-portability risk**: the frozen format pins exit codes and the `RECEIPT_PIN=PASS` / `RECEIPT_PIN=FAIL ` prefix, but the exact reason string (`digest header`) for malformed-header failures is implementation wording. C1's predicate scores "exact exit and token" on 20 frozen cases; any production reimplementation of `tools/receipt-pin.py` that rewords failure reasons will fail exact-token matching even when behaviorally correct. Recommend L1 pin reason-string wording (or confirm frozen cases avoid reason-string-sensitive tokens) when acquiring the tool.
3. Reference performs no working-tree hashing; digest bound to `git cat-file blob REV:path` — consistent with "digest binds the Git blob at the declared revision".

## Evidence (this folder)
- `short32.rcpt`, `short32.rcpt.out`, `short63.rcpt`, `short63.rcpt.out`, `control-full.rcpt`, `control-full.rcpt.out`, `facts.env` (REV, FULL, SHORT32, SHORT63)
- `probe13-fixture-driver.sh` — reproducible driver

## Environment / installs
- No tools installed or updated this seat. python3 (system), git (system), sha256sum only.
- Pacman untouched; no service restarts; no network fetches.
- Scratch deleted before yield (asserted at end of run).
