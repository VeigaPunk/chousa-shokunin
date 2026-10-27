# CounterScribe — round-60 counter operability & depth

Seat: `CounterScribe` (leaf, no spawns). Scope: the frozen claims in
`corpus/evidence/round60-claims.md`, the two round-60 counters under
`corpus/evidence/round60/`, the prior committed C1 evidence
(`corpus/evidence/round58/c1-count.py`, `round58/controls/`), and the current
S101 counter/source. No external live fetch. No writes outside this report;
fixture builders and probes lived in `/fast/scratch/hyaku/chousa-r60/CounterScribe/`
and are removed before yield — their source is quoted inline below so every
finding is re-derivable from this file plus the lane.

Judged axes: **operability** (does the frozen command run, and does its verdict
track the predicate) and **depth** (does a leg observe the thing it names, and
can a cheaper control reach the target).

---

## 0. Verdicts up front

| Claim | Frozen predicate | Measured | Verdict |
|---|---|---|---|
| **C1** operability | `c1-count.py --builder <b> --work <fresh> --seed 6001` prints `C1=PASS` exit 0 **iff** (a) candidate reaches the safe path, (b) pinned r55 proves the unsafe control, (c) the `=PASS`-injection mutant is scored as a failure | The predicate prints `C1=PASS` exit 0 for a builder whose whole body is `sys.exit(0)` (writes nothing, prints nothing). It also does so for the token forger, for an artifact forger, and for a stderr forger. Condition (c) is satisfied by an **unreachable** state string, not by detection | **not met (kill rule hit)** — "any child output injection passes target" is measured true. Do not admit C1 as frozen |
| **C2** depth (S101) | `c2-count.py --root <lane-copy> --work <fresh>` establishes source digests and quote location, verifies the **new** entry's exact observation and no-overreach, requires the scorecard disposition; **base must fail because no round-60 entry exists** | Base (unmodified lane) prints `C2=PASS` exit 0. The three legs it passes are satisfied by bytes committed at round 49; no round-60 entry exists, so the base-fail precondition is unsatisfiable. An appended overreach sentence and garbage metadata both still print `C2=PASS` | **unprovable as frozen** — base passes, so the target cannot be distinguished from a do-nothing round |

Both counters are deterministic (C1: three fresh runs, identical output), so
neither verdict is flakiness.

---

## 1. Freeze integrity — the digest in the assignment does not cover the dispatched bytes

| Fact | Evidence |
|---|---|
| On-disk claims file | `sha256sum corpus/evidence/round60-claims.md` → `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` |
| Digest frozen in the seat prompt, `w1-spec.json`, `w1-dispatch.json` | `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440` |
| Normalizations tried | as-is `65721569…`; trailing-newline stripped `cae804fa…`; CRLF `dbb847b8…`; whitespace-stripped `cae804fa…` — none matches `09d8053f…` |
| History | `git log --all -- corpus/evidence/round60-claims.md` → empty; `git status --porcelain` → `?? corpus/evidence/round60-claims.md`, `?? corpus/evidence/round60/`, `?? .ufo/waves/round-60/` (0 tracked files across all three) |
| mtimes | claims `17:51:18`, c1 counter `17:51:38`, c2 counter `17:52:14`, `w1-spec.json` `17:55:15` — the file predates the dispatch and was not rewritten after it |

Consequences, stated without overreach: the bytes every seat read are the bytes on
disk; the digest the assignment calls immutable names nothing in this checkout, and
no committed blob anchors the claims at all, so a closure cannot re-derive the
frozen text from git until L1 commits it. I did not modify the file and do not
adjudicate which artifact is canonical — L1 owns that reconciliation. Recorded here
because a per-leg counter verdict is only as good as the freeze it is measured
against, and the same mismatch is independently reported by `w1/C2CounterAudit.md`.

---

## 2. C1 — `corpus/evidence/round60/c1-count.py` (sha `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`)

### 2.1 Measured builder matrix

Command shape, run against eight fixture builders plus the lane default
(`noop0` = `print('=PASS'); sys.exit(0)`; `silent0` = `sys.exit(0)`; `stderr_forge`
= `print('=PASS C1=PASS', file=sys.stderr); sys.exit(0)`; `liar_write` = writes a
fake `spans/S601-1.txt` and `spans.tsv` without reading any source; `delete0` =
unlinks `S777-*.txt`, exits 0; `fail0`/`fail2`/`crash` = exit 1 / 2 / raise):

