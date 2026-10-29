# Round 63 · wave w1 · MutProbe (mutation-tester) — C2 PROBE leg

Target: `corpus/evidence/round63/controls/candidate-git-revision-probe.py` (sha256 ccd702f4…, read-only)
and the frozen counter's PROBE leg in `corpus/evidence/round63/c2-count.py` (read-only). Scratch
`/fast/scratch/hyaku/chousa-r63/MutProbe/` (deleted before yield). No lane, fleet or git writes.
Tools: git 2.56.0, python 3.14.8, man, col — all present; nothing installed or upgraded.

## Findings

1. **A forged printer passes both layers (SURVIVED, M20).** A probe that replays the committed
   `candidate-git-revision-probe.txt` and runs no git gets `PROBE_FACTS=14/14`, exit 0, and the
   counter's PROBE leg reads `PROBE=1/1`. The leg checks output text, PROBE_FACTS and the `HEADER git=`
   string against live `git --version`; it does not check that git ran. Limit for the C2 entry and
   the round lesson (frozen counter unchanged): "the PROBE leg proves the committed text reproduces
   on the live git version; it does not prove a probe run produced it".
2. **The probe's own self-check is untested by the committed output (M10, M13).** All 14 facts hold on
   this host, so `ok = True` and dropping `all(facts)` from the exit code are invisible (both survive
   on their own). They are caught only when a fact is also wrong (M11: counter by_counter; M16: the
   DIFFERENT line still prints and flags by_probe). Calibration: the probe's ok-path has no
   independent test in the frozen battery.
3. **P12 does not test the clamp (SURVIVED, M07).** `--short=2` and `--short=4` both return 4 characters
   on this git (minimum length 4), so P12 cannot tell them apart. The fact is still true but no longer
   tests the clamp. Routed as a limit for a future probe amendment (not this frozen round).
4. **The user-config leak is invisible on this host (M22), visible elsewhere.** `~/.gitconfig` is absent
   and `~/.config/git/` is empty here, so dropping `GIT_CONFIG_GLOBAL` from BASE_ENV survives. With a
   poisoned `HOME` (`~/.gitconfig` with `core.abbrev=8`) it is killed by_probe (X2). The pristine probe is
   unaffected by the same poisoned `HOME` (X3, control PASS). The scrub works; the committed output only
   guards hosts with no user git config.
