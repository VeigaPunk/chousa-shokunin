# R82ScoutNovelty — per-surface recon for C2 K4 (ground already held) and the frontier

Seat: `R82ScoutNovelty` (leaf, read-only; no lane or fleet git/jj mutation, no production edits).
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scratch (deleted at end of seat): `/fast/scratch/hyaku/chousa-r82/R82ScoutNovelty/`.
Receipts: `.ufo/waves/round-82/w1/R82ScoutNovelty/receipts/` (each `.out` file is the recorded output
of the `.txt` command file next to it).

Revisions read:
- base `142b6f0c08e645ef9507f6d880be44e518c39043` (round-81 tip)
- egress `5d792e1e953649e801d9bf1f64093b1f0d4dac8c`, prefreeze `38f5af8268b2807811dded3d7d7221ff3f509495`
- freeze `57c0d16795db97ed09b69034e335e725ce577285`
- landing `b4a41d251b488f06b4a6ab01a11bc12ce72edd20` (the bytes under attack)
- tip `46dd1dc31e55c5a9133a0da47e22f8b598946cf1` (after receipts)

No network fetch was made: no item in this seat names a re-open, and the egress table
(`corpus/evidence/round82/egress-approval.md`) permits a seat GET only for a URL its wave item names.
Every read below is from committed bytes.

---

## 1. C2 K4 — does any BASE entry already hold a decision table / decision list on choosing or aligning a review question frame?

**Answer: no. K4 does not fire.** The ground was not already held at base.

### 1.1 The frozen grep — every hit, judged

Command (receipt `r01-base-frame-grep.txt` / `.out`):

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -i -E \
  'PICO|PCC|PECO|SPIDER|question fram|answerable question|eligibility criteri|protocol deviation|review question' \
  142b6f0c08e645ef9507f6d880be44e518c39043 -- corpus/knowledge corpus/README.md SKILL.md PROVINCE.md
