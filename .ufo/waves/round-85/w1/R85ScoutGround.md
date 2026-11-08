# R85ScoutGround — read-only reconnaissance on C2 ground, novelty and S020 disposition

Seat: `R85ScoutGround` (scout m_antigravity role). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Host `Linux 7.2.11-arch1-1`, date 2026-11-08. Read-only; no lane/fleet git or jj mutation, no commits, no network
fetches (my wave item names no re-open URL), no production edits. No tools were installed or upgraded this round
(stock `git`, `python3`, `grep` only), so the operator tooling record for this seat is empty.

Revisions under attack:
- base `43c3f7284eee4889cdcc6ac1626573f6579cd533` (round-84 tip + verifier spot-check)
- freeze `5d0b94139ae8baf60d6f630715bc495f0a93b448` (claims + egress table, committer time `2026-11-08T03:54:30Z`)
- claims amendment `02df67db4f9ad39f8ebc73984ce50ea1fbea315f`
- landing / current tip `64803d33362f50cf9094e91fc3a4a07216c563ca` (committer time `2026-11-08T04:31:25Z`)

Receipts written under my output folder, all citable:
- `.ufo/waves/round-85/w1/R85ScoutGround/receipts/r85scout-k4-ground.txt`
- `.ufo/waves/round-85/w1/R85ScoutGround/receipts/r85scout-novelty-held-ground.txt`
- `.ufo/waves/round-85/w1/R85ScoutGround/receipts/r85scout-s020-disposition.txt`
- `.ufo/waves/round-85/w1/R85ScoutGround/receipts/r85scout-depth-counter.txt`
- `.ufo/waves/round-85/w1/R85ScoutGround/receipts/r85scout-novelty-same-document.txt`
- `.ufo/waves/round-85/w1/R85ScoutGround/receipts/r85scout-s020-disposition-details.txt`

---

## Surface 1 — C2 K4 (ground): does any base-list entry cite S215 / S026 / S024, or contain their URLs?

**Answer: no. K4 as amended does not fire.**

Command (run at both revs, one per URL and one for the three ids):

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -F '<url>' <rev> -- corpus/knowledge
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -E '(^|[^A-Za-z0-9])(S215|S026|S024)([^A-Za-z0-9]|$)' <rev> -- corpus/knowledge
```

Observed (receipt `r85scout-k4-ground.txt`):

| rev | URL | rc | result |
|---|---|---|---|
| base `43c3f72` | `https://www.w3.org/TR/prov-o/` | 1 | no hit in `corpus/knowledge` |
| base `43c3f72` | `https://www.gofair.foundation/r1-2` | 1 | no hit |
| base `43c3f72` | `https://schema.org/lastReviewed` | 1 | no hit |
| base `43c3f72` | ids `S215\|S026\|S024` | 1 | no hit |
| landing `64803d33` | `https://www.w3.org/TR/prov-o/` | 1 | no hit |
| landing `64803d33` | `https://www.gofair.foundation/r1-2` | 1 | no hit |
| landing `64803d33` | `https://schema.org/lastReviewed` | 1 | no hit |
| landing `64803d33` | ids `S215\|S026\|S024` | 0 | 12 hits, **all** in `corpus/knowledge/provenance-recording-r85.md` |

Per-file membership scan of `corpus/evidence/round85/base-knowledge.txt` (96 files; the list is exactly the 96 `.md`
files of `corpus/knowledge` at base — `comm` on the sorted tree listing vs the list gives no difference apart from
`.gitkeep`), reading each file's `source:` line from the landing rev:

```
git show <landing>:corpus/knowledge/<each file> | head -15 | grep source:
→ files with source: line naming S215/S026/S024: 0
```

So the amended K4 ("a base-list entry cites S215, S026 or S024, or contains their URLs") is satisfied on its own terms
at the landing rev. **K4 did not fire.** The 12 landing hits are inside the *new* entry, which is by construction not
in the base list (`base-knowledge.txt` and the base tree agree exactly; `provenance-recording-r85.md` is the only new
knowledge file at landing).

### 1a. Ground-proximity finding (K4 holds on form; the document ground is partly held)

This is the part the wave should not lose, because the counter's E7 test and the frozen K4 rule are both written on
**S-ids and URL strings**, not on documents.

