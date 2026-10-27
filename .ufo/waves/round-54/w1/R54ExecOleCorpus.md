# R54ExecOleCorpus — held-out fidelity of the C1 OLE `.doc` text form

seat R54ExecOleCorpus (leaf) · lane `chousa-shokunin` · round 54 wave 1
candidate `tools/capture-text.py` @ `8a7d0f13` (`sha256 e7e381b6…`), base `c49ffc6c`. Claims frozen at
`5a1a2063`: nothing here proposes a change to a predicate, target, counter or control — findings only.
scratch `/fast/scratch/hyaku/chousa-r54/R54ExecOleCorpus` (`TMPDIR` there, removed at the end); every soffice
run `-env:UserInstallation=file://$S/prof --headless`; `pgrep -u $USER -f "UserInstallation=file://$S"` empty at the end.

## Reproduce
```
find /home/vgpnk/Projects /usr/share /usr/lib/libreoffice -xdev -type f \
  \( -iname '*.doc' -o -iname '*.dot' -o -iname '*.xls' -o -iname '*.ppt' -o -iname '*.msg' \) 2>/dev/null   # 41 hits
# content scan for D0CF11E0A1B11AE1 over /home/vgpnk/Projects /usr/share /usr/lib/libreoffice /usr /var /srv /etc /root /home /mnt /media and every .qcache file (read-only)
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py <file>
python3 corpus/evidence/round54/c1-count.py --seed 54 --per-leg 2 --work <scratch>/counter-work
soffice -env:UserInstallation=file://<scratch>/prof --headless --convert-to "txt:Text (encoded):UTF8" --outdir <scratch>/oracle <doc>
```

## A. Every OLE blob on this host outside the five pinned `.raw` (15 distinct byte-blobs)

| blob sha256[:16] | files (read-only) | tool rc | class |
|---|---|---|---|
| `d341c133e37d65f0` | kasegi r12,r13,r14 `std2020_wd.doc` | 0 (33239 B) | **byte twin of pinned `54fe0734`/`74ced3e9`** |
| `ac0fad62ed9a11fa` | chousa r13 `nmpa-2019-27-annex.doc` | 0 (34234 B) | **byte twin of pinned `bdff491a`** |
| `870203c496f701c9` | lore r13,r16 `sflep_xls.xls` | 2 | `REFUSED ole-not-word` |
| 10 distinct `*.sdv` (`cf35c46f…`,`65365530165a…`,`333c629c…`,`435f2614…`,`7e8258e3…`,`c95fce33…`,`847dddb6…`,`15150424…`,`aebc8d49…`,`be67cc35…`) | `/usr/lib/libreoffice/share/gallery/` + user `sg30.sdv` | 2 each | `REFUSED ole-not-word` |
| `d681031dc93c8989`, `c60d93180d277268` | `/usr/share/cmake/Templates/CMakeVSMacros{1,2}.vsmacros` | 2 each | `REFUSED ole-not-word` |

**No Word `.doc` bytes exist on this host outside the pinned set.** Both host `.doc` files are byte-identical
to pinned captures — `cmp` clean, sha256 equal — so the counter's four distinct documents are the whole Word
corpus this host can offer. Every other OLE blob (spreadsheet, StarOffice gallery, VS macro storage) is refused
`ole-not-word`, exit 2, stdout empty, no `Traceback`. The 32 extension hits that are not OLE (4 graphviz
`.dot`, 1 kbd `no-latin1.doc`, 25 gettext `.msg`, 1 `firebird.msg`) refuse `REFUSED neither a zip package nor an OLE compound file`.

## B. The counter's REAL comparison, verbatim, on the held-out Word instances

| document | rc | flat | oracle flat | ratio | 0.90–1.10 | unheld | lines needing the ≤12-char label drop |
|---|---|---|---|---|---|---|---|
| host `std2020_wd.doc` (≡ 54fe0734) | 0 | 11448 | 11779 | 0.972 | pass | 0 | **119 of 344** |
| host `nmpa-2019-27-annex.doc` (≡ bdff491a) | 0 | 12480 | 12494 | 0.999 | pass | 0 | 14 of 248 |
| pinned `6dc68fd6` (no host copy) | 0 | 24667 | 24667 | 1.000 | pass | 0 | 0 of 386 |
| pinned `b539a802` (no host copy) | 0 | 792 | 800 | 0.990 | pass | 0 | 1 of 14 |

REAL passes on held-out instances, but for `54fe0734` **35 % of held lines** need the leading-label escape — it
is load-bearing, not incidental. Char-level diff tool vs oracle for `54fe0734`: 293 chars only in the tool, 624
only in the oracle, of which 9×`——` and the TOC numbers `1`…`11` (LibreOffice renders auto-numbering; Word keeps
it in the list tables, not the text stream). The tool's flat form also opens with a 260-char cover block the
LibreOffice export omits (`ICS35.040L80中华人民共和国国家标准…`); the line check is one-directional, so extra tool text passes.

## C. Six documents from inputs the counter's generator never makes

The generator is HTML→`.doc` with `<p>`, `<table>` and one `<a href>`; its documents carry `ccpText` and nothing
else (checked: `gaudit0/1.doc` → `{'ccpText': 495}` / `{'ccpText': 524}`). Built from RTF and flat-ODF instead:

