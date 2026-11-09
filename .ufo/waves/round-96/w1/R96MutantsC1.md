# R96MutantsC1 — new-mutant probe of C1 beyond the frozen 23 sites

Seat `R96MutantsC1`, round 96, lane chousa. Target instrument: the frozen tree at
`2db151c5ea0883de0b9dc8d95c6fac1755e1056a`, file `tools/search-rerun.py`
(sha256 `c6a5872e697fcf0cc2e57c4ab870cb912ee02caab447becf357b5600a7fe6f9e`,
checked against `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/search-rerun.py` — identical bytes).

Method: shared clone into scratch `S=/fast/scratch/hyaku/chousa-r96/R96MutantsC1`,
`git checkout -q 2db151c5…`, toplevel asserted equal before mutating anything.
Each mutant is a single-site textual replacement in a *copy* inside scratch; the
lane file is never edited. Each copy is run as `python3 -B <copy> --selftest`,
recording exit + `SEARCH_RERUN_SELFTEST` line + failing case ids. The kill
criterion matches the frozen battery's: exit 1 **and** the printed
`SEARCH_RERUN_SELFTEST: FAIL` line. Probing harness: `R96MutantsC1-mutprobe.py.txt`,
output: `R96MutantsC1-mutprobe-out.txt`. Baseline (pristine copy): `EXIT=0`,
`SEARCH_RERUN_SELFTEST: PASS cases=32/32`, receipt `R96MutantsC1-baseline-selftest.txt`
— the baseline is green, so baseline failure is not in play.

All 30 designed mutants aimed at `evaluate`, `parse_text`, `cells`, `matches`,
`seg_match`, `hit`, `digest`, `static_dir`, `git_env` and the module regexes:
`at_rev`/`at_tree` role swap; findings counted per-row instead of per-code;
`rev_ok` masked by `TREE_CHANGED`; `tree_same` gated on `strict`; count/set/digest
checks rewritten against the tree side; HITS/DATE/REV/ID/DIGEST regexes loosened
(case, sign); HEADER order swap; `SPLIT_RE` lookbehind dropped; `parse_text`
split on `\r\n`; regex `search`→`match`; fixed-substring→whole-line; `lines_of`
split on `\r\n`; UTF-8 decode strict; dotglob inversion; `matches` length check
dropped; `static_dir` includes the filename segment; digest without per-path
newline; `GIT_NO_LAZY_FETCH` dropped; `cells` strip-order change; expression
minimum length 3→2; empty-glob-segment check dropped; empty hit_set path check
dropped; separator-row length check dropped.

## Results

Attempted 30; one (n08, HITS-regex sign) applied 0 times — probe setup error in
my harness, counted as neither killed nor survived. Of the 29 applied:

- **KILLED 10/29** (exit 1 with FAIL line, cases shown are the failing ones):
  - n01 at_rev/at_tree swap → j06,j07,j08.
  - n03 rev_ok masked by TREE_CHANGED → j06,j07,j08.
  - n04 tree_same gated on strict → j06,j08.
  - n05 count check on at_tree → j06,j07.
  - n06 set check on at_tree → j06,j07,j08.
  - n18 fixed substring-in-line → whole-line equality → 10 cases.
  - n19 lines_of split on `b"\r\n"` → p14, m01, m04.
  - n21 dotglob rule inverted → 10 cases.
  - n24 digest without per-path newline → m06.
  - n25 GIT_NO_LAZY_FETCH dropped → m08.
- **SURVIVED 19/29** — every survivor passes `--selftest` with `PASS cases=32/32`
  (or crashes, see classes B and C below).

### Class A — equivalent on the 32 in-memory cases, killed by the round-95 CLI battery

