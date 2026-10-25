# R51SentScope — round 51 wave 1: scope and hazard review

seat R51SentScope (leaf, no dispatch) · 2026-10-25 · lane tip `cfe6c9f`, base `9ec1751a24231e899ceea4688e21c8edf6046d35`
Scratch `/dev/shm/chousa-r51-R51SentScope` (deleted at exit); every run of mine used `TMPDIR=/dev/shm/chousa-r51-R51SentScope/tmp`.
No install performed. I attacked no axis predicate; operability/depth/calibration verdicts belong to the other seats.

## H1 — write surfaces of the counters, the tool and the control builders (severity: medium)

`grep -n 'open(\|write\|mkdtemp\|shutil' corpus/evidence/round51/*.py corpus/evidence/round51/controls/*.py tools/assimilate-rows.py` → 82 matches / 7 files.

| surface | writes | destination | verdict |
|---|---|---|---|
| `c1-count.py:77-79,119,209` | package + `out/` | `mkdtemp("chousa-r51-c1-")`, rmtree in `finally` | scratch, but **`$TMPDIR` else `/tmp`** |
| `c2-count.py` | **none** (zero matches) | — | read-only; `quote-substance-check.py` and `inference-ground.py --counts /dev/null` without `--json` (only `inference-ground.py:530` writes, under `--json`) |
| `c3-count.py` | **none** (zero matches) | stdout | read-only, H3 |
| `build-spans.py:193-198` | `spans.tsv`, `spans/*`, unlinks orphan `spans/*` | `<root>/corpus/evidence/round51` | in-lane by design |
| `build-c2-controls.py:30,37,44,58,67` | evidence copy + tooled package | `mkdtemp("chousa-r51-<tag>-")`, `--out r/adopt` | scratch; **leaks on `check=True`** |
| `build-c3-controls.py:25-40,45,56` | file copies, zero-byte pointers | `mkdtemp("chousa-r51-c3-")` | scratch; H4 |
| `assimilate-rows.py:345-452` | ids, entry copies, `append.md`, `renumber.tsv`, `stripped.tsv` | `--out` (required, caller-chosen) | `--out` only |

