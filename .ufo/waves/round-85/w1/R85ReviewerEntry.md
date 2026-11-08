# R85ReviewerEntry — C2 K3 (warrant) attack on provenance-recording-r85.md @ 64803d33362f50cf9094e91fc3a4a07216c563ca

Seat: R85ReviewerEntry. Lane: chousa round 85. Revision under attack: 64803d33362f50cf9094e91fc3a4a07216c563ca.
Frozen predicate: `corpus/evidence/round85/claims.md` lines 106–114 (K3 warrant).
Entry: `corpus/knowledge/provenance-recording-r85.md` (sha256 c93f4b1ad8a2a1962e1205c9fa5c6f8e48c098563149994252ec5a95f563eadc; byte-identical at 02df67db and 64803d33 — verified `git show` diff empty).
Captures (committed bytes, sha256 in head): S215 `6e48bcc4a04d13b7b3ebb68e.txt` 8c9aeabb466f…, S026 `67983a3dbbd1d690aa648744.txt` 27ee75739788…, S024 `11d6cc56bb24adfc61eea2b4.txt` 97fe1a6adbd2….

K3 as frozen: "a non-author reviewer shows, for any decision-table row, (a) that its Do or Never states something its cited quotes do not state or entail, or (b) a sentence of the same cited source (located in the committed capture, quoted by line) that contradicts the row's Do or Never. One such row falsifies C2."

Standard applied per seat spec: strict but exact. A row merely narrower than the source is not a firing. Each row checked (a) Do follows from quotes, (b) Never is negated from what quotes require within their hedges, (c) full paragraph + section read for contradicting sentences. Inference/Limits judged as residuals only.

---

## Row 1 — "Naming what a resource derives from" — Warrant Q1, Q3 (S215)

Row text (entry lines 34): Do = "form the provenance chain with the derivation property where the chain's entities are set"; Never = "deliver a resource that passes for a primary when it derives from an identified earlier entity".

What the quotes say:
- Q1 (S215 line 779, §3.1 Starting Point Terms): "Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property." Modal word is *can be formed* — capability, not obligation.
- Q3 (S215 line 781): "then we can say that the bar chart prov:wasDerivedFrom the dataset." Introduced by line 780 "if the Activity that created the bar chart is not known or is not of interest" — the sentence is conditional on the Activity being unknown/uninteresting. It licenses a representation; it does not command it. The Do ("form the… chain…") states what the property is for. The entry's `## What this entry governs` (L16) correctly scopes to "keep only what each quote states about naming a source and its dates" — so the Do is a naming recommendation, and the quote does state the naming mechanism. (a) passes: the Do describes the stateable relation, not a MUST; no source sentence contradicts this narrowing.
- Never: word "primary" does not occur in Q1/Q3, nor in the §3.1 paragraph (lines 779–783 read in full; surrounding §3.1 lines 744–799 likewise contain no "primary"). The only primary-source apparatus in S215 is `prov:hadPrimarySource`, a *subproperty* of `prov:wasDerivedFrom` (§3.2 line 991: "Three subproperties of prov:wasDerivedFrom are also provided… prov:hadPrimarySource cites a preceding Entity produced by some agent with direct experience…"; full definition L3926–3930: "A primary source… is… something produced by some agent with direct experience and knowledge about the topic… As such, it is important for secondary sources to reference those primary sources from which they were derived"; guidance L2330: "The more specific subproperties of prov:wasDerivedFrom … should be used when applicable"). That passage *supports* the Never's direction (a primary relationship is a derivation that secondary sources reference) but it also contradicts the Never's letter: the source's rule is "should be used when applicable" (L2330), not a blanket prohibition on treating any derived resource as "primary". More exactly, the Never condemns "deliver a resource that passes for a primary when it derives from an identified earlier entity" — but S215 itself derives the concept of primary-ness *from* derivation (L3930: "A primary source relation is a particular case of derivation…"). So the Never as worded describes something the source says is legitimate, provided the direct-experience condition holds (L3926). The quotes cited (Q1, Q3) require nothing about primaries at all.

Finding: Row 1 Never introduces "primary" without quote support. The cited quotes (Q1/Q3, S215 §3.1) contain no primary-source requirement or prohibition; the word must be imported from an uncited subproperty definition (§4, L3926–3930) that, read at L3930, makes "primary" a *special case* of derivation, contradicting the Never's blanket phrasing. This is K3(a): the Never states something its cited quotes do not state or entail. The Do half holds; the Never half does not. The neighboring prose "where the chain's entities are set" also adds a precondition ("entities are set") the quotes don't state — but that is mere narrowing and not counted as a firing; the "primary" import is the firing-grade defect.

