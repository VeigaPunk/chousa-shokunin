# ScribeMistakes — round 45 wave 1 scoped findings

Role: scribe, leaf seat (no subagent dispatch, no fetch, no production writes).
Assignment: mine candidate `## Mistakes` rows for `corpus/lessons/round-45.md`
from the round-44 non-author spot-check (routed D1-D6) and the round-44 lesson;
mark which round-45 frozen claims address (C1=D5, C2=D2, C3=D1); draft the D4
erratum.

## Commands run (verbatim decisive output)

```
$ read corpus/evidence/round45/claims.md            # frozen predicates, controls
$ read corpus/lessons/round-44-verifier-spotcheck.md # D1-D6
$ read corpus/lessons/round-44.md                    # five mistakes
$ read corpus/evidence/round44/seat-logs/ReviewC1Shape.log
error: Cannot combine --prompt with --auto.
$ read tools/parent-lifetime.sh
# Contract: … Exit 0 when the end line is written. Exit 1 if a child
# pid was not captured. Exit 2 on usage.        (lines 3-8)
TIMEOUT=420                                        (line 20)
… printf 'end … n_spawned=%s n_reaped=%s\n' … exit 0  (lines 106-108)
$ read corpus/evidence/round44/c1-count.py
# end-line values drive n_spawned/n_reaped; a truncated receipt → 0/64, FAIL.
$ read SKILL.md   # ## Gates rows 77-99 end at r39 counters + r35/r36 witnesses; no r40+ rows
$ python3 corpus/evidence/round45/c2-count.py --list
ENTRY_POINTS=54
GATES_ROWS=18
REGISTERED=25/54
UNREGISTERED=29
C2=FAIL
rc=1
$ stat /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt
Modify: 2026-10-23 20:36:20.291295276 -0300    (Access/Birth same second)
$ sha256sum <same>
d2a58e70eb8a2b4e42836c0b3df5035c67a45bbce71c412cbcd2bfb155d4848f
$ grep -n '21:47' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
# only unrelated 2026-10-22 entries (lines 786-790); no chousa round=44 21:47:59 line
$ grep -n 'launch chousa round=44\|complete chousa round=44' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
1223:2026-10-24T21:36:37-03:00 launch chousa round=44 pgid=3105723 driver=hyaku-inline attempt=1
1232:2026-10-24T22:53:23-03:00 complete chousa round=44; hyaku-inline attempt=1
```

No tools installed (none needed). No scratch dir created.

## Candidate `## Mistakes` rows for round-45.md

Each row: class · evidence pointer (path:line) · captured-by · fix · shown able to fail.

### R1 — D1 evidence provenance (ADDRESSED BY C3)
- Class: `attribution` (a capture called "committed" that is not).
- Evidence: spot-check D1 (`round-44-verifier-spotcheck.md:87-91`): the RFC/WARP/E2867
  captures are gitignored (`shokuknow/.gitignore:5`), never tracked; `c3-count.py`
  hardcodes the out-of-lane `.qcache` path, so round-44 C3 was not reproducible from
  the lane tree. The same word recurs in the lesson (`round-44.md:24-25,135-136`).
- Captured-by: `none` at freeze — QUALITY 25/quote-reopen bind a quote to a registry
  row, but no criterion demanded the cited capture bytes be committed in-lane, so
  "committed" entered prose un-measured.
- Fix: C3's route — commit the located spans plus capture digests into the lane
  (`corpus/evidence/round45/spans.tsv`, lane-committed span files) and cite
  `sha256(url)[:24].txt` identity; reword remaining cites to "on-disk capture".
- Shown able to fail: `claims.md:100-105` — the forged-span control (self-consistent
  manifest, invented quotes) passes `--lane-only` and fails default
  (`CAPTURE_BOUND=0/4`, `COUNTS_REDERIVED=0/7`, exit 1); the do-nothing control
  gives `ENTRIES=0/2`, exit 1.

### R2 — D2 gate registry drift (ADDRESSED BY C2)
- Class: `reference-drift` (SKILL.md Gates table drifted from the committed tree).
- Evidence: spot-check D2 (`round-44-verifier-spotcheck.md:155`); measured
  `c2-count.py --list`: `ENTRY_POINTS=54`, `GATES_ROWS=18`, `REGISTERED=25/54`,
  `UNREGISTERED=29`, `C2=FAIL`, exit 1. Unregistered includes r40-r44 counters
  (incl. `round44/errata-count.py`), `tools/parent-lifetime.sh`,
  `tools/absent-split.py`, `tools/quarantine-check.py`, and the three r45 counters.
- Captured-by: `none` at freeze — PROTOCOL §Gate standard (Delivery) required the
  registry row, but nothing measured it; the round-44 C2 predicate measured a
  different object (disposition table), not the Gates table.
