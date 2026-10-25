# RevRowTagCount — attack on SKILL.md `## Gates` row `tag-count` (QUALITY 64, r45)

Seat: L1Chousa45.RevRowTagCount. Commit measured: 5e8c7ad2f7b8254d83358820286e3d12ca4672d1
(archive tree at /tmp/chousa-r45-RevRowTagCount/tree; all runs inside that tree).
No tools installed; no network; no lane writes; scratch deleted at end.

## Row under attack (SKILL.md line 111, verbatim)

```
| `tag-count` (QUALITY 64, r45) | check | `python3 corpus/evidence/round45/tag-count.py [--scorecard PATH] [--from N] [--to N]` (default rounds ≥ 45) | `TAGGED=k/n`; exit `0` every claim row of the selected round sections carries a `ground` or `plumbing` cell and n ≥ 1 · exit `1` any untagged row or no rows · exit `2` scorecard missing | `--from 35 --to 44` → `TAGGED=0/22`, exit 1 (`corpus/evidence/round45/controls/tag-control-r35-r44.txt`) | proposal `considerthese/2026-10-24.md` (2026-10-24); QUALITY 64 | read-only | chousa |
```

Cell count: **exactly 8 cells** (CELL_COUNT 8: name, kind, entry, verdict map, self-test, pinned values, write scope, owner). Header row has 8 columns. ✓

## Per-cell verdict

### 1. name — holds
` `tag-count` (QUALITY 64, r45)`. Matches QUALITY.md entry 64 (line 583: "64. **Every round verdict tags each claim as research ground or plumbing.**") which names `corpus/evidence/round45/tag-count.py` as its check.

### 2. kind — holds
`check`. QUALITY 64 is a check (not a gate/tool), consistent.

### 3. entry — holds
`python3 corpus/evidence/round45/tag-count.py [--scorecard PATH] [--from N] [--to N]` (default rounds ≥ 45).
- Script exists and is executable at the commit: `corpus/evidence/round45/tag-count.py` (sha256 587007fa8348249162b90445fa03facbb0939adcd788d7ed0f5bf055ed831e1b).
- argparse accepts exactly `--scorecard`/`--from`/`--to`; defaults lo=45, hi=10**6, scorecard = LANE/SCORECARD.md (LANE = parents[3] of resolved script path = tree root). SCORECARD.md exists at commit (199434 bytes) — default target resolves.
- Verified by running: all three options behave as named (below).

### 4. verdict map — holds
Row text: `TAGGED=k/n`; exit 0 every claim row of selected round sections carries ground/plumbing and n ≥ 1; exit 1 any untagged row or no rows; exit 2 scorecard missing.

Observed (verbatim decisive output):
- Default run (rounds ≥ 45): `TAGGED=0/0` `TAG=FAIL`, RC=1. No `## Round 45+` section exists in SCORECARD.md at the commit (`grep -n '^## Round'` max is Round 44; CLAIM_ROWS_ROUND45PLUS 0), so this falls exactly on the documented exit-1 "no rows" branch — matches the verdict map as written. (Note: exit-0 branch is unreachable from committed state; not a defect of the row, see Residual.)
- Exit 0 branch reproduced with a synthetic scorecard (tagged rows): `TAGGED=3/3` `TAG=PASS`, RC=0.
- Exit 1 branch reproduced with one untagged row: `UNTAGGED round=45 | C1 | operability | nope |`, `TAGGED=1/2` `TAG=FAIL`, RC=1.
- Exit 2 branch: `--scorecard /nonexistent-missing-scorecard.md` → `TAG=FAIL scorecard-missing`, RC=2.
All four stated behaviors reproduce exactly.

### 5. self-test — holds
Row text: `--from 35 --to 44` → `TAGGED=0/22`, exit 1 (`corpus/evidence/round45/controls/tag-control-r35-r44.txt`).

Observed: `python3 corpus/evidence/round45/tag-count.py --from 35 --to 44` ⇒ stdout byte-identical to the control file except the capture's trailing `exit=1` line (script itself never prints `exit=`); 22 `UNTAGGED round=35..44` lines; `TAGGED=0/22`; `TAG=FAIL`; TRUE_RC=1. Control file exists at commit (sha256 a0dce153b0bc55d0359ed7ad57217760641d51f5d8bbf0cb5937ab9faa509502). ✓

### 6. pinned values — holds
Row text: proposal `considerthese/2026-10-24.md` (2026-10-24); QUALITY 64.
- `considerthese/2026-10-24.md` exists at commit (sha256 5837fc7de0a5456072592e1b5d332dc1fb3eb51bfc6f5ca2680e72347a7696ba); its "Self-improvement proposals" section contains verbatim the bullet "**Tag each round as research ground or plumbing.**" (line 58), dated 2026-10-24. Tag-count docstring's "Proposal mined from considerthese/2026-10-24.md" is accurate.
- QUALITY 64 exists in `corpus/QUALITY.md` (line 583) and its text matches this gate's semantics (ground/plumbing tag cells; same check invocation; same r35–44 control).
- Date (2026-10-24) matches the proposal file's header.

### 7. write scope — holds
`read-only`. Source review of tag-count.py: opens only the scorecard for reading; no writes (no receipt, no temp files, no mutation of the tree). Runs inside a copy of the committed tree changed nothing.

### 8. owner — holds
`chousa`, matching the other rows in `## Gates`.

## Overall verdict
All 8 cells **hold**. No falsification found. The counter is operable, the verdict map and self-test both reproduce exactly, and the pinned-value citations resolve at the commit.

## Residual risk / verification gaps
1. Default invocation on the committed tree prints `TAGGED=0/0` and exits 1 because SCORECARD.md has no round ≥ 45 section yet. This is the documented "no rows" branch, not a defect — but it means the gate is currently vacuous (can only fail) until a round-45 verdict section lands; re-check after round 45 closes.
2. The counter's "tagged" test is syntactic: a cell equal to `ground`/`plumbing` (after `*`/whitespace strip) — it does not judge whether the tag is *truthful* (QUALITY 64 itself says "A tag's truth is a reader's check"). Not a row defect; documented in QUALITY 64.
3. Control file captures a trailing `exit=1` line the script does not produce; this is a capture convention, output otherwise identical.

Commands producing decisive output (all run inside the archive tree):
- `python3 corpus/evidence/round45/tag-count.py` → `TAGGED=0/0` `TAG=FAIL`, RC=1
- `python3 corpus/evidence/round45/tag-count.py --from 35 --to 44` → 22× `UNTAGGED`, `TAGGED=0/22`, `TAG=FAIL`, TRUE_RC=1; diff vs control (minus last line) empty
- `python3 corpus/evidence/round45/tag-count.py --scorecard /nonexistent-missing-scorecard.md` → `TAG=FAIL scorecard-missing`, RC=2
- synthetic tagged scorecard → `TAGGED=3/3` `TAG=PASS`, RC=0; synthetic with one untagged row → `TAGGED=1/2` `TAG=FAIL`, RC=1
- `grep -n '^## Round' SCORECARD.md | tail -8` (max Round 44); CLAIM_ROWS_ROUND45PLUS = 0
- sha256: considerthese/2026-10-24.md 5837fc7de0a5456072592e1b5d332dc1fb3eb51bfc6f5ca2680e72347a7696ba; tag-count.py 587007fa8348249162b90445fa03facbb0939adcd788d7ed0f5bf055ed831e1b; control a0dce153b0bc55d0359ed7ad57217760641d51f5d8bbf0cb5937ab9faa509502
