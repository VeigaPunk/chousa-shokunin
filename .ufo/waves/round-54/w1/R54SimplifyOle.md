# R54SimplifyOle — YAGNI review of the C1 candidate (OLE `.doc` text form)

seat R54SimplifyOle (leaf, no dispatch) · lane chousa-shokunin · 2026-10-26

## Target and identity
- Candidate `tools/capture-text.py` at `8a7d0f137a352000d78704ba5695ded8857104fe`, sha256
  `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89` (= `git cat-file -p
  8a7d0f1:tools/capture-text.py | sha256sum`), so every line number below is the candidate's. Base
  `c49ffc6c…`: `git diff --stat` = `242 insertions(+), 4 deletions(-)`; OLE block = lines 125-347.
- **Drift (not mine, untouched):** the working tree ≠ candidate — `sha256sum tools/capture-text.py` =
  `e7e381b675353e85578f04d0fba6948d4b6d532b174c7d3baff5c8fcfe65009d`, `git status --porcelain` =
  ` M tools/capture-text.py` (uncommitted +4/-1 Prc bound, hunk in §6), so `c1-count.py`'s default
  `--tool` no longer measures the candidate — its printed `sha256=` is the only discriminator.

## Method (cwd `/fast/scratch/hyaku/chousa-r54/R54SimplifyOle`, `TMPDIR` = scratch)
1. Coverage: `instr.py` = candidate + `sys.settrace` recorder (16 lines after `from __future__`, path
   from `C1_TRACE`), run under the frozen counter `c1-count.py --tool …/instr.py --seed 54` →
   `GEN NONWORD ENCRYPTED MALFORMED REAL REGRESS = PASS`, `LEGS=6/6`, `C1=PASS`; 22 `Cfb` constructions,
   19 `doc_text_form` bodies, 136 `text_form` calls, 10 345 line records.
2. Deletions: variants `vA…vH`, each through the same counter (`--tool <v> --seed 54 --per-leg 3`) plus
   sha256 of each pinned capture's text form; `vH` = the two recommended deletions combined.
3. Five extra documents made at review time with local `soffice`
   (`-env:UserInstallation=file://$S/prof`) to separate *dead* from *merely unmeasured*: `ctl.doc`
   (U+2011 + U+00AD), `big.doc` (8 089 088 B, `nfat=124 difat0=0x3680 ndifat=1` → real DIFAT),
   `ctl-v4.doc` (4096-byte-sector CFB re-laid from `ctl.doc`), `hdr-ascii.doc`/`hdr-cjk.doc`
   (docx with `<w:headerReference>`, `ccpHdd=37`/`27`).

## Coverage — what the frozen legs never execute (candidate line → hits)
```
0 hits: 135 short/unsigned guard · 147 nfat>nsect · 152-157 DIFAT body · 160 FAT outside · 174 dir-name
length · 181 no root · 199 chain cycle · 206 stream>chain · 214 stream>MAX_PART · 221/225/230 mini guards
· 245 wIdent · 251 nFib<0xC1 · 257/261/264 FIB walk · 267/269 table/Clx · 273-283 Prc/Pcdt/PlcPcd
· 287/296/301 piece bounds · 289 cp0>=ccpText break · 324 0x1E -> "-" · 339/342 OLE>MAX_PART/MemoryError
hit: 138 shift refusal 1 · 144 partial-sector pad 4 · 217/218 regular vs mini 23/6 · 222 mini sectors 222
· 137 shift in (9,12) evaluated 22 never true · 293/299 compressed/UTF-16LE 4/73 · field marks 229 each
```
Leg-exercised core: magic, FAT via `difat[0]`, directory, **both** stream paths, v3 size mask, padding,
both piece encodings, field stack, tab — everything else above needs input no leg makes.

## Deletions (each proven inert: `LEGS=6/6`, `C1=PASS`, identical pinned text forms)
Pinned receipt — `cmp -s hashes-base.tsv hashes-<v>.tsv` succeeds for A,B,C,D,E,F,G,H:
```
54fe0734c01f699e735b4b0a	7dbf2a21706b5c04	rc=0   b539a80218080da56a75b624	70ca0f0d6d4a7c34	rc=0
74ced3e9311594a8cc3f1f42	7dbf2a21706b5c04	rc=0   bdff491a75c6abeda1d9c01d	f0b0899794420b0c	rc=0
6dc68fd6b32ce9c8dfcebcebce8	a8e3e7ad213b6ec5	rc=0
tool=…/orig.py sha256=fd0ed3f5… GEN/NONWORD/ENCRYPTED/MALFORMED/REAL/REGRESS=PASS LEGS=6/6 C1=PASS
tool=…/vH.py   sha256=ed173f02… LEGS=6/6 C1=PASS          (seed=54 per-leg=3 for every run)
```
**A. `ndifat` dead binding — DELETE (recommended).** 141
`self.cutoff, mfat0, nmfat, difat0, ndifat = struct.unpack_from("<IIIII", data, 0x38)`; AST walk:
`ndifat loads=[] stores=[141]` (no LSP device in this seat — `read xd://lsp` → "No such tool"; this is
a structural AST reference check, not LSP-semantic). `vA` unpacks `<IIII` into 4 names: `LEGS=6/6`,
5/5 pinned hashes identical, five extra docs `→ same` (`big.doc orig=987592b2406f00b9 vA=… same`).
**B. Duplicate OLE-magic authority — DELETE the clause (recommended).** 134
`if len(data) < 512 or data[:8] != OLE_MAGIC:` re-checks bytes `text_form` already compared (334); AST:
`Cfb loads=[240]` only, inside `doc_text_form` (def 239) whose only load is 340 inside `text_form`, so
`data[:8] != OLE_MAGIC` is unreachable by construction and only `len(data) < 512` is live. `vG` narrows
it → `LEGS=6/6`, 5/5 pinned hashes identical. Net removed: one clause, one duplicated rule.
**C. Three branches qualify literally but do not earn deletion** — each is a third authority for a
condition another branch refuses in the same class: 214 `if size > MAX_PART:` (`vE`, capture claiming a
314572800-byte `WordDocument`: `REFUSED ole-malformed: sector 42 outside the file` vs the candidate's
`… stream 'WordDocument' of 314572800 bytes (limit 268435456)`); 146 `if nfat > self.nsect:` (`vF`,
`nfat=9999`: `… FAT sector outside the file` vs `… 9999 FAT sectors in a 18-sector file`); 159
`if any(x >= self.nsect …)` — redundant with `sector()` (192), which refuses the same class and is
exactly what `vE` printed, while 159 is `vF`'s fallback. All three keep `LEGS=6/6` + identical hashes
when dropped; tradeoff is 1-2 lines each buying a message that names the anomaly, so `vH` keeps them.