Severity: This row alone falsifies C2 under K3 as frozen ("One such row falsifies C2"). The defect is the word "primary" in the Never (entry L34), unsupported by Q1/Q3.

## Row 2 — "Recording a derivation's direction" — Warrant Q2 (S215)

Q2 (S215 line 780): "A derivation is a transformation of one entity into another." Do: "state the transformation from one entity into another" — near-verbatim restatement; follows. Never: "call two unrelated entities a derivation" — the quote defines derivation as transformation; unrelated entities by definition are not in a transformation relation, so the Never is the negation within the quote's hedge. Full §3.1 paragraph (lines 779–783) and §3.2 derivation-subproperty paragraph (lines 991–997: derivation subtypes wereQuotedFrom / wasRevisionOf / hadPrimarySource) contain no sentence contradicting either half; the subtypes refine, not contradict, the direction claim. No K3 basis. Held.

## Row 3 — "Recording the bounds of an entity's existence" — Warrant Q4 (S215)

Q4 (S215 line 1021, §3.2 Expanded Terms, fourth category): "The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence." Do: "state the generation moment and the invalidation moment that bound it" — restatement of Q4's "bound the starting and ending moments"; the quote's "can be used" is capability language and the Do, read as the lane's recording instruction, does not upgrade it to a source MUST in a way contradicted by the source (the source never says entities need no bounds). Never: "describe an entity as atemporal, with no generation or invalidation moment" — the quote says these properties *can be used* to bound; it does not say entities *must* have both moments. An entity described without those moments is not thereby contradicted by Q4, since "can" is permissive. Strictly, the Never overshoots Q4: Q4 permits bounding, it does not require both bounds for every entity. However, the surrounding paragraph (L1019–1023 read in full) hedges in the same direction: "an Entity *may* be bound by points in time" (L1020); "The Activities that led to… *can* be provided" (L1021). The source's modality is uniformly permissive, and the row's Never is a genuine negation of the Do rather than a claim the source requires both bounds. Under the seat's strict-but-exact standard, this is a narrowing-to-instruction case: does the Do "state" something the quote does not state? The Do says "state the generation moment and the invalidation moment" — the quote supports stating both as the bounding device. The Never ("describe… as atemporal") is the natural opposite of using the bounding properties. No sentence in §3.2 (L1019–1023) or §3.1 contradicts either half; in particular nothing exempts entities from temporal bounds. No K3(a) or K3(b) located. Held — but see residual: the row's imperative ("state the generation moment and the invalidation moment") reads more categorical than Q4's "can be used" / L1020 "may be bound"; noted as wording stronger than the hedge, not a K3 firing because a row narrower than the source is excluded, and the negation stays within the Do.

## Row 4 — "Recording a resource's provenance" — Warrant Q5 (S026)

Q5 (S026 line 453, "Interpretation of R1.2" paragraph, read in full L451–454): "Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions..." Do lists exactly Q5's first four facets verbatim. Follows. Never: "ship data with no record of how it came to be" — S026's following sentence (L453, same line): "Provenance information helps people and machines assess whether a resource meets their criteria for their intended reuse…" Nothing in the paragraph (L451–454) or the FIP addendum (L458: "Principle R1.2 is addressed through the Provenance Model") contradicts the Never; absence of any provenance record is the opposite of "detailed provenance includes facets…". The one-sided modality concern (Q5 says "includes facets such as…" — illustrative, not exhaustive) cuts toward the row being narrower, which the seat standard excludes from K3. Held.

## Row 5 — "Recording the source behind a resource" — Warrant Q6 (S026)

