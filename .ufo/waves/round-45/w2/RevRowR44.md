# Review: SKILL.md Gates row `research-gate round-44 counters` (line 108)

Reviewed at lane commit `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` (archive tree
`/tmp/chousa-r45-RevRowR44/tree`, git archive). Verdict: **HOLDS — all 8 cells**.

## Row shape
Row 108 splits into exactly **8 cells** (name, kind, entry, verdict map, self-test,
pinned values, write scope, owner). Verified: `len(line.strip().strip('|').split('|')) == 8`.

## Entry cell — every command re-run inside the archive tree
| command | observed (verbatim) | rc | verdict-map claim | result |
|---|---|---|---|---|
| `python3 corpus/evidence/round44/c1-count.py` | `N_SPAWNED=64/64 N_REAPED=64/64 PARENT_PID_MATCH=1/1 ZERO_PIDS=0 NAMES_MATCH=64/64 C1=PASS` | 0 | C1 exit 0, same counts | holds |
| `python3 corpus/evidence/round44/c2-count.py` | `CONSISTENT=39/39 REVERIFIED=36/36 LEFT_NAMED=3/3 C2=PASS` | 0 | C2 exit 0, same counts | holds |
| `python3 corpus/evidence/round44/c3-count.py` | `ENTRY_CITES=1/1 QUOTE_LOCATED=1/1 URL_MATCH=1/1 C3=PASS` | 0 | C3 exit 0, same counts | holds |
| `python3 corpus/evidence/round44/errata-count.py --file corpus/evidence/round44/controls/errata-two.txt` | `ERRATA=2 ERRATA_COUNT=PASS` | 0 | exit 0 iff PASS; observed `ERRATA=2` | holds |
| `... errata-count.py --file corpus/evidence/round44/controls/errata-zero.txt` | `ERRATA=0 ERRATA_COUNT=FAIL` | 1 | exit 1 iff zero | holds |
| `... errata-count.py --file corpus/evidence/round44/controls/missing.txt` | `ERRATA=0 ERRATA_COUNT=FAIL missing` | 2 | exit 2 usage/missing file | holds |
| usage: each counter with `--nonsense` / `errata-count.py` without `--file` | argparse usage error | 2 | exit 2 usage/env | holds |

## Self-test cell — every control re-run
- C1 do-nothing missing receipt (`--receipt /nonexistent/receipt`): `C1=FAIL receipt-missing`, rc 1. Cell: "each exit 1" — holds.
- C1 `controls/pids0.receipt`: `N_SPAWNED=0/64 ... C1=FAIL`, rc 1 — holds.
- C1 `controls/prose.receipt`: `C1=FAIL prose`, rc 1 — holds.
- C2 `controls/all-left.tsv`: `CONSISTENT=3/39 REVERIFIED=0/36 LEFT_NAMED=3/3 C2=FAIL`, rc 1. Cell: "`REVERIFIED=0/36`, exit 1" — holds (LEFT_NAMED=3/3 as expected for left-named rows).
- C3 `--entry /nonexistent/entry`: `ENTRY_CITES=0/1 QUOTE_LOCATED=0/1 URL_MATCH=0/1 C3=FAIL entry-missing`, rc 1 — holds.
- Errata `controls/errata-zero.txt`: rc 1; `controls/errata-two.txt`: rc 0 — holds (errata-two.txt has exactly 2 `^Erratum [0-9]+` lines; errata-zero.txt has 0).

## Pinned-values cell — hashes exist; claims unchanged
- `043f19a1db91288947493d9f879e61e7a9f07241` — commit "round-44: freeze parent-lifetime,
  disposition, and RFC quote claims before scoring". `claims.md` blob at that commit
  `f2e7a74a810c9c44e010c489931575ce029b2c291f23072b36d64f1c35d51aeb` == blob at
  `5e8c7ad` (same hash). Claims still frozen exactly as pinned. Holds.
- `d82cec904bf0fb8736886b9f17be913c7807427a` — commit exists; `merge-base --is-ancestor`
  of `5e8c7ad` rc 0 (measured HEAD is real history). Holds.
- `44aaf33cd37e2583fff13397f5a4b60a011ec1ab` — commit exists ("round-44: add the two
  adopted version-binding entries to the corpus coverage map"). Holds.

## D1 sentence (verdict-map cell)
"D1: reads an untracked campaign capture path, not reproducible from the lane tree alone."
Verified true by code + host state:
- `c3-count.py:26-28` hardcodes `CACHE = /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, outside the lane root (`.../chousa-shokunin`).
- `c3-count.py:60-63`: `located` stays False unless `capture.is_file()`; `capture = CACHE/(sha256(URL)[:24]+".txt")` = `d0c4a09a9de32cb91d5e3797.txt`.
- That file exists on host (107130 bytes) and contains `constitutes a promise that the resource state` (grep count 1) — so C3 passes only while it does.
- `.qcache` appears in zero `git ls-files` entries of the lane; the archive tree does not contain it. A lane-tree-only run cannot yield `QUOTE_LOCATED=1/1` (would be 0/1, rc 1). D1 holds.

## Write-scope / owner cells
`read-only; counters write no lane receipts` — source inspection of all four scripts shows
no writes (read-only opens); runs in the scratch tree produced no files. `chousa` —
consistent with sibling rows. Holds.

## Residual risk / gaps
- "No superseding counter observed" is a negative claim; the round44 evidence dir listing
  shows only c1/c2/c3/errata counters, consistent, but absence cannot be proven globally.
- C2's `UNTRACKED`/`MODIFIED` report paths are present in the committed archive, so C2
  runs green in-tree; this matches the row's exit contract ("untracked" = status at
  measurement time).
- `errata-count.py` docstring self-describes as "QUALITY 62 demonstration, not a round-44
  claim counter"; the row's own verdict map governs its observed behavior (all three exit
  codes matched), so no inconsistency.
- No fetch performed; no lane/state writes; scratch `/tmp/chousa-r45-RevRowR44` removed.
