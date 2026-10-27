# R56ReviewProvince — C2 province check: where the grey-literature search requirement lives

seat R56ReviewProvince · chousa round 56 W1 · 2026-10-27 · read-only item.
Method: read `chousa-shokunin/PROVINCE.md` and all 20 sibling `*-shokunin/PROVINCE.md` files
(glob `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` → 21 files incl. chousa); two
sibling vocabulary sweeps; line-pinning greps (results pasted inline). No scratch writes, no
tool installs, no network, no live fetch; only lane write is this file. Commands are grep-tool
invocations (pattern → path → observed output); no shell grep substitutes.

## Q1 — Is the question chousa's or a sibling's?

The question decomposes into two parts, and the split decides it.

**(a) Locating the requirement in the document — chousa's.** `chousa-shokunin/PROVINCE.md:5-8`
(Owns): "question framing; **source hierarchy (primary / secondary / aggregator / unsourced)**;
citation chaining and hop resolution; **claim-vs-source verification**; **search-strategy
taxonomy**; the external-target approval table …; this lane's own corpus and gates". Asking
*where* a national standard states a grey-literature search duty — which clause, which
information-source list position, which table row — and binding that to a byte-exact quote,
offset and span is exactly search-strategy taxonomy + claim-vs-source verification applied to
this lane's own corpus. Line :3 (Domain) is "deep-research method (調査) — the reusable craft
of source research". Lane precedent is direct: `corpus/README.md:1204` — "A Chinese regulator's
guideline puts the grey-literature question in the report itself … (`S124`), with a bias
rationale — **the lane held 灰色文献 only as a source category before**" (round-55 entry
`grey-literature-and-chinese-search-record-r40.md`, README.md:1195); round 53 already scanned
the issued quality-control guideline's text form for 灰色文献 (README.md:1146: "0 occurrences
of 检索日期 and 灰色文献"). The C2 theme (`corpus/evidence/round56/claims.md:130-133`) is the
same method on a new document set; the staged rows exist in the working tree
(`corpus/evidence/round56/spans.tsv:3` — S127 offset 24544, "（9）灰色文献：未公开发表研究信息…")
and the entry file is present (`corpus/knowledge/grey-literature-field-china-r42.md`, glob hit).

**(b) The documents' pharmacological/regulatory substance — nobody's, therefore adjacent.**
Sweep A: pattern `药|临床|循证|灰色|药品`, case-sensitive, over all 21 PROVINCE.md →
**No matches found**. Sweep B: pattern `pharmac|[Rr]egulator(y|\b)|\bdrug\b|\bDrug\b` →
**No matches found**. No sibling province claims pharmacology, drug regulation, or
clinical evidence-based medicine. (A looser case-insensitive `grade` sweep hits only
LLM-benchmark graders/graded receipts — kengaku PROVINCE.md:19,108; kaidoku:192; kama:77,153 —
not clinical evidence grading.) So the substantive content of 药品临床综合评价 documents has
no owner; per chousa PROVINCE.md:17 "**Out of province → report, never absorb**", the entry
reports what the documents say as captured source content and absorbs none of it as a chousa
claim. Fleet convergence confirms (a): 11 siblings explicitly route research method to chousa —

| sibling | line | text (abridged) |
|---|---|---|
| kengaku | PROVINCE.md:137 | "**chousa** | research method — … the question → source-hierarchy → citation-chain → claim-vs-source method stays chousa's … this lane holds neither method nor duplicates it" |
| souji | :82-83 | "chousa-shokunin owns the research method and source hierarchy; souji's `corpus/SOURCES.md` applies it and does not restate it" |
| kotodama | :19 | Refuses "general source-research method (chousa)" |
| kumitate | :29 | "Research method → chousa" |
| kama | :168-169 | "The generic pinning *method* … is chousa's ground; the specific re-pin of the two held docs rows is kama's" |
| kotoba | :57 | sibling-census row: "chousa owns the research method, its tools and gates (PROVINCE.md:3-8 at the head)" |
| audio | :53 | "research method (chousa)" |
| lore | :27 | "chousa — research method, not lore canon" |
| kake | :36-37 | "`chousa` owns research method and source hierarchy" |
| kasegi | :47 | "chousa — research method and source hierarchy" |
| kagi | :67 | "chousa owns the research method (`SOURCES.md` restates neither method nor admission bar)" |

The other nine (tsukuroi, tameshi, mori, mado, game-dev-2d, game-dev-3d, revenger, tabi,
kaidoku) name no chousa claim; their domains (OS, verification method, observability, desktop,
games, RE, browser) are disjoint from both parts of the question.