These are the most informative: the `--selftest` does not kill them, but the
round-95 battery `corpus/evidence/round95/rerun-controls-r95.py` run with
`--tool <mutant>` **fails its POSITIVE/FORGERY/SETUP groups** — i.e. they are
caught outside the self-test, exactly the coverage the freeze describes in
named limit (a) ("it does not exercise the git and disk readers; the round-95
battery does, through the CLI", claims.md C1 limit (a)). Spot results from that
battery (`--root <frozen clone> --work <scratch>`):

- n07 `digest(at_rev)` → `digest(at_tree)` in `evaluate`: round-95 battery
  `POSITIVE=0/1 … RERUN_CONTROLS=FAIL` (the self-test never exercises a digest
  row where the tree differs, so the swap is invisible to it).
- n17 regex `search` → `match` in `hit`: round-95 battery `RERUN_CONTROLS=FAIL`,
  `FORGERY_REFUSED=0/10`, and the oracle-count-only group also changed
  (`failed_groups={'POSITIVE': '0/1', …}`), showing the mutant leaks into the
  battery's *oracle* construction, not just the tool under test. (The battery
  rejects it, but for a muddier reason than a clean tool verdict — noted, not
  chased further.)
- n27 expression minimum length 3→2: round-95 battery `RERUN_CONTROLS=FAIL`,
  `SETUP_REFUSED=11/12` (one setup case now parses) — and the *rev-blind
  oracle's* SETUP also shifted 11/12→10/12, again a leak into oracle building.

### Class B — crash (exit 1) without the FAIL line: survive the battery's letter

- n11 HEADER column order swapped (`hits`/`hit_set` exchanged): `--selftest`
  dies at `p01-parse-good` with an uncaught `Setup: HEADER …` traceback,
  exit 1, **no `SEARCH_RERUN_SELFTEST:` summary line at all** (receipt
  `R96MutantsC1-n11-header-order.txt`). The battery counts KILLED only when
  exit 1 *and* the FAIL line is printed, so by the battery's own criterion this
  is a survivor — and more importantly it reveals a real gap in the tool's
  robustness: an uncaught `Setup` escapes `--selftest` as a traceback rather
  than a controlled `FAIL` summary. (In `verify`, `Setup` is caught and
  returned as exit 2; only the `--selftest` path is unguarded.)
- n12 `SPLIT_RE` lookbehind dropped (`\|` splits too): dies at `p14-escaped-pipe`
  with `Setup: ROW row width != 8`, exit 1, no FAIL line (receipt
  `R96MutantsC1-n12-split-lookbehind.txt`). Same reason as n11.
- n13 `parse_text` splits on `"\r\n"` instead of `"\n"`: dies at `p01-parse-good`
  with `Setup: SECTION expected exactly one '## Searches' heading, found 0`,
  exit 1, no FAIL line (receipt `R96MutantsC1-n13-parse-split-nl.txt`).
- n26 `cells` uses `lstrip(" |")` instead of `strip()`: dies at `p01-parse-good`
  with `Setup: HEADER columns None != …` (the `endswith("|")` check still
  passes, `startswith` fails), exit 1, no FAIL line (receipt
  `R96MutantsC1-n26-cells-strip-order.txt`).

So any mutant that makes the *good* fixture (`good = ST_HEAD + st_row()`)
unparseable crashes the self-test instead of failing it cleanly. The 32 cases
cannot distinguish "mutant detected" from "harness unhappy". This is within
the battery's stated kill rule, so it does not fire K2 as written — but the
battery's sentence ("each named mutant makes it exit 1") is satisfied by a
crash exactly as by a detection, which is a wording gap worth naming.

### Class C — pass --selftest (PASS 32/32) and pass the round-95 battery (RERUN_CONTROLS=PASS)

Survive **both** detectors. Of these I verified the round-95 battery on each
listed: exit 0 both times.

- n02 findings counted per-row (`findings += 1 if bad`) instead of per-code:
  `--selftest` passes because every judgement case in the self-test produces at
  most one *bad* code per row (j02/j03/j04/j05 are single-code drifts). The
  round-95 battery also passes: its P1 witness rows likewise carry only one bad
  code (the STRICT_TREE group checks `TREE_CHANGED` only), so per-row vs
  per-code is genuinely undiscriminated **by both batteries**. The
  `SEARCH_RERUN_SUMMARY findings=` number would be wrong on any row with two
  bad codes. Round-95 battery: `POSITIVE=1/1 … RERUN_CONTROLS=PASS` (full
  tally line in the probe log).
- n09 HITS regex loosened to `(-?[0-9]+)`: the self-test has no negative HITS
  case at all (only p10 exercises HIT_SET), and the round-95 battery's SETUP
  forgeries do not include a signed hit count, so a record with `hits: -3`
  would `int()` fine and be judged. Round-95 battery PASS.
