# MutC1V2Run — mutation test of the v2 counter `run()` and sandbox (round 62, w1)

Target: `corpus/evidence/round62/c1v2-count.py` (sha256 prefix `b7016fba91b03460`, unmodified).
Battery: `corpus/evidence/round62/c1v2-battery.py` (prefix `9afe00b917fb95e2`, unmodified).
Every mutant was a copy in scratch laid out as `<dir>/corpus/evidence/round62/c1v2-count.py` + `<dir>/tools/capture-text.py`,
run as `python3 -B <lane>/corpus/evidence/round62/c1v2-battery.py --counter <mutant> --work <scratch>/b/<name>`
(default `--landed` = lane `tools/build-spans.py`). Nothing under the lane was written; scratch removed; no installs.

## Findings

- Intact control (frozen counter, same command): `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, exit 0 (log line from `DONE X00-intact`). My harness reproduces the frozen result.
- 17 new mutants (M01–M17; none of X01–X12). Battery: **5 KILLED** (battery exit 1), **12 SURVIVED** (battery PASS).
- Of the 5 KILLED, 3 are killed by a forger accepted (M01, M02, M10: F12, F12, F10). 2 are killed without any forger: M07 rejects honest builders, M15 fails closed on every subject. They count as KILLED but do not show forger coverage.
- Of the 12 SURVIVED, **7 are real control gaps** (M03, M05, M06, M09, M11, M12, M13). Each has a named builder that the mutant accepts (or hangs on) and the intact counter rejects (or survives). The battery has no subject for these paths. **5 are equivalent** (M04, M08, M14, M16, M17), with the reason given per row.
- Battery-level verdicts are not the whole story for the gap rows: the kill builders below were run through the mutant counter directly (`--builder`, or one leg via a probe harness). They are not in the frozen battery and are not a rewrite of it; they are candidate limits for the next round.
- Operability note: a battery run took 128–240 s when four ran concurrently on this host (X00 170 s), not the "about 50 s" in the brief. Calibration only.

## Results table

Edit = exact old→new text applied to the frozen counter (each asserted to match its stated count, then compiled).
"Forgers newly accepted" = battery `SUBJECT FORGER … MISS` lines (battery log).

| # | mutant and edit | battery verdict (log) | forgers newly accepted | KILLED/SURVIVED | classification |
|---|---|---|---|---|---|
| M01 | tools-true: `tools_unchanged` body → `return True` | `FORGERS_REJECTED=11/12 BATTERY=FAIL`, exit 1 | F12 | KILLED | forger kill (P03 is the only tools check; F12's `__pycache__` then passes) |
| M02 | tools-py-only: compare only `*.py` entries (`p.suffix == '.py'`, `n.endswith('.py')`) | `11/12 BATTERY=FAIL`, exit 1 | F12 | KILLED | forger kill (a `__pycache__` dir is invisible to the filter) |
| M03 | clean-true: `clean_out` → `return True` | `12/12 BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP** — killer `fI2` (below) |
| M04 | clean-no-symlink: `if not fx.out.is_dir() or fx.out.is_symlink():` → `if not fx.out.is_dir():` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **equivalent** — `snap()` on a symlink root returns `{".": ("l", target)}` (counter lines 109–110), so the final `all(v[0]=="d")` is False anyway. Probe `fA` (refusal leaves `out` as symlink to empty dir): P05 FAIL under intact and M04 alike |
| M05 | rc-shift: `rc = os.waitstatus_to_exitcode(status)` → `rc = status >> 8` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP** — killer `fB-segv` (below) |
| M06 | rss-zero: `"rss_kib": ru.ru_maxrss,` → `"rss_kib": 0,` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP** — killer `fC-rss` (below) |
| M07 | rusage-children: `wait4` → `waitpid` + `getrusage(RUSAGE_CHILDREN)` (2 sites) | `LANDED=0/3 POSITIVES=1/4 FORGERS_REJECTED=12/12 BATTERY=FAIL`, exit 1 | none | KILLED | killed by **false rejects** of honest builders (max RSS over all earlier children, e.g. H20 ~230 MiB), not by forgers |
| M08 | no-fsize: remove `setrlimit(RLIMIT_FSIZE, …)` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **equivalent for forgers** — F08 (cheats unless FSIZE == 512 MiB) is rejected in plain (detection false → base) and in neutral (random 384 MiB/768 MiB/1 GiB ≠ 512 MiB). Named limit: no frozen subject writes >384 MiB; FSIZE only bounds disk (INFERENCE that no forger uses it) |
| M09 | no-kill-child: `SANDBOX` without `--kill-child` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP in the stated guarantee, verdict-invisible** — probe `orphanMARKG` (below): two orphan builders alive after the counter returned |
| M10 | no-mount-proc: `SANDBOX` without `--mount-proc` | `11/12 BATTERY=FAIL`, exit 1 | F10 | KILLED | forger kill (host `/proc` shows the counter's command line, so F10 goes honest in both profiles) |
| M11 | stderr-undrained: neutral `drain()` returns at once for stderr (`if store is not None: return`) | `BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP (positive side)** — killer `pD-bigstderr` (below): a correct builder is rejected |
| M12 | timeout-false: `"timeout": rc == -9}` → `"timeout": False}` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP** — killer `fE-hang-bigform` (below) |
| M13 | no-new-session: `start_new_session=True` → `False` (2 sites) | `BATTERY=PASS`, exit 0 | none | SURVIVED | **GAP** — killer `orphanMARKG` hang (below): counter never returns |
| M14 | timer-pid-only: `lambda: os.killpg(p.pid, SIGKILL)` → `lambda: p.kill()` (2 sites) | `BATTERY=PASS`, exit 0 | none | SURVIVED | **equivalent under `--kill-child`** — probe `orphanMARKG`: 0 orphans, same as intact (unshare death → PDEATHSIG kills pid 1 → namespace gone) |
| M15 | no-user-ns: `["unshare", "-Ufp",` → `["unshare", "-fp",` | `LANDED=0/3 … BATTERY=FAIL`, counter exit 2 on every subject | none | KILLED | killed by the **fail-closed gate** (host is non-root; no `-U` → unshare fails), not by forgers |
| M16 | as-plain-only: `setrlimit(RLIMIT_AS)` only if `fx.profile != 'neutral'` | `BATTERY=PASS`, exit 0 | none | SURVIVED | **equivalent for the battery** (INFERENCE, not probed): a forger counts only if it passes both profiles, and the plain profile still enforces AS; no frozen subject allocates against AS (X10 already named this gap) |
| M17 | no-finally-killpg: remove post-wait `os.killpg(p.pid, SIGKILL)` (2 sites) | `BATTERY=PASS`, exit 0 | none | SURVIVED | **equivalent under the PID namespace** — probe `fH2` (helper writes a marker 2 s after the builder exits): marker absent under intact (0/2) and M17 (0/2); a no-sandbox control writes it (2/2), so the probe is sensitive |

## Killer builders for the gap rows (run through the mutant counter; not in the frozen battery)

All probes used the mutant counter file directly. "intact" = frozen `c1v2-count.py`. Each forger file is landed `build-spans.py` embedded (zlib+base64) with a wrapper; `land()` returns the landed exit code.

- **M03 — `fI2-residue-fresh.py`** (on refusal, if `out/` was absent before the run, leave `out/spans/S999-1.txt`). Full counter: intact `LEGS=13/20 C1V2=FAIL` (P05, H14, H15, H17, H18, H19, H20 fail); M03 `LEGS=20/20 C1V2=PASS` (twice). The frozen battery has no refusal subject that leaves residue (its base builder leaves none). Battery would accept it.
- **M05 — `fB-segv.py`** (landed; after rc 0, `ctypes.string_at(0)`). Intact: `LEG P01 TXT fail … rc=-11`, `LEGS=15/20`; M05: `LEGS=20/20 C1V2=PASS`. Note: a pid-1 builder that SIGKILLs itself is ignored by its own PID namespace; the probe `fB-sigkill` (SIGKILL) exits 0 under intact too (`LEGS=20/20`), so it is not a kill. Use SIGSEGV.
- **M06 — `fC-rss.py`** (landed; if any cache file >8 MiB, hold 110 MiB resident and exit 1). Intact: `LEG H14 BIGTXT fail … rss_kib=125684 limit=98304`, H15 `rss_kib=126396`, `LEGS=18/20`. M06: H14/H15 `rss_kib=0`, `LEGS=20/20 C1V2=PASS`.
- **M09 — `orphanMARKG.py`** (`os.setsid(); time.sleep(10**6)`), one leg `leg_p01` per profile through `probe.py`, each run waits out the 60 s timeout. Under M09, after the probe returned, two orphan `build-spans.py`/`ageko.py` processes were alive (`pgrep` showed pids under `probes/w-G-M09-p01/plain` and `/neutral`). Intact: 0 orphans; M14: 0. The battery never times out, so its verdict does not move. The claim's words "no helper outlives the builder" hold only with `--kill-child`, and M09 shows that on the timeout path.
- **M11 — `pD-bigstderr.py`** (a correct landed builder that writes 300 000 bytes to stderr first; POSITIVE). `leg_p01`: intact plain `rc=0`, neutral `rc=0`; M11 plain `rc=0`, neutral `rc=-9` (pipe full, 60 s timeout) → FAIL. No battery positive writes more than 64 KiB to stderr.
- **M12 — `fE-hang-bigform.py`** (landed; `time.sleep(10**6)` if a `.raw` member exceeds 10 MiB, i.e. the H20 DOCX). `leg_h20`: intact `(False, 'rc=-9 …')` in both profiles; M12 `(True, 'rc=-9 …')` in both profiles. No battery subject hangs.
- **M13 — `orphanMARKG.py` (hang)**, `leg_p01` through the M13 counter with `timeout 200`: exit 124 (did not return within 200 s); the Timer thread printed `ProcessLookupError` at `os.killpg` (mutant line 350). Intact returns after 60 s with `rc=-9`. A hung subject in the battery would stall the counter until the battery's 1800 s subprocess timeout raised.
- **M04 — `fA-outlink.py`** (refusal leaves `out` as symlink to an empty dir): P05 FAIL under intact and M04 alike (`LEGS=13/20` both). Shows the equivalence above.
- **M17 — `fH2-helper-writes.py`** (after rc 0, a `setsid` child writes `HELPER-WROTE` 2 s later): marker absent after probe under intact (0/2) and M17 (0/2). No-sandbox control (`SANDBOX = []`): marker present (2/2).
- **M14** — see `orphanMARKG` probe above (0 orphans, as intact).

## Survivor classification

- Gaps (7): M03 (`fI2`), M05 (`fB-segv`), M06 (`fC-rss`), M09 (`orphanMARKG`, setsid + hang, leftover processes), M11 (`pD-bigstderr`), M12 (`fE-hang-bigform`), M13 (hang builder).
- Equivalent (5): M04 (snap symlink entry), M08 (F08 rejected by neutral in both cases; FSIZE not verdict-relevant for frozen forgers), M14 (`--kill-child` tears namespace down), M16 (both-profile rule; AS not used by any subject, INFERENCE), M17 (PID-namespace teardown; probe-backed).
- Routed to the next round's battery as limits, not rewrites: M03/M05/M06/M11/M12/M13 each need a subject; M09 needs a timeout-path orphan check; M12/M13 cost ~60 s per hung leg.

## Method and bounds

- Mutants: exact-string edits, each asserted to match its count (1 unless noted), `py_compile` checked. Intact X00 run beside them.
- Each battery run used a fresh `--work`; all completed (none hung). Concurrency 4.
- Probes: `probe.py` imports the counter module and calls one `leg_*` with a builder for plain and neutral; full-counter probes used `python3 -B <counter> --builder <forger> --work <dir>`.
- Hygiene: NS-init processes ignore SIGTERM; killed with `pkill -9` (M09/M13 leftovers) and confirmed 0 remaining. Scratch `/fast/scratch/hyaku/chousa-r62/MutC1V2Run/` removed. Frozen files unchanged (sha256 prefixes above re-read after the runs; no lane writes; no git mutation).
- Tools: none installed; `unshare`, `setsid`, Python 3.14.8 as present.

VERDICT: KILLED=5/17 survivors_that_are_gaps=7
