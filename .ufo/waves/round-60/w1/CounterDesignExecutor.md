# CounterDesignExecutor — round-60 counter design against the frozen C1/C2 predicates

**Seat.** CounterDesignExecutor (leaf executor, axis **operability**; depth secondary). **Mode.**
Bounded analysis only: the frozen round-60 claims, the prior committed round-58/round-59 counter
evidence, and the two round-60 counters as they exist in the working tree. **No production edit, no
lane/tracked write, no fetch, no install, no spawn.** Scratch was
`/fast/scratch/hyaku/chousa-r60/CounterDesignExecutor` (created, used, removed before yield).

**Pins measured this seat (working tree, round-60 evidence is untracked — `git status --
corpus/evidence/round60/` → `?? corpus/evidence/round60/`):**

```
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe  corpus/evidence/round60/c2-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
```

Freeze note (independent measurement, no file changed): the assignment names claim SHA
`09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; `sha256sum` over the frozen
file returns `65721569…` as above. Reconciliation belongs to the L1/freeze owners; this seat did not
touch the file.

**Headline.** Both frozen predicates are falsified by their own counters, and each fails on the
*positive* direction (a do-nothing control reaches the target), not only on a typo. C1's injection
leg is dead code, and the counter accepts an unimplemented printer as `C1=PASS`. C2's counter passes
on the pre-round-60 tree, so the declared before-state is not implemented. Details and one-command
reproductions follow.

---

## 1. C1 — frozen predicate vs. the counter that is supposed to measure it

Frozen requirement (claims file, C1): run
`python3 corpus/evidence/round60/c1-count.py --builder <builder> --work <fresh-absolute-dir> --seed 6001`;
it prints `C1=PASS` and exits 0 **iff** (a) candidate safe + foreign file intact, (b) pinned r55
deletes it, (c) the output-injection mutant **prints `=PASS` but is scored as a failure**. "The
counter captures child output only for diagnosis; output bytes cannot establish a leg state."

### F1 (decisive) — leg (c) is dead code; `INJECTION_REJECTED` is a constant 1/1

`corpus/evidence/round60/c1-count.py:41-44`:

```python
candidate_safe = p.returncode == 0 and intact          # :41
baseline_bad   = p.returncode == 0 and not intact      # :42
forged_safe    = p.returncode == 0 and not intact      # :43  <- identical predicate to :42
return p.returncode, "candidate_safe" if candidate_safe else ("baseline_bad" if baseline_bad else ("forged_safe" if forged_safe else ""))
```

`:42` and `:43` are the same boolean; `"baseline_bad"` is selected first, so **`"forged_safe"` is
unreachable**. `forge_blocked = forge_state != "forged_safe"` (`:63`) is therefore `True` for every
possible input, and `INJECTION_REJECTED=1/1` (`:71`) is hard-wired. Measured against the counter's
own mutant file (`:60`, bytes identical to the probe body — both hash `60630ebd…`):

```
$ python3 probe_mutant.py
counter_written_mutant rc=0 state='candidate_safe'
forge_blocked=True
forged_safe_reachable=no
```

The mutant is scored `candidate_safe` — i.e. **success** — while the counter reports
`INJECTION_REJECTED=1/1`. That is requirement (c) inverted twice over: the mutant is not scored a
failure, and the leg that was supposed to score it cannot fail.

### F2 (decisive) — an unimplemented printer reaches `C1=PASS`, exit 0

Same three lines the counter names as the forgery (`:60`), supplied as `--builder`:

```
$ printf "import sys\nprint('=PASS')\nprint('all seven hazards accepted')\nsys.exit(0)\n" > forged_printer.py
$ python3 corpus/evidence/round60/c1-count.py --builder "$S/forged_printer.py" --work "$S/f1" --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0
```

A builder with no refusal logic at all — a script that writes no `spans.tsv`, decodes no capture,
never inspects `--out` — satisfies (a). So does a `sys.exit(0)`-only script ("silent_rc0" in the
state probe, `state='candidate_safe'`). This is the §9 forbidden case: the declared target is
reachable by a do-nothing control. The counter never asserts a positive artifact from the candidate
(`grep -c 'spans.tsv\|SPANS_ROWS'` → **0**), so "reaches the independently observed safe path" is
measured as "did not delete one seeded file and exited 0".

### F3 (decisive) — the safe/hazard polarity is inverted against frozen round-58 bytes

The seeded fixture is round-58's FOREIGN hazard (`out/spans/S777-1.txt`, `:32-34`). Round 58 froze
the opposite verdict for exactly this state — `corpus/evidence/round58/c1-count.py:217-218`:

```python
if proc.returncode == 0:
    legs.append(f"FOREIGN={FAIL}(rc=0, orphans deleted: foreign gone={not foreign.exists()})")
