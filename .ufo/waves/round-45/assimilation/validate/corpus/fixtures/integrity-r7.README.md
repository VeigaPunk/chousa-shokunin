# integrity-r7.md / integrity-r7-broken.md — reference-integrity record pair (chousa round 7)

Round-7 binding-integrity move (dispatch 2026-10-16): the round-6 gate
(`0c3d51ed…`) composes one verdict from four modes, but a record can carry
DANGLING cross-section references — an id-shaped token that names no declared
row — and every one of the six landed modes passes it. This fixture pair
pre-registers, as fixed local inputs with fixed expected outputs, the verdict a
landed `integrity` section must produce: `integrity-r7.md` carries a
reference-integrity mix in which every claim-id / source-id / sweep-id
reference resolves, and `integrity-r7-broken.md` carries exactly two dangling
references (a sweep cell naming an UNDECLARED claim id, a hop citing an
UNDECLARED source id) that pass every r1-r6 mode and must make the composed
verdict DRIFT with two `REF_UNRESOLVED` findings.

## Authoring state

Lane HEAD `4835426` (round-6 records commit). Before-state runs use the
round-6 gate recovered from git —
`git show 4835426:tools/research-gate.sh` →
`0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8` — where
the `integrity` section does not exist. After-state runs use the landed round-7
revision `3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2`
(sha re-checked identical before and after the runs below; the mode's sha moved
several times during the wave, so the after-state block pins it). The fixtures
are uncommitted under `corpus/fixtures/`; no commits by this seat.

## What each file is

| file | role |
|---|---|
| `integrity-r7.md` | positive control — the `full-r6.md` record bytes plus the reference mix below; every reference resolves |
| `integrity-r7-broken.md` | dangling twin — differs from the positive in exactly five lines: the two planted dangling references plus `claims_file` / `note` / `question` text (not defects; the companions are byte-identical) |
| `integrity-r7.claims.jsonl` / `integrity-r7-broken.claims.jsonl` | the bound claims companion, byte-identical to each other; three verbatim spans in the pinned exports, all `expect=supported` |

Both records are `full-r6.md` (sha256 `878c2c50…`) with the mix applied;
everything else — the four sources, three resolved export hops, three pointed
claims, two negatives, the two rejections, the approval row — is the full-r6
material unchanged.

## The mix (positive, `corpus/fixtures/integrity-r7.md`)

| path:line | added material | reference class | resolves to |
|---|---|---|---|
| `integrity-r7.md:31` | Chain hop 4: `| 4 | C3 | S4 | line | this record is declaration-and-pointer-level acceptance only. | resolved | … |` | source-id reference `S4` (and claim-id reference `C3`) | `## Sources` row S4 (tier `fleet-gate`); the anchor is `corpus/knowledge/archived-export-intake.md:11`, verified `at=line:11` |
| `integrity-r7.md:54` | Sweeps row SW3: `| SW3 | C2 | <empty archive naming> | … |` | claim-id reference `C2` | `## Claims` row C2 |

Existing material the extractor also sees, all resolving: hops 1-3
(`from=C1..C3`, `to=S1..S3`), SW1.claim_id=`N1` / SW2.claim_id=`N2`
(Negatives rows), N1.sweep=`SW1` (Sweeps row), SW2's `where=S1,S2,S3`
(Sources rows). SW3's `where` re-runs SW1's exact
`research/deep-research-2026-09-28/saved-*,research/deep-research-2026-09-28/*-snapshot-*`
naming, so its verified verdict rides the same measured-empty archive set.

## The twin defects (`corpus/fixtures/integrity-r7-broken.md`)

| path:line | cell | defect | expected after-finding |
|---|---|---|---|
| `integrity-r7-broken.md:31` | Chain hop 4 `from` | `C3` → `S9` — a source id declared nowhere | `REF_UNRESOLVED` (`kind=source id=S9 section=chain row=4 cell=from`) |
| `integrity-r7-broken.md:54` | Sweeps SW3 `claim_id` | `C2` → `C9` — a claim id declared nowhere | `REF_UNRESOLVED` (`kind=claim id=C9 section=sweeps row=SW3 cell=claim_id`) |

`diff integrity-r7.md integrity-r7-broken.md` is exactly five lines: those two
defect lines, the twin's `claims_file` row naming its own (byte-identical)
companion, and the `note`/`question` text that names the twin's purpose.

