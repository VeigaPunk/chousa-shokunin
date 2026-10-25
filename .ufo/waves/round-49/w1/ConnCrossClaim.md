# ConnCrossClaim — round 49 w1 URL-binding cross-claim probe

Seat: ConnCrossClaim (leaf; no subagents/jobs). Read `~/.omp/agent/RULES.md` and `skill://godspeed`; no install performed. Scratch used under `/tmp/chousa-r49-ConnCrossClaim/` and removed at end. Only write: this report.

## Question and scope

Compared the URL key used by the C1 adopter and C2 counter with round-47 C3's literal substring check; checked theme URLs against lane `corpus/SOURCES.md` and staged rows. No changes to either frozen predicate or counter/control; this is a probe only.

## Commands run and observed evidence

1. Opened `tools/assimilate-rows.py:61-69`, `corpus/evidence/round49/c1-count.py:78-90`, `corpus/evidence/round49/c2-count.py:71-79`, `corpus/evidence/round47/c3-count.py:118-124`, and `scripts/sources-census.sh:600-605` (via search). C1 adopter, C1 counter, C2 counter, and census all use the same key: first URL; strip fragment and one trailing slash; drop scheme; lowercase host only. Query and path remain case-sensitive and otherwise exact. C3 instead checks `url in row[1]` after finding row by id; it performs no URL normalization.

2. Ran a local Python comparison with explicit concrete pairs. Output:

```
NCPSSD slash: norm_equal=True; c3_substring=False
case-only host: norm_equal=True; c3_substring=False
fragment stripped: norm_equal=True; c3_substring=True
query parameter differs: norm_equal=False; c3_substring=True
scheme differs: norm_equal=True; c3_substring=False
same host different help path: norm_equal=False; c3_substring=True
ZCMU query present vs absent: norm_equal=False; c3_substring=False
```

Concrete pair lines emitted by that command included:

```
staged=https://www.ncpssd.cn/ ; row=https://www.ncpssd.cn
staged=https://www.ncpssd.cn/ ; row=https://www.ncpssd.cn/service/help?mainTitle=x
staged=https://www.zcmu.edu.cn/x.doc?e=.doc ; row=https://www.zcmu.edu.cn/x.doc
```

The clearest demonstrated disagreement is the NCPSSD homepage slash pair: C1/C2's normalized equality binds; C3's substring does not. Conversely, a more dangerous false positive for substring is the NCPSSD homepage vs its `/service/help?...` page: `https://www.ncpssd.cn/` is a substring of that distinct help URL, but normalized equality rejects it. The C1/C2 normalizer retains query strings: ZCMU `?e=.doc` is not equal to the same path without that query. It does not equate NCPSSD homepage with help-page, which has another host (`ncpssd.org`) in the actual staged source evidence.

3. Parsed 95 rows from the BASE_REV registry (`git show 414a2ec6cde05a921dbdd9e02e7ae56b0db647ef:corpus/SOURCES.md` to scratch; `grep -c '^| S'` → `95`) and current registry. URL-normalized equality against all nine C2 theme URLs returned **no theme matches** in either BASE or current lane registry. Current `corpus/SOURCES.md:96` is S086, a FEVER PDF; reviewed `corpus/SOURCES.md:96-105` (S086–S095), none of which carry a theme URL. Thus no lane SOURCES.md row already carries a URL normalizing equal to a theme URL.


4. Checked adoption package rows. `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` parsed as 114 staged row-shaped lines, including staged S087/S088/S089/S091/S092/S100/S101/S102/S103. Scratch `.ufo/waves/round-49/assimilation/adopt/append.md` parsed as 9 new lane rows S096–S104. Both staged package and scratch adoption rows carry theme URLs as expected; they are not existing lane rows. The append's normalized-duplicate scan found repeated UM PDF URL only in the staged package (among prior package rows), including S105–S108; the nine scratch append rows contain no theme URL duplicates. This is an important cross-claim issue: a package-wide census is not equivalent to the frozen C2 lane-registry test.

