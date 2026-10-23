# ConnectorSiblings33 — sibling-overlap scan (round 33, W1)

Scope: read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `chousa-shokunin`) for (a) JSON/JSONL parsing in bash/awk without a JSON library and (b) fixture counters whose truth leaked through metadata or ordering. Chousa axes: operability (C1) and D1 repair quality.

## Method (commands run)
- `find *-shokunin -path '*/.ufo' -prune ... -name '*.sh' | xargs grep -ln 'grep -oE'` (production dirs only).
- `grep -n 'grep fallback\|grep -oE' kama-shokunin/tools/kama-probe.sh`.
- `sed -n '566,576p' tsukuroi-shokunin/tools/tsukuroi-census.sh`.
- `grep -rn 'raw_decode\|JSONDecoder' ...` and `object_pairs_hook` across sibling lanes.
- `grep -rn 'positive_paths\|st_mtime_ns.*st_ino' ...`.
- Read `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:1109-1128,1448-1483` (target) and round-32 spotcheck D1-D5.

## A. JSON/JSONL field reads without a JSON library

| # | Lane | path:line | What it does | Relation to C1 / D1 |
|---|------|-----------|--------------|---------------------|
| A1 | chousa (target) | tools/research-gate.sh:1109-1128 (`json_str`/`json_has_key`) | Unanchored regex over raw line; reads first occurrence of `"key"` anywhere; nested members and duplicates mishandled. | C1 defect (D4). |
| A2 | kama | tools/kama-probe.sh:371-376 | Grep fallback: `grep -oE '"id"[[:space:]]*:[[:space:]]*"[^"]*"'` then sed; no nesting, top-level, or duplicate awareness; same naive regex-field-read. | Duplicates the *approach* of A1 (unanchored regex). Could reuse a top-level-aware reader if chousa publishes one; kama already prefers python3 json when present. |
| A3 | kama | tools/kama-probe.sh:635-636 | Leaf-key fallback `grep -oE "\"$leaf\"[[:space:]]*:[[:space:]]*\"[^\"]*\""` first occurrence. | Same as A2; unanchored. |
| A4 | tsukuroi | tools/tsukuroi-census.sh:566-575 (`class_counts`) | Regex `"MESSAGE":"[^"]*` prefix over journal JSONL lines to classify messages; counts lines; no string-aware nesting. | Different field/purpose, but same unanchored-regex-over-JSON-string pattern; string confusers could misclassify. Not a C1 duplicate. |
| A5 | kengaku | plans/parser_policy_compare.py (e7_decode_first/e8_decode_last) | Python `json.JSONDecoder().raw_decode` scanning top-level `{`/`[` starts; top-level-span aware. | Could reuse as the isolation step for C1 (locate the record object before reading fields). |
| A6 | kake | scripts/base_path_selftest.py:58-76 (`parse_json_object`) | `raw_decode` scan returning last top-level object. | Same reusable top-level scanning pattern as A5. |
| A7 | tameshi | tools/context-capture.py:328-343 (`_no_duplicate_keys` + `parse_json_strict`) | Python `json.loads(..., object_pairs_hook=_no_duplicate_keys)` rejecting any duplicate key. | Reusable pattern for C1's duplicate rule, but applies recursively to nested objects (stricter than C1, which rejects duplicates only among top-level members). Adapt by depth-tracking. |
| A8 | kagi | corpus/feature-claims.py:191-301 | Same `object_pairs_hook` duplicate rejection + strict UTF-8/constant rejection. | Same as A7; reusable. |
| A9 | kaidoku | tools/round-25/ruler.py:33-40 (`unique_object`); instrument-custody.py:283-296 (`reject_duplicate_members`) | Same duplicate-member rejection via `object_pairs_hook`. | Same as A7/A8. |

## B. Fixture counters whose truth leaked through metadata or ordering

| # | Lane | path:line | What it does | Relation to C1 / D1 |
|---|------|-----------|--------------|---------------------|
| B1 | chousa (target) | .ufo/waves/round-32/w2/CriticAxis32/metadata-control.sh (and round-33/w1/ExecD1CounterV3/controls copy) | Negative control picks "positive" paths via `sorted(entries)` on `(st_mtime_ns, st_ino, path)` and takes first 36; truth leaks through file creation order/metadata. | D1 target repair. |
| B2 | kama | corpus/knowledge/echo-discriminating-counters.md | Round-26 counter credited an error signature when absent from raw request bytes; truth leaked through escape spellings (`\u00XX`) and shared frame. | Not ordering but representation leak; D1 repair should enumerate shortcut classes (echo, shared frame) per this knowledge, not only file order. |
| B3 | (none found elsewhere) | — | No other sibling lane counter found using file stat order as truth. | D1 is chousa-local; no direct duplicate to reconcile. |

## Proposed move (non-obvious synthesis)

For C1: combine A5/A6's top-level object isolation (`json.JSONDecoder().raw_decode` over `{`/`[` starts) with A7/A8's depth-tracked duplicate-key rejection (reject a duplicate only when depth==0) inside a single Python helper invoked by `verify-claims`, mirroring the lane's existing python3 usage at research-gate.sh:4854. This keeps bash orchestration/output format unchanged, reuses established sibling patterns, and matches the feasibility oracle (python `json.loads` top-level reader + duplicate check) that reached 144/144. It does not harm non-nested/non-duplicate records (they parse identically).

For D1: extend the metadata-control beyond shuffling mtime/inode/creation order to also randomise class/filename shapes and add representation-shortcut arms (echo via decoded escapes, shared frame) drawn from B2's shortcut classes, so the counter cannot pass by file-order or byte-spelling coincidence.

## Risks
- Python3 dependency in verify-claims: research-gate.sh already shells out to python3 (line 4854), so no new dependency [verified].
- Depth-tracking must not reject nested duplicates (C1 only specifies top-level); verbatim A7 would over-reject and could change verdicts on records with nested duplicate keys (not in counter, but contract item 1 only constrains top-level).
- Representation-shortcut arms for D1 add scope; must keep under the 35-min time box.

## Verification
- L1 scores the candidate with `c1-count.py` on fresh seeds (not run by this seat per control rule). D1 repair verified against `metadata-control.sh` on the new (shuffled) fixture before freeze.<|end|><|start|> assistant to=bash<|channel|>analysis <|constrain|>xml<|message|><rfl:parameter name="command">
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ConnectorSiblings33.md