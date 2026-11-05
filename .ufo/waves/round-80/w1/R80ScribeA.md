# R80ScribeA — round 80 w1, scribe draft for C2 (calibration)

Leaf seat. Draft only: `corpus/SOURCES.md`, `corpus/lessons/round-80.md`, `corpus/QUALITY.md` and every frozen artifact are untouched. Pinned base `b7803829922770b890e9f4efdd30d12c3695439a`; everything read with `git show <rev>:<path>` or `git cat-file` (no URL, no network, no clone, no git mutation). Access date used: 2026-11-04. Tools installed or upgraded: none. Scratch `/fast/scratch/hyaku/chousa-r80/R80ScribeA/` removed before yield; every cited receipt is in `.ufo/waves/round-80/w1/R80ScribeA/receipts/`.

Deliverable: `.ufo/waves/round-80/w1/R80ScribeA/draft-sources-rows.md` (four registry rows, four `GATE-RECORD` lines with per-line verification, the `## Gate` block, flags for the L1).

## Work performed

1. Read the frozen `corpus/evidence/round80/claims.md` (C1 and C2 predicates, kill rules, sourced claims) and `corpus/lessons/round-79-verifier-spotcheck.md` (non-author closure).
2. Measured the pinned bytes:
   - `git cat-file -t b7803829…` → commit; `corpus/QUALITY.md`, `corpus/lessons/round-79-verifier-spotcheck.md`, `corpus/lessons/round-79.md`, `corpus/SOURCES.md` all exist at `b7803829`.
   - `git show b7803829:corpus/QUALITY.md | sed -n '1054p;1056p'` → line 1054 = criterion 146, line 1056 = criterion 147 (matches the brief).
   - `git show b7803829:corpus/lessons/round-79-verifier-spotcheck.md | sed -n '222p'` → the operability (C1) row of §4.
   - `git show 3eb4a3ca:.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt | wc -l` → 11 (`receipts/S198-receipt-3eb4a3ca.txt`).
3. Wrote the four GATE-RECORD lines to scratch and ran this seat's own four-test counter (`receipts/check_gate.py`, R1 revision resolves, R2 path present, R3 quote is a substring of the line, R4 `wc -w` equals `words=` and ≤25).
4. Ran per-line shell verification (`receipts/row-verify.sh` → `receipts/row-verify.txt`) and the old-record measurements (`receipts/old-record.txt`).
5. Checked row shape: 12 pipes per row (11 cells), no cell contains `|`, statuses and tiers within the existing vocabulary (`mined` 158, `queued` 19, `rejected` 21 at the base).

## Findings

Each finding names the command, the receipt and the observed line with its exit code.

**F1 — The four new rows resolve on the committed bytes.** Command: `python3 -B check_gate.py gate-records.txt`. Receipt: `receipts/gate-check.txt`. Observed: `S199 … line_n=222 … PASS`, `S200 … line_n=1056 … PASS`, `S201 … line_n=1054 … PASS`, `S202 … line_n=2 … PASS`, `GATE_RECORDS_CHECK=PASS failures=0`, `exit=0`. Limit: this is this seat's counter, not the frozen `gate-grounding-check.py`, which was not run.

**F2 — Per-line verification, all four.** Receipt: `receipts/row-verify.txt`. Each `grep -c -F` prints `1` with `# exit: 0`; each `wc -w` prints S199 `16`, S200 `15`, S201 `25`, S202 `9`, all equal to the recorded `words=`.

