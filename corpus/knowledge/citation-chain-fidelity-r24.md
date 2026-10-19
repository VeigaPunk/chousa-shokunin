# Citation-chain fidelity — a resolved anchor is not a faithful hop (round 24)

source: S005 https://aclanthology.org/2025.acl-long.1534/ §4 "Measuring Citation Fidelity" + §6 "'Telephone Effect' in Citation" + Figure 1 fn 1 (PDF opened 2026-10-19); S003 https://hapgood.us/2019/06/19/sift-the-four-moves/ §"Trace claims, quotes, and media back to the original context" (opened 2026-10-19); local: corpus/knowledge/chain-resolution-r3.md:133 (resolved ≠ semantic support), corpus/knowledge/anchor-boundaries-r4.md:131 (same limit post-hardening)
verified-at: 2026-10-19 (round 24; S005 PDF pp. 31786–31794 opened at the anthology URL, S003 section opened at hapgood.us, all quotes re-read against the rendered text; the gate boundary re-read in the two named local entries — no gate re-run, fidelity comparison is outside its design)
recheck: 90d (`bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..` confirms the resolve-only boundary at the then-current gate; re-open S005 §4/§6 and the S003 section for revisions)

## Claim

`verify-chain` `resolved`/`verdict=match` establishes that a locator — heading text, verbatim quote, or whole line — EXISTS at each hop; it does not establish that the hop preserves the proposition and its qualifiers. A `faithful` disposition requires a per-hop comparison of the relayed claim against that hop's own source text (proposition, scope, quantity, hedge, date); a hop whose anchor resolves but whose relay was never compared stays `resolved-unchecked`, and a hop that cannot be opened stays `unresolved`. Falsifier: exhibit one `resolved` hop whose relay alters the source's proposition/scope/hedge — if resolving implied fidelity, no such case could exist; S005 Figure 1 supplies one in scholarship and the lane's fixture supplies one locally (chain-r3.md hop 6: two anchors resolve while the relayed statements disagree, chain-resolution-r3.md:133-136).

## Evidence

- S005 §4, p. 31790: "Assessing citation fidelity requires measuring how faithfully a citation reflects the original findings of the cited work." — fidelity is a property to measure, not to infer from the citation's existence.
- S005 §6, p. 31793: "scientific claims can evolve or degrade, as they are repeatedly paraphrased, summarized, or reinterpreted in subsequent research" — degradation is hop-by-hop.
- S005 Figure 1 fn 1, p. 31786: "The low-fidelity citation case overstates conclusions by failing to accurately specify the study population." — the lost qualifier is scope/population, checklist item 2.
- S003 §"Trace claims…": "trace the claim, quote, or media back to the source, so you can see it in it’s original context" and "get a sense if the version you saw was accurately presented" — the move is a comparison against original context, not a link-existence check.
- Local, observation: "the mode never parses meaning" (chain-resolution-r3.md:134); the limit stands post-hardening — "Not semantic support, not agreement, not context" (anchor-boundaries-r4.md:131).

## How chousa applies it

Per-hop fidelity checklist — at each `resolved` hop, compare the relay text against the source text the anchor landed on:

1. **Proposition** — same predicate asserted (X causes Y, not merely relates to Y)?
2. **Scope / population** — same who/where/when the claim covers?
3. **Quantity** — same numbers, units, denominators, intervals?
4. **Hedge / modal** — same may/suggests/in-this-sample qualifiers?
5. **Date / revision** — relay cites the revision actually read?

Worked example — HYPOTHETICAL chain, illustrative only, no artifact behind it:

| relay at hop (hypothetical) | source states | disposition |
|---|---|---|
| "A cut readmissions ~12% in discharged heart-failure patients (n=86; authors flag the small sample)" | identical proposition, population, number, hedge | `resolved` → faithful |
| "A cuts readmissions" | same study; scope and hedge dropped | `resolved` → altered-qualifier — the hop drifts the claim; log and re-derive from the source |
| cites a page now 404 | unopenable | `unresolved` — exempt and counted; no fidelity claim possible |

Relation to `SKILL.md:19`: the decision row's output — "chain with each hop's anchor verified or marked unresolved" — is the anchor layer this entry extends; its "never" column ("stopping at a summary of the citation") is the intermediary-engagement hazard S005 §6 measures. A record that stops at `resolved` and re-asserts the claim is exactly the low-fidelity hop the telephone effect propagates.

## Limits

- Observation: S005 measured ~13M sentence pairs in S2ORC full texts with a supervised 1–5 scorer; its numbers (e.g. the 0.06 intermediary effect) hold for that corpus and measure, not for web chains.
- Inference (labelled): that blog/web citation chains distort the same way, and that the five-item checklist approximates what S005's model scores — both are this entry's inference, not S005's finding.
- Observation: `verdict=match` is byte existence at token boundaries; semantic comparison stays outside the mode by design (chain-resolution-r3.md:258).
- Unknown: no lane-local fidelity measurement exists — verify-chain has no semantic arm, and the checklist's error rate on real chains is unmeasured this round.

## Rejected

- Rejected: "anchor found = claim faithfully relayed." Reason: S005 Figure 1 keeps an anchor — the cited letter exists and is quoted — while the relay drops the population qualifier; the lane's fixture hop 6 resolves over disagreeing statements. Flip: accept if the gate gains a per-hop comparison arm AND a labelled set shows `resolved` and `faithful` agreeing ~1:1.
- Rejected: "citing the review that cites the original is equivalent to citing the original." Reason: S005 §6 measures lower fidelity under intermediary engagement, correlated with the intermediary's own fidelity. Flip: accept for a specific claim if that intermediary's relay is itself verified faithful against the original at that claim.
