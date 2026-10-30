# Attack20 — round64 attempt2 independent review

Advisory only; no admission, integration, production change, or frozen-rule repair.

Axes: operability (C1), calibration (C2), sourced depth (C3); review objectives are faithful predicates, evidence provenance, and error-path honesty. L1 remains canonical planner. Candidate `controls/ref-preflight-v3.py` is not production. No saturation or resume-continuity claim is evaluated by these instruments.

## Findings, highest severity first

### High — C1's frozen benign expectations contradict its own fixtures

`corpus/evidence/round64/claims.md:36-61,89-93` requires both the frozen battery pass and the whole-name/mirror contract. `c1-battery-v3.py:386-394` draws separate `tag()` values for the created E12/E13 file and the README reference, but `:442-443` requires exit 0. Distinct draws create an unindexed real file and a phantom indexed file: a conforming G02 must fail. Minimal counterexample: create `escaped_q00000001.md`, index only `knowledge/escaped\_q00000002.md`; unescaping does not make those names equal. Likewise `gate notes q00000001.md` versus `knowledge/gate%20notes%20q00000002.md`. These are literal examples of the frozen generator's mismatch, not executed probes. Random collisions are possible, so this is not a claim of mathematical impossibility for every conceivable seed.

The committed before receipt `controls/c1v3-before-full.txt:38-44` actually records E12/E13 FAIL and `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`, matching the frozen before counts. But those two failures cannot honestly be attributed solely to the old checker's normalization false positives. The fixture is independently invalid. A green supplement cannot satisfy the frozen kill rule. Independently inspected `diff -u` shows `c1-battery-supplement.py` changes exactly E12/E13 to reuse a single draw; it is a distinct post-freeze instrument, not the frozen claim's authority. This confirms, rather than hides or repairs, the disclosed mismatch.

### High — C3's counter compares the diagnostic against the wrong path and does not add a directory level

`claims.md:198-203,231-239` requires the exact missing path under a one-level relocation. `c3-count.py:86-92` copies to `WORK/rel-N/lane-copy/corpus/evidence/round65/script.py`. This has the same lane-relative depth as `corpus/evidence/round64/script.py`, not one additional directory. Each copied instrument computes `HERE.parents[2]` (`c3-count.py:34-38`, `run-receipts-v3.py:25-30`), hence the actual diagnostic names `WORK/rel-N/lane-copy/corpus/SOURCES.md`. The counter instead wants `mirror.parent / needs[0]`, which is `WORK/rel-N/lane-copy/corpus/evidence/corpus/SOURCES.md`. These paths are different.

This is a deterministic static counterexample to the expected relocation matching, not an observed run result. Even correctly firing startup assertions cannot satisfy this frozen oracle. `controls/c3-before.txt:1-7` proves only the shifted mutant's unnamed diagnosis and the shift-only result; it does not establish the full after target. Preserve a frozen failure; route a corrected relocation instrument separately.

### Medium — C2 counts harness timeouts as successful mutant kills

`c2-mutrun.py:28-33` promises a leg that itself errors is a harness error (exit 2). Actual `:164-174` catches `subprocess.TimeoutExpired`, appends `('TIMEOUT', False, 'leg timeout')`, then counts `bool(fired)` as a kill. Static minimal counterexample: if each mutant's first subprocess times out, each receives one false TIMEOUT leg; all twelve are counted killed and the runner returns 0 with `AUDIT_MUTANTS_KILLED=12/12`. No behavioral matrix leg has completed in that scenario. This is a runner error-path weakness, not evidence that the committed v1 receipt was produced under timeouts: `controls/c2-mutrun-v1.txt:1-13` contains normal named legs and the claimed six survivors.

### Medium — the promised unmutated C2 receipt control is not implemented by the frozen runner

`claims.md:164-167` says the runner re-derives the committed checker's outputs at the same run and prints each unmutated leg's actual output beside its expectation. `c2-mutrun.py:86-100,135-174` reads the target, immediately patches each mutant, executes only mutants, and prints mutant status plus failed-leg rc strings. There is no unmutated-target run or actual-versus-expected baseline output. The before receipt itself also has only twelve MUT lines and the summary. Thus the frozen before count/survivor list is faithfully transcribed, but this additional claimed control is absent. Together with timeout-as-kill, a high killed count alone cannot establish that the environment still accepts the unmodified checker.

### Low — C3's universal instrument wording exceeds its enumerated coverage

`claims.md:194-198` says every round64 instrument deriving a lane file from `__file__`, then enumerates three. `c2-mutrun.py:49-53` also derives `LANE = HERE.parents[2]` and asserts `corpus/SOURCES.md`; it is absent from `c3-count.py:41-45`. This does not invalidate a result explicitly limited to the frozen three; it does invalidate interpreting `3/3` as exhaustive coverage of the instrument family. The inherited erratum already discloses this limit.

## Provenance and observed command evidence

- `git log -1 --format='%H %s' bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/claims.md` — exit 0; output `92a084175f9534296527b77a2b7fe38560b96b18 round-64: frozen instruments and controls (c1-battery-v3, claims-audit-v2, mutant generator+runner, relocation counter, before-receipts)`. Read-only provenance inspection, no git mutation.
- `sha256sum corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/gen-audit-mutants.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/controls/root-shift-mutant.py tools/claims-audit-v2.py` — exit 0. Prefixes respectively `4b3f0b658bcd3bb6`, `6e1055b28d315e32`, `0045787ee9de3974`, `465a8c5efbb870f7`, `0f3cfae75f711f17`, `f0f9b26083ff62c3`, `db0e28dd4c033259`; all match `claims.md:263-266`.
- `diff -u corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/c1-battery-supplement.py` — exit 1 (differences); only E12/E13 tag reuse changes, as described above.
- `git --version && sha256sum --version && diff --version` — exit 0; `git version 2.56.0`, `sha256sum 0.8.0`, `diff diff (pi-uu-diff) 0.8.0`. Existing tools only; no installations or updates.
- LSP discovery `read xd://lsp` returned `No such tool`; no mounted LSP server/device was available. Text search and source inspection are literal fallback, not semantic references/diagnostics proof.

## Residual risk and verification gaps

No benchmark, battery, alternate runtime, mutable fixture, or network command was run. Reported before outputs are inherited receipts, not new executions. Counterexamples above are source-derived and explicitly distinguished from measured output. Candidate behavior and after counts remain unverified here; no PASS or closure is recommended from this review. The known erratum independently agrees with C1/C3 findings, but is not treated as an instruction or replacement predicate. C2 timeouts and baseline-control absence arise directly from the frozen runner bytes. No scratch tree or clone was created; no cleanup was needed. Only this seat's reports were written.

## Self-evaluation

Accuracy 4/5: hashes and actual receipt lines are observed; runtime counterexamples are static, labeled as such. Completeness 4/5: C1–C3 before receipts and relevant predicate/error paths covered; no fresh runtime after evidence. Clarity 4/5: separates claim failure, supplement repair, and runner weakness; five findings add some length. Actionability 4/5: exact source paths and frozen-rule consequences supplied; only L1 can route fixes and closure. Conciseness 4/5: provenance retained for reproducibility rather than compressed away. Overall 4.0/5. Highest-value improvement is a separately authorized non-author runtime check of corrected instruments, without admitting the frozen claims from replacement results. Would the user agree: likely, provided this remains advisory and does not masquerade as a fresh run.