5. Searched read-only absent-defect register for theme URLs. It contains relevant prior records for NII manual (S082), J-STAGE FAQ (S084), NCPSSD homepage (S086), ZCMU DOC (S095), and HIT DOC (S096), with prior campaign IDs; these are register records, not lane Registry rows. The absent-defect register is read by C2 for quarantine-verdict coverage; it does not itself create a lane binding.
## Contradictions / cross-surface effects

- C1 and C2 are aligned on URL identity with the census; round-47 C3 is not. They differ both ways: suffix extensions can pass substring while failing identity equality, and normalization-equivalent URLs can fail substring. These are not interchangeable evidence predicates.
- The scheme is discarded, host case folded, fragment and one final slash removed, but query retained. Thus C1/C2 deliberately conflate scheme, host case, fragment, and terminal slash while preserving query distinctions. This behavior comes from the shared census normalizer; no evidence here warrants changing a frozen predicate.
- `c2-count.py` demands exactly one lane Registry row for each normalized theme URL (`c2-count.py:138-152`). It will reject ambiguity rather than selecting one. This matters because the staged package already contains multiple historical rows normalizing to the same UM PDF URL (including staged S105–S108), although the current lane registry has none of those theme URLs. The isolated nine-row adoption append is not itself ambiguous.
- C2's source lines are exact staged URLs (`c2-count.py:145`), while the normalized row match can tolerate a scheme/host-case/fragment/slash difference. A normalized match therefore is insufficient unless the entry's exact source line also names the staged URL. C1 uses the same URL key for ID remapping; second-order consequence: package IDs may be held by normalized document identity even where textual URL forms differ, but C2 still requires source-line concordance.

## One bounded proposal

Preserve all frozen claims; add this result to the lane's C2 Gate/interpretation, not to the predicate: explicitly state that current-lane uniqueness is the relevant binding boundary, and that the staged package's pre-existing UM-PDF duplicate keys are not grounds to claim a duplicate lane binding. Cite the observed `S105–S108` package matches and the zero-match BASE/current registry scan. This prevents a package-wide duplicate scan from being mistaken for a C2 falsifier while retaining C2's exact-one-row rule on the lane registry. A second reusable note for future checks: quote both favorable disagreement directions (NCPSSD slash normalization vs literal miss; homepage-prefix substring false positive vs exact normalized mismatch) whenever comparing legacy substring checks to census-key binding.

Affected axes: improves **calibration** by distinguishing normalized identity, substring containment, and package-level repetition; supports **depth** by tracing the theme's URL identity through source registry, adoption, counter, and quarantine register. No demonstrated harm to **operability**: this is an interpretation/reporting boundary only and does not alter the adopter, counter, target, or controls.

Risks: a slash-only example is a normalization boundary, not proof that all NCPSSD paths are equivalent; the help page is a distinct host in the actual capture-adoption evidence. UM-PDF package duplicates could be substantive for other package workflows, but C2's frozen predicate binds against the lane registry, so do not transfer this finding to a different counter. No live fetch was attempted.

## Verification / cleanup

Commands actually exercised above: file reads; `git show` for BASE_REV SOURCES; `grep -c '^| S'` (95); Python URL-pair comparisons; Python parsers over BASE/current/staged/scratch Registry rows; grep of absent-defect register; scans of current registry rows. No frozen counter was run because this seat's assigned task was the URL cross-claim probe and the lane's wave owner runs the round counters. No install. Scratch cleanup command: `rm -rf /tmp/chousa-r49-ConnCrossClaim`; observed `test ! -e ...` → `scratch-removed`.

VERDICT: attacked URL-binding equivalence across C1/C2/C3 and checked for pre-existing theme bindings; found concrete normalization/substring disagreements and no theme-normalized URL in the BASE or current lane Registry, with a separate staged-package UM-PDF duplicate caveat.
