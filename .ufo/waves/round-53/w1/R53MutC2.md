# R53MutC2 — C2 counter mutation test (round 53, wave 1)

Seat: `R53MutC2` (mutation tester, `/skill:godspeed`). Target: the FROZEN claim **R53-C2**
(`corpus/evidence/round53/claims.md`), counted by `corpus/evidence/round53/c2-count.py`.
No lane file was written; the only write here is this report. All fixtures lived under
`/fast/scratch/hyaku/chousa-r53/R53MutC2/` and were removed at the end.

## Instruments (copied, not edited)

- `c2-count.py` → scratch `…/ev` and every fixture release; sha256 `15fa85a5002027a73b03de5d406947f8f8dfd8935c5e896fa6169214da9402df` (lane == scratch == restored-after-mutation).
- `build-spans.py` → same; sha256 `0de9d32dca855cb34812d5c9443a88791df61183fa69d4e0bd1683bfebe7b341`.
- `tools/` (inference-ground.py incl.) and `corpus/evidence/round51/quote-substance-check.py` copied into each fixture.
- The counter's two `BASE_REV` git queries got a scratch fixture repo with `refs/replace/5b550133d79bc09c82d8965cce2e48c2598b8c3e` → a pre-round-53 commit (`corpus/SOURCES.md` registry = S001/S002 only; `corpus/knowledge` term-free), verified by `git show`/`git grep -l …` (rc 1). `TMPDIR` set to scratch for every run.

## Fixtures

Quotes are single whole lines of the `.txt` captures (byte-exact, each occurs exactly once,
≤160 chars, ≤25 whitespace words; Chinese lines ≤160 chars): JMLA S117, Cochrane S121, QCG PDF S118
(base); QCG notice S119 and NMPA copy S120 (m1–m3). Entries carry `source: S### — <url>`,
their NEW_GROUND term, the quotes, and a `#### Inference` section whose backticked tokens are
span substrings; `build-spans.py` built `spans.tsv` + spans, anchors were spliced from the printed
`QUOTE <id> char N` values.

Base fixture (3 entries, bound S117/S118/S121, refused notice+NMPA): pristine counter output

```
ENTRIES=3/3 (min 2) REFUSED_ENTRIES=0    BOUND=3/5 (min 3) REFUSED=2
BOUND_IDS=S117,S118,S121   REF_ID_UNBOUND=0   NEW_GROUND=3/3
QUOTE_ROWS=9 ON_BOUND=9/9   SPAN_IDS=3/3   QUOTES_IN_SPAN/ENTRY/LESSON=9/9
QUOTE_SHORT=9/9  SPAN_CONTEXT=9/9  CAPTURE_BOUND=9/9  SUBSTANCE=PASS
ANCHOR_BOUND=3/3   INFERENCE_GROUNDED=3/3   QUARANTINE_VERDICTS=0/0
C2=PASS   (exit 0)
```

Kill fixtures (each is a *plausible bad lane state*; pristine counter FAILS each on the exact
leg the mutation touches):

