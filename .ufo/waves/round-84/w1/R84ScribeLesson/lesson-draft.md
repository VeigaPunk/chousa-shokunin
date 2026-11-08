# round-84 lesson — draft sections (seat `R84ScribeLesson`)

Draft, not landed. Wave `chousa-r84-w1`; Gate block taken at the scored landing
`03bbb4580b39b442be69f998fae2db48d64b8c93`. Receipts cited below live in
`.ufo/waves/round-84/w1/R84ScribeLesson/receipts/` (each names the exact command, the
observed output line and the exit code).

Every command below was run against a `git archive 03bbb458…` extraction under
`/fast/scratch/hyaku/chousa-r84/R84ScribeLesson/`, with `--repo` = the lane checkout
(read-only `git cat-file` only). No lane git or jj command mutated anything.

---

## Mistakes

Mined this round: **one** mistake, with the fix shown able to fail. It is not one of the
three candidates named in the seat brief — and that is deliberate. All three candidates are
already mined in the committed lesson at `03bbb458` (rows 1 and 2 of its `## Mistakes`
table) or, for the Unicode-digit class, already recorded as **QUALITY 164** in
`corpus/lessons/round-83.md:68`; re-mining any of them would duplicate committed text
instead of adding evidence. The row below is candidate (b) taken one round further back than
the committed row takes it: the defect is **not** round 84's own control design but round
83's committed overlay fixture, latent in round 83 and live in round 84 — and the
committed row records only the round-84 symptom. This row therefore carries the earlier-round
root, the lateness proof and the counter-level before/after that the committed row lacks.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a control overlay fixture written for an earlier round's ground was reused against a wider ground, and the fixture's **single-valued** `used-by` cell silently removed the real entry from the fresh set — so the control failed for a reason unrelated to what it was testing, and would have failed the same way in the round that wrote it | root in an earlier round: `corpus/evidence/round83/c1-controls/B1-salad-boundary/replace.txt` at `3b616420` — its `used-by` cell holds one value, `corpus/knowledge/ctl-entry-r83.md` — and round 84 reused that fixture verbatim (`corpus/evidence/round84/c1-controls/B1-salad-boundary/replace.txt`, pre-fix `3a17f4da`) against a wider tree. Latent in round 83: the real r83 entry `corpus/knowledge/appraisal-judgment-records-r83.md` did **not** exist at round 83's control rev `1b9b2ff8` (`git cat-file -e 1b9b2ff8:corpus/knowledge/appraisal-judgment-records-r83.md` → rc 128), and round 83's own control receipt `corpus/evidence/round83/controls/receipts/c1-b1-salad-boundary.txt` prints `entries=1` — the control entry only, so the erased `used-by` cost nothing. Live in round 84: the round-84 base list adds the r83 entry (`corpus/evidence/round84/base-knowledge.txt` 94 → 95 lines), so the real entry was in scope when the overlay replaced the S214/S018/S023 rows | self — seat `R84ScribeLesson`, at the round-84 scored landing, by re-applying **round 83's committed** overlay bytes to the landing tree (receipt `10-used-by-overlay-before-after.txt`) | a control overlay must name **every** entry that claims the row it replaces (`used-by` accepts a comma-separated list), and a control fixture must be diffed against the tree it will be applied to before it is run — a fixture that names one entry silently narrows the fresh set of every other entry that claimed the row. **Shown able to fail:** same landing tree, same frozen `depth-r84.py`, the round-83-shaped overlay before the fix and the committed comma-separated overlay after — before `ENTRY search-transparency-reporting-r84.md ok=no rows=11 quotes=0/12 fails=E3,E6` / `DEPTH_R84=FAIL` rc 1; after `ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-` / `DEPTH_R84=PASS` rc 0 (receipt `10-used-by-overlay-before-after.txt`). Scope: a **control-fixture** defect, not a defect of the lesson's content, of the counters, or of the tool — the counters were right to refuse a tree whose registry no longer claimed the real entry |

