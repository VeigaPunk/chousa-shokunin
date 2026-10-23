# Round 36 w1 — RevClaimPredicate: P1/P2 prose vs counter code (reviewer seat)

Seat: `L1chousa36.RevClaimPredicate` · 2026-10-23 · leaf, read-only on production files.
Target: `corpus/evidence/round36/claims.md` P1/P2 versus `corpus/evidence/round36/c1-count.py`
and `corpus/evidence/round36/c2-count.py` — label strings, thresholds, pass computation,
exit condition, field names. Plus fresh-seed re-derivations of both predicates.

## Identity pins (sha256sum, run 2026-10-23)

| File | sha256 |
|---|---|
| `tools/research-gate.sh` | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` (landed, matches brief) |
| `.ufo/waves/round-36/controls/base-gate-r36.sh` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (r35 blob, matches brief) |
| `corpus/evidence/round36/c1-count.py` | `3fefffe745ed10d2fd06c4c3cc9073ab7bfb46dd82e32c166976fd3aaf4c35be` |
| `corpus/evidence/round36/c2-count.py` | `3c699aab0614fff78f88d1b8570166439014a360ee378c0a143bf204a96e4362` |
| `tools/argv-witness.py` | `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` |
| `tools/mechanism-witness.py` | `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` |
| `controls/ctl-c2-stub-pass.py` | `ee0e0cc7d38a191443e948daeed3bfe3b9bc8b474d61114dcaeeeb75ca86fbb7` |
| `controls/ctl-c2-stub-fail.py` | `c8dab587d553b477560457e6d45d2cf2569310e0d66e389646c2c5788d871dfb` |

`git rev-parse master` → `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (wave base, matches brief).

## P1 — claim prose vs c1-count.py code

Scenario inventory check: exactly 14 `score("…")` calls, S1–S14 (`c1-count.py:452,459,479,486,493,502,516,528,541,576,609,622,636,653`), mapping 1:1 onto the fourteen classes in claims.md C1's sentence (PATH shim→S1, BASH_ENV→S2, PATH-less→S3, relative/missing/non-GNU→S4/S5/S6, distinct-path→S7, default-pin LIVE `--version`→S8, override-beats-shim→S9, per-record attribution→S10, manifest hash shim→S11, C-locale→S12, pin echo→S13, drift token→S14).

| Claim prose (claims.md, read 2026-10-23) | Code (c1-count.py) | Agree? |
|---|---|---|
| "prints `ENGINE_SWAP_CANARY=14/14`" | L72 `LABEL = "ENGINE_SWAP_CANARY"`, L73 `TOTAL = 14`, L664 `print("%s=%d/%d" % (LABEL, passed, TOTAL))` → byte-exact `ENGINE_SWAP_CANARY=14/14` | YES |
| "Code condition: `passed == 14`" | L659 `passed = sum(1 for r in results if r["pass"])`; L660 `holds = passed == TOTAL and ref_a and ref_b` (`TOTAL=14`) | YES |
| "and both reference runs sane" | L435–437 `ref_a` (fixture A: rc 1, drift, K1 supported/match, K2/K3 unsupported/mismatch); L552–553 `ref_b` (fixture B: rc 0, no drift, all supported/match); L445–446 aborts `RuntimeError("reference run A not sane…")` if ref_a fails | YES |
| "receipt label `predicate_holds`" | L662 receipt key `"predicate_holds": holds`; L677 `return 0 if receipt.get("predicate_holds") else 1` | YES (it is a receipt key next to `label`, not the label itself — wording only) |
| "a scored run whose `gate_sha256` differs from the receipt's is not the claim's measurement" | L662 `"gate_sha256": sha256_file(gate)` recorded in every receipt — checkable | YES |
| Kill rule "weakening its fixture (reference no longer sane) is not a measurement" | `ref_a`/`ref_b` inside `holds` (L660) — a weakened fixture forces `holds=false` even at 14/14 | YES |
| "no committed run … against the landed gate prints a lower count" | not code-observable (meta-condition over the receipt corpus); committed set: only 14/14 ×2 vs landed gate (see below) | N/A (meta, satisfied by committed set) |

**P1 "same sentence?" verdict: YES.** Every prose token (`ENGINE_SWAP_CANARY`, 14, `passed`,
reference-run sanity, `predicate_holds`, exit-on-predicate) has a byte-identical or
semantically identical code counterpart. No threshold or field-name divergence.

## P2 — claim prose vs c2-count.py code

