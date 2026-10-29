# ScribeSkillRows — round 62, wave w1 (scribe)

Rows: `.ufo/waves/round-62/w1/ScribeSkillRows/rows.md` (exact row text, insertion line for each). Nothing applied to `SKILL.md`; no frozen path written; no git mutation; no network.

## Findings

1. **Gates row (counter-validity battery)** — drafted, insert after `SKILL.md:148` (`chousa round-61 counters and checks`). Its `before` value is observed in this seat: the battery on `controls/null-pass.py` gives `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL`, exit 1. The `after` value (`c1v2-count.py` → `BATTERY=PASS`, `LEGS=20/20 C1V2=PASS` at three seeds) is **not run here** and is marked `[INFERENCE]` in the row.
2. **Decision row (opening paths under an untrusted directory)** — drafted, insert after `SKILL.md:26` (the round-61 `Write derived evidence` row). The per-flag behaviour is observed (probe P02–P09, below). The combined `RESOLVE_NO_SYMLINKS | RESOLVE_BENEATH` set is **not probed** by the lane probe; the row says so.
3. **Error-pattern row (counter accepts a detection forger)** — drafted, insert after `SKILL.md:51` (the r30 `address check passes` row). Observed: round-61's counter reads `C1=PASS` 20/20 on every forger.

## Probe-path and registry gaps (for L1 integration)

- **The probe the row names is not landed.** `corpus/evidence/round62/openat2-probe.py` and `openat2-probe.txt` do not exist (`ls corpus/evidence/round62/openat2-probe.*` → no such file). Only `corpus/evidence/round62/controls/candidate-openat2-probe.py` / `.txt` exist. The row cites the frozen landing path; it is not live until the probe lands. Landing = copy of the candidate, byte-identical, to the claims path, with its committed output.
- **S138–S140 are not in `corpus/SOURCES.md`.** `grep -n 'S13[89]\|S140' corpus/SOURCES.md` shows only the `## Leads` line (openat2 at line 326), not opened rows. The row cites the man page and header paths directly; once the rows land, the `source` cells can be bound to them.
- **Battery invocation.** `null-pass.py` run directly without arguments raises `ValueError: list.index(x): x not in list` (it needs `--builder`); under the battery it works. The row documents the battery form, not a direct call. (A first battery call I made with `null-counter.py` and no mode argument gave a non-control result; it is my misuse, not evidence, and is not cited.)

## Commands run (output observed)

- `python3 -B corpus/evidence/round62/controls/candidate-openat2-probe.py --work <scratch>/probe` → exit 0; `KERNEL 7.2.11-arch1-1`, `PYTHON 3.14.8`, `HEADER ... __NR_openat2=437`; `PROBE P01 python-os-has-openat2 observed=False`; `P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened`; `P03 ... final-component observed=ELOOP`; `P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP`; `P05 ... final-component observed=ELOOP`; `P06 openat2-NO_SYMLINKS-plain-path-inside observed=opened`; `P07 openat2-BENEATH-dotdot-escape observed=EXDEV`; `P08 openat2-BENEATH-absolute-symlink observed=EXDEV`; `P09 openat2-BENEATH-relative-symlink-inside observed=opened`; `P10`–`P14` all `ok`; `PROBE_FACTS=14/14`. Second run, stdout `diff` against `controls/candidate-openat2-probe.txt`: identical (`SAME`).
- `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/controls/null-pass.py --work <scratch>/bat3` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL`, exit 1. Matches `controls/null-counters.txt` (`null-pass` line).
- `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx`, line 86: "the effect of the RESOLVE_NO_SYMLINKS flag, which affects the treatment of symbolic links in all of the components of path, differs from the effect of the O_NOFOLLOW ... which affects the handling of symbolic links only in the final component"; line 84 (O_PATH + O_NOFOLLOW + NO_SYMLINKS final-symlink fd, consistent with P14 `observed=True`).
- `/usr/include/linux/openat2.h` lines 33–45: `RESOLVE_NO_XDEV 0x01`, `RESOLVE_NO_MAGICLINKS 0x02`, `RESOLVE_NO_SYMLINKS 0x04`, `RESOLVE_BENEATH 0x08`, `RESOLVE_IN_ROOT 0x10`, `RESOLVE_CACHED 0x20`.
- Read, not re-run: `controls/c1v2-before.txt` (every forger `counter_exit=0 want=1 MISS`; `FORGERS_REJECTED=0/12 BATTERY=FAIL`); `controls/null-counters.txt`; `controls/c1v2-controls.txt` (`CONTROLS_UNEXPECTED=0`; X10 `SURVIVED`, named gap).

## Limits

- The probe is one kernel (7.2.11-arch1-1), one filesystem, x86_64 (`controls/candidate-openat2-probe.py` docstring).
- Row 2's combined-flag advice is `[INFERENCE]`; a combined-flag probe is the next falsifiable step, not run here.
- The battery's after-target is not observed in this seat; the row's `after` cell is marked as not run.
- The r61 entry `corpus/knowledge/derived-output-safety-r61.md` is cited only as a neighbour row, not re-verified.

## Sources cited (distinct, 12)

1 `corpus/evidence/round62/claims.md` · 2 `corpus/evidence/round62/c1v2-battery.py` · 3 `corpus/evidence/round62/controls/c1v2-before.txt` · 4 `corpus/evidence/round62/controls/null-counters.txt` · 5 `corpus/evidence/round62/controls/null-pass.py` · 6 `corpus/evidence/round62/controls/c1v2-controls.txt` · 7 `corpus/evidence/round62/controls/candidate-openat2-probe.py` · 8 `corpus/evidence/round62/controls/candidate-openat2-probe.txt` (S140 output) · 9 `/usr/share/man/man2/openat2.2.gz` (S138) · 10 `/usr/include/linux/openat2.h` (S139) · 11 `corpus/evidence/round61/c1-count.py` (before-counter, named in row 1) · 12 `SKILL.md` lines 13–26, 40–51, 77–148.

Scratch `/fast/scratch/hyaku/chousa-r62/ScribeSkillRows/` removed before yield.

VERDICT: ROWS_DRAFTED=3/3 cited_sources=12