Write-escape guards hold: `--entry /etc/passwd` → `rc=2 must be relative`; `--entry ../../etc/passwd` → `rc=2`, and neither `out2` nor `out3` was created (the entry check precedes `out.mkdir`). A REFUSED run still writes three files under `--out` (D3 forbids only `renumber.tsv`/`append.md`, so the predicate holds; the docstring's "nothing claimed" reads narrower than it is):
```
$ python3 tools/assimilate-rows.py … --out t1/out --entry e.md   # registry without ## Registry
COLLISIONS=0 / REFUSED registry has no `## Registry` heading / REFUSED registry rows outside the Registry section: S001
rc=1 ; ls t1/out → collisions reg-ids staged-ids
```
Live leak evidence — `build-c2-controls.py:59` uses `check=True`, so a `CalledProcessError` skips `rmtree` at line 69 and the copied package stays in `$TMPDIR`:
```
$ stat -c '%y %a %n' /tmp/chousa-r51-tooled-37yfo4be ; du -sh /tmp/chousa-r51-tooled-37yfo4be
2026-10-25 19:52:16 700 /tmp/chousa-r51-tooled-37yfo4be
676K    /tmp/chousa-r51-tooled-37yfo4be
```
Empty-dir variant: five `/tmp/chousa-r51-c1-*` exist (`/tmp/chousa-r51-c1-4wbm_1it`, 20:27:25, empty) from hard kills. Mode 0700, so no disclosure; the boundary's "/dev/shm only" is the caller's job, not the counters'.
Impact: the frozen counting command writes outside the lane, and one failure path leaves 676K of lane+staged corpus in `/tmp`.
Smallest remediation: `dir="/dev/shm/…"` (or a required `TMPDIR`) in the three `mkdtemp` calls; `try/finally: shutil.rmtree(r)` in `build-c2-controls.py`.

## H2 — fixtures that run git writes in the lane (severity: none; verified)

Git call sites: `c2-count.py:145,182`, `c3-count.py:85-86`, `build-c2-controls.py:36` — all `["git", "-C", str(LANE), "show"|"grep", …]` with `LANE` a module constant (`parents[3]`); `--root` never reaches the git call. No `init/commit/add/checkout/reset/stash/-c` anywhere: `grep -rn 'git init\|git commit\|git add\|git checkout\|git stash\|git reset\|git -c' corpus/evidence/round51/ tools/assimilate-rows.py` → no output. Empirical, markers with **no git command between marker and `find`**:
```
$ find .git -newer $M -type f    # after c2-count.py          → (no output)
$ find .git -newer $M2 -type f   # after build-c2-controls.py  → (no output)
```
Method note: `find .git -newer marker` false-positives on `.git/index` if your own `git status` runs after the marker; I hit that and re-ran cleanly.

## H3 — `c3-count.py`'s `git -C LANE show BASE:...` is read-only (severity: none; verified)

`c3-count.py:85-86` reads two blobs only. Isolated test (marker → counter → `find`, no git in between):
```
$ touch $M; sleep 1; python3 corpus/evidence/round51/c3-count.py >/dev/null; find .git -newer $M
c3 exit=1 ; (no output) ; sha256sum -c idx-before.txt → .git/index: OK
```
`git status --porcelain` before/after identical; no lane file gained a fresh mtime. Tip observation: `CAP_ROWS=36 (base 36) POINTERS=74 (base 74) DANGLING=5 C3=FAIL exit=1` (SCORECARD.md:1843 2073 2074 2616, SHONEN.md:10) — the erratum's 5, not the filed 8.

## H4 — the symlink-the-lane-tree control (severity: low today, latent write-through)

`build-c3-controls.py:26-31` symlinks every top-level lane entry into the scratch root. Guard, verbatim (`:51-52`):
```python
if q.is_symlink() or any(x.is_symlink() for x in q.parents if x != r and r in x.parents):
    continue
```
The scratch run the assignment asked for, at the tip:
```
$ TMPDIR=/dev/shm/… python3 corpus/evidence/round51/controls/build-c3-controls.py > rerun.txt; echo $?   → 0
$ git status --porcelain before/after → STATUS_IDENTICAL (only the pre-existing ?? .ufo/waves/round-51/*)
$ diff rerun.txt corpus/evidence/round51/controls/c3-controls-erratum.txt → MATCHES_ERRATUM_FILE
$ for n in measure measure-l1 c1-supplement.py round25-meta-differential.log; do [ -e $n ] && echo EXISTS || echo absent; done
absent absent absent absent
```
So **no lane file changed**: the five dangling pointers (`measure/final/`, `measure-l1/c1-s36361.json`, `measure-l1/c2-s36371.json`, `c1-supplement.py`, `round25-meta-differential.log`) name no lane path, so every write lands inside the scratch root. The filed `c3-controls.txt` (8 dangling) is the pre-erratum run; the erratum file reproduces byte-identically — a calibration plus for C3's controls.

Two holes, from a line-for-line replica of `scratch()` + the EMPTY loop (scratch only):
```
SKIP   corpus/knowledge/zzz-missing.md  guard=1
SKIP   tools/zzz-missing.py             guard=1
WRITE  measure/final/                   guard=0 inside_scratch=True
WRITE  ../escape/x.md                   guard=0 realpath=/dev/shm/chousa-r51-R51SentScope/sim/escape/x.md inside_scratch=False
RESOLVE 5-dot pointer                   guard=0 realpath=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-51.md
```
(a) The guard **skips** every pointer under a symlinked lane directory, so the EMPTY leg never exercises the non-empty rule there; it is effective only where the first component is absent from the lane (true of today's five).
(b) A pointer carrying `..` escapes, and `pointers()` keeps such tokens (`"..."` is rejected, `".."` is not): `pointers("`../../home/…/corpus/x.md` `../escape/x.md`")` → `['../../home/…/corpus/x.md', '../escape/x.md']`.
Exploit path: a SCORECARD row with `` `../../../../../home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-51.md` `` (5 dots from the scratch root resolves exactly there — `realpath` confirmed) makes the EMPTY leg `mkdir -p` + `write_bytes(b"")` through that path: a zero-byte truncation of a lane file, guard silent because the escape is lexical. Today no pointer has `..`, so the control is safe as filed.
Smallest remediation: before writing require `".." not in PurePath(ptr).parts`, `not ptr.startswith("/")`, and `realpath(q).startswith(realpath(r) + sep)` — the guard `c2-count.py:130-133` (`safe_span`) and the tool's `--entry` check already use.

## H5 — `ASSIMILATE_CITES` is an unowned global switch (severity: high; it flips a frozen verdict)

Callers invoking the tool with **no** `--cites`, hence inheriting the environment: `round49/c1-count.py:178-180`, `round50/c1-count.py:61,97,119`, `round51/c1-count.py:62` (both default legs), `round51/controls/build-c2-controls.py:59`, plus `const-tool.py`/`echo-tool.py` which `execv` the real tool. Read at `tools/assimilate-rows.py:315,320` as `a.cites or os.environ.get("ASSIMILATE_CITES") or "source"`. Documented only in the tool docstring; the lane bar never mentions it: `grep -rn 'ASSIMILATE_CITES' SKILL.md QUALITY.md README.md PROVINCE.md` → no output.

Same seed, two environments:
```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --seed 7
SELFTEST_DEFAULT=PASS / SOURCE_ONLY=PASS appended=1 bodyonly=[['corpus/knowledge/e.md','S524']] / LEGS=5/5 C1=PASS exit=0
$ ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py --seed 7
SELFTEST_DEFAULT=FAIL / SOURCE_ONLY=FAIL appended=2 bodyonly=[] / LEGS=3/5 C1=FAIL exit=1
```
and at the tool level, both directions: round-50 pin `env -u` → `SELFTEST=FAIL findings=20 expected=26`, `=all` → `SELFTEST=PASS findings=26 expected=26`; lane default selftest `env -u` → `SELFTEST=PASS findings=25 expected=25`, `=all` → `SELFTEST=FAIL findings=35 expected=25`.
Exploit path: a seat whose shell exports `ASSIMILATE_CITES=all` (the round-50 reproduction needs exactly that) runs the frozen round-51 counter in the same shell and reports `C1=FAIL` for a tool that passes; conversely an exported `source` breaks the round-50 counter's `BASELINE`/`PERTURB` legs, which want 26 findings against the 20 the unset tool prints.
Impact: the C1 verdict is not reproducible from the counting command alone — the routed round-50 defect "pin the revision a counter was measured against" reappearing as an unpinned environment.
Smallest remediation: `c1-count.py:60` → `env=dict(os.environ, ASSIMILATE_CITES="")` (empty is falsy → `"source"`; the explicit `--cites all` leg still wins) and print the effective mode. Freeze-owner's call.

## Lane pollution observed from wave-1 seats (not mine; severity: low, clear before the tip measurement)

`corpus/evidence/round51/zero.txt` — untracked, 0 B, mtime `2026-10-25 20:29:40`; absent from my snapshot `s2` (after my builder run), present in `s3`. `.ufo/waves/round-51/w1/R51CritForgeC3.md:124` calls it "a sibling seat's …, not mine". It is exactly the artifact shape the EMPTY control creates, sitting in the lane instead of a scratch root.
`corpus/evidence/round51/__pycache__/build-spans.cpython-314.pyc` — 15616 B, 20:21, **git-ignored** (`.gitignore:3 corpus/**/__pycache__/`), so `git status` cannot see it: a seat that imports a counter as a module writes into the lane invisibly. My own `importlib` load of `c3-count.py` left no `.pyc` (`find corpus/evidence/round51 -name '*.pyc'`).
Remediation: delete both; a "lane untouched" claim must use `find`/`sha256sum`, not `git status` alone.

VERDICT: attacked the round's write surface — H2/H3 clean (no git writes; `git show` verified read-only), H4 safe at the tip but latently write-through via `..` pointers and vacuous for lane-dir pointers, H1 leaks scratch to `/tmp` (676K observed), H5 flips the frozen C1 verdict `LEGS=5/5 C1=PASS` → `LEGS=3/5 C1=FAIL` from the ambient `ASSIMILATE_CITES`; plus two sibling-seat artifacts found in the lane.