- The base-list entry `corpus/knowledge/metadata-screen-r25.md:3` already carries the **canonical** PROV-O URL and
  cites `S033` for exactly the three terms the new entry teaches:
  `source: … ; S033 https://www.w3.org/TR/2013/REC-prov-o-20130430/ §3.1 'prov:wasDerivedFrom' and §3.2 entity-lifetime paragraph (derivation and as-of time are separate facts → 'source:' and 'verified-at:') …`
  and at `:24-26`: "PROV-O records derivation (`prov:wasDerivedFrom`) and entity-lifetime times
  (`prov:generatedAtTime` / `prov:invalidatedAtTime`) as separate facts (S033), which is the split between `source:`
  and `verified-at:`."
- `S215` is the **same document**, reached by a different URL string. The new capture says so itself:
  `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt:36` — "This version: http://www.w3.org/TR/2013/REC-prov-o-20130430/
  **Latest published version: http://www.w3.org/TR/prov-o/**" (same file, title "PROV-O: The PROV Ontology",
  "W3C Recommendation 30 April 2013" at `:34-35`).
- `corpus/SOURCES.md:228` (S215) names the same Recommendation, 2013-04-30, and `corpus/SOURCES.md:43` (S033) names
  the canonical URL of the same document; S033 is `mined` with used-by `corpus/knowledge/metadata-screen-r25.md`.

Consequence for the counter: `depth-r85.py` E7 fires only if the source's S-id is on a base entry's `source:` line, or
if the source's **registry URL string** occurs in base-entry text. `https://www.w3.org/TR/prov-o/` occurs in no base
entry, so E7 passes for S215 — correctly per its own written rule, and the counter's PASS is a true PASS by its rules.
But `metadata-screen-r25.md` already teaches PROV-O derivation/entity-lifetime for the *same* document. The counter's
E4 quote-novelty rule also passes for Q4 because the full §3.2 sentence does not appear verbatim in any base
*knowledge entry* (r25 paraphrases it) — it lives verbatim in `corpus/lessons/round-25.md`, which E4 does not scan.

**Confidence: high** that K4 as written does not fire. **The residual ground question is a reading matter for the
wave's K3/ground reviewer, not something I can settle from the bytes.** I am reporting it as a fact, not a verdict.

### 1b. Predicate (C2 K1) — met at the landing rev

Frozen counting command, run against a `git archive` extraction of the landing rev:

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 64803d33362f50cf9094e91fc3a4a07216c563ca | tar -x -C <scratch>/tree-landing
python3 -B <scratch>/tree-landing/corpus/evidence/round85/depth-r85.py --root <scratch>/tree-landing
```

Observed (receipt `r85scout-depth-counter.txt`), rc=0:

```
ENTRY provenance-recording-r85.md ok=yes rows=6 quotes=7/7 fails=-
DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3
DEPTH_R85=PASS
```

This matches the amended predicate (`entries=1 ok_entries=1`, `rows=` ≥ 6, `located_quotes=` ≥ 7, `fresh_sources=3`,
`DEPTH_R85=PASS`, rc 0). **C2 K1 did not fire.** Note the counter does not exist at the base rev
(`corpus/evidence/round85/depth-r85.py` absent from the base tree — python exits 2, "No such file or directory"); the
frozen do-nothing control `corpus/evidence/round85/controls/receipts/c2-d0-donothing.txt` prints
`entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0 / DEPTH_R85=FAIL / depth rc=1`.

---

## Surface 2 — Novelty vs held ground

### 2a. Nearest neighbour

**`corpus/knowledge/metadata-screen-r25.md` is the nearest neighbour**, and it is *held ground for the S215 content*.
It is in `base-knowledge.txt` (confirmed present, count 1) and is the only base entry that teaches the three PROV-O
terms the new entry's rows 1–3 teach. Exact sentences that differ:

| held (r25) | new (r85) |
|---|---|
| `metadata-screen-r25.md:24-26` "PROV-O records derivation (`prov:wasDerivedFrom`) and entity-lifetime times (`prov:generatedAtTime` / `prov:invalidatedAtTime`) as separate facts (S033), which is the split between `source:` and `verified-at:`." | `provenance-recording-r85.md:34` "Naming what a resource derives from \| form the provenance chain with the derivation property where the chain's entities are set \| deliver a resource that passes for a primary when it derives from an identified earlier entity \| Q1, Q3 (S215)" |
| `metadata-screen-r25.md:36` "state the generation moment and the invalidation moment that bound it" is **not** in r25; r25 has only the split claim "derivation and as-of time are separate facts" | `provenance-recording-r85.md:36` "Recording the bounds of an entity's existence \| state the generation moment and the invalidation moment that bound it \| describe an entity as atemporal, with no generation or invalidation moment \| Q4 (S215)" |
| `metadata-screen-r25.md:96-99` "S033 supersedes S020's teaching: PROV times bound an entity's existence, not whether a research claim is true or when an analyst checked it. Using separate source/time fields for verification is explicitly a lane inference, not PROV-O's definition of verification. S020's historical row remains queued." | `provenance-recording-r85.md` `## Inference` "For this lane a 'resource' is a `corpus/SOURCES.md` row or a `corpus/knowledge/` entry; `generatedAtTime` / `invalidatedAtTime` motivate the `verified-at:` + `recheck:` pair, and R1.2's facets are the lane's Gate record itself. The sources state none of this mapping." |

