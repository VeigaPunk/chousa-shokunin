# CorpusAudit — frozen round-60 claim and evidence audit

## Scope and verdict

Read-only audit of the frozen claims, prior committed evidence, and current round-60 counter/source artifacts. No live fetch or edits to claims, counters, lane corpus, or source data. Conclusion: **C1 and C2 do not verify on the available post-wave evidence; both should be reported unprovable/not admitted, not PASS.** This is a scoped evidence review, not a full round admission judgment.

## Freeze integrity

The frozen claim bytes currently at `corpus/evidence/round60-claims.md` hash to `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (`sha256sum corpus/evidence/round60-claims.md`). This differs from the assignment's asserted immutable SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. File left untouched. The named base commit `b379919a873e7080a31ef92c7002f55f5374e2c6` exists, but `git show <base>:corpus/evidence/round60-claims.md` reports the path absent; it cannot validate these claim bytes. **Observed discrepancy; cause, timing, and intended bytes unresolved.** Do not silently substitute the observed hash for the expected one or assert immutability is established.

## C1 — operability / counter verdict integrity

Frozen C1 requires the safe candidate path with foreign-file preservation, a pinned round-55 destructive control, and an exact-token injection mutant scored as failure (`corpus/evidence/round60-claims.md:7-11`). The pre-work receipt reports `INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`, exit 1 (`.ufo/waves/round-60/c1-before.txt:1-8`). This is a valid baseline stop, not evidence of the after-state.

The current implementation cannot substantiate the claimed injection-rejection leg. `corpus/evidence/round60/c1-count.py:37-44` classifies `candidate_safe` when the child returns zero and leaves the seeded foreign file intact; captured output is not read for verdict derivation. Yet its injected mutant merely prints `=PASS` and exits zero (`:58-63`), so it too is classified safe; `forge_blocked` is then true because the test rejects only `forged_safe` (`:60-63`), and the same result can satisfy `candidate_ok` (`:68-75`). The independent post-dispatch critic reproduced a PASS/exit-0 counterexample with this no-op token printer (`.ufo/waves/round-60/w1/C1CounterCritic.md:5-19`); CounterProbe independently explains the same state conflation (`w1/CounterProbe.md:3-14`). Therefore the displayed `INJECTION_REJECTED=1/1` is not evidence the frozen mutant-fails condition holds. This does **not** show that stdout/stderr are directly parsed, nor does it establish any broader builder security result.

The non-author reports identify a concrete gap: the mutant must emit the exact token while independently failing the required safe-path observation, and the counter must distinguish that from candidate success; candidate success itself needs a positive observable beyond return code plus sentinel preservation (`C1CounterCritic.md:30-32`; `IntegrityCritic.md:5-15`). No repair or after-work pass is established in this audit. **C1 verdict: not verified / unprovable against the frozen predicate.**

## C2 — depth / S101-scoped note

Frozen C2 requires a new scoped correction note, exact observation and no overreach checked against the committed S101 capture, citation/metadata and declared disposition; its base must fail because the round-60 entry is absent (`corpus/evidence/round60-claims.md:13-17`). The current `c2-count.py` instead sets `ENTRY` to the pre-existing `corpus/knowledge/citation-count-semantics-r37.md` (`:8,13`), checks broad metadata/scope substrings (`:17-20`), and does not test a new round-60 note, exact observation/overreach, QUALITY disposition, or the parsed `--work` value. `--root` does not isolate the text form: `form` is fixed to the script checkout's `ROOT` while raw and entry use the supplied root (`:5-8,12-16`). Thus these checks do not enforce the frozen base-fails or lane-copy predicate. C2CounterAudit reports the baseline counter run printing all flags and `C2=PASS`, exit 0, while no round-60 note is required (`.ufo/waves/round-60/w1/C2CounterAudit.md:5-18,25`). IntegrityCritic independently identifies missing exact-note, disposition, and root-isolation checks (`w1/IntegrityCritic.md:17-25`). **C2 verdict: not verified / do not admit a new knowledge entry on this counter PASS.**

The bounded source observation is supported by offline evidence only: `s101-receipt.txt:1-6` records URL, 2026-10-27 access date, raw and text-form digests, and the located line-245 quote `c. 文献类型及载体类型标志；`; the quote says what the committed captured copy states, not current validity or CNKI implementation. `w1/S101Reopen.md:5-17` preserves that boundary and notes the entry's prior quote-limit. This source observation does not cure C2's missing round-specific admission proof. No external fetch made.

## Prior evidence and mistake signal

The earlier round-59 lesson recorded both the absent pre-dispatch claims freeze and the R58 false-positive/token-verdict defect (`corpus/lessons/round-59.md:25-33`); round-58 lesson records the prior counter's inability to represent its positive state and says no C2 entry was admitted (`corpus/lessons/round-58.md:24-27`). Current round's C1/C2 counter defects are further distinct counterexample evidence, but this seat makes no corpus lesson edit and does not claim a fix. These reports are evidence for the non-verification findings, not a substitute for a landed repair or independently adjudicated round closure.

## Evidence boundary

Observed paths and line references above are lane-local and resolve from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Read-only inspection only; no tests/counters were run by this seat, no network access, no installs, and no git/jj mutation. Scratch was explicitly created at `/fast/scratch/hyaku/chousa-r60/CorpusAudit/` and removed before handoff.
