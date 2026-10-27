# CounterFixReviewer — Round-60 w1 (C1 counter-fix review)

**Seat.** CounterFixReviewer (leaf reviewer; no subagent dispatch). **Scope.** Bounded review of the
round-60 C1 counter fix — `corpus/evidence/round60/c1-count.py` — against the frozen C1 predicate in
`corpus/evidence/round60-claims.md`, prior committed evidence (round-58 frozen counter, R59Executor09),
and current source. No live fetch, no writes outside this report, no git/jj mutation. All runs used
scratch `/fast/scratch/hyaku/chousa-r60/CounterFixReviewer/` (removed before yield; outputs pasted here).

**Method.** Static read of the counter, four measured runs in isolated scratch work dirs (frozen
predicate invocation shape `--work <fresh-abs-dir> --seed 6001`), digest-variant tests on the claims
file, and hash pins of every artifact the predicate names. C2/S101 is out of my seat's scope (covered
by S101*/C2* seats).

## 0. Pins (all measured this seat, 2026-10-27)

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sha256sum <paths>
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py   (worktree)
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  (git show 9e73a03:…round58/c1-count.py — identical: r58 bytes FROZEN ✓)
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py   (= the unsafe r55 bytes: the fix candidate does not exist yet)
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
```

Lane tip `b379919a873e7080a31ef92c7002f55f5374e2c6` (round-59 spot-check), matching the claim base.
`git status --porcelain` → `?? corpus/evidence/round60-claims.md`, `?? corpus/evidence/round60/`
(both untracked; see §3).

## 1. Findings — C1 counter fix vs its own frozen predicate

Frozen predicate (claims, C1): `c1-count.py --builder <builder> --work <fresh-abs> --seed 6001`
prints `C1=PASS` / exit 0 **iff** (a) candidate reaches the independently observed safe path without
deleting the foreign file, (b) pinned r55 control deletes it, (c) output-injection mutant prints
`=PASS` but is scored a failure. Kill rule: candidate fails safe path, any child output injection
passes target, or baseline control does not prove destruction.

**F1 — CRITICAL: clause (c) is a tautology; the injection leg cannot fail.**
`round60/c1-count.py:42-44` — `baseline_bad` and `forged_safe` are the *same expression*
(`rc == 0 and not intact`), and `:44` returns `baseline_bad` first, so the `"forged_safe"` state is
unreachable and `forge_blocked = forge_state != "forged_safe"` (`:63`) is unconditionally true for
every rc==0 run that leaves the file alone. The embedded mutant (`:55-57`: prints `=PASS`, exit 0,
touches nothing) is never scored a failure — its state bucket is `candidate_safe` — and the leg never
asserts the mutant's output (`p.stdout`/`p.stderr` are captured at `:37` and never read), so a mutant
that prints nothing scores identically. `INJECTION_REJECTED=1/1` therefore carries no information
about injection. The predicate's "(c) prints `=PASS` but is scored as a failure" is not implemented:
the counter's own injection stub, handed in as `--builder`, is credited `C1=PASS` (sibling
BuildCounter §2.2 run C — independently consistent with the dead-branch proof here).

**F2 — CRITICAL: clause (a) accepts a do-nothing builder; the "safe path" is never observed.**
`candidate_safe = rc == 0 and intact` (`:41`). No check reads `out/spans` after the candidate: the
default run shows the builder writing `S601-1.txt`, and the counter never looks at it. Measured M2
below: a builder that prints `=PASS` and writes **nothing** yields `C1=PASS`, exit 0 — the exact
do-nothing-control failure mode the fleet lesson (§9: a target must be one a do-nothing control
cannot reach) forbids. This alone blocks C1 admission as scored.

**F3 — PASS (the one clause the counter does enforce): live injection is killed.**
M3 below: a candidate that prints `=PASS` **and** deletes the foreign file, exit 0, scores
`CANDIDATE_REFUSAL=0/1`, `C1=FAIL`, exit 1. Destruction — not output — is the only thing that can
flip the verdict, which is the correct polarity; output bytes genuinely cannot establish a leg state
(`:38-44` reads only rc + filesystem). Kill rule clause "any child output injection passes target"
holds.

**F4 — MEDIUM: the r55 control is bound by path only.**
`:19` resolves `BASE/"controls/build-spans-r55.py"` with no runtime digest; round 58 pinned
`R55_BUILDER_SHA = 1ed2650a…` and round 60 dropped the pin. Today's control matches `1ed2650a…`
(§0), so no drift has occurred, but a swapped control would silently redefine the negative leg.
Fail-closed sha256 check recommended before admission.

**F5 — LOW.**
- `--seed` parsed (`:53`), never read: the predicate's `--seed 6001` is decorative.
- `CANDIDATE_REFUSAL` (`:72`) is a misnomer: the leg accepts `rc == 0`; the round-58 scenario
  semantics (hardened builder refuses orphan deletion, rc≠0) are inverted — the leg rewards
  tolerance of the orphan foreign file and would score an honest refusing candidate FAIL (see §2
  default run; the current default builder *is* the unsafe control, so this is the honest before
  state, but the label/semantics mismatch should not survive into the after state).
- Reused `--work` crashes with uncaught `FileExistsError` (`:28-29` `cache.mkdir()`): fail-closed,
  acceptable, but a clean "work dir not fresh" refusal is better.
- Wave hygiene: `corpus/evidence/round60/__pycache__/c1-count.cpython-314.pyc` (mtime 17:57,
  untracked) — a seat imported the counter module instead of running it, leaving bytecode in the
  lane tree. Run probes with `python3 -B` or `PYTHONDONTWRITEBYTECODE=1`.

## 2. Measured runs (scratch; builder mutants sha256-pinned)

```
$ python3 corpus/evidence/round60/c1-count.py --work $S/wk-default --seed 6001     # M1: default builder (= r55 bytes)
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1
# receipts: wk-default/candidate/out/spans contained S601-1.txt (built), foreign S777-1.txt deleted by the builder

