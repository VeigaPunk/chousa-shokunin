# R54W2ExecOleHeldout — held-out behaviour of the landed OLE text form vs its docstring

seat: R54W2ExecOleHeldout (leaf) · lane `chousa-shokunin` · round 54 wave 2 · attacks C1's OLE text form
scratch: `/fast/scratch/hyaku/chousa-r54/R54W2ExecOleHeldout` (removed at end) · no network, no lane writes

## 0. What I ran it on

- Tool under test: `tools/capture-text.py`, sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.
  `git -C chousa-shokunin rev-parse HEAD` = `25abbe82b9f2b7c6e24580ac3f028611ba21f01f`; the named wave tip is
  `447cf7ed…`, and `git rev-parse 447cf7ed…:tools/capture-text.py HEAD:tools/capture-text.py` prints `43931dddc43bd52e62e87419aa07a0c52f542fe2` twice and
  `git cat-file -p 447cf7ed…:tools/capture-text.py | sha256sum` prints the same digest above — I tested the exact blob the spec names;
  HEAD only added report/marker commits (`git log --oneline -3` → `25abbe8`, `178667d`, `447cf7e`).
- Oracle/authoring: `soffice --version` → `LibreOffice 26.8.1.1 680(Build:1)`; every run
  `soffice -env:UserInstallation=file://$S/prof --headless --convert-to 'doc:MS Word 97' --outdir …`, `HOME=$S`.
  No tool installed, no pacman (paused host-wide); `/usr/bin/time` is absent, so timing is `time.time()` in a wrapper.
- Docstring lines quoted below are from `sed -n 27,40p tools/capture-text.py` (line numbers as printed by `grep -n`).

## 1. Result table — ten held-out shapes, tool vs docstring

Every `.doc` below is LibreOffice's Word 97 export of a `.fodt` I authored in scratch; "markers(utf16,cp1252)" is a raw-byte count on the
`.doc`, i.e. proof the feature actually reached the file (a `0` count would make the probe vacuous). `ctl=[]` = the stdout text form held no code
point below 0x20 other than tab/newline and no U+FFFD. Commands and outputs are pasted verbatim in §2.

