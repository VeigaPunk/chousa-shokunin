# Round 41 — verifier spot-check (non-author integrator)

author: hyaku closure (non-author integrator, @m_swe)
date: 2026-10-24
round: 41 (attempt 1)
lane: chousa
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/chousa.md` (erratum b0b681d appended post-filed)
measured-claims base: lane tip `a3aac04492a3a5e99e351fc9941fcba801c152fe`; current lane tip at closure: `d720b1de0864e68d7cbe79fbb9d3f1a340bade25` (append-only lesson addendum, lane identity)

## Step-1 conformance

- Report committed by lane identity: `a54d40c8a9a9bf3a7f5706d8f262eab26172690e` (`chousa-shokunin <chousa@shokunin.local>`); erratum appended by same identity (`b0b681d5`, +4 lines, append-only — conforms to the filed-bytes rule).
- `SHONEN` heading present in the report with one `[~]` line per box, each carrying a resolvable pointer (`SKILL.md` Gates table, LOG.md round-41 entry, `tools/research-gate.sh --selftest`, `PROVINCE.md`).
- Cited commits `b173b094`, `1bd90013`, `a3aac044` — all `git cat-file -t` = commit and `merge-base --is-ancestor <h> master` holds; lane master and HEAD both resolve `d720b1de` at closure (addendum is a direct child of `a3aac044`, lesson-only, +19 lines).
- `jj-lane.sh state`: `branch=master local=d720b1de remote=d720b1de ahead=0 behind=0 head=detached` — pushed, clean of lane debt.
- Worktree leftovers: `tracked=2 untracked=33` — all under `.ufo/waves/round-40/w1/` (orchestrator-dispatched r40 wave seat reports + `swarm-registry.json`, not lane-authored) plus `corpus/evidence/round41/receipts/cells/cells.json` (modified — the receipt file c1-count.py rewrites on every run; observed tmp-path churn only, consistent with an r40 wave seat re-verifying the receipts, e.g. ExecC1Selftest). Named here per inherited-state rule; left untouched and restored to its pre-closure bytes after the closure's own counter runs (sha256 `93291368…` before and after).
- Dispatched prompt `.ufo/prompts/chousa-round-41.md` carries the full round contract: mission/axes binding, 1–3 falsifiable claims, frontier step (SOURCES contract v1, census command, mistakes, sourced claim), L2 floor, report contract incl. `SHONEN` heading + commit-hash citation + report path + commit-before-report ordering + lane write scope, push scope, L0 side channel; hyaku addendum §6. Committed at `e3d0b034`.
- Driver digest (`.ufo/watchdog.log` lines 1168/1172): `2026-10-24T04:15:40-03:00 launch chousa round=41 pgid=1521000 driver=hyaku-inline attempt=1`; `2026-10-24T04:34:10-03:00 complete chousa round=41; hyaku-inline attempt=1`.
- Marker check: real report with substance, not a marker — status `ok`.

## Per-claim re-checks (re-measured by closure; commands run on the committed work tree = tip bytes for all measured files)

### C1 — operability (lowest non-retired axis, 3/10) — RE-MEASURED

- `python3 corpus/evidence/round41/c1-count.py --gate .ufo/waves/round-41/controls/base-gate-r41.sh` → `CAPTURE_PIN_MATCH=1/12`, exit 1 (only S1-base-clean passes; S2–S12 all fail). Matches committed `controls/control-before.txt` and the report's before figure.
- `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` → `CAPTURE_PIN_MATCH=12/12`, exit 0 (S1–S12 PASS). Matches committed `corpus/evidence/round41/measure-after-c1.txt`.
- Mechanism spot-read in committed bytes `a3aac044:tools/research-gate.sh`: `CAPTOOL_NAMES=(mktemp sed mkdir cat rm sort readlink dirname date tr wc od head stat)` (:332), `captool_pin_init` (:355, called :383), `CAP_CHILD_PATH=${RESEARCH_GATE_CAPTURE_PATH:-/usr/bin:/bin}` (:4071), child env `-u LD_PRELOAD -u LD_LIBRARY_PATH` + `PATH="$CAP_CHILD_PATH"` (:4153-4154). Real mechanism, not assertion.
- Receipt semantics: the counter stamps `gate` + per-cell evidence into `receipts/cells/cells.json`; closure restored the wave-state bytes after its runs (the file is a run-artifact overwritten by design — recorded as observation, not defect).
- Verdict: **improved** (frozen predicate, do-nothing control 1/12 < target, kill rule satisfied before data).

### C2 — calibration (W04 disposition alignment) — RE-MEASURED

- `python3 corpus/evidence/round41/c2-count.py` (landed tree) → `W04_DISPOSITIONED=5/5`, exit 0. Matches committed `measure-after-c2.txt`.
- Before-state reproduced without touching the lane: a `/tmp` copy of `c2-count.py` resolves `LANE` to a tree with no TSV → `W04_DISPOSITIONED=0/5` (S051/S053/S073/S074/S075 all "no disposition row"), exit 1. Matches committed `controls/c2-control-before.txt`.
- `w04-dispositions.tsv` read: 5 rows, each with warn-id, url, disposition vocab (`same-page-distinct-section` ×3, `supersede-row-required`, `retained-rejected-duplicate`) and an evidence cell resolving to SOURCES rows/search-log text. Join-based, not advisory prose.
- Verdict: **improved**.

### No-harm — EVIDENCE-VERIFIED (sibling gate not executed by closure; committed tally inspected)

- Committed evidence: `corpus/lessons/round-41.md:11` records `PASS (275 cases, 0 skipped)` on the landed gate with the `metadata-stat-unavailable` regression repaired through `RESEARCH_GATE_STAT` (red-before shown: non-GNU stub refused `STAT_PROVENANCE`); `SCORECARD.md` r41 section records the same tally; r39 spot-check + `capture-bash-pin-r39.md` establish the 272→275 baseline lineage. Revision measured: work commit `1bd90013` / tip `a3aac044`.
- `SCORECARD.md` diff `6bc90e04 → a3aac044`: additions only (r41 measured-claims table, r40 routed dispositions, planned r42); no score lowered, no axis harmed; depth/coverage/freshness marked narrowly improved, adjacency unchanged — consistent with the diff (new sourced knowledge entry + sources).

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured 1/12 → 12/12 on the frozen 12-cell table |
| calibration | improved | C2 re-measured 0/5 → 5/5 join-verified dispositions |
| depth | improved | sourced `capture-path-pin-r41.md` with measured surface + named limits |
| coverage | improved (narrow) | invocation-pinning subground admitted; PROVINCE-adjacent craft ground |
| freshness | improved | S075/S076 opened this round from installed copies; S067/S071/S072 re-cited |
| adjacency | unchanged | contested-scope handling unchanged; r40 wave findings routed, not absorbed |

## Discernment spot-check (LEARNING.md — non-author, ≥1 admit + ≥1 reject + ≥1 new SOURCES row)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/capture-path-pin-r41.md` | ADMIT | the entry + `c1-count.py` run + gate bytes `a3aac044:tools/research-gate.sh` | agree | provenance trio present; cites S075/S076/S067; mechanism verified in committed bytes (pin table, CAP_CHILD_PATH, LD scrub); kill record reproduces under my own runs (1/12 → 12/12); named limits enumerated honestly |
| reject: fetching canonical URLs of the man pages | REJECT | `.ufo/l0-questions.md` (fetch-scope `8d77e6c1` unanswered) + r40 wave `SentinelFetchScope` findings (unapproved docs.python.org GET) | agree | with the fetch-scope L0 open and an r40 seat's unapproved live GET on record, refusing egress and recording roff-printed URLs as provenance is the correct gate call; flip condition stated (operator approval or L0 answer) |
| SOURCES row S075 (`mktemp(1)` installed man) | row written this round | `zcat /usr/share/man/man1/mktemp.1.gz` | agree | ≤25-word quote verified verbatim at decompressed DESCRIPTION (line 11, inside cited 8–12); `#mktemp-d` tty-link at decompressed line 16 as recorded; file SHA-256 `9abddc15…` re-derived byte-exact; tier A for installed-binary contract is right |
| SOURCES row S076 (`sed(1)` + `sed.info`) | row written this round | `zcat /usr/share/info/sed.info.gz` + `sha256sum` of both installed files | agree | quote verified verbatim at node 3.3 decompressed lines 621–622 (inside cited 619–623); both file SHA-256s re-derived byte-exact (`06c76292…` man, `35eb9c6f…` info); tier A justified |
| search-log r41 entry | recorded | `corpus/SOURCES.md` ## Search log | agree | bounded, named surfaces, identified/screened/included counts, stop rationale, open-L0 clause restored (F3 remediation) |

