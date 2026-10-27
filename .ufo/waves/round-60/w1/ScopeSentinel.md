# ScopeSentinel — round-60 frozen-claim scope boundary sweep

**Seat.** ScopeSentinel (leaf sentinel, no dispatch). **Bounded surface:** the frozen claims at
`corpus/evidence/round60-claims.md`, prior committed evidence, and the current round-60 counters/sources
as they exist on disk. No external fetch, no writes outside this report, no commits or git/jj
mutations. **Read-only. Every probe ran under `/fast/scratch/hyaku/chousa-r60/ScopeSentinel` (removed
before yield); lane tree untouched (receipt R15).**

## Verdict

Neither frozen claim's declared measurement scope is the scope its counter measures.

- **C1** declares per-leg structured states over the frozen safe and hazard legs; its counter has **3
  aggregate booleans and 0 hazard legs** (r58: 11 legs, 7 of them hazard legs — receipt R11). Of the 3,
  **two are invariant to the `--builder` argument** (one provably constant, one a fixed-artifact test),
  and the third is satisfied by a builder that writes nothing. The frozen target `C1=PASS` is therefore
  reached without any safe-path behaviour, while the only in-tree candidate (byte-identical to the
  "unsafe" baseline control) **fails** it.
- **C2** declares verification of "the new entry's exact observation and no overreach", a scorecard
  disposition, and "base must fail because no round-60 entry exists"; its counter points `ENTRY` at the
  **pre-existing** `citation-count-semantics-r37.md`, never reads SCORECARD, and **prints `C2=PASS` on
  the untouched claim base**. The claim's after-state already exists before the round begins.
- Consequently both claims fail the round contract's §9 do-nothing-control rule *as frozen*, and neither
  can be admitted on these predicates. This is a **pre-landing** scope defect: the counters, not the
  claims' prose, are what a closure would score.
- **Freeze provenance is unverifiable:** the claims file is untracked and its measured digest
  `65721569…` does not equal the digest declared in the dispatch (`09d8053f…`) under five normalizations
  tested (R2). Nothing in the tree witnesses what bytes the freeze was taken over.

No live `resume_continuity_v1` implementation or canonical run logic exists in this lane's `tools/` or
`corpus/` (R17); that sentinel duty has no testable surface here, and it is not asserted.

