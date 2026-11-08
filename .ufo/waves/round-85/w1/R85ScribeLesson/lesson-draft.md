# round-85 lesson — draft sections (seat R85ScribeLesson)

**Status: DRAFT, not landed.** These four sections replace `corpus/lessons/round-85.md`'s `## Mistakes`,
`## considerthese`, `## Assimilation` and extend its `## Gate` block. Nothing here is committed; the landing
bytes at `64803d33362f50cf9094e91fc3a4a07216c563ca` are untouched. Every receipt cited below was written by
this seat under `.ufo/waves/round-85/w1/R85ScribeLesson/receipts/` and is reproducible by
`receipts/00-fixture-construction.sh`.

**Already adopted elsewhere in the wave.** While this seat was measuring, the L1 appended two blocks to the
working-tree lesson — `## Corrections` (items 1–3) and `## Corrections (second block — wave R85ScribeLesson)`
(items 4–6) — and `plans/round-85.md` amendment 10 and `corpus/QUALITY.md` criterion 172 now cite this seat's
receipts 01/02/04. Items 4–6 of that second block state the same three findings this draft argues: the Gate
block's "none new" sentence (item 4), the floors-relaxed-to-the-artifact defect (item 5), and the missing
"first candidate run" receipt (item 6). **The `## Mistakes` and `## Gate` sections below are therefore the
narrative form of already-recorded corrections, not new claims**; they should be merged with that block rather
than filed beside it, and this draft does not duplicate items 1–3.

---

## Mistakes

Assessment of the two rows already drafted in `corpus/lessons/round-85.md:53-54`: **row 1 is confirmed, with its
evidence pointer repaired; row 2 is replaced.** Both fixes are shown able to fail — the counter output before and
after each fix is pasted below.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `vacuous-predicate` — the prefreeze C2 named a ground the frozen counter's own rules could never admit: `source:` named S020 and S023, but E6 requires three FRESH ids on the `source:` line and E7 excludes any id a base-list entry already cites (S023 is `source:`-cited by `search-transparency-reporting-r84.md`, base-list line 88). A frozen predicate of `fresh_sources=2` was therefore unreachable by construction: `fresh_sources` is the count of FRESH ids on the `source:` line, so `fresh_sources=2` can only be printed when E6 has already failed. | `corpus/evidence/round85/claims.md` at the freeze `5d0b9413` (C2 `source:` S020/S023; predicate `fresh_sources=2`); `corpus/knowledge/provenance-recording-r85.md:3` (`source: S215, S026, S024` at the landing rev); base-list `corpus/evidence/round85/base-knowledge.txt:88` + `corpus/knowledge/search-transparency-reporting-r84.md:3` (`source: S214, S018, S023`); receipts `01-counter-prefreeze-ground.txt`, `02-counter-fresh-sources-2.txt` | QUALITY 169 (new) | **dry-run the frozen counter against a stub entry before the freeze.** Showed able to fail: with the prefreeze ground the counter prints `fails=E6,E7` and rc 1; with the amended ground it prints `fails=-` and rc 0 (receipts 01 and 03 below). |
| `predicate-relaxed-to-the-artifact` — the prefreeze predicate also fixed a numeric floor (`rows= ≥ 7`, `located_quotes= ≥ 8`) that the amended ground could have met, and the amendment lowered it to the landed values (`rows= ≥ 6`, `located_quotes= ≥ 7`) in the same commit that changed the ground. The floor was not a barrier; it was re-based. A frozen count that is lowered in the same breath as the ground it was measured against measures nothing. | `corpus/evidence/round85/claims.md` at the freeze (`rows= ≥ 7`, `located_quotes= ≥ 8`, `fresh_sources=2`) vs. at `02df67db` (`rows= ≥ 6`, `located_quotes= ≥ 7`, `fresh_sources=3`) — `git diff 5d0b9413 02df67db -- corpus/evidence/round85/claims.md`; receipt `04-counter-prefreeze-floors-reachable.txt` | QUALITY 169 (new) | **a count floor is set by what the ground admits, not by what the first candidate happens to produce.** Showed able to fail: on the amended ground, an entry with one extra located quote and one extra decision row reaches `rows=7 located_quotes=8` and `DEPTH_R85=PASS` rc 0 — the prefreeze floor was satisfiable and was lowered anyway (receipt 04). |

**Repairs to the two drafted rows, stated plainly.** The drafted row 1 is confirmed on substance; its *evidence
pointer* was wrong in two ways and is repaired here. The drafted row 2 is not confirmed and is replaced.

