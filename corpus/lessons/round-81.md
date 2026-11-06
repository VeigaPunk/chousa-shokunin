# Round 81 — two knowledge entries on research-method ground, and three checklist items that carry a command

Lane `chousa`. Base `378fda82dc2cbcc555a0565052cc408121813cef` (round-80 tip, closed
`rejected-honest-stop`); prefreeze controls `f7929f877e6fd54f4dc5ce7f993da46bc7df43f9`; claims frozen at
`bb54e7f89da9ba4213aec9d976c13f3f4ba548fb` (`corpus/evidence/round81/claims.md`); candidate landing
`7e2da96a0541946e796384d42fea18e09ede9e9f` — the bytes the claims were scored on. Drafted by seat
`R81ScribeLesson` (receipts under `.ufo/waves/round-81/w1/R81ScribeLesson/receipts/`), integrated and landed by the
L1 with the wave's findings, kill-rule outcomes and the post-scoring corrections added. Both claims are honest
stops (see `## Kill-rule outcomes`).

The round leaves the lane's own battery surface. C1 changes what the lane *knows* (two entries on
citation searching and on correction/retraction status, grounded on registry rows opened this round);
C2 changes what the lane can *run* (checklist items 2, 4 and 5 gain `Run:` lines that discriminate).
S208, the BMJ correction, is kept as a rejected row: the host answered 403.

## Gate

One record per new registry row. `fetched` is the `refetch.tsv` time (UTC) and the registry `opened`
date; `tier` is the registry tier; each quote is located in the committed capture text of the row after
whitespace collapse, at 1–25 words (`wc -w`).

```
GATE-RECORD S203 url=https://eprints.whiterose.ac.uk/id/eprint/214348/8/Hirt_etal_BMJ_Guidances_On_Terminology_AAM.pdf fetched=2026-11-06T18:44:29Z tier=A decision=admit capture=corpus/captures/f2489455cc311a4de981e926.txt capture_sha256=31493aa66bfd6625… words=13 quote="Backward and forward citation searching are known as direct citation searching (Figure 1)."
GATE-RECORD S204 url=https://pmc.ncbi.nlm.nih.gov/articles/PMC11386270/ fetched=2026-11-06T18:44:29Z tier=A decision=admit capture=corpus/captures/c52a1f15884a78028febcf43.txt capture_sha256=b905aae1afc0b798… words=15 quote="Citation indexes are bibliographic databases that record citations in addition to the usual article record."
GATE-RECORD S205 url=https://www.nlm.nih.gov/bsd/policy/errata.html fetched=2026-11-06T18:44:30Z tier=A decision=admit capture=corpus/captures/371c55117727d526805f030d.txt capture_sha256=08b4b3c0ad9215b0… words=13 quote="the erratum notice is simply linked to the citation for the corrected article."
GATE-RECORD S206 url=https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html fetched=2026-11-06T18:44:30Z tier=A decision=admit capture=corpus/captures/f221c90f69188f775e32cd34.txt capture_sha256=e1251d472cd517b5… words=10 quote="The journal should archive all prior versions of the article."
GATE-RECORD S207 url=https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/ fetched=2026-11-06T18:44:31Z tier=A decision=admit capture=corpus/captures/43a45b49723f7677d6446c92.txt capture_sha256=72a5a93d456ee798… words=25 quote="Some other update types, such as expressions of concern and corrections, are also included in the data, but these are not as comprehensive as retractions."
GATE-RECORD S208 url=https://www.bmj.com/content/387/bmj.q2458.full.txt fetched=2026-11-06T18:44:31Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
```

**Location command** (one per admitted row; `<key>` and `<quote>` are the record's `capture` file name and
quote, `wc -w` is run on the quote alone):

```sh
LOC='import sys;t=" ".join(open(sys.argv[1],encoding="utf-8",errors="replace").read().split());print("FOUND" if " ".join(sys.argv[2].split()) in t else "ABSENT")'
python3 -c "$LOC" corpus/captures/<key>.txt '<quote>'    # → FOUND, exit 0
printf '%s\n' '<quote>' | wc -w                         # → the words= value in the record
```

