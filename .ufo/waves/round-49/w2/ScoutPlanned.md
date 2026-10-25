# ScoutPlanned — round-49 wave-2, bounded round-50 data walk

seat: ScoutPlanned (scout, leaf — no subagents, no background jobs, no installs).
date: 2026-10-25 · lane `chousa-shokunin` · network: none (L0 `8d77e6c1` open; every
source read is an on-disk `.qcache` capture). Writes: this report only. Scratch
`/dev/shm/chousa-r49-ScoutPlanned` deleted.

**Item attacked:** the round-50 plan the lane froze for itself —
`SCORECARD.md:2588-2590` ("adopt the next same-theme package entry
`cnki-citation-check-r40.md` with an NCPSSD help-page row") — plus the walk the item
asks for: which un-adopted same-theme / next-theme candidates `merge/chousa/` holds and
which three are most adoptable. No frozen predicate, target or counter is proposed for
change.

## 1. Population

```
$ ls /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/ | wc -l   → 55
$ ls /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/ | wc -l          → 71
```
8 staged entries are already in the lane (`aggregator-vs-source-r36`,
`citation-count-semantics-r37`, `claim-support-test-r37`+amendment,
`evidence-archive-field-policy-r41`, `evidence-pool-versioning-r39`+amendment,
`evidence-snapshot-coverage-r40`) → **47 un-adopted**; plus 3 staged files that are
*amendments* to lane entries (`citation-version-binding-r36`/`-r37`,
`search-log-method-r39`; `MERGE-REPORT.md:56` "append, do not replace"). Lane registry
now holds S001–S103, no gaps (S096–S103 = this round's eight appends). Merge ids are
S082–S195; the S082–S095 collision is already resolved on disk
(`corpus/lessons/round-49.md:52-63`), so round 50 renumbers by document, from S104.
Capture key verified: `sha256("https://support.nii.ac.jp/ja/cir/manual_articles_detail")[:24]`
= `09fc63de41f293d43d631c46` = the capture named for lane row S096. ✓

## 2. The walk — 47 candidates

`cap` = captures under `.qcache` at `sha256(url)[:24]`; `reg` = absent-defect register
row on that URL (register ids are **campaign** ids, not merge ids — match by URL:
register `S096` = merge `S101` = lane S101); `form` = decodable form. `.md` omitted.

| candidate(s) | staged ids | cap | reg | form |
|---|---|---|---|---|
| cnki-citation-check-r40 / -query-r47 / -matching-modes-r42 / -public-surface-r43 / -comparison-basis-r46 | S124,S180,S149,S160,S175 | 5/5 | – | PDF,PDF,HTML,HTML,HTML |
| citation-check-status-vocabulary-r48 / citation-matching-semantics-r41 / istic-citation-verification-r39 | S187,S135,S136,S145,S118 | 5/5 | – | PDF,PDF×3,HTML |
| chinese-search-log-r37 (+amendment) | S102,S103,S104,S111,S112 | 5/5 | – | PDF×3,HTML×2 |
| search-log-fields-r36 / search-tracking-record-r40 | S082,S083,S090,S134 | 4/4 | **S077** | HTML×3,PDF |
| japanese-search-record-r38 (+amendment) / japanese-prisma-item-wording-r40 | S109,S110,S125,S126,S129 | 5/5 | **S104,S105,S120** | PDF×4,HTML |
| chinese-search-record-r39 / chinese-prisma-s-access-r41 | S116,S117,S119,S141 | 4/4 | **S111,S112,S114** | PDF×2,HTML×2 |
| grey-literature-and-chinese-search-record-r40 / -r41 / -field-boundary-r43 / -field-china-r42 / -mandate-scope-r48 / -national-route-r44 | S130,S131,S133,S142,S161,S155,S156,S157,S190,S168,S169 | 11/11 | **S125** | **OLE**,HTML×6,PDF×4 |
| source-type-taxonomy-r36 / -r37 | S085,S086,S093,S101 | 4/4 | **S080,S088,S096** | HTML×2,PDF,**OLE** |
| chinese-regulator-guideline-currency-r41 / chinese-document-status-fields-r42 / reachability-route-map-r42 / abolition-instrument-form-r42 | S143,S144,S147,S150,S154,S158,S151,S148,S152,S153 | 10/10 | – | HTML×7,PDF×3 |
| repeal-instrument-class-r43 / repeal-decision-series-r44 / dated-compilation-as-currency-r47 / regulator-mandate-vs-centre-silence-r47 | S159,S165,S166,S167,S178,S179,S184,S176,S177 | 6/9 | – | HTML×6,PDF×2,**no capture**,local file |
| quality-control-guideline-issued-text-r48 / regulator-register-scopes-r48 / national-centre-publication-record-r46 / nmpa-document-classes-r45 | S185,S186,S190,S188,S174,S173 | 5/6 | – | PDF×3,HTML×2,local file |
| chinese-journal-open-delivery-r43 / -issue-toc-r44 / -issue-placement-r45 / -doi-and-printed-contents-r47 | S162,S163,S164,S172,S181,S182,S183 | 7/7 | – | PDF×4,HTML×3 |
| prisma-s-route-without-doi-r48 / prisma-s-identifier-routes-r49 / online-first-address-routes-r50 / western-instrument-alignment-r50 | S189,S191,S192,S194,S193,S195 | 2/6 | – | local×3,HTML,PDF |
| chain-resolution-r3-amendment | S105–S108 | 0/4 | – | lane-local artifacts |

20 chousa register rows (all `payload-absent`) touch **8** candidates' URLs. Five sit on
this round's *theme* URLs and already carry an `absent-as-written` verdict
(`corpus/lessons/round-49.md:111-125`: register S082, S084, S086, S095, S096); the other
15 touch no round-50 candidate URL, so a round-50 lesson needs verdicts only for its theme.

**OLE (2 candidates).** `bdff491a75c6abeda1d9c01d` (S130 gcpunion `.doc`) and
`6dc68fd6b32ce9c8dfcebce8` (S101 jc.hit `.doc`): both `.raw` heads = `d0cf11e0a1b11ae1`
(OLE2); their `.txt` sidecars are lossy — `read_text.find` = −1, count 0/0, for all five
S101 quotes. Read as `open(raw,'rb').read().decode('utf-16le')` per
`corpus/lessons/round-49.md:68-70`. ✓

## 3. Two defects a round-50 adopter inherits

**(a) Id-token danger — 13 of 47 candidates.** The round-49 C2 control failed because
staged ids name lane rows of *other* documents. Live sets: `chinese-search-log-r37`
(S071,S072,S079,S101 — in lane-namespace S071/S072/S079 are the GNU `env`/`bash`/rfc7089
rows and S101 the jc.hit `.doc`; the sentence means PRISMA-S/Cochrane/J-stage,
`chinese-search-log-r37.md:55-72`), `cnki-citation-check-r40` (S076,S109,S111),
`search-tracking-record-r40` (S069,S094,S114,S130), `cnki-citation-check-query-r47`
(S119,S170 — S170 names the HDPR paper in the merge package, not the CNKI privacy policy
the sentence means; that is S175), `citation-check-status-vocabulary-r48` (S119),
`grey-literature-and-chinese-search-record-r40` (S097,S114),
`regulator-mandate-vs-centre-silence-r47` (S125,S152), `source-type-taxonomy-r37` (S075),
`japanese-prisma-item-wording-r40` (S097), `japanese-search-record-r38-amendment` (S097),
`chain-resolution-r3-amendment` (S073,S078,S084), `chinese-search-log-r37-amendment`
(S091,S092,S093), `chinese-search-record-r39` (S097).

**(b) The package's own `used-by` correction was not absorbed.**
`MERGE-REPORT.md:98-104` states S102/S103 point at *two* entries
(`citation-count-semantics-r37.md, chinese-search-log-r37.md`); the landed rows say one:
```
$ grep -E '^\| S10[23] ' corpus/SOURCES.md | awk -F'|' '{print $2,"||",$(NF-1)}'
 S102  ||  corpus/knowledge/citation-count-semantics-r37.md
 S103  ||  corpus/knowledge/citation-count-semantics-r37.md
```
So `chinese-search-log-r37.md` — the one candidate two of whose three sources are
already lane rows (S102 = toho-shoten PDF, S103 = UM PDF) — lacks the pointer the
package expected the lane to carry.

## 4. Grounding — the candidates' own quotes in their captures

Every quoted span (backtick/「」/“”/"") ≥8 chars of the candidate, located in that
candidate's own capture text form (`q` = quoted spans, `grounded` = located):
```
cnki-citation-check-r40       q= 8 grounded= 2   (S124 PDF)
cnki-citation-check-query-r47  q= 1 grounded= 0   (S180 PDF)
cnki-matching-modes-r42        q= 1 grounded= 0   (S149 HTML)
cnki-public-surface-r43        q= 2 grounded= 0   (S160 HTML)
cnki-comparison-basis-r46      q= 1 grounded= 0   (S175 HTML)
citation-check-status-vocabulary-r48 q=1 grounded=0 (S187 PDF)
chinese-search-log-r37         q= 2 grounded= 0   (S102/S103/S104 PDF)
source-type-taxonomy-r37       q= 6 grounded= 3   (S093 PDF, S101 OLE)
search-log-fields-r36          q= 7 grounded= 1
reachability-route-map-r42     q= 4 grounded= 4
search-tracking-record-r40     q=11 grounded= 5
```
The CNKI cluster grounds weakly **because the PDF wraps lines**: in
`e3ca8f4fdd15420b80096a75.txt`, `'状态共分为三种类型' in txt` → **False** (split
`状\n态共分为三种类型` at 30947); `没找到` occurs once at 30952. A round-50 span must pick
quotes surviving the wrap, or the byte-exact rule (`build-spans.py:127`) refuses.

## 5. Ranking — the three most adoptable

1. **`cnki-citation-check-r40.md`** — the plan's own pick. One source (S124), one capture
   (`e3ca8f4fdd15420b80096a75`, PDF+`.txt`+`.raw`), **no register row**, entry already
   narrowed in the package. Costs: 3 dangerous tokens to re-point (S076/S109/S111) and
   re-picking quotes around the PDF wrap. Its document is the *same* file as staged
   S135/S180/S187, so one lane row unblocks four package entries.
2. **`cnki-citation-check-query-r47.md`** — same document (S180 → the same capture as #1),
   no register row, and it is a *correction* of a prior over-claim (round 12's "CNKI does
   not publish how 引文核对 forms its query"), which is actionable. Costs: 2 dangerous
   tokens (S119; S170→S175). Binding it with #1 needs one lane row.
3. **`cnki-matching-modes-r42.md`** — one source (S149), no register row, **no dangerous
   tokens**, and its terms locate: `相关度匹配` @17618, `精确匹配` @17711, `模糊匹配` @17773 in
   `625375f640d6eb3be0990ef2.txt`. But it is **out of theme**: the round-49 lesson rejected
   it this round (`corpus/lessons/round-49.md:151-153`, "a different feature from citation
   counts"), flip = "a frozen question about CNKI's search-platform matching taxonomy".
   Adoptable only if the L1 freezes that question. Same-cost next-theme alternative:
   `cnki-comparison-basis-r46` (S175) or `cnki-public-surface-r43` (S160).

**Flag to the planner:** `chinese-search-log-r37.md` is mechanically cheapest (two of three
sources already lane rows S102/S103, §3b) and is the entry the package re-pointed
S102/S103 to — but it is **not same-theme** (Chinese search log; and it is the target of
round-49's refused NCPSSD document) and its prose carries 4 dangerous tokens. Not a
round-50 pick without a rewrite.

## 6. The live hazard in the plan as written

`SCORECARD.md:2590` plans "an NCPSSD help-page row". That capture is
`c4e1446a42d0a709c34097be` = `sha256("https://ncpssd.org/service/help?mainTitle=%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98")[:24]`
(reproduced from that URL). Two facts an adopter must not inherit:

1. **Its `.raw` is byte-identical to its `.txt`** (45,308 bytes, UTF-8+BOM, 664 CRLF).
   The lesson's S100/S101 rule (`.raw` = OLE → UTF-16LE) does **not** apply: UTF-16LE
   decoding gives mojibake (`'믯\u0dbfഊഊഊ…'`). Only UTF-8 is readable.
2. **The offset convention differs.** The lesson cites the two quotes at `24872` and
   `25269` (`corpus/lessons/round-49.md:120`) — those are **`utf-8-sig`**-decoded char
   offsets. The lane's span convention (`build-spans.py` `form_texts` →
   `read_text(encoding="utf-8")`, universal newlines) puts the same quotes at **24557** and
   **24954** (664 CRLF→LF collapses). Every anchor the lane has written (S096–S103) is
   `read_text`-side: S097 `char 2760` = `read_text.find` 2760, while its `utf-8-sig` offset
   is 2953. Cross-check over all 31 span rows: **31/31** have `offset + span.find(quote)`
   equal to a `char N` in their row's anchor cell, and that equals `read_text.find` for the
   22 `.txt`-form rows and `utf-16le.find` for the 9 `.raw`-form rows; the `utf-8-sig`
   reading coincides with only **12/31** — exactly the 12 rows whose capture has no CRLF,
   where the conventions cannot differ. Copying the lesson's offsets into an anchor cell
   yields an anchor that does not locate its quote under `c2-count.py:187-188`
   (`all(c in offsets.get(r[0], set()) …)`).

This is a calibration defect in the round-49 lesson's NCPSSD paragraph (no bound row
carries those offsets — the NCPSSD row was refused), not in C1 or C2.

## 7. Not done

No claim/predicate/counter/registry/entry/lesson modified — the only write is this
report. No live fetch; no network egress. I did **not** run `c1-count.py`/`c2-count.py`
(other seats' items) and did **not** test entailment — only capture availability, form,
register status, id-token safety, quote locatability and the offset convention.

VERDICT: ScoutPlanned (round-50 planning data walk over the 47 un-adopted
`merge/chousa/` entries) — holds — every candidate's capture, register and id-token
facts re-derive from disk, the three most adoptable are `cnki-citation-check-r40.md`,
`cnki-citation-check-query-r47.md` and `cnki-matching-modes-r42.md` (the last
out-of-theme unless its flip question is frozen), and the plan's NCPSSD help-page row
must re-derive its `char N` anchors in the lane's `read_text` convention
(24557/24954), not the lesson's `utf-8-sig` offsets (24872/25269).
