ATTACKS: C1 after-state on tip 1fc5ed1 vs measure-after.txt, c1-controls.txt, c1-before.txt; R46 counter; fixture pins

VERDICT: holds

All runs on /tmp/chousa-r47w2-RerunC1/tree (git archive of 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d).

1. C1 counter @ tip (c1-count.py --root <tree>):
```
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=3/3
CANARY=pass
R46_COUNTER=pass
R46_ENTRIES=2/2
C1=PASS
exit=0
```
Identical line-by-line to corpus/evidence/round47/measure-after.txt:5-13 (exit=0). No disagreement.

2. Controls @ tip, each via c1-count.py --tool <tree>/corpus/evidence/round47/controls/<x>.py:
- base-tool-r46.py: TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=0/3 CANARY=fail R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL exit=1 — matches c1-controls.txt:3-11.
- always-exit-1.py: POSITIVE_PASS=0/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL exit=1 — matches c1-controls.txt:13-21.
- neg-word-refuser.py: POSITIVE_PASS=1/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL exit=1 — matches c1-controls.txt:23-31.
No disagreement.

3. Before-state reproduced on freeze commit 22a44b8b (git archive to /tmp/chousa-r47w2-RerunC1/freeze, c1-count.py run with no --root; cwd=freeze tree):
```
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=0/3
CANARY=fail
R46_COUNTER=pass
R46_ENTRIES=2/2
C1=FAIL
exit=1
```
Identical line-by-line to controls/c1-before.txt:2-10. The before-recording's header hash (c3ea067e…) equals sha256 of tools/inference-ground.py at both 22a44b8b and 9a9f94db `git show <c>:tools/inference-ground.py | sha256sum` → c3ea067e165f00c1cf40939628ce3f59afc6d6d60119a92060b9055e03e6bbb3). Counter c1-count.py byte-identical freeze↔tip (6d39dce5… both).

4. R46 counter on tip archive (`python3 <tree>/corpus/evidence/round46/c1-count.py --root <tree>`):
```
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=3/3
CANARY=pass
C1=PASS
exit=0
```
Matches measure-after.txt:75-81 (exit=0). Round-46 counter byte-identical freeze↔tip (524b9eef… both); R46 entries (evidence-pool-versioning-r39.md, amendment) and round46/spans.tsv byte-identical freeze↔tip — the R46 leg is canonical.

5. Fixture pins: PINNED (c1-count.py:45-56, 10 entries) vs sha256 of every file in live /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/inference-ground-r47/ AND in the archive tree — all 10 hashes match exactly (counts.json 17fb165b…; junk-flip-asserted 01ef1689…; junk-flip-denied 440cc5cf…; junk-flip-figure 67997d02…; positive-affirmed 7278efd7…; positive-figure-negated 7a15216a…; positive-negation-kept 2119e3e8…; spans.tsv 38a536bd…; spans/S901-1.txt 7c2aa321…; spans/S902-1.txt c2184ca7…). No extra/missing pinned files; FIXTURES_CHANGED= ∅.

6. Probe realness (not a trivial scorer): tool run directly per fixture (same argv c1-count uses) — junk-flip-asserted rc=1 "FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revised'" (span-negated phrase asserted positively); junk-flip-denied rc=1 token='the release ships a frozen pool / frozen' (affirmed phrase denied); junk-flip-figure rc=1 token='7,572 / counts key figures/answers_named_source' (affirmative-key figure re-denominated as negative); positives positive-negation-kept / positive-affirmed / positive-figure-negated each rc=0 GROUND: PASS. All three claimed classes exercised and only they fail; canary (neutral names) passes — no filename keying.

7. Claim wording vs implementation: rule sentence (claims.md:32-41) matches docstring rule 5 verbatim (inference-ground.py:26-35); refinements paragraph (claims.md freeze-adjacent; docstring :36-45) all implemented: every occurrence read w/ mixed-polarity abstain (phrase_polarity :290-305), negator bounded to phrase's own line+clause (occurrence_polarity :274-287), implicit negators (IMPLICIT_NEG :251-253), un- prefixed flip (:327-330), digit-boundary figures (numeral_in :140-143), key-path ancestors (count_keys :344-373), mixed-polarity keys abstain (key_negated/figure_flip :376-395). Kill rule in counter (c1-count.py:92-97) present. No hidden backdoor found; named limits (lexical, synonyms/antonyms/word-windows) are declared in claims.md:62-64 and docstring :55-58.

Verification gaps: none for the claim as stated. Residua: pin set doesn't cover any future extra fixture file (would go unnoticed by c1-count), but that changes nothing in the frozen measured state; R46 leg scored on tip tool, which the R46 counter's own "before" covers.

Scratch /tmp/chousa-r47w2-RerunC1/ will be deleted before finish.
