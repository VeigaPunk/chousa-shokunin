# Round 83 — lesson draft (seat `R83ScribeLesson`)

Draft of the sections `corpus/lessons/round-83.md` does not yet carry, for the L1 to integrate at
`aca2a781ef2db375881c21bf407e153f786ac61f`. The existing `## Gate` block is at that revision and is not rewritten here;
the addendum below appends to it. **Not landed by this seat.** Receipts:
`.ufo/waves/round-83/w1/R83ScribeLesson/receipts/` (paths below are relative to the lane root).

## Mistakes

Mined this round: a closure counted knowledge entries with a command that counts every file in the directory, so the
placeholder `corpus/knowledge/.gitkeep` was counted as an entry and both endpoints of a before/after pair came out one
high — while the round's own gate printed the correct number in the same wave.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a count whose unit is "entry" was taken with a command whose unit is "file": the directory placeholder was counted as a knowledge entry, so both endpoints of a before/after pair are one high, and the number was written into the closure beside a gate line that already carried the right one | `SCORECARD.md:3756` reads "knowledge 94 → 95 on question framing"; `corpus/lessons/round-82-verifier-spotcheck.md:24-25` names the cause ("counts `corpus/knowledge/.gitkeep`"); the same wave's gate line reads `GATE G02 knowledge-index PASS 94 entries indexed` (`R82CriticClaims.md:245`) | the round-82 verifier spot-check (non-author), conformance defect (1), status-neutral | count `.md` files, not tree entries: `git ls-tree -r --name-only <rev> corpus/knowledge \| grep -c '\.md$'` |

**The two commands, run at both endpoints** (`receipts/01-knowledge-recount.txt`):

```
$ git -C … ls-tree -r --name-only 142b6f0c corpus/knowledge | grep -c '\.md$'
93                                    # rc 0   (receipt line 5)
$ git -C … ls-tree -r --name-only 142b6f0c corpus/knowledge | wc -l
94                                    # rc 0   (receipt line 8)
$ git -C … ls-tree -r --name-only 03b586d1 corpus/knowledge | grep -c '\.md$'
94                                    # rc 0   (receipt line 15)
$ git -C … ls-tree -r --name-only 03b586d1 corpus/knowledge | wc -l
95                                    # rc 0   (receipt line 18)
```

The report's pair is the second command's output at both ends; the `.md` count is 93 → 94. The direction is unchanged
and both absolute numbers are one high.

**The fix, shown able to fail** (same receipt, lines 24–28). The check compares a claimed count with the `.md` count:

```
RECOUNT_CHECK rev=142b6f0c claimed=94 md=93 MISMATCH
RECOUNT_CHECK rev=142b6f0c claimed=93 md=93 MATCH
RECOUNT_CHECK rev=03b586d1 claimed=95 md=94 MISMATCH
RECOUNT_CHECK rev=03b586d1 claimed=94 md=94 MATCH
```

The first and third lines are the report's numbers and the check refuses them; the second and fourth are the corrected
numbers and it accepts them. A check that accepted both would not be a check.

**Why the round's own output did not stop it.** The round-82 gate counted entries by the `.md` rule and printed
`GATE G02 knowledge-index PASS 94 entries indexed` at the landing (`R82CriticClaims.md:245`; the landing tree
`b4a41d25` has `md=94`, `all=95`, `receipts/08-egress-and-landing-count.txt:11-14`). The closure wrote 95. The correct
number was already in the wave; nothing compared the two.

**What the round did about it.** No lane file changed from this seat: the wrong number sits in `SCORECARD.md`, a
fleet-root file this seat may not edit, and the correction belongs to whoever owns the closure. What this lesson fixes
is the counting command and the cross-check: a knowledge count is `grep -c '\.md$'`, compared with the gate's
`entries indexed` line before it is written down.

**Residual.** The round-82 verdict does not change: one entry was added, so the direction is right and only the
absolute numbers are wrong. A later reader who recounts finds 93 → 94 where the closure says 94 → 95; that is the
failure this class produces.

## considerthese

Read: `considerthese/2026-11-06.md` (newest, cursor `f7449f9`) and `considerthese/2026-11-05.md` (cursor `378fda8`);
neither file was edited (`md5sum` in `receipts/05-considerthese.txt:6-7`). One still-unimplemented proposal named:
**2026-11-06, "One open Gate-record S-id per daily review"** — pick one id from the ScoutA remainder (S170, S171,
S173–S176, S178, S179, S182, S183, S191, S193), `git show <rev>:<path>`, re-count the quote, report match/mismatch.

