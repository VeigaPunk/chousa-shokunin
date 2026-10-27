# ClaimReviewer — round-60 w1 (bounded claim review)

Seat: ClaimReviewer (reviewer, leaf — no dispatch). Scope per assignment: frozen claims
`corpus/evidence/round60-claims.md`, prior committed evidence, current counter/source only.
Canonical runtime: system `python3`; lane HEAD verified `b379919a873e7080a31ef92c7002f55f5374e2c6`
(the claim base named in the frozen claims header). No LSP server is available in this seat's
tooling, so caller/definition checks are text-level; the counters have exactly one in-repo
reference each (the claims doc itself; grep over `*.md|*.py|*.sh` excluding wave files returned
only `corpus/evidence/round60-claims.md:9,17`) — no caller blast radius. All execution ran under
scratch `/fast/scratch/hyaku/chousa-r60/ClaimReviewer/` (removed after this report). No writes
outside this report; no git/jj mutation. Frozen-claims bytes untouched by this seat: `sha256sum`
re-verified identical at seat start and seat end (`65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`).

## 0. Freeze provenance — assignment SHA does not match the frozen bytes (unresolved)

- Assignment pins SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`
  (w1-dispatch.json / w1-spec.json, every seat task string).
- Observed file sha256: `65721569…` (twice, start and end of this seat). Git blob:
  `git hash-object` → `5ea0acf0881f950be640754a21408a71ebd95e5e`. Neither matches.
- Normalization probes (rstrip newline, +newline, CRLF, strip) — computed in scratch, five
  variants — none match the pinned value. The pinned SHA matches nothing derivable in-repo except
  the dispatch text itself.
- Same mismatch independently observed by sibling seats: `w1/C2CounterAudit.md:22`,
  `w1/S101Reopen.md:21`. No evidence of post-dispatch mutation (file untracked since dispatch,
  hash stable across the wave window, mtime predates seat start).
- Recommendation: L1 must state the pinned SHA's derivation (what bytes, what time) before
  closure, or re-pin. The claims content itself is coherent and its stated base matches HEAD.

## 1. C1 — operability (round-58 C1 counter measurement integrity)

Verified positives first:
- **Output-blindness holds.** `run()` derives states only from `p.returncode` and the independently
  read foreign-file bytes (`c1-count.py:41-43`); captured stdout/stderr are never read. The claim's
  core requirement "output bytes cannot establish a leg state" is structurally true of these bytes.
- **Fail-closed paths.** Timeout → `(124, "")` → leg fails; any exception propagates nonzero;
  non-fresh `--work` crashes at `cache.mkdir()` rather than silently reusing state.
- **Baseline leg discriminates empirically.** `BASELINE_DISCRIMINATES=1/1` in all runs: pinned
  `corpus/evidence/round58/controls/build-spans-r55.py` exits 0 and deletes
  `out/spans/S777-1.txt` (reproduced directly in scratch).
- **Round-58 bytes frozen.** `git status --porcelain corpus/evidence/round58` empty at HEAD
  `b379919a`; claims' "Before" corroborated by committed
  `.ufo/waves/round-59/w1/R59Executor09.md` §5–7 (exact `C1=PASS`, exit 0, with all seven refusal
  legs `fail(...)` via stderr spliced into leg strings).

Findings, severity-ordered:

- **C1-1 [CRITICAL] The candidate leg awards C1=PASS to a do-nothing forge — the exact-token
  forge the claim says is rejected.** Leg (a) is `candidate_ok = candidate_state ==
  "candidate_safe"` (`c1-count.py:69`) where `candidate_safe = p.returncode == 0 and intact`
  (`:41`): exit 0 plus untouched foreign file, with **no check that the builder produced any
  build product**. Measured:
  ```
  $ printf 'import sys\nprint("=PASS")\nsys.exit(0)\n' > $S/stubs/noop-pass.py
  $ python3 corpus/evidence/round60/c1-count.py --builder $S/stubs/noop-pass.py \
        --work $S/c1work/run4 --seed 6001
  INJECTION_REJECTED=1/1
  BASELINE_DISCRIMINATES=1/1
  CANDIDATE_REFUSAL=1/1
  C1=PASS
  (exit 0)
  ```
  The run-4 candidate workdir contains only the untouched foreign fixture (`out/spans/S777-1.txt`)
  — no `spans.tsv`, no `S601-1.txt`: the builder built nothing and printed `=PASS`, and the counter
  passed it. So "the new counter's structured result path … rejects the same exact-token forge"
  (claims, C1 After-target) is **false for the current counter bytes** when the forge is supplied
  as the builder under test; it is rejected only in the counter's own hardcoded internal forge leg.
- **C1-2 [HIGH] The current default candidate is destructive in the probe scenario, so C1=FAIL
  today.** `tools/build-spans.py` on the counter's exact fixture exits 0 **and deletes** the
  foreign span (reproduced in scratch: `cand-rc=0`, `out/spans/` contains only `S601-1.txt`):
  ```
  $ python3 corpus/evidence/round60/c1-count.py --builder tools/build-spans.py \
        --work $S/c1work/run1 --seed 6001
  INJECTION_REJECTED=1/1  BASELINE_DISCRIMINATES=1/1  CANDIDATE_REFUSAL=0/1  C1=FAIL  (exit 1)
  ```
  This is consistent with the claim's own disclaimer (builder not claimed fixed), and the
  predicate's `<builder>` is a placeholder for a new candidate — but the round report must record
  the measured FAIL honestly; the counter does not pass today and cannot distinguish the current
  candidate from the unsafe r55 control (both exit 0 and delete).
- **C1-3 [MEDIUM] The injection leg is vacuous by construction.** The forge leg always runs the
  counter's internal stub written at `c1-count.py:60` (prints `=PASS`, exits 0, touches nothing);
  `--builder` never flows into it (`:61-63`). Since the stub cannot delete the foreign file, state
  `"forged_safe"` (rc 0 + destroyed, `:43`) is unreachable and `forge_blocked` is tautologically 1.
  The leg does not test injection resistance at all; the real protection is output-blindness, and
  the leg line misreports it. A destructive forge supplied as the *candidate* is classified
  `baseline_bad` and fails only via the candidate leg (measured, run3 with a delete-and-print
  stub: `C1=FAIL`, `INJECTION_REJECTED=1/1`).
- **C1-4 [LOW] State taxonomy is misleading vs the claim's "per-leg structured states".**
  `baseline_bad` and `forged_safe` are the identical expression (`:42-43`); a non-destructive
  forge-as-candidate is classified exactly like a safe candidate (`candidate_safe`). There are no
  refusal legs in this counter despite the claim's refusal-leg language; the battery is one
  scenario with three boolean states, two identical.
- **C1-5 [LOW] `--seed` accepted and unused** (`:53`; predicate pins `--seed 6001`). Dead
  parameter; harmless but should be documented or removed.

## 2. C2 — depth (sourced S101 correction note)

Verified positives:
- Raw pin targets a committed capture: `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` present in
  `git ls-files`; `RAW_PIN=1/1`. Error path fail-closed (`C2=ERROR …`, exit 2).
- The pinned quote genuinely exists in committed raw bytes: UTF-16LE
  `文献类型及载体类型标志` at byte offset 24322 of the `.raw` (located in scratch). The committed
  `.txt` rendering is lossy (begins with U+FFFD-mangled OLE magic; contains no `文献类型`), so the
  `.raw` is the only committed locus of the quote.
- The scoped-limit strings exist in the committed entry (`corpus/knowledge/citation-count-semantics-r37.md:5,74-80`),
  last modified round-49 (`git log`: `763b337`).

Findings:

- **C2-1 [CRITICAL] "Base must fail" is violated: the counter passes on pristine base.**
  ```
  $ git archive HEAD | tar -x -C $S/basecopy          # pristine copy of b379919a
  $ python3 corpus/evidence/round60/c2-count.py --root $S/basecopy --work $S/c2work-base
  RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
  C2=PASS   (exit 0)
  ```
  Every checked string is round-49-committed content; the counter references no round-60 entry,
  note, or scorecard. Consequently C2's declared before→after is **unmeasurable**: before and
  after both read `C2=PASS` (measured on the current tree too: `C2=PASS`, exit 0). A claim whose
  own counter cannot fail post-work is not falsifiable as landed.
- **C2-2 [HIGH] Three frozen-predicate requirements are unimplemented.** The predicate requires
  "verify the new entry's exact observation and no overreach against those source bytes" and
  "require the scorecard's declared disposition". The counter (`c2-count.py:13-20`) checks only
  digests, one quote count, and two pre-existing strings; there is no new-entry path, no
  observation-vs-source-byte comparison, and no SCORECARD read anywhere in the file.
- **C2-3 [MEDIUM] `--root` is applied asymmetrically and quote location comes from uncommitted
  bytes.** `raw` resolves under `a.root` but `form` is hardcoded to this repo's ROOT
  (`c2-count.py:13`) — proven by the base run passing while the copy has no
  `.ufo/waves/round-60/s101-open.txt`. `QUOTE/LINE=245` is derived from that uncommitted wave form
  (`FORM_SHA a8e3e7ad…`, differs from the committed round-58 form `9d0191dc…`); the counter never
  decodes the committed `.raw` (UTF-16LE) to locate the quote in committed bytes, contrary to
  "establish … quote locations from committed S101 raw capture".
- **C2-4 [LOW] `--work` accepted and unused; metadata pin is a brittle em-dash string**
  (`:13,17`) — acceptable as a pin, noted only.

## 3. Claim-level review

- **Falsifiability.** C1: falsifiable — executable predicate, measurable before (run1 FAIL today;
  committed R59 false positive), crisp kill rule. C2: as counter-implemented, not falsifiable
  w.r.t. its before→after (C2-1); it is falsifiable only via pin breakage, which tests bytes, not
  the claim.
- **Causal separation.** Verified structurally: the two counters are disjoint files with no shared
  inputs or outputs; C2's entry work cannot affect C1's verdict. The claims' independence sentence
  holds.
- **Scope honesty.** C1's disclaimer ("does not claim the builder itself meets all hazard legs")
  matches observed behavior (default candidate deletes; C1-2). However the claim's After-target
  wording ("rejects the same exact-token forge") overstates what the bytes do (C1-1, C1-3). C2's
  "explicitly records the existing knowledge entry's S101 source-quote limit" describes content
  already committed at round-49 — the round's new-content delta has no counter visibility.
- **L0 reference.** `8d77e6c1` verified open at fleet `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:136,140`.
- **One canonical runtime / rerouting.** Both counters derive ROOT from `__file__` only; no
  re-exec or same-identity rerouting observed; all runs used system `python3`.
- **`resume_continuity_v1`.** No resume paths exist in this lane's scope; nothing to verify (N/A).

## 4. Verdicts (recommendation only — non-binding)

- **C1: predicate satisfiable only by a new builder candidate; counter under-verifies legs (a) and
  (c) as worded.** Recommend recording C1 `unprovable-as-landed` for "rejects the same exact-token
  forge" until the counter (i) requires an observed build product derived from the seeded quote
  (e.g. `spans.tsv`/`S601-1.txt` consistent with the cache bytes) on the candidate leg, and (ii)
  runs the forge through the same candidate path as the builder under test rather than a hardcoded
  stub.
- **C2: counter fails its own frozen predicate (base must fail).** Recommend counter rework before
  any admission: decode the committed `.raw` (UTF-16LE) for quote location, point every input at
  `--root`, add the new-entry/no-overreach check and SCORECARD disposition requirement. The scoped
  note itself is groundable (quote at committed `.raw` offset 24322; rendered at committed
  `corpus/evidence/round59/s101-open.txt:245`); present-day validity/CNKI overreach remains
  explicitly unknown per the claims' own Gate requirement.
- **Freeze SHA: reconcile before closure** (section 0).

## 5. Residual risk and verification gaps

- No LSP server in seat tooling: caller/definition conclusions are text-grep-based (fallback
  recorded per protocol; the zero-caller result is a literal-grep fact, not semantic proof).
- The pinned assignment SHA's origin could not be derived from repo bytes; its cause and timing
  remain open (section 0).
- Sibling wave receipts (`w1/c1-before.txt`, `c1-control-proof.txt`, `s101-receipt.txt`) are
  uncommitted and were treated as non-authoritative context; all C1/C2 evidence above was
  regenerated independently in this seat's scratch.
- I did not audit the round-60 builder work itself (out of seat scope); C1-2 implies any round
  report claiming `C1=PASS` without a new candidate builder would contradict measured behavior.
