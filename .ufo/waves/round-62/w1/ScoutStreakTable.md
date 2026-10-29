# ScoutStreakTable — round 62 w1 — weakness-streak re-registration

Seat: scout (leaf, no subagents). Scope: why `corpus/evidence/round53/weakness-streak.py` exits 1 with
`corpus/evidence/round53/recurring.tsv`, per-row decision (regex vs claimed), minimal re-registration.
No lane edits outside this report; no network; no git mutation. Scratch `/fast/scratch/hyaku/chousa-r62/ScoutStreakTable/`
deleted before yield. All runs `python3 -B`, cwd = lane root, `--root` absolute.

## Findings

1. **Tool mechanics.** A row passes iff computed trailing streak (consecutive matching rounds back from the
   newest `round-N.md`, text = lesson + its `-verifier-spotcheck.md`) equals the claimed value, and a streak ≥ 3
   names an existing routed path. Any new matching round at the tip invalidates a previously correct claimed value.
2. **Current state (39 round files, 1..61).** RW-1 `forg(e|ed|able|ery)`: hits 35–37, 44–47, 49–61; trailing run
   49–61 = **13** vs claimed 5. RW-3 `relative redirect|fleet root|misroot|fleet-root`: trailing = **1** (round 61
   only) vs claimed 2. Exit 1 reproduced (see Evidence).
3. **RW-1: the regex is right, the claimed value is stale.** The regex measures *exposure naming*, and that is its
   registered semantics — round-53 lesson records it: "The forgeable-frozen-counter class (RW-1) reads a streak of 5
   with this lesson (rounds 49–53): the streak is exposure, not failure" (`corpus/lessons/round-53.md:78`). Claimed=5
   was correct at registration and is simply one field behind the tip. Matches opened: r49 (genuine — replay/hollow-
   quote counters, `round-49.md` CritForgeC2 rows), r53 (registration round, "fifth round running", `round-53.md:19`),
   r60 (names the counter defect via "the output-forge branch is unreachable/tautological" — the *corrected class* is
   do-nothing-reachable, not forgeable). Round 56 contains no "forgeable" at all (matches via "forges"/seat names;
   RevStreak corrected 56 to none-at-freeze). Non-matching opened: r48 (plumbing/receipt errata), r43 (absent-class
   split; counters 15/15 PASS), r38 (clean; note its "forging the refusal token" — a stem near-miss showing the
   regex counts `forge|forged|forgeable|forgery` only). RevStreak's class corrections (56, 59-label, 60) live in the
   class column, which this row never claimed to read.
4. **RW-3: the regex is wrong; the claimed value counted a clean round.** The regex fires on the *check's name*, not
   on incidents. Round 61's match is the clean sweep ("misroot files copied back: 0", `round-61.md` Misroot sweep);
   round 53's registration-era match was also clean ("Status-neutral strays | None this round at the fleet root or
   the lane root (misroot sweep in the report)", `round-53.md`) — so claimed=2 already embedded one false positive,
   and today's streak=1 is a pure false positive. The seven genuine incidents use incident language: r27
   ("misroot: seat report written relative to fleet root"), r30/r33 ("wrote its report at/to the fleet root"; r33
   line-wraps as "wrote\nits"), r45/r46 ("Class: misroot"), r52 ("wrote two files at the fleet root with relative
   redirects"), r57 ("landing (tool misroot) — … wrote 86 capture files … into the FLEET repo", `round-57.md:46`).
5. **Re-registration.** Two new rows below (RW-4 supersedes RW-1, RW-5 supersedes RW-3); RW-1/RW-3 must be retired —
   with all four rows present the tool still exits 1 (verified). The routed path `corpus/evidence/round53/c1-supplement.py`
   exists (verified). INFERENCE: round 62's lessons will likely name forgery again (the routed counter repair), so
   RW-4's claimed value will need re-basing next round — that per-round re-base is the tool's documented design
   ("pair it with each round's" class, round-53.md:78).

## Proposed recurring.tsv rows (verbatim; tab-delimited, 5 fields)

```
RW-4	frozen counter forgeable — exposure naming at tip (supersedes RW-1; claimed re-based r62, rounds 49-61)	forg(e|ed|able|ery)	corpus/evidence/round53/c1-supplement.py	13
RW-5	stray write outside scratch — incident wording (supersedes RW-3; sweep/check names excluded)	misroot:|Class: misroot|tool misroot|wrote\s+(its|their|two|86)[^|\n]{0,60}fleet root|copied back: [1-9]	-	0
```

RW-5 measures incidents only: hit set over the whole record = {27, 30, 33, 45, 46, 52, 57} (exactly the seven
incident rounds; clean mentions in 1, 24, 25, 26, 34, 36, 37, 44, 53, 55, 61 do not match); trailing streak 0.

## Evidence (commands and observed output)

- `python3 -B corpus/evidence/round53/weakness-streak.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --table …/round53/recurring.tsv` →
  `FAIL RW-1 streak=13 claimed=5 first_in_run=49 routed=corpus/evidence/round53/c1-supplement.py`,
  `FAIL RW-3 streak=1 claimed=2 first_in_run=61 routed=-`, `WEAKNESS_ROWS=2 FAILING=2`, `exit=1`.
- Proposed table (scratch copy, same tool) → `OK RW-4 streak=13 claimed=13 … routed=corpus/evidence/round53/c1-supplement.py`,
  `OK RW-5 streak=0 claimed=0 first_in_run=- routed=-`, `WEAKNESS_ROWS=2 FAILING=0`, `exit=0`.
- Combined table (RW-1, RW-3, RW-4, RW-5) → `WEAKNESS_ROWS=4 FAILING=2`, `exit=1` (retirement required).
- Census (script replicating the tool's `text()` join of lesson + spot-check): RW-1 old-regex hits
  35,36,37,44,45,46,47,49,50,51,52,53,54,55,56,57,58,59,60,61, trailing 13.
- `grep -i 'still forgeable' corpus/lessons` → only `round-54.md:21` ("…is still forgeable") and `round-61.md:36`
  ("the amended counter is still forgeable by detection").
- `grep -iE '\|\s*[0-9]+\s*\|\s*forgeable' corpus/lessons` → only `round-61.md:49-58` (the RevStreak table rows).
- `grep -i forgeable corpus/lessons/round-60*.md` → no matches. `grep -i forgeable corpus/lessons/round-56*.md` → no matches.
- Round texts opened: `round-48.md:1-53`, `round-43.md:1-53`, `round-38.md:1-53` (all free of the named weaknesses),
  plus the r49/r53/r60/r61/r57/r52/r45/r46/r33/r30/r27 match contexts listed above.

## Verdict

VERDICT: STREAK_ROWS_RIGHT=1/2 proposed_rows=2