| feature | substory in the `.doc` | rc | flat / oracle | REAL | text form vs the docstring |
|---|---|---|---|---|---|
| footnote | `ccpFtn=40` | 0 | 75 / 76, 0.987 | **FAIL** | footnote body excluded ✔ ("footnotes … are not in it"), but the **reference mark U+0002 is dropped** while LibreOffice renders it as the digit `1`. Unheld line: `Sentence with a footnote1 and more body words.` |
| header + footer | `ccpHdd=133` | 0 | 55 / 55, 1.000 | pass | excluded ✔ ("headers … are not in it"); the txt export excludes them too, so both agree |
| text box | `ccpTxbx=38` | 0 | 83 / 83, 1.000 | pass | excluded ✔; the `0x08` shape anchor emits nothing per "every other code point below 0x20" |
| nested table | `ccpText` only | 0 | 157 / 157, 1.000 | pass | every outer **and inner** cell kept in document order; `0x07` cell/row ends → newline as documented |
| TOC field | `ccpText` only | 0 | 178 / 178, 1.000 | pass | code `TOC \o "1-2" \h` dropped, result kept ✔; empty result emits nothing ✔; nested `PAGEREF` drops the code and keeps `5` ✔ |
| inline image | `Data` stream | 0 | 93 / 93, 1.000 | pass | `0x01` anchor emits nothing; picture bytes never enter the text form ✔ |

Only the footnote breaks the counter's REAL rule, and it breaks it *while the tool matches its docstring*: U+0002
is below 0x20, so "every other code point below 0x20 emits nothing" drops it, but the oracle's reader text carries
the anchor digit. Consequence: a quote copied from a reader that spans an anchor is unlocatable —
`--locate 'MARKERTOKEN1 tail…'` → `LOCATED count=0 offset=-1`, the label-free quote → `count=1`.

## D. Quantitative falsifier: auto-numbered lists sink the ratio floor

Labels live in the `.doc` list tables, never in the text stream, so the tool cannot emit them while the oracle
renders them. Same shape, growing density (`<ol>` short items; the generator never emits `<ol>`):

| items | tool flat | oracle flat | ratio | REAL |
|---|---|---|---|---|
| 20 | 496 | 547 | 0.907 | pass |
| 40 | 976 | 1087 | **0.898** | **FAIL (below 0.90)** |
| 80 | 1936 | 2167 | 0.893 | FAIL |
| 160 | 3978 | 4510 | 0.882 | FAIL |

Zero unheld lines in every row — the failure is purely the length band. A real numbered-clause standard (this
corpus's own document class) fails REAL at ≥40 short items although its text form holds every line.
`--locate '2. Clause 2 ZZZ2 MARKERTOKEN'` → `LOCATED count=0`; the label-free quote → `count=1`.

## E. Other byte-level checks against the docstring

- `0x1E` → `-` and `0x1F` dropped: built `A\x1eB` / `C\x1fD` → `A-B` / `CD`; U+00A0 kept, as documented.
- cp1252 bytes undefined in cp1252 (`0x81,0x8D,0x8F,0x90,0x9D`) map via `chr(c)` to **C1 controls** (`U+0081`…),
  above 0x20 and not U+FFFD, so "below 0x20" and "no U+FFFD" both pass while a control enters the text form.
  Demonstrated by overwriting file offset 11100 of `6dc68fd6` (inside its 349-byte compressed piece) with `0x81`:
  rc=0, output contains `U+0081`. That is the docstring's stated behaviour, not a drift.
- `fComplex` (fast-saved) is set only on `bdff491a` (`flags=0x5014`) and reads correctly (0.999); `0Table` is
  exercised only by `bdff491a`, `1Table` by the rest — both branches covered by real bytes.
- CFB paths: pinned captures use sector chains (`WordDocument` 82 KB–174 KB, ss=512, cutoff 4096); the generated
  documents land in the **mini stream** (WordDocument 3.6 KB) — GEN and REAL exercise the two stream paths.
- No OLE file here uses sector shift 12; every blob is `shift=9`, so the tool's 4096-sector branch is unexercised.

## Frozen counter status (for the L1; not a verdict on C1)
```
c1-count.py --seed 54 --per-leg 2 --work … → LEGS=6/6, C1=PASS ;  unseeded (seed 801097686) → LEGS=6/6, C1=PASS
```
C1 as frozen holds; what does not generalize is its REAL rule beyond the five pinned captures (C, D).

## Tooling
No installs or upgrades; stdlib only plus the host `soffice` (LibreOffice 26.8.1.1). No network, no `pacman`, nothing written outside my scratch and this report.

## Risks / blockers
- REAL's oracle tolerance is doing real work: 35 % of `54fe0734`'s lines need the ≤12-char label drop and the band fails at 0.898 for a 40-item list, so a future pinned numbered standard reddens the leg for a reason unrelated to the tool.
- Held-out Word coverage is exhausted on this host; further Word-byte falsification needs a capture the cache does not hold, which L0 `8d77e6c1` forbids this round.
- C1's GEN leg never makes a footnote, header/footer, text box, TOC field, image or auto-numbered list, so all of C and D is invisible to it by construction.

VERDICT: attacked the frozen C1 OLE text form with every OLE blob on the host (15 distinct; **0 new Word bytes** —
both host `.doc` files are byte twins of pinned captures, the rest correctly `ole-not-word`) and with six feature
documents plus a list-density ladder from inputs the counter never makes: the tool matches its docstring on all
six and REAL passes every real Word instance (0.972/0.999/1.000/0.990), but the counter's own REAL rule fails on a
document with a footnote reference mark (unheld `Sentence with a footnote1 …`) and on numbered lists at ≥40 items
(ratio 0.898 < 0.90) — findings reported, predicates untouched.
