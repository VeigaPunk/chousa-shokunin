# R84ScoutNovelty — round-84 seat report

Seat: scout (novelty / ground). Lane: chousa-shokunin. Read-only reconnaissance, two surfaces:
(1) C2 K4 (ground), (2) S017 disposition. No lane writes; no git/jj mutation; no network GETs
(my item names no re-open URL, so I fetched nothing).

Base `408ae68f9e445fc911f713d5bbb3a64dda1ab9fe` · landing `03bbb4580b39b442be69f998fae2db48d64b8c93`.
Scratch `/fast/scratch/hyaku/chousa-r84/R84ScoutNovelty/` (deleted on yield). Receipts cited below are copied
into `.ufo/waves/round-84/w1/R84ScoutNovelty/receipts/`.

---

## Surface 1 — C2 K4 (ground): is the new entry on un-cited ground?

### 1.1 K4 as frozen at the landing revision — HELD (no kill)

K4 (frozen): *"a base-list entry (`base-knowledge.txt`) cites S214, S018, or S023 or contains their URLs."*

Command and observed result (receipt `receipts/k4-ground.txt`):

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -E 'S214|S018|S023' \
      408ae68f9e445fc911f713d5bbb3a64dda1ab9fe -- corpus/knowledge
exit_code=1                      # no hits

$ git -C ... grep -n -E 'S214|S018|S023' \
      03bbb4580b39b442be69f998fae2db48d64b8c93 -- corpus/knowledge
exit_code=0                      # hits, all inside corpus/knowledge/search-transparency-reporting-r84.md
                                  #   :3  source: S214, S018, S023
                                  #   :22-33  the twelve Located-quote rows
                                  #   :39-49  the eleven decision-table rows
                                  #   :64  a Limits bullet naming S018
