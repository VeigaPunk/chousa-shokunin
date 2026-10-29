# RevC1V2LegsH2 — review of legs H10 SPANSLINK, H11 FILELINK, H12 TSVLINK (C1 v2 counter)

Seat: reviewer (leaf). Scope: `corpus/evidence/round62/c1v2-count.py` (frozen, sha256 prefix `b7016fba91b03460`, read only, never edited): docstring lines 28-32 and 44-45, legs at lines 491-546, main loop at 690-716. Nothing written under the frozen paths, `tools/`, `corpus/`, or `SKILL.md`; no git writes; every counter or driver run used `python3 -B`. Scratch `/fast/scratch/hyaku/chousa-r62/RevC1V2LegsH2/` deleted before yield.

## Method

1. Full counter on three existing correct builders (controls, unmodified) and on two scratch variants of mine, with `C1V2_SEED` set:
   `C1V2_SEED=<N> python3 -B corpus/evidence/round62/c1v2-count.py --builder <B> --work <absent dir>`
2. A driver that imports the frozen module read only (`importlib`, `-B`) and calls `leg_h10/h11/h12` per profile, so the three legs can be run on stubs quickly. It mirrors the counter's rng and exception handling.
3. Do-nothing and hazard controls: `base-build-spans.py` (round-61 unhardened), `exit 0`, `exit 1`, `exit 2`, uncaught exception, self `SIGSEGV`, self `SIGKILL`, a hang (`time.sleep`), a junk writer that exits 2, a refuse-by-dying stub.
4. Sandbox probe: `unshare -Ufp --kill-child --mount-proc python3 -B -c "import os; os.abort()"` and the same with self `SIGKILL`.

## Findings (ordered by severity)

### F1 — TAUTOLOGY: a hung builder passes H10, H11, H12 in both profiles (contradicts the docstring)
- Docstring lines 44-45: "Every run has a 60 s timeout (a timeout fails the leg)". The legs do not check it. H10 returns `(unchanged and (r["rc"] != 0 or healed))` (line 512); H11 at 529; H12 at 545. A timeout gives `rc=-9`, which is `!= 0`. Compare H18 (line 628) and H20 (line 660), which test `not r["timeout"]`.
- Repro: builder `import time; time.sleep(100000)` (scratch `b/s_hang.py`). Driver output:
  `LEG H10 SPANSLINK | plain: ok rc=-9 victim_unchanged=True | neutral: ok rc=-9 victim_unchanged=True`
  `LEG H11 FILELINK | plain: ok rc=-9 victim_unchanged=True | neutral: ok rc=-9 victim_unchanged=True`
  `LEG H12 TSVLINK | plain: ok rc=-9 victim_unchanged=True | neutral: ok rc=-9 victim_unchanged=True`
- Consequence: a builder that never finishes and never touches anything is accepted by three legs. INFERENCE (not run): the full counter would still fail it through the other legs, since 60 s per run exceeds the leg budget; the defect is at leg level.
- Fix candidate for the next round's battery (not applied here): add `and not r["timeout"]` to H10–H12.

### F2 — TAUTOLOGY: any non-zero exit with no action passes H10–H12
- The "exit non-zero" branch accepts a builder that does nothing and exits non-zero. Repro (driver, both profiles, all three legs ok):
  - `sys.exit(2)`: `LEG H10 SPANSLINK | plain: ok rc=2 victim_unchanged=True | neutral: ok rc=2 victim_unchanged=True`
  - `sys.exit(1)`: `ok rc=1` for H10, H11, H12 in both profiles
  - uncaught `RuntimeError` (exit 1): `ok rc=1` for H10, H11, H12 in both profiles
- Full counter on these stubs (`C1V2_SEED=7`): `s_exit2` LEGS=14/20, `s_exit1` LEGS=11/20, `s_raise` LEGS=11/20, all `C1V2=FAIL`. The battery still rejects them through the other legs (P01, P04, H07, H09, H16), so the counter's verdict is not defeated; H10–H12 themselves cannot tell a refusal from a stub. H07/H09/H16 pin the exit code (H09 and H16 require `rc == 2`).

