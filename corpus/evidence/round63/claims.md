# Round 63 — chousa — frozen claims

Frozen before any wave seat is dispatched. Base: lane master `a847a37cc263c80417ee1cdf650de33e2f91a839`.
Date 2026-10-28. This file's own sha256 and the freeze commit are carried in the wave context and in the report;
neither can be written inside the file (QUALITY 116). File digests below are written as 16-hex prefixes
(`sha256 prefix <16 hex>`), never as 64-hex tokens, so a prefix is checkable with `sha256sum FILE | cut -c1-16`.
No predicate, counter, battery, kill rule or target below changes after the freeze commit; a changed rule is not the
claim's rule. Post-wave findings against a frozen instrument are routed as limits and supplements, never as a rewrite.

Round 62's closure (`corpus/lessons/round-62-verifier-spotcheck.md`, section Routed to the lane, five items) and the
round-62 report's own caveats are the reason for the shape of this round. Item 2 asked to carry the v3 counter and
battery work forward; this round does not take it (a different operability move, below), and says so: the
`Planned — round 63` row of `SCORECARD.md` (candidates: a v3 counter and battery, the C2 counter's control gaps, the
size-watch threshold) is amended by `Planned — round 63 (amended before the freeze)` in the same commit. Item 1
(a bare export exits 2 from the C2 counter) is addressed by `c2-count.py`'s `--fleet` handling and its message; item 3
(no checker for false statements in a frozen claims file) gets a read by wave seats after the freeze (`CritCalibration`,
`RevC1Contract`, `ExecClaimsStatements`), and a false statement they find is recorded in an erratum file, never edited
into this one; item 4 (use the edit tool) is in every seat's context, and the report discloses one slip of the L1's own
(a shell python replacement on the new reference tool); item 5 changes nothing in `SHONEN.md`.

Files created by the round (do not exist at the freeze; a path listed here is not a false pointer):
`Created by the round:` `tools/lane-preflight.py`, `corpus/knowledge/git-revision-identity-r63.md`,
`corpus/evidence/round63/git-revision-probe.py`, `corpus/evidence/round63/git-revision-probe.txt`,
`corpus/lessons/round-63.md`.

## C1 — operability (capability acquisition): a lane preflight that runs the lane's own checks and names the failing gate

Target axis: operability — the lane's only numerically scored axis, historical 3/10 on the round-1 archived-export
observable; that numeric observable is not moved and no new score is invented. The claim is a capability: on
success `SCORECARD.md` enters one `capabilities` row for `tools/lane-preflight.py`. Tag `plumbing`.

**The tool's contract** (the sentence the battery's docstring points at). `python3 tools/lane-preflight.py
[--root DIR] [--fleet DIR] [--work DIR] [--skip G08[,G..]] [--only G01[,G..]]` prints one line per gate in id order,
`GATE <id> <name> PASS|FAIL|ENV <detail>` (a gate not selected: `GATE <id> <name> SKIP`), then one summary line
`PREFLIGHT=<passed>/<run> FAILED=<ids|none> ENV=<ids|none> SKIPPED=<ids|none>` (`run` counts the gates that were not
skipped). Exit 0 when every gate that ran passed; 1 when any gate FAILED; 2 on a usage error (an unknown gate id: no
summary line) or when no gate failed but one could not run (ENV). A gate that crashes is a FAIL, never a pass.
Gates (id, name, rule), each reading only files under `--root`:

- G01 census — the fleet's `scripts/sources-census.sh validate --file ROOT/corpus/SOURCES.md` exits 0 (script from
  `--fleet DIR/scripts`, else `$SHOKUNIN_ROOT/scripts`, else ROOT's parent's `scripts`; none found: ENV);
- G02 knowledge-index — every file name of `corpus/knowledge/*.md` occurs in `corpus/README.md`;
- G03 lesson-gate — every `corpus/lessons/round-<N>.md` has a heading line `## Gate` followed by a non-word character
  or the end of the line (`## Gates` does not count);
- G04 shonen-pointers — every path-shaped word inside a backtick span of `SHONEN.md` (a whitespace-separated word
  with a `/`, or ending `.md .log .py .sh .json .txt .tsv .jsonl`; leading `(` and trailing `;,.)` stripped, a
  trailing `:N` or `:N-M` stripped; a word starting with `<`, `-` or `$`, containing `*` or `<`, or starting `http:`
  or `https:` is not a pointer) exists under ROOT;
- G05 scorecard-paths — every whitespace-separated token inside a backtick span of the evidence cell (third cell) of a
  table row under a `## Capabilities…` heading of `SCORECARD.md` that matches `corpus/…`, `tools/…` or `.ufo/…`
  (no whitespace, `*`, `<` or `>`; `;` and `,` stripped) exists under ROOT;
- G06 freeze-selftest — `python3 -B tools/freeze-check.py --selftest` exits 0 and prints a `FREEZE_CHECK=` line;
- G07 assimilate-selftest — `python3 -B tools/assimilate-rows.py --selftest` exits 0 and prints `SELFTEST=PASS`;
- G08 gate-selftest — `bash tools/research-gate.sh --selftest` exits 0 and prints `RESEARCH_GATE_SELFTEST: PASS`.