**F3 — The round-79 Gate record is wrong in three places, measured.** Receipt: `receipts/old-record.txt`.
- S196 (lesson says 25 words): the quote is verbatim on line 1056 (`grep -c -F` → `1`) and is **27** words (`wc -w` → `27`).
- S197 (lesson says 24 words): verbatim on line 1054 (`grep -c -F` → `1`) and is **25** words (`wc -w` → `25`).
- S198 (lesson's located quote `the audit window is the last … block`, 10 words): `grep -c -F -- 'the audit window is the last' receipt.txt` → `0`, `# exit: 1`. The receipt is 11 lines (`receipts/S198-receipt-3eb4a3ca.txt`, `wc -l` → 11), so the row's "lines 1-20" overstates it.

**F4 — Insertion point for the rows.** At `b7803829`, `grep -n '^| S198 \|^## '` on `corpus/SOURCES.md` → `210:| S198 …`, `212:## Paths`. The four rows go between line 210 and the `## Paths` heading, inside the `## Registry` table (round 79 lost three rows appended at end of file; `E12`).

**F5 — Frozen claims.md and the dispatch disagree on S199's kind.** `corpus/evidence/round80/claims.md` (C1 "Sourced claims") says `S199` is "own-work A: the round-79 structure-identity receipts, opened this round". The dispatch says `own-work B`, the round-79 spot-check's payload finding, anchor line 222. The draft follows the dispatch and flags the conflict. Note: line 222 cites only the payload channel; the structure-identity finding is at `corpus/lessons/round-79-verifier-spotcheck.md` lines 129–131 and is not what the row's quote grounds. The L1 must choose; the frozen file is not amended.

**F6 — Lineage of the base.** `git log --oneline acca2449..b7803829` → one commit, `b7803829 round-79 verifier spot-check (integrator, hyaku): non-author admit/reject`; `git show --stat` → 1 file, 286 insertions (`corpus/lessons/round-79-verifier-spotcheck.md`). `git cat-file -e acca2449:corpus/lessons/round-79-verifier-spotcheck.md` → rc 128. So the spot-check file exists only at the base revision used by the rows, not at `acca2449`, which is the revision the spot-check's own header names as lane tip. Claims.md calls `b7803829` the "round-79 lane tip"; the lineage shows it is `acca2449` plus the spot-check commit.

**F7 — S200's 15-word quote is measured, not copied.** `claims.md` names a "15-word located quote" for S200 without printing it. The draft uses `by any normalizer that knows its marker family, so the closure is a per-channel measurement` (`wc -w` → 15; `grep -c -F` on line 1056 → 1). I did not search criterion 147 exhaustively for other 15-word runs; a different substring must be re-measured with the same checks.

**F8 — Quote bounds.** Every quote is ≤25 words (16, 15, 25, 9). S201's quote is exactly 25, the bound's maximum; the lesson-stated count (24) was off by one.

**F9 — Not run.** `scripts/sources-census.sh validate` was not run against the drafted table (it needs the rows landed; the L1 runs it after landing). The frozen `gate-grounding-check.py` was not run (frozen; the L1's landed copy counts). No check was run on any file other than the pinned revisions and this seat's draft.

## Pinned-byte sha256 (measured with `git show <rev>:<path> | sha256sum`)

| path | rev | sha256 |
|---|---|---|
| `corpus/QUALITY.md` | `b7803829` | `8521a4356df054d93c4365df5efc8e362c753da68515752f7ccbc8a7fda51c81` |
| `corpus/lessons/round-79-verifier-spotcheck.md` | `b7803829` | `13f9558f565b696ba1138c6e883640144b62712337196c60173b8406fd966b7c` |
| `corpus/lessons/round-79.md` | `b7803829` | `13283695588ba7a16e4ce4f92b192bd64c5179b254e8c47934c29b32b8e2ada3` |
| `corpus/SOURCES.md` | `b7803829` | `c3e81be238f4b98e9410adee63cb09876ac47ff2ec127418f804fcdc5f349674` |
| `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` | `3eb4a3ca` | `db3a8068e3eee34c51d0f8b567db3bc38fa61b8a4ed35040d9af518bfccad597` |

## Out of scope / not touched

No edit to `corpus/SOURCES.md`, any lesson, `corpus/QUALITY.md`, `corpus/evidence/round79/`, `corpus/evidence/round80/`, `scripts/`, `.ufo/state`, `MANIFEST.json`, any sibling repo, or `~/.local/bin`. No commit, push, subagent or network call.
