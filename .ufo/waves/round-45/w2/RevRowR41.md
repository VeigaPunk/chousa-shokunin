# RevRowR41 — falsification of SKILL.md Gates row `research-gate round-41 counters` (row 105)

Measures over committed bytes at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`, archive tree
`/tmp/chousa-r45-RevRowR41/tree`, every counter run inside the tree (lane root).

## Row shape
Row 105 has exactly **8 cells** (9 `|` in the raw line, same as the header line 77; no escaped pipes): name | kind | entry | verdict map | self-test | pinned values | write scope | owner. Holds.

## Per-cell verdict

### name (`research-gate round-41 counters`) — holds
Name cell matches the row's subject.

### kind (`gate`) — holds
Both counters behave as gate checks (exit 0 iff all cells hold, 1 otherwise; no exit-2 harness path claimed or present).

### entry — holds
Ran both commands from the archive-tree root:
- `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` → `CAPTURE_PIN_MATCH=12/12`, all 12 cells PASS, **exit 0**.
- `python3 corpus/evidence/round41/c2-count.py` → `W04_DISPOSITIONED=5/5`, **exit 0**.

### verdict map — holds
Observed values equal the map: `CAPTURE_PIN_MATCH=12/12` (C1), `W04_DISPOSITIONED=5/5` (C2); exit 0 when all hold; exit 1 on any other count (see self-test controls below). No exit-2 path triggered.

### self-test — holds
- C1 on the do-nothing control `.ufo/waves/round-41/controls/base-gate-r41.sh` (present at commit) → `CAPTURE_PIN_MATCH=1/12` (S1 only PASS), exit 1 — byte-matches committed `control-before.txt` (1/12, S1 pass).
- C2 with `w04-dispositions.tsv` removed (in a hardlink copy of the tree) → `W04_DISPOSITIONED=0/5`, exit 1, FAIL S051/S053/S073/S074/S075 "no disposition row" — byte-matches committed `c2-control-before.txt`.

### pinned values — holds
- `corpus/evidence/round41/claims.md` exists at commit. Freeze commit `b173b0943e647f7e3a365689df19debe40fd9dd2` exists; its `claims.md` bytes == committed bytes (sha256 `d9e1e6a010694077f5217dd51374b1c98942ddee31f4f89ee77743f076040e77`).
- Work commit `1bd9001330f19d89ec36592010d4218881ea5941` exists and is an ancestor of `5e8c7ad` (`1bd9001 round-41: pin capture invocation surface (12/12); W04 dispositions (5/5); …`).
- All receipt paths exist at commit: `measure-after-c1.txt` (12/12, `AFTER_EXIT=0`), `measure-after-c2.txt` (5/5, `AFTER_EXIT=0`), `receipts/cells/cells.json`, `w04-dispositions.tsv`. Reruns reproduce the same values (receipt regen: 11/12 cells byte-identical; S10 differs only in the mkdtemp temp-dir name inside evidence stderr — non-deterministic temp naming, not a defect).

### write scope — holds
Full-tree sha256 manifest (13,884 files) before/after the entry runs: exactly one file changed — `corpus/evidence/round41/receipts/cells/cells.json`. Confirms "C1 writes per-cell receipts under corpus/evidence/round41/receipts/cells/" and C2 read-only.

### owner (`chousa`) — holds

## Residual risk / verification gaps (not defects in the row)
- **C2 is host-path-bound**: `c2-count.py` hardcodes `CENSUS="/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` and `validate --root /home/vgpnk/Projects/shokunin`; it measures the live fleet census, not the frozen commit bytes. It reproduced 5/5 because the live census still emits exactly the 5 pinned W04 ids (S051/S053/S073/S074/S075). The row's measurement is true today but is not reproducible from the committed tree on a different host without the same absolute census path.
- C1's receipt regen is deterministic modulo temp-dir names (above).

## Verdict: **holds** — no actionable defect found; all 8 cells and both commands' claimed behavior reproduce at 5e8c7ad.
