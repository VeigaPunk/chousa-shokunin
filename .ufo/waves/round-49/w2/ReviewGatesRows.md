# ReviewGatesRows — w2 gate: the two new `## Gates` rows vs the code

Scope: SKILL.md rows added at adoption commit 1254ab2 (`git log -S` on both row names → `1254ab2 round-49: adopt derived-index theme…`): line 130 `assimilate-rows`, line 131 `chousa round-49 counters and checks`. Method: read both rows verbatim (`SKILL.md:130:raw`, `:131:raw`), read every named script, then probed the tool's verdict map live. No `lsp` device exists in this seat's tool inventory, so definition/caller checks are static reads + execution, not semantic server output.

## Required command (cwd = lane checkout, TMPDIR=/dev/shm/chousa-r49-ReviewGatesRows)

```
$ python3 corpus/evidence/round47/c2-count.py --list | tail -8
ENTRY_POINTS=104 (abc=91 dependence=+3 check_named=+10)
FLOOR=92
GATES_ROWS=54
REGISTERED=104/104
UNREGISTERED=0
DANGLING=0
MISMATCHES=0
C2=PASS
EXIT=0
```

## Row `assimilate-rows` (SKILL.md:130) vs tools/assimilate-rows.py

- Entry shape matches argparse (`assimilate-rows.py:120-126`: five required opts, repeatable `--entry`).
- "writes only under `--out`": every write targets `out/` (`:152-154` ids; `:236-246` entries/append.md/renumber.tsv/stripped.tsv). No input is written. Holds.
- Exit 0 tokens: `COLLISIONS=n` `:155`, `CITED= APPEND= HELD=` `:247`. Exit 1: entry missing/not UTF-8 `:168-172`, cited row ≠11 cells `:175`, no URL `:177`, recheck `:224`. Exit 2: missing file / calendar-invalid `--opened` `:138-142`, non-UTF-8 `:148-150`, absolute/`..` entry `:143-146`. All exist.
- Live probe (scratch fixture, exit/stdout/stderr):
  - missing staged → `2`, calendar-invalid `2026-02-30` → `2`, `/etc/passwd` entry → `2`, `../x.md` entry → `2`, non-UTF-8 staged → `2`.
  - missing entry file → `1`, stdout `COLLISIONS=0`, stderr `REFUSED entry missing: corpus/knowledge/absent.md`.
  - no entries → `0` `COLLISIONS=0`; with entries → `0` `COLLISIONS=0 | CITED=2 APPEND=1 HELD=1`; renumber shows held-by-URL `S002→S001` and append `S003→S002` (next id from registry max).
  - recheck `30d prose` → `0`, cell reduced to `30d`, prose logged in `stripped.tsv`.
- **F1 (minor, row-text wording — fails closed):** row exit-1 clause says a recheck is refused when it has "no leading calendar-valid date/`NNd`/cadence". The code accepts a cadence only as the ENTIRE cell (`RECHECK_RE` anchored `^…$`, `:60`); a mixed cell may lead only with a date or `NNd` (`LEAD_RE`, `:61` — no cadence alternative). Probe: recheck `weekly; prose` → exit `1`, `REFUSED S003: recheck 'weekly; prose' has no leading valid date or NNd` (`:224`), though the row's plain reading (leading cadence suffices) predicts acceptance. Code is stricter than documented; no input the code accepts is refused by the row's reading. Fix is a SKILL.md word, not code.
- Self-test cell: `corpus/evidence/round49/controls/copy-tool.py` exists; `controls/c1-before.txt:11-17` shows `SETS_PASS=0/3`, `GUARD … -> FAIL`, `PIPE … CELLS=13 … -> FAIL`, `C1=FAIL` — "fails every set, GUARD and PIPE" holds.

## Row `chousa round-49 counters and checks` (SKILL.md:131) vs corpus/evidence/round49/*.py

All six named entry files exist (wc: 402/241/207/59/68/31 lines). Flags `[--tool PATH]` (c1-count.py:338-341) and `[--lane-only]` (c2-count.py:171-172) exist.

