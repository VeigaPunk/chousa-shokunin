# ScoutRegistryFirst — C3 registry policy preservation (static)

Seat `ChousaR27.ScoutRegistryFirst`, round 27 attempt 1. Base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`. Author-lane advice only.

**Method:** static code reading and committed receipts. No gate, selftest,
regression script, oracle, differential, shell probe, `/proc` read, strace,
mount or debugger was run. Round-26 failures are accepted as ground truth from
their committed reports; nothing was reproduced. Every fixture described below
is synthetic and suggested, not executed.

**Assigned item:** C3 — preserve the duplicate-ID first-row and first-table
policies; document the scope and keep it from broadening.

## 1. Observed state at write time

- `metadata_registry_load` is `tools/research-gate.sh:2361-2469`; `local LC_ALL=C`
  is 2366.
- The lane working tree carries C1's usage-harness hunks only: `git diff -U0 --
  tools/research-gate.sh` shows four hunks beginning at 6010/6021/6029/6108 and
  **no hunk in 2361-2469**. The registry anchors below are exact in the lane
  tree now. `patches/ExecUsage.patch` exists; `patches/ExecRegistry.patch` does
  not, and the `ExecRegistry` clone was clean at base when checked.
- Parser facts, observed:
  - 2412-2416: a line with fewer than two `|` is a table break. Once a table is
    accepted it ends the scan; before that it clears only `header_candidate`,
    leaving `id_col`/`status_col`/`usedby_col` stale (the reported leak).
  - 2431-2441: row loop under `header_found`. 2433-2434 `[[ -z
    ${META_REGISTRY_STATUS[$row_id]+x} ]]` stores the first row for an id and
    ignores later rows. 2437-2438 store the trimmed raw cells.
  - 2443-2451: candidate followed by an all-dash pipe line is a header. The
    separator test `^:?-{3,}:?$` never compares cell counts.
  - 2453-2467: a non-separator pipe line clears the candidate and indices, then
    the same line is re-scanned for the three names; `if ((x_col < 0))` keeps
    the first occurrence of a repeated header name.
  - 2469: no accepted table exits 2 with the existing message.
  - 2408: the two global arrays are re-declared on every load.

## 2. Policies that must survive the C3 patch

| policy | enforcer (current lines) | independent control |
|---|---|---|
| P1 duplicate id → first row wins, later rows ignored | 2433-2434 | selftest `metadata-registry-duplicate-first-row` (research-gate.sh:6246-6256; base 6221-6231); differential `first-duplicate`/`second-duplicate` (round26-registry-differential.sh:117-118); oracle `records.setdefault` (round26-registry-oracle.py:57) |
| P2 first **accepted** table is authoritative; no later table contributes rows or overrides columns | 2413 break plus `header_found` set once at 2449 and never cleared | none — gap (§5) |
| P3 first occurrence of a duplicated header name binds the column | 2455-2461 `if ((x_col < 0))` | none |
| P4 header names are exact, case-sensitive `id`/`status`/`used-by` after ASCII trim | 2418-2429, 2462 | every registry control |
| P5 a data row's id is exactly `^S[0-9]{3,}$`; other cells skip the row | 2433 | `adv-long-id` / four-digit differential fixtures |
| P6 rows are harvested only until a non-table line; a dash row is just a non-matching row, not a stop | 2412, 2431-2440 | none (divergence in §5) |
| P7 one finding per standalone S-id occurrence; no dedupe | 2472-2507 scanner, strip at 2503 | r27 `two-real-occurrences` expects 2 (round27-regressions.py:149) |

The r26 `FRegistryHeaderless` defect and the required repairs do not require
changing P1-P7. Written as a rule: **a break discards a header *candidate*; a
break after `header_found` is terminal.** The r27 control `reorder-clean`
(round27-regressions.py:130, exit 0) confirms the first half: a candidate
broken by prose is not a table, and scanning continues to the next fresh named
header. No control asks the second half to change.

## 3. Minimal change shape, and why it leaves P1/P2 intact

Suggested edit locations, for the integration owner (not applied by this seat):

1. In the non-table branch (2413-2415) reset `id_col=-1; status_col=-1;
   usedby_col=-1` and the new width local, in addition to
   `header_candidate=0`. Keep `((header_found)) && break` **before** the reset.
   Do not clear `header_found`, and do not `continue` past the break.
2. Record `header_width=${#cells[@]}` where `header_candidate=1` is set (2464).
   In the candidate branch require `${#cells[@]} -eq header_width` in addition
   to the all-dash test. On mismatch, take the existing discard path (2453-2454)
   and keep scanning; do **not** call `die_usage` with a new message. The final
   no-table branch (2469) already supplies the expected diagnostic
   (`metadata registry has no table`), which round27-regressions.py:135-141
   requires for the `delimiter-too-*` controls.
3. Compare widths through the already-split `cells` array, after the same
   one-leading/one-trailing-pipe strip and ASCII trim used for rows. Comparing
   raw pipe counts would reject valid no-outer-pipe tables.

Expected outcome of that shape (by reading, not run): `header-break-blank`,
`header-break-prose`, `delimiter-too-short`, `delimiter-too-long` exit 2 with
zero verdict lines; `reorder-clean` stays 0; `reorder-queued` stays
NOT_MINED; `valid-table` stays 0; the duplicate-first-row control stays
NOT_MINED. The r26 S01/S02/S03 class becomes exit 2 and S04/S05 bind the right
columns.

For the S-id scan (2472-2507), the preservation invariants are: word characters
are `[[:alnum:]_]` under C locale, so `_` is **not** a boundary
(`underscore-glued`, line 146, expects 0 findings); one finding per standalone
token, no set/dedupe (`two-real-occurrences`, line 149, expects 2); no id from
either side of a glued run (`glued-before-terminal`, 144); `META_SOURCE_NO_ROW_ID`
only when no standalone token exists; finding code, severity `warn`, surface
`metadata` and message text unchanged. Set `local LC_ALL=C` in the scan function
itself so the ASCII contract does not depend on dynamic scope from
`verify_metadata`. Do not use a tokenizer that maps `_` to a separator: that
would turn `_S002` into a valid id and flip `underscore-glued` to rc 1.

## 4. Scope that must not broaden

The following are unresolved grammar questions in the r26 receipts (FRH-4) or
observed quirks, not part of the C3 repair. Changing any of them would alter
which table or rows are accepted and is outside this ticket:

- fence-aware registry parsing (a fenced example table still shadows the real
  one; FRH-4 G04);
- 4-space indented-code rejection (G05);
- HTML-comment or blockquote awareness (G06/G08);
- merging later tables, "best table" search, or refreshing `header_found` after
  a break (P2);
- adopting the oracle's `strip('|')` cell split instead of the one-pipe strip;
  G10/G11 are known gate-vs-oracle differences and the gate's stricter reading
  is existing behavior;
- stopping row harvesting at an all-dash separator row (P6/§5);
- changing header-name case/backtick rules, used-by comma/trim/`./` rules
  (2489-2500), finding codes, severities, or refusal strings;
- deduplicating S-id occurrences.

## 5. Coverage gaps and suggested synthetic controls

- **First-table (P2) has no control.** Every existing registry fixture has one
  table. Suggested independent control for `corpus/evidence/round27-regressions.py`
  (synthetic temp root, no host files): table A accepts `S001` as mined with
  `used-by` naming the entry; a prose or blank break; table B also lists `S002`
  mined with the same `used-by`; the entry cites `S002`. First-table policy
  expects exit 1 with `META_SOURCE_ROW_MISSING ... source_id=S002`; a parser
  that resumes scanning after the break reports clean. This discriminates the
  policy, whereas a second `S001` row is masked by P1.
- **Duplicate-row cardinality.** The selftest checks the finding substring and
  verdict count, and the differential compares finding-ID sets
  (round26-registry-differential.sh:196-215), so a rewrite that stored both
  duplicate rows and emitted the finding twice would pass both. An r27 control
  counting `^FINDING META_SOURCE_NOT_MINED` = 1 on the existing duplicate shape
  would guard P1's observable cardinality.
- Existing coverage is otherwise adequate for P1 (selftest + differential +
  oracle), P4/P5 (all fixtures) and P7 (r27 harness counts).

## 6. Denylist boundary map (cross-check for the same patch)

`is_denylist_path` (595-606) matches globs against `ptr_file_part` (573-576),
which truncates at the first `:`. Filesystem-path callers that must move to a
raw full-path predicate: 2375 (`$path`, `$canon`), 2382 (`$fdcanon`), 2584
(`$file`, `$canon`), 2591 (`$fdcanon`), and 636 (`$canon` in
`ptr_resolves_meta`). Pointer-shaped callers that must keep the truncating
wrapper: 621 (anchored `$p`), 650, 1129, 1598, and the direct `ptr_file_part`
use at 902. `claim_source_path` checks only the pointer form (1129) and then
opens `$canon` without a denylist recheck (FRRD-2); adding one is a safeguard
change on a currently-CLEAN class and needs an explicit decision, not an
incidental one.

Preserve the refusal order at 2370-2375 (`not found`/`not a regular file`
before `denylist`, FRRD-5), the exact strings (`metadata registry refused:
denylist` at 2407), and the fact that a colon in an ordinary pathname is not
itself forbidden (round27-regressions.py:169).

## 7. Confidence, unknowns, unrun checks

- **High confidence** in the line-level readings and in P1/P2/P3/P6 as written
  above; all quoted behavior is a direct trace of the cited lines.
- **[INFERENCE]** that the §3 shape keeps every r27 expectation. Nothing was
  executed, and the `ExecRegistry` patch did not exist when checked.
- **Unknown / decision for L1:** whether a width mismatch followed by a valid
  later table should be skipped (oracle-compatible, recommended) or fatal. The
  r27 controls cannot distinguish them; the oracle `continue`s
  (round26-registry-oracle.py:37-39).
- **Unknown:** the adjacent-table divergence. Two tables with no intervening
  non-table line: the gate harvests the second table's data rows with the first
  table's indices (2413 does not fire; 2431 reads them), while the oracle stops
  at the second separator row (oracle:50-53). No control exercises it; do not
  "fix" it under C3 because it changes accepted rows.
- **Unrun:** `bash tools/research-gate.sh --selftest`,
  `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`,
  `bash corpus/evidence/round26-registry-differential.sh`, the oracle, and any
  source/mount/proc probe. L1 should run the first three once after
  integration; note the differential compares finding-ID sets and therefore
  cannot catch duplicate emission counts.

Correction (append-only): §5 cites `round26-registry-differential.sh:196-215`
for the set comparison; the per-entry finding-ID set construction is 213-215
and the equality tests are 225-226 and 244-255.

Inherited-limitation note (append-only, per the C3 claim): the fence/indent/
comment/blockquote grammar gaps, the adjacent-table row-harvesting divergence,
and the absent first-table control are inherited parser limitations that this
repair does not resolve. They must be reported as limits; nothing here supports
a whole-gate safety claim. Same for resource behavior: the consumed-text strip
loop is replaced by exact token scanning, but no memory/time measurement was
made, so no resource-safety inference is claimed.

Anchor drift (append-only): integration continued after this report was
written; a fourth usage-harness hunk landed at 6257 and the duplicate selftest
case is now at 6240-6250 (identity `metadata-registry-duplicate-first-row`,
currently 6248). The registry parser (2361-2469) remained hunk-free on recheck,
so the parser anchors stand; cite the selftest/differential case identities, not
their line numbers, once integration is complete.