Spot-check result: **agree on all sampled decisions (5/5)** — admit, reject, and both new rows re-opened and verified from installed copies only. No external fetch performed by this closure.

## Trend verdicts

- **expansion: improved** — one admitted knowledge entry on previously-unheld ground (capture-invocation pinning) citing mined S075/S076 opened this round; sources 74 → 76 rows re-counted (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 74 @ `6bc90e04`, 76 @ `a3aac044`).
- **quality: improved** — invocation surface fails closed under PATH/loader interposition (do-nothing 1/12 → 12/12); selftest 275/275 per committed evidence; the only regression was repaired through the documented override channel with red-before shown.
- **discernment: improved** — the non-author spot-check (this file) agrees with the gate on the sampled admit and reject (LEARNING.md: agreement on admits and rejects = improved).

## Census

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0; five advisory W04 warnings (S051, S053, S073, S074, S075) + `ok` — all five carry C2 disposition rows.

## Defects and routed items (status-neutral unless noted)

- D1 (routed, next owner = r40 counter lineage): r40 `c1-count.py` at committed tip reports `R39_ACTIVE_RECEIPTS=2/6` (gate-sha256 refusals after the r41 gate commit); 6/6 replays only at pinned `6bc90e0` + gate `4253c187…`. Lane's post-landing addendum + fleet erratum correctly scope this as expected receipt-sha binding; successor-counter design (named measured revision / reissue under new sha) is routed to round 42 — per the lane's own r42 pre-registration.
- D2 (observation): receipt artifact `corpus/evidence/round41/receipts/cells/cells.json` is tracked yet rewritten on every counter run; it drifts in the shared worktree (wave seats and this closure both regenerated it). Consider untracking or seeding it in the scenario design — routed to the lane's next round.
- D3 (observation): the r41 wave remains prepared-not-dispatched (35 seats, validator `plan`/`run` exit 0); same as r40 — orchestrator dispatches prepared waves. Not a lane defect.
- D4 (note for operator): SHONEN boxes are all `[~]` lane-asserted with resolvable pointers; they are checkable by a non-author (gate selftest, LOG entries, PROVINCE) — promotion is operator-owned and not exercised here.
- No conformance defects found in the report contract; the lane's disclosure of post-filed addenda (lesson addendum d720b1de, report erratum b0b681d) conforms to append-only correction rules.

## Re-measurement ledger

| check | command | observed | committed record | match |
|---|---|---|---|---|
| C1 before | `c1-count.py --gate controls/base-gate-r41.sh` | `CAPTURE_PIN_MATCH=1/12` exit 1 | `controls/control-before.txt` | yes |
| C1 after | `c1-count.py --gate tools/research-gate.sh` | `CAPTURE_PIN_MATCH=12/12` exit 0 | `measure-after-c1.txt` | yes |
| C2 before | `c2-count.py` (TSV absent, /tmp copy) | `W04_DISPOSITIONED=0/5` exit 1 | `controls/c2-control-before.txt` | yes |
| C2 after | `c2-count.py` | `W04_DISPOSITIONED=5/5` exit 0 | `measure-after-c2.txt` | yes |
| census | `sources-census.sh validate chousa` | exit 0, 5× W04 + ok | report/lesson census | yes |
| selftest | committed tally (not re-executed) | `PASS (275 cases, 0 skipped)` | lesson :11, SCORECARD r41 | evidence-verified |
