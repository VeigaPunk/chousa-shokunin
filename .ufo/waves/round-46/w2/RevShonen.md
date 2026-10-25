# RevShonen — SHONEN.md box audit (round 46, wave 2, falsify)

Item: check each of `SHONEN.md`'s four promotion boxes against the repo state now. SHONEN.md not edited.
Pin: HEAD `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`; byte checks run in a `git archive` extract (`/tmp/chousa-r46w2-RevShonen`, deleted after), lane runs labelled. `SHONEN.md` sha256 `6cebe10f9b2a855447c3cc4e06a8e846c09912285e0c89b79e02854a290e2e71`, last touched `d8c8cff` (2026-10-21, round 25): rounds 26–46 are invisible in it. Standard applied: `corpus/knowledge/audit-r11.md:237-238` (`[x]` only with a named non-author verifier; `[~]` with a resolvable pointer).

## Box verdicts

| # | box (SHONEN.md line) | verdict | how |
|---|---|---|---|
| 1 | SKILL.md: real tables, error patterns, checklists, cited sources (5) | **HOLDS** | sections present and substantive; 17/17 knowledge paths and 12/13 `S###` resolve |
| 2 | ≥1 end-to-end domain task executed and logged (7) | **HOLDS** on its primary leg; **third pointer FAILS** | r9 recipe reproduces byte-for-byte; r25 hold battery 11/12 (S1) |
| 3 | Instructions executable by an agent without oral context (9) | **DOES NOT HOLD as stated** | cited command passes, but 3 of 6 checklist items carry no command, incl. the r46-target item (S2); one cited receipt is now false (S3) |
| 4 | No cross-domain bleed, PROVINCE.md accurate (11) | **HOLDS** | PROVINCE unchanged since `3282042`; all 61 knowledge entries in-province; refused tokens only in deny lists |

## Findings

### S1 (HIGH) — Box 2's r25 "explicit-root hold battery" no longer reproduces: 11/12

`corpus/evidence/round25-holds/battery.sh:73` runs `--drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json`; the stored expectation is `GATE_DRIFT: none` / `EXIT_CODE=0` (`corpus/evidence/round25-holds/holds/drift-r12.log:1-2`). Today:

```
$ bash corpus/evidence/round25-holds/battery.sh /tmp/chousa-r46w2-RevShonen /home/vgpnk/Projects/shokunin
MATCH selftest (exit 0)
-GATE_DRIFT: none        +GATE_DRIFT: +resolvable drift      (diff vs holds/drift-r12.log)
-EXIT_CODE=0             +EXIT_CODE=1
DIFF drift-r12 (exit 1)
MATCH verify-all-A-r9 (exit 0)   … MATCH verify-claims-r2 (exit 0)
BATTERY_EXIT=1
```
Same in the real lane tree: `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` → `GATE_DRIFT: +resolvable drift`, exit 1.

Attribution — **not** the r46 landing and not my arm; the gate revision that changed the canonical capture is round 32:

```
$ for rev in 0f96bc1^ 0f96bc1 HEAD; do bash /tmp/gate-$rev.sh --drift <r12 baseline>; done
0f96bc1^   GATE_DRIFT: none
0f96bc1    GATE_DRIFT: +resolvable drift      # 2026-10-23, round 32
HEAD       GATE_DRIFT: +resolvable drift
```
The identical failure reproduces at base `6e2630a`. The r12 baseline is the only drift baseline in the tree (`corpus/evidence/gate-baseline-{r8,r12}-*.json`, last touched round 12), so after `0f96bc1` the r25 "holds" receipt cannot be re-earned. `LOG.md:916` states "all twelve explicit-root controls match their stored outputs/exits" and `SHONEN.md:8` cites that battery: both are now false; `corpus/evidence/round25-final-holds.log:2` (`MATCH drift-r12 (exit 0)`) records only the pre-`0f96bc1` state. Two r25 instruments are hit, not one — `round25-measure.sh` also ends `GATE_DRIFT: +resolvable drift` `EXIT=1` at the landing where its log records `GATE_DRIFT: none` (S3). Fix is a lane decision I do not take here: re-pin the baseline at current bytes and refresh `holds/drift-r12.log`, or retire `drift-r12` from the live battery and mark the battery frozen-at-r25 with its date.

### S2 (MEDIUM) — 3 of 6 executable-checklist items carry no command; the r46 tool is not wired in

`SKILL.md:64` heads `## Checklist (executable)`; the six items are at lines 66, 68, 69, 70, 71, 72. `Run:` lines exist only at 67 (item 66) and 73 (item 72); item 71 embeds its command inline. Items **68, 69, 70** name no command:
- `SKILL.md:69` "Observation, inference and unknown stay separate." — the exact sentence round-45 D7 / C1 was routed to make runnable. The r46 capability landed and is registered (`SKILL.md:116`), yet the checklist item that needs it is untouched. An agent reading only SKILL.md has no path from a knowledge entry to the tool's inputs: `python3 tools/inference-ground.py --help` requires `--entry --spans --counts`, and the only span producer named in SKILL is `corpus/evidence/round46/build-spans.py`, which builds the C3 evidence-pool manifest, not a per-entry spans TSV. The capability is fixture-only in practice — distinct from the semantic limit the lane records (`corpus/lessons/round-46.md` mistake 2): this is a wiring gap.
- Items 68 and 70 are enforced by gate modes (`fail-negative-without-sweep` is selftest case 11; sweeps/rejections run inside `verify-all`) but the checklist does not say so.

### S3 (MEDIUM) — Box 3's cited receipts are r25-era; one is now false