```

Observed exit 0, seven hits in six files. Judgement per hit:

| # | Base location | Line (quoted) | Judgement |
|---|---|---|---|
| 1 | `PROVINCE.md:5` | `**Owns:** question framing; source hierarchy (primary / secondary / aggregator /` | **adjacent** — a province-ownership declaration naming the topic; no frame choices, no rows. |
| 2 | `SKILL.md:3` | `description: "Deep-research method (調査) — question framing, source hierarchy, citation chaining, claim-vs-source verification. …` | **adjacent** — front-matter trigger list naming the topic. |
| 3 | `SKILL.md:17` | `\| Research a question \| question framing → source hierarchy → chain → claim check \| starting from a search box with no question \| a research record with a declared question \|` | **adjacent** — the lane's own intent table row. It orders the lane's *method steps* ("question framing → source hierarchy → …") and forbids "starting from a search box with no question". It names no frame (no PICO level, no PCC, no eligibility alignment) and decides nothing about choosing one. |
| 4 | `corpus/knowledge/archived-export-intake.md:89` | `\| CL-07 \| inference \| general \| export-unverified \| SKILL.md:17 \| \| answer to the question, YES in part, the archive alone supports reusable research-method claims about FORM, question framing before search CL-02, hedged negatives as corrective labels CL-03, …` | **adjacent** — this is the near neighbour claims.md names. It names "question framing before search" as one *label* inside an archive's claim list; it holds no decision rows and no frame-choice list. Its `## Question` (lines 24–34) asks whether three archived exports support reusable method *claims*, not how to frame a question. |
| 5 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md:15` | `- **1.文献研究的质量控制: what the instrument requires of a search.** … for research evidence it hands the criteria to the evaluation theme with PICOS as an option, "证据，应根据评价主题确定纳入与排除标准，可基于"PICOS"" (char 10167); …` | **adjacent** — the second near neighbour claims.md names. One Chinese instrument's inclusion rule, quoted; PICOS is reported as 可 ("may") in *that* instrument's rule. The entry's file has no `##` decision section at all (headings: `#### Observation`, `#### Inference`, `#### Unknown`). |
| 6 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md:26` | `- **The inclusion rule belongs to the evaluation theme, with PICOS optional and the evidence floor class-specific.** `S118` reads "证据，应根据评价主题确定纳入与排除标准，可基于"PICOS"" — 可, not 应 …` | **adjacent** — an inference bullet about one instrument, not a decision list. |
| 7 | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md:11` | `- **The protocol-writing paragraph names PRISMA-P, its size and the search's features.** … beside eligibility criteria and whether unpublished material and abstracts are included; …` | **adjacent/unrelated** — it concerns what PRISMA-P asks a *protocol* to record, not which question frame to pick. |

### 1.2 The structural sweep (what a decision list on frames would look like)

Command (receipt `r14-k4-base-sweep.txt` / `.out`), at base:

- `git grep -n -E '^#+.*[Dd]ecision' BASE -- corpus/knowledge` → **exactly three** hits:
  `citation-searching-tarcis-r81.md:29`, `correction-retraction-status-r81.md:36`, `recheck-due-r26.md:21`.
  All three are on citation searching, correction/retraction status, and recheck scheduling respectively — **none** on question framing.
- `git grep -l -i 'PICO' BASE -- corpus/knowledge` → **one** file only: `quality-control-guideline-issued-text-r48.md` (the named near neighbour).
- `git grep -l -i -E '\bPCC\b|SPIDER|\bPECO\b' BASE -- corpus/knowledge` → **none** (exit 1).
- `git grep -n -i -E 'PICO|PCC|PECO|SPIDER' BASE -- corpus/README.md` → **none** (exit 1).
- `git grep -n -E '^#+.*[Dd]ecision' BASE -- corpus/README.md` → **none** (exit 1): the README has no decision section of its own.
- `git grep -n -i -E 'question fram|PICO|PCC|PECO|eligib' BASE -- PROVINCE.md SKILL.md corpus/QUALITY.md corpus/MINT.md` → three hits, all listed in the table above (PROVINCE.md:5, SKILL.md:3, SKILL.md:17); QUALITY.md and MINT.md contribute **nothing**.
- Base `corpus/lessons/`: `git grep -n -i -E 'PICO|PCC|PECO|SPIDER' BASE -- corpus/lessons` → two hits, both in `round-53.md` and both quoting S118's PICOS sentence (the same near neighbour). `git grep -n -i 'question fram' BASE -- corpus/lessons` → none.
- Base `corpus/knowledge/` headings that could carry a frame-choice list (`grep -i -E 'rule|checklist|guide|choose|when to|frame|eligib|criteria'` over all `^#+ ` headings) → only `## Disposition rule`, `## Disposition table`, `## The rule*`, `## The sweep rule`, `## The token rule (exact)`, `## The seven rule classes`, `## Reading rule` — read; each is about metadata screens, gate findings, aliasing or token boundaries. **No frame-choice list anywhere.**

### 1.3 Two further base surfaces checked

- `corpus/SOURCES.md` at base, row S008: `… | sections 2.1 rationale and 2.3 three PICO levels; last updated August 2023, Handbook v6.5 | Frame an answerable question first and keep review PICO, synthesis PICO, and included-study PICO distinct | queued | …` — the *registry* row already names the three PICO levels (a one-line `teaches` cell on a `queued` row with no capture at base), and `## Paths` in the same file says "scope the question before searching (PICO levels)". This is a **registry-level** statement of the topic, not a base *entry* holding a decision table/list, and K4 as written targets "a base-list entry" (the base-list is `corpus/evidence/round82/base-knowledge.txt`, i.e. `corpus/knowledge/*.md`). Worth reporting as the closest base surface, and as a caution to the K3 reviewer: the S008 row's `teaches` cell already said the three-PICO-levels thing before this round, so the new entry's rows 4–6 are *grounding of a pre-existing registry proposal*, not a new topic. It is still, on the frozen K4 wording, not a fire (the base entry list holds no such table).
- `corpus/captures/` at base: `fd7eed5e0e6c64e22bc1470c` (chapter-02) and `dedff231d5c3d3cdb0b4f8e3` (crossmark) are **absent** at base (receipt `r14`, section on capture sets); the landing added exactly five `.txt` captures (diff of base vs landing capture lists: `213237301753814b95b24684`, `97223722748a928c3c6912b5`, `bcb4a695b2aa019305121cff`, `dedff231d5c3d3cdb0b4f8e3`, `fd7eed5e0e6c64e22bc1470c`; rc 1 on the diff = five added, none removed). So the round fetched genuinely new bytes for S008/S028 rather than reusing a base capture.

**Conclusion for K4: held (not fired).** No base-list entry, README, SKILL.md, PROVINCE.md, QUALITY.md, MINT.md or lesson holds a decision table or decision list on choosing or aligning a review question frame. The two near neighbours claims.md names (`archived-export-intake.md:89`, `quality-control-guideline-issued-text-r48.md:26`) are adjacent, as claims.md itself states.

### 1.4 The near neighbour claims.md does *not* name (for the K3 reviewer's attention)

Base `corpus/SOURCES.md` `## Paths` (lines 224–227) and base row S008's `teaches` cell both already carry the PICO-levels idea, and base `corpus/knowledge/western-instrument-alignment-r50.md` carries an **"alignment"** subject — but its subject is *instrument* alignment (Cochrane handbook vs. Chinese quality-control guideline), not objective–question–eligibility alignment; it has no decision table and no frame rows. Base `corpus/knowledge/citation-searching-tarcis-r81.md` is the lane's other decision-table entry; its subject is citation searching, and its `eligib` hits are about *eligible records* found by a search, not eligibility criteria. Neither is same ground.

---

## 2. Registry at the landing revision

### 2.1 Duplicate URLs (census W04) — the landing introduces **no** new duplicate URL

Command (receipts `r05-census-base.txt` / `r06-census-landing.txt`):

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root <tree> --file <tree>/corpus/SOURCES.md
```

Base tree (extracted at `142b6f0c…`) and landing tree (extracted at `b4a41d25…`) both print the **identical**
five W04 warnings — `S051`, `S053`, `S073`, `S074`, `S075` — and then `file ok`, exit 0. **No W04 row names
S008, S028, S209, S210 or S211.**

Why this is worth stating (the near-miss a reviewer might suspect): the three JBI rows S209/S210/S211 sit on
one host (`jbi-global.atlassian.net`) and one wiki space, but the census normalises the whole URL
(`url_of()` keeps host+path, lower-cases the host) and the three paths differ
(`…/pages/355862667/10.2.2+Developing+the+title+and+question`, `…/pages/355862687`, `…/pages/355862707`).
Also S008's row already existed at base with the identical URL (it was `queued`, so it was not a new
duplicate); the re-open changed only `anchor`, `status`, `usedby` (receipt `r10`).

Note on `E11`: running the census against a *copy* of `SOURCES.md` placed outside the tree prints many
`E11 … missing used-by` lines, because `E11` resolves `used-by` paths against the tree root. Against the
tree's own registry (`--root <tree> --file <tree>/corpus/SOURCES.md`) the result is `ok`, exit 0. The
E11 lines are an artefact of the invocation, not a lane defect — **do not read them as one.** (I reproduced
both forms; only the in-tree form is the lane's.)

### 2.2 Row-count delta and statuses

Census `census` mode: base `rows=208, status.queued=19, status.mined=166, status.rejected=23`;
landing `rows=211, status.queued=17, status.mined=171, status.rejected=23`. Delta: +3 rows
(S209, S210, S211), −2 queued (S008, S028), +5 mined.

### 2.3 Rows still `queued` that the new entry could have cited — none were, and none could be

Queued at landing: `S009 S010 S011 S012 S017 S018 S019 S020 S021 S022 S023 S024 S026 S027 S030 S031 S032` (17).

- **No queued row has any capture in the tree.** Command: for each queued row, `sha256(url)[:24]` and
  `corpus/captures/<key>.txt` existence — output: `capture: False` for **all 17**. So no queued row could
  have supplied a located quote (the counter's E3 needs a committed capture + a fresh `refetch.tsv` row).
- `refetch.tsv` rows dated on/after the round start (`$5 >= 2026-11-06T19:41:56Z`) exist for exactly five
  ids: `S008 S028 S209 S210 S211` — the round's own five. No queued row was fetched.
- The two queued rows a reviewer might have expected to see cited for the *frame* topic are **S009**
  (Cochrane MECIR risk-of-bias standards; scope "the MECIR conduct standards for risk-of-bias judgments")
  and **S017** (PRISMA 2020 statement; scope "reporting standard for systematic-review search
  transparency"). Neither is a question-framing source, and neither has a capture. `S019` (Cochrane
  Handbook ch. IV, updating a review) is queued but is the *same URL* as mined S029, whose row
  `teaches` cell opens "supersedes S019 — …"; the base `metadata-screen-r25.md:89` records
  "S029 supersedes S019". Citing S019 would have meant re-asserting a superseded row.
- The landing README's Frontier bullet names exactly `S009 (MECIR risk-of-bias), S017 (PRISMA 2020) and
  S019 (updating a review) stay queued` — consistent with the registry and with the base README's
  known-gap line 859 ("the queued SOURCES rows S008–S012, S017, S018 waiting for an entry that mines them").
  **Caveat:** line 859 is inside the `## Frontier` section and still names **S008** as queued, while S008
  is `mined` at the landing. The round-82 section does not correct that stale line. That is a residual
  (a stale frontier sentence), not one of the frozen kill rules.

### 2.4 Did the S008 re-open change anything the row says?

Receipt `r10-s008-row-diff.txt` / `.out` (cell-by-cell diff of the S008 row, base vs landing):

| cell | same? | base | landing |
|---|---|---|---|
| id / source / kind / tier / scope | yes | — | — |
| `anchor` | **no** | `sections 2.1 rationale and 2.3 three PICO levels; last updated August 2023, Handbook v6.5` | `sections 2.1 Key Points and 2.3 (the three PICO stages: review PICO, PICO for each synthesis, PICO of the included studies) as served 2026-11-06 (capture key fd7eed5e0e6c64e22bc1470c); Handbook v6.5` |
| `teaches` | **yes** | `Frame an answerable question first and keep review PICO, synthesis PICO, and included-study PICO distinct` | identical |
| `status` | **no** | `queued` | `mined` |
| `opened` | yes | `2026-10-19` | `2026-10-19` (unchanged — correct for a re-open) |
| `recheck` | yes | `on-release` | `on-release` |
| `usedby` | **no** | `—` | `corpus/knowledge/question-framing-frames-r82.md` |

So: **the taught content of S008 did not change** — the `teaches` cell is byte-identical to base. What
changed is the anchor (now names the three PICO stages and pins the capture) and the status/used-by
bookkeeping. Two precision notes on the new anchor, both about the anchor's own accuracy:

1. The anchor says "sections 2.1 **Key Points** and 2.3". In the capture, `Key Points:` is a **chapter-level
   box** (line 531), immediately *before* the `2.1 Rationale for well-formulated questions` heading (line
   538); there is exactly **one** `Key Points` occurrence in the whole capture (receipt
   `r11-s008-anchor-vs-quote-location.txt` / `.out`), and it is not a section named "2.1 Key Points". The
   base anchor's "2.1 rationale" named the real §2.1 heading. A reader following the landed anchor will
   find §2.1 at the right place but the box labelled "Key Points" is chapter-scoped. This is a labelling
   imprecision in a registry cell, not a claim defect.
2. The anchor omits §2.5.2, yet **quote Q5 sits there**: receipt `r11` locates Q5 at capture line 690 under
   the nearest heading `2.5.2 Changing review questions` (Q1–Q4 are at lines 558–562 under §2.3). The
   landed entry's row 7 ("No relevant source has been read yet … Q5 (S008)") therefore rests on a section
   the row's own anchor does not name. (The uncommitted working-tree edit visible in the lane — not part of
   the landing — corrects the anchor to name "the chapter Key Points box, section 2.3 … and 2.5.2 Changing
   review questions", which is the same reading I reached independently. The landing revision itself does
   not carry it.)