The lesson's own `## Mistakes` table at `03bbb458` already carries rows 1 and 2 for this
round (the S017→S214 split and this overlay). Row 2 above is proposed as a **sharper
statement of row 2**, not as an additional row: it moves the root to round 83, adds the
latent-then-live proof, and adds the counter-level before/after. Nothing in this draft
contradicts the committed lesson.

---

## considerthese

Read (never edited) `considerthese/2026-11-07.md` and `considerthese/2026-11-06.md`.

**One still-unimplemented proposal, named: "One open Gate-record S-id per daily review"**
(`considerthese/2026-11-06.md:28` — "Against the ScoutA remainder list, pick one id,
`git show <rev>:<path>`, re-count the quote, and report match/mismatch").

**This round does not implement it.** Evidence, at the scored landing:

- The twelve remainder ids from round 80's survey (`corpus/lessons/round-80.md:141`:
  S170, S171, S173–S176, S178, S179, S182, S183, S191, S193) still have **zero**
  `GATE-RECORD` lines anywhere under `corpus/lessons/` — measured per id, all `0`
  (receipt `08-considerthese.txt`).
- Round 84's own `## Gate` block opened three **new** sources (S214, S018, S023) and
  re-counted none of the twelve.
- The round-84 lesson says the proposal "is implementable via `tools/gate-records.py
  verify`; this round's lesson uses that command for its three records"
  (`corpus/lessons/round-84.md`, `## considerthese`). That is true of the three **new**
  records and stops there: the tool reads only the `GATE-RECORD` line grammar, while the
  twelve remainder records are written in two **older** grammars — ten as `| S170 |`
  table rows in lessons 70–72, and two (S191, S193) as prose `Admit S191` / `Admit S193`
  bullets in lessons 77–78. Grammar census per id: receipt `11-defect-id-grammar-census.txt`
  (table-row / prose-Admit / `GATE-RECORD`-line counts). The tool therefore reports
  `GATE_RECORDS files=1 records=0 ok=0 fail=0` on every lesson that carries them —
  measured on `corpus/lessons/round-70.md`, `-71.md`, `-72.md`, `-77.md`, all rc 1. Across
  all 132 lesson files the tool sees exactly 21 records (the S008–S214 set of lessons
  80–84); it cannot see a single one of the twelve it is meant to re-count.
- Reason it stayed unimplemented: the round's depth claim was bounded by its own frozen
  ground (S214, S018, S023), and re-counting the twelve would mean re-opening quotes in
  lessons 70–79 — outside the round's frozen scope and outside the wave's egress
  allowance.

Consequence for the lane: the "daily review of one open Gate-record id" habit cannot be
discharged by the round-84 tool as it stands. It needs either the twelve old rows
re-expressed in the `GATE-RECORD` grammar, or a reader for the older table grammar.

---

## Assimilation

**none.**

Reason, re-counted at the round-84 scored landing: the round-78 collision ledger is
unchanged and still blocks adoption — `wc -l` on
`.ufo/waves/round-78/assimilation/collisions` = **111** lines (111 distinct ids) against
`.ufo/waves/round-78/assimilation/staged-ids` = **114** lines and `reg-ids` = 192 lines;
only 3 of the 114 staged ids do not collide; and `git log -- .ufo/waves/round-78/assimilation/collisions`
lists exactly one commit (`3eb4a3ca`, round 78), so nothing has renumbered them
(receipt `07-assimilation-collisions-recount.txt`).

Nothing was adopted: no `merge/chousa/` package bytes were read into scratch, no theme
was re-grounded, and no §10 validation was run. The campaign tree is not under this lane's
root at all — a `find` for a directory named `merge` under `/home/vgpnk/Projects/shokunin`
returns 0 hits; the package bytes live outside the fleet root
(`/home/vgpnk/Projects/shokuknow/merge/chousa/`, read-only, untouched). Until the 111
collisions are renumbered, an adopted theme would inherit ids that already exist in the
lane's registry.