## Unexercised but load-bearing — KEEP (each with a counterfactual receipt)
A-G all give `LEGS=6/6` and identical pinned text forms, so "inert under the legs" cannot decide these.
- **DIFAT body 150-157 + `FREESECT` 126.** `vB` (loop removed) on a plain 8 MB LibreOffice `.doc` — no
  leg and no pinned capture exceeds 801 KB, so none needs DIFAT — gives
  `REFUSED ole-malformed: sector chain at 15796` where the candidate prints 7 100 100 bytes; live above ≈7.1 MB.
- **v4 / 4096-byte sectors (137).** `vC` (`shift != 9`) on my 4096-sector CFB: `REFUSED ole-malformed:
  sector shift 12`; the candidate returns `0df6a2cbcf5c2bba`, identical to the 512-sector twin.
- **0x1E → `-` (323-324).** `ctl.doc`'s `WordDocument` holds exactly one U+001E code unit and no U+2011;
  candidate prints `hyphen AAA-BBB …`, `vD` prints `hyphen AAABBB …` — silent character loss.
- **`if cp0 >= ccp_text: break` (288-289).** Unreached in all 11 documents measured (`cp0>=ccpText=0`
  everywhere, header docs included, since `ccpHdd` is truncated by `min(cp1, ccp_text)`). Guard, not
  weight: with `ccpText` shrunk to 1 on a pinned 18-piece capture the candidate prints 1 char exit 0 and
  `vI` (guard removed) gives `REFUSED ole-malformed: piece outside WordDocument` (`cnt` goes negative).
- **cp1252 fallback `or chr(c)` (236).** Only 2 compressed pieces exist (`6dc68fd6…`), none containing
  0x81/0x8D/0x8F/0x90/0x9D, so it is unobserved; documented promise, one `or`.

## Docstring audit — promised but missing?
Present and consistent with the code: signature, `WordDocument`, `wIdent 0xA5EC`, `nFib>=0xC1`,
`fEncrypted|fObfuscated`, `fWhichTblStm` 0x0200, `fcClx/lcbClx`, `ccpText` at Lw[3],
0x0D/0x0B/0x0C/0x07→LF, 0x09→tab, 0x1E→`-`, other <0x20 dropped, 0x13-0x15 stack (no separator →
nothing), class-first `ole-*`, missing table stream. The three named: *v4* — not promised, implemented
and working (§4): undocumented acceptance, not a defect — document it or narrow acceptance. *`ndifat`* —
read, never used; the walk is bounded by `len(difat) < nfat + per` (151), not the header count (§3 A).
*`FREESECT`* — one correct chain terminator (151); every pinned capture has `difat0=0xFFFFFFFE`, so it
is exercised as "terminates immediately".

## 6. Working-tree drift I did not touch (for the L1)
`git -C chousa-shokunin diff -- tools/capture-text.py`, uncommitted (blob `521dadb` → `c1f5831`):
```
-        i += 3 + struct.unpack_from("<h", clx, i + 1)[0]
+        cb_grpprl = struct.unpack_from("<h", clx, i + 1)[0]
+        if cb_grpprl < 0 or i + 3 + cb_grpprl > len(clx):
+            raise Refused("ole-malformed: Prc GrpPrl outside the Clx")
+        i += 3 + cb_grpprl
```
It hardens an unexercised path (274: 0 hits) keeping the class — not weight I would delete, but a
receipt that matters must name the sha it measured.

## Preserved contract
`capture-text.py RAW [--locate QUOTE]`: exit 0 with the text form; exit 2 with
`REFUSED ole-not-word|ole-encrypted|ole-malformed` and empty stdout; `LOCATED count=<n> offset=<o>`
against that form. The `.docx` path is untouched by every variant (`REGRESS` = `LEGS=9/9` +
`SUPPLEMENT_LEGS=4/4` in all nine runs); `vH` changes no line of any measured text form.

## Tooling
Nothing installed (no pacman/uv/npm needed; `python3`, `soffice` present). Every `soffice` run used `-env:UserInstallation=file://$S/prof`; scratch removed.

VERDICT: built a line-coverage profile of the C1 candidate under the frozen counter and deleted in
scratch — two true dead-weight items (`ndifat` binding, duplicate OLE-magic clause) are inert
(`vH`: `LEGS=6/6`, 5/5 pinned text forms byte-identical), three size/count guards are inert but earn
their one line, and the five remaining unexercised branches (DIFAT, v4, 0x1E, the `ccpText` break,
cp1252 fallback) are load-bearing for real documents no leg makes — the patch's weight is justified
except those two lines.
