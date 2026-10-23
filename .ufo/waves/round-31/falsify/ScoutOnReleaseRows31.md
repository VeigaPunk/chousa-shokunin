# ScoutOnReleaseRows31 — own-work SOURCES rows with recheck on-release, re-read against the tip gate

Round 31, wave 2 falsify. Lane revision read: `ee1024fd492144c9c7b315890fac247543c37208`; gate
`tools/research-gate.sh` SHA-256 `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c`
(the C2 landing gate). Question: after the round-31 change to `verify_claims`, are the anchor and
teaches cells of the own-work rows with `recheck=on-release` still accurate?

**Verdict: holds — 9/9 rows still accurate, zero cell edits proposed.** No row's anchor or teaches
is invalidated by the round-31 change; all nine anchors were located and their described code exists
at the tip with the clause the teaches names.

## Round-31 blast radius (isolation)

`git diff be7b8d8d54962286417465a305fd9a1a7b3b1525 ee1024fd -- tools/research-gate.sh` → 321
insertions / 28 deletions, hunks only at: file header `:23-30,48-70`, `usage` `:340`, `jfield`
`:1092` (+9 lines), `tok_span_all` `:1354` (new), `verify_claims` `:1401-1587`, selftest tail
`:6707`. No hunk intersects `metadata_iso_date/add_days` (`:2448-2516`), `metadata_registry_*`
(`:2518-2700`), `verify_metadata` (`:2711-2960`), the `--json` append block (`:3063-3223`), or
`claim_source_path` (`:1167`). `jfield` is called only from `verify_claims` (`:1422-1440`).
Target rows are also unchanged in `corpus/SOURCES.md` by round 31: `git diff 6d0ae19 ee1024f --
corpus/SOURCES.md` is 3 insertions (S057-S059) only.

Commands run (all from lane root, `TMPDIR=/fast/scratch/hyaku/chousa-r31/w2/ScoutOnReleaseRows31/tmp`):
`TMPDIR=… timeout 1150 bash tools/research-gate.sh --selftest` → exit 0,
`RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)`; log copied to
`.ufo/waves/round-31/falsify/ScoutOnReleaseRows31/selftest-tip.log`.
(`bash tools/research-gate.sh selftest` printed usage, exit 1 — the flag is `--selftest`.)
Read-only git only (`cat-file`, `show`, `diff`, `log`); no installs, no network.

## Per-row result

