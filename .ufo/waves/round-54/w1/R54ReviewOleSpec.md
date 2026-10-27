# R54ReviewOleSpec — what the frozen C1 OLE text form drops or misreads

seat: R54ReviewOleSpec (leaf; no dispatch). Read: `corpus/evidence/round54/claims.md` @ lane
5a1a20630d8176a816a60bb43b0d0e7ee2db19a0, `tools/capture-text.py` @ 8a7d0f13, `c1-count.py`
`leg_real`. Everything below is from bytes I opened; no campaign quote or date is reused.

Scratch `/fast/scratch/hyaku/chousa-r54/R54ReviewOleSpec` (TMPDIR set there; removed at exit;
private soffice profile `-env:UserInstallation=file://$S/prof`).

## Method

```
$ for f in 54fe… 6dc68… b539a… bdff4…; do python3 tools/capture-text.py $Q/$f.raw > $S/$f.tool.txt; done   # exit=0 ×4
$ soffice -env:UserInstallation=file://$S/prof --headless --convert-to "txt:Text (encoded):UTF8" … $S/$f.doc
$ python3 $S/wsdiff.py $S/$f.tool.txt $S/lo/$f/$f.txt     # ws0 char diff + c1-count's own line rule
```

| capture | ccpText | ccpFtn | ccpHdd | ccpTxbx | HdrTxbx | pieces | tool ws0 | LO ws0 | ratio | char-diff |
|---|---|---|---|---|---|---|---|---|---|---|
| 54fe0734… | 15922 | 0 | 164 | 0 | 59 | 15 (UTF-16) | 11448 | 11779 | 0.9719 | cover +260, labels −591 |
| 6dc68fd6… | 27791 | 0 | 0 | 0 | 0 | 18 (2× cp1252) | 24667 | 24667 | 1.0000 | **opcode list EMPTY** |
| b539a802… | 889 | 0 | 13 | 66 | 0 | 3 (UTF-16) | 792 | 800 | 0.9900 | labels −8 |
| bdff491a… | 13804 | 0 | 152 | 5 | 0 | 1 (UTF-16, 0Table) | 12480 | 12494 | 0.9989 | bullets −14 |

`c1-count` REAL rule replayed line-for-line (`wsdiff.py`): **count=0 misses on all four**. The
counter passes; the classes below are what it structurally cannot see.

## Class verdicts

**(a) List numbering — tool RIGHT, rule should say so.** Auto-numbers live in PlfLfo/LST, not the
piece table, so the text form cannot hold them. Measured escape-hatch use: 54fe 119 of 344 LO
lines (dropped tokens: `——`×9, appendix `序号` values 1…48 ×67, §-numbers ×28 (`5.2.3.3.1`…),
`表1`…`表10` ×10, `图1`/`图2`, `b)`, **bibliography markers `[1]`/`[2]`**), b539 1 (`5.`), bdff 14
(`•`). Two consequences a reader notices: 54fe appendix A's `序号` column is *entirely absent*
(tool:389 = `序号` then cells; LO:288 renders `    1 \t网络\t低\t无\t不需要\t9`), and the
参考文献 entry numbers are gone (LO `    [1] Common Vulnerability Scoring System v3.1: …` vs tool
`Common Vulnerability Scoring System v3.1: …`) — the one loss that touches C2's own axis.

**(b) Footnotes/headers — tool RIGHT per rule; nothing lost here.** ccpFtn=0 in all four; the
header stories (54fe 164, bdff 152, b539 13) are excluded and LO excludes them too, and b539's
textbox story (ccpTxbx=66) duplicates a main-story paragraph byte for byte (tool line 32).

**(c) Field results — tool RIGHT (results kept, codes dropped).** `54fe`'s TOC result is present,
its code absent. Side effect: the cached TOC duplicates every heading, so `--locate '代码问题'` →
`LOCATED count=2 offset=384`, exit 1, and `'概述'` → count=16, exit 1 — a heading quote in a
standards `.doc` is unlocatable; the two pinned quotes are body sentences, so the leg passes.

**(d) Special characters — tool WRONG.** Fixture `special.docx` → LO → `.doc`; raw main story is
`A U+00A0 B U+2002 C U+2003 D 0x1F E 0x1E F`:
```
tool: A   B   C   D  E - F        LO: A U+00A0 B U+2002 C U+2003 D U+00AD E U+2011 F
```
0x1E (non-breaking hyphen) is flattened to ASCII `-` (U+2011 → `-`); 0x1F (optional hyphen,
U+00AD) is **dropped** by the "every other code point below 0x20 emits nothing" clause. 0xA0 /
U+2002 / U+2003 are preserved correctly. Latent: no pinned capture carries 0x1E or 0x1F
(`inv.py`: x0 in all four), so the REAL leg never exercises it; a capture using U+2011 or U+00AD
would fail the ws0 line check spuriously.