The box's command resolves: `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, exit 0 (85 s, archive copy), matching the Gates pin. Second receipt reproduces exactly: `bash corpus/evidence/round25-meta-differential.sh` → `AGREE=54/54 (fixtures=27, modes normal+strict)`, exit 0. The first does not: `corpus/evidence/round25-measure-after.log` records `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)` and `GATE_DRIFT: none`; re-running `bash corpus/evidence/round25-measure.sh <tree>` gives `METADATA_COMPLETE=25/28`, `RESEARCH_GATE: DRIFT … drift=3` (that honest-negative part still reproduces) and `GATE_DRIFT: +resolvable drift`, `EXIT=1`. The log is stale on its own face too (154 vs 275 cases; gate `63a39282` vs `2cb04bdd`): the pointer resolves but no longer shows what it is cited to show.

### S4 (LOW) — SHONEN.md has not moved since round 25

`git log -1 -- SHONEN.md` → `d8c8cff 2026-10-21 round-25: … canonical SHONEN form`. The whole 275-case gate, the 72-entry registry and the r46 tool are absent, and every pointer still carries the "lane assertion / no non-author verifier" caveat `audit-r11.md:237` requires. Consistent with `[~]`, but the evidence is old; box 3 is where the age became a false statement (S3).

### S5 (LOW) — `S093` in SKILL.md is not resolvable from the registry

12 of the 13 distinct `S###` tokens in SKILL.md resolve as `corpus/SOURCES.md` row ids (`^| \`?S###`). `S093` (`SKILL.md:106`, the quarantine-check control cell, "C2 do-nothing control (S093 flipped absent→present)") is a round-42 fixture **register** id, not a registry row; `corpus/SOURCES.md:263` mentions it only as "Rejected staged S093". Not presented as a source, so an ambiguity rather than a broken citation — but "cited sources" (box 1) cannot be verified for that token from SOURCES.md.

### S6 (INFO) — the live worktree is mid-wave and no longer equals the landing

While this audit ran, `git status --short` showed `M SKILL.md`, `M tools/inference-ground.py`, `M corpus/evidence/round46/{c1,c2,c3}-count.py`, all six `controls/*.txt`, and `M corpus/lessons/round-46.md` (17383 B vs 16274 B at HEAD, mtime 07:38). The divergence is measurable: at the landing `c2-count.py --list` prints `ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS`; in the worktree `ENTRY_POINTS=73 (… named=71) REGISTERED=73/73`. Both agree on `UNREGISTERED=0`, and the pinned landing also gives `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` and `CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`. No box verdict changes; but "repo state now" has two byte states, and any receipt taken from the worktree during wave 2 is unpinned. (`tools/__pycache__/inference-ground.cpython-314.pyc` carries mtime 07:38 — an importing run during the wave; gitignored at `.gitignore:2`, not a lane byte.)

## Box 1 and Box 4 detail

Box 1 HOLDS: `## Decision table` (9 rows, `SKILL.md:13-31`), `## Error patterns` (8 rows, 39-50), `## Boundaries` (52), `## Checklist (executable)` (64), `## Gates` (75; `GATES_ROWS=35` per the counter). All 17 distinct `corpus/knowledge/*.md` paths cited in SKILL.md exist; the r46 rows carry verdict maps and controls. `git status --short -- SKILL.md` was clean at these reads, so they are `d09fc8e7` bytes (`blob 9ecc7345`).

Box 4 HOLDS: `PROVINCE.md` sha256 `cf7826a43aaab7c00708ab54bb46577217e7a67ab44a43a33e17ee2a58c1bbec`, unchanged since `3282042` (round 1). All 61 `corpus/knowledge/*.md` titles are research-method, claim/citation, or the lane's own gate mechanics (the umbrella "this lane's own corpus and gates" covers ~12 tool-internals entries such as `dead-zone-pcre-r34.md`, `bash-local-expansion-r35.md`, `reader-allocation-r26.md`). Refused-domain vocabulary appears only as the enforcement deny lists (`corpus/knowledge/scope-refusal-r12.md:21-23`) and the gate enforces them — selftest cases 86-91, 112-119, 124 (`scope-fail-bounty`, `scope-fail-model-quality`, `scope-fail-orchestration`, `scope-fail-llm-*`, `scope-comment-shadow`) passed in the 275-case run, closing `audit-r11.md:231` O3 ("not executable enforcement") as of round 12.
Residual, note only: 43 files under `.ufo/waves/round-46/` are tracked in the lane repo, including `w1-dispatch.json` and `swarm-registry.json` — wave-harness records of fleet dispatch, i.e. orchestration material committed to lane history although PROVINCE routes that subject to kumitate. No method or knowledge file teaches it, so the box's statement holds; the artifacts sit outside the vocabulary PROVINCE uses.

## Residual risk and verification gaps

- Box 2 detail: the r9 recipe reproduces exactly — `for r in A B C; do bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/$r-r9.md --claims corpus/fixtures/claims-r9.jsonl --root ..; done` → A `RESOLVED_HOPS=6/7` / `refs=13 resolved=12 unresolved=0`, B `6/7` / `14/13/0`, C `7/8` / `15/14/0`, all `sections=5 run=5 absent=0`, `RESEARCH_GATE: CLEAN`, exit 0; record sha256s equal the README pins (`dfd2ae1a…`, `abfa5290…`, `97be0e69…`).
- Not run: the full-corpus `verify-all` sweep and the six `corpus/fixtures/archives-r9/controls/` controls. Outside a box pointer; the box-2 leg above plus the 11 matching battery cases are what I ran.
- S1's fix has two defensible shapes (re-pin vs retire) and I chose neither; whichever is taken, `LOG.md:916` and `SHONEN.md:8` need the receipt they name to match. A re-pin also needs a fresh `holds/drift-r12.log`, or the battery stays red.
- No tool installs or updates; no network.