$ … --builder $S/noop-builder.py --work $S/wk-noop --seed 6001                     # M2: prints =PASS, exit 0, writes nothing
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0                                                                             # 69c51f4425283167e36be8843fd44c10300835bb15768596403ac3291c683497

$ … --builder $S/inject-builder.py --work $S/wk-inject --seed 6001                 # M3: prints =PASS, deletes foreign, exit 0
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1                                                                             # aa00d99c20398200b9b6093a1f9d6fafb92d8f3beb29ee5b15715a1f2338b5f6
```

M2 is the admission-blocking receipt: the counter's target is reachable by a do-nothing control.
M3 shows the kill rule's destructive arm works. M1 is the honest before-state — the default
`--builder` is byte-identical to the unsafe control, so `C1=FAIL` today is expected mid-round and is
not itself a defect; the defects are F1/F2, which would survive a correct candidate landing.

## 3. Freeze integrity (recorded; adjudication belongs to the L1 + freeze seats)

The assignment stamps immutable claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`;
the named file hashes `65721569…`. No encoding variant reconciles them (measured: raw
`65721569…`, rstrip-NL `cae804fa…`, plus-NL `ed2999d0…`, CRLF `dbb847b8…`, git blob
`5ea0acf0…`). Mtime ordering: claims 17:51:18 < w1-spec 17:55:15 < w1.ready 17:55:21 <
w1.ready.dispatched 17:56:56 — the on-disk bytes predate dispatch, so the stamp was taken over
different (draft) bytes or miscomputed; the file is untracked, so pre-dispatch bytes are
unrecoverable. The frozen predicate's referents (`round60-claims.md`, `round60/c1-count.py`,
`round60/c2-count.py`) are all uncommitted at tip `b379919` — until `jj-lane.sh` lands them, the
predicate bytes remain mutable (kumitate r42 hazard). Round-58 bytes **are** frozen (§0: committed ==
worktree == `65da18bb…`), so the "round-58 bytes remain frozen" line of the claim holds. Sibling
BuildCounter F1 reached the same mismatch independently; the whole wave keyed its analysis to the
on-disk bytes.

**Verdict.** The round-60 C1 counter, as frozen on disk (`66e50763…`), does **not** satisfy its own
frozen predicate: the iff fails on clauses (a) and (c) (F1, F2, M2). C1 must not be admitted on this
counter. Because the claims text names this counter as the frozen predicate, repairing F1/F2 is a
predicate amendment: the L1 should fix the counter (per-leg live assertion: mutant must print
`=PASS` **and** delete to exercise the injection arm; candidate leg must observe the produced span
bytes and, per the declared hardening semantics, settle the refuse-vs-tolerate polarity of the
orphan foreign file; pin the r55 control sha; use or drop `--seed`), then re-freeze claims +
counter with a recomputed digest and commit both through `jj-lane.sh` **before** any seat scores C1
as final — a rule changed after scoring is not the claim's rule.

**Residual risk / gaps.** I did not execute the round-58 counter end-to-end this seat (its before
behavior is pinned by R59Executor09 and the byte-freeze check); I did not audit c2-count.py (C2
seats' scope); sibling-overlap note: BuildCounter independently reports F1/F2-class defects with
matching receipts — my M3 live-injection kill, the digest-variant table, and the mtime-ordering
argument are additive. Scratch dir removed after this report was written.

— CounterFixReviewer, 2026-10-27