The last pair is the substantive one: r25 explicitly labels the source/time-field mapping as "a lane inference, not
PROV-O's definition of verification"; r85 re-asserts the same mapping (as the `verified-at:` + `recheck:` pair) — but
r85 does label it under `## Inference (lane's, not stated by the sources)`, so the labelling discipline matches. The
*subject matter* (PROV-O derivation + entity-lifetime as the lane's own derivation/provenance vocabulary) is the same
material r25 already carries, from the same W3C Recommendation, via S033.

Second-nearest, for row shape rather than source: `corpus/knowledge/search-transparency-reporting-r84.md` (also a
base-list entry) already has the same two *situations* re-grounded on DCMI S023:
- `:46` "| Recording what a resource derives from | name the related resource from which the described resource is derived | record a resource without naming its source | Q9 (S023) |" vs new `:34` "Naming what a resource derives from …"
- `:47` "| Recording when a resource changed | state the date on which the resource was changed | record a modification without its date | Q10 (S023) |" vs new `:39` "| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | pass a record off as reviewed when only its modification date is known | Q7 (S024) |"

The two entries differ in source and in wording (S023 DCMI `source`/`modified` vs S215 PROV-O + S024 `lastReviewed`),
so r84 is not ground for S215/S026/S024; but the r85 rows are re-statements of situations r84 already covers.

The other two entries I was asked to check teach neither provenance recording nor any of the four markers:
- `corpus/knowledge/recheck-due-r26.md` — due-date scheduling (`recheck:` arithmetic, `--as-of` freshness). No
  `prov:` term, no FAIR, no `lastReviewed`.
- `corpus/knowledge/correction-retraction-status-r81.md` — correction/retraction status checks (S205/S206/S207/S028).
  No `prov:` term, no FAIR, no `lastReviewed`.
Grep receipts for all six marker strings across the four files: `r85scout-novelty-held-ground.txt`.

### 2b. Quote novelty across the whole corpus, not just base entries

Seven declared quotes (`provenance-recording-r85.md:22-28`). Byte-exact search of the base rev's
`corpus/lessons/round-{80..85}.md` and `corpus/knowledge/*.md`:

| quote | source | words | prior exact occurrence at base |
|---|---|---|---|
| Q1 "Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property." | S215 | 12 | none |
| Q2 "A derivation is a transformation of one entity into another." | S215 | 10 | none |
| Q3 "then we can say that the bar chart prov:wasDerivedFrom the dataset." | S215 | 11 | none |
| Q4 "The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence." | S215 | 19 | **`corpus/lessons/round-25.md:69`** (as the S020 quote) and **`:199`** (as the S033/S020 supersession row) — byte-identical |
| Q5 "Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions" | S026 | 20 | **`corpus/lessons/round-25.md:75`** (the S026 quote) — byte-identical |
| Q6 "using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit" | S026 | 17 | none |
| Q7 "Date on which the content on this web page was last reviewed for accuracy and/or completeness." | S024 | 16 | **`corpus/lessons/round-25.md:73`** (S024) and **`:197`** (S031/S024) — byte-identical |

So **3 of 7 quotes are re-quotes of sentences the lane already located in round 25**, two of them (Q4, Q7) for the very
rows this round re-opens. `depth-r85.py` E4 only compares declared quotes against the concatenated text of the 96
**base knowledge entries** (`base_text`), not against lessons, so E4 passes by construction. The claims file's own
framing (Amendment 1) says S023's "`modified` Definition repair … not re-quoted, to keep the new entry's quotes novel
and its ground new" — the same novelty intent, applied to S023, is not applied to Q4/Q5/Q7.

**Confidence: high** on the byte-identity facts (exact substring search, receipts `r85scout-novelty-same-document.txt`
section B). Whether re-quoting a previously located sentence is "novel" is a claim-reading call for the wave's
reviewer/critic seats, not mine.

### 2c. K3-adjacent observations on two decision rows (for the reviewer seats; I am not the non-author reviewer)

These are evidence, offered as K3 candidates; K3 requires a non-author reviewer to show them, so they are not my
verdict.

- **Row 5** (`provenance-recording-r85.md:38`): Never = "cite a tool by name alone, without version or step", warrant
  Q6 (S026). The GO FAIR capture contains **zero** occurrences of the substrings "version" or "step" (case-insensitive,
  whole capture `67983a3dbbd1d690aa648744.txt`, count 0), and the sentence the quote comes from
  (`…/67983a3dbbd1d690aa648744.txt:453`) speaks of "starting-data or source-resource … funding/resources … who owns
  the data, who should be given credit, and any filters or cleansing processes that have been applied
  post-generation" — no version, no step. "version or step" is not in the quote nor in the cited source's
  surrounding text.
- **Row 6** (`provenance-recording-r85.md:39`): Never = "pass a record off as reviewed when only its modification date
  is known", warrant Q7 (S024). The Schema.org capture contains **zero** occurrences of "modif" (both
  `11d6cc56bb24adfc61eea2b4.txt` and `.raw`, count 0); Q7 says only "Date on which the content on this web page was
  last reviewed for accuracy and/or completeness." The "modification date" comparison is asserted in the **registry
  row**, `corpus/SOURCES.md:34` S024 `teaches` = "A last-reviewed date for accuracy is a property separate from
  publication or modification dates" — and it is precisely the comparison that the **superseding** row S031 declines:
  `corpus/SOURCES.md:41` "supersedes S024 — lastReviewed records the date a web page was last reviewed for accuracy
  and/or completeness; **no comparison to other date properties claimed**". Round 85 revives S024 (queued→mined,
  used-by the new entry) and leaves S031 queued.
