# W1 CounterMutation — round-60 C1 counter mutation probe

Seat: CounterMutation (leaf, no dispatch). Scope: frozen claims
`corpus/evidence/round60-claims.md`, prior committed evidence
(`corpus/evidence/round58/*`), current counter/source only. One probe, per
mutation-tester contract. No external fetch, no writes outside this report and
`/fast/scratch/hyaku/chousa-r60/CounterMutation/` (removed before yield), no
commits or git/jj mutation. No tool installs (pacman paused; none needed).

## Freeze-integrity observation (ride-along, not the probe)

The tasking pins claims SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.
The on-disk file `corpus/evidence/round60-claims.md` hashes
`65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`
(`sha256sum`, measured 2026-10-27 pre-probe). The file is untracked in git
(`git status --porcelain`: `?? corpus/evidence/round60-claims.md`; lane HEAD
`b379919a873e7080a31ef92c7002f55f5374e2c6`), so no committed blob arbitrates
which bytes the pinned SHA names. I did not modify the file. The invariants
probed below are quoted from the on-disk bytes; if the pinned SHA names
different bytes, L1 should re-pin or re-freeze before wave close.

## Challenged invariant (C1)

- "captured builder stdout/stderr cannot satisfy a refusal leg"
- "the counter exits 0 only when the frozen safe and hazard legs meet their
  declared requirements"
- Kill rule: "any child output injection passes target"

Target surface: `corpus/evidence/round60/c1-count.py` (uncommitted round-60
counter; pristine SHA256
`66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`).

## Mutant (one plausible defect, smallest behavior-bearing point)

The r58 defect class was target-token output satisfying refusal checks; the
counter's own guard comment at the site reads "Stdout and stderr are
deliberately excluded from all verdict derivation". The plausible regression is
consulting captured stdout in the safe-leg derivation — one-token mutation at
scratch line 41 (scratch copy only; lane bytes never edited):

```diff
--- root/p/q/r/c1-count.py (scratch copy of lane counter)
-        candidate_safe = p.returncode == 0 and intact
+        candidate_safe = p.returncode == 0 and (intact or "=PASS" in p.stdout)
```

Mutant SHA256 `bbc76915e190d48a9682f0e89908aaaea94af7aac1316cb9cbc8a1b1be21974c`
(snapshot kept at scratch `mutant-snapshot.py` during the probe).

## Detector

- **D1 (conformance context)**: `python3 -B c1-count.py --builder tools/build-spans.py --work <fresh>` — the frozen predicate's literal one-line run.
- **D2 (kill-rule probe, decides the verdict)**: same command with
  `--builder hazard-inject.py`, a round-58-class output-injection hazard:
  prints the exact `=PASS` token, exits 0, and deletes the seeded foreign
  orphan `out/spans/S777-1.txt` (fixture provenance: forged fixture the counter
  itself writes, plus the destructive leg demonstrated by pinned r55 in
  `corpus/evidence/round58/controls/c1-controls.txt` `BEFORE_FOREIGN=deleted`).
  Expected on pristine: `C1=FAIL`, exit 1 (injection must not pass). The
  predicate is an iff, so a destructive token-emitting candidate reaching
  `C1=PASS` violates it.

Rig: scratch `root/{corpus,tools}` symlinks (read-only use) +
`root/p/q/r/c1-count.py` so the copy's `parents[3]` root and pinned R55 path
resolve; every run passed an explicit `--work` under scratch. Lane repo bytes
untouched (verified below).

## Results (actual outputs)

| state | run | output | exit |
|---|---|---|---|
| pristine `66e507…` | D1 default | `INJECTION_REJECTED=1/1 BASELINE_DISCRIMINATES=1/1 CANDIDATE_REFUSAL=0/1 C1=FAIL` | 1 |
| pristine | D2 hazard | `INJECTION_REJECTED=1/1 BASELINE_DISCRIMINATES=1/1 CANDIDATE_REFUSAL=0/1 C1=FAIL` | 1 |
| mutant `bbc769…` | D1 default | `INJECTION_REJECTED=1/1 BASELINE_DISCRIMINATES=1/1 CANDIDATE_REFUSAL=0/1 C1=FAIL` | 1 |
| mutant | D2 hazard | `INJECTION_REJECTED=1/1 BASELINE_DISCRIMINATES=1/1 CANDIDATE_REFUSAL=1/1 C1=PASS` | **0** |
| restored `66e507…` | D2 hazard | `INJECTION_REJECTED=1/1 BASELINE_DISCRIMINATES=1/1 CANDIDATE_REFUSAL=0/1 C1=FAIL` | 1 |

Leg-state capture (importing the copied module, `run()` direct):

- pristine: forged→`candidate_safe`, hazard→`baseline_bad`, r55→`baseline_bad`
- mutant: hazard→`candidate_safe` — the destructive token-emitter becomes
  indistinguishable from a safe candidate once stdout enters the derivation.

## Verdict

**Killed** — by D2, the kill-rule probe the frozen predicate's iff names:
pristine rejects the injection hazard (`C1=FAIL`/1), mutant accepts it
(`C1=PASS`/0) purely via the stdout disjunction while the foreign file was
deleted. The baseline (pristine D2) met its expected behavior, so this is a
kill, not an inconclusive.

**Coverage finding (no contract change proposed):** the literal one-line form
of the frozen predicate (D1, candidate = the real builder) is blind to the
mutant — identical output and exit on pristine and mutant bytes. The invariant
"output bytes cannot establish a leg state" is only exercised when the kill
rule is run as a probe (candidate = token-emitting destructive hazard). The
claims text already names that kill rule, so the contract is sound as written;
verification must actually run it, not only the default invocation.

Secondary observations captured during the probe (recorded, not judged):

1. The `forged_safe` branch is unreachable under the pinned forge fixture: the
   counter's own forged.py prints `=PASS` but never deletes, so its run lands
   `candidate_safe` and `forge_blocked` is satisfied vacuously via the
   safe-path branch. Injection rejection is real (the leg cannot be satisfied
   by tokens) but the named state is dead code for this fixture.
2. A destructive candidate and the destructive r55 baseline share the identical
   `baseline_bad` condition (`rc==0 and not intact`); they are distinguished
   only by which builder ran. On pristine this still yields the correct
   verdict (`CANDIDATE_REFUSAL=0/1`).
3. Pristine D1 is `C1=FAIL` exit 1 with the current default builder — the
   candidate builder still deletes the foreign orphan, matching L1's pre-work
   baseline `.ufo/waves/round-60/c1-before.txt` (CANDIDATE_REFUSAL=0/1) and
   `c1-control-proof.txt`. Expected mid-round; inconclusive for the
   conformance direction only, and not load-bearing for the kill verdict.

## Restoration evidence

- Before mutation: scratch copy `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7` (== lane source, verified at copy time).
- After restore: same SHA256, byte-identical to lane source; restored D2 run reproduces pristine behavior (`C1=FAIL`, exit 1).
- Lane repo untouched: `corpus/evidence/round60/c1-count.py` hash `66e50763…` before and after; `git status --porcelain` unchanged (3 untracked entries: `.ufo/waves/round-60/`, `corpus/evidence/round60-claims.md`, `corpus/evidence/round60/`).
- Scratch `/fast/scratch/hyaku/chousa-r60/CounterMutation/` removed after the probe.
