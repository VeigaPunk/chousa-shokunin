# chousa round 99 — frozen claims (L1 `ChousaR99`)

Base `47ed34fa785288837f84cde9db15c41300854a78` (round-98 landing plus its non-author spot-check). Freeze F = the lane
commit that first carries this file; its hash is recorded in `plans/round-99.md` `## Freeze` by the next commit (a
commit cannot name its own hash — round-98 spot-check routed defect 1). Fresh-start rule: not bound (r91-r98
admitted, MANIFEST closures). Two claims, two axes, no exploratory claim. Machine form: `claims.json`.

Causal separability: C1 changes `tools/gate-records.py` only; C2 adds one knowledge entry, its registry rows and
captures. C2's gate records verify OK under the base tool and under the C1 tool alike (none of its captures is a
challenge page); C1's battery reads S234's capture (C2's round, but a rejected row no entry cites) and no C2 file.

## C1 `C1-GATE-CHALLENGE-R99` — operability (lowest axis, historical 3/10)

**Sentence.** `tools/gate-records.py verify` gains a CHALLENGE check: a url/admit record, or a rev record whose path
is `corpus/captures/<24 hex>.txt`, fails with code CHALLENGE (exit 1) when its capture's normalized, lower-cased text
has at most 200 words and contains one of the 11 frozen `CHALLENGE_MARKERS`. Through the public CLI it refuses seven
challenge-page records in a scratch lane (three committed captures — S230 reCAPTCHA, S229 cookie wall, S234 "Client
Challenge" — and four written by the battery), admits four non-challenge records (two committed captures, a
300-plus-word article that names "reCAPTCHA" and "Just a moment", a 30-word page with no marker), refuses four records
on the production path (`--root` the lane: url/admit on S230 and S234, rev on S230 and S229 at BASE), prints output
byte-identical to the base tool on every committed knowledge/lesson file carrying GATE-RECORD lines, and five
stand-in tools (short-only, marker-only, known-bytes, scratch-only, lane-only) each fail the battery. The base tool
admits all seven challenge records.

**Counting command.**

    python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>

**Predicate (frozen).** stdout carries
`NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=n/n BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5` with
n ≥ 25 (n counts the files at the measured revision; 25 at F) and `CHALLENGE_CONTROLS_R99=PASS`; exit 0.

**Before (do-nothing control).** The base tool through the same battery (`--tool <base tool> --no-oracles`; the
oracles are patches of the candidate, so they have no base form): `NEG_REFUSED=0/7 … PROD_REFUSED=0/4 …
CHALLENGE_CONTROLS_R99=FAIL`, exit 1 (`corpus/evidence/round99/before/c1-base.txt`).

**Kill rules.** K1 any NEG or PROD record admitted, or failing with a code other than CHALLENGE alone. K2 any POS
record refused. K3 any HARM file whose stdout or exit code differs from the base tool's. K4 any oracle passing the
battery. K5 the battery passing with `--tool` = the base tool.

**Named limits.** (a) Lexical: a challenge page in other words than the 11 markers, or longer than 200 words, passes.
(b) A real document of at most 200 words that contains a marker phrase is refused (false refusal). (c) Markers are
matched after the tool's normalization only (curly quotes, whitespace, lower case): no NFKC, so full-width letters or
a zero-width character inside a marker pass. (d) The url/unreach form has no capture and is not checked; a rev
record whose path is not under `corpus/captures/` is not checked. (e) The battery's oracle set is five patches; it
does not show that every wrong tool fails it. (f) QUALITY 126 detection forgers: o4/o5 detect the scratch lane by the
absence/presence of `.git`; a forger that detects the battery any other way (process tree, `S9xx` fixture ids, the
`fixture.invalid` host) is not scored.

## C2 `C2-ENTRY-R99` — coverage (new province ground: measured quotation-error rates)

**Sentence.** New entry `corpus/knowledge/quotation-error-rates-r99.md`, sourced on S236 (Europe PMC's core record of
Jergas & Baethge 2015, the authors' own abstract, tier B) and S233 (Mogull 2017, publisher full text, tier A), both
opened this round, holds 23 located quotes (J0-J8, G0-G13) and an 8-row decision table on how often a cited source
fails the citing sentence, how a mismatch is classed (major/minor, source error) and how the rate is counted. Every
number a Do cell states is printed in one of that row's own warrant quotes. At BASE no knowledge entry contains the
phrase "quotation error" and the entry is absent.

**Counting commands.**

    python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md
    bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-rates-r99.md --root .
    python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-rates-r99.md --root .
    python3 -B corpus/evidence/round99/entry-controls-r99.py --root .

**Predicate (frozen).** `GATE_RECORDS files=1 records=25 ok=25 fail=0` exit 0; `METADATA_COMPLETE=1/1` and
`RESEARCH_GATE: CLEAN` exit 0; `rev_match=4/4` and `SEARCH_RERUN: CLEAN` exit 0; controls tally
`QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0
BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2` and `ENTRY_CONTROLS_R99=PASS`, exit 0.

**Before.** Entry absent at BASE: `gate-records.py verify` exit 2 (`GATE_RECORDS_ERROR missing`), controls exit 2;
`BASE_TOPIC_HITS=0` (`corpus/evidence/round99/before/c2-base.txt`).

**Kill rules.** K1 a quote not in its source's capture, or a J quote outside its JSON field. K2 a Do-cell number not
printed in that row's warrant quotes. K3 the S236 record is not Jergas & Baethge 2015 (pmid, doi, year, journal,
volume) or S233's capture lacks its doi/title. K4 a forgery accepted or a no-claim edit refused. K5 a decision row's
Do cell states what its warrant quotes do not say (a paraphrase that widens or reverses a quote) — judged by a
reviewer, not by the controls.

**Named limits.** (a) S236 is an abstract, read through an index record (tier B). (b) Both sources are about medical
journal articles; nothing here measures the lane's own citation-failure rate. (c) The controls check numbers and
quote presence, not that a paraphrase is faithful beyond its numbers (K5 is reviewer-judged). (d) The two rates
(25.4% pooled over 28 studies, 14.5% re-counted over 15) count different things; the entry does not reconcile them.

## Amendments

(none at F)