Q6 (S026 line 453, same sentence): "using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit". Do: "state the starting data or source resource, and who owns the data and should be given credit" — subset of Q6; the Do drops Q6's "using what funding/resources" facet (narrowing, not contradiction). Never: "cite a tool by name alone, without version or step". Strict check: Q6 mentions neither tools, versions, nor steps. The full paragraph (L451–454) and FIP note (L458–463, read to L473) contain no sentence about tools, versions, or steps — the word "version" and "tool" do not occur in the S026 capture outside the facet list; grep for version|tool|filter|cleansing returns only L453 itself (facets "filters or cleansing processes" and "funding/resources"). The paragraph's closing purpose clause ("assess whether a resource meets their criteria for their intended reuse") does not entail a tool-version prohibition. A Never about citing tools without version/step is not the negation of anything Q6 requires within its hedges; it is an imported complementary practice (the lane's citation hygiene) dressed as a source-derived Never.

Finding: Row 5 Never, words "tool", "version", "step" (entry L38), have no support in Q6 or anywhere in S026's captured page. K3(a): the Never states something its cited quote does not state or entail. This is the cleanest K3(a) in the entry — the Never's nouns do not appear in the source at all.

Severity: Row 5 alone would falsify C2 under K3 as frozen. Combined with Row 1, C2 is falsified on two independent rows.

## Row 6 — "Recording when content was last reviewed" — Warrant Q7 (S024)

Q7 (S024 line 211, full page 313 lines read): "Date on which the content on this web page was last reviewed for accuracy and/or completeness." Do: "state the date the content was last reviewed for accuracy and completeness" — faithful restatement (drops "and/or" hedge, immaterial). Never: "pass a record off as reviewed when only its modification date is known". The S024 capture is the Schema.org property page for `lastReviewed` alone; it contains no mention of modification dates, `dateModified`, or any prohibition on conflating them (grep for modified|dateModified returns no informative line; the page cross-references only "Use on these types: WebPage", L241–249, and version footer L292–300). The Never's "modification date" concept is imported from outside S024 (it belongs to DCMI/DC Terms or Schema.org `dateModified`, neither cited here). The question for K3(a) is whether Q7 entails the Never: Q7 defines a review date as a distinct fact ("last reviewed for accuracy and/or completeness") — conflating it with a modification date would misstate the definition, so the Never is arguably the negation of using the defined property wrongly. But the subject of the Never is a *lane record*, not a Schema.org `lastReviewed` marking; the sentence prohibits passing off a record whose only date is a modification date, a practice Q7 neither describes nor forbids. Strict-but-exact: this is the weakest of the three outside-quote candidates. It is not a direct contradiction — no S024 sentence contradicts it — and distinguishing "reviewed" from "modified" is entailed by the definition itself (Q7's content). I do not count Row 6 as a K3 firing; the Never survives as a definitional negation (a review date is not a modification date). It is, however, unsupported in the stronger sense that "modification date" is not an S024 term; recorded as a residual overreach rather than a kill.

With the full-page check: S024 is uniformly definitional (L9 title, L198 canonical URL, L211 definition, L225–235 type Date, L241–249 used on WebPage). No sentence contradicts the row. Held (weakly; see residuals).

---
## S215 vs S020 same-document check (by content)

Claim under test: S215's page is the same document as S020's canonical URL (the alternate URL carries the material).

