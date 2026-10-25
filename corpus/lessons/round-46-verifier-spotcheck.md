# Round 46 — chousa verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)

## 1. Conformance (step 1)

- **Report committed by lane identity**: first fleet commit of `.ufo/reports/round-46/chousa.md` is `666c473e` (round-46: chousa report — name the final lane tip), authored `chousa-shokunin <chousa@shokunin.local>`. The report is tracked at that path.
- **SHONEN heading**: present at line 177, exactly one line per box (4 boxes), each `[~]` + resolvable pointer.
- **Cited lane commits exist and are ancestors of `master`** (tip `5c6e2ca1f3f11425c38e42fdcf10914e9b73cb62`): `git merge-base --is-ancestor` OK for `c2f0e9d` (freeze), `1e9756f5` (landing), `b8bc44f4` (final receipt), and base `6e2630a6`.
- **Lane state**: helper `jj-lane.sh state` → branch=master, local=remote=`5c6e2ca`, `ahead=0 behind=0`, head=detached, untracked=0. `status --porcelain` shows only the three inherited modified JSONs (`.ufo/waves/round-40/w1/swarm-registry.json`, `round-41/w1/swarm-registry.json`, `corpus/evidence/round41/receipts/cells/cells.json`) — left-modified since round 45, named as inherited in the report, not round-46 work.
- **Dispatch/completion digest** (from watchdog, copied): `2026-10-25T07:10:05-03:00 launch chousa round=46 pgid=3265394 driver=hyaku-inline attempt=1`; `2026-10-25T08:14:45-03:00 complete chousa round=46; hyaku-inline attempt=1`. No `lane-dead-no-report` line.
- **Prompt contract**: dispatched prompt carries MISSION/AXES binding (§1), claims rules (§2), frontier step (2b), L2 floor (§3), report contract incl. SHONEN heading and commit-hash citation (§4), push scope/L0 (§5), hyaku addendum (§6). Template contract present.

## 2. Claims — re-measured over committed bytes

All after-states re-run by me over `git archive 5c6e2ca1f3f11425c38e42fdcf10914e9b73cb62` (branch tip), not the working tree.

| claim | command (committed) | observed at tip | reported (measure-after.txt) | match |
|---|---|---|---|---|
| C1 operability | `python3 corpus/evidence/round46/c1-count.py` | `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass C1=PASS` exit 0 | identical | ✓ |
| C2 calibration | `python3 corpus/evidence/round46/c2-count.py --list` | `ENTRY_POINTS=81 (tools=8 counters=50 named=79) GATES_ROWS=36 REGISTERED=81/81 UNREGISTERED=0 C2=PASS` exit 0 | identical | ✓ |
| C3 depth | `python3 corpus/evidence/round46/c3-count.py` (+ `--lane-only`) | default `CAPTURE_BOUND=11/11 … C3=PASS` exit 0; `--lane-only` `CAPTURE_BOUND=skipped C3=PASS` exit 0 | identical | ✓ |

Before-states reproduced on the base tree (`git archive 6e2630a6`) + final counters: C1 `C1=FAIL` (tool absent/no-fixtures), C2 `ENTRY_POINTS=79 … UNREGISTERED=21 C2=FAIL` exit 1, C3 `CAPTURE_BOUND=0/11 C3=FAIL` — the before→after direction is real and matches the committed refreshed receipts.

## 3. Gate evidence (PROTOCOL §Gate standard — Closure consequence: committed evidence verified, no lane gate executed)

- **C1**: counter + `tools/inference-ground.py` + six byte-pinned fixtures + CANARY leg; control receipts `c1-controls.txt` (always-pass `JUNK_KILLED=0/3`, cite-only `1/3`, name-oracle `CANARY=fail`) consistent with frozen controls.
- **C2**: registry counter over committed bytes. I re-tested the four *declared* forges (prose paste, six-cell row, eight-pipe no-`exit`, row after next `## `) against the **final** counter: all four remain refused (`C2=FAIL`, nonzero exit). `c2-controls.txt` also contains eight refusal blocks plus two passing blocks (dotslash, 7pipe) — see routed defects 3–4.
- **C3**: `build-spans.py --check` → `SPANS_ROWS=11 STALE=0` exit 0 at tip. Independently re-opened all five captures in the campaign qcache (`.qcache/sha256(url)[:24].txt`): capture digests match `spans.tsv` `capture_sha256` for all five, and for all 11 spans the committed quote appears in the slice at the recorded offset *and* in the citing entry.

