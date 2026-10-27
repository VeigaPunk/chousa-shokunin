# R54ReviewOleTool — line-by-line review of the C1 candidate's OLE `.doc` text form

**Under review.** `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff c49ffc6ce1c3de87c1dfa96856239ed7274bf07b 8a7d0f137a352000d78704ba5695ded8857104fe -- tools/capture-text.py` (+242/-4), read against [MS-CFB] and [MS-DOC] from memory (no fetch) and against the tool's own docstring.
**Identity.** `sha256sum tools/capture-text.py` in the lane = `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89` = my scratch copy = the candidate at 8a7d0f1. Line numbers below are that file's.
**Nothing frozen is touched.** No predicate, target, counter or control is proposed for change; F1 below is a defect in the *tool*, and the 4-line fix I verified keeps the frozen counter at 6/6 (§5).
**Environment.** Python 3.14.8, LibreOffice 26.8.1.1. Scratch `/fast/scratch/hyaku/chousa-r54/R54ReviewOleTool` (removed at exit; `pgrep -u $USER -f soffice` empty at the end — no `soffice.bin` left). **No tool installed** (nothing to install; `olefile` was not needed — the point is to test the candidate's own reader, not to replace it).

## 1. Spec conformance that holds (each item run, not reasoned)

Probe harness (scratch-only, removed at exit): `mkdoc.py` (a synthetic MS-CFB/MS-DOC writer) + `test_driver.py`, `probe_prc.py`, `probe_more.py`; the tool is run as `python3 tool_candidate.py <file>`.

| # | [MS-CFB]/[MS-DOC] item | candidate site | observed |
|---|---|---|---|
| 1 | header: sector shift 0x1E / mini 0x20, FAT count 0x2C, dir start 0x30, cutoff 0x38, mini FAT 0x3C/0x40, DIFAT 0x44/0x48, DIFAT array 0x4C (109 entries → byte 512) | 136, 140, 141, 148 | all offsets correct; `struct.unpack_from("<109I", data, 0x4C)` ends exactly at 512 |
| 2 | v4 (4096-byte) sectors: sector 0 at file offset 4096 | 190 `(sid+1)*self.ss` | `e-v4.doc` (shift 12, 4096-byte sectors): `rc=0 stdout='Hello 世界\nSecond paragraph\n'` |
| 3 | 64-bit stream size; v3 masks to 32 bits | 176 `<IQ` @116, 177 | correct for both sector sizes |
| 4 | DIFAT chain: each sector holds ss/4−1 FAT ids, **last 4 bytes = next pointer** | 150-158 | `j-difat.doc`: 128 FAT sectors + 1 DIFAT sector (16,130,560 B): `rc=0 stdout_len=8000000` |
| 5 | directory: NameLength 2..64, type 5 = root, type 0 = unallocated, name = UTF-16LE minus the null | 170-179 | `REFUSED ole-malformed: directory entry N name length` / `no root entry` reachable; valid entries decode (`\x05SummaryInformation`, `\x01CompObj`) |
| 6 | mini stream lives in the **root entry**'s stream; mini FAT chain | 183, 213-232 | `f-mini.doc` (WordDocument+1Table both <4096 → mini stream): `rc=0 stdout='Hello 世界\n…'` |
| 7 | FIB flags: fWhichTblStm 0x0200, fEncrypted 0x0100, fObfuscated 0x8000 | 248, 267 | `p3-obfuscated.doc` (0x8200): `REFUSED ole-encrypted: FIB fEncrypted/fObfuscated set`; `p8-0table.doc` (flag 0 → `0Table`): `rc=0 stdout='Hello\n'`; the real capture `bdff491a…` has flag 0 → `0Table` and reads ✓ |
| 8 | csw/cslw/cbRgFcLcb walk; **ccpText = FibRgLw97 index 3** (FIB 0x4C); **fcClx = FibRgFcLcb97 index 33** (FIB 0x1A2) | 254-262 | confirmed against the four real captures: e.g. `6dc68fd6…` gives ccpText 27791 and a piece table whose CPs run 0…27791; `bdff491a…` gives ccpText 13804 with piece CPs to 13962 (= ccpText+ccpHdd 152+ccpTxbx 5+1) → the clip to ccpText is right |
| 9 | wIdent 0xA5EC, nFib ≥ 0xC1 | 244, 250 | `p5-wident.doc` → `REFUSED ole-not-word: … wIdent 0xA5EC`; `p4-nfib95.doc` (nFib 0x65) → `REFUSED ole-not-word: nFib 0x65 predates Word 97` |
| 10 | Prc (clxt 0x01) skipped, **cbGrpprl signed** | 271-274 | valid Prcs skipped: `p1-prc-valid.doc` and `p2-prc-two.doc` → `rc=0 stdout='Hello\n'` — **but see F1 for invalid ones** |
| 11 | PlcPcd size = 12n+4; PCD = 2 flag + 4 fc + 2 prm | 285-291 | `(lcb-4) % 12` enforced; fc read at `4*(n+1)+8*k+2` ✓ |
| 12 | FcCompressed = bit 30, byte offset = fc/2 | 292-295 | real compressed pieces in `6dc68fd6…` (piece 7 `fc=0x40005400` → offset 10752, piece 9 `fc=0x40005c00` → 11776) decode as cp1252 ✓ |
| 13 | **cp1252 map, incl. the five undefined bytes** | 235-237 | Python's cp1252 leaves exactly `0x81 0x8D 0x8F 0x90 0x9D` undefined; the tool's `or chr(c)` fallback maps them to U+0081/008D/008F/0090/009D ("the same code point", as the docstring says) — `d-cp1252.doc` stdout = `A€‚‘Ÿ\u0081\u008d\u008f\u0090\u009dB\n` (0x80→U+20AC, 0x82→U+201A, 0x91→U+2018, 0x9F→U+0178) ✓ |
| 14 | field model: 0x13 begin / 0x14 separator / 0x15 end; code dropped, result kept; a field with no separator emits nothing | 306-317 | `h-fields.doc` (`A\x13 HYPERLINK "http://x" \x14anchor\x15B\x13nocode\x15C`) → `stdout='AanchorBC\n'` (URL absent) |
| 15 | nested fields: an inner field's result inside the **outer code** region is code; inside the **outer result** region it is text | 317 `any(stack)` | `nested.doc` → `stdout='Aouter-result r2 B\n'` (inner result in the outer code dropped; inner result in the outer result kept) |
| 16 | 0x0D/0x0B/0x0C/0x07 → newline, 0x09 → tab, 0x1E → `-`, other <0x20 → nothing | 318-325 | `cells.doc` (`a\x07b\x07c\x0d`) → `'a\nb\nc\n'` |
| 17 | refusals `ole-not-word` / `ole-encrypted` / `ole-malformed`, exit 2, nothing on stdout | 241-283 | `p6-no-table.doc` → `REFUSED ole-malformed: the FIB's table stream is missing`; `g-piece-oob.doc` → `REFUSED ole-malformed: piece outside WordDocument`; `p7-fcclx-oob.doc` → `REFUSED ole-malformed: Clx outside the table stream` |
| 18 | the five pinned campaign captures read as OLE Word 97+ | 239-325 | all four distinct documents: exit 0, **0 U+FFFD, 0 control chars** (tool output vs the counter's LibreOffice oracle: ratio 0.9719 / 1.0000 / 0.9900 / 0.9989, every oracle line ≥8 chars found) |

## 2. F1 (defect, medium) — the Clx Prc walk trusts a signed `cbGrpprl`: a malformed `.doc` hangs the tool forever or crashes it with a Traceback

`tools/capture-text.py:271-274`:

```python
271:    while i < len(clx) and clx[i] == 0x01:
272:        if i + 3 > len(clx):
273:            raise Refused("ole-malformed: truncated Prc in the Clx")
274:        i += 3 + struct.unpack_from("<h", clx, i + 1)[0]
```

`cbGrpprl` is read as a **signed** 16-bit value (correct per MS-DOC 2.9.75) but is used unchecked: a negative value makes `i` shrink, so the loop either never advances (an infinite spin) or indexes before the buffer (IndexError). The tool's own docstring promises "`ole-malformed` (a sector, chain, directory entry, **Clx** or piece outside its stream or file …)", and the counter's refusal contract is "exit 2, nothing on stdout, a stderr line starting `REFUSED ole-malformed`, **no Traceback**" — neither holds.

Reproduction (scratch, absolute paths):

```
$ python3 probe_prc.py
cbGrpprl=-3: TIMEOUT after 10s (the tool hangs)
cbGrpprl=-100: rc=1 stdout=b''
    stderr last line: ['IndexError: index out of range']
    Traceback present -> uncaught exception
cbGrpprl=-32768: rc=1 stdout=b''
    stderr last line: ['IndexError: index out of range']
    Traceback present -> uncaught exception
cbGrpprl=-4: rc=2 stdout=b''   stderr='REFUSED ole-malformed: no Pcdt in the Clx'
cbGrpprl=0:  rc=2 stdout=b''   stderr='REFUSED ole-malformed: no Pcdt in the Clx'
```

```
$ python3 tool_candidate.py cases/prc--100.doc ; echo "rc=$?"
Traceback (most recent call last):
  File ".../tool_candidate.py", line 400, in <module>    sys.exit(main())
  File ".../tool_candidate.py", line 384, in main        text = text_form(a.raw)
  File ".../tool_candidate.py", line 340, in text_form   return doc_text_form(data)
  File ".../tool_candidate.py", line 271, in doc_text_form
    while i < len(clx) and clx[i] == 0x01:
                           ~~~^^^
IndexError: index out of range
rc=1
```

The fixture is a well-formed CFB (v3, WordDocument + 1Table in the mini stream) whose Clx is `01 FD FF` (clxt 0x01, cbGrpprl = −3) followed by a valid Pcdt — i.e. the kind of file an untrusted capture can be. `cases/prc--3.doc` never returns (the counter's own `timeout=300` would turn the hang into a leg failure; a lane workflow reading a hostile capture hangs outright).

**Fix (verified, L1 integrates) — `tools/capture-text.py`:**

```python
    while i < len(clx) and clx[i] == 0x01:
        if i + 3 > len(clx):
            raise Refused("ole-malformed: truncated Prc in the Clx")
        cb_grpprl = struct.unpack_from("<h", clx, i + 1)[0]
        if cb_grpprl < 0 or i + 3 + cb_grpprl > len(clx):
            raise Refused("ole-malformed: Prc GrpPrl outside the Clx")
        i += 3 + cb_grpprl
```

With it: `prc--3` → `REFUSED ole-malformed: Prc GrpPrl outside the Clx` (rc 2), `prc--100` → same, `prc--32768` → same; the valid-Prc probes still print `Hello\n`; and the frozen counter still passes (§5). **Ledger note (2026-10-26, after this review): the lane worktree's `tools/capture-text.py` already carries this exact hunk uncommitted (`sha256 e7e381b675353e85578f04d0fba6948d4b6d532b174c7d3baff5c8fcfe65009d`, = my patched copy; HEAD is still 9caf8fc) — the defect as reviewed belongs to the candidate commit 8a7d0f1.**

## 3. F2 (verification gap, not a claim change) — the frozen counter cannot see F1

`corpus/evidence/round54/c1-count.py` `leg_malformed` builds exactly two shapes: the file cut short before the WordDocument stream, and a sector shift of 7. Neither reaches the Clx walk, so `MALFORMED=PASS` certifies nothing about the Prc/Pcdt path. The five OLE captures that exist in the campaign cache (the only OLE-magic `.raw` files under `.qcache`, verified by scanning every `*.raw` for `D0CF11E0A1B11AE1`) all parse cleanly, so F1 is **latent today** — it is a hazard for any future capture, not a present misreading. I report it; I do not propose changing the frozen leg.

## 4. F3 (doc drift, owner: L1) — the landed docs now describe the tool falsely

* `SKILL.md:134` (the `capture-text` Gates row): "Reads OOXML zips only: an OLE `.doc` (UTF-16LE runs, round 48), a PDF or an HTML capture is refused, not converted" — now false: the candidate reads an OLE `.doc` through the CFB/FIB/piece-table reader, and the row's exit-2 list (`not a zip, …`) lacks the three `ole-*` classes.
* `corpus/README.md:1120`: "the text form of an OOXML `.docx` capture … refusals for non-zip, relationship-less, non-Word and inflated packages" — the tool no longer refuses an OLE file as "not a zip" (`c1-before.txt` shows the base message `REFUSED not a zip (an OOXML capture is a zip package)`; the candidate's message is `neither a zip package nor an OLE compound file (a Word capture is one of them)`), and it now has three more refusal classes.
* `corpus/QUALITY.md` 87 says the defined text form is "tools/capture-text.py **for OOXML**"; QUALITY is append-only, so this wants a new criterion for the OLE form rather than an edit.

## 5. What I measured of the frozen counter (read-only runs, TMPDIR in my scratch)

```
$ python3 corpus/evidence/round54/c1-count.py --tool $S/tool_candidate.py --seed 7 --per-leg 2 --work $S/work-seed7
GEN=PASS 2 docs | NONWORD=PASS 2 sheets | ENCRYPTED=PASS 2 docs | MALFORMED=PASS 2 docs | REAL=PASS 5 captures | REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6
C1=PASS
$ python3 …/c1-count.py --tool $S/tool_candidate.py --per-leg 3 --work $S/work-unseeded     # seed 156681170
LEGS=6/6   C1=PASS
$ python3 …/c1-count.py --tool $S/tool_patched.py --seed 7 --per-leg 2 --work $S/work-patched
LEGS=6/6   C1=PASS        # the F1 fix changes nothing for the frozen claim
```

So C1 as frozen **does** measure 6/6 on the candidate, twice, plus once on the F1-fixed copy. My review's objection is to the tool's uncovered Clx path, not to the counter's verdict.

## 6. Residual risk / gaps in my own review

* I could not run a real MS Word-written `.doc` (no such capture on disk and no network): the compressed-piece path was exercised only by `6dc68fd6…` (two cp1252 pieces) and by my synthetic `d-cp1252.doc`.
* Not exercised on real bytes: a Word 2003+ FIB with `cbRgFcLcb` ≠ 93 (the captures carry 164/183 — the candidate walks the counts instead of assuming 93, which is why they read correctly; noted, not a defect), `fComplex` fast-saved documents, and a `.doc` whose Clx carries a `Prc` (LibreOffice writes none). The text form omits auto-generated list numbering and the header/footer story (docstring: "main document story only") — the same shape as the `.docx` form; it is why `54fe0734…`'s flat length ratio is 0.9719 rather than 1.0.

**VERDICT: reviewed the candidate `tools/capture-text.py` (8a7d0f1) line by line against [MS-CFB]/[MS-DOC] and its docstring — 18 spec items verified by running 20 synthetic probes plus the four real OLE captures (all correct: header offsets, v4 sectors, 64-bit sizes, DIFAT chain, mini stream, FIB walk and ccpText/fcClx indices, PlcPcd, fc/2 compressed pieces, the cp1252 map with its five undefined bytes, the field/nesting model, the three `ole-*` refusals), found one real defect (F1: the Clx Prc walk trusts a signed `cbGrpprl` → a malformed `.doc` hangs the tool forever or exits 1 with a Traceback instead of `REFUSED ole-malformed`; a 4-line bound fixes it and the frozen counter still reads 6/6), one counter blind spot (F2: the frozen MALFORMED leg never reaches the Clx) and one doc-drift finding (F3: SKILL.md:134 and corpus/README.md:1120 still call the tool OOXML-only).**