- **C1**: exit `0` iff `SETS_PASS=3/3` and GUARD/PIPE PASS (`c1-count.py:395-398`); tokens `SETS_PASS` `:395`, `GUARD` `:306`, `PIPE` `:335` exist; `C1=PASS`/`C1=FAIL` `:397`. Exit `1` any leg (`:398`, incl. `TOOL=absent` → `C1=FAIL` `:358-360`). Exit `2`: `PACKAGE_CHANGED` `:351-352`, `NO_BASE_REV` `:371-372` — both named; code also exits `2` on `NO_CENSUS` `:354-355` and a failing base census `:389`, which the row's "package changed or no base rev" does not name (same usage/env code as sibling rows; nothing wrongly named).
- **C2**: exit `0` iff `nb >= MIN_BOUND` (=7, `c2-count.py:62`) and `nb + refused == 9` and every leg full (`:235-238`); tokens `BOUND` `:217`, `REFUSED`, `REF_ID_UNBOUND` `:219`, `ANCHOR_BOUND` `:228`, `INFERENCE_GROUNDED` `:229`, `QUARANTINE_VERDICTS`/`QUARANTINE_BLOCKED_ADOPTED` `:230-231` exist. Exit `2` `NO_BASE_OR_REGISTER` `:131-132` = "no base/register". `--lane-only` prints `CAPTURE_BOUND=skipped` `:227`.
- **build-spans**: prints `SPANS_ROWS= STALE=` `:172`; `--check` exit `0` iff `STALE=0` else `1` `:173`; refused quote → `sys.exit(1)` `:143`; usage (no input `:72`, bad header `:76`, malformed row `:97`, missing cache `:186`) → exit `2`. Matches "0 built or STALE=0 · 1 refused quote or stale row · 2 usage".
- **a05-check**: `UNCORRECTED` token `:53`, exit `1` iff bad else `0` `:55` — matches "0 every propagation corrected · 1 an UNCORRECTED line". **F2 (minor, row omission):** the script also returns `2` when `corpus/lessons/` is absent (`:31`); the row names no exit 2 for this check.
- **quote-substance-check**: `FAILURES=` `:63` with exit `1` iff failures; `HOLLOW_QUOTE`/`OVERWIDE_SPAN`/`NO_SUBSTANTIVE_QUOTE` (`:45-61`); exit `2` no manifest `:38-39`. Matches.
- **capture-age-check**: `FRESHNESS_CAPTURE_AGE=PASS|FAIL` `:26`, exit `0`/`1` `:27`, exit `2` usage/unreadable `:22`. Matches (QUALITY 71 in docstring `:9`).
- Self-test cell: `controls/c2-before.txt` carries `BOUND=0/9`, `REF_ID_UNBOUND=11`, `C2=FAIL` — the row's "staged copy `REF_ID_UNBOUND=11`" holds.

## Verdict-map direction check

Every exit code and printed token named in either verdict map exists in its script (F1 is the row over-promising an acceptance, not naming a token the code lacks; F2 is the row under-naming an exit). No token in the code contradicts a row claim. `measure-after.txt` C1=PASS/C2=PASS was not re-derived here (replay is another seat's assignment); this review is static + probe evidence.

## Residual risk / verification gaps

- Counters C1/C2 not replayed; control files inspected, not regenerated.
- `NO_CENSUS`/base-census exit-2 paths (c1-count.py:354-355,389) and a05 exit 2 (`:31`) unexercised at runtime; code-read only.
- C2's quarantine register parsing (`:196-206`) and verdict regex were not probed with synthetic lessons; scope was the verdict map.

VERDICT: SKILL.md:130-131 Gates rows — partly — every named exit code and token exists in the scripts (probed live for assimilate-rows), but the assimilate-rows exit-1 wording overstates cadence acceptance (leading-cadence+prose rechecks refuse, F1) and a05-check's exit 2 is unnamed (F2).
