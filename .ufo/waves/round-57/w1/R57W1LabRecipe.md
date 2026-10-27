# R57W1LabRecipe — the frozen recipe + the CONSISTENT leg, probed with synthetic bytes

seat: `R57W1LabRecipe` (labrat) · wave: round-57 w1 (chousa) · date: 2026-10-27
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` · claims under study: **R57-C2** (frozen at `c2f914c53201a8f8ee4fef823b82681051d55592`) and **R57-C3** (frozen at `fd95724d56a33a150cd2638fadd2ce1f3425e6c`), read from `corpus/evidence/round57/claims.md`
frozen counter probed: `corpus/evidence/round57/c2-count.py`, sha256 `d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9`, **unchanged**
method: imported the frozen `recipe_txt` / `html_to_text` / `defined_form` as a module (`importlib.util.spec_from_file_location`) over a **byte-identical scratch copy** of the counter (`sha256sum` equal, asserted). The lane was only ever READ. No network fetch was made; only committed bytes under `corpus/captures` were read.
no predicate, target, counter, control or recipe is proposed for change here — findings against the frozen items are reported, not patched.

## 1. The two legs, as frozen (the code under test)

`c2-count.py:120-132` (recipe), `:135-144` (FLAG leg's defined form), `:212-213` (CONSISTENT test):

```python
def recipe_txt(raw, tmp):
    if raw[:5] == b"%PDF-":
        ... subprocess.run(["pdftotext", "-layout", str(p), "-"], ...)
        if txt.strip(): return txt                       # blank -> fall through
    txt = raw.decode("utf-8", "replace")
    if re.search(r"(?is)^\s*(?:<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])", txt[:4000]):
        txt = html_to_text(txt)
    return txt

def defined_form(root, raw_p, txt_p, ct):
    if raw[:8] == OLE or raw[:4] == ZIP: return ct.text_form(str(raw_p))
    return txt_p.read_bytes().decode("utf-8","replace").replace("\r\n","\n").replace("\r","\n")
    #                                                    ^ newlines normalised here only

if txt is not None and txt == recipe_txt(raw, tmp).encode("utf-8") \
        and ok[-1]["txt_sha256"] == sha(txt):
    consistent += 1
```

**Instrumentation used to decide whether a branch was taken** (no re-implementation of the predicate): `html_to_text` was applied **iff** `recipe_txt(raw) != raw.decode("utf-8","replace")`; the PDF branch was taken **iff** `pdftotext -layout` stdout was non-blank.

## 2. The four cases — recipe output class and which leg reads it how

| case | recipe output class (measured) | CONSISTENT leg reads it as | FLAG leg reads it as |
|---|---|---|---|
| **1** PDF whose `pdftotext` output is blank | **FALLBACK**: `raw.decode("utf-8","replace")` of the PDF bytes — 549 B hand-built empty-content PDF → `recipe head='%PDF-1.4\n1 0 obj\n<< /Type /Catalog…'`; corrupt `%PDF-` → `'%PDF-1.4\nnot a pdf\n%%EOF\n'` | byte-compare against the *same* recipe → **always equal** for any lane-written `.txt`; the leg certifies "the fetch tool wrote the recipe", not "the text is meaningful" | the `.txt` is binary noise; **every pinned quote is absent** → DRIFTED + `FRESHNESS-FLAG` |
| **2** HTML start just inside vs just outside 4000 chars | **inside** → `html_to_text` (tags stripped); **outside** → plain utf-8 decode, tags literal. Exact boundary measured: marker ending at char **4000 fires**, at **4001 does not** | both sides recompute the *same* recipe → a store-written `.txt` still compares equal | the `.txt` keeps literal `<` `>` when detection fails, so a quote spanning a tag boundary is **absent**; and *inversely*, a quote **containing** markup is present only when detection **fails** |
| **3** CRLF `.txt` vs the recipe output | recipe output **keeps the source CRLF** (`' \r\n QUOTE-MARKER here\n\r\n second line\n '`, 2 CR bytes) | **byte-exact**: an LF-normalised `.txt` of a CRLF source **FAILS** the comparison (`False`) | `defined_form` normalises `\r\n`→`\n`, so the **same bytes still yield the quote** (`True` in both forms) |
| **4** UTF-16 HTML page | utf-8/`replace` decode: **U+FFFD only for the BOM's 2 invalid bytes**, **65 NUL** interleaved between every ASCII byte; the frozen marker regex needs a **contiguous** ASCII marker → **`html_to_text` is NOT applied** (`html_to_text_applied=False`, `'<'` still present) | byte-compare against the same recipe → equal | the `.txt` is the mangled decode: **no ASCII quote can be found** |

### Case-by-case evidence (commands run, output as observed)

**Case 1.** `python3 probe8.py` (frozen `recipe_txt` imported):
```
  valid empty-content PDF: pdftotext rc=0 stdout=1B blank=True
     html_to_text_applied=False recipe head='%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendob'
  corrupt %PDF-: pdftotext rc=1 stdout=0B blank=True
     html_to_text_applied=False recipe head='%PDF-1.4\nnot a pdf\n%%EOF\n'
