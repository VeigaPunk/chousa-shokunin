# Round 62 — chousa — frozen claims

Frozen before any wave seat is dispatched. Base: lane master `8607de84723d5ff9bbcbe71eedebd6a0d30bfd87`.
Date 2026-10-28. This file's own sha256 and the freeze commit are carried in the wave context and in the
report; neither can be written inside the file (QUALITY 116). File digests below are written as 16-hex
prefixes (`sha256 prefix <16 hex>`), never as 64-hex tokens, so a prefix is checkable with
`sha256sum FILE | cut -c1-16` and the freeze check's stray-digest rule stays meaningful. No predicate,
counter, kill rule or target below changes after the freeze commit; a changed rule is not the claim's rule.
Post-wave findings against a frozen counter are routed as limits and supplements, never as a rewrite.

Round 61's closure (`corpus/lessons/round-61-verifier-spotcheck.md`, routed defects 1 and 2) is the reason for
claim C1: the round-61 span-builder counter was forgeable by detection (`CritC1Sniff` 20/20 at 3 of 3 seeds,
`CritC1Detached`, `CritC1Rss`). Every instrument below was therefore built and exercised before this freeze
against do-nothing counters, do-nothing builders, single-defect mutants and positive controls. Receipts:
`corpus/evidence/round62/controls/`.

## C1 — operability: a counter that tells a hardened builder from one that only looks hardened

Target axis: operability (the lane's only scored axis, historical 3/10 on the round-1 archived-export
observable; that numeric observable is not moved and no new score is invented — the claim is the battery
count below). Tag `plumbing`. This claim changes no builder; `tools/build-spans.py` stays at sha256 prefix
`c366492005ce304a`.

**Predicate R62-C1** (the sentence in the docstring of `corpus/evidence/round62/c1v2-battery.py`): run on a
counter K — any program taking `--builder B --work DIR` that exits 0 for pass and 1 for fail — the battery
builds, into a fresh scratch directory with a random salt comment on each, three copies of the landing builder
(K must exit 0 on each), four independently written correct builders (exit 0 on each), twelve forgers F01–F12
(each carries the landing builder's code and runs the unhardened round-61 base builder unless a detection test
fires — cwd name, environment keys, directory layout, file names, URL host shape, the parent's command line,
LANG, the file-size limit, stdin, any process's command line, stdout being a file — or, F12, writes bytecode
and has a detached `setsid` helper delete `__pycache__` after the builder exits; K must exit exactly 1 on each)
and four do-nothing builders (`exit 0`, `exit 2`, the base builder, the base builder printing the pass tokens;
K must exit exactly 1 on each), and prints `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4
BATTERY=PASS` and exits 0.

Counting command (from the lane root; `--work` absent or empty; scratch under `$HYAKU_SCRATCH/chousa-r62/`):

    python3 corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/c1v2-count.py --work <dir>

**Before**: the same battery on the round-61 counter `corpus/evidence/round61/c1-count.py` prints
`LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL`, exit 1: all twelve forgers
read 20/20 `C1=PASS` (`corpus/evidence/round62/controls/c1v2-before.txt`).
**After target**: the same command on `corpus/evidence/round62/c1v2-count.py` (sha256 prefix `b7016fba91b03460`)
prints `FORGERS_REJECTED=12/12 BATTERY=PASS`, exit 0, and `python3 corpus/evidence/round62/c1v2-count.py
--builder tools/build-spans.py --work <dir>` prints `LEGS=20/20 C1V2=PASS` (exit 0) at three fresh random seeds
(no seed given; `C1V2_SEED` unset) and once more by the closure.

What the v2 counter changes against v1 (instrument, frozen): each of the 20 legs runs twice, a `plain` profile
(v1's layout) and a `neutral` profile (random directory, builder, quotes, cache and output names, URL host shape,
extra environment variables, LANG, PATH order and RLIMIT_FSIZE, an empty cwd outside the fixture, a closed-pipe
stdin, stdout and stderr as pipes), and a leg passes only when both pass; every run is inside a fresh
`unshare -Ufp --kill-child --mount-proc` namespace (no helper outlives the builder; the builder cannot see the
counter), under a 200 MiB address-space limit; the seed is read from the environment `C1V2_SEED`, never from argv;
the `Traceback`-token tests of H16 and H17 are gone (exit code and tree only); refusal snapshots compare mtimes.

**Do-nothing and discrimination receipts** (all committed before the freeze): the round-61 counter 0/12 on the
forgers; `null-pass.py` (always exit 0) accepts 0/12 forgers and 0/4 stubs; `null-fail.py` (always exit 1) rejects
the landing builder 0/3; `null-hashlist.py` (accepts only known file hashes) rejects the salted landing builder
0/3 — all three `BATTERY=FAIL` (`controls/null-counters.txt`). The intact counter X00 and ten single-defect mutants (X01–X08, X10, X12) of the v2
counter (`controls/run-c1v2-controls.py`, `controls/c1v2-controls.txt`): each mutation that removes one profile
feature or the sandbox lets exactly the forgers that feature stops through and the battery exits 1
(`CONTROLS_UNEXPECTED=0`); mutant X10 (drop the address-space limit) SURVIVES — no forger in the battery depends
on it (named gap). A target no do-nothing counter reaches: the best do-nothing scores `FORGERS_REJECTED` 12/12 only
by rejecting the landing builder too (`LANDED=0/3`).