S028's row: same three-cell shape (anchor widened to add "and the How Crossmark works paragraph, as served
2026-11-06 (capture key dedff231d5c3d3cdb0b4f8e3)"; status `queued`→`mined`; used-by → the r81 entry);
`teaches` byte-identical.

---

## 3. `corpus/README.md` — coverage-map placement and accuracy of the round-82 section

### 3.1 Which coverage row the new entry belongs under

The README's top `## Coverage map` table (lines 3–96) is **not** where a new entry goes. Measured:
that table names 43 `knowledge/*.md` files, while the base `corpus/knowledge/` holds 93 `.md` files
(`git ls-tree -r --name-only BASE -- corpus/knowledge | grep '\.md$' | wc -l` → 93). Sixty base entries are
absent from the top map — including both round-81 entries
(`citation-searching-tarcis-r81.md`, `correction-retraction-status-r81.md`) and, at base, `S009`-era
entries. The lane's convention is a **per-round section at the end of the file**:
`## Round81 coverage and frontier (2026-11-06)` at base line 1367, `## Round82 coverage and frontier
(2026-11-06)` at landing line 1377. The landing puts the new entry in a per-round table row under the
Round82 section — **the right place**, matching the immediate precedent. The G02 knowledge-index gate
passes at the landing tree: `GATE G02 knowledge-index PASS 94 entries indexed` (receipt `r09`… see §5).