elif not foreign.exists(): ...
```

Round 60 scores that same fixture `candidate_safe` only when `rc == 0` (`:41`). A builder that obeys
round 58 — refuses with `rc != 0`, leaves the file intact, names the reason — scores `state=''`:

```
$ python3 corpus/evidence/round60/c1-count.py --builder "$S/honest_refuser.py" --work "$S/f2" --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1
```

So `C1=PASS` under round 60 *implies* `FOREIGN=FAIL` under round 58, and round-58 conformance implies
round-60 `C1=FAIL`. The two frozen artifacts are mutually exclusive on the same fixture; the C1 claim
is not causally separable from the round-58 FOREIGN leg it cites as its antecedent. The claim text
("does not claim the builder itself meets all hazard legs") does not repair this: the counter's only
verdict-bearing fixture *is* the hazard fixture.

### F4 — legs (a) and (b) are the same bytes under the default invocation

```
$ sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
1ed2650a…c80bf6  tools/build-spans.py
1ed2650a…c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
```

`--builder` defaults to `ROOT/tools/build-spans.py` (`:51`) and `R55` is `:19`; both resolve to
byte-identical files (corroborating `round-59/w1/R59Executor09.md` §1). The same program cannot be
`candidate_safe` (rc0 ∧ intact) and `baseline_bad` (rc0 ∧ ¬intact) in the same run, so the default
invocation can never print `C1=PASS` — measured:

```
$ python3 corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work "$S/t1/candidate" --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1
```

`BASELINE_DISCRIMINATES=1/1` is then not a control at all: it certifies that the candidate's own
bytes delete the file. A discriminating control must be pinned *other* bytes, and equality with the
candidate must be a pre-failure, not a leg pass.

### F5 — the hazard battery and containment legs were dropped, not restructured

The claim says the counter "exits 0 only when the frozen safe and hazard legs meet their declared
requirements". The counter has no leg list:

```
$ grep -c 'legs.append' corpus/evidence/round58/c1-count.py   # 23
$ grep -c 'legs.append' corpus/evidence/round60/c1-count.py   # 0
$ grep -c 'DENIED'      corpus/evidence/round58/c1-count.py   # 3
$ grep -c 'DENIED'      corpus/evidence/round60/c1-count.py   # 0
$ grep -c 'p\.stdout\|p\.stderr' corpus/evidence/round60/c1-count.py   # 0
```

The seven refusal classes (FOREIGN, SYMLINK_OUT, SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW,
MANY_QUOTES), the reason-class assertions, the outside-`--out` denial check and `ESCAPE_ENTRY` are
all gone; only one boolean over one seeded file remains. "Captured output cannot satisfy a refusal
leg" is true only because **there is no refusal leg left to satisfy** — the specific round-58
token forgery is not measured structurally, it is deleted along with its subject.

### F6 — `--seed` is declared in the predicate and unused

`grep -c 'a\.seed' corpus/evidence/round60/c1-count.py` → **0** (`--seed` is only defined, `:53`). The
fixture (`S601`, one fixed quote, `:27-31`) is constant. Two seeds produce identical output
(`--seed 6001` and `--seed 9999`: same three lines, `C1=FAIL`, exit 1). A declared predicate
parameter that changes nothing is a calibration defect; either it drives fixture ids/offsets (as
round 58's `synth_text` did) or the predicate must stop naming it.

### F7 — smaller design gaps (operability, non-deciding)

- `:35` `before = foreign.read_bytes()` is read then compared via a second read at `:38`; `intact`
  does not exclude a rebuild that rewrites the file with identical bytes (fine) but also does not
  exclude a candidate that writes elsewhere in `out/`, `cache/` or the lane (nothing is snapshotted).
- `:23-26` `work.mkdir(...); cache.mkdir(); out.mkdir()` raise `FileExistsError` on a reused `--work`
  (the predicate says fresh, but the failure mode is a traceback, not a named leg).
- `:15` `import tempfile` unused; `:28` `__import__("hashlib")` avoids the module import.
- `:37` timeout 30 s vs round 58's 60 s default: a slow candidate becomes `state=''` (fail) with no
  distinction between "refuses" and "was killed".
- Verdict labels `CANDIDATE_REFUSAL` and `INJECTION_REJECTED` name behaviours the code never
  measures (there is no refusal observation and no injection observation); the printed vocabulary
  overstates the measurement.

---

## 2. C2 — the counter passes on the tree the predicate says must fail

Frozen requirement (C2): `<lane-copy>` must **fail because no round-60 entry exists**; the counter
must "verify the new entry's exact observation and no overreach against those source bytes, verify its
S101 citation and metadata, and require the scorecard's declared disposition."

### G1 (decisive) — `C2=PASS` on the frozen base tree, which holds no round-60 entry

Base tree materialised read-only from the claim base (`b379919…`), with no `.ufo/` at all, so the
form pin cannot come from the copy:

```
$ git -C "$L" archive b379919 corpus/knowledge/citation-count-semantics-r37.md corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw | tar -x -C "$S/basecopy"
$ python3 corpus/evidence/round60/c2-count.py --root "$S/basecopy" --work "$S/c2base"
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

