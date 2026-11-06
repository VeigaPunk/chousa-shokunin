# R83ScribeLesson — report

Seat: lesson scribe (leaf, no dispatch). Lane `chousa`, root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Tip read: `aca2a781ef2db375881c21bf407e153f786ac61f`. No network, no git/jj mutation, no production edit, no
`pacman`/tool install (nothing installed, so no tool record). Scratch `/fast/scratch/hyaku/chousa-r83/R83ScribeLesson/`
deleted at yield.

## Behavior

Drafted the four sections `corpus/lessons/round-83.md` does not yet carry, for the L1 to integrate: `## Mistakes`
(one mined mistake, with the fix shown able to fail), `## considerthese` (one still-unimplemented proposal, not
implemented), `## Assimilation` (`none`, re-counted), and a `## Gate` addendum (one admit, one reject, both drawn from
the block at `aca2a781`). Delivered at
`.ufo/waves/round-83/w1/R83ScribeLesson/lesson-draft.md`; nothing landed.

## Checks run

| # | command | receipt | observed | rc |
|---|---|---|---|---|
| 1 | `git -C LANE ls-tree -r --name-only 142b6f0c corpus/knowledge \| grep -c '\.md$'` | `receipts/01-knowledge-recount.txt:5` | `93` | 0 |
| 2 | `git -C LANE ls-tree -r --name-only 142b6f0c corpus/knowledge \| wc -l` | `:8` | `94` | 0 |
| 3 | `git -C LANE ls-tree -r --name-only 03b586d1 corpus/knowledge \| grep -c '\.md$'` | `:15` | `94` | 0 |
| 4 | `git -C LANE ls-tree -r --name-only 03b586d1 corpus/knowledge \| wc -l` | `:18` | `95` | 0 |
| 5 | discriminator, claimed vs `.md` count at both revs | `:25-28` | `MISMATCH / MATCH / MISMATCH / MATCH` | 0 |
| 6 | `python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md` | `receipts/02-gate-verify.txt:3-7` | `GATE_RECORDS files=1 records=3 ok=3 fail=0` | 0 |
| 7 | same tool on per-record extracts (S009, S213) | `:12-14`, `:18-20`, `:21-30` | `records=1 ok=1 fail=0` each | 0 |
| 8 | hand location, round-82 `LOC` one-liner, three quotes | `receipts/03-gate-locate.txt:6-8`, `:11-13`, `:16-18` | `FOUND` ×3; `wc -w` = 24, 14, 16 | 0 |
| 9 | `sha256sum` of the three captures vs record prefixes and refetch `txt_sha256` | `:21-23`, `:25-27`, `:31` | `3dfd10e5…`, `3b57cb03…`, `f5dae335…` all match | 0 |
| 10 | Millard reject: hand location in S212 capture | `receipts/04-reject-millard.txt:6-8` | `FOUND`, 11 words | 0 |
| 11 | same tool on the lesson (is the reject in class?) | `:17-21` | `records=3`, not 4 — prose, out of class | 0 |
| 12 | anchor check S009 / S212 / S213 vs captures | `receipts/07-anchors.txt:5-12`, `:15`, `:20-27`, `:31-37` | rows/headings present; C60 row present | 0 |
| 13 | `git diff --numstat a46534a5 81b81173 -- corpus/SOURCES.md` | `:48` | `3 1 corpus/SOURCES.md` | 0 |
| 14 | egress commit time vs first fetch | `receipts/08-egress-and-landing-count.txt:3-9` | `2026-11-06T17:53:00-03:00` (= 20:53:00Z) < `20:53:06Z`; 3 URLs in table | 0 |
| 15 | landing-tree knowledge count | `:11-14` | `md=94`, `all=95` | 0 |
| 16 | `md5sum` of the two considerthese files (read-only) | `receipts/05-considerthese.txt:6-7` | `0e4db2da…`, `06f8df13…` | 0 |
| 17 | twelve ScoutA ids across round-83 material, own receipts excluded | `:34-36` | `0` files | 0 |
| 18 | ledger rows / `CT-2026110` rows | `:20-23` | `36` rows; `0` (rc 1) | 1 |
| 19 | `wc -l` collisions / staged-ids / reg-ids; registry rows; last commit | `receipts/06-collisions.txt:3-11` | `111 / 114 / 192 / 213`; `3eb4a3ca 2026-11-04` | 0 |
| 20 | `ls .ufo/waves/round-83/assimilation` | `:13-14` | `No such file or directory` | 2 |

## Findings

**F1 — S009 anchor boundary note (residual, out of the frozen kill class).** The registry anchor reads "standards
C52-C59 table rows"; the committed capture also carries a `C60` row at line 503 whose text is "Not applicable", and the
page's own title range is C52-C60 (capture lines 14, 307, 401). Command:
`grep -n '^ C60 ' corpus/captures/ea16817cb78993196ea1a095.txt` → `503: C60 Not applicable`, rc 0
(`receipts/07-anchors.txt:15`). No decision changes: C60 carries no standard, the entry cites none of it, and the
record's quote is the C55 row at line 494. Reported, not repaired (the registry is not this seat's to edit).

