# C1BuilderControl — builder-side control audit of the round-60 C1 counter

**Seat.** C1BuilderControl (leaf executor, axes: operability, depth). **Scope.** The builder-control
legs of the frozen round-60 C1 predicate only: whether the pinned r55 builder is a real negative
control, whether the candidate/safe leg can be satisfied without builder work, and whether the
injection leg measures anything. No counter or builder file edited, no fetch, no install, no spawn,
no git/jj mutation. Scratch `/fast/scratch/hyaku/chousa-r60/C1BuilderControl` (removed before yield).

## Pins measured this seat

```
$ sha256sum corpus/evidence/round60/c1-count.py corpus/evidence/round58/controls/build-spans-r55.py \
            tools/build-spans.py tools/capture-text.py
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
$ cmp -s corpus/evidence/round58/controls/build-spans-r55.py tools/build-spans.py && echo identical
identical
```

The negative control and the candidate are **byte-identical at claim base**. That is expected (the
claim's before-state is the unhardened builder), and it is sound only because the control lives in a
separate frozen copy that a candidate fix does not touch — which is true today (F4 below is about
the missing *check*, not the missing copy).

Precondition note (not this seat's finding, already reported by a sibling): the claims artifact
`corpus/evidence/round60-claims.md` hashes `65721569…`, not the `09d8053f…` named in every seat
prompt, and `git log --all -- corpus/evidence/round60-claims.md` is empty — the freeze is untracked.
Cited by `C2CounterAudit.md` in this same directory. My analysis below is against the bytes on disk
(`65721569…`), which are the bytes the counter and receipts were built from.

## What the three legs actually test (claim clause → code)

| Claim clause (round60-claims.md C1) | Counter leg | Code |
|---|---|---|
| (a) "candidate reaches the independently observed safe path without deleting the foreign file" | `CANDIDATE_REFUSAL` | `c1-count.py:41,68-69` |
| (b) "pinned r55 builder provides the known unsafe control by deleting it" | `BASELINE_DISCRIMINATES` | `c1-count.py:42,66-67` |
| (c) "output-injection mutant prints `=PASS` but is scored as a failure" | `INJECTION_REJECTED` | `c1-count.py:43,60-63` |

## Findings

| # | severity | location | finding | evidence |
|---|---|---|---|---|
| F1 | critical | `c1-count.py:38,41,68-69` | The safe leg is **work-blind**: `candidate_safe = returncode == 0 and foreign intact`. A builder that does nothing (`sys.exit(0)`, 23 bytes) reaches `C1=PASS`, exit 0. The counter never observes `spans.tsv`, a span file, or any build output, so "reaches the independently observed safe path" is not measured — only "did not delete one file". | §C (`C1=PASS`), §M (`out/` holds only the seeded foreign file) |
| F2 | critical | `c1-count.py:24,37,62,66,68` | Leg directories are **fixed names** (`forge`, `baseline`, `candidate`) and are the child's `cwd` (`subprocess.run(..., cwd=work)`). A forge that is destructive in every leg whose cwd is not literally `candidate` reaches `C1=PASS` without any builder work — QUALITY criterion 85's exact defect class ("work directories carry random names"). | §R (`C1=PASS`, exit 0) |
| F3 | critical | `c1-count.py:42-43,63` | `INJECTION_REJECTED` is a **constant**. `baseline_bad` and `forged_safe` are the same predicate (`rc == 0 and not intact`); `baseline_bad` is tested first, so `forged_safe` is unreachable and `forge_blocked = forge_state != "forged_safe"` is `True` for every possible builder. The counter's own mutant is scored `candidate_safe` — the *same* state an honest non-deleting candidate gets — so the leg cannot distinguish the two. Claim clause (c) is satisfied by construction, not by measurement. | §F (state set = `{'', 'baseline_bad', 'candidate_safe'}`), §L (`forged.py state='candidate_safe'`), §D (exit-1 builder still `1/1`) |
| F4 | high | `c1-count.py:19,66` | The "pinned r55 builder" is pinned **by path only**. Round 58 froze the control by digest (`round58/claims.md`: `1ed2650a…`; `round58/c1-count.py:350` compares it); round 60 dropped that check. Substituting a different destructive stub at that path still prints `BASELINE_DISCRIMINATES=1/1`. A candidate-side edit that overwrites the control copy would silently pass. | §I (stub `c0541015…` → `1/1`) |
| F5 | high | `c1-count.py:41,68` vs `round58/claims.md` C1 clause (1), `round58/c1-count.py:209-224` | **The two frozen claims require opposite behaviour on the same fixture.** Round 58 froze "a foreign `S###-N.txt` … is preserved and causes **refusal** before orphan deletion" (exit ≠ 0). Round 60 accepts only exit 0 with the file intact. A builder that implements round-58's target is scored `CANDIDATE_REFUSAL=0/1` → `C1=FAIL`. | §O (`C1=FAIL`; direct run: `refused FOREIGN S777-1.txt`, exit 1, file preserved) |
| F6 | medium | `c1-count.py:23-26,55` | `--work` is not re-runnable: `work.mkdir(exist_ok=True)` then `cache.mkdir()` / `out.mkdir()` without `exist_ok` → `FileExistsError` traceback, no `C1=` line, exit 1. A crash and a legitimate `C1=FAIL` are indistinguishable to a closure that reads the exit code. | §G |
| F7 | medium | `c1-count.py:53,71-73` | The leg named `CANDIDATE_REFUSAL` passes on `returncode == 0` — it tests the *opposite* of a refusal. The counter has no refusal leg at all, so claim clause "captured builder stdout/stderr cannot satisfy a refusal leg" is vacuously true here. `--seed 6001`, named in the frozen predicate, is accepted and never used. | §N (`seed` at `:53` only), §A/§B |
| F8 | medium | `.ufo/waves/round-60/c1-control-proof.txt` | The pre-dispatch control proof did not score a do-nothing control against the **new** counter: item 1 runs the round-58 counter and is excluded as "builder CLI interface mismatch", item 2 cites the round-59 forgery, item 3 relies on the base builder failing. The prompt's §9 control ("cheapest control that skips the claimed work") was therefore never run — and it meets the target (§C). | §C, `c1-control-proof.txt` items 1–3 |

## Positive results (credit where the control does work)

- **The r55 control is a real, deterministic negative.** It deletes every `spans/S###-N.txt` not in
  the current manifest through its orphan-cleanup loop (`tools/build-spans.py:203-205`, `SPAN_RE`
  `:47`); both `S777-1.txt` and a second seeded `S778-2.txt` are removed while `notes.txt` survives.
  Attribution to the hazard path, not to the fixture, is therefore exact. (§H)
- **The counter does discriminate a genuine fix.** A manifest-scoped cleanup (delete only
  span-named files the previous `spans.tsv` listed) prints `C1=PASS`, exit 0, and still builds and
  preserves the foreign file. (§P) So F1/F2 are under-specification of the safe leg, not an
  unsatisfiable target.
- **The round-58 output-injection forgery class (P6) is closed.** No leg reads `proc.stdout` or
  `proc.stderr` (only comments at `:40,:65`); verdicts derive from return code and file bytes. (§N)

## Measurements (verbatim; every run used `--work` inside this seat's scratch)

### A — pinned r55 as candidate (the control against itself)

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder corpus/evidence/round58/controls/build-spans-r55.py --work <scratch>/A-baseline --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

### B — lane builder `tools/build-spans.py` (claim base)

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

Matches the filed `c1-before.txt` (its four lines, same order). Base is honestly a stop.

### C — do-nothing builder (`noop.py`, `14c75fb9…`, 23 bytes: `import sys; sys.exit(0)`)

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

### D — always-fail builder (`rc1.py`, `2239d46e…`, `sys.exit(1)`)

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

`INJECTION_REJECTED=1/1` in A, B, C, D and E: constant.

### E — token-forging *and* destructive builder (`delforge.py`, `aaf6a0a1…`: prints `=PASS`, unlinks every `out/spans/*`, exits 0)

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

### F — `run()` state enumeration (`state-probe.py`, `41b37d5d…`, imports the counter read-only)

```
noop_rc0_intact: returncode=0 state='candidate_safe'
delforge_rc0_deleted: returncode=0 state='baseline_bad'
rc1_intact: returncode=1 state=''
states emitted: ['', 'baseline_bad', 'candidate_safe']
```

`forged_safe` never appears. Static confirmation: `:42` and `:43` are the same expression and `:42`
is evaluated first in the `:44` chain.

### G — `--work` reuse

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work <scratch>/G-reuse --seed 6001   # first run
CANDIDATE_REFUSAL=0/1
C1=FAIL
$ python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work <scratch>/G-reuse --seed 6001   # second run
  File ".../c1-count.py", line 25, in run
    cache.mkdir()
FileExistsError: [Errno 17] File exists: '<scratch>/G-reuse/forge/cache'
exit=1
```

No `C1=` line on the second run.

### H — hazard attribution (pinned r55 run directly on the counter's fixture shape)

```
before: S777-1.txt  S778-2.txt  notes.txt
$ python3 -B corpus/evidence/round58/controls/build-spans-r55.py --quotes .../quotes.tsv --out .../out --cache .../cache
QUOTE S601 char 0 spans/S601-1.txt
SPANS_ROWS=1 WRITTEN=1
exit=0
after:  S601-1.txt  notes.txt
```

Cleanup source: `tools/build-spans.py:203-205` (`if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files: p.unlink()`), `SPAN_RE` `:47` = `^S\d{3}-\d+\.txt$`. The counter's fixture name is chosen to match.

### I — control substituted at the pinned path (scratch copy of the evidence layout)

```
$ sha256sum <scratch>/swap/corpus/evidence/round58/controls/build-spans-r55.py
c0541015196694faff1190c8c96c7d0773918cc5d2005cd705862901fec91916   # a 10-line destructive stub, NOT r55
$ python3 -B <scratch>/swap/corpus/evidence/round60/c1-count.py --builder <scratch>/swap/tools/build-spans.py --work <scratch>/I-swap --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

`BASELINE_DISCRIMINATES=1/1` on a control that is not the pinned artifact: the control is any
program that deletes span-named files and exits 0. With the file absent the leg reports `0/1` and
fails closed (no crash), so absence is handled; *substitution* is not.

### L — the counter's own injection mutant, scored

```
$ ls -l <scratch>/A-baseline/forged.py
-rw-r--r-- 74 ... forged.py          # import sys / print('=PASS') / print('all seven hazards accepted') / sys.exit(0)
$ python3 -B forged-state.py corpus/evidence/round60/c1-count.py <scratch>/A-baseline/forged.py <scratch>/L-forged-work
forged.py returncode=0 state='candidate_safe' forge_blocked=True
```

The mutant is scored *safe*, not rejected; the leg passes because a different string
(`forged_safe`) is absent.

### M — what the passing do-nothing candidate left behind

```
$ find <scratch>/C-noop/candidate/out -maxdepth 2
<scratch>/C-noop/candidate/out
<scratch>/C-noop/candidate/out/spans
<scratch>/C-noop/candidate/out/spans/S777-1.txt
```

No `spans.tsv`, no span file: `C1=PASS` with zero build work.

### N — source facts

```
$ grep -n -E 'stdout|stderr|seed' corpus/evidence/round60/c1-count.py
40:        # stderr are deliberately excluded from all verdict derivation.
53:    ap.add_argument("--seed", type=int, default=6001)
65:        # it deletes the seeded foreign file while attempting a rebuild.
```

No verdict reads child output; `--seed` is parsed and never used.

### O — round-58 target behaviour under the round-60 counter (`r58-honest.py`, `6b41be9e…`: refuse when a span-named file is absent from `spans.tsv`, else delegate to pinned r55)

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder <scratch>/r58-honest.py --work <scratch>/O-conflict --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
$ python3 -B <scratch>/r58-honest.py --quotes .../quotes.tsv --out .../out --cache .../cache
build-spans: refused FOREIGN S777-1.txt: not in manifest
exit=1
S777-1.txt        # preserved
```

### P — a legitimate round-60 fix does pass (`r60-target.py`, `ff59da19…`: r55 with manifest-scoped orphan cleanup)

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder <scratch>/r60-target.py --work <scratch>/P-target --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
$ python3 -B <scratch>/r60-target.py --quotes .../quotes.tsv --out .../out --cache .../cache
QUOTE S601 char 0 spans/S601-1.txt
SPANS_ROWS=1 WRITTEN=1
exit=0
S601-1.txt  S777-1.txt
```

### R — cwd-keyed forge (`cwdforge.py`, `e0e01f8f…`: destructive everywhere except when `cwd` basename is `candidate`)

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder <scratch>/cwdforge.py --work <scratch>/R-cwdforge --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

Forge source (reproducible from this report):

```python
import os, pathlib, sys
a = sys.argv[1:]
out = pathlib.Path(a[a.index("--out") + 1])
sd = out / "spans"
if pathlib.Path(os.getcwd()).name != "candidate" and sd.is_dir():
    for p in sd.iterdir():
        p.unlink()
print("=PASS")
sys.exit(0)
```

## Verdicts on the frozen predicate's three clauses

- **(a) candidate safe path — NOT met as implemented.** Reachable by a do-nothing stub (§C) and by a
  cwd-keyed forge (§R); the "independently observed safe path" is never observed (§M). The target is
  satisfiable by a real fix (§P), so this is a counter defect, not a target defect.
- **(b) baseline control — met, with an unbound pin.** The r55 copy is deterministically destructive
  on exactly the hazard path (§H) and is byte-separate from the candidate (§K), so a candidate fix
  does not disarm it; but the pin is by path, and substitution is accepted (§I).
- **(c) output-injection mutant — not measured.** `INJECTION_REJECTED` cannot be 0 (§F), and the
  mutant is scored `candidate_safe` (§L). The clause is decoration, not a test.

**Net.** At base the counter honestly reports `C1=FAIL` (§A/§B), and it will report `C1=PASS` for a
genuine fix (§P) — but it will equally report `C1=PASS` for a builder that does nothing and for a
builder that detects its own leg. The round-60 C1 predicate is therefore still forgeable in the
direction C1 exists to close: a verdict that does not bind the work.

## Required repairs (bounded; for the counter owner, not applied by this seat)

1. Make the safe leg work-bound: require the candidate to have produced `spans.tsv` with the
   expected row and span bytes (the round-58 `expect_ok` shape) before `candidate_safe` can hold.
2. Randomize leg directory names per run (QUALITY criterion 85) and stop exposing the leg identity
   via `cwd`; or run every leg through a wrapper that normalizes `cwd`/`--out`.
3. Delete `forged_safe` or make the injection leg measurable: score the mutant's *behaviour*
   (e.g. its state must differ from `candidate_safe`), and assert that the leg can fail.
4. Verify the control's digest in code (`R55_BUILDER_SHA = 1ed2650a…`, as round 58 did at
   `round58/c1-count.py:350`), and fail closed with a named line when it differs.
5. Reconcile F5 with round 58 explicitly: either the fixture must be a case where success is the
   safe outcome (round 58 froze refusal for this exact class), or clause (a) must accept refusal and
   the claim's wording must say so.
6. Make `--work` re-runnable (`exist_ok=True`) and print a `C1=` line on any internal error, so a
   crash is never read as a verdict; drop or use `--seed`; rename `CANDIDATE_REFUSAL` to what it
   tests.

## Limits

- Analysis is limited to the builder-control legs; the C2 counter, the registry/frontier step, and
  the claim's score delta are other seats' scope.
- No live fetch; L0 `8d77e6c1` untouched. No external truth claimed about S101 or any source.
- The scratch builders above are probes, not proposals for the lane's builder: `r60-target.py` is a
  demonstration that a manifest-scoped cleanup satisfies the counter, not a reviewed hardening.
- Not exercised: `c2-count.py`, the full round-58 battery, any scorecard scoring.

## Hygiene

Lane reads only (`read`/`grep`/`sha256sum`/`python3 -B` against lane files); every run wrote under
`/fast/scratch/hyaku/chousa-r60/C1BuilderControl`, all with `PYTHONDONTWRITEBYTECODE=1` and
`python3 -B` so no `__pycache__` was created in the lane. Lane write: this report only. Scratch
removed after the final run. No installs (Python 3.14.8 present); `/home/vgpnk/.omp/agent/RULES.md`
rules therefore not exercised and pacman not run.

Observed, not authored here: `corpus/evidence/round60/__pycache__/c1-count.cpython-314.pyc`
(mtime 17:57:59, before this seat's first run) — a sibling seat imported the counter without `-B`.
Left in place for the L1 to sweep; it is untracked lane residue, not evidence.

---
seat: C1BuilderControl
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-60/w1/C1BuilderControl.md
scratch: /fast/scratch/hyaku/chousa-r60/C1BuilderControl (removed)
lane writes: .ufo/waves/round-60/w1/C1BuilderControl.md (this file) only
