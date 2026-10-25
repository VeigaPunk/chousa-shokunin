# W2 ScribeLog — round-49 LOG entry, verified against artifacts

Seat: scribe (leaf). Scope: draft the round-49 entry for `LOG.md` in the round-48
shape and check every figure it states against the lane tree at
`87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0` (tracked bytes equal
`4ce61fc59e30b9215514841fe658e96cc998d138`).
Freshness: unchanged — L0 `8d77e6c1` open, so the newest capture the lane may read stays at 2026-10-25; nothing fetched.
No production file written; scratch `/dev/shm/chousa-r49-ScribeLog` deleted.

## Evidence (commands run in the lane checkout, `TMPDIR=/dev/shm/chousa-r49-ScribeLog`)

```
$ python3 corpus/evidence/round49/c1-count.py
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=4b995dbc2e950613a632c83dba068e932396c1cf1d6a44dc1255f1c4f04abc32
SET_A ... BY_DOC=9/9 REWRITE=2/2 SHAPE=9/9 URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> PASS
SET_B ... BY_DOC=3/3 REWRITE=1/1 ... -> PASS
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 ... -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3 / C1=PASS / exit=0

$ python3 corpus/evidence/round49/c2-count.py
ENTRIES=2/2  BOUND=8/9 (min 7) REFUSED=1  REF_ID_UNBOUND=0
QUOTE_ROWS=28 ON_BOUND=28/28  SPAN_IDS=8/8  QUOTES_IN_SPAN=28/28  QUOTES_IN_ENTRY=28/28
QUOTES_IN_LESSON=28/28  QUOTE_SHORT=28/28  SPAN_CONTEXT=28/28  CAPTURE_BOUND=28/28
ANCHOR_BOUND=8/8  INFERENCE_GROUNDED=2/2  QUARANTINE_VERDICTS=5/5 (S082,S084,S086,S095,S096)
C2=PASS / exit=0

$ python3 corpus/evidence/round49/build-spans.py --check      → SPANS_ROWS=28 STALE=0 / exit=0
$ python3 corpus/evidence/round49/quote-substance-check.py    → IDS=8 QUOTES=28 FAILURES=0 / exit=0
$ python3 corpus/evidence/round49/a05-check.py
CORRECTED round-47-verifier-spotcheck.md:29 / CORRECTED round-48.md:34
A05_PROPAGATIONS=2 CORRECTED=2 / exit=0

$ # a05 before-leg: freeze-rev lessons + tip checker in a scratch root
$ git archive fe740e78 corpus/lessons | tar -x -C $S; cp corpus/evidence/round49/a05-check.py $S/corpus/evidence/round49/
$ python3 $S/corpus/evidence/round49/a05-check.py
UNCORRECTED round-47-verifier-spotcheck.md:29 / UNCORRECTED round-48.md:34
A05_PROPAGATIONS=2 CORRECTED=0 / exit=1

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
file W04 S051 / S053 / S073 / S074 / S075 duplicate url ... ; file ok .../corpus/SOURCES.md ; exit=0
$ git show 414a2ec6:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3}'   → 95
$ grep -cE '^\| *S[0-9]{3}' corpus/SOURCES.md                      → 103
$ grep -E '^\| *S(09[6-9]|10[0-3]) ' corpus/SOURCES.md | awk -F'|' '{gsub(/ /,"",$5);print $2,$5}'
 S096A S097A S098A S099B S100B S101B S102B S103B
$ comm -12 <(sort .ufo/.../assimilation/reg-ids) <(sort .../staged-ids) → 14 lines S082..S095
$ cat .ufo/.../assimilation/guard-proof/{collisions,collisions-col0} → "S002" / (empty)
$ wc -l corpus/evidence/round49/{spans.tsv,quotes.tsv} → 29 / 29  (28 data rows each)
$ git diff 414a2ec6 1254ab26 -- corpus/SOURCES.md | grep -c '^-[^-]' → 0 ; '^+[^+]' → 9
$ python3 corpus/evidence/round49/capture-age-check.py .../.ufo/reports/round-48/chousa.md
FRESHNESS_CAPTURE_AGE=FAIL / exit=1        (QUALITY 71 "shown able to fail" leg holds)
$ python3 corpus/evidence/round47/c2-count.py --list | tail -3 → REGISTERED=104/104 MISMATCHES=0 C2=PASS
$ git log -1 --format=%ci fe740e78 17:02:34 / 65940928 17:03:37 / 1254ab26 17:20:44 / 4ce61fc5 17:25:34
$ ls -l .ufo/waves/round-49/w1.ready.dispatched → 2026-10-25_17:07:55   (freeze precedes the wave)
$ git status --short → only ` M LOG.md` plus untracked wave files: the three R40/R41 JSON paths are clean
$ ls .ufo/waves/round-49/inherited/ → 3 *.diff files, committed in fe740e78
$ w1/swarm-registry.json members=40 roles {scribe 17, executor 9, reviewer 4, critic 4, mutation-tester 2,
  connector 2, scout 2}; reports on disk 38 (missing ScoutCoverage, ScoutInherited)
$ w2/swarm-registry.json members=35 roles {executor 16, scribe 5, critic 4, mutation-tester 3, reviewer 3,
  connector 2, simplifier 1, scout 1}; reports on disk 5 (wave in flight)
$ grep -c "0 bytes free" .ufo/waves/round-49/{w2-spec.json,w2-dispatch.json} → 1 / 1  (seat briefs only)
$ df -B1 /tmp → 105990909952 bytes free at draft time
$ python3 corpus/evidence/round49/capture-age-check.py .ufo/waves/round-49/w2/ScribeLog.md
FRESHNESS_CAPTURE_AGE=PASS / exit=0        (after the freshness line was made single-line; FAIL before)
```

