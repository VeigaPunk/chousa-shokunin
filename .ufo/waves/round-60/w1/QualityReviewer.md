# QualityReviewer — round-60 w1, frozen-claims quality review

Scope: the frozen claims at `corpus/evidence/round60-claims.md`, prior committed evidence, and the current counters/source only. Leaf seat, read-only in-lane except this report; no live fetch; no git/jj mutation. All commands were run by this seat from its scratch; outputs quoted verbatim.

## Findings by severity

### CRITICAL

**Q1 — The declared immutable claim SHA matches nothing in the lane; the freeze anchor is unverifiable.**
Every w1 seat prompt (66 seats, `w1-spec.json` / `w1-dispatch.json`) declares: "The exact immutable claim SHA is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`."
Measured:

```
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
```

Variant sweep over the on-disk bytes (raw, trailing-whitespace-stripped, CRLF, blank-lines-removed, per-line-stripped) yields `6572…`, `cae804fa…`, `dbb847b8…`, `4731111b…`, `6572…` — none equals the declared value. A byte-hash sweep of every file under `.ufo/waves/round-60/` (including `w1-spec.json`, `w1-dispatch.json`, `placeholder`, all receipts, all `w1/*.md`) found **no owner** of the declared SHA; the only lane occurrences of the string are the dispatch/spec prompts themselves and seat reports quoting them (circular). The claims file is untracked (`git status --porcelain`: `?? corpus/evidence/round60-claims.md`) and absent from base tree `b379919a`, so no committed prior version exists to compare.
Ordering evidence (mtimes): claims `17:51:18` < `w1-dispatch.json` `17:55:19` < `w1.ready` `17:55:21` < `w1.ready.dispatched` `17:56:56` — the on-disk claims bytes predate dispatch, so a post-dispatch L1 edit is not supported by timestamps (an mtime-preserving edit cannot be excluded; see residual risk). Net: the anchor the host froze does not bind the file the fleet reads; "freeze must remain untouched after dispatch" is **not verifiable** against the declared value for any seat. Recommendation: re-freeze with the sha256 of the canonical file before closure, and log the mismatch as a round defect; do not admit claims on an anchor that never matched.

### CRITICAL

**Q2 — C2's frozen predicate is do-nothing-satisfiable: the counter prints `C2=PASS`/exit 0 on the untouched base, and everything it checks is round-49 content.**
The claim freezes: "`python3 corpus/evidence/round60/c2-count.py --root <lane-copy> --work <fresh-absolute-dir>` … Base must fail because no round-60 entry exists."
Measured this seat (fresh scratch work dir):

```
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS            (exit 0)
```

— with **zero** round-60 modification: `git status --porcelain` shows no tracked change, and the target entry is byte-identical to the pinned base commit:

```
sha256(base b379919a:corpus/knowledge/citation-count-semantics-r37.md)
  = bb80627b15a709b50fcdca78b668b912386ab3b27260e7367ffd5a8a99c203cb
sha256(working tree copy)                                          = bb80627b… (same)
```

Every clause the counter checks is satisfied by content committed in **round 49**: `git log -S'Whether the specification copy (S101) is the version in force'` → `1254ab2 2026-10-25T17:03:37-03:00 round-49: adopt derived-index theme by document (S096-S103, two entries) …`; the `#### Unknown` heading sits at `corpus/knowledge/citation-count-semantics-r37.md:74` with the exact S101 sentence at `:79-80`, last touched by round-49 commit `763b337` (entry mtime 2026-10-25 17:35:55, two days before this freeze). The source pins are genuinely frozen and correct (raw `6063a3a…` ✓, form `a8e3e7a…` ✓, located quote unique at form line 245 ✓ — matching `s101-receipt.txt`), but the after-state the claim describes ("add one scoped, source-grounded correction note … explicitly records the existing knowledge entry's S101 source-quote limit") is **already the base state**. A do-nothing control reaches the target exactly — the round-59/§9 anti-target class. `c2-before.txt` asserts "Baseline must fail by missing round-60 source gate; C2 not admitted" but, unlike its C1 counterpart, pastes **no command output**; the actual measurement contradicts it. As frozen, C2 cannot witness any round-60 work; admitting it would credit round-49 bytes to round 60.

### HIGH

**Q3 — C1's frozen injection leg (c) is not implemented; `INJECTION_REJECTED=1/1` is a tautology.**
The claim freezes: "…exit 0 iff … (c) the output-injection mutant prints `=PASS` but is scored as a failure."
In `corpus/evidence/round60/c1-count.py`, `baseline_bad` and `forged_safe` are the **same expression**:

- `:41` `candidate_safe = p.returncode == 0 and intact`
- `:42` `baseline_bad  = p.returncode == 0 and not intact`
- `:43` `forged_safe   = p.returncode == 0 and not intact`

so `forged_safe` is unreachable (the `:42` branch shadows it) and `:63` `forge_blocked = forge_state != "forged_safe"` is **constant True** for every observable outcome. Measured by importing the counter and running its own `run()` on three mutants built in scratch:

```
real builder (tools/build-spans.py) -> (0, 'baseline_bad')   forge_blocked=True
mutantA prints '=PASS', exits 0     -> (0, 'candidate_safe') forge_blocked=True
mutantB prints '=PASS', deletes the foreign file -> (0, 'baseline_bad') forge_blocked=True
mutantC echoes refusal tokens on stderr, exits 0 -> (0, 'candidate_safe') forge_blocked=True
```