`ENTRY` is `corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8`), a round-37 file
mtime 2026-10-25 17:35, present at the claim base. Every "entry" assertion (`:17-18`) is a literal
substring already in that file — `source: S101 — https://jc.hit.edu.cn/`, `verified-at:`, `recheck:`,
`#### Unknown`, and the sentence "Whether the specification copy (S101) is the version in force"
(`corpus/knowledge/citation-count-semantics-r37.md:5,74-80`). The `EXPECTED` quote (`:9`) is only
counted as a unique line of the *form* (`:15-16`), never located in, or compared with, any entry
sentence. Before == after: the counter has zero discriminating power for the round's claimed note,
and the frozen "base must fail" arm is not implemented. (Same finding as
`w1/C2CounterAudit.md`, independently reproduced here at the frozen base rather than the live tree.)

### G2 — required checks absent

```
$ grep -ci 'scorecard' c2-count.py   # 0
$ grep -ci 'gate'      c2-count.py   # 0
$ grep -ci 'anchor\|char ' c2-count.py   # 0
$ grep -c 'a\.work'    c2-count.py   # 0
```

The predicate's "require the scorecard's declared disposition" has no code. No Gate/access-date
check, no anchor/`char N` locator for the new note, no overreach scan. `--work` is parsed (`:13`) and
never used, so the predicate's `--work <fresh-absolute-dir>` is decorative and the counter does not
isolate its reads.

### G3 — `--root` is not hermetic (confirmed by the base copy above)

`:7` and `:13` pin `form = ROOT/'.ufo/waves/round-60/s101-open.txt'` where `ROOT` is the script
checkout (`:5`). The base copy contains no `.ufo/` yet prints `FORM_PIN=1/1`, proving the form is
read from the live lane while the entry/raw are read from `--root`. Two authorities in one verdict.

### G4 — the absent-entry state is `ERROR`, not a verdict

```
$ python3 corpus/evidence/round60/c2-count.py --root "$S/noentry" --work "$S/c2noentry"
C2=ERROR FileNotFoundError: ... citation-count-semantics-r37.md
EXIT=2
```

Exit 2 is indistinguishable from an environmental fault. The predicate's before-arm needs a named
`C2=FAIL`, not an exception.

---

## 3. Verdict against the frozen predicates

