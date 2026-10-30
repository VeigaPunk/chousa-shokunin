# SourceBefore — round64 `controls/c1v3-before-full.txt` header audit (round65 w1)

Seat: SourceBefore (scout, leaf — no subagent dispatch). Read-only; no production writes; read-only git only with explicit `-C`. Lane HEAD verified `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` == freeze; `git status --porcelain` on the receipt clean. Tools installed: none. Scratch `/fast/scratch/hyaku/chousa-r65/SourceBefore/` never created (all work was direct reads + short git reads); cleanup verified no-op.

## 1. The receipt as stored (observed)

- Two copies, byte-identical: `sha256sum` = `ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b`, 44 lines each, `diff -q` clean:
  - `corpus/evidence/round64/controls/c1v3-before-full.txt`
  - `.ufo/waves/round-64/c1v3-before-full.txt`
- Content: line 1 `LEG CLEAN clean ok ok` (the S156 quote), then 42 more `LEG …` lines, ending line 44 `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`. It is a bare captured battery output: no header block, no channel markers, no trailing sections.
- Blob identity (read-only git, explicit `-C`): blob `236ff2a0382b637eafd857a5f326bdf53a090182` at base `d6ed8155…` == blob at freeze `f99de3bd…` == HEAD; SHA-256 of the blob bytes = `ca05f579…` (matches both copies and registry S156). Object name (SHA-1) ≠ content digest (SHA-256) — exactly the identity/digest distinction claim C2's entry must draw, with concrete values.

## 2. Missing headers, enumerated (observed)

Canonical self-contained receipt format (round65 claims C1; `corpus/evidence/round65/controls/ref-receipt-pin.py`; `c1-count.py`): line 0 `REVISION=<40 lowercase hex>`; line 1 `EXIT=<0..255 decimal>`; line 2 `SHA256=<64 lowercase hex> <canonical repo-relative POSIX path>`; line 3 empty separator; then nonempty body. Exactly one of each header, in that order. Digest binds the Git blob at the declared revision (via `git cat-file blob REV:path`), never working-tree bytes. Validator exits 0 consistent / 1 invalid / 2 usage.

In `c1v3-before-full.txt` all of it is absent:

1. **REVISION header** — absent. Line 1 is `LEG CLEAN clean ok ok`; no revision is declared anywhere in the file.
2. **EXIT header** — absent. The process exit is not encoded in the file at all; it is only inferable from the body aggregate `BATTERY=FAIL` under the battery's FAIL→nonzero contract.
3. **SHA256 + path digest header** — absent. No content digest, no canonical path declaration, no blob binding.
4. **Empty separator** — absent (nothing to separate; body starts at line 1).
5. Auxiliary provenance its own round64 siblings carry is also absent: `COMMAND=[…]`, `SEED=…`, and `STDOUT`/`STDERR` channel markers (compare `c1-frozen-after-0.txt`, `c1-v2-cross-0.txt`). Consequence: the file does not even declare which channel its 44 lines came from — the same channel-provenance ambiguity round64's erratum item 6 already recorded for `audit-v2-fault.txt`.

Structural consequence under the reference validator: `ref-receipt-pin.py` requires ≥5 lines and `lines[0] == 'REVISION=' + revision`; this file fails at line 0 → `RECEIPT_PIN=FAIL header/body`, exit 1. It instantiates the counter's `no-revision`, `no-exit`, `no-digest` negative classes simultaneously (`c1-count.py` cases 4–13 of the 17 negatives; the frozen case list: no-revision, wrong-revision, short-revision, no-exit, negative-exit, overflow-exit, word-exit, no-digest, wrong-digest, short-digest, missing-blob, traversal, absolute, duplicate, no-separator, no-body, upper-digest).

## 3. Provenance elsewhere — where each missing fact actually lives (observed)

