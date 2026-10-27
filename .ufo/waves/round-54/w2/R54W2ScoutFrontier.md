# R54W2 — Seat `R54W2ScoutFrontier` — next-round (round-55) frontier scout

scope: rank three round-55 claim candidates (axis, counter, cheapest do-nothing control). No draft, no
production write, no adoption. Lane tip read `178667dc` (W1 reports + W2 dispatch on top of the
integrated tip `447cf7ed4dc1a3708518b99e9a5e62e177c11ce9`; `git diff --stat 447cf7e 178667d --
corpus/README.md corpus/lessons/round-54.md corpus/evidence/round54` → no output, frontier files
identical). Frozen round-54 claims (`claims.md` + `claims-erratum.md` E1–E4) read; nothing below
touches them. Scratch `/fast/scratch/hyaku/chousa-r54/R54W2ScoutFrontier`, removed on exit. No
network, no install, no soffice.

## Sources opened

`corpus/README.md:1165-1189` Round54 coverage/frontier (Left-open: entitled copy · S101 carrier
alphabet vs span builder · 表Ａ．２ applicability · S130 field); `corpus/lessons/round-54.md:25-67`
(Gate: S101 leg refusal + flip, S130 refusal + flip, quarantine S080/S088/S096, considerthese);
`merge/chousa/MERGE-REPORT.md` (114 staged rows, 58 entries, S170/S171 queued, S123→S078-style
held rows); W1 `R54ExecS130Probe` + `R54ScoutNextThemes`; `claims.md` C1/C2 + `claims-erratum.md`
E1–E4; `QUALITY.md:937-943` items 97–100; `build-spans.py:107-127`; SCORECARD "Round 54 pointer
corrections" (nine lines); absent-defect register `.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(25 `| `chousa` |` lines; row S125 round6 at :56, S096 round2 at :46).

## Checks run (observed)

```
$ python3 tools/capture-text.py $Q/bdff491a75c6abeda1d9c01d.raw > s130.txt
rc=0 bytes=34234 err=0
$ python3 tools/capture-text.py $Q/bdff491a75c6abeda1d9c01d.raw --locate "是否检索灰色文献等关键问题"
LOCATED count=1 offset=4678
$ utf16 = raw.decode('utf-16le','replace') → chars=121964 fffd=887 quote@57497
```

so `build-spans.py` `raw_form` (non-zip `.raw` → UTF-16LE, `:113`) slices a form where every new `.doc`
anchor is wrong (4678 vs 57497) — the named blocker for both S130 and the S101 leg. Row S101
(`SOURCES.md:111`) still prints "UTF-16LE text of the raw .doc capture" anchors `char 11170…34374`;
the nine `correction:` lines supersede them into the defined form (`SCORECARD.md:2740-2748`). No
`source: S101` line in `corpus/knowledge/source-type-taxonomy-r37.md` (grep → 1). Staged
`grey-literature-and-chinese-search-record-r40.md` cites S130 `.doc` + S131 cnpharm + S133 medsci;
S133's URL is byte-identical to lane S113 (`SOURCES.md:123`, `SOURCES.append.md:58`). Register row
for the `.doc` URL is `chousa | round6 | S125 | payload-absent` with a straight-quote `即灰色文献`
the document never prints (it writes `即“灰色文献”`, probe §5).

## Ranked round-55 claim candidates

### 1. The NMPA grey-literature search-record field (depth, sourced) — S130 + S131, closing the round-53 refusal

- **Axis:** depth (sourced). The `.doc`'s form blocker is gone (probe: 13,718 chars, 0 U+FFFD, LO
  oracle 248/248 @ ratio 0.9989); the staged entry's spine is in province (search-record field).
- **Counter (c2-count-shaped):** new rows S124 (`.doc`), S125 (S131 article) BOUND — one row each,
  first-cell URL, `mined`, `used-by` == citing entries, `source:` lines; ≥3 located quotes per id
  **in the defined text form** — which forces the form-aware span builder (the round's paired
  operability claim, below); anchors at located offsets; `inference-ground` PASS; a canonical
  `register S125 (round 6) verdict:` line in the lesson (absent in rounds 48–53, probe §6.4;
  the row's quote wording is absent-as-written, curly-vs-straight quote).
- **Cheapest do-nothing control:** land the staged r40 entry unchanged — `source: S133` names a URL
  held as lane S113 → unbound S-token / duplicate-document refusal; quotes pinned in the UTF-16LE
  form → span check fails (offset 57497 ≠ 4678); the staged `paymentAmount=10` "sold for 10 yuan"
  inference is not carried (`元`/`购买`/`付费`/`价格` all 0, probe §6.3). Carry rules: keep currency
  Unknown (`2019`/`二〇一九` 0 in the `.doc` form; `2019-06-18` lives only in S131), drop S144
  (refused) and the announcement number, re-tier S130 (third-party host, undated).
- **Prerequisite:** the span builder below. Companion candidates S142 （协和医学杂志 survey, `灰色文献`
  5× @7162/@9757) and S143 (NMPA English notice, `June 18, 2019` @1344) are captured and readable —
  optional third document, second-voice breadth.