## Q2 — What the entry must report as adjacent, not absorb

Three content classes the C2 documents carry. Each is quotable evidence (report), never
adjudicated doctrine (absorb):

1. **Clinical/pharmacological substance** — what the workflow standard's evaluation dimensions,
   data sources and steps mean medically. The entry may state, quote-bound, *that the document
   lists* ten information sources (staged S127 row, SOURCES.md:137: "the draft lists
   灰色文献：未公开发表研究信息 as the ninth of ten information sources, one grade line closing
   the whole list") — the list *position and wording* is search-method ground; the *medical
   adequacy* of those sources is out of province, unowned (Sweep A/B), so it is reported, never
   endorsed or refuted.
2. **Evidence-grading content** — the standard "adopts the 中国循证医学中心 evidence-quality
   grading and Oxford recommendation strengths" (staged S127 row, SOURCES.md:137; staged S129
   rows, SOURCES.md:139 and round56/quotes.tsv:19-21: "灰色文献 未公开发表的研究信息 … Ⅰ级 A"
   and "采用中国循证医学中心的证据分级体系进行证据分级评价"). The frozen predicate requires the
   string 中国循证医学中心 to be *held* in the entry (claims.md:107-109 "at BASE_REV no
   `corpus/knowledge` file held `中国循证医学中心`, and the entry holds it"). Province-wise:
   holding it as *document attribution* (who grades, per the document, at a recorded offset) is
   source metadata and in; asserting the grading system's validity, or grading anything with it,
   is out. No sibling owns clinical evidence grading (sweeps), so there is no route — the
   out-of-province clause (:17) governs.
3. **Regulatory status/obligation** — whether a group standard (T/CLPA, staged quotes.tsv:6
   "T/CLPA XXXX—2025"), an NHC guideline (S130, SOURCES.md:140: tier B "never for the current
   management guideline") or the issued QC guideline creates compliance duties. Issuance facts
   (who, when, what carrier, tier A/B rationale) are provenance the hierarchy needs and are
   chousa's; the *meaning of compliance* is out.

**Arrow caveat.** chousa PROVINCE.md:10-11 refuses "model-quality or evaluation claims
(→ kengaku)". That arrow does *not* route clinical drug-evaluation content to kengaku:
kengaku PROVINCE.md:3 scopes its Domain to "LLM/model research & evaluation" and :6 refuses
"anything outside this domain". Clinical evaluation is outside kengaku's domain, so it is
simply unowned — the entry must not read :11 as a licence to hand off, nor as ownership.

**Also in province (must not be refused away):** document-class placement of the four bound
candidates (ttbz standard text = primary standard wording; 编制说明 = drafter's note, tier B,
SOURCES.md:138 "never for the grading system's content"; journal-hosted copy = secondary
carrier; NHC guideline = issuer's text); the BY DOCUMENT renumber S168→S127, S156=S169→S128,
S155→S129, S157→S130 with held S118 (claims.md:133-136); and the same-theme merge of staged
r44 (`grey-literature-national-route-r44.md`) into the r42 entry by document
(claims.md:131-132) — citation-chaining/hop-resolution work. No external-target approval
arises: every source is an on-disk capture (claims.md:10-12, L0 `8d77e6c1` open), consistent
with the :13 refusal of unapproved live-target research.

## Residual risk / verification gaps

- Sweeps read PROVINCE.md working-tree tips only, not pinned commits and not sibling
  `corpus/`/`SKILL.md`: a sibling corpus entry touching 循证/pharmacology without a province
  claim would not be caught. Ownership text is the province declarations, but contested scope
  should go to the integrator, not be absorbed either way.
- Sibling declarations drift (precedent: tsukuroi's "re-read the cited declaration before a
  later handoff", tsukuroi PROVINCE.md:53-55); the kengaku/souji/etc. pins are current-tree,
  so a later sibling commit could move the boundary.
- The staged round-56 rows/entry exist in the working tree; whether they land and pass the
  frozen counter is C2's counter's job, not judged here.

VERDICT: attacked the C2 province boundary — locating the grey-literature search requirement in
the standard is chousa's (PROVINCE.md:5-8; sibling routing concurs); clinical substance,
evidence-grading (中国循证医学中心/Ⅰ级 A) and compliance meaning are unowned-adjacent (zero
drug/regulatory vocabulary hits in sibling provinces), report quote-bound and never absorb.