Evidence:
- S215 capture header (L34–36): "PROV-O: The PROV Ontology / W3C Recommendation 30 April 2013 / This version: http://www.w3.org/TR/2013/REC-prov-o-20130430/ Latest published version: http://www.w3.org/TR/prov-o/…". The S215 capture was itself fetched from the alternate URL (refetch.tsv L177: S215 https://www.w3.org/TR/prov-o/ → 6e48bcc4…, http 200, txt_sha256 8c9aeabb466f… matching the capture sha). Its content declares its own canonical version URL to be the REC-prov-o-20130430 URL — i.e., the alternate URL serves the identical Recommendation document as S020's canonical URL.
- The refetch history corroborates the identity: the same capture key 6e48bcc4… is bound to rows S020/S215/S033 (refetch.tsv L175–177, L179), with S020's canonical URL attempts returning 403 (L167–169) and the alternate URL succeeding (L177 http 200). The_registry rows confirm: S020, S033, S215 all carry the same title "PROV-O: The PROV Ontology, W3C Recommendation 2013-04-30" and the same anchor (§3.1 wasDerivedFrom; §3.2 entity-lifetime paragraph) (SOURCES.md L30, L43, L228).
- Content match: the S215 capture's §3.1 and §3.2 text quoted above is byte-present in the committed capture and is precisely S020/S033's anchor material.

Conclusion: S215's page IS the same document as S020's canonical URL (the W3C Recommendation REC-prov-o-20130430), retrieved via its "Latest published version" alternate URL. The alternate-URL framing in the amendment is accurate; this check does not fire. (Note: K3 only concerns the entry's rows; this identity check was requested and passes. The K4 ground question — whether a base entry cites S215/S026/S024 — is outside this seat's K3 assignment and was not invoked; the rows above are attacked solely on warrant.)

---

## Inference and Limits (residuals, not K3 rows)

Inference (L41–45): explicitly labelled "lane's, not stated by the sources"; maps "resource" to SOURCES.md rows / knowledge entries, motivates `verified-at:` + `recheck:` from generated/invalidated times, and calls R1.2 facets "the lane's Gate record itself". The disclaimer is genuine; the mappings (generatedAtTime → verified-at) conflate entity-generation time with source-verification time, a conflation the sources do not make. Because it is labelled inference, this is not a K3 firing, but it is overreach in the residual sense: the prose "motivate the verified-at + recheck pair" softens a category gap (existence bounds ≠ verification policy) that the registry scope ("not a recheck or verification policy", S215/S020/S033) explicitly disclaims. Residual concern: a reader skimming `## Inference` could take the motivating link as source-backed. The label mitigates; it does not eliminate the slippage.

Limits (L47–53):
- "PROV-O is a description of provenance relations, not a rule for when to re-verify a source" — accurate and consistent with the registry scope; no overreach.
- "FAIR R1.2 is a foundation interpretation, not a W3C recommendation" — accurate (S026 is a GO FAIR Foundation page, L117 title, not a W3C Recommendation; PROV-O by contrast is a W3C Recommendation, S215 L35). The entry correctly distinguishes the two authorities. No overreach.
- "Schema.org's lastReviewed is a publication-date-adjacent property, not a verification-policy date… The row takes only its definition" — accurate; consistent with the Row 6 reading above. The phrase "publication-date-adjacent" is lane characterization but harmless.

Residuals summary: Inference's verified-at motivation is the only overreach of note; Limits are sound. Neither is a K3 row, neither fires C2, both reported as requested.

---

## K3 adjudication

- Row 1 Never ("passes for a primary", L34): FIRES K3(a). Word "primary" unsupported by Q1/Q3; the source's primary-source apparatus (S215 L3926–3930, L2330) makes primary a case of derivation, contradicting the Never's blanket phrasing and requiring a cite the row lacks.
- Row 2: held.
- Row 3: held (modality noted as residual wording strength, not a K3 firing).
- Row 4: held.
- Row 5 Never ("cite a tool by name alone, without version or step", L38): FIRES K3(a). Nouns "tool", "version", "step" absent from S026 capture; no entailment from Q6.
- Row 6: held (weakly; "modification date" imported but definitionally entailed distinction).
- S215 = S020 document identity: verified by content (capture header L35–36 + refetch L177); not a firing.

Under frozen K3 ("One such row falsifies C2"), C2 is falsified on the landing bytes. The landing did not change the entry bytes (identical at 02df67db and 64803d33), so the "repairs after scoring do not rescue" clause is not even reached — the scored bytes carry both defects.

Verification commands (all read-only; lane untouched; receipts copied to seat folder):
- `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && git show 64803d33362f50cf9094e91fc3a4a07216c563ca:corpus/knowledge/provenance-recording-r85.md | sha256sum` → c93f4b1ad8a2… (= worktree sha); `git show 02df67db:…` diff → identical.
- `grep -n "Provenance chains comprising only Entities|A derivation is a transformation|then we can say that the bar chart|prov:generatedAtTime and prov:invalidatedAtTime" corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt` → L779, L780, L781, L1021.
- `grep -n "Detailed provenance includes facets" corpus/captures/67983a3dbbd1d690aa648744.txt` → L453 (single paragraph L451–454 read).
- `grep -n "hadPrimarySource|primary source|primary" corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt` → contextual anchors L991–997, L2330, L3926–3930.
- Registry: `grep -n "S215|S020|S033" corpus/SOURCES.md` → L30, L43, L228. Refetch: `grep -n "prov-o|6e48bcc4" corpus/evidence/round57/refetch.tsv` → L167–169 (403s), L175–177 (200, S215), L179.
- No network used by this seat (no egress rows invoked; seat names no re-open). No tool installs/updates (operator rule read; pacman pause respected; nothing installed).

VERDICT: R85ReviewerEntry C2 fired — Rows 1 and 5 Nevers state what their cited quotes do not state or entail (K3(a)), falsifying C2 on the landing bytes.