```text
BUILDER        EXIT INJECT     BASELINE   CANDID   C1
noop0          0    1          1          1        PASS
silent0        0    1          1          1        PASS
stderr_forge   0    1          1          1        PASS
liar_write     0    1          1          1        PASS
delete0        1    1          1          0        FAIL
fail0          1    1          1          0        FAIL
fail2          1    1          1          0        FAIL
crash          1    1          1          0        FAIL
lane-default   1    1          1          0        FAIL
```

`INJECTION_REJECTED=1/1` and `BASELINE_DISCRIMINATES=1/1` in all nine runs: both
legs are **constants**, not observations of the candidate.

### 2.2 F1 — a do-nothing control reaches the frozen target

`silent0` writes no file, prints nothing, and exits 0; the counter prints
`C1=PASS` and exits 0. The frozen predicate's condition (a) is "the candidate
reaches the independently observed safe path". The counter never observes the
safe path's artifacts — no `spans.tsv`, no span file, no digest, no offset — so
"reached the safe path" is inferred entirely from the child's own exit code.
That is the same authority transfer the claim set out to remove: `c1-count.py:39-40`
says stdout/stderr are excluded from verdict derivation, but the safe leg's only
positive signal is `p.returncode == 0` (`:41`), which the child controls just as
freely as its output bytes.

### 2.3 F2 — `INJECTION_REJECTED` is satisfied by an unreachable state (dead branch)

`c1-count.py:42-44`:

```python
baseline_bad = p.returncode == 0 and not intact
forged_safe  = p.returncode == 0 and not intact      # identical predicate
return p.returncode, "candidate_safe" if candidate_safe else ("baseline_bad" if baseline_bad else ("forged_safe" if forged_safe else ""))
```

