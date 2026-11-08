# R86ScoutRegistry — round-86 per-surface reconnaissance over the source registry (C2 / K1 scope)

Seat `R86ScoutRegistry`, lane `chousa-shokunin`, wave `round-86/w1`. Leaf seat: no dispatch, no production edits,
no lane/fleet git or jj mutation, no commits or pushes. Every check below reads **committed bytes** of the
landing revision `667a5d091dc46168ed95eda0ae7f19a9bcf139a2` (extracted with
`git -C <lane> archive 667a5d09 | tar -x -C <scratch>`); **no network was used**.

Scratch: `/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry/` (created with `mkdir -p`, deleted before yield).
All receipts cited here are copied into `.ufo/waves/round-86/w1/R86ScoutRegistry/receipts/`.

**Counting rule used throughout §4** (stated because it changes the answer): the citing entry's date is the
entry's own `verified-at:` header when present, else the file's **first commit date in UTC**. The lane commits
in `-0300` local time and its entries declare UTC dates in `verified-at:`, so the local-clock reading is wrong
by one day for late-evening commits. §4b shows the raw local-date reading and why it is an artifact.

**Baseline I ran first** (the counter under test, on the landing tree, no mutation):

```
$ python3 -B <scratch>/corpus/evidence/round86/curation-r86.py --root <scratch>
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
CURATION_R86=PASS
exit 0
```
(receipt: `receipts/counter-blindspots.txt` header block for the unmutated baseline is the same counter file;
the mutation battery below records the mutated runs.)

---

## §1 — Supersession edges in `corpus/SOURCES.md` (rows whose `teaches` opens `supersedes S0NN —`)

**Count: 10 edges** at the landing revision (same 10 as at base `3bfb6885958ad4a674ad1896f70d1e836be609e4`;
2 rows added by the landing commit, S216/S217, are not supersession rows).

Receipt: `receipts/sec1-supersession-edges.txt` — command
`python3 -B receipts/s1.py` (run against the git-archive tree of `667a5d09`).