### F3 — TAUTOLOGY (laxness): a refusal may leave writes behind and H10–H12 still pass
- H10–H12 check only the victim and (`rc != 0` or healed). They do not check that a refusal wrote nothing. H07 (line 475), H09 (line 488) and H16 (line 599) check the output tree on refusal; H10–H12 do not.
- Repro: `s_junk.py` writes `out/junk.txt` and exits 2. Driver: `LEG H10 ... plain: ok rc=2 victim_unchanged=True | neutral: ok rc=2 victim_unchanged=True`; same for H11 and H12.
- The docstring's "(exit non-zero, or ...)" permits this literally. Under claim C1's output-safety reading, a refusal that leaves partial output is a hazard the legs should catch. I count it as a defect of the legs, not a counter bypass.

### F4 — FALSE POSITIVE candidate (instrument): a builder that refuses by dying is reported as exit 0
- Under `unshare -Ufp --kill-child --mount-proc`, a builder that dies from a self-sent fatal signal is reported `rc=0`, not `rc=-9` or `-11`:
  - sandbox probe: `os.kill(os.getpid(), SIGKILL)` gives shell rc 0; `os.abort()` gives shell rc 139.
  - `s_segv.py` (self SIGSEGV): full run and driver show `FAIL rc=0` for H10, H11, H12 in both profiles.
- Repro of a refusal by death (`s_refusekill.py`: if `out/spans` is a link, `os.kill(os.getpid(), SIGKILL)`; otherwise exit 0). It writes nothing and sets no status. Driver output:
  `LEG H10 SPANSLINK | plain: FAIL rc=0 victim_unchanged=True | neutral: FAIL rc=0 victim_unchanged=True`
  `LEG H11 FILELINK | plain: FAIL rc=0 victim_unchanged=True | neutral: FAIL rc=0 victim_unchanged=True`
  `LEG H12 TSVLINK | plain: FAIL rc=0 victim_unchanged=True | neutral: FAIL rc=0 victim_unchanged=True`
- The docstring accepts "exit non-zero"; a SIGKILL death is a non-zero termination in POSIX terms, so the leg should accept it. The counter reports it as 0 and the leg fails. The timeout path reports `-9` correctly because the timer's `killpg` kills the `unshare` process itself; the discrepancy only arises for signals delivered to the namespace's PID 1.
- Mechanism: INFERENCE (not isolated): under `unshare -f` the child is PID 1 of the new namespace, and its self-sent fatal signals are either ignored or mapped to status 0 by `unshare`. The observations (shell rc 0 for SIGKILL, rc 139 for abort, `rc=0` in the counter) are measured.
- Severity: a false positive only for refusals by death, which no correct builder performs; still a counter-level misreport (the sandbox reports a signal death as success).

## Correct builders: false-positive hunt (no leg-level false positive found; 5 builders)

| builder | policy for H10–H12 | H10 plain / neutral | H11 plain / neutral | H12 plain / neutral | full counter |
|---|---|---|---|---|---|
| controls `pos-indep1.py` (sha256 19d1f414…) | refuse every link, exit 2 | ok rc=2 / ok rc=2 | ok rc=2 / ok rc=2 | ok rc=2 / ok rc=2 | LEGS=20/20 PASS (seed 101) |
| controls `pos-indep2.py` (sha256 f37723f2…) | refuse DIR/spans link (exit 2); replace file links by rename | ok rc=2 / ok rc=2 | ok rc=0 healed / same | ok rc=0 healed / same | LEGS=20/20 PASS (seed 102) |
| controls `pos-indep3.py` (sha256 51c40345…) | refuse every link (exit 2), mkstemp + replace | ok rc=2 / ok rc=2 | ok rc=2 / ok rc=2 | ok rc=2 / ok rc=2 | LEGS=20/20 PASS (seed 103) |
| scratch W1 = pos-indep2 + DIR/spans link unlinked after all checks, then mkdir | replace DIR/spans link | ok rc=0 healed / same | ok rc=0 / same | ok rc=0 / same | LEGS=20/20 PASS (seed 21) |
| scratch W2 = pos-indep3 + spans.tsv link treated as absent when writing (regular-file compare only) | replace manifest link | ok rc=2 / same | ok rc=2 / same | ok rc=0 healed / same | LEGS=20/20 PASS (seed 21) |

- W1 edits (scratch only): lines 321-322 (raise on a link at `DIR/spans`) replaced by `sst = None` (`span_names` returns `[]` for a link); `os.unlink(sd)` added before `sd.mkdir` at line 392, i.e. after every preflight check. Both files parse (`ast.parse`).
- W2 edits (scratch only): the link refusal at line 221 skips the manifest (`(p.is_symlink() and p != m)`); the manifest compare at line 226 requires `not m.is_symlink()`.
- Result: no correct builder fails any of the three legs in either profile. All five check before any write; they differ in link policy (refuse all, or replace) and in code path (`os.open` with `O_NOFOLLOW` and `os.replace`, versus `mkstemp`).
- Not built (time): a builder that stages every write outside DIR and moves it in after the checks. INFERENCE, not run: I expect it to pass for the same reason.

