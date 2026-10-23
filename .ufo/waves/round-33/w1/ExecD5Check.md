# Round 33 / W1 — D5 repair: `no-name-signals.sh` process-signal check

**Seat:** `ChousaR33.ExecD5Check` · **Routed defect:** D5
(`corpus/lessons/round-32-verifier-spotcheck.md:168-169`: seats must not signal processes by
name; `pkill -x sleep` killed three sibling `sleep` processes in RerunC1b).
**Verdict: PASS for D5 operability.** The check is delivered, fails on the round-32 tree at the
routed site with the exact `path:line`, passes on clean trees, and its false-positive classes are
enumerated below with a demonstrated treatment for each.

**Bounds honoured:** no `c1-count.py` invocation (control rule), no C1 work, no production-file
edit (`tools/`, `corpus/`, `SCORECARD.md`, …), no git/jj writes, no installs, no network, no
subagents, no background jobs, and no process signalled by me. Artifacts are confined to
`.ufo/waves/round-33/w1/ExecD5Check/` (14,246 B total, every file ≤ 1,520 B) plus scratch
`/fast/scratch/hyaku/chousa-r33/w1/ExecD5Check/` (the `TMPDIR`, one copy of this report for the
self-scan in `selfscan/`, its output, and the removed `chmod 000` probe fixture).

## 1. Deliverable

`.ufo/waves/round-33/w1/ExecD5Check/no-name-signals.sh` — 7,529 B, mode `755`,
SHA-256 `453388d0ed6b1b567162614d3430192d26724aa08ee374422e0cc605b969cb95`.

```
usage: no-name-signals.sh [--code-only] [--exclude PATH]... [--max-bytes N] DIR...
exit: 0 clean, 1 hits listed, 2 usage or I/O error
```

It walks `DIR...` recursively for `*.md *.sh *.py *.txt *.json` (files > 16 MiB skipped and
counted; binary files skipped by `grep -I`), prints one `HIT path:line [kind; category] excerpt`
line per hit — `kind` is `code` for `.sh/.py` and `doc` for `.md/.txt/.json` — then a summary line
and one verdict line whose exit code always matches the printed verdict. It excludes its own
resolved path so its pattern table cannot report itself.

Detected forms (all demonstrated in `fixtures/dirty`, 14 hits, exit 1):

| category | form | proof |
|---|---|---|
| `pkill` | any `pkill …` (`-x`, `-f`, …) | `fixtures/dirty/reports/seat.md:2`, `scripts/run.sh:3` |
| `killall` | `killall …`, `killall5` | `reports/seat.md:3-4`, `scripts/run.sh:4` |
| `kill-cmdsub` | `kill [opts] $(pgrep …)`, quoted/backtick forms, `$(pidof …)` | `reports/seat.md:5-8`, `scripts/run.sh:5` |
| `xargs-kill` | `pgrep`/`pidof`/`ps … \| xargs … kill` | `reports/seat.md:9-10`, `data/receipt.json:1` |
| `kill-ps-name` | `kill [opts] $(ps … -C name …)` | `reports/seat.md:11` |

Regexes are bash EREs (`RE_PKILL`, `RE_KILLALL`, `RE_CMDSUB`, `RE_PSNAME`, `RE_XARGS` at
`no-name-signals.sh:62-65`). A union pre-filter (`grep -lZI`) selects candidate files; each
candidate is then scanned line-wise so the hit set is deduplicated and line numbers are exact.

## 2. Evidence — it fails on round-32, passes on clean trees

Commands run from `.ufo/waves/round-33/w1/ExecD5Check/` with
`TMPDIR=/fast/scratch/hyaku/chousa-r33/w1/ExecD5Check/tmp` and `timeout` bounds:

| command (abridged) | exit | key output |
|---|---|---|
| `./no-name-signals.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32` | **1** | `HIT …/round-32/w2/RerunC1b.md:31 [doc; pkill] …` |
| same, elapsed `date +%s` pair | 1 | 2 s; 480 candidate / 1,525 scanned / 0 large skipped |
| `./no-name-signals.sh fixtures/clean` | **0** | `0 hits … RESULT CLEAN (exit 0)` |
| `./no-name-signals.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/tools` (real tree) | **0** | `0 hits, 2 scanned` |
| `./no-name-signals.sh fixtures/dirty` | 1 | 14 hits, all five categories |
| `./no-name-signals.sh fixtures/prose` | 1 | 4 doc hits (rule citations) |
| `--exclude fixtures/prose/citations.md --exclude fixtures/prose/incident.txt fixtures/prose` | **0** | adjudicated suppression works |
| `--code-only fixtures/dirty` | 1 | 3 hits, all `[code; …]` |
| `--max-bytes 10 fixtures/dirty` | 0 | `3 large file(s) skipped (> 10 B)` |
| `./no-name-signals.sh fixtures/names` | 1 | hits on `-dashfile.md` and `has space.md` |
| `./no-name-signals.sh --exclude fixtures .` | **0** | 1 scanned (the script itself), 0 hits → self-exclusion |
| no arguments | **2** | usage on stderr |
| `/nonexistent-p33` | **2** | `not a directory` |
| `chmod 000` fixture holding `pkill` | **2** | stdout `RESULT INCOMPLETE (exit 2…)`; stderr `IO-ERROR cannot scan batch (1 file(s)): grep: … Permission denied` |

