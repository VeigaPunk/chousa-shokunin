# FxSrcDCMI — source review

Axes: freshness (fresh source reopening); calibration (scope and claim fit).
Reviewed the full private checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a`; measured `tools/research-gate.sh` SHA-256 `63a39282b614a6e4189e535d685bb00a3c7269e5720299c6e089bf5512fd9da8`.

## Findings (Low)

- `corpus/lessons/round-25.md:68` locates S019's quote at Cochrane “Key Points,” but that passage says “Cochrane reviews should be assessed periodically to determine whether an update is needed” (13 words; current page, Key Points). The Gate quote adds “All”; the exact 14-word sentence appears in §IV.1, not Key Points. The S019 row anchor includes §IV.1 (`corpus/SOURCES.md:29`), so the source and periodicity claim remain supported; correct the quote location or quote Key Points verbatim. The entry's source locator at `corpus/knowledge/metadata-screen-r25.md:3` inherits the same location mismatch.

## Source decisions

- **S023 — AGREE queued.** Fresh read of DCMI Metadata Terms confirms the Gate quote is a verbatim 10-word substring at §2, `/terms/` `source` Definition: “A related resource from which the described resource is derived.” (`corpus/lessons/round-25.md:72`; source: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#source). The same page defines `modified` as “Date on which the resource was changed” and `valid` as “Date (often a range) of validity of a resource” (§2, `#modified`, `#valid`). It identifies itself as a DCMI Recommendation, issued 2020-01-20. Thus `spec`/tier A is defensible for these definitions; scope and anchor are bounded to the three term definitions, explicitly not a freshness/verification policy; `teaches` is supported. `queued` and `used-by —` fit: no knowledge entry consumes S023 (`metadata-screen-r25.md:3-27` cites S019/S020 only; corpus search found S023 only in registry/path/Gate records, not knowledge).
- **S019/S020 — AGREE mined for the bounded use in the metadata screen.** The entry labels its key-design rationale an “inference,” says it is within each row's scope, and states neither source prescribes the header (`metadata-screen-r25.md:20-27`). Cochrane supports periodic review currency; mapping that to `recheck:` is explicitly the lane's inference. PROV-O §3.1/§3.2 supports derivation and entity existence bounds, not a verification timestamp or header policy; that mapping to `source:`/`verified-at:` is also explicitly an inference, not full-header endorsement.
- **S025 — AGREE rejected.** The quote at `round-25.md:74` is the exact §4.2 HTTP-cache equation (5 whitespace tokens; https://www.rfc-editor.org/rfc/rfc9111, §4.2). The source defines HTTP response freshness, not research-record validity; tier C/rejection is well scoped. Its flip is meaningful because it permits only a labelled analogy paired with a directly relevant method source, rather than accepting RFC 9111 as policy authority (`SOURCES.md:35`; `round-25.md:79-82`).

## Residual risk and verification gaps

- PROV-O's generated/invalidation times are entity lifecycle bounds, not a claim that a record was verified at that time. The knowledge entry's explicit inference and no-header-endorsement caveat keep its use bounded (`metadata-screen-r25.md:24-27`).
- Full-pin history preserves both packaging failures: `0fc037e` omitted `tools/research-gate.sh` (prose said 154 cases while bundled gate was SHA prefix `752e4e38…`/136 cases), and `d8c8cff` still omitted `corpus/evidence/README.md` (`round-25.md:111-133`). Full source review used `e93ac711…`; its scoped diff from `0fc037e` adds the packaging-correction section to the lesson. No gate or selftest was run for this source-only assignment.
- LSP unavailable: `read xd://lsp` returned “No such tool”; no LSP references/definitions/diagnostics were available. Literal searches were only used to locate source-row occurrences, not as semantic proof.
- No installs.

VERDICT: Agree S023 queued, S019/S020 mined under the entry's explicit inference boundary, and S025 rejected; flag only the S019 quote-location correction above. Advisory, not outside closure.