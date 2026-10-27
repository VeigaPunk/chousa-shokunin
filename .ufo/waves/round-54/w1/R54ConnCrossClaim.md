# R54ConnCrossClaim — cross-claim and cross-fleet findings

## 1. Lane quote forms

Observed command: `grep -n 'UTF-16\|utf-16\|raw decode\|\.raw' corpus/SOURCES.md corpus/knowledge/*.md` (21 hits). The only lane quote anchors explicitly described as whole-file UTF-16LE raw `.doc` decodes are:

- `corpus/SOURCES.md:110` S100: anchors 1296, 1431, 2843; `corpus/knowledge/citation-count-semantics-r37.md:3-4` identifies both raw UTF-16LE form and quoted claims.
- `corpus/SOURCES.md:111` S101: anchors 11170, 11205, 11993, 12161, 13247, 34374; `corpus/knowledge/citation-count-semantics-r37.md:5-6` identifies the same form and the claims.

Observed checks: cache keys `b539a80218080da56a75b624` (S100) and `6dc68fd6b32ce9c8dfcebce8` (S101), each with `.raw` and `.txt` sidecars. The `.txt` is not the quoted text form: for S101 the text `为便于文献的统计和期刊评价` is absent from `.txt`. Whole-file `raw.decode('utf-16le', errors='replace')` finds S101's six cited phrases at the recorded offsets (e.g. 11170 and 11205), while the C1 candidate `python3 tools/capture-text.py <S101.raw>` produced 469 lines / 47,356 bytes. In that C1 form all six phrases occur exactly once at new offsets: 11972, 12007, 12963, 12795, 14049, 25123; it has no U+FFFD or forbidden control characters. For S100 the C1 form is 842 characters / 2,290 bytes; three cited phrases occur once at offsets 16, 151, 510. Thus **re-anchor S100 and S101 row anchors and the corresponding S100/S101 source descriptions in `citation-count-semantics-r37.md` using the landed OLE form**; do not alter frozen C1/C2 predicates. The round-52 docx precedent needs no re-anchor: S115 is already described as `tools/capture-text.py` text in `corpus/SOURCES.md:125` and `corpus/knowledge/japanese-search-record-niph-form-r52.md:3-5`.

Other grep hits are already explicit sidecar/text forms, not these raw OLE decodes: S113 `chinese-prisma-s-reception-r52.md:3` (HTML `.txt`, UTF-8); S105 `cnki-citation-check-r40.md:3` (PDF `.txt`, `pdftotext -layout`); S116 `japanese-prisma-item-wording-r40.md:4,11,15` (PDF text / archive and original-failure distinction); S118/S119 `quality-control-guideline-issued-text-r48.md:3-4` (PDF/HTML `.txt`).

## 2. Other lanes' standard records/copies

Observed command: `grep -n 'openstd\|std\.samr\|iso\.org/standard\|copy hosted' */corpus/SOURCES.md`. There were no sibling hits for `openstd` or `samr` (confirmed by case-insensitive sibling grep). Sibling ISO record examples:

- `lore-shokunin/corpus/SOURCES.md:31` S023 and `:40` S032: ISO 8601-2 record, tier A; live ISO page bot-challenged/HTTP 403, lifecycle checked through Wayback captures. This is authority-page metadata, not operative standard text.
- `kasegi-shokunin/corpus/SOURCES.md:97`: ISO/IEC 29147 and 30111 standard-record URLs are listed among leads; no opened text or tier is claimed there.
- `revenger-shokunin/corpus/SOURCES.md:98`: ISO/IEC 27042 catalog lead, explicitly HTTP 403; no tiered text claim.

The search's `copy hosted` matches outside the target theme were chousa rows S100/S101/S103/S105 (e.g. `chousa-shokunin/corpus/SOURCES.md:110-115`), tier B. The staged GB/T pattern is explicit: S085 (SAMR authority record, tier A) and S086 (official openstd notice, tier A) state identity/status and that the portal serves metadata rather than text; S093 is the JMU editorial-office reproduction, tier B, expressly scoped to the reproduced text and not authority (`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:10-11,18`).

## 3. Pattern and recommendation

At the structural level, “identity at the authority, text at a copy” matches the lane's separation of evidence roles, but the linkage strength differs. GB/T uses SAMR/openstd for identity/status and a JMU copy for operative wording; the staged source description says the authority serves no text and the copy is not the authority (`SOURCES.append.md:10-11,18`). Round-53 S118/S119 also separates wording from issuance: `corpus/knowledge/quality-control-guideline-issued-text-r48.md:3-4,8-14` assigns PDF S118 the text and notice S119 the issuer/act/dates; its notice HTML has one href to the PDF (`:14`), closing the pair by address. The GB/T authority-to-JMU relation is not shown as an authority link, so the identity-to-copy join is weaker and must remain an explicit uncertainty rather than be inferred from the authority record.

S116 is a distinct fallback case, not an exact analogue: `corpus/SOURCES.md:126` records the web-archive copy and original URL; `corpus/knowledge/japanese-prisma-item-wording-r40.md:15,25` records the original failed capture and unresolved currency. Round-53 closure `corpus/lessons/round-53.md:66` refused a proposed archived-translation expansion because the same bytes were already lane S116. The archive supplies readable text where the original failed; it does not itself establish current publisher authority.

**Recommendation:** keep identity/status and operative text as separate evidence roles; for a non-authority standard copy, cite the authority only for identity/status, the copy only for textual propositions, state whether an address-level authority link was observed, and hand-check copy identity/currency rather than treating matching titles as proof. Separately re-anchor S100/S101 to the defined C1 form; retain S115 as the DOCX precedent. This improves operability and depth without changing frozen claims.

VERDICT: attacked raw OLE quote anchoring and cross-lane authority/copy analogies; S100/S101 anchors are re-locatable in the C1 form, while GB/T authority-to-copy linkage remains weaker than the address-linked S118/S119 pair.