| case | fixture (sha256¹⁶, bytes) | markers in `.doc` | tool stdout (rc 0) | docstring clause | verdict |
|---|---|---|---|---|---|
| (a) footnote | `a_footnote.doc` 429e588e2b29ed5b 9728B | FOOTNOTETEXT (1,0) | `'MAINBODY first paragraph.\nBody with a footnote reference here.\nMAINBODY last paragraph.\n'` | l.29-30 "footnotes … are not in it" | **holds** |
| (b) header+footer | `b2_headerfooter.doc` 9f5b6dd094652c9d 9728B | HEADERTEXT (1,0), FOOTERTEXT (1,0) | `'MAINBODY header footer test v2.\n'` | l.29-30 "headers … not in it" | **holds** |
| (c) text box | `c2_textbox.doc` 8309537486e3bb9e 10240B | TEXTBOXTEXT (1,0) | `'MAINBODY textbox v2 before.MAINBODY textbox v2 after.\n'` | l.29-30 "text boxes are not in it" | **holds** (see C2 note) |
| (d) comment | `d_comment.doc` 8085969c72af669c 9216B | COMMENTTEXT (1,0) | `'MAINBODY comment test.\nAnnotated sentence here.\n'` | l.29-30 "comments … not in it" | **holds** |
| (e) tracked, whole ¶ | `e3_tracked.doc` 4ef01de429320ee3 9216B | DELETEDTEXT (1,0), INSERTEDTEXT (1,0) | `'MAINBODY kept text before.\nKEPT alpha INSERTEDTEXT added by the tracked insertion.\nKEPT beta \nMAINBODY kept text after.\n'` | l.34-36 "…carry sprmCFRMarkDel … emits nothing, while tracked insertions … are emitted" | **holds** |
| (e′) tracked, mid-¶ | `e4_tracked.doc` 8843d63ba17a4123 9216B | DELETEDTEXT (1,0), INSERTEDTEXT (1,0) | `'MAINBODY kept text before.\nKEPT alpha INSERTEDTEXTinsertion tail.\nKEPT beta deletion tail.\nMAINBODY kept text after.\n'` | same | **holds** |
| (f) nested table | `f2_nestedtable.doc` 12f85002e3d1e526 10240B | INNERCELL beta (1,0) | `'MAINBODY nested table v2.\nOUTERCELL one.\nINNERCELL alpha.\n\nINNERCELL beta.\n\n\nOUTERCELL two.\n\nMAINBODY after table.\n'` | l.31 "0x07 cell or row end … a newline" | **holds** (order and both cells; one newline per cell *and* per ¶, as written) |
| (g) TOC field | `g3_toc.doc` ccde9576cebf2a76 9728B | TOCRESULT (2,0), `TOC \` (1,0) | `'MAINBODY toc v3.\nHEADINGONE Alpha\nbody under alpha.\nHEADINGTWO Beta\nbody under beta.\nTOCHEADING Contents\nTOCRESULT HEADINGONE Alpha 1\nTOCRESULT HEADINGTWO Beta 1\n'` | l.32 "a field emits only its result … the field code is dropped" | **holds** (code bytes present, no code text in stdout) |
| (h) hidden text | `h_hidden.doc` 8b84c668b590cf87 9216B | HIDDENTEXT (1,0) | `'MAINBODY hidden test.\nVISIBLE before HIDDENTEXT hidden run after.\n'` | l.36-37 "hidden (vanish) text [is] emitted" | **holds** |
| (i) hyphens | `i2_hyphen.doc` 52c38f25c9e1e2be 9216B | plain-hyphen (1,0) | `'MAINBODY hyphen v2.\nsofthyphen and non-breaking and plain-hyphen.\n'` | l.31 "0x1E a `-`" + l.37 "every other code point below 0x20 emits nothing" | **holds** (0x1F dropped, 0x1E → ASCII `-`) |
| (j) 300 pages | `j_big.doc` 49456113a0e935ae 1426432B | PAGE299 (1,0) | 644900 B, 300 `PAGE` + 6000 `FILLER` markers, **125 ms**, child maxrss 30.6 MB | — (performance) | **holds** |

## 2. Commands and the outputs I read them from

Tool head, for the record (`sha256sum` and lane rev, §0), then the per-document run:

```
$ python3 tools/capture-text.py conv3/e3_tracked.doc        # 'MAINBODY kept text before.\nKEPT alpha INSERTEDTEXT added by the tracked insertion.\nKEPT beta \nMAINBODY kept text after.\n'
$ python3 tools/capture-text.py conv3/e3_tracked.doc --locate 'DELETEDTEXT removed by the tracked deletion.'
LOCATED count=0 offset=-1        # rc=1: the tracked deletion is not in the text form
$ python3 tools/capture-text.py conv3/e3_tracked.doc --locate 'INSERTEDTEXT added by the tracked insertion.'
LOCATED count=1 offset=38        # rc=0: the tracked insertion is
$ python3 corpus/evidence/round54/tracked-deletion-check.py
tracked.doc rc=0 OK 'alpha INSERTEDTEXT bravo charlie\nvisible HIDDENTEXT end 中文删除测试\n第二 保留\n'
tracked.docx rc=0 OK 'alpha INSERTEDTEXT bravo charlie\nvisible HIDDENTEXT end 中文删除测试\n第二 保留\n'
TRACKED_DELETION=PASS
```

### 2.1 The tracked-deletion rule, checked at the CHPX level (not just at the output)

`e3_tracked.doc` piece text and CHPX runs, dumped with a scratch reader that imports the tool's `Cfb` only:

```
ccpText=164  pieces n=1 cps=(0, 164)
  piece k=0 cp=0..164 fc=2048 comp=False
  text='MAINBODY kept text before.\rKEPT alpha INSERTEDTEXT added by the tracked insertion.\rKEPT beta DELETEDTEXT removed by the tracked deletion.\rMAINBODY kept text after.\r'