| fixture | deviance | pristine failing leg |
|---|---|---|
| fx-m1 | 1 entry (E_QCG) citing S118/S119/S120; E_STR/E_WIA refused-entry-named; JMLA+Cochrane refused-doc | `ENTRIES=1/3 (min 2)` |
| fx-m2 | E_WIA missing, **not** refused-entry-named; S118 used-by=E_QCG only | `REFUSED_ENTRIES=0` → 2+0≠3 |
| fx-m3 | E_WIA missing, refused-entry-named; **S118 used-by also lists E_WIA** | `BOUND=3/5 REFUSED=1` (4≠5); `REF_ID_UNBOUND=3` |
| fx-m4 | entries hold the wrong NEW_GROUND terms (each holds another's term, not its own) | `NEW_GROUND=0/3` |
| fx-m5 | S117 anchor adds a second, plausible-but-wrong `char 2365` (a S118 offset) | `ANCHOR_BOUND=2/3` |
| fx-m6 | span `S117-1.txt` tail tampered (last 40 chars → `x`), quote intact | `CAPTURE_BOUND=8/9` |

## Mutants (single smallest behavior-bearing change each; sha256 after mutation)

| # | code change | sha256 (first 16) |
|---|---|---|
| M1 | `MIN_ENTRIES = 2` → `1` | `48a06068d7a503e3` |
| M2 | `refused_entries = [p for p in ENTRIES if p not in texts and any("refused-entry" in l and p in l for l in lesson.splitlines())]` → drop the `any(...)` guard | `00a5e3b25c92fd95` |
| M3 | binding condition `used == citing` → `sorted(set(used) - set(refused_entries)) == citing` | `b505fe8806969c1c` |
| M4 | `term in texts[entry]` → `any(t in texts[entry] for t in TERMS.values())` | `00a2fd72e863523c` |
| M5 | `all(c in offsets.get(r[0], set()) for c in chars)` → `chars[0] in offsets.get(r[0], set())` | `9dfdef08ec7ff760` |
| M6 | `ft[o:o + len(span)] == span` → `ft[o:o + 16] == span[:16]` | `9ca8a9949f2e6915` |

(M3's first cut crashed (unbound `lesson`); fixed by hoisting `refused_entries` above the loop —
semantics unchanged. Real output for the final M3 is reported.)

## Kill matrix (all runs: `python3 <fixture>/corpus/evidence/round53/c2-count.py --root <fixture>`)

| mutant | on kill fixture | on base fixture | verdict |
|---|---|---|---|
| M1 | `ENTRIES=1/3 (min 1) … C2=PASS` rc 0 | `C2=PASS` rc 0 | **KILLED** |
| M2 | `REFUSED_ENTRIES=1 … C2=PASS` rc 0 | `C2=PASS` rc 0 | **KILLED** |
| M3 | `BOUND_IDS=S117,S118,S119,S120 … C2=PASS` rc 0 | `C2=PASS` rc 0 | **KILLED** |
| M4 | `NEW_GROUND=3/3 … C2=PASS` rc 0 | `C2=PASS` rc 0 | **KILLED** |
| M5 | `ANCHOR_BOUND=3/3 … C2=PASS` rc 0 | `C2=PASS` rc 0 | **KILLED** |
| M6 | `CAPTURE_BOUND=9/9 … C2=PASS` rc 0 | `C2=PASS` rc 0 | **KILLED** |

Every mutant is killed by a plausible bad lane state, and none fails the healthy base fixture.
No mutant survived all buildable inputs. (`git rev-parse --show-toplevel` asserted equal to each
fixture root before every commit; lane repo untouched throughout — counter sha in the lane repo
unchanged at `15fa85a5…`.)

## Located quotes (base fixture machine lines: `QUOTE<TAB>staged-id<TAB>url<TAB>quote<TAB>entry-path`)

```
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	       with sufficient detail to enable reproducibility. PRISMA 2020, an updated version of the PRISMA (Preferred Reporting	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	       focusing on reporting the search components of systematic reviews. Several significant changes were implemented in	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	       to report search strategies for all databases, registries, and websites that were searched. PRISMA-S also recommends	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	 Both free-text and subject headings (e.g. Medical Subject Headings (MeSH) and Emtree) should be used.	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	 specific details of the interventions (e.g. dose, frequency);	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	 For further details on this topic, please refer to Section 1.1. of the online Technical Supplement and its subsections. 	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	  药品临床综合评价是药品供应保障决策的重要技术工具。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	  一是需求分析。药政司牵头，评估中心配合开展国内药品临	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	制定过程中应注意的重点难点问题，确保质控指南贴合工作需求。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
```

Builder printed anchor offsets `S117 char 712/954/1196`, `S121 char 6806/123085/18178`,
`S118 char 2365/2944/3002`; registry anchor cells carry exactly those `char N` values.

## Restoration / cleanup

After each mutant run the fixture counter was re-copied from pristine and sha-verified equal
(`15fa85a5…`). No lane/git-index/fleet/package file was touched. Entire scratch
`/fast/scratch/hyaku/chousa-r53/R53MutC2/` removed (`rm -rf`) on completion.

VERDICT: mutated the frozen C2 counter in six ways (min-entries, refused-entry check,
used-by-set, NEW_GROUND, anchor-first-char, capture-prefix); all six mutants were killed by
plausible bad lane states and none regressed the healthy base fixture — C2's discriminating
legs hold against every buildable input.
