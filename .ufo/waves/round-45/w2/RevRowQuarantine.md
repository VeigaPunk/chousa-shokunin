# Review: Gates row `` `quarantine-check` round-42 gates `` (SKILL.md line 106 @ 5e8c7ad)

Item: the `## Gates` row whose name cell is `` `quarantine-check` round-42 gates `` — re-run every entry command inside the archive tree, compare verdict map / self-test cells with observations, open every pinned-values path at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1, confirm 8 cells.

Setup: `mkdir -p /tmp/chousa-r45-RevRowQuarantine/tree && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x -C /tmp/chousa-r45-RevRowQuarantine/tree`. All runs below: `cd /tmp/chousa-r45-RevRowQuarantine/tree` (removed at finish). External inputs read: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (exists) and `.qcache/` (exists) — read-only.

Row cell count: split on `|` → exactly **8 cells** (name, kind, entry, verdict map, self-test, pinned values, write scope, owner) ✓.

## Per-cell verdict

**1. name / 2. kind** — ` `quarantine-check` round-42 gates` | `gate` — **holds** (verbatim match; row 106).

**3. entry** — commands: `python3 tools/quarantine-check.py {slice,examine,verdict,digests}` and `python3 corpus/evidence/round42/c1-count.py`/`c2-count.py`.
- `slice` → exit 0, 24 lines (ids S077..S125; 20 `payload-absent` + 4 `the gate block named no locator…`).
- `examine` → exit 0, 43 lines (3 sample lines: `S077\t1\tno-capture…`, `S077\t2…`, `S077\t3…`).
- `verdict` → exit 0, 24 lines (sample: `S077\tunverifiable\tno local capture…cache`).
- `digests` → exit 0, 1 register line (`register …absent-defect-register.md 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`) + 20 capture sha256 lines.
- `c1-count.py` → exit 0: `SLICE_REDERIVE_MATCH PASS tool=24 independent=24` … `MUTANT_DETECTED PASS mutant=23 base=24`; counts `SLICE_REDERIVE_MATCH=24/24 QUOTES_EXAMINED=43/43 REPRODUCIBLE=1/1 POSITIVE_CONTROL=1/1 NEGATIVE_CONTROL=1/1 MUTANT_DETECTED=1/1`.
- `c2-count.py` → exit 0: `VERDICTED=24/24 CLASS_CONSISTENT=24/24 REASON_NONEMPTY=24/24 FLIP_NONEMPTY=24/24 VOCAB_OK=24/24 DUPLICATE_ROWS=0 ROWS_OUTSIDE_SLICE=0 C2=PASS`.
- **holds**.

**4. verdict map** — tool exit 0 ok (slice 24 rows / examine 43 quotes / verdict 24 rows / digests register+cache sha256) observed. exit 1 findings: reproduced — `slice --register <empty>` → `quarantine-check: slice is empty — the register holds no data rows for chousa`, exit 1. exit 2 usage/env: reproduced — missing register/cache → `register not readable` / `capture cache not readable`, exit 2 (×3 subcommands). C1 set: all six counts observed at 4/24, 43/43, 1/1×4, exit 0; failed path exercised via control (exit 1). C2 set: all seven metrics observed, exit 0; failed path via control (exit 1). `none superseded (current versions)`: single `tools/quarantine-check.py`; grep across tree finds no later quarantine-check tool/counter (round43+ artifacts are distinct tools absent-split/research-gate). — **holds**.

**5. self-test** — (a) C1 do-nothing control: reproduced in a scratch tree without `tools/` → stderr `c1-count: the gate tool is absent: …/c1ctl/tools/quarantine-check.py`, exit 1; committed control `corpus/evidence/round42/controls/c1-control-before.txt` records the identical message/exit. (b) mutant register (one lane data row dropped): counter reports `MUTANT_DETECTED PASS mutant=23 base=24`. (c) C2 do-nothing control (S093 flipped absent→present): reproduced by mutating `quarantine-verdicts.tsv` in a scratch tree → `CLASS_CONSISTENT=23/24 … MISMATCH S093 table=present independent=absent C2=FAIL`, exit 1; committed control `c2-control-before.txt` matches exactly. (d) tool slice on empty register: exit 1 (above). — **holds**.

**6. pinned values** — `corpus/evidence/round42/claims.md` exists at 5e8c7ad; header: `Frozen at the round-42 freeze commit… Base: lane tip 872bf3a3507875b382313f955d15960f9638256f`. Both pinned commits exist: `git cat-file -t dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc` → commit; `… 872bf3a3507875b382313f955d15960f9638256f` → commit. `git show dd63b6c:corpus/evidence/round42/claims.md | sha256sum` = `git show 5e8c7ad:…` = `48d67eb5e16f799259e2de13082672119488ab75d545db2055993c18655ccff1` (claims.md unchanged since freeze; freeze commit stat carries claims.md + tool + both counters). All 5 receipts exist; bodies byte-identical to my fresh runs (diff after 3 header comment lines): `digests.txt`, `examine.txt`, `verdict.txt`, `c1-after-freeze.txt`, `c2-after.txt`. — **holds**.

**7. write scope** — `read-only (tool and counters write nothing; C1's scratch controls live in its own temp dir)`. Tool subcommands write nothing (verified). **But** running `c1-count.py` in the tree creates `tools/__pycache__/quarantine-check.cpython-314.pyc` (fresh archive: 19 committed .pyc → 20 after run; that pyc is NOT in the committed tree — `git ls-files | grep quarantine-check.*pyc` empty; committed pycs are all under `.ufo/waves/…` scratch dirs). A new untracked bytecode file in the lane root is a filesystem write, so "counters write nothing" is not literally true; no data/receipt/table content is touched. — **holds-narrowed**: trivial incidental Python bytecode cache (untracked), not a content write; all operational claims stand.

**8. owner** — `chousa` — holds.

## Verdict
Row **holds** on every operational cell (entry, verdict map, self-test, pinned values, name/kind/owner, 8 cells). One narrow caveat: C1 counter emits an untracked `tools/__pycache__/quarantine-check.cpython-314.pyc` on run (write-scope cell only literally).
