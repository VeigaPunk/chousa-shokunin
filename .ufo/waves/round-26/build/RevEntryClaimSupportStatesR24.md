# Freshness re-verification — `claim-support-states-r24.md`

- Checked the current admitted entry and the prescribed private clone at prereg base `f361d12e44687841e30ec35710ddb366c6f795e0` (observed `HEAD`). SHA-256 of the entry matched in both trees: `f1e719d1aadd614968898f1034f32c28c7df7fa3f38aa3c71799e3e563064651`.

## Recheck (clone; cwd `/tmp/chousa-r26-RevEntryClaimSupportStatesR24`)

- Exact `recheck:` shell command: `grep -n 'None of the five proves' corpus/README.md` → **exit 0**; one hit at `corpus/README.md:179`, and the full line continues “None of the five proves semantic support, location binding, uniqueness or the source's own truth”.
- QUALITY 13/root-layout corroboration: `bash tools/research-gate.sh verify-metadata corpus/knowledge/claim-support-states-r24.md --root /home/vgpnk/Projects/shokunin` → **exit 0**; `META ... source=present verified_at=dated recheck=scheduled verdict=clean`, `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`. The root was explicitly the fleet root.

## Source and claim check (opened 2026-10-21)

- S006, <https://arxiv.org/html/2605.06635v1>: all quoted anchors still occur verbatim: §3.3 “These dimensions form an increasing hierarchy of verification difficulty.”; §3.3.1 “Link Works assesses URL accessibility without LLM inference.”; §3.3.3 “citations where the source exists and is topically relevant but does not support the specific claims attributed to it”.
- S007, <https://arxiv.org/html/2601.08536v3>: §2.1 quote still occurs verbatim: “this only measures the accuracy of the citations and does not necessarily confirm that the information is correct”.
- Prereg-base `corpus/SOURCES.md:16-17`: both are tier A, `mined`, name the exact entry in `used-by`, and their scopes/anchors cover the limited framework-dimensions and support-vs-correctness claims. The note does not import benchmark results. Its extension of “truth” and application to the gate are explicitly labeled inference (`corpus/knowledge/claim-support-states-r24.md:72-75`). The local known-gaps quote is present at `corpus/README.md:179-180`; local practice anchors `SKILL.md:20-23,41` support the recorded claim-verification and unresolved states.

## Finding — low severity, stale local locator

- `corpus/knowledge/claim-support-states-r24.md:51-52` cites `SKILL.md:103-115` for the byte-exact token-boundary span check and `SKILL.md:112` for “contradicted” being structural, not semantic. In the prereg-base `SKILL.md`, lines 103-117 concern the root-slash boundary and old `emit_finding` behavior, not those claims. The matching anchors are `SKILL.md:119-123` (byte-exact token-boundary span) and `SKILL.md:128-130` (structural, never semantic). The adjacent external-URL/no-fetch statement at entry lines 53-54 is substantiated at `SKILL.md:403-407`, not by the cited 103-115 range. The method claims reverify, but these local citations fail QUALITY 2 until corrected.

## Residual risk and gaps

- Reverification is against the version-pinned arXiv URLs (S006 v1, S007 v3); whether newer arXiv versions exist was not checked. The gate metadata run reports a scheduled cadence, not a computed due date.
- No installs.

VERDICT: STALE — entry lines 51-52 (and adjacent lines 53-54) have incorrect/missing local anchors; the cited external quotes and substantive distinctions reverify. Installs: none.