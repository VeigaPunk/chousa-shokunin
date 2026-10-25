# ScribeShonen — round-45 wave-1 scribe report

Seat: `L1Chousa45.ScribeShonen` (author-lane scribe, leaf; no dispatch).
Item: read `chousa-shokunin/SHONEN.md`; draft one line per promotion-check box
for the round-45 report, each with its evidence pointer; write this scoped
findings file to `.ufo/waves/round-45/w1/ScribeShonen.md`.

## Verdict

Draft of the four SHONEN.md box lines below. No box can be `[x]`: this
wave's seats are all author-lane, so no named NON-AUTHOR verifier qualifies.
All four are `[~]` with resolvable pointers (all verified to exist on disk at
observation time). Box 3 still carries the open D2 Gates-registry gap,
targeted by C2; C2's live count at observation time is UNREGISTERED=29 —
the gap is open, the ScribeGate peers' rows had not landed when I measured.

## Commands run (verbatim, decisive lines)

1. `python3 corpus/evidence/round45/c2-count.py --list` (lane root, commit
   d82cec9):
   - `ENTRY_POINTS=54  GATES_ROWS=18  REGISTERED=25/54  UNREGISTERED=29`
   - `C2=FAIL` `EXIT=1`; the 29 paths are rounds 31–34 counters (10), rounds
     40–45 counters (18), `corpus/evidence/round44/errata-count.py`, and
     `tools/absent-split.py`, `tools/parent-lifetime.sh`,
     `tools/quarantine-check.py` — identical to the freeze control
     `controls/c2-control-base.txt` (scored at d29bf47d).
2. `python3 corpus/evidence/round45/c1-count.py` → `CASES_MATCH=1/5`
   (`a_empty_exits_3=FAIL b_ok_exits_0=ok c_timeout_exits_3=FAIL
   d_no_timeout_exits_2=FAIL e_start_timeout_s=FAIL`), `C1=FAIL`, exit 1 —
   equals the round-44 tool control `controls/c1-control-r44-tool.txt`; the
   launcher exit-contract work had not landed at observation time.
3. `python3 corpus/evidence/round45/c3-count.py` and `--lane-only`: both
   `ENTRIES=0/2 … C3=FAIL`, exit 1 — staged entries not yet adopted into the
   lane (staged sources exist in `merge/chousa/knowledge/corpus/knowledge/`:
   `evidence-archive-field-policy-r41.md` 2263 B, `evidence-snapshot-coverage-r40.md`
   3037 B; captures exist on disk with sizes 4771 / 145088 / 10184813 B).
4. Pointer existence check (Bash `-e`): `LOG.md`, `PROVINCE.md`,
   `corpus/knowledge/metadata-screen-r25.md`, `corpus/fixtures/archives-r9`,
   `corpus/evidence/round25-measure-after.log`,
   `round25-meta-differential.log`, `round25-final-measure.log`,
   `round25-final-holds.log`, `.ufo/waves/round-25/build/ConnectorMetaSiblings.md`
   — all present. `LOG.md:455` is `## Round 9 — archives verified end-to-end`.
5. `SKILL.md` structure: `## Decision table`, `## Error patterns`, `## Checklist
   (executable)`, `## Gates` sections present; 50 `|`-leading rows in the file;
   the Gates section (415 lines) has 23 `|` rows, of which 18 meet the C2 row
   rule (≥8 `|`, contains `exit`).

## SHONEN.md box lines for the round-45 report

- `[~]` SKILL.md contains real decision tables, error patterns, checklists,
  cited sources — `chousa-shokunin/SKILL.md` (## Decision table / ## Error
  patterns / ## Checklist / ## Gates, 50 rows); `corpus/knowledge/metadata-screen-r25.md`
  (lane assertion; no non-author verifier this wave).
- `[~]` At least one end-to-end domain task executed and logged in LOG.md —
  `LOG.md:455` Round 9 archive verification; `corpus/fixtures/archives-r9/`;
  r25 explicit-root hold battery `corpus/evidence/round25-final-measure.log`,
  `round25-final-holds.log` (lane assertion).
- `[~]` Instructions executable by an agent without oral context — `bash
  tools/research-gate.sh --selftest` → PASS (275 cases); `corpus/evidence/round25-measure-after.log`,
  `round25-meta-differential.log` (lane assertion). Open D2 Gates-registry gap
  carried here, targeted by C2: live `python3 corpus/evidence/round45/c2-count.py --list`
  at commit d82cec9 → `UNREGISTERED=29`, `C2=FAIL`, exit 1 (matches
  `controls/c2-control-base.txt`); gates rows for `tools/parent-lifetime.sh`,
  `tools/absent-split.py`, `tools/quarantine-check.py` and the 26 counter
  entry points were still missing at observation time (ScribeGate peers in
  flight).
- `[~]` No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md`;
  `corpus/knowledge/metadata-screen-r25.md` Limits; `.ufo/waves/round-25/build/ConnectorMetaSiblings.md`
  (lane assertion).

## Gates / touched surfaces

None (scribe only; no production writes). I wrote only this report file.

## Out-of-scope items

- Production edits (Gates rows, AVeriTeC entry adoption, launcher exit-contract
  fix, counts/spans) belong to sibling seats and were observed only.
- No fetch performed; captures read only for existence/size provenance.

## Findings

- Freeze and live C2/C1 states agree: 29 unregistered, 1/5 — D2 open.
- C3 targets are absent from the lane (0/2), consistently with wave-1 build
  phase; the staged sources and captures with the recorded sizes are in place.
- Tool installs/updates: none (no tooling change needed).

## Artifacts

- This report: `.ufo/waves/round-45/w1/ScribeShonen.md`
- Controls read: `corpus/evidence/round45/controls/c1-control-r44-tool.txt`,
  `c2-control-base.txt`, `c3-control-do-nothing.txt`, `c3-control-forged-span.txt`
- Staged sources: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-archive-field-policy-r41.md`,
  `evidence-snapshot-coverage-r40.md`
- Captures: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/{ce16d57277fedfd4f0e7750e,412b146a2720ce6557268d05,974299ae4b5f3bdb808b36a9}.txt`