- Fix: add a Gates row for every committed gate entry point (all 29 unregistered),
  each named by repo-relative path, row starting `|`, ≥8 `|`, containing `exit`
  (C2's row rule, `claims.md:47-53`).
- Shown able to fail: the counter fails today (exit 1); after the fix, deleting any
  row, renaming/moving an entry point, or omitting a new counter re-opens the
  mismatch because the counter enumerates the full committed set.

### R3 — D3 L2-floor wording (NOT addressed by C1-C3)
- Class: `attribution` (asserted compliance not held).
- Evidence: spot-check D3 (`round-44-verifier-spotcheck.md:115-117`): the report
  stated "§3 L2 floor: met inside waves 2 and 3", but the addendum places the floor
  inside wave 1 (or the single v2 wave) and wave 1 ran zero seats.
- Captured-by: the addendum's §3 L2-floor rule (protocol norm, not machine-checkable).
- Fix: restate the floor's location or name the deviation; round-45 wording must
  match the actual wave-1 seat count.
- Shown able to fail: the reported sentence contradicts the addendum's text verbatim;
  a corrected sentence describing waves 2/3 as the floor still fails the addendum's
  placement. No command-level check exists (normative).

### R4 — D4 minor numbers (NOT addressed; erratum below)
- Class: `number-drift`.
- Evidence: lesson `round-44.md:28` (launch 21:47:59) and `:161` (E2867 mtime
  20:37); spot-check D4 (`round-44-verifier-spotcheck.md:157`).
- Captured-by: `none` (prose numbers; freshness grade unaffected).
- Fix + shown able to fail: see erratum — every corrected figure is verified against
  `stat` and `watchdog.log`; any other value fails those sources.

### R5 — D5 launcher exit contract + seat timeout (ADDRESSED BY C1)
- Class: `vacuous` (exit-status-overclaim, lesson mistake 4) + `provider`
  (seat-timeout, lesson mistake 5); merged as D5.
- Evidence: lesson `round-44.md:58-68` (W3ExecSelftest: `end … n_spawned=0
  n_reaped=0` then exit 0) and `:72-78` (27/32 seats `exit_code=124` at the 420 s
  `timeout`); `tools/parent-lifetime.sh:5-6` ("Exit 0 when the end line is written"),
  `:20` (`TIMEOUT=420`).
- Captured-by: QUALITY 63 ("a launcher's exit status is not evidence that its seats
  ran") — published at closure, after the freeze, so `none` at freeze.
- Fix: C1's exit contract (`claims.md:23-29`) — exit 3 on zero tasks or any seat
  timeout, required `--timeout` recorded as `timeout_s=` in the start line, exit 2
  when `--timeout` omitted.
- Shown able to fail: `claims.md:34-37` — the round-44 launcher control blob scores
  `CASES_MATCH=1/5` (case b only), exit 1; the new launcher must score 5/5.

### R6 — D6 inherited tree (NOT addressed; pending operator ruling)
- Class: `landing` (recognized pre-existing debt, not new).
- Evidence: spot-check `round-44-verifier-spotcheck.md:27-35,159` — three modified
  files (`.ufo/waves/round-40/w1/swarm-registry.json`, `round-41/w1/...`,
  `corpus/evidence/round41/receipts/cells/cells.json`) stay uncommitted as the named
  `left-named` rows.
- Captured-by: the operator's r43 L0 ruling (pending); `none` machine.
- Fix: await the ruling; do not commit or patch them this round.
- Shown able to fail: n/a (no fix attempted).

## Round-44 lesson mistakes — disposition
- M1 launch-flag (`--auto`+`--prompt`): **closed in round 44** (`ReviewC1Shape.log:1`;
  fix drop `--auto`; shown able to fail: `kimi --auto --prompt pong` exit 1 vs
  `kimi --agent-file … --prompt pong` exit 0). Not addressed by C1-C3.
- M2 registry-insert (E12): **closed in round 44** (census E12; rows inserted after
  S078 inside `## Registry`; shown able to fail: outside-registry insert re-prints E12).
- M3 receipt-truncation: **partially closed** — round-44 named the `end` line as the
  completeness marker and excluded the truncated w2 receipt; C1 carries the discipline
  forward (receipts must open with `start … timeout_s=…`; a truncated/no-`end` case
  cannot pass).
- M4 exit-status-overclaim = R5 (C1). M5 seat-timeout = R5 (C1).

## D4 erratum draft (for round-45 lesson)

```
## Erratum — round-44 lesson figure corrections (routed D4)
- E2867 capture mtime: `round-44.md:161` gives 20:37 −0300. `stat` on
  shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt →
  Modify: 2026-10-23 20:36:20.291295276 −0300 (Access/Birth same second); sha256
  d2a58e70… matches the lesson's recorded digest. Correct value: 20:36:20 −0300.
- Launch clock: `round-44.md:28` gives 2026-10-24T21:47:59−03:00. `watchdog.log`
  carries exactly one chousa round=44 launch — `:1223`:
  2026-10-24T21:36:37−03:00 launch chousa round=44 pgid=3105723 driver=hyaku-inline
  attempt=1, complete `:1232` 22:53:23. The wave-2 freshness seat already used
  21:36:37 (`round-44.md:161`), matching the driver digest (`spot-check:23-25`).
  No 21:47:59 line exists. Correct launch: 21:36:37 −03:00.
- Freshness grade unchanged: every capture (10-23) predates the launch (10-24) under
  both readings. Per QUALITY 62, this correction is to the lesson, not to round-44
  claims, so it is not counted by `errata-count.py`.
```

## Limits
- No fetch, no network egress; no lane-production edits; only this report was written.
- `c2-count.py --list` reflects the current working tree (round-45 counters present);
  it is a count, not a seat score of C2.
- The D3 row has no command-level falsifier; it is a normative-wording row.
