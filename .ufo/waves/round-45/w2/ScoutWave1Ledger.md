# Scout Wave-1 Ledger — round 45 wave 2 (falsify)

Seat: L1Chousa45.ScoutWave1Ledger (scout, leaf; no dispatch, no fetch, no lane writes except this report).
Item: account wave 1 at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 — list the 46 registry members, confirm each has a committed report, count dead seats, find out-of-report write admissions, produce the seat-role mix table.

## 1. Members vs committed reports

Registry: `.ufo/waves/round-45/w1/swarm-registry.json` (wave `chousa-r45-w1`, reportDir `.ufo/waves/round-45/w1`).
Committed tree at 5e8c7ad2 (`git ls-tree -r --name-only 5e8c7ad2… .ufo/waves/round-45/w1/`): 45 `.md` report files + `swarm-registry.json` (46 paths total).

Set difference (computed, not eyeballed): members = 46, reports = 45; members without report = **[ScoutCoverageGround]**; reports without member = [] (every committed `.md` maps to a registry member).

### Dead seats: 1

| Seat | role | registry item (abridged) |
|---|---|---|
| ScoutCoverageGround | scout | "Coverage check: read corpus/README.md (coverage map, `## Frontier`) and grep corpus/knowledge/ for archive, snapshot, Memento, cached, AVeriTeC, FEVER, revision-binding… Draft the two coverage-map rows…" — no report file exists at the commit. |

No other member lacks a report. All 45 reports are committed at the target commit (no report is uncommitted or missing).

## 2. Out-of-report write admission

Scanned all 45 reports for restore/revert/checkout/reset/stash/amend/write-outside/admission language. Only one seat's report admits touching a lane file:

**ScribeGateR41** (`.ufo/waves/round-45/w1/ScribeGateR41.md`, lines 59–63, 79–85):

> "C1 unconditionally rewrites `corpus/evidence/round41/receipts/cells/cells.json` (no flag to suppress it): I snapshotted its bytes (sha256 `1f5c0afae8024c50013e9a9060988c14506115125e3823042e4512833f293b80`), ran the counter, then restored the original bytes; post-restore sha256 matches the snapshot exactly. `cells-before.json` untouched. No other lane file touched."
> …
> "Lane left byte-identical to pre-run state (receipt sha256 confirmed after restore). No git/jj operations; no fetch; no census-registry edits."

Verdict: this is a disclosed **transient lane-file write + restore** (the round-41 counter `c1-count.py` writes `receipts/cells/cells.json`; the seat rewrote that committed receipt and restored it byte-identical, sha256-verified). It did not persist — the committed tree at 5e8c7ad2 is unaffected — and it is acknowledged in the report, but it is the only wave-1 admission of writing (even temporarily) outside the seat's own report file, against the milestone's "no production writes by seats". MutC2Forges's "restore" language applies to scratch clones under `/tmp` (lane files hash-verified untouched); MutC1Mutants/MutC3Mutants/ExecLauncherPatch ran solely on /tmp copies; no other report claims a lane-file write.

## 3. Seat-role mix table (46 members)

| role | count | seats |
|---|---|---|
| scribe | 19 | ScribeGateR31, ScribeGateR32, ScribeGateR33, ScribeGateR34, ScribeGateR40, ScribeGateR41, ScribeGateR42, ScribeGateQuarantine, ScribeGateR43, ScribeGateAbsentSplit, ScribeGateR44, ScribeGateLauncher, ScribeGateR45, ScribeRowsNormalize, ScribeEntryFieldPolicy, ScribeEntrySnapshot, ScribeQuality64, ScribeMistakes, ScribeShonen |
| reviewer | 6 | ReviewQuoteReadmeSource, ReviewQuoteReadmeClaim, ReviewQuotePaperCache, ReviewQuotePaper404, ReviewC1Counter, ReviewGatesSection |
| critic | 5 | CritFieldPolicyInference, CritSnapshotInference, CritRejectPoolAmendment, CritC1Harm, CritC2Framing |
| scout | 5 | ScoutProvinceFit, ScoutQuarantineOverlap, ScoutCollisionRecheck, ScoutInheritedTree, **ScoutCoverageGround (dead — no report)** |
| executor | 4 | ExecRecountTrain, ExecEmptyEvidenceRecord, ExecLauncherPatch, ExecLauncherEdge |
| mutation-tester | 3 | MutC1Mutants, MutC2Forges, MutC3Mutants |
| connector | 2 | ConnectSiblings, ConnectRouteTable |
| sentinel | 1 | SentNoEgress |
| simplifier | 1 | SimplifyCounters |
| **total** | **46** | (45 reports committed) |

## 4. Commands (verbatim decisive)

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r --name-only 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 .ufo/waves/round-45/w1/
# → 45 *.md + swarm-registry.json
python3 - <<'EOF'   # set difference
members: 46 reports: 45
members without report: ['ScoutCoverageGround']
reports without member: []
EOF
# jq: .members | to_entries[] | "\(.key) \(.value.role)" → 46 lines; roles as table above.
```

No tools installed; no scratch created; nothing to delete. No fetch/network.

Remaining unknowns: none for the accounting item; the dead seat's content (coverage-map rows) never landed, so its two drafted rows do not exist at the commit — relevant to C3/coverage-map falsification by sister seats.