| Claim prose (claims.md) | Code (c2-count.py) | Agree? |
|---|---|---|
| "prints `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass`" | L272–274 `print("%s=%d/%d OUTPUT_EQUIV=%d/%d LANDED_ATTRIB=%s RENAMED=%s" % (LABEL, separated, len(SWAPS), output_full, …))`; L54 `LABEL = "WITNESS_PER_RECORD"`; `len(SWAPS)==5` (L55–56) → byte-exact signature | YES |
| "separated == 5" | L259–260 `separated = sum(1 for n in SWAPS if …["output_full"] and …["witness"] == "fail")` | YES |
| "output_equiv == 5" | L258 `output_full = sum(1 for n in SWAPS if receipt["variants"][n]["output_full"])`; receipt key `output_equiv` (L268) | YES |
| "landed attribution covers every record" | L230–231 `landed_attr_ok = isinstance(landed_attr, dict) and landed.get("unattributed") == []`; receipt key `landed_attrib` ∈ {pass, absent, fail} (L269) | YES |
| "the renamed control passes" | L261–262 `renamed_ok = bool(…["output_full"] and …["witness"] == "pass")`; `RENAMED = "V6-renamed-matcher"` (L57); receipt key `renamed` ∈ {pass, fail} (L270) | YES |
| Kill rule "any variant that is not output-full … must not count as separated" | `separated` requires `output_full` AND fail (L259–260); `renamed_ok` requires `output_full` (L261) | YES |
| Kill rule "a renamed-matcher run the witness kills" | `renamed_ok` requires witness `pass` on an output-full V6 (L261–262) | YES |
| five classes "python-exact, environment-keyed, stderr-forging, one-call-for-show, body-replaced" | L55–56 `SWAPS = ["V1-python-exact","V2-env-keyed","V3-witness-forge","V4-one-call-for-show","V5-body-replaced"]` — same five, same order | YES |
| "predicate_holds=true" / exit | L263–265 `holds = (separated == len(SWAPS) and output_full == len(SWAPS) and landed_attr_ok and landed.get("witness") == "pass" and renamed_ok)`; L290 exit 0 iff holds | PARTIAL — code has a **fifth arm** `landed.get("witness") == "pass"` that the prose code-condition line does not state (Finding F3) |

**P2 "same sentence?" verdict: YES on the printed signature and the four stated code conditions;
with one unstated extra arm in `holds`** (`landed witness == "pass"`, L264). The printed
four-field signature cannot express that arm: a hypothetical run with full landed attribution
but `witness=="fail"` on the landed gate would print the exact P2 signature with
`predicate_holds=false`. Direction: code strictly stricter than prose; no committed receipt
exercises the gap (see F3). Both field spellings and value vocabularies match byte-for-byte.

## Findings (severity-ordered; none affect counter behavior)

**F1 — calibration, low (docstring contradicts frozen claim + committed receipt).**
`c2-count.py:36-38` (accessed 2026-10-23): "separates only 3/5 (V3 and V5 pass it)". The frozen
claim (claims.md C2 Before) says 2/5 with V2, V3, V5 passing, and the committed receipt
`.ufo/waves/round-36/measure/c2-before-legacy-s36001.json` says `WITNESS_PER_RECORD=2/5` with
`"V2-env-keyed": [9,9,"pass"]`, `"V3-witness-forge": [9,9,"pass"]`, `"V5-body-replaced": [9,9,"pass"]`
(only V1, V4 fail). The receipt and claims.md agree; the counter's header comment is wrong about
V2 and the count. Header comment only — `SWAPS`/`holds` logic is untouched. Fix: one-word
erratum or comment correction in a future counter generation; do NOT edit the committed counter.

**F2 — calibration, low (docstring arithmetic).**
`c1-count.py:14-15` (accessed 2026-10-23): "the ten demonstrations of `.ufo/waves/round-35/`
plus the three routed gate defects" — 10+3=13, but `TOTAL = 14` (L73) and claims.md plus the
committed receipt `c1-before-s36001.json` name FOUR routed defects (S11–S14 all FAIL).
Header comment only.

**F3 — frozen-predicate precision, low.**
`c2-count.py:263-265` `holds` includes `landed.get("witness") == "pass"`, which neither the P2
"Code condition" sentence ("separated == 5 and output_equiv == 5 and landed attribution covers
every record and the renamed control passes") nor the P2 kill rule mentions. Unexercised by any
committed receipt: `c2-stubfail-s36001.json` shows the nearest case (`LANDED_ATTRIB=fail
RENAMED=fail` at 5/5 separated, `predicate_holds=false`) — its failure is already covered by
stated arms. Residual exposure: only the pass-attribution-but-fail-verdict edge above.
Recommend a claims.md erratum adding "and the landed gate's own witness verdict is pass" to the
code-condition line.

**F4 — kill-rule letter vs committed controls, low.**
P2 kill rule: "Any run below 5/5 separation … kills C2." The round's own committed negative
control `ctl-c2-stub-pass.py` run (receipt `c2-stubpass-s36001.json`, gate `a7d3922c…`) prints
`WITNESS_PER_RECORD=0/5` against the landed gate — by the letter, that kills C2, while
claims.md itself commits the control as evidence the counter is honest. Kill rules are plainly
meant to apply to scored candidate measurements, not named negative controls; one erratum
sentence ("controls excluded") would close this. P1's analogous clause is not exposed (no
committed c1 run against `a7d3922c…` below 14/14).

