# ScoutStreak — round 63 w1 — recurring-weakness streak update

## Findings

1. Current streaks (computed, not claimed): **RW-4 streak=14** (first_in_run=49, i.e. every round
   file 49–62 matches the `forg(e|ed|able|ery)` regex; claimed=14 agrees), **RW-5 streak=0** (no
   round file back from the tip matches its incident-wording regex; last lane match is round 57,
   `round-57.md:46` "landing (tool misroot)"). Tool verdict `WEAKNESS_ROWS=2 FAILING=0`, exit 0 —
   both rows self-consistent and RW-4's routed path exists.
2. **Round 63's C1 shares RW-4 — the forgeable-frozen-counter class — with round 62's C1.**
   Round 62's C1 was the v2 battery/counter against round 61's forgeable `c1-count.py`, and
   round-62 Mistakes row 1 names the class explicitly ("forgeable counter — rounds 49–61 name it:
   `recurring.tsv` RW-4"). Round 63's C1 is the next instrument in that lineage: a planted-defect
   battery (`c1-battery.py`: CLEAN + 15 defect legs + 6 benign legs) whose two null controls are
   exactly the round-62 forgery shapes — `null-pass.py` (do-nothing, `DEFECTS=0/15`) rejected by
   the defect legs, `null-diff-oracle.py` (forger, `BENIGN=0/6`) rejected by the benign legs,
   `null-selfreport.py` also rejected; 15 of 16 mutants killed, M11 survives as an equivalent
   mutant (named gap).
3. What the round's frozen counters do to the streak:
   - **C1 battery**: keeps the class *named and live* (streak extends to 15 if the round-63 lesson
     writes `forg*`, INFERENCE — the frozen claims file itself names forgers, the M11 survivor and
     the null controls) while *closing*, for the preflight capability, the two cheapest forgery
     shapes round 62 demonstrated. It cannot retire the class: M11 is a declared equivalent
     mutant, the battery never runs G08, and gate names on `GATE` lines are unchecked (named
     limits).
   - **C2 counter**: structural — TRIO/ROWS/QUOTES/COVERAGE/CLAIMS/ECHO/LIMITS/PROBE/MAP/CENSUS
     with git-version binding and `--config`; 21 FAIL variants include fabricated, cross-row and
     uncited quotes, but the `non-sequitur` control PASSES (named limit). Entailment stays a
     reader's check, so C2 likewise extends the class's exposure record without closing it.
   - Net: both instruments push RW-4's streak forward as *exposure handled*, not exposure closed;
     the row retires only when a round's lesson stops naming forgeability, unreachable this round
     given the declared M11 and non-sequitur limits.
4. RW-5 stays a watch row: quiet 5 rounds (last hit r57), and this round gives the class fresh
   surface (the C1 tool contract's "no write outside `--work`", the battery's variant copies) —
   carry it unchanged with claimed 0.

## Evidence

- Tool read first (`corpus/evidence/round53/weakness-streak.py`): streak = consecutive newest
  `corpus/lessons/round-N.md` / `round-N-verifier-spotcheck.md` files whose text matches the row
  regex (case-insensitive); exit 1 on claimed≠computed or a streak≥3 row with a missing routed
  path.
- Command run (scratch created, TMPDIR pointed at it, removed in the same shell — no residue):
  `TMPDIR=/fast/scratch/hyaku/chousa-r63/ScoutStreak python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/weakness-streak.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --table /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round62/recurring.tsv`
  →
  `OK   RW-4 streak=14 claimed=14 first_in_run=49 routed=corpus/evidence/round53/c1-supplement.py frozen counter forgeable — exposure naming at the tip (supersedes RW-1; claimed re-based in round 62, rounds 49-62)`
  `OK   RW-5 streak=0 claimed=0 first_in_run=- routed=- stray write outside scratch — incident wording (supersedes RW-3; sweep and check names excluded)`
  `WEAKNESS_ROWS=2 FAILING=0` ; `rc=0`.
- Routed-path existence: `corpus/evidence/round53/c1-supplement.py` present (glob, 1 hit).
- RW-5 last lane naming: `grep -n` class hits in `corpus/lessons` end at `round-57.md:46`
  ("landing (tool misroot)"); earlier hits r27, r30, r33, r45, r46, r52 — none after r57, hence
  streak 0.
- Class lineage: `corpus/lessons/round-62.md` Mistakes row 1 "forgeable counter — … rounds 49–61
  name it: `recurring.tsv` RW-4"; round-63 frozen `claims.md` C1 controls (`null-pass.py`
  `DEFECTS=0/15`, `null-diff-oracle.py` `BENIGN=0/6`, M11 equivalent-mutant survivor) and C2 named
  limit ("entailment is not machine-checked … `non-sequitur` … PASSES").
- Battery docstring read (`c1-battery.py:1-43`): CLEAN/DEFECTS/BENIGN leg structure as claimed;
  no instrument was run beyond the streak tool (not this item's scope).

## Proposed new `recurring.tsv` rows (literal tabs)

Regexes are deliberately unchanged so streaks stay comparable round over round; only the label,
routed path and claimed streak move.

```
RW-4	frozen counter forgeable — exposure naming at the tip (supersedes RW-1; re-based in round 62; rounds 49-63; round 63's C1 planted-defect battery rejects the do-nothing (null-pass DEFECTS=0/15) and diff-oracle (null-diff-oracle BENIGN=0/6) forgeries; M11 equivalent mutant and C2's non-sequitur limit keep the class live)	forg(e|ed|able|ery)	corpus/evidence/round63/c1-battery.py	15
RW-5	stray write outside scratch — incident wording (supersedes RW-3; sweep and check names excluded; quiet since round 57)	misroot:|Class: misroot|tool misroot|wrote\s+(its|their|two|86)[^|\n]{0,60}fleet root|copied back: [1-9]	-	0
```

Conditions and alternatives for the L1:

- RW-4 `claimed=15` holds only if the round-63 lesson or its verifier-spotcheck matches
  `forg(e|ed|able|ery)` (INFERENCE: the frozen claims file and the wave's reviews of the M11 gap
  and the null controls make that near-certain, but the tool counts lesson files, not claims). If
  the lesson never writes `forg*`, land the row with `claimed=0` — the class retires.
- RW-4 routed path: `corpus/evidence/round63/c1-battery.py` (exists) is proposed as the class's
  current instrument; keeping the incumbent `corpus/evidence/round53/c1-supplement.py` (also
  exists) is equally valid — the tool only checks existence at streak≥3.
- RW-5 `claimed=0` holds unless a round-63 lesson records a stray-write/misroot incident; any
  incident flips the computed streak to 1 and the row must say 1.

Report: .ufo/waves/round-63/w1/ScoutStreak.md

VERDICT: STREAK_RW4=14 new_rows=2
