ATTACKS: C1 verdict wording — scorecard/capability/gate rows, QUALITY 67, tool docstring, lesson 4–5, frozen-rule drift, false-refusal cost, "improved" vs trade
VERDICT: overclaim (two concrete false survivor/limit statements) + **trade** (axis harm, not net improvement)

## 0. Verified ground truth
- Lane tip `1fc5ed1` archive. `c1-count.py` at tip: `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0 — the claim's counter leg verifies as declared.
- `tools/inference-ground.py` sha256 `244a1897…` = SKILL.md row-pinned value; file unchanged since `980fe43f` (wave-1 fix).
- Diff `a15610a5`→`980fe43f`: +83/−31 lines; the FROZEN rule sentence in `claims.md:33-41` was NOT edited by any commit (confirmed by `git show` of both wave commits touching only the tool). Post-wave-1 changes are refinements of the *work*, not of the sentence.

## 1. Counterexample — "double negation still passes" is now FALSE at tip (overclaim)
Frozen claim (`claims.md:62-64`) and lesson (`round-47.md:110-114`) and SCORECARD (`:2505`) all state double negation still passes (`CritC1Survivors` 3/3b, measured on `a15610a5`).
Tip run, entry quoting affirmed span phrase `the release ships a frozen pool` (S901), correct double-negation bullet:
```
Since `the release ships a frozen pool`, the pool is not unfrozen at release (S901).
```
`python3 tools/inference-ground.py …` → `FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / unfrozen'` + `… / release'`, exit 1.
At `a15610a5` the same bullet emits only the `release` finding (no `unfrozen`) — the `un`-prefix branch (`inference-ground.py:327-330`) refuses `un`+stem even when a negator directly precedes it, so the affirmed-phrase double negation that used to pass now fails. Reason: `un`-prefix check fires before the negator-window logic and ignores any preceding negator.
Impacted: calibration (false refusal), claim wording (survivor list stale), docstring ("no rule widened toward acceptance" is false in this dimension).

## 2. Counterexample — clause-bound look-back widens acceptance (contradicts docstring)
Tool docstring (`:36-39`) and lesson mistake 4 claim "no rule widened toward acceptance of a flip"; the clause bound is presented as a pure over-refusal fix. But it also converts old refusals into passes: a negator in the three words *before* the phrase but outside its line/clause no longer negates it.
Scratch span: `previous list line: no revision is recorded\npool: the release ships a frozen pool of pages`; bullet `the pool is frozen at release` → `GROUND: PASS` exit 0. Under the frozen sentence read literally (negator "among the three span words before it"), `no` sits in that window and the bullet would be refused; under tip's clause-bounded `occurrence_polarity` (`:276-285`) it passes. The lesson itself documents the same flip (mistake 4: `(Unlabelled)` on a previous list line first made r46 fail, then the clause bound restored it). So "no rule widened toward acceptance" is misleading: the look-back scope was *silently narrowed* relative to the sentence, and that narrowing widens acceptance for cross-line negators.

## 3. Understated false-refusal cost — 5/10 is tuning-set, not held-out
- SCORECARD `:2505`: "correct bullets with a negator outside the window are refused (tuning set 5/10 after the wave-1 fix; held-out rate in the round report)".
- `round-47.md:73-75`: "That ten-bullet set was used to tune, so it is not a held-out measure; wave 2's fresh set is."
- Wave-2 `gen-w2-spec.py:73` defines the fresh held-out seat (`HeldOutA`, k/12) — it has not produced a report yet (`w2/` contains only `swarm-registry.json`). The "held-out rate in the round report" does not exist. A 50% false-refusal rate on the *only measured set* is a material precision cost; calling the axis "improved" without a measured rate is premature.

## 4. No overclaim on entailment / D7 closed — but figure-leg reachability overstated
- Verdict text is careful: "NOT entailment … still passes (`CritC1Survivors`)" and lesson says "D7 … narrowed, not closed" — no D7-closure or "refuses every flip" overclaim (b7-combined passes; documented).
- Capability row (`SCORECARD.md:2524`): "refuses … or re-denominate a counts figure against its key" — overstates reachability: lane entries run with `--counts /dev/null` (`SKILL.md:70`, `c3-count.py:174`), so `figure_flip` fires only on fixtures (wave-1 `CritC1Survivors` §3). As a lane capability the figure leg is fixture-only.

## 5. Rule on "improved" vs trade
The counter leg verifies (C1=PASS) and the D7 body that motivated the round now exits 1; nothing pre-existing regressed on the counter. But: (a) the tool refuses 9/10 → 5/10 correctly-reasoned bullets in the only measured set, with no held-out figure yet; (b) the post-fix semantics silently diverge from the frozen sentence (clause-bound negation, `un`-prefix branch) in both directions; (c) a documented survivor class (double negation) is now refused. That is a real capability gain minus a real, unmeasured precision cost — **a trade (axis harm on operability's usability side)**: the verdict should be "improved with a measured-but-held-out false-refusal cost" or "trade", not bare "improved"; the survivor statement "double negation … still passes" must be corrected to "double negation passes only when no `un`-prefixed scope word is used".

Commands: `git archive 1fc5ed1`; `c1-count.py`; `inference-ground.py` on 3 scratch entries; `git log/diff a15610a5..980fe43f`; grep of lessons/LOG/scorecard for held-out. No installs, no fetch; scratch `/tmp/chousa-r47w2-CritC1Claim/` removed at close.