**(e) Table cell order — order right, cell/row delimiter WRONG.** `.doc` holds cell ends as 0x07
and paragraph ends as 0x0D; the tool maps **both** to `\n`, while LO maps 0x07→TAB, 0x0D→`\n`.
Raw `6dc68` row: `类型\x07普通\r图书\x07会议\r论文\x07` → LO `类型\t普通` / `图书\t会议` /
`论文\t报纸`; tool six separate lines. `bdff` RCT table header (14 cells) becomes 14 lines
(tool:99–112) with the row end as one blank line — and because empty cells also emit 0x07, the
row grid is unrecoverable (0x07-run lengths up to 15 in bdff, up to 4 in 54fe). A reader cannot
recover 6dc68's substance, the type-letter mapping `M C N J D R S P G B O K`.

**(f) Deleted / revision text — tool WRONG; asymmetric with its own .docx form.** MS-DOC keeps
deleted runs in the piece table and marks them in character properties, which the tool never
reads (`raw.py` shows the run as plain text: `bravo DELETEDTEXT charlie`).
Fixture `<w:del><w:delText>DELETEDTEXT</w:delText>` → LO → `.doc`:
```
$ python3 tools/capture-text.py tracked.docx   HEAD alpha INSERTEDTEXT bravo  charlie      # w:delText dropped (documented)
$ python3 tools/capture-text.py tracked.doc    HEAD alpha INSERTEDTEXT bravo DELETEDTEXT charlie   # emitted
```
The `.doc` genuinely carries the revision, not flat text: .doc→.docx round-trip gives
`w:del=1 w:ins=1 delText=['DELETEDTEXT']`. LO's txt export also emits it, so the frozen REAL leg
cannot see it. No pinned capture has `w:del` (docx round-trip: `w:del=0` ×4).

**(g) Hidden text — tool WRONG.** Fixture `<w:vanish>` → `.doc` → .doc→.fodt round-trip still has
`fo:visibility="hidden"`; tool prints `VISIBLE HIDDENTEXT AFTER` as ordinary text. LO's txt export
also emits it, so the counter cannot see it. No pinned capture has `w:vanish` (×4 zero).

**(h) Where the tool is MORE complete than its own oracle.** 54fe's cover page (`ICS 35.040`,
`L80`, `中华人民共和国国家标准`, `GB/T 30279—XXXX`, `代替 GB/T30279—2013,GB/T 33561—2017`,
`（征求意见稿）`, `2019-10-10`, `XXXX - XX - XX发布/实施`) sits in the **main story at CP 0**
(`raw.py`: `ICS\u200235.040\rL80\r<PIC>\r中华人民共和国国家标准\r…`) and the tool emits it; LO's txt
export drops it because LO imports those paragraphs as `draw:frame`/`draw:text-box`. Tool right,
oracle lossy: the 0.90–1.10 band for 54fe is the *residual* of +260 tool-only and −591 LO-only
characters — two opposite errors cancelling.

## Counter blindness (reported, not patched — predicates are frozen)

1. `leg_real`'s test is `w in flat` on the whitespace-free form: one-directional, so the tool's
   +260-character cover is never checked, and deleting all whitespace erases exactly the cell/row
   structure from (e). Cell-grid loss is invisible by construction.
2. Revision and hidden text pass because both the tool *and* the LibreOffice oracle emit them:
   even a two-directional comparison would not detect (f)/(g).
3. The escape `re.match(r"^\s*\S{1,12}\s+(.*)$", line)` drops **any** leading token of ≤12
   non-space characters, not a list label. On these captures every dropped token is a label
   (`——`, `•`, `5.`, `1`…`48`, `5.2.3.3.1`, `[1]`), but the mechanism would silently absorb up to 12
   characters of real leading content on any line.
4. Undefined cp1252 bytes (0x81/0x8D/0x8F/0x90/0x9D) become U+0081… as declared; above 0x20, so
   the "below 0x20" clause passes, but they are C1 controls. Absent from all four captures.

## Residual risk and verification gaps

- (d) is a latent spurious-failure path: one U+2011 or U+00AD in any future pinned capture fails
  the REAL ws0 line check with no hint that a character class, not the piece table, is at fault.
- Fixing (f)/(g) needs a character-property (CHPX/FKP) walk the tool does not have, plus a rule
  decision between the Word "All Markup" and "No Markup" views; the frozen predicate chooses
  neither. [INFERENCE: that a CHPX walk suffices — I did not decode CHPX bytes.]
- Not run: `c1-count.py` end to end (only its REAL-leg line rule replayed); a Word-authored `.doc`
  with revision marks (mine is LibreOffice-authored); fast-save/multi-PCD pieces.

VERDICT — I attacked the frozen C1 text form on the four pinned captures plus six rebuilt
fixtures: the piece-table path is sound (6dc68 ws0 is byte-identical to LibreOffice; 54fe is
*more* complete than its oracle), but the form silently emits tracked-deleted and hidden text,
flattens U+2011, drops U+00AD and erases cell/row boundaries. The docstring declares the 0x07
collapse and 0x1E→`-`; it does not declare that revision-marked and hidden runs are emitted, and
the frozen REAL leg cannot see any of the four classes.
