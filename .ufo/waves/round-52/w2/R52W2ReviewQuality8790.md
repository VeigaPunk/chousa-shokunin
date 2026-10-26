# R52W2ReviewQuality8790 — attack on QUALITY.md criteria 87–90 (round 52, wave 2, falsify)

Seat: review of `corpus/QUALITY.md` criteria 87–90. For each: ran its check from the lane root
(`/home/vgpnk/Projects/shokunin/chousa-shokunin`), reproduced its "shown able to fail" red state exactly
where the fixture exists, confirmed cited files/counts/offsets, and checked the cited `## Mistakes` row
exists and says the same. Every command below ran this session on the landed lane (freeze `37468ead`,
C1 candidate `804a4537`, commit `e769c037` head). No installs (none needed); scratch only under
`/fast/scratch/hyaku/chousa-r52/R52W2ReviewQuality8790`, removed at the end.

## 87 — capture read through a defined text form

Check (QUALITY.md:917): `python3 tools/capture-text.py <raw> --locate '<quote>'` → `LOCATED count=1 offset=<N>`
for every quote a lesson cites from an OOXML capture, and an entry's `char N` equals that offset.

- Landed tool on the NIPH raw (`3a8b45977cd111e45e3980a5.raw`, 178,056 B, sha256 `16fc8c55…`):
  `rc=0`, stdout 19,682 chars. All 14 S115 quotes from the lesson's "All located quotes" table re-located:
  `LOCATED count=1 offset=9/42/1446/8389/8996/9020/9189/9257/9391/9408/9419/9428/19496/19521`, rc 0 for
  all 14; identical to the lesson table and to `char N` in `corpus/knowledge/japanese-search-record-niph-form-r52.md` (lines 3, 11–16).
- Main-part counts (zipfile+ElementTree): `w:instrText` 50, `mc:Fallback` 60, `w:delText` 0, `w:txbxContent` 42 — matches.
- Red states reproduced: `c1-count.py --tool controls/naive-tool.py` → `LEGS=4/9 C1=FAIL`
  (REVISIONS/LAYOUT/ALTCONTENT/MAIN_PART/REFUSE fail; `REAL=PASS rc=0 count=1 locate=(0, 1, 10319) chars=21910`);
  `--tool controls/cache-txt-tool.py` → `LEGS=0/9 C1=FAIL` (`REAL … chars=168953`, count=0).
- **Defect — wrong cited count.** Criterion 87 and lesson line 60 say the `.txt` sidecar is "168,952 characters,
  72,117 U+FFFD". Measured: `len(sidecar.decode("utf-8","replace"))` = **168,953**, U+FFFD 72,117, `文献検索` 0;
  `wc -m` = 168953; decode of the raw zip bytes = 168,953. W1 evidence agrees with 168,953: `R52ExecRealDocx.md`
  §5 ("sidecar … 168953 chars, 72117 U+FFFD") and `R52DraftEntryNiph.md` §61 (prints `168953 72117`).
  168,952 is an off-by-one that persists in QUALITY 87 and in the lesson decision table (line 60).
- Mistakes row 1 exists, cites the same control files/commands/offsets (10319-of-21910 vs 8996-of-19682), and
  carries the same wrong 168,952 figure in the lesson line 60. Claim R52-C1 cited in the criterion exists
  (`claims.md` §R52-C1) and matches.

## 88 — counter varies representation; fixed-input leg pins content

Check (QUALITY.md:919): `python3 corpus/evidence/round52/c1-supplement.py [--tool PATH]` → PREFIX, RELS_FORM,
SYNTAX, REAL_TEXT.

- Supplement vs landed tool: `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS` exit 0.
- Red reproduced: `--tool controls/forge-shape.py` → `0/4` (REAL_TEXT `chars=21`); `--tool controls/naive-tool.py`
  → `0/4`. Frozen counter vs forge: `c1-count.py --tool controls/forge-shape.py` → `LEGS=9/9 C1=PASS`, `REAL …
  locate=(0, 1, 0) chars=21` — the vacuous pass.
- Embedded facts verified: forge-shape.py is exactly 85 lines; keyed to the generators' spelling (regex on
  `_rels/.rels` fixed attribute order, exact `<w:tab/>`/`<w:br/>`, regex drops of `mc:Fallback`/`w:delText`/
  `w:instrText`/`w:tabs`); REAL leg memoized on pinned sha256 `16fc8c55…` with stub `REAL_QUOTE+"\n"` = 21 chars;
  c1-count REAL leg checks only self-consistency (`rc==0 and count==1 and locate==(0,1,txt.find(q))`).
- REAL_TEXT pin: `build-spans.py` `docx_text` on the NIPH raw → 19,682 chars, sha256
  `754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9` = `TEXT_SHA` in the supplement.
- Named limit holds (real XML parser passes = implemented rule); E1 (`claims-erratum.md`) and Mistakes row 3
  exist and say the same; supplement reported beside the frozen counter.

## 89 — verdict offset re-located in its stated form

