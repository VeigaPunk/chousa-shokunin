# Round 79 verifier spot-check — chousa (closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-05T01:12:44Z against lane tip
`acca24498b8259d179db144a8bb2d44c0935e2c1` (branch `master`, local == remote, `ahead=0 behind=0`,
`head=detached`, `untracked=1`), base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`, prefreeze
instruments/controls/repairs `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`, claims freeze
`b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`. Report `.ufo/reports/round-79/chousa.md`, committed in
the fleet repo by the lane identity (`chousa-shokunin <chousa@shokunin.local>`, fleet commit
`6448ea4aef51ec7ea1a84750e044813e168038bb`), contained in `origin/main` and `origin/master`.
Dispatch digest copied from the mutable `.ufo/watchdog.log` (lines 2582 and 2599 at read time):
`2026-11-04T21:04:34-03:00 launch chousa round=79 pgid=289331 driver=hyaku-inline attempt=1`;
`2026-11-04T21:52:12-03:00 complete chousa round=79; hyaku-inline attempt=1`.

This closure is non-author: it wrote nothing in the lane except this file. No sibling gate or
self-test was executed; under PROTOCOL §Gate standard (Closure consequence) every lane-owned verdict
below is **committed-evidence verified**, and the before→after deltas are re-derived by plain
git/grep/sha256/regex measurements over committed bytes that this closure ran itself. Three
read-only reviewer seats were not needed: the lane's own wave retained a receipt for every point
this closure had to re-check, and every check below was run directly.

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| lane pushed, nothing outstanding | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=acca2449… remote=acca2449… ahead=0 behind=0 head=detached tracked=0 untracked=1` | PARTIAL (see D2) |
| no uncommitted round work | `git -C <lane> status --porcelain` | `?? corpus/evidence/round79/controls/selfcheck2-after-landing.txt` | **FAIL** (D2) |
| report authored by the lane identity | `git -C <fleet> log --format='%an %ae %H %s' -- .ufo/reports/round-79/chousa.md` | `chousa-shokunin <chousa@shokunin.local> 6448ea4a… round-79: chousa report (hyaku sweep: L1 returned without committing; attribution defect)` | PASS on identity; attribution defect D1 |
| report is pushed in the fleet repo | `git branch -r --contains 6448ea4a…` | `origin/main`, `origin/master` | PASS |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN'` on the report; `grep -cE '^- \`\[~\]\`'`; `git show acca2449:SHONEN.md \| grep -cE '^- \[[ x~]\]'` | heading at line 176; four `[~]` rows; `SHONEN.md` holds four boxes | PASS |
| cited commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> master` for `e2bf2bbb`, `b58a02db`, `acca2449` | three of three `ancestor=yes` (tested against `master`, never `@{u}`; HEAD is detached) | PASS |
| the landing commit is cited by hash | `grep -oE '\b[0-9a-f]{7,40}\b' .ufo/reports/round-79/chousa.md` | no `acca2449…` token; lines 6 and 119 carry the literal `LANDING` | **FAIL** (D3) |
| report sections, in order | `grep -nE '^## '` | lines 12 Work performed, 113 Landed changes, 121 Before → after measurements, 138 Sources & frontier, 160 Trend verdicts, 176 SHONEN — template order | PASS |
| report lands after the lane commit | report committer `2026-11-04 21:52:10 -0300` vs landing committer `21:50:32 -0300` | report is 98 s later and 2 s before the driver's `complete` line | PASS |
| prompt carries the template contract | rendered `templates/round-prompt.md` with the chousa substitutions (`chousa`, `79`, fleet root, lane axes, `chousa-shokunin`) compared to `.ufo/prompts/chousa-round-79.md` | the rendered template is a **byte prefix** of the dispatched prompt (8 408 chars, `startswith` true); the §6 hyaku addendum follows at char 8 408 | PASS |
| L2 floor and round band | `w1-spec.json` `items`, `w1-results.json` `seats`, `scripts/hyaku/ufo-wave-policy.json` | 12 seats in one v1 wave; policy `waveMinLanes=8 waveMaxLanes=16`; roles executor 3, scout 1, scribe 1, connector 1, reviewer 2, critic 2, mutation-tester 1, sentinel 1 → attack 5/12 = 41.7 % | PASS |
| godspeed lead on every seat | first line of each of the 12 spec item prompts | 12/12 begin `You are a Godspeed-enabled subagent.` (the host's directive form) | PASS |
| no conflicting L2 route map quoted | `MISSION.md` §L2 concurrency vs the addendum's route lines | MISSION states bucket classes only (heavy-reasoning / fast-execution / economy); the addendum's alias map is the operator's live `task.agentModelOverrides` table, which MISSION does not contradict | PASS |

Defects and observations (all status-neutral; none is a marker predicate):

- **D1 — the report was swept, not landed by its author.** The report's own subject says "L1
  returned without committing; attribution defect". The commit carries the lane identity, so the
  report is landed (a swept report is still landed; history is never rewritten to fix attribution),
  but the lane-round did not land its own record. Recorded, not repaired.
- **D2 — one uncommitted lane file, cited by the report.** `corpus/evidence/round79/controls/`
  `selfcheck2-after-landing.txt` (402 bytes, mtime 21:50, `REV=acca24498b8259d179db144a8bb2d44c0935e2c1`,
  `SELFCHECK2=PASS unresolved=0/3`, `# exit: 0`) is untracked. The report's C2 row cites it as the
  landing re-measure, so that pointer is not durable at closure and the "no uncommitted round work"
  clause fails. The receipts that are committed (`selfcheck2-after.txt`) carry `REV=worktree`.