### 2. The OLE-aware span builder (operability) unblocking the E3-cut S101 carrier-alphabet leg (depth)

- **Axis (paired claims, mirroring round 54's C1+C2):** operability — the builder reads an OLE
  `.doc` through `tools/capture-text.py` and refuses a form it cannot define, so every `span_file`
  is "the exact slice of the capture text form at the recorded offset" for `.doc` captures too;
  and depth — the S101 leg lands: the data specification's own carrier alphabet (14.3.4 four pair
  codes `磁带—MT,磁盘—DK,光盘—CD,联机网络—OL`; 15.5 one-letter GB 3469 `P—印刷本,M—缩微制品`; 文献类型标志
  `M C N J D R S P G K`) beside the standard's five-row 表Ａ．２, with the `M` collision across both
  tables (W1 `R54DraftEntryStb` QUOTE lines: 4 S101 quotes located, `inference-ground` PASS).
- **Counter (c1-count-shaped):** for each pinned OLE capture (five `.raw`, four documents —
  S100, S101, S130 + two more), quotes.tsv rows must produce span files whose offset is in the
  defined form (locate → `count=1`, offset named), not the UTF-16LE decode; a non-zip non-OLE
  `.raw` keeps the UTF-16LE reading only as a named-form row, and an entry may not mix forms.
- **Cheapest do-nothing control:** `build-spans.py@447cf7e` — non-zip `.raw` falls to
  `decode('utf-16-le')` (:113), where the S130 field sentence sits at 57497 (887 U+FFFD) and every
  defined-form anchor misses; a `.doc` quote row either fails location or binds the undefined form
  Mistakes row 2 named. Second control (the depth pair's): the W1 TOOLED control already printed
  `HELD_BAD=1` — citing `source: S101` without the row's `used-by` update fails QUALITY 100's leg.
- **Also in scope cheaply:** rewrite `SOURCES.md:110-111` anchor cells' stale "UTF-16LE" label and
  offsets to the corrected defined-form values the nine `correction:` lines already name (QUALITY
  97: an anchor names its form).

### 3. Theme B — archived Japanese translation as a closed set (depth; reserve)

- **Axis:** depth (sourced). Three unheld captured documents: staged S137 Wayback timemap
  (`9c28bfe4b85259c263428afd`, 5 link lines, two mementos), S146 CDX JSON (`324014043c04385c7ada030c`,
  digest `77FLJAP2…` per row), staged S096 Portico preservation approach (`226e5818f8f3125e55b5de7d`,
  `authentic replica … provenance must be verifiable` 1@1887 — the lane's own flip wording).
- **Counter:** c2-count-shaped over the new rows; ordinary `.txt` forms, so the round-54 builder
  works unchanged — cheapest of the three.
- **Cheapest do-nothing control:** re-land the staged `archived-translation-currency-r41` (refused
  r53): "withdrawn" has no source (the only original capture is `rc=28`), timemap+CDX are two views
  of one store (not "independent endpoints"), and CDX `length` differs beside an equal digest —
  each a substance/entailment failure. Real limit: the 2025-02-18 memento has no capture, so
  "closed set of two identical states" rests on the CDX digest alone; new ground is thin (the
  2026-04-18 identity is already recorded in `japanese-prisma-item-wording-r40.md:25`).

## Left-open items with no candidate

- **Entitled copy of the standard / 表Ａ．２ applicability:** no staged row or capture covers an
  authority-served or third-party-applying text (grep of `SOURCES.append.md` + staged knowledge for
  `7714`/`表Ａ．２` hits only the theme's own files) — cannot be claimed from the package this round.
- **Runner-up noted, not ranked:** W1's #2, the drug-evaluation source-taxonomy family
  (S155/S156/S157/S161/S168; `灰色文献` once each in S155/S168, 0 in S157; S168 a `T/CLPA XXXX—2025`
  draft) — viable depth claim behind the same counter shape, but the W1 scout flags a province
  argument ("source taxonomy", not drug policy) and a draft-status carry; the three above are
  strictly cheaper or closer to a stated refusal flip.

VERDICT: attacked the round-54 Left-open list against capture bytes, the frozen machinery and the
staged package — ranked (1) the S130 grey-literature entry (closes the r53 flip's text-form half;
needs the OLE-aware builder and a canonical S125 verdict line), (2) the form-aware span builder
plus the E3-cut S101 carrier-alphabet leg (unblocks every `.doc` quote; do-nothing = the UTF-16LE
fallback), (3) theme-B archived translations (cheapest, no tool dependency, thin ground, staged
defects to carry) — no draft written, no production file touched.
