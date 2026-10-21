# ConnectFailures — one record/scope discipline for C1 usage and C3 registry

Seat: `ChousaR27.ConnectFailures` (connector, leaf). Base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`. Read-only static analysis only: no
gate, selftest, regression suite, differential, build, lint, or formatter was
executed. The lane was mid-integration while this was read; the hashes below pin
exactly what was observed (later integration may change them).

- baseline gate (`HEAD:tools/research-gate.sh`, also
  `.ufo/waves/round-27/baseline-research-gate.sh`): sha256
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
- working gate at read time: sha256 `045c073e70c78103e14189350bb06a15ce622ae539fe2b1732f8adad77f7a3f1`
- `corpus/evidence/round27-regressions.py` at read time: sha256
  `3198bf2184637df5715dc5ae4777b7af7b5810c3ba3ae72fcfd0ba3f158aa751`
  (183 lines)

## Assigned item and principle

Connect the C1 usage-record grammar mistake and the C3 registry state mistakes to
the source-vs-claim representation principle, and avoid a second method.

The gate already states and implements the principle: a record counts only at its
declared anchor and inside its declared scope; text that merely mentions the
grammar is source, not a record. Existing precedents in `tools/research-gate.sh`:
a fenced ``## `` is "literal text, not a heading" (`:411-412`); claim spans match
at token boundaries (`:234`, `:346`); `verify-all` counts `^RESEARCH_GATE: `
lines and requires exactly one (`:2832-2839`). C1's harness and C3's parser are
local readers that bypass this rule, in four shapes of the same error:

| shape | mention treated as record | correct record |
|---|---|---|
| C1 harness | `Verdict: RESEARCH_GATE: CLEAN\|DRIFT` inside help (`:385`) matched by `$out != *'RESEARCH_GATE: '*` (baseline `:6016`) | a line beginning `^RESEARCH_GATE: ` |
| C3 header | column names seen in an earlier table/prose line (`:2412-2415`) | `id`/`status`/`used-by` header immediately paired with a same-width delimiter |
| C3 S-id | a consumed literal prefix plus a re-anchored `^` inside glued text (`:2503`) | one whole standalone ASCII token occurrence |
| C3 path | citation-anchor prefix from `ptr_file_part` (`:573-576`) applied to a filesystem path (`:595-606`) | the complete filesystem path that is opened |

Contract quotes: C1 "Count verdict records by anchored `^RESEARCH_GATE: `, not
help-text substrings." (`corpus/evidence/round27-claims.md:5-8`); C3
"Filesystem-path denylist checks must inspect complete filesystem paths, not
citation-anchor prefixes; preserve existing citation-pointer semantics."
(`:13-15`).

## Evidence

1. **C1 production shape.** The integrated patch adds
   `metadata_asof_usage_accepts` at `tools/research-gate.sh:6010` and calls it
   from `metadata_asof_usage_case` (`:6021`). The anchored count is correct
   (`grep -c '^RESEARCH_GATE: '`), the three real cases and diagnostics are
   unchanged (`:6102-6107`), and the newer controls sit after case 187
   (`:6254-6266`), with a help-text accept control and a first-line DRIFT
   reject control. This addresses the r26 receipt
   (`.ufo/waves/round-26/falsify/FNoTrade.md:115-137`) without changing the
   production usage text.

2. **C1 oracle now cannot run on the base archive.** The suite extracts both
   `metadata_asof_usage_accepts` and `metadata_asof_usage_case` and aborts with
   `parser.error` if either is absent (`round27-regressions.py:70-79`). The base
   gate contains zero occurrences of `metadata_asof_usage_accepts` (observed:
   `grep -c` = 0) and defines only the function. Static trace, not executed:
   the base run reaches the `metadata_asof_usage_accepts` loop iteration, finds
   no match, calls `parser.error` (`:78`), and exits 2 **before any `observe`**.
   The suite's own contract says exit 2 is setup (`:4`, `:7-8`), not mismatch.
   So the required "run unchanged on an isolated base archive"
   (`corpus/evidence/round27-claims.md:23`) cannot produce the C1 red-before
   rows, and it also suppresses every C2/C3 baseline row. If the extraction were
   base-compatible, the old predicate would fail the suite's
   `correct-usage-with-help` and `nonrecord-mention-is-not-verdict` scenarios
   (expected helper-script exit 0, old predicate gives 1): the true red-before.

3. **C3 header state and width.** A non-pipe line clears only
   `header_candidate`; `id_col`/`status_col`/`usedby_col` survive
   (`tools/research-gate.sh:2412-2415`). The next pipe line reuses them, and the
   delimiter is accepted without comparing its cell count (`:2443-2467`). r26
   receipts: `.ufo/waves/round-26/falsify/FRegistryHeaderless.md:41-83`
   (headerless acceptance, reorder false negative/positive) and `:85-93`
   (width). Controls expect exactly these shapes at
   `round27-regressions.py:128-133`.

4. **C3 token rescan.** `source_scan=${source_scan#*"$source_match"}` (`:2503`)
   removes the shortest prefix ending in the first textual occurrence of the
   match, not the matched occurrence; when the match ends at `$`, an earlier
   glued copy is consumed and the remainder re-anchors `^`, inventing ids and
   multiplying findings (`FRegistryIdBoundary.md:28-46`). Controls at
   `round27-regressions.py:144-150` require `S002,S002` -> two findings (per
   occurrence), `S002x and S002` -> one, and zero for glued-before-terminal; a
   dedupe set would fail the two-occurrence control.

5. **C3 path predicate.** `is_denylist_path` matches on `ptr_file_part`
   (`:573-576`, `:595-606`), so a filesystem path is truncated at its first
   `:`. Filesystem callers: `:2375` (raw and canon), `:2382` (fdcanon),
   `:2584` (entry raw and canon), `:2591` (entry fdcanon); `:636` checks a
   `readlink -f` result but still uses the pointer predicate. Receipt:
   `.ufo/waves/round-26/falsify/FRegistryRegistryDeny.md:25-30,59-75,91-97`
   (B1-B6). A naive full-path-only replacement is **not monotone**: a synthetic
   registry literally named `k.env:1` is refused at base (`ptr_file_part` =
   `k.env`) but would be opened after a full-path-only swap (CriticPathScope
   CX1). The fix must be the union, not a replacement.

## Affected axes

- **Operability (C1):** the integrated production behavior is right, but the
  independent suite's base run is a setup abort; the final PASS would rest on a
  baseline that never ran. Fixing extraction restores the red-before and keeps
  the 187+controls structure.
- **Calibration (C3):** all three named falsifiers are the same
  record/scope error; the controls already encode the expected per-occurrence
  and width outcomes.
- **Freshness (C2):** untouched. The only C2 constraint is negative: any new
  Unicode/`--as-of` usage control must call the same usage predicate
  (`metadata_asof_usage_case`/`_accepts`), not a fourth predicate, and the
  mode-check order at `:6295-6297` must not move (CriticHarness hold).

## Proposed move (one bounded move)

**Make every reader decide from a record present at its own anchor and scope —
including the oracle, which must anchor on the shipped function that exists in
both revisions, not on a symbol introduced by the fix. Reuse the gate's existing
anchored-record method; add no second predicate, tokenizer, reset path, or
pattern list.**

Application A — C1 (oracle + harness):

1. In `round27-regressions.py:72-79`, treat `metadata_asof_usage_accepts` as an
   optional companion: always require and extract `metadata_asof_usage_case`;
   if the helper regex misses, `continue` instead of `parser.error`. Base then
   extracts the self-contained function (old predicate) and reports the two C1
   mismatches before proceeding to C2/C3; final extracts both and reports zero.
   Expected values and scenarios stay byte-identical; this only removes a
   post-fix shape precondition.
2. Keep the production helper as one predicate authority (already integrated).
   Keep the four gate-selftest controls (verdict, exit, diagnostic, help-accept,
   first-line DRIFT); they must remain after case 187 so ordinals 1-187 are
   unchanged, and each negative control must isolate one clause.
3. Do not add an unanchored or newline-glob verdict check; the only verdict
   predicate is the anchored count, the same text used by `verify-all`.

Application B — C3 (parser, one scope machine):

1. One reset transition, `registry_header_reset`, clears `header_candidate`,
   `id_col`, `status_col`, `usedby_col`, **and** the stored header width. Call it
   at every non-table/break line (`:2412-2415`), when a candidate fails its
   delimiter (`:2454`), and on a partial header (`:2466`). Record the header
   width on the line that sets `header_candidate=1` (`:2463`); accept the
   delimiter only when its cell count equals that width (`:2443-2451`). A
   non-table line after an open table closes it (first-table-wins, unchanged);
   before a table is open, scanning may resume only for a fresh named header.
   No column state may outlive its table.
2. Replace the regex-loop/strip in `metadata_registry_check_source`
   (`:2474-2504`) with one normalization pass, `local LC_ALL=C`, then iterate
   whole words: `source_words=${source_value//[^A-Za-z0-9_]/ }` and keep words
   matching `^S[0-9]{3,}$`. Emit per occurrence (`S002,S002` -> two findings),
   never dedupe, never re-anchor in consumed text. Keep the existing
   status/used-by finding bodies and messages byte-identical.
3. One denylist pattern authority: move the glob body of `is_denylist_path`
   (`:597-605`) into `denylist_match`; keep `is_denylist_path` as the
   pointer wrapper (`ptr_file_part`) unchanged; add
   `deny_fs() { is_denylist_fs_path "$1" || is_denylist_path "$1"; }` so refusal
   is a superset of base. Use `deny_fs` at `:2375` (both operands), `:2382`,
   `:2584` (both), `:2591`, and the canonical target at `:636`. Do not
   `norm_ptr` a filesystem path, do not alter `fdcanon` before
   `metadata_registry_entry_path`, and keep refusal order/messages identical.
   If the claim-source arm (`:1129`, plus a canon check after `:1155`) is left
   unchanged, report that as an explicit residual; do not claim gate-wide
   complete-path denial.

Why this is one move: the same rule predicts the oracle's post-fix symbol
precondition, the stale header, the phantom id, and the colon bypass. It also
keeps the round's proposals compatible: the C1 patch stays as integrated; the
C3 patch uses the critics' smallest shapes, but under one invariant rather than
four independent patches.

## Risks

- Editing the oracle after seeing the patch can look like fitting. Constrain the
  edit to optional extraction; do not change scenarios, expected exits, required
  tokens, counts, or `observe()`. Freeze and hash the suite before the baseline
  and final runs; record both hashes.
- If L1 instead inlines the predicate and deletes the helper, revert the suite
  to a single-function extraction and drive the selftest controls through the
  shipped function via a `$WORK` stub and `SELF` (subshell, read the child's
  `failures` count). That is one predicate and one extraction target; do not
  keep both shapes.
- Control insertion after 187 changes the total to 190; docs must state the new
  total and that 1-187 are unchanged. Namespace-skip lines are `skip-case`, not
  `ok-case`, and move later lines into the legacy161 window; record the skipped
  count and compare `LEGACY_CASES_SHA` only under matching availability.
- C3 width state is itself state: clear it on all three reset paths, and test
  header 3 / prose / 4-cell lookalike + 4-cell delimiter -> exit 2. Preserve
  reordered 4/4 acceptance.
- Switching the open-table close from `break` to a continued scan could merge a
  later table's rows. Keep first-table-wins; resume only when no header was
  found.
- Tokenizer: ASCII classes under `local LC_ALL=C`; `${v//[^A-Za-z0-9_]/ }` turns
  newlines into boundaries (correct); never `sort -u` or an assoc set.
- Denylist: full-path-only regresses `k.env:1`; the union is mandatory. Do not
  copy the glob list (two authorities drift). The `:636` union only adds
  refusals; check case 128 `ptr-deny-symlink` and the 129-132 claim cases stay
  green.
- C2: new usage controls must reuse the same predicate; no fourth predicate;
  keep mode validation before date validation (`:6295-6297`).

## Verification (unrun here; L1 once, after all patches land)

1. Freeze the suite hash; run on an isolated base archive:
   `python3 corpus/evidence/round27-regressions.py --gate <baseline>`.
   Expected after the extraction fix: exit 1 with the C1
   `correct-usage-with-help` and `nonrecord-mention-is-not-verdict` mismatches,
   plus the C3 header/reorder/width/glued/colon baseline mismatches; **not
   exit 2**. The unsafe long-token crash is not rerun; mark that baseline item
   skip from the committed r26 receipt.
2. Final tree: same command, exit 0, `mismatches: 0`, per-claim mismatches 0.
3. `bash tools/research-gate.sh --selftest`: PASS; cases 1-187 identical by
   ordinal and name; controls 188+ ok; record skipped count and
   `LEGACY_CASES_SHA` under the same namespace availability.
4. Isolated mutation controls (private copies, never production): restore the
   old `$out != *'RESEARCH_GATE: '*` -> help-accept control must FAIL; restore
   the literal-prefix rescan -> glued controls must FAIL; full-path-only
   denylist -> a new `k.env:1` refusal control must FAIL; omit width check ->
   `delimiter-too-short`/`-long` must FAIL.
5. `bash corpus/evidence/round26-registry-differential.sh` and
   `bash corpus/evidence/round26-date-differential.sh` on isolated copies;
   frozen metadata checks as applicable; record exits.
6. Static: the suite's extraction must succeed against the baseline gate
   (`grep -c metadata_asof_usage_accepts` = 0 there; function present).

## Touched surface and limits

Only this report was written:
`.ufo/waves/round-27/build/ConnectFailures.md`. No production/test/fixture
edit, no lane Git/jj/index write, no gate/test/selftest/differential execution,
no network, host-secret, `/proc`, strace, mount, namespace, or debugger probe,
and no tool install. Observations are static reads plus text-only regex/hash
checks; the base-run exit 2 and the extraction outcome are traces from code and
are marked as such, not executed evidence. This report does not admit round26,
does not certify criterion-6 semantics, and makes no resource-safety claim.
