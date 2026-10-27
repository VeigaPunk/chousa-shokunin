# R55CritEntailInf — staged-entry entailment attack

Axes: depth/sourcing, calibration, operability. Frozen predicates are not challenged or changed; this review tests staged inference/unknown wording against lane evidence.

## Findings

1. **“Q15 is answered, and the answer is a regulator, not a journal” — narrow.** The primary decoded OLE form supports that the cited document is a NMPA guideline, but does not resolve broader Q15 absent its exact question framing. Defined form command:

```text
python3 tools/capture-text.py .../.qcache/bdff491a75c6abeda1d9c01d.raw
length 13718; “是否检索灰色文献” count=1 offset=4678
```

At offset 4678 the sentence says: “应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。” (one line; exact form). Staged entry Observation identifies S130 as 国家药品监督管理局 guideline; lane frozen C2 identifies document and URL. Suggested: “This document answers the narrow question whether this NMPA guideline makes grey-literature searching a reported field: yes; its issuer is a regulator, not a journal.”

2. **“Three literatures now require the same non-database disclosure, none of them PRISMA's” — cut.** This overstates both commonality and requirement. S097 is not a Japanese industry form: `corpus/SOURCES.md` line 107 identifies it as a JST/J-STAGE publisher page about DOI and citation links; `corpus/knowledge/aggregator-vs-source-r36.md` lines 5, 42 likewise concern citation links. Therefore the staged attribution “Japanese industry form asks whether a hand search was done (S097)” is a wrong-document identity. NIPH is S115, not S114: line 125 identifies S115 as the NIPH cost-effectiveness reporting template; its bound lane entry is `japanese-search-record-niph-form-r52.md`, source S115. S114 is instead the Chinese PRISMA 2020 checklist (SOURCES.md line 124). The claim of three literatures, including a Japanese leg sourced to S097, does not survive. The “none of them is PRISMA's” clause is also unsound as an inference: NIPH S115 is a reporting template, not by itself a literature or national practice; this review did not inspect all PRISMA requirements. The staged text itself acknowledges only the selected PRISMA items elsewhere, not exhaustive absence.

3. **“PRISMA 2020's items do not carry [the non-database part]” — cut / replace with scoped contrast.** Lane S114 item 6 explicitly includes websites, organisations, reference lists, and “其他 检索或咨询 途径” among information sources; `corpus/knowledge/chinese-prisma-s-reception-r52.md` lines 13, 20–21 quotes it and distinguishes item 7 strategy coverage. S116 is Japanese PRISMA checklist. These are direct counterexamples to saying PRISMA carries no non-database source disclosure. Safer: “The NMPA field explicitly asks whether grey literature was searched; that is not the same field as PRISMA item 6's source enumeration, and this evidence does not establish that PRISMA has no grey-literature requirement.”

4. **“The blocker is a price” — narrow to portal-record evidence; underlying item remains unread.** S113 is the lane's held MedSci portal row, not S133 (staged namespace). `corpus/SOURCES.md` line 123 scopes S113 to the portal record/abstract, not item text; `corpus/knowledge/chinese-prisma-s-reception-r52.md` lines 4, 8 document S113/S114. The lane evidence available here establishes an attachment/payment field on the portal record, not that price is the sole blocker (e.g. access, attachment availability, or authorization were not tested in this attack). The staged observation says paymentAmount=10; lane C2 freezes S113-only citation. Suggested: “The portal record lists an attachment and paymentAmount=10; the item-by-item text remains unread, and this round did not establish that price is the sole access blocker.”

5. **Held regulator-required grey-literature field? Yes, at least one held entry.** `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n '灰色文献' -- corpus/knowledge` returns `chinese-search-record-r39.md` lines 14–15 and 24: S109 asks for 灰色文献 retrieval/recording in an animal-review protocol table; line 24 contrasts that requirement with S110 practice. This is a Chinese journal recommendation, not a regulator requirement. `quality-control-guideline-issued-text-r48.md` lines 16 and 31 explicitly reports zero 灰色文献 in S118's text form. Thus among evidence opened by this sweep, the stated regulator-required grey-literature field is the staged NMPA material, not a pre-existing lane entry; the pre-existing occurrence must not be misdescribed as regulator-required.

## Evidence distinction

Staged identifiers S130/S131/S133 are not lane identifiers. Frozen round-55 C2 specifies lane S124/S125/S126 for the NMPA documents and lane S113 only for MedSci. Lane S097 and S114 are different documents from the staged entry's asserted Japanese legs; S115 is the NIPH form. Commands and file lines above were observed locally; no network/source fetch was performed.

VERDICT: The staged inference is not entailed as written: Japanese S097 is a wrong-document identity, PRISMA non-database exclusion is contradicted by S114, and the price claim exceeds the held S113 portal-record evidence; narrow the NMPA claim to its specific reported field and issuer.