# Round 75 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed round 75: before `8022f72c889c904b5657d52c7f29e1643392a216`, freeze A `43a7a0db52c8aabdf32735f58e09610e05200e79`,
landing `ad57562215a1a729e6ab8c7e13ef713c4e5843d1`, final tip / lane HEAD `e515c9624278cef906671d76188cb44e2a3445fe`.
This review neither improves the authored round nor re-admits any earlier round.

## Conformance and disposition

Status **ok**: a landed report with checkable work, not a marker. Admission **true**, verdict `admitted`: both frozen
claims verify on their predicates and no owned axis is harmed.

- `git log --format='%an %H' -- .ufo/reports/round-75/chousa.md` (fleet repo) returned
  `chousa-shokunin 8b96e7e3d1796e296b71db8a5132d935a97adb2f`; the commit is 2026-11-04 16:28:13 -0300, after the lane
  tip 16:27:16, and adds only the 163-line report. It is an ancestor of the fleet `origin/master` tip `b8fce783…`.
- `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin` returned
  `branch=master local=e515c962… remote=e515c962… ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` was empty before this file was written.
  `git ls-remote origin refs/heads/master` returned `e515c962…`, so the round is pushed.
- `git merge-base --is-ancestor <hash> master` exited 0 for the before, freeze, landing and final-tip hashes. Ancestry was
  tested against branch `master`, never detached HEAD or upstream shorthand.
- The report carries `## SHONEN` once with four `[~]` rows, matching the four boxes in `SHONEN.md`; the lane wrote no `[x]`.
- The dispatched prompt `.ufo/prompts/chousa-round-75.md` is committed (`04af487a…`, 15:58:47, before the 15:58:49 launch)
  and carries the round-level contract — mission/axes §1, L2 floor ≥8 in one batched dispatch §3, commit-then-push §5,
  push scope §5, L0 channel §5 — plus the five child-lane items: report path and sections §4, report-lands-last with the
  pushed-hash citation §addendum 4, the `SHONEN` heading rule §4, and the explicit write scope at §addendum 3.
- Driver digest from `.ufo/watchdog.log`: `2026-11-04T15:58:49-03:00 launch chousa round=75 pgid=1466307
  driver=hyaku-inline attempt=1`; `2026-11-04T16:28:42-03:00 complete chousa round=75; hyaku-inline attempt=1`.
- Wave: `.ufo/waves/round-75/w1-dispatch.json` counts `spawn=10 total=10` under policy band 8–16; `w1-results.json`
  carries 10 settled seats — 3 executor, 2 reviewer, 1 each scout/scribe/connector/critic/mutation-tester (4 attack seats,
  40%), 0 residual, no dead seat. L1 held the canonical planner seat.

## Claim re-checks

No sibling gate was executed (PROTOCOL §Gate standard, Closure consequence). **C1 is committed-evidence verified**;
**C2's arithmetic is independently re-measured over committed bytes**, with its counter verdict evidence-verified.

### C1 — operability (lowest non-retired axis; numeric score deliberately held at 3/10)

Frozen predicate: `python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round75/loader-matrix-v2.py
--work DIR` exits 0 and prints exactly `BATTERY=PASS forgers_rejected=5/5 positive=2/2`.