### 3.2 Accuracy of the round-82 section — two defects, one clean item

Section text as landed (receipt `r13-readme-round82-section.txt` / `.out`):

```
## Round82 coverage and frontier (2026-11-06)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/question-framing-frames-r82.md` | question framing: PCC for mapping questions, PICO/PECO when a map precedes a systematic review, the three PICO stages (eligibility, each synthesis, what included sources investigated), eligibility derived per frame element, protocol deviations reported with justification | S008, S209, S210, S211 |

- `knowledge/correction-retraction-status-r81.md` gains a round-82 Crossmark addendum (S028 queued → mined).
- `lessons/round-82.md` — S008 re-opened (queued → mined), S209–S211 admitted, S028 dispositioned; gate fix for the round-81 K2 forms.
- Frontier: S009 (MECIR risk-of-bias), S017 (PRISMA 2020) and S019 (updating a review) stay queued.
```

**(a) DEFECT — `lessons/round-82.md` does not exist.** The bullet names a lesson file as holding round-82
content. `git ls-tree -r --name-only b4a41d25… -- corpus/lessons/round-82.md` → empty output (file absent);
same at tip `46dd1dc3…` → absent. The last committed lessons are `round-80.md`, `round-81.md` (plus
`-verifier-spotcheck.md` companions). The round-81 section names `lessons/round-81.md`, and that file
*does* exist at base — so the round-82 bullet breaks the precedent it copies. claims.md's "Frontier step
(not a claim)" list does include "Mine one mistake into `corpus/lessons/round-82.md` `## Mistakes`", so
the file is *expected* to appear in the round — but as of the landing revision and the tip it does not
exist, while the README asserts it does. Note this does **not** trip G02 (G02 indexes only
`corpus/knowledge/*.md` against the README and checks README↔knowledge path pairing, so a
`lessons/…` path is outside its scope) and does not trip the census (`E11` only checks `used-by` cells).
It is a plain README-accuracy defect: the coverage section claims a note the tree does not hold.
(Scope note, observed while finishing: by the time this seat wrote its report, another seat had created
`corpus/lessons/round-82.md` as an **untracked** file in the lane worktree. That copy is not in the landing
revision or in the tip, so the finding as stated — the *committed* tree holds no such note — stands; and the
README text remains ahead of the commit either way.)
The related r81 routed defect 4 ("commit the G02 `PREFLIGHT=1/1` run at the final tip as a receipt") is
likewise still open at the tip: `git ls-tree -r --name-only HEAD -- corpus/evidence/round82` lists only
`after/c1-after.txt`, `after/c1-selftest-after.txt`, `after/c2-after.txt` — **no G02/preflight receipt**
(receipt `r13`; `git grep -l 'GATE G02' HEAD` finds only round-63/round-64 wave files, none under
`corpus/evidence/round82`).