| Row | Anchor at tip | Verdict |
|---|---|---|
| S001 | setup error `manifest unreadable` at `:3063`; append block opening `# A manifest whose last byte is not '\n'` at `:3177`; selftest cases 134-136 | **still accurate**. Selftest run printed `ok-case 134 json-unterminated-manifest exit=0`, `ok-case 135 json-nul-terminated-manifest exit=0`, `ok-case 136 json-unreadable-manifest exit=2` — same names, same numbers. Append still prepends `$'\n'` when `od -An -tx1` of the last byte is not `0a`. Scope parenthetical verified: the knowledge entry's r24 gate sha `752e4e38…` equals `git show 6572827:tools/research-gate.sh \| sha256sum` (r24 landing commits 6572827/095b90c/d730ae4 all carry it); the tip gate is a later sha, which the row's "round-24 landing revision" scoping already says. |
| S034 | `verify_metadata` `:2711`; one bounded snapshot `read -r -d '' -n` `:2795`; streamed `while IFS= read -r line` parse `:2809`; receipt `corpus/evidence/round26-measure-before.log:2-8` | **still accurate**. `grep -c 'readarray\|mapfile' tools/research-gate.sh` = 0; only per-entry `metadata_lines+=` output rows, no per-line array. Receipt carries the four-shape 8,388,000-byte table, `C1_AMPLIFIED=4/4`, `base=ba333325…`. Teaches ("bounded snapshot can still amplify…parse without a line array…measure output identity and RSS") matches both. |
| S035 | `metadata_add_days` `:2497`; `META_RECHECK_OVERDUE` `:2939`; spec addendum `corpus/evidence/round26-claims.md:132` | **still accurate**. `metadata_add_days` pins `LC_ALL=C`, normalizes with one ERE `^0*([123456789][0123456789]*)?$`, bounds at 7 digits and at 9999-12-31; the overdue finding fires only when `freshness == overdue`, while `on-release` sets `due_date=on-release freshness=event` (`:2936-2937`) and unknown stays `unknown`. The decimal/range addendum is present as the "C2 arithmetic is decimal…" paragraph. |
| S036 | `metadata_registry_load` `:2518`; `metadata_registry_check_source` `:2642`; `META_SOURCE_ROW_MISSING` `:2664`; `META_SOURCE_USEDBY_MISSING` `:2681` | **still accurate**. Status check (`META_SOURCE_NOT_MINED`) and exact repo-relative used-by match with only `./` normalization (`:2677`) are present; findings are warn/metadata, i.e. declared local relationships, as the teaches says. |
| S040 | `FNoTrade.md:115-137` (`### F1 — selftest FAIL at the immutable target` … `the selftest exit will go red.`); base `64eec5d4…` exists | **still accurate**. The fix the teaches names is what the tip harness does: `nverdict=$(grep -c '^RESEARCH_GATE: ' …)` in ~20 sites, and `metadata_asof_usage_accepts` rejects a matcher fault (`((grc <= 1)) && …`). Limit, not an inaccuracy: the report's internal gate line cites (`:6016`, `:390/385`) were measured at the r26 base and no longer resolve at tip; the row's anchor cites report lines, which are immutable. |
| S041 | `FDateAsOfUsage.md:75-86`; `FDateHugeCadence.md:34-44`; base `64eec5d4…` exists | **still accurate**. Both repairs are at tip: `metadata_iso_date` opens with `local LC_ALL=C` (`:2448-2449`) and is what the top-level `--as-of` check calls (`:6920`); `metadata_add_days` replaced the extglob `+(0)` strip with the single ERE (no recursion). |
| S042 | `FRegistryHeaderless.md:41-49`; `FRegistryIdBoundary.md:28-45`; `FRegistryRegistryDeny.md:23-30`; base `64eec5d4…` exists | **still accurate**. Tip resets `id_col/status_col/usedby_col/header_width` on a non-pipe line (`:2588-2591`); S-id scan is exact-token (`grep -oE` then `grep -xE`, `:2650-2652`) and `source_scan=${source_scan#*` occurs 0 times; `is_denylist_fs_path` (`:632`) and citation-pointer `is_denylist_path` (`:638`) remain distinct. |
| S043 | `FC3ValidTable27.md:59`; `IntegTokenCost.md:20`; `FC2Allzero128K07.md:18`; `FC1CorrectUsageWithHelp00.md:7`; checkpoint `dd72641e…` exists | **still accurate**. All four lines resolve verbatim to the named defects (escaped-pipe 5-vs-4 cells, 12-34x cost, `line=${line%$'\r'}` quadratic, verdict/fail-open). All four teaches clauses exist at tip: width from cells after `\|`-preserving split (`:2607-2635`), `grep -xE` prefilter before the id loop, substring CR strip at both read loops (`:2569`, `:2813`), fail-closed matcher (`:6193-6196`; case `metadata-asof-usage-matcher-fault` `:6703`). |
| S045 | `ResNoHarm.md:53-69` = F2 block through its "Smallest correction"; base `11d7c5da…` exists | **still accurate**. `claim_source_path` `:1167` is outside every round-31 hunk; `is_denylist_fs_path "$canon"` still refuses (`:1198`), so "denylist not waived" holds; the report's correction (match relative to `src_root`, `:69`) is the root/ancestor exemption the row calls unapproved, and `SOURCES.md:117-120` still records the parent's non-approval. No live instruction selects or exempts roots: `grep -n exempt AGENTS.md SKILL.md CORPUS.md QUALITY.md` returns only chain/sweep/integrity exemption prose unrelated to path roots. |

## Proposed old→new cell text

None. No anchor or teaches cell is inaccurate at the tip.

## Limits

- Predicate counters were not rerun: this item asks whether the row cells describe the tip
  correctly, and the row anchors that matter (S001's case numbers, the r24-generated behaviour)
  were exercised through the gate's own selftest instead. No claim about C1/C2 counts is made here.
- Historical rows (S040-S045) are revision-scoped records: their reports' internal gate line
  numbers legitimately point at the old checkpoints named in their anchor cells, so they must not be
  used to navigate the tip file.
- Confidence: high for anchors (each located and, for S001, executed); high for teaches (each clause
  located in the tip code, not inferred from prose).
