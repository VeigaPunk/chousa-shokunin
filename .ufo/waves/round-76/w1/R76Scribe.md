# R76Scribe — round 76 seat report (chousa lane)

Seat: **R76Scribe** (scribe, wave r76 w1). Scope: draft three `corpus/SOURCES.md` registry
rows and three lesson `## Mistakes` rows for round 76; review the L1's in-worktree drafts
rather than appending duplicates. Draft only — nothing committed.

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
Frozen predicate set: `corpus/evidence/round76/claims.md` (read first).
Controls commit (instruments + receipts): `da9ac7ec684fe9fe9ad5554cab6180057255b76b`.
Claims freeze: `5daa3628389c164f6ee34027be77d26b175c0de7`. Base: `1af39fed6058ad46fc075b72fddaae838f43273e`.

---

## 1. What this seat produced

Two draft artifacts, both under this seat's own wave folder, plus this report:

- `.ufo/waves/round-76/w1/R76Scribe/draft-SOURCES-rows.md` — the three drafted registry rows
  (S187 admit, S188 admit, S189 reject), normalised to the censused 11-column schema.
- `.ufo/waves/round-76/w1/R76Scribe/draft-Mistakes-rows.md` — three drafted lesson
  `## Mistakes` rows in the `class | evidence | captured-by | fix` shape.

Verification receipts (same folder): `census-receipts.txt`, `probe-as-drafted.txt`,
`probe-corrected.txt`, `probe-c2-timeout.txt`, `probe-c2-exit2.txt`.

## 2. The three registry rows (drafted)

**S187 — ADMIT, own-work B, mined.** Source `corpus/lessons/round-75-verifier-spotcheck.md`
routed defect 1 (C1 rationale and battery coverage). Quotes re-opened at the anchor
revision: line 125, 14 words, "commit subject, tree ids and byte sizes are stable metadata
channels, and four content-blind"; line 127, 9 words, "the twelve-entry declared-order
oracle to the battery's subject set". Anchor `1af39fed6058ad46fc075b72fddaae838f43273e`,
lines 124–128. Both spans are contiguous on their named lines; both are ≤25 words.

**S188 — ADMIT, own-work B, mined.** Same file, routed defect 2 (the C2 counter is a
presence test). Quote: line 130, 16 words, "polarity and magnitude rather than substring
presence, require the correction block to be the final section". Anchor
`1af39fed6058ad46fc075b72fddaae838f43273e`, lines 129–131.

