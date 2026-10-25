ATTACKS: round-48 candidate scan across sibling lanes (receipt re-verification, polarity/negation checks, byte-faithful captures, held-out precision fixtures)
VERDICT: holds — none of the three round-48 candidates absorbs live sibling ground; two reusable sibling mechanisms identified (tameshi registry-replay, mado held-out oracle suite).

Scope: chousa SCORECARD.md:2528-2534 (round-48 plan). Sibling lanes scanned (read-only): audio, game-dev-2d/3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi. No network, no mutations, no tools installed. Scratch: none needed (read-only).

## 1. Receipt re-verification tooling (round-48 candidate a: repair the four round-39/40 receipts failing gate-sha256-mismatch)

- tameshi `tools/registry-replay.py` (lines 4-36): replays frozen registry requirements at a pinned revision; refuses publication when any runner row did not hold (RUNNER_NOT_HELD); takes the runner digest from the clone copy that actually executes. This is the exact "replay from pinned rev, digest of executing bytes" shape chousa QUALITY 68 (corpus/QUALITY.md:662-697) does with `git archive` + `c1-count.py`. Reusable directly as a second leg if round 48 wants receipt re-verification beyond the four failing receipts.
- tameshi `tools/receipt-measure.py` (lines 5-37): splits runner_sha256 vs instrument_sha256, pins FROZEN_GATE_SHA / FROZEN_MEASURE_SHA constants, HISTORICAL sha256→label table. Pattern for distinguishing "the gate that ran" from "the receipt bytes" — same naming chousa uses in `record_sha256`/`gate_sha256` (corpus/lessons/2026-10-16-verify-all-composition.md:196).
- kama `tools/round33-gate-receipts.py` (lines 3-42): capture+audit receipts from a pinned lane revision; audit replays each case from its pinned source revision; CASES dict pins expected exit codes and stdout per case. Reusable as the fixture-regression harness for the four failing receipts (each expected `VERIFY: ok` at adding commit, refusal at tip).
- kama `tools/gate-registry-check.py` (lines 4-17): sibling analog of chousa c2-count — registers every tracked counter against SKILL.md tables, verdict line `registered R unregistered U defective D`, exit 0 iff U=D=0. Same contract text as chousa C2 (`REGISTERED=93/93 UNREGISTERED=0`); no conflict, both are lane-local instruments.
- mori `tools/mori-census.sh` --pin/--drift with volatile-field masking (`DRIFT_VOLATILE_SPECIAL` line 2771, mask regex line 2789, note line 2929). chousa SCORECARD:109 already names "mori-style pins" as the sibling pattern; relevant to drift design, not to the four failing receipts.
- kotodama `tools/gates/frozen/handoff-packet-check/r9-pre/freeze.txt` (lines 6-21): baseline pins revision + source sha256 + copy sha256 + snapshot; repin dirs exist per round (frozen/round-18/repin-d2, round-20, round-23). Closest sibling precedent for byte-faithful capture pinning (round-48 candidate c).
- kumitate `scripts/receipt-attest.mjs` (lines 3-14; v3 nonce ledger + GNU sha256sum text-mode sidecar) and `scripts/receipt-evidence.mjs` (round-58 reproduction + descending nonce-sweep, proxy-check.mjs:476): attestation-grade; beyond chousa's integrity need. kumitate round-52 connector (ConnOverlap.md:27-34) already documented that chousa's seat refuses kumitate pins — same homonym boundary applies to round 48.

## 2. Polarity/negation checks (round-48 candidate b: held-out precision fixtures for the polarity probe)

- No sibling implements windowed text-negation detection. audio's polarity is signal-level: `corpus/knowledge/2026-10-12-threshold-calibration.md:33` ("comparator polarity follows code only") and negative-control tables in `corpus/fixtures/measure_audio.py` lines 21412/23628 (r84a/r85a classifier negatives). Different domain; not reusable, do not confuse.
- kotoba negation/polarity grep hits are knowledge prose (e.g. corpus/knowledge/skill-selection-rules-round50.md), not tooling.
- Therefore candidate (b) targets a genuinely unclaimed gap: the named limit in chousa `tools/inference-ground.py:55` ("a correct bullet whose negator sits outside the window is refused") has no sibling mechanism. The fleet's closest precedent is mado's held-out oracle suite (below), reusable as organization/scoring pattern, not as polarity logic.

## 3. Held-out precision fixtures and shortcut guards

- mado `.ufo/waves/round-20/precision/` (CaseAdoptW2-*.jsonl oracle cases), `tools/mado-tripwire.py:1011` ("held-out fx8/fx9"), SCORECARD:1341-1343 (precision P 66/66; recall controls held-out 0/12 → 0/12; full suite incl. held-out 172/187 → 174/187) and SCORECARD:1455 (score rubric `10 * matching new oracle cases / frozen new oracle cases`). The fleet's existing held-out oracle precedent; the fixture/case format and scoring rubric are portable to (b).
- kaidoku `tools/round-34/replay-gate.py` (lines 4-30): REPLAY_GATE_REFUSED + mandatory registered positive control; refuses freezing a counter when any reader shortcut meets the target (input size/label/whole-file digest/record order). Directly portable as a guard that a held-out polarity fixture set is not learnable by shape — matches (b)'s motivation.

## Overlap verdict

- (a) stays chousa-local if it remains a repair of `verify-receipts.py` in git-archive copies (QUALITY 68). It would absorb sibling ground only if generalized into a fleet-wide receipt re-verifier: tameshi registry-replay and kama round33-gate-receipts already own replay-from-pinned-rev; kumitate owns attestation-grade; kake owns receipt-timestamp parsing (S032/S033/S034; scripts/receipt_replay.py; corpus/knowledge/static-canonical-preflight.md:159-166).
- (b) is disjoint from every sibling (text-level windowed negation is unclaimed); mado's held-out suite is precedent, not overlap.
- (c) byte-faithful captures: kotodama freeze.txt bytes pattern and audio's byte-exact re-derivation (reports/round-83/r83-scribe.md:28,201) are precedents; no sibling owns a chousa `merge/chousa/` assimilation.

## Risks

- kumitate's round-52 connector already routes the homonym boundary for `receipt`/`pin`; round 48 prose must not claim a fleet-first receipt re-verifier (tameshi/kama/kumitate/kake prior art).
- If (b) borrows mado's scoring rubric verbatim, cite mado SCORECARD:1455; otherwise the "first held-out precision fixture set" novelty sentence would be false in fleet terms.
- kaidoku replay-gate.py references "QUALITY 67" of its lane; not a chousa criterion — no cross-lane criterion semantics.

## Verification (run)

- `grep -rln "polarity|negator|negation" <sibling>/tools/ <sibling>/scripts/` → no sibling tooling hits; kotodama frozen inputs are data artifacts, not detectors.
- `grep -rln "receipt" <sibling>/tools/` → tameshi (receipt-measure.py, receipt-window.py, registry-replay.py), kama (round33-gate-receipts.py), kaidoku (round-33 timestamps), kotodama (gates/frozen), kumitate (scripts/), mori (census pins).
- `grep -rn "held-out" mado-shokunin/tools/mado-tripwire.py` → line 1011; `ls mado-shokunin/.ufo/waves/round-20/precision/` → CaseAdoptW2-*.jsonl suite.