**(b) RESIDUAL — the base Frontier sentence at line 859 is now stale.** It still reads "the queued SOURCES
rows S008–S012, S017, S018 waiting for an entry that mines them", while S008 is `mined` at the landing.
The round-82 section does not amend that line. Same class as (a): a README statement the tree contradicts.

**(c) CLEAN — the coverage table row itself is accurate.** Its "Holds" text matches the entry's own rows:
PCC for mapping questions (row 1, Q6/Q7), PICO/PECO when a map precedes a systematic review (row 2, Q8),
the three PICO stages (rows 4–5, Q1/Q2/Q3 — "eligibility, each synthesis, what included sources
investigated"), eligibility derived per frame element (row 3, Q10), protocol deviations reported with
justification (row 9, Q11). Its "Sources" cell `S008, S209, S210, S211` equals the entry's `source:` line
and the registry's `usedby` for those four rows. The two other bullets are also true of the tree: the
r81 entry does carry a Crossmark addendum at the landing, and S028 is `mined`.

### 3.3 The S028 addendum's own "Never" cell — a K3-candidate I flag but do not adjudicate

`corpus/knowledge/correction-retraction-status-r81.md` gained (at the landing) an addendum row whose Never
cell reads "treat an absent Crossmark button as 'no correction or retraction' — it shows only that the
publisher did not deposit the signal". The addendum itself says so explicitly ("The 'never' clause is the
lane's reading of S028's 'Members place the Crossmark button…'; S028 does not itself state what an absent
button means"), and the capture supports the *positive* half ("Members place the Crossmark button close to
the title of an item on their web pages and in PDFs.", capture line 183, and "Crossmark lets readers know
when a substantial change affecting the citation or interpretation has occurred…", line 164 — both located,
receipt `r09` and the capture reads). Because the addendum labels the inference as the lane's own, a
non-author reviewer may reasonably accept it. I flag it because it is the one "Never" clause in this round
that is not traceable to a quote, and it is not in the new entry the C2 counter scores — so the C2 counter's
PASS says nothing about it.

