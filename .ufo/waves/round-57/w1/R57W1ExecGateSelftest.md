# R57W1ExecGateSelftest — round-57 tooling regression check

seat: `R57W1ExecGateSelftest` (executor) · lane: `chousa-shokunin` · base `6656f07` · lane tip at dispatch `f9736a3` · scratch: `/fast/scratch/hyaku/chousa-r57/R57W1ExecGateSelftest/` (removed before yield; `TMPDIR=$PWD`, `PYTHONDONTWRITEBYTECODE=1`) · tools installed: none (none needed; `RULES.md` read)

## 1. research-gate selftest — PASS, 275 cases, exit 0

```
$ export TMPDIR=$S PYTHONDONTWRITEBYTECODE=1
$ bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --selftest > selftest.out 2>&1; echo "EXIT=$?"
ok-case  273 pin-bash-path-shim           exit=0
ok-case  274 bash-pin-override-missing    exit=2
ok-case  275 bash-pin-override-fake       exit=2
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
EXIT=0
```
`grep -c "^ok-case" selftest.out` → `275`; `grep -n "FAIL-case\|RESEARCH_GATE_SELFTEST" selftest.out` → only line 277, the PASS line. No FAIL-case, **0 skipped**, wall 82.20 s.

**Case count vs the committed expectation — match (275 = 275).** The lane's registered pin is `SKILL.md:80` (`… --selftest` → `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`), byte-identical at base and tip (`git show 6656f07:SKILL.md | sed -n '80p' | sha256sum` = `sed -n '80p' SKILL.md | sha256sum` = `651735715ec29618f6ad415b8508e1283794370e35cc9281b69718fab3d5e6d3`); `corpus/lessons/round-39.md:62`, `round-41.md:11` and `.ufo/waves/round-43/w1/ExecNoHarmGate.md:22` record the same 275. **Calibration note on the dispatch hint:** the ladder in my item (20→30→40→44→54→64→74) is the *r1–r7* history in `corpus/knowledge/claim-verification-r2.md:144` (30), `chain-resolution-r3.md:169` (40), `anchor-boundaries-r4.md:169` (44), `sweeps-rejections-r5.md:220` (54), `verify-all-r6.md:269` (64), `reference-integrity-r7.md:230` (74) — not this lane's current gate. The gate's own printer (`tools/research-gate.sh:8685`) prints the count it ran: 275, as committed. No round defect: no FAIL, 0 skipped.

**Round-57 tooling additions do not touch the gate.** `git diff --name-status 6656f07 HEAD -- tools/` → exactly `A tools/capture-fetch.py` (+200 lines). `tools/research-gate.sh` is byte-identical base→tip (`2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34` at both) and never references the new tool (`grep -n "capture-fetch" tools/research-gate.sh` → no match). This is a regression check of an *unchanged* gate; the 275/275 is the expected outcome, not a fresh signal about round 57's fetch tool.

**Drift baselines (supporting).** `--drift …/gate-baseline-r12-20261019T115519Z.json` → `GATE_DRIFT: +resolvable drift`, exit 1; `…-r8-20261016T033757Z.json` → `GATE_DRIFT: +resolvable GATE drift record_sha256`, exit 1. Both reproduce **identically in a `git archive` extract of the base commit** (`git archive 6656f07 | tar -x -C $S/basecopy`, same two commands → same lines, same exits) — a pre-existing stale-baseline condition (`.ufo/waves/round-46/w2/RevShonen.md:30,37-40`), **not** a round-57 regression.

## 2. round-56 `c1-count.py` — ENV_CHANGED (not a measurement)

```
$ python3 corpus/evidence/round56/c1-count.py --work $S/c1work
CANDIDATE=0/2 seed7=('ENV', 2) seed56=('ENV', 2)
MUTANT M1 NO_SLICE SURVIVED   … (all nine SURVIVED)
PROBE P1 FORKEXEC NOT_DENIED seed7=('ENV', 2)   PROBE P2 DIRFD NOT_DENIED seed7=('ENV', 2)
CANDIDATE=0/2 KILLED=0/9 DENIED=0/2
C1=FAIL
EXIT=1
```
Every run exits `ENV_CHANGED`, so the counter measures nothing. Direct cause, from the gate itself:
```
$ python3 corpus/evidence/round56/c1-gate.py --seed 7 --per-leg 2 --work $S/gate1
tool=…/tools/build-spans.py sha256=1ed2650a… seed=7 per-leg=2
ENV_CHANGED pinned capture 54fe0734c01f699e735b4b0a digest
EXIT=2
```
`corpus/evidence/round56/c1-gate.py:78` reads the campaign cache `CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")` — that directory is **empty** (its parent mtime = the 2026-10-27 02:16:49 deletion already recorded in `corpus/lessons/round-56.md:14`). `:81` pins four OLE `.raw` captures by sha256-prefix; `:238` `env_fail(f"pinned capture {k} digest")` fires on the first miss — matching the round-57 dispatch instruction in `corpus/evidence/round57/egress-approval.md` ("Counters pinned to .qcache will exit ENV_CHANGED and must not be presented as measurements"). Reported as ENV_CHANGED, **not** as a measurement; no frozen counter was edited.

### 2a. What round-57's re-fetch already restored (scratch probe, mutating only scratch copies)

