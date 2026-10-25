# MutC2Forges — C2 counter mutation probes (round 45, wave 1)

Seat: L1Chousa45.MutC2Forges (mutation-tester). Item: forge-tests C2 counter
`corpus/evidence/round45/c2-count.py` against five mutations of the Gates
section; confirm a new `tools/x.sh` is enumerated. Lane bounds: leaf, no
subagent dispatch. No installs made (used python3, cp, sha256sum; pacman
untouched).

## Setup
- Scratch copy at `/tmp/chousa-r45-MutC2Forges/` keeping relative layout
  (`SKILL.md`, `tools/`, `corpus/evidence/`); every run used
  `python3 /tmp/chousa-r45-MutC2Forges/corpus/evidence/round45/c2-count.py --root /tmp/chousa-r45-MutC2Forges --list`
  (counter bytes identical to lane, sha256 `fdb2019207d294a53666a4eda4fcf5d41a6be45d342e0fe654f72ca82cfe2af5`).
- Pristine SKILL.md sha256 `cd9c8e3f4d964f651aa7a6307689303d2b0204d40fc1b579cb523369ed0633fb`
  = lane SKILL.md sha256; verified identical after every restore.
- Baseline on pristine copy: `ENTRY_POINTS=54 GATES_ROWS=18 REGISTERED=25/54
  UNREGISTERED=29 C2=FAIL`, exit 1 — matches claims.md freeze before (29).
- Probe path used: `tools/parent-lifetime.sh` (real unregistered entry point
  from baseline list); `tools/x.sh` for the enumeration + ### probes.
- Gates section spans lines 75–490 (next `## ` heading is line 491
  `## Round26 metadata options and resource qualification`).

## Probes (mutate → run counter → restore exact bytes; all restored hashes = baseline)

| # | Mutation | Counter output (decisive) | Verdict |
|---|---|---|---|
| (a) | path pasted into a **prose line** inside Gates (after separator row) | `GATES_ROWS=18 UNREGISTERED=29 C2=FAIL` exit 1; `tools/parent-lifetime.sh` still listed | refused (prose is not a row) — matches frozen rule |
| (b) | row with **7 `|`** (contains `exit` and the path) | `GATES_ROWS=18 UNREGISTERED=29 C2=FAIL` exit 1; path still listed | refused (<8 separators) — matches frozen rule |
| (c) | row with **8 `|`**, no `exit` | `GATES_ROWS=18 UNREGISTERED=29 C2=FAIL` exit 1; path still listed | refused (no `exit`) — matches frozen rule |
| (d) | **fully valid row** (9 `|`, `exit`) placed after next `## ` heading (line 491) | `GATES_ROWS=18 UNREGISTERED=29 C2=FAIL` exit 1; path still listed | refused (outside `## Gates` section) — matches frozen rule |
| — | add `tools/x.sh` (new file) | `ENTRY_POINTS=55 … UNREGISTERED=30 C2=FAIL` exit 1; `tools/x.sh` listed | new tools file **is enumerated** and reported unregistered |
| (e) | **fully valid row** (9 `|`, `exit`) inside a `### ` subsection within Gates (after `### Probe subsection`), naming `tools/x.sh` | `ENTRY_POINTS=55 GATES_ROWS=19 REGISTERED=26/55 UNREGISTERED=29 C2=FAIL` exit 1; `tools/x.sh` **absent** from list | row counted: counter treats `### ` as INSIDE the section — matches frozen rule (section ends only at next `## ` heading) |

## Conclusion
- All five forges behaved exactly as the frozen predicate R45-C2 prescribes:
  path must sit in a line that starts with `|`, carries ≥8 `|`, contains
  `exit`, and lies between `## Gates` and the next `## ` heading.
- Counter source locations: entry-point enumeration `c2-count.py:31-42`
  (files directly under `tools/` + `corpus/evidence/round*` name regex);
  row gate `c2-count.py:45-55` (`startswith("## ")` toggles `inside`;
  `### ` does not); unregistered check `c2-count.py:71` (substring match).
- No killed mutant: every probe survived (correctly refused/accepted);
  UNREGISTERED stayed ≠0 → `C2=FAIL` exit 1 throughout, so the counter was
  not fooled into PASS by any forge.
- Lane files untouched (SKILL.md, tools/, corpus/evidence/ all hash-verified);
  no git/jj/network activity. Scratch `/tmp/chousa-r45-MutC2Forges/` and
  probe outputs deleted.