## 4. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| admit `evidence-pool-versioning-r39.md` (S085–S087) | admitted | qcache `5a631adb…` (fever.ai dataset page), `1c15b611…` (NAACL-HLT 2018 PDF text), `7800e2e1…` (Zenodo record API) | AGREE | quotes located verbatim in captures and slices (incl. the two-column `evi-`/`dence` hyphen-split join at the PDF); entry cites only `mined` rows |
| admit `evidence-pool-versioning-r39-amendment-2026-10-23.md` (S088–S089; S079/S081 re-bound by document) | admitted | qcache `b73f7e8dd…` (AVeriTeC page), `78761b633aee…` (arXiv HTML) | AGREE | slice quotes verbatim; document-based id binding (not arithmetic) confirmed |
| reject `claim-support-test-r37-amendment-2026-10-23.md` (staged) | rejected | campaign staged rows | AGREE | lane holds neither the base entry nor the wave-3 material it continues; staged ids collide with lane-held rows on *different* documents; flip condition is concrete |
| quarantine row S086 (register `payload-absent`), hand-check verdict | present → adoptable | Scache `1c15b611…` | AGREE | all three register quotes present once the PDF column interleave is removed and the `ev-`/`idence` split is joined (`95.42% precision and 72.36% recall in evi-` / `dence retrieval.`); `absent` was a mechanical false positive of the known class |

## 5. Axes and trend verdicts

Per-axis verdicts (no axis harmed; SCORECARD diff base→tip is additive-only — the round-46 verdict section is appended, no existing row or score changed):

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 re-measured PASS; checklist item now runnable |
| calibration | improved | C2 re-measured PASS on the literal frozen set (81/81) |
| depth | improved | C3 re-measured PASS both modes; entries corrected against captures |
| coverage | improved | two admitted entries on coverage-map ground the map did not hold; five new tier-A `mined` rows S085–S089 |
| freshness | unchanged | captures predate launch; no live surface touched |
| adjacency | unchanged | no sibling holds the ground; fleet habit stated, not discovered |

Trends: **expansion improved** (two admitted entries on uncovered ground, each `source:` citing a mined row opened this round); **quality improved** (three counters pass over committed bytes, fixes shown able to fail in `controls/`, entries narrowed and corrected); **discernment improved** (the outside spot-check agrees with the gate on the sampled admit *and* reject).

## 6. Routed defects for the lane

1. **Freeze-time sentence/code gap (C2).** At freeze, NAMED regex `(?:tools|corpus)/…` was narrower than the literal frozen sentence ("every existing repo-relative `*.py`/`*.sh` path named in SCORECARD/claims", no prefix restriction). The late wave-2 seat `CritC2Scope` surfaced it; the widening (`1e9756f5`) is judged a **repair bringing the instrument up to its literal frozen predicate**, not a §9 post-scoring rule change: the predicate sentence never changed; the change is stricter (79 vs 71 entry points) and cannot manufacture a pass; the claim verifies under *both* instruments (pre-widening 73/73 at `3807537d`; literal-set 81/81 at tip); before/after receipts were both refreshed on the same final instrument. Residual: freeze should pin the literal implementation so sentence == code == receipt at freeze time.
2. **Kill floor not enforced (C2).** The counter only tests `UNREGISTERED==0`; `ENTRY_POINTS` below the frozen floor 71 still prints `C2=PASS` (deleting legs reproduces this). Measured values satisfy the floor (81 ≥ 71), so the claim holds, but route the floor check into the counter.
3. **Stale control receipt labels (C2).** `controls/c2-controls.txt` receipts were generated with the pre-widening counter (header digest `f2fcb654…` vs committed final `f93cb107…`; numbers show `named=66/71`, not final `79/81`). I re-verified the four declared forges against the final counter and they still refuse; refresh the labels/numbers and reconcile the header count ("ten forges: nine refusals and one positive control" vs the file's actual eight refusals + two passing blocks).
4. **Cheap-gate residue (C2).** One 8-pipe row containing `exit` registers paths regardless of cell roles, and `./`-prefixed names register (dotslash). This is a named limit ("row truth is a reader's check"; mention-based, not dependence-based) consistent with the claim's disclaimer — keep it named; consider cell-role parsing next round.
5. **Anchor char drift (C3/SOURCES).** Prose `anchor` characters in SOURCES rows/lesson (e.g., S085 "char 2349"/"char 2360") differ from `spans.tsv` offsets (2280); the registry `anchor` cell is not checked by the counter (named limit) — align or state the revision basis.
6. **Report wording.** "seat `CritC2Scope` produced no report … its report is committed" is self-contradictory; the seat's report *is* committed at tip `5c6e2ca` (added by the final commit). Clean up the wording next round.

## 7. Conclusion

All three claims verify by re-measurement over committed bytes (C1/C2/C3 re-measured; gate evidence verified from committed artifacts), no axis is harmed, and the outside spot-check agrees with the gate on both the sampled admit and reject. Round admitted. SHONEN boxes remain `[~]` (author-asserted) — promo checkable by a non-author, operator-owned.
