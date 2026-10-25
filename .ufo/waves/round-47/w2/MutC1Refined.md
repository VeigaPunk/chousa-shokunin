ATTACKS: mutation-test the round-47 C1 REFINEMENTS of tools/inference-ground.py @ 980fe43 (one /tmp mutant per refinement), scored with the frozen corpus/evidence/round47/c1-count.py
VERDICT: holds — pristine tool scores C1=PASS; but the frozen counter KILLS only 2 of 7 refinement mutants (c, d, via R46_ENTRIES); 5 survive (a, b, e, f, g) ⇒ the pinned six-fixture set does not exercise 5 of 7 refinements (coverage defect in the frozen counter, not in the tool). Every survivor has a minimal /tmp killer; each SHOULD have been killed by the frozen counter given a fixture exercising the refinement it documents.

All runs: pristine = git show 980fe43:tools/inference-ground.py (sha256 244a1897feec49a5a08625a0ca8d0cb3c490675678badeb3ee23d97a4329667e); mutants in /tmp/chousa-r47w2-MutC1Refined/mutants/ (hashes below). No tool installs; no pacman.

== 1. Baseline (pristine) — frozen counter ==
$ python3 corpus/evidence/round47/c1-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --tool <pristine>
TOOL=present
POSITIVE_PASS=3/3
JUNK_KILLED=3/3
CANARY=pass
R46_COUNTER=pass
R46_ENTRIES=2/2
C1=PASS
exit=0

== 2. Seven mutants, scored by the SAME frozen counter ==
mut-a IMPLICIT_NEG emptied (tools/inference-ground.py:253 -> `IMPLICIT_NEG = set()`; 0b400d8f…a53c2):
  TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0  -> SURVIVED
mut-b UN_NEG_RE never matches (line 254 -> re.compile(r"(?!)"); 05315aa6…a2c0):
  identical all legs PASS -> SURVIVED
mut-c clause-bounded look-back -> plain last-3-words (line 286 `before = re.split(r"[\n.;:()]", s[:idx])[-1]` -> `before = s[:idx]`; 4030623a…004fd):
  R46_ENTRIES=1/2 C1=FAIL exit=1 -> KILLED
mut-d phrase_polarity back to first-span-only (lines 290-305 -> a15610a implementation; 6a741457…82b0):
  R46_ENTRIES=1/2 C1=FAIL exit=1 -> KILLED
mut-e figure_flip first occurrence only (lines 391-395 -> next(finditer) break; 08328313…2d):
  identical all legs PASS -> SURVIVED
mut-f key_negated leaf-key only (line 377 -> leaf = path.rsplit("/",1)[-1]; 23a828dd…fda2):
  identical all legs PASS -> SURVIVED
mut-g `un`-prefix flip removed (lines 327-330 deleted; 3f9c0999…e8e8):
  identical all legs PASS -> SURVIVED

== 3. Kill mechanism for c/d (round-46 entry regression) ==
Counter leg = `python3 <mutant> --entry <r39 entry> --spans corpus/evidence/round46/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root <lane> --quiet`.
mut-c and mut-d both fail the BASE entry corpus/knowledge/evidence-pool-versioning-r39.md (rc 1), pass the amendment (rc 0) => R46_ENTRIES=1/2.
Verbose (mut-c): GROUND entry=...r39.md section=1 bullets=4 tokens=7 grounded=7
FINDING INF_POLARITY_FLIP bullet=1 token='Pre-processed Wikipedia Pages (June 2017 dump) / pages'
GROUND: FAIL exit=1
Root cause: corpus/evidence/round46/spans/S085-2.txt line 5 renders ` Pre-processed Wikipedia Pages (June 2017 dump) ` on its own line, preceded by line 3 ` Shared Task Blind Test Dataset (Unlabelled) `. `is_neg("unlabelled")` is True (UN_NEG_RE: un+labell+ed); pristine's clause split ([\n.;:()]) discards the previous line so the phrase reads affirmed; the mutants' plain look-back takes the last 3 words of the whole preceding text -> "unlabelled" -> negated -> bullet 1's "pages" (no negator within +-3) flips. So R46_ENTRIES legitimately pins refinements (c) and (d).

