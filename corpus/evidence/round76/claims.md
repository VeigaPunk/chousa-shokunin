# Round 76 frozen claims — successor discrimination (attempt 1)

Base: `1af39fed6058ad46fc075b72fddaae838f43273e` (master, Linux host, `ls-remote` = local).
Prefreeze instruments and control receipts: `da9ac7ec684fe9fe9ad5554cab6180057255b76b` — the
controls commit strictly precedes this freeze (r75 routed defect 3; `souji` QUALITY Q120).

Reads done before declaring: the r75 closure (admitted) and its non-author spot-check
`corpus/lessons/round-75-verifier-spotcheck.md` routed defects 1–5, and the r75 lesson's
`## Instrument limits`. Routed defects 1 and 2 are this round's two claims; 3 (chronology) is
honoured by the controls-first commit above; 4 (receipt precision) is honoured by naming the
controls revision in every receipt; 5 (parser red-before) is answered by the label-pair control.
R73's completed battery/preflight is not re-claimed; no Windows-host question is treated as
answered.

Two claims, distinct axes, causally separable.

## C1 — operability (lowest scored non-retired axis, 3/10; the historical 3/10 is not moved)

**Claim.** The lane's candidate-running loader matrix can bind a correction counter only after a
committed detection-forger battery passes it, and the successor matrix closes the answer-key
channels round 75 left open: the commit-subject oracle that reached 12/12 on the r75 matrix is
rejected, the twelve-entry declared-order oracle is rejected, and a stalled candidate cannot
stall the matrix.

**Predicate (one sentence, one command).**
`python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR`
exits 0 and prints exactly `BATTERY=PASS forgers_rejected=11/11 positive=2/2`.

**Instruments (frozen at `da9ac7ec684fe9fe9ad5554cab6180057255b76b`).**
`loader-matrix-v3.py` (sha256 `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f`)
keeps the twelve-case contract but: every case commit carries the literal subject `case`; every
fixture file body carries a per-run salt line and every mutation a per-run random-length pad line,
so tree ids, blob sizes and size deltas vary per run; the candidate child runs in its own session
under `LOADER_MATRIX_CHILD_TIMEOUT` and is killed on expiry; only the seed digest is printed.
`matrix-battery-v3.py` (sha256 `217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360`)
runs thirteen salted subjects at two runs each — two positives (the r74 successor counter and the
independently written r75 reference counter) and eleven forgers: constant-pass, constant-fail,
order-twelve, diff-only, naive-grep, subject-map, tree-identity, size-map, harness-source,
seed-leak, hang. Each subject copy sits in a random-named directory and carries a salt line.

**Before (do-nothing state, committed before this freeze).** The same battery over the r75 matrix
`corpus/evidence/round75/loader-matrix-v2.py` (sha256 `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7`):
`BATTERY=FAIL forgers_rejected=9/11 positive=2/2`, exit 1
(`corpus/evidence/round76/controls/before-battery-v2-matrix.txt`). The `subject-map` forger reads
only `git log -1 --format=%s` and reaches `marks=12/12/PASS` on both runs — the r75 answer key —
and the `hang` forger stalls both matrix invocations past the battery's 300 s bound.

**After (pre-freeze positive control, committed before this freeze).**
`BATTERY=PASS forgers_rejected=11/11 positive=2/2`, exit 0
(`corpus/evidence/round76/controls/after-battery-v3-matrix.txt`), 13 subjects × 2 runs; every
forger `REJECTED`, both positives `12/12/PASS` twice. Negative control: the r75 presence counter
(wrong contract) scores `LOADER_MATRIX=0/12 MATRIX=FAIL`, exit 1
(`controls/negative-r75-counter-on-v3.txt`), so blanket refusal is not the gain. Parser pair: the
battery accepts a matrix that prints `LOADER_MATRIX=… C1=PASS` (`BATTERY=PASS`) and refuses an
unknown label (`forgers_rejected=0/11 positive=0/2`, `BATTERY=FAIL`)
(`controls/parser-label-pair.txt`).

**Kill rule.** Any forger scored as not rejected in either run, any positive not accepted in both,
or a `BATTERY=` line that is not exactly `PASS forgers_rejected=11/11 positive=2/2` → C1
unprovable/honest-stop. Matrix, battery, forgers and predicate are frozen at the controls commit;
changing a case, a check or the battery after any seat has scored it is a new claim.