CHPX FKP pn=5 crun=5 fcs=(2048, 2124, 2212, 2234, 2322, 2374)
  run r=1 fc=2124..2212 marks_deleted=False sprms=[('0x801','01'), …]   # fRMarkIns — emitted, as documented
  run r=3 fc=2234..2322 marks_deleted=True  sprms=[('0x800','01'), …]   # fRMarkDel — dropped
  tool deleted_runs -> [(2234, 2322)]
```

`e4_tracked.doc` (mid-paragraph, 1-char-granular): `deleted_runs -> [(2200, 2222)]` = exactly `'DELETEDTEXT'`; the tool prints
`'…KEPT beta deletion tail.…'` — the deleted span gone, the rest of the sentence intact. So the landed fix (erratum E2) works on a
**held-out authoring path** (canonical `.fodt` `<text:tracked-changes>` → LO `.doc`), not only on W1's `.docx`→`.doc` fixture.

### 2.2 The lookalike that does *not* falsify it — `e2_tracked.doc` (my first, wrongly authored fixture)

My first tracked `.fodt` put the changed text **both** in the `<text:changed-region>` **and** in the body paragraph. LO exported both:

```
piece text='MAINBODY kept text before.\rKEPT alpha INSERTEDTEXT added by the tracked insertion.INSERTEDTEXT added by the tracked insertion.\rKEPT beta DELETEDTEXT removed by the tracked deletion.DELETEDTEXT removed by the tracked deletion.\rMAINBODY kept text after.\r'
  run r=3 fc=2322..2410 marks_deleted=True   text='DELETEDTEXT removed by the tracked deletion.'   ← dropped by the tool
  run r=4 fc=2410..2550 marks_deleted=False  text='DELETEDTEXT removed by the tracked deletion.\rMAINBODY kept text after.\r'   ← NOT marked
