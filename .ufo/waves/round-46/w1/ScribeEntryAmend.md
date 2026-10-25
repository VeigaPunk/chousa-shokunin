# ScribeEntryAmend — round 46 wave 1 (chousa C3, amendment entry)

item: draft the lane's re-grounded `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`
(S088 AVeriTeC page, S089 AVeriMaTeC paper), grounded on the two on-disk captures; report staged
byte/reference defects; no production edit, no fetch, no dispatch.

verdict: **draft complete and pass-verified** against the frozen C3 predicate in a scratch mirror
(`C3=PASS`, exit 0, both modes). The production file at report time is a *different* draft written by a
sibling; it also passes the counter. Four assignment-level gaps remain in it (F2). I wrote no lane file.

## Commands and decisive output

1. `sha256sum`/`wc -c` on both captures (read-only):
```
12775 .../b73f7e8dd5b0ace740e48046.txt   603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b
126093 .../78761b633aee2289e5874ce9.txt  35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c
```
`sha256(url)[:24]` reproduces both filenames (S088 averitec page, S089 2505.17978v2).

2. Offset/token verification against the captures (every offset the draft cites, asserted as a slice):
```
OK 1064 classified into four labels
OK 2904 Our best estimate for the date the claim first appeared
OK 3077 If the claim first appeared on the internet, a url to the original location
OK 3185 Where possible, an archive.org link to the original claim url
OK 3929 An archive.org link for the source url
OK 5285 https://web.archive.org/web/20230323135844/https://en.wikipedia.org/wiki/Hunter_Biden
OK 9375 "answer_type": "Unanswerable"      OK 9407 "source_url": ""
OK 2928 contextual dependence, temporal leakage, and evidence insufficiency
OK 3001 claim normalization, temporally constrained evidence annotation, and a two-stage sufficiency check
OK 3022 temporally constrained evidence annotation
OK 7137 published before the claim’s date
OK 14547 To ensure long-term accessibility, all source pages are archived on the internet archive.
OK 20073 restricted to dates prior to the claim date
OK 42465 to retrieve online evidence published prior to the claim date
OK 42537 the exact dates of a small portion of claims ( 5 % 5\% ) were unavailable
OK 3200 κ = 0.742   OK 3239 74.7 %   OK 3253 consistency on QA pairs   OK 7615 free-marginal
offset-bad: 0
```
3. Apostrophe leg (the required report-both case):
```
"before the claim's date" - -        (ASCII U+0027: ABSENT from both captures)
'before the claim’s date' - S089     (U+2019: present in the S089 capture)
'74.7%' - -                          (no space: ABSENT)
'74.7 %' - S089                      (space: present)
```
4. `python3 corpus/evidence/round46/c3-count.py` on the lane **as first read** (sibling's draft):
```
ENTRIES=2/2 CITES_BOUND=0/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11 REF_ID_UNBOUND=2 REF_BOUND=2/2 C3=FAIL   exit=1
```
`REF_ID_UNBOUND=2` = the staged ids `S071` and `S095` were still inside that draft. The file changed
under me afterwards (unexpected sibling write); **at report time** the same command prints
`CITES_BOUND=5/5 REF_ID_UNBOUND=0 ... C3=PASS`, `exit=0`.
5. Scratch mirror (`/tmp/chousa-r46-ScribeEntryAmend/root`: real `spans.tsv`+`spans/`, real base entry,
   my draft as the amendment, real `SOURCES.md` plus five synthetic S085–S089 `mined` rows placed
   inside `## Registry`): `c3-count.py --root <scratch>` → `ENTRIES=2/2 CITES_BOUND=5/5
   QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11
   REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`, exit 0; `--lane-only` identical with
   `CAPTURE_BOUND=skipped`, exit 0. The registry rows are the only synthetic part (ExecRegistryMirror owns them).
6. Two falsifiers of my own draft (same mirror): curly→ASCII → `QUOTES_IN_ENTRY=10/11 C3=FAIL`
   exit 1; reintroducing one disallowed id → `REF_ID_UNBOUND=1 C3=FAIL` exit 1.

## Draft (re-grounded amendment)

```markdown
# The later corpus answers the durability question per citation: an archived copy and a dated claim

source: S088 — https://fever.ai/dataset/averitec.html — the "AVeriTeC Dataset" header paragraph (char 1064, the four-label sentence) and the Data Format field list (chars 2904, 3077, 3185 and 3929); build `refs/heads/live build 385`, `Last updated: 2026-04-02T10:58:13.945736`
source: S089 — https://arxiv.org/html/2505.17978v2 — the Abstract's method sentence (char 3022), the archive-practice sentence (char 14547), the evidence-restriction sentences (chars 7137, 20073 and 42465) and the annotation-consistency figures (chars 3200 and 3239); arXiv:2505.17978v2 [cs.CL] 07 Oct 2025
verified-at: 2026-10-25
recheck: 365d — re-open the dataset page and the arXiv HTML; confirm the two cached-field descriptions, the claim-date description, the archive-practice sentence and the evidence-date sentences are unchanged (both captures re-opened 2026-10-25, no fetch)
ground: the open half of the durability question. The base entry shows that a FEVER verdict is made durable by freezing one dated pool, so what binds a verdict's *individual* citations, and at what date? The later AVeriTeC corpus answers with an archive link per cited URL and a date on the claim, and AVeriMaTeC states the date constraint as a rule. **This entry continues `corpus/knowledge/evidence-pool-versioning-r39.md` by path** — the lane now holds both, the FEVER release entry and this AVeriTeC/AVeriMaTeC amendment — and it adds to the base entry without replacing it. Opened from on-disk captures; no fetch.

#### Observation

- **An evidence answer pairs a live URL with an archived copy.** Evidence answers carry a `source_url` and a `cached_source_url` described as "An archive.org link for the source url" (S088, char 3929), and the worked supported example shows `https://en.wikipedia.org/wiki/Hunter_Biden` beside `https://web.archive.org/web/20230323135844/https://en.wikipedia.org/wiki/Hunter_Biden` (S088, char 5285). The pairing is documented practice rather than a schema invariant: the capture's one answer marked `"answer_type": "Unanswerable"` carries `"source_url": ""` and no archive field (S088, char 9375).
- **The claim's own location is paired the same way, but only as a best effort.** `original_claim_url` applies "If the claim first appeared on the internet, a url to the original location" (S088, char 3077), while `cached_original_claim_url` is "Where possible, an archive.org link to the original claim url" (S088, char 3185).
- **The claim carries a date.** `claim_date` is "Our best estimate for the date the claim first appeared" (S088, char 2904).
- **The page states four labels, and the capture wraps one of them.** Claims are "classified into four labels" (S088, char 1064): `Supported`, `Refuted`, `Not Enough Evidence`, `Conflicting Evidence/Cherry-picking`. The third label is split across two lines in this capture, so no contiguous four-label sentence is quoted here.
- **The later paper states the archive practice in its own words.** "To ensure long-term accessibility, all source pages are archived on the internet archive." (S089, char 14547). It does not restate the field dictionary: `cached_source_url` occurs zero times in the S089 capture and `archive.org` once, as a footnote URL (sweep: `grep -c cached_source_url` prints 0, `grep -c archive.org` prints 1; S089).
- **The later paper states the date constraint as a mechanism and as a pipeline rule.** It mitigates "contextual dependence, temporal leakage, and evidence insufficiency" (S089, char 2928) through "claim normalization, temporally constrained evidence annotation, and a two-stage sufficiency check" (S089, char 3001); annotators were given search bars "to retrieve online evidence published prior to the claim date" (S089, char 42465), and the interface's returned pages are "restricted to dates prior to the claim date" (S089, char 20073), with the annotated evidence kept "published before the claim’s date" (S089, char 7137).
- **The paper reports its own agreement figures, as rendered tokens.** It reports a "free-marginal" κ = 0.742 on verdicts and 74.7 % consistency on QA pairs (S089, chars 3200, 3239 and 3253). The capture interleaves each figure with its LaTeX source, so the lane quotes the tokens and not the rendered sentence.

#### Inference

- **The durability answer here is per citation, and it is an archived copy rather than a revision id.** AVeriTeC fixes the state of each cited page with an archive link stored beside the live URL (S088); the base entry's FEVER release instead fixes one pool by dump and binds each verdict to a URL plus a sentence id inside it. The per-citation field is the finer instrument, and it costs one extra value per evidence answer (S088).
- **The claim's date is what makes the archive binding mean something, and it is a claim property, not an evidence property.** AVeriTeC dates the claim (S088) and the later pipeline admits evidence only from before that date (S089), so the pair — archived copy plus claim date — is what excludes a source that post-dates the claim; an archive link alone would not, because an archived copy of a later page is still a later page (S088, S089).
- **This is the instrument the lane already holds for its own sources, applied one level finer.** RFC 7089 (`S079`) makes an archived state addressable by date, and the NDL E2867 WARP note (`S081`) puts the capture timestamp in the URL itself; AVeriTeC applies that route per citation rather than per corpus (S088).
- **The lane's byte pin answers a different question, and the missing part is a time field.** The lane's `sha256` pin fixes the bytes of the file it read (`corpus/knowledge/revision-binding-r31.md`), and the lane's own archive entry records that its byte hash is not a point-in-time anchor (`corpus/knowledge/citation-version-binding-r37.md`). The corpus-side answer is to store the point in time beside the citation (S088), which is a value the lane's claim record does not carry.
- **The fourth label is a support state the lane's chain mode has never had.** `Conflicting Evidence/Cherry-picking` (S088) is a claim-level judgement over evidence items pointing different ways, and the later paper says it follows the same four-way schema (S089), so the state is not a peculiarity of the 2024 release.

#### Unknown

- **The archive values are conditional, and a null is not a count.** The supported and refuted examples carry `"original_claim_url": null` beside the same null cache field (S088), so the null case in this capture is a claim with no original URL to archive, not a claim that appeared online and lost its snapshot. How often either case occurs is not measured here; the count by value over the training split is `corpus/knowledge/evidence-snapshot-coverage-r40.md`, and the field reading is `corpus/knowledge/evidence-archive-field-policy-r41.md`.
- **Whether the archived capture is the state the annotator read is not established by either source.** The archive link carries its own timestamp, and neither document says it matches the annotation moment or that a later capture could not differ from the one read (S088, S089).
- **The date constraint has a stated hole.** "the exact dates of a small portion of claims ( 5 % 5\% ) were unavailable" (S089, char 42537), and those claims were dated from their fact-checking article instead (S089), so the constraint is only as good as the claim date.
- **No evidence-selection recall figure for this corpus was read in either capture.** The base entry's weaker-link argument therefore gets no successor number here, and the lane's own `sha256` pin is not a substitute for one (S088, S089).
- **Staged material corrected on adoption, byte level.** The staged sentence wrote the possessive with an ASCII apostrophe (U+0027) where the capture has a right single quotation mark (U+2019), so the lane quotes the capture's bytes at char 7137. The staged label enumeration inserted a conjunction between the last two labels that the capture's sentence does not contain (S088, char 1064). The staged ellipsis spliced a date phrase from one sentence onto wording from another; the two contiguous tokens are quoted separately (S089, chars 7137 and 20073). The staged read of the null example asserted a claim that first appeared on the internet; the capture's null example has `original_claim_url` null as well (S088).
- **Staged material corrected on adoption, reference level.** Two prose ids from other campaign numbering were re-bound by document: RFC 7089 is lane `S079` and the NDL E2867 WARP timestamp-in-URL note is lane `S081`. The staged pointer to a lane amendment id this lane never held was replaced by the lane path `corpus/knowledge/citation-version-binding-r37.md`, which is where the byte-hash-is-not-a-time-anchor point actually sits (S088).
```

## Findings

- **F1 — staged defects, each located.** (a) ASCII `before the claim's date` absent from both captures;
  capture has U+2019 at S089 char 7137. (b) Staged four-label sentence joins the last two labels with
  "and"; the capture has no `, and "Conflicting` (checked, false) and wraps `Not` / `Enough Evidence`
  across lines; the contiguous tokens exist separately, the joined sentence does not. (c) Staged
  "74.7%": the capture renders `74.7 % 74.7\%`, so the no-space form is absent. (d) Staged read of the
  null archive as "claims that first appeared on the internet" is inverted: the null example carries
  `"original_claim_url": null` too (S088). (e) Staged "limited ... to those published before the
  claim's date" splices two different sentences.
- **F2 — production file at report time (`sha256 20509f13…`, sibling-authored) passes the counter but
  keeps four assignment-level gaps the counter does not measure.** line 21: Inference bullet citing
  only `S079`/`S081`, no S088/S089. line 15: `74.7%` (not verbatim; capture `74.7 %`). line 28:
  "AVeriTeC is text-and-image claims" — neither capture says this of AVeriTeC (S089 says it of
  AVeriMaTeC, `1,297 real-world image-text claims`, char 2681). line 29: attributes the
  byte-hash-is-not-a-time point to `citation-version-binding-r36.md`; the literal statement is r37
  line 17 ("a version anchor the lane's byte hash is not"), r36 states the converse. My draft uses r37.
- **F3 — new grounding the staged entry lacked.** S089 states the archive practice itself at char 14547
  ("all source pages are archived on the internet archive"), and states the constraint's hole at char
  42537 (5 % of claim dates unavailable). Both are now cited; the staged entry cited neither.
- **F4 — CITES_BOUND depends on registry rows S085–S089** (`status=mined`, `used-by` the entry path,
  inside `## Registry`); the scratch rows are synthetic placeholders, not evidence. ExecRegistryMirror owns them.
- **Out of scope / not done:** no network fetch; no lane production file, index or jj touched; no
  subagents; no tool installs (nothing needed). Scratch tree `/tmp/chousa-r46-ScribeEntryAmend/` deleted.

## Pointers

- Draft: `/tmp/chousa-r46-ScribeEntryAmend/draft.md` — sha256 `e17d9ec81a77daf8d00e19f1c6619bda1973dd57952fababfc33a246f39ff7b7` (deleted with scratch; text is above).
- Captures: `…/.qcache/b73f7e8dd5b0ace740e48046.txt` (sha256 `603f9b42…528b`), `…/78761b633aee2289e5874ce9.txt` (sha256 `35bdf1c1…480c`).
- Manifest rows I must match: `corpus/evidence/round46/spans.tsv:9-12` (S088 ×2, S089 ×2).
- Counter: `corpus/evidence/round46/c3-count.py` — `CROSS_REFS` at :52, pass expression at :148-150 and :153-155.
- Phrase precedent read for "continues by path": staged base ground `…/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md:9`; lane ground-line voice `corpus/knowledge/citation-version-binding-r36.md:6`.
- Production file inspected (not edited): `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`, sha256 `20509f1366e360c212cd5e1191f9500b34b9f62445293ad37a22e473a87ba16a`.

Report: .ufo/waves/round-46/w1/ScribeEntryAmend.md
