# Round 75 frozen claims — fresh start (attempt 1)

Base: `8022f72c889c904b5657d52c7f29e1643392a216` (master, Linux host, `ls-remote` = local).
Fresh-start reads done before declaring: the three rejected closures r72/r73/r74 and their
non-author spot-checks (`corpus/lessons/round-72-verifier-spotcheck.md`,
`round-73-verifier-spotcheck.md`, `round-74-verifier-spotcheck.md`), plus the r75 binding
prerequisites (meet QUALITY 126, kill the surviving source-blind order oracle, exercise real
committed appends and deletions through `load()`, retain public-path expected rc/check IDs).
R73's completed battery/preflight is **not** re-claimed; no Windows-host question is treated as
answered.

Two claims, distinct axes, causally separable.

## C1 — operability (lowest scored non-retired axis, 3/10)

**Claim.** The lane can bind a candidate-running loader matrix only after a committed
detection-forger battery passes it (QUALITY 126), and the successor matrix kills the r74
source-blind invocation-order oracle and the diff-only oracle that the r74 matrix accepted 9/9.

**Predicate (one sentence, one command).**
`python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work DIR`
exits 0 and prints exactly `BATTERY=PASS forgers_rejected=5/5 positive=2/2`.

**Instrument.** `corpus/evidence/round75/matrix-battery.py` (seven salted subjects: two
positives — the r74 successor counter and an independently written reference implementation of
the same documented contract — and five forgers: constant-pass, constant-fail, the r74
invocation-order oracle bytes unchanged, a diff-only oracle, and a naive presence-grep sibling).
Each subject runs the matrix twice at independent seeds; a forger counts as rejected only when
both runs exit 1 with fewer than full marks, a positive counts as accepted only when both runs
exit 0 with full marks.

**Before (do-nothing state, executed and committed before this freeze).** The same battery over
the round-74 matrix `corpus/evidence/round74/loader-matrix.py` (sha256
`979638251845071cfb2c5e130cd81800251c5a6cb041438deb258d8877e2ff8d`):
`BATTERY=FAIL forgers_rejected=2/5 positive=2/2`, exit 1
(`corpus/evidence/round75/controls/before-battery-r74-matrix.txt`). Three forgers are accepted
9/9, the invocation-order oracle among them — the surviving forge the r74 closure routed.

**After (pre-freeze positive control, executed and committed before this freeze).** The same
battery over `corpus/evidence/round75/loader-matrix-v2.py` (sha256
`95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7`):
`BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0
(`corpus/evidence/round75/controls/after-battery-v2-matrix.txt`); case-level oracle detail
`controls/order-oracle-through-v2.txt` (5/12); the frozen r73 counter — the known-bad loader —
scores 3/12 exit 1 through the same public path (`controls/negative-r73-counter-on-v2.txt`).

**Real committed appends and deletions through `load()` (QUALITY 134 / r73 section 5 item 1).**
The successor matrix writes twelve disposable fixture repositories, one real commit per case, and
invokes the candidate through its public `--lane --base --rev` CLI: unchanged, three appends,
three deletions, equal-line replacement, receipt change, and three append-only-but-structurally-
wrong cases (a second anchored heading appended to each protected file) whose verdict is
decidable only from protected-file content. Every case's expected exit code and expected failed
check-id set are declared independently in the matrix and printed per case
(`expected_rc=`, `expected_failed=`).

**Kill rule.** Any forger accepted in either run, any positive rejected, or a `BATTERY=` line that
is not exactly `PASS forgers_rejected=5/5 positive=2/2` → C1 unprovable/honest-stop. Matrix,
battery, forgers and predicate are frozen at commit A; changing a case, a check or the battery
after any seat has scored it is a new claim, not this one's rule.

**Recorded limits (QUALITY 126).** The battery proves these seven salted subjects at these
frosted inputs. It does not prove arbitrary-forgery freedom: a forge that fully re-implements
the seven checks is, for these inputs, a correct counter. Order randomisation is probabilistic
(one oracle run scored 5/12, the battery's two runs 3/12 and 2/12; a lucky permutation is not
excluded). The content cases cover three duplicate-heading mutations only, not arbitrary prose
drift. No claim of semantic entailment, arbitrary-counter robustness, or general matrix
correctness — the matrix is a contract test for the r73 C2 contract.

## C2 — calibration (sourced on S184, opened this round)

**Claim.** The r74 spot-check's routed status-neutral defect is corrected append-only: the
round-74 lesson's two `Located quote:` token counts, recorded as 18 words and 13 whitespace
tokens, are superseded by the derived 16 and 11 in an appended correction block.

**Predicate (one sentence, one command).**
`python3 -B corpus/evidence/round75/c2-count.py --lane . --rev <landing> --base 8022f72c889c904b5657d52c7f29e1643392a216`
exits 0 and prints exactly `C2=PASS checks=4/4`.

**Before.** At the base, the same command prints `C2=FAIL checks=1/4` exit 1 with
`DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`
(`corpus/evidence/round75/controls/before-c2.txt`) — the recorded counts contradict the quoted
bytes; the correction block is absent.

**Checks.** Q1 the correction block appears exactly once; Q2 it states the derived 16 and 11;
Q3 it names the superseded 18 and 13; Q4 append-only (`git diff --numstat` removes zero lines
from `corpus/lessons/round-74.md`). The command always prints the derived values so the block's
numbers are re-derived at the measured revision.

**Kill rule.** Correction block absent, derived counts not 16/11, superseded values unnamed, or a
non-zero deletion count on the lesson → C2 honest-stop; the frozen bytes are not amended after
scoring.

## Shared boundaries

No network, no package adoption, no host question presumed answered, no sibling repo or fleet
repo writes other than the round report and L0 appends. Non-author spot-check requested for the
SOURCES admit/reject set; dispatched wave seats are author-lane evidence, not promotion
reviewers. Round shape: one v1 wave of 10 seats (3 executor, 1 scout, 1 scribe, 1 connector,
2 reviewer, 1 critic, 1 mutation-tester = 4 attack seats, 40%); L1 holds the canonical planner
seat; no residual call planned; no dead seat replaced.
