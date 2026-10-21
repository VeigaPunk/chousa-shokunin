# ReviewNoTrade — round 27 static review

Axes: operability, freshness, calibration. Reviewed the live diff against base `64eec5d41c7cf7f17f5ce1e968e28b3769952596` and the six named r26 failure receipts only. No execution or verification. The `lsp` device is unavailable (`xd://lsp` returned “No such tool”); literal grep was used only to locate source anchors, followed by source reads. No tools installed.

## Findings

### Critical — C3 denylist still truncates filesystem paths before checking

The gate diff does not change this path. `tools/research-gate.sh:573-596` implements `ptr_file_part` by discarding everything after the first `:` and `is_denylist_path` applies that citation-pointer transformation. `metadata_registry_load` uses it on the raw path, canonical path, and fd-canonical path (`:2375`, `:2382`). Thus a synthetic filesystem path such as `a:b/.config/reg.md` still evades the denylist; r26 observed the registry read and parsed to CLEAN (`FRegistryRegistryDeny.md:23-31,59-75,91-98`).

**Acceptance oracle:** with only newly-created synthetic files, a valid registry at a colon-prefixed denylisted path must be refused with exit 2 and `metadata registry refused: denylist` before registry contents are read; a benign path remains accepted. Preserve citation-anchor behavior: do not globally change `ptr_file_part`/`is_denylist_path`, which also serve citation paths. Use a filesystem-path check that examines the complete path for raw, canonical, and fd-canonical registry identities.

### High — C2 date grammar is still locale-dependent

`metadata_iso_date` still uses `[0-9]` and immediately converts matched text arithmetically (`tools/research-gate.sh:2295-2298`); the r26 CLI call is outside the C-locale scope. The committed receipt observed non-ASCII decimal input accepted by the shape check under UTF-8, then Bash arithmetic diagnostics and exit 1 rather than usage exit 2 (`FDateAsOfUsage.md:51-97`). No C2 change appears in the current gate diff.

**Acceptance oracle:** under inherited UTF-8 locale, synthetic fullwidth/Arabic-Indic and mixed non-ASCII digit dates are rejected with exit 2, the existing diagnostic, no Bash arithmetic diagnostic, and no `RESEARCH_GATE:` verdict. ASCII valid/invalid date controls retain Gregorian/calendar behavior, year 1–9999, and strict `as-of > due` overdue semantics. Keep plain mode unchanged.

### High — C2 leading-zero normalization can still terminate the process

`metadata_add_days` still applies extglob `+(0)` before the length bound (`tools/research-gate.sh:2343-2351`). R26 observed stack failure on long leading-zero cadence text before the guard, including loss of all directory output (`FDateHugeCadence.md:34-57,75-91`). No C2 change appears in the current gate diff.

**Acceptance oracle:** newly-generated 128-KiB leading-zero cadence whose decimal value is representable computes the ordinary due date without termination; all-zero cadence computes zero days; maximum span `0001-01-01 + 3652058d` remains `9999-12-31`; overflow remains `due=unknown freshness=unknown`. Keep the independent date differential’s expectations intact; avoid recursive normalization before bounding.

### High — C3 registry header state and delimiter width remain unfixed

At `tools/research-gate.sh:2412-2415`, a non-table line clears `header_candidate` but leaves `id_col`, `status_col`, and `usedby_col` stale. The separator check at `:2443-2451` validates each delimiter cell but does not compare delimiter width to header width. R26 documented headerless tables passing and column misbinding (`FRegistryHeaderless.md:41-83`), as well as mismatched header/delimiter widths being accepted (`:85-94`). The current gate diff has no C3 hunk.

**Acceptance oracle:** synthetic table-shaped data after a blank/prose/fence break must not reuse a prior named header; without a fresh `id`/`status`/`used-by` header it exits 2 with no verdict. A fresh valid header after a break remains accepted. Delimiter cell count must equal the named header width; mismatches refuse. Preserve existing well-formed registry behavior.

### High — C3 S-id scan can invent and duplicate occurrences

`metadata_registry_check_source` still removes the first literal occurrence of the matched text rather than advancing from the regex match position (`tools/research-gate.sh:2472-2504`). With a glued token before a standalone terminal `S001` (for example `see S001S002 and S001`), the consumed-text rescan can turn glued `S002` into a match or emit duplicate finding lines. R26 recorded false-positive findings and multiplicity inflation (`FRegistryIdBoundary.md:28-45,66-99`). No C3 change appears in the current gate diff.

**Acceptance oracle:** synthetic source values containing glued `xS001`, `S001x`, `_S001`, `S001_`, and `S001S002` plus a later standalone ID yield only the actual standalone ASCII IDs, each occurrence processed once; assert exact finding lines/counts, not only finding-ID sets. Preserve the independent exact `used-by` rule: comma split, whitespace trim, repeated leading `./` normalization only, then literal path equality (`FRegistryExactPath.md:18-24,48-96`).

## C1 static disposition

No actionable issue found in the C1 hunk. The usage predicate now counts anchored `^RESEARCH_GATE: ` records (`tools/research-gate.sh:6010-6013`); original three usage cases remain, and appended synthetic controls cover a help-text positive, wrong exit, missing diagnostic, and actual CLEAN/DRIFT records (`:6257-6267`). This is static inspection only, not a PASS claim. Acceptance remains full selftest PASS, all 187 original case identities retained, and all new controls passing; do not weaken exit-2 or diagnostic expectations (claims `round27-claims.md:5-7`; r26 receipt `FNoTrade.md:115-137`).

## Residual risk

Do not describe the whole registry reader as resource-bounded or fully Markdown/GFM-aware. R26 records pipe-dense registry allocation/time amplification and repeated `source_scan` copying costs (`FNoTrade.md:141-177,181-196`); the registry grammar also has documented fence/example and escaped-pipe limitations (`FRegistryHeaderless.md:85-113`). These remain outside this scoped repair and should stay disclosed.

## Verification gaps

No selftest, date/registry differential, synthetic regression, build, lint, or formatter was run. Main’s one post-integration verification remains required; no result is claimed here.