Check (QUALITY.md:921): every `register S### … verdict:` block's quote line `char N` equals the quote's offset
in the named form (for `form capture-text`: the tool's `--locate`).

- Green reproduced: round-52 S120 block — `--locate` of the three quote lines gives `LOCATED count=1 offset=8996`,
  `9020`, `9428` (rc 0), matching `char 8996/9020/9428 form capture-text`.
- Red reproduced: round-51 S120 line (`round-51.md:88-89`) states `char 39411` in "form .raw unzipped →
  word/document.xml UTF-8"; `find("SRにおける文献検索期間について明記する。")` in `word/document.xml` of
  `3a8b4597.raw` → **-1** (the sentence is split across runs; even the prefix `SRにおける` is absent from the XML).
- Mistakes row 2 exists, cites both W1 reports (`R52DraftMistakes` row 5, `R52ExecQuarantine`) and the round-51
  spot-check acceptance; says the same. Named limit "a manual check, not a counter" is accurate — nothing
  executable enforces this; line 921 names no command for non-`capture-text` forms (DEINT/.txt), so only `form
  capture-text` blocks are bound.

## 90 — refuses non-target part type and inflated part

Check (QUALITY.md:923): tool exits 2 with `REFUSED main part '…' is not WordprocessingML …` on
`cb101e95f5f5e98d019eeca1.raw` and `REFUSED '…' inflates to <n> bytes (limit 268435456)` on a part over 256 MiB.

- Landed tool on `cb101e95….raw` → rc 2, stderr `REFUSED main part 'xl/workbook.xml' is not WordprocessingML
  (root {http://schemas.openxmlformats.org/spreadsheetml/2006/main}workbook)`. Candidate (git show
  `804a4537:tools/capture-text.py`, sha256 `3986a9715328175d…`) → rc 0, empty stdout — red reproduced.
- Landed tool on `b539a80218080da56a75b624.raw` (OLE `.doc` theme part) → rc 2 `REFUSED main part
  'theme/theme/themeManager.xml' is not WordprocessingML (root {…drawingml…}themeManager)`; candidate → rc 0,
  empty. `e9761e99….raw` (second `.xlsx`) also rc 2 on the landed tool.
- Inflated part: the L1's exact fixture (524,901-byte package → 360,000,113 B → 60,000,000 chars) is **not on
  disk** (W1 scratch removed; no bomb fixture under the lane, wave dirs or staged package). Reconstructed an
  equivalent fixture in scratch (789,293 B package; `word/document.xml` inflates to 270,900,180 B): landed tool
  → rc 2 `REFUSED 'word/document.xml' inflates to 270900180 bytes (limit 268435456)`; candidate → rc 0 printing
  133,300,000 chars. Message shape and limit (268435456) exactly as named.
- Named limits verified: pyexpat `EXPAT_VERSION = expat_2.9.0` on Python 3.14.8; criterion 18 ("A byte-read cap
  is not a memory or time bound") exists at QUALITY.md:104; bound is uncompressed bytes per part (message proves it).
- Mistakes rows 5 and 6 exist and say the same; row 6 carries the unreproducible-from-disk figures above.
- **Class-coverage gap (answer to "which of the four would not catch a regression of its own class"): criterion
  90.** Its check pins exactly one non-Word part type (the `xl/workbook.xml` case) and one inflated main part.
  The criterion's own class is plural — any non-target part type — and its evidence sentence names three red
  inputs (two `.xlsx` **and** the OLE theme part `b539a802`); `.pptx` is untested (W1 `R52ExecRealDocx`: "No
  `.pptx`"). A regression that reintroduced acceptance of the OLE-theme/`.pptx` classes (while keeping the
  `.xlsx` refusal) would pass the check verbatim; no byte `..` or `b539a802` fixture is in the check, and the
  inflated-part leg has no concrete on-disk fixture to run. The other three catch their own class (87: naive
  4/9 & sidecar 0/9; 88: forge/naive 0/4 vs tool 4/4; 89: round-51 line -1). 87's check is also sampling-limited
  to lesson-cited quotes, but its cited red inputs do catch the cheap readers.

## Verdict

Attacked QUALITY 87–90: all four checks' pass outputs and red states reproduce on the landed tool/candidate
(89's and 90's red states on preserved fixtures; 90's exact L1 bomb figures unreproducible — fixture not
preserved, class reproduced by reconstruction); one defect found — criterion 87 (and lesson line 60) cites the
sidecar as 168,952 characters, measured 168,953 (U+FFFD 72,117 correct); criterion 90 is the one of the four
whose check would not catch a regression of its own class (OLE-theme/`.pptx` refusal classes untested, inflated
leg has no executable fixture).
VERDICT — attacked QUALITY 87–90 on the landed lane: all four checks' pass outputs and red states reproduce (90's L1 bomb figures reconstructed, fixture not preserved); defect: criterion 87 cites the sidecar as 168,952 chars vs measured 168,953; criterion 90's check would not catch a regression of its own class (OLE-theme/pptx untested, inflated leg without executable fixture).