## Hazard effectiveness and masking (question b)

- `base-build-spans.py` (round-61 unhardened) fails H10, H11, H12 in BOTH profiles, each `FAIL rc=0 victim_unchanged=False` (full run, seed 7, and driver).
- Names: H10–H12 use the fixed contract names `spans/`, `spans.tsv`, and `victim`, `victim.txt`, `victim.tsv` in both profiles. The neutral profile randomizes only the `out`, `cache`, builder, quotes and cwd names (`Fx.__init__`, lines 153-170). None of these changes which path is linked. I found no name that disables a hazard. A random `out` name equal to `spans` is ~1e-7 likely (and would not disable the hazard anyway).
- The AND rule (`passes = plain and neutral`, line 716) means a profile can add a failure but never mask one. So "neutral masks a hazard" could only happen if neutral failed to create the hazard; the base result shows it does.

## Profile-dependent verdicts (question c)

- Observed: for all nine builders I ran on H10–H12 (base, s_exit1, s_exit2, s_raise, s_segv, s_junk, s_refusekill, s_hang, pos-indep1/2/3, W1, W2), no leg verdict differed between `plain` and `neutral`.
- Inputs that differ by profile and could in principle matter: random out/cache/builder/quote/cwd names; env (`HOME`, `LANG`, `LC_ALL`, extra variables, shuffled `PATH`); `RLIMIT_FSIZE` (512 MiB plain; 384 MiB, 768 MiB or 1 GiB neutral); `RLIMIT_AS` (200 MiB plain; 200–224 MiB neutral); stdin (`/dev/null` plain, closed pipe neutral); stdout/stderr (files plain, pipes neutral).
- H10–H12 verdicts use only exit code, victim snapshot and output tree, so the size limits and stdio do not reach them. A profile can change an H10–H12 verdict only through a name- or environment-sensitive builder; I did not construct one.
- Verdict-by-profile list: none observed. INFERENCE: profile does not affect H10–H12 verdicts for ordinary builders. Not run: a name-sensitive or env-sensitive builder.

## Commands and outputs (receipts)

- `unshare -Ufp --kill-child --mount-proc true; echo sandbox_rc=$?` → `sandbox_rc=0`; Python 3.14.8.
- `sha256sum c1v2-count.py | cut -c1-16` → `b7016fba91b03460`; `sha256sum tools/build-spans.py | cut -c1-16` → `c366492005ce304a` (both match the claims).
- `C1V2_SEED=101/102/103 python3 -B c1v2-count.py --builder <pos-indep1/2/3>` → `LEGS=20/20 C1V2=PASS`, `rc=0` each.
- `C1V2_SEED=7 ... --builder base-build-spans.py` → `LEGS=11/20 C1V2=FAIL`, `rc=1`; H10–H12 each `FAIL rc=0 victim_unchanged=False` in both profiles.
- Stubs (full run, seed 7): `s_exit0` LEGS=1/20, `s_exit2` 14/20, `s_exit1` 11/20, `s_segv` 1/20, `s_raise` 11/20 (all FAIL).
- `C1V2_SEED=21` on W1 and W2 → `LEGS=20/20 C1V2=PASS` each.
- Driver: `python3 -B drv.py <builder> <tag> <seed>`; outputs quoted in F1–F4 and the table.

## Not done / limits

- The signal-death mechanism was tested only with two self-signals and one abort; no isolation of `unshare`'s exit-status mapping.
- Controls and variants are Python builders written against this lane's contract; no non-Python builder was tried.
- Entailment of the legs' messages: out of scope.
- Tooling: nothing installed; no pacman use.

## Recommendations (routed; the frozen counter is not changed by this seat)

1. F1: add `and not r["timeout"]` to H10–H12 (as H18/H20 do) in the successor battery.
2. F2/F3: pin refusal to "exit 2 and nothing written" in H10–H12, as H07/H09/H16 do, or record the gap as a named limit.
3. F4: record a signal death as non-zero in a successor counter (for example read the status in the parent without relying on `unshare`'s exit mapping).

VERDICT: LEG_DEFECTS=4 false_positive=1 tautology=3 legs=H10 SPANSLINK, H11 FILELINK, H12 TSVLINK
