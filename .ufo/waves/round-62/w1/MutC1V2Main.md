# MutC1V2Main — mutation test of `main()` in the R62-C1 v2 counter

Seat: mutation-tester (leaf). Target: `corpus/evidence/round62/c1v2-count.py` `main()` (read-only; frozen).
Method: copies of the counter with one edit each, laid out as `<dir>/corpus/evidence/round62/c1v2-count.py` +
`<dir>/tools/capture-text.py`, scored by the frozen battery (`c1v2-battery.py --counter <mutant> --work <dir>`,
one full run per mutant, random counter seeds). Kill rule: battery exits 1 with a forger accepted (`MISS`).
Where the battery is blind, a probe builder in scratch was run directly against the intact counter and the mutant.
No lane file was written; no tools installed; no network; scratch deleted before yield.

## Findings (first)

1. **Baseline holds.** Intact counter under the battery: `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, rc=0.
2. **4 of 15 mutants are killed by the battery** (N04, N10, N11, N15). Each kill is by forgers the battery already has.
3. **The battery is blind to five real control gaps** (N01, N02, N03, N09, N14). Each is shown by a probe the battery does not contain: a single-leg / single-profile defect (N01, N02, N10), a builder whose leg raises an exception (N03), an absent `unshare` (N09, **fail-open**), and a non-empty `--work` (N14, **deletes the caller's files**).
4. **Structural cause (INFERENCE from the 12 forgers' fixed behaviour):** every battery forger fails many legs in the profile it does not detect, and every forger is detected only in the plain profile or by both. No battery subject fails exactly one leg, fails exactly one profile, raises inside a leg, or runs without the sandbox. So the `all(oks)` pairing, the `20/20` threshold, the profile-level pairing and the exception path are only exercised by redundancy, not by any subject.
5. **Probability artefact.** N01 (`oks[0]`, pairing on the first sampled profile) survives the battery only because with 20 legs and a random order, a multi-leg forger is caught almost surely. Against a single-leg, single-profile defect it is accepted 4/6 times per probe (below).

## Mutants and verdicts

| id | edit in `main()` (or its wiring) | battery verdict | forgers newly accepted | result |
|---|---|---|---|---|
| N01 pair-first | `results[n] = (oks[0], det)` | BATTERY=PASS (12/12, 4/4) | none | SURVIVED — gap (probes below) |
| N02 pair-neutral-only | `results[n] = (dict(per_profile)["neutral"][j][0], det)` | BATTERY=PASS | none | SURVIVED — gap (plainH19 probe) |
| N03 exception-passes | the two `(False, "counter exception` in the `except Exception` handler → `(True,` | BATTERY=PASS | none | SURVIVED — gap (exc probe) |
| N04 profile-not-set | drop `PROFILE["name"] = pname` (neutral legs run the plain layout) | FORGERS 3/12 | F01 F02 F03 F04 F05 F07 F08 F09 F11 | KILLED |
| N05 seed-fixed | `seed = 7` instead of env/randbits | BATTERY=PASS | none | SURVIVED — equivalent (see below) |
| N06 no-leg-shuffle | `order` not shuffled | BATTERY=PASS | none | SURVIVED — equivalent |
| N07 profile-order-fixed | `for pname in PROFILES:` (no seeded sample) | BATTERY=PASS | none | SURVIVED — equivalent under `all()` |
| N08 preflight-off | `if pre.returncode != 0:` → `if False:` | BATTERY=PASS | none | SURVIVED — contract gap, no false pass |
| N09 preflight-exc-open | `except (OSError, TimeoutExpired)` path `return 2` → `return 0` | BATTERY=PASS | none (battery never runs without `unshare`) | SURVIVED — **gap, fail-open** (probe below) |
| N10 threshold-19 | `verdict = passed >= len(LEG_NAMES) - 1` | FORGERS 11/12 | F12 | KILLED (plus one-leg probe) |
| N11 fail-exit-2 | `return 0 if verdict else 2` | FORGERS 0/12, STUBS 0/4 (all exit 2) | none (all 16 MISS) | KILLED (trivially) |
| N12 verdict-line-const | print `C1V2=PASS` always; exit unchanged | BATTERY=PASS | none | SURVIVED — printed-verdict contract gap, not acceptance |
| N13 cleanup-inverted | `if not a.keep:` → `if a.keep:` (work kept by default) | BATTERY=PASS | none | SURVIVED — documented contract ("deleted unless --keep") unchecked |
| N14 nonempty-guard-off | `if work.exists() and any(work.iterdir()):` → `if False:` | BATTERY=PASS | none | SURVIVED — **gap, destructive** (probe below) |
| N15 pair-by-first-name | `oks = [g[0][0] for ...]` (multi-name legs use the first name's result) | FORGERS 11/12 | F12 | KILLED |

Killed: 4/15 (N04, N10, N11, N15). N11 and N15 are noted as weak kills: N11 is a whole-counter exit change, N15 is kept only by F12 (its only failing leg is P03 NOPYC).

## Probes the battery lacks (direct runs, scratch builders, not frozen)

Probe builders are the landed `tools/build-spans.py` with one edit each; the counter copies the builder into a fixture beside `capture-text.py`.

- **one-leg-H19** (landed minus the `..` entry test, `or ".." in ...` removed): intact `LEGS=19/20 C1V2=FAIL` rc=1; **N10 `LEGS=19/20 C1V2=PASS` rc=0 (accepted)**.
- **plainH19** (`..` accepted only when stdout is a regular file, i.e. only in the plain profile): intact `LEGS=19/20 C1V2=FAIL` rc=1; **N02 `LEGS=20/20 C1V2=PASS` rc=0 (accepted, 1/1)**; N01 accepted 4/6 runs (`LEGS=20/20` in runs 1,2,3,6).
- **neutralH19** (mirror, only in the neutral profile): intact `LEGS=19/20 C1V2=FAIL` rc=1; N02 rejects (`LEGS=19/20 FAIL`); N01 accepted 4/6 runs (1,2,5,6).
- **exc-unreadable** (landed plus `chmod 0` on the first span file after a successful build): intact `LEGS=13/20 C1V2=FAIL` rc=1 (counter exceptions `PermissionError` recorded as fail); **N03 `LEGS=20/20 C1V2=PASS` rc=0 (accepted)**. A first attempt with a wrapper builder was discarded: the wrapper lacked the sibling `capture-text.py` and broke P02, so its output is not used.
- **noUnshare** (`PATH` without `unshare`, do-nothing `exit 0` builder): intact `rc=2`, stderr `c1v2-count: sandbox unavailable ([Errno 2] ... 'unshare'); fail closed`; **N09 `rc=0`, zero `LEG` lines, stub accepted** (the counter returns PASS without running a single leg).
- **N08 with fake `unshare` that exits 1** (`pb/N08-noshell`): intact `rc=2` (fail closed); N08 `LEGS=11/20 C1V2=FAIL` rc=1. Rejected, not accepted: N08 changes the exit code, not the verdict direction, so it is contract-only.
- **sentinel** (non-empty `--work` containing `sentinel.txt`, stub-exit0 builder): intact `rc=2` `--work ... must be absent or empty`, **sentinel survives**; N14 `rc=1` and **sentinel deleted** (the counter's `finally: rmtree(work)` runs on the caller's directory).
- **N13 cleanup-inverted, stub-exit0 builder**: work dir `n13/work` (1.5 MB of fixture trees) remains after the run; intact removes it (`work exists after run: no`).
- **N12 under the battery**: a forger scored `counter_exit=1 ... LEGS=10/20 C1V2=PASS` (the printed verdict contradicts the exit code; the battery reads only the exit code).

## Survivor classification

**Real control gaps (5)** — a builder the intact counter rejects is accepted, or a caller's data is destroyed, or a precondition fails open:
- N01 `oks[0]` pairing: accepts single-leg single-profile defects 8/12 across two probes (intact: 0 accepted).
- N02 neutral-only judging: accepts a plain-only defect 1/1 (intact: rejected). Named missing subject: a forger whose defect exists only in the plain profile.
- N03 exception-as-pass: accepts a landed builder with one unreadable span (intact: 13/20 FAIL). Missing subject: a builder that makes a leg raise.
- N09 fail-open preflight: a do-nothing builder is accepted when `unshare` is absent (intact rejects with rc=2). Missing subject: a run with no sandbox.
- N14 unguarded `rmtree(work)`: deletes a non-empty `--work` (intact refuses). Missing subject: a non-empty `--work`.

**Contract-only (3)** — the counter's documented behaviour is not checked, but no builder is accepted by the mutant:
- N08 preflight off (documented exit 2 on no userns; mutant exits 1 with 11/20 FAIL): no false pass.
- N12 printed verdict constant (documented line `LEGS=... C1V2=PASS`): the printed line can disagree with the exit code; the battery reads the exit code only.
- N13 cleanup inverted (documented "deleted unless --keep"): leftover fixtures; the battery removes its own subject dirs and cannot see it.

**Equivalent for the battery predicate (3):**
- N05 fixed seed, N06 no leg shuffle, N07 fixed profile order. Under `all(oks)` the leg order and seed influence only fixture contents and cross-leg state. The battery has no cross-leg state (each leg uses fresh `leg-<hex>` / random-named fixtures; the child env is clean and cannot read the seed). INFERENCE: equivalent for this battery; N07 is only non-equivalent together with N01-style pairing.

Sandbox observation (INFERENCE, not run): the battery's F06/F10 (parent/any cmdline) appear never to fire in either profile, because the builder runs under the unshare process rather than the counter; that would make the sandbox, not the profiles, defeat them, and leave a neutral-only judge (N02) with no neutral-only forger to catch.

## Recommendations (routed; not written to frozen files)

Per the claim rule, these are battery supplements for the next round, not edits to the frozen battery or counter:
1. A single-leg, single-profile forger (plainH19 / neutralH19 construction) — catches N01, N02 and N10-style thresholds.
2. A subject that makes a leg raise (exc-unreadable) — catches N03.
3. A run with `unshare` absent that expects exit 1 or 2 and no PASS — catches N09.
4. A non-empty `--work` subject that expects exit 2 and the sentinel to survive — catches N14.
5. Check that the printed `C1V2=` token agrees with the exit code — catches N12.

## Commands and evidence

- Baseline: `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/c1v2-count.py --work <scratch>/b/base` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, rc=0.
- Mutant batteries: 15 runs, each with its own `--work` under scratch; per-mutant output lines as in the table (`SUBJECT FORGER F.. MISS`, `BATTERY=...`).
- Probes: direct counter runs listed above; each probe builder source is in scratch and is deleted with it.
- No `git` mutation; one read-only `git status` in the lane (not cited).

## Tool and host notes

- No tools installed; no network; no pacman (host-wide pause respected).
- Scratch `/fast/scratch/hyaku/chousa-r62/MutC1V2Main` (mutant copies, probe builders, battery work dirs) deleted before yield.
- One shell misstep (a leftover `set -e` in the persistent shell) produced a discarded sentinel run; the reported sentinel result is a clean rerun with explicit checks.

VERDICT: KILLED=4/15 survivors_that_are_gaps=5
