# SweepA05 — round 49 w1: a05 / 3/12 mislabel sweep (routed defect 1 of round-48-verifier-spotcheck.md)

Seat: SweepA05 (leaf, godspeed). Lane: chousa. Scope: sweep every mention in the lane repo
(SCORECARD.md, corpus/QUALITY.md esp. criterion 69, corpus/lessons/round-47*.md, round-48*.md,
LOG.md, SKILL.md, tools/inference-ground.py docstring) that reads 3/12 as false refusals or a05
as a correct-but-refused bullet. True figure: 2/12 (p03, p04); a05's refusal by the R47 tool was
correct (round-48 closure ruling (a)). Append-only corrections drafted; no text rewritten.

## 1. Grep commands and outputs

All commands ran from the lane root; repo-wide scan then enumerated-file scan.

```
$ grep -rn -E 'a05' --include='*.md' --include='*.py' --include='*.txt' . | grep -v '^.git/'
```
Enumerated-scope a05 hits (repo-wide scan; full output in tool transcript): none in
SCORECARD.md, corpus/QUALITY.md, LOG.md, SKILL.md, tools/inference-ground.py. In
corpus/lessons/: round-47-verifier-spotcheck.md:39,41,43,46,47,65,74,78,79,87 (the r48
spotcheck itself, i.e. the correction document); round-48.md:71 (deferral, see §3).

```
$ grep -rn -E '3/12' --include='*.md' --include='*.py' --include='*.txt' . | grep -v '^.git/'
```
Enumerated-scope 3/12 hits: corpus/lessons/round-47-verifier-spotcheck.md:29
("exit-level 3/12 incl. a05, an over-refusal of a common construction") and :35
("precision cost measured 2–3/12 false refusals"); corpus/lessons/round-48.md:34 (S095 Gate
block verbatim quote of the same phrase). No 3/12 in SCORECARD.md, QUALITY.md, LOG.md, SKILL.md,
tools/inference-ground.py.

```
$ grep -rn -E 'exit-level' --include='*.md' --include='*.py' --include='*.txt' . | grep -v '^.git/'
```
Hits: corpus/lessons/round-47-verifier-spotcheck.md:29; corpus/lessons/round-48.md:34
(quote); corpus/lessons/round-48-verifier-spotcheck.md:46,78 (correction document itself);
.ufo/waves/round-48/w2/AttackPrecision.md:54,68 (wave-scratch argument, §4).

```
$ grep -rn -E 'over-refusal' --include='*.md' --include='*.py' --include='*.txt' . | grep -v '^.git/'
```
Enumerated-scope hits are all the **C3 path-denylist** topic, unrelated to a05/3/12:
SCORECARD.md:1155,1161,1517,1569; LOG.md:796,1120,1121,1151; SKILL.md:593,614; QUALITY.md:
none; tools/inference-ground.py: none. corpus/lessons/round-47.md:68 is a different probe
(9 of 10 refused), not the 12-set.

```
$ grep -n -E 'HeldOutA|2/12|a05|3/12' SCORECARD.md corpus/QUALITY.md LOG.md SKILL.md tools/inference-ground.py
$ grep -n -oE 'HeldOutA|2/12|a05|3/12|exit-level|over-refusal' SCORECARD.md LOG.md SKILL.md corpus/QUALITY.md tools/inference-ground.py | sort | uniq -c
```
Checked: every `2/12` hit in LOG.md:1488,1790, SCORECARD.md:2286, SKILL.md:106 is the
substring of `12/12` (pass-rate metrics, not refusals). LOG.md:1796 contains `a05` twice —
accurate history + deferral, see §3.

## 2. Hits needing correction (3)

| # | path:line | text (abridged) | correction? | drafted append-only correction sentence |
|---|---|---|---|---|
| 1 | corpus/lessons/round-47-verifier-spotcheck.md:29 | "`HeldOutA` refuses 2/12 correctly-reasoned bullets (exit-level 3/12 incl. a05, an over-refusal of a common construction) vs 0 before" | **YES** — reads 3/12 incl. a05 as false refusals; overcounts by one | "Correction (round 49, append-only; supersedes the parenthetical above): the R47 tool's true false-refusal count on this set is 2/12 (p03, p04); a05's refusal was correct — the bullet denies the affirmed phrase — so 'exit-level 3/12 incl. a05' overcounts the defect class by one (see corpus/lessons/round-48-verifier-spotcheck.md:46,78)." |
| 2 | corpus/lessons/round-47-verifier-spotcheck.md:35 | "precision cost measured 2–3/12 false refusals" | **YES** — range leaves 3 open as a false-refusal count | "Correction (round 49): the precision cost is 2/12 false refusals (p03, p04); the '3' in '2–3/12' counted a05, whose refusal the round-48 closure ruled correct." |
| 3 | corpus/lessons/round-48.md:34 (S095 Gate block) | "…quote: “`HeldOutA` refuses 2/12 correctly-reasoned bullets (exit-level 3/12 incl. a05, an over-refusal of a common construction)”. … The first grounds the measured false-refusal cost" | **YES** — propagates the mislabel into the S095 Gate block | "Correction (round 49, beside the S095 quote): the quoted figure is the propagated error — the true false-refusal figure is 2/12 (p03, p04), and a05's refusal was correct; 'exit-level 3/12 incl. a05' overcounts by one (see corpus/lessons/round-48-verifier-spotcheck.md:46,78). The row's admissibility is unaffected; the quoted claim is not." |