**Kill rule** (frozen): C1 is verified only when the battery on the unmodified `c1v2-count.py` reads
`BATTERY=PASS` at the landing commit and at the closure, and `LEGS=20/20 C1V2=PASS` at three fresh seeds. A miss
is an honest stop, not narrowed after landing. A forger or false positive a wave seat demonstrates beyond the
twelve is routed as a counter limit and added to the next round's battery, not a refutation.

**Named limits** (disclosed before data): a builder that detects the sandbox itself (`NSpid` in
`/proc/self/status`, `getpid() == 1`), a feature neither profile varies (the `capture-text.py` file name, the
`S###` id shape, the quote vocabulary), the leg's content, or that waits out the counter, is not stopped; a
builder that reads a 192 MiB capture in a detached helper under the address-space limit is bounded, not
measured, and a builder that keeps the read in shared memory below the limit is not measured; the forgers are
authored by the lane that wrote the counter (overfit risk); the battery's builders are all Python.

## C2 — coverage (sourced): kernel-enforced path resolution, `openat2(2)`

Target axis: coverage. The surface it moves is operating-system path-resolution semantics for a tool that opens
paths under a directory it does not control: round 61's entry `derived-output-safety-r61.md` records O_NOFOLLOW,
O_EXCL, rename and the check-then-write window; the lane holds nothing on the kernel call that closes that
window. Command that shows it unmoved: `grep -rl openat2 corpus/knowledge` prints nothing (exit 1) at the base. This is
the round's sourced claim: the entry cites registry rows S138, S139 and S140, each opened this round
(2026-10-28; S138 is the lead recorded in `corpus/SOURCES.md` `## Leads` by round 61). Tag `plumbing`.

**Predicate R62-C2** (the sentence in the docstring of `corpus/evidence/round62/c2v2-count.py`): in the lane tree
the file `corpus/knowledge/openat2-resolve-r62.md` exists and carries TRIO, ROWS, QUOTES, COVERAGE, CLAIMS, ECHO,
LIMITS, PROBE, MAP and CENSUS as that docstring defines them — counted `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=k/k
COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`. New against round 61: ECHO (a
claim that only repeats its quote fails), PROBE (the entry rests on `corpus/evidence/round62/openat2-probe.py`,
whose live output must equal the committed `openat2-probe.txt`, 14/14 facts) and MAP (`corpus/README.md` names
the entry).

Counting command: `python3 corpus/evidence/round62/c2v2-count.py` (lane root; reads `man`/`col`, the probe and the
census script). Rows to land: S138 `openat2(2)` (installed man-pages 6.19-1 page, tier A), S139
`/usr/include/linux/openat2.h` (linux-api-headers 7.2-1, tier A), S140 the probe output (own-work, tier B).

**Before**: `ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 ECHO=0/1 LIMITS=0/1 PROBE=0/1 MAP=0/1
CENSUS=1/1 C2=FAIL`, exit 1 (`controls/c2v2-before.txt`). **After target**: `C2=PASS` exit 0, and `grep -c openat2
corpus/knowledge/openat2-resolve-r62.md` is positive.

**Do-nothing and discrimination receipts** (`controls/c2v2-controls.txt`, `controls/run-c2v2-controls.py`): a scratch
mirror with the positive rows and the positive entry `controls/c2v2-positive-entry.md` passes; the absent entry,
absent rows and 18 single-defect variants (fabricated quote, cross-row quote, uncited quote, queued row, old
`opened`, missing `used-by`, no limits, no `[INFERENCE]` limit, junk claim, quote over 25 words, no trio, echo claim,
missing probe script, edited probe output, stale probe output, missing README map, wrong header file, wrong anchor)
all FAIL (`C2V2_CONTROLS_UNEXPECTED=0`). Round 61's recorded limit "an echoing claim reaches PASS" is closed in v2
(`echo-claim` FAILs). The remaining named limit, recorded: a claim that adds words but does not follow from its quote
still reaches PASS (`non-sequitur`, expected PASS) — entailment is judged by non-author reviewers, not by the counter.

**Kill rule** (frozen): C2 is verified only when `c2v2-count.py` on the landing commit prints `C2=PASS` and the
closure's entailment read finds no claim unsupported by its quotes. The counter bytes (sha256 prefix
`817d5fc0b94e9fc8`) do not change after the freeze.

**Named limits**: the quotes describe man-pages 6.19 and linux-api-headers 7.2-1 on this host; the probe runs on
one kernel, one filesystem and x86_64 only; entailment is not machine-checked.

## Frontier step (not a claim)

Census before/after with the exit codes; one mistake mined into `corpus/lessons/round-62.md` `## Mistakes` (the
forgeable-counter class of rounds 49–61, captured-by `none` until this round's battery, red-before
`controls/c1v2-before.txt`); the sourced claim is C2; at least one admit and one reject from this round's rows for
the non-author spot-check.

## Wave shape and what the seats may and may not do

One v2 wave `w1`, 64 seats, attack share at least 25 %. Seats attack the counters, the battery and the entry, and draft
the entry and the lesson; seats do not edit the frozen counters, battery or controls, and never commit.
