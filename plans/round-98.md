# Round 98 plan — chousa (L1 `ChousaR98`, attempt 1)

Base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6` (round-97 landing plus the round-97 non-author spot-check
`corpus/lessons/round-97-verifier-spotcheck.md`). Round-97 closure: admitted (operability improved, depth improved).
No fresh-start rule binds this round (the last three closures, r95-r97, are admitted); the §9 rules do: each claim
beats a committed do-nothing control, scored by the frozen counter, before the freeze
(`corpus/evidence/round98/before/`). No earlier attempt of this round exists (`.ufo/watchdog.log` has only the
attempt-1 launch line); nothing inherited.

## Why these claims

- SCORECARD `## Planned — round 98` item 1 (operability, the lowest axis) and the round-97 spot-check's routed
  defects 1 and 2: `R97MutantsC1` left 19 mutants no lane instrument catches, five of them in the guard and summary
  code, and a hash-of-self self-test passes the round-97 battery. C1 adds a guard canary (`g00`) that runs the guard
  and summary code itself on fixed case sets, 18 cases (`r17`-`r34`) aimed at the survivors, and a battery that
  scores the 37 seat-written mutants from committed bytes, requires three equivalent mutants to survive (which a
  hash-of-self self-test cannot) and adds a guard-blind and a hash-of-self stand-in to the oracles. Do-nothing
  score: the round-97 tool kills 12 of the 37.
- Planned item 2 (depth): the PRESS 2015 primary routes stay blocked from this host — CADTH report 477 appendices
  403 (S228), PubMed a cookie challenge (S229), NCBI Bookshelf a reCAPTCHA page (S230) — but Europe PMC's public
  REST record of PMID 27005575 carries the statement's own abstract (S231, http 200). C2 holds it and finishes the
  question lines the round-97 entry left (`R97ScoutSources` F-C3: 16 of S225's question lines quoted). Do-nothing
  score: 16/36 question lines, entry absent.
- Item 3 (carried debt): D1 (`S224` names two documents in `refetch.tsv`) stays carried — it needs a reader rule in
  `tools/gate-records.py`, which this round does not touch. Round-97 routed defect 4 (battery docstring wording,
  mutant runs inheriting the lane as cwd) is fixed in the round-98 battery: its docstring states what it runs on the
  lane and that it does not see git-ignored paths, and every scored run has a scratch cwd. Routed defect 3 (C2
  Never cells not instrument-checked) is answered by wording, not an instrument: every round-98 Never cell is the
  negation of its Do clause or "(none stated by the sources)", and K3 makes that a kill rule for the reviewer.

## Routes tried (approval table `corpus/evidence/round98/egress-approval.md`, written before the first GET)

| id | route | result |
|---|---|---|
| S228 | CADTH report 477 appendices PDF | http 403, curl rc 22 (attempt 1) |
| S229 | PubMed 27005575 | http 203, cookie-challenge page (stored by the tool as bytes; never cited) |
| S230 | NCBI Bookshelf NBK98350 | http 200, reCAPTCHA page (stored by the tool as bytes; never cited) |
| S231 | Europe PMC REST core record, PMID 27005575 | http 200, the record with `abstractText` |

## Pre-freeze fixes (before any seat scored)

- **P0** — the first battery run printed `g06-refusal-detail SETUP applies 3 times`: two new cases wrote
  `return exc.code == ...`, which contains the mutant's site `            return exc.code`. The cases now bind
  `code = exc.code` first, and the site is unique again (`EXTERNAL_R97_KILLED=35/37 setup=0`).

## Wave

One v1 wave of 12 seats under `scripts/hyaku/ufo-wave-policy.json`, attack share >= 25 %. L1 holds the canonical
planner seat.

## Amendments after the freeze — re-frozen at F2 (wave-forced)

Recorded with their seat artifacts in `.ufo/waves/round-98/claims.md` § Amendments: C1 A1-A5, C2 B1-B7. In short:
the canary gains a one-failure and a four-failure set (A1); the battery gains DIRECT_PATH (A2), KILL_RULE and pinned
set sizes (A3); checker-of-the-checker survivors are named, not repaired (A4); the entry's M1 is the record's title
and the controls check each S231 quote's JSON field and the record's identity (B1, B4); row 2's Never cell is
"(none stated by the sources)" (B2); named limit (c) is corrected (B3); S231 is tier B (B5); three more forgeries
and an ACCEPT leg (B6).

Correction to `## Why these claims` (A5, `R98RevenPrior` (1)): "19 mutants no lane instrument catches, five of them
in the guard and summary code" is `R97MutantsC1`'s count. At BASE the round-97 battery, run with `--tool` on g01,
g03 or g04, fails (its mutant legs collapse), so those three were caught by a battery, not by the self-test; g02
and g05 were caught by nothing. C1 speaks of the self-test.

L1 re-score of `R98MutantsC1`'s probe (`R98MutantsC1-probe98.py.txt` MUTANTS) on the F2 tool, frozen kill rule: S02,
S03 now KILLED; D01-D04 still survive the self-test alone (the battery's DIRECT_PATH leg catches them); G01-G03, D05,
R32 survive (A4; R32 is caught by the round-95 battery).
