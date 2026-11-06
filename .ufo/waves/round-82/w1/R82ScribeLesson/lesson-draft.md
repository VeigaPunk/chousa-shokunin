# Round 82 — question framing, and a gate that refuses the placeholder class (draft)

Lane `chousa`. Base `142b6f0c08e645ef9507f6d880be44e518c39043` (round-81 tip, closed `rejected-honest-stop`);
egress table `5d792e1e953649e801d9bf1f64093b1f0d4dac8c` (committed 2026-11-06T19:41:56Z, before the first row of
this round's fetches at 19:42:03Z); prefreeze instruments, fixtures and captures
`38f5af8268b2807811dded3d7d7221ff3f509495`; claim freeze `57c0d16795db97ed09b69034e335e725ce577285`; candidate
landing `b4a41d251b488f06b4a6ab01a11bc12ce72edd20` — the bytes every command below was run against. Drafted by
seat `R82ScribeLesson` (receipts under `.ufo/waves/round-82/w1/R82ScribeLesson/receipts/`). The seat used no
network, wrote nothing outside its wave folder and scratch, and measured no claim predicate. Sections
`## Claim outcomes` and `## Kill-rule outcomes` are the wave's and the L1's; they are not drafted here.

The round moves two surfaces: the gate (it must refuse the round-81 K2 forms and a declared placeholder class
through the unchanged SKILL.md item-2 and item-4 Run lines) and one knowledge entry on question framing. This draft
records only what the Gate section can show from committed bytes and what the mistake section can show from the
records.

## Gate

One record per registry row touched this round. `fetched` is the `refetch.tsv` time (UTC); `tier` is the registry
tier; each quote is located in the committed capture text of the row after whitespace collapse, at 1–25 words
(`wc -w`). All five fetches answered HTTP 200 with `curl_rc=0` (`corpus/evidence/round57/refetch.tsv:152-156`), and
every URL appears in `corpus/evidence/round82/egress-approval.md`'s intended-target table, written before the fetch.

```
GATE-RECORD S008 url=https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 fetched=2026-11-06T19:42:03Z tier=A decision=admit capture=corpus/captures/fd7eed5e0e6c64e22bc1470c.txt capture_sha256=598abc098b574159… words=18 quote="The review PICO (planned at the protocol stage) is the PICO on which eligibility of studies is based"
GATE-RECORD S209 url=https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question fetched=2026-11-06T19:42:05Z tier=A decision=admit capture=corpus/captures/213237301753814b95b24684.txt capture_sha256=8581ca1827f4ae13… words=20 quote="If changes are made, deviations from the protocol with supporting justification should be made transparent within the final scoping review"
GATE-RECORD S210 url=https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862687 fetched=2026-11-06T19:42:08Z tier=A decision=admit capture=corpus/captures/bcb4a695b2aa019305121cff.txt capture_sha256=fc857da335013077… words=17 quote="JBI suggests utilising the PCC (population, concept and context) approach to formulate review questions for scoping reviews."
GATE-RECORD S211 url=https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862707 fetched=2026-11-06T19:42:10Z tier=A decision=admit capture=corpus/captures/97223722748a928c3c6912b5.txt capture_sha256=b8b542d9a1d8feed… words=21 quote="each element of the PCC approach is broken down into a further description of what the review will include and exclude."
GATE-RECORD S028 url=https://www.crossref.org/services/crossmark/ fetched=2026-11-06T19:42:10Z tier=A decision=admit capture=corpus/captures/dedff231d5c3d3cdb0b4f8e3.txt capture_sha256=ad526ada8cc8f76d… words=16 quote="They commit to informing us if there is an update such as a correction or retraction"
```

**Location command** (one per record; `<key>` and `<quote>` are the record's `capture` file name and quote,
`wc -w` is run on the quote alone):

```sh
LOC='import sys;t=" ".join(open(sys.argv[1],encoding="utf-8",errors="replace").read().split());print("FOUND" if " ".join(sys.argv[2].split()) in t else "ABSENT")'
python3 -c "$LOC" corpus/captures/<key>.txt '<quote>'    # → FOUND, exit 0
printf '%s\n' '<quote>' | wc -w                         # → the words= value in the record
```

The five filled invocations and their outputs are in `receipts/01-gate-quote-locate.txt` at lines 6–11 (S008),
13–18 (S209), 20–25 (S210), 27–32 (S211), 34–39 (S028); all five print `FOUND`, rc 0, and the `wc -w` values are
18, 20, 17, 21, 16. The capture digests are full in `receipts/02-capture-sha-vs-refetch.txt:3-7`, where each equals
the `txt_sha256` cell of its 2026-11-06 `refetch.tsv` row (`MATCH` on all five, rc 0) — the bytes located are the
bytes that fetch stored.

- **Admit S008** (docs, A, opened 2026-10-19, re-opened this round). The chapter still divides the PICO into three
  stages at which it is fixed: the review PICO (the eligibility basis), the PICO for each synthesis, and the PICO
  of the included studies. The located sentence is the first of those; the entry's planned-vs-found rows (its Q1–Q3)
  rest on all three. The old anchor named "sections 2.1 rationale and 2.3 three PICO levels"; the new anchor names
  "2.1 Key Points and 2.3 (the three PICO stages …) as served 2026-11-06". **The new anchor misdescribes the page's
  structure** — see the drift note below; the `teaches` cell is unchanged and still warranted by 2.3.
- **Admit S209** (docs, A, opened 2026-11-06). The paragraph on protocol deviations: a protocol is fixed first, and
  a change made later is reported as a deviation with its justification in the final review. Grounds the entry's
  deviation row (its Q11). The slug/title question is decided below.
- **Admit S210** (docs, A, opened 2026-11-06). The paragraph run states the PCC frame for scoping questions, calls
  such a question broader and hypothesis-generating against a systematic review's hypothesis-testing, and names
  PICO/PECO as an alternative when the map precedes a systematic review. Grounds the entry's frame-choice rows
  (Q6–Q8); the "unclear question → incoherent review" sentence (Q9) is in the same capture.
- **Admit S211** (docs, A, opened 2026-11-06). The sentence at the eligibility section: each PCC element is broken
  down into what the review will include and exclude; the capture's `Population`, `Concept`, `Context` headings at
  lines 739–745 are the headings the anchor names. Grounds the eligibility row (Q10).
- **Admit S028** (docs, A, opened 2026-10-21, queued since round 21, re-opened this round). Crossref's "How Crossmark
  works" paragraph: members commit to inform Crossref of an update such as a correction or retraction. This row is
  mined into the **round-81** entry, which gained a round-82 addendum (`corpus/knowledge/correction-retraction-status-r81.md`
  lines 61–75, `source:` line now `S205, S206, S207, S028`; the addendum is absent at base: `git show 142b6f0c:…`
  prints 0 hits). Its two quoted lines both locate in the capture (`FOUND`, 15 and 19 words). The `never` clause in
  that addendum ("an absent button shows only that the publisher did not deposit the signal") is the lane's reading,
  and the addendum says so.

**Anchor drift (S008), found by this Gate and reported, not repaired.** The new anchor cell reads
"sections 2.1 Key Points and 2.3 …". In the capture the `Key Points:` box is at line 531, *before* the
`2.1 Rationale for well-formulated questions` heading at line 538; it is the chapter's key-points box, not a part of
section 2.1. The old anchor's `2.1 rationale` names a heading the page still carries (line 538), and the entry's
quoted sentences all sit under `2.3 Defining the scope of a review question` (heading line 556; Q1 at line 560).
No decision changes — 2.3 warrants the row — but the anchor cell should read "the chapter's Key Points box and
section 2.3", and a reader who searches "2.1 Key Points" finds no such section heading. Receipts:
`receipts/03-registry-diff.txt:55-93` (the `grep -n` and the 531–560 context window) and, for the row cells,
`receipts/03-registry-diff.txt:7-9`.

**Registry cell changes, old → new.** All from
`git diff 142b6f0c08e645ef9507f6d880be44e518c39043 b4a41d251b488f06b4a6ab01a11bc12ce72edd20 -- corpus/SOURCES.md`
(`--numstat` = `5 2 corpus/SOURCES.md`; the five insertions are the two rewritten rows and the three new rows,
`receipts/03-registry-diff.txt:3`). No other registry line changed.

| row | status | anchor | recheck | used-by |
|---|---|---|---|---|
| S008 | `queued` → `mined` | `sections 2.1 rationale and 2.3 three PICO levels; last updated August 2023, Handbook v6.5` → `sections 2.1 Key Points and 2.3 (the three PICO stages: review PICO, PICO for each synthesis, PICO of the included studies) as served 2026-11-06 (capture key fd7eed5e0e6c64e22bc1470c); Handbook v6.5` | `on-release` → `on-release` (unchanged) | `—` → `corpus/knowledge/question-framing-frames-r82.md` |
| S209 | — → `mined` | new: `the protocol paragraph on deviations, as served 2026-11-06 (capture key 213237301753814b95b24684)` | — → `on-release` | — → `corpus/knowledge/question-framing-frames-r82.md` |
| S210 | — → `mined` | new: `paragraphs on PCC, hypothesis-generating questions and PICO/PECO alternatives, as served 2026-11-06 (capture key bcb4a695b2aa019305121cff)` | — → `on-release` | — → `corpus/knowledge/question-framing-frames-r82.md` |
| S211 | — → `mined` | new: `opening paragraphs and the Population/Concept/Context headings, as served 2026-11-06 (capture key 97223722748a928c3c6912b5)` | — → `on-release` | — → `corpus/knowledge/question-framing-frames-r82.md` |
| S028 | `queued` → `mined` | `introductory text before Benefits of Crossmark` → `introductory text before Benefits of Crossmark and the How Crossmark works paragraph, as served 2026-11-06 (capture key dedff231d5c3d3cdb0b4f8e3)` | `180d` → `180d` (unchanged) | `—` → `corpus/knowledge/correction-retraction-status-r81.md` |

Base has zero rows `^| S20[9-9] ` or `^| S21[0-1] ` (`grep -c` prints 0, rc 1) and three at the landing
(`receipts/03-registry-diff.txt:15-19`).

**S209: the slug and the served title — admit, with the drift recorded.** The URL's slug is
`10.2.2+Developing+the+title+and+question`; the page's served title is `10.2.2 Developing your protocol` — the HTML
title (capture line 189), the content breadcrumb (line 715) and the h1 (line 733). The capture's navigation sidebar
also lists the sibling titles 10.2.1–10.2.12 (lines 495–583), 10.2.3 and 10.2.4 among them; the slug's "title and
question" wording is the only place that phrase survives. The page id (`355862667`) does not appear in the captured
text at all (0 hits), so the served title and the URL are the only identifiers a reader has.
Decision: **admit**. The slug is a creation-era Confluence slug; the document served under it is section 10.2.2 and
carries the deviation paragraph the row's `teaches` cell and the entry's Q11 rest on (20 words, `FOUND`). The
registry row already names both the served title and the slug in its title cell, so no correction is needed; a
future citation must use the served title. What would flip this to reject: the served page being a different
section, or the deviation paragraph being absent — neither holds (`receipts/04-s209-title-slug.txt:6-9`, `:18`,
`:47-52`).

**Reject-for-now: SPIDER and PRISMA-ScR (no registry row, nothing taught).** Both frames were named in the round's
ground recon as frames the entry could have treated; neither was opened. There is no registry row for either
(`grep -c -i spider corpus/SOURCES.md` → 0; `grep -c -i 'prisma-scr\|prisma scr'` → 0), no round-82 refetch row
(0), and none of the five round-82 captures carries either token (0/5). The entry rests on neither (0 hits).
SPIDER is worse than unopened here: the lane's SPIDER material is a **known-absent quote** — the round-29
control `ReviewFixtureAbsentEdits.md:40` records that `"SPIDER"`, `"spider"`, `"frame their questions"` have 0 hits
on the S008 page, and the round-82 S008 capture prints 0 as well. PRISMA-ScR occurs in committed knowledge only
inside a reference list (`japanese-search-record-r38.md:31`, the token sits inside `PRISMA-ScR` there); it is a
reporting checklist, not a rule for choosing or aligning a frame, and the entry's stated limit already excludes
reporting standards. **Flip:** a method document that states *when* SPIDER applies (or a PRISMA-ScR item that
states how the frame is chosen, not merely reported) is opened and its ≤25-word wording located; then it competes
for a row. Receipt: `receipts/05-unopened-candidates.txt`.

**What this Gate does not check.** The captures are trusted only as committed bytes matching their fetch record
(verified above); no live re-open was made — the seat's item names none, so no network was used. Whether each
located quote *grounds* the row it is cited for is the reviewer's question (C2/K3), not a substring test's. The
S008 anchor drift is logged, not repaired: the registry is frozen at the landing for this round.

## Mistakes

Mined this round: a seat described its own fixture's defect in words the fixture's bytes do not carry, and the
description was carried into the closure's count unchecked.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a record's stated defect form was never checked against the record's own cells: the description and the bytes disagree, and the gate's line cannot tell them apart | `.ufo/waves/round-81/w1/R81ReviewerC2/records/r4-07-alt-section.md`, F4-5 in `attack.md` §4, described as "the kept rejection (reason present, flip empty) sits in a section named `## Rejected sources`". The flip cell actually reads "a fixture that quoted a citation-searching standard verbatim would flip this rejection" (12 words), and `diff` against `corpus/evidence/round81/checklist-fixtures/item4-pass.md` shows exactly one changed line, the heading `## Rejections` → `## Rejected sources` (receipt `06-r4-07-description-vs-bytes.txt:5-17`). The closure counted it among "the eleven K2 records" (`corpus/lessons/round-81-verifier-spotcheck.md:103`; the count is the 6 F2 + 5 F4 rows of `attack.md`, receipt `07-described-form-check.txt:37-44`) | the round-82 prefreeze check, not the round-81 wave: `corpus/evidence/round82/claims.md` §Prefreeze discovery (line 19, committed at the freeze) and this seat's own re-measurement (`receipts/06-r4-07-description-vs-bytes.txt`, `receipts/07-described-form-check.txt`). The L1's helper `corpus/evidence/round82/mistake-r4-07.txt` carries the same probe but is **untracked** and absent from the landing (`git cat-file -e b4a41d25:…` → rc 128), so it is not cited as evidence | run the description against the bytes before it leaves the seat — `check-described-form.py <record> --reason present --flip absent` — and, when the described form does not exist, **build** it instead of describing the record into it. Round 82 did both: `r4-07b-alt-section-noflip.md` is the described form built from `item4-fail` with the heading renamed, and `r4-07` is a positive control (`c1-manifest.tsv:50`, `P4-alt-section-complete … REJECTIONS_OK=1/1`) |

**Why the round-81 gate output could not have caught it.** At `7e2da96a` the sweeps mode reads only the section
literally named `Rejections` (the mechanism `attack.md` §4 states, `SEC_BODY[Rejections]`); under `## Rejected sources`
it sees no row. The old gate therefore prints the
*identical* line for the complete rejection and for the empty-flip one:

```
$ bash "$S/tree-r81/tools/research-gate.sh" verify-sweeps <r4-07> --root "$S/tree-r81"
VERIFIED_SWEEPS=1/1 REJECTIONS_OK=0/0
RESEARCH_GATE: CLEAN (… rejections=0 rejections-ok=0 findings=0 drift=0)   rc=0
$ bash "$S/tree-r81/tools/research-gate.sh" verify-sweeps <r4-07b> --root "$S/tree-r81"
VERIFIED_SWEEPS=1/1 REJECTIONS_OK=0/0
RESEARCH_GATE: CLEAN (… rejections=0 rejections-ok=0 findings=0 drift=0)   rc=0
```

(`receipts/06-r4-07-description-vs-bytes.txt:31-42`.) The K2 firing stands — both records exited 0, so both were
valid fail controls — but the *mechanism* the seat stated was not in the bytes, and the only place the difference
appears is the cells. A wave that repeated the description would have carried a wrong mechanism into the freeze.

**The fix, shown able to fail.** The checker reads the kept-rejection table under any heading containing
"reject" (the convention the landed gate uses), and tests each described leg against the cell:

```
$ python3 .ufo/waves/round-82/w1/R82ScribeLesson/check-described-form.py \
    .ufo/waves/round-81/w1/R81ReviewerC2/records/r4-07-alt-section.md --reason present --flip absent
  id=R1 heading='## Rejected sources' reason_present=1 flip_present=1
  DESCRIBED-FORM OK id=R1 leg=reason described=present
  DESCRIBED-FORM MISMATCH id=R1 leg=flip described=absent bytes=present
DESCRIBED_FORM bad=1
RC=1
```

```
$ python3 …/check-described-form.py corpus/evidence/round82/c1-records/r4-07b-alt-section-noflip.md \
    --reason present --flip absent
  id=R1 heading='## Rejected sources' reason_present=1 flip_present=0
  DESCRIBED-FORM OK id=R1 leg=reason described=present
  DESCRIBED-FORM OK id=R1 leg=flip described=absent
DESCRIBED_FORM bad=0
RC=0
```

Both legs are in `receipts/07-described-form-check.txt:5-24`. The same description against the record's real cells
(`--flip present`) passes, which is the description the round-81 seat should have written (`receipts/07-described-form-check.txt:27-35`).

**What the round did about it.** The landed gate now distinguishes the two records: `r4-07` prints
`REJECTION id=R1 … reason=present flip=present observed=complete verdict=match` / `REJECTIONS_OK=1/1`, rc 0, and
`r4-07b` prints `flip=absent observed=incomplete` plus `FINDING SWEEP_REJECTION_INCOMPLETE … section=Rejected
sources` / `REJECTIONS_OK=0/1`, rc 1 (`receipts/06-r4-07-description-vs-bytes.txt:45-59`). The manifest assigns
`r4-07b` as `F4-5 … refuse SWEEP_REJECTION_INCOMPLETE` and `r4-07` as the positive control — the form the seat
described now exists as bytes of its own.

**Residual.** The round-81 verdict does not change: the record still exited 0 at `7e2da96a`, so it remains a K2
fail control. What was wrong is the description, and the closure's phrase "the eleven K2 records" now names one
whose stated mechanism is wrong. A later reader who checks the description against the bytes (as this seat did)
finds the described form absent; that is the failure this class produces.

## considerthese

Read: `considerthese/2026-11-06.md` (newest, cursor `f7449f9`) and `considerthese/2026-11-05.md` (cursor
`378fda8`); neither file was edited (`md5sum` in `receipts/08-considerthese.txt:7-9`). One still-unimplemented
proposal named:
**2026-11-06, "One open Gate-record S-id per daily review"** — pick one id from the ScoutA remainder (S170, S171,
S173–S176, S178, S179, S182, S183, S191, S193), `git show <rev>:<path>`, re-count the quote, report
match/mismatch.

**Not implemented this round.** Evidence: excluding one fleet-wide grep artifact, the twelve ids occur 0 times in
round-82 material (`receipts/08-considerthese.txt:12-19`); that artifact's single S183 hit is a sibling lane's id
(`mado-shokunin/corpus/knowledge/mutation-testing-r28.md:34`, quoted in
`R82ConnectorSiblings/scan-method-vocab-siblings.txt:60`), not a chousa Gate record. `corpus/lessons/round-82.md`
does not exist (`ls` → `No such file or directory`, rc 2), and
`git diff --name-only 142b6f0c b4a41d25 | grep -E 'considerthese|lessons'` prints nothing. Reason: the frozen
claims bind the round to C1/C2; this seat's item fixes its Gate to the round's own five rows; and the proposal is a
daily-review habit of the reflection bot, which a leaf scribe can draft but cannot land. The 2026-11-06 file's first
proposal ("keep a proposal→adoption ledger") is **not** the open one: a ledger exists
(`corpus/evidence/round54/considerthese-ledger.tsv`, 35 rows, last `CT-20261026-4`), though it has no row for either
2026-11-05/06 proposal (0 hits for `CT-2026110[56]`).

## Assimilation

**none.** Reason: `merge/chousa` id collisions were measured in round 78 and nothing has renumbered them.
Re-count at `b4a41d25`: `.ufo/waves/round-78/assimilation/collisions` has **111** lines against **114** staged ids
(`wc -l`, `receipts/09-collisions.txt:3-9`, rc 0); `reg-ids` is still 192 and the live registry now has 211 rows
(`grep -c '^| S[0-9]' corpus/SOURCES.md`). The file's last commit is `3eb4a3ca` (2026-11-04), so these are the same
bytes round 81 counted. No package bytes read, no campaign tool run, no shokuknow write.

## Appendix — receipts for this draft (integrator scaffolding, not part of the lesson)

| # | file | what it shows |
|---|---|---|
| 01 | `receipts/01-gate-quote-locate.txt` | five locator invocations, `FOUND` rc 0, `wc -w` = 18/20/17/21/16 |
| 02 | `receipts/02-capture-sha-vs-refetch.txt` | five capture sha256 = their `refetch.tsv` `txt_sha256`, `MATCH` |
| 03 | `receipts/03-registry-diff.txt` | `--numstat` 5/2, both rewritten rows, three new rows, full diff |
| 04 | `receipts/04-s209-title-slug.txt` | S209 served title vs slug, page-id absence, S210/S211 page-id absence |
| 05 | `receipts/05-unopened-candidates.txt` | SPIDER / PRISMA-ScR: no row, no fetch, no capture, absent-quote history |
| 06 | `receipts/06-r4-07-description-vs-bytes.txt` | r4-07 diff and flip cell; old gate identical on both records; landed gate differs |
| 07 | `receipts/07-described-form-check.txt` | checker failing on the stated form, passing on the built one, eleven-count |
| 08 | `receipts/08-considerthese.txt` | files read and digests, twelve-id absence, lessons file absent, ledger state |
| 09 | `receipts/09-collisions.txt` | 111 collisions / 114 staged / 192 reg-ids / 211 registry rows |
| — | `check-described-form.py` | the described-form checker used in §Mistakes |
