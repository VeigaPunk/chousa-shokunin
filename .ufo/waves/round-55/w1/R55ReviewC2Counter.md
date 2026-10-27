# R55 C2 counter review — same-sentence audit

## Evidence / execution

Commands run (counter command intentionally returns 1 for the current unpopulated lane):

```text
python3 -c '<import counter; load BASE capture-text; evaluate form_text for GCP, CNPHARM, NMPA_EN, MEDSCI>'
BASE_CAPTURE_TOOL_SHA256 2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc key=bdff491a75c6abeda1d9c01d raw_defined=True raw_form=True txt_form=False
http://m.cnpharm.com/201906/18/c280684.html key=27d4865f201e99c1fed9f79b raw_defined=False raw_form=False txt_form=True
https://english.nmpa.gov.cn/2019-07/18/c_388252.htm key=d663d66e2d39f868d84b1781 raw_defined=False raw_form=False txt_form=True
https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 key=453d492becd9a2f4632cb8dd raw_defined=False raw_form=False txt_form=True
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round55/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
ENTRIES=0/1 (min 1) REFUSED_ENTRIES=0
HELD_CITED=- HELD_BAD=0
BOUND=0/3 (min 2) REFUSED=0
BOUND_IDS= GUIDELINE_BOUND=no
REF_ID_UNBOUND=0
NEW_GROUND=0/0
QUOTE_ROWS=0 ON_BOUND=0/0
SPAN_IDS=0/0 (min 3 each)
QUOTES_IN_SPAN=0/0
QUOTES_IN_ENTRY=0/0
QUOTES_IN_LESSON=0/0
QUOTE_SHORT=0/0
SPAN_CONTEXT=0/0
CAPTURE_BOUND=0/0
SUBSTANCE=FAIL
ANCHOR_BOUND=0/0
INFERENCE_GROUNDED=0/0
QUARANTINE_VERDICTS=0/1 (S125)
QUARANTINE_BLOCKED_ADOPTED=0
C2=FAIL (exit 1)
```

BASE byte provenance independently checked: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show dba605deb5cd5ed4874e0e3c39ba24737409cd80:tools/capture-text.py` returned 0, 20,203 bytes, SHA-256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`; this matches the frozen expected digest and the tool used by `_base_tool` (c2-count.py:92–107). No LSP device is mounted; literal source review used instead.

## Predicate/docstring/enforcement, clause by clause

The frozen predicate appears at claims.md C2; its corresponding counter docstring at c2-count.py:4–34 reproduces it verbatim in substance (same sentence; the claims copy is the source of authority). The enforcing behavior is:

- Entry exists / “by document”: c2-count.py:67–69 and 190–192 define the single required entry and load it; 323–325 requires exactly the configured entry set to exist. This tests the designated entry path, not a general entry discovery census.
- Three documents bound/refused, guideline required: constants at 70–85; row matching/eligibility and refusal checks at 194–214; totals and required GCP bound at 306–307, 323–325. It matches one 11-cell Registry row with URL in first source cell (`r[1]`), requires non-base ID, `mined`, opened date, `used-by` equal to configured citing entries, and `source:` line in each citing entry (202–210). REFUSED requires no row, no source URL in loaded entry text, and `refused-doc` URL in lesson (211–214). Exact total catches documents that are neither validly bound nor refused.
- Held S113 and entry S-token restriction: 218–230; held row must be base ID/URL and each citing entry must have exact S113 source line and be in `used-by`; unbound occurrence counting feeds final gate at 308, 324. `ID_RE` is `S` plus at least three digits (86).
- Novel term: BASE grep of `corpus/knowledge` and presence in entry at 232–236, gated at 325.
- Span/quote rules: manifest iteration at 240–265 counts bound identity, quote appearances in span/entry/lesson, limits, context, exact form slice; per-ID minimum at 265; final gate 325–327. Exact source form logic is 139–164: OLE/zip `.raw` recognized by magic bytes; only matching raw digest is passed to `ct.text_form`; sidecar ignored on the raw-defined branch; otherwise matching `.txt` digest read UTF-8 with universal newline translation. Quote-substance executable gate at 267–269. Anchor char offsets at 271–275. Inference tool execution at 277–285.
- Register sweep/verdict gate: theme URLs from DOCS and MEDSCI alias at 287–288; only rows containing `chousa`, round token, S-token, and theme URL are admitted at 289–296; lesson verdicts parsed at 297–300; blocked adopted-document verdict check at 301–302; final gate requires verdict count equal register IDs and no blocked verdict (327).

Separability: literal search of the entire counter found **zero** `build-spans.py` occurrences and no builder import or execution. It does contain `capture-text.py` only in explanatory strings and `_base_tool`’s explicit `git show BASE_REV:tools/capture-text.py` import path (lines 92–107); measured BASE bytes match the frozen hash above. The counter also runs other specified checks (`quote-substance-check.py`, `inference-ground.py`) and git show/grep; it does not invoke the C1 builder.

## Findings / gaps

- **No predicate mismatch found** between frozen C2 and the counter docstring. Primary potentially consequential scope detail: “exactly the existing entries citing it” is computed over the sole configured `ENTRIES` set (lines 67–69, 201), consistent with this one-entry frozen target; it is not a repository-wide search.
- The requested four-capture probe confirms GCP’s `.raw` digest returns a defined form and its `.txt` digest returns `None`; the other three URLs are non-OLE and resolve from `.txt` only. This directly tests the `.txt`-digest rejection for the gcpunion row.
- Register sweep result observed: `QUARANTINE_VERDICTS=0/1 (S125)`. The denominator/sweep finds exactly one theme `chousa` row, S125; no lesson verdict line exists in the current lane state, so the predicate is not yet met. It does **not** print the literal standalone count `1`; it prints it as denominator `(S125)` while printing observed verdict count `0`. If “sweep prints how many: 1” is intended to require an explicit count of register rows, current output does not provide that standalone count, although its denominator conveys it. Current counter run overall fails because the entry/manifest/lesson are not yet present; that is not a counter-specific regression.

VERDICT: C2 counter’s frozen predicate and form-source separation are implemented as specified; four capture forms and base-tool provenance verified; the live register sweep identifies one row (S125) but has zero verdicts in the current lane state.