5. **Output-invisible or cosmetic changes survive by design:** M15 (fixture commit bytes change; the probe
   prints lengths and booleans, never ids) and M21 (trailing space; the counter's `probe_lines` rstrips).
   Equivalent mutants, not gaps.
6. **Probe exit 2 is not the named self-flag.** M04, M14, M19 end with exit 2 and a stderr message
   (`RuntimeError: ... pathspec 'a.txt' did not match`, `... Needed a single revision`, `no 4-digit
   collision found`). Counted by_counter because the frozen PROBE leg fails on rc≠0; the probe's own
   DIFFERENT/exit-1 flag does not name them.
7. **Process note.** My first M23 mutant left an empty `for` body (IndentationError, rc 1). That exit looked
   like a kill, so it was not counted. It was redone as X1 (`if False:`), a valid mutant killed by the probe's
   own P13 DIFFERENT line. The tally below uses only the valid run.

## Method

- Pristine control P00: standalone `python3 -B <mutant> --work <fresh>` → `PROBE_FACTS=14/14`, exit 0;
  counter PROBE leg `PROBE=1/1`, rc 0. Frozen runner `run-c2-controls.py --work … --keep` rerun: all 21
  listed variants `OK`, `C2_CONTROLS_UNEXPECTED=0` (146 s wall, output identical in shape to
  `controls/c2-controls.txt`).
- Each mutant is applied to a scratch copy of the probe with exact-one-match anchors (the driver aborts
  on a non-unique anchor). Run standalone with an outer environment that sets `GIT_CONFIG_COUNT=1`,
  `GIT_CONFIG_KEY_0=core.abbrev`, `GIT_CONFIG_VALUE_0=8`. Then placed at the mirror's
  `corpus/evidence/round63/git-revision-probe.py` (mirror built as `run-c2-controls.py` builds it, from
  `candidate-git-rows.txt`, `c2-positive-entry.md`, the committed probe output) and run through
  `c2-count.py --root MIRROR --fleet /home/vgpnk/Projects/shokunin --work <fresh>`.
- Layer rule: **by_probe** = the probe's own `DIFFERENT` line or exit 1. **by_counter** = not by_probe, and
  the PROBE leg reads `PROBE=0/1`. **SURVIVED** = neither.

## Mutant table (23 valid mutants)

| id | mutant | probe alone | counter PROBE leg | layer |
|---|---|---|---|---|
| M01 | P01 expected 40→41 | DIFFERENT P01, exit 1 (13/14) | 0/1 | by_probe |
| M02 | P02 expected 64→63 | DIFFERENT P02, exit 1 (13/14) | 0/1 | by_probe |
| M03 | 4-hex second object not stored (`hash-object -w` dropped) | DIFFERENT ×3 (11/14), exit 1 | 0/1 | by_probe |
| M04 | no `-C` on git calls | exit 2, `pathspec 'a.txt' did not match` | 0/1 (rc 2) | by_counter |
| M05 | sha256 fixture is `init sha1` | DIFFERENT P02, exit 1 | 0/1 | by_probe |
| M06 | sha256 probe removed (P02 call gone) | 13/13, exit 1 (`len(facts)!=14`) | 0/1 | by_probe |
| M07 | `--short=2` → `--short=4` | 14/14, exit 0 | 1/1 | **SURVIVED** (finding 3) |
| M08 | `GIT_CONFIG_GLOBAL` → file with `core.abbrev=8` | DIFFERENT P13 (observed 8), exit 1 | 0/1 | by_probe |
| M09 | PROBE label renamed | 14/14, exit 0 | 0/1 (same_as_committed=False) | by_counter |
| M10 | `ok = True` | 14/14, exit 0 | 1/1 | **SURVIVED** (finding 2) |
| M11 | M01 + M10 | 14/14, exit 0 (line says `expected=41 ok`) | 0/1 | by_counter |
| M12 | HEADER git fixed to `git version 0.0.0` | 14/14, exit 0 | 0/1 | by_counter |
| M13 | exit ignores `all(facts)` | 14/14, exit 0 | 1/1 | **SURVIVED** (finding 2) |
| M14 | fixture branch `master` (no `main`) | exit 2, `Needed a single revision` | 0/1 (rc 2) | by_counter |
| M15 | fixture commit bytes changed | 14/14, exit 0 | 1/1 | **SURVIVED** (finding 5) |
| M16 | M01 + exit ignores `all(facts)` | DIFFERENT P01 printed, exit 0 (13/14) | 0/1 | by_probe |
| M17 | report printed on stderr | stdout empty, exit 0 | 0/1 | by_counter |
| M18 | `PROBE_FACTS` printed one fewer, all facts true | 13/14 printed, exit 0 | 0/1 | by_counter |
| M19 | 4-digit collision loop capped at n > 5 | exit 2, `no 4-digit collision found` | 0/1 (rc 2) | by_counter |
| M20 | canned printer (replays committed text, runs no git) | 14/14, exit 0 | 1/1 | **SURVIVED** (finding 1) |
| M21 | trailing space on each PROBE line | 14/14, exit 0 | 1/1 (counter rstrips) | **SURVIVED** (finding 5) |
| M22 | `GIT_CONFIG_GLOBAL` dropped from BASE_ENV | 14/14, exit 0 on this host | 1/1 | **SURVIVED** here; X2 (poisoned HOME): DIFFERENT P13 observed 8, exit 1 → by_probe |
| M23 | `GIT_*` scrub loop disabled (run as X1, `if False:`) | DIFFERENT P13 observed 8, exit 1 | 0/1 | by_probe |

Controls: P00 pristine 14/14, `PROBE=1/1`. X3 pristine under poisoned HOME: 14/14, `PROBE=1/1` (not killed = correct).

## Tally

Killed 16/23: by_probe 8 (M01, M02, M03, M05, M06, M08, M16, M23), by_counter 8 (M04, M09, M11, M12,
M14, M17, M18, M19). Survived 7 (M07, M10, M13, M15, M20, M21, M22 as run on this host). M22 is killed
by_probe under a poisoned HOME (X2), not counted in the 16. Of the 7 survivors, M15 and M21 are
expected-equivalent, and M22 is equivalent on this host. M07, M10, M13 and M20 are real gaps (findings
1–3).

Commands and output: `python3 -B candidate-git-revision-probe.py --work <fresh>` → `PROBE_FACTS=14/14`,
exit 0 (2.45 s). `python3 -B run-c2-controls.py --work <fresh> --keep` → `C2_CONTROLS_UNEXPECTED=0`.
Driver `mutdrive.py` → `TALLY killed=16/23 by_probe=8 by_counter=8 survived=7`. Follow-up `extra.py` →
`EXTRA [('X1-M23-fixed', 'by_probe'), ('X2-M22-poisonHOME', 'by_probe'), ('X3-pristine-poisonHOME', 'SURVIVED')]`
(X3 is the control, so SURVIVED = not killed, as intended).

INFERENCE: the 7 survivors and the 16 kills describe this host (git 2.56.0, no user git config). A host
with a user `core.abbrev` would kill M22 by_probe in a live run, as X2 shows.

VERDICT: PROBE_MUTANTS_KILLED=16/23 by_probe=8 by_counter=8