| re-check | command / committed input | observed output |
|---|---|---|
| instrument identity at the tip | sha256 of `corpus/evidence/round75/{loader-matrix-v2,matrix-battery,ref-counter,c2-count}.py` from `git show e515c962:<path>` | `95bdd493…`, `c35e937b…`, `909987ce…`, `bf0250e7…` — equal to the digests pinned in `claims.md` and the receipts |
| do-nothing control | `controls/before-battery-r74-matrix.txt` (r74 matrix `97963825…`) | `BATTERY=FAIL forgers_rejected=2/5 positive=2/2`, `EXIT=1`; order-oracle, diff-only and naive-grep each `9/9` ACCEPTED |
| after at the landing | `controls/after-battery-at-landing.txt` (v2 matrix `95bdd493…`) | `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, `EXIT=0`; order-oracle `5/12, 4/12` and diff-only `9/12, 9/12` REJECTED; positives `12/12` twice |
| stability | `controls/battery-stability-r75.txt` | three further runs all `BATTERY=PASS forgers_rejected=5/5 positive=2/2`; order-oracle `5/6, 2/3, 2/4 /12` |
| blanket-refusal guard | `controls/negative-r73-counter-on-v2.txt` | frozen r73 counter `LOADER_MATRIX=3/12 MATRIX=FAIL`, `EXIT=1` — a known-bad loader is not accepted |
| shuffle is load-bearing | `controls/shuffle-necessity-r75.txt` | 12-entry declared-order oracle `4/12` on the frozen matrix, `12/12` on a fixed-order copy |
| acceptance rule (static read) | `matrix-battery.py:96–130` | positive ACCEPTED only when both runs exit 0 with full marks and PASS; forger REJECTED only when both runs exit 1 with `marks[0] < marks[1]`; battery exits 0 only when 5/5 and 2/2 |
| public path (static read) | `loader-matrix-v2.py:100–143` | 12 cases (unchanged, 3 append, 3 delete, replace-equal, receipt-change, 3 duplicate-heading), `secrets.randbits(64)` shuffle, candidate invoked `--lane --base --rev`, per-case `expected_rc=`/`expected_failed=` |

C1 verdict **improved**: the frozen predicate holds at the reviewed tip, the two forgers the r74 matrix accepted at 9/9
are rejected, and the negative control keeps blanket refusal from being a gain. The claim's rationale sentence
"decidable only from protected-file content" is false as written — four content-blind metadata counters reach 12/12
(`R75Critic` §2–§3) — but the lane recorded the falsification append-only and amended no frozen byte or predicate.
The five-forger battery is a discrimination floor, not forged-freedom.

### C2 — calibration

Frozen predicate: `c2-count.py --lane . --rev <landing> --base 8022f72c…` exits 0 and prints `C2=PASS checks=4/4`,
with the correction block stating the derived counts.

| re-check | command / committed input | observed output |
|---|---|---|
| independent derivation | extract the two `Located quote:` strings from `e515c962:corpus/lessons/round-74.md`, whitespace-split | S182 `16` tokens, S183 `11` tokens; the authored lines record `18` and `13` |
| correction block | `e515c962:corpus/lessons/round-74.md`, lines 42–44 | `## Correction — round-74 quote counts` appears once, states 16/11, names the superseded 18/13; the authored Gate lines are unchanged |
| append-only | `git diff --numstat 8022f72c e515c962 -- corpus/lessons/round-74.md` | `4	0` — no deleted line |
| counter verdict | `controls/after-c2.txt` at the landing | `DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`; `C2=PASS checks=4/4`; `EXIT=0` |
| bytes at the tip | `git diff --name-status ad575622 e515c962` | only five control receipts were added; the lesson and counter are unchanged |

C2 verdict **improved**: the count defect the r74 spot-check routed is corrected append-only with the right arithmetic,
and the corrected values are re-derived rather than asserted. The counter's own limits — presence-test polarity and
magnitude, endpoint-only Q4, no base ancestry — are disclosed and routed below; they do not change the observed block.

## Axis verdicts

`git diff 8022f72c e515c962 -- SCORECARD.md` is additions-only; no score row changed and no capability row was added.
The round diff is 202 files, +11984/−0; `PROVINCE.md`, `SKILL.md`, `corpus/README.md` and `corpus/knowledge/` are
untouched.

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 predicate met; order-oracle and diff-only forgers rejected; negative control retained; score held at the historical 3/10 as declared |
| calibration | improved | C2: 18/13 → 16/11 corrected append-only, `C2=PASS checks=4/4` |
| depth | unchanged | no knowledge entry or externally grounded fact this round |
| freshness | unchanged | no drift surface re-measured; S184–S186 are own-work with `on-release` rechecks |
| coverage | unchanged | `PROVINCE.md`, `SKILL.md`, `README.md`, `knowledge/` untouched |
| adjacency | unchanged | sibling scan read-only by the connector; nothing absorbed |

## Independent discernment spot-check