| Missing from receipt | Recorded where |
|---|---|
| Exit = 1 | round64 `claims.md` lines 66–67: "**Before** (receipt `.ufo/waves/round-64/c1v3-before-full.txt`, exit 1, committed at or before the freeze)"; repeated with tallies in fleet `SCORECARD.md:3060` and `.ufo/reports/round-64/chousa.md:31`. **Not** in round64 `controls/measurement-summary.json` — its 14-entry `runs[]` array omits `c1v3-before-full` entirely (fleet-wide grep confirms: only MANIFEST, round reports, SCORECARD and seat notes reference this receipt). |
| Execution revision | Recorded nowhere for this run. `claims.md` says only "committed at or before the freeze". The round64 after/cross receipts pin `REVISION=944955cc…`; the before receipt pins nothing. |
| Content digest | Not in the receipt. Supplied externally by round65 `corpus/evidence/round65/source-openings.json` S156 (`sha256 ca05f579…`, quote at `line1`) and `corpus/SOURCES.md` row S156 (scope B, "lines1–44 at base d6ed8155…"). |
| Registry acknowledgment of the gap | Fleet `MANIFEST.json:32751` (QUALITY item): "(3) c1v3-before-full.txt lacks a self-contained REVISION/EXIT header (provenance rides frozen claims.md)". `corpus/lessons/round-65.md` Mistakes row 1: "Before receipt relies on surrounding provenance instead of self-contained headers"; routed item 3: "New validator and revision/exit-bearing prefreeze controls; final receipts also carry blob digest. The old before receipt remains unmodified." |

## 4. Elsewhere vs self-contained — why the distinction matters (analysis)

- A bare capture is a verdict log, not a verifiable measurement record. Its consistency cannot be checked without trusting adjacent prose (claims), a registry row (S156), or run-time memory. Each external stand-in is itself only as trustworthy as its own provenance chain — that is the gap the R65 canonical header format closes.
- Exit is a process property; the body aggregate `BATTERY=FAIL` correlates with exit only via the battery's contract. round64 Draft06 already flagged it: "Claims lines 67–68 attribute exit 1 to it; the plain receipt itself does not independently encode the process exit." The attribution is [INFERENCE] consistent (FAIL→1) but external.
- The receipt cannot be retro-validated into the new format: the format's REVISION must equal a caller-supplied revision and the digest must bind that blob — there is no recorded execution revision to supply, and no in-file digest to compare against blob `236ff2a0…`/`ca05f579…`. Per the lesson's routed item 3 it stays admitted as inherited before-evidence, unmodified; claims C1's red-before is the absent-target control, not this file.
- Scope guard (S157, lesson title "receipt consistency is not execution proof"): even a fully headered, blob-bound receipt proves header/body consistency, not that the recorded output was really produced by that execution. The old receipt is weaker still: not even consistency-checkable.
- The lane's own new artifacts only partially reach the canonical shape today: round65 prefreeze control `corpus/evidence/round65/controls/c1-before.txt` carries `REVISION=d6ed8155…`, `EXIT=1`, `ARGV=[…]` but no SHA256 header — conforming to "revision/exit-bearing prefreeze controls", with digest headers promised for final receipts (routed item 3).

## 5. Facts / inference / unknowns

- Observed: every path+line citation in §1–§3; hashes via `sha256sum`; blob ids via read-only `git cat-file`/`rev-parse` with explicit `-C`.
- [INFERENCE]: exit-1/FAIL-contract consistency; unknowability of the historical execution revision from stored evidence.
- Remaining unknowns: the actual exit and subject/instrument revisions of the original before run (unrecorded in any artifact found); whether the original capture dropped stderr content (channel undeclared; E11's embedded `UnicodeDecodeError` line shows error text lived in the body).

## Claim mapping

- **C1**: this receipt exercises exactly the negative-case classes the frozen 20-case counter covers (no-revision / no-exit / no-digest); it is a source example of the format gap, not one of the 20 cases and not the C1 before control.
- **C2**: S156 verified this round — quote `LEG CLEAN clean ok ok` located at line 1; digest `ca05f579…` recomputed and matches; the object-identity (`236ff2a0…`, SHA-1 blob) vs content-digest (`ca05f579…`, SHA-256) distinction documented with concrete pinned values.

Source: receipt (both copies, full); round64 `claims.md:59-75`, `claims-erratum.md`; `controls/measurement-summary.json`, `c1-frozen-after-0.txt`, `c1-v2-cross-0.txt`; round65 `claims.md`, `c1-count.py`, `controls/ref-receipt-pin.py`, `controls/c1-before.txt`, `source-openings.json:15-33`; `corpus/SOURCES.md:165-167`; `corpus/lessons/round-65.md`; fleet `MANIFEST.json:32751`, `SCORECARD.md:3060`, `.ufo/reports/round-64/chousa.md:31`; round64 w1 seat notes (Draft06, Attack20) for prior independent flags.