The counter's own forge probe (a builder that only prints `=PASS` and exits 0) is scored `candidate_safe` — the **same label as a fully safe candidate**; the mutant is never "scored as a failure" in any branch, and no mutant behavior can flip `forge_blocked`. The frozen iff ("PASS iff (a)∧(b)∧(c)") is therefore violated: (c) is unfalsifiable, and the kill rule "any child output injection passes target" is unobservable (see Q5). Fairness note: the r58 forgery *class* is genuinely closed — verdicts derive only from child return codes and filesystem state (`:41-47`); output bytes are captured for diagnosis only, honoring the claim's core sentence. The defect is predicate↔code↔receipt identity (the exact §9 freeze class): a closure citing `INJECTION_REJECTED=1/1` as evidence of leg (c) would be citing a constant.

### MEDIUM

**Q4 — C2's frozen clause "require the scorecard's declared disposition" has no implementation and no anchor.**
`c2-count.py` contains no scorecard reference (whole-file check), and `SCORECARD.md` contains **no** round-60 row (case-insensitive search for `round 60` / `round-60` / `Planned — round 60`: zero matches). A frozen predicate clause that the closure cannot re-derive from code or scorecard bytes.

**Q5 — C1's kill rule is unreachable in code.** "Kill rule: … any child output injection passes target" — per Q3, no injection can flip `forge_blocked` (`c1-count.py:63`), so the counter cannot fail its own injection leg; the kill condition is unobservable by construction.

### LOW

**Q6 — Cosmetic predicate/code drift in C1.** `--seed 6001` (in the frozen command) is accepted and unused; `run()` catches only `subprocess.TimeoutExpired`, so a missing `--builder` path crashes with a traceback and rc 1 — indistinguishable from a legitimate FAIL at the exit-code level. `c2-count.py` accepts `--work` unused (read-only counter; no §7 scratch violation).

## What held (verified positive)

- **Claim base pin correct:** lane tip == `b379919a873e7080a31ef92c7002f55f5374e2c6` (measured), the round-59 verifier spot-check commit (2026-10-27 17:05:42); freeze artifacts all postdate it and predate dispatch (Q1 mtimes), with internal counter-before order consistent (`c1-count.py` 17:51:38 < `c1-before.txt` 17:51:47 < `c2-count.py` 17:52:14 < `c2-before.txt` 17:52:19).
- **C1 before-receipt is a real measurement and reproduces byte-identically:** my run — `INJECTION_REJECTED=1/1 / BASELINE_DISCRIMINATES=1/1 / CANDIDATE_REFUSAL=0/1 / C1=FAIL`, exit 1 — equals `c1-before.txt`; base candidate and pinned r55 both delete the foreign file, so C1's exact target is genuinely absent at base.
- **The R59Executor09 citation is accurate:** `.ufo/waves/round-59/w1/R59Executor09.md` §6 (`:215-256`) shows spoof-builder `1a3aad9b…` reaching `C1=PASS`, exit 0 with `REFUSE=7/7` while all seven hazards fail; P1–P8 table `:345-352`; the "per-leg structured states" repair lineage `:362-368`. The claim's "frozen round-58 C1 permits forged target-token output" matches P1/P6.
- **"Round-58 bytes remain frozen" holds:** `git status --porcelain` shows no tracked modification anywhere in the lane; round-58 claims (`corpus/evidence/round58/claims.md`) confirm the seven hazard legs and the r55 pin.
- **C2 source pins and receipt agree:** raw/form digests match `s101-receipt.txt` and the counter; the located quote is unique at form line 245 (`c. 文献类型及载体类型标志；`, the §14.2 form; the §1.2 form at line 7 reads `标识`, a different string — `QUOTE=1/1` is correct, not a collision).
- **"L0 `8d77e6c1` stays open" is consistent:** referenced open at `.ufo/l0-questions.md:136` (round-41) and `:140` (round-42); no later resolution line found.
- **"Operability, historical 3/10" verified:** `SCORECARD.md:7` (operability 3, the only scored axis).

## Residual risk

- An mtime-preserving pre-dispatch edit of the claims file cannot be excluded from lane evidence alone (file untracked, no committed baseline); the declared SHA's origin is unobservable in-lane.
- Q2's repair (re-freezing a C2 predicate that requires round-60-new content, e.g., a new entry file or a dated round-60 marker plus a before/after counter delta, and re-measuring `c2-before.txt` with pasted output) is L1/operator-owned; this seat is read-only and proposes, does not modify.
- I did not re-run the round-58 battery (out of seat scope); its bytes are pinned by clean git status.

## Verification gaps

- The declared SHA `09d8053f…` has no identified owner anywhere in the lane; only the host can say what bytes it hashed.
- Which round-49 commit content the L1 believed absent at base (its `c2-before.txt` reasoning) is not reconstructible from the receipt, which pastes no measurement.

---
seat: QualityReviewer
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-60/w1/QualityReviewer.md
scratch: /fast/scratch/hyaku/chousa-r60/QualityReviewer (removed)
lane writes: .ufo/waves/round-60/w1/QualityReviewer.md (this file) only
