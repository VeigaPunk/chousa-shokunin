# Round 44 lesson

author: chousa L1 (Kimi fresh L1)
date: 2026-10-24
base: `e6983f6e242c7b82bd9a9c5ee170257624e8f109`
freeze: `043f19a1db91288947493d9f879e61e7a9f07241`

No external fetch. L0 `8d77e6c1` is still open. This lesson does not duplicate
that question, the register-staleness question, or the inherited-tree question.

## Claims

Frozen in `corpus/evidence/round43/claims.md` is the previous round. This
round's predicates are in `corpus/evidence/round44/claims.md`, frozen before
any seat scored.

- C1 operability: the launcher log proves one parent pid reaped every spawned
  child. Dead seats are not a miss. A prose assertion and a pids-0 log fail.
  The cheapest forge (a hand-written log with invented pids) is named and is
  not what the counter stops. A wave-2 critic re-read that sentence
  (`.ufo/waves/round-44/w2/W2CritForge.md`).
- C2 calibration: 36 inherited reports are reverified-commit; 3 modified JSON
  files are left-named with `not hunk-verified`. An all-left table fails.
- C3 depth: lane S079 is the RFC 7089 URL, not staged S081. The quote is in
  the committed capture.

Freshness is unchanged. The captures' mtimes are 2026-10-23 20:33 and 20:36
-0300. This round launched at 2026-10-24T21:47:59-03:00. Opening those
captures is not a freshness improvement.

## Mistakes

1. Class: launch-flag. Evidence: every wave-1 seat log ends
   `error: Cannot combine --prompt with --auto.`
   (`corpus/evidence/round44/seat-logs/ReviewC1Shape.log`). Captured-by: none
   at freeze. The selftest spawned `sleep`, not `kimi`, so it could not catch
   the flag pair. Fix: drop `--auto`. Shown able to fail: `kimi --auto --prompt
   pong` exits 1 with that error; `kimi --agent-file … --prompt pong` exits 0.
   The 64 wave-1 names were not replaced.
2. Class: registry-insert. Evidence: the first scratch validate exited 1 with
   `E12 S079 row outside Registry section`
   (`.ufo/waves/round-44/assimilation/validate-census.txt` was overwritten by
   the passing run; the failing insert is recorded here). Captured-by: census
   E12. Fix: insert the rows after the S078 line, inside `## Registry`. Shown
   able to fail: the outside-registry insert is the E12 the census already
   prints on a row past `## Paths`. The in-section mirror exited 0.
3. Class: receipt-truncation. Evidence: `.ufo/waves/round-44/w2-parent-lifetime.receipt`
   carries 5 `reap` lines and no `end parent_pid=` line; the launcher was killed
   when the orchestrator process died mid-wait. Captured-by: none at freeze —
   `c1-count.py` reads `n_spawned`/`n_reaped` from the `end` line, so a
   truncated receipt scores 0 and fails, but nothing said the receipt must be
   *complete* to be evidence. Fix: treat the `end` line as the receipt's
   completeness marker; a receipt without it proves nothing and is named as
   truncated, never as parent-lifetime evidence. Shown able to fail: the
   wave-2 receipt scores `N_SPAWNED=0/64`, `N_REAPED=0/64`,
   `PARENT_PID_MATCH=0/1`, `C1=FAIL`, exit 1. Wave 3's receipt carries
   `end parent_pid=3635446 … n_spawned=32 n_reaped=32`.
4. Class: exit-status-overclaim. Evidence: wave-3 seat `W3ExecSelftest` ran
   `tools/parent-lifetime.sh` with a malformed dispatch JSON; the script
   printed `end … n_spawned=0 n_reaped=0` and **exited 0**
   (`.ufo/waves/round-44/w3/W3ExecSelftest.md`). Captured-by: none at freeze —
   the script's own header says "Exit 0 when the end line is written", which is
   a contract about the receipt, not about seats. Fix: QUALITY 63 — a
   launcher's exit status is not evidence that its seats ran; the receipt's
   `n_spawned`/`n_reaped` is the tell. Not fixed in this round: the frozen C1
   predicate reads the receipt, and changing the launcher's exit contract after
   the claims were scored would move the ground under the measurement. The
   defect is named for the next round.

## Mistakes (continued)

5. Class: seat-timeout. Evidence: wave 3's receipt records `exit_code=124` for
   27 of its 32 seats; `timeout --signal=TERM --kill-after=20 420` in
   `tools/parent-lifetime.sh` killed them at 420 s, and 23 seats left no
   report. Captured-by: none at freeze. Fix: the next round's launcher must
   size the timeout from the heaviest item, or dispatch a lighter item set;
   420 s was sized for wave 2's lighter items. Not fixed here: the dead seats
   stay dead and the round is already at its 128-seat ceiling.

## Gate

Theme: version binding of a citation to a prior state. One theme. Two entries.
Three rows. No fetch.

Admit:

- `corpus/knowledge/citation-version-binding-r36.md` cites lane S079. Staged
  id of that URL was S081. Lane id is S079 because the URL is the evidence and
  S079 is the next free lane id. Not staged-id minus 2.
  Located quote (7 words), access 2026-10-24, no fetch: "constitutes a promise
  that the resource state". Capture
  `d0c4a09a9de32cb91d5e3797.txt`, sha256
  `c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc`, byte
  offset 14896 (wave-2 reviewer, `.ufo/waves/round-44/w2/W2ReviewRfc.md`).
  Recheck prose stripped to `365d`. Stripped prose: re-open the RFC and confirm
  section 2.1.1 still carries the promise sentence.
- `corpus/knowledge/citation-version-binding-r37.md` cites lane S080 (staged
  S091, WARP FAQ) and lane S081 (staged S092, E2867). Located quote (8 words),
  access 2026-10-24, no fetch: "National institution websites are archived once
  per month". WARP capture sha256
  `a7e46e274b0784f81426bdc602785b03db1fa87f8f34916097d42ff36cac8dc8`.
  E2867 located token: `warp.ndl.go.jp/web/20250102112233`. Capture sha256
  `d2a58e70eb8a2b4e42836c0b3df5035c67a45bbce71c412cbcd2bfb155d4848f`.
  Recheck prose stripped to `90d` (S080) and `180d` (S081).

Reject:

- Staged S082, the SAMR record for GB/T 7714-2025, and the GB/T half of
  `citation-version-binding-r36.md`. Reason: round 43 classed that row
  not-carried, and this round did not fetch. Flip: a text capture of that
  record contains the issued and effective dates as a contiguous span.
- Staged S093, the Portico page, and the Portico half of
  `citation-version-binding-r37.md`. Reason: round 43 classed that row
  misquote. A partial overlap is not the staged sentence. Flip: a capture
  where the four-factor authenticity sentence is one contiguous span matching
  the staged teaches cell.

S077: `assimilation/collisions` is empty. S077 is not a row-start id in the
staged append. It occurs once, inside a cell of staged S093
(`.ufo/waves/round-44/w2/W2ScoutS077.md`). Lane S077 stays the pdftotext
manual. No id was shifted by adding one. The indented guard still catches a
scratch `  | S079 |` row; a column-zero pattern misses it
(`assimilation/guard/collisions` is `S079`).

used-by on the adopted rows lists only the entries that cite them. Status
`mined`. No cell contains a pipe.

Scratch census before the append: `validate --file` on the mirrored registry
plus the three rows, exit 0, five W04, no E03/E04
(`assimilation/validate-census.txt`).

## Sources opened

- S079 RFC 7089, from the committed capture, no fetch.
- S080 WARP FAQ, from the committed capture, no fetch.
- S081 E2867, from the committed capture, no fetch.

## Spot-check

Seats this lane dispatched are still the lane. What the wave-3 seats found against
the landed state, and what it means for the claims:

- `W3MutC1` — C1's kill rule holds. Zeroing one `reap` child's pid gives
  `ZERO_PIDS=1`, `C1=FAIL`, exit 1; changing `end parent_pid` gives
  `PARENT_PID_MATCH=0/1`, `C1=FAIL`, exit 1. The same seat notes a limit: a
  `spawn` line's `child_pid=` is never read by the counter, because `parse()`
  collects child pids from `reap` records only. The landed receipt's spawn and
  reap child pids agree pairwise, so the gap is cosmetic today; the counter's
  name is wider than what it checks.
- `W3MutC2` and `W3CritBlind` — C2's kill rule holds. A corrupted digest gives
  `REVERIFIED=35/36`; a deleted row gives `LEFT_NAMED=2/3`; a blank reason
  gives `REVERIFIED=35/36`; a modified path reclassified as `reverified-commit`
  gives `LEFT_NAMED=2/3`. All exit 1, none false-PASSes. Residual blind spots
  named by the seat and not fixed here: a coordinated two-file edit (report
  bytes plus its digest row) still passes; extra rows in the table move no
  counter; duplicate rows last-win; the reason text of a reverified row is
  checked only for non-emptiness.
- `W3CritFresh` did not report (killed by the 420 s timeout). The freshness
  grade rests on wave 2's `W2CritFresh`, which measured the capture mtimes
  against the launch clock: RFC capture 2026-10-23 20:33, WARP 20:36,
  E2867 20:37 -0300, against a launch of 2026-10-24T21:36:37-03:00. Grade:
  unchanged.
- `W3RevS079` — the S079 row splits into 11 columns with no pipe in any cell,
  the same shape as the other 80 data rows, and the entry cites `source: S079`
  and not `source: S081`. C3 is not falsified.
- `W3SimpIds` — the id binding is by document, not by arithmetic. The staged
  file calls PRISMA-S "S079", so the string "S079" names two different
  documents in the two files; the landed offsets are −2, −11 and −11, so no
  constant shift reproduces the landed binding. URL equality does.
- `W3ExecFileCensus` — the validate-before-append mirror exits 0 with the same
  five W04 warnings and no E03/E04.
- `W3ExecShaRfc` — the capture file name is the first 24 hex digits of
  sha256 of the URL string, confirmed by two independent computations.
- `W3CritScope` — the write-scope audit found no file of this round's outside
  the lane tree, and the fleet-root sweep found no misrooted seat file.

Pending: the non-author spot-check. A seat this lane dispatched is still the
lane, so none of the above counts as external verification.