Copied `c1-gate.py`/`c1-count.py` into `$S/probe/` (frozen originals untouched), repointed `CACHE` at the lane's own `corpus/captures/`:
```
$ python3 gate-lanecache.py --seed 7 --per-leg 2 --work $S/probe/w1
GENOLE=PASS 2 docs, 4 quotes
OLEPIN=PASS 3 captures, 6 quotes
REFUSE=PASS 4 cases
REGRESS=FAIL spans.tsv differs from round 54's
LEGS=3/4
```
**3 of the 4 pinned OLE captures now exist lane-owned and satisfy the gate's own digest pin.** Their lane `.raw` sha256 prefixes equal `c1-gate.py:81-86` exactly — `6dc68fd6…`→`6063a3aff7a4081e93a6`, `b539a802…`→`46d1866ce9afd51682e7`, `bdff491a…`→`ac0fad62ed9a11fa3bd1` — and they are the same three round-57 re-fetches (S100, S101, S124; `corpus/evidence/round57/refetch.tsv` rows 18/19/42, raw_sha256 identical to the r56 pins). The 4th pin `54fe0734c01f699e735b4b0a` exists **nowhere on this host** (`find /home/vgpnk/Projects /fast/scratch -name "54fe0734*"` → no hit; a sha256-prefix scan of every `corpus/captures/*` → no hit). Its URL is recoverable from the sibling lane's history (`git -C /home/vgpnk/Projects/shokuknow log --all -S…` → blob `a3f055c3…` in `ba6779f0`): `http://kass.sacinfo.org.cn/kfs/token/download/nxherxmuespndfkb` (the 2020 征求意见稿 of the GB/T 漏洞分类分级 draft, a token-download endpoint). It is **not** in `corpus/SOURCES.md` and **not** pinned by any spans manifest, so it falls outside the round-57 egress table's first two rows — fetching it is an L1 decision, not mine (my item also forbids external fetches), and as a token URL it may be dead regardless.

Running the frozen counter against the lane-byte gate copy (scratch only):
```
$ python3 <lane>/corpus/evidence/round56/c1-count.py --gate $S/probe/gate-lane2.py --work $S/probe/c1work
CANDIDATE=0/2 seed7=(1,'PASS','PASS','PASS','FAIL') seed56=(1,'PASS','PASS','PASS','FAIL')
MUTANT M1..M9 … KILLED (9/9)   PROBE P1 FORKEXEC DENIED   PROBE P2 DIRFD DENIED
CANDIDATE=0/2 KILLED=9/9 DENIED=2/2
C1=FAIL   EXIT=1
```
Read: on lane-owned bytes the counter's **mutant-kill (9/9) and hook-denial (2/2) machinery is fully alive** — its discriminating power is intact and only its byte-identity leg fails.

### 2b. Why REGRESS cannot pass on lane bytes (measured, not inferred)

Rebuilt round-54's `quotes.tsv` against the lane's captures with `tools/build-spans.py` (exit 0, `SPANS_ROWS=33 WRITTEN=33`) and diffed against `git show dba605d:corpus/evidence/round54/spans.tsv`: 33/33 rows and 33/33 span files **byte-identical**; the only differing column across all rows is column 2 (`capture_sha256`) on the **6 S121 rows**, and substituting round-54's pinned digest into those 6 rows reproduces round-54's `spans.tsv` **byte for byte** (`built-with-r54-digest == r54 committed spans.tsv: True`). Cause: S121's page bytes changed between round 54 and now — lane `.txt` digest `ed4dde2e…` vs round-54's pin `4e46154f…`, exactly C2's `DRIFTED` verdict for S121 with `absent=0/6` (all six quotes still occur; content intact, only the digest moved). REGRESS is pinned to the deleted cache's exact bytes, so it cannot be re-earned from any re-fetch: the counter is a *byte-identity* claim about round 54's captures and round 57 deliberately re-fetched them. **Reported, not patched** (claims and counter frozen).

## 3. Context read (not a claim of mine)

`python3 corpus/evidence/round57/c2-count.py --verbose` → `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0 (DRIFTED: S083 S087 S113 S114 S121; UNREACHABLE: S105). Read-only observation of committed state; C2's verdict is the L1's.

## 4. Boundaries honoured

Lane writes: only this report file. No `git commit/add/stash/checkout/reset/push` and no mutating `jj` anywhere. `/home/vgpnk/Projects/shokuknow` read-only (one `git log`/`git show`/`git cat-file` for the missing pin's URL; no campaign tool run, no write). Fleet root `/home/vgpnk/Projects/shokunin` untouched. All mutated gate/counter copies lived under `$S` and are deleted; the frozen `c2-count.py`, `c3-count.py` and controls builders were never edited.

**VERDICT: attacked the round-57 tooling addition via the research-gate selftest (PASS, 275 cases, 0 skipped, exit 0, matching the committed SKILL.md:80 pin of 275) and via round-56 `c1-count.py` (ENV_CHANGED, not a measurement: its gate reads the deleted sibling `.qcache`; on lane-owned bytes the counter's 9/9 mutant kills and 2/2 hook denials still fire, and its one failing leg is byte-pinned to round-54's drifted S121 capture) — the round-57 gate regression SURVIVED; the round-56 counter is ENV_CHANGED-blocked by a missing external cache, not by round-57.**
