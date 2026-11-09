# R97MutantsC1 — mutation probe of C1 beyond its 30 named sites

Seat `R97MutantsC1`, lane chousa round 97. Tree attacked: freeze `F =
9a0ce2015fa0254848f2f32f612b20caf7dc5478` (scratch clone at
`/fast/scratch/hyaku/chousa-r97/R97MutantsC1/repo`, created with the prescribed
`git clone -q --shared` + checkout; `git rev-parse HEAD` verified equal to F
before any probe). Scratch will be deleted before yield.

**Axes:** (A) claim-sentence coverage — where does the C1 sentence say more than
the 47 cases enforce; (B) sentence-veracity — does any survivor falsify a C1
sentence as worded (named limits (a)(b) are part of the claim).

**Method.** 37 new one-site mutants of `tools/search-rerun.py` at F (probe
script: `.ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt`, full output:
`.ufo/waves/round-97/w1/R97MutantsC1-mutprobe-out.txt`). None shares an
(old, new) pair — nor even an old-site — with the 30 named mutants (28 from
`.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt` + 2 Sentinel `git_env`
pairs + exclusions n08/n30); verified by an automated cross-check
(`named30=30 mine=37 PAIR COLLISIONS: [] OLD-SITE COLLISIONS: []`). Each mutant
applied exactly once; then `--selftest` with the frozen battery's `killed()`
rule (exit 1 + `SEARCH_RERUN_SELFTEST: FAIL` + no traceback). Every survivor
was then run through the round-95 battery
`python3 -B corpus/evidence/round95/rerun-controls-r95.py --root $S/repo --
work $S/w --tool <mutant>`; covered = battery FAIL, uncovered = PASS.

Self-test baseline at F: exit 0, last line
`SEARCH_RERUN_SELFTEST: PASS cases=47/47` (reproduced before probing).

## Headline

- **KILLED by the self-test: 12/37** (`g06,g07,p08,p10,p11,m01,m02,m04,e03,e04,
  e05,v02`).
- **Survived the self-test: 25/37.** Of those: 6 covered by the round-95
  battery (`m03,e01,e02,u01,u06,u07` — all user-visible through `verify`);
  **19 uncovered outright**; 1 (`m05`) shown equivalent on str inputs but
  diverging on non-ASCII paths (details below) — counted among the 19
  uncovered because the divergence is real, see m05.
- Equivalences that fully exonerate a mutant (semantic no-op under all
  inputs): **0 of 37**. Strongest near-miss: none.

## Survivors, classified

Format: name (site) — selftest / r95 / class — witness.

**Guard mutants (named limit (b) owns — outside the 30).** All 5 survived the
self-test and the r95 battery and are **uncovered**:
- `g01-case-always-true` (`results.append((cid, bool(ok)))` → `True`), `g02-
  case-setup-only` (`except Exception` → `except Setup`), `g03-case-count-all`
  (`k=n` always), `g04-summary-always-pass` (`FAIL` → `PASS` in summary),
  `g05-selftest-return-0` (`return 0`). They score `--selftest` rc=0 and the
  r95 battery `RERUN_CONTROLS=PASS` (the r95 battery never runs `--selftest`;
  no oracle exists in the r97 battery either). **Class: uncovered, excepted by
  named limit (b).** Consequence: the sentence "each [case] inside a guard
  that turns an exception raised inside the case into that case's FAIL" is
  enforced by no external oracle — it is a statement about the code, not a
  checked invariant. A reader who trusts the guard could regress `g02` and
  every future crash-with-ValueError case would traceback out of the run
  (no summary line) — precisely round-96 class B — with no instrument
  complaining. (b) admits this; it is nonetheless a *coverage finding*.

