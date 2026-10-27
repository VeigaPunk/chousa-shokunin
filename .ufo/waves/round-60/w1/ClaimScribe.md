# ClaimScribe — round-60 frozen-claim operability and depth analysis

**Seat.** ClaimScribe (leaf scribe, lane `chousa`, round 60, wave w1). **Judged on:** operability, depth.
**Scope.** Bounded analysis of the two frozen claims in
`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round60-claims.md`, against prior
committed evidence and the *current* round-60 counters/source only. No external/live fetch, no lane
edit (this file is my only write), no commit, no git/jj mutation, no subagents.

**Scratch.** `/fast/scratch/hyaku/chousa-r60/ClaimScribe/` (created, used, removed before yield; every
receipt below is pasted inline so nothing depends on scratch surviving).

---

## 1. Inputs and pins (measured this seat)

| Artifact | Observed | Status |
|---|---|---|
| `corpus/evidence/round60-claims.md` | `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`, 3355 bytes | **untracked** (`git ls-files` empty) |
| assignment's "exact immutable claim SHA" | `09d8053f…a440` | **does not match** any byte form I could construct (§5) |
| claim base `b379919a873e7080a31ef92c7002f55f5374e2c6` | present, `round-59 verifier spot-check` | committed |
| `corpus/evidence/round60/c1-count.py` | tracked: no | untracked |
| `corpus/evidence/round60/c2-count.py` | tracked: no | untracked |
| `corpus/evidence/round58/claims.md` (contrast) | tracked: yes | committed |
| `tools/build-spans.py` vs `corpus/evidence/round58/controls/build-spans-r55.py` | both `1ed2650a…` | byte-identical |
| `.ufo/waves/round-60/s101-open.txt` vs `corpus/evidence/round59/s101-open.txt` | both `a8e3e7ad…`, `cmp` IDENTICAL | wave copy untracked, corpus copy committed |

Round-60-era counts that frame everything below: the frozen package lands **two** claims (`C1`
operability, `C2` depth), on disjoint files, so **causal separability holds** — each is runnable
without the other. Both, however, are counters first; the claims' truth depends on whether those
counters can fail for the right reason. They largely cannot.

---

## 2. C1 — the round-60 counter cannot fail for the reason the claim names

Frozen predicate (claims file, C1): the counter "must print `C1=PASS` and exit 0 **iff** (a) the
candidate reaches the independently observed safe path without deleting the foreign file, (b) the
pinned r55 builder provides the known unsafe control by deleting it, and (c) the output-injection
mutant prints `=PASS` but is scored as a failure."

### 2.1 A do-nothing candidate reaches `C1=PASS`, exit 0 — observed

```sh
$ printf 'import sys\nsys.exit(0)\n' > <scratch>/noop.py
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 -B corpus/evidence/round60/c1-count.py --builder <scratch>/noop.py \
      --work <fresh-abs-dir>/p2 --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

The base candidate, for contrast (`--builder tools/build-spans.py`, same counter):

```text
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

Cause: `run()` derives its whole state from two facts only — `p.returncode == 0` and
`foreign` still hashing to `b"preserve-me\n"` (`c1-count.py:38-44`). Nothing checks that the candidate
produced a span, read the seeded cache entry, or emitted anything. A three-byte script that does
nothing is therefore `candidate_safe` (`:41`) and is accepted. This is exactly the §9 sizing test —
"a target must be one a do-nothing control cannot reach" — failing: **the do-nothing control reaches
the target.** The printed label `CANDIDATE_REFUSAL` (`:73`) also misnames it: the claim's leg (a) is
about *reaching the safe path*, the code tests *exiting 0 and not deleting*.

### 2.2 `INJECTION_REJECTED` is a tautology — it is 1 for every possible run

The injected artifact is authored by the counter itself (`:60`):
`print('=PASS'); print('all seven hazards accepted'); sys.exit(0)` — it never touches the seeded
foreign file. So `intact` is always `True`, the state is always `candidate_safe`, and
`forged_safe = p.returncode == 0 and not intact` (`:43`) is **unreachable**. `forge_blocked =
forge_state != "forged_safe"` (`:63`) is therefore the constant `1`, printed as
`INJECTION_REJECTED=1/1` (`:71`). Note also that `:42` and `:43` are the *same expression*, so the
state enum has a dead branch and the baseline/forge distinction is only which subject was run.

Empirically constant across five different candidates (base-destructive, no-op, nonexistent,
token-only, token+delete): `INJECTION_REJECTED=1/1` in all five. The leg cannot report failure, so it
carries no measurement.