---

## 4. What the frozen counters say at the landing (measured, not inherited)

Both counters were re-run by this seat against a fresh `git archive` extraction of the landing revision
(receipts `r07-depth-counter-landing.txt` / `.out` and `r08-k2-gate-counter-landing.txt` / `.out`):

```
$ python3 -B <tree>/corpus/evidence/round82/depth-r82.py --root <tree>
ENTRY question-framing-frames-r82.md ok=yes rows=9 quotes=11/11 fails=-
DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4
DEPTH_R82=PASS
exit=0
```
(C2 predicate target: `entries=1 ok_entries=1`, `rows>=5` → 9, `located_quotes>=5` → 11,
`fresh_sources>=3` → 4. **Met.**)

```
$ python3 -B <tree>/corpus/evidence/round82/k2-gate-r82.py --root <tree>
RUNLINE item=2 found=yes cmd=f=<record.md>; ! bash tools/research-gate.sh verify "$f" --root . | grep -q …
RUNLINE item=4 found=yes cmd=bash tools/research-gate.sh verify-sweeps <record.md> --root .
…
RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6
K2_GATE=PASS
exit=0
```
(C1 predicate target: `RUNLINES=2/2`, `K2_REFUSED=11/11`, `HOLD_REFUSED=9/9`, `CLASS_REFUSED=24/24`,
`POSITIVE=6/6`, `K2_GATE=PASS`, rc 0. **Met.**)

