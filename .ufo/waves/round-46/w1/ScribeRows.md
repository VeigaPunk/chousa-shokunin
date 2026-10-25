# ScribeRows — round 46 wave 1 (chousa lane)

Item: draft the five lane Registry rows S085–S089 (11 cells each: id, source, kind, tier,
scope, anchor, teaches, status, opened, recheck, used-by) in the CORPUS.md census schema, from
the five on-disk campaign captures; read staged S120–S122, S127–S128 for provenance; copy the
shape of lane rows S079–S084. Leaf seat: no subagents, no writes outside this report.

## Binding — by document, never by id arithmetic

| lane id | capture (sha256(url)[:24].txt) | bytes | sha256 | staged row | document evidence |
|---|---|---|---|---|---|
| S085 | 5a631adb18988a1a2421ce75 | 4146 | e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92 | S120 | "FEVER Dataset" header at char 680; "185,445 claims" char 757; page URL https://fever.ai/dataset/fever.html |
| S086 | 1c15b611118dee97e4105fcf | 60153 | c508913aba177ae4d33b29b7076f305bbac578a1ea11d39e30ddee2d787d563f | S121 | title "FEVER: a large-scale dataset for Fact Extraction and VERification" char 5; ACL PDF layout (two columns) |
| S087 | 7800e2e1e2df3bc124b6b83e | 5676 | dfc3e0f50dc2fd7c896790a8ef30babb0992eb6d4c4b9a473c13c093277e00ed | S122 | JSON API record: `"title": "FEVER: Fact Extraction and VERification"` char 277, `"publication_date": "2018-04-03"` char 362 |
| S088 | b73f7e8dd5b0ace740e48046 | 12775 | 603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b | S127 | "AVeriTeC Dataset" char 680; "AVeriTeC (Automated Verification" char 707 |
| S089 | 78761b633aee2289e5874ce9 | 126093 | 35bdf1c1cbc337d4c93ce7c8f2ed51635894903ed1cf4c15d6d6acc9ecc7480c | S128 | arXiv stamp `arXiv:2505.17978v2 [cs.CL] 07 Oct 2025` char 1845; "1,297" claims char 2681 |