No network; no write outside `--work`.

**Predicate R63-C1** (the sentence in the docstring of `corpus/evidence/round63/c1-battery.py`): run on a tool T — a
program that takes `--root DIR [--fleet DIR] [--skip G08] [--only G03]` and prints the `GATE`/`PREFLIGHT=` lines of the
contract above — the battery copies the lane once into a scratch golden, then for each of 22 legs copies the golden
to a random-named variant directory, applies one change, copies T's bytes to a random path outside the variant, runs
it from an empty cwd with a minimal environment, and requires: CLEAN (the unchanged variant, run with `--skip G08`:
exit 0, `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`); fifteen defect legs D01–D15, each naming the exit code and
the exact FAILED and ENV sets (D13: exit 2, no PREFLIGHT line), all other run gates PASS and a summary line equal to
the count of its own GATE lines; six benign legs B01–B06 that edit files the gates read (or no gate reads) and keep
the lane valid: exit 0, all run gates PASS — and prints `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0.

Counting command (from the lane root; `--work` absent or empty; scratch under `$HYAKU_SCRATCH/chousa-r63/`):

    python3 corpus/evidence/round63/c1-battery.py --tool tools/lane-preflight.py --fleet <fleet root> --work <dir>

and, once, the full run including G08 (several minutes on a loaded host):

    python3 tools/lane-preflight.py --root . --fleet <fleet root>

**Before**: the tool does not exist; the battery prints `CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=FAIL`, exit 1
(`corpus/evidence/round63/controls/c1-before.txt`). **After target**: the same command prints `CLEAN=1/1
DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0, in three runs at the landing commit with `C1_SEED` unset, and the full
run prints `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none`, exit 0.

