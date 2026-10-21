# FxSrcElliott — source review (advisory)

Axes: freshness, calibration. Re-opened the primary PubMed abstract for S022 and checked the current registry, round-25 Gate, metadata entry, and source definitions. These are lane-dispatched judgments, not outside closure.

## Findings

- **Medium — S019 `teaches` exceeds its cited scope.** `corpus/SOURCES.md:29` says the periodic decision is a “recorded” act, but the cited Cochrane Chapter IV Key Points say reviews should be assessed periodically to determine whether an update is needed; the cited IV.1–IV.2 guidance does not require recording that assessment. Keep the row mined, but remove “recorded” or mark it as a lane inference. The actual metadata rationale is calibrated: `corpus/knowledge/metadata-screen-r25.md:20-27` labels its derivation from S019/S020 as inference and explicitly says neither source prescribes the header.
- **Low — S022 `teaches` embeds an unlabelled inference.** The Gate quote at `corpus/lessons/round-25.md:71` is an exact 14-word substring of the PubMed abstract’s LSR definition: “systematic reviews that are continually updated, incorporating relevant new evidence as it becomes available.” The abstract confirms the paper’s definition and rationale. `corpus/SOURCES.md:32` has the right `paper` kind, tier A for the original paper’s own definition, narrow scope (not metadata design), and abstract anchor. “the limit case of a short recheck cadence” is a useful inference, not the paper’s stated metadata/recheck rule; label it as inference or narrow `teaches` to the source’s definition. Queued / `used-by —` is appropriate because no knowledge entry uses S022; the Gate is a source-audit quote, not a mined metadata claim.

## Checked decisions

- **S019 mined — agree, with the wording correction above.** Its Cochrane Handbook kind/tier/scope/anchor fit its own periodic update guidance; `used-by` correctly names `corpus/knowledge/metadata-screen-r25.md`.
- **S020 mined — agree.** PROV-O is a primary W3C spec (tier A for the scoped terms); the cited `prov:wasDerivedFrom` and entity-lifetime anchors support derivation and generation/invalidation time facts, not a recheck or verification policy. The metadata entry labels the mapping to its own `source:` / `verified-at:` convention as inference and disclaims a full-header endorsement (`metadata-screen-r25.md:20-27`). `used-by` names the consuming entry.
- **S025 rejected — agree.** The RFC 9111 §4.2 quote in `round-25.md:74` matches the HTTP-cache freshness formula. Its scope is HTTP response caching, so rejecting it as general research-record validity authority is grounded; the flip (explicit analogy paired with a direct method source) is meaningful.

Residual risk: PROV-O’s §3.2 time bounds describe an Entity’s existence, not truth or verification of a knowledge claim; preserve the current inference label. No builds/tests run; none assigned. No installs.

VERDICT: Agree with the S019/S020 mined, S022 queued, and S025 rejected decisions; request the two source-row calibration edits above.