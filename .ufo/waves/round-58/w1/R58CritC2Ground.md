# R58CritC2Ground — C2 NEW_GROUND critique

## Counterexample

The frozen `NEW_GROUND` test treats the literal `载体类型标识` as the novelty unit. Base knowledge already expresses the same carrier-designation concept with close synonyms, including in the same S101 specification: `文献类型及载体类型标志` (“citation type and carrier-type marks”). It also already has a separate entry detailing carrier identifiers, carrier codes, and slash notation for GB/T 7714-2025. Thus an entry can pass the literal-marker gate by substituting this wording for an already-known concept; marker absence is not evidence of new semantic coverage.

## Evidence (base = `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`)

- Frozen `c2-count.py` lines 152–155 run `git grep -l '载体类型标识' BASE -- corpus/knowledge` and define `new_ground` as “literal absent from base AND literal present in entry.” No synonym, proposition, or coverage comparison occurs. This is the counter's frozen condition, not a test I ran; no C2 counter result is claimed.
- Base search command:
  `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -e '载体类型标识' -e '载体类型标志' -e '文献载体标识' -e '文献类型及载体类型标志' -e 'GB3469' -e 'GB 3469' -e '3469' b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 -- corpus/knowledge/source-type-taxonomy-r37.md corpus/knowledge/citation-count-semantics-r37.md corpus/SOURCES.md`
- Relevant base output:
  `...:corpus/knowledge/citation-count-semantics-r37.md:27:  "文献类型及载体类型标志".`
  `...:corpus/knowledge/source-type-taxonomy-r37.md:20:  `文献类型标识、文献载体标识应按照附录Ａ著录。...`
  `...:corpus/knowledge/source-type-taxonomy-r37.md:21:  ... `文献载体标识前。` ...`
  `...:corpus/knowledge/source-type-taxonomy-r37.md:24-27: carrier table rows MT, DK, CD, OL, MM; type table 图书 = Ｍ.`
  The base query returned no `载体类型标识` or `GB3469` hit in these files, but returned the synonymous concepts above. S101 is already listed in base `SOURCES.md` as a source whose reference elements include `文献类型及载体类型标志` (row S101); base `citation-count-semantics-r37.md:23-31` records that item.
- Re-opened the lane-owned S101 raw capture through the pinned defined-form tool (no network):
  `TMPDIR=/fast/scratch/hyaku/chousa-r58/R58CritC2Ground python3 -B tools/capture-text.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw | python3 -c 'import sys; t=sys.stdin.read(); qs=("1．2 参考文献类型及其标识","根据GB3469规定，以单字母方式标识","建议以下列双字母作为标识","被引用为参考文献时需在参考文献类型标识中同时标明其载体类型","[M/CD]—光盘图书(monograph on CD–ROM)；","与文献标志码(Document code)"); print("chars",len(t)); [print(repr(q),"count",t.count(q),"offset",t.find(q)) for q in qs]'`
  Output: `chars 27012`; each of the six queried strings occurs once, at offsets 315, 336, 590, 683, 838, and 11723 respectively. This is text presence in the defined capture form, not proof of the specification's current validity or truth beyond its words.

## Assessment

The synonym hit falsifies the inference that the marker-only gate demonstrates semantic novelty. It does **not**, by itself, falsify all C2 substance: the base S101 entry mentions the combined field but does not list these older GB3469 provisions, while the existing S123 entry concerns the 2025 standard. The reopened S101 form contains more discriminating candidate coverage—GB3469 single-letter and double-letter passage, carrier notation/examples, and a separate document-code mention—which is not established as already covered by the cited base passages. Whether the submitted entry actually adds those propositions remains untested here; it was not present at the path when opened. Do not treat the literal-string predicate as a substitute for that comparison.

**Impacted axis:** depth (NEW_GROUND component only; not a whole-C2 verdict).

**Smallest safe correction:** Keep the frozen counter unchanged. For judging novelty, compare the entry's claimed propositions against base coverage using discriminating content (legacy GB3469 alphabet, the `[type/carrier]` combination/examples, and distinction from document code), not a new spelling of “carrier-type mark.” Retain source-specific scope and separate textual presence from entailment/truth.

VERDICT: The attack falsifies the frozen literal-marker test as a semantic novelty demonstration; the broader S101 coverage claim is not falsified by this counterexample and remains inconclusive pending comparison of the actual entry.