The five filled invocations and their outputs are in `receipts/01-gate-quote-locate.txt` at lines
3–4 (S203), 7–8 (S204), 11–12 (S205), 15–16 (S206), 19–20 (S207); all five print `FOUND` and exit 0.
The capture digests are full in `receipts/08-capture-sha.txt:3-7`, where each equals the `txt_sha256`
cell of its 2026-11-06 `refetch.tsv` row (`MATCH` on all five, rc 0) — the bytes located are the bytes
that fetch stored. A self-check re-parses these six records and re-derives every field from
`refetch.tsv` and the capture files: `GATE_RECORDS=6 bad=0`, rc 0
(`receipts/11-draft-gate-selfcheck.txt`).

- **Admit S203** (paper, A, opened 2026-11-06). The accepted manuscript of the TARCiS statement; the
  located sentence is the terminology the entry's first table rows rest on (backward = seed's references,
  forward = what cites the seed); the entry quotes six further recommendation lines from the same
  capture (the depth counter locates every quote line in both entries: `located_quotes=14`, receipt
  `02-c1-depth-landing.txt:6`). It is **not** the version of record: the entry says so and cites no
  recommendation-5 wording, because the correction (S208) could not be read.
- **Admit S204** (docs, A, opened 2026-11-06). A methods guide that splits citation searching the same way and
  names where forward links live (citation indexes). It is **not independent** of S203: its citation-searching
  passage cites Hirt et al. 2024 (`R81ReviewerEntries.md` item 2); it grounds the definition of what an index holds,
  not the "combine two indexes" row (that is S203 recommendation 6). Tier A is soft for a secondary guide
  (reviewer item 8).
- **Admit S205** (docs, A, opened 2026-11-06). PubMed's own description of linked notices: an erratum is
  linked to the corrected article's citation, and a retracted article carries the `Retracted Publication`
  publication type. Grounds the status-check rows; the negative-sweep rule in the entry's decision table
  is the entry's own inference (its `Inference` section says so), not S205's.
- **Admit S206** (spec, A, opened 2026-11-06). ICMJE's version-control paragraph: prior versions archived,
  earlier electronic versions marked as superseded. Grounds the version row — which, as landed, contradicted the same passage's next sentence "The citation should be to the most recent version." (capture line 222; reviewer K3 finding, corrected after scoring).
- **Admit S207** (docs, A, opened 2026-11-06). Crossref's statement of what the Retraction Watch data
  cover and how completely: updated every working day; expressions of concern and corrections are
  included but less comprehensively than retractions. The located quote is **25 words**, exactly the
  predicate's upper bound (1–25 inclusive); the depth counter counted it (`located_quotes=14` includes
  it), and a future edit that lengthens the sentence by one word would drop the row from P2.
- **Reject S208** (paper, A, opened 2026-11-06). The TARCiS correction, BMJ 2024;387:q2458. The fetch
  answered `curl rc 22, HTTP 403` at 2026-11-06T18:44:31Z (`refetch.tsv:151`, `receipts/04-s208-unreachable.txt:3`);
  no capture was stored (`ls corpus/captures/5802b641e7092ed5c07e36e4.txt` → `No such file or directory`,
  rc 2, same receipt lines 16–17), so no quote exists and nothing is taught from it. This is unreachability,
  not fabrication. **Flip condition** (registry cell, receipt line 10): a readable copy of the correction
  (publisher page or an index record carrying its text) is opened and its recommendation-5 wording located.

**Registry cell changes, old → new.** All six rows are new at the landing (base has zero rows
`^| S20[3-8] `: `grep -c` prints 0, rc 1; `git diff --stat 378fda82..7e2da96a -- corpus/SOURCES.md` is
`6 ++++++`, 0 deletions — `receipts/05-registry-cells.txt:3-7`). No existing row's cell changed.

| row | status | recheck | used-by |
|---|---|---|---|
| S203 | — → `mined` | — → `365d` | — → `corpus/knowledge/citation-searching-tarcis-r81.md` |
| S204 | — → `mined` | — → `365d` | — → `corpus/knowledge/citation-searching-tarcis-r81.md` |
| S205 | — → `mined` | — → `365d` | — → `corpus/knowledge/correction-retraction-status-r81.md` |
| S206 | — → `mined` | — → `365d` | — → `corpus/knowledge/correction-retraction-status-r81.md` |
| S207 | — → `mined` | — → `365d` | — → `corpus/knowledge/correction-retraction-status-r81.md` |
| S208 | — → `rejected` | — → `30d` | — → `—` (unchanged: nothing uses a rejected row) |

