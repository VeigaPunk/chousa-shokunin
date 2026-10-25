# ExecC1Regress — round 47 wave 1 — regression sweep of the polarity probe

seat: `L1Chousa47.ExecC1Regress` (executor, leaf; no labrat spawned)
lane HEAD: `a15610a59aaeaf43b79ccc650acee4bd4da00341` (probe landing); base tool `9a9f94db:tools/inference-ground.py`
tools: landed `tools/inference-ground.py` sha256 `8899e786…7a0a40`; round-46 `ig46.py` sha256 `c3ea067e…6bb3`
installs: none. No fetch, no lane writes besides this report. Scratch `/tmp/chousa-r47-ExecC1Regress/` deleted.

## Item

For every `corpus/knowledge/*.md` (61 files), run the round-46 tool and the landed tool with
(m46) `--spans corpus/evidence/round46/spans.tsv --counts /dev/null` and
(m45) `--spans corpus/evidence/round45/spans.tsv --counts corpus/evidence/round45/counts.json`,
both with `--registry corpus/SOURCES.md --root <lane>`. Tabulate exit changes and new
`INF_POLARITY_FLIP`, judge each one, and run both C1 counters.

## Verdict

**NO REGRESSION, measured.** 0/61 entries changed exit under either manifest set. 0 `INF_POLARITY_FLIP`
findings over the corpus. All 244 outputs are byte-identical between the two tools: the concatenated
outputs of each tool hash to sha256 `222038d2bd43bce0765850eee6d6583f6c569cd6c24de92155abcfcdead70ad5`.
The table of new flips is empty, so there is nothing to judge as a true flip or a false positive.
Instead, every bullet the probe actually evaluated is judged below as a true negative.

Manifest pins: round46 `spans.tsv` `d9bdd226…5964`; round45 `spans.tsv` `fbb6862c…80ac`;
round45 `counts.json` `ded8747e…665c`; `SOURCES.md` `c69c75bd…6274`.

## Exit table (round-46 tool -> landed tool)

| exits (m46, m45) | entries |
|---|---|
| 0->0, 1->1 | 2 (`evidence-pool-versioning-r39`, `-r39-amendment-2026-10-23`) |
| 1->1, 1->1 | 59 |

Finding-code histogram, identical for both tools. m46: SECTION_ABSENT 54, TOKEN_NOT_IN_SPAN 12, UNCITED 12,
UNGROUNDED 10. m45: SECTION_ABSENT 54, TOKEN_NOT_IN_SPAN 15, UNCITED 12, UNGROUNDED 10. POLARITY_FLIP 0.

## Where the probe can reach (the sweep is not vacuous)

The probe only examines tokens that a span or a counts key has already grounded (landed tool, `main`:
`if ok and not is_num` / `if ok and is_num`). 54 entries have no `#### Inference` section. Of the 7 that
do, 4 ground 0 tokens. The reachable surface is 17 probe evaluations, recorded by a trace harness that wraps
`polarity_flips` and `figure_flip`:

- m46, `evidence-pool-versioning-r39.md:20-22`: 6 phrase evaluations. All read `negated=False`, so only
  rule P2 applies. Stem hits in the bullets are `pages` ×2 and `recall`; no negator sits in the 3 words before any hit.
  - `:20` "The release fixes the pages by shipping `Pre-processed Wikipedia Pages (June 2017 dump)`"
    is affirmative, matching the span. TRUE NEGATIVE.
  - `:22` "agree with the super-annotators' at `recall of 72.36%`" is affirmative. TRUE NEGATIVE.
- m46, `evidence-pool-versioning-r39-amendment-2026-10-23.md:19-22`: 4 phrase evaluations, all
  `negated=False`. Hits: `archived`, `date`, and `claim` ×3.
  - `:19` "it is an archived copy rather than a revision id" asserts the span's sense (`An archive.org
    link for the source url`). TRUE NEGATIVE.
  - `:20` "The date is a claim property": the "not read it" later in the bullet is more than 3 words from any hit.
    TRUE NEGATIVE; the bullet keeps the span's polarity.
- m45, `evidence-snapshot-coverage-r40.md:20-21`: 7 figure evaluations (P3). Every key is
  positive-polarity: `evidence_nonempty`, `evidence_with_field`, `claims_nonempty`, `claims_with_field`,
  `claims_empty`, `real_source_answers`, `filled_web_archive`. No negator in the next 4 words; for example `5,959` is followed by
  "carry a web archive". TRUE NEGATIVE.
- Rule P1 (a phrase its span negates) was **never exercised** by the real corpus. No grounded phrase in it
  sits in a negating span. Only the r47 fixtures cover P1.

## Falsifiers on corpus text (copies in /tmp; one edit each)

| mutation | round-46 tool | landed tool |
|---|---|---|
| mutA (P2): amendment `:19` "it is an archived copy rather than" -> "it is not an archived copy but" | exit 0 PASS | exit 1 `INF_POLARITY_FLIP bullet=1 token='An archive.org link for the source url / archived'` |
| mutD (P3): snapshot `:21` add "1,968 answers carry a key field;" (1,968 = `answers_without_key`) | no POLARITY line | `INF_POLARITY_FLIP bullet=2 token='1,968 / counts key answers_without_key'` |
| mutC (P3 limit): snapshot `:20` "(1,386 against 1)" -> "(1,386 records with a claim field against 1)" (1,386 = `claims_empty`) | no POLARITY line | **no POLARITY line (passes)** |

mutC is a real flip that passes. `NEG_KEY_PARTS = {"no","not","none","without"}` does not include
`empty`, so a figure from a key like `claims_empty` or `evidence_empty` (round45 `counts.json`) is
treated as positive-polarity. The rule is lexical and its key word list is frozen, so this case sits
inside the declared named limit; it is not a gap in the predicate. Recorded as an observation only. I
propose no change to the predicate, the counter, the fixtures, the floor or the target.

## Counters (verbatim)

```
$ python3 corpus/evidence/round46/c1-count.py
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=3/3
CANARY=pass
C1=PASS
exit=0
$ python3 corpus/evidence/round47/c1-count.py
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=3/3
CANARY=pass
R46_COUNTER=pass
R46_ENTRIES=2/2
C1=PASS
exit=0
```

## Commands run (decisive output)

1. `git show 9a9f94db:tools/inference-ground.py > /tmp/chousa-r47-ExecC1Regress/ig46.py` -> exit 0.
2. Sweep loop over 61 files × 2 tools × 2 manifest sets -> `2 0->0 1->1`, `59 1->1 1->1`; `CHANGED:` empty;
   `POLARITY:` empty. Per-file `cmp` of t46 vs t47 outputs: no DIFF lines.
3. `cat out/*.t46.txt | sha256sum` and `cat out/*.t47.txt | sha256sum` -> both `222038d2…70ad5`.
4. Trace harness (importlib on landed tool, wrapping the probe functions) on the 3 reachable entries.
   The 17 evaluations listed above all returned `flips=[]` / `flip=False`, and each run's exit code matched the sweep.
5. Mutations mutA, mutC and mutD, as in the falsifier table.
6. Both counters, as above.

## Risks / blockers

- Coverage: the corpus test exercises P2 (10 evaluations) and P3 (7 evaluations). P1 gets 0 evaluations on real
  text, so its precision on the lane corpus is unmeasured. Its regression risk is also currently nil, because
  no entry reaches it.
- m45 is an older manifest. Under it the two evidence-pool entries exit 1 with both tools (TOKEN_NOT_IN_SPAN).
  That is not a probe effect, because the outputs are identical.
- No blockers.