---

## Gate addendum

For the non-author spot-check, drawn from the existing `## Gate` block at `03bbb458`,
each verified with `python3 tools/gate-records.py verify` **and** the hand location
command of rounds 81–82 (whitespace-collapsed containment + `wc -w`).

**Check command (replaces the hand location command, as in round 83):**
`python3 tools/gate-records.py verify --root <tree> --repo <lane> corpus/lessons/round-84.md`
→ three `OK` lines (`S214`, `S018`, `S023`), `GATE_RECORDS files=1 records=3 ok=3 fail=0`,
rc 0 (receipt `01-gate-verify-landing.txt`, `07-gate-addendum.txt`).

### Admit S214 — the PRISMA 2020 checklist PDF record

- Tool: `GATE_RECORD corpus/lessons/round-84.md:18 S214 OK`, rc 0.
- Hand location: the quote is FOUND in `corpus/captures/a640b15abf781e5c583d7088.txt`
  at line 17; `wc -w` of the quote = **17** = the record's `words=17`.
- Provenance: that capture's sha256 begins `4cbf8881578dbc7b`, equal to the
  `txt_sha256` cell of the S214 `refetch.tsv` row (fetched `2026-11-08T02:21:13Z`,
  curl_rc 0, http 200); the registry row is `mined`, tier A, `used-by
  corpus/knowledge/search-transparency-reporting-r84.md`.
- Boundary note: this record is the second fetch of the same PDF bytes — the first is the
  S017-keyed row at `02:14:35Z` (`refetch.tsv`), the S214-keyed row at `02:21:13Z`. The
  lesson's "the checklist page linked to the PDF" is not what the bytes show: the
  S017 checklist-page capture `1f5f4eec0b85edf1dc53db7b` contains **no** PDF href (0 hits
  for `PRISMA_2020_checklist-ab3g`; its only two URLs are a Creative Commons licence and
  `prisma.shinyapps.io/checklist/`), and all five S214 quotes are ABSENT from both S017
  captures (`259c96bf7088a12bc7ce65c4`, `1f5f4eec0b85edf1dc53db7b`) and FOUND in the PDF
  capture at lines 17, 18, 19, 20, 53 (receipt `13-quote-locations.txt`). The URL
  direction of the PDF discovery is a prose claim of the round, not a Gate-record fact; the
  same point was reached independently by seat `R84ScoutNovelty` (finding 7).

### Reject S017 — the PRISMA 2020 landing page as a source of the checklist quotes

- The round's disposition (`corpus/lessons/round-84.md`, registry changes: "S017: fetched
  … but reverted to queued — the landing page carries no quotable checklist text") is
  **confirmed**.
- Hand location: each of the five S214 quotes is **ABSENT** from the S017 landing-page
  capture `corpus/captures/259c96bf7088a12bc7ce65c4.txt` and from the S017 checklist-page
  capture `corpus/captures/1f5f4eec0b85edf1dc53db7b.txt`; the same five are **FOUND** in
  the PDF capture `a640b15abf781e5c583d7088.txt` (lines 17–20, 54).
- Tool: a forged admit record for S017 (url = the landing page, capture = the landing-page
  capture, the checklist quote) is refused — `GATE_RECORD …:1 S017 FAIL QUOTE_ABSENT`,
  rc 1 (receipt `12-gate-addendum-forgeries.txt` §A). The tool cannot be talked into
  treating the landing page as quotable.
- Boundary note: the S017 landing page *was* fetched successfully (curl_rc 0, http 200,
  `refetch.tsv` rows at `02:13:58Z` / `02:14:24Z`); the rejection is of the page as a
  **source**, not of the fetch. S017's registry row remains `queued`, `used-by —`.