| Frozen arm | Declared | Measured | Evidence |
|---|---|---|---|
| C1 (a) candidate safe path | reached, independently observed | reached by a no-op printer and by `exit(0)`; no artifact observed | F2 |
| C1 (b) r55 control deletes | proves discrimination | true, but under default `--builder` the control *is* the candidate bytes | F4 |
| C1 (c) injection scored failure | mutant printed `=PASS`, scored fail | mutant scored `candidate_safe`; the `forged_safe` class is unreachable | F1 |
| C1 exit 0 iff (a)∧(b)∧(c) | iff | exits 0 with (c) false | F1,F2 |
| C1 `--seed 6001` | fixture parameter | unused | F6 |
| C2 base fails (no entry) | `C2=FAIL` | `C2=PASS`, exit 0, on the frozen base tree | G1 |
| C2 new-entry observation/overreach | verified | not implemented | G1,G2 |
| C2 scorecard disposition | required | absent | G2 |
| C2 `--work` isolation | fresh dir | ignored | G2 |

**Operability verdict: `harmed`-class, not landed.** The round's target is the round-58 forgeable
aggregate verdict; the replacement still admits a forge (F2), its injection leg is arithmetically
constant (F1), and it certifies the exact behaviour round 58 marks FAIL (F3). No round-60 C1 verdict
should be read as evidence about the builder until the polarity is restored.

---

## 4. Minimal corrections (each with the test that must fail before, pass after)

1. **Make the injection leg measurable.** Score the fixture on `(returncode, foreign-intactness)` with
   the *expected* polarity: hazard fixture → `rc != 0` ∧ intact = refused; `rc == 0` = fail. Then the
   printer (rc 0, prints `=PASS`) fails and the honest refuser (rc 1, intact, named reason) passes —
   the opposite of today (F3). Kill the `forged_safe` branch or give it a distinct, reachable
   predicate; add a self-test asserting `INJECTION_REJECTED` can print `0/1`
   (`--builder` = printer, with the mirror-image expectation).
2. **Require a positive artifact** for the safe path: `spans.tsv` present, `SPANS_ROWS` matching the
   quote row, `spans/S601-1.txt` bytes equal to the 80-char window. A silent `exit(0)` must then
   fail (F2).
3. **Separate the control from the candidate.** Refuse to run (`EXIT=2`) when
   `sha256(--builder) == sha256(R55)` under the default invocation, or pin a control whose bytes
   cannot equal a fixable candidate; today's `BASELINE_DISCRIMINATES` is the candidate's own failure
   (F4).
4. **C2: name the round-60 artifact.** Set `ENTRY` to the round-60 note the claim admits (or require
   a base→target diff of a named path), locate `EXPECTED` in that entry's Gate/observation with the
   `char N` anchor, check its access date, and implement the scorecard-disposition assertion; the
   counter must print `C2=FAIL` (exit 1) on the base tree (G1, G2).
5. **Honor `--root` and `--work`** in both counters (G3, G2), and either use `--seed` to derive
   fixture ids/offsets or drop it from the frozen predicate (F6).
6. If the intent is to repair round-58's verdict derivation rather than replace it with a one-file
   probe, derive the seven hazard legs from structured states (`leg, expected_rc, expected_reason,
   forbidden_touches`) without ever scanning child text — otherwise the frozen "safe and hazard legs"
   clause in the C1 claim is simply not the artifact under test (F5).

---

## 5. Risk and what this seat does not establish

- Not established: whether the C1 claim can be *re-frozen* this round without changing its predicate
  (it cannot, by F1/F3 — the predicate's (a) and (c) are the broken arms; a post-data rule change is
  not the claim's rule). That is an L1/closure decision; this seat records it, it does not rule on it.
- Not established: any builder-hardening verdict. `tools/build-spans.py` is still the round-55 bytes
  (`1ed2650a…`) and still deletes foreign spans (`tools/build-spans.py:201-205`), so a hardened
  candidate does not exist in the lane; C1's "before → after" cannot show a repaired builder this
  round, only a repaired measurement.
- The `--root` non-hermeticity (G3) also means any C2 run against a lane copy is contaminated by live
  lane state; treat all C2 PASS lines produced before a fix as void.
- Freeze digest named in the assignment differs from the file's sha256 (§ Pins). No file changed.

**Hygiene.** Scratch `/fast/scratch/hyaku/chousa-r60/CounterDesignExecutor` used only for fixtures,
lane copies and probes; removed before yield. No writes outside this report, no lane/tracked file
edited, no git/jj mutation, no external fetch, no tool install.
