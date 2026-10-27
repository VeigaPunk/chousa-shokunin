# Round 55 W1 — staged-entry entailment attack

## Method and evidence

Commands run:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw > "$S/doc.txt"
cp .../.qcache/27d4865f201e99c1fed9f79b.txt "$S/report.txt"
cp .../.qcache/453d492becd9a2f4632cb8dd.txt "$S/med.txt"
```

The first command used the mandated capture-text decoder on the OLE `.raw`, not its sidecar. Character offsets below are `find()`-style offsets in those decoded/UTF-8 universal-newline text forms. I swept the form for the listed exact terms; counts are included. `S130` means lane target S124, `S131`→S125, `S133`→S113. The package observation bullets are assessed separately from their inferences.

## Bullet-by-bullet result

1. **S130 / S124, report field and protocol:** **ENTAILED with a wording qualification.** Form offset 4652: `应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。` (`是否检索灰色文献` occurs once). It expressly says the *report* should state whether grey literature was searched. `应当` is “should/shall” in guideline language, but is not the text `必须`; the English “requires” is defensible as normative rendering, but should be narrowed to “the guideline says the report should state…” rather than assert a legally binding requirement. The issuer is named by this document itself: `国家药品监督管理局` occurs once at offset 33 in the introductory text. Thus “A Chinese regulator” is supported, but “names” could misleadingly mean that the document names an issuer in a formal imprint; safest wording: “The guideline text refers to the NMPA…”
2. **S130 / S124, collection and reason:** **ENTAILED, but one phrase overstates the mandate.** Form offset 994 begins `以及其他未公开发表的文献等…`; offset 930 contains `数据资料包括…会议摘要、学术论文集以及其他未公开发表的文献等`; offset 994 contains the explicit recommendation `查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。灰色文献中可能包含阴性研究结果…若…只纳入已公开发表的文献会引入发表偏倚。` The four named examples and publication-bias rationale are present. The text says “应当注意收集” (should take care to collect), so “requires the reviewer to collect” should be narrowed to “says reviewers should take care to collect”; do not conflate this recommendation with a hard requirement. The preceding material also includes conference abstracts and proceedings, so the enumerated list is examples, not exhaustive.
3. **S131 / S125, issuer/date/structure/Cochrane:** **MIXED: issuer, date, five-part structure and Cochrane are ENTAILED; “issued” date is OVERSTATED.** Report form offset 377 says `6月18日，国家药品监督管理局发布通告，发布…`; its page metadata at offset 248 gives `2019-06-18`. The report’s own offset 817 says the guideline comprises “概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面,” then names Cochrane’s standardized process and whole-process quality control. Thus the source supports the five parts and Cochrane description. Date precision 2019-06-18 comes from page metadata, while body only says June 18; narrow to “the report is dated 2019-06-18 and says the NMPA issued the notice on 18 June.” `Cochrane` occurs once in this form.
4. **S133 / S113, portal fields and abstract:** **ENTAILED.** Form offset 4051 contains `haveAttachments=1`; offset 4178 contains `paymentAmount=10` (one match). Abstract offset 2389 says PRISMA-S is a PRISMA 2020 extension with 16 items; says the paper interprets it item-by-item and discusses cross-disciplinary generality, limitations as a reporting standard, and Chinese-database application challenges. This supports the stated abstract summary and the portal-record attachment/amount fields, not the stronger implication that the whole article itself is inaccessible without payment. The downloaded attachment name is visible at offset 2728; price metadata alone does not prove a login wall, technical failure, or that payment is required to read every form of the item.

## Requested phrase checks / corrections

- “requires” for stating whether grey literature was searched: source says `应当说明` at S124 offset 4652. Narrow to guideline “says/indicates the report should state”; avoid claiming statute-level enforceability.
- “requires” for unpublished material: source says `应当注意收集` at S124 offset 994. Narrow to “should take care to collect.” Named items are indeed conference papers, unpublished dissertations, industry reports, consultancy reports; non-exhaustive examples.
- “issued … on 18 June 2019”: report body S125 offset 377 says June 18 with no year; metadata S125 offset 248 supplies 2019-06-18. Attribute the date to page metadata, not the body.
- “consists of five parts”: supported by S125 offset 817, explicitly “五个方面.”
- “Cochrane”: present once in S125 at offset 817; wording on standardized procedures and whole-process quality control is supported.
- `paymentAmount=10`: present once in S113 at offset 4178; `haveAttachments=1` once at 4051. Correct field evidence, but does not establish “price, not login wall/technical failure” as an exhaustive access diagnosis.
- No source sweep yielded `paymentAmount=10` in S124/S125; this is specific to S113. (S113's `paymentAmount=10` count = 1.)

## Smallest safe narrowing for the entry

1. Replace “requires” in the S124 paragraph with “says the evaluation report should state” and “says reviewers should take care to collect.” Keep the four examples and publication-bias rationale, while describing them as examples.
2. Attribute `2019-06-18` to S125 page metadata; describe the body as saying “6月18日” rather than independently supplying the year.
3. In the S113 paragraph/inference, state exactly that the portal record has `haveAttachments=1` and `paymentAmount=10`; remove the categorical “price, not a login wall or a technical failure” conclusion unless separately evidenced.
4. The guideline text itself names 国家药品监督管理局, so “Chinese regulator” is supportable; distinguish this textual issuer reference from a formal issuer/imprint claim if retaining “names.”

## Axes

- **Depth:** first falsifier/narrowing: the entry treats two `应当` recommendations as unqualified requirements and overstates what portal price metadata establishes about access.
- **Operability:** source forms were opened via the specified local cache and decoder; no live fetch or campaign tool used.
- **Calibration:** positive/negative entailments and offsets are explicit; no unsupported claim that the source content is absent.

VERDICT: Attacked staged-entry entailment against S124/S125/S113 defined forms; core content is present, but normative force, date attribution, and access conclusions require the narrowings above.