Both defect cells sit on rows the gate does NOT exempt (chain row status
`resolved`; sweeps row with no status column) — deliberately, so both ids are
verdict-bearing regardless of how the exemption boundary is read. The landed
integrity mode counts the reference tokens of an exempt-status row
(unresolved / blocked-no-fetch / rejected / labelled-dead / not-applicable)
exempt rather than required to resolve, pinned by the impl's own selftest case
`integrity-exempt-counted`; this pair also carries one such token measured in
place — N2's `sweep=SW2` binding, `REF kind=sweep id=SW2 … observed=exempt
verdict=exempt status=unresolved`. An earlier revision of this pair put the
source defect behind an exempt hop; measured at the first landed integrity
revision it was counted exempt, so the pair was re-shaped to the non-exempt
`from` cell — the class boundary is named here, not silently tolerated.

## Before state — measured at gate `0c3d51ed…` (verbatim)

Both fixtures compose CLEAN through every landed mode: the reference cells sit
in positions no r1-r6 mode reads (`chain.from` is not inspected by the
structure or chain modes; a sweeps `claim_id` is not inspected by any mode).

```text
$ bash gate-r6-0c3d51ed.sh verify-all corpus/fixtures/integrity-r7.md --root ..
research-gate research-gate-r1 — ts=… — mode=verify-all — record=corpus/fixtures/integrity-r7.md — claims=/…/corpus/fixtures/integrity-r7.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