```
`pypdf` is not installed (`ModuleNotFoundError`), so the PDF was hand-built in scratch (a valid 1-page PDF with an empty `BT ET` content stream, 549 B) — `pdftotext` accepts it (rc=0) and emits 1 byte, which is blank after `.strip()`, so the frozen code falls through to the utf-8 fallback. **This branch is LIVE in the lane**: `corpus/captures/c71776bc3084de059b84569d.raw` (S133, `https://forten-sp.oss-cn-shanghai.aliyuncs.com/userfiles/FT004792/00aae3ac38844a3489ce0eefb0ed0b43.pdf`, `refetch.tsv` row id=S133 attempt=1, rc=0 http=200) is a **scanned** PDF — `/Font` count **0**, `/Image` count **4**, `/DCTDecode` 2, `Producer: RICOH MP C3504ex` — so `pdftotext` yields 2 bytes (blank) and the recipe falls back: `.txt` = 788 869 B with **157 330 U+FFFD**. C3's `form_of()` (`c3-count.py:137-148`) reads the `.txt` for every non-OLE/zip raw, so this capture enters C3 as binary noise: `heading_title` matches **0/7** reference titles (`probe7.py`). It is *not* in the frozen 47, so C2 is unaffected — but a C3 candidate chosen from such a scanned PDF can never bind.

**Case 2 and Case 2b (inversion).** `python3 probe8.py` / `probe3.py`:
```
  pad=3985: html_to_text_applied=True  marker_ends_at_char=3999 slice_holds_4000 chars tags_stripped=True
  pad=3986: html_to_text_applied=True  marker_ends_at_char=4000 slice_holds_4000 chars tags_stripped=True
  pad=3987: html_to_text_applied=False marker_ends_at_char=4001 slice_holds_4000 chars tags_stripped=False
    detected=True  quote '<p>alpha</p>'     in .txt: False
    detected=False quote '<p>alpha</p>'     in .txt: True
```
The slice is `txt[:4000]` of the **decoded** text, and the pattern is anchored `^`, so the *whole* marker must fit inside the first 4000 characters (leading whitespace is consumed by `\s*` but still counts against the window). Variants that change the outcome even well inside 4000 (`probe3.py`): an **XML prolog** before the doctype → not detected; a **UTF-8 BOM** before the doctype → not detected (the BOM is U+FEFF, not whitespace); a **leading comment** → not detected; leading `\n\t` or lowercase `<!doctype html` or bare `<html>` → detected. Real lane bytes show this is not hypothetical: `9695437cac165bb4b6145deb.raw` starts `'\ufeff<!DOCTYPE html PUBLIC "'` → **html_start_fired=False**. The inversion lines show a quote **containing** markup can only exist in the `.txt` when the HTML-start branch **fails** — the branch is a silent byte-level switch over which quotes are physically possible.

**Case 3.** `probe2.py` / `probe6.py` on the frozen functions, synthetic then real:
```
  recipe output (repr): ' \r\n QUOTE-MARKER here\n\r\n second line\n '
    stored .txt == recipe bytes (CRLF kept):   CONSISTENT=True   FLAG quote found=True
    stored .txt LF-normalised (same text):     CONSISTENT=False  FLAG quote found=True
  S097 (291 CRLF) … CONSISTENT leg: as-stored=True  after LF-normalisation=False
        FLAG leg (defined_form, real capture-text) quote 'J-STAGEが連携している外部サービス …':
        CRLF-form found=True  LF-form found=True
        verdict: as-stored -> REPRODUCED; after LF-normalisation -> DRIFTED
```
(also S125 with 185 CRLF, S099 with 75.) **The two code paths treat the same bytes differently, and the difference is per-frozen**: the predicate text in `claims.md` fixes CONSISTENT as "its `.txt` **equals** the frozen campaign recipe applied to its `.raw`" (a byte identity), while the FLAG leg's defined text form is "an OLE or zip raw: the stdout of `tools/capture-text.py`; otherwise the `.txt`" — and the counter's `defined_form()` is where the newline normalisation lives (`c2-count.py:143`). Neither was changed here.
**Real coupling, measured:** 7 of the 47 pins are the digest of a **CRLF-bearing `.txt`** (S097 291, S098 291, S099 75, S111 390, S119 206, S122 688, S125 185) — `probe7.py` §1. For those, an LF-normalising edit of the `.txt` (a git autocrlf-style checkout, a text editor, a re-save) silently flips REPRODUCED → DRIFTED while the FLAG leg keeps finding the quote: the byte leg and the quote leg disagree about the same file. `build-spans.py:86-89` reads the same `.txt` and normalises newlines for the form but digests the **raw** bytes — the same split, already baked into the pin's construction.

