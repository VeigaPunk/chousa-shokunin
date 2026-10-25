# CritEntryAgg — attack on `corpus/knowledge/aggregator-vs-source-r36.md`

Falsify seat, wave 2. Target: the C2 entry, claim by claim, against its four captures (S096 `09fc63de41f293d43d631c46`, S097 `167e9db7dde3c998838e3469`, S098 `fea98dc5a5a486c988dd415c`, S099 `32d1d24b24fce96d2a078ec0` under `…/.qcache/`). No production file written; scratch `/dev/shm/chousa-r49-CritEntryAgg` created and removed.

## Checks run (command → observed output)

```
$ python3 - <<'EOF'   # sha256 index of .qcache; slice every spans.tsv row at its offset
... open(Q+f, encoding='utf-8').read() ...    # .txt universal-newline mode, as build-spans.py:61
rows 28 BAD under text-mode read: []
EOF
$ python3 corpus/evidence/round49/c2-count.py  → C2=PASS CAPTURE_BOUND=28/28 QUOTES_IN_ENTRY=28/28
                                                 INFERENCE_GROUNDED=2/2 rc=0
$ python3 corpus/evidence/round49/quote-substance-check.py → IDS=8 QUOTES=28 FAILURES=0
```

Byte-mode reading of the same `.txt` files gives `slice BAD` on 16 rows (S097/S098/S099): those captures are CRLF (S099 raw has 75 CRs) and the builder reads text mode, so `offset` indexes the newline-normalised form while `capture_sha256` is the raw-byte digest. All 12 spans of *this* entry are `.txt` forms, so the post-freeze CR-clipping repair (claims-erratum.md) does not touch this entry — verified, not assumed. Uniqueness: every quote occurs exactly once in its capture (`qcount_in_file 1`, 28/28); every SOURCES.md `char N` = spans offset + 80 (S096 `char 3599` = 3519+80). Held ground read: `SKILL.md:18,25-33`; `contextual-source-admission-r24.md:51-58,79`; `SOURCES.md:13,106`; `lessons/round-49.md:53-62`.

## Overclaims (sentence · evidence · smallest correct narrowing)