$ bash gate-r6-0c3d51ed.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..
research-gate research-gate-r1 — ts=… — mode=verify-all — record=corpus/fixtures/integrity-r7-broken.md — claims=/…/corpus/fixtures/integrity-r7-broken.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0        # the hole: both dangling references pass all six r1-r6 modes
```

The chain mode's own hop-4 line for the twin shows the dangling `from` cell is
not read at all (identical to the positive's, byte for byte):

```text
CHAIN hop=4 status=resolved observed=verified source=chousa-shokunin/corpus/knowledge/archived-export-intake.md anchor=line:"this record is declaration-and-pointer-level acceptance only" at=line:11 verdict=match
RESOLVED_HOPS=4/4
RESEARCH_GATE: CLEAN (hops=4 verified=4 exempt=0 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
```

## After state — measured at gate `3ba718bf…` (verbatim)

```text
$ bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root ..
research-gate research-gate-r1 — ts=… — mode=integrity — record=corpus/fixtures/integrity-r7.md
REF kind=claim id=C1 section=chain row=1 cell=from observed=resolved verdict=match
REF kind=source id=S1 section=chain row=1 cell=to observed=resolved verdict=match
REF kind=claim id=C2 section=chain row=2 cell=from observed=resolved verdict=match
REF kind=source id=S2 section=chain row=2 cell=to observed=resolved verdict=match
REF kind=claim id=C3 section=chain row=3 cell=from observed=resolved verdict=match
REF kind=source id=S3 section=chain row=3 cell=to observed=resolved verdict=match
REF kind=claim id=C3 section=chain row=4 cell=from observed=resolved verdict=match
REF kind=source id=S4 section=chain row=4 cell=to observed=resolved verdict=match
REF kind=sweep id=SW1 section=negatives row=N1 cell=sweep observed=resolved verdict=match
REF kind=sweep id=SW2 section=negatives row=N2 cell=sweep observed=exempt verdict=exempt status=unresolved
REF kind=claim id=N1 section=sweeps row=SW1 cell=claim_id observed=resolved verdict=match
REF kind=claim id=N2 section=sweeps row=SW2 cell=claim_id observed=resolved verdict=match
REF kind=source id=S1 section=sweeps row=SW2 cell=where observed=resolved verdict=match
REF kind=source id=S2 section=sweeps row=SW2 cell=where observed=resolved verdict=match
REF kind=source id=S3 section=sweeps row=SW2 cell=where observed=resolved verdict=match
REF kind=claim id=C2 section=sweeps row=SW3 cell=claim_id observed=resolved verdict=match
INTEGRITY refs=16 resolved=15 unresolved=0
RESEARCH_GATE: CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..
research-gate research-gate-r1 — ts=… — mode=integrity — record=corpus/fixtures/integrity-r7-broken.md
REF kind=source id=S9 section=chain row=4 cell=from observed=unresolved verdict=mismatch
REF kind=claim id=C9 section=sweeps row=SW3 cell=claim_id observed=unresolved verdict=mismatch
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
INTEGRITY refs=16 resolved=13 unresolved=2
RESEARCH_GATE: DRIFT (refs=16 resolved=13 unresolved=2 exempt=1 findings=2 drift=2)
exit=1

$ bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --root ..
research-gate research-gate-r1 — ts=… — mode=verify-all — record=corpus/fixtures/integrity-r7.md — claims=/…/integrity-r7.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=16 resolved=15 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..
research-gate research-gate-r1 — ts=… — mode=verify-all — record=corpus/fixtures/integrity-r7-broken.md — claims=/…/integrity-r7-broken.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity state=run verdict=DRIFT findings=2 drift=2 tally=INTEGRITY refs=16 resolved=13 unresolved=2
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2)
exit=1        # the two dangling references, and nothing else, drift the composition
```

The pre-registered contract above holds as pre-registered: `integrity-r7.md`
composed CLEAN with `unresolved=0`; `integrity-r7-broken.md` composed DRIFT
naming exactly the integrity section, with exactly the two dangling ids —
`S9` (chain `from`) and `C9` (sweeps `claim_id`) — while structure, claims,
chain and sweeps all stay CLEAN with the same tallies as the positive. The
round-6 trio regresses unchanged (full-r6 CLEAN run=5 with its integrity
section CLEAN; full-r6-broken DRIFT drift-sections=2; full-r6-absent CLEAN
run=4 absent=1), and the selftest closes `PASS (74 cases)` at the same
revision, whose r7 family independently witnesses these classes:
`integrity-pass`, `integrity-fail-dangling-claim` (a sweeps `claim_id`),
`integrity-fail-dangling-source` (a rejection `ref`),
`integrity-fail-dangling-chain-claim` (a chain `from`),
`integrity-fail-dangling-sweep` (a claims `sweep`), `integrity-exempt-counted`,
`integrity-fail-counting`, two setup exits, and the composed `all-dangling`.

## Honest boundaries

- The mix and the twin were authored before the `integrity` section landed and
  re-measured at the landed revision; the before-state uses the round-6 gate
  recovered from git, so both sides of the falsifiable claim are measured, not
  argued. A later revision that changes the extraction rule should reproduce
  this contract from the record bytes and this README.
- The exempt-status class is deliberately not a drift witness in this pair
  (see §The twin defects): the landed section counts exempt-row tokens
  exempt-but-counted, and this pair measures that boundary in place through
  N2's `sweep=SW2` token rather than asserting against it.
- SW3 re-checks the same path-set emptiness as SW1 (two saved-copy naming
  globs), not a content census; both verified verdicts are properties of
  `research/deep-research-2026-09-28/` at the pinned fleet state, and hop
  anchors (including the intake's line 11) are properties of the pinned local
  bytes. Under a different `--root` the fleet-root-relative pointers do not
  resolve and every mode reports refused/unresolved.
- No URL appears anywhere in either record; any re-run is local reads only.
  Nothing here is a receipt: the round's receipts, note, scorecard and LANE
  manifest belong to other seats.
- No scalar score, no promotion, no field-readiness claim.

## Inventory sha256 (2026-10-16, as measured above)

```text
4310ce86aa45f3d7d4b7d04c4ebf480a7b59748510ab0f132c5411dd8acd1b1b  integrity-r7.md
fd4e213f03faf9a76bbca3896b11fe6530878e727fefb974043ffb4a9f9a05b8  integrity-r7-broken.md
8e83b23d04e92961f7781e556d600b94a313e083c79d32a517fcb16ec17dabb3  integrity-r7.claims.jsonl
8e83b23d04e92961f7781e556d600b94a313e083c79d32a517fcb16ec17dabb3  integrity-r7-broken.claims.jsonl
```

## Re-run

```bash
cd chousa-shokunin
sha256sum tools/research-gate.sh
bash tools/research-gate.sh verify-all       corpus/fixtures/integrity-r7.md --root ..          # composed CLEAN; integrity unresolved=0
bash tools/research-gate.sh verify-all       corpus/fixtures/integrity-r7-broken.md --root ..   # composed DRIFT, drift-sections=1, two REF_UNRESOLVED
bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root ..
bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..
bash tools/research-gate.sh verify           corpus/fixtures/integrity-r7-broken.md --root ..   # the hole: structure stays CLEAN
bash tools/research-gate.sh verify-chain     corpus/fixtures/integrity-r7-broken.md --root ..
bash tools/research-gate.sh verify-sweeps    corpus/fixtures/integrity-r7-broken.md --root ..
bash tools/research-gate.sh verify-claims    corpus/fixtures/integrity-r7.claims.jsonl --root ..
bash tools/research-gate.sh --selftest

# before-state (round-6 gate recovered from git; sha256 0c3d51ed…)
git show 4835426:tools/research-gate.sh > /tmp/gate-r6-0c3d51ed.sh
bash /tmp/gate-r6-0c3d51ed.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..   # CLEAN: the hole, dangling refs pass
```
```