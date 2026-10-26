# R52ConnSiblings — sibling-overlap scan (round 52 w1)

Seat work: grep every sibling lane (`*-shokunin` under the fleet root,
skipping `chousa-shokunin`; surfaces `corpus/`, `tools/`, `SKILL.md`,
`PROVINCE.md`; all read-only) for `docx`, `word/document.xml`, `OOXML`,
`zipfile`, `w:t`, `python-docx`, `pandoc`, `文献検索`, `检索报告`, `PRISMA`,
`search record`, `search log`; verdict on overlap with chousa holding
`tools/capture-text.py` and the three round-52 staged entries (S125 NIPH
`.docx`, S129 Japanese PRISMA checklist, S111/S112 Chinese PRISMA-S
reception). No tools installed (none needed; RULES.md read).

## Commands run (grep tool, case-insensitive unless noted)

```
[grep A] full set: 20 corpus dirs + 8 tools dirs + 18 SKILL.md + 20 PROVINCE.md
pattern: docx|word/document\.xml|OOXML|zipfile|w:t|python-docx|pandoc|文献検索|检索报告|PRISMA|search record|search log
→ 153+ files hit; bulk is the generic `## Search log` registry heading (see §3);
  no OOXML tooling hit.

[grep B] tools-only (8 dirs): docx|word/document\.xml|OOXML|w:t|python-docx|pandoc
→ NO MATCHES.

[grep C] SKILL.md-only: docx|OOXML|word/document|w:t|python-docx|pandoc|zipfile
→ 1 hit: revenger SKILL.md:369 (`zipfile-docs` document-title correction row S044).