Gate selftest at the landing tree (`bash tools/research-gate.sh --selftest`, run once by this seat):
`RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`, exit 0 — **C1 K4 not fired** (K4 requires PASS, no
skip, and ≥275 cases; 280 ≥ 275, 0 skipped).

**A note on the C1 Run-line byte-equality.** The counter's `FROZEN_RUNLINE` compares only the *command*
inside the backticks, and it reports `found=yes` for both items with the base command text verbatim — so the
counter's check passes. But the landing **did** edit the surrounding prose of both Run lines in `SKILL.md`
(appending "Round 82: …" sentences), so the full Run *lines* are not byte-identical to base even though the
backticked commands are. The counter is unaffected (it extracts the command with
`re.match(r"^\s+- Run: `([^`]+)`", nxt)`); the frozen claim wording "the SKILL.md item-2 and item-4 Run lines
stay byte-identical to base" is therefore satisfied **only in the counter's sense** (the command), not for
the whole line. Since the counter is frozen and is the scoring instrument, this is not a kill; it is a
wording observation for the C1 reviewer.

---

## 5. Other surfaces measured (for the frontier)

- **Preflight G01–G07 at the landing tree** (`python3 -B tools/lane-preflight.py --root <tree> --fleet
  /home/vgpnk/Projects/shokunin --work <scratch> --only G01,…,G07`):
  `G01 census PASS`, `G02 knowledge-index PASS 94 entries indexed`, `G03 lesson-gate PASS 59 lessons carry
  ## Gate`, `G04 shonen-pointers PASS 10 pointers resolve`, `G05 scorecard-paths PASS 95 capability pointers
  resolve`, `G06 freeze-selftest PASS`, `G07 assimilate-selftest PASS`, `PREFLIGHT=7/7`, exit 0. G08 skipped
  (the selftest was run separately, §4).
- **Quote presence** (receipt `r09-quote-presence.txt` / `.out`): all eleven declared quotes of the new
  entry are present (whitespace-collapsed) in their committed capture texts, and each capture's sha256
  equals its `refetch.tsv` `txt_sha256` cell: `fd7eed5e…` → `598abc09…`, `bcb4a695…` → `fc857da3…`,
  `97223722…` → `b8b542d9…`, `21323730…` → `8581ca18…`, `dedff231…` → `ad526ada…`. C2's K2 (quote absent /
  sha mismatch) is not fired by anything I could measure.
- **Round-82 lesson / mistake material**: `corpus/lessons/round-82.md` absent (see §3.2a). The
  round-82 mistake candidate is being mined as an *untracked* file `corpus/evidence/round82/mistake-r4-07.txt`
  in the lane worktree, whose content is a receipt-shaped check of the r81 r4-07 description
  (`described_form_present=0` → the r81 description does not match the bytes; control record
  `described_form_present=1`). I did not write it.
- **Uncommitted lane state at the tip** (observed, not touched): `git status --porcelain` in the lane shows
  ` M corpus/QUALITY.md`, ` M corpus/SOURCES.md`, ` M corpus/knowledge/question-framing-frames-r82.md`,
  `?? corpus/evidence/round82/mistake-r4-07.txt`, plus untracked `.ufo/waves/round-82/` wave files. The
  `question-framing-frames-r82.md` diff rewrites row 1's Never to "treat the map as a test of an effect",
  row 7's Never to "expect, as a rule, to fix the final question before any relevant source is known", and
  appends a `## Correction (round 82, after scoring)` section that itself states the round's C2 verdict is
  "falsified by its own kill rule K3". Those are post-scoring repairs in the worktree, not the landing bytes
  I attacked; the landing revision `b4a41d25…` still carries the original row 1 Never ("force an
  intervention, comparator and outcome onto a mapping question", warrant Q6, Q7). **The landing bytes I was
  asked to attack are the ones that matter for scoring** — the repair does not rescue the landing revision,
  and claims.md's K3 says a repair after scoring does not rescue the claim.
- **The landing's row 1 is a K3 candidate I can measure but not adjudicate.** Warrant Q6 = "JBI suggests
  utilising the PCC (population, concept and context) approach to formulate review questions for scoping
  reviews." Warrant Q7 = "A scoping review question is broader than those in systematic reviews and can be
  seen as hypothesis-generating, whereas a systematic review is hypothesis-testing". The Never cell at the
  landing reads "force an intervention, comparator and outcome onto a mapping question". Neither quote
  states a prohibition; the same page's next paragraph (Q8, capture line 840) says "there may be a compelling
  argument to use a different question format (such as PICO or Population, Exposure, Comparator, Outcome
  [PECO]), such as when performing a structured analysis of existing research or research gaps, or as a
  precursor to a systematic review" (receipt `r12-q8-truncation.txt` / `.out`), i.e. the source admits
  PICO/PECO for a map that feeds a systematic review — which contradicts the Never clause as written.
  That is exactly the K3 question the claims file reserves to a non-author reviewer; I record the
  evidence and leave the verdict to that seat.

---

## 6. Findings, ranked

1. **C2 K4 does not fire.** No base entry / README / SKILL.md / PROVINCE.md / QUALITY.md / MINT.md / lesson
   holds a decision table or decision list on choosing or aligning a review question frame. The only base
   `PICO` mention in `corpus/knowledge/` is the r48 near neighbour claims.md already names; both named near
   neighbours are adjacent, not same ground. (Receipts `r01`, `r14`.)
2. **C2's own counters pass at the landing** — `DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11
   fresh_sources=4 / DEPTH_R82=PASS` rc 0; all 11 quotes located in their captures; all five capture sha256s
   match their `refetch.tsv` cells. (Receipts `r07`, `r09`.)
3. **README defect (accuracy):** the Round82 coverage section names `lessons/round-82.md`, which exists in
   neither the landing revision nor the tip; and the base Frontier sentence at line 859 still calls S008
   queued. Neither is caught by any gate. (Receipt `r13`.)
4. **r81 routed defect 4 still open at the tip:** no committed G02/`PREFLIGHT=1/1` receipt exists under
   `corpus/evidence/round82` (only three `after/*.txt` receipts). (Receipt `r13`.)
5. **Registry:** no new duplicate URL (census W04 set unchanged, 5 pre-existing rows); S008's `teaches`
   cell is byte-identical to base — the re-open changed only `anchor`, `status`, `usedby`; the landed
   `anchor` names "2.1 Key Points" (a chapter-level box, one occurrence in the capture, before the §2.1
   heading) and omits §2.5.2, where quote Q5 actually sits. (Receipts `r05`, `r06`, `r10`, `r11`.)
6. **K3 candidate at the landing bytes** (not adjudicated here): row 1's Never clause is not stated by Q6/Q7
   and is contradicted by Q8 in the same source page. (Receipt `r12`.)
7. **C1 wording observation:** the two SKILL.md Run *lines* were reworded at the landing (the backticked
   commands were not), so "byte-identical Run lines" holds only in the counter's sense. (Receipt `r08`.)

Tooling: no tool was installed or upgraded by this seat (`uv`/`npm`/`pacman` untouched). The only binaries
used are `git`, `python3`, `bash`, `grep`, `awk`, `sha256sum`, `sed`, `sort`, `diff` — all pre-installed.
The fleet census `scripts/sources-census.sh` (fleet root, read-only, unmodified) was used unmodified.