- **D3 — the landing commit is a placeholder.** Report lines 6 and 119 read `LANDING`; the landing
  hash `acca2449…` existed 98 s before the report was committed. Two real hashes
  (`e2bf2bbb…`, `b58a02db…`) are cited, so this is a defective report, not a completion marker.
- **D4 — the LOG entry contradicts the report, SCORECARD and lesson on C2.** `LOG.md` §Round 79
  says "C2's kill rule names the hollow repair and the newer-block window; both are refused", while
  the report, the SCORECARD row and the lesson all record the kill rule **firing** on the
  duplicate-116 input (`R79CriticA/selfcheck2-duplicate116-head.txt` prints `SELFCHECK2=PASS
  unresolved=0/3` exit 0). A falsified sentence in an append-only file needs a named correction
  entry in the next round.
- **D5 — a mislabelled QUALITY block.** Criteria 150–151 are round-79 wave findings but sit under a
  `## Round-80 addition` heading, while 149 sits under `## Round-79 addition`
  (`git diff ee70e6df acca2449 -- corpus/QUALITY.md`). A reader taking the heading as the round of
  record is misled; round numbers are a lane-claim surface.
- **D6 — revision binding of the control receipts.** The C1 receipts name only
  `BATTERY_PATH`/`BATTERY_SHA256`, not the lane revision measured (§Gate standard: "a verdict names
  the revision it was measured against"); the revision is asserted by `claims.md`, not by the
  receipt. The C2 after receipt names `REV=worktree`, and its landing replacement is D2's untracked
  file. This is the round-78 routed defect 9 class one layer out.

## 2. Claim re-checks (step 2)

Two claims, frozen in `corpus/evidence/round79/claims.md` in the freeze commit `b58a02db` before any
seat scored. Both frozen predicate lines hold on the committed bytes; **both frozen kill rules
fired**, and the lane says so in its report, its SCORECARD verdict block and its lesson (not in its
LOG entry — D4). Each before→after below is either **re-measured** by this closure with a plain
command over committed bytes or **evidence-verified** on the committed receipt (the lane's gates
were not executed).

### Instrument identity (my own measurement, `git show <rev>:<path> | sha256sum`)

| instrument | controls `e2bf2bbb` | landing `acca2449` | `claims.md` |
|---|---|---|---|
| `corpus/evidence/round79/matrix-battery-v6.py` | `bb91406e9130d9a1…42a61e1d` | same | same |
| `corpus/evidence/round79/forge-battery.py` | `5761edc5c0123211…4fc936` | same | same |
| `corpus/evidence/round79/derivative-check.py` | `af6fbe722c92096a…35397bc1` | same | same |
| `corpus/evidence/round79/selfcheck-v2.py` | `b99ccee5b20bb29c…f88ffeed2` | same | same |
| `corpus/evidence/round79/selfcheck-control.py` | `00cf811a686e885d…eb9f4499d` | same | same |
| `corpus/evidence/round79/forgers/a8-v5-salt-normalizer.py` | `65f590afaa6cf88f…d6373c953` | same | same |
| `corpus/evidence/round79/forgers/a9-v6-wrapper-normalizer.py` | `851222ed6fff9c83…be6b306c5` | same | same |
| `corpus/evidence/round78/matrix-battery-v5.py` (the subject C1 supersedes) | — | `5545a4718690a80e…032b5af0` | same |
| `corpus/evidence/round78/selfcheck.py` (the counter C2 supersedes) | — | `f5acdd825ab7dcaf…2837bf9af` | same |

No instrument moved between the controls commit and the landing, and `git diff --name-only
e2bf2bbb acca2449 -- corpus/evidence/round79/controls/` prints **0** files: the frozen receipts are
the landed receipts. The only post-controls edit under `corpus/evidence/round79/` is `claims.md`'s
own controls-hash sentence, which landed in the freeze commit itself (`git diff e2bf2bbb acca2449 --
corpus/evidence/round79/claims.md` → 2 insertions, 3 deletions, all in the header paragraph).

### C1 — operability (lowest scored non-retired axis; the historical numeric 3/10 held)

Mechanism delta re-derived from committed bytes (plain `grep -n`):

| property | v5 at `ee70e6df` | v6 at `acca2449` |
|---|---|---|
| subject copy | `:179 def salted_copy(…)`, `:194 name = "_r78" + secrets.token_hex(6)` — the salt is source text written into the copy | `:184 _drop_docstrings`, `:203 _rename`, `:126 exec(_m.loads(_b.b85decode({payload!r})), …)` — no source text, a marshalled payload in a wrapper |
| recoverable by a four-line normalizer | yes (round-78 `a8` deletes the `_r78<hex>` family) | no textual remainder to strip (round-79 `a9` hashes the empty string) |

Receipts (evidence-verified, §Gate standard):

| side | receipt | observed |
|---|---|---|
| before (`ee70e6df`, v5 `5545a471…`) | `corpus/evidence/round79/controls/forge-battery-before-v5.txt` | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1`, `# exit: 1`; `a8-v5-salt-normalizer rc=0 … verdict=FORGED`, the other five REFUSED/DETECTED, positive `ACCEPTED` |
| after (v6 `bb91406e…`) | `controls/forge-battery-after-v6.txt` | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`, `# exit: 0`; `a8 … verdict=REFUSED`, positive `ACCEPTED` |
| supporting measurement | `controls/derivative-before-v5.txt` → `controls/derivative-after-v6.txt` | `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096` exit 1 → `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` exit 0 |
| independent 40-byte re-measure (seat, committed) | `.ufo/waves/round-79/w1/R79ReviewA/receipts/maxwin.out` | `MAXWIN_SUBJECTS_DERIVATIVE40=0/13`, every subject `maxwin=23`, `EXIT=0`; the 23 shared bytes are the shebang line |

The battery's own predicate line re-read from a seat receipt, not re-executed:
`R79ExecA/c-battery-v6.txt` and `R79CriticA/a10-receipt.txt` both carry
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` at `# exit: 0`.

**Kill rule fired — verified from the receipt and from the forger's committed source.**
`R79CriticA/a10-receipt.txt` reaches `BATTERY=PASS forgers_rejected=11/11 positive=2/2
oracle=REJECTED`, `RECEIPT_LINES=113`, `# exit: 0`, and the committed
`R79CriticA/a10-payload-decode.py` is what it says it is: it regexes the wrapper's
`b85decode('<payload>')` literal, `marshal.loads` it, collects the code object's string constants
and identifies the subject by Jaccard against a statically built table — no execution, no scoring,
and re-emission preserves every literal, so renaming cannot defeat it. `R79ExecC`'s
`matrix-structure-identity.py` is the same channel one step further: `BATTERY=PASS … EXIT=0` on
**v5 and v6** (`receipt-v5-structure-matrix.txt`, `receipt-v6-structure-matrix.txt`), while its
one-integer control prints `LOADER_MATRIX=0/12 MATRIX=FAIL` (`control-semantic-altered-subject.txt`),
i.e. an identity lookup, not an evaluator. C1's frozen kill rule says "if **any** forger is FORGED"
while its predicate counts six, so **C1 does not verify as written** — the claim's target sentence
(the textual channel) and its kill rule (a universal clause) name different sets, which is the
round-78 routed defect 1 shape recurring and is carried by QUALITY 151.

Do-nothing control: at the base the only battery on disk is v5, whose receipt is `handled=5/6` at
exit 1 with `a8` FORGED, and its copies are 13/13 textual derivatives. A round that does nothing
cannot reach the target.

### C2 — calibration (sourced on S197)

I re-derived the three classes with plain reads over committed bytes (no execution of the lane's
counter), then compared with the committed receipts.

| class | base `ee70e6df` | landing `acca2449` |
|---|---|---|
| S1 registry cell parity | `## Gates` header 8 cells, row 168 **7** cells (my own cell splitter over `git show`) → unresolved | row 168 still 7 cells (append-only), `correction: SKILL.md:168 cells=7 digest=e6e751ec67878243` present → resolved |
| S2 QUALITY pointers | criterion 116 body cites `corpus/evidence/round59/claims.md` in backticks; `git cat-file -e ee70e6df:corpus/evidence/round59/claims.md` → rc 1 (absent) | criterion 116 is untouched (append-only) and still carries that token; criterion 149 carries `supersedes: 116 digest=ae134338138ad3e0` and names the path only in prose, so the committed landing receipt prints `missing=[116] superseders={116: [149]} unresolved=[]` → resolved by the digest superseder, not by erasing the defect |
| S3 stranded `## Mistakes` row | `corpus/lessons/round-77.md` line 73 sits under `## Boundaries` (my own section walk) | `erratum: round-77.md:73 digest=7f2d54a7eb33df54` present, filed bytes untouched → resolved |

**My independent digest re-derivation** (`sha256(text)[:16]` over the named bytes, computed by this
closure with its own script, not by the counter):

| repair line | digest it carries | digest I computed | source |
|---|---|---|---|
| `correction: SKILL.md:168` | `e6e751ec67878243` | `e6e751ec67878243` (`SKILL.md` line 168, rstripped) | `git show acca2449:SKILL.md` |
| `supersedes: 116` (criterion 149) | `ae134338138ad3e0` | `ae134338138ad3e0` (criterion 116 body at `ee70e6df`) | `git show ee70e6df:corpus/QUALITY.md` |
| `erratum: round-77.md:73` | `7f2d54a7eb33df54` | `7f2d54a7eb33df54` (line 73 of `corpus/lessons/round-77.md`) | `git show acca2449:corpus/lessons/round-77.md` |

So the three repairs are bound to the bytes they name, not asserted from memory.

Receipts (evidence-verified): `controls/selfcheck2-before.txt` → `SELFCHECK2=FAIL unresolved=3/3`
exit 1 at `REV=ee70e6df…`; `controls/selfcheck2-after.txt` → `SELFCHECK2=PASS unresolved=0/3` exit 0
at `REV=worktree` (D6); the untracked landing re-measure (D2) prints the same PASS at
`REV=acca2449…`. Controls: `controls/selfcheck-control-before.txt` →
`CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2` — the predecessor prints PASS on both
round-78 false greens and the successor refuses both.

**Kill rule fired — verified from the receipt and from the committed source.**
`R79CriticA/selfcheck2-duplicate116-head.txt` (tree: HEAD `b58a02db` + a newer
`## Round-<n> addition` block re-using criterion number `116.`) prints
`CHECK S2-quality-pointers ok … superseders={} unresolved=[]` and `SELFCHECK2=PASS unresolved=0/3`
at `# exit: 0`, and `corpus/evidence/round79/selfcheck-v2.py:146` reads `out[current] = [line]`, so
the later block's body replaces criterion 116's and the live dead pointer disappears from the audit.
Independently `R79ReviewB/05-dupid-v2.txt` prints the same PASS on a mirror. Two further inputs of
the same class: a blank line before the malformed Gates row
(`R79ReviewB/07-blankwindow-no-repair-v2.txt`) and a stranded `## Mistakes` row whose first cell is
the literal word `class` (`R79ReviewB/08-stranded-probes-v2.txt`). C2's frozen kill rule names
exactly "a newer block hides an earlier criterion from the audit", so **C2 does not verify as
written**; QUALITY 150 carries the three audit-window gaps.

Do-nothing control: without the successor counter and the digest-bearing repairs the same bytes
print `SELFCHECK2=FAIL unresolved=3/3` at exit 1, and the predecessor prints PASS on the hollow
mirror — a do-nothing round cannot reach the target.

## 3. Discernment spot-check (step 3) — I am the named non-author reviewer

Sampled all three of the round's `## Gate` decisions (two admits, one reject); every source was
re-opened at the revision the row pins.

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S196 (own-work B) | admit, mined; grounds C1's target | `git show ee70e6df:corpus/QUALITY.md`, line 1056 = criterion 147 opening bold sentence: "A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt." — **verbatim, but 27 words** (`wc -w`), not the 25 the lesson states | **agree on the decision; disagree on the record** | the quote is real, on the stated line, and grounds C1's target (a requirement produced by round 78's own falsification, not a measurement of the successor), so the admit stands — but 27 words breaches the ≤25-word bound and the lesson's "25 words, `wc -w`" is false; the row's anchor line is correct |
| S197 (own-work B) | admit, mined; grounds C2's target | `git show ee70e6df:corpus/QUALITY.md`, line 1054 = criterion 146 opening bold sentence, verbatim; **25 words** (`wc -w`), lesson states 24 | **agree** | the quote is on the stated line, inside the bound (exactly 25) and grounds the successor requirement; only the stated count is off by one |
| S198 (own-work C) | reject, kept with reason and flip | `git show 3eb4a3ca:.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` — the file is **11 lines**; `grep -c "audit window is the last"` on it → **0**, and the same grep over `corpus/` and `.ufo/waves/round-78/` finds the string only in the round-79 lesson itself | **agree on the decision; disagree on the record** | rejecting a receipt that prints a predicate as a *source about verification method* is the right taste call (it is the counter's own evidence, the S195 class), and the flip is actionable — but the lesson's "located quote" is a paraphrase of the predecessor's source (`corpus/evidence/round78/selfcheck.py:138`), not a quote of the cited receipt, and the row's "wave file lines 1-20" overstates an 11-line file |

The round's own scribe seat found all three of these (`R79ScribeA.md:215-250`,
`R79ScribeA/draft-mistakes-rows.md:60-110`, each with the command and its output, including the
recommended 13-word replacement quote) and the landed lesson carries none of the corrections, no
`## Mistakes` row for the class and no criterion behind it — routed as defect 1 below.

Registry re-check (my own census, not the lane's): rows **195 at `ee70e6df` → 198 at `acca2449`**
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), tiers A 123/123, B 54 → 56, C 18 → 19;
statuses mined 156 → 158, queued 19, rejected 20 → 21; `git diff ee70e6df acca2449 --
corpus/SOURCES.md` shows three added rows and no edited cell. Malformed rows `NF!=13` → **0**;
duplicate ids → **none**; enum/tier-inflation violations → **none**; `mined` rows whose `used-by`
paths do not exist → **none**. `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa` re-run by this closure → `EXIT=0`, `ok` on
`corpus/SOURCES.md`, the same five pre-existing `W04` duplicate-url warnings
(S051/S053/S073/S074/S075).

## 4. Axis and trend verdicts

`git diff --numstat ee70e6df acca2449` over the owned surfaces: `LOG.md` 42/0, `SCORECARD.md` 43/0,
`SKILL.md` 4/0, `corpus/QUALITY.md` 9/0, `corpus/SOURCES.md` 3/0, `corpus/lessons/round-77.md` 2/0 —
every one append-only. Round total `363 files changed, 21179 insertions(+)`, **zero deletions**.
`PROVINCE.md`, `corpus/README.md` and `corpus/knowledge/` are untouched (0 files in the diff).

| axis | verdict | basis |
|---|---|---|
| operability (C1) | **improved** | measured, not asserted: the six enumerated forgery channels go `handled=5/6` exit 1 → `handled=6/6` exit 0 on the same forged bytes, the textual-derivative measurement goes `13/13 MAX_WINDOW=4096` → `0/13 MAX_WINDOW=23` (independently re-measured by `R79ReviewA`'s `maxwin.out`), and the positive control is still ACCEPTED. The claim as written does not verify (its kill rule fired on the payload-decoding forger) and no numeric score moved — the historical 3/10 is held — so this is a narrow artifact delta, not a capability gain: the round also shows the battery is fully forgeable through the payload channel on **both** batteries |
| calibration (C2) | **improved** | the three routed self-assessment classes resolve, re-derived by this closure 3/3 → 0/3 over committed bytes (cell parity, pointer resolution, heading position), and the three repair digests recompute byte-exactly to what the repair lines carry. The counter that was to certify them is falsified for the duplicate-identifier window, so the improvement rests on direct inspection plus the digest binding, not on the lane's PASS line |
| depth | **unchanged** | no `knowledge/` entry, no decision-table row, no domain fact added; the registry gained two gate rows and a correction line |
| freshness | **unchanged** | no drift pin added or re-verified beyond the instruments' own digests; every `SOURCES.md` `recheck` cell stays `on-release`, none advanced |
| coverage | **unchanged** | no province surface added or moved; `PROVINCE.md` untouched |
| adjacency | **unchanged** | `R79ConnectorA` compares the sibling rows it names (tsukuroi 683ae456, kasegi c1051749, souji d05a0001, kama 3ff23da3, mado a722c604) and absorbs none; no sibling file touched |

| trend | verdict | evidence |
|---|---|---|
| expansion | **unchanged** | no admitted `knowledge/` entry, no capability row (`SCORECARD.md` capabilities table untouched), no `corpus/README.md` or `PROVINCE.md` ground. The three registry rows are curation (two admits, one rejection); a rejection is taste, not expansion |
| quality | **improved** | a weaker criterion is superseded by a stronger one and the supersession is digest-bound (149 supersedes 116, `ae134338138ad3e0` recomputed here), both round-78 false greens are closed with before receipts and controls (`v1_false_greens=2/2 v2_refusals=2/2`), QUALITY 150–151 carry the surviving gaps, and every change to a frozen artifact is append-only (numstat above, zero deletions). Nothing was weakened: the surviving payload channel is measured and recorded, never certified sound |
| discernment | **improved** | this non-author spot-check agrees with the gate on all three admit/reject decisions, and the round falsified both of its own frozen claims inside the round with independent reproductions (`R79CriticA` `a10` + duplicate-116; `R79ReviewB` 05/07/08; `R79ExecC` structure matrix) and turned the disagreements into QUALITY 150–151 with five mined mistake rows. Caveat carried, not smoothed: the three grounding-record defects above were found by the lane's own seat and left unlearned, and are routed as defect 1 — the decision-level agreement is what this verdict rests on, as in rounds 76–78 |

## 5. Routed defects (owner chousa, next round)

1. **The Gate's grounding records for S196/S197/S198 are defective and the round's own
   corrections were not applied.** S196's quote is 27 words while the lesson states "25 words,
   `wc -w`" (over the ≤25-word bound); S197's is 25 while the lesson states 24; S198's "located
   quote" occurs nowhere in its cited 11-line receipt and its anchor span (lines 1-20) overstates
   the file. `R79ScribeA` filed all three with commands and a recommended 13-word replacement. Fix
   next round: land the corrections as new rows whose `teaches` opens `supersedes S196 —` /
   `supersedes S198 —` (rows are append-only), record the old→new counts in the lesson, and add a
   `QUALITY.md` criterion that a located quote is re-opened, `grep -c`'d at the named location and
   `wc -w`'d before the row is written.
2. **`corpus/evidence/round79/controls/selfcheck2-after-landing.txt` is uncommitted** although the
   report cites it as C2's landing re-measure. Commit it (or state in the next lesson why it stays
   untracked) and make the landing re-measure a committed receipt next time.
3. **The report's `LANDING` placeholder.** The filed report cannot be rewritten; land an erratum
   naming `acca24498b8259d179db144a8bb2d44c0935e2c1` as the landing commit the two `LANDING` cells
   refer to.
4. **`LOG.md` §Round 79's outcome sentence contradicts the report, SCORECARD and lesson on C2's
   kill rule.** Append a named correction entry (append-only, never a rewrite) stating that the
   newer-block window was **not** refused and the duplicate-116 input fired the kill rule.
5. **QUALITY 150–151 sit under a `## Round-80 addition` heading** while 149 sits under
   `## Round-79 addition`, though all three are round-79 wave findings. Record the mislabel in the
   next lesson and keep one heading convention per round.
6. **Revision binding of control receipts.** The C1 receipts name only the battery path and
   sha256, not the lane revision measured; the C2 after receipt is `REV=worktree`. Adopt the
   lesson's own successor rule — a control receipt names the revision it was measured at — as a
   `QUALITY.md` criterion, and name the revision in every receipt from now on.
7. **Carried, recorded not repaired:** the payload-decoding channel (`a10`) and the
   structure-identity matrix remain full forgeries of both batteries; `a9` is empty in content;
   `RECEIPT_LINES` exposes an append, not a truncation; the `--work`/toolchain legs stay outside the
   frozen predicate; a digest binds a repair line to bytes, not to the truth of its prose. QUALITY
   150/151 and the lesson's instrument-limits section carry them.
8. **Carried from the round-78 closure (still open):** the round-78 registry row's missing
   isolated-fixture self-test (`--selftest` absent from `matrix-battery-v6.py`, `forge-battery.py`,
   `selfcheck-v2.py` — `grep -ci 'selftest|self-test'` → 0/0/0), and `work-contract.py` never
   comparing Case A's matrix exit.

## 6. Operator note

All four `SHONEN` boxes look checkable by a non-author from committed artifacts: box 1 (the `## Gates`
registry rows for v6, the six-forger battery and the v2 counter, plus QUALITY 1–151), box 2 (the
`LOG.md` §Round 79 entry and the round's end-to-end instrument runs under
`corpus/evidence/round79/controls/`), box 3 (three pasteable commands with exit maps in `SKILL.md`),
box 4 (`PROVINCE.md` untouched and `R79ConnectorA`'s non-absorption). Promotion remains
operator-owned; this closure wrote no `[x]` anywhere.

**Closure ruling.** Lane status `ok` (a real report with checkable committed work, cited commits
ancestors of the branch, lane pushed, prompt faithful to the template). `admitted: false` — both
claims fail their own frozen kill rules and the lane says so itself. Verdict
`rejected-honest-stop`: no axis is harmed, both artifacts are measurably better on the channels the
round set out to close, and the falsification — plus the payload channel it exposes — is the
round's honest result.