The round-32 hit, verbatim from `.ufo/waves/round-32/w2/RerunC1b.md:31` (context read at
`:28-36`), where the seat discloses the incident:

```
so it is counted as a concurrency-only pair. My cleanup `pkill -x sleep` in an early probe also
killed 3 sibling `sleep` processes (pids 3866732, 849717, 893574) — overbroad, mine would have
sufficed.
```

Independent oracle over the same tree (same five extensions):
`grep -rnE '\bpkill\b|\bkillall\b' --include='*.md' --include='*.sh' --include='*.py' --include='*.txt' --include='*.json' …/.ufo/waves/round-32`
→ exit 0, exactly one line, `round32/w2/RerunC1b.md:31`. The checker found the same single line
(`out/round32.out`, SHA-256 `9b49b2317ad08be1f2ad52ee5246cc3e3b8fa631ba33d276cca4706d52e4f2ff`).
No other round-32 artifact contains a name signal, so a clean result on this tree would have been
a checker miss, not a clean tree.

Retained outputs (`out/`): `round32.out`, `dirty.out` (`e8e5bcfd…`), `clean.out`
(`d007ffaf…`), `prose.out` (`cbdc1748…`), plus `prose-excluded`, `dirty-codeonly`, `sizeguard`,
`names`, `ioerror`, `selfexclude`, `lane-tools`, `noargs`, `nodir` (`.out`/`.err` pairs).

Tooling observed (no installs): `GNU bash 5.3.20`, `grep (pi-uu-grep) 0.2.0`, `find 0.8.0`;
all flags used (`grep -E -I -l -n -Z`, `find -printf %s\0%p`, `sort -z`, `readlink -f`) behaved
as required in every run above.

## 3. False positives and how they are treated

The check reports **text**, not executed commands. Classification is deliberately fail-closed:
any line containing a detected form is listed and the exit is 1. Each class below was exercised.

| # | class | where exercised | treatment |
|---|---|---|---|
| 1 | prose that quotes the rule/incident (`pkill`, `killall`, verbatim ban lists) | `fixtures/prose/citations.md:2,3,4`, `incident.txt:1` | **Listed as `[doc; …]`, exit 1.** Indistinguishable from a recorded command at text level — and required here: the round-32 D5 evidence is itself prose (`RerunC1b.md:31`). |
| 2 | deny-list table rows / string literals naming the tools | `citations.md:4`; `dirty/data/receipt.json:1` | listed as doc hits for the same reason. |
| 3 | the checker's own pattern table and header | `.` with `--exclude fixtures` | excluded by resolved absolute path: 1 file scanned, 0 candidate, exit 0. |
| 4 | code comments containing a banned token | same rule as class 1 (`code` kind) | listed; a comment can be uncommented, and intent is not computable from text. |
| 5 | a report that quotes a command while documenting it | this report itself, copied to `/fast/scratch/hyaku/chousa-r33/w1/ExecD5Check/selfscan/report.md` | **Observed:** exit 1, 11 `[doc; …]` hits (`report-selfscan.out`, SHA-256 `9f6eff312d10c07599da4d227c632a75c58d36286021878a3cb3d969a62e8760`); scope scans should pass `--exclude .ufo/waves/round-33/w1/ExecD5Check.md`. |
| 6 | **not hits (verified)**: inspection (`pgrep -af …`, `ps -ef \| grep …`), scoped kills `kill "$pid"`, `kill -- -$$`, `kill %1`, `kill -TERM 4321`, `kill -TERM $(cat gate.pid)`, English words (`killer`, `kill switch`, `killing`, `skilled`) | `fixtures/clean/reports/seat.md`, `fixtures/clean/scripts/run.sh` | 0 hits, exit 0 — the check does not punish the required scoped-cleanup pattern. |

Adjudication is explicit, never silent: `--exclude PATH` (repeatable) drops one file or subtree by
resolved path; the summary still reports how many files were scanned, and excluding every
candidate yields `0 candidate file(s), 0 scanned file(s)` rather than a false "clean tree".

## 4. Limits (reported, not fixed)

- Evasion is not detected: aliasing (`alias pk=pkill`), token concatenation, `command pkill`,
  `busybox killall`, `ssh host pkill`, and pipelines split across lines (`pgrep … \` newline
  `| xargs kill`). This is a hygiene gate, not an adversary-proof sandbox.
- `kill $(ps …)` without `-C`, and non-`xargs` pipelines (`ps | awk | while read; kill`), are out
  of scope; `kill -9 -1` and direct PID lists are not name/pattern signalling and deliberately
  pass.
- `grep -I` silently skips binary files even if they contain a match; symlinks are not followed
  (`find -type f`), and files above `--max-bytes` are counted as skipped in the summary.
- The check cannot prove a listed command executed — only that the artifact text carries the
  form. That is the same limitation as the routed disclosure.

**Integration (parent-owned):** the script is *not* wired into `tools/research-gate.sh`; seats may
not edit lane production files. Parent can invoke it per wave as a pre-data control, e.g.
`.ufo/waves/round-33/w1/ExecD5Check/no-name-signals.sh .ufo/waves/round-33` and adjudicate `[doc]`
hits, or fold the five regexes into the gate battery. Round-32 is the regression case (must exit 1 with
`w2/RerunC1b.md:31`); `fixtures/clean` and the lane `tools/` tree are the clean cases (must exit 0).