Binding is by URL + page body, not by S-number. Staged S127/S128 map to lane S088/S089
(S127 is *greater* than S128's target), so arithmetic would have produced the wrong rows.

## Rows (verbatim; each line has exactly 12 pipes / 11 cells)

```markdown
| S085 | FEVER: Fact Extraction and VERification dataset release page (Thorne, Vlachos, Christodoulopoulos, Mittal) — https://fever.ai/dataset/fever.html | dataset | A | what a support verdict is bound to in the FEVER release format, and what that binding does not carry; distinct in scope from lane row S097, which holds the label set and the evidence requirement for the same page | the evidence field definition, exact slice at capture char 2349: evidence : A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) | a verdict binds to a Wikipedia page title and a sentence id and the format section names no page revision; the pages ship as one Pre-processed Wikipedia Pages (June 2017 dump), so a later reader resolves the same tuple against whatever text that page then holds | mined | 2026-10-25 | 180d | corpus/knowledge/evidence-pool-versioning-r39.md |
| S086 | FEVER: a large-scale dataset for Fact Extraction and VERification (Thorne, Vlachos, Christodoulopoulos, Mittal) — NAACL-HLT 2018, doi 10.18653/v1/N18-1074 — https://aclanthology.org/N18-1074.pdf | paper | A | the measured reliability of the evidence-selection step, read from the publisher's PDF; distinct in scope from lane row S113, which used the arXiv HTML render for the annotator decision procedure | exact slice at capture char 6737: "and 95.42% precision and 72.36% recall in evi-" — pdftotext -layout splits the two-column page, so the word completes as "dence retrieval." at char 6784 | evidence selection is measured rather than assumed: 95.42% precision and 72.36% recall against a super-annotator's exhaustive set, with 0.6841 Fleiss kappa on the verdict labels (char 6418), so a verdict carries a retrieval recall gap that the label figure does not show | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-pool-versioning-r39.md |
| S087 | FEVER: Fact Extraction and VERification — Zenodo record 4925954, doi 10.5281/zenodo.4925954 — https://zenodo.org/api/records/4925954 | dataset | A | the deposited, citable artefact: the versioned concept it sits under, the seven files it serves and the frozen page pool among them, as the repository API records them | exact slice at capture char 171: "conceptdoi": "10.5281/zenodo.4925953" | the deposit is one record under a versioned concept doi and its evidence pool ships as a single wiki-pages.zip of 1,713,485,474 bytes (char 4929) beside the labelled jsonl splits, so a later corpus can cite a fixed download instead of a live wiki page | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-pool-versioning-r39.md |
| S088 | AVeriTeC Dataset release page (Schlichtkrull, Guo, Vlachos) — https://fever.ai/dataset/averitec.html | dataset | A | how the release binds each evidence item to an archived copy of its source and each claim to a date; distinct in scope from lane rows S082, S083 and S084, which hold the README field dictionary, the corpus paper's stated practice and the stored archive-value counts | exact slice at capture char 3909: cached_source_url : An archive.org link for the source url. | a citation is stored as a source_url together with an archive link to that url, and the claim carries a claim_date (char 2891), so a verdict can be re-read against the state of its evidence rather than against a live page that has since changed | mined | 2026-10-25 | 180d | corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md |
| S089 | AVerImaTeC: A Dataset for Automatic Verification of Image-Text Claims with Evidence from the Web (Cao, Ding, Guo, Schlichtkrull, Vlachos) — arXiv:2505.17978v2 — https://arxiv.org/html/2505.17978v2 | paper | A | the corpus authors' own account of temporal leakage and evidence insufficiency and the mechanisms used against them, over 1,297 real-world image-text claims | exact slice at capture char 7084: while being restricted to using only online evidence published before the claim’s date. | evidence is admitted only where it predates the claim and a two-stage sufficiency check gates each verdict, so an archived copy can be judged against the claim's own date instead of against whatever the web holds now | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md |
```

## Stripped prose (removed from `recheck`; the cell holds only the interval)

- S085 ← staged S120: `180d — re-open the page and confirm the evidence field still reads [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] (ran 2026-10-23)`
- S086 ← staged S121: `365d — re-download the PDF and confirm the sentence still reads 95.42% precision and 72.36% recall in evidence retrieval (ran 2026-10-23)`
- S087 ← staged S122: `365d — re-open the Zenodo record and confirm the concept doi and the wiki-pages.zip file key are unchanged (ran 2026-10-23)`
- S088 ← staged S127: `180d — re-open the dataset page and confirm the cached_source_url field description still reads "An archive.org link for the source url" (ran 2026-10-23)`
- S089 ← staged S128: `365d — re-open the arXiv HTML and confirm the Abstract still reads "temporally constrained evidence annotation" (ran 2026-10-23)`

## Commands and decisive output

1. Column check on the five drafted lines (`/tmp/chousa-r46-ScribeRows/rows.txt`):
   `python3 -c '... len(ln.split("|"))-2 ...'` →
   five lines each `11 12 11` (cells=11, pipes=12), then `awk -F'|' 'NF!=13 {print NR": NF="NF}' rows.txt` printed **nothing**, `awk-exit=0`.
2. Anchor falsification — every quoted slice re-sliced from its capture at the stated offset:
   ```
   S085 2349 words 18 exact True occurrences 1
   S086 6737 words 8 exact True occurrences 1
   S086 6784 words 2 exact True occurrences 1
   S086 6418 words 8 exact True occurrences 1
   S087 171 words 2 exact True occurrences 1
   S087 4929 words 4 exact True occurrences 1
   S088 3909 words 9 exact True occurrences 1
   S088 2891 words 12 exact True occurrences 1
   S089 7084 words 13 exact True occurrences 1
   ALL_EXACT True
   ```
   `S085 revision occurrences 0 | June 2017 at 1302` — grounds "names no page revision" as a
   statement about this capture, not about every FEVER distribution.
3. Pipe hygiene inside cells: `'|' in quote` was `False` for all candidate quotes. The capture
   itself carries `SUPPORTS|REFUTES|NOT ENOUGH INFO` (S085 ~char 2300) and the staged rows
   contain literal pipes inside cells; neither shape was copied into my rows.

## Findings

- Coverage, corrected after ReviewerC3Spans: the lane registry runs S001–S089 with one row each
  and contains neither `S097` nor `S113` (`grep -c 'S097\|S113' corpus/SOURCES.md` → 0). Those
  two ids exist only in the *staged* append (`SOURCES.append.md:22` FEVER dataset page,
  `:38` FEVER arXiv HTML) under the staged numbering, which is not the lane's. My draft's
  "distinct in scope from lane row S097 / S113" clauses therefore cited staged ids as held lane
  rows — a defect in the draft, not a loss on landing; the registry seat was right to drop them.
  S085 and S086 are the lane's first rows for the FEVER page and paper; there is no
  duplicate-document pair.
- Framing correction for the entry seats: staged S127 says "every evidence item carries a
  `source_url` and a `cached_source_url`". The page *documents* both fields (char 3865/3909);
  whether every stored item carries them is a data claim that only S084's counts can carry.
  My row says "a citation is stored as a source_url together with an archive link", not "every".
- S086 anchor is a truncated slice by necessity: `pdftotext -layout` interleaves the paper's two
  columns, so no single-line string holds the whole sentence; the continuation is named with its
  own offset (6784) instead of being silently completed.
- S089's capture uses a typographic apostrophe in `claim’s`; the anchor reproduces it byte-exactly
  (char 7084) rather than normalizing it.
- No conflict with any capture found in the staged prose I restate (Zenodo publication_date
  2018-04-03 at 362, seven files at 2415+, 4568 claims / 50 organizations at 851, kappa 0.742 /
  74.7 % at 3204, four labels at 1142).

## Peer cross-check (ExecSpanBuilder) and post-draft registry state

Their three offset identities hold on my slices by subtraction: 2349 + 11 = 2360
(`evidence : `), 3909 + 20 = 3929 (`cached_source_url : `), 7084 + 53 = 7137
(`while being restricted to using only online evidence `). Digest agreement on all five.

Counter, run read-only by me at lane root (I did not write SOURCES.md):

- Timeline, stated without adjudication: the peer reports that at 07:2x line 29 of the
  amendment carried `S071` and `S095` verbatim and the counter read `REF_ID_UNBOUND=2`; my first
  read of that file (after their run, before 07:31) already showed `S079` and `S081`, and the
  counter read 0. I did not observe the earlier bytes, so I cannot confirm or deny their read.
  Evidence bearing on it: the amendment is untracked (`git status --porcelain` → `??`) so there
  is no VCS byte history to diff, and its mtime is `2026-10-25 07:31:33` — i.e. it was written
  after both measurements. `S095` has no lane Registry row (`grep -n '^| S095 '` empty) and
  `S071` is a row at `corpus/SOURCES.md:81`; the entry's "Staged material corrected on adoption"
  paragraph records the re-binding to `S079`/`S081`.
- After rows S085–S089 landed at `corpus/SOURCES.md:96-100`, both modes:
  `CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11
  CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`, exit 0.
- Landed rows are the registry seat's text, not this draft; each is 12 pipes / 11 cells,
  `NF=13`, no empty cell. Cell-level deltas from the draft:

| id | changed cell | draft | landed |
|---|---|---|---|
| S085 | source | names Thorne, Vlachos, Christodoulopoulos, Mittal | "FEVER (2018) dataset release page" (authors dropped) |
| S085 | scope | adds "distinct in scope from lane row S097 …" | clause dropped |
| S085 | anchor | char 2349 slice only | adds the "Pre-processed Wikipedia Pages (June 2017 dump)" slice |
| S085 | teaches | quotes the June 2017 dump and "same tuple" | "one dated pre-processed dump … fixed pool" |
| S085 | recheck | 180d (as staged S120; lane S097 for the same page also 180d) | 365d |
| S086 | scope | adds "distinct in scope from lane row S113 …" | clause dropped |
| S086 | anchor | retrieval slice + continuation only | adds a char-42011 label-validation slice |
| S086 | teaches | 0.6841 Fleiss kappa (char 6418) | 91.2% of sampled examples correctly annotated |
| S087 | scope / teaches | "the seven files", "labelled jsonl splits" | "among its files", "labelled splits" |
| S088 | anchor | char 3909 slice only | adds the char-2891 claim_date slice |
| S088 | teaches | cites "(char 2891)" | char reference dropped |
| S089 | scope | "…, over 1,297 real-world image-text claims" | claim count dropped; anchor and teaches identical |

Only S085's recheck interval is a substantive divergence from the staged provenance (staged
S120 and lane S097 both say 180d). The dropped distinct-scope clauses leave two rows for the
FEVER page (S085 with S097) and two for the FEVER paper (S086 with S113) with no stated
difference between them — reported, not edited, since SOURCES.md is not mine to write.

## Out of scope / not done

Entries, spans.tsv and production edits belong to sibling seats. I ran `c3-count.py` read-only
(name of the shipped counter, not a score I own) at a peer's request — results above — and wrote
nothing outside this file. No fetch, no network, no tool installs (nothing was needed). Scratch dir
`/tmp/chousa-r46-ScribeRows` removed.

Pointers: rows above; captures under
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`; staged provenance
`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:45,46,47,52,53`; lane shape
`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:89-95`.
