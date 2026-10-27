# QualityEvidenceScribe — round-60 evidence quality of the frozen claims

**Seat.** QualityEvidenceScribe (leaf, no dispatch, no subagents). **Scope.** Whether the evidence
base the two frozen round-60 claims rest on is *operable* (its declared counting commands run and
discriminate) and *deep* (pointers resolve, historical premises hold on committed bytes, predicate
text matches the artifact that scores it). Read-only against the lane: no product edit, no counter
edit, no fetch, no install, no `git`/`jj` mutation, no sibling/fleet write. Scratch
`/fast/scratch/hyaku/chousa-r60/QualityEvidenceScribe` (240 KB) used and removed before this yield.

**Inputs.** `corpus/evidence/round60-claims.md` (3 355 B, mtime `2026-10-27 17:51:18 -0300`),
`corpus/evidence/round60/{c1-count.py,c2-count.py}`, `corpus/evidence/round58/`,
`tools/build-spans.py`, `.ufo/waves/round-60/{c1-before.txt,c2-before.txt,c1-control-proof.txt}`,
`.ufo/waves/round-59/w1/R59Executor09.md`, `corpus/knowledge/citation-count-semantics-r37.md`,
`corpus/SOURCES.md:111`. Claim base `b379919a873e7080a31ef92c7002f55f5374e2c6` = lane `master` =
`origin/master` (measured).

---

## 1. Freeze attestation — the asserted immutable SHA identifies no bytes

The seat prompt (and every seat prompt in `w1-spec.json`) states: *"The exact immutable claim SHA is
`09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`."* It does not match the file.

```
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md

plain:            65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
no-trailing-nl:   cae804faeb016bf18d8183355e3885b7269e3fbce0a70d790cd688e5bb7175be
strip-CR:         65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
single-nl:        65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
blobhdr-sha256:   d27121a5e34e36d888e85378836e371510e4390745155ccf6a4300a05d967f55
```

No serialization of the file reaches the asserted value. A working-tree sweep of every file ≤2 MiB
(`find . -type f -size -2M … | xargs -0 sha256sum | grep 09d8053f…`) returned **no match**
(`sweep_exit=1`); `git log --all -S'09d8053f…'` returned nothing (`history_search_exit=0`, empty) —
the string was never committed as content. The only occurrences in the lane are inside the prompt
text of `.ufo/waves/round-60/w1-spec.json` (40+ seats). So the one identity the round hands every
seat as the freeze is **not re-derivable from any lane bytes I could reach** — `09d8053f…` is
unverified provenance, not a digest of the claims file.

Secondary freeze defects, measured:

| # | severity | finding | evidence |
|---|---|---|---|
| F1 | critical | Asserted freeze SHA matches no serialization, no working-tree file, no history occurrence | hash table + sweep + `git log -S` above |
| F2 | high | The claims file and **both counters are untracked**: `?? corpus/evidence/round60-claims.md`, `?? corpus/evidence/round60/`, `?? .ufo/waves/round-60/s101-open.txt` — the "frozen" predicate and its instrument are working-tree bytes, so post-dispatch immutability is attested only by mtime/hash observation | `git status --porcelain` |
| F3 | medium | mtime `17:51:18.665` precedes the dispatch marker `w1.ready` `17:55:21.918`, i.e. the freeze *was* written before dispatch | `stat -c%y` both paths |
| F4 | note | Freeze unchanged across this seat: same hash `65721569…` and same mtime at first and last read (seat-level non-tamper attestation, this observer only) | two `sha256sum` runs |

`git cat-file -e b379919a…:<path>` confirms the *historical* substrate is committed
(`round58/c1-count.py`, `controls/build-spans-r55.py`, `tools/build-spans.py`,
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, `corpus/knowledge/citation-count-semantics-r37.md`
all tracked at tip). Only the round's own new instruments are outside version control.

---

## 2. Decisive measurements — both frozen targets are reachable by a do-nothing control

Both claims freeze a target that the contract (§9, phase-4 rule) requires a do-nothing control to be
unable to reach. Both counters are reached at base, with no round work performed.

### 2.1 C1 = PASS with a builder that does nothing

