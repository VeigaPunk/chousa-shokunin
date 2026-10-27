# R54ExecDocxRegress — byte-identity of the OOXML path, and the refusal-wording change

seat `R54ExecDocxRegress` (executor) · chousa · round 54 · wave 1 · axes operability, depth
base `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b` · candidate `8a7d0f137a352000d78704ba5695ded8857104fe`
scratch `/fast/scratch/hyaku/chousa-r54/R54ExecDocxRegress/` (removed on exit). Read-only elsewhere; the
only file written is this report. Nothing frozen is touched: findings are reported, not patched.

## 0. The bytes I measured (the tool changed under me mid-wave)

```
$ git -C …/chousa-shokunin show c49ffc6…:tools/capture-text.py > $S/base.py
$ git -C …/chousa-shokunin show 8a7d0f1…:tools/capture-text.py > $S/cand_committed.py
$ cp …/chousa-shokunin/tools/capture-text.py $S/cand_worktree.py && sha256sum $S/*.py
6902db6acf3ae5a0ac579ff88ae4fe4a36877b7b960c438bf36a67007b26be17  base.py            (= BASE_REV)
fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89  cand_committed.py  (= candidate 8a7d0f1)
e7e381b675353e85578f04d0fba6948d4b6d532b174c7d3baff5c8fcfe65009d  cand_worktree.py  (UNCOMMITTED)
$ diff cand_committed.py cand_worktree.py
<         i += 3 + struct.unpack_from("<h", clx, i + 1)[0]          # signed cbGrpPrl, unchecked
>         cb_grpprl = struct.unpack_from("<h", clx, i + 1)[0]
>         if cb_grpprl < 0 or i + 3 + cb_grpprl > len(clx):
>             raise Refused("ole-malformed: Prc GrpPrl outside the Clx")
>         i += 3 + cb_grpprl
```
The committed bytes are what the frozen counter names; the working-tree edit is another seat's
(`R54ReviewOleTool.md` F1). **Committed bytes hang on a crafted `.doc`; worktree bytes refuse it (F1).**

## 1. The OOXML path is byte-identical — 8 zip captures, 5 hand-built variants

Cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`: 2596 `.raw` = 8 zip
(`PK\x03\x04`) + 5 OLE + 2583 other. Base vs committed candidate — stdout sha256(16), exit, stderr:

```
3a8b45977cd1 base rc=0 sha=754aae4266a1 | cand rc=0 sha=754aae4266a1 | stderr identical=True
b825f17cafd0 base rc=0 sha=9ef944621610 | cand rc=0 sha=9ef944621610 | stderr identical=True
68a1f5a90ad0 / 6fef2cd89a58 / bcaebc1a0c62  base rc=2 sha=e3b0c44298fc | cand rc=2 sha=e3b0c44298fc | identical=True  REFUSED no _rels/.rels in the package
9990f37099e6 base rc=2 sha=e3b0c44298fc | cand rc=2 sha=e3b0c44298fc | identical=True  REFUSED no officeDocument relationship in _rels/.rels
cb101e95f5f5 / e9761e99ba40  base rc=2 sha=e3b0c44298fc | cand rc=2 sha=e3b0c44298fc | identical=True  REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root {…spreadsheetml/2006/main}workbook)
```
**Zero differences on the zip path** (all 8: stdout bytes, exit code, stderr). Five hand-built variants
(plain package with `mc:Fallback`/`w:delText`/`w:instrText`/`w:tab`/`w:br`; no `_rels/.rels`; External
`officeDocument` first; percent-encoded target; `.xlsx` root) identical too: `plain`/`external_first`/
`pct_target` → `rc=0 sha=7d8cbf4a0996` on both, `no_rels`/`root_xlsx` → `rc=2` on both. The candidate's
OOXML form equals the frozen builder's independent reader `build-spans.py docx_text` (`3a8b45977cd1`
equal=True len 19682, `b825f17cafd0` equal=True len 18841; the other six `None`/`''` on both sides).
**Finding: the candidate is a strict superset on the OOXML path** — it re-routes only files whose first
8 bytes are the OLE magic; every other byte takes the identical branch.

## 2. The OLE path is the intended difference (base refuses, candidate renders)

Five OLE captures = the C1 counter's five pins, four distinct documents (`74ced3e9…` is a byte twin of
`54fe0734…`; identical output). Base stderr on 4 of them: `REFUSED not a zip (an OOXML capture is a zip
package)`; on `b539a802…`: `REFUSED main part 'theme/theme/themeManager.xml' is not WordprocessingML (root
{…drawingml/2006/main}themeManager)`. Candidate, all five exit 0:

```
54fe0734c01f sha=7dbf2a21706b len=33239   74ced3e93115 sha=7dbf2a21706b len=33239   6dc68fd6b32c sha=a8e3e7ad213b len=47356
b539a8021808 sha=70ca0f0d6d4a7c34 len=2290   bdff491a75c6 sha=f0b089979442 len=34234
```
`b539a802…` is the round-52 erratum E2(a) row (OLE `.doc` with an embedded OPC zip): base refused it as
a theme part, the candidate renders the OLE Word story. No U+FFFD, no code point < 0x20 in any of the
five forms; the two pinned quotes locate once (`6dc68fd6…` `LOCATED count=1 offset=12795`, `bdff491a…
LOCATED count=1 offset=4678`). Independent oracle (private profile, `soffice
-env:UserInstallation=file://$S/prof --headless --convert-to "txt:Text (encoded):UTF8"`): **0 oracle
lines missing**, whitespace-free ratios **0.972 / 0.972 / 1.000 / 0.990 / 0.999**.