## Draft round-49 entry (report text only; `LOG.md` untouched by this seat)

## Round 49 — 2026-10-25 (first package adoption under addendum section 10; derived-index theme; section-10 adopter)

Claims froze in `corpus/evidence/round49/claims.md` at `fe740e7838b338d17fec9338c909557e6e7fed7d` (17:02:34, before the W1 dispatch at 17:07:55) after scoring both do-nothing controls (`controls/c1-before.txt`: `TOOL=absent C1=FAIL`; `controls/copy-tool.py` `SETS_PASS=0/3 C1=FAIL`; `controls/c2-before.txt`: lane `ENTRIES=0/2 C2=FAIL`, staged copy `REF_ID_UNBOUND=11 C2=FAIL`). Tool candidate `65940928cc9332b386bcbca92571451cc4374cbe`; adoption `1254ab262b2fbc199923345d389f85d0debbef6e`; tool fixes from W1 `ReviewToolCode` (tab headings, calendar-valid dates, non-UTF-8) `4ce61fc59e30b9215514841fe658e96cc998d138`; after-measurement `corpus/evidence/round49/measure-after.txt` (`87e93353`). No fetch; L0 `8d77e6c1` open.

- **C1 operability (capability)**: `tools/assimilate-rows.py` (sha256 `4b995dbc…`) — section-10 adopter (by-document renumbering with one simultaneous substitution, census-schema rows, 0–3-space collision report). `python3 corpus/evidence/round49/c1-count.py` → `SETS_PASS=3/3`, `GUARD COLLISIONS=['S002'] -> PASS`, `PIPE CELLS=11 … -> PASS`, `C1=PASS` exit 0. Named limit (W1 `CritForgeC1`, QUALITY 72): a replay of the tool's outputs on the frozen inputs also passes; the perturbed-package probes are non-frozen supplementary evidence.
- **C2 depth (sourced)**: `corpus/knowledge/aggregator-vs-source-r36.md` (85 lines, S096–S099) and `citation-count-semantics-r37.md` (79 lines, S100–S103) adopted by document; eight rows S096–S103 (A +3, B +5), zero existing rows changed; staged S091 NCPSSD homepage refused (`lessons/round-49.md:131`); 28 quote rows in `corpus/evidence/round49/spans.tsv`. `python3 corpus/evidence/round49/c2-count.py` → `BOUND=8/9 REFUSED=1 … CAPTURE_BOUND=28/28 ANCHOR_BOUND=8/8 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=5/5 C2=PASS`. Post-freeze `build-spans.py` change disclosed in `claims-erratum.md` (bare CR in the two UTF-16LE `.doc` spans; `CAPTURE_BOUND` was 21/28 before it).
- **Frontier / SOURCES**: registry 95 → 103, no existing row touched; `sources-census.sh validate --file corpus/SOURCES.md` exit 0 with the five pre-existing W04 (S051, S053, S073, S074, S075); search-log Round 49 entry in the `## Search log` section. Section-10 collision check: 14 ids S082–S095 (`comm -12`), guard proof S002 present under the 0–3-space pattern and absent at column zero.
- **Corrections / quality**: a05 propagations — freeze-rev lessons with the tip checker → `CORRECTED=0`, exit 1; lane tip → `CORRECTED round-47-verifier-spotcheck.md:29`, `CORRECTED round-48.md:34`, exit 0 (the checker itself landed with the corrections). QUALITY 69 round-49 note, 71 (capture-age line, `considerthese/2026-10-25.md:55-56`), 72 (substance floor / perturbed-input leg); criterion 69's pointer note is written but its attribution line at `QUALITY.md:712` still names "round-48.md Mistake 4". `SKILL.md` Gates +2 rows; round-47 registry `REGISTERED=104/104`.
- **Inherited**: the three R40/R41 JSON leftovers reverted to committed bytes (clean in `git status`); pre-revert diffs committed at the freeze commit in `.ufo/waves/round-49/inherited/`; the round-48 QUALITY 69 sentence landed (QUALITY diff +35 lines at `1254ab2`).
- **Waves**: W1 registry 40 seats (scribe 17, executor 9, reviewer 4, critic 4, mutation-tester 2, connector 2, scout 2), 38 reports landed (ScoutCoverage, ScoutInherited outstanding); W2 registry 35 seats (executor 16, scribe 5, critic 4, mutation-tester 3, reviewer 3, connector 2, simplifier 1, scout 1), 5 reports landed (wave in flight). L1 held the planner seat. `/tmp` exhaustion is recorded only in the W2 seat briefs ("0 bytes free"); no receipt measured it and `/tmp` holds 105.99 GB free at draft time. No tool installs.

