# R58SentinelCounterScope — frozen C1 counter: safety / misleading-behavior audit

Read-only inspection. Lane HEAD `5da0a6375a554e1229492a8cb0b9695bd8e85456`; frozen commit
`9e73a031ab1ac3bac343de008850d7d87f9e5634`. `git diff 9e73a03..HEAD -- corpus/evidence/round58/`
touches only added control files; `claims.md` and `c1-count.py` are unchanged since freeze
(`c1-count.py` sha256 `65da18bb…c703d3f`, 406 lines). `tools/build-spans.py` at HEAD still equals the
round-55 pin `1ed2650a…c80bf6`, so `controls/c1-before.txt` is still the live baseline (reproduced
leg-for-leg). Scratch `S=/fast/scratch/hyaku/chousa-r58/R58SentinelCounterScope` (counter + controls
copied there; all probes run against copies). No lane writes, no git/jj mutation, no fetch.

## Findings

**F1 — CRITICAL, blocking: the frozen counter can never print `C1=PASS`.** `:51` `PASS = "pass"`;
`:391` `ref_pass = all(("=PASS" in l) for l in ref_legs)`; every refusal leg is formatted with
`{PASS}` (`:160`, `:223`, `:234`) and therefore reads `FOREIGN=pass(refused)`. Case-sensitive
`"=PASS"` never matches, `ref_pass` is constant-`False`, `verdict` (`:394`) is always `"FAIL"`
(exit 1, `:402`). The receipt `c1-measure-after.txt` demanded by claims.md is unobtainable for *any*
builder, including a conforming one. Probe (counter's own module, in scratch):
```
PASS constant: 'pass' | '=PASS' in 'FOREIGN=pass(refused)': False
ref_pass on all-green legs: False | ok_pass on all-green legs: True
```
Run evidence — scratch mutant, all 11 legs green, controls denied:
```
$ python3 -B c1-count.py --builder mutant.py --work $S/w-mut3 --controls $S/controls
EMPTY_OK=pass … FOREIGN=pass(refused) … MANY_QUOTES=pass(refused) … HELDOUT_OK=pass
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```
Impact: the wave's C1 gate is unsatisfiable as frozen; a correct executor patch will still report
`C1=FAIL` and may be misattributed. `REFUSE=0/7` is printed on *every* run (`c1-before.txt` too), so
the summary cannot distinguish "no refusals" from this bug. Proposal (not applied): compare
`.lower()` at `:391`. Frozen → the L1 decides whether the claim or the counter is authoritative.

**F2 — HIGH: uncontrolled deletion of an arbitrary caller path.** `:174-177` `if work.exists():
shutil.rmtree(work)` with no absoluteness, containment, or freshness check. Exploit: run from the
documented cwd (fleet root) with a relative/typo `--work .`, or point `--work` at the lane, a sibling
repo, or the shared scratch parent.
```
$ python3 -B c1-count.py --builder /bin/true --work $S/victim      → victim/keep.txt GONE
$ cd $S/dotwork && echo sentinel > keep.me && mkdir sub && echo x > sub/f
$ python3 -B ../c1-count.py --builder /bin/true --work .
OSError: [Errno 22] Invalid argument: PosixPath('.')      # after contents were deleted
--- dotwork after ---   (empty: keep.me, sub/f gone)
```
Impact: one wrong `--work` recursively deletes committed evidence, a sibling checkout, or the fleet
root's contents (`rmdir('.')` fails *after* the wipe); it also wipes other seats' scratch under the
shared `chousa-r58/` parent. Remediation: require absolute, `resolve()`, refuse unless under
`$HYAKU_SCRATCH/chousa-r58/`, and refuse a non-empty dir instead of rmtree-ing it.

**F3 — HIGH: `SYMLINK_OUT` forbidden-touch semantics are inverted — the leg passes exactly when the
builder writes through the symlink.** `:158` `if not p.exists(): return FAIL("…was
touched/removed")`; `:232` passes `real/"spans.tsv"`. Absence (correct) is scored FAIL; presence
(hazard committed) passes, and `:233-236` only *appends* `"(target-dir-written!)"` to a line that
still contains `=PASS`. Probe (synthetic `CompletedProcess`, builder printed `SYMLINK --out refused`):
```
A refuse+no-write          : SYMLINK_OUT=fail(.../probe-inv/spans.tsv was touched/removed)
B refuse+wrote-into-target : SYMLINK_OUT=pass(refused)
```
Run evidence: mutant wrote `spans.tsv` into the symlink target then refused →
`SYMLINK_OUT=pass(refused)(target-dir-written!)`, and `$S/w-mut3/realdir/` holds `partial.txt` +
`spans.tsv`. Impact: C1 clause (2) cannot be certified; a symlink-following builder passes the leg
meant to catch it. Remediation: `if p.exists(): FAIL`; make the `any(real.iterdir())` branch fatal.

**F4 — MEDIUM-HIGH: `FOREIGN` checks only the foreign file.** `:211-223`: on refusal the only
assertions are `foreign.exists()` and a reason token (`"777" in err or "foreign" in err.lower()`).
The legitimate orphans from the three-quote build (`spans/S501-1.txt`, `S502-1.txt`, `S503-1.txt`)
are never checked, so a builder may delete them and then refuse — contradicting C1 clause (1)
"refused **before** orphan deletion". Evidence: same run, mutant unlinks `spans/S5*.txt` then
refuses → `FOREIGN=pass(refused)`, and afterwards `out-empty/spans/` holds only `S777-1.txt`.
Remediation: snapshot `out/spans` before the FOREIGN invocation and assert byte-equality on refusal.

**F5 — MEDIUM: the harness hands the tested builder the lane's live capture store as its writable
cache.** `:343` passes `LANE/"corpus"/"captures"` as `--cache`; `:59-66` snapshots only `work`, so
that dir is never diffed. The store *is* the cache layout: `sha256(url)[:24]` reproduces
`6dc68fd6b32ce9c8dfcebce8`, and `corpus/captures/` holds 129 `.raw`/`.txt` pairs (the `.txt` derived
forms are committed evidence). A candidate that caches a derived `txt` into `<cache>/<key>.txt`
rewrites C2/S101 source evidence mid-measurement and the leg still reports green. Not exercised
(deliberately did not let a builder write into the lane). Remediation: stage the one `.raw` into
`work/cache`, or snapshot/diff the lane dir around that leg.

**F6 — MEDIUM: controls are optional; absence of controls still satisfies the verdict.** `:366-382`
+ `:393` `denied_pass = (denied == total) if total else True`; `--controls` defaults to `None`, so a
missing/typo'd dir prints `DENIED=0/0` (observed) and the "controls must not reach PASS" clause is
vacuous. Corollary of F1: controls are "denied" because `ref_pass` is always false, so
`CONTROL_REFUSEALL=denied` / `CONTROL_build-spans-r55=denied` carry no information (same run in which
the mutant passed every leg). Remediation: require `--controls`, fail when `total == 0`.

**F7 — LOW-MEDIUM: no process containment, no memory bound, unbounded snapshot reads.** No
`start_new_session`/`killpg`/`setrlimit` anywhere (grep: no matches), so `subprocess.run(timeout=…)`
kills only the direct child — grandchildren survive a leg with write access to `work`. `FIFO_TXT` /
`DEVZERO_TXT` rely on a 20 s clock with no memory cap (a builder swallowing `/dev/zero` grows until
SIGKILL). `snapshot()` (`:59-66`) reads every file under `work` unbounded and skips symlinks
(`not p.is_symlink()`), so symlink substitutions in `work` escape the containment diff. Measured peak
child RSS on a 9 MB-on-disk fixture (80 MiB sparse raw + 100 k-row tsv): **197.9 MiB**.
Remediation: `start_new_session=True` + killpg, RLIMIT_AS on the child, size cap in `snapshot()`.

**F8 — LOW: refusal reasons are substring-matched text, not causes.** `:155-160` matches
`err.lower()` against `["SIZE","ROWS","CAP"]` / `["NOT_REGULAR","FIFO","REGTYPE","SYMLINK"]`, `:223`
against `"777"`/`"foreign"`. My mutant satisfies all six token classes with hand-written strings
wrapped around only lstat/size/row-count probes. I built no runnable token-only false positive
(unrun) — reported as discriminator calibration, not as an exploited path.

**F9 — LOW: an always-refusing builder crashes the counter instead of rendering a verdict.**
`:211-212` seeds `out/spans/S777-1.txt` without creating `out/spans`, so a builder that never writes
(including the shipped `REFUSEALL.py` used as `--builder`) aborts with
`FileNotFoundError: …/out-empty/spans/S777-1.txt`, exit 1, **no `C1=` line** (observed with
`--builder /bin/true`). The control loop then counts "denied" on a crash (`tail` empty), not on a
measured verdict. Remediation: `mkdir(parents=True, exist_ok=True)` before seeding; emit `C1=FAIL`
on any internal error.

## Verified-absent / not findings
- No network in the counter, `tools/build-spans.py`, or `tools/capture-text.py` (`urllib.parse` only,
  for OPF rel targets); no fetch performed. Egress is honoured by the code, not enforced: all fixtures
  are cache hits, so a candidate's fetch-on-miss path would stay silent.
- Recursion is bounded at depth 1 — the child invocation (`:368-376`) passes `--builder` but never
  `--controls`. Its 1800 s timeout is finite.
- `HERE`-relative `BEFORE_BUILDER` fails *closed* when the counter runs from a copy
  (`BEFORE_FOREIGN=absent`) — an operator trap, not a safety hole; `HELDOUT_OK` only reads the lane.

## Unrun
Real candidate builder (lane still at the r55 pin, so no C1 after-state exists yet); a builder that
writes into the lane capture store (F5 is code-read only); egress probe for a fetch-on-miss candidate
(no live fetch authorized). Scratch removed after this report.

VERDICT: The frozen C1 counter at `9e73a03` is **falsified as a usable gate**: the verdict is
structurally unsatisfiable (F1, `PASS="pass"` vs `"=PASS"`), and even with F1 repaired it would
certify a builder that writes `spans.tsv` through a symlinked `--out` (F3, inverted forbidden-touch)
and deletes legitimate orphan spans before refusing (F4), while it unconditionally rmtree's any
caller-supplied `--work` tree (F2) and exposes the lane's live `corpus/captures` as a writable cache
with no containment check (F5).
