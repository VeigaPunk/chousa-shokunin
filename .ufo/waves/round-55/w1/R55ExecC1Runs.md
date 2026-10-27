# R55ExecC1Runs — C1 (operability) independent re-measurement, round 55 wave 1

seat `R55ExecC1Runs` (executor, leaf). Axis attacked: **operability** — independent re-measurement of the
frozen C1 predicate on the candidate builder. No predicate, target, counter, control or production file
changed; my only write is this report. Scratch `/fast/scratch/hyaku/chousa-r55/R55ExecC1Runs` (removed).
No installs/upgrades (soffice 26.8.1.1 680(Build:1) and git were present), no network, no pacman/uv/npx,
no git/jj mutation, no LibreOffice profile outside my scratch.

## 1. Candidate identity (before measuring)

```
$ sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  .../tools/build-spans.py
$ git -C .../chousa-shokunin show 6ca924995d48facbf704d2aa22ddaec236059039:tools/build-spans.py | sha256sum
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  -
$ git -C .../chousa-shokunin rev-parse 6ca924995d48facbf704d2aa22ddaec236059039
6ca924995d48facbf704d2aa22ddaec236059039
$ sha256sum .../corpus/evidence/round55/c1-count.py
5506f240c53ff83c7c17b7252c7627871b4b1af7c1ca739b461fdbcc32048906  .../c1-count.py
```
The worktree builder is the committed candidate blob `6ca92499` — what I measured is what was frozen.

## 2. Five runs, fresh empty `--work` under my scratch each

Command form: `python3 .../corpus/evidence/round55/c1-count.py [--seed N | --per-leg 5 --seed 55]
--work $S/<dir>`; every `--work` dir was created new (the counter's own precondition
`usage: --work must be empty`). Outputs pasted verbatim, in order:

```
# run 1: --seed 7
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=7 per-leg=3
GENOLE=PASS 3 docs, 6 quotes
OLEPIN=PASS 4 captures, 12 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
RC=0
# run 2: unseeded
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=611073137 per-leg=3
GENOLE=PASS 3 docs, 6 quotes
OLEPIN=PASS 4 captures, 12 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
RC=0
# run 3: unseeded
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=582257669 per-leg=3
GENOLE=PASS 3 docs, 6 quotes
OLEPIN=PASS 4 captures, 12 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
RC=0
# run 4: unseeded
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=806430991 per-leg=3
GENOLE=PASS 3 docs, 6 quotes
OLEPIN=PASS 4 captures, 12 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
RC=0
# run 5: --per-leg 5 --seed 55
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=55 per-leg=5
GENOLE=PASS 5 docs, 10 quotes
OLEPIN=PASS 4 captures, 20 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
RC=0
```
The three system seeds differ from each other and from 7 (`611073137`, `582257669`, `806430991`), so the
runs are not one sheet re-printed: GENOLE drew 3 fresh `.doc` + 6 quotes and OLEPIN 12 quotes per run, and
run 5 doubled both (10/20) while `judge()`'s checks (manifest header, row echo, `capture_sha256`,
span-name sequence, `span == form[o:o+len(span)]`, `len(span) > len(quote)`,
`o + span.find(quote) == char`, the `QUOTE <id> char <N>` stdout echo, no extra/missing span file) all
held. No `ENV_CHANGED`, no exit 2, no timeout.

## 3. Process and tree hygiene after every run

`pgrep -u $USER -af "$S"` after each of the five runs printed `(none)` — no `soffice.bin`/`oosplash` of
mine survived (the counter's profile is `work/soffice-profile`, inside my scratch); the final check before
removing scratch also printed `(none)`. Lane tree:

```
# baseline, before any run of mine          # after runs 1-5
?? .ufo/waves/round-55/w1.ready             ?? .ufo/waves/round-55/w1.ready
?? .ufo/waves/round-55/w1.ready.partial     ?? .ufo/waves/round-55/w1.ready.partial
?? .ufo/waves/round-55/w1/                  ?? .ufo/waves/round-55/w1/
?? corpus/evidence/round55/c1-measure-after.txt
                                            ?? corpus/evidence/round55/c1-seed-sweep-L1.txt
```
The one new entry is the concurrent L1 sweep's receipt, not mine: baseline `pgrep` already showed the
L1's own `soffice` on profile `.../chousa-r55/L1/ws/soffice-profile`, and that file's own header reads
`# R55-C1 L1 seed sweep (robustness receipt, not the frozen target): seeds 1001-1040, --per-leg 4,
candidate 6ca92499`. My runs cannot write it: c1-count.py touches `LANE` only via
`subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:{p}"], ...)` at c1-count.py:393, everything
else under `work`. No tracked file, index entry or jj state touched by my runs.

## 4. Frozen target verdict

Target: `LEGS=4/4`, `C1=PASS` exit 0 on three independent unseeded runs **and** once with `--seed 7`.
Observed: 4/4 and `C1=PASS`, rc 0 in all four required runs (unseeded seeds 611073137, 582257669,
806430991; seed 7), plus 4/4 on the wider `--per-leg 5 --seed 55` run. Kill rule not triggered — no leg
failed anywhere, no `ENV_CHANGED`. C1's after-measurement therefore passes on a seed set I chose myself.

Residual, reported not patched (predicates are frozen): (a) all my runs and the L1 sweep share one
LibreOffice build and the same four pinned captures, so GENOLE/REGRESS are independent of the seed but not
of the host converter — a converter change would nonetheless surface as `ENV_CHANGED` or
`span is not a slice`, judged on `capture-text.py` output rather than the raw, not as a silent pass;
(b) the single lane-status delta is a sibling's receipt, left untouched.

VERDICT: attacked C1 operability by independent re-measurement of the frozen counter on candidate
`6ca92499` (sha256 `1ed2650a…80bf6`, equal to the pinned blob) — 4/4 LEGS / C1=PASS / rc 0 on seed 7 and
on three unseeded runs (and 4/4 at `--per-leg 5 --seed 55`), no surviving `soffice.bin`, lane tree unchanged
by my runs: the frozen target is met.
