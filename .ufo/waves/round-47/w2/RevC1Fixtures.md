ATTACKS: C1 fixtures as oracle — are the three junk fixtures of corpus/fixtures/inference-ground-r47 strawmen that a cheaper rule also kills? Scored the two required cheap tools plus two variants against c1-count.py (frozen predicate, pinned fixture bytes).
VERDICT: holds — C1=PASS reproduces (3/3, 3/3, canary=pass, R46 counter=pass, R46 entries=2/2, twice). The strawman hypothesis is rejected: no cheap lexical rule I built reaches C1=PASS; the two required rules kill 1/3 and 0/3 of the junks. The junk fixtures are not strawmen for bullet-lexeme rules.

## Baseline (frozen claim)
$ python3 corpus/evidence/round47/c1-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / CANARY=pass / R46_COUNTER=pass / R46_ENTRIES=2/2 / C1=PASS (rc=0); rerun identical → same.

Production kill tokens (per-fixture, verbose runs):
- junk-flip-asserted.md: FINDING INF_POLARITY_FLIP token='no revision is recorded / revised'
- junk-flip-denied.md: FINDING INF_POLARITY_FLIP token='the release ships a frozen pool / frozen'
- junk-flip-figure.md: FINDING INF_POLARITY_FLIP token='7,572 / counts key figures/answers_named_source'
Positives all GROUND: PASS rc=0.

## Cheap tools (wrappers around controls/base-tool-r46.py; lexical helpers imported from tools/inference-ground.py)
Built in /tmp/chousa-r47w2-RevC1Fixtures/ (cheapA.py, cheapB.py, cheapC.py, cheapE.py), each: parse same args as base, run base as subprocess, add rule findings as INF_POLARITY_FLIP, exit 1 if rule fires or base failed.
- cheapA: refuse any bullet whose UNQUOTED text contains a negator AND a word sharing a 5-letter stem with a quote (the assignment's rule).
- cheapB: refuse every bullet whose QUOTED phrase contains a negator (assignment's second tool).
- cheapC: refuse any bullet whose unquoted text contains a negator (minimal variant).
- cheapE: refuse any bullet whose quoted phrase OR unquoted text contains a negator (maximal variant).

## Scores (c1-count.py --tool <it>; verbatim decisive lines)
cheapA: POSITIVE_PASS=2/3 JUNK_KILLED=1/3 CANARY=fail R46_COUNTER=pass R46_ENTRIES=0/2 C1=FAIL
cheapB: POSITIVE_PASS=2/3 JUNK_KILLED=1/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=2/2 C1=FAIL
cheapC: POSITIVE_PASS=1/3 JUNK_KILLED=2/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL
cheapE: POSITIVE_PASS=1/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL
None reach C1=PASS. The only rule that kills all three junks (cheapE) also kills two of three positives: the junk negators and the legitimate (non-flipped) negators are lexically identical bullet words; separation needs span-side context.

## Per-fixture r47 detail (rc / #INF_POLARITY_FLIP)
cheapA: negation-kept 1/1, affirmed 0/0, figure-negated 0/0 | asserted 0/0, denied 1/1, figure 0/0
cheapB: negation-kept 1/1, affirmed 0/0, figure-negated 0/0 | asserted 1/1, denied 0/0, figure 0/0
cheapC: negation-kept 1/1, affirmed 0/0, figure-negated 1/1 | asserted 0/0, denied 1/1, figure 1/1
cheapE: negation-kept 1/1, affirmed 0/0, figure-negated 1/1 | asserted 1/1, denied 1/1, figure 1/1

Why the required rules fail:
- junk-flip-asserted: the negator "no" lives INSIDE the quote (`no revision is recorded`); unquoted text has no negator, so rule A (and C) can't fire; rule B fires, but nothing lexical distinguishes this from positive-negation-kept, which quotes the same span legitimately (production distinguishes via span polarity: phrase negated → bullet asserts a scope word with no nearby negator).
- junk-flip-denied: the negation is in the bullet body ("not frozen"), none in the quote; rule B can't fire; rule A/C fire, but so they do on legitimate positives (negation-kept, figure-negated, r46 positive-a).
- junk-flip-figure: the bullet has NO quotes at all; only bullet-lexeme rules that fire on bare unquoted negation catch it, which over-collects on positive-figure-negated ("1,582 sourced answers carry no archive key" is legitimate). Production handles it via counts-key-path negation (key figures/answers_named_source is affirmative; bullet re-denominates), requiring counts.json, not bullet lexemes.

R46 legs: cheapB kills r46 positive-c (quote "no revision is recorded" ⇒ rc=1 flips=1) ⇒ R46_COUNTER=FAIL; cheapA kills neither r46 positive (R46_COUNTER=pass) but kills both real entries (stem-overlap "pages"/"revision" with quotes plus unquoted "no"/"not" ⇒ R46_ENTRIES=0/2); cheapC/cheapE fail both legs (entries contain unquoted negators: "no per-citation stamp", "does not do"). Exact counter argv for entries — --registry root/corpus/SOURCES.md --counts /dev/null --quiet, all-absolute — returns rc=0 for the production tool on both entries.

## Residual risk / verification gaps
- I scored only four cheap lexical rules (the two required plus a minimal and a maximal variant); other bullet-only heuristics (e.g., stem-overlap without negator, figure-presence OR negator) might approximate, but any rule that fires on all three junks necessarily fires on a positive (cheapE proves the collision). A cheap rule could only pass by keying on fixture names or span files — excluded by CANARY (neutral names) and by the counter's pinned-span checks; no such cheat is exercised here.
- The R46_ENTRIES leg was re-verified by logging the counter's exact argv via a fake tool (argv.log) and by direct re-run (rc=0); one early confusion was my own ad-hoc run with a misspelled registry path, not a counter defect.
- No tools were installed (none needed); no network egress; no lane production files modified. Scratch /tmp/chousa-r47w2-RevC1Fixtures/ removed before finishing.
