# AttackPrecision — round 48 wave 2: falsification of the frozen 12 held-out correct-bullet cases and the 11/12 floor

ATTACKS: R48-C1 (frozen at `4bbd2348578bb6288c0700dabf37cea04225bfb6`), the `precision-count.py` leg only — the twelve `p01–p06/a01–a06` correct-bullet cases, their HeldOutA provenance, and the `CORRECT_BULLETS_PASS>=11/12` target. Labels and target inspected, not adjusted. Quarantine register rows are the sibling `QuarantineS*` lanes' slice; not re-hand-checked here.

VERDICT: predicate **holds** as frozen (baseline 9/12 < 11/12 reproduced; C1=FAIL exit 1 reproduced), but the set has **three material defects**: (1) provenance — it is a verbatim republish of the already-measured, already-published HeldOutA bodies against a tool that has since changed, not a held-out set for this round; (2) denominator — 3 of 12 cases are mechanism-neutral (cannot trigger rule 5), so engaging precision is 6/9, not 9/12; (3) label a05 is defensible only under one of two readings, and HeldOutA's own count line (2/12) contradicts its table (3 refusals). None of these kills C1; they cap what "11/12" certifies.

## 1. Baseline verified (commands + output)

```
$ git rev-parse HEAD
4bbd2348578bb6288c0700dabf37cea04225bfb6
$ git status --porcelain -- corpus/evidence/round48/ tools/inference-ground.py corpus/fixtures/inference-ground-r47/
(empty — freeze commit is tip, no drift)
$ sha256sum tools/inference-ground.py
9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b   # ≠ HeldOutA's measured 244a1897…
$ python3 corpus/evidence/round48/precision-count.py
p01=PASS p02=PASS p03=REFUSED p04=REFUSED p05=PASS p06=PASS
a01=PASS a02=PASS a03=PASS a04=PASS a05=REFUSED a06=PASS
CORRECT_BULLETS_PASS=9/12  MIN_CORRECT_PASS=11/12  PRECISION_GATE=FAIL   exit=1
$ python3 corpus/evidence/round48/c1-count.py
REFINEMENT_CASES=5/5  CORRECT_BULLETS_PASS=9/12  PRECISION_GATE=FAIL
LEGACY_R47=PASS  C1=FAIL   exit=1
```
Both reproduce `controls/before.txt` exactly; the do-nothing control stands. Attack04 is confirmed dead (no `w1/Attack04.md`; registry entry exists but no report).

## 2. Provenance defect — the set is not held out for round 48

- All 12 bodies are literal copies of the round-47 wave-2 `HeldOutA` probe set (`.ufo/waves/round-47/w2/HeldOutA.md:12-25`), which was measured against tool `1fc5ed19` (sha `244a1897…`). Since then `02d95d3` ("round-47: C1 wave-2 fixes") changed the tool (sha `9d789b34…`): span-side explicit-only negators, `un-` flip respects a preceding negator, `free` removed from `IMPLICIT_NEG`, `UN_NEG_RE` lookahead widened, leaf-key polarity. I diffed it (`git diff 1fc5ed19 HEAD -- tools/inference-ground.py`): none of the five deltas is on a code path any of the 12 cases exercises (no `free`, no `unfit/unpack/…`, span phrases unchanged, `unrecorded` in a01 is `is_neg` before the un-branch, no numerals). So the recycled set still measures the same three defects — but the lesson's own record (`round-47.md` "Held-out measurements … at `1fc5ed19`: false refusals 2/12 … They were not re-run after `02d95d32`") means the *prior evidence* is pre-fix and stale; the frozen counter is now the only current measurement, and it measures a set whose text was already public. Every candidate can be tuned directly on the case literals (`precision-count.py:11-23`) — acceptable for a regression floor, but "held-out precision" overstates it (w1 Attack27 §4–6 made the same point).
- Provenance detail: 11/12 bodies are verbatim HeldOutA; **p01 is reworded**. HeldOutA's table records `no revision can be traced … impossible to verify`; the frozen case reads `no revision can be traced, so this claim cannot be checked`. Same mechanism class (leading `no` + distant `cannot`), both PASS, but the set is not byte-faithful to the evidence it cites.

## 3. Per-case label audit (quote → finding → verdict)

Span polarity ground truth: `spans/S901-1.txt` = "…**no revision is recorded** per sentence" (phrase negated in-span, scope stems `revis`,`recor`); "the release ships a frozen pool" and `spans/S902-1.txt`'s "the archived copy is dated at build" are affirmed (scope `relea,ships,froze,pool` / `archi,copy,dated,build`).