```
$ printf 'import sys\nsys.exit(0)\n' > noop.py
$ python3 -B corpus/evidence/round60/c1-count.py --builder noop.py --work <fresh>
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

The r60 counter observes only `p.returncode == 0` and foreign-file intactness
(`c1-count.py:41-43`); it asserts nothing about `--out` (`cache.mkdir()`/`out.mkdir()` at `:25-26`
are the only writes, and no `spans.tsv` check exists anywhere — `grep -n "spans.tsv" → 0 hits`).
A process that produces nothing satisfies "reaches the safe path" vacuously: clause (a) of the
frozen predicate (`claims.md:9`) is not measured at all.

### 2.2 C1 = PASS when the injection mutant *is* the candidate (kill rule fires)

The counter itself writes its injection mutant at `:60` (`print('=PASS') …; sys.exit(0)`). Handing
that same mutant to `--builder`:

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder forged.py --work <fresh>
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

The frozen kill rule (`claims.md:11`) reads: *"…any child output injection passes target…"*. It does.
Under its own kill rule the frozen C1 is already a miss at the claim base, with no builder work and
no seat data required.

### 2.3 The injection leg is a dead branch (why `INJECTION_REJECTED` is always `1/1`)

```
c1-count.py:41        candidate_safe = p.returncode == 0 and intact
c1-count.py:42        baseline_bad  = p.returncode == 0 and not intact
c1-count.py:43        forged_safe   = p.returncode == 0 and not intact     # identical to :42
c1-count.py:63        forge_blocked = forge_state != "forged_safe"
```

`:42` and `:43` are the same predicate; the ternary at `:44` returns `baseline_bad` before
`forged_safe` can ever be selected, so `forge_state == "forged_safe"` is unreachable and
`forge_blocked` is **always True**. Measured across four unrelated builders, `INJECTION_REJECTED=1/1`
in every run. Clause (c) ("the output-injection mutant … is scored as a failure") has no scoring
path.

### 2.4 Discrimination matrix (C1 counter, five builders, fresh `--work` each)

| builder | behaviour | INJECTION | BASELINE | CANDIDATE | verdict | exit |
|---|---|---|---|---|---|---|
| `noop.py` (`sys.exit(0)`) | does nothing | 1/1 | 1/1 | 1/1 | **C1=PASS** | 0 |
| `forged.py` (counter's own mutant) | prints `=PASS`, exits 0 | 1/1 | 1/1 | 1/1 | **C1=PASS** | 0 |
| `refuseall.py` (`sys.exit(1)`) | refuses everything | 1/1 | 1/1 | 0/1 | C1=FAIL | 1 |
| `destructive.py` (deletes `out/spans/S777-1.txt`) | deletes foreign file | 1/1 | 1/1 | 0/1 | C1=FAIL | 1 |
| `tools/build-spans.py` (lane builder) | deletes foreign file, rc 0 | 1/1 | 1/1 | 0/1 | C1=FAIL | 1 |

The instrument separates "destructive" from "non-destructive" only. It cannot separate "did the
work safely" from "did nothing": the *correct* behaviour and the *null* behaviour land on the same
verdict, while honest refusal is penalised. As a measurement of the C1 claim ("Replace C1's
forgeable aggregate verdict with per-leg structured states…") this counter scores nothing.

### 2.5 C2 = PASS at the claim base, before any round-60 entry exists

```
$ python3 -B corpus/evidence/round60/c2-count.py --work <fresh>
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

The frozen predicate (`claims.md:17`) says: *"Base must fail because no round-60 entry exists."* It
does not fail. The counter's `ENTRY` is not a round-60 entry at all — it is the pre-existing
`corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8`), tracked at tip, mtime
`2026-10-25 17:35` (an r49-era entry). That entry already carries every feature the counter checks,
including the exact sentence the C2 claim says it will add:

```
$ grep -n "#### Unknown" -A6 corpus/knowledge/citation-count-semantics-r37.md
74:#### Unknown
79:- Whether the specification copy (S101) is the version in force, and whether
80:  the counted records in S100 or S102 apply its codes.
```

So C2's target ("add one scoped, source-grounded correction note that separates what S101's offline
capture states … and explicitly records the existing knowledge entry's S101 source-quote limit") is
already satisfied by committed bytes written four rounds earlier. The do-nothing control meets the
target: C2, as frozen, is unfalsifiable.

