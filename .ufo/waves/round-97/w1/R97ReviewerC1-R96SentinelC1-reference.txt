# R96SentinelC1 — side-effect audit of `tools/search-rerun.py --selftest` at F (claim C1, K4)

Seat: `R96SentinelC1` (leaf, no dispatch). Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Attacked tree: clone `--shared` of the lane at `2db151c5ea0883de0b9dc8d95c6fac1755e1056a` (the freeze F), under
`/fast/scratch/hyaku/chousa-r96/R96SentinelC1/repo`. Scratch removed at exit. No lane file, no sibling repo,
no `scripts/`, no `.ufo/state`, no `MANIFEST.json` was written; the only files I wrote are this report and the
13 receipts beside it.

Tools: `strace` 7.2 (system), `/usr/bin/grep` GNU 3.12, Python 3.14.8 (system). No installs, no network.

---

## Scope answered first, in the order asked

| Question | Answer |
|---|---|
| Every opened path not interpreter/stdlib? | **Only the tool's own source and its directory** (`…/repo/tools/search-rerun.py`, `…/repo/tools`). Nothing else outside `/usr/lib/python3.14`, `/usr/lib/lib*`, `/usr/lib/locale`, `/usr/lib/gconv`, `/etc`, `/usr/bin`. |
| Every `execve`? | **One** — `/usr/bin/python3` itself. No `git`, no other binary. |
| Every `connect`? | **None.** Also no `socket`/`bind`/`listen`/`accept`/`sendto`/`recvfrom`/`socketpair` at all. |
| Every write to an fd other than 1/2? | **None.** 66 `write(1, …)`, zero elsewhere. No `openat` with `O_WRONLY`/`O_CREAT`/`O_TRUNC`/`O_APPEND`. No `creat`/`unlink`/`rename`. |
| Does `m08-env-scrub` leave `os.environ` exactly as it was? | **Yes** — `ENV_IDENTICAL True`, `ENV_DIFFS {}` in all three caller configurations (no `GIT_DIR`; hostile `GIT_DIR`/`GIT_OBJECT_DIRECTORY`/`GIT_ALTERNATE_OBJECT_DIRECTORIES`; `GIT_DIR` set to the empty string). The case restores `GIT_DIR` in a `finally`. |
| Does `--selftest` behave the same with hostile `GIT_DIR`/`PYTHONPATH`? | **`GIT_DIR`: yes** (identical `PASS cases=32/32`, exit 0, for `/nonexistent`, `/etc`, a hostile repo, and a clone holding the base commit). **`PYTHONPATH`: no** — see Finding 5. |
| Does the battery write only under `--work` and clean up on a failing run? | **Writes only under `--work` — yes, except the lane's `.git/index`** (Finding 4). **Cleanup on a normal failing run: yes (0 leftovers). On a killed run: no — 48 files left** (Finding 6). |

---

## Findings, most severe first

### Finding 1 — HIGH: `m08-env-scrub` does not assert `GIT_NO_REPLACE_OBJECTS`; dropping it yields a **false CLEAN** verdict, and no lane instrument notices

`tools/search-rerun.py:478` — the whole assertion is:

```python
case("m08-env-scrub", "GIT_DIR" not in env and env.get("GIT_NO_LAZY_FETCH") == "1")
```

`git_env()` (line 113-118) sets three guards — `GIT_NO_REPLACE_OBJECTS=1`, `GIT_NO_LAZY_FETCH=1`,
`GIT_TERMINAL_PROMPT=0` — and the module docstring calls the first of them the guard that keeps the re-run
"off another object store" ("with replace refs and lazy (promisor) fetches switched off"). The selftest asserts
**one** of the three. `grep -n 'GIT_NO_REPLACE_OBJECTS\|GIT_TERMINAL_PROMPT'` over
`corpus/evidence/round95/` + `corpus/evidence/round96/` returns **0 hits**: the guard the lane documents is
asserted by no test in either round.

**Exploit path (receipt `R96SentinelC1-replace-refs-false-clean.txt`).** A one-site mutation of `git_env()`
that drops `"GIT_NO_REPLACE_OBJECTS": "1"` (mutant `E1`) passes the selftest 32/32 (exit 0), passes the
round-95 battery (`RERUN_CONTROLS=PASS`, exit 0) **and** passes the round-96 battery
(`MUTANTS_KILLED=23/23 … SELFTEST_CONTROLS=PASS`, exit 0). With that mutation, a repo-local
`refs/replace/<blob>` — a ref, not part of the commit tree, so `git status --porcelain` stays clean — makes
`git cat-file blob` return attacker bytes for the recorded revision:

* the record claims `hits=1` at a revision whose committed blob does **not** match (0 matches in truth);
* the mutant prints `SEARCH_RERUN: CLEAN`, exit 0 — **a false CLEAN on a false record**;
* the shipping tool on the same repo and the same replace ref prints `SEARCH_RERUN: DRIFT`, exit 1.

Control: deleting the replace ref makes the mutant report DRIFT (exit 1) and the shipping tool report DRIFT
(exit 1). The replace ref is the sole cause of the divergence.

This is the round-95 sentinel's own containment class (`git_env`'s docstring cites "R95SentinelScope findings
1,2,4"), re-opened and unasserted in round 96.

### Finding 2 — MEDIUM-HIGH: the `NO_WRITE` group cannot see a lane write, so K4 ("`--selftest` writes a file") is unenforced

The group compares `git status --porcelain` before and after (battery lines 161-165). Two blind spots, both
demonstrated:

**(a) Baseline poisoning** (receipt `R96SentinelC1-no-write-ordering-detail.txt`). The battery runs the tool under
test in the **POSITIVE leg first** (`selftest(tool)`, cwd = lane root, ambient `HOME`), long before the NO_WRITE
leg's `before` snapshot. A lane write the selftest makes is therefore *already in the baseline*. Mutant `W3`
(one site: the selftest writes `tools/lane-side-effect.txt`) yields
`CASE no-write rc=0 left=[] lane_status_same=True ok` → `NO_WRITE=1/1` → `SELFTEST_CONTROLS=PASS`, exit 0 —
while the lane has gained the file (`?? tools/lane-side-effect.txt`).
Control: the same tool's NO_WRITE leg run **in isolation** on a clean lane *does* detect it
(`before='?? tools/mutant-W3-tmp.py\n'`, `after='?? tools/lane-side-effect.txt\n?? tools/mutant-W3-tmp.py\n'`,
not equal).

**(b) Porcelain prints paths, not content** (receipt `R96SentinelC1-no-write-blindspot.txt`). Mutant `T1`
(one site: the selftest appends to the **tracked** capture `corpus/captures/1a8c36c4c24444967bd9c3ce.txt`) also
scores `NO_WRITE=1/1 ok` while the tracked file is genuinely corrupted — `git diff --stat` shows
`5 ++++-`, and the file contains `CORRUPTED-BY-SELFTEST` twice. The porcelain line is ` M corpus/captures/…`,
identical before and after, because porcelain reports the path and the status letter, never the bytes.

The group does have power against a write into the empty cwd (`W1` → `left=['selftest-side-effect.txt']`,
`NO_WRITE=0/1`, `SELFTEST_CONTROLS=FAIL`), so the group is not vacuous — but the lane-write case, which is what
K4 names, is invisible to it.

### Finding 3 — MEDIUM: the selftest has no case for a row carrying **two** codes; `findings += len(bad)` may be collapsed to `1`