**S189 — REJECT, own-work C, rejected, used-by `—`.** Source
`corpus/evidence/round76/claims.md` at `5daa3628389c164f6ee34027be77d26b175c0de7`, line 27,
quote "`BATTERY=PASS forgers_rejected=11/11 positive=2/2`". Reject reason and the concrete
flip: the claims file is the lane's own declaration of its own predicate, so it is not
evidence that the predicate holds — the committed receipts are; flip: admit scoped to the
claim text if an admitted entry ever rests on a declaration as the only record of a
prediction. The flip matches the shape of the lane's earlier own-narrative rejections
(S185 "the bar content is measured against, not a source"; S183 "synthetic check fixtures
bypass the defective loader").

## 3. Findings against the L1's in-worktree drafts

Two defects, both in the *anchoring/quoting* of the drafts, both confirmed by a fail-closed
probe rather than by reading alone.

**F1 — the S187/S188 anchor revision does not contain the file the rows cite.** The L1's
in-worktree `corpus/SOURCES.md` rows and the in-worktree lesson Gate both anchor
`corpus/lessons/round-75-verifier-spotcheck.md` at `e515c9624278cef906671d76188cb44e2a3445fe`.
That revision is the r75 landing tip; the spot-check file was added after it.

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show e515c962:corpus/lessons/round-75-verifier-spotcheck.md`
  → exit 128, `fatal: path 'corpus/lessons/round-75-verifier-spotcheck.md' exists on disk, but not in 'e515c962'`.
- The file's blob `c53d32c944460213812368d92b8f21527c0b464e` exists at `1af39fed…`, `da9ac7ec…`
  and `5daa3628…` only. S187/S188 therefore anchor at `1af39fed6058ad46fc075b72fddaae838f43273e`
  with the blob named (identical at `da9ac7ec…`), and the SOURCES row carries the blob so a
  later reader can tell the three are the same bytes.
- The S189 anchor is already correct: `claims.md` exists at `5daa3628…` (it does not exist
  at `da9ac7ec…` — the claims file lands one commit after the controls).
- Evidence: `.ufo/waves/round-76/w1/R76Scribe/probe-as-drafted.txt` (exit 1,
  `QUOTE_PROBE items=7 failures=2`, `FAIL S187/S188 anchor-revision-missing`).

**F2 — the stated word counts are the whole line's counts, not the quoted spans'.** The
Gate prints the S187 quote "…and four content-blind" labelled "(17 words)"; that span is
**14** whitespace words — 17 is the count of the whole of line 125, which begins
`content" is false:`. The S188 span is **16** words labelled "(17 words)"; 17 is the count
of the whole of line 130, which ends `, and`. The lane's own precedent counts the *span*:
the round-75 Gate prints 20 and 13 words for its two quotes, and whitespace-split of those
exact spans gives 20 and 13. Both spans stay under the 25-word bar, so this is a
precision defect in the record, not a gate failure. Evidence: whitespace-split of the
spans read back from `da9ac7ec:corpus/lessons/round-75-verifier-spotcheck.md` lines
125/127/130, compared against `corpus/lessons/round-76.md` Gate lines 15 and 20.

**F3 — a receipt-precision sentence the receipts do not yet bear.** `claims.md` line 11
says routed defect 4 is "honoured by naming the controls revision in every receipt". No
committed r76 receipt names a revision: `grep -cE '\b[0-9a-f]{40}\b'` over
`da9ac7ec:corpus/evidence/round76/controls/*.txt` returns 0 for all six. The r75 receipts
it replaces carried `measured-at=8022f72c889c904b5657d52c7f29e1643392a216` in five of ten.
The r76 receipts do carry the instrument digests, so the bytes are recoverable, but the
tree they were measured in is not named. This is reported, not edited — the controls commit
is committed and the claims file is frozen, and the round's own rule forbids amending a
frozen instrument after a seat has scored it. The L1 chooses between appending the
measured revision to the receipt headers and correcting the claims sentence.

## 4. Gates run (all fail-closed, with exit codes)

| gate | command | result |
|---|---|---|
| quote/anchor probe, L1's anchors | `python3 .ufo/waves/round-76/w1/R76Scribe/probe/quote-anchor-probe.py items.json` (scratch copy) | **exit 1** — 2 anchor failures; `probe-as-drafted.txt` |
| quote/anchor probe, corrected anchors | same tool, `items-fixed.json` | **exit 0** — 5/5 contiguous, all ≤25 words; `probe-corrected.txt` |
| census validate, baseline (lane at `5daa3628`, no new rows) | `sources-census.sh validate --file $S/mirrorA/corpus/SOURCES.md` | **exit 0** — only the five pre-existing W04 warnings (S051, S053, S073, S074, S075) |
| census validate, L1's three rows + cited lesson file | `… --file $S/mirrorB/corpus/SOURCES.md` | **exit 0** — same five W04s; rows 186→189, A123/B48/C15→A123/B50/C16, mined 150→152, rejected 17→18 |
| census validate, same rows with the cited lesson file **absent** | `… --file $S/mirrorC/corpus/SOURCES.md` | **exit 1** — `E11 S187 missing used-by corpus/lessons/round-76.md`, same for S188: the check is fail-closed, not vacuous |
| census validate, this seat's corrected rows | `… --file $S/mirrorD/corpus/SOURCES.md` | **exit 0** — same five W04s, same 189/A123/B50/C16/mined 152/rejected 18 |
| C2 battery vs a counter that **sleeps** on every bogus fixture | `c2-battery.py --counter <sleep-counter> --work DIR --child-timeout 5` | **exit 1**, `C2_BATTERY=FAIL bogus_rejected=0/6 positive=1/1 lane=PASS` — a timeout is not scored as a rejection (`probe-c2-timeout.txt`) |
| C2 battery vs a counter that **exits 2** on the bogus fixtures it detects | same, crash counter | **exit 1**, `C2_BATTERY=FAIL bogus_rejected=2/6 …` — exit 2 is counted as a rejection for the two fixtures it crashed on, but the four it did not detect still fail, so the battery does not go green on a partial crash (`probe-c2-exit2.txt`) |
| lane counter over committed bytes (read-only, run from `/tmp`) | `python3 -B corpus/evidence/round76/correction-count-v2.py --lane <lane> --base 8022f72c889c904b5657d52c7f29e1643392a216 --rev master` | **exit 0** — `DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`, `C2V=PASS checks=9/9`, matching `claims.md` line 97 |

The last two probes are **not** attacks on the frozen instruments; they characterise how
the frozen C2 battery scores a timeout and a non-zero exit, so the L1 can state the
instrument's limits accurately. Neither shows the battery going green on a wrong counter.

## 5. Boundaries honoured

- **Leaf seat.** No subagents, no `agent://all`, no network, no tool installs (nothing to
  install; `RULES.md` read, no pacman transaction attempted — the orchestrator's pacman
  guard is respected).
- **No production edit.** The lane's `corpus/SOURCES.md`, `corpus/lessons/round-76.md`,
  `corpus/evidence/round76/**`, `corpus/QUALITY.md`, `tools/` and `SCORECARD.md` were not
  written by this seat. The L1's uncommitted worktree edits to `corpus/SOURCES.md`,
  `corpus/lessons/round-76.md` and `SCORECARD.md` were read, never touched.
- **No lane or fleet git/jj mutation.** No commit, no push, no branch or ref write, no
  `git add`. Every `git` call in this seat was a read (`show`, `cat-file`, `rev-parse`,
  `ls-tree`, `ls-files`, `merge-base --is-ancestor`, `log`, `status`, `diff`). The lane's
  `git rev-parse --show-toplevel` prints `/home/vgpnk/Projects/shokunin/chousa-shokunin`
  and that is the only tree any command touched; fixtures were built under scratch.
- **Scratch discipline.** All clones, mirrors and fixtures lived under
  `/fast/scratch/hyaku/chousa-r76/R76Scribe/` and were deleted before this report was
  finalised; the receipts that mattered were copied into the wave folder first. No file
  over 50 MB went to `/tmp`; the C2 counter run used `/tmp` only as the cwd of a read-only
  child process.
- **Answer-key hygiene.** No probe reveals a case's class or label: the battery's own
  output was used as-is, and the two probe counters I wrote derive their behaviour from
  the *text* of a lesson file, not from a case's identity, argv, path or parent command line.

## 6. Out of scope / not this seat's call

- Whether the corrected anchor (`1af39fed…`) or an alternative revision should be printed
  in the rows — the L1 owns the registry edit; this seat supplies the verified value.
- Whether F3 is fixed in the receipts or in the claims sentence (both are frozen-adjacent).
- The claim verdicts themselves (C1/C2 predicates): this seat did not re-score them. The
  receipts it read were read as evidence for the rows, not re-judged.
- The non-author spot-check of the admit/reject set: requested by the round, owned by
  whoever the L1 dispatches. The probe in §4 is a scribe's own check, not that review.

## 7. Conflicts for the canonical judge

- **F1 (anchor revision).** The L1's rows and Gate name `e515c9624278cef906671d76188cb44e2a3445fe`
  for a file that does not exist at that revision. Verbatim: `fatal: path
  'corpus/lessons/round-75-verifier-spotcheck.md' exists on disk, but not in 'e515c962'`.
  The file's blob `c53d32c944460213812368d92b8f21527c0b464e` is present at `1af39fed…`,
  `da9ac7ec…` and `5daa3628…`. This seat's rows use `1af39fed…` and name the blob.
- **F2 (word counts).** Gate line 15 prints "(17 words)" over a 14-word span; Gate line 20
  prints "(17 words)" over a 16-word span. The 17s are the whole-line counts of lines 125
  and 130. The lane's own r75 Gate counts spans (20, 13).
- **F3 (receipt precision vs claims).** `claims.md` line 11: "4 (receipt precision) is
  honoured by naming the controls revision in every receipt". Committed r76 receipts name
  zero revisions.

## 8. Artifacts

| path | what |
|---|---|
| `.ufo/waves/round-76/w1/R76Scribe.md` | this report |
| `.ufo/waves/round-76/w1/R76Scribe/draft-SOURCES-rows.md` | drafted S187 / S188 / S189 registry rows with their verification evidence |
| `.ufo/waves/round-76/w1/R76Scribe/draft-Mistakes-rows.md` | drafted lesson `## Mistakes` rows (3) |
| `.ufo/waves/round-76/w1/R76Scribe/census-receipts.txt` | census validate + census on four scratch mirrors, with exit codes |
| `.ufo/waves/round-76/w1/R76Scribe/probe-as-drafted.txt` | quote/anchor probe on the L1's anchors — exit 1, 2 anchor failures |
| `.ufo/waves/round-76/w1/R76Scribe/probe-corrected.txt` | same probe on the corrected anchors — exit 0 |
| `.ufo/waves/round-76/w1/R76Scribe/probe-c2-timeout.txt` | C2 battery vs a sleeping counter — exit 1 |
| `.ufo/waves/round-76/w1/R76Scribe/probe-c2-exit2.txt` | C2 battery vs a counter exiting 2 — exit 1 |

**Tooling:** none installed or upgraded this round; no pacman transaction attempted (host
pacman guard in force). Scripts used: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(read-only), `git`, `python3` (standard library only), `sha256sum` via `git show | sha256sum`.