| # | edge | target status | superseding status | teaches contradiction? |
|---|---|---|---|---|
| 1 | S029 → S019 | queued | mined | **YES** — S019 "deciding to update is a recorded, periodic act" / "assessed on a schedule" vs S029 "this sentence does not prescribe a recorded schedule" |
| 2 | S030 → S022 | queued | queued | **YES** — S022 "the limit case of a short recheck cadence" (asserted) vs S030 "recheck-cadence comparison is a lane inference" |
| 3 | S031 → S024 | queued | mined | **YES** — S024 "a property separate from publication or modification dates" vs S031 "no comparison to other date properties claimed" |
| 4 | S032 → S021 | queued | queued | **YES** — S021 "Findings that need updating appear early …" vs S032 "a signal is not itself an update" |
| 5 | S033 → S020 | queued | mined | **YES** — S020 "time bounds on an entity's validity" vs S033 "entity-lifetime facts, not verification time or truth-validity" |
| 6 | S073 → S070 | mined | mined | teaches agree; **anchor contradicts** (see finding F-1 below) |
| 7 | S176 → S171 | mined | mined | no (explicitly "S171's teaching … stand unchanged") |
| 8 | S200 → S196 | mined | mined | no (S200's text is the QUALITY-147 headline S196 paraphrases) |
| 9 | S201 → S197 | mined | mined | no (S201's text is the QUALITY-146 headline S197 paraphrases) |
| 10 | S202 → S198 | rejected | rejected | no (both are the same rejection, re-anchored) |

### Edges where the superseded row is `mined` while the superseding row is not

**Count: 0 at the landing revision.** The counter's `SUPERSEDED_LIVE` predicate
(`curation-r86.py:90-95`) therefore prints `0`, and the counter's own kill rule K1 is not fired.
For contrast, the same one-liner on the base tree `3bfb6885` prints **1** —
`S031(queued) → S024(mined)` — which is the round-85 inversion the round-86 landing closed
(`S024` mined→queued, `S031` queued→mined; landing commit `667a5d09` diff on `corpus/SOURCES.md`,
and `corpus/lessons/round-86.md`). The landing therefore closes the routed inversion in the
direction the counter tests.

### Edges where the superseding row's `teaches` contradicts the target's

**Count: 5** — edges 1, 2, 3, 4, 5 above. In every one the superseded row's `teaches` cell still asserts
the claim its superseder refuses; the correction is carried only by the *superseding* row's cell (its
`teaches` opens `supersedes S0NN —`), never by a marker inside the superseded row. Because all five
superseded rows are `queued` (not `mined`) at the landing, none of them is a live citation
(all five carry `used-by = —`), so this is a *live-assertion residue in non-live rows*, not an inversion.

**Finding F-1 (anchor contradiction inside a both-mined pair — byte-verified).**
S070 and S073 are the same document (both anchor file SHA-256 `93c17dff…403f`, both
`/usr/share/man/man1/sha256sum.1.gz`; verified on this host: `sha256sum /usr/share/man/man1/sha256sum.1.gz`
→ `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`). Decompressing the committed man page
gives line 11 = `Print or check SHA256 (256\-bit) checksums.` (6 words) and line 20 =
`read checksums from the FILEs and check them` (8 words). But:

- **S070.anchor**: "… SYNOPSIS `-c, --check` (decompressed lines 4–11, 19–20, 54–56; **quote at line 11**)"
- **S073.teaches**: "the anchor label `SYNOPSIS -c, --check` is wrong; lines 19–20 sit under DESCRIPTION.
  **Offsets and quote unchanged**: \"read checksums from the FILEs and check them\" (8 words at **line 20**)"

S073 declares the quote *unchanged* while quoting a different string at a different line than the row it
supersedes. The `.SH SYNOPSIS` line really is line 5 with body 6–7 and no option entries, and `.SH DESCRIPTION`
is line 8 — S073's structural correction is right; its "quote unchanged" clause is not, and S070's anchor
still carries the wrong label. **The counter cannot see this**: `SUPERSEDED_LIVE` requires target `mined` AND
superseding **not** `mined`, so a both-mined pair is out of scope by construction, and the counter never
compares a pair's anchor/teaches cells. Receipt: `receipts/sec1-F1-manpage-anchor.txt` — command
`sha256sum /usr/share/man/man1/sha256sum.1.gz` (→ `93c17dff…403f`, the SHA both rows pin) plus
`gzip -dc … | awk '{printf "%d\t%s\n", NR, $0}' | sed -n '3,22p'` (lines 3–22 of the decompressed page) and
`… | sed -n '11p' | wc -w` / `… | sed -n '20p' | wc -w` (6 and 8 words). The edge list itself is in
`receipts/sec1-supersession-edges.txt` (row 6).

---

## §2 — Normalized-URL groups with ≥2 rows, and contradicting `teaches` within a group

**Count: 207 distinct URL groups; 9 groups hold ≥2 rows.** Normalization: last `https?://…` token in the
`source` cell, lower-cased host, `www.` stripped, trailing `/` stripped, query/fragment dropped.
Receipt: `receipts/sec2-url-groups.txt` — commands `python3 -B receipts/s2.py` and the appended
per-group classifier.

| group | rows | contradicting `teaches`? |
|---|---|---|
| `cochrane.org/…/chapter-iv` | S019 (queued), S029 (mined) | **YES** — recorded schedule vs "does not prescribe a recorded schedule" |
| `docs.python.org/3/library/hashlib.html` | S059 (mined), S074 (rejected) | no — S074 is a *rejection* that explicitly defers to S059 ("S059 already holds this page and digest-input scope"); duplicate scope, not contradiction |
| `docs.python.org/3/library/socket.html` | S052, S053 (both mined) | no — disjoint scopes (timeout vs `create_connection`) |
| `gnu.org/software/coreutils/manual/coreutils.html` | S071, S073, S075 (all mined) | no *within the group* (env `-u` / sha256sum `--check` / `mktemp -d`); see F-1 — the group's real partner **S070 is missing from this group** |
| `pubmed.ncbi.nlm.nih.gov/17638714` | S021 (queued), S032 (queued) | **YES** — "Findings that need updating appear early" vs "a signal is not itself an update" |
| `pubmed.ncbi.nlm.nih.gov/28912002` | S022 (queued), S030 (queued) | **YES** — "the limit case of a short recheck cadence" vs "recheck-cadence comparison is a lane inference" |
| `schema.org/lastReviewed` | S024 (queued), S031 (mined) | **YES** — the refused comparison; this is the round-85 routed defect, closed by the landing (S024 → queued) |
| `w3.org/TR/2013/REC-prov-o-20130430` | S020 (queued), S033 (mined) | **YES** — "an entity's validity" vs "entity-lifetime facts, not verification time or truth-validity" |
| `w3.org/TR/2017/REC-html52-…/syntax.html` | S050, S051 (both mined) | no — disjoint scopes (head end tag vs in-head insertion mode) |

**Groups with contradicting `teaches`: 5 of 9** (the Cochrane ch.iv, both PubMed pairs, schema.org
lastReviewed, and the W3C PROV-O pair). In all five the superseded row is `queued` with `used-by = —`,
so no live citation carries the contradicted text at the landing.

### F-2 — URL grouping misses two same-document pairs that DO contradict

Two pairs share a document but never share a normalized URL, so a URL-grouped contradiction scan cannot see them:

1. **S070 ↔ S073** — same file SHA-256 `93c17dff…403f`, same man page. S070's `source` cell carries only the
   local path (`/usr/share/man/man1/sha256sum.1.gz`, no `http`), so it lands in a `NOURL:` bucket while S073
   carries the canonical `gnu.org/…/coreutils.html#cksum-c` URL and lands in the gnu.org group. The pair's
   contradiction is the F-1 anchor/quote clash.
2. **S020 ↔ S215** — same PROV-O Recommendation, two URL strings: the canonical
   `https://www.w3.org/TR/2013/REC-prov-o-20130430/` (S020, S033) and the alternate
   `https://www.w3.org/TR/prov-o/` (S215, mined, cited by `corpus/knowledge/provenance-recording-r85.md`).
   S215.teaches "…bound the starting and ending moments of an entity's existence" **agrees** with S033 and
   **contradicts** S020's "time bounds on an entity's validity". So the contradiction that the URL grouping
   reports as S020-vs-S033 is also visible as S020-vs-S215 under document identity, and S020 loses on both counts.

**Grouping by document identity instead of URL** (file SHA-256, capture key, or local path — all three
cross-checks run): exactly 2 multi-row identity groups exist — `93c17dff…` → {S070, S073} and
`9b027d02…` → {S066, S069} — plus the local-path groups `sha256sum.1.gz` → {S070, S073},
`grep.1.gz` → {S066, S069, S146}, `recon-run-r70.txt` → {S171, S176}. S066/S069/S146 are disjoint scopes
(grep flags vs `--diff-filter`), and S171/S176 explicitly do not contradict ("S171's teaching … stand unchanged").
**Document-identity groups with a contradicting pair: 1** ({S070, S073}, F-1).

---

## §3 — Mined rows whose `used-by` path does not exist at the landing revision

**Count: 0.** 181 mined rows, 197 `used-by` path references, all 197 resolve to an existing file at
`667a5d09`; no mined row has an empty `used-by`. Widening to every status: 198 paths checked, 0 missing.
Receipt: `receipts/sec3-used-by-paths.txt` — command `python3 -B receipts/s3.py`.

### F-3 — two mined rows point at a file that never names them (dangling citation pointer)

Not a missing path, but the same class of defect one level up, and invisible to the counter
(which never opens `used-by` at all):

```
S174  mined  used-by = corpus/evidence/round71/claims.md   -> that file contains no token "S174"
S175  mined  used-by = corpus/evidence/round71/claims.md   -> that file contains no token "S175"
```
`corpus/evidence/round71/claims.md` names only `S171`, `S173`, `S176` (receipt §3, third block). The two rows'
subject matter *is* in that file (the timeout capability probe and the case-258 D5 ground), but by
prose/control-path reference, not by row id. Severity: low (both rows are mined with correct anchors), but
it means the registry's `used-by` pointer is not a machine-checkable citation edge for these two rows.

---

## §4 — Rows whose `opened` date is later than the first entry that cites them

**Count: 0** under the lane's own UTC convention (entry date = its `verified-at:` header, else first UTC commit).
**Every mined row with a citing entry has `opened` ≤ that entry's date.**
Receipt: `receipts/sec4-opened-vs-first-citation.txt` — command `python3 -B receipts/s9.py`
(the script is also copied as `receipts/s9.py`).

### F-4 — the same check under raw local-clock git dates reports 7 hits, all timezone artifacts

Receipt: `receipts/sec4-opened-vs-first-citation.txt` (second block, `receipts/s7.py`) and
`receipts/sec4b-timezone.txt`:

```
S018, S023, S214  opened=2026-11-08  first citing entry = corpus/knowledge/search-transparency-reporting-r84.md
S046, S047, S048, S049  opened=2026-10-23  first citing entry = corpus/knowledge/quote-reopen-r29.md
```
Both citing entries were committed late in the local evening (`3a17f4da` = `2026-11-07T23:22:58-03:00`,
`30c9d24d` = `2026-10-22T22:47:42-03:00`), so their *author-date* renders as the previous calendar day
while the lane's own `verified-at:` headers say `2026-11-08` and `2026-10-23 UTC` — the r29 entry even
records "local clock 2026-10-22, UTC-3" explicitly. In UTC there is no inversion: **0**.
The registry's `opened` cell for these rows was itself rewritten by the r84 landing (`3a17f4da`) — S018/S023/S214
read `queued | 2026-10-19` / `2026-10-21` at `3a17f4da^` and `mined | 2026-11-08` after — so the current
`opened` values are the re-open dates and are consistent with the entries that cite them.

---

## §5 — Defects the frozen C2 counter cannot see (mutations on a scratch copy)

Receipt: `receipts/counter-blindspots.txt`, produced by `receipts/mutate-counter-blindspots.py`
(each mutation applied to a fresh copy of the landing tree; the frozen counter is then run against that
copy; nothing under the lane repo is touched).

| id | mutation | observed line | exit | reads |
|---|---|---|---|---|
| M1 | re-mine `S024` while `S031` stays mined (both-mined inversion) | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS` | 0 | **counter blind** |
| M2 | r85 entry's `source:` and Q7 re-pointed from `S031` to the superseded `S024` | same green line / `CURATION_R86=PASS` | 0 | **counter blind** |
| M3 | delete the literal `supersedes S024 —` marker from S031's `teaches`, re-mine `S024` | same green line / `CURATION_R86=PASS` | 0 | **counter blind** |
| M4 | reword the marker to `S024 is corrected here:`, re-mine `S024` | same green line / `CURATION_R86=PASS` | 0 | **counter blind** |
| M5 | delete Q13 (the `modified` Definition quote) from the r84 entry | `MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19` / `CURATION_R86=FAIL` | 1 | counter fires (as designed) |
| M6 | put `modification` into the r85 row-6 Never cell | `UNENTAILED_TERM=1` / `UNENTAILED corpus/knowledge/provenance-recording-r85.md row=Recording when content was last reviewed term=modification` / `CURATION_R86=FAIL` | 1 | counter fires (as designed) |
| M7 | restore the round-85 inversion (S024 mined, S031 queued) | `SUPERSEDED_LIVE=1` / `SUPERSEDED_STILL_LIVE S024 is mined while S031 supersedes it and is queued` / `CURATION_R86=FAIL` | 1 | counter fires (as designed) |

Reading of these, with the counter's own bytes as the evidence:

- **M2 is the sharpest.** The frozen claim's kill rule K4 says the round-85 entry must cite `S031`
  ("the round-85 entry cites the superseded `S024` instead of `S031`" is a K4 violation). The counter **cannot
  detect that**: `S024` and `S031` carry the same URL, so `capture_text()` resolves both to the same capture
  (`11d6cc56bb24adfc61eea2b4`), the quote still locates (`QUOTES_LOCATED=20/20`), and the K4 violation is
  invisible. K4 is asserted in prose but has no counter arm.
- **M3/M4** show the supersession relation is detected purely by a string-prefix regex
  (`re.match(r"supersedes (S\d{3,}) —", teaches)`, `curation-r86.py:90`). Any re-worded, re-punctuated or
  relocated marker loses the edge. The edge is currently triple-encoded in 4 rows (`S073` also in `anchor`,
  `S200`/`S201`/`S202` also in `source`), so the redundancy exists but is not read by the counter.
- **M1** is the disclosed narrowing: the plan records that the pre-freeze bytes counted *every* edge whose
  target was mined (5 on the base tree) and were narrowed to the live-vs-unadopted form because two-row
  histories where both rows are `mined` are legitimate (`corpus/QUALITY.md:1112`, criterion 174). The
  consequence is that the counter cannot distinguish the repaired state (S024 queued) from a both-mined
  re-inversion (S024 mined, S031 mined) — M1. That is a scope limit of the instrument, not a defect in the
  landed bytes, and it is disclosed; it is reported here because the claim text ("no row that a later row
  supersedes is `mined` while the superseding row is not") is narrower than a reader may assume.
- **M5/M6/M7** confirm the three arms the counter *does* own are live on this tree (a dropped Definition
  quote, an unentailed defect term, and the restored inversion each fail the run).
- **Two further scope limits read from the counter's bytes** (no mutation needed):
  (a) `parse_registry` keeps a row only if it splits into exactly 11 cells
  (`curation-r86.py:44-48`), so any row whose cell contains a literal `|` is dropped from the registry map
  entirely — its supersession edge and status pair vanish silently. **0 such rows today** (all 217 rows split
  into 11 cells; receipt `sec1`/`s2` both re-derive 217).
  (b) `MODIFIED_DEF_CITED` is computed over the *located quotes* of either entry
  (`curation-r86.py:137-140`), independent of the decision table's Warrant cell — so it is satisfied by the
  quote's presence, not by row 9's warrant pointing at it. M5 shows the dependency is on quote presence.
- **F-1 restated:** the counter has no arm that compares a supersession pair's anchor/teaches cells, so the
  S070/S073 "quote unchanged" contradiction (§1, F-1) is invisible even though the underlying man page is
  byte-verifiable from the host's own file (SHA-256 pinned identically in both rows).

---

## Counts at a glance

| section | question | count |
|---|---|---|
| §1 | supersession edges (landing) | 10 |
| §1 | edges with superseded `mined` + superseding not `mined` | **0** (base `3bfb6885`: 1) |
| §1 | edges whose superseding `teaches` contradicts the target's | **5** |
| §1 | both-mined edges with an anchor/teaches contradiction | **1** (F-1, S070↔S073) |
| §2 | normalized-URL groups | 207 (9 with ≥2 rows) |
| §2 | ≥2-row groups with contradicting `teaches` | **5 of 9** |
| §2 | document-identity groups with a contradicting pair | **1** (F-2, S070↔S073) |
| §3 | mined rows with a non-existent `used-by` path | **0** (197 paths checked) |
| §3 | mined rows whose `used-by` file never names the row | **2** (F-3, S174/S175) |
| §4 | mined rows with `opened` later than the first citing entry (UTC) | **0** |
| §4 | same, raw local-clock git dates | 7 — all timezone artifacts (F-4) |
| §5 | counter blind spots demonstrated (M1–M4) / arms confirmed live (M5–M7) | **4 / 3** |

## Remaining unknowns (not resolved by this seat)

- Whether the five §1 teaches contradictions are *intended* to persist in `queued` rows (the r25 note says
  "Original broader teachings remain as superseded history, not unmarked current advice") or are an
  unclosed residue. The registry's own convention points the first way; the r85 routed defect points the
  second way for S024/S031 specifically.
- Whether F-1's "quote unchanged" clause in S073 is a transcription slip or a deliberate re-pointing of the
  anchor. The bytes of the man page are pinned identically in both rows, so the file cannot distinguish them.
- Whether the `used-by` pointer is contractually required to name the row id (S174/S175 point at a file
  that describes their subject without naming them; `corpus/QUALITY.md` criterion 6 constrains the *entry's*
  `source:` header, not the registry's `used-by` back-pointer).

## Tooling

No tool was installed, upgraded or removed this round; no `pacman`, `uv tool`, `npx` or `cargo install` was
run. Everything used was already on the host: `git`, `python3` (3.x, stdlib only), `gzip`, `sha256sum`,
`grep`, `awk`, `sed`, `tar`. Channel / version / reason: not applicable — no install was needed for any check.

## Scratch cleanup

`/fast/scratch/hyaku/chousa-r86/R86ScoutRegistry/` (tree extract, base extract, man-page working copy, all
mutation copies, analysis scripts) was removed before this report was yielded; every receipt cited above was
copied into `.ufo/waves/round-86/w1/R86ScoutRegistry/receipts/` first.

VERDICT: R86ScoutRegistry C2 held — at the landing revision no superseded row is `mined` while its superseding row is not (0/10 edges), all mined `used-by` paths exist (197/197), and no mined row's `opened` postdates its first citing entry under the lane's UTC convention (0), while five superseded `queued` rows still assert the claim their superseder refuses and S070's anchor contradicts S073's "quote unchanged" on the pinned man page (byte-verified, counter-invisible).
VERDICT: R86ScoutRegistry C1 n/a — this seat ran no C1 battery and makes no C1 claim.