**Parse-loosening mutants (named limit (a) owns — "fresh mutant elsewhere may
survive").** 9 survived both, all **uncovered**, each with a concrete
user-visible witness (verified by building the witnessing record and running
`parse_text` in both pristine and mutant):
- `p01-cells-no-endpipe` — a row missing its trailing `|` parses OK instead
  of `Setup:ROW`. Witness: `ST_HEAD + st_row().rstrip().rstrip('|') + '\n'` →
  base `Setup:ROW`, mutant `OK`.
- `p02-heading-contains` (`== "## Searches"` → `in`) — heading
  `## Searches catalog` accepted instead of `Setup:SECTION`. Witness above.
- `p03-double-section` (`len(starts) != 1` → `not starts`) — two `## Searches`
  sections accepted. Witness above.
- `p04-separator-2dash` (`-{3,}` → `-{2,}`) — `|--|--|…` separator accepted
  instead of `Setup:TABLE`. Witness: 2-dash separator → base `Setup:TABLE`,
  mutant `OK`.
- `p05-hitset-dash-path` (`elif hs and hs != "-"` → `elif hs`) — `hits=2,
  hit_set=-` accepted as path list `['-']` instead of `Setup:HIT_SET`.
  Witness verified.
- `p06-where-dot-segment` (dropped `"." in parts`) — `where=.` accepted
  instead of `Setup:WHERE`. Witness verified.
- `p07-expr-no-end-backtick` (dropped `endswith("`")`) — `` `abc `` (no
  closing backtick) accepted instead of `Setup:EXPRESSION`. Witness verified.
- `p09-posix-lower` (`[A-Za-z]` → `[a-z]`) — regex `expr='[[:ALPHA:]]+'`
  accepted instead of `Setup:EXPRESSION`; Python then reads it as a nested-set
  char class (different meaning) — silent semantic shift.
- `m03-hit-fixed-startswith` (`needle in line` → `startswith`) — survives
  self-test, **covered by r95** (`CASE positive rc=1` FAIL); user-visible.
- `m05-digest-str-sort` (bytes-sort → str-sort of paths) — **uncovered**.
  Equivalence check: identical on single-byte strings, but *divergent on
  multi-codepoint/non-ASCII and surrogateescape paths*: fuzz found
  `['\udca8ǎIĩ.txt', 'ȑƾ\udcc2\udcf1Ŗ.txt', 'ƎɵÿȤ.txt']` → base
  `a5bcf956…` vs mutant `2bd8cee4…`. The `digest()` docstring explicitly
  claims the surrogateescape-correct byte sort; this mutant breaches it for
  non-ASCII/non-UTF-8 paths while both m06 (ASCII names only) and the r95
  fixtures (ASCII captures only) stay blind.

**evaluate mutants.** `e01-rev-token-swap` (rev=MATCH/DRIFT strings swapped)
survives the self-test (selftest `judge()` reads only index 7 of the line)
but **covered by r95** (`strict-tree` CASE FAIL — r95 consumes the token).
`e02-count-lt` (`!=` → `<`) survives the self-test but **covered by r95**
(`f5-zero` wants `{COUNT_DRIFT, SET_DRIFT}`, mutant gives `{SET_DRIFT}`).

**git_env mutant.** `v01-env-git-prefix` (`GIT_` → `GIT`) **uncovered**:
selftest `r13-env-guards` plants only `GIT_*` variables, so the stranded-`GIT`
key set is identical; a caller exporting any `GIT`-prefixed non-`GIT_`
variable (e.g. `GITFOO=1`) has it silently dropped by the mutant and passed
through by the base (verified: base keeps `GITFOO`, mutant drops it). No
instrument sets such a variable.

**Git/disk-reader mutants (named limit (c) owns — "self-test does not exercise
the git and disk readers").** 5 survived both, all **uncovered**:
- `u02-run-at-rev-tops-0` (`tops` → `tops[0]`) — a record with two globs in
  distinct static dirs (`a/*.txt, b/*.txt`) loses `b/` from the at-rev read.
  r95 fixture rows all share static dir `corpus/captures`. Witness:
  `tops=(('a/',), ('b/',))` vs mutant `tops[0]='a/'`.
- `u03-blob-silent` (blob read error → silent empty bytes) — verified:
  `blob(…, 'deadbeef'*5)` → base `Setup:REV unreadable`, mutant
  `RECEIVED b''` (a missing blob silently scores as an empty file instead of
  a setup error — the exact promisor-fetch failure mode the tool exists to
  refuse).
- `u04-static-dir-bracket` (wildcard set `*?[` → `*?`) — `static_dir('a[b]/
  c.txt')`: base `''`, mutant `'a[b]'` (verified). A bracket segment above
  the glob pattern escapes the static-dir pruning; no case or fixture uses
  brackets.
- `u05-tree-files-jj` (`.jj` unpruned) — `.jj` files leak into the tree scan.
  Scratch clone has no `.jj`, so the r95 CLONE_TREE leg cannot see it.
- `u01-verify-return-0`, `u06-git-timeout-0`, `u07-record-exists-refused` —
  not reader-only; **covered by r95** (`strict-tree`/`positive`/`f1` CASE
  FAIL).

## Does any survivor make a C1 sentence false as worded?

Read with limits (a)(b)(c) as part of the claim (they are printed under the
claim): **no firing sentence.** Every uncovered survivor falls in a class the
claim itself fences off — (a) parse/evaluate/matching sites, (b) guard/summary
machinery, (c) git/disk readers. K1/K2/K3 are not met: all 30 named mutants
remain killed (untouched by my probe), nothing in the 30 is re-scored here,
and no survivor is a stand-in or a named external. But three of the uncovered
survivors are *worse than* limit-(a) suggests, and worth the lane's attention:

1. **The guard is unobserved in both directions.** `g01`–`g05` show the
   self-test's verdict line, case count, and exit code can all be corrupted
   with *no* instrument in the tree noticing (the r97 battery never calls
   `--selftest` on a guard-corrupted tool, and the r95 battery never calls
   `--selftest` at all). The claim's central sentence — "each inside a guard
   that turns an exception … into that case's FAIL" — is exactly the surface
   nobody checks. Limit (b) names the exclusion; the exclusion is doing a lot
   of work.
2. **`u03-blob-silent` breaks the tool's own refusal contract** ("a partial
   clone's missing blob is a setup error, not a network fetch" — tool
   docstring) with a stack trace-free silent wrong answer, invisible to r95.
3. **`p04/p05/p06/p07` are interview candidates for `Setup` regressions** the
   r95 SETUP leg enumerates (12 malformed records) but only for its 12 chosen
   malformations; these six new shapes of "malformed record" pass the whole
   instrument stack and then either silently evaluate or crash later.

## Equipment

No tooling installed (system Python 3.14, GNU grep not needed). Probe ran
1011s wall time under `/fast/scratch/hyaku/chousa-r97/R97MutantsC1/`; scratch
deleted before yield per seat spec. Counts: 37 mutants probed, 12 killed, 6
covered-by-r95, 19 uncovered, 0 equivalent.

No production source modified; only `.ufo/waves/round-97/w1/` files written
(this report, `R97MutantsC1-mutprobe.py.txt`, `R97MutantsC1-mutprobe-out.txt`).

VERDICT: R97MutantsC1 C1 held — none of 37 new mutants makes a C1 sentence false as worded under its named limits, but 19 uncovered survivors (including the fully-unobserved guard machinery) are coverage findings the lane should see.
VERDICT: R97MutantsC1 C2 n/a — probe touched only tools/search-rerun.py behaviour, not the C2 entry or its sources.