---

## 3. C1 — predicate, kill rule and counter disagree

| # | severity | location | finding | evidence |
|---|---|---|---|---|
| C1-1 | critical | `claims.md:9` vs `c1-count.py:41` | Clause (a) "reaches the independently observed safe path" is never observed: no `spans.tsv`/output assertion exists; `noop` PASSes | §2.1 |
| C1-2 | critical | `c1-count.py:42-43,63` | Clause (c) is a dead branch; `INJECTION_REJECTED` is constant `1/1` for any builder | §2.3, §2.4 |
| C1-3 | critical | `claims.md:11` kill rule | Injection passes the target at freeze ⇒ the claim's own kill rule is triggered before data | §2.2 |
| C1-4 | high | `c1-count.py:53` | `--seed 6001` is parsed and never read (only other `seed` occurrence is a comment at `:65`) — the predicate's seed implies fixture variation that does not exist | `grep -n seed` |
| C1-5 | high | `claims.md:5,9` vs `c1-count.py` | Predicate text says the counter "exits 0 only when the frozen safe and hazard legs meet their declared requirements"; the r60 counter has **no legs at all** (`legs.append` count: r58 = 23, r60 = 0). The after-state describes an artifact that does not exist | `grep -c legs.append` both files |
| C1-6 | medium | `c1-count.py:25-26` | Not idempotent per `--work`: second run with the same dir raises `FileExistsError` (`…/forge/cache`) and exits 1 — a crash is indistinguishable from `C1=FAIL` by exit code alone | measured (`second_run_exit=1`) |

**What does hold on C1's historical side.** The premise the round inherits — that the *frozen
round-58* counter credits an echoing builder — is sound on committed bytes, twice over:

* `.ufo/waves/round-59/w1/R59Executor09.md` (tracked at tip) §6 shows the full run with every one of
  the seven refusal legs at `fail(...)`, `SUMMARY … REFUSE=7/7`, and still `C1=PASS` / `EXIT=0`.
* The mechanism is visible in the committed r58 source: `expect_refuse` splices candidate
  stderr/stdout into the leg string (`round58/c1-count.py:150-156`, `:222-223`) and the verdict
  substring-scans that text (`:391` `ref_pass = all(("=PASS" in l) …)`, `:394`).
* `corpus/evidence/round58/c1-count.py` still hashes `65da18bb…` — exactly the pin R59Executor09
  recorded — so the statement "Round-58 bytes remain frozen" (`claims.md:9`) is verified.
* `tools/build-spans.py` and `corpus/evidence/round58/controls/build-spans-r55.py` are
  **byte-identical** (`1ed2650a…`), so no candidate hardening has landed and the "known unsafe
  control" is still the live candidate.

That makes C1's repair *necessary*; it does not make the round-60 instrument a measurement of it.

---

## 4. C2 — predicate and counter disagree, and the counter is not root-scoped

| # | severity | location | finding | evidence |
|---|---|---|---|---|
| C2-1 | critical | `c2-count.py:8` vs `claims.md:17` | Base PASSes; the counter scores the pre-existing r49 entry, not a round-60 entry | §2.5 |
| C2-2 | critical | `claims.md:17` | "Base must fail" is false ⇒ do-nothing control meets target ⇒ §9 disqualifier | §2.5 |
| C2-3 | high | `claims.md:17` vs `c2-count.py:16-18` | Predicate requires "verify the new entry's exact observation and no overreach" and "require the scorecard's declared disposition". The counter reads **no** SCORECARD (`grep SCORECARD → 0 hits`), no round-60 entry, and checks only three substrings: one literal line (`EXPECTED='c. 文献类型及载体类型标志；'` present exactly once), `'#### Unknown' in body`, and one sentence in body | `c2-count.py:18` |
| C2-4 | high | `c2-count.py:7,13` | `form = ROOT/'.ufo/waves/round-60/s101-open.txt'` uses the module-level `ROOT`, so `--root <lane-copy>` cannot vary that input; the declared lane-copy invocation is half-honoured and a mutated form cannot be tested | source line + `--root` binding at `:13` |
| C2-5 | high | `.ufo/waves/round-60/s101-open.txt` | One of C2's two pinned inputs is an **untracked wave artifact** (`??`), so C2 is not re-derivable from committed bytes although the predicate says "from committed S101 raw capture" | `git status --porcelain` |
| C2-6 | medium | `.ufo/waves/round-60/c2-before.txt` | The "before" receipt is prose only: no command, no output, no exit code, and its central assertion ("Baseline must fail by missing round-60 source gate") is contradicted by the executed counter. Not a receipt. | file read vs §2.5 |