**O1 — fails (false authority; distorts held ground).** r36:49-52 "That is the lane's own tier rule — an aggregator is never the source — stated first-party by the aggregator, which supports scoping an index's reference list to the aggregator tier." `SKILL.md:18` is a *ranking* row (`primary > secondary > aggregator > unsourced claim`; failure mode "treating an aggregator as a primary source") and `SKILL.md:25-33` calls the ladder "this lane's own construction … a working standard". `r24:53-55` states the opposite exception verbatim: "An aggregator that *is* the artifact (a changelog for 'what shipped') can be tier-A-for-scope". S096 is exactly that case — the index's own manual is the artifact for "how CiNii derives its list", which is why row S096 carries tier `A`. → "S096 is the index's own statement about its own derivation — the artifact for this scope (tier A by r24's tier-for-this-scope rule) — and it shows the index's list cannot substitute for the paper's own reference list when the claim is about the paper; not that an aggregator is never a source."

**O2 — fails (mis-describes rung 3).** r36:31-32 "Rungs 3 and 4 work on the reference text, not on an identifier (S098)." Rung 3 is `3.引用文献の原文情報からDOIを検出して検索` (S098 char 29749): input is the reference text, the search key is a DOI — an identifier. Row S098's `teaches` cell already says "a DOI extracted from the reference text", so entry and registry disagree. → "Rungs 3 and 4 take the reference text as input; rung 3 extracts a DOI from it and searches by that identifier, rung 4 falls back to parsing it into bibliographic data (char 29706, 29749, 29775)."

**O3 — partly (unsupported quality ranking; inherits O2's mis-sort).** r36:61-64 "a hop resolved by parsing reference text is a weaker evidential object than one resolved by DOI." The answer gives `引用元の所在確認は、次の順で解析・検索を実施しています` (S098 char 29592) plus a list — a *search order*; no reliability statement appears in it. After O2 the dichotomy also fails to partition the ladder (1 and 3 are DOI matches; 2 and 4 are not). → "record the rung; an identifier match (rungs 1, 3) and a bibliographic parse (rungs 2, 4) are different kinds of hop and should not be pooled"; a reliability judgement may stay only if marked as the lane's own (identity match vs string similarity), not as read off the ladder order.

**O4 — fails (exclusivity contradicted by the entry's own sources).** r36:54-56 "so a hop checked against an index can be unresolved only because the index has not yet linked the reference." Counterexamples: S096 char 3684 `同定・統合された参考文献だけが表示されます` (unmatched references are *never* shown — permanent, not temporal) and S098 char 29482 `システムが引用元の所在を特定できた文献にリンクを付与しています` (a link exists only where a rung located the work). S097's lag is subset-bounded too: it covers `J-STAGEが連携している外部サービス に登録されている` works (char 2760), while the same capture says links appear when the article is published (char 2716). → "can be unresolved because the index has not yet linked it (S097, partner-registered works, days to two weeks) *or* because no rung located it (S098) and unmatched references are never shown (S096); the two causes are indistinguishable from an empty list."

**O5 — partly (comparator unsupported; capture-local support unquoted).** r36:57-58 "an empty cited-by list from an index is weaker evidence than an empty search of the sources themselves." No capture compares the two operations, "an empty search of the sources themselves" is never defined, and the object S096 names as authoritative is `実際の論文の参考文献` (char 3519). The unquoted in-capture support is S096 char 3577 `随時増加していきます。` under 被引用文献. → "an empty cited-by list is not evidence of absence — S096 char 3577 and S097's lag both allow emptiness; only the citing work's own reference list settles a negative hop."

**O6 — partly (title generalises across system and direction).** r36:2 "A citation index's reference list is a derived artefact, and it is incomplete in time." "Derived" is S096's *matching* caveat; the time statements are S096's *cited-by* growth (char 3577) and S097's DOI-link lag on a publisher platform (char 2760) — not a citation index's reference list. → "…and its cited-by list grows over time (S096 char 3577); DOI links for works registered in partner services lag days to two weeks (S097 char 2760)."

**O7 — partly ("the one method here" false in its own frame; "procedure" glosses a heuristic).** r36:65-69 "S099 gives that kind of move a concrete, field-tested procedure … it is the one method here that produces evidence about a source from outside the source." The S003 named in the same sentence is such a method, and S097/S098 (a third party resolving hops) also produce evidence about a source from outside it. S099's abstract says students "practiced the heuristic of 'lateral reading'" and that the intervention was six 50-minute lessons — a heuristic and an intervention, not a stated procedure. → "the operational form of S003's 'investigate the source' move, with a measured classroom effect at abstract level"; drop "the one method here". (The SIFT↔Wineburg pairing is legitimate as lane inference — neither capture links them; the abstract credits "research with professional fact checkers".)

**O8 — minor (quote stops before the clause the paraphrase needs).** r36:20-23 quotes `CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており` (S096 char 3752) then says the services "cover and merge differently, so their lists need not match each other" — carried by the *unquoted* continuation at char 3801 (`（それに伴って）別の手法で同定・統合処理を行っているため … 必ずしも一致していません`). → extend the quote through char 3801's clause, or mark the merge/mismatch clause as paraphrase of the unquoted continuation.

**O9 — minor (unused, mis-slotted evidence).** r36:36-38 puts the DOI-URL lag `DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。` (S097 char 2607) inside "The chain grows after publication". That lag is DOI resolution, not chain growth, and no inference uses it. → own sentence, or drop.

## What holds (attacked, survived)

- All 28 quotes byte-exact and unique; 28/28 spans exact slices; 8/8 anchors = `char N`. No reconstructed quote — S099's abstract is complete in the capture ("…digital content. These findings inform efforts…"), so display truncation is not a fabrication risk here.
- S096's operative statements rendered correctly (matched-only, char 3684; count of matched items, not the printed count): the "derived artefact" leg is sound. S098's four rungs are present in capture order; "link only where the system located the work" is a fair rendering of `付与しています`. S097's Observation scoping ("registered in its partner services") is correct — O4's overreach is confined to the Inference.
- S099 kept at tier B / abstract level; n = 271, n = 228, "matched control design" byte-exact; the Unknown names the paywall and the missing effect sizes.
- `ground:` verified: `grep -n -i 'scopus|web of science|cnki|cinii|pubmed' corpus/SOURCES.md` yields only S021/S022/S030/S032 — PubMed-*hosted papers*, not index documentation — so "the lane held no first-party statement from an index" is true.
- `adopted:` id map matches `lessons/round-49.md:53-62` by document (S087→S096, S088→S097, S089→S098, S092→S099); the NCPSSD homepage refusal is recorded there. Frozen legs pass at the lane tip (`C2=PASS`, `FAILURES=0`); this entry's evidence is untouched by the post-freeze builder change.

## Residual re-derivation hazard (not an overclaim; reported)

`capture_sha256` is the digest of the file *bytes* while `offset` indexes the newline-normalised text (`build-spans.py:61` uses `read_text`). A reader who hashes the file and slices the bytes — the natural reading of "the digest of the FILE" — gets 16/28 mismatched slices on the CRLF captures. Same code reproduces; different code fails silently.

VERDICT: aggregator-vs-source-r36.md's nine inference/observation sentences — fails (two outright: O1's "an aggregator is never the source" is not the lane's rule and contradicts r24:53-55 and row S096's own tier A; O4's "only because" is contradicted by S096 char 3684 and S098 char 29482), seven narrowable — while every quote, span, anchor and tier scoping in the entry itself verifies byte-exact.