**Controls (all committed before the freeze; `controls/c1-controls.txt`, `controls/run-c1-controls.py`,
`controls/c1-reference-runs.txt`)**: 22 control tools, every one run through the same battery:
the reference candidate `controls/pos-ref-preflight.py` reads `BATTERY=PASS` (and three further runs read the same,
`c1-reference-runs.txt`); an absent tool, `null-pass.py` (always says all passed: `DEFECTS=0/15`), `null-fail.py`
(always says all failed: `CLEAN=0/1`), `null-diff-oracle.py` (knows the committed lane and fails any gate whose
file differs from the lane's bytes: `DEFECTS=15/15 BENIGN=0/6`, rejected only by the benign legs) and
`null-selfreport.py` (eight PASS lines, a `8/8` summary: `CLEAN=0/1`) all read `BATTERY=FAIL`; sixteen single-defect
mutants M01–M16 of the reference (first-failure-only, a gate that always passes, ENV counted as pass, silent skip, a
wrong summary count, exit always 0, no `:N` suffix strip, an index check that checks nothing, census exit ignored,
selftest exit ignored, token check dropped, all SCORECARD tables read, `--only` ignored, unknown id accepted,
exact-heading rule, first path word only): fifteen read `BATTERY=FAIL` with the legs the runner names, and M11 (token
check dropped; the selftest's exit code already carries the verdict) SURVIVES as an equivalent mutant (named gap).
`C1_CONTROLS_UNEXPECTED=0`. A target no do-nothing tool reaches: the best do-nothing (`null-pass.py`) passes CLEAN
and the six benign legs and fails every defect leg; the best forger (`null-diff-oracle.py`) passes CLEAN and every
defect leg and fails every benign leg.

**Kill rule** (frozen): C1 is verified only when the battery on the unmodified `c1-battery.py` reads `BATTERY=PASS`
for `tools/lane-preflight.py` at the landing commit (three runs) and at the closure, and the full run reads
`PREFLIGHT=8/8`. A miss is an honest stop, not narrowed after landing. A forger, hole or false positive a wave seat
demonstrates is routed as a limit and added to the next round's battery, not a refutation.

**Named limits** (disclosed before data): the battery never runs G08 (its minutes of CPU: the full run is the one
receipt for that gate) and so cannot show a G08 defect caught; it does not check the gate names printed on the
`GATE` lines (only ids, statuses and counts); the gate set is chousa's own (a `chousa-` lane shape: SHONEN, SCORECARD,
`corpus/` layout; other lanes are not claimed); G06 depends on the lane carrying the round-59 to round-61 wave files
the freeze selftest reads, and the golden copy carries them; the tool runs the lane's own committed tools inside
`--root` (no sandbox); the rules for G04 and G05 are lexical, not semantic; the reference candidate and the
benign and defect legs were written by the lane that wrote the battery (overfit risk, partly met by
`null-diff-oracle.py`).

## C2 — coverage (sourced): what pins a citation to a git revision

Target axis: coverage. The surface it moves is the revision identity of a cited repository artifact: `SKILL.md`
requires every claim to carry a pointer to the artifact and the revision read, and `corpus/knowledge/revision-binding-r31.md`
covers the sha256 pin of source bytes; the lane holds nothing on what a git revision name (full or abbreviated object
name, annotated or lightweight tag, branch, `<rev>:<path>` blob) names. Command that shows it unmoved:
`grep -rl 'rev-parse' corpus/knowledge` prints nothing (exit 1) at the base. This is the round's sourced claim: the
entry cites registry rows S142, S143 and S144, each opened this round (2026-10-28; local sources only — the installed
Arch package pages and the lane's own probe; no URL is fetched, L0 `8d77e6c1` is open). Tag `plumbing`.

**Predicate R63-C2** (the sentence in the docstring of `corpus/evidence/round63/c2-count.py`): in the lane tree the
file `corpus/knowledge/git-revision-identity-r63.md` exists and carries TRIO, ROWS, QUOTES, COVERAGE, CLAIMS, ECHO,
LIMITS, PROBE, MAP and CENSUS as that docstring defines them — counted `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=k/k
COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`. New against round 62's counter: the
git version is bound (the entry's Limits must contain the live `git --version` line, and the committed probe output's
`HEADER git=` line must equal it), `--config` selects a configuration (the default, `git`, is the claim; `openat2` is
a control), and the fleet root is documented and handled (`--fleet`, `$SHOKUNIN_ROOT`, else the lane's parent; a
missing census script exits 2 with a message naming the flag).

Counting command: `python3 corpus/evidence/round63/c2-count.py [--fleet <fleet root>]` (lane root; reads `man`, `col`,
`git`, the probe and the census script). Rows to land: S142 `git-rev-parse(1)` (installed git 2.56.0-1 page, tier A),
S143 `gitrevisions(7)` (same package, tier A), S144 the probe output (own-work, tier B). A rejected row (a source
opened and refused) is expected beside them for the Gate's reject; it is not a counted target.

**Before**: `ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 ECHO=0/1 LIMITS=0/1 PROBE=0/1 MAP=0/1
CENSUS=1/1 C2=FAIL`, exit 1 (`controls/c2-before.txt`). **After target**: `C2=PASS` exit 0, and `grep -c rev-parse
corpus/knowledge/git-revision-identity-r63.md` is positive.

**Do-nothing and discrimination receipts** (`controls/c2-controls.txt`, `controls/run-c2-controls.py`): a scratch
mirror with the candidate rows `controls/candidate-git-rows.txt`, the candidate entry `controls/c2-positive-entry.md`
and the candidate probe passes (`positive`); `absent`, `no-entry-rows` and 19 single-defect variants (fabricated quote,
cross-row quote, uncited quote, queued row, old `opened`, missing `used-by`, no limits, no `[INFERENCE]` limit, limits
without the git version, junk claim, quote over 25 words, no trio, echo claim, missing probe script, edited probe output,
probe output for another git version, missing README map, wrong header file, wrong anchor) all FAIL, 21 FAIL variants
in all; `non-sequitur` (a claim that adds words but does not follow from its quote) PASSES, the named limit; the
`openat2` configuration on the lane tree itself (round 62's committed entry) PASSES — `C2_CONTROLS_UNEXPECTED=0`.

**Kill rule** (frozen): C2 is verified only when `c2-count.py` on the landing commit prints `C2=PASS` and the
closure's entailment read finds no claim unsupported by its quotes. The counter bytes do not change after the freeze.

**Named limits**: the quotes describe the pages of git 2.56.0-1 on this host and the probe one git version on one
host; entailment is not machine-checked (the counter is structural plus an echo screen); five of the candidate
probe's fourteen expectations are the author's inference and say so in their `# cite` comments.

## Frontier step (not a claim)

Census before and after with exit codes (`.ufo/waves/round-63/census-start.txt` is the start, exit 0); one mistake
mined into `corpus/lessons/round-63.md` `## Mistakes`; the sourced claim is C2; at least one admit and one reject
(a rejected row opened this round) for the non-author spot-check.

## Frozen instruments, digests and receipts

sha256 prefixes of the frozen bytes: `c1-battery.py` `0073fba73c89aaf8`, `c2-count.py` `606207e224c0b7cf`,
`controls/pos-ref-preflight.py` `07683086fd6c6b41`, `controls/run-c1-controls.py` `8e9bd4c3e304b5f0`,
`controls/run-c2-controls.py` `8b2b371340b01b58`, `controls/candidate-git-revision-probe.py` `ccd702f4e9a2f7c4`,
`controls/c2-positive-entry.md` `93ad2c681783b6ce`, `controls/candidate-git-rows.txt` `cfdf7b117c26a07f`.
The receipts under `controls/` are the committed output of the runners at these bytes.

## Wave shape and what the seats may and may not do

One v2 wave `w1` inside the 64–128 band, attack share at least 25 %. Seats attack the battery, the reference tool, the
counter, the probe and the candidate entry, review each gate, and draft the entry, rows and lesson; seats do not edit
the frozen instruments or controls, and never commit. The L1 integrates: the landed `tools/lane-preflight.py` is the
reference candidate plus whatever wave findings it adopts, and must pass the unmodified battery.