**What does hold on C2's source side** (the depth is real where it is historical):
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` is tracked and hashes to the counter's pin
`6063a3af…`; `corpus/SOURCES.md:111` carries the S101 row with its locators; the r37 entry is
tracked and its Gate metadata (`verified-at: 2026-10-25`, `recheck: 180d`) predates the round. The
quote at `LINE=245` of the pinned form is a genuine located line of the offline capture. The defect
is not the source — it is that the round's *new* content gate collapses to substrings already
present, so nothing about round 60 is being measured.

---

## 5. Pointer resolution (every lane pointer in the frozen claims; measured)

| claim pointer | status | hash / location |
|---|---|---|
| `corpus/evidence/round60/c1-count.py` | resolves, **untracked** | 3 842 B, mtime 17:51 |
| `corpus/evidence/round60/c2-count.py` | resolves, **untracked** | 1 955 B, mtime 17:52 |
| `tools/build-spans.py` | resolves, tracked at tip | `1ed2650a…` |
| pinned r55 builder `round58/controls/build-spans-r55.py` | resolves, tracked at tip | `1ed2650a…` (identical to candidate) |
| `round58/c1-count.py` (frozen, "bytes remain frozen") | resolves, tracked at tip | `65da18bb…` = R59Executor09's pin |
| W1 `R59Executor09.md` ("C1=PASS with all seven hazards failing") | resolves, tracked at tip | §6 of that report: `C1=PASS`, `EXIT=0`, 7/7 refusal legs `fail` |
| S101 raw capture | resolves, tracked | `6063a3af…` = counter pin |
| `.ufo/waves/round-60/s101-open.txt` (capture-text form) | resolves, **untracked** | `a8e3e7ad…` = counter pin |
| `corpus/SOURCES.md` S101 row | resolves | line 111 |
| `corpus/knowledge/citation-count-semantics-r37.md` (existing entry) | resolves, tracked | 6 806 B, mtime 2026-10-25 17:35 |
| claim base `b379919a…` | resolves | = `master` = `origin/master` |

No pointer is dead. Every defect above is a *semantic* mismatch between predicate text, instrument
and state — not a broken link.

---

## 6. Before-receipt fidelity (C1 only)

`.ufo/waves/round-60/c1-before.txt` is an honest transcription: re-running its command on current
bytes reproduces its four verdict lines exactly (only my appended `counter_exit=1` line differs).

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work <fresh>
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
counter_exit=1
$ diff <(grep -E '^(INJECTION|BASELINE|CANDIDATE|C1=)' .ufo/waves/round-60/c1-before.txt) <my run>
4a5
> counter_exit=1
```

So the L1's "before" is reproducible. The problem is the instrument's semantics, not the receipt's
fidelity. Two related provenance defects remain:

* the "before" was measured with the **round-60** counter (written 17:51, untracked, i.e. not present
  at claim base `b379919a…`), so before and after are not measured on the same instrument and no
  delta is attributable to the claimed work;
* `.ufo/waves/round-60/c1-control-proof.txt` is prose, not a run: item 1 records an excluded attempt
  ("expected builder CLI interface mismatch, excluded") with no command and no output; item 3 points
  at `c1-before.txt`, i.e. at the new counter, not at the frozen r58 counter the claim exists to fix.

---

## 7. Depth and operability assessment

**Operability.** Both counters execute, exit deterministically, and are pasteable commands (predicate
text matches the CLI: `--builder/--work/--seed`, `--root/--work`). Two operability defects:
`--seed` is a no-op and `--work` is non-idempotent (C1-4, C1-6). Both counters honour `--work` for
their fixtures (no hardcoded `/tmp`); C1 still defaults its scratch to
`HYAKU_SCRATCH/chousa-r60/c1-count` when `--work` is omitted, which is the sanctioned scratch root.

**Depth.** The *historical* depth is genuine: the r58 forgery mechanism is pinned in committed bytes
(counter hash, mechanism lines, an independent seat's full run), the r55 control is byte-stable, and
the S101 quote chain (capture digest → SOURCES row → r37 Gate) resolves. The *round-specific* depth
is absent: neither frozen predicate constrains anything the base state does not already satisfy, and
neither counter can distinguish the claimed work from doing nothing. A 3 355-byte claim file with two
untracked instruments, both of which PASS at base, is not yet an evidence base a closure can judge —
the honest reading today is **C1: miss under its own kill rule; C2: miss (target already met at
base)**, pending whatever the executor lands, because no post-work run can change a target that the
null control already reaches.

**One line for the round report.** Quality-evidence verdict: `C1 = PASS-reachable-by-null-control`,
`C2 = PASS-at-base`; freeze identity `09d8053f…` unverifiable against lane bytes.

---

## 8. Conflicts for the canonical judge — reported verbatim, not resolved here

1. Prompt assertion vs measured bytes: prompt says *"The exact immutable claim SHA is
   `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`"*; the file hashes
   `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` and no serialization, sweep or
   history occurrence yields `09d8053f…`.
2. Receipt assertion vs measurement: `.ufo/waves/round-60/c2-before.txt` says *"Baseline must fail by
   missing round-60 source gate; C2 not admitted."*; the executed counter prints `C2=PASS`, exit 0,
   `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1`.
3. Predicate vs instrument: `claims.md:9` says the counter must print `C1=PASS` *iff* (a), (b), (c);
   measured `C1=PASS` with `a = false` (no builder work) and with `c` structurally unreachable
   (`c1-count.py:42-43`).
4. Predicate vs instrument: `claims.md:17` requires the scorecard's declared disposition and a new
   entry's observation to be verified; `c2-count.py` never opens `SCORECARD.md` and never opens a
   round-60 entry.

## 9. Recommended repair (pointer only — this seat edited nothing)

1. Publish the freeze identity from measured bytes once the L1 commits the claims file, and replace
   the prompt SHA with that digest; an unverifiable "immutable SHA" cannot certify a freeze.
2. Give each counter a discriminating predicate **before** data: C1 needs a positive-path assertion
   (the artifact the builder must produce), a must-FAIL control, and an injection mutant whose
   leg state is a typed field — never a comparison that collapses to a constant. C2 needs the
   round-60 entry as `ENTRY` (or an explicit, already-met detector), SCORECARD disposition read, and
   `form` resolved from `--root` with the form bytes committed.
3. Delete the unused `--seed` or make it real; make `--work` re-runs explicit (fresh-dir assertion
   with a clear error) instead of a traceback that exits 1.
4. Keep the r58 mechanism findings: they are the strongest committed evidence this round has.

## 10. Limits / hygiene

- Read-only against the lane: `read`, `grep`, `sha256sum`, `stat`, `git status/cat-file/log -S` (all
  read-only). No `git`/`jj` mutation, no fetch, no fleet/sibling write, no commit.
- Lane writes: this report only. Scratch `/fast/scratch/hyaku/chousa-r60/QualityEvidenceScribe`
  (240 KB: five stub builders + counter work dirs) removed before yield; nothing else remains under
  that path. No receipts were copied into the wave dir because the assignment forbids writes outside
  this report — every output above is transcribed verbatim instead.
- Not installed, not upgraded: no tool was needed (python3 3.14 present; pacman untouched).
- Not exercised: any live fetch (L0 `8d77e6c1` stays open), the r58 spoof-builder reproduction (its
  bytes were scratch-only in round 59; the mechanism is cited from committed source and the committed
  seat report instead of re-executed), the assimilation/quarantine item (other seats).
- `/tmp` untouched; no file created outside my scratch and this report.

---
seat: QualityEvidenceScribe
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-60/w1/QualityEvidenceScribe.md
scratch: /fast/scratch/hyaku/chousa-r60/QualityEvidenceScribe (removed)
lane writes: this report only
