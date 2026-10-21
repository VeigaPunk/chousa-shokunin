# ScoutMetadataHeader — fenced metadata, continuation, and header-boundary preservation

Assigned item: C2/C3 ensure fenced metadata/continuation/header-boundary behavior remains
unchanged. Static read-only: I executed no gate, selftest, differential, regression, or probe;
opened no host file and no live process; installed no tools. Base is lane master
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`; line numbers below are that revision and each is
paired with quoted anchor text so a shifted executor clone can relocate it.

Confidence notation: **OBSERVED** = read directly in source/committed receipts; **INFERENCE** =
derived by trace, not executed.

## 1. The only fence/continuation state machine (entry metadata) — OBSERVED

`verify_metadata`, `tools/research-gate.sh:2627-2682`. It is per-entry state, reset at
2627-2630 (`fence_char='' fence_len=0 active_key=''`); the whole function runs under
`local LC_ALL=C` (`:2539`), so every `[[:space:]]`/`[0-9]` test below is ASCII, already
locale-stable on the entry side. Rules are applied in this exact order:

| # | Predicate (exact) | Effect | Line |
|---|---|---|---|
| R1 | line := `${line%$'\r'}` | one trailing CR removed before any test | 2632 |
| R2 | `^[[:space:]]*$` | `active_key=''` — runs **before** the fence branch, so a blank/space-only line clears continuation even inside a fence | 2633 |
| R3 | in fence (`-n $fence_char`) | append raw line to `source_value`/`verified_value`/`recheck_value` only when `active_key` matches; never parse a key, never break on `## `; then closer test and `continue` | 2634-2646 |
| R4 | closer `^ {0,3}(\`{3,}\|~{3,})[[:space:]]*$` | closes only if marker char equals opener char **and** length ≥ opener; whitespace-only trailing allowed; info-string trailing is not a closer | 2640-2644 |
| R5 | opener `^ {0,3}(\`{3,}\|~{3,})(.*)$` | append the opener line to the active value, then enter fence and `continue` (opener is content, not a key) | 2647-2655 |
| R6 | `[[ $line == '## '* ]]` | break. Literal `##` + one ASCII space at column 0 only: `##Claim`, `##`, `##\tX`, and indented ` ## X` do not break | 2656 |
| R7 | `^(source\|verified-at\|recheck):(.*)$` | column-0 key, no space before `:`, case-sensitive; `active_key=''` then set; `source` becomes active **only** under `--registry`; values are replaced, never appended (last key wins) | 2658-2676 |
| R8 | any other line | appended to the active value with a leading newline (`$'\n'"$line"`); continuation is what feeds `META_RECHECK_ROOT_PARENT` and source S-id scanning | 2677-2681 |
| R9 | unclosed opener | stays in fence through EOF; every later line is content, so later keys are never parsed (fail-closed) | 2631/2646 loop exit |

Observable consequences that are existing contract, not accidents:

- Fenced keys cannot satisfy a missing key. Pinned by selftest `metadata-fenced`
  (`:5823`, expects three ABSENT findings and exit 1).
- A fenced `## ` is literal; keys after the closer are parsed. Pinned by
  `metadata-fenced-heading` (`:5967`, expects clean, `METADATA_COMPLETE=1/1`).
- Only literal `## ` ends the region; `##\tLiteral` is not a boundary. Pinned by
  `metadata-literal-heading` (`:5912`, expects `recheck=scheduled` from the line after the
  tab line), plus `metadata-after-heading` (`:5835`) and `metadata-heading-boundary`
  (`:5979`, duplicate `recheck` last-wins then boundary).
- A non-key line such as `note: … --root ..` stays in the preceding `recheck` value.
  Pinned by `metadata-nonkey-continuation` (`:5887`, expects `META_RECHECK_ROOT_PARENT`).