**F2 — self-reference artifact in the twelve-id measurement (method, recorded).** The first pass of
`grep -rhoE 'S170|…|S193' corpus/evidence/round83/ corpus/lessons/round-83.md .ufo/waves/round-83/ | wc -l` printed
`60` (`receipts/05-considerthese.txt:11-12`) because the receipt file it had just written lists the ids; the only
hitting files are this seat's own two (`:27-28`). Excluding the seat folder the count is `0` (`:34-36`, rc 0). The
corrected number is the one used in the draft.

**F3 — the mined mistake, reproduced.** Round-82's closure records "knowledge 94 → 95" (`SCORECARD.md:3756`); the
`.md` count is 93 → 94 and the all-files count is 94 → 95, the difference being `corpus/knowledge/.gitkeep`
(`receipts/01-knowledge-recount.txt:5,8,15,18`; gitkeep present at both revs, `:11`, `:21`). The round's own gate
printed `GATE G02 knowledge-index PASS 94 entries indexed` at the landing (`R82CriticClaims.md:245`) — the correct end
number was already in the wave. The discriminator refuses the closure's numbers and accepts the corrected ones
(`:25-28`). Status-neutral for the round-82 verdict (direction unchanged). The candidate was kept: it reproduces from
bytes at two pinned revisions, the closure itself names it, and the round's own gate line carries the correct number —
so the failure is a comparison nobody made, not a missing measurement. No better-evidenced candidate was found in the
rounds this seat read (round-82 lesson, round-82 spot-check, round-83 claims).

**F4 — no kill-rule firing found in the checks this seat ran.** All three Gate records verify (`receipts/02-gate-verify.txt:3-7`),
all three quotes locate with the recorded word counts (`receipts/03-gate-locate.txt:6-18`), all three capture digests
equal their refetch `txt_sha256` cells (`:21-31`), the egress table precedes the first fetch (`receipts/08-egress-and-landing-count.txt:3-9`),
and the registry diff is the three rows the lesson names (`receipts/07-anchors.txt:41-48`). The Millard reject is
prose, not an in-class record (`receipts/04-reject-millard.txt:17-21`).

## Gates

- Frozen C2 predicate (b) exercised exactly as written: `python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md`
  → `records=3 ok=3 fail=0`, rc 0 at `aca2a781` (`receipts/02-gate-verify.txt:6-7`).
- The draft's Gate addendum carries one admit (S009) and one reject (Millard et al.), each with its command, receipt
  and observed line.
- No claim was scored by this seat; the depth counter and the entry's K2/K3 warrant checks were not run.

## Touched surfaces

Written, all under the seat's output folder:
`.ufo/waves/round-83/w1/R83ScribeLesson/lesson-draft.md`, `run-receipts.sh`, `receipts/00-env.txt` … `receipts/08-egress-and-landing-count.txt`,
`receipts/s009-only.md`, `receipts/s213-only.md`. Nothing else was created, modified or deleted in the lane or the
fleet root; no commit, no push, no `jj`.

## Out of scope

- Not scored: C1 depth (K1–K4) and C2's K1–K4 beyond predicate (b). The S009 record's *warrant* for the entry's rows is
  C1/K3's reviewer question, not a substring test's.
- Not repaired: the `SCORECARD.md` count (fleet-root file), the S009 anchor range, any registry/capture/refetch byte.
- Not done: no live re-open (the item names none), so the lesson's "search query that located the two Handbook
  chapters" line is unverified by this seat; no depth-counter run; no package bytes read for assimilation.

## Artifacts

- `.ufo/waves/round-83/w1/R83ScribeLesson/lesson-draft.md` — the four drafted sections.
- `.ufo/waves/round-83/w1/R83ScribeLesson/receipts/` — `00-env.txt`, `01-knowledge-recount.txt`,
  `02-gate-verify.txt`, `03-gate-locate.txt`, `04-reject-millard.txt`, `05-considerthese.txt`,
  `06-collisions.txt`, `07-anchors.txt`, `08-egress-and-landing-count.txt`, `s009-only.md`, `s213-only.md`.
- `.ufo/waves/round-83/w1/R83ScribeLesson/run-receipts.sh` — the driver that produced them.

VERDICT: R83ScribeLesson C1 n/a — this seat drafted lesson sections and verified one record's bytes (S009: quote FOUND at 24 words, capture sha equals refetch cell, registry row consistent); it did not run the depth counter or test the entry's K2/K3 warrant.
VERDICT: R83ScribeLesson C2 held — the frozen predicate (b) at aca2a781 prints records=3 ok=3 fail=0 rc 0, and the addendum's admit/reject checks introduce no C2 kill-rule firing.