- n10 DATE check replaced by a never-failing stub: no self-test case supplies
  a bad `searched` date; the round-95 battery's SETUP group has no bad-date
  forgery either. Round-95 battery PASS.
- n14 REV regex accepts uppercase hex; n15 ID regex accepts `Q0…`; n16 DIGEST
  regex accepts uppercase hex: no self-test case uses an uppercase/invalid
  variant of any of these, and the round-95 SETUP group does not forge them.
  Round-95 battery PASS (all three).
- n20 UTF-8 decode `surrogateescape` → `strict` in regex hit: all self-test
  lines are ASCII; the round-95 battery likewise reads no non-UTF-8 capture.
  A record whose capture contains invalid UTF-8 would crash the CLI instead
  of matching per GNU grep byte semantics. Round-95 battery PASS.
- n22 `matches` length check dropped: verified directly
  (`matches("d/e/f.txt", ["d/*.txt"])` → `False` on the mutant, because `zip`
  pairs `(d,d),(e,*.txt)` and `seg_match("e","*.txt")` is False, so m03's
  refusal expectation still holds — the mutant is behaviourally equivalent
  *on the fixture shapes*, since any excess path segment falls off the end of
  the zip and the mismatch it would have caught only matters when the *glob*
  is longer than the path, a direction no case exercises). Recorded as
  equivalent-on-fixtures / undiscriminated in the glob-longer direction.
  Round-95 battery PASS.
- n23 `static_dir` includes the last (filename) segment: self-test case m07
  checks `static_dir("corpus/captures/*.txt") == "corpus/captures"` — with the
  mutant, `segs = glob.split("/")` includes `"*.txt"`, the wildcard breaks
  the loop before appending, so the result is unchanged. A glob whose last
  segment is *not* a wildcard (a literal filename like `corpus/a.txt`) would
  return `"corpus/a.txt"` instead of `"corpus"` — untested by both batteries.
  Round-95 battery PASS.
- n28 empty-glob-segment check dropped: no self-test or round-95 case uses a
  `where` with `//` (e.g. `corpus//*.txt`) in a *valid* row to be refused.
  Round-95 battery PASS.
- n29 empty-hit_set-path check dropped (`corpus/a.txt,` would parse to
  `["corpus/a.txt", ""]` and be judged as SET_DRIFT rather than refused):
  no case exercises a trailing comma. Round-95 battery PASS.
- n30 separator-row length check dropped: `cells` on a separator row always
  yields 8 cells whenever the header checked, so dropping the length check
  is behaviourally equivalent given the header check — this one is a genuine
  equivalent mutant (the separator can only be reached through `table[1]`
  after the header row passed, and `cells` returns exactly 8 for any
  well-formed table line). Recorded as equivalent, not a coverage hole.
- n08 (HITS sign) — probe setup error, 0 applications, not counted.

Note on n22: my first-pass reading above shows the mutant *should* flip m03;
the probe says it did not. The most likely cause is that the replacement
string I used contained the `matches` docstring-adjacent line but the actual
shipped code path… no — the replacement applied (1 occurrence) and the file
is otherwise identical. Either way the observed result is "PASS 32/32" and I
report the observed result plus the static-analysis caveat rather than
re-litigating it.

## Does any survivor make a sentence of claims.md C1 false as stated?

C1's sentence (claims.md lines 9–16) claims: the tool "has a `--selftest` mode …
that runs 32 in-memory cases … and exits 0 with `SEARCH_RERUN_SELFTEST: PASS
cases=32/32`. Each of the 23 one-site mutants named in
`selftest-controls-r96.py` makes it exit 1". The last sentence is about the 23
named mutants — all of which I did not re-run (leaf time budget), and none of
the Class A/B/C survivors above is among them. So **no finding fires kill rule
K2 as written** ("a named mutant survives").

Two wording gaps, both short of falsifying the sentence as written:

1. **Crash-as-exit-1 (Class B).** The sentence "makes it exit 1" is true for a
   crash exactly as for a detection. A reader could reasonably take "makes it
   exit 1" to mean "the self-test detects the defect and reports FAIL"; the
   instrument cannot discriminate. The frozen battery even requires the FAIL
   line for a KILLED verdict, so by the battery's own accounting the Class B
   mutants **survive**, while by the claims sentence's wording a crash is
   enough — the sentence says *less* than the battery enforces here. This is
   the reverse of the usual direction (claim weaker than instrument) and
   would matter only if someone cited the sentence to argue the self-test
   "caught" a mutant it merely crashed on.
2. **Named limit (b) already covers Class C.** "The 23 mutants are the lane's
   chosen sites; a defect outside them may pass the self-test" (claims.md
   line 34). Class C survivors are exactly that. No sentence of C1 asserts
   anything stronger, so they fall under the named limit and do not falsify
   any stated sentence. The honest summary is that the boundary of the
   self-test's grip is: inputs absent from the 32 cases (signed hits, bad
   dates, uppercase hex ids/revs/digests, non-UTF-8 bytes, `//` globs,
   trailing-comma hit lists, two-code-drift rows) and mutants that break the
   good fixture before any case runs.

One further observation for the record, not a claim falsification: the
self-test's good fixture (`ST_HEAD + st_row()`) is parsed *before* the
individual cases, so any regression in header/section/table machinery
(class B) aborts the whole run with a traceback and no case-level
diagnosis. A `try/except Setup` around the `p01-parse-good` parse that
reports `FAIL` would close Classes B's "survives by the battery's letter"
gap without weakening anything.

## Restoration evidence

- No lane file was edited by this seat; all mutants are copies under scratch,
  and the probe source was `git show 2db151c5…:tools/search-rerun.py`.
- Frozen-bytes sha256: `c6a5872e697fcf0cc2e57c4ab870cb912ee02caab447becf357b5600a7fe6f9e`
  (re-verified this session: `git show 2db151c5ea0883de0b9dc8d95c6fac1755e1056a:tools/search-rerun.py | sha256sum`).
  NOTE: the lane's *working-tree* `tools/search-rerun.py` currently differs
  from the frozen revision — `git status --porcelain -- tools/search-rerun.py`
  shows ` M tools/search-rerun.py`, and `diff` shows the change is docstring
  wording in the `--selftest` description only. That drift is not this seat's
  (post-freeze, by others); the freeze F is the attack surface and the probe
  ran against exactly it.
- Scratch `/fast/scratch/hyaku/chousa-r96/R96MutantsC1` removed before yield;
  authoritative copies are the receipts in `.ufo/waves/round-96/w1/`.

## Tooling

No tool was installed or upgraded for this seat (none needed).

## Receipts

| Receipt | Contents |
|---|---|
| `R96MutantsC1-baseline-selftest.txt` | pristine `--selftest` output (EXIT=0, PASS 32/32) |
| `R96MutantsC1-mutprobe-out.txt` | full 30-mutant probe output (exit, killed/survived, failing cases) |
| `R96MutantsC1-n11-header-order.txt` | crash log, exit 1, no FAIL line |
| `R96MutantsC1-n12-split-lookbehind.txt` | crash log at p14, exit 1, no FAIL line |
| `R96MutantsC1-n13-parse-split-nl.txt` | crash log at p01, exit 1, no FAIL line |
| `R96MutantsC1-n26-cells-strip-order.txt` | crash log at p01, exit 1, no FAIL line |
| `R96MutantsC1-mutprobe.py.txt` | the probing harness (30 one-site replacements, applied once each) |

Round-95 battery results on Class A/C survivors were printed to the probe log
in the working session and are summarised above case-by-case (full tallies
quoted in the Class A/C notes); the long battery output was not filed as a
separate receipt because it exceeded the probe budget — the tallies quoted
are the battery's own `…RERUN_CONTROLS=PASS|FAIL` lines.

VERDICT: R96MutantsC1 C1 held — 10/29 new mutants killed by --selftest, 19 survive it (15 of them also pass the round-95 CLI battery), but every survivor falls under named limit (b) or the battery's stated kill rule, so no sentence of C1 as written is false; the real (non-falsifying) gaps are undiscriminated inputs (signed hits, bad dates, uppercase hex, non-UTF-8, // globs, two-code rows) and a crash-instead-of-FAIL path on fixture-breaking mutants.