1. **Drafted row 1's cited receipt does not contain the lines it is cited for.** `corpus/lessons/round-85.md:53`
   cites "scoring receipt `corpus/evidence/round85/controls/receipts/c2-d0-donothing.txt` and the E6/E7 lines of
   the first candidate run". `c2-d0-donothing.txt` holds three lines — `DEPTH_R85 entries=0 ok_entries=0 rows=0
   located_quotes=0 fresh_sources=0` / `DEPTH_R85=FAIL` / `depth rc=1` — i.e. it is the **tree-at-base do-nothing
   control**, not a candidate run; it contains no `E6` and no `E7`. The "first candidate run" receipt the row
   cites **does not exist in the lane**: `grep -rn "fails=E6,E7" .` over the whole repository returns three hits,
   all of them prose (`corpus/QUALITY.md:1100`, `corpus/lessons/round-85.md:53`, `plans/round-85.md:22`) and
   **zero receipt files** — the same grep over `.ufo/waves/round-85/` finds only `R85CriticClaims`'s unrelated
   `c2-reland` control. QUALITY 169's own pointer — "scoring in `.ufo/waves/round-85/` evidence" — names a
   directory in which no such scoring receipt exists. The claim the row makes is nonetheless true and now has a
   receipt: this seat's `01` reproduces `fails=E6,E7` at the prefreeze ground, and `02` shows the frozen
   predicate's own number (`fresh_sources=2`) printing only beside a FAIL. Note also that `claims.md` at the freeze
   points its "**Before**" line at `controls/receipts/c1-d0-donothing.txt` while the file on disk is
   `c2-d0-donothing.txt` — a broken pointer inside the frozen claims file itself.

2. **Drafted row 2 is not confirmable and is replaced.** `corpus/lessons/round-85.md:54` asserts the prefreeze
   "predicted a 9-quote, 7-row entry while the counter's E4 novelty rule rejects every quote the round-84 entry
   already carries, so only 7 quotes / 6 rows were reachable", citing "first candidate run `quotes=4/9`, `rows=7`".
   * The string `quotes=4/9` appears **nowhere in the repository** except in that lesson row itself — it is the row
     citing itself. There is no receipt of that run.
   * The "9 quotes" figure is not in the frozen claims either: at the freeze the predicate reads `rows= ≥ 7`,
     `located_quotes= ≥ 8`, `fresh_sources=2`; the number 9 first appears in QUALITY 169 (working-tree, not
     committed) and in the lesson row.
   * The E4 attribution is **refuted by the counter itself**. E4 excludes a quote that occurs in the normalized
     text of a base-list entry; the amended entry's seven quotes come from S215/S026/S024, none of which is
     quoted by the round-84 entry, so E4 never fires — the landing counter prints `fails=-`. And the amended
     ground reaches `rows=7 located_quotes=8` with `DEPTH_R85=PASS` rc 0 (receipt 04), so the floors were
     reachable and the count relaxation was a choice, not a ceiling.
   * Replaced by the `predicate-relaxed-to-the-artifact` row above, which is the same defect with a receipt.

**Counter output, before and after each fix** (all runs: `python3 -B corpus/evidence/round85/depth-r85.py --root
<tree>`, tree = `git archive 64803d33 | tar -x` with the named edit applied; scratch
`/fast/scratch/hyaku/chousa-r85/R85ScribeLesson`, reproducible via `receipts/00-fixture-construction.sh`):

```
# BEFORE — prefreeze ground. Fixture b1 = the landing tree with ONE edit: the entry's
#          source: line changed from 'S215, S026, S024' to 'S020, S023, S215'. All seven
#          quotes stay located (E3 passes), so only the GROUND rules can fire.  receipt 01
ENTRY provenance-recording-r85.md ok=no rows=6 quotes=7/7 fails=E6,E7
DEPTH_R85 entries=1 ok_entries=0 rows=6 located_quotes=7 fresh_sources=1
DEPTH_R85=FAIL
exit=1

# BEFORE — the frozen predicate's own number, fresh_sources=2, printed. Fixture b2 = the
#          landing tree with ONE edit: the source: line changed to 'S215, S026, S023'.
#          S023 is named but not FRESH for this entry.  receipt 02
ENTRY provenance-recording-r85.md ok=no rows=6 quotes=7/7 fails=E6,E7
DEPTH_R85 entries=1 ok_entries=0 rows=6 located_quotes=7 fresh_sources=2
DEPTH_R85=FAIL
exit=1

# AFTER — landing revision, amended ground (source: S215, S026, S024).  receipt 03
ENTRY provenance-recording-r85.md ok=yes rows=6 quotes=7/7 fails=-
DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3
DEPTH_R85=PASS
exit=0

