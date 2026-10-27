# R58CritC2Scope — C2 province boundary

## Assessment

**Recommendation: keep the proposed S101 carrier-alphabet entry in chousa; no sibling route is evidenced.** It is a source-scoped account of what a held bibliographic specification says, used to support claim-vs-source verification. It is not a claim that GB3469 is currently valid or that journals enforce it. That limit is material: the topic is bibliographic, but the deliverable is grounded source research rather than a standards-authority or implementation claim.

## Counterexample / boundary risk

Strongest counterexample: a table of Chinese document-type and carrier identifiers can look like subject-matter reference content rather than reusable research method. Chousa's SKILL.md calls its domain the reusable *method* of source research (lines 8–11), so merely collecting an alphabet without an explicit verification use would risk scope drift. Here, however, the frozen claim is explicitly about located text in a registered S101 capture, and the proposed entry distinguishes the source's own statements from current validity and wider membership. That makes the entry a bounded source finding, not a general standard guide.

## Evidence

- `chousa-shokunin/PROVINCE.md:3-8` defines deep-research method and owns question framing, source hierarchy, citation chaining/hop resolution, claim-vs-source verification, search taxonomy, and this lane's corpus/gates. It does not reserve research outputs to method-of-search mechanics alone.
- `chousa-shokunin/SKILL.md:8-11, 20-23` likewise defines source research and claim/source checking; its decision table says a research record carries the declared question and support states remain separate.
- Frozen `corpus/evidence/round58/claims.md:13-17` scopes C2 to S101's located text and explicitly excludes present-day validity and broader semantic truth. Frozen C2 quote set contains the section heading, type/carrier notation, examples, and a separate document-code heading. No live fetch is part of this determination.
- `corpus/SOURCES.md:111` already registers S101 as a B-tier copy of the data specification, with use scope covering its fields/type identifiers, reference-record elements including 文献类型及载体类型标志, and separate 文献标志码 classifications. This is direct lane evidence of source admission for the subject, not an inferred new owner.
- Existing `corpus/knowledge/citation-count-semantics-r37.md` already uses S101 alongside Chinese citation-index sources to record what those sources say about reference fields and journal evaluation; `corpus/knowledge/normative-reference-chain-china-r57.md` similarly records what Chinese normative documents bind users to, with explicit limits. The new alphabet is a distinct slice, not the same authority repeated: the r37 entry mentions the field but does not enumerate the type/carrier notation.
- Fleet sibling `PROVINCE.md` sweep for `bibliograph|文献类型|GB ?3469|GB/T 7714|carrier` produced only incidental hits in game-dev-3d, kaidoku, kengaku; none declares Chinese bibliographic type/carrier identifiers as owned. `kotodama` is fictional linguistic-cultural worldbuilding, and its `SKILL.md` bibliography hit concerns a phonetics citation correction, not a real-world bibliographic standard. No better sibling route is supported by these hits.

## Route and correction

The smallest safe correction is **no scope change**: retain the entry only as S101-attributed, source-limited knowledge; preserve the explicit non-claim about current standards validity and codes outside the frozen evidence. If the final text instead presents a normative/current code list, interpretation of GB3469, or journal-compliance guidance, that broader claim should be removed or separately routed for ownership review rather than silently absorbed here. No other lane's province presently supplies a better destination.

Impacted axis: **adjacency**. This is a boundary assessment only; it does not decide C2's truth, admission, or score.

## Checks / provenance

Read frozen claims and exact `c2-count.py`/`quotes.tsv` before assessment. The claims, counter and quote-set last-change commits are each `9e73a031ab1ac3bac343de008850d7d87f9e5634`; raw capture digest observed with `sha256sum` is `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, matching the frozen claim. `git diff 9e73a031ab1ac3bac343de008850d7d87f9e5634 -- corpus/evidence/round58/{claims.md,c2-count.py,c2/quotes.tsv,c1-count.py}` produced zero lines for each file. No counter was run for this scope task, no live fetch was made, and no source-repository file was changed.

VERDICT: C2 S101 carrier-alphabet province challenge survives as a genuine boundary question but is resolved in-province on the current frozen, source-limited claim; no sibling owner is evidenced. Broader standards-validity or compliance claims would be out of scope and require rerouting.