Worse for the claim text: leg (c) says the mutant is "scored as a failure", but the code scores it
`candidate_safe` and reports it as *rejected*. Plan sentence, code condition and receipt label are
three different things — the §9 rule ("the same sentence in the plan, the same condition in the
counter's code and the same label in the receipt") is broken. And the scenario the claim promises to
reject does not exist in the counter: a builder that **fails and prints `=PASS`** is never constructed;
the stub prints `=PASS` and *passes* (the no-op path). Measured:

```text
# <scratch>/token-only.py: print("=PASS"); exit(0); touches nothing
C1=PASS  exit=0          # token output is irrelevant — good — but so is the token test
# <scratch>/token-plus-delete.py: print("=PASS"); unlink out/spans/S777-1.txt; exit(0)
CANDIDATE_REFUSAL=0/1
C1=FAIL  exit=1          # the only discriminating condition is file state, not injection
```

### 2.3 The claim's "safe and hazard legs" do not exist in the counter

The C1 predicate sentence requires the counter to exit 0 "only when the frozen safe and hazard legs
meet their declared requirements", and the claim's headline promises "per-leg structured states".
The round-60 counter implements **one scenario and three aggregate booleans** — there is no per-leg
state table, and the round-58 battery is gone:

```sh
$ grep -cE 'SYMLINK|FIFO|DEVZERO|MANY_QUOTES|FAT_RAW|ESCAPE_ENTRY|HELDOUT' \
    corpus/evidence/round58/c1-count.py corpus/evidence/round60/c1-count.py
r58=31   r60=0
```

`R59Executor09.md` §1 (committed wave evidence) records the round-58 battery as 4 safe legs
(`EMPTY_OK`, `REBUILD_OK`, `HELDOUT_OK`, `ESCAPE_ENTRY`) plus 7 hazard legs (`FOREIGN`, `SYMLINK_OUT`,
`SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`, `MANY_QUOTES`). Round 60 scores 11 legs → 1
scenario. So "a failing leg cannot produce the exact PASS predicate by output injection" is true
**vacuously**: the hazard legs whose output could be forged are no longer run. The claim disclaims
that "the builder itself meets all hazard legs" — that is honest — but the counter also stops
*measuring* the hazard legs, and the predicate sentence claims otherwise.

### 2.4 What is genuinely improved (credit where due)

The round-58 forgery class was a **candidate-controlled substring scan**: refusal reason strings
interpolated the candidate's own stderr and `ref_pass` scanned them for `=PASS`
(`R59Executor09.md` §6, committed). The round-60 counter removes that class structurally: child
output is captured (`:37`) and then **never read** — `grep -n 'p\.stdout|p\.stderr'` finds nothing; only
`p.returncode` and filesystem state reach the verdict (`:38-44`). Output injection into the verdict path
is impossible by construction. That is a real, narrow improvement, and it is the reason the claim's
"output bytes cannot establish a leg state" is satisfied.

### 2.5 Operability defects (bounded probe)

- **Not re-runnable in the same `--work`:** `cache.mkdir()` / `out.mkdir()` (`:25-26`, no
  `exist_ok`) → `FileExistsError`, traceback, exit 1 and **no `C1=` line**:
  ```text
  FileExistsError: [Errno 17] File exists: '<work>/p2/forge/cache'
  rc=1
  ```
  The frozen predicate says "fresh-absolute-dir", but the default work root is a *fixed* path
  (`:55`, `<HYAKU_SCRATCH>/chousa-r60/c1-count`), so two concurrent default runs collide and neither
  gets a verdict.
- **`--seed` is declared and never used** (`:53`; no other `seed` reference). The predicate's
  `--seed 6001` is decorative.
- **A missing/syntax-broken candidate is reported as `CANDIDATE_REFUSAL=0/1`, not as an error:**
  `python3 -B <missing>` exits 2, so the counter prints a clean `C1=FAIL` and hides the cause (the
  builder is passed to the interpreter, not exec'd directly).
- **`capture_output=True` is retained in memory and discarded**, although the module docstring says
  child output is "captured only for diagnosis". There is no diagnostic path.
- **`BASELINE_DISCRIMINATES` is candidate-independent:** it depends only on the committed r55 control
  being destructive (`:67`). Given the committed repo it is a constant 1. So of the three printed
  legs, **two are constants and the third is satisfied by a no-op** — the receipt's shape
  (`3× /1`) overstates the measurement.

### 2.6 C1 verdict

**Operability: not admissible as written.** The predicate is satisfiable without the work the claim
describes (do-nothing candidate → PASS), one leg is a tautology, one is a repo constant, and the
predicate's own labels diverge from its code. `c1-before.txt` is internally consistent with the
counter (base candidate is destructive → `CANDIDATE_REFUSAL=0/1`), so this is not a broken receipt;
it is a counter whose positive path is too weak to be evidence. **Depth: harmed by the change itself**
— hazard coverage drops from 11 legs to 1 scenario on the same surface. Report as an honest stop for
C1 unless the counter is fixed and re-measured; do not read the base `C1=FAIL` as a builder verdict.

---

## 3. C2 — the counter passes at base and cannot be re-derived from committed bytes

### 3.1 Base passes (frozen predicate says it must fail) — independently reproduced

```sh
$ python3 -B corpus/evidence/round60/c2-count.py \
    --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work <fresh-abs-dir>/c2
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

The frozen predicate's "Base must fail because no round-60 entry exists" is contradicted: the counter
reads `corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8,13`), a pre-existing entry, and
its `metadata`/`scoped` conditions (`:17-18`) are literal substrings that already hold. This duplicates
sibling `C2CounterAudit.md` (independent agreement, not a second piece of evidence); my run is only
to confirm it on current bytes rather than cite it.

### 3.2 `--root` does not isolate the pinned form — observed on a real foreign tree

`FORM` is bound to script-global `ROOT/'.ufo/waves/round-60/s101-open.txt'` (`:7`), while `raw` and
`entry` use `--root` (`:13`). Extracted the committed claim base to scratch
(`git archive b379919a | tar -x -C <scratch>/committed-tree`) and ran:

```text
# committed tree contains neither corpus/evidence/round60/ nor .ufo/waves/round-60/s101-open.txt
$ python3 -B corpus/evidence/round60/c2-count.py --root <scratch>/committed-tree --work <…>/p7a
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

It passes by silently reading the *live lane's uncommitted* form. Relocating the counter into that
tree (so `ROOT` is the tree) exposes the dependency:

```text
$ python3 -B <scratch>/committed-tree/corpus/evidence/round60/c2-count.py \
      --root <scratch>/committed-tree --work <…>/p7b
C2=ERROR FileNotFoundError: [Errno 2] No such file or directory:
  '<scratch>/committed-tree/.ufo/waves/round-60/s101-open.txt'
```

So the frozen predicate ("establish source digest and quote locations from **committed** S101 raw
capture using the pinned capture-text form") fails the §9 re-derivation requirement: the round's own
verdict cannot be reproduced from committed bytes. **A one-line fix already exists and is unused** —
`corpus/evidence/round59/s101-open.txt` is committed and byte-identical (`a8e3e7ad…`, `cmp` clean).

### 3.3 What the counter actually verifies vs what the predicate claims

| Predicate clause | Implementation | Gap |
|---|---|---|
| "establish source digest" | raw SHA pinned (`:10`) and compared (`:16`) | holds |
| "and quote locations from committed S101 raw capture" | `EXPECTED` located in the **derived form** (`:15`), `LINE=245` is a form line | the raw capture is never decoded or searched; "location in raw" unproven |
| "verify the new entry's exact observation" | `metadata` = 4 substring tests on the *old* r37 entry (`:17`) | no new entry, no observation comparison |
| "and no overreach against those source bytes" | `scoped` = 2 literal substrings (`:18`) | an overreaching note that contains those two literals **passes**; entailment is untested |
| "require the scorecard's declared disposition" | absent | no SCORECARD read anywhere in the file |
| "base must fail" | contradicted (§3.1) | — |

The counter is a pins-and-literals gate. That is defensible as a *pin* check and is exactly why it
passes at base; it is not the observation/overreach gate the claim promises. `--work` is also
accepted and never used (`:13`), so the "fresh-absolute-dir" in the predicate is inert.

### 3.4 C2 verdict

**Operability: fails the frozen predicate's own base-fail and committed-bytes requirements** (both
measured above). **Depth: unprovable** — the check that would separate a scoped observation from
overreach does not exist, and the entry it inspects predates the round, so a `C2=PASS` would credit
this round with knowledge it did not land. Honest stop for C2 as written.

---

## 4. Freeze integrity (affects both claims)

The assignment's immutable claim SHA `09d8053f…a440` does not match the file: observed
`65721569…018d1` (3355 bytes, starts `# `, ends `.\n`). I tested ten byte forms — raw, CRLF, LF-from-CRLF,
trailing-newline stripped, extra newline, UTF-16LE with and without BOM, `sha256("blob <len>\0"+bytes)`,
sha256-of-digest, and lines-joined-without-final-newline — **none match**:

```text
raw                 65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
crlf                dbb847b81e834ecff97ca54bc2fe149a1fcdd2f8d2aa90aa50ac4c079778ba54
stripped_trailing_nl cae804faeb016bf18d8183355e3885b7269e3fbce0a70d790cd688e5bb7175be
plus_nl             ed2999d04baa057a20d57614d3d29f2497a8eabbbd30601b48af2bdbe8154a7c
utf16le             64ad4183b90a720ba4d629871d326734a9b3378a8373e95b8830e9e02f473cca
utf16le_bom         33f089e18fdce7204f2e3ac63023848694563a673dd3b56affbb2dc209a057f7
git_blob_sha256     d27121a5e34e36d888e85378836e371510e4390745155ccf6a4300a05d967f55
sha256_hex_of_sha256 9da259130d62c2f3c1098b86d27133a5a8f414c8fa71ff6abb42f13741b6a4ca
```

(sha1 git blob is `5ea0acf0…`, also not the target.) The artifact is also **untracked**, while the
round-58 freeze it replaces is committed — so as things stand the freeze has neither a matching
declared digest nor a committed identity. Round 59's routed defect ("pre-dispatch claims freeze is
missing; require a nonempty frozen artifact **plus revision binding** before ready") recurs in the
weaker form: artifact present, binding absent. Siblings `S101Reopen.md` and `C2CounterAudit.md`
observed the same mismatch independently; I did not touch the file.

**This does not in itself falsify either claim** — the formulas and thresholds I analysed are the
ones in that file, and changing bytes would invalidate them. It does mean no closure can verify the
frozen package against the assignment's stated digest as-is, and the mismatch must be reconciled
before any landed commit cites "frozen at" a hash.

---

## 5. Cross-claim findings

1. **Both counters fail the do-nothing / base-fail control the same way**: C1 accepts work that was
   not done (no-op → PASS); C2 accepts state that predates the round (base → PASS). The two claims
   are *causally separable* but share one defect class: verdicts derived from presence/pins rather
   than from the property named in the claim sentence.
2. **Both depend on self-authored or uncommitted inputs** (C1's `forged.py` written by the counter,
   C2's form read from `.ufo/waves/`), so neither can be re-derived by a non-author from committed
   bytes alone — the closure requirement in §9.
3. **The narrow improvement both can defend** is negative-space: C1 provably cannot read child output
   into its verdict; C2 provably pins raw-capture digest. Neither is enough for admission.

---

## 6. Smallest safe corrections (bounded, each independently checkable)

**C1**
1. Require an artifact from the candidate: after the run, assert `out/spans/` contains the `S601` row
   derived from the seeded `quotes.tsv`/cache. This alone makes the no-op control fail.
2. Replace the self-authored forge with a **candidate** that fails a leg and prints `=PASS` on both
   streams; derive the leg from typed state (`(returncode, preserved: bool, artifact: bool)`), never
   from text. Then `INJECTION_REJECTED` can actually be 0.
3. Emit one line per scored property with its own predicate (`CANDIDATE_ARTIFACT=`, `CANDIDATE_PRESERVES=`,
   `BASELINE_DESTROYS=`), and make the exit status depend on the conjunction of the printed lines, so
   the receipt cannot print `1/1` for a constant.
4. Wrap `run()` so any exception prints `C1=ERROR <Type>: <path>` and exits non-zero with a `C1=` line;
   create the work tree uniquely (`tempfile.mkdtemp(dir=…)`) or clear it before use; delete or
   implement `--seed`; print child output on failure or drop `capture_output`.

**C2**
1. Point `FORM` at `root/'corpus/evidence/round59/s101-open.txt'` (committed, byte-identical) —
   restores committed-bytes re-derivation with no digest change.
2. Point `ENTRY` at a round-60-specific path that **must not exist at base**, and require a nonzero
   exit on the unmodified tree before any PASS is accepted.
3. Replace the two literals with a check that the note's quoted span appears in the located raw/form
   text and that its prose introduces no claim beyond that span (a prohibited-phrase list tied to the
   already-named unknowns: "in force", "CNKI", "current", "still valid").
4. Read SCORECARD for the declared disposition, as the predicate requires; use or drop `--work`.

**Freeze**
5. Commit the claims artifact (or a digest line inside a committed file) and reconcile
   `09d8053f…`; a round that cites an uncommitted freeze repeats the round-59 routed defect.

---

## 7. Limits of this seat

- I did not adjudicate QUALITY admission, did not judge either entry's wording, and did not run the
  round-58 counter battery (frozen bytes stay untouched; `R59Executor09.md` is cited, not re-run).
- The do-nothing probe is a *counter* control, not a builder verdict. Whether `tools/build-spans.py`
  is repairable, and whether C1 should be re-frozen on a broader predicate, is the L1's call.
- No network, no lane file writes besides this report, no git/jj, no subagents. Scratch removed;
  all receipts are inline above.
