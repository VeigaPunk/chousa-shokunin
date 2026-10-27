# C2GroundingScribe — round-60 grounding evidence

**Seat.** C2GroundingScribe (leaf scribe, round-60 wave 1). **Scope.** Bounded grounding analysis of the
frozen claims against: `corpus/evidence/round60-claims.md`, the two round-60 counters, the prior committed
evidence those claims cite, and the lane's current bytes. Read-only against the lane: this file is the
only lane write. No fetch, no commit, no git/jj mutation, no spawn.

**Why this seat.** "Grounding" = does every artifact and pin a frozen predicate names actually resolve,
is its provenance committed, and does the counter's code implement the clause the predicate states. It
is a mapping job, not a falsification verdict: the attack seats (C1CounterCritic, CounterMutation,
C2CounterAudit, CounterAudit) own the verdicts. Everything below is measured or quoted, never inferred
without a marker.

## 0. Pins as measured (t0 and t1, byte-identical)

```
$ sha256sum corpus/evidence/round60-claims.md corpus/evidence/round60/{c1,c2}-count.py
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe  corpus/evidence/round60/c2-count.py
```

`stat`: claims size 3355, mtime `2026-10-27 17:51:18.665690725 -0300` (ctime equal); c1-count 3842 @
`17:51:38`; c2-count 1955 @ `17:52:14`. A t1 re-run at the end of this seat printed the same three digests
(`diff` of the two receipt files empty → `STABLE: byte-identical to t0`), so the freeze did not move under
this seat. **These digests bind every claim below; if a later seat edits either counter, re-measure.**

Lane tip: `jj-lane.sh state` → `branch=master local=b379919a… remote=b379919a… ahead=0 behind=0
head=detached`; `git log -1 b379919a…` → `2026-10-27 17:05:42 -0300 protocol-shokunin · round-59
verifier spot-check (integrator, hyaku): non-author admit/reject`. The base commit the claims file names
(`:3`) is the lane tip.

## 1. G1 — the declared immutable claim SHA resolves to no artifact in the lane

The assignment and all 64 seat prompts carry: *"The exact immutable claim SHA is
`09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`."*

```
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1   # ≠ 09d8053f…
$ grep -rl '09d8053f5f09a26c…a440' chousa-shokunin .ufo
chousa-shokunin/.ufo/waves/round-60/w1-spec.json
chousa-shokunin/.ufo/waves/round-60/w1-dispatch.json
```

The digest exists only inside the dispatch payload. Normalization variants of the current bytes were
tested and none match (no-trailing-newline `cae804fa…`, one-more-newline `ed2999d0…`, CRLF `dbb847b8…`,
stripped-ends `cae804fa…`, LF-collapse = raw). A digest scan of every file under `.ufo/waves/round-60`
and `corpus/evidence` (`find … -size -2M | sha256sum`) found no file carrying `09d8053f…` either.

**Grounding consequence.** No seat can verify the frozen bytes against the pin it was given, and no
closure can re-derive the claim's identity from the digest. The cause (a post-digest edit of the claims
file, a digest of a different serialization, or a digest taken by another tool) is **not** determined by
this seat and is not asserted; what is established is that the pin, as handed to the wave, resolves to
nothing in the lane. This is a **blocking** defect for any admissibility claim that quotes "the exact
immutable claim SHA" as its warrant.

## 2. G2 — the whole round-60 evidence set is untracked at the claim base

```
$ git ls-files --error-unmatch corpus/evidence/round60-claims.md
error: pathspec 'corpus/evidence/round60-claims.md' did not match any file(s) known to git
$ git status --porcelain
?? .ufo/waves/round-60/
?? corpus/evidence/round60-claims.md
?? corpus/evidence/round60/
$ git ls-tree -r --name-only b379919a… corpus/evidence/round60
                                        # empty
```

Claims artifact, both counters and the wave dir have **no committed bytes at the claim base**. Contract
§9 requires each after-state to be "one concrete value that the closure can re-derive with one command
over committed bytes"; today the closure can only read working-tree files that another seat may still be
writing. This is why the digest in G1 matters: an uncommitted predicate has no independent pin.

## 3. G3 — the prior evidence C1's "before" cites does resolve, and is committed