Enumerating the expression over `rc ∈ {0,1,2,-9,124} × intact ∈ {T,F}` yields states
`{'', 'candidate_safe', 'baseline_bad'}` — **`forged_safe` is unreachable**. Therefore
`forge_blocked = forge_state != "forged_safe"` (`:63`) is true for every possible
child. Proof by mutation: replacing the `forged_safe` computation with `False`
changes no leg's meaning (the state machine is identical for all inputs) — the
printed `INJECTION_REJECTED=1/1` cannot fail. The frozen condition (c) ("the
output-injection mutant ... is scored as a failure") is therefore met by text, not
by measurement: the same exact-token forge the claim targets is scored
`candidate_safe` and helps produce `C1=PASS` (row 1 of the matrix).

A second, independent statement of the same hole: the counter's own forge fixture
is `print('=PASS'); print(...); sys.exit(0)` (`:60`) — it touches nothing, so it is
indistinguishable at the observation layer from a correct non-destructive builder.
The forge leg has no observable that the candidate leg lacks.

### 2.4 F3 — the safe-path check regressed from round 58

The round-58 counter verified safe legs against expected artifacts:
header, row count, `capture_sha256`, `offset` and span bytes
(`corpus/evidence/round58/c1-count.py:114-147`, `expect_ok`), plus a
write-outside-`--out` snapshot diff (`:141-146`). The round-60 counter replaces all
of that with `rc == 0 and intact` (`:41`). The round-60 file is not a hardening of
the safe leg; it is a removal of it. Empirically: the round-58 counter does **not**
emit `C1=PASS` for `silent0` — it dies at `round58/c1-count.py:211-212` trying to
seed the foreign file into an `out/spans` the no-op never created (exit 1, no
`C1=` line). So the before-state failed loudly and the after-state passes: that is
a regression in the direction of the axis, not progress on it. (The before-state's
crash is itself a defect — a counter may not die on a legal-but-empty builder — but
it is a *different* defect and does not convert into a false PASS.)

### 2.5 F4 — the baseline leg is a repository constant, not a discriminator

`base_state = run(R55, …)` (`:66`) always executes
`corpus/evidence/round58/controls/build-spans-r55.py`; `R55` is fixed at
`:18-19` and takes no digest pin (round 58 pinned `R55_BUILDER_SHA` at
`round58/c1-count.py:38`; round 60 dropped the pin). Because the leg's input never
varies with `--builder`, `BASELINE_DISCRIMINATES=1/1` is a statement about the
checkout, not about the candidate — it stays 1 for every builder in the matrix,
including `crash`. The word "discriminates" is not calibrated to anything the leg
varies. Also note `baseline_bad` requires `rc == 0 and not intact` (`:42`): the
frozen requirement is only "deletes the foreign file", so a destructive builder
that legitimately refuses (`rc != 0` after deleting) would be scored as *not*
baseline_bad and force `C1=FAIL` — an unstated coupling between the negative
control's exit code and the aggregate verdict.

### 2.6 F5 — the lane's own default builder is byte-identical to the negative control

```text
1ed2650a… tools/build-spans.py
1ed2650a… corpus/evidence/round58/controls/build-spans-r55.py
```

With no `--builder`, `a.builder` defaults to `ROOT/"tools/build-spans.py"`
(`:51`) — the same bytes the counter runs as its unsafe control. The frozen
command therefore cannot reach `C1=PASS` on the lane's own implementation
(`lane-default` row: `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`, exit 1); the behaviours
differ only in `work` dir, so the two legs are contradictory by construction. The
predicate writes `<builder>` as a placeholder and the lane holds no builder that
preserves foreign files, so the claim's after-state is currently uninstantiable
without writing a new builder this round.

### 2.7 F6 — operability: error path collides with `FAIL`, and `--work` is not reusable

| Probe | Result |
|---|---|
| Re-run with same `--work` | `FileExistsError` at `:25` (`cache.mkdir()`), traceback, **exit 1**, no leg lines |
| `--builder` pointing at a missing file | leg lines print `CANDIDATE_REFUSAL=0/1 C1=FAIL`, **exit 1** (the missing script's rc=2 + intact file yields the empty state) |
| Exit-code taxonomy | `0`=PASS, `1`=FAIL, and `1`=counter crashed — a harness cannot distinguish "the counter says FAIL" from "the counter broke". The sibling counter uses `2` for ERROR (`c2-count.py:22`), so the convention already exists in this round. |
| `--seed 6001` | parsed (`:53`) and never read; no RNG anywhere in the file. Round 58 used `random.Random(seed)` for fixture synthesis (`round58/c1-count.py:77-79,183`). The frozen predicate's `--seed` is decorative, so the fixture is fixed and the "fresh dir" requirement is the only variability. |
| `--work` cleanup | `finally` (`:76-79`) removes only the env-default base; with an explicit `--work` it leaves the seeded fixture (including `forged.py`) behind. Reports as scratch, not lane pollution. |

### 2.8 F7 — `ROOT` from `__file__` makes the counter immovable

`ROOT = pathlib.Path(__file__).resolve().parents[3]` (`:17`), and both control
inputs (`BASE`, `R55`) derive from it (`:18-19`). Copying the counter anywhere else
silently loses the negative control:

```text
$ cp corpus/evidence/round60/c1-count.py /fast/scratch/…/c1-relocated.py
$ python3 c1-relocated.py --builder …/builders/noop0.py --work … --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=0/1      # python3 could not open the vanished R55 path
CANDIDATE_REFUSAL=1/1
C1=FAIL
EXIT=1
```

It fails closed (good), but the leg is not reported as missing, just scored 0, so a
reviewer reading `BASELINE_DISCRIMINATES=0/1` cannot tell "the control did not
discriminate" from "the control was not found". The mutation test in §2.3 hit this
first and it reads exactly like a verdict. Any counter the closure may re-run on a
fresh clone or a lane copy needs `--base`/`--r55` parameters (or a digest-pinned
absolute path, as round 58 did).

### 2.9 What C1's fix therefore needs (smallest safe change, not applied — seat has no write scope)

1. `candidate_safe` must be an artifact observation: `spans.tsv` exists, exactly one
   row `S601`, `capture_sha256 == sha256(cache/<key>.txt)`, `offset == 0`, and
   `spans/S601-1.txt` contains the quote plus the surrounding bytes — i.e. port
   round-58 `expect_ok` back in, then take the foreign-file observation as an
   additional conjunct.
2. Replace the dead branch with a **positive** forbidden classification:
   `state = "no_artifact"` when `rc == 0` and no valid `spans.tsv`; `INJECTION_REJECTED`
   = that state was produced for the `=PASS` mutant. Then the score can be 0.
3. Decouple `baseline_bad` from `rc == 0` (require deletion; record rc separately).
4. Pin `R55` by digest; parameterize `BASE`/`R55`; return `2` on a counter error;
   make `run()` idempotent (`exist_ok=True`) or document one-shot `--work`.

---

## 3. C2 — `corpus/evidence/round60/c2-count.py` (sha `a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe`)

### 3.1 Base passes (measured, deterministic)

```text
$ python3 corpus/evidence/round60/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work …/c2-base
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

The frozen predicate says "Base must fail because no round-60 entry exists". The
base is the unmodified lane; it passes. Mechanism, line by line:

| Leg | Line | What it actually reads |
|---|---|---|
| `METADATA=1/1` | `:17` | `body.startswith('\n# ')`, one `source: S101 — https://jc.hit.edu.cn/` substring, and the *presence* of `verified-at:` / `recheck:` anywhere |
| `LIMIT=1/1` | `:18` | `'#### Unknown'` and `'Whether the specification copy (S101) is the version in force'` in the body |
| `QUOTE=1/1`, `LINE=245` | `:15,19` | `EXPECTED` occurs once in the pinned form; `LINE` is printed but never compared to any expected value |

Those substrings are pre-existing committed content:
`corpus/knowledge/citation-count-semantics-r37.md` sha `bb80627b…` (working copy ==
`master` blob, 6806 bytes), `git blame` puts `#### Unknown` at line 74 and
`Whether the specification copy (S101) is the version in force` at line 79 in
round-49 commit `1254ab2`. `ENTRY` (`:8`) points at that r37 entry, not at any
round-60 note; the counter has **no concept of a round-60 entry**, so "base fails
because no round-60 entry exists" is not expressible and the base cannot fail for
the stated reason. This is the §9 shape the fleet already ruled out: re-scoring on
inputs the lane already holds is not new ground, and a target the do-nothing state
already reaches is not a target.

### 3.2 `LIMIT` does not test no-overreach — an overreaching entry still passes

Mutation, in scratch: copy the lane's entry into a scratch root and append

```text
- Overreach probe: CNKI implements this type/carrier notation today and every
  present-day index counts by it. No source in this lane states that.
```

```text
$ python3 c2-count.py --root …/c2-root --work …/c2-tampered
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

The claim requires verifying "the new entry's exact observation and no overreach
against those source bytes". Nothing inspects the entry's observation text (it is
never split out of the body), nothing compares it to the located quote, and there
is no forbidden-claim check, so the leg the claim names is not the leg the counter
runs. `LIMIT` is a positive substring test: it can only confirm a sentence the
entry already had.

### 3.3 `METADATA` accepts garbage — and round-58's pin discipline is gone

```text
$ sed -e 's/^verified-at: 2026-10-25$/verified-at: banana/' -e 's/^recheck: 180d$/recheck: whenever/' …
$ python3 c2-count.py --root …/c2-root2 --work …
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
```

`verified-at` / `recheck` are matched as bare keys, so no ISO date, `NNd` cadence
or symbolic cadence is validated even though CORPUS.md requires one. Contrast
round 58, which pinned the tool it depends on
(`CAPTURE_TEXT_SHA = "2c0140bc…"` at `round58/c1-count.py:39`); the S101 counter
pins digests of data (`:10-11`) but not the tool that renders the form.

### 3.4 The pinned form IS derivable from the committed raw — the fix is a one-line check

Everything needed for a derivation leg already exists and agrees:

```text
$ python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw | sha256sum
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
$ sha256sum .ufo/waves/round-60/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
$ sha256sum corpus/evidence/round59/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
$ python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw --locate 'c. 文献类型及载体类型标志；'
LOCATED count=1 offset=12960          # form line 245
$ sha256sum tools/capture-text.py
2c0140bc…                             # unchanged since the round-58 pin
```

So the form is byte-identical to the committed round-59 rendering **and** to a
fresh derivation from the committed raw. `FORM_PIN` currently proves only that some
writer produced `a8e3e7ad…`; because the counter does not re-derive it, a writer
could substitute an arbitrary form and still pass as long as the bytes hash to the
pin. Two cheap repairs: (i) compare `hashlib.sha256(subprocess capture-text(raw))`
with `FORM_SHA` instead of trusting the file, and (ii) point `FORM` at the
committed `corpus/evidence/round59/s101-open.txt` rather than an untracked
`.ufo/waves/round-60/` copy, which nothing commits until L1 lands the round.

### 3.5 `--root` is mixed authority: the form is always read from the live lane

`:13` computes `raw` and `entry` from `root`, but `form = ROOT/'.ufo/waves/round-60/s101-open.txt'`
with `ROOT` from `:5`. Witness: a scratch root carrying a **poisoned** local form
(`POISONED LOCAL FORM` + the quote, sha `fc46fbbb…`) still scores `FORM_PIN=1/1`:

```text
$ python3 c2-count.py --root …/c2-root --work …
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
```

A digest match cannot repair the authority mix: the leg named "verify against those
source bytes" is reading bytes from outside the `<lane-copy>` the predicate
names. (`--root` on an empty tree fails cleanly with `C2=ERROR … exit 2`, so the
error taxonomy is sound; the defect is silent mixing, not crashes.)

### 3.6 `--work` is inert

`a.work` is parsed (`:13`) and never used; the counter allocates no scratch and
writes nothing. Harmless, but the frozen predicate's `--work <fresh-absolute-dir>`
simulates isolation it does not have.

### 3.7 What C2's fix therefore needs

1. `ENTRY` must name the round-60 artifact itself and prove it is new (file absent
   at the frozen base commit, or a required marker), with the base run asserted
   nonzero before any target PASS.
2. A negative leg: a banned-phrase list (present-day validity, CNKI implementation,
   "in force") that a tampered entry must trip — the mutation in §3.2 becomes the
   regression control.
3. Validate `verified-at` against ISO/`NNd`/symbolic cadence; validate the
   `source:` URL against the registry row, not a substring.
4. `FORM`: derive from `raw` with the pinned `tools/capture-text.py` and compare
   digests; derive the path from `--root`; prefer the committed round-59 form.
5. Drop `LINE` from the leg list or compare it to a frozen expected line.

---

## 4. Reproduction commands (all read-only against the lane)

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
S=/fast/scratch/hyaku/chousa-r60/CounterScribe
sha256sum "$L/corpus/evidence/round60-claims.md"                     # 65721569…
python3 "$L/corpus/evidence/round60/c1-count.py" --work "$S/a" --seed 6001
python3 "$L/corpus/evidence/round60/c2-count.py" --root "$L" --work "$S/b"
printf 'import sys\nsys.exit(0)\n' > "$S/silent0.py"
python3 "$L/corpus/evidence/round60/c1-count.py" --builder "$S/silent0.py" --work "$S/c" --seed 6001
python3 "$L/tools/capture-text.py" "$L/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw" | sha256sum
sha256sum "$L/tools/build-spans.py" "$L/corpus/evidence/round58/controls/build-spans-r55.py"
git -C "$L" blame -L 74,80 master -- corpus/knowledge/citation-count-semantics-r37.md
```

## 5. Falsifiers — what would refute this report

- **F1/C1**: a builder that writes nothing but still yields `C1=FAIL`. None of the
  three I ran does (`silent0`, `noop0`, `stderr_forge` all `C1=PASS`); a reviewer
  re-running §2.1 with any `--builder` that exits 0 and leaves `S777-1.txt` alone
  refutes it only by showing a non-PASS result.
- **F2**: a `--builder` that makes `INJECTION_REJECTED=0/1`. The dead branch
  predicts none exists; a single counterexample kills the finding.
- **F3**: a safe-leg artifact check inside `c1-count.py` — there is none
  (`grep -n 'spans.tsv' corpus/evidence/round60/c1-count.py` is empty).
- **C2/G1**: a base run that fails. My run passes; if a reviewer's base run fails,
  the root or the tree differs and that difference is itself the finding.
- **C2/G2**: an appended overreach sentence that makes `C2=FAIL`.

## 6. Bounds and hygiene

- Writes: this file only. Nothing edited in `corpus/evidence/round60-claims.md`,
  the counters, `tools/`, the fleet repo, or any sibling lane. No git/jj mutation,
  no commits, no pushes, no external fetch, no installs.
- Scratch `/fast/scratch/hyaku/chousa-r60/CounterScribe/` used for the eight fixture
  builders, the two C2 tamper roots, the relocated counter copy and the mutation
  copy; removed before yield (their content is quoted above).
- Not adjudicated here: which artifact is the canonical frozen claims text (§1 —
  L1 owns that), and whether C1/C2 land at all (the claim's closure does).
