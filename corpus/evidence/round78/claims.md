# Round 78 frozen claims — the outer battery's answer key, subject identity and verdict receipt; the lane's self-assessment resolving

Frozen 2026-11-04, before any seat scored anything. Base revision
`53dbd512d0ab70055338cb44898a6db70049537f` (round-77 tip). Pre-freeze instruments and
controls commit `93e0432eb5bb9c4492d540bc6a6358ed3f8d4392`. Two claims, distinct axes, each
causally separable: C1 changes the outer battery's bytes and needs only those bytes; C2
changes three self-assessment surfaces and needs only those edits.

Instrument digests at the controls commit (`sha256sum`, full):

| instrument | sha256 |
|---|---|
| `corpus/evidence/round78/matrix-battery-v5.py` | `5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0` |
| `corpus/evidence/round78/forge-battery.py` | `ba98db41e0c82ba0ff3b7cb4259764fcfb85c54b17137da02655ee751f1c5143` |
| `corpus/evidence/round78/work-contract.py` | `e51d8917afd1c202f35e8395360ef8bba3f11de544c1614ade748c3d87ffa8a0` |
| `corpus/evidence/round78/selfcheck.py` | `f5acdd825ab7dcafa1385ad2b9a6c22df848c4e856947746cd006c22837bf9af` |
| `corpus/evidence/round77/matrix-battery-v4.py` (the subject C1 supersedes) | `155fafb16b6931449abefb60575029f273959ba4e94a4db48ac22e525f106a3d` |

## C1 — operability (lowest scored non-retired axis; the historical numeric 3/10 is held)

**Target axis:** operability — a runnable artifact whose stated outcome a reader can
re-derive. The round changes the *outer battery* surface, not the number the lane reports.

**Predicate (frozen sentence, identical to the instrument's docstring and the receipt label):**

> `python3 -B corpus/evidence/round78/forge-battery.py --battery corpus/evidence/round78/matrix-battery-v5.py --work DIR`
> exits 0 and prints exactly `FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1`.

`handled` counts the four round-77 falsification forgeries that are REFUSED (battery exits
non-zero, receipt intact, last `BATTERY=` line FAIL) or DETECTED (the battery's own
`RECEIPT_LINES` trailer does not match the receipt). The positive control is the lane's
legitimate matrix `corpus/evidence/round76/loader-matrix-v3.py`, which must still be ACCEPTED.

**Before (measured at base `53dbd512`, receipts committed with the controls):**
`controls/forge-battery-before-v4.txt` — `FORGE_BATTERY=FAIL forgers_handled=0/4 positive=1/1`,
`# exit: 1`. The three identity forgeries reach the exact predicate line at exit 0 and the
detached append is believed; that is round 77's own `R77CriticA/rcpt-a1.txt`, `rcpt-a2.txt`,
`rcpt-a7.txt`, `rcpt-a5d.txt`, re-measured here on this host.

**After (measured at controls `93e0432e`):** `controls/forge-battery-after-v5.txt` —
`FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1`, `# exit: 0`.

**Kill rule:** C1 fails if the after receipt's predicate line differs, if the positive control
is MISS, or if any forger is FORGED. A seat that finds a forger reaching `BATTERY=PASS` on v5
without scoring a subject falsifies the *claim*, not the counter, and it is reported.

**Do-nothing control:** with no round-78 work the only battery on disk is
`corpus/evidence/round77/matrix-battery-v4.py`, whose receipt is `handled=0/4` at exit 1 — a
do-nothing round cannot reach the target. The `--print-order` twin (M1) restores the round-77
ORDER digest, so the target is reachable only with the order line absent.

**Supporting evidence, not the predicate:** `controls/work-contract-before-v4.txt`
(`WORK_CONTRACT=FAIL survived=no unwritable_exit=1 file_exit=1`, exit 1) →
`controls/work-contract-after-v5.txt` (`WORK_CONTRACT=PASS survived=yes unwritable_exit=2
file_exit=2`, exit 0), QUALITY 142 → 144.

**Recorded limits (not the predicate, stated rather than hidden):** the content leg remains a
shape requirement; the salt closes the trailing-strip class and not a normalizer that deletes
every unrecognised inert statement; `RECEIPT_LINES` exposes an append instead of preventing it;
a truncated receipt is not detected by the trailer (the exit code stays authoritative).

## C2 — calibration (sourced on S193/S194, opened this round)

**Target axis:** calibration — the lane's self-assessment read against observed repo state. The
predicate counts mismatches; it is not an assertion.

**Predicate (frozen sentence, identical to the instrument's docstring and the receipt label):**

> `python3 -B corpus/evidence/round78/selfcheck.py --lane .` exits 0 and prints exactly
> `SELFCHECK=PASS unresolved=0/3`.

The three classes are the round-77 non-author spot-check's routed defects 1, 3 and 4: the
`SKILL.md` gate-registry row whose cell count does not match its header (row 168, 7 cells
against 8, no owner cell); the `QUALITY.md` criterion whose backticked pointer resolves to no
committed path (142, `receipts/02c-work-unwritable.*`); and the `## Mistakes` row of
`corpus/lessons/round-77.md` stranded below `## Boundaries` (line 73).

**Before (measured at base `53dbd512`):** `controls/selfcheck-before.txt` —
`SELFCHECK=FAIL unresolved=3/3`, `# exit: 1`, one unresolved finding per class.

**After (measured at controls `93e0432e`):** `controls/selfcheck-after.txt` —
`SELFCHECK=PASS unresolved=0/3`, `# exit: 0`.

**Kill rule:** C2 fails if the after receipt's predicate line differs, or if a seat shows the
counter reaching `PASS` on a tree where one of the three defects is still present (the
supersession/correction/erratum escape hatch is lexical and that is its exposure).

**Do-nothing control:** without the three repairs the counter prints `unresolved=3/3` at exit 1
on the same bytes; the escape hatches it accepts (`correction:`, `supersedes:`, `erratum:`
lines) exist only in the round-78 edits, so a do-nothing round cannot reach the target.

## Shared boundaries

No network, no package adoption, no sibling-lane or fleet-repo write other than the round
report and L0 appends, no host question presumed answered. Frozen instruments and receipts are
never amended after a seat scores them; a post-freeze finding is reported as a limit, never as
a repaired predicate. Seats are author-lane evidence: the non-author closure still rules.