| case | body (frozen literal) | observed | label verdict |
|---|---|---|---|
| p01 | `no revision can be traced, so this claim cannot be checked` | PASS; `no` and `cannot` are in-window negators of `revis` | correct — consistent absence claim |
| p02 | `the frozen pool lacks revision markers` | PASS; `lacks` ∈ `IMPLICIT_NEG` in-window | correct |
| p03 | `this release's revision history is nonexistent` | REFUSED, `INF_POLARITY_FLIP … / revision`; `nonexistent` is in no negator list (`non-`, not `un-`) | label correct (absence asserted by an unlisted absence word); refusal is a false positive — same class as w1 p03 `absent` |
| p04 | `the release cannot show that any sentence has been revised` | REFUSED, `… / revised`; `cannot` is 7 words before `revised`, outside 3-before/2-after | label correct; refusal is the distance false positive (w1 p05 class) |
| p05 | `a published page is distributed without revision records` | PASS; `without` in-window of `revision`/`records` | correct — but HeldOutA's note misattributes the pass ("`without` = listed negator" beside `records`): it is in-window of **both** scope stems |
| p06 | `the pool is unsuitable for revision-sensitive evaluation` | PASS; `unsuitable` matches `UN_NEG_RE` (…able) in-window | correct |
| a01 | `a later page cannot be an unrecorded update` | PASS — but **mechanism-neutral**: no affirmed scope stem is reused (`unrecorded`'s stem is not `relea/ships/froze/pool`; `is_neg` skips it anyway) | correct label; contributes nothing to probe precision |
| a02 | `the pool is stable after its release` | PASS; `pool`,`release` reused, no negator in before-window | correct; engages P2 |
| a03 | `its contents are fixed` | PASS — **mechanism-neutral** (no scope stem; `conte`/`fixe` absent) | correct label; free pass |
| a04 | `snapshotted on the build date` | PASS; `build` reused, no negator | correct; engages P2 |
| a05 | `that date is not the copy's build date` | REFUSED, `the archived copy is dated at build / build` (P2: `not` is 3 words before scope word `build`) | **disputed, defensible only narrowly**: under the intended reading ("the visible date is *not the build date*", i.e. a different proposition than "dated at build") it is a correct bullet over-refused. Read plainly — `that date` = the archived copy's date, and it "is not the build date" — the bullet *does* deny the affirmed phrase, making the label wrong. HeldOutA:24,34 also classified it over-refusal; the ambiguity is why it is a weak held-out member, not why the label fails |
| a06 | `needs a separate timestamp` | PASS — **mechanism-neutral** (no scope stem reused) | correct label; free pass |

Correct/incorrect summary: 11/12 labels are semantically correct; a05's correctness holds only on the charitable reading. No case is a mislabeled flip that would inflate the baseline.

## 4. HeldOutA internal contradiction (evidence-quality defect)

`HeldOutA.md:12` headlines "**refusals 2/12** (p03, p04); every other bullet PASS" — but its own table (`:24`) lists a05 `exit=1`, and `:33-34` says "The other nine bullets confirm" / "Affirmed half: 5/6 pass", which is 3 refusals. The named non-author spotcheck already resolved it to "**exit-level 3/12 incl. a05**" (`round-47-verifier-spotcheck.md:29-30`). The round-47 lesson (`round-47.md:145`) still carries the stale `2/12` and the admission-rule caveat "a counter score does not overrule the external verification's verdict" is what imports that misprint. A falsifier reading only the headline undercounts the defect class the floor encodes (3, not 2).

## 5. Is 11/12 a defensible threshold?

Defensible, narrowly — and weaker than it reads:

- **For:** `≥11` forces a candidate to fix at least 2 of 3 measured false-refusal classes (p03 unlisted absence, p04 distance, a05 scope-ambiguity) while keeping the legacy/refinement/mutation legs green; a do-nothing (9/12) fails; an always-refuse fails. In the frozen C1 the precision leg is not standalone, so w1 Attack28/31's "accept-all passes" attack is contained: an exit-0 tool yields `JUNK_KILLED=0/3`, `LEGACY_R47=FAIL`, `un-prefix-flip`/`repeated-figure` failures.
- **Against:** (a) denominator dilution — a01/a03/a06 cannot trigger rule 5 at all, so the floor's real demand is 8/9 on engaging cases and the headline "11/12" reads as ~92% precision where engaging precision is currently 67%; (b) `returncode==0` pass criterion (`precision-count.py:48`) conflates findings-exit-1 with usage-exit-2/harness error into "REFUSED", and asserts no finding code — a pass for the wrong reason is invisible; (c) the threshold permits shipping *any* 2-of-3 fixes — e.g. adding `nonexistent`-type words + scoping a05's `not` leaves the distance class (p04) permanently refused, the hardest and most natural one; (d) a strictly better candidate that fixes all 3 but loses one of the six current passes to a new mechanism class also prints 9–11/12 with no diagnostic of *which* cases moved — regression-in-passing is undetectable from the aggregate.
- Net: 11/12 is the tightest defensible bound that tolerates one residual known defect; 12/12 would be aspirational (fixes p04 require real scope work), 10/12 would admit shipping two unfixed classes. Keep it, but the claim's "held-out precision floor" wording should be read as "regression floor over a recycled set with an inflated denominator."

## 6. Counterexample (strongest) and smallest safe correction

**Counterexample:** a candidate that adds `nonexistent` (and kin) to `IMPLICIT_NEG` and narrows P2 so `not` before a scope word kills only when no same-stem token intervenes reaches `CORRECT_BULLETS_PASS=11/12` while leaving p04's distance class refused and all legacy legs green — the frozen predicate is satisfied by fixing the two cheapest defects and permanently codifying the third. The counter cannot distinguish that outcome from a principled fix.

**Smallest safe correction (documentation only — no predicate, label, target, fixture, or counter change):** (i) in `claims.md` consumers' reports and the round-48 lesson, quote the precision leg as "9→≥11 of a recycled HeldOutA set, 3 of 12 mechanism-neutral, engaging-precision target 8/9", not "held-out precision ≥11/12"; (ii) correct HeldOutA's count citation wherever it propagates — the measured figure is 3/12 exit-level refusals (spotcheck already records this); (iii) when the round-48 candidate lands, require its report to name which of p03/p04/a05 remain refused — a per-case manifest, which `precision-count.py` could print at zero cost (it already prints per-case lines) but the claim does not require preserving. No label or target adjustment is proposed.

## Evidence bounds

Local only; no fetch (L0 `8d77e6c1` open). Commands run: the two counters above, `git rev-parse/status/diff/log`, `sha256sum`, plus direct verbose runs of `tools/inference-ground.py` on reconstructed p03/p04/a05/p01/p06/a01 entries reproducing the cited FINDING tokens (`/build`, `/revision`, `/revised`). Scratch `/tmp/chousa-r48-AttackPrecision/` deleted at close. No installs.