Re-opened the three `## Gate` sources at the pinned revision; two admits and one reject sampled.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S184 | admit, own-work B / mined | `43a7a0db:corpus/lessons/round-74-verifier-spotcheck.md:73–74` | agree | The two routed defects are verbatim there — a 20-word and a 13-word quote, both ≤25 — and the row's `teaches` is exactly those instructions; `used-by` resolves to `corpus/lessons/round-75.md`. |
| S185 | reject, own-work C / QUALITY 126 as a source row | `43a7a0db:corpus/QUALITY.md:1002` (criterion 126) | agree | The criterion is the bar content is measured against, not an origin of content; the row states a concrete flip. |
| S186 | admit, own-work B / mined | `43a7a0db:.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py:3` and `forge-order-oracle.log:11`; sha256 | agree | Line 3 is the 13-word quote "Never reads --lane bytes nor any repository content. Scores 9/9 on the frozen"; the log line is `LOADER_MATRIX=9/9 C1=PASS`; the file digest `180d1a3d…` equals the r75 frozen copy. The row grounds the r74 discrimination failure, not forge-freedom. |

All Gate quotes for the new rows are ≤25 words (S184: 20/13; S186: 13/2) and verbatim at their named locations; the
access date 2026-11-04 and the pinned revision are present. No URL was fetched because all three are committed paths.

Row census over committed blobs (`^ {0,3}\|\s*S\d{3,}\s*\|`): **183 → 186**; tiers A123/B46/C14 → A123/B48/C15;
statuses mined148/queued19/rejected16 → mined150/queued19/rejected17; `git diff --numstat` on `corpus/SOURCES.md`
is `3	0`, so no earlier row byte changed.

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ exit 0, `chousa ok …/corpus/SOURCES.md`, with only the pre-existing W04 duplicate-URL warnings S051, S053, S073,
S074, S075 — the same five at both ends. No new E or W finding.

## Learning trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | +3 registry rows is curation; no knowledge entry, coverage-map advance or capability row (`git diff --name-status` shows no `corpus/knowledge/`, `README.md`, `PROVINCE.md` or `SKILL.md` change). |
| quality | improved | The r74 lesson's wrong 18/13 counts are superseded by the re-derived 16/11 append-only; QUALITY 135–137 are lesson-cited criteria; the r74 matrix's forge-blindness is repaired with its surviving classes recorded, not certified away. |
| discernment | improved | This non-author spot-check agrees with both admits and the reject; the round's six attack findings became recorded limits and criteria 135–137, and three own mistakes are mined with guards. |

## Routed defects

1. **Owner chousa — C1 rationale and battery coverage.** The frozen sentence "decidable only from protected-file
   content" is false: commit subject, tree ids and byte sizes are stable metadata channels, and four content-blind
   counters reach 12/12. Next round: name the channels in the matrix header and add a metadata-reading subject plus
   the twelve-entry declared-order oracle to the battery's subject set — the shuffle is load-bearing but unobserved by
   the frozen battery.
2. **Owner chousa — the C2 counter is a presence test.** Bind the derivation to the authored bullet/heading, assert
   polarity and magnitude rather than substring presence, require the correction block to be the final section, and
   check base ancestry for Q4. Disclosed in `## Instrument limits`; still an open instrument defect.
3. **Owner chousa — control chronology.** The controls share the freeze commit and precede only the dispatch; the
   sibling precedent (`souji` QUALITY Q120) wants the controls in a commit strictly preceding the predicate freeze.
   Split the next round's controls commit from the claims commit.
4. **Owner chousa — receipt precision.** `controls/after-battery-v2-matrix.txt` names `measured-at=8022f72c…` while
   the instrument was untracked at that moment. The digest makes the bytes recoverable and they land byte-identically,
   but the receipt should name the measured worktree-plus-digest state or be re-run at the freeze commit.
5. **Owner chousa — parser-slip red-before.** `controls/mutation-battery-parser-slip.txt` demonstrates the narrow regex
   in isolation, not the battery command exiting non-clean; the first failing receipt was overwritten before commit.
   Ship the actual red-before battery run, or retain the failing receipt, before the fix counts.

## Operator notes

All four `SHONEN.md` boxes remain `[~]` lane assertions. Boxes 1–3 (SKILL decision tables/checklists, an end-to-end
logged task, executable without oral context) look checkable by a separately scheduled non-author promotion review;
promotion remains operator-owned and no box was marked here. Carried operator questions (external-fetch approval,
historical Windows flock/load, promotion and non-author entailment) remain unanswered and were routed around, not
presumed answered.

Self-evaluation: accuracy 5/5 (claims re-measured from committed bytes; C1 gate outcomes evidence-verified, not
re-executed per protocol); completeness 5/5; clarity 4/5 (the predicate/axis/admission distinction is essential);
actionability 4/5 (five routed defects remain lane-owned); conciseness 4/5.