**Locating query (the record the egress table requires).** One `web_search`, query
`TARCiS statement citation searching Hirt BMJ 2024 PMC full text`, 2026-11-06 (L1 session). Chosen URLs: S203's
White Rose PDF and S208's BMJ correction. The correction's existence rests only on the search-result text for
`https://www.bmj.com/content/387/bmj.q2458.full.txt`, recorded here verbatim as returned: "In this paper by Hirt and
colleagues (*BMJ* 2024;385:e078384, doi:10.1136/bmj-2023-078384, published 9 May 2024), a small error in
recommendation 5 of the TARCiS statement has been corrected." This is a search snippet, not an opened page; it is
the warrant (tier C, unverified) for the entry's version caveat and nothing else.

**What this Gate does not check.** The five captures are trusted only as committed bytes matching their
fetch record; K2 (a live re-open of every counted quote) was not run by this seat — the seat's item names
no re-open, so no network was used. S208's "a correction exists, of a small error in recommendation 5"
rests on the search-result snippet the entry's `Version caveat` records, not on a read page. Whether each
located quote *grounds* the decision-table row it is cited for is K3's question (reviewer), not a
substring test's.

## Claim outcomes (measured at the landing revision `7e2da96a`)

| claim / axis | frozen predicate | measured | kill rules | verdict |
|---|---|---|---|---|
| C1 depth | `DEPTH_R81=PASS`, rc 0 | `DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14`, rc 0 (`R81ExecRepro`, `R81ScribeLesson/receipts/02-c1-depth-landing.txt`); base rc 1 | K1 held; K2 held (14/14 live re-opens present, `R81ExecReopen.md`); K3 contested — fires on its spirit, not its letter (below) | **honest stop** — predicate met, but the counter is not a depth measure: two 10-line filler entries with one-word quotes print `DEPTH_R81=PASS` (`R81CriticClaims/receipts/r09-c1-filler-entries.txt`), the §9 cheapest control the freeze omitted |
| C2 operability | `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, rc 0 | reproduced, rc 0; base `3/6 0/3` rc 1 | **K2 fired** (`R81ReviewerC2/attack.md`, `R81ExecRepro/c2-k2/`, `R81CriticClaims.md`, `R81ExecTrial.md`) | **falsified by its own kill rule — honest stop** |

## Kill-rule outcomes (frozen before data; reported, never repaired)

- **C1 K3.** `R81ReviewerEntries.md` item 1: the correction entry's "newer article version" row said *cite the version
  read*; S206 capture line 222 says "The citation should be to the most recent version." The entry's two located S206
  quotes (lines 218, 220) do not themselves contradict the row; the frozen K3 names "its cited located quote", so on
  its letter K3 holds, while the row did contradict its cited source. The L1 (author) does not claim the letter:
  the row was wrong, and C1 is reported as an honest stop on that and on the filler control together.
- **C2 K2.** The landed item-4 line exits 0 on a kept rejection whose flip cell is `-`, `n/a`, `none` or `TBD`
  (the gate reads any non-empty cell as present), and the item-2 line exits 0 on a negative claim naming a sweep id no
  row declares, a header-only `## Sweeps`, or a `where` of `n/a` (read as a zero-hit local glob). Six item-2 and five
  item-4 records, `R81ReviewerC2/attack.md`. Each is the item text's own defect in a named form.
- **Counter limits (mutation, `R81MutationCounters.md`):** 12/18 C1 and 9/17 C2 single-clause mutants survive the frozen
  controls; the P4 shared-quote branch is unexercised (d15); `CHECKLIST=PASS` beside `CHECKLIST_RUN=5/6` survives (c09).

## Post-scoring corrections (quality repairs; no verdict changes)

Landed after the wave, measured against the scored bytes, never offered as a claim result:
- `corpus/knowledge/correction-retraction-status-r81.md`: the version row now cites the most recent version (S206
  line 222 quoted); the erratum quote's antecedent condition is restated (reviewer items 1, 6).
- `corpus/knowledge/citation-searching-tarcis-r81.md`: S204 no longer called independent; the two-index row's warrant
  is S203 rec 6 only; "run" softened to "consider" for recs 2/8 as the source words them; the rec-5 row names the
  search snippet recorded in `## Gate` (reviewer items 2–5).
- `SKILL.md` items 2 and 4: the Run lines' prose names the K2 forms they pass, so the checklist stops overstating.
- `corpus/README.md`: a round-81 coverage section — the landing had left the lane's own G02 knowledge-index gate
  failing (`R81ScoutNovelty.md` F3: base PASS 91, landing FAIL 2 unindexed). Restored.
- Novelty honesty (`R81ScoutNovelty.md` §1.4): base row S120's capture already cited TARCiS and a MECIR errata/retraction
  check; the ground was in the corpus, not in an entry.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a draw's prose label drifted from the verdict its committed receipt prints — the label is a claim about the receipt, and nothing compared them | `corpus/lessons/round-80-verifier-spotcheck.md:27` and `:73`: the report prose orders the two v7 draws as "run1 PASS, run2 FAIL"; the receipts carry the opposite — `.ufo/waves/round-80/w1/R80ExecA/r80a-after-v7-run1.txt:216` = `BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=1/2 fresh_forgers=1/2 oracles_rejected=5/5`, `.ufo/waves/round-80/w1/R80ExecA/r80d-v7-run2.txt:216` = `BATTERY=PASS … fresh_positive=2/2 fresh_forgers=2/2`; both files are committed at `7e2da96a` (`git cat-file -e` exits 0) | the non-author closure at `378fda82` (round-80 spot-check), not the round; the receipts were right and the sentence citing them was not | cite a draw by receipt path, and let a counter compare the stated label to the printed `BATTERY=` verdict: `python3 -B .ufo/waves/round-81/w1/R81ScribeLesson/check-draw-labels.py LABELS.tsv` (`label<TAB>receipt<TAB>PASS\|FAIL`; exit 0 iff all match) |

The fix, shown able to fail. Run with the prose labels (run1 PASS, run2 FAIL):

```
DRAW-LABEL MISMATCH label=run1 receipt=.ufo/waves/round-80/w1/R80ExecA/r80a-after-v7-run1.txt stated=PASS actual=FAIL
DRAW-LABEL MISMATCH label=run2 receipt=.ufo/waves/round-80/w1/R80ExecA/r80d-v7-run2.txt stated=FAIL actual=PASS
DRAW_LABELS bad=2
RC=1
```

and with the receipt-true labels (run1 FAIL, run2 PASS):

```
DRAW-LABEL OK label=run1 receipt=.ufo/waves/round-80/w1/R80ExecA/r80a-after-v7-run1.txt verdict=FAIL
DRAW-LABEL OK label=run2 receipt=.ufo/waves/round-80/w1/R80ExecA/r80d-v7-run2.txt verdict=PASS
DRAW_LABELS bad=0
RC=0
```

Full receipt `receipts/07-draw-label-fix.txt:3-6` (failing) and `:9-12` (passing); the checker is
`.ufo/waves/round-81/w1/R81ScribeLesson/check-draw-labels.py` and the two label files are
`labels-bad.tsv` / `labels-good.tsv` beside it. The class recurs because a draw's verdict is already one
greppable line: the check costs one comparison, and the round-80 receipts would have carried the prose
labels out of the door otherwise.

### Round-81 mistakes (L1)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| the freeze omitted the cheapest passing forger for both claims: a filler entry (C1) and fixture-keyed Run lines (C2) | `R81CriticClaims/receipts/r09-c1-filler-entries.txt` (two 10-line entries, one-word quotes, `DEPTH_R81=PASS`); `R81CriticClaims.md` C2 (base + three fixture-keyed lines → `CHECKLIST=PASS`) | dispatch §9 "build the cheapest control that skips the claimed work"; the freeze built forgers of the *grounding* (ids, dates, bytes) but none of the *content* | QUALITY 162: a counter's control set includes a minimal-content forger; shown able to fail — the r81 counter prints PASS on `r09`, so the criterion's check fails on this round's own control set |
| a candidate Run line was positive-controlled only on the fixture pair the L1 wrote, not on the item text's own defect forms | pre-landing probe `corpus/evidence/round81/negA-probe.md`: `verify-sweeps` alone rc 0 on a negative claim with no sweep (`R81ScribeR80Defects/receipts/01-negA-verify-sweeps-alone.txt`); after the composite line, the wave still found six item-2 and five item-4 forms rc 0 (`R81ReviewerC2/attack.md`) | frozen C2 K2 — it fired | QUALITY 161 (defect-form controls) and 162; shown able to fail: the landed item-4 line exits 0 on `flip=-` (`R81ExecRepro/c2-k2/item4-flip-dash.txt`) |
| external fetches ran before the round's approval table was written, and the table's seat row cannot be satisfied as written | `refetch.tsv` rows 18:44:29Z–18:44:31Z vs `egress-approval.md` commit 18:47:58Z (`R81SentinelScope.md` S1); seat row mandates `capture-fetch.py` while forbidding its writes (S2, inherited from round 57) | `SKILL.md` Boundaries ("a window without an approval table is loopback-only"); nothing mechanical | write and commit the approval table before the first GET; a seat row names `quote-reopen.py` or a single curl GET into scratch only. Shown able to fail: `git log -1 --format=%cI f7929f87` (18:47:58Z) is later than every 2026-11-06 `refetch.tsv` time |

## considerthese

Read: `considerthese/2026-11-05.md` (cursor `378fda8`) and `considerthese/2026-11-06.md` (cursor
`f7449f9`); neither file was edited. One still-unimplemented proposal named:
**2026-11-06, "One open Gate-record S-id per daily review"** — pick one id from the ScoutA remainder
(S170, S171, S173–S176, S178, S179, S182, S183, S191, S193), `git show <rev>:<path>`, re-count the
quote, report match/mismatch.

**Not implemented this round.** Evidence: the twelve ids appear nowhere in the round's evidence or wave
outside this seat's own folder. The unfiltered `grep -rn` matched three lines, all inside this draft and
its receipt (`receipts/09-considerthese-check.txt:50-54`); with `--exclude-dir=R81ScribeLesson` it prints
`0` (same receipt `:55-57`). `git diff --stat 378fda8..7e2da96a` touches `SKILL.md`,
`corpus/SOURCES.md`, the two entries, the captures/refetch and round-81 evidence, and no lesson
(`:2-49`); `corpus/lessons/round-81.md` does not exist (`ls` → `No such file or directory`, rc 2,
`:60-62`). Reason: the frozen claims bind
this round to C1/C2; the wave's only defect seat drafts corrections to the round-80 spot-check's §6 items
(a different list — six routed defects, not the twelve Gate-record ids); and this seat is a leaf scribe,
which can draft but not land a daily-review habit. This Gate section re-opens only the round's six **new**
rows, each against its own capture — the same method, applied to a different list.

## Assimilation

**none.** Reason: `merge/chousa` id collisions were measured in round 78 and nothing has renumbered
them. Re-count at `7e2da96a`: `.ufo/waves/round-78/assimilation/collisions` has **111** lines against
**114** staged ids (`wc -l`, `receipts/06-collisions.txt:3-5`, rc 0); the live registry list has 192 ids.
No `merge` directory exists under the fleet root at depth ≤ 4 (`find … -maxdepth 4 -type d -name merge | wc -l`
→ `0`, `receipts/09-considerthese-check.txt:63-64`), so there is no package to read. No package bytes
read into the lane, no campaign tool run, no shokuknow write.

## Limits of this record

- K2 (C1) was exercised by `R81ExecReopen` (14/14 present live; the S203 PDF byte-identical to its capture); K3 by
  `R81ReviewerEntries`. Whether the entries are wise is the closure's judgment, not a counter's.
- The captures are trusted as committed bytes matching their fetch record and, on 2026-11-06, the live hosts.
- The `## Gate` search query and snippet are recorded from the L1 session, not from a committed fetch.
