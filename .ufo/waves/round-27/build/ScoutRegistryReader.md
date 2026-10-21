# ScoutRegistryReader — C3 registry parser state, token identity, full-path denial

Seat `ChousaR27.ScoutRegistryReader` (scout, leaf, static read-only). Round 27 attempt 1.
Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`; base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`.

Observed state while writing this report:

- `tools/research-gate.sh` is 6376 lines, sha256
  `8ee706b29a6c013db5459a70ada2c07eba387788707a3bde7c40a96c75ac4f8f`. The working
  tree diff contains only C1 usage-harness edits at `:6007-6120`; every C3 line below
  is byte-identical to the r26 target `0e9784bd…` (base gate sha256
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`).
- `corpus/SOURCES.md` already carries the own-work registry row S042 for this class
  (working-tree diff, registry block after S039).
- `ExecRegistry`'s clone at `.ufo/waves/round-27/work/ExecRegistry` was clean at
  `64eec5d` with the same base gate hash when inspected; no C3 patch existed yet.

No code, gate invocation, selftest, or regression script was executed. No LSP device is
mounted (`read xd://lsp` → “No such tool”); locations are literal-search plus line-range
reading, not semantic proof. No installs or updates.

Assigned item: C3 — registry-header state leaking across non-table lines, S-id
consumed-text rescanning, and filesystem-path vs citation-pointer denylist identity.

Grounding quote (17 words): “Require fresh named headers after breaks, matching
header/delimiter widths, standalone ASCII S-ids without invented or duplicate
occurrences” — `corpus/evidence/round27-claims.md:15`.

Accepted ground truth (not rerun): `.ufo/waves/round-26/falsify/FRegistryHeaderless.md`,
`FRegistryIdBoundary.md`, `FRegistryRegistryDeny.md`, plus the r26 lesson rows
R26-M7/M8/M9 at `corpus/lessons/round-26.md:179-181`.

---

## 1. Header state and width (FRegistryHeaderless)

Defect, by code reading:

- `tools/research-gate.sh:2412-2415` — a non-table line clears only
  `header_candidate`; `id_col`, `status_col`, `usedby_col` keep their values from an
  earlier header candidate. The next `|`-bearing line is then treated as a header
  candidate because the stale `>= 0` test at `:2463` succeeds regardless of its cells.
  A following delimiter row sets `header_found=1` and rows are read with the stale
  indices (false accepts; column misbinding in both directions).
- `:2443-2451` — a delimiter row is accepted without comparing its cell count to the
  header's. Falsifier G01 (2-cell delimiter under a 3-cell header) and G02 (4-cell
  delimiter) are accepted today; the regression expects exit 2.

Minimal correction (all state local to `metadata_registry_load`):

1. Add `header_width=-1` to the `local` list at `:2363-2364`.
2. At `:2414`, reset all of: `header_candidate=0 header_width=-1 id_col=-1
   status_col=-1 usedby_col=-1`.
3. In the `:2443` separator branch, require equal cell counts:
   `(( ${#cells[@]} == header_width )) || is_separator=0` before/alongside the
   per-cell `:?-{3,}:?` test; on acceptance also clear `header_width` (unused after).
4. At `:2463-2464`, on a successful name scan set `header_width=${#cells[@]}` next to
   `header_candidate=1`; on failure keep the existing three-column reset.

This makes the header/delimiter pair adjacent, freshly named, and width-equal, matching
the independent oracle's pair rule (`round26-registry-oracle.py:34-46`). It does
not add a body-row width rule (the oracle does not have one either).

Expected outcomes against `corpus/evidence/round27-regressions.py:124-140`:

| control | current | after |
|---|---|---|
| `header-break-blank` / `header-break-prose` | accepted via stale columns (0/none) | exit 2, `metadata registry has no table`, 0 verdict records |
| `reorder-clean` (4 columns, new header after prose) | false finding or accept depending on stale index | exit 0, one verdict, findings=0 |
| `reorder-queued` | misbound status column | exit 1 + `META_SOURCE_NOT_MINED` |
| `delimiter-too-short` / `delimiter-too-long` | exit 0 | exit 2, no verdict record |
| `valid-table` | exit 0 | unchanged |

Real-registry control: `corpus/SOURCES.md:9-10` has 11 cells in both header and
delimiter, so the width rule does not change the current population run.

## 2. S-id token identity (FRegistryIdBoundary)

Defect: `metadata_registry_check_source` (`:2472-2507`) uses
`source_id_re='(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)'` (`:2474`) and consumes
each match with `source_scan=${source_scan#*"$source_match"}` (`:2503`). Bash reports no
match offset, so the strip removes the shortest prefix ending in the matched *text*.
When the last standalone id ends the value, an earlier glued copy of that text is the
first literal occurrence; the remainder starts mid-token and `^` re-anchors, inventing
`s002`/`S003` from `S001S002` and re-emitting one token as two or three findings.
Falsifier rows b1/b2/b5/b6 and b3/b11/b12 are the accepted evidence.