## 3. Checked-clean mentions (no correction)

- SCORECARD.md:2505 — "refused 2 of 12 correctly-reasoned bullets (HeldOutA; the round-46
  tool refuses 0)" → reads the true figure 2/12. :2513 — "the cost is 2/12 held-out correct
  bullets refused" → true figure. :2545 — "CORRECT_BULLETS_PASS=9/12" (pass rate, factual);
  "W2 AttackPrecision.md disputes the a05 label (the prior R47 non-author verdict called it a
  false refusal); re-open a05 in closure before generalizing" → deferral, no endorsement.
- LOG.md:1796 — "W2 AttackPrecision.md disputes the a05 label; the R47 non-author closure had
  treated it as a false refusal. This report asks the current closure to re-open a05…" →
  accurate history + deferral, not a reading of a05 as correct-but-refused.
- corpus/QUALITY.md criterion 69 (lines 689–703) — no `a05`/`3/12`/`exit-level`; framing is
  count-free ("records the false refusals and their cue/window classes"; the R47 tool control
  prints `CORRECT_BULLETS_PASS=9/12` — a pass rate). No correction needed.
- tools/inference-ground.py docstring — no `a05`/`3/12`/`exit-level`/`over-refusal`; Named
  limit is a generic caveat ("A correct bullet can still be refused when… an in-window P2
  negator that semantically scopes to a neighbouring word"), not a claim about a05.
- corpus/lessons/round-47.md:146 — "false refusals **2/12** correctly-reasoned bullets
  (`HeldOutA`)" → already the true figure (vindicated by the closure; AttackPrecision's
  "stale 2/12" charge is the position the closure ruled against).
- corpus/lessons/round-48.md:71 — "W2 AttackPrecision.md disputes a05 as an ambiguous 'correct'
  label (11/12 are unambiguous); the closure must independently adjudicate it" → deferral,
  superseded by the closure; no misreading.
- corpus/lessons/round-48-verifier-spotcheck.md — is itself the correction document; :46
  already states the true figure and :78 is this routed defect.

## 4. Out-of-enumerated-scope occurrences (wave-scratch seat reports; not corrected per scope)

Same grep also found readings of a05 as correct-but-refused / 3/12 as false refusals inside
.ufo/waves/round-48/ seat reports, which the enumeration does not include: w1/Attack31.md:26
("p03, p04, a05 are concrete correct-case false refusals"), w1/Attack27.md:11, w1/Attack28.md:36,
w2/AttackPrecision.md:54,68 (argued the 3/12 count; ruled wrong by the closure), w2/VerifyFrozenClaim.md:25.
These are historical records of the dispute; the closure's ruling supersedes them. Flagged for the
record only.

## 5. Fixture grounding of the judgment

Opened: `corpus/fixtures/inference-ground-r47/spans/S902-1.txt:1` = "the archived copy is dated
at build time; a placeholder value is not an archive link"; `corpus/evidence/round48/precision-count.py:22`
case a05 = quote "the archived copy is dated at build", body "that date is not the copy's build
date". The bullet quotes the affirmed phrase and asserts the date "is not" the copy's build date —
a direct denial; refusal correct (matches round-48-verifier-spotcheck.md:41–47). True false
refusals: p03 (implicit negator `nonexistent`, precision-count.py:14) and p04 (`cannot` outside
window, :15).

## 6. Tooling

None installed (no install expected; read `~/.omp/agent/RULES.md` first). No network/live fetch;
no production file, git index, or jj state touched. Only write: this report.

## VERDICT
Swept a05/3/12/exit-level/over-refusal across the enumerated docs: 3 hits need append-only
corrections (r47 spotcheck :29 and :35, r48 S095 Gate block :34) — true figure 2/12 (p03,p04),
a05's refusal correct; SCORECARD/QUALITY-69/LOG/SKILL/inference-ground.py docstring checked clean.