**Recorded limits (QUALITY 126/135/137).** The battery proves these thirteen salted subjects at
these saltings; it does not prove arbitrary-forgery freedom, and a counter that reads the unified
patch text or re-implements every check is correct for these inputs. Order randomisation is
probabilistic. The matrix's commit graph still shows all twelve case commits, so a candidate that
reads patch text can reconstruct the case set; that class is content reading, not metadata. The
child bound is 3 s under the battery and 20 s by default; a correct-but-slow counter can be
killed at the bound, which is a rejection the battery cannot distinguish from a stall.

## C2 — calibration (sourced on S187/S188, opened this round)

**Claim.** The lane's record-correction instrument is no longer a presence test: the successor
counter rejects six structurally bogus correction blocks that the r75 counter accepted or could
not bind to the authored bullet, while still accepting the lane's real correction block and one
independently worded valid block.

**Predicate (one sentence, one command).**
`python3 -B corpus/evidence/round76/c2-battery.py --counter corpus/evidence/round76/correction-count-v2.py --work DIR`
exits 0 and prints exactly `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS`.

**Instruments (frozen at the controls commit).** `correction-count-v2.py` (QUALITY 136): derives
both counts from the authored `- Admit S182` / `- Reject S183` bullets rather than the first
`Located quote:` match, and scores V1 authored-bullet derivation, V2 word-boundary corrected
values, V3 superseded values with a cue, V4 polarity, V5 magnitude, V6 last-section position, V7
base ancestry, V8 append-only, V9 not-inside-an-HTML-comment. `c2-battery.py` builds seven
disposable fixture repositories (one valid block, six bogus) and runs the counter on each plus on
the real lane at `--rev master` over base `8022f72c889c904b5657d52c7f29e1643392a216`.

**Before.** The same battery with `--counter corpus/evidence/round75/c2-count.py` prints
`C2_BATTERY=FAIL bogus_rejected=2/6 positive=1/1 lane=PASS`, exit 1
(`corpus/evidence/round76/controls/before-c2-battery.txt`): negation, magnitude (`161 whitespace
tokens`), comment-only and mid-file blocks each score `C2=PASS checks=4/4`.

**After.** `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS`, exit 0
(`controls/after-c2-battery.txt`) — `610e5655…` v2 counter; the lane leg re-derives
`DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13` and scores `C2V=PASS checks=9/9`.

**Kill rule.** Any bogus fixture accepted, the valid fixture or the lane leg rejected, or a
`C2_BATTERY=` line that is not exactly `PASS bogus_rejected=6/6 positive=1/1 lane=PASS` → C2
honest-stop. Frozen bytes are not amended after scoring.

**Recorded limits.** The fixtures are text-shaped blocks; the counter binds position, polarity,
magnitude and ancestry for this block shape and does not prove the prose's meaning.

## Shared boundaries

No network, no package adoption, no host question presumed answered, no sibling repo or fleet repo
writes other than the round report and L0 appends. Non-author spot-check requested for the SOURCES
admit/reject set; dispatched wave seats are author-lane evidence, not promotion reviewers. Round
shape: one v1 wave of 12 seats (3 executor, 1 scout, 1 scribe, 1 connector, 2 reviewer, 2 critic,
1 mutation-tester, 1 sentinel = 6 attack seats, 50%); L1 holds the canonical planner seat; no
residual call planned; no dead seat replaced.

## Correction — round-76 claims prose

- Appended by round 77, append-only; the frozen bytes above are unchanged.
- Superseded text: the header clause "4 (receipt precision) is honoured by naming the controls
  revision in every receipt". It is false as written — the prefreeze receipts name worktree digests,
  not the controls revision (`corpus/lessons/round-76-verifier-spotcheck.md`, routed defect 3, lines
  160-164). The frozen bytes above are quoted here, never rewritten.
- Corrected fact: the prefreeze receipts name worktree digests, not the controls revision; a
  successor claims file does not repeat the sentence.
- This block is round 77's C2 landing artifact; the counter is
  `corpus/evidence/round77/c3-count.py` (`C3=PASS checks=5/5` at the landing revision).