## Pins (all measured this seat)

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin
state branch=master local=b379919a873e7080a31ef92c7002f55f5374e2c6 remote=b379919a873e7080a31ef92c7002f55f5374e2c6 ahead=0 behind=0 head=detached tracked=0 untracked=3
```

```
$ sha256sum corpus/evidence/round60/c1-count.py corpus/evidence/round60/c2-count.py \
            corpus/evidence/round60-claims.md .ufo/waves/round-60/s101-open.txt \
            corpus/knowledge/citation-count-semantics-r37.md corpus/evidence/round58/c1-count.py
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe  corpus/evidence/round60/c2-count.py
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
bb80627b15a709b50fcdca78b668b912386ab3b27260e7367ffd5a8a99c203cb  corpus/knowledge/citation-count-semantics-r37.md
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py
```

Claim base `b379919a` is the current lane tip (ahead=0), so both counters are being read against the
tree the claims name. `c1-count.py` mtime 17:51, `c2-count.py` mtime 17:52, dispatch `w1.ready` 17:55:
these bytes predate dispatch and are the ones scored below.

## C1 — declared scope vs measured scope

Claim: `corpus/evidence/round60-claims.md:7`; predicate: `:9`; before→after/kill rule: `:11`.

| Claim/predicate clause | What the counter actually does | Status |
|---|---|---|
| "per-leg structured states" (`:7`) | Prints 3 aggregate `N/1` counters (`c1-count.py:71-73`); no per-leg typed record, no reason enum, no leg identity beyond the label | **not implemented** |
| "captured builder stdout/stderr cannot satisfy a refusal leg" (`:7`) | There is **no refusal leg**; `stdout`/`stderr` are captured and never read (`:37`), so the property holds by omission | **vacuous** |
| "a failing leg cannot produce the exact PASS predicate by output injection" (`:7`) | No failing leg exists to inject into; the "injection mutant" is a 3-line script that prints `=PASS` and exits (`:60`), classified `candidate_safe` (`:41-44`) | **not measured** |
| (a) "candidate reaches the independently observed safe path without deleting the foreign file" (`:9`) | `candidate_safe = returncode == 0 and foreign intact` (`:41`) — no span artifact is produced or checked | **narrower: no-op satisfies** |
| (b) "the pinned r55 builder provides the known unsafe control" (`:9`) | `R55` is a **path** (`:19`); no digest pin (R10: `c1_builder_sha_pin=0`). `tools/build-spans.py` is byte-identical to that control (`1ed2650a…`) | **unpinned; candidate == baseline** |
| (c) "the output-injection mutant prints `=PASS` but is scored as a failure" (`:9`) | `forged_safe` is unreachable (`:43` duplicates `:42` and sits later in the `elif` chain); `forge_blocked = state != "forged_safe"` is **always true** | **constant-true leg** |
| "exits 0 only when the frozen safe and hazard legs meet their declared requirements" (`:7`) | Exit is `passed = forge_blocked and baseline_discriminates and candidate_ok` (`:70`); two terms are candidate-invariant, the third is the no-artifact test above | **not the declared condition** |
| `--seed 6001` is part of the frozen command (`:9`) | `--seed` is parsed (`:53`) and never read (R10: `c1_seed_reads=0`) | **decorative argument** |

### Leg falsifiability (the measurement-integrity core)

`INJECTION_REJECTED` cannot print 0 for **any** builder: candidate/baseline/forged are assigned from
the two booleans `(returncode == 0, foreign intact)` (`:41-44`), where `forged_safe`'s condition is
exactly `baseline_bad`'s and later in the chain, so the string `"forged_safe"` is unreachable and
`:63` is a tautology. Measured directly with a **destructive** token-printing forge:

```
$ python3 corpus/evidence/round60/c1-count.py --builder <S>/forge_destructive.py --work <S>/c1-forge-destructive --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
```
(R7: a builder that prints `=PASS` **and deletes the foreign file** still scores `INJECTION_REJECTED=1/1`.)

`BASELINE_DISCRIMINATES` is a property of the committed `corpus/evidence/round58/controls/build-spans-r55.py`
bytes, not of the candidate; it is fixed unless that tracked file changes, and the counter does not pin it.
Only `CANDIDATE_REFUSAL` varies with `--builder`, and it varies only on `rc == 0 ∧ foreign intact`.

### Do-nothing control (round contract §9)

```
$ printf 'import sys\nsys.exit(0)\n' > <S>/noop.py
$ python3 corpus/evidence/round60/c1-count.py --builder <S>/noop.py --work <S>/c1-noop --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0
```

The no-op writes no `spans.tsv` and no spans; the only files in its out tree are the counter's own
fixtures (`<S>/c1-noop/candidate/{cache/*.txt,out/spans/S777-1.txt,quotes.tsv}`). A builder that returns
0 and does nothing **meets the frozen target**. Per §9 the counter or target is therefore wrong; per
QUALITY 115 the positive path was never shown to require the intended behaviour.

### The in-tree candidate fails the target (honest, and the claim cannot be landed without builder work)

```
$ python3 corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work <S>/c1-candidate --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1
```
Replicated `run()` verbatim (R8): `RC 0`, `FOREIGN_EXISTS False`, `INTACT False` — the candidate deletes
the seeded `S777-1.txt`, exactly as the pinned r55 control does. So with `--builder tools/build-spans.py`
the candidate and the baseline are the **same bytes** and both destructive; the only way this predicate
reaches `C1=PASS` today is a builder that does nothing (above) or a narrow builder patch that the claim
explicitly does not claim to make (`:7` "does not claim the builder itself meets all hazard legs").

### Scope contraction against the frozen predecessor

```
$ grep -oE '\b(EMPTY_OK|REBUILD_OK|HELDOUT_OK|ESCAPE_ENTRY|FOREIGN|SYMLINK_OUT|SYMLINK_CACHE|FIFO_TXT|DEVZERO_TXT|FAT_RAW|MANY_QUOTES)\b' corpus/evidence/round58/c1-count.py | sort -u | wc -l
11
$ grep -oE '(INJECTION_REJECTED|BASELINE_DISCRIMINATES|CANDIDATE_REFUSAL)' corpus/evidence/round60/c1-count.py | sort -u | wc -l
3
$ grep -cE '(SYMLINK_OUT|SYMLINK_CACHE|FIFO_TXT|DEVZERO_TXT|FAT_RAW|MANY_QUOTES|FOREIGN)=' corpus/evidence/round60/c1-count.py
0
```

The "before" surface is 4 safe legs + 7 hazard legs + `BEFORE_FOREIGN` integrity + control denial
(`corpus/evidence/round58/claims.md:5-13`; counter hash still `65da18bb…`, untouched). The "after" surface
is 3 booleans over one fixture. The before→after pair is therefore **not commensurable**: the round-58
aggregate is not replaced (its bytes stay frozen and it remains the only C1 instrument of record), and
the R59-forge scenario — a builder that fails all seven hazards and injects `=PASS` into stderr, proven
`C1=PASS` on the frozen bytes (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`) — **cannot be replayed**
against a counter with no hazard legs.

## C2 — declared scope vs measured scope

Claim: `corpus/evidence/round60-claims.md:15`; predicate: `:17`.

| Predicate element (`:17`) | Counter implementation (`c2-count.py`) | Status |
|---|---|---|
| source digest from committed raw capture | `RAW_PIN` over `root/corpus/captures/…raw` against `RAW_SHA` (`:10,15-16`) | implemented |
| quote locations using the pinned capture-text form | one occurrence of one fixed phrase in the form (`:9,15-16`), line number printed | implemented minimally (1 phrase, not "locations" of the note) |
| "verify the **new entry's** exact observation" | `ENTRY = root/corpus/knowledge/citation-count-semantics-r37.md` (`:8`) — a pre-existing file, present at claim base `b379919` (R14) | **object substituted** |
| "no overreach against those source bytes" | no overreach leg exists; nothing distinguishes what the entry asserts from what the capture states | **not implemented** |
| S101 citation + metadata | substring presence of `source: S101 — https://jc.hit.edu.cn/`, `verified-at:`, `recheck:` (`:17`) | implemented as presence only |
| "require the scorecard's declared disposition" | no SCORECARD read (R10: `c2_scorecard_refs=0`); SCORECARD has **no Round 59/60 header at all** (R12) | **not implemented and unsatisfiable at freeze** |
| "Base must fail because no round-60 entry exists" | base state **passes**: `C2=PASS`, exit 0 (R9) | **contradicted** |
| `--work <fresh-absolute-dir>` isolation | `--work` parsed and never used (R10: `c2_work_reads=0`); no directory created (R10) | **decorative argument** |
| `<lane-copy>` authority | `FORM` is built from script `ROOT`, not `--root` (`:7,13`): a root with **no `.ufo/` at all** still scores `FORM_PIN=1/1` (R11) | **mixed authority** |

### Receipts

```
$ python3 corpus/evidence/round60/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work <S>/c2work
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

```
$ git -C chousa-shokunin cat-file -e b379919a873e7080a31ef92c7002f55f5374e2c6:corpus/knowledge/citation-count-semantics-r37.md && echo ENTRY_EXISTS_AT_CLAIM_BASE=yes
ENTRY_EXISTS_AT_CLAIM_BASE=yes
$ git -C chousa-shokunin diff --stat b379919a -- corpus/knowledge corpus/captures
(no output)          # no round-60 change to either tree
```

The pre-existing entry already contains the scoped limit the claim says it will add:
`corpus/knowledge/citation-count-semantics-r37.md:74-86` — `#### Unknown` with "Whether the
specification copy (S101) is the version in force…" and the ISO-versus-GB/T quote-limit paragraph.
`LIMIT=1/1` is satisfied by that base text, not by any round-60 note.

Root mix, measured:

```
$ find <S>/fakeroot -maxdepth 2 -type d | sort
<S>/fakeroot
<S>/fakeroot/corpus
<S>/fakeroot/corpus/captures
<S>/fakeroot/corpus/knowledge
$ python3 corpus/evidence/round60/c2-count.py --root <S>/fakeroot --work <S>/c2fake
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
```

A `--root` containing no `.ufo` still passes, because the pinned text form is read from the original
checkout. The predicate's `<lane-copy>` isolation is not implemented; a copy's verdict depends on
another tree's bytes.

## Causal separability (contract §2.3) — holds, but the pair is not commensurable

C1 and C2 are separable: `c2-count.py` names no round-58 artifact (R16: 0 hits) and `c1-count.py`
names no knowledge entry (R16: 0 hits); neither writes through the other; each can be run alone. So the
*claim independence* clause is met. What is not met is **before→after commensurability**: C1's "before"
is an 11-leg counter and its "after" is a 3-boolean one over a different fixture, so the pair cannot
demonstrate that the R59 forge is now rejected — it can only demonstrate that a no-op builder returns 0.

## Freeze boundary (must stay untouched; measured once, not edited)

The assignment declares the immutable claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.
Measured at read time:

```
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
```

Five normalizations of the same bytes were hashed; **none** equals the declared digest (R2):
`raw 65721569…`, no-trailing-newline `cae804fa…`, CRLF `dbb847b8…`, whitespace-trimmed `cae804fa…`,
LF+extra-newline `ed2999d0…`. So `09d8053f…` is either a digest of a different artifact or of a
superseded revision; from lane bytes alone it is unresolvable. Aggravating: the claims file is
**untracked** (`git ls-files` → empty; `git status` → `?? corpus/evidence/round60-claims.md`), so no
committed object witnesses the freeze, and QUALITY 118's "spec and dispatch bound to the same digest"
cannot be re-derived. This report does not edit or "repair" the freeze.

## Smallest remediation (bounded; for the *next* freeze — this round's predicates are already scored)

Round contract §9 is explicit that "a rule changed after any seat has scored is not the claim's rule
(kumitate r42)". W1 seats have already scored these predicates (`C1CounterCritic.md`, `C2CounterAudit.md`,
`S101Reopen.md` exist in this wave). So the honest disposition for round 60 is **C1 and C2 not admitted**;
the fixes below belong to the next round's pre-data freeze, with their control receipts committed
*before* ready.

**C1 (next freeze), criterion the counter must satisfy — structured legs, each able to fail:**
1. Make the safe leg an **artifact** check, not a return-code check: run the candidate over the fixture
   and require `out/spans/S601-1.txt` bytes / offsets to equal an independently derived expectation
   (the r58 `HELDOUT_OK`/`REBUILD_OK` pattern), plus `out/spans/S777-1.txt` byte-identical. A no-op
   builder must then score `CANDIDATE_REFUSAL=0`.
2. Pin the baseline by digest: `assert sha256(R55_builder)==<frozen>` and fail the leg with a distinct
   reason when the pin mismatches (currently path-only, R10).
3. Either restore at least one hazard leg (a fixture whose refusal is *observable*, e.g. the r58
   `FOREIGN`/`SYMLINK_OUT` cases) or delete the words "hazard legs" from the predicate. A predicate
   cannot require a leg the counter does not have.
4. Replace the dead-branch mutant with the R59 spoof shape: a builder that fails the declared hazard,
   prints the exact target token, and **also** writes the escaping artifact; require
   `INJECTION_REJECTED=0` for it and `=1` only when the structured leg states (not text) reject it.
   As written, the leg's expression must be able to evaluate false; today it cannot.
5. Either use `--seed` or drop it from the frozen command; bind a pre-freeze receipt that shows the
   no-op builder is denied and a positive builder reaches the exact target.

**C2 (next freeze):**
1. Name the round-60 entry path in the predicate and make a **base-absent** check part of the counter
   (`ENTRY` missing ⇒ nonzero), so a do-nothing round fails.
2. Derive every input — raw capture, text form, entry, scorecard — from `--root`; keep `--work` real and
   require it to be created (scratch discipline, round contract §7.4).
3. Implement the two missing legs as positive prohibitions: a banned-assertion set drawn from the claim
   ("in force", "CNKI implements", "current") must be absent from the note, and `Gate` must carry the
   URL, access date, and ≤25-word located quote.
4. Read the scorecard row named by the claim and require it to exist before freeze (today there is no
   Round 59/60 disposition, so the clause as frozen is unsatisfiable — R12). If the disposition is
   written only at landing, the predicate must say "absent until landing" instead of "require".

**Operability (both counters, applies even if a re-freeze slips):**
- Catch `OSError`/`FileExistsError` from `run()` and return a typed `ERROR` leg instead of a traceback:
  a second run on an existing `--work` currently dies inside `cache.mkdir()` with no `C1=` line (R13),
  which a reader mistakes for a scored FAIL.
- `c1-count.py` inherits the caller's whole environment into the child (`env={**os.environ,…}`);
  pass only `PATH`, `PYTHONDONTWRITEBYTECODE`, `TMPDIR` for a reproducible probe.
- `c2-count.py` depends on the **untracked** `.ufo/waves/round-60/s101-open.txt` (not gitignored, not
  committed — R14). Either derive the form in-process with the pinned `tools/capture-text.py`, or commit
  the form as wave evidence; otherwise the counter is not re-derivable from committed bytes.

## Receipt index

| # | Probe | Result |
|---|---|---|
| R1 | `sha256sum corpus/evidence/round60-claims.md` | `65721569…` ≠ declared `09d8053f…` |
| R2 | 5 normalizations of the claims bytes hashed | none == `09d8053f…` |
| R3 | `jj-lane.sh state` | `branch=master local=b379919a… ahead=0 behind=0` |
| R4 | C1 on `tools/build-spans.py` | `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`, exit 1 |
| R5 | C1 on a no-op builder | `C1=PASS`, exit 0; no spans written by the "candidate" |
| R6 | C1 on a token-printing no-op | `C1=PASS`, exit 0 |
| R7 | C1 on a token-printing **destructive** builder | `INJECTION_REJECTED=1/1` (leg constant) |
| R8 | verbatim `run()` replication for the candidate | `RC 0`, `FOREIGN_EXISTS False`, `INTACT False` |
| R9 | C2 on the untouched lane root | `C2=PASS`, exit 0 |
| R10 | counters read `--seed`/`--work`/scorecard/R55-pin | `0,0,0,0` |
| R11 | leg census r58 vs r60 | 11 vs 3 named legs; 0 hazard legs in r60 |
| R12 | SCORECARD headers | last header is Round 58; no Round 59/60 disposition |
| R13 | C1 re-run on an existing `--work` | uncaught `FileExistsError`, no `C1=` line, exit 1 |
| R14 | entry at claim base / knowledge diff / form tracking | entry exists at `b379919`; no diff; form untracked |
| R15 | `git status --porcelain` after every probe | only pre-existing `?? round60*` / `?? .ufo/waves/round-60/` |
| R16 | cross-references between the two counters | 0 and 0 |
| R17 | `resume_continuity_v1` in `tools/`, `corpus/`, `scripts/` | no live implementation (matches round-38 sentinel note) |

## Boundary statement

No source, capture, counter, claim file, scorecard, registry or wave artifact was modified. All probe
outputs above were produced in `/fast/scratch/hyaku/chousa-r60/ScopeSentinel`, copied here as text, and
the scratch tree was removed before yield. No live fetch, no tool install, no commit, push, or git/jj
mutation was performed. The frozen claims file was read only.