- `source:` continuation is captured only with `--registry`; an indented continuation id is
  scanned. Pinned by `metadata-registry-positive-continuations` (`:6241`, expects
  `findings=0` for `source: citation continuation` + `  S0001`, and `verified-at: 2026-10-20`
  + `  checked the claim` without `META_VERIFIED_AT_BARE`).
- CRLF headers are accepted. Pinned by `metadata-crlf` (`:5841`).
- The entry-side value shape tests downstream are unchanged by this item:
  `verified_state=dated` is prefix-only (`:2698`); `recheck_first` is the first non-space
  token (`:2715`); `metadata_verified_at_bare` is whitespace-only after the date
  (`:2523-2527`, called at `:2710`); due/freshness uses `metadata_iso_date` +
  `metadata_add_days` + strict `asof_days > due_days` (`:2737-2762`).

The independent r25 oracle implements the same grammar: `header_bounds` marks fence lines
outside and cuts at `line.startswith("## ")`; `metadata_values` stops a value at a blank line
or an outside key line and keeps fenced lines as pieces
(`corpus/evidence/round25-meta-oracle.py:26-77`). The r26 differential's `adv-fenced.md`
(`corpus/evidence/round26-registry-differential.sh:142`) and `adv-continuation.md` (`:138`)
are executable shape controls for R3/R6/R8.

## 2. Registry "header" boundary (C3 repair target) — OBSERVED

`metadata_registry_load`, `tools/research-gate.sh:2410-2468`, already `local LC_ALL=C`
(`:2366`).

- G1 table line ⇔ at least two `|` bytes (`*'|'*'|'*'`, `:2412`); one trailing CR stripped
  (`:2411`); outer ASCII trim then at most one leading and one trailing `|` removed
  (`:2417-2421`); cells split with a sentinel and re-trimmed (`:2422-2429`). Empty trailing
  cells are real cells.
- G2 a non-table line while `header_found=0` only resets the candidate (`:2413-2415`;
  **the defect: the three column indices survive**). While `header_found=1` the same line
  `break`s the whole registry scan (`:2413`) — first-table-wins. `corpus/SOURCES.md` depends
  on this: rows 11–52, blank 53, `## Paths` 54; rows after 53 are deliberately not read.
- G3 candidate header: exact cell names `id`, `status`, `used-by` (`:2456-2462`); case
  variants, backticks and `used_by` are rejected; extra columns allowed; duplicate names use
  first index.
- G4 candidate must be followed immediately by a delimiter row whose every cell matches
  `^:?-{3,}:?$` (`:2443-2449`). Current code never compares cell counts (the r26 G01/G02
  defect). A non-separator pipe line resets candidate **and** columns and is then re-scanned
  as a possible header (`:2453-2467`) — the "line-pair" shape, keep it.
- G5 after `header_found`: rows are any later table line; first cell `^S[0-9]{3,}$`, first
  duplicate wins, all other rows ignored (`:2431-2441`).
- G6 grammar errors end in the single existing `die_usage`
  `metadata registry has no table with id, status, and used-by columns` (`:2469`), exit 2,
  zero `META`/`RESEARCH_GATE:` output. The registry is loaded once before the entry loop
  (`:2570-2571`), so no registry shape may become a per-entry finding.
- G7 status quo, preserve unless L1 expands scope: the loader has **no fence and no comment
  state**. A table inside ``` or `<!-- -->` is parsed; a fenced example table can win
  first-table and shadow the real one (r26 FRegistryHeaderless FRH-4 G03/G04, committed as
  an unresolved contract gap). Adding fence awareness here would be a behavior change
  outside the three named C3 failures.

## 3. What each executor must not perturb — ordered hazards

ExecDates (C2), confined to `metadata_iso_date` (`:2295-2308`) and `metadata_add_days`
(`:2343-2359`):

1. Put `local LC_ALL=C` **inside** `metadata_iso_date` (and preferably
   `metadata_add_days`), not only at the CLI site `:6325-6328`. `round27-mechanisms.py`
   counts `C2_locale_unpinned_date_validator` as `'local LC_ALL=C' not in iso`, and the
   probe is named in the claims (`C2` base 2 → target 0). A global `export LC_ALL=C` is not
   needed; the entry loop is already C-scoped and a global change spills into unrelated
   modes.
2. Keep character classes ASCII. `[0-9]` under C is right; `[[:digit:]]` after a locale fix
   is a widening hazard; `[0123456789]` is an explicit alternative.
3. Keep `10#$digits` (after normalization) so `08`/`09` are decimal, not octal; keep the
   `<= 7` bound **after** zero-strip; keep `return 1` → `due=unknown freshness=unknown`
   for out-of-range (no exit, no finding). `metadata_add_days` must remain a pure predicate.
4. Replace `digits=${digits##+(0)}` (`:2348`) with a non-recursive normalizer.
   `[[ $digits =~ ^0*([0-9]*)$ ]]; digits=${BASH_REMATCH[1]}` is the r26-demonstrated
   shape (linear, 128 KiB zeros → 0.19 s in that sandbox). A shell `while` strip is O(n²)
   at 128 KiB and risks the 30 s regression timeout; the `+(0)` extglob recurses into
   SIGSEGV at ~68k zeros (accepted r26 receipt, not rerun).
5. Do not move date work into the header loop or change `recheck_first`/`verified_first`
   extraction, R1-R9, or the downstream predicates. The entry-side failure mode
   FDateAsOfUsage is the unpinned CLI call only; inside `verify_metadata` the locale is
   already C. Keep the exact diagnostic `--as-of must be a valid YYYY-MM-DD date` and keep
   validation before `verify_metadata` (regression requires exit 2 and 0 verdict lines).

ExecRegistry (C3):

1. Minimal header-state repair: at `:2412-2415`, after `header_candidate=0`, also reset
   `id_col`/`status_col`/`usedby_col` (and any new stored header-width variable). Keep the
   `header_found → break` arm untouched (G2). This is what makes `header-break-blank`,
   `header-break-prose`, `reorder-clean`, `reorder-queued` and FRH S01-S05 behave.
2. Width repair: store the candidate header's cell count when setting the candidate
   (`:2463-2464`) and require the delimiter line's cell count to equal it before accepting
   (`:2448`). Count cells **after** the G1 split, not raw pipes: `id | status | used-by` vs
   `---|---|---` (no outer pipes), alignment colons, and CRLF must all still pass. Reset the
   stored width on both candidate-reset paths (`:2453-2454`, `:2466`). A rejected width must
   fall through to continued scanning and ultimately the existing no-table `die_usage`
   (regression requires the substring `metadata registry has no table`); do not add a new
   per-entry finding or echo cell text.
3. `round27-mechanisms.py` also expects the exact sequence `header_candidate=0\n\s*continue`
   to disappear from this function; insert the resets between them (same or separate lines)
   and do not leave that two-line shape.
4. S-id identity: replace the regex+`${source_scan#*"$source_match"}` rescan
   (`:2474-2504`, strip at `:2503`) with a single pass that yields one id per standalone
   token, in textual order, from the **whole** accumulated value. Keep multiplicity
   (`S002,S002` → 2 findings), the absent-row vs not-mined branches, `META_SOURCE_NO_ROW_ID`
   when zero tokens, and 3+ digit `S` ids (4+ valid). A `local LC_ALL=C` in this function is
   a no-op today and makes "standalone ASCII" self-contained. Byte-class tokenization
   (non-`[[:alnum:]_]` → separator) matches the accepted r26 mutation; the alternation
   regex with a correct match-span advance is equivalent if it preserves counts and
   boundaries.
5. Continuation is input, not a parser to change: `source_value` arrives from R8 with
   embedded `\n` and possible empty first value. `adv-continuation.md` and
   `metadata-registry-positive-continuations` require continuation tokens to count; a
   glued-prefix-before-end-of-value case on a continuation line (`source: x S001S003` +
   `  S001`) must yield zero row-missing findings.