[grep D] CJK/PRISMA/"search record" over full set → hits in §2.
[grep E] `^## Search log|^### Search log|^#### Search log` over 20 corpora → 36 files.
[grep F] docx|OOXML|word/document\.xml|python-docx over full set → URL/label hits §2.
[glob] `corpus/**/*.docx` under all sibling corpora → none.
```

## Hits by lane (path:line)

- **audio**: corpus/SOURCES.md:35 `## Search log` (registry convention; curl+pdftotext method).
- **game-dev-2d**: corpus/SOURCES.md:46 `## Search log`; lessons/r101-export-capability.md:13 `z2.zip` export receipt (ZIP container test, no import/OOXML).
- **game-dev-3d**: corpus/SOURCES.md:54 `## Search log`; artifacts/zip-r10/verify_carrier.py:5,27 `zipfile` member inventory of GLB carriers; lessons/r10-zip-review.md:12 `zipfile` reading.
- **kagi**: corpus/README.md:83 "bounded search record"; corpus/SOURCES.md:76,124,182,393 `## Search log`; sources-census.sh:45,205,393,507 (enforces Search-log section shape — contract gate).
- **kaidoku**: corpus/SOURCES.md:164 `## Search log`; evidence/round-32/sources/pe-format.html:3993,6128 + pe-format.md:1220,2390 + round-33 copies — Microsoft Authenticode `.docx` URL/label only; evidence/round-36/c1/{K3,K4}/oracle.tsv:188,1798 `pandoc.vim` and :689 `prisma.vim` (firmware blob member filenames); evidence/round-41/c1/V4/* `libzipfile.so` inventory members (binary blob listing).
- **kake**: corpus/SOURCES.md:185 `## Search log`; lessons/round-57.md:102 `## Search log (rule 5)`.
- **kama**: corpus/SOURCES.md:259 `## Search log`.
- **kasegi**: corpus/SOURCES.md:78 `## Search log`; SOURCES.md:14 row S008 "linked DOCX path dated 2023-02"; source-snapshots/round-24/S008.txt:82,168 and round-40/S021.txt:200 "(DOCX, 35.93 KB" labels; round-35/S052.txt:7862 "-docx" URL fragment.
- **kengaku**: corpus/SOURCES.md:161 `## Search log`; lessons/round-29.md:52; evidence/round26-sources/gate.md:23 "overlapping scoped lists, not a deduplicated PRISMA count" — **disclaims** PRISMA counting.
- **kotoba**: corpus/SOURCES.md:186 `## Search log`; lessons/round-66-verifier-spotcheck.md:62 (search-log cite).
- **kotodama**: corpus/SOURCES.md:875 `## Search log` (+ lessons round-52..56); SOURCES.md:360 "NDL Search record 畫圖百鬼夜行" (national-library DB name).
- **kumitate**: corpus/SOURCES.md:194 `## Search log`.
- **lore**: corpus/SOURCES.md:52 `## Search log`.
- **mado**: corpus/SOURCES.md:336 `## Search log` (+ lessons 45–47).
- **mori**: corpus/SOURCES.md:287 `## Search log`; evidence/sources-r36/S205.src:81–83,125–128 — captured guideline text: "Search log … PRISMA-inspired, not PRISMA-compliant: question/query, where searched, date, identified/screened/included/excluded counts…" (only PRISMA-language sibling content).
- **revenger**: corpus/SOURCES.md:76 `## Search log` (+ lessons 63–64); corpus/snapshots/APPNOTE.TXT:260–263 (.DOCX listed among ZIP extensions); SOURCES.md:54,58 zipfile docs rows S040/S044 (screened-and-excluded: raw byte walk, no zipfile behavior claim); fixtures/replay_fixtures.py:32–43, apk-r65/generator.py:166–180 (authored ZIP fixtures); knowledge/round-63-zip-central-directory-evidence.md (manual struct readout; zipfile docs excluded).
- **souji**: corpus/SOURCES.md:192 `## Search log`.
- **tabi**: corpus/SOURCES.md:167 `## Search log` (+ lessons 33–34).
- **tameshi**: corpus/SOURCES.md:154 `## Search log`.
- **tsukuroi**: corpus/SOURCES.md:259 `## Search log`.
- **文献検索 / 检索报告**: ZERO hits anywhere in siblings.

## PROVINCE.md claims (a)/(b)

All 20 sibling PROVINCE.md files read (full read or scan). NO file claims
(a) document-format text-extraction tooling or (b) systematic-review
search-record ground:

- (a): no PROVINCE.md names docx/OOXML/w:t/python-docx/pandoc or any
  document-text extraction. Closest tool mentions are unrelated: kaidoku
  PROVINCE.md:62 host fallback readers incl. `unzip` (generic archive);
  kagi PROVINCE.md:56 `rendered-text-v1.py` (quote/page digest/normalizer,
  not format extraction); game-dev-3d PROVINCE.md:6–11 REA static-inspection
  tooling (artifact containers).
- (b): no sibling claims search-record ground. Each lane runs a per-registry
  `## Search log` (SOURCES contract) with identified/screened/included/
  excluded counts; kengaku explicitly disclaims PRISMA-count ground
  (evidence/round26-sources/gate.md:23); mori's captured guideline calls the
  convention "PRISMA-inspired, not PRISMA-compliant" (S205.src:126).
- Cross-lane routing: siblings route research method/capture to chousa —
  kengaku PROVINCE.md:262 ("capture and citation method stay chousa's"),
  souji :82–83 ("chousa-shokunin owns the research method and source
  hierarchy"), lore :27 ("chousa — research method"), kotodama :19–20
  (refuses "general source-research method (chousa)").

## Verdict

**NO OVERLAP.** Chousa uniquely holds `tools/capture-text.py` (the fleet's
only OOXML `.docx`→text extractor; header confirms `_rels/.rels`
officeDocument resolution, `w:t`/`w:tab`/`w:br`/`w:cr`/`w:p` handling,
`mc:Fallback`/`w:delText`/`w:instrText`/`w:pPr/w:tabs` exclusion, exit 2
REFUSED) and the three search-record entries (staged rows S125/S129/
S111/S112 → planned lane ids S113–S116). No sibling parses wordprocessingml,
no sibling tool imports python-docx/pandoc, and no other lane claims
search-record ground. Closest sibling file: **mori
corpus/evidence/sources-r36/S205.src:125–128** (captured PRISMA-inspired
search-log convention text — content similarity, not ownership); runner-up
kagi corpus/README.md:83 ("bounded search record").

VERDICT: attacked the sibling-overlap scan (20 lanes × corpus/tools/SKILL/PROVINCE, 13 terms) — no overlap; chousa alone holds capture-text.py and the three search-record entries; closest sibling file mori corpus/evidence/sources-r36/S205.src:125–128.
