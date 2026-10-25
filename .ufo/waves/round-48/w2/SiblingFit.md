# SiblingFit — sibling-overlap scan: R48 false-refusal finding + proposed lexical polarity behavior

**Verdict:** NO sibling PROVINCE.md claims ownership of either contested surface. The false-refusal fix to `tools/inference-ground.py` (polarity lexicon: `IMPLICIT_NEG`, `UN_NEG_RE`, `occurrence_polarity` 3-word scope, `figure_flip` key-path negation) and the `#### Inference`-bullet grounding gate sit squarely inside chousa's declared province ("this lane's own corpus and gates"; `chousa-shokunin/PROVINCE.md:5-8`). Eight siblings explicitly route research method to chousa; zero claim a natural-language negation/polarity lexicon or research-corpus inference-grounding. Read-only scan; no writes outside this report, no network, no installs.

## Method (actual commands and observed output)

```
$ for f in */PROVINCE.md; grep -n -i "polarity|negat|lexic|pars|inference|research.method|
   claim-vs-source|source.verif|grounding|grounded|language|english|refus" "$f"
   # 21 lane provinces scanned: audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama
   #   kasegi kengaku kotoba kotodama kumitate lore mado mori revenger souji tabi tameshi tsukuroi
$ python3 -c "json.load(MANIFEST.json)['roster']" → roster len 13; 21 *-shokunin dirs all hold PROVINCE.md
```

Observed: `polarity` → 0 hits in any sibling province; `negat` → 0 ownership hits (only kake:375 "non-endorsement … not a crawl refusal"); `language` → 0 ownership hits (only mado:78 "English upstream documentation channels" — a citation-channel rule, not NLP); `pars*` hits are kaidoku binary-format parsers and kake publisher/parser limits (kake:58, :302 sitemap parsing), none lexical NLP; `inference` hits are revenger/kaidoku/game-dev-3d/mori evidence-label and attribution terms, none a research-corpus gate.

## Finding 1 — research-method inference-grounding: chousa-owned, affirmations from eight siblings

- chousa `PROVINCE.md:5-8` Owns: "question framing; source hierarchy (primary/secondary/aggregator/unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy; …; this lane's own corpus and gates." `#### Inference`-bullet grounding of knowledge entries is claim-vs-source verification on the lane's own corpus — verbatim in-scope.
- Explicit sibling grants: audio `:53` "research method (chousa)"; kagi `:67` "chousa owns the research method (`SOURCES.md` restates neither method nor admission bar)"; kake `:36` "`chousa` owns research method and source hierarchy"; kasegi `:47` same; kengaku `:137` "research method … stays chousa's (`chousa-shokunin/SKILL.md`); this lane holds neither method nor duplicates it"; kumitate `:27` "Research method → chousa"; kotodama `:19` refuses "general source-research method (chousa)"; lore `:27` "chousa — research method, not lore canon"; souji `:82` "chousa-shokunin owns the research method and source hierarchy".
- Vocabulary overlap, no scope conflict: revenger `:6-7` and kaidoku `:6` own "observation/inference/unknown" evidence-ledger discipline *over shipped artifacts*; game-dev-3d `:11` adopts it for static artifact inspection. kengaku `:140` states the rule: "the shared word 'probe' carries no scope" — same for "inference". Chousa's gate verifies its own knowledge-entry inference bullets against cited spans; substrate disjoint.
- Adjacent-but-clear: tameshi owns "verification-fixture craft" (`PROVINCE.md:8-18`) but `:14-16` "every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general). Never edits a sibling's gate code". So: instrument code+behavior = chousa; a *generalized* claim that polarity-checking is a reusable fleet fixture method is tameshi-shaped and cannot be claimed from one lane.
- kotoba census row (kotoba `PROVINCE.md:51`): "chousa | adjacent | … | deep-research method; kotoba cites it, never re-derives it (`corpus/QUALITY.md`: claim admission stays here, the research method stays chousa's)".

## Finding 2 — language polarity parsing (negation lexicon, un- prefix rules, scope window): UNOWNED by any sibling; defaults to the owning lane's instrument

- No sibling province declares NLP-style ownership: no `polarity`/`negat`/`language`/`english`-grammar rows; kotoba's only "lexical" claim is a frontmatter approximation (`PROVINCE.md:15`: `trigger.no_xml_tag` "approximated lexically on the unparsed `name`/`description` text") — prompt/skill surfaces, not English-negation semantics of research bullets.
- Default owner: the instrument owner. `tools/inference-ground.py` is chousa's gate; the lexical polarity behavior is lane-internal implementation detail unless the round's claim asserts generality. C1's tag line (`claims.md:19`) already caps this: "plumbing. No semantic-entailment claim is made; human correctness of this fixed set remains outside this lexical counter" — the proposed behavior stays a lane gate predicate, not a claimed NLP discipline.
- If a W1/W2 proposal widened the lexicon into a *fleet-standard* polarity language or a shared refusal-taxonomy, that would be contested/unowned ground: no province covers it, so it routes per tsukuroi `:41-42` "unresolved ownership goes to the protocol integrator, never to whichever lane answered first."

## Finding 3 — contested-scope routing (where it goes if contested)

- Lane rule: `chousa-shokunin/PROVINCE.md:17` "Out of province → report, never absorb" — echoed verbatim in kagi/kake/kasegi/kengaku/kotoba/kotodama/kumitate provinces.
- Operator channel: fleet `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` — live precedents: kaidoku/revenger RE-domain overlap pending at line 42 (kotoba `:55`, `:65`); kotoba precedence rule provisional pending answer at line 105 (kotoba `:46`, `sibling-overlap-census-round49.md` §Round 51, routed D6); census finding of *no documented tie-break* between overlapping descriptions (kotoba `:16` round-48 row, S022/S023/S018).
- Instrument-adjacency: if the polarity behavior were proposed as reusable mutation/fail-closed craft → tameshi's two-lane evidence rule (`tameshi:15-16`); as observation/inference ledger over artifacts → revenger/kaidoku (themselves unresolved, integrator-held); as skill/frontmatter wording → kotoba. None of those is triggered by the frozen R48-C1 instrument change.

## Risks / non-overlap caveats

1. Scan is PROVINCE.md-only per assignment: sibling `SKILL.md`/corpus could hold un-declared polarity claims; provinces are the authoritative ownership record each lane cites across-lane (kagi `:67`, souji `:82` both cite provinces as the ownership source).
2. `kake-shokunin/PROVINCE.md:36` boundary: kake holds domain findings only; if a polarity rule were applied to *kake's* publisher-facing text rather than chousa corpus entries, ownership shifts to kake. R48-C1 fixtures are chousa `corpus/SOURCES.md`-rooted only — in-province.
3. Worktree copies of PROVINCE.md under `.ufo/waves/**` are sibling evidence snapshots, not separate owners; only the 21 lane-root files were treated as authoritative.
4. Provinces were read at working-tree HEAD (commits pinned where provinces themselves pin siblings, e.g. kotoba's per-lane commit column); no fetch performed — sibling tips may have moved since their pinned cites.

**Report trailer:** `.ufo/waves/round-48/w2/SiblingFit.md` — L1Chousa48.SiblingFit, connector, read-only.