```

The three URLs, checked at both revisions:

```
$ git -C ... grep -n -F 'https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf' <rev> -- corpus/knowledge
exit_code=1   (rev 408ae68)      exit_code=1   (rev 03bbb45)
$ git -C ... grep -n -F 'https://aclanthology.org/2026.acl-long.1430/' <rev> -- corpus/knowledge
exit_code=1   (rev 408ae68)      exit_code=1   (rev 03bbb45)
$ git -C ... grep -n -F 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/' <rev> -- corpus/knowledge
exit_code=1   (rev 408ae68)      exit_code=1   (rev 03bbb45)
```

**No base-list entry cites S214, S018 or S023, and no base-list entry contains any of the three URLs, at
either revision.** The only hits at the landing revision are inside the new entry itself, which is by
definition not in the base list. A partial-URL sweep (`PRISMA_2020_checklist|aclanthology\.org/2026\.acl-long\.1430|dublincore\.org|dcmi-terms|1430`)
over `corpus/knowledge` at the base revision returned one unrelated hit
(`sweeps-rejections-r5.md:97`, the source-code line number `:1397-1430`).

**K4 does not fire.** The frozen counter agrees on its own E7 leg: with the pinned base list, the entry
passes E7 and the counter prints `fails=-`:

```
$ python3 -B corpus/evidence/round84/depth-r84.py --root <landing tree>
ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-
DEPTH_R84 entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3
DEPTH_R84=PASS
rc=0
```

### 1.2 The same ground, in content — PARTIALLY ALREADY TAUGHT (novelty finding, not a K4 kill)

The K4 rule is a *citation* test (S-id / URL). The *teaching* ground overlaps more than the rule notices.
Base entries already teach PRISMA-2020 search reporting from translated copies of the same checklist —
Japanese (`corpus/knowledge/japanese-prisma-item-wording-r40.md`, S116) and Chinese
(`corpus/knowledge/chinese-prisma-s-reception-r52.md`, S114). Verbatim from the base revision:

- `corpus/knowledge/japanese-prisma-item-wording-r40.md:12` — *"**Item 6 (情報源) names five source
  classes and the advice taken.** `すべてのデータベース，研究登録，Web サイト，組織，文献リスト` (char 475) … The
  next sentence adds the date: `それぞれの情報源が最後に調べられた日付を記載する` (char 592)."*
- `corpus/knowledge/japanese-prisma-item-wording-r40.md:13` — *"**Item 7 (検索戦略) names the strategy, its
  filters and limits, over three source classes.** `用いたフィルターや制限も含め，` (char 641) … `試験登録，Web
  サイトの完全な検索戦略を記載する` (char 753)."*
- `corpus/knowledge/japanese-prisma-item-wording-r40.md:19` — *"**The two search items ask for sources,
  their dates and a strategy, not for a searcher.**"*
- `corpus/knowledge/chinese-prisma-s-reception-r52.md:13` — *"**Item 6 names the source classes and asks
  for each source's date.**"* … `:14` — *"**Item 7 asks for the complete strategy with its filters and
  limits.**"*
- `corpus/knowledge/search-tracking-record-r40.md:12,13,14` — the PRISMA-S per-source count and the
  flow-diagram column allocation.

**Reading:** the new entry's rows 1–3 (Q1/Q2/Q3 — sources searched, when last searched, full strategy with
filters and limits) restate **PRISMA 2020 checklist items 6 and 7**, which the lane already holds in
Japanese and Chinese. The genuinely new content is rows 4–5 (items 8 and 16a — the *English* wording of
the selection-method and search-results items; the base's Japanese copy only mentions item 8 as a reviewer
count, `japanese-prisma-item-wording-r40.md:14`), plus the whole S018 block and the whole S023 block
(`git grep -i -E 'evidence-based text generation'` → rc=1 at base; `git grep -i -E 'dublin|dcmi|dcterms'` →
rc=1 at base, i.e. the DCMI ground is untouched by any base entry).

So the ground is **new by citation** (K4 holds) but **not new by subject for rows 1–3**. This is a
depth/novelty observation for the wave's reviewer; it is not a K4 kill under the frozen wording, and I do
not claim one.

### 1.3 A note on the entry's own framing (not a K4 kill)

`corpus/knowledge/search-transparency-reporting-r84.md:10` says *"Held entries say how a query is built
(`search-query-exposure-r51.md`, `search-query-templates-r54.md`) …"*. Neither file has ever existed in this
lane:

```
$ git log --all --pretty=format: --name-only | sort -u | grep -cE 'search-query-exposure-r51|search-query-templates-r54'
0
$ git cat-file -e 408ae68f...:corpus/knowledge/search-query-exposure-r51.md   → MISSING at base
$ git cat-file -e 03bbb458...:corpus/knowledge/search-query-templates-r54.md → MISSING at landing
```

The only occurrence of either name anywhere in the repo is this entry's own line 10. The lane's held
query-construction ground is thin — `git grep -n -i -E 'query template|building a query|query construction'`
over base `corpus/knowledge` returns rc=1 (no hits) — but the *names* it cites for it are dangling. Also
`:10` cites `PROTOCOL.md` §4–§6; `PROTOCOL.md` exists only at the **fleet root**
(`/home/vgpnk/Projects/shokunin/PROTOCOL.md`), not in the lane (`git cat-file -e 03bbb458...:PROTOCOL.md` →
not in lane), and it has **no numbered sections** (`grep -cE '^#+ *[0-9]+[.)] '` → 0; its `##` headings are
Round-robin rounds / Evidence standard / Gate standard). The lane's own method doc is `SKILL.md`. And the
Inference section's `corpus/logs/` path has never existed (`git log --all --name-only | grep -c '^corpus/logs'`
→ 0). Cosmetic-to-the-counter, but these are unsupported references in a landed entry.

---

## Surface 2 — S017 disposition

### 2.1 Does the S017 landing capture carry an 8–25 word quote about search reporting? NO.

`corpus/captures/259c96bf7088a12bc7ce65c4.txt` is 2,895 chars. Keyword counts (receipt
`receipts/s017-disposition.txt`): `search` 0, `databas` 0, `registr` 0, `websit` 0, `organis` 0,
`reference list` 0, `strateg` 0, `last searched` 0, `filters` 0 — only `checklist` 5, `flow diagram` 3,
`item` 4. Sentence scan for 8–25-word units returns **0** sentences. The whole capture's prose is nav
chrome plus three long lines (87w / 40w / 9w) describing what PRISMA 2020 *is*:

> "PRISMA 2020 consists of a statement paper , which includes a description of how the reporting guideline
> was developed and presents a checklist of items and sub-items, an expanded checklist that details
> reporting recommendations for each item/sub-item, an abstract checklist , and template flow diagrams for
> original and updated reviews."

That 87-word blob does contain a quotable 17-word span (*"presents a checklist of items and sub-items, an
expanded checklist that details reporting recommendations for each item/sub-item"*) — but it says what the
checklist **is**, not what a search record must report, and it is not the 8–25-word located quote the
counter requires of a decision row's warrant. **The "no quotable checklist text" rationale for reverting
S017 is factually correct.** The checklist-page capture
`corpus/captures/1f5f4eec0b85edf1dc53db7b.txt` is the same story (29 non-empty lines, all nav; the only
two URLs are `https://creativecommons.org/licenses/by/4.0/` and `https://prisma.shinyapps.io/checklist/`).

### 2.2 Does the PDF (now S214) carry the items? YES.

```
$ grep -n -i -E 'Specify all databases|date when each source|full search strategies|methods used to decide whether|results of the search and selection' \
      corpus/captures/a640b15abf781e5c583d7088.txt
17:Information              6    Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies. Specify the
18:sources                       date when each source was last searched or consulted.
19:Search strategy          7    Present the full search strategies for all databases, registers and websites, including any filters and limits used.
20:Selection process        8    Specify the methods used to decide whether a study met the inclusion criteria of the review, including how many reviewers screened each record
53:Study selection      16a    Describe the results of the search and selection process, from the number of records identified in the search to the number of studies included in
exit_code=0
```

### 2.3 Is the S017→S214 split correct? YES, and the mechanism checks out — with three observations.

The split is **forced** by the counter's `fresh()` (`depth-r84.py:135`, verified by `grep -n 'def fresh'`): a registry row is fresh only if
its **first http(s) URL** hashes to a capture key that exists, with a matching refetch row
(`curl_rc` 0, http 2xx, `fetched_utc` ≥ ROUND_START, `txt_sha256` = sha256 of that capture) whose
`used-by` names the entry. S017's registry URL is the **landing page**
(`https://www.prisma-statement.org/prisma-2020`), whose key `259c96bf7088a12bc7ce65c4` is the nav-only
capture — so S017 could never hold the PDF's quotes, and registering the PDF under its own URL was the
only way to land them. Verified independently: `sha256("https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf")[:24]`
= `a640b15abf781e5c583d7088` = the capture filename, and the refetch row's `txt_sha256` matches sha256 of
that file for all three admitted rows (S018 `248b43277f376e437a356909`, S023
`f5545a194c06ab421875b047`, S214 `a640b15abf781e5c583d7088`).

S017's registry row is byte-identical at base and at landing — `status=queued`, `used-by=—`, `opened=2026-10-19`.
Across **all** history the S017 row's status value has only ever been `queued` (`git log --all -p --
corpus/SOURCES.md | grep '^+| S017 '` → single unique value `queued`). So "reverted to queued" is a slight
overstatement: S017 was **never mined**; it was fetched and left queued. The disposition is right; the
verb is not. There is **no `GATE-RECORD` for S017 in any lesson** (`grep -rn 'GATE-RECORD S017' corpus/lessons/`
→ no hits), while the lesson records only S214/S018/S023 — consistent with a never-admitted source, but it
means the S017 fetch is recorded only in `refetch.tsv`.

**Observation A — the PDF was fetched twice.** `refetch.tsv` carries the checklist PDF twice: once under id
`S017` at `2026-11-08T02:14:35Z`, and again under id `S214` at `2026-11-08T02:21:13Z`, same URL, same key
`a640b15abf781e5c583d7088`, same `txt_sha256`. The egress table allows "one GET per attempt … more than 3
attempts per URL" — two attempts is within the letter — but the second GET exists only so the S214-keyed
refetch row exists for the counter's `fresh()`. The counter's freshness test needs the refetch row keyed by
`(id, url)` = `(S214, <pdf url>)`; the S017-keyed row at 02:14:35 cannot satisfy it. The extra fetch is a
mechanical requirement of the counter, not a scope violation.

**Observation B — the lesson's link story is not in the captured bytes.** `corpus/lessons/round-84.md:15` (verified by `grep -n 'checklist page linked to the PDF'`)
says *"S017's landing page was fetched first and reverted; the checklist page linked to the PDF."* The
checklist-page capture contains **zero** occurrences of `PRISMA_2020_checklist-ab3g` and only two URLs
(creativecommons, prisma.shinyapps.io) — it links the PDF by anchor text (`PRISMA 2020 checklist ( PDF ,
Word )`), not by a captured href. The PDF's URL was located by the lesson's recorded **search query**
(*"PRISMA 2020 checklist pdf prisma-statement.org"*), which the lesson does state; the *link* claim is the
part the capture does not support.

**Observation C — the egress table's intended-target list covers one URL of the five fetched.** The table
(`corpus/evidence/round84/egress-approval.md:25-27`) has a single intended-target row:
`S017 (re-open) | https://www.prisma-statement.org/prisma-2020`. The other four fetched URLs — the
checklist page, the checklist PDF (×2), the ACL anthology page, the DCMI terms page — are **absent from
the intended-target table** (verified `grep -qF` per URL → only the landing page is `IN-TABLE`). The table's
scope row does allow "open of a public research-method document … located by search", so the fetches are
arguably inside the *scope*; but the lesson's `## Gate` sentence *"every URL appears in
`corpus/evidence/round84/egress-approval.md`'s intended-target table, committed before the first fetch"*
(`corpus/lessons/round-84.md:13`) is **not** true of that table — only of the scope table. The commit-time
ordering itself does hold: the egress table commits at `2026-11-07T23:11:05-03:00` (= `2026-11-08T02:11:05Z`),
the first fetch is `2026-11-08T02:13:58Z` — 2m53s later.

---

## Cross-cutting: the frozen predicate set was amended after the freeze

This bears on both surfaces and is the most consequential thing I found. The frozen claim file and the
frozen base list were **both edited after the freeze commit**, in the same commit that fetched the sources
and landed the entry.

**1. `claims.md` changed between the freeze and the landing.** `sha256` at freeze `3b616420` is
`f6f032a6f1d40292…`; at landing `03bbb458` it is `19d68274b82d3f90…` (the pin file
`corpus/evidence/round84/instrument-pins.txt` pins the **landing** value, and that pins file was itself
created at the landing rev, `03bbb458` — *after* the edit). The diff moves C2's ground from S017 to
S214/S018/S023, rewrites K4 from *"cites S017 or contains its URL"* to *"cites S214, S018, or S023 or
contains their URLs"*, and changes C1's fresh-positive count from six to five and `RC=3/3` to `RC=4/4`.
The K4 rewrite is *wider* (three S-ids instead of one), so it is not a tightening in the candidate's favour
— but the frozen predicate set is not frozen, and the diff should be read by the wave.

**2. `base-knowledge.txt` changed between the freeze and the landing.** At freeze `3b616420` it is 94 lines
(sha `b457155bec3773fd…`); at landing it is 95 lines (sha `67bd637845d7aa94…`). The added line is
`appraisal-judgment-records-r83.md`. **That one line is load-bearing for C2's predicate**, because the
counter treats any file not in the base list as a candidate new entry. Measured, same landing tree, same
counter, only the list differs:

```
$ python3 -B <landing tree>/corpus/evidence/round84/depth-r84.py --root <landing tree>   # freeze-time 94-entry list
ENTRY appraisal-judgment-records-r83.md ok=no rows=10 quotes=0/16 fails=E3,E6
ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-
DEPTH_R84 entries=2 ok_entries=1 rows=21 located_quotes=12 fresh_sources=3
DEPTH_R84=FAIL
rc=1
```

With the landing's own 95-entry list the same tree prints `entries=1 ok_entries=1 … DEPTH_R84=PASS rc=0`.
So **the amendment is required for the PASS**, and the frozen counter's own docstring still describes the
*old* anchor: `depth-r84.py:9` says the base list is *"corpus/evidence/round83/base-knowledge.txt (the
knowledge set at 8fff80ee, the round-83 egress commit)"*, and `appraisal-judgment-records-r83.md` did
**not** exist at `8fff80ee`
(`git cat-file -e 8fff80ee:corpus/knowledge/appraisal-judgment-records-r83.md` → absent; it was added at
`81b81173`, which *is* in the base rev `408ae68f`). The 95-entry list matches the base rev exactly (95 `.md`
files at `408ae68f` ↔ 95 list lines, set difference empty both ways) — so the **amendment is the correct
fix**, and the counter's docstring is the stale artifact. I verified the amended list does not smuggle the
candidate's own ground: the added file's `source:` line is `source: S009, S212, S213`, it contains **none**
of the twelve new quotes (0/12), and it contains none of the three URLs.

**3. The `c1-d0-donothing` before-control does not reproduce the claims' stated "Before" line.** The claims
say the before-control at base prints `entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0`. The
committed receipt `corpus/evidence/round84/controls/receipts/c1-d0-donothing.txt` prints
`entries=1 ok_entries=0 rows=10 located_quotes=0 fresh_sources=0` — because at the freeze tree the *tree's
own* 94-entry list still makes the r83 entry look new. The receipt is honest about what it ran; the frozen
sentence does not describe it. Reproduced both ways at the freeze tree `3b616420`:

```
freeze tree + freeze-time list (94) → ENTRY appraisal-judgment-records-r83.md ok=no … fails=E3,E6
                                       DEPTH_R84 entries=1 ok_entries=0 rows=10 … FAIL   rc=1
freeze tree + pinned list      (95) → DEPTH_R84 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0
                                       DEPTH_R84=FAIL                               rc=1
```

The committed receipt's `at REV` line also names the *control* rev (`d047cd8d`), not the base rev it says
"tree at base" — it was re-run at `d047cd8d` after `BASE_REV` was added to the runner.

**4. `run-controls-r84.sh` changed between freeze and landing** (sha `3a8dcbf24773eb45…` → `2a20115c278dce78…`):
`BASE_REV` and `mkbase` were added, `c1-d0` moved to the base rev, and `c2-k0` switched from "tool absent" to
the pre-repair `81b81173` tool. The claims file at landing describes the *new* `c2-k0` (*"pre-repair tool
`81b81173` → FAIL, EXPECTED_CODE 262/288"*) — the freeze-time claims described *"tool absent → FAIL"*.
The counters themselves (`depth-r84.py`, `gate-records-r84.py`) and `c2-positives.tsv` are **byte-identical**
freeze → landing (sha unchanged), so the instruments were not touched; the *inputs* to them were.

**Controls reproduce.** Re-running the committed runner with my own scratch
(`HYAKU_SCRATCH=/fast/scratch/hyaku/chousa-r84/R84ScoutNovelty bash corpus/evidence/round84/run-controls-r84.sh
03bbb4580b39b442be69f998fae2db48d64b8c93 <out>`) gives **9/9 as expected**, `CONTROLS_AS_EXPECTED=9/9`, rc 0
(receipt `receipts/controls-summary.txt`). The `c1-d0` receipt reproduces the committed text byte-for-byte
except the scratch path.

---

## Findings summary

| # | Finding | Evidence | Severity |
|---|---|---|---|
| 1 | C2 **K4 holds** — no base-list entry cites S214/S018/S023 or contains their URLs, at base or landing | `receipts/k4-ground.txt`; git grep rc=1 at both revs | no kill |
| 2 | Rows 1–3 restate PRISMA 2020 items 6–7, already taught in Japanese (S116) and Chinese (S114) at base | `japanese-prisma-item-wording-r84.md:12,13,19`; `chinese-prisma-s-reception-r52.md:13,14` | novelty, not K4 |
| 3 | Entry line 10 cites two files that never existed (`search-query-exposure-r51.md`, `search-query-templates-r54.md`) and `PROTOCOL.md` §4–§6 (fleet-root file, no numbered sections) | `git log --all --name-only | grep -cE …` → 0 | unsupported refs |
| 4 | S017 landing capture has **no** 8–25-word quote about search reporting (0 such sentences; `search`/`databas`/`registr`/`strateg` all 0) → the revert rationale is correct | `receipts/s017-disposition.txt` | confirms claim |
| 5 | S017 was **never mined** in any revision (status always `queued`), so "reverted to queued" is inaccurate wording; disposition itself correct | `git log --all -p -- corpus/SOURCES.md` → single value `queued` | wording |
| 6 | The checklist PDF was fetched twice (S017-keyed 02:14:35Z, S214-keyed 02:21:13Z); the second is required by the counter's `fresh()` `(id,url)` keying | `refetch.tsv` rows 162 and 173 | within egress letter |
| 7 | Lesson says "the checklist page linked to the PDF"; the checklist-page capture contains no PDF href (0 hits for `PRISMA_2020_checklist-ab3g`; only 2 URLs, neither the PDF) | `corpus/captures/1f5f4eec0b85edf1dc53db7b.txt` | unsupported claim |
| 8 | Lesson says "every URL appears in the egress table's **intended-target** table"; that table has 1 row (the landing page) while 5 URLs were fetched — true only of the scope table | `egress-approval.md:25-27`; per-URL `grep -qF` | unsupported claim |
| 9 | **Frozen `claims.md` was edited after the freeze** (sha `f6f032a6…` → `19d68274…`), rewriting C2's ground, K4's target set and C1's fresh-positive count | `diff` freeze→landing; `git log --oneline --ancestry-path` | frozen-set integrity |
| 10 | **Frozen `base-knowledge.txt` was edited after the freeze** (94→95 lines, adding `appraisal-judgment-records-r83.md`); the added line is **load-bearing** — with the freeze-time list the landing tree FAILS (`entries=2 ok_entries=1`, rc 1) | side-by-side counter runs, above | frozen-set integrity |
| 11 | The added base-list entry makes the counter's own docstring stale (`depth-r84.py:16` still names `8fff80ee`, where the file did not exist); the 95-entry list matches the base rev exactly | `git cat-file -e 8fff80ee:…` → absent; set difference empty | docstring stale |
| 12 | The committed `c1-d0-donothing` receipt prints `entries=1 rows=10`, not the claims' stated `entries=0 rows=0`; the receipt's `at REV` names the control rev, not the base rev | receipt file vs `claims.md:90-91` | before-leg mismatch |
| 13 | `run-controls-r84.sh` changed after the freeze (`3a8dcbf2…` → `2a20115c…`); the counters and `c2-positives.tsv` did **not** | sha comparison | instruments vs inputs |
| 14 | Controls reproduce 9/9 (`CONTROLS_AS_EXPECTED=9/9`, rc 0) on my own scratch | `receipts/controls-summary.txt` | pass |

**Tools:** none installed or upgraded. Everything ran on the stock host (`git`, `python3`, `grep`, `bash`);
no network was used (my item names no re-open URL). No tool/version/channel table is required.

**Unresolved / not mine to settle:** whether the post-freeze edits to `claims.md` and `base-knowledge.txt`
were authorised by the L1 integrator (I did not look for an authorisation record outside the lane's history),
and whether finding 2 is disqualifying under a K3 reading — that is the wave reviewer's call, not a scout's.

VERDICT: R84ScoutNovelty C2 held — K4 does not fire (no base-list entry cites S214/S018/S023 or their URLs at either revision), though rows 1–3 restate PRISMA items 6–7 already held in Japanese and Chinese.
VERDICT: R84ScoutNovelty C2 held — the S017 landing capture carries no 8–25-word quote about search reporting, so the revert to `queued` is correct in substance (S017 was never mined, so "reverted" is loose wording) and the S214 PDF split is forced by the counter's `fresh()` URL-keying.