tool stdout: 'KEPT beta DELETEDTEXT removed by the tracked deletion.\n'
```

The sentence a reader would put on trial — l.34-35, "a run whose character properties (the CHPX FKP pages of the PlcBteChpx) carry
sprmCFRMarkDel — a tracked deletion — **emits nothing**" — is **not** contradicted here: the copy that survives is run r=4, which carries no
CHPX deletion mark (the tool printed r2's tail + r4, and `deleted_runs` = the r3 range only). The document itself stores a second, unmarked copy,
because my `.fodt` stored the text twice; with the canonical single-store authoring (§2.1) the deletion is dropped and only one copy exists.
I record it because its stdout is byte-identical in shape to the bug E2 fixed, and a reviewer re-deriving the claim from this shape would mis-call it.

## 3. Byte-level confirmation of the two hyphen code points (case i)

Piece text of `i2_hyphen.doc`, decoded at its recorded FC:

```
'MAINBODY hyphen v2.\rsoft\x1fhyphen and non\x1ebreaking and plain-hyphen.\r'
codepoints: 0x0d, 0x1f, 0x1e, 0x0d
```

LibreOffice writes U+00AD as word character **0x1F** and U+2011 as **0x1E**; the tool emits `soft hyp`→`softhyphen` (0x1F dropped) and
`non‑breaking`→`non-breaking` (0x1E → ASCII `-`). Both match l.31 and l.37 exactly. Note the cross-form divergence this creates (the OOXML
path would emit U+00AD and U+2011 verbatim, not `-`), which the docstring does not claim away: it scopes the mapping to the OLE form only.

## 4. Caveats that are *not* predicate breaches

- **Caveat 1 — the inline text-box anchor glues its neighbours.** Case (c) prints `before.MAINBODY` with no separator: the as-character drawing
  anchor is a code point below 0x20 and l.37 says such code points emit nothing. Consistent, but any held-out reader expecting a space there
  is wrong, not the tool.
- **Caveat 2 — the footnote *number* is absent.** LO's own export puts the auto-number in its text (`…footnote reference1 here.`), the tool prints
  `…footnote reference here.` — the number is generated at layout time, and the reference char 0x02 is dropped under l.37. C1's frozen
  must-hold rule already tolerates exactly this class (it allows dropping one leading list label), so no leg moves.
- **A two-column nested table does not survive LibreOffice's Word 97 export at all** — not a tool finding, but it bounds what (f) can prove.
  For my first nested fixture (`conv/f_nestedtable.doc`, inner table 2 columns × 1 row) the raw bytes hold `INNERCELL beta` **0** times
  (`utf16=0`), so the cell never reached the document and the probe was vacuous; with the inner table as 1 column × 2 rows
  (`f2_nestedtable.doc`) the cell is present (`utf16=1`), survives LO's `.doc`→`.fodt` round-trip (count 1) and LO's txt export
  (`'…OUTERCELL one.\nINNERCELL alpha.\tINNERCELL beta.\n\tOUTERCELL two.\nMAINBODY after table.\n'`), and the tool prints it in document order.
  Recorded so nobody reads the v1 loss as text-form behaviour.

## 5. Not exercised, and why (no silent gap)

- **0x0C page/section break** (l.31): both authoring attempts (`fo:break-before="page"`, `<text:soft-page-break/>`) make LO's Word 97
  exporter write a paragraph property or nothing, never a 0x0C in the piece text (`piece cps ['0x9','0xd','0xd','0xb','0xd']` for the
  tab/page-break/line-break probe). 0x09→`\t` and 0x0B→`\n` **were** exercised in that probe:
  `'TABLEFT\tTABRIGHT\nPAGEBREAK SECOND PAGE\nLINE\nBREAK\n'`.
- **Tracked deletion inside a compressed (cp1252) piece** — the one place the mechanism could still leak. LO writes UTF-16 pieces for every
  fixture here (byte scan: `cp1252=0` for all markers, `comp=False` for all pieces), so I could not build it. I did close the *convention*
  question it rests on: on the pinned capture `6dc68fd6b32ce9c8dfcebce8` (18 pieces, 2 compressed) 1118 CHPX runs land inside compressed
  pieces and decode as sensible cp1252 at the FKP FC itself (`fc=10758..10765 comp=True text='Library'`), i.e. the FKP FCs are byte offsets,
  exactly the space `live()` compares (`off + x`), so the deletion filter is not misaligned by compression. [INFERENCE] this means the
  compressed-piece case would behave the same, but it was not measured on a document carrying fRMarkDel.
- **A field with no separator** (l.32-33) and `ole-encrypted`/`ole-malformed` refusals: outside this seat (frozen counter legs).

## 6. Housekeeping

- Scratch `/fast/scratch/hyaku/chousa-r54/R54W2ExecOleHeldout` removed at end; every output path was absolute under it; `PYTHONDONTWRITEBYTECODE=1`
  on every lane-tool invocation (no `__pycache__` dropped in the lane by me).
- No `soffice.bin` of mine left: after each conversion `pgrep -a soffice.bin` printed `no soffice.bin left` / `no soffice.bin`. One
  `pgrep` during the run showed a **sibling** process (`-env:UserInstallation=file://…/R54W2SentFinal/…`) — not mine, not killed.
- Lane writes: this report only. No git/jj command ran anywhere except `git rev-parse/log/cat-file` reads on the lane.

VERDICT: attacked the landed OLE `.doc` text form with ten held-out LibreOffice-made documents (footnote, header+footer, text box, comment, tracked deletion+insertion whole- and mid-paragraph, nested table, TOC field, hidden text, 0x1F/0x1E hyphens, 300 pages) and it survived every docstring clause it claims — tracked-deleted runs are genuinely dropped (CHPX `sprmCFRMarkDel`, `--locate` count=0) while insertions, hidden text and field results are emitted, in 125 ms for 300 pages; no contradiction found, two named caveats and two unexercised clauses disclosed.