- Flip condition (as recorded): a landing page or checklist page whose own text carries
  the checklist sentences.

### Reject S020 — PROV-O as a source of any derivation or date claim

- The round's rejection (`corpus/lessons/round-84.md`, "Rejected this round": S020 PROV-O,
  HTTP 403, three attempts) is **confirmed** from committed bytes: three `refetch.tsv` rows
  for S020 at `2026-11-08T02:16:01Z`, `:03Z`, `:08Z`, each `curl_rc=22`, `http=403`, and
  the `txt_sha256` cell is `-` — no body was stored, so there is no capture to quote.
- Tool: a forged admit record for S020 that names the (never written) capture is refused
  with four codes — `GATE_RECORD …:1 S020 FAIL CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH`,
  rc 1 (receipt `12-gate-addendum-forgeries.txt` §B); the capture file
  `corpus/captures/fc127d142427c83cc805fe67.txt` does not exist.
- Tool, positive form: the rejected fetch **can** be written as the tool's `url/unreach`
  record — `GATE-RECORD S020 … decision=reject capture=none curl_rc=22 http=403 …` prints
  `S020 OK`, rc 0 (receipt §C). S020 is therefore rejected as a *source* with a flip
  condition already recorded (a readable copy of the PROV-O recommendation opened and its
  `wasDerivedFrom` definition located), and nothing in the entry rests on it.

---

## Routed to round 85 (addition)

1. **The frozen round-84 depth counter's own docstring contradicts its code.** Its
   `Usage:` line names `corpus/evidence/round83/depth-r84.py` — a path that has **never
   existed in any revision** of the lane (`git log --all -- corpus/evidence/round83/depth-r84.py`
   → no commits; `git cat-file -e 03bbb458:corpus/evidence/round83/depth-r84.py` → rc 128),
   so the counter's documented invocation cannot be run at all (rc 2, "No such file or
   directory"). Its prose also names round 83's base list
   (`corpus/evidence/round83/base-knowledge.txt`) and round 83's `ROUND_START`
   (`2026-11-06T20:53:00Z`) while the code reads round 84's
   (`corpus/evidence/round84/base-knowledge.txt`, `2026-11-08T02:05:00Z`). The two
   constant sets are not cosmetic: run with the docstring's constants the counter prints
   `entries=2 ok_entries=2 rows=21 located_quotes=28 fresh_sources=6`, run with the code's
   constants it prints `entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3`
   — the documented contract measures a different population, one that includes the
   previous round's already-landed entry. Receipts `04-docstring-vs-code.txt` (a
   docstring-vs-code checker reports `bad=3` on the round-84 counter and `bad=0` on the
   round-83 and round-82 counters it was copied from) and
   `06-docstring-constants-measure-differently.txt`. The counter is frozen and its repair
   cannot rescue a scored claim; the fix is prospective — a counter's `Usage` line, base
   list and `ROUND_START` prose must be regenerated from the code in the same commit, and
   a copy-forward check should compare them.

2. **The `url/unreach` form cannot express a 203 cookie-wall.** A well-formed unreach
   record for a 403 row (curl_rc 22, http 403) verifies `OK` (rc 0), but the same form for
   the PubMed rows' `curl_rc=0 http=203` is refused `FAIL REFETCH` (rc 1), because the
   tool's success test is "curl_rc == 0 and http starts with `2`" — and 203 is a 2xx. So
   the round's rejections of S021/S022/S032 as "HTTP 203 cookie-challenge pages, no
   content" are correct in substance but cannot be written as `GATE-RECORD` unreach lines
   under the tool's current contract. Receipt `09-setup-leg-and-versions.txt` and the
   S020/S021 fixtures; capture bytes for both PubMed keys are the 190-byte wall
   "pubmed.ncbi.nlm.nih.gov Cookies must be enabled … HHS Vulnerability Disclosure",
   and neither "survival analysis" nor "living systematic review" occurs in them.