| reference (claims `:3`, `:11`) | state | evidence |
|---|---|---|
| base `b379919a…` | exists, is the lane tip, ahead 0 | `jj-lane.sh state` |
| `.ufo/waves/round-59/w1/R59Executor09.md` | **tracked** | `git ls-files --error-unmatch` |
| `C1=PASS` with all seven hazards failing | states it at `:215-254` | §6 "Correction": candidate `spoof-builder.py` `1a3aad9b…`, `SUMMARY OK=4/4 REFUSE=7/7`, `C1=PASS` (`:249-250`), "Every refusal leg is `fail(...)`" (`:254`) |
| "frozen round-58 C1 permits forged target-token output" | same §6, P6 row `:350` | `"=PASS"` substring over candidate stderr |
| round-58 bytes frozen | unchanged | `sha256 corpus/evidence/round58/c1-count.py` = `65da18bb…`, the digest R59 cited; file tracked |
| pinned r55 builder | exists, **byte-identical to the lane builder** | `sha256` of `corpus/evidence/round58/controls/build-spans-r55.py` = `1ed2650a…` = `tools/build-spans.py` |

So C1's *narrative* before-state is grounded in committed evidence. It also means the candidate the
frozen predicate calls "the candidate" is, at base, the same bytes as the destructive control: running the
counter on `tools/build-spans.py` reproduces the wave's own `c1-before.txt` (`CANDIDATE_REFUSAL=0/1
C1=FAIL EXIT=1`).

## 4. G4 — C1 predicate clause map: clause (c) has no implementation (dead branch)

Frozen predicate (`round60-claims.md:9`): `C1=PASS` **iff** (a) candidate reaches the safe path without
deleting the foreign file, (b) the r55 builder shows the destructive control, (c) the output-injection
mutant prints `=PASS` **but is scored as a failure**.

Code in `corpus/evidence/round60/c1-count.py` (`66e50763…`):

```
41:        candidate_safe = p.returncode == 0 and intact
42:        baseline_bad = p.returncode == 0 and not intact
43:        forged_safe = p.returncode == 0 and not intact
44:        return p.returncode, "candidate_safe" if candidate_safe else ("baseline_bad" if baseline_bad else ("forged_safe" if forged_safe else ""))
...
63:        forge_blocked = forge_state != "forged_safe"
69:        candidate_ok = candidate_state == "candidate_safe"
70:        passed = forge_blocked and baseline_discriminates and candidate_ok
71:        print(f"INJECTION_REJECTED={int(forge_blocked)}/1")
```

`:43` is the same predicate as `:42`, and `:44` tests those two first, so **`"forged_safe"` is
unreachable**; `forge_blocked` is therefore a constant `True` and `INJECTION_REJECTED=1/1` carries no
information. Measured directly by importing the counter's own `run()`:

```
$ python3 -B -   # imports c1-count.py, runs its own forged.py against a fresh fixture dir
forged rc=0 state='candidate_safe'  -> forge_blocked=True
R55 path resolves: …/round58/controls/build-spans-r55.py True
r55 rc=0 state='baseline_bad'
```

Clause (c) is thus **not implemented**: the exact-token forge is scored `candidate_safe` (the *passing*
state), not a failure, while the leg still prints rejected. Clause (a) is implemented only as
`rc == 0 and foreign file intact` — there is no observation that a build ever happened (no `spans.tsv`
read, no row count). Clause (b) is implemented and observed `1/1`. The predicate's phrase "the frozen safe
**and hazard legs**" has no counterpart in the file: the round-60 counter contains no hazard/refusal leg
(symlink, FIFO, device, oversize, row cap) — the seven r58 legs are dropped, not restructured.

## 5. G5 — the do-nothing control reaches the frozen C1 target

```
$ printf 'import sys\nsys.exit(0)\n' > $S/noop-builder.py          # sha256 14c75fb904c57c21…
$ python3 -B corpus/evidence/round60/c1-count.py --builder $S/noop-builder.py \
      --work $S/noop-run --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0

$ python3 -B corpus/evidence/round60/c1-count.py --builder $S/c1-run/forged.py \
      --work $S/forge-as-candidate --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0
```

A two-line script that never reads `--quotes`, never touches the cache and never writes a span satisfies
the frozen predicate, and so does the counter's own injection mutant once it is passed as the candidate.
Contract §9: "A target must be one a do-nothing control cannot reach… if it meets the target, the counter
or target is wrong." The predicate also leaves `<builder>` unbound, so the verdict is a function of an
arbitrary argument rather than of lane state: with `--builder tools/build-spans.py` the same bytes print
`C1=FAIL` (observed), with `--builder <noop>` they print `C1=PASS`. This is the same forgeability class
C1 claims to remove, moved from stdout to exit status. Verdict belongs to the critic seats; the grounding
fact is that the target is reachable without any claimed work.

## 6. G6 — the C2 counter passes at base, where the frozen predicate requires failure

Frozen predicate (`:17`): "…and require the scorecard's declared disposition. **Base must fail because no
round-60 entry exists.**"

```
$ ls corpus/knowledge | grep -i 'r60\|round60\|round-60'
                                        # empty: no round-60 entry exists
$ python3 -B corpus/evidence/round60/c2-count.py --root . --work $S/c2-run
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

Cause, from the file (`:8`): `ENTRY=ROOT/'corpus/knowledge/citation-count-semantics-r37.md'` — a
round-37 entry that already carries both needles the counter tests:

```
$ grep -n '#### Unknown' corpus/knowledge/citation-count-semantics-r37.md        → 74
$ grep -n 'Whether the specification copy' corpus/knowledge/citation-count-semantics-r37.md → 79
```

So base PASS is structural, not incidental: the counter never looks for a round-60 entry. The wave's own
`c2-before.txt` asserts the opposite ("Baseline must fail by missing round-60 source gate; C2 not
admitted") and is contradicted by the artifact it describes. Consequence for the claim: the declared
before→after cannot be measured, and the do-nothing control (admit nothing) reaches the target.

## 7. G7 — C2 predicate clause map: three of five clauses unimplemented; `--work` is inert

| predicate clause (`:17`) | implementation |
|---|---|
| "establish source digest … from committed S101 raw capture" | ✅ `RAW_SHA` vs `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (`:6,:10`), digest matches, file tracked |
| "…and quote locations … using the pinned capture-text form" | partial: `FORM` is hardcoded `ROOT/'.ufo/waves/round-60/s101-open.txt'` (`:7`) — the **untracked** wave-dir copy, never `--root`; a missing/edited copy exits 2 although committed bytes for the same form exist (G8) |
| "verify **the new entry's** exact observation and no overreach against those source bytes" | ❌ no round-60 entry is read; the only content checks are two substring tests on r37 |
| "verify its S101 citation and metadata" | partial: `:18` substring tests `'\n# '`, `'source: S101 — https://jc.hit.edu.cn/'`, `'verified-at:'`, `'recheck:'` on r37 |
| "require **the scorecard's** declared disposition" | ❌ `grep SCORECARD c2-count.py` → no match; and `grep -c 'round-60' SCORECARD.md LOG.md` → `0`,`0`, so no disposition exists to require |

`--work` is declared at `:13` (`p.add_argument('--work', …)`) and **never referenced again**
(`grep 'a.work'` → no match): the predicate's mandatory `--work <fresh-absolute-dir>` is a no-op, and the
counter writes nothing, so the scratch-discipline clause cannot be exercised.

## 8. G8 — the pinned form is reproducible and already has a committed home

```
$ python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > $S/form-repro.txt
EXIT=0
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  $S/form-repro.txt   # = FORM_SHA
47356 bytes / 27012 chars
$ sha256sum corpus/evidence/round59/s101-open.txt .ufo/waves/round-60/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  corpus/evidence/round59/s101-open.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
```

The form is deterministic from committed `tools/capture-text.py` (`2c0140bc…`, the round-58 pin) plus the
committed capture, and the round-59 evidence file is **byte-identical** (47356 B, 27012 chars). The
located quote `c. 文献类型及载体类型标志；` occurs exactly once, at form line 245, matching the wave's
`s101-receipt.txt`. So this pin is sound; the defect is only that the counter reads the uncommitted copy
instead of the committed one. (The round-58 form, `9d0191dc…`/1680 B, is a different, frozen form and is
not used by this counter.)

## 9. G9 — claim-internal statements that do hold

- Axis naming: `SCORECARD.md:2908` records "[C1 operability (lowest numeric axis, historical scale
  3/10)]" and `:2915` the round-58 `operability … unprovable` verdict → C1's axis label is accurate.
- S101 registry row exists: `corpus/SOURCES.md:111`, id `S101`, tier `B`, status `mined`, recheck
  `180d`, `used-by` = `corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md,
  corpus/lessons/round-59.md` → "sourced S101" is accurate, and the row is already mined (no new row is
  claimed).
- The "existing knowledge entry's S101 source-quote limit" is real: `r37:79` already says "Whether the
  specification copy (S101) is the version in force…"; `r37:26-31` already quotes the type/carrier
  notation ("its reference elements include 文献类型及载体类型标志") and the 14.1/14.4 format rules.
  Reported as a grounding observation for the non-author gate: C2's proposed "correction note" lands on
  text the lane already holds, and round-59's non-author spot-check already ruled this exact slice
  (admit as source evidence only; reject current-status) —
  `corpus/lessons/round-59-verifier-spotcheck.md` "Discernment spot-check" table. Whether that is
  duplication (a §9 "re-scoring ground the lane already holds") or a genuine depth move is the
  reviewer's call, not this seat's.
- Round-59 routed the requirement "re-freeze C1/C2 only after their positive controls reach the exact
  final predicate" (`corpus/lessons/round-59-verifier-spotcheck.md`, "Routed defects"). G5 shows the
  round-60 C1 positive control overshoots: it is reachable by a no-op.

## 10. Conflicts, verbatim (for the canonical judge)

| # | frozen claim text | observed artifact state |
|---|---|---|
| X1 | "The exact immutable claim SHA is `09d8053f…a440`" | on-disk `65721569…18d1`; digest appears only in `w1-spec.json`/`w1-dispatch.json`; no normalization or lane file matches (G1) |
| X2 | claim base "`b379919a…` (round-59 non-author review)" | base commit is correct, but none of the round-60 evidence exists at it: `git ls-tree b379919a… corpus/evidence/round60` is empty (G2) |
| X3 | "(c) the output-injection mutant prints `=PASS` but is scored as a failure" | the mutant is scored `candidate_safe`; `forged_safe` is unreachable; `INJECTION_REJECTED=1/1` is constant (G4) |
| X4 | "the counter exits 0 only when the frozen safe and hazard legs meet their declared requirements" | no hazard legs exist in `c1-count.py`; the only safe leg is `rc==0 and foreign intact` (G4, G5) |
| X5 | kill rule: "any child output injection passes target" / §9 "a target a do-nothing control cannot reach" | `sys.exit(0)` as `--builder` prints `C1=PASS`, exit 0; the counter's own `forged.py` as `--builder` does the same (G5) |
| X6 | C2: "Base must fail because no round-60 entry exists" | base prints `C2=PASS`, exit 0 with zero round-60 entries; `c2-before.txt` asserts the opposite (G6) |
| X7 | C2: "verify the new entry's exact observation and no overreach against those source bytes … require the scorecard's declared disposition" | no new-entry read, no source-byte comparison, no SCORECARD read; `--work` unused; no round-60 disposition exists in SCORECARD/LOG (G7) |

## 11. Limit of this seat's evidence

- I did not modify, repair or re-freeze anything. Digests `c1-count 66e50763…`, `c2-count a19b0678…` are
  the measured bytes; a later seat edit invalidates every verdict above and the L1 must re-measure.
- Not exercised: the full round-58 battery, the r59 spoof builder, any write-path hazard (symlink/FIFO/
  oversize), and the other wave-1 seats' concurrent output. I assert nothing about whether some future
  builder could make C1 pass honestly; I only observed that today's lane builder is byte-identical to the
  destructive control and that a no-op passes.
- No external fetch. S101's present-day validity and CNKI implementation remain unknown (L0 `8d77e6c1`
  open); nothing here asserts them.
- Noted for the assimilation/sources seats, not adjudicated here: `.ufo/waves/round-60/collisions` is
  non-empty and lists 52 ids including `S101` — per digest §10 a non-empty collision file must be fixed
  in scratch before any registry append.

## 12. Hygiene

- Scratch: `/fast/scratch/hyaku/chousa-r60/C2GroundingScribe` — created for the fixtures, the `run()`
  probe, the no-op builder, the form reproduction, and the t0/t1 digest receipts; **removed before
  yield** (`rm -rf`). Every output quoted above is transcribed in full, and each is reproducible from the
  command shown against the pins in §0.
- Lane writes: this report only. `git status --porcelain` before and after this seat is unchanged
  (`?? .ufo/waves/round-60/`, `?? corpus/evidence/round60-claims.md`, `?? corpus/evidence/round60/`).
- Tool installs: none needed (python3 present); `~/.omp/agent/RULES.md` install rules were therefore not
  exercised and pacman was not run. No fetch, no commit, no git/jj mutation.

---
seat: C2GroundingScribe
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-60/w1/C2GroundingScribe.md
scratch: /fast/scratch/hyaku/chousa-r60/C2GroundingScribe (removed)
lane writes: .ufo/waves/round-60/w1/C2GroundingScribe.md (this file) only