`evaluate` appends one code per condition, so a row can carry `COUNT_DRIFT,SET_DRIFT` together (the round-95
battery's own `f5-zero` and `f6-engine` forgeries produce exactly that). No `j*` case in the selftest has a
row with two codes, so `findings += len(bad)` and `findings += 1 if bad else 0` are indistinguishable there.
Mutant `A` (one site) passes the selftest 32/32 (exit 0), the round-95 battery (`RERUN_CONTROLS=PASS`, exit 0)
**and** the round-96 battery (`SELFTEST_CONTROLS=PASS`, exit 0). Receipt
`R96SentinelC1-mutant-findings-collapse-and-partial-scrub-verdict.txt` shows the observable difference on a
forged row with both a count and a set drift:

* shipping tool → `findings=2`, exit 1
* mutant A → `findings=1`, exit 1

The verdict is unchanged, so this is a reporting defect rather than a wrong verdict — but the tool's summary line
under-reports the number of findings, and no lane instrument distinguishes the two forms.

### Finding 4 — LOW-MEDIUM: the battery's own header says "Read-only on the lane (`git show`, `git status`)", but `git status` rewrites the lane's `.git/index`

Receipt `R96SentinelC1-battery-writes-lane-index.txt`. `git status --porcelain` refreshes the stat cache and
**rewrites `.git/index`**; the index sha256 changes across a single `git status` call (measured). `git show`
does not (control). So the round-96 battery writes a file outside `--work`, into the lane's `.git` directory.
The bytes are a stat-cache refresh, not content — the lane's tracked files and HEAD are unaffected and the
"lane status unchanged" property the claim states still holds — but the battery's own "Writes only under
`--work`" and "Read-only on the lane" statements are not literally true.

### Finding 5 — LOW: `--selftest` is not hermetic against a hostile `PYTHONPATH`

Receipt `R96SentinelC1-hostile-pythonpath.txt`. The tool imports `hashlib` (and `argparse`, `fnmatch`, `os`,
`re`, `subprocess`) by bare name, so a `PYTHONPATH` entry shadowing a stdlib module changes the selftest's
behaviour: with a shadowing `hashlib.py`, `--selftest` dies with `ImportError: hostile hashlib shadow` and
**exit 1** — never reaching its 32 cases, so the gate's PASS line never appears and the failure looks like a
genuine tool defect. A `sitecustomize.py` on `PYTHONPATH` executes **before** the tool's own code and can
write into the lane (demonstrated: `injected-by-sitecustomize` appeared in the lane root, and the battery
correctly reported `NO_WRITE=0/1`). The battery inherits `PYTHONPATH` too. Low severity — it needs a hostile
environment, and the tool's docstring already says "Python 3.13+ standard library only" — but the selftest is
registered as a *gate*, so a hostile `PYTHONPATH` turns the gate into an arbitrary-code executor.

### Finding 6 — LOW-MEDIUM: the battery cleans up only on a normal exit

Receipt `R96SentinelC1-battery-cleanup.txt`. Cleanup is `finally: shutil.rmtree(work, ignore_errors=True)`, which
`SIGKILL` and `SIGTERM` bypass. A run killed mid-way leaves **48 files** under `--work` (the base-tool copy, the
23 mutant copies, the oracle stubs) — measured for both signals. A *normal failing* run (exit 1) cleans up fully
(0 leftovers). Nothing is written outside `--work` and the lane is untouched, so the blast radius is confined to
the operator's scratch dir; the claim's "Writes only under `--work`" survives, but the battery docstring's
"(removed at exit)" does not.

### Finding 7 — LOW: the `GIT_*` scrub is only checked for `GIT_DIR`; a narrowed scrub survives every lane instrument

Receipt `R96SentinelC1-partial-git-scrub.txt`. Mutant `D` changes the scrub to keep every `GIT_*` variable except
`GIT_DIR` (`if k != "GIT_DIR"` instead of `if not k.startswith("GIT_")`). It passes the selftest 32/32 (exit 0)
and the round-95 battery (`RERUN_CONTROLS=PASS`, exit 0). Under a hostile `GIT_WORK_TREE` or
`GIT_OBJECT_DIRECTORY` the mutant refuses (`SEARCH_RERUN_ERROR ROOT` / `REV`, exit 2) rather than lying — the
containment still fails closed, which is why I score this LOW rather than HIGH. But `GIT_CONFIG_GLOBAL` passes
through unscrubbed and the verdict stays `CLEAN` (exit 0) either way, so the narrowing is silent. The r96
mutant `m20-no-env-scrub` only distinguishes the full scrub from no scrub at all.

---

## What holds

* **The shipped `--selftest` is itself clean under strace** — no file written, no `git` executed, no socket
  opened (receipt `R96SentinelC1-strace-selftest.txt`). The K4 kill rule is not violated by the tool as it
  stands; it is the *instrument* that cannot enforce it.
* **C1 predicate 1** holds: `python3 -B tools/search-rerun.py --selftest` → exit 0, last line
  `SEARCH_RERUN_SELFTEST: PASS cases=32/32`, 32 case lines, breakdown 14 parse / 8 matching / 10 judgement —
  matching the claim's "14 parse cases, 8 matching cases and 10 judgement cases" exactly
  (`R96SentinelC1-c1-predicate-verification.txt`).
* **C1 predicate 3** holds: `grep -c '^| \`search-rerun\` (r96 re-registration' SKILL.md` → 1, kind cell
  `gate`.
* **The "Before" state** holds: the base tool at `bbf64970` exits 2 on `--selftest` (argparse: the subcommand
  is required).
* The selftest is deterministic (5 runs, identical md5) and cwd-independent.
* The round-95 battery and mutant rebuild still pass on the changed tool: `REGRESSION_R95=2/2`, full battery
  `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1
  REGRESSION_R95=2/2 CASES=32` → `SELFTEST_CONTROLS=PASS`, exit 0 (full run with the regression leg, ~10 min).
* All 23 named mutants are killed (23/23); the three stand-ins are rejected (3/3); the base tool exits 2.
* **C2 was not falsified** (receipt `R96SentinelC1-c2-controls-and-predicate.txt`).
  `gate-records.py verify` → `GATE_RECORDS files=1 records=31 ok=31 fail=0` exit 0;
  `research-gate.sh verify-metadata` → `METADATA_COMPLETE=1/1 … RESEARCH_GATE: CLEAN` exit 0;
  `search-rerun.py verify corpus/knowledge/search-peer-review-dedup-r96.md --root .` →
  `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 … SEARCH_RERUN: CLEAN` exit 0;
  `entry-controls-r96.py` → `FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SEARCHES=3/3 … ENTRY_CONTROLS=PASS` exit 0.
  My C2 work was a side-effect check on the `verify` path (the same tool, same exit-2 containment), so I did not
  audit the entry's 8 decision rows against their quotes — that is the C2 depth seat's scope, not mine.

---

## Smallest remediations

1. **Finding 1** — extend `m08-env-scrub` to assert all three guards and the full scrub:
   `env.get("GIT_NO_REPLACE_OBJECTS") == "1" and env.get("GIT_TERMINAL_PROMPT") == "0" and not [k for k in env if k.startswith("GIT_") and k not in (...)]`.
   Verified: the strengthened assertion still passes the shipping tool (`PASS cases=32/32`, exit 0). Add a
   round-96 mutant at the `env.update(...)` site so the guard is inside the 23.
2. **Finding 2** — take the NO_WRITE `before` snapshot **before** any group invokes the tool (or snapshot the
   lane's file mtimes/hashes rather than porcelain), and compare tracked-file *content* (`git diff --stat`
   or a hash of the tracked tree), not porcelain paths.
3. **Finding 3** — add one judgement case whose row carries two codes (e.g. count drift **and** set drift),
   asserting `findings == 2`.
4. **Finding 5** — invoke the gate with `-I` (or `-E` plus an explicit `PYTHONPATH=`) so a hostile
   `PYTHONPATH` cannot shadow a stdlib module.
5. **Finding 6** — install a `SIGTERM`/`SIGINT` handler that cleans up, or document that a killed run leaves
   `--work` populated.
6. **Finding 4** — either drop the "Read-only on the lane" wording (it is `git status` that writes) or use
   `git --no-optional-locks status` / `GIT_OPTIONAL_LOCKS=0` to avoid the index refresh.

---

## Receipts (all under `.ufo/waves/round-96/w1/`, prefixed `R96SentinelC1-`)

| File | Covers |
|---|---|
| `R96SentinelC1-strace-selftest.txt` | strace of `--selftest`: opens, execve, connect, writes, clone, cwd dir after |
| `R96SentinelC1-m08-environ.txt` | `os.environ` restoration, 3 caller configurations |
| `R96SentinelC1-replace-refs-false-clean.txt` | Finding 1 — false CLEAN, with delete-ref and shipping-tool controls |
| `R96SentinelC1-no-write-blindspot.txt` | Finding 2b — tracked-file corruption scored `NO_WRITE=1/1 ok`; cwd-write control |
| `R96SentinelC1-no-write-ordering.txt` | Finding 2a — lane write scored `NO_WRITE=1/1 ok`, battery PASS |
| `R96SentinelC1-no-write-ordering-detail.txt` | Finding 2a mechanism — baseline poisoning, with isolated-leg control |
| `R96SentinelC1-mutant-findings-collapse-and-partial-scrub-verdict.txt` | Findings 3 and 7 — `findings=2` vs `findings=1`; scrub narrowing |
| `R96SentinelC1-battery-writes-lane-index.txt` | Finding 4 — `.git/index` rewritten by `git status`; `git show` control |
| `R96SentinelC1-hostile-pythonpath.txt` | Finding 5 — shadowed `hashlib`, `sitecustomize.py` write |
| `R96SentinelC1-battery-cleanup.txt` | Finding 6 — 48 leftovers on SIGKILL/SIGTERM; 0 on normal failure |
| `R96SentinelC1-battery-inventory-and-predicate.txt` | battery source anatomy; unasserted guard sites; E1 through both batteries |
| `R96SentinelC1-c1-predicate-verification.txt` | C1 predicates 1 and 3, case-count breakdown, base-tool exit 2 |
| `R96SentinelC1-c2-controls-and-predicate.txt` | C2 predicates 1-4 — all CLEAN; C2 not falsified |
| `R96SentinelC1-partial-git-scrub.txt` | mutant D at the scrub site, with the r95 battery result |

---

VERDICT: R96SentinelC1 C1 fired — the shipped `--selftest` is strace-clean and every C1 predicate holds, but the claim's K4 kill rule ("`--selftest` writes a file") is unenforced by the instrument that claims to enforce it (the `NO_WRITE` group scores a tracked-file-corrupting and a lane-writing selftest `1/1 ok`), and `m08-env-scrub` leaves `GIT_NO_REPLACE_OBJECTS` unasserted, so a one-site mutation passes every lane instrument while turning a false record into a false CLEAN verdict.
VERDICT: R96SentinelC1 C2 held — `gate-records.py verify` gives `records=31 ok=31 fail=0` and `search-rerun.py verify` on the r96 entry gives `rev_match=8/8 … SEARCH_RERUN: CLEAN` (exit 0); my lane's C2 work was a side-effect check on the `verify` path only, and the entry's decision rows against their quotes were not audited here.