== 4. Survivor killer fixtures (each minimal; pristine vs mutant on the counter's exact leg shape) ==
All under /tmp/chousa-r47w2-MutC1Refined/killers/<k>/ (hashes below; command: python3 <tool> --entry entry.md --spans spans.tsv --counts counts.json --root <k>).

killer a_implicit_neg (junk; sha: entry b8ba15e9…c930, spans.tsv 6cc86213…c9d, spans/S901-1.txt 03c87953…4c8):
  spans/S901-1.txt: "the release lacks a frozen pool of cargo"
  bullet: Because `a frozen pool` is shipped, the pool is frozen at release (S901)
  pristine: FINDING INF_POLARITY_FLIP 'a frozen pool / pool' + '/ frozen' -> exit 1
  mut-a:  GROUND: PASS -> exit 0   [mutant misses "lacks"]

killer b_un_neg_re (junk; sha: entry 621fd3a5…ea3, spans.tsv 1d3d6b99…6907, S901-1.txt 61acb958…257):
  spans/S901-1.txt: "untraceable, the archive link appears"
  bullet: The manifest archives `the archive link` and keeps it (S901)
  pristine: FINDING INF_POLARITY_FLIP 'the archive link / archives' -> exit 1
  mut-b:  GROUND: PASS -> exit 0   [mutant misses "untraceable"]

killer e_figure_first_occurrence (junk; sha: entry 0a418784…e58, spans.tsv a77064f6…1c, S902-1.txt c57b2703…5a59, counts.json fa2382c6…3a3):
  counts.json {"figures":{"answers_without_archive_key":1582}}; span has no digits (so figure grounds via counts leg)
  bullet: 1,582 sourced answers carry no archive key, and 1,582 answers feed the corpus count (S902)
  pristine: FINDING INF_POLARITY_FLIP '1,582 / counts key figures/answers_without_archive_key' (x2) -> exit 1
  mut-e:  GROUND: PASS -> exit 0   [second occurrence unchecked]

killer f_key_leaf_only (positive; sha: entry 3f2bcbde…af5, spans.tsv e0ed1a50…fe, S902-1.txt e4ff2102…1d6c, counts.json 0ebb4fc0…c74):
  counts.json {"without_archive":{"count":1582}} (negation only on ancestor key)
  bullet: 1,582 records carry no archive bucket, so they are unbound (S902)
  pristine: GROUND: PASS -> exit 0
  mut-f:  FINDING INF_POLARITY_FLIP '1,582 / counts key without_archive/count' -> exit 1   [leaf-only misreads key as affirmative]

killer g_un_prefix_flip (junk; sha: entry b2b9753b…50, spans.tsv 37199e9a…680, S901-1.txt 78057723…5e5):
  spans/S901-1.txt: "the release ships a frozen pool"
  bullet: Because `a frozen pool` is unfrozen at release, it drifts (S901)
  pristine: FINDING INF_POLARITY_FLIP 'a frozen pool / unfrozen' -> exit 1
  mut-g:  GROUND: PASS -> exit 0   [un- form ignored]

== 5. Should the frozen counter have killed the survivors? ==
YES for all five. c1-count.py's docstring declares the predicate is "the same sentence as claims.md", whose round-47 refinements paragraph names each behavior: implicit negators (`lacks`, `absent`, `un…able`/`un…ed`) -> a/b; every figure occurrence at digit boundaries -> e; key-path parts incl. any ancestor key -> f; `un`-prefixed flip -> g. The counter's scoring legs, however, only read six pinned fixtures (POSITIVES/JUNKS, corpus/fixtures/inference-ground-r47/) + R46 entries, none of which contain an implicit negator, an un- negator, a repeated figure, a nested counts key, or an un- flip. So each survivor is a pure coverage gap: had any of the killer fixtures above been part of the pinned set, the same code would print JUNK_KILLED=2/3 or POSITIVE_PASS=2/3 and C1=FAIL (its `killed()`/pos legs are exactly the commands run in section 4). The frozen counter does not, therefore, pin five of the seven refinements; the C1=PASS claim holds only for the tool as frozen.

Mutant hashes: a 0b400d8f9a242e645733a946023eb1556db16b7e42a12cf5a10ab62e679a53c2; b 05315aa6af5b299565dffaad36dbafd7a4f1f19759822b9505e96cbaafb3a2c0; c 4030623a7fd366ff6c6b8739f13fde6a82fc4eb1d583f7955954d9bb09b004fd; d 6a74145746a929829958bb9bc0a0e7201d38ad2ddd745c19be8dcf92a44682b0; e 083283132941e9ff8447cb694b388b42ecc4dafca345e206e9fd51dfabd7932d; f 23a828dd7f513ec047b9bf59e0b03012fcf8231ab8d790262b0381283348fda2; g 3f9c0999e6b232a5fbca21221f77f6ffe6629ccb28a6e2d8bce75ae737e976e8. Pristine 244a1897feec49a5a08625a0ca8d0cb3c490675678badeb3ee23d97a4329667e (== git show 980fe43:tools/inference-ground.py). Killer fixture hashes: list in section 4. Scratch /tmp/chousa-r47w2-MutC1Refined/ removed on completion; no lane files modified (no git/jj mutations; lane git status untouched apart from pre-existing untracked w2 files).
