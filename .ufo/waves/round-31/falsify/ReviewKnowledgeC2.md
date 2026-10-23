# WAVE 2 FALSIFY — ReviewKnowledgeC2 (round 31)

Target: `corpus/knowledge/revision-binding-r31.md` (landed in ee1024f; unchanged since — latest touch per `git log`). Gate under test: `tools/research-gate.sh` working tree bytes, SHA-256 `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c` (matches the landed C2 gate `c23d7537…`); `git status --porcelain` clean for the gate, doc and claims files at review time (only `SCORECARD.md` modified, see F1). Scratch: `/fast/scratch/hyaku/chousa-r31/w2/ReviewKnowledgeC2/` (script `examples.sh`, fixtures `fx/`); no lane writes, read-only git only.

## Method

1. Statement-by-statement read of the doc against `tools/research-gate.sh` verify_claims (r31 block ~1443-1512, refusal `claim_source_path` 1167-1265, `emit_finding` 415-418), claims.md §C2 v2, S058/S059 rows (`corpus/SOURCES.md:68-69`), lessons `## Gate` (round-31.md:47,55-56), SKILL.md checklist item 1 (SKILL.md:66-67).
2. 13 behavioral probes E1-E13 against the landed gate (fixtures under scratch `--root`), including the two assigned edge cases (unreadable file, non-string pin). All commands `timeout`-bounded; gate runs read-only, exit codes recorded.
3. `bash tools/research-gate.sh verify-metadata corpus/knowledge/revision-binding-r31.md --root ..` → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`, exit 0.

## Verified holds (evidence)

- Pin syntax: `^[0-9a-f]{64}$` (gate :1460). Uppercase/63/65/empty/`sha256:`-prefix/non-hex/leading-space all `observed=invalid` + `CLAIM_RECORD_INVALID` "sha256 malformed (not 64 lowercase hex characters)" (E6, 7/7 invalid).
- Non-string pin (number/null/bool/object/array): `json_has_key` true, `json_str` fails → invalid (E4, E5: 5/5 invalid). Doc's "A present non-string `\"sha256\"` is malformed" matches.
- Stale: `observed=stale` + exact finding shape `FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=id=E2 pin=9aed7d04410b actual=e761de488dc7` (E2); fires with span ABSENT and no `CLAIM_SPAN_NOT_FOUND` (E3) — "before and regardless of the span check" holds.
- Byte-exactness: CRLF source with exact-bytes pin → supported (E9); no-final-newline pin → supported, wrong pin → stale (E10). Doc's CRLF/newline paragraph holds.
- Refusal precedence: external source with valid pin → `refused` (`CLAIM_SOURCE_EXTERNAL`, crit), never hashed (E11). "A refused source is never opened or hashed" holds.
- Match → existing span verdict: span present → supported (E1); span absent → `unsupported` with `CLAIM_SPAN_NOT_FOUND`, no revision finding (E12); `expect=unsupported` → `CLAIM_SPAN_UNEXPECTED` as before (E13).
- Unknown keys ignored (E7 CLEAN); absent pin unchanged (selftest case S0 absent, and gate :1503 `[[ -n $sha_present ]]`).
- S058/S059 rows: anchors, teaches, and status match the doc's use (S058 hash/compare/fail-on-no-match; S059 hexdigest, "the page does not say lowercase"); quotes sit under lessons `## Gate` (:47), opened once each by ScribeSrcSRI/ScribeSrcHashlib as the doc records.
- claims.md v2 conformance: precedence list (invalid > refused > stale > span), optional-pin limit wording, SKILL.md landing line byte-identical at SKILL.md:67 directly under item 1 (:66, item text unchanged).

## Findings

**F1 (medium, doc accuracy — dangling reference, 2 sites).** Doc line 4 and line 30 both point to "SCORECARD.md, section 'Round 31'" for the counter's measured result. No such section exists: `grep -En "Round 31|REVISION_BINDING|revision-binding|120/120" SCORECARD.md` → zero matches; last header is `## Planned — round 31 (not started)` (SCORECARD.md:1730, file 1735 lines) at HEAD ad20a66, and the working-tree ` M SCORECARD.md` diff (+3 lines) adds a round-30 network note, not a Round 31 section. The measured C2 receipts live only in `.ufo/waves/round-31/measure/after-c2-run{1,2}.json` (both carry `REVISION_BINDING_MATCH`; not SCORECARD). If the close-of-wave seat lands a Round 31 verdict section, the pointer becomes true; as the doc is landed now, the pointer is false. Fix: point to the measure receipts, or land the section the doc names.

**F2 (minor, doc accuracy — misleading sentence).** "A source whose digest cannot be measured reads `stale` (`actual=unreadable`), never a match" implies an unreadable source reads stale. Observed (E8): `chmod 000` source + valid pin → `observed=refused`, `FINDING CLAIM_SOURCE_MISSING` ("not a readable regular file under allowed roots"), never stale — `claim_source_path` refuses at :1240-1243 (`[[ ! -f $canon || ! -r $canon ]]`) before any hash. The `actual=unreadable` branch (:1504-1506) is reachable only if the file becomes unmeasurable between the `-r` probe and `sha256sum` (a TOCTOU window) or `sha256sum` itself fails. The load-bearing half ("never a match", fail-closed) is correct and the doc's own precedence item 2 states refusal precedence; the sentence should name refusal as the normal outcome of an unreadable file, with `actual=unreadable` as the race-window residual.

## Verdict

**Holds.** Gate behavior matches the frozen contract and every checkable doc statement on all 13 probes; verify-metadata CLEAN. Two doc-level defects (F1 dangling SCORECARD pointer ×2; F2 misleading unreadable-source sentence); no gate, contract, finding-shape, or precedence defect found. No attack on the C2 landing succeeded.

## Limits

- E8 run as uid 1000 (not root); as root the `-r` probe passes and the outcome could differ — untested.
- `actual=unreadable` reachability via the TOCTOU window is [INFERENCE] from code reading (:1240 vs :1504), not orchestrated.
- SCORECARD.md is being edited by sibling seats during this review; F1 is a snapshot at review time (HEAD ad20a66 + then-current working tree).
- Full counter re-runs (P2 seeds) left to the RerunC2A/B seats; this review ran small examples only.