## Findings on the earlier in-tree draft (`LOG.md` working copy, uncommitted)

1. **Pointer fix is a note, not a repair.** `QUALITY.md:710-711` says the round-48 lesson has no `Mistake 4`, yet `QUALITY.md:712` still ends the criterion with "— `corpus/lessons/round-48.md` Mistake 4; S095." The draft's phrase "pointer fix" overstates it.
2. **Census flag.** The draft says `validate --root`; the script's interface is `validate --file PATH` (`scripts/sources-census.sh:8`). `validate --root` is not a valid invocation — `corpus/evidence/round25-sources-census.sh` rejects it (`cd: validate: No such file or directory`, exit 1).
3. **W1 seat vs report count.** 40 is the registry count; 38 reports exist. Both scouts were still running when this seat read the tree.
4. **W2 count is registry-only** (35 seats, 5 reports) — must be labelled as such while the wave runs.
5. **`/tmp` incident has no measurement receipt.** The only record is the seat brief text; the host now reports 105.99 GB free, so the entry should cite the brief and the current state, not state the condition as standing.
6. **a05 before-leg is a reconstruction**: `a05-check.py` did not exist at the freeze commit (first appears in `1254ab2`), so "exit 1 → 0" is reproducible from freeze bytes but was not recorded at freeze.

## Out of scope / limits

No product file, counter, predicate or target touched. C1 mechanism probing beyond the frozen inputs
(perturbed packages) belongs to the W2 executor seats; I did not run them and claim nothing about them.
No campaign tool from `shokuknow` was run; no network; no install.

VERDICT: round-49 LOG entry draft (all stated figures against lane artifacts) — holds with corrections — every quantitative claim I re-ran reproduces (C1=PASS 3/3, C2=PASS 8/9 + 28/28, 95→103, 14 collisions, 40/35 seat splits, a05 1→0), but the draft must state the census flag as `--file`, split registry seats from landed reports, cite the `/tmp` claim to the seat briefs only, and drop "pointer fix" for QUALITY 69 while `QUALITY.md:712` still cites the nonexistent Mistake 4.