- **Row 1** Never = "deliver a resource that passes for a primary when it derives from an identified earlier entity"
  (`:34`); the PROV-O capture has zero occurrences of "passes for a primary" (68 hits for "primary" are all
  `prov:hadPrimarySource` / `prov:PrimarySource` / `prov:qualifiedPrimarySource` / "the three primary classes").
- **Q3** (`:24`) begins mid-sentence with "then we can say that the bar chart prov:wasDerivedFrom the dataset." —
  it is a verbatim substring of the capture (`…/6e48bcc4a04d13b7b3ebb68e.txt:781`, following line 780 "A derivation
  is a transformation of one entity into another. For example, if the Activity that created the bar chart is not known
  or is not of interest,"), so E3 is satisfied, but as a standalone quote its antecedent clause sits in Q2's sentence.

---

## Surface 3 — S020 disposition data

### 3a. Refetch rows for both PROV-O URLs

`corpus/evidence/round57/refetch.tsv` at the landing rev (receipt `r85scout-s020-disposition.txt` §"refetch rows",
`r85scout-s020-disposition-details.txt` §2–§3):

**Canonical URL `https://www.w3.org/TR/2013/REC-prov-o-20130430/`** (key `fc127d142427c83cc805fe67`) — 3 rows:

| line | id | attempt | fetched_utc | curl_rc | http |
|---|---|---|---|---|---|
| 167 | S020 | 1 | 2026-11-08T02:16:01Z | 22 | 403 |
| 168 | S020 | 2 | 2026-11-08T02:16:03Z | 22 | 403 |
| 169 | S020 | 3 | 2026-11-08T02:16:08Z | 22 | 403 |

**All three are pre-freeze** (freeze committer time `2026-11-08T03:54:30Z`) and are already present at the base rev
`43c3f72` — they were added by round-84's commit `3a17f4da` ("round-84: fetch S214/S018/S023, land
search-transparency entry, fix controls", `2026-11-07T23:22:58-03:00`). **Round-85 made zero attempts on the canonical
URL.** `git diff 43c3f72 64803d33 -- corpus/evidence/round57/refetch.tsv` adds 7 rows, none of them the canonical URL.

**Alternate URL `https://www.w3.org/TR/prov-o/`** (key `6e48bcc4a04d13b7b3ebb68e`) — 4 rows, all round-85:

| line | id | attempt | fetched_utc | curl_rc | http | txt_sha256 |
|---|---|---|---|---|---|---|
| 175 | S020 | 1 | 2026-11-08T03:54:43Z | 22 | 403 | `-` |
| 176 | S020 | 2 | 2026-11-08T03:54:47Z | 22 | 403 | `-` |
| 177 | S215 | 3 | 2026-11-08T03:55:52Z | 0 | 200 | `8c9aeabb466fb6d133c6a83cfc546a49336af782d0b7f2fccebcc55c2eb1f2a4` |
| 179 | S033 | 1 | 2026-11-08T04:15:56Z | 22 | 403 | `-` |

Attempts per URL: canonical **3** (all pre-freeze, all 403, no digests); alternate **4** (three 403 + one 200 with
digests), of which the 200 is the only one the depth counter consumes.

**Egress-cap observation.** `corpus/evidence/round85/egress-approval.md` ("Intended targets (each gets at most 3
attempts)", and the "not allowed" column "more than 3 attempts per URL") — the alternate URL received **4** GETs this
round (03:54:43Z, 03:54:47Z, 03:55:52Z, 04:15:56Z). The 4th is filed under id `S033` with attempt number `1`, i.e.
the attempt counter restarted under a different id for the same URL. Not a C2 kill rule; reported because the lesson
and the egress table both talk about attempt counts and the table's own bound is what is exceeded. **Confidence: high**
(row-level facts); the *reading* of whether a seat re-open or the L1 caused it is outside my remit (no wave item names
a re-open, and the egress table permits a seat re-open of a URL with a round-85 row).

### 3b. Is the alternate URL the same document as the canonical one?

**Yes.** Two independent pieces of evidence:

1. The capture's own self-declaration, `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt:36`:
   "This version: http://www.w3.org/TR/2013/REC-prov-o-20130430/ **Latest published version:
   http://www.w3.org/TR/prov-o/** Implementation report: … Previous version: …", with title "PROV-O: The PROV Ontology"
   (`:34`) and "W3C Recommendation 30 April 2013" (`:35`).
2. The distinctive §3.2 entity-lifetime sentence quoted for the **canonical** URL in round 25
   (`corpus/lessons/round-25.md:69` for S020 and `:199` for the S033/S020 supersession row) occurs verbatim in the
   new capture at `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt:1021` — the same sentence the new entry declares as
   Q4.

Caveat on the comparison the task asked for: the canonical side has **no capture at all**. There is no
`corpus/captures/fc127d142427c83cc805fe67.*` file (present: `False`) and `git log --all -- 'corpus/captures/fc127d…*'`
plus `git rev-list --all --objects | grep fc127d…` return **0 objects** — the canonical URL was never successfully
captured in the lane's history. So a capture-to-capture comparison is impossible; the available comparison is
canonical-URL-located-quote vs new capture (above), which is conclusive for document identity.

### 3c. S033 and S020 disposition

- `corpus/SOURCES.md:43` — **S033 is `mined`, not queued.** status `mined`, opened `2026-10-21`, recheck `365d`,
  used-by `corpus/knowledge/metadata-screen-r25.md`, URL `https://www.w3.org/TR/2013/REC-prov-o-20130430/` (the
  **canonical** PROV-O URL), teaching "supersedes S020 — PROV-O records derivation and entity generation/invalidation
  times separately; these are entity-lifetime facts, not verification time or truth-validity". Identical at base and
  landing.
- `corpus/SOURCES.md:30` — **S020 stays `queued`**, opened `2026-10-21`, used-by `—`, unchanged base→landing.

Correction to the brief's premise: **the amended claims file no longer says anything about S020 or S033.**
`corpus/evidence/round85/claims.md` at the landing rev contains only S215 (×5), S026 (×5), S024 (×5), S023 (×1) —
zero mentions of S020/S033. The freeze-time text (`5d0b9413`) did mention S020 (×7) and S033 (×2), including K4's
"S020's superseded row S033 (old URL) is not ground…"; Amendment 1 (`02df67db`) removed both S020 and S033 from the
claims file entirely (diff quoted in receipt `r85scout-novelty-same-document.txt` §D). The "S020 stays queued"
statement now lives only in `corpus/lessons/round-85.md:36` ("S020: unchanged (`queued`)") and in the registry.

### 3d. Deviations found in the landed lesson (`corpus/lessons/round-85.md`) — factual, from committed bytes

1. **`round-85.md:23-24`** — "the canonical `REC-prov-o-20130430` URL answered HTTP 403 on three attempts in round 84
   **and again this round** (rows in `refetch.tsv`, `curl_rc=22`)". The three canonical rows are dated
   `2026-11-08T02:16:0xZ`, i.e. **before** the round-85 freeze (`03:54:30Z`) and already present at the base rev;
   there is no round-85 canonical attempt in the table. "again this round" is not supported by `refetch.tsv`.
2. **`round-85.md:72`** (routed to round 86) — "S020's canonical URL is dead for this lane (**six 403 rows**)". The
   canonical URL has **3** rows; the six is the total across **both** PROV-O URLs (3 canonical + 3 alternate).
3. **`round-85.md:30-31`** — "opened date 2026-10-21 **kept** (first open)" for S026 and S024. The landing registry
   rows say `opened=2026-11-08` for both (`corpus/SOURCES.md:34` S024, `:36` S026); at base they were `2026-10-21`.
   The lesson contradicts the registry it committed (and round 25's lesson recorded the first open as 2026-10-21 for
   both, `corpus/lessons/round-25.md:73` and `:75`).

None of these three is a C2 kill rule; they are committed-byte deviations in the round's own lesson.

---

## What I did not check / remaining unknowns

- **K2 (located) live-page leg:** K2 requires a non-author re-open that gets HTTP 200 and tag-strips a quote. My wave
  item names no re-open URL and the egress table requires one to be named, so I performed **no** network fetch. I did
  not test the live pages; I verified only that all 7 quotes occur in the committed captures (`6e48bcc4…txt:779,780,
  781,1021`; `67983a3d…txt:453`; `11d6cc56…txt:211`).
- **Who issued the 4th GET to `https://www.w3.org/TR/prov-o/`** (row 179, id `S033`, 04:15:56Z): L1 vs a seat re-open.
  The row's attempt counter restarting at 1 under a new id is a fact; the actor is not recorded in the table.
- **Whether the K4/E7 ground reading in §1a should be re-scoped** is a claim-reading decision for the L1/reviewer, not
  a measurement I can make from bytes. I report the byte facts and the counter's behaviour under its own rule.
- I did not run the C1 counter or attack `tools/gate-records.py`; C1 is not in my wave item.

## Summary table

| claim | kill rule touched | outcome | one-line basis |
|---|---|---|---|
| C2 | K4 (ground) | **held** | no base-list entry cites S215/S026/S024 nor contains their three URLs (grep rc=1 at base and landing; per-file `source:` scan 0/96); ground-proximity via S033's same document reported as a reading note |
| C2 | K1 (predicate) | **held** | frozen counter at landing prints `entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3 / DEPTH_R85=PASS`, rc 0 |
| C1 | — | **n/a** | not in this seat's scope; no C1 measurement performed |

Tooling record: no install, no upgrade, no channel used (stock `git`/`python3` only). Pacman guard respected — no
pacman transaction attempted.

VERDICT: R85ScoutGround C2 held — C2's K4 and K1 kill rules do not fire on the landing bytes (no base-list entry cites S215/S026/S024 or their URLs; the frozen counter prints DEPTH_R85=PASS rc 0), though the S215 row points at the same PROV-O document already taught by held ground metadata-screen-r25.md via S033 and 3 of 7 quotes are byte-identical to round-25 located sentences.
VERDICT: R85ScoutGround C1 n/a — this seat's wave item covers only C2 ground/novelty and S020 disposition, and no C1 measurement was run.
