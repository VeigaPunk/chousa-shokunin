# ScribeGateR41 — draft SKILL.md Gates row for round 41 (r45 w1)

Item: draft the missing Gates row for round 41's gate entry points
(`corpus/evidence/round41/c1-count.py`, `corpus/evidence/round41/c2-count.py`)
per the round-45 wave-1 spec, read-only, no fetch, no production writes.

## Evidence read

- `SKILL.md:75-99` — Gates table; existing row conventions (`research-gate
  round-37 counters` etc.). No round-40/41/42/43/44 rows exist (table ends at
  `mechanism-witness` r35); next `## ` is line 491. Gap confirmed.
- `corpus/evidence/round41/claims.md` — C1/C2 frozen predicates, counters,
  before/after targets: C1 `CAPTURE_PIN_MATCH=<k>/<n>` exit 0 iff k==n, else 1
  (before target < n/12, ~1/12; after 12/12); C2 `W04_DISPOSITIONED=<k>/<n>`
  exit 0 iff k==n and n>=1 (before 0/5; after 5/5). No exit-2 contract.
- `SCORECARD.md:2280-2287` — round-41 measured claims: work commit
  `1bd9001330f19d89ec36592010d4218881ea5941`, freeze commit
  `b173b0943e647f7e3a365689df19debe40fd9dd2`; C1 `1/12` → `12/12`, C2
  `0/5` → `5/5`.
- `LOG.md:1484-1492` and `corpus/lessons/round-41.md` — measurement receipts
  (control-before 1/12, measure-after-c1 12/12, c2-control-before 0/5,
  measure-after-c2 5/5).
- `corpus/evidence/round41/w04-dispositions.tsv` — five rows (S051, S053,
  S073, S074, S075).
- `corpus/evidence/round41/measure-after-c1.txt`, `measure-after-c2.txt` —
  recorded after-values (verbatim below).

## Commands run (from lane root, read-only)

`python3 corpus/evidence/round41/c2-count.py` → output verbatim:

```
W04_DISPOSITIONED=5/5
EXIT=0
```

`python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh`
(output trimmed to decisive lines) →

```
CAPTURE_PIN_MATCH=12/12
  PASS S1-base-clean
  PASS S2-trap-inventory
  PASS S3-sed-suppress
  PASS S4-mktemp-preseed
  PASS S5-cat-poison
  PASS S6-rm-suppress
  PASS S7-sort-reverse
  PASS S8-mkdir-suppress
  PASS S9-override-relative
  PASS S10-override-nongnu
  PASS S11-child-tr
  PASS S12-loader-env
EXIT=0
```

Both reproduce the pinned after-values at the current tree (2026-10-25).
Neither counter has an exit-2 contract; no `--receipt`-style option exists.
C1 unconditionally rewrites `corpus/evidence/round41/receipts/cells/cells.json`
(no flag to suppress it): I snapshotted its bytes (sha256
`1f5c0afae8024c50013e9a9060988c14506115125e3823042e4512833f293b80`), ran the
counter, then restored the original bytes; post-restore sha256 matches the
snapshot exactly. `cells-before.json` untouched. No other lane file touched.

## Verdict — row to append to the Gates table (after the `mechanism-witness`
row, before the `**Historical — Round-25…` paragraph)

```
| research-gate round-41 counters | gate | `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` · `python3 corpus/evidence/round41/c2-count.py` (lane root) | `CAPTURE_PIN_MATCH=12/12` (C1) · `W04_DISPOSITIONED=5/5` (C2); exit `0` iff every applicable cell holds; any other count exit `1` | C1 on the do-nothing control `.ufo/waves/round-41/controls/base-gate-r41.sh` → `CAPTURE_PIN_MATCH=1/12` (`control-before.txt`); C2 with the TSV absent → `W04_DISPOSITIONED=0/5` (`c2-control-before.txt`) | contract `corpus/evidence/round41/claims.md` (freeze `b173b0943e647f7e3a365689df19debe40fd9dd2`), measurement at work commit `1bd9001330f19d89ec36592010d4218881ea5941`; receipts `corpus/evidence/round41/measure-after-c1.txt`, `measure-after-c2.txt`, `receipts/cells/cells.json`, `w04-dispositions.tsv` | C1 writes per-cell receipts under `corpus/evidence/round41/receipts/cells/`; C2 read-only (runs the census `validate`); no network | chousa |
```

8 cells, single line, starts `| ` ends ` |`; every entry point named by full
repo-relative path; verdict map states both exit codes and the exact PASS print
values; self-test names the failing controls with their recorded pre-values;
pinned values cite the measured lane commit, freeze commit, and receipt files;
write scope is accurate (C1 rewrites `receipts/cells/cells.json`; C2 only
invokes `scripts/sources-census.sh validate` read-only).

## Touched surfaces

- Wrote only `.ufo/waves/round-45/w1/ScribeGateR41.md` (this report).
- Scratch `/tmp/chousa-r45-ScribeGateR41/` created and deleted; `c1.out`,
  `cells.json.orig` lived there only.
- Lane left byte-identical to pre-run state (receipt sha256 confirmed after
  restore). No git/jj operations; no fetch; no census-registry edits.

## Out-of-scope items

- No other round's Gates row was drafted (separate scribe seats).
- Control re-runs (base-gate-r41.sh / TSV-absent) NOT re-executed — their
  pinned pre-values are quoted from committed control receipts
  (`control-before.txt`, `c2-control-before.txt`) per the round-41 lessons, and
  re-running the C2 control would require deleting the committed TSV.

## Findings

- Round-41 row absent from SKILL.md → this draft fills one of the 29
  unregistered entries counted at the C2 freeze.
- Both counters currently reproduce their pinned after-values exactly
  (12/12, 5/5, exit 0), so the row's verdict map states observed values, not
  remembered ones.
- No tools installed (none needed); no updates recorded.

Pointers: `SKILL.md:75` (Gates table), `SCORECARD.md:2280`,
`corpus/evidence/round41/claims.md:61-105`, `corpus/lessons/round-41.md:9-10`.