**Case 4.** `python3 probe8.py`:
```
  UTF-8 HTML (control)   html_to_text_applied=True  U+FFFD=  0 NUL=  0 'QUOTE-MARKER' in .txt=True  '<' still present=False
  UTF-16LE + BOM         html_to_text_applied=False U+FFFD=  2 NUL= 65 'QUOTE-MARKER' in .txt=False '<' still present=True
  UTF-16LE no BOM        html_to_text_applied=False U+FFFD=  0 NUL= 65 'QUOTE-MARKER' in .txt=False '<' still present=True
  UTF-16BE + BOM         html_to_text_applied=False U+FFFD=  2 NUL= 65 'QUOTE-MARKER' in .txt=False '<' still present=True
```
**Measured contrary to the brief's expectation**: the brief assumed `html_to_text` "still applies" to a UTF-16 page. It does not. The frozen regex `(?is)^\s*(?:<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])` needs a **contiguous** ASCII marker; UTF-16 interleaves NUL between every ASCII byte, so the marker never matches. Consequence: the `.txt` keeps the mangled decode and **no ASCII quote can be found**; only the BOM's 2 invalid bytes become U+FFFD (the NUL bytes are valid UTF-8 and survive as U+0000). Per the seat contract I report this against the frozen recipe rather than proposing a change.

## 3. Two structural properties of the CONSISTENT leg the L1 should know

**(a) It is tautological for lane-written bytes.** `tools/capture-fetch.py:146` writes `(store/<key>.txt) = recipe_txt(raw, tmp).encode("utf-8")` — the *same expression* the counter re-evaluates at `c2-count.py:212`. Measured: `c2-count.recipe_txt` vs `tools/capture-fetch.py.recipe_txt` on every stored raw → **identical = 58, different = 0**; every stored pair re-checked → **56/56 byte-equal to the frozen recipe, 0 differing**. So `CONSISTENT=46/46` proves the `.txt` was produced by the recipe and not edited afterwards; it does **not** re-derive anything about the document. It can only fail on a hand-edited or newline-normalised `.txt` (Case 3).

**(b) The `txt_sha256` conjunct is the part that is not tautological.** `c2-count.py:213` also requires `ok[-1]["txt_sha256"] == sha(txt)`. Checked against the real `refetch.tsv`: **56/56** last-successful-attempt rows match the stored `.txt` exactly. Two rows do **not** match — S113 attempt 1 and S114 attempt 1 — because attempt 2 superseded them (`raw` differs between the two successful attempts: S113 `18201d555f05` → `ba8dbc5a02a1`, S114 `fe77ace1f4a3` → `56c2f612d6b4`), so the stored `.txt` is attempt 2's. The counter reads the **last** successful attempt, so this is correct behaviour, not an anomaly — but it does mean the *lane's own two fetches of the same URL minutes apart returned different bytes*, which is the mechanism behind S113/S114's DRIFTED.

**Recipe fidelity, checked against the campaign original.** The campaign's `quote-lint.py` (`shokuknow/.ufo/waves/corpus-expansion-1/quote-lint.py:497,509,515-521`) uses the same `-layout` pdftotext, the same 4000-char HTML test, the same `html_to_text`; its whitespace class is written as the literal byte `\xc2\xa0` where the lane copy writes `\u00a0` — the same U+00A0, so identical behaviour. **The `-layout` flag is load-bearing**: on the lane's own PDF raws, `pdftotext -layout` output differs from plain `pdftotext` output for **25 of 25** PDFs, and the frozen recipe reproduces the `-layout` bytes for 25 of 26 (the 26th is the blank-scanned PDF of Case 1, which has no text layer at all).

## 4. Live state at measurement time (read-only)
- `python3 corpus/evidence/round57/c2-count.py` → `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit **0**.
- `python3 corpus/evidence/round57/c3-count.py` → `ENTRY=no … BOUND=0/7 (min 4) … SUBSTANCE=FAIL … C3=FAIL`, exit **1** (no entry, no `corpus/evidence/round57/c3/` yet — the C3 build is still ahead).
- DRIFTED forensics (`probe4.py`): for each of S083/S087/S113/S114/S121 I computed 9 candidate text forms of the **current** raw (raw bytes; utf-8 decode; utf-8 decode CRLF→LF; `html_to_text` always; `html_to_text` CRLF→LF; `html_to_text` + whitespace-collapse; `html_to_text` without tag→space; utf-8 decode + whitespace-collapse; the frozen `recipe_txt`). **None reproduces the pin for any of the five.** The DRIFTED verdicts are therefore genuine upstream byte changes, not recipe-equivalence artifacts — the DRIFTED set is honest.
- Refetch ledger: 128 rows, header as frozen. S105 has 3 failed attempts (`curl_rc=28`, 08:06:12Z / 08:30:12Z / 08:33:48Z — the first two are ≥600 s apart, so UNREACHABLE holds); S100/S103/S106 recovered on attempt 2 and are now REPRODUCED; S082–S130 each have 2 successful attempts.
- Store census at measurement: 59 `.raw`, 56 `.txt`, **17** `.txt` containing CRLF; 26 PDF raws, 3 OLE, 1 ZIP, 29 text.
- Which recipe branch each of the 47 pinned captures takes (`probe3.py` §CASE 5b): **PDF→pdftotext 20** (S086 S090 S091 S094 S102 S103 S106 S107 S108 S109 S110 S112 S116 S117 S118 S123 S127 S128 S129 S130) · **OLE/ZIP→utf-8 binary 4** (S100 S101 S115 S124) · **text→html_to_text 19** · **text→no html branch 3** (S082 markdown, S087 JSON, S122 CRLF-comment) · **no capture 1** (S105). The blank-pdftotext fallback fires **0 times** inside the frozen 47 — it is latent there and live only outside it (S133).

## 5. Where the two legs read genuinely different texts (measured)

For the 4 OLE/ZIP pinned captures the CONSISTENT-leg text and the FLAG-leg text are **different strings of the same bytes**:
```
  S100 (OLE)  CONSISTENT-leg text = recipe_txt(raw) = utf-8/replace of the binary: len=762306 U+FFFD=308430
              FLAG-leg text = capture-text.py text_form(.raw): len=842
              quotes found in the FLAG-leg text: 3/3      quotes found in the .txt (binary noise): 0/3
  S101 (OLE)  … FLAG-leg len=27012   quotes 6/6   |  .txt quotes 0/6
  S115 (ZIP)  … FLAG-leg len=19682   quotes 15/15 |  .txt quotes 0/15
  S124 (OLE)  … FLAG-leg len=13718   quotes 11/11 |  .txt quotes 0/11
```
(measured counts: S100 3/3 vs 0/3, S101 6/6 vs 0/6, S115 15/15 vs 0/15, S124 11/11 vs 0/11.) The `.txt` for these is 0 % useful text; the CONSISTENT leg nonetheless certifies it byte-for-byte, and the FLAG leg finds every quote in `capture-text.py`'s rendering instead. This is exactly the per-frozen split ("an OLE or zip raw: the stdout of `tools/capture-text.py`; otherwise the `.txt`") — reported, not patched.

## 6. Boundaries honoured

Only `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-57/w1/R57W1LabRecipe.md` was written in the lane. No git or jj mutation was run anywhere. The fleet repo `/home/vgpnk/Projects/shokunin` and `shokuknow` were read-only (`shokuknow`'s campaign tool was never executed — only its source read). No fetch was made; only committed bytes under `corpus/captures` and the committed `refetch.tsv` were read. Scratch lived only in `/fast/scratch/hyaku/chousa-r57/R57W1LabRecipe/` (`TMPDIR=$PWD`, `PYTHONDONTWRITEBYTECODE=1` exported) and **was deleted before this yield** (`rm -rf -- /fast/scratch/hyaku/chousa-r57/R57W1LabRecipe`). Tooling: none installed — the probe used only the Python 3.14.8 stdlib (`importlib`, `hashlib`, `re`, `subprocess`) plus the already-installed `pdftotext` 26.08.0 (`/usr/bin/pdftotext`); `pypdf` is absent and no substitute was installed.

VERDICT: probed the frozen R57-C2 recipe + CONSISTENT leg with synthetic bytes (blank-pdftotext PDF → utf-8 binary fallback; HTML marker boundary at exactly char 4000; CRLF `.txt` → byte leg fails while the quote leg passes; UTF-16 → `html_to_text` **not** applied, contrary to the brief) and grounded them on real lane bytes — the frozen recipe **survived** every probe with no defect found in its code path, but the CONSISTENT leg is **tautological** for lane-written bytes (56/56 `.txt` byte-equal to the same expression the fetch tool writes), 7 of 47 pins are **byte-coupled to CRLF-bearing `.txt`** files whose LF-normalisation would flip REPRODUCED→DRIFTED, the blank-PDF fallback is **live** on a scanned C3 candidate whose `.txt` is 157 330 U+FFFD of binary noise and can bind 0/7 reference titles, and the 5 DRIFTED verdicts are genuine upstream byte changes (9 candidate text forms of the current bytes reproduce no pin) — none of which is patched here.
