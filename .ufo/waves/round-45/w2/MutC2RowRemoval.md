# MutC2RowRemoval — mutation probe: delete each of the 12 new `## Gates` rows one at a time (C2 calibration)

Seat: mutation-tester (leaf). Lane: chousa, round 45 wave 2 (falsify). Measured over committed bytes at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` only; never touched the lane repo, its git index, jj, the fleet repo, or `/home/vgpnk/Projects/shokuknow`.

## Method
- Extracted `git archive 5e8c7ad…` into `/tmp/chousa-r45-MutC2RowRemoval/tree` (pristine; SH256 `ba4e2c9f…` of SKILL.md equals `git show 5e8c7ad…:SKILL.md`).
- The twelve rows added this round are the `## Gates` table lines 100–111 (after the `mechanism-witness` row at line 99): research-gate round-31 counters (100), round-32 v1 counters (101), round-33 C1 v1/v3 counters (102), round-34 v1/v2 counters (103), round-40 (104), round-41 (105), quarantine-check r42 (106), absent-split r43 (107), round-44 (108), round-45 (109), parent-lifetime (110), tag-count (111).
- For each line 100–111: fresh full copy of the archive tree; the line deleted from that copy's SKILL.md (verified: mut copy keeps exactly 29 gates rows and lacks exactly that line); ran `python3 corpus/evidence/round45/c2-count.py --root . --list` from inside the copy. Baseline first, on the pristine tree. First harness attempt was invalid (hardlink aliasing: `cp -al` + in-place write corrupted all copies — rerun with real copies).
- No tools installed; no network; no lane writes. Scratch cleaned at end.

## Baseline (pristine, commit 5e8c7ad…)
```
ENTRY_POINTS=54  GATES_ROWS=30  REGISTERED=54/54  UNREGISTERED=0  C2=PASS  (exit 0)
```

## Per-row deletion results (counter `--list` output paths, verbatim)
| deleted row (line) | UNREGISTERED paths after deletion | count | counter exit |
|---|---|---:|---:|
| 100 research-gate round-31 counters | `corpus/evidence/round31/c1-count-v3.py`, `c1-count.py`, `c2-count-v3.py`, `c2-count.py` | 4 | 1 C2=FAIL |
| 101 research-gate round-32 v1 counters | `corpus/evidence/round32/c1-count.py`, `c2-count.py` | 2 | 1 C2=FAIL |
| 102 research-gate round-33 C1 v1/v3 counters | `corpus/evidence/round33/c1-count-v3.py`, `c1-count.py` | 2 | 1 C2=FAIL |
| 103 research-gate round-34 v1/v2 counters | `corpus/evidence/round34/c1-count-v2.py`, `c1-count.py` | 2 | 1 C2=FAIL |
| 104 research-gate round-40 counters | `corpus/evidence/round40/c1-count.py`, `c2-count.py` | 2 | 1 C2=FAIL |
| 105 research-gate round-41 counters | `corpus/evidence/round41/c1-count.py`, `c2-count.py` | 2 | 1 C2=FAIL |
| 106 `quarantine-check` round-42 gates | `corpus/evidence/round42/c1-count.py`, `c2-count.py`, `tools/quarantine-check.py` | 3 | 1 C2=FAIL |
| 107 `absent-split` (round 43) | `corpus/evidence/round43/c1-count.py`, `c2-count.py`, `c3-count.py`, `tools/absent-split.py` | 4 | 1 C2=FAIL |
| 108 research-gate round-44 counters | `corpus/evidence/round44/c2-count.py`, `c3-count.py`, `errata-count.py` (NOT c1-count.py) | 3 | 1 C2=FAIL |
| 109 chousa round-45 counters | `corpus/evidence/round45/c2-count.py`, `c3-count.py` (NOT c1-count.py) | 2 | 1 C2=FAIL |
| 110 `parent-lifetime` (r44; exit contract r45) | `tools/parent-lifetime.sh` | 1 | 1 C2=FAIL |
| 111 `tag-count` (QUALITY 64, r45) | (none) | 0 | 0 C2=PASS |

## Findings
1. **Row 111 (`tag-count`) removal changes nothing** — duplicate/no-authority row for C2. Its artifact `corpus/evidence/round45/tag-count.py` is outside the counter's entry-point universe (`COUNTER` regex matches only `c\d+-count*.py`, `verify-receipts.py`, `errata-count.py`; `tag-count.py` matches none and isn't under `tools/`). Deleting it leaves `UNREGISTERED=0`; the row adds no C2 registration.
2. **Two paths are registered by two new rows each** (double registration via substring matching against incidental mentions in the parent-lifetime row's self-test/pinned-values cell):
   - `corpus/evidence/round44/c1-count.py` → new rows at lines 108 (round-44 counters) and 110 (parent-lifetime).
   - `corpus/evidence/round45/c1-count.py` → new rows at lines 109 (round-45 counters) and 110 (parent-lifetime).
   Verified: deleting only 108 or only 109 leaves these paths registered (they do not appear in the `--list` output above).
3. Every other new row (100–110) is individually load-bearing: deleting any one flips C2 to FAIL with the concrete paths listed. 29 entry points are covered solely by the new rows (21 only by old rows, 4 by both).
4. C2 predicate itself **holds** on the committed bytes: baseline `UNREGISTERED=0`. The defects found are a redundant row (111) and two doubly-registered paths (44/45 c1-count.py) — calibration findings, not predicate failures.

## Evidence
- Pristine SKILL.md (tree) sha256 `ba4e2c9f14c77e92c582e64c31f5466f31b45cb34e68c346038891941a947544` = git-archived SKILL.md.
- Mutated copies: `mut-100/SKILL.md` `de7510895d…`, `mut-111/SKILL.md` `e8212bd441…`; all 12 copies verified to have exactly 29 gates rows and to lack exactly their target line.
- Full verbatim counter outputs (baseline + 12 runs) recorded in the harness run; key lines reproduced above.
- No tool installs this seat; no network; no live fetches; no lane/fleet writes; scratch deleted.