6. Do not change used-by semantics (`:2489-2498`): comma split, ASCII trim, repeated leading
   `./` strip only, exact equality with the root-relative entry path. Basename or path
   normalization changes would break the adversarial suite (`adv-basename.md`,
   `adv-dot.md`, `adv-other-usedby.md`, `adv-trailing.md`).
7. Path denylist: the registry and entry call sites are filesystem paths, but
   `is_denylist_path` (`:595-607`) matches `ptr_file_part` (`:573-576`, `${p%%:*}`), so a
   colon earlier in a path hides `/.config/` etc. Add a full-path predicate for
   `metadata_registry_load` raw/canon/fd-canon (`:2375`, `:2382`) and, if in scope, the
   entry raw/canon/fd-canon (`:2584`, `:2591`). Do **not** change `ptr_file_part` or
   `is_denylist_path` for citation pointers: `check_pointer`/`ptr_resolves_meta` keep the
   `path:line` anchor semantics, and r26 FRRD-2/FRRD-5 (existence-vs-refusal ordering,
   refusals before `openat`) must stand. `round27-mechanisms.py` counts three raw
   `is_denylist_path "$path|$canon|$fdcanon"` calls in the registry function and expects 0.

## 4. Independent controls already in-tree (do not weaken)

| Control | Location | What it pins |
|---|---|---|
| `metadata-fenced`, `metadata-fenced-heading`, `metadata-after-heading`, `metadata-literal-heading`, `metadata-heading-boundary`, `metadata-nonkey-continuation`, `metadata-crlf` | `tools/research-gate.sh:5823,5967,5835,5912,5979,5887,5841` | R1-R9 exactly as section 1 |
| `metadata-registry-positive-continuations` | `:6241` | R8 source/verified-at continuation with registry |
| `metadata-registry-*` table cases | `:6157-6258` | G3-G5 (missing/queued/used-by/bare/no-id/duplicate/nul) |
| `adv-fenced.md`, `adv-continuation.md`, 12-column reordered registry | `corpus/evidence/round26-registry-differential.sh:112-152` | fence literal keys + heading, continuation ids, extra/reordered columns |
| `header_bounds`/`metadata_values` | `corpus/evidence/round25-meta-oracle.py:26-77` | same grammar independently; r25 differential AGREE is the metadata-side oracle |
| C3 table/token/deny cases | `corpus/evidence/round27-regressions.py:121-174` | reset-on-break, width equal/±1, reorder, glued/underscore/duplicate occurrence counts, colon deny |
| `C2`/`C3` mechanism counts | `corpus/evidence/round27-mechanisms.py` | locale pin, zero-strip, stale sequence, rescan line, three raw-path calls |

`round26-date-differential.sh:73-81` writes plain three-key headers (`source`/`verified-at`/
`recheck` then blank + `## Details`), so a boundary regression that drops keys would surface
there as `due=unknown` over many cases; it sets no `LC_ALL`, which is why the CLI locale fix
is the one under test.

## 5. New synthetic fixtures I recommend (not created, not run)

All bytes newly generated under an ephemeral dir; expected values are derived statically
from sections 1-2. Each entry is `name → header bytes → expected observable`.

Entry-side preservation (no registry unless stated):

1. `fence-recheck-only` → ```yaml / `recheck: 90d` / ``` / `source: S001` /
   `verified-at: 2026-10-20 checked` / `## Claim` → exit 1, `recheck=absent`,
   `META_RECHECK_ABSENT`, `METADATA_COMPLETE=0/1`. A parser that reads fenced keys flips it
   to scheduled/complete.
