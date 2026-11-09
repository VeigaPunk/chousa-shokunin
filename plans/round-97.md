# Round 97 plan — chousa (L1 `ChousaR97`, attempt 1)

Base `c8087ac529003e667505bcc624f9a7bde0cffbce` (round-96 landing; the round-96 non-author spot-check
`corpus/lessons/round-96-verifier-spotcheck.md` is on the lane). Round-96 closure: admitted (operability improved,
depth improved). No fresh-start rule binds this round; the §9 rules do: each claim beats a committed do-nothing
control, scored by the frozen counter, before the freeze (`corpus/evidence/round97/before/`).

## Why these claims

- SCORECARD `## Planned — round 97` item 1 (operability, the lowest axis): close the self-test's measured blind
  spots — `R96MutantsC1` class C (signed hits, bad dates, uppercase hex, two-code rows, non-UTF-8, `//` globs,
  trailing commas, literal-filename static dirs, glob-longer-than-path) and class B (a fixture-breaking mutant
  crashes with a traceback instead of printing FAIL), and `R96SentinelC1` F1/F7 (`git_env` guards). C1 takes it,
  scored against those seats' own mutants read from committed round-96 bytes, so the target is set by a non-author
  and the base tool's 10/30 is the do-nothing score. Not taken: the F2 NO_WRITE baseline is rebuilt (battery-start
  status + diff digest) but is not a claim; the `verify`↔`evaluate` tie (§Aa) stays a named limit.
- Planned item 2 (depth): the PRESS 2015 checklist's own wording. Every primary route answered 403 from this host
  (CADTH E&E, CADTH Table 9 and 10, J Clin Epidemiol, core.ac.uk) and `web.archive.org` refused TCP; two reachable
  reprints were found (Cochrane editors' checklist PDF; Karolinska library page). C2 holds the checklist questions
  through the stronger reprint (S225, B) and measures how far the second (S226, C) agrees — the disagreement is
  itself a finding the round-96 abstract-level reading could not show.
- Item 3 (carried debt) stays carried; see `## Routed defects`.

## Pre-freeze fixes (before any seat scored)

- **P0** — the first battery run crashed in setup: `ast.literal_eval` cannot read `n08`'s old string, which the
  round-96 probe writes as `r'...' + "\n"`. The battery's reader now accepts `str + str` and nothing else; n08 is
  still excluded (it applied 0 times in round 96).
- **P1** — the first C2 controls run failed `g2`: the forged "line join" (L21 + the next words) is in fact on the
  same capture line, so the gate correctly accepted it. `g2` now joins capture line 36 to line 38 skipping 37
  (`QUOTE_ABSENT`). The run also showed `gate-records.py` would accept a quote joined across *adjacent* lines
  (it matches the whitespace-collapsed whole text), so a ONE_LINE binding was added inside POSITIVE.
- **P2** — a SKILL.md checklist item for the new entry was drafted at line 86 and removed: it shifted the Gates
  table by two lines and broke the round-96 correction's `SKILL.md:180` pointer. The round-97 note is a
  `correction:` line after the round-96 one instead, and adds no line above row 180.

## Routed defects from the round-96 spot-check

- D1 (refetch id collision: the J Clin Epidemiol 403 row carries id `S224`) → **not written this round**. The TSV is
  read by `tools/gate-records.py`, `tools/capture-fetch.py` and `tools/store-record-audit.py`; a correction row of
  a new shape has not been shown safe for all three. Recorded in `LOG.md` as an open correction with the parser
  question; S227 this round was registered before any `## Gate` record cites it, so the round-96 mistake does not
  repeat.
- D2 → C1.
- D3 (four gate-kind tools with no `--selftest`) → carried.

## Wave

One v1 wave of 12 seats, attack share ≥25 %. L1 holds the canonical planner seat.