## 3. The refusal wording changed — and breaks nothing that consumes it

New text `REFUSED neither a zip package nor an OLE compound file (a Word capture is one of them)`
(`tools/capture-text.py:347`); old `REFUSED not a zip (an OOXML capture is a zip package)`.
**20 non-zip non-OLE captures (10 PDF + 10 HTML), base vs candidate — every one: base `2 0` / cand `2 0`**
(10 PDF by `%PDF-` magic, 10 HTML by `<html`/`<!doctype html` in the sidecar head), e.g.
`02408e0c9018e826396cd149.raw base 2 0 | cand 2 0`, `25671090f50c165a0d4c0ab9.raw base 2 0 | cand 2 0`.
**Whole population, all 2583 non-zip non-OLE `.raw`, both tools:** `base(rc,out) cand(rc,out) =
(2,0,2,0) → 2583` · exit-code differences **0** · stdout-length differences **0**.
Audit of every lane file matching the old wording (`grep -rn 'not a zip' … | grep -v /waves/`):
`round52/c1-count.py:16` + `round52/claims.md:42` (docstring prose; the check is
`any(l.startswith("REFUSED") …)`, `round52/c1-count.py:243`, wording-agnostic — verified
`round52/c1-count.py --tool tools/capture-text.py --seed 54` → `LEGS=9/9 C1=PASS` exit 0 and
`round52/c1-supplement.py --tool tools/capture-text.py --seed 54` → `SUPPLEMENT_LEGS=4/4
C1_SUPPLEMENT=PASS` exit 0, base identical); `round52/controls/naive-tool.py:9` +
`round52/controls/forge-shape.py:31` (the control's own text; controls key on their own bytes);
`round54/controls/c1-before.txt` (base's stderr quoted — a receipt of the *base*'s behaviour, which
must say `not a zip`); `round54/claims.md:71` "the base refuses every OLE file as `not a zip`"
(describes the base — still true, §2); `tools/capture-text.py:49` (the candidate's own docstring —
**cosmetic**: a class list, not a quoted string; `:54` already names the new class);
`SKILL.md:134` (`capture-text` Gates row — **no break, but STALE**: still says "Reads OOXML zips only: an
OLE `.doc` (UTF-16LE runs, round 48) … is refused, not converted", while after the candidate an OLE
`.doc` is rendered; another seat drafts the round-54 Gates rows, the L1 owns the merge);
`corpus/README.md:1120` (same staleness, README row).

**Answer to the assigned question: no lane counter, gate or doc matching the old wording breaks.** Every
consumer keys on the `REFUSED` prefix or on exit code + empty stdout, both unchanged on all 2596 files.

## 4. Findings against the candidate (reported, not patched)

**F1 — the committed candidate hangs forever on a malformed OLE `.doc`; the worktree bytes refuse it.**
The Clx walk adds an unchecked *signed* `cbGrpPrl` (`cand_committed.py:274`), so `-3` leaves `i` still
and `while i < len(clx) and clx[i] == 0x01` never ends. On-disk reproduction built from the real pinned
capture (the `1Table` stream's Clx at file offset 116109 rewritten with a `0x01` Prc whose `cbGrpPrl` is
`-3`, then a valid Pcdt):

```
$ python3 $S/cand_committed.py $S/hang_prc_minus3.doc  → TIMEOUT after 15s (infinite loop)
$ python3 $S/cand_worktree.py  $S/hang_prc_minus3.doc  → rc=2 out=0 'REFUSED ole-malformed: Prc GrpPrl outside the Clx'
```
Sweep of `cbGrpPrl` on the same file: `-1,-2,-4,-5,0,1,2` → committed refuses (`no Pcdt in the Clx`);
**`-3` alone hangs** (committed) / refuses (worktree). The frozen counter cannot see it:
`leg_malformed` (`round54/c1-count.py:238-252`) builds only a file cut short before its WordDocument
stream and a sector shift of 7 — neither reaches the Clx walk. Same defect as `R54ReviewOleTool.md` F1;
my file is an independent on-disk reproduction from a real capture, not a synthetic CFB. **The L1 must
say which bytes are the candidate of record**; the counter measures `fd0ed3f5…` (committed) and passes 6/6
on both (`--tool $S/cand_worktree.py --seed 7 --per-leg 3` → `LEGS=6/6 C1=PASS` exit 0).

**F2 — the candidate exits 1 with a Python Traceback where the base refused with exit 2.** A missing
path, a directory or an unreadable file: base `rc=2 'REFUSED not a zip …'`; candidate `rc=1` +
`FileNotFoundError`/`IsADirectoryError`/`PermissionError` (uncaught, `capture-text.py:332`,
`open(path,"rb")` outside refusal handling). The docstring says exit 2 covers "refused (…) or usage".
No frozen leg passes a nonexistent path, so no leg flips; the exit-code contract regressed for a
non-capture path.

**F3 — otherwise no traceback on malformed OLE bytes.** 400 random-byte mutations of `6dc68fd6…` and
300 OLE-magic random files: **0 tracebacks**, all exit 2; truncations refuse cleanly (`ole-malformed:
short or unsigned header`, `… 2 FAT sectors in a 0-sector file`, `… FAT sector outside the file`).

**F4 — C2's text form for an OLE `.doc` is still the UTF-16LE fallback, not the tool's OLE form.**
`round54/c2-count.py:123-133` resolves a `.raw` digest through `build-spans.py raw_form`, which for a
non-zip is `b.decode("utf-16le", errors="replace")` (`build-spans.py:108-113`) — 263 U+FFFD for
`6dc68fd6…`. The two readers therefore disagree by a constant shift: `文献类型及载体类型标志` is at
**12161** in `raw_form` (the offset lane row `corpus/SOURCES.md:111` and the round-49 span rows use —
verified: all six round-49 `S101` rows re-derive `row_offset + span.find(quote)` = `raw_form.find(quote)`)
but at **12963** in the candidate's OLE form. A span cut from the tool's stdout would **fail** the
counter's `CAPTURE_BOUND` (`ft[o:o+len(span)] == span` against `raw_form` → `False`). C2 never runs the
tool (claims.md says so), so C2 is unaffected — but any seat re-anchoring S101 in the tool's OLE form
must cut the span from `raw_form`.

**F5 — the round-47 gate-registry counter now fails, from the round-54 landing, not the candidate.**
`python3 corpus/evidence/round47/c2-count.py` → `REGISTERED=139/142 UNREGISTERED=3 MISMATCHES=3
C2=FAIL` **exit 1**; `--list` names exactly `corpus/evidence/round54/{build-spans,c1-count,c2-count}.py`.
The same command on the base tree (`git archive c49ffc6…`) → `139/139 UNREGISTERED=0 MISMATCHES=0
C2=PASS` exit 0; the freeze tree (`5a1a206…`) already shows the 3 unregistered paths. A `SKILL.md` Gates
row naming the three round-54 counters is needed (another seat's draft). `round47/c1-count.py` passes.

## 5. Frozen-counter runs (read-only; TMPDIR in my scratch)

```
$ TMPDIR=$S python3 corpus/evidence/round54/c1-count.py --seed 7 --per-leg 3
tool=…/tools/capture-text.py sha256=fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89 seed=7 per-leg=3
GEN=PASS 3 docs · NONWORD=PASS 3 sheets · ENCRYPTED=PASS 3 docs · MALFORMED=PASS 3 docs · REAL=PASS 5 captures
REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4'] · LEGS=6/6 · C1=PASS   (exit 0)
$ … c1-count.py --per-leg 3   (three unseeded runs) → run1/run2/run3 LEGS=6/6 C1=PASS exit 0
$ TMPDIR=$S python3 corpus/evidence/round54/c2-count.py
ENTRIES=2/2 · REFUSED_ENTRIES=0 · HELD_CITED=- HELD_BAD=0 · BOUND=3/3 · REFUSED=0 · BOUND_IDS=S121,S122,S123
REF_ID_UNBOUND=0 · NEW_GROUND=2/2 · QUOTE_ROWS=33 ON_BOUND=33/33 · SPAN_IDS=3/3 · QUOTES_IN_SPAN=33/33
QUOTES_IN_ENTRY=33/33 · QUOTES_IN_LESSON=0/33 · QUOTE_SHORT=33/33 · SPAN_CONTEXT=33/33 · CAPTURE_BOUND=33/33
SUBSTANCE=PASS · ANCHOR_BOUND=3/3 · INFERENCE_GROUNDED=2/2 · QUARANTINE_VERDICTS=0/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0 · C2=FAIL   (exit 1)
```
**C1 passes its frozen counter on the committed candidate (4/4 runs). C2 is nearly met** — only
`QUOTES_IN_LESSON=0/33` and `QUARANTINE_VERDICTS=0/3` are outstanding; both live in
`corpus/lessons/round-54.md`, which does not exist yet (`c2-count.py:150` reads that path). Earlier in
the wave, before the entries landed, the same counter printed `ENTRIES=0/2 BOUND=0/3 C2=FAIL` exit 1.
Quarantine facts for the L1, measured from the captures (`text.find` on each capture's own text form;
**no verdict is offered here**): **S080** (SAMR record, key `adf6ba934e813b2c326fa150`, HTML; `.txt`
sidecar 3591 chars) — the register quote `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01`
occurs **0** times, the sidecar writes `标准号 \n GB/T 7714-2025 …` with **no** `：` (`'标准号：' count 0`,
`'标准号' count 1` at 1327), while its parts are all present (`GB/T 7714-2025` ×2 at 1239, `发布日期` ×1 at
1354, `实施日期` ×1 at 1382, `2025-12-02` ×2, `2026-07-01` ×2). **S088** (JMU PDF, key
`0f33243fd7ac2fe88b85c1ba`, `.txt` sidecar 83 061 chars) — the register quote occurs **0** times; the
capture reads `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` (**no** trailing `ｅ` after `ｍｒ`) and uses
**no** ` / ` separators (`'缩微资料（ｍｉｃｒｏｆｏｒｍｅ' count 0`, `'缩微资料（ｍｉｃｒｏｆｏｒｍ' count 1` at
59201, `'/' count 0`). **S096** (HIT `.doc`, key `6dc68fd6b32ce9c8dfcebce8` — the same file as the C1
REAL pin) — the ellipsis-joined register quote occurs **0** times in the tool's OLE form, in `raw_form`
and in the sidecar, while its components occur once each in the tool's OLE form
(`文献类型及载体类型标志` @12963, `版本（初版省略）` @203, `出版项（出版地、出版者、出版年）` @223); that
sidecar is 128 416 chars with **14 486 U+FFFD** and holds none of them (`find → -1`).

## 6. Housekeeping

No tool install was needed (stock `python3`, host LibreOffice 26.8.1.1, `git`); no `pacman` transaction
was run. LibreOffice ran only with a private profile under my scratch
(`-env:UserInstallation=file://$S/prof`); `pgrep -u $USER -f "UserInstallation=file://$S"` → **none**
afterwards. Scratch removed on exit. No production file, another seat's report, the git index, jj
state, the fleet repo, a sibling lane or `shokuknow` was written or mutated; `git` was read-only
(`show`, `archive`, `status`, `diff`). No network; every source is an on-disk `.qcache` capture.

**VERDICT — attacked the OOXML path for byte-identity between base `c49ffc6` and candidate `8a7d0f1`
(8 zip captures + 5 hand-built variants: **zero** stdout/exit/stderr differences; 2583 non-zip non-OLE
captures: exit 2 and empty stdout on both, only the refusal sentence changed) and audited every lane
file matching the old "not a zip" wording (**none breaks** — consumers key on the `REFUSED` prefix),
while finding that the **committed** candidate **hangs forever** on a crafted OLE `.doc` with
`cbGrpPrl = -3` (the uncommitted worktree bytes refuse it), that C1 passes its frozen counter 4/4, and
that **C2 is short only of the round-54 lesson** (`QUOTES_IN_LESSON=0/33`, `QUARANTINE_VERDICTS=0/3`),
with the round-47 gate registry newly failing on three unregistered round-54 counters.**