2. `fence-heading-literal` → three keys / ```markdown / `## Claim` / ``` / `recheck: never`
   → exit 0, `META_RECHECK_UNSCHEDULED`, `recheck=unscheduled verdict=clean` (the later key
   is read because the fenced heading did not break). A lost fence state gives scheduled/no
   info finding.
3. `unclosed-fence-before-keys` → ``` then the three keys, no closer, EOF → exit 1, all
   three ABSENT findings, `METADATA_COMPLETE=0/1` (fail-closed). An "unclosed opener is
   plain text" parser flips to clean.
4. `heading-no-space` → three keys / `##Claim` / `recheck: never` → exit 0,
   `recheck=unscheduled`. A boundary widened to `^##` keeps `90d` and prints scheduled.
   Same expected for ` ## Claim` (one leading space).
5. `fenced-continuation-rootparent` → `recheck: 90d` / ``` /
   `bash tools/x.sh --root ..` / ``` → exit 0, `META_RECHECK_ROOT_PARENT`, scheduled clean.
   Pins R5/R8 append order.
6. `blank-in-fence-clears` → `recheck: 90d` / ``` / blank / `bash tools/x.sh --root ..` /
   ``` → exit 0, scheduled clean, **no** root-parent finding. Pins R2 before R3.

Registry-side boundary (with a matching synthetic entry):

7. `width-reject-then-valid` → `HDR3` / `SEP2` / `ROW` / blank / `HDR3` / `SEP3` / `ROW` →
   exit 0 clean. Pre-fix the first 2-cell separator is accepted and the queued first row
   yields `META_SOURCE_NOT_MINED`; this pins width + continued scanning.
8. `width-reject-then-headerless` → `HDR3` / `SEP2` / `ROW` / `prose` / `| a | b | c |` /
   `SEP3` / `ROW` → exit 2, `metadata registry has no table`, 0 verdict lines. The rejected
   2-cell separator must leave no width or column state that the later headerless table can
   reuse; note the first `HDR3` never became a found table.
9. `no-outer-pipes`, `alignment-colons`, `crlf-registry` → (a) `id | status | used-by` +
   `---|---|---` + row; (b) `| id | status | used-by |` + `|:---|:---:|---:|` + row;
   (c) standard table joined with `\r\n` → each exit 0 clean. A width check based on raw
   pipes/line length fails at least one.
10. `continuation-token-count` → entry `source: S002` + `  S002`, registry S002 queued →
    exit 1 with exactly two `^FINDING META_SOURCE_NOT_MINED\b` lines.
11. `continuation-glued-prefix` → entry `source: x S001S003` + `  S001`, registry S001
    mined/used-by entry, no S003 → exit 0, zero row-missing and zero not-mined findings.
12. `fenced-registry-status-quo` (observation only, decide before locking) → registry is one
    fenced table with S001 queued → today exit 1 `META_SOURCE_NOT_MINED`, because G7 has no
    fence state. Locking this freezes the FRH-4 contract gap; not required by C3.

## 6. Unrun and unresolved

- No execution of `--selftest`, `round27-regressions.py`, `round27-mechanisms.py`,
  `round25-meta-differential.sh`, `round26-{date,registry}-differential.sh`, or the gate at
  all; every expected value above is static. Main agent owns the single verification pass.
- Not probed: Unicode-whitespace edge between R2/R4 (gate `[[:space:]]` under C) and the r25
  oracle's Python `.strip()` (Unicode-aware); non-glibc regex engines; the exact effect of a
  future global locale pin on non-metadata modes (recommend function-local pins only).
- Registry fence/comment awareness (G7) remains an unresolved contract decision; my advice
  is to leave it unchanged this round because round27-regressions has no such fixture.
- Entry-path colon deny (FRRD-2) is inherited and outside the three named C3 failures;
  the regression only exercises `--registry`. Fixing it is compatible with this report as
  long as pointer semantics stay intact.
- The 187/161 selftest identity counts and the population `METADATA_COMPLETE` values are
  main-agent measurements; I make no claim about them.
