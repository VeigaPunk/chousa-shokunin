# Round 81 — two knowledge entries on research-method ground, and three checklist items that carry a command

Lane `chousa`. Base `378fda82dc2cbcc555a0565052cc408121813cef` (round-80 tip, closed
`rejected-honest-stop`); prefreeze controls `f7929f877e6fd54f4dc5ce7f993da46bc7df43f9`; claims frozen at
`bb54e7f89da9ba4213aec9d976c13f3f4ba548fb` (`corpus/evidence/round81/claims.md`); candidate landing
`7e2da96a0541946e796384d42fea18e09ede9e9f` — the bytes measured below. **This file is a draft by seat
`R81ScribeLesson`; it is not landed.** Every number was re-measured on 2026-11-06 against `7e2da96a` or
against committed capture bytes at that revision; each measurement names its command and its receipt under
`.ufo/waves/round-81/w1/R81ScribeLesson/receipts/`.

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
- **Admit S204** (docs, A, opened 2026-11-06). A second, independent methods guide that splits citation
  searching the same way and names where forward links live (citation indexes). Grounds the entry's
  "combine two indexes" row and the definition of what an index holds.
- **Admit S205** (docs, A, opened 2026-11-06). PubMed's own description of linked notices: an erratum is
  linked to the corrected article's citation, and a retracted article carries the `Retracted Publication`
  publication type. Grounds the status-check rows; the negative-sweep rule in the entry's decision table
  is the entry's own inference (its `Inference` section says so), not S205's.
- **Admit S206** (spec, A, opened 2026-11-06). ICMJE's version-control paragraph: prior versions archived,
  earlier electronic versions marked as superseded. Grounds the "cite the version read" row.
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

**Locating query.** `web_search(TARCiS statement citation searching Hirt BMJ 2024 PMC full text)`, one
search, `history://ChousaR81:134` (L1 session transcript). No committed file records the query; the
egress table (`corpus/evidence/round81/egress-approval.md:21`) requires it in the lesson `## Gate`, so
this line is the record and the landing author should keep it (or land the query beside the row).
`receipts/10-search-query-and-knowledge-delta.txt:2-3`.

**What this Gate does not check.** The five captures are trusted only as committed bytes matching their
fetch record; K2 (a live re-open of every counted quote) was not run by this seat — the seat's item names
no re-open, so no network was used. S208's "a correction exists, of a small error in recommendation 5"
rests on the search-result snippet the entry's `Version caveat` records, not on a read page. Whether each
located quote *grounds* the decision-table row it is cited for is K3's question (reviewer), not a
substring test's.

## Claim outcomes (measured at the landing revision)

| claim / axis | frozen predicate | measured at `7e2da96a` | receipt |
|---|---|---|---|
| C1 depth | `DEPTH_R81=PASS`, rc 0, entries ≥ 2 | `DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14` / `DEPTH_R81=PASS` / `RC=0` | `receipts/02-c1-depth-landing.txt:6-8` |
| C2 operability | `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS`, rc 0 | `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` / `CHECKLIST=PASS` / `RC=0` | `receipts/03-c2-checklist-landing.txt:9-11` |

Commands (tree = `git archive 7e2da96a | tar -x -C <scratch>`, then from that tree):

```sh
python3 -B corpus/evidence/round81/depth-r81.py --root "$D"        # rc 0
python3 -B corpus/evidence/round81/checklist-run.py --root "$D"    # rc 0
```

C1's counter counts two entries: `citation-searching-tarcis-r81.md` and
`correction-retraction-status-r81.md`; the knowledge set is 92 files at base and 94 at the landing
(`git ls-tree -r … corpus/knowledge | wc -l`, `receipts/10-search-query-and-knowledge-delta.txt:5-7`).
C2's counter reports every item runnable and the three new legs discriminating (`item2-pass.md:rc=0:ok,
item2-fail.md:rc=1:ok`; `item4-…`; `item5-fail.tsv:rc=1:ok`). The frozen before-state
(`controls/c1-k0-donothing.txt` `entries=0 … FAIL rc=1`; `controls/c2-k0-donothing.txt`
`3/6 DISCRIMINATE=0/3 FAIL rc=1`) is quoted from `claims.md`, **not re-run**: `run-controls.sh` writes
under `corpus/evidence/round81/controls/`, outside this seat's write scope.

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

## What this draft does not do

- It is not landed and touches no production file; it is a leaf seat's draft.
- K2 (live re-open of counted quotes) and K3 (decision-table contradiction) were not exercised here. K2
  needs one GET per HTML row plus `pdftotext` for S203; this seat's item names no re-open, so no network
  was used.
- The five captures are trusted as committed bytes whose sha256 equals their fetch record; whether the
  hosts still serve those bytes is untested.
- The do-nothing and forgery controls were not re-run (their receipts live under
  `corpus/evidence/round81/controls/`, outside this seat's write scope); the frozen before-state is
  quoted from `claims.md`.
- No domain judgment beyond quote location: whether a located quote grounds the decision-table row it is
  cited for is the reviewer's K3, and whether the two entries are wise is the closure's judgment.
- The `## Gate` search query is recorded from the L1 session transcript, not from a committed path.