# BEFORE for the second fix — the PREFREEZE floors (rows>=7, located_quotes>=8) on the amended
#                         ground: fixture b3 = the landing tree + one extra S215 quote (Q8) + one
#                         extra decision row.  receipt 04
ENTRY provenance-recording-r85.md ok=yes rows=7 quotes=8/8 fails=-
DEPTH_R85 entries=1 ok_entries=1 rows=7 located_quotes=8 fresh_sources=3
DEPTH_R85=PASS
exit=0
```

**E7 in isolation** (fixture b4, receipt 13) — making S023 FRESH for the entry by adding it to the S023 registry
row's `used-by`, and naming it on the `source:` line, removes E6 but not E7:

```
ENTRY provenance-recording-r85.md ok=no rows=6 quotes=7/7 fails=E7
DEPTH_R85 entries=1 ok_entries=0 rows=6 located_quotes=7 fresh_sources=3
DEPTH_R85=FAIL
exit=1
```

S023 is `source:`-cited by the base-list entry `search-transparency-reporting-r84.md`
(`corpus/evidence/round85/base-knowledge.txt:88`; that entry's `source: S214, S018, S023`), so E7 fires whatever
S023's freshness is — which is why the prefreeze ground could not be rescued by re-pointing the row.

The second pair is the fix's own demonstration: with one more located quote and one more decision row the amended
ground reaches the **prefreeze** floors and passes, so `rows= ≥ 7` / `located_quotes= ≥ 8` were satisfiable on the
ground the amendment adopted — the amendment lowered them to `≥ 6` / `≥ 7` anyway. `fresh_sources=2` (the frozen
predicate) is unreachable in the other direction: receipt 02 shows the counter printing `fresh_sources=2` and
failing, because E6 needs three FRESH ids on the `source:` line.

---

## considerthese

Read `considerthese/2026-11-07.md` and `considerthese/2026-11-06.md` (never edited).

**One still-unimplemented proposal: "One open Gate-record S-id per daily review"**
(`considerthese/2026-11-06.md`, still carried in the 2026-11-07 file's open-items list as "Twelve open Gate-record
defects from the r80 ScoutA survey still unopened"). **This round does not implement it.**

Evidence for the "not implemented" verdict (receipts 07 and 08):

- The twelve ids are `S170, S171, S173, S174, S175, S176, S178, S179, S182, S183, S191, S193`
  (`corpus/lessons/round-80.md:141`, the r80 ScoutA survey). `grep -l -E '^GATE-RECORD (S170|S171|S173|…|S193) '
  corpus/lessons/*.md` returns **no file**: none of the twelve carries a `GATE-RECORD` line in any committed
  lesson. They are not reachable by `tools/gate-records.py verify` at all, because the tool only reads lines whose
  first text is `GATE-RECORD`, and every lesson's `## Gate` block from round 80 onward is the four-column
  pipe-table form. The tool cannot substitute for the proposal's own method ("`git show <rev>:<path>`, re-count the
  quote, and report match/mismatch").
- Running the tool over every committed lesson — the one-command form the r83 lesson named — gives
  `GATE_RECORDS files=134 records=24 ok=24 fail=0` rc 0 (receipt 07): the sweep is clean, but its 24 records are
  the rounds 80–85 lessons, not the twelve backlog ids.
- No round-85 wave artifact touches any of the twelve ids (`grep -rn "S170\|S191\|S182" .ufo/waves/round-85/`
  returns only this seat's own receipt).

**Reason it was not done, and what would count as doing it.** The round's claim cap was spent on the two repairs
and the twelve-id drip has no carrier in the wave spec (the r83 lesson reached the same conclusion: "none of the
twelve remainder ids is a round-83 Gate record"). The proposal is not implemented by "the tool runs clean over the
lessons" — it asks for one backlog id per day, re-counted by hand at its cited revision, and the backlog ids are
invisible to the tool. A round that wants to close it should (a) give one seat one backlog id, (b) have that seat
run `git show <rev>:<path>` and re-count the quote, and (c) write the verdict as a receipt, which is what the
r80 ScoutA survey itself was. Until a backlog id is re-counted and receipted, the twelve stay open.

---

## Assimilation

**none.**

Reason, and the re-count: `merge/chousa/` is not present in this lane's tree — the merge package lives in a
sibling repository (`/home/vgpnk/Projects/shokuknow/merge/chousa`), and `SKILL.md` records no `merge/chousa` path
for this lane. Nothing was adopted, so no campaign bytes were read, no collision check was run, and no
re-grounding was performed. The standing id-drift evidence is unchanged from round 78:
`wc -l .ufo/waves/round-78/assimilation/collisions` → **111** lines, against 114 staged ids and 192 registry ids
(receipt 10) — the same three counts the r83 seat re-counted (`R83ScribeLesson/receipts/06-collisions.txt`), so
the id-drift question is still unresolved and still a candidate for a future round with a real §10 validation.

---

## Gate (addendum for the non-author spot-check)

The landing `## Gate` block carries three `GATE-RECORD` lines (S215, S026, S024), all `decision=admit`, and no
reject row. This addendum names **one admit and one reject (planned)** for the non-author spot-check, drawn from
that block, and records the verification each is checked with.

**Verification used.** `python3 -B tools/gate-records.py verify --root . corpus/lessons/round-85.md` →
three `OK` lines, exit 0 (receipt 05: `GATE_RECORDS files=1 records=3 ok=3 fail=0`, exit=0). The hand
"Location command" of rounds 81–82 is the whitespace-collapse locator; all three quotes locate `FOUND` in their
committed captures, exit 0, and their `wc -w` values are 12, 20 and 16 — matching each record's `words=` field
(receipt 06).

| # | record | spot-check decision | why | verification |
|---|---|---|---|---|
| A | `GATE-RECORD S215 url=https://www.w3.org/TR/prov-o/ fetched=2026-11-08T03:55:52Z tier=A decision=admit …` (`corpus/lessons/round-85.md:14`) | **admit** | tier `A` matches the S215 registry row; `capture_sha256=8c9aeabb466fb6d1…` is a prefix of the capture's own sha; the refetch row for `(S215, https://www.w3.org/TR/prov-o/, key 6e48bcc4…, 2026-11-08T03:55:52Z)` has `curl_rc=0` and `http=200`; the 12-word quote locates verbatim at `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt:779` | `GATE_RECORD …/round-85.md:14 S215 OK` (receipt 05); locator `FOUND`, `wc -w` = 12 (receipt 06) |
| R | `GATE-RECORD S033 url=https://www.w3.org/TR/prov-o/ fetched=2026-11-08T04:15:56Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none` | **reject (planned — not present in the landing block)** | the round-85 ledger holds a refused attempt on this URL that the Gate block does not record: `refetch.tsv` line 179, `S033 https://www.w3.org/TR/prov-o/ … 2026-11-08T04:15:56Z rc=22 http=403`. The tool accepts this row in unreach form and refuses to certify the URL as opened: `GATE_RECORD …:1 S033 OK` rc 0 | the tool accepts it, so a spot-check can run it unchanged (receipt 11) |

**On the landing block's "no new reject row".** The landing block says "Rejected this round (kept as a decision, no
registry row): none new — every candidate URL opened answered 200 and carried a locatable quote"
(`corpus/lessons/round-85.md:39-40`). **That sentence is not accurate as written, and the fix is a one-line
correction rather than a new registry row.** The round-85 ledger holds **three** non-200 rows after the freeze,
not zero: lines 175 and 176 (`S020 https://www.w3.org/TR/prov-o/`, `curl_rc=22`, `http=403`) and line 179
(`S033 https://www.w3.org/TR/prov-o/`, `curl_rc=22`, `http=403`) (receipt 09). All three are attempts on the
**alternate** PROV-O URL; the canonical `REC-prov-o-20130430` URL was **not** fetched at all this round — its only
three rows (lines 167–169) are round-84's, at `02:16:01Z`–`02:16:08Z`, before the freeze. So the block's other
sentence — "the canonical `REC-prov-o-20130430` URL answered HTTP 403 on three attempts in round 84 **and again
this round**" (`corpus/lessons/round-85.md:23-24`) — attributes to this round three attempts the ledger shows did
not happen. The honest wording is: *the alternate PROV-O URL was refused twice under S020 (lines 175–176) and once
under S033 (line 179), and succeeded on the third attempt under S215 (line 177); the canonical URL was not fetched
this round.*

**No new reject row is nevertheless the right call, for a different reason than the one stated.** The refusals
above are *attempt* failures on one URL that was then admitted under a new id (S215), not candidate sources that
were examined and turned down: no refused URL carries a capture, a quote, or a registry row change, so there is
nothing to reject as a source. The defect is in the block's *narration*, not in its row set: it claims a fetch
that did not occur and calls three 403 rows "none". A non-author should check the narration against
`refetch.tsv` lines 175–179 rather than against a new row.

**One further item for the spot-check, drawn from the same block.** The landing block's "Rejected this round …
none new" sentence and its canonical-URL sentence are the two claims a spot-check can most cheaply falsify, and
both are checkable from committed bytes alone (`awk -F'\t' 'NR>1 && $5>"2026-11-08T03:54:30Z"{print $1,$2,$5,$6,$7}'
corpus/evidence/round57/refetch.tsv` — receipt 09). Neither needs a fetch.

**Also for the spot-check, from the same block:** the S215 record's `fetched=2026-11-08T03:55:52Z` is the third
attempt on the alternate URL, and the two earlier attempts are filed under **S020** (lines 175–176) while the
third is filed under **S215** (line 177) — the same URL, three attempts, three different ids, one of them (S033,
line 179) after the success. The registry carries S020, S033 and S215 as three separate rows for one document.
The Gate block's per-id narrative does not mention this; a spot-check that wants to know which row owns the
alternate URL should read the ledger, not the block.
