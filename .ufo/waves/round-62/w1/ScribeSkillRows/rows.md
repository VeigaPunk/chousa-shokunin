# ScribeSkillRows — draft rows for SKILL.md (round 62, w1)

Draft only. Not applied to `SKILL.md`; the L1 integrates. Each block gives the line after which the row belongs
and the exact row text. Sources are cited inside each row. Items marked `[INFERENCE]` were not run.

## Row 1 — Gates table (new gate row)

Insert after: line 148 (`| \`chousa round-61 counters and checks\` | gate | ...`)

```
| `c1v2-battery` (round 62; counter-validity battery, C1 operability) | instrument | `python3 corpus/evidence/round62/c1v2-battery.py --counter PATH --work DIR [--landed PATH] [--only SUBJECT...]`; when a counter runs a candidate tool, run this battery before the counter binds any data to that tool | `0` `BATTERY=PASS` (`LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4`) · `1` `BATTERY=FAIL` · `2` usage/env | do-nothing counters `corpus/evidence/round62/controls/null-pass.py` run here: `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL` exit 1; `null-fail.py`, `null-hashlist.py` `BATTERY=FAIL` (`controls/null-counters.txt`); round-61 counter `corpus/evidence/round61/c1-count.py` `FORGERS_REJECTED=0/12 BATTERY=FAIL` (`controls/c1v2-before.txt`); mutant set `controls/run-c1v2-controls.py` `CONTROLS_UNEXPECTED=0` (`controls/c1v2-controls.txt`, X10 SURVIVED as a named gap) | counter target `corpus/evidence/round62/c1v2-count.py` `BATTERY=PASS` and `LEGS=20/20 C1V2=PASS` at three fresh seeds (`[INFERENCE]` not run in this seat); contract `corpus/evidence/round62/claims.md` C1 | `--work` scratch only (fresh salted builders); no network | chousa
```

## Row 2 — Decision table (new decision row)

Insert after: line 26 (`| Write derived evidence (spans, manifests) under a caller-named directory (r61) | ...`), before the blank line 27.

```
| Open a path under a directory the caller does not control (r62) | pick the flag by the components it must judge: `O_NOFOLLOW` judges only the final component (`python3 -B corpus/evidence/round62/openat2-probe.py --work DIR` lines P02 `opened` through an earlier symlink, P03 `ELOOP` at the final one); `RESOLVE_NO_SYMLINKS` judges every component (P04 `ELOOP`, P05 `ELOOP`, P06 `opened` for a plain inside path); `RESOLVE_BENEATH` refuses an escape (P07 `EXDEV` for `..`, P08 `EXDEV` for an absolute link) and admits an inside relative link (P09 `opened`); the call is `openat2(437)` through `ctypes` because `os` has no openat2 (P01 `observed=False`); flag values from `/usr/include/linux/openat2.h` (S139); meaning from `openat2(2)` `RESOLVE_NO_SYMLINKS` (man-pages 6.19, S138, the note that its effect differs from `O_NOFOLLOW`) | `O_NOFOLLOW` alone to guard a path whose parent directories the caller does not control; reading `RESOLVE_BENEATH` as a symlink refusal (P09); typing flag values from memory | `RESOLVE_NO_SYMLINKS` with `RESOLVE_BENEATH` on a directory descriptor, plus a final-component `O_NOFOLLOW` or `O_PATH` check `[INFERENCE: the combined flag set is not probed; each flag is probed alone]`; the probe prints `PROBE_FACTS=14/14` and its `PROBE` lines equal `corpus/evidence/round62/openat2-probe.txt` | per-case `PROBE` lines matching the committed output; `PROBE_FACTS=14/14`; `diff` of those lines against the committed file empty
```

## Row 3 — Error patterns table (new error-pattern row)

Insert after: line 51 (`| the address check passes and the connection goes elsewhere (r30) | ...`), before the blank line 52.

```
| a counter exits 0 on a detection forger (r62) | the counter scores the builder's exit code only on the harness it runs; a builder that runs the unhardened base unless it detects the harness (cwd name, environment keys, command line, stdout type, file names) passes every leg. Round 61's counter read `C1=PASS` 20/20 on each of twelve forgers: `FORGERS_REJECTED=0/12 BATTERY=FAIL` (`corpus/evidence/round62/controls/c1v2-before.txt`). Run `corpus/evidence/round62/c1v2-battery.py` before the counter binds data; a docstring that says a counter rejects forgers is not that result (`corpus/evidence/round62/claims.md` C1) |
```

## Source trail (commands run in this seat)

- `python3 -B corpus/evidence/round62/controls/candidate-openat2-probe.py --work /fast/scratch/hyaku/chousa-r62/ScribeSkillRows/probe` → exit 0; 14 `PROBE` lines, `PROBE_FACTS=14/14`; stdout identical to `corpus/evidence/round62/controls/candidate-openat2-probe.txt` (second run diffed: `SAME`).
- `python3 -B corpus/evidence/round62/controls/null-pass.py` run as a battery counter: `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/controls/null-pass.py --work <scratch>/bat3` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL`, exit 1 (matches `controls/null-counters.txt`).
- `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` line 86 (RESOLVE_NO_SYMLINKS vs O_NOFOLLOW) and line 84 (`O_PATH`+`O_NOFOLLOW` final symlink).
- `/usr/include/linux/openat2.h` lines 33–45 (RESOLVE_* values); probe `HEADER` line `__NR_openat2=437`.
- Committed receipts read, not re-run: `controls/c1v2-before.txt` (`FORGERS_REJECTED=0/12`, every forger `counter_exit=0 want=1 MISS`), `controls/null-counters.txt`, `controls/c1v2-controls.txt` (`CONTROLS_UNEXPECTED=0`; X10 `SURVIVED`).
