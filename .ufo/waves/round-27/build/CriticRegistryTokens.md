# CriticRegistryTokens — C3 S-id scanner: duplicate findings and allocation

Seat: critic, read-only static analysis. Base 64eec5d41c7cf7f17f5ce1e968e28b3769952596.
No code, gate, selftest, or regression script executed. No installs.
ExecRegistry clone observed clean at base (`git diff` empty) when this was written, so this critiques the base code and likely fix shapes, not a patch.

## Defect location

`tools/research-gate.sh:2472-2507` `metadata_registry_check_source`:

- `:2474` `source_id_re='(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)'`
- `:2503` `source_scan=${source_scan#*"$source_match"}`

Bash `=~` reports no match offset. The strip removes through the FIRST textual occurrence of the matched text. The regex match itself is the leftmost *standalone* occurrence, so an earlier non-standalone copy of the same text is consumed instead. Two consequences:
1. the real occurrence is rescanned, which duplicates the finding;
2. the remainder starts mid-token, so `^` then accepts a glued suffix as standalone, which invents an id.

## Counterexamples (static trace against base; expectations from `corpus/evidence/round27-regressions.py:140-152`)

| source | base trace | base findings | expected |
|---|---|---|---|
| `see S001S002 and S001` | match ` S001`(end) → strip first ` S001` → `S002 and S001` → `^S002` invented | NOT_MINED×1 | 0 |
| `see S001S003 and S001` | same → `^S003` invented | ROW_MISSING×1 | 0 |
| `ref S002x and S002` | strip first ` S002` (in `S002x`) → `x and S002` → rescan | NOT_MINED×2 | 1 |
| `ref S002S002 and S002` | → `S002 and S002` → `^S002`, then ` S002` | NOT_MINED×3 | 1 |
| `S002,S002` | two real occurrences | 2 | 2 (must be preserved) |

## Tempting fixes that still fail

- **Strip through the id only** (`${source_scan#*"${BASH_REMATCH[2]}"}`): this has the same first-occurrence bug. `ref S002x and S002` leaves `x and S002`, which duplicates. `S001S002 and S001` leaves `S002 and S001`, and `^` invents S002.
- **Dedupe by id** (an associative "seen" set, or the r26 oracle's `set(...)` at `round26-registry-oracle.py:122`): this breaks `two-real-occurrences`, where the r27 control requires 2 NOT_MINED findings. The contract counts per occurrence. Only the presence-only r26 oracle tolerates either behavior. Impacted axis: calibration. The r27 harness would reject this; it is not a tradeoff.
- **Keeping the loop and adding a "previous char" check**: this is not possible because `=~` gives no offset. Any `#*literal` strip has the defect.

## Smallest safe correction

Tokenize once over ASCII word bytes, then test each whole word. This is per occurrence, never rescans, and never invents ids. It matches the r26 oracle's ASCII boundary `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` (`round26-registry-oracle.py:12`) exactly.

```bash
metadata_registry_check_source() {
  local source_value=$1 entry_path=$2 entry_base=$3
  local LC_ALL=C IFS=$' \t\n'
  local source_words source_id found_id=0 used_by token matched i
  local -a used_by_tokens=()
  source_words=${source_value//[^A-Za-z0-9_]/ }
  for source_id in $source_words; do
    [[ $source_id =~ ^S[0-9]{3,}$ ]] || continue
    found_id=1
    # ... existing three-way classification body unchanged (:2481-2502) ...
  done
  ((found_id)) || emit_finding META_SOURCE_NO_ROW_ID info metadata \
    "entry=$entry_base source has no S-id"
}
```

Notes:
- The unquoted `$source_words` is safe. After the substitution only `[A-Za-z0-9_ ]` remain, so no glob metacharacters can survive and noglob is unnecessary. Word splitting uses the local default IFS.
- Declare `local LC_ALL=C` in the helper itself instead of inheriting it through `verify_metadata`'s dynamic scope (`:2539`). That keeps `A-Z`/`0-9` byte ranges if a future caller changes, which is the same locale lesson as C2. Bytes ≥0x80 become boundaries, the same as the oracle's Unicode-letter-is-boundary behavior.
- Use a for-loop over the expansion instead of `read -a <<<`, which avoids a here-string temp file for a large `source:` value. [INFERENCE] bash ≥5.1 uses a pipe only when the here-string fits the pipe buffer.
- The used-by matching (`:2488-2501`) and the finding codes and text stay byte-identical. Exact used-by rules are untouched.

Expected outcome: all seven ID-occurrence controls at `round27-regressions.py:140-148` match, with `ROW_MISSING`=0 everywhere and per-occurrence counts of 0/0/0/1/1/2/1. The valid-table and r26 registry-differential behavior is unchanged, because finding-code sets are identical for standalone ids.

## Allocation and complexity (scoped, not a broad resource claim)

- **Base:** each iteration re-runs the ERE over the whole remainder and builds a new remainder string, so the cost is at least O(k·n) bytes copied for k occurrences in an n-byte `source:` value. The value is bounded only by the 8 MiB entry cap (`:271`). [INFERENCE] bash's shortest-left `#*pat` removal tries successive prefix ends with `strmatch`, so each strip can be superlinear. Not measured; no timing claim.
- **Proposed:** one substitution copy plus one word list, O(n) memory at about 2–3× the value. [INFERENCE] bash 5.x fixed-length bracket patterns make `//[...]/ ` linear. The work per occurrence is then just the existing classification plus `emit_finding`.
- **Inherited, not fixed by this change (report, don't claim):**
  - Findings are per occurrence by contract, so an adversarial `source:` with about 10⁶ repeated non-mined ids still appends about 10⁶ `FINDING_LINES` entries (`:392-395`).
  - A mined id repeated k times re-splits `used-by` k times. An optional per-id result cache would remove that without changing counts, but it is not required.
  - An id with a very long digit run is echoed verbatim into finding text.
  - `metadata_registry_load` uses one here-string per registry line (`:2422`) plus the whole-content here-string (`:2468`).

## Adjacent interplay (owned by other seats; flagged only for duplicates)

- **Registry rows:** duplicate row ids stay first-wins silently (`:2433-2434`). This is the existing documented r26 behavior (`round26-claims.md:95`), so it is not a duplicate-finding source. Keep it unchanged.
- **Header state:** a non-table line resets `header_candidate` but not `id_col/status_col/usedby_col` (`:2412-2415`). Those columns are reset only when a candidate fails its separator (`:2454`), so stale columns let a later unnamed row become a header. That is the `header-break-*` failure. The fix must reset all three columns there, and must compare the separator cell count to the stored header cell count for `delimiter-too-short` and `delimiter-too-long`. These changes do not interact with the token fix.

## Impacted axes

- **Calibration:** primary; fixes invented and duplicate findings.
- **Operability:** neutral.
- **Freshness:** neutral; the locale is pinned locally.

## Unrun checks (for L1, once after integration)

- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` (C3 occurrence block)
- `bash corpus/evidence/round26-registry-differential.sh`, run on an isolated copy
- `bash tools/research-gate.sh --selftest`, where all 187 original case identities must remain
