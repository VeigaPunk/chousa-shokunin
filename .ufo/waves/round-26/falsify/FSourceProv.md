# FSourceProv — S039 PROV-DM §5.2.1 quote/location/scope attack (round26 attempt1)

Seat: `ChousaR26R.FSourceProv` (author-lane advisory; not an outside judge).
Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` from
`corpus/evidence/round26-measured-revision.json`, extracted with
`git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FSourceProv/tree`
(exit 0). Claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e` was not
re-measured. Lane HEAD at the time was the same commit, `0e9784bd`.
Archive digests match the revision JSON: `tools/research-gate.sh` c2c813f1…,
`corpus/SOURCES.md` 8308e629…, `corpus/knowledge/registry-link-r26.md` 248224a2….
`corpus/lessons/round-26.md` (not in the JSON input list) is c8734fc9….

VERDICT: **not falsified.** The S039 quote is verbatim, has 23 words, appears
exactly once in the document, and sits inside the cited `#term-Derivation`
§5.2.1. No lane record presents optional generation/usage as registry policy.
Every record that mentions S039 scopes it as optional derivation detail and
labels the source/used-by analogy as inference.

## Observed (static public documentation only)

| check | command | result |
|---|---|---|
| open cited version | `curl -sS -L -o prov-dm.html -w … https://www.w3.org/TR/2013/REC-prov-dm-20130430/` | exit0, HTTP200, final URL unchanged, 271572 bytes, sha256 `5c925c21bc96c285b25017c3b90d82cf74251d07713b71fcb81ca60f873c9e88` |
| anchor | `grep -n 'id="term-Derivation"'` | line2471 `<section id="term-Derivation">`, line2472 `<h4>5.2.1 Derivation</h4>`. The registry anchor `section5.2.1 Derivation, term-Derivation` (`SOURCES.md:49`) resolves |
| exact quote | python: tag-strip + whitespace-normalize the `term-Derivation` section, then `q in section` and document count | `QUOTE_IN_SECTION True`, `WORDS 23`, `COUNT_IN_DOC 1`. Raw HTML line2485 is in the section's first `<p>`, after the glossary definition and before the PROV-N `wasDerivedFrom(id; e2, e1, a, g2, u1, attrs)` definition |
| optionality | same section text | “activity : an OPTIONAL identifier (a)…; generation : an OPTIONAL identifier (g2)…; usage : an OPTIONAL identifier (u1)…”. Next sentence after the quote: “Optional information such as activity, generation, and usage can be linked to derivations…” |
| latest version | `curl -sS -L -o latest.html https://www.w3.org/TR/prov-dm/` | HTTP200, sha256 is the same `5c925c21…`, so the cited REC is still the latest published version (freshness holds as of 2026-10-21) |
| errata | `curl … https://www.w3.org/2011/prov/errata.html` (linked from the REC) | exit0, HTTP200, 18090 bytes, sha256 `88dc4c9c…`. Occurrences in the tag-stripped text: `5.2.1` 0, `Derivation`/`derivation` 0, `wasDerivedFrom` 0. No erratum touches the quoted text |
| no registry concept | count over the full tag-stripped document | `registry` 0, `used-by` 0 |

The quote at `corpus/lessons/round-26.md:45` stops at “can be provided”. The
original sentence continues: “, so as to make the derivation path, through
usage, activity, and generation, explicit.” The cut is clean and does not
change the meaning; the 23 words keep the permissive “can”.

## Scope audit — every S039 / PROV-DM mention in the target tree

`grep -rniE 'PROV-DM|\bPROV\b|prov-dm|wasDerivedFrom|S039'` over `*.md/*.sh/*.py/*.json`.
`SCORECARD.md` and `SKILL.md` have no hits (`grep` exit1).

- `corpus/SOURCES.md:49`: scope is “optional generation/usage detail; not a registry or verification requirement”. Teaches “PROV-DM permits …”, which matches the source's “can be provided” and OPTIONAL. Status `mined`, used-by `corpus/knowledge/registry-link-r26.md`, recheck 365d.
- `corpus/knowledge/registry-link-r26.md:1`: `source:` says “§5.2.1 Derivation (optional generation and usage details)”. That matches the OPTIONAL markers.
- `corpus/knowledge/registry-link-r26.md:14-17`: “permits explicit generation and usage details” (S039, §5.2.1), followed by “an analogy [INFERENCE], not a PROV-DM rule. PROV-DM does not prescribe this registry, the mined status, or these findings.” The negative claim agrees with the zero `registry`/`used-by` counts above. It is an absence observation, not something quoted.
- `corpus/lessons/round-26.md:45`: Gate boundary is “optional derivation detail, not a required registry/checker; the source/used-by analogy is explicitly an inference”.
- `corpus/README.md:64` indexes S039 for the registry-link note and says “a declaration relation is not semantic citation support”. `corpus/README.md:866-868` says the registry policy is “the lane's design, not … PROV requirements”.
- `corpus/SOURCES.md:66-69,76-87` (navigation and search log): it says “not a Cochrane or PROV requirement” and calls the registry policies “explicitly the lane's design rather than external requirements”.
- `LOG.md:1028` gives only a list of S034–S039 ids, with no policy claim.

No record uses S039 to support finding semantics, the `mined` status,
exact-path `used-by`, or `META_*` severities. QUALITY7 (scoped tier-A use)
and QUALITY8 (source states “can be provided”, never claimed as a
requirement or as truth) both hold for this row.

## Inference / residual (not falsifications)

- [INFERENCE] The build seat `SrcProvDmDerivation.md:4` places the quote in the “paragraph after the definition”. The quote follows the glossary definition but precedes the formal PROV-N definition. The production lesson says only “section5.2.1 Derivation”, which is accurate. This is an advisory-report wording note only.
- The entry's `verified-at:` (`registry-link-r26.md:2`) describes the spec and control checks but does not say S039 was reopened. Whether that matters for criterion 6 is outside this item's question and is not graded here.
- No gate, selftest, probe, `--registry` run, or mutation was executed. This item names no bounded checks, so none were run.

## Tools

No installs or updates. I used only the existing `curl`, `python3`, `git`, `sha256sum`, and `grep`. Sandbox: `/tmp/chousa-r26-falsify-FSourceProv` (archive tree, `prov-dm.html`, `latest.html`, `errata.html`).
