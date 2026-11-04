# R76Scribe — drafted lesson `## Mistakes` rows (round 76)

Seat R76Scribe (chousa lane). Draft only — NOT committed. The lane's
`corpus/lessons/round-76.md` is READ-ONLY for this seat; the L1 (ChousaR76) owns the
lesson text. Shape is the round-75 lesson's `class | evidence | captured-by | fix`
four-column table (see `corpus/lessons/round-75.md` `## Mistakes`, lines 36–42).

Each row's evidence is a committed r76 receipt or a committed instrument, opened at the
controls commit `da9ac7ec684fe9fe9ad5554cab6180057255b76b` with
`git -C <lane> show da9ac7ec:<path>`. No claim below rests on an uncommitted file.

---

| class | evidence | captured-by | fix |
|---|---|---|---|
| a registry row anchored at a revision that does not contain the file it cites, so its located quote cannot be re-opened where the row says it can | the L1's in-worktree S187 and S188 rows both anchor `corpus/lessons/round-75-verifier-spotcheck.md` at `e515c9624278cef906671d76188cb44e2a3445fe`; that revision is the r75 landing tip and the spot-check file was added after it, so `git -C <lane> show e515c962:corpus/lessons/round-75-verifier-spotcheck.md` exits 128 with "exists on disk, but not in e515c962"; the file's blob `c53d32c944460213812368d92b8f21527c0b464e` exists at `1af39fed…`, `da9ac7ec…` and `5daa3628…` only | the scribe's fail-closed anchor probe, which resolves the anchor revision and path before testing the quote: `.ufo/waves/round-76/w1/R76Scribe/probe-as-drafted.txt` prints `FAIL S187 anchor-revision-missing` and `FAIL S188 anchor-revision-missing`, `QUOTE_PROBE items=7 failures=2`, exit 1 | anchor the rows at `1af39fed6058ad46fc075b72fddaae838f43273e` (the commit that adds the file; blob identical at `da9ac7ec…`) and name the blob, so the quote is re-openable at the revision the row prints; the probe re-run on the corrected anchors exits 0 (`.ufo/waves/round-76/w1/R76Scribe/probe-corrected.txt`) |
| a located quote's stated word count is taken from the whole source line, not from the quoted span, so the printed count does not match the printed quote | the L1's in-worktree lesson Gate prints the S187 quote as "commit subject, tree ids and byte sizes are stable metadata channels, and four content-blind" and labels it "(17 words)"; that span is 14 whitespace words, while 17 is the word count of the whole of line 125 (`content" is false: commit subject, … content-blind`); the same holds for S188, whose 16-word span is labelled "(17 words)" against whole-line 130 (which ends ", and"); the round-75 lesson's own quotes are counted on the span (20 and 13) | whitespace-split of the exact quoted span read back from `da9ac7ec:corpus/lessons/round-75-verifier-spotcheck.md` lines 125, 127 and 130, compared against the counts printed in the in-worktree `corpus/lessons/round-76.md` Gate lines 15 and 20 | print the count of the quoted span (S187 line 125 = 14 words, line 127 = 9; S188 line 130 = 16), or widen the quote to the whole line; the quoted span stays contiguous on the named line either way, so the ≤25-word bar holds |
| a receipt that names the instrument digest but never the revision it was measured at leaves the claim's own chronology unreadable from the receipt | none of the six committed r76 receipts names a 40-hex revision: `git -C <lane> show da9ac7ec:corpus/evidence/round76/controls/<each>.txt \| grep -cE '\b[0-9a-f]{40}\b'` returns 0 for all six, while `corpus/evidence/round76/claims.md` line 11 says routed defect 4 (receipt precision) "is honoured by naming the controls revision in every receipt"; the r75 receipts it replaces did carry one (`measured-at=8022f72c889c904b5657d52c7f29e1643392a216` in five of the ten r75 receipts) | the scribe's read of the committed receipts against the claims sentence they are cited for, at `da9ac7ec` and `5daa3628` | add the measured revision to each r76 receipt header — `measured-at=da9ac7ec684fe9fe9ad5554cab6180057255b76b` — beside the digests already printed, so the receipt is re-derivable at the revision the claim names; the digests alone make the bytes recoverable but not the tree they were measured in |

---

## Notes for the L1 (not part of the table)

- The third row above is a **receipt-precision** observation, not a change to a frozen
  instrument. The controls commit `da9ac7ec…` is already committed and the claims file is
  frozen at `5daa3628…`; per the round's own rule ("a rule changed after any seat has
  scored it is not the claim's rule"), this is reported, never edited. Whether to append
  the measured revision to the receipts or to correct the claims sentence is the L1's call.
- The first two rows concern only the **wording of the rows and the Gate** in the
  in-worktree drafts. The S187/S188/S189 row *content* (kind, tier, scope, status,
  used-by, recheck, opened) is unchanged from the L1's draft and passes the census.
- No production file was written by this seat. The only files this seat wrote are under
  `.ufo/waves/round-76/w1/R76Scribe/` and this seat's report
  `.ufo/waves/round-76/w1/R76Scribe.md`.