**Not implemented this round.** Evidence: the twelve ids occur in **0** files of round-83 material once this seat's own
receipts are excluded (`receipts/05-considerthese.txt:34-36`, rc 0; the first pass's 60 hits at `:11-12` are this
seat's own receipt text listing the ids — a self-reference artifact, recorded at `:25-28`); the round's Gate records are
S009, S212, S213 (`:15-17`), none in the remainder list; the proposal→adoption ledger that would record adoption has 36
rows and no row for either 2026-11-05 or 2026-11-06 proposal (`:20-23`, `grep -c CT-2026110` → 0, rc 1). Reason: the
frozen claims bind round 83 to C1/C2 on S009/S212/S213, and the proposal is a daily-review habit of the reflection bot —
a leaf scribe can draft it but cannot land it.

## Assimilation

**none.** Reason: `merge/chousa` id collisions were measured in round 78 and nothing has renumbered them. Re-count at
`aca2a781`: `.ufo/waves/round-78/assimilation/collisions` has **111** lines against **114** staged ids (`wc -l`,
`receipts/06-collisions.txt:3-5`, rc 0); `reg-ids` is still 192 (`:7`) and the live registry now has 213 rows
(`grep -c '^| S[0-9]' corpus/SOURCES.md`, `:9`). The file's last commit is `3eb4a3ca` (2026-11-04, `:11`), so these are
the same bytes rounds 81–82 counted. No round-83 assimilation directory exists (`ls` → `No such file or directory`,
rc 2, `:13-14`). No package bytes read, no campaign tool run, no shokuknow write.

## Gate — non-author spot-check addendum

Appends to the `## Gate` block at `aca2a781`. One admit and one reject, both drawn from that block; the block's three
records are unchanged and all three still verify.

**Tool check.** `python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md` prints
`GATE_RECORD corpus/lessons/round-83.md:19 S009 OK`, `:20 S212 OK`, `:21 S213 OK`,
`GATE_RECORDS files=1 records=3 ok=3 fail=0`, rc 0 (`receipts/02-gate-verify.txt:3-7`). Each record also passes alone
(`:12-14` S213, `:18-20` S009).

**Egress ordering, verified.** `8fff80ee` is committed at `2026-11-06T17:53:00-03:00` = 20:53:00Z, six seconds before
the first fetch (20:53:06Z), and the three URLs are rows of its intended-target table
(`receipts/08-egress-and-landing-count.txt:3-9`; `corpus/evidence/round83/egress-approval.md:28-30`).

- **Admit S009** (spec, A, opened 2026-10-19, re-opened this round). The MECIR page's C55 row is the sentence
  "Collect the source of information for each risk of bias judgement (e.g. quotation, summary of information from a
  trial report, correspondence with investigator etc.)." It locates in the committed capture
  `corpus/captures/ea16817cb78993196ea1a095.txt` at line 494 (`FOUND`, rc 0, 24 words —
  `receipts/03-gate-locate.txt:6-8`); the capture's sha256 `3dfd10e567809633e762…` (`:21`) equals the `txt_sha256`
  cell of refetch row 157 (`:31`), whose `curl_rc` is 0 and `http` 200. The registry row (`corpus/SOURCES.md:19`) is
  `mined`, tier A, used-by `corpus/knowledge/appraisal-judgment-records-r83.md`, and the diff `a46534a5..81b81173`
  touches exactly that row plus the two new ones (`--numstat` = `3 1`, `receipts/07-anchors.txt:41-48`). The anchor's
  parenthetical matches the capture's rows: C53 "Assessing risk of bias in duplicate" (line 487), C54 "Supporting
  judgements of risk of bias" (491), C55 "Providing sources of information for risk of bias assessments" (493)
  (`receipts/07-anchors.txt:5-12`). The entry's rows 3 and 5 rest on Q1/Q2, i.e. C54/C55.
  **Boundary note, reported not repaired:** the anchor's range reads "standards C52-C59 table rows", but the capture
  also carries a `C60` row at line 503 whose text is "Not applicable" (`receipts/07-anchors.txt:15`), and the page's
  own title range is C52-C60 (capture lines 14, 307, 401). No decision changes — C60 carries no standard and the entry
  cites none of it — but a reader who takes "table rows" as the page's range finds one row unnamed.
- **Reject (kept as a decision, no registry row): the Millard et al. study result quoted inside S212.** The block
  rejects "the Millard et al. finding quoted inside S212 (one reviewer for about one-third of articles with a
  machine-learning tool)" as support for any row. Verified: the sentence "about one-third of articles could be assessed
  by just one reviewer" locates in the S212 capture at line 622 (`FOUND`, rc 0, 11 words —
  `receipts/04-reject-millard.txt:6-8`), inside a paragraph that opens "Novel methods for assessing risk of bias are
  emerging" and attributes the result to "A study showed" (`:11`); the chapter's own standard, the S212 record's
  quote, is at line 611 ("…should be performed independently by at least two people", `:14`). The entry's Limits note
  already excludes it (`corpus/knowledge/appraisal-judgment-records-r83.md:69-70`) and no decision row cites it
  (`grep -c -i millard` on the entry → 0, `receipts/04-reject-millard.txt:28`). The reject is prose, not an in-class
  `GATE-RECORD`: the tool counts `records=3`, not 4 (`:17-21`), which is the frozen class working as declared. Flip
  condition unchanged: the primary study opened and its design read — this seat made no fetch, its item names no
  re-open.

**What this addendum does not check.** No live re-open: the seat's item names none, so no network was used; the captures
are trusted as committed bytes whose sha256 equals the refetch cell. Whether a located quote *grounds* the row it is
cited for is C1's K3 reviewer question, not a substring test's. The C60 boundary note is reported, not repaired.