Correction: tokenize once, classify each whole token, keep one finding per occurrence.

```bash
metadata_registry_check_source() {
  local source_value=$1 entry_path=$2 entry_base=$3
  local LC_ALL=C
  local source_id found_id=0 used_by token matched i
  local -a used_by_tokens=()
  while IFS= read -r source_id; do
    [[ $source_id =~ ^S[0-9]{3,}$ ]] || continue
    found_id=1
    # existing three-way classification body (:2481-2502) byte-identical
  done < <(printf '%s\n' "$source_value" \
             | LC_ALL=C grep -oE '[[:alnum:]_]+' || true)
  ((found_id)) || emit_finding META_SOURCE_NO_ROW_ID info metadata \
    "entry=$entry_base source has no S-id"
}
```

- Delete `source_id_re`, `source_match`, and the `:2503` strip. Nothing else changes:
  codes, severities, text, and used-by matching (`:2488-2501`, exact root-relative path)
  stay as-is.
- Per-occurrence is required, not optional: `round27-regressions.py` expects
  `S002,S002` → 2 `META_SOURCE_NOT_MINED` records and one standalone `S002` in
  `ref S002x and S002` → 1. A `seen[]` dedupe (as in the r26 oracle's set) would fail
  the first control. The oracle is occurrence-blind; the regression is authoritative
  here.
- Do **not** land `${source_value//[^A-Za-z0-9_]/ }` with a word-for loop. The code's
  own measured note says: “The previous negated-class expansion was quadratic in the
  string length — measured >60 s at the 8 MiB source” (`:1102-1105`). A `source:` value
  can approach the 8 MiB entry cap (`:271`, `:2584-2604`), so that substitution risks a
  fresh hang under the same cap. `grep -oE`/`tr -cs` stream linearly; the `grep`
  process substitution runs the loop in the current shell, so `emit_finding` counters
  and `FINDING_LINES` are preserved. `|| true` keeps `set -euo pipefail` quiet when
  there are no tokens.
- `LC_ALL=C` is passed to the tokenizer explicitly. The function already declares
  `local LC_ALL=C`, but the explicit child environment makes the ASCII class
  independent of an inherited UTF-8 locale. [INFERENCE] A token adjacent to a
  non-ASCII byte is split exactly as the oracle's ASCII lookaround does
  (`round26-registry-oracle.py:12`).

Expected against `round27-regressions.py:142-156`: glued-before-terminal 0 findings;
glued-missing 0; underscore-glued 0; nonstandalone-duplicate 1; glued-repeat-duplicate
1; two-real-occurrences 2; adjacent-real-ids 1 `NOT_MINED` and 0
`META_SOURCE_ROW_MISSING`. The frozen differential's `adv-noid.md` shape (all four
standalone-boundary forms, no trailing id) is unchanged.

## 3. Complete-path denylist (FRegistryRegistryDeny)

Defect: `is_denylist_path` (`:595-606`) matches `ptr_file_part` output, and
`ptr_file_part` (`:573-576`) returns `${p%%:*}`. That truncation is the citation-anchor
grammar; applied to a filesystem path it stops at the first `:`, so
`a:b/.config/reg.md` and `x:y.env` are opened and parsed (falsifier B1-B6; entry arm
FRRD-2 at the same target and base).

Split the predicate, never change its pattern body:

```bash
denylist_match() { # TEXT -> rc0 when TEXT carries a denied component
  local f=$1
  case "$f" in
    *op.env|*.env|*server.token*|*credentials/*|*/oauth/*) return 0 ;;
  esac
  [[ $f == *chrome-profile* || $f == *Cookies* || $f == *"Login Data"* ]] && return 0
  [[ $f == *'/.omp/'* || $f == *'/.config/'* || $f == *'/.local/state/'* ]] && return 0
  [[ $f == '.omp/'* || $f == '.config/'* || $f == '.local/state/'* ]] && return 0
  return 1
}

is_denylist_path() { # citation pointer: the first ':' is the anchor (unchanged)
  local f; f=$(ptr_file_part "$1")
  denylist_match "$f"
}

is_denylist_fs_path() { # complete filesystem path: ':' is a name byte
  denylist_match "$1" || denylist_match "$(norm_ptr "$1")"
}
```

Switch exactly the raw-path calls, leaving the four pointer calls alone:

| site | function | argument | action |
|---|---|---|---|
| `:636` | `ptr_resolves_meta` | `readlink -f` canonical target | `is_denylist_fs_path` |
| `:2375` ×2 | `metadata_registry_load` | `--registry` value, its canonical form | `is_denylist_fs_path` |
| `:2382` | `metadata_registry_load` | `/proc/$$/fd/N` canonical target | `is_denylist_fs_path` |
| `:2584` ×2 | `verify_metadata` entry loop | entry path, canonical form | `is_denylist_fs_path` |
| `:2591` | `verify_metadata` entry loop | fd canonical target | `is_denylist_fs_path` |
| `:621`, `:650`, `:1129`, `:1598` | pointer/source/chain citations | pointer cells | keep `is_denylist_path` |

Preserved: the `norm_ptr` backtick leniency (second probe), the r22 bare-start forms,
the r21 “deny the canonical target” intent, and the four pointer call semantics
(`path:line` truncation). Refusal ordering and text are untouched: `-e/-r/-f`
(`:2369-2372`), then denylist before `open`, then fd/stat, nlink, size, bounded read,
NUL (`:2377-2406`). No fd/size/NUL/multilink arm is edited.

Expected against `round27-regressions.py:157-171`: `colon-denied-component`,
`colon-denied-suffix` → exit 2 with `metadata registry refused: denylist` and 0
anchored verdict records; `ordinary-colon-is-allowed` → exit 0 with one verdict;
plain `.config` case unchanged. Existing selftest identities remain: 128
`ptr-deny-symlink` (`:5581-5598`), 129-132 claim path-start cases (`:5619-5650`), 152
`metadata-denylist-alias` (`:5876-5879`) — all canonical targets are colon-free, so the
predicate change is invisible to them. The r26 M2 diagnostic changed `:596` globally
and was rejected; this split is the non-global form.

## 4. Severity/ordering notes

- Findings stay `warn` (row/used-by) and `info` (no-id), emitted in token order; the
  r26 differential compares per-entry finding sets and the r27 regression counts
  anchored finding lines.
- Exit 2 branches keep zero `^RESEARCH_GATE: ` records (`die_usage` `:389-390`), which
  the C3 controls assert.
- No output text changes. `META_*` codes, `METADATA_COMPLETE`, and the verdict summary
  format are untouched.

## 5. Inherited limits — report, do not claim whole-gate safety

These remain after the three repairs and must not be presented as fixed:

1. Registry grammar is still line-pair based, not GFM-aware: tables inside fences,
   indented code, or HTML comments are accepted; a fenced example can shadow the real
   table (FRegistryHeaderless FRH-4 G03-G07, FNoTrade F3). First table still wins.
2. Oracle disagreement is shape-limited: Python `strip()` Unicode trimming and doubled
   outer-pipe collapse (FRH-3 H12/G10/G11) mean differential “agreement” is not a
   byte-exact grammar identity.
3. Literal-colon paths cited as pointers are still truncated at the first `:`
   (`:573-576`). That is the preserved citation grammar, named here so the full-path
   fix is not read as pointer-path support.
4. `claim_source_path` (`:1125-1218`) checks the denylist on the raw citation only and
   never rechecks the canonical target before stat/read; not changed by C3.
5. `metadata_registry_load` still splits every `|`-bearing line into a per-line array.
   FNoTrade F2 measured 4 MiB pipe-dense input at 1.13 GiB RSS / 75.68 s; this patch
   does not bound table-row parsing, so “bounded registry reader” remains an overclaim.
6. Findings are per occurrence by contract, so a dense adversarial `source:` value can
   still append one `FINDING_LINES` entry per token (FNoTrade F3); this is behavior,
   not a bug to dedupe away.
7. A registry path that is absent is reported `not found` before the denylist runs
   (FRRD-5): exit 2 either way, but it is an existence oracle for protected paths.
   Order was intentionally not changed.

## 6. Unrun checks (L1, once after integration)

- `bash tools/research-gate.sh --selftest` — original 187 case identities preserved;
  this seat ran nothing.
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` —
  expect 0 mismatches; C3 controls above are the acceptance set.
- `bash corpus/evidence/round26-registry-differential.sh` on an isolated copy — expect
  no new gate/oracle disagreement on r24plus, pop29, adversarial.
- `bash corpus/evidence/round26-measure.sh "$PWD" c3` — frozen controls unchanged.
- `bash -n tools/research-gate.sh` / shellcheck, if the lane runs them.

No pass is claimed from this seat; the suggestions are author-lane advice, not an
outside admission. Report path relative to the lane root:
`.ufo/waves/round-27/build/ScoutRegistryReader.md`. Read-only: no product code, test,
fixture, index, or sibling report was modified.

## Trailer

Seat `ChousaR27.ScoutRegistryReader`, style scout, round 27 attempt 1. Observed base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`; C3 sites byte-identical to gate sha256
`c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. No LSP available;
literal-search evidence only. No tools installed or updated.