No MEETS finding: no output-equivalent engine scored 14/14 in S1–S9/S11–S14 fixtures, no
witness bypass passed P2, and the do-nothing control scores 10/14 and 2/5 as claimed. The
one-call-for-show limit (C1/C2 shared, stated in claims.md Limits) is confirmed by design:
`V4-one-call-for-show` is separated only because it skips calls for some records
(`c2-fresh-s36311.json`: `attrib=2` vs 9 records); a call-for-show engine that calls for every
record remains outside C2's power — as disclosed, not argued away.

## Independent fresh-seed re-derivation (this seat)

Both against the landed tree (`master` = `700bd5fc…`, gate sha `a7d3922c…`), scratch
`C1_TMP/C2_TMP/WITNESS_TMP/TMPDIR=/tmp/hyaku/chousa-r36/w1/RevClaimPredicate`, `timeout 1700`:

1. `python3 corpus/evidence/round36/c1-count.py --gate tools/research-gate.sh --seed 36301 --receipt .ufo/waves/round-36/w1/RevClaimPredicate/c1-fresh-s36301.json` → exit **0**, prints `ENGINE_SWAP_CANARY=14/14`, all 14 scenarios PASS (S7 `matcher_calls: 4` observed on the distinct-path recorder; S11 `true_gate_sha` = landed sha; S14 `GATE_DRIFT: -GATE_GREP`, rc 1). Wall 4.56 s.
2. `python3 corpus/evidence/round36/c2-count.py --gate tools/research-gate.sh --witness tools/argv-witness.py --seed 36311 --receipt .ufo/waves/round-36/w1/RevClaimPredicate/c2-fresh-s36311.json` → exit **0**, prints `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass`; V1–V5 all `output=9/9 witness=fail`, V6 `output=9/9 witness=pass`. Wall 19.31 s.

Receipts: `c1-fresh-s36301.json` sha256 `fb83c8ebbcf830b15787f033f9c63303acfc0f74d43d4095e733e873e7ba20e4`;
`c2-fresh-s36311.json` sha256 `dfab316156f8e5e143a1facf2a9733f46e9d22ad339467fd5e787c53391b2482`.
Both record `gate_sha256=a7d3922c…`, `predicate_holds=true`. Seeds 36301/36311 are fresh
(no 36001/36011/36021 reuse). Committed corpus cross-check: no committed run against the landed
gate prints lower than the claimed counts, outside the two named stub controls (F4).

## Files opened (all 2026-10-23)

`.ufo/waves/round-36/w1-briefs/RevClaimPredicate.md`; `corpus/evidence/round36/claims.md`;
`corpus/evidence/round36/c1-count.py` (lines 1–100, 376–680); `corpus/evidence/round36/c2-count.py`
(lines 1–60, 179–294); `.ufo/waves/round-36/measure/` (8 receipts, summarized);
`.ufo/waves/round-36/controls/` (listing + sha256); no production file modified.

## Commands run (verbatim, exit codes)

- `sha256sum tools/research-gate.sh .ufo/waves/round-36/controls/base-gate-r36.sh corpus/evidence/round36/c1-count.py corpus/evidence/round36/c2-count.py tools/argv-witness.py tools/mechanism-witness.py` → exit 0
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → exit 0, `700bd5fc…`
- receipt-summary `python3 -c …` over the 8 committed measure receipts → exit 0
- the two counter runs above → exit 0 / exit 0
- `sha256sum` over the two fresh receipts + controls → exit 0

## Verdict

**VERDICT: PASS.** P1 and P2 are faithfully encoded: label strings, thresholds (14/14, 5/5),
field names (`OUTPUT_EQUIV`, `LANDED_ATTRIB`, `RENAMED`), pass computations, reference-run
sanity, and exit-on-`predicate_holds` all match the frozen prose; both predicates independently
re-derived `predicate_holds=true` on fresh seeds 36301 (c1) and 36311 (c2) against landed gate
`a7d3922c…`. Four low-severity calibration defects found, all documentation-precision, none
behavior-affecting: F1 (c2 docstring 3/5 vs receipt 2/5), F2 (c1 docstring "three" routed
defects vs four), F3 (unstated fifth `holds` arm: landed witness pass), F4 (P2 kill-rule letter
condemns the round's own stub-pass control). Recommend errata for F1–F4; no claim blocked.

## Residual risk / verification gaps

- One fresh seed per claim (not two) from this seat — the second fresh seed per claim is the
  executors' lanes (36321/36331/36341 pool); the freeze requires two per claim across the wave.
- F3's edge (landed attribution full while witness verdict fail) was reasoned from code, not
  constructed — no fixture built for it; building one would require a witness that fails the
  landed gate while reporting complete attribution, which no committed control does.
- The c1 docstring/c2 docstring fixes are deliberately NOT applied (committed counters are
  frozen evidence); they belong to the lane's erratum process, not this review seat.
