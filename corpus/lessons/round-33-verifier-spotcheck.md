# Round 33 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-23 UTC (host clock UTC-3). Runtime model string exposed to this closure session:
`anthropic/claude-opus-5-5`, reached through the configured `task` route; no model parameter was
passed. Round 33 ran once (L1 `ChousaR33`, attempt 1). This closure used no work of the lane's
seats as its own evidence; it read their committed bytes.

Seven read-only reviewer seats re-checked parts of the evidence: R33C1Census, R33Chrono,
R33Shortcut, R33Repairs, R33NoHarm, R33Sources, R33Conform (suffix `-2`: the first spawn of the
same batch was refused at the 100-job limit and spawned nothing; it was resent unchanged). None
died. This closure did not execute the lane's gate (`tools/research-gate.sh`), its counters
(`c1-count*.py`, `c2-count*.py`) or the fuzz harness (`fuzz_c1.py`), per PROTOCOL §Gate standard,
Closure consequence. R33Repairs ran two plain read-only scripts the lane committed as counting
commands (`corpus/evidence/round33/d2-census.py`, `no-name-signals.sh`); neither is the gate.
Driver digest, copied from `.ufo/watchdog.log` (lines 892, 904):

```
2026-10-23T05:15:09-03:00 launch chousa round=33 pgid=709425 driver=hyaku-inline attempt=1
2026-10-23T06:27:52-03:00 complete chousa round=33; hyaku-inline attempt=1
```

## Decision

- Status `ok`, admitted **false**, verdict `rejected-honest-stop`.
- C1 operability meets its frozen predicate on the landed gate: `TOPLEVEL_FIELD_MATCH` 60/156 →
  156/156 on gate `43a1af35…4346`, seeds 3701 and 3702, frozen counter `cb354dd1…a514`. No
  committed v2 receipt on any committed lane gate is below 156.
- C1 does **not** verify. A gate that masks the counter's six fixed confuser strings, regex-strips
  nested containers and counts repeated keys (`w2/L1ShortcutMask/mask-gate.sh`, sha256
  `ae7d4bfc…`) scores 156/156 on the same unamended counter (seeds 3391, 3392). It does no string
  lexing, so contract clause 3 ("string content is never structure") is not discriminated by the
  declared measure. Round prompt §6.9: a target a skip-the-work control can reach means the counter
  or target is wrong. The lane reports this itself; this closure confirms it from bytes.
- The differential fuzz is not the frozen measure. It was authored after candidate data, and the
  three receipts cited as "final gate" evidence are bound to a different gate (defect E1 below).
  It cannot rescue the claim.
- No axis is harmed. The only claim does not verify, so the round is not admitted.
- Blocker class: the same as round 32 (a frozen counter met by a post-data shortcut control; r32
  C2 no-reader metadata control, r33 C1 fixture-literal mask). Recorded for the orchestrator.

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H %cI' -- .ufo/reports/round-33/chousa.md` | `chousa-shokunin chousa@shokunin.local 6467ba90cff0… 2026-10-23T06:27:18-03:00`, 40 s after lane tip `1b6312e5` (06:26:38-03:00) |
| `SHONEN` heading | `grep -n SHONEN .ufo/reports/round-33/chousa.md` | `114:## SHONEN`, four `[~]` lines matching the `SHONEN.md` boxes verbatim; pointers resolve at `1b6312e5` (SKILL.md 77–88, LOG.md:1253 `## Round 33`, `measure/final/battery.out`; PROVINCE.md 0 commits in range) |
| Cited lane commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` | 11/11 commit tokens rc=0 (2b9cc73a 3b528b9a e3e24ec8 96be7925 eb179ec3 7f6aeb70 0fb300b5 4c076a0f 0cad05eb 1b6312e5 + full tip). Six non-commit tokens are gate SHA-256 prefixes: f4731885, 52f07c74, 94a7be5a, 165acd5f, 43a1af35 equal `git show <rev>:tools/research-gate.sh \| sha256sum` at base, eb179ec, 0fb300b, 0cad05e, 1b6312e; b808e9b5 is the disclosed uncommitted edit state |
| Round commits authored by lane | `git log --format='%h %an <%ae> %cI' 2b9cc73a..1b6312e5` | 9/9 `chousa-shokunin <chousa@shokunin.local>` |
| Pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain --ignored` | `branch=master local=remote=1b6312e5… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; ignored only `.jj/`, `.ufo/interactive-sessions/` |
| Prompt carries template contract | `render_prompt` (`shokunin-watchdog.sh:172-185`) + addendum `subst` (`inline.sh:43-59`) re-rendered to /tmp and diffed (R33Conform) | Empty diff; §1–5 identical to `templates/round-prompt.md` (fleet copy = canonical, sha256 `b48b57ca…` both); §6 is the hyaku addendum and only adds; no L2 route table quoted (defers to host table, as `MISSION.md:63-65`). Prompt commit `480c98bb` 05:15:08-03:00, 1 s before the launch line |
| Misroot (SentinelParser33) | `ls /home/vgpnk/Projects/shokunin/.ufo/waves/round-33/`; `git -C /home/vgpnk/Projects/shokunin log --all -- '.ufo/waves/round-33/*'`; fleet `status --porcelain` | No fleet-root copy remains, none was ever committed to the fleet repo, fleet porcelain has no round-33 path. Lane copy committed in `1b6312e5`. Byte identity cannot be re-proven now: the only other copy was deleted as the prompt requires, and the lane's `cmp` result has no committed output (E5) |

Conformance defects (status-neutral): none in step 1.

## Claim — re-check against `1b6312e5`

C1 rests on a lane-owned counter that drives the lane gate. It is **evidence-verified** from
committed receipts, not re-executed. This closure and its seats re-measured counter, gate and
receipt bytes.

| Measurement | Command (lane root) | Observed |
|---|---|---|
| Counter frozen | `git log -- corpus/evidence/round33/c1-count-v2.py`; `git show {e3e24ec,1b6312e}:… \| sha256sum` | One commit, `e3e24ec` (05:35:29-03:00, design v2). `cb354dd1b5bd…a514` at both revisions |
| P1 v2 text frozen | `git diff e3e24ec 1b6312e -- corpus/evidence/round33/claims.md` | Empty: the contract file is byte-identical since design v2 |
| Gate chain | `git show <rev>:tools/research-gate.sh \| sha256sum` for all 10 revisions | base→e3e24ec/96be792 `f4731885`; eb179ec, 7f6aeb7 `52f07c74`; 0fb300b, 4c076a0 `94a7be5a`; 0cad05e `165acd5f`; 1b6312e `43a1af35` |
| Before | `jq … controls/L1-design-v2/c1v2-base-s3311.json` | `60/156`, `predicate_holds=false`, gate `f4731885`, counter `cb354dd1` |
| After | `jq … measure/final/c1v2-s370{1,2}.json` | `TOPLEVEL_FIELD_MATCH=156/156`, `predicate_holds=true`, gate `43a1af35`, counter `cb354dd1`, utc 09:24:27Z / 09:24:31Z |
| Kill rule census | every committed JSON under `.ufo/waves/round-33/` with `counter_sha256=cb354dd1…`, grouped by `gate_sha256` (closure python + R33C1Census `jq '..\|objects'`) | Committed lane gates: `f4731885` ×13 (all 60), `52f07c74` ×2, `94a7be5a` ×87–88, `165acd5f` ×3, `43a1af35` ×2 — all 156, none lower. Every other gate maps to a committed control/mutant `.sh` except three never-committed worktree states: `45d76b4f` ×3 (156), `fc08410e` ×1 (156), `b808e9b5` ×1 (0). None of those five receipts is cited as P1 evidence in the report, SCORECARD hunk or lesson; `b808e9b5` is named only as a non-revision |
| Chronology | commit times; receipt `utc` (R33Chrono) | Design v2 08:35:29Z < first candidate receipt 08:41:21Z (`measure/candidate/c1v2-s3351.json`). 71/73 v2 control receipts precede it; the two later ones (`controls/L1-mistake/v2-s338{1,2}`, 08:51–08:52Z, 144/156, committed in `4c076a0`) score the v1-mistake gate as lesson evidence, not as a freezing control. `w2/Chronology33.md`'s "every committed control receipt has utc < 08:41:21Z" is stale at tip for that reason |
| Shortcut counterexample | `jq … w2/L1ShortcutMask/mask-s339{1,2}.json`; `mk-mask-gate.py:13-43`; `c1-count-v2.py:73-80` | 156/156, `predicate_holds=true`, gate `ae7d4bfc`, counter `cb354dd1`, utc 09:07:28Z / 09:08:03Z (post-data), first committed `4c076a0`. The six masked literals equal the counter's six module-constant confusers; no confuser content varies by seed. Counter unchanged after it |
| Pre-data control for that shape | `w1-spec.json:56-61`, `w1/swarm-registry.json:98`, `controls/L1-v2-rescore/summary.txt` | CtlC1Shortcut was registered with `agentId=null` and left no artefact (the disclosed `cyber_policy` hold). No other pre-data control masks the confusers; best non-oracle v2 control 142/156 |
| Fuzz receipts cited as final-gate evidence | `jq .gate_sha256 measure/final/fz-9021{2,3,4}.json`; sha256 of every `tools/research-gate.sh` revision in `git rev-list --all`; `ls -la --time-style=full-iso /fast/scratch/hyaku/chousa-r33/L1/perf/` | All three bind `b2c07eda…9b4b`, which matches no committed blob. The L1's scratch gate `L1/perf/tools/research-gate.sh` now hashes `43a1af35` with mtime 06:23:31-03:00, after the three fuzz runs (06:22:47, 06:23:00, 06:23:14), and `selftest4.log` (251 cases) is 06:24:27. The 650+650+650 agreement was measured on an earlier scratch state, not on the landed gate (E1) |
| Other committed fuzz receipts | `w2/FuzzDiff33/*.json` (R33Shortcut) | `94a7be5a` (650/650, 750/750, 100/100), `165acd5f` (750/750), `45d76b4f` (750/750, uncommitted worktree), base `f4731885` 313/750. None binds `43a1af35`. No fuzz receipt exists for the mask gate; from its bytes, two fuzz confusers (`fuzz_c1.py:41,44`) carry a `}` inside a string the mask does not cover, so the fuzz would likely reject it [INFERENCE, not executed] |
| No harm | `measure/final/battery.out` vs `w1/ExecNoHarmBase33/battery-base.out` (R33NoHarm) | Header `gate_sha256=43a1af35`, `lane_revision=0cad05eb` (tip at run time; gate committed in `1b6312e`). Selftest PASS 251 (base 241); first 241 `ok-case` lines identical (sha256 `7ee6b24c…` both). claims-r2 17/17 CLEAN, chain-r3 17/22, broken 1/2 DRIFT, observable 3/3, r31 v3 132/132 ×2, r32 C2 v2 132/132 ×2 — every row equal to base. Cases 242–251 present at `research-gate.sh:7628-7738` |
| SCORECARD | `git diff 2b9cc73a 1b6312e5 -- SCORECARD.md` | +53/−0, append-only. Operability 3 → 3. Records "P1 v2 met; not verified by its counter for clause 3". Its capability row says "clause 3 rests on the fuzz evidence" (E1) |
| Registry home | `git diff 2b9cc73a 1b6312e5 -- SKILL.md` | +18/−12: selftest tally 241 → 251, new round-33 counters row. `SKILL.md:83` still says metadata cases 137–154 (CalibrationSkill33; the report says not fixed) |

### Weighing the fuzz (orchestrator asked)

The fuzz is real non-counter evidence of better behaviour. Its Python reference parses records
with `json` and judges claims independently of the gate; base agrees on 313/750 and committed
intermediate gates agree on every record. But it is post-data (harness first committed in
`0cad05e`, after the candidate receipts), it was never run against the shortcut, and no committed
fuzz receipt binds the landed bytes. It supports `unprovable-but-better`; it is not a verification.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| operability | unprovable-but-better | Non-author ruling, not admission. The declared counter is met by a fixture-literal shortcut, so it cannot show clause 3. Clauses 1–2 (nested members ignored, repeated read fields invalid) are discriminated by the counter's nested and duplicate classes (controls ≤142/156). Selftest cases 242–251 assert exit codes and finding ids for nested, duplicate and confuser records. The fuzz agrees 100% on committed intermediate gates (`94a7be5a`, `165acd5f`) versus 313/750 at base. The battery is unchanged. Better behaviour, not proven by the declared measure |
| coverage | unchanged | No coverage claim; D1 is quality work on a held rule |
| depth | unchanged | No depth claim; QUALITY 36–41 appended (+48/−0) |
| freshness | unchanged | S001–S061 untouched (`corpus/SOURCES.md` +2/−0) |
| calibration | unchanged | No calibration claim; the stale `SKILL.md:83` range was not introduced by this round's claim and is routed (E3) |
| adjacency | unchanged | `git diff 2b9cc73a 1b6312e5 -- PROVINCE.md` empty |

## Discernment spot-check (`corpus/lessons/round-33.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S062 RFC 8259 | admit, tier A, mined | `curl https://www.rfc-editor.org/rfc/rfc8259.txt` → 200, sha256 `61a5378f…cd2d7` (matches the lesson) | agree | "The names within an object SHOULD be unique." found at line 322; "Many implementations report the last name/value pair" at line 333, both in §4 Objects (line 316). The corrected anchor 316–335 (+343–344) covers both full sentences |
| S063 Python `json` docs | admit, tier A, mined | `curl https://docs.python.org/3/library/json.html` → 200, sha256 `5ceeeaf6…5608b` (matches; footer 07:34 UTC unchanged) | agree | After tag strip and whitespace squeeze, "By default, this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name:" occurs once, under "Repeated Names Within an Object" |
| ECMA-404 | reject (not opened) | `rfc8259.txt` lines 198–214; host registry grep (no `ecma-international` host in the lane) | agree | RFC 8259 cites ECMA-404 normatively and says the grammar is intended to be the same. The host is not registered. A tier-A source already covers the point |
| Design v1 counter `c1-count.py` | reject as P1 counter (pre-data) | `jq … controls/L1-mistake/v1-s338{1,2}.json`, `v2-s338{1,2}.json` | agree | The three-key duplicate gate (`86bc8b96`) scores 144/144 under v1 (`ab6b2ae2…`) and 144/156 under v2 (`cb354dd1…`). v1 accepted a wrong gate |
| Counter v2 as verification of clause 3 | reject (post-data) | `w2/L1ShortcutMask/` receipts and builder | agree | See the claim table: 156/156 with no string lexer |

Newly written rows re-opened: S062 (`corpus/SOURCES.md:72`) and S063 (`:73`). Located quotes are
8, 7, 6 and 22 words (`wc -w`), all ≤25. The `teaches` cells are paraphrases.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` printed
`W04 S051 …`, `W04 S053 …` (pre-existing duplicate-URL warnings) and `chousa ok …`; exit 0. Rows
61 → 63 (`grep -c '^| S0' corpus/SOURCES.md` at `2b9cc73a` and at `1b6312e5`).

## Repairs D1–D5 and QUALITY 36–41

| Item | Evidence | Observed |
|---|---|---|
| D1 | `c2-count-v3.py` (added `7f6aeb7`, sha256 `6f362ece…`, unchanged since): `:283` shuffles write order, `:291-295` draws mtime/atime independent of class | The round-32 metadata control: 132/132 under v2 (re-run), 87–98/132 under v3 (`w1/ExecD1CounterV3`, `w2/RerunD1v3`, `w2/MutD1Counter`). Control receipts 08:30–08:31Z precede the first landed-gate v3 receipt 08:41:46Z. Landed gates 132/132 incl. `measure/final/c2v3-s370{3,4}` on `43a1af35` |
| D2 | `python3 corpus/evidence/round33/d2-census.py --gate 10f2fe12` | `C1 receipts on gate 10f2fe12: 21`; SCORECARD correction appended, naming the three extra RerunC1b receipts |
| D3 | `measure/final/battery.out` header | `lane_revision`, `gate_sha256`, battery script sha present; the QUALITY 38 check prints `HEADER_MISSING` on the r32 battery and `HEADER_OK` on r33 |
| D4 | C1 | Clauses 1–2 fixed and counter-discriminated; clause 3 not counter-verified (above) |
| D5 | `bash corpus/evidence/round33/no-name-signals.sh .ufo/waves/round-32` | Exit 1, `HIT w2/RerunC1b.md:31`. On round 33 it exits 1 on 64 prose/fixture/self hits; no executed seat code signals by name |
| QUALITY 36–41 | `git diff 2b9cc73a 1b6312e5 -- corpus/QUALITY.md` | +48/−0. Each row's able-to-fail pointer resolves to committed failing bytes (36 r32 metadata control 132/132; 37 census 21; 38 header check; 39 RerunC1b hit; 40 mask 156/156; 41 `b808e9b5` 0/156). QUALITY 40's remedy (per-seed confusers, mask scored before freezing) is not yet built |

## Trend verdicts

- **expansion: improved.** New knowledge entry `corpus/knowledge/claim-record-fields-r33.md`
  (+82/−0; sources S062, S063, both `mined`, both re-opened above with their quotes found). It is
  on ground the coverage map did not hold (top-level claim-field reading). Caveat: its fuzz
  sentence (lines 65–66) mis-binds the gate (E1).
- **quality: unprovable-but-better.** D1–D5 are repaired and verified, and QUALITY 36–41 each have
  a committed failing case. But a newly admitted entry and the SCORECARD capability row say 1950/1950
  fuzz agreement "on the final gate", and those receipts are bound to `b2c07eda`, not `43a1af35`. So
  not every admitted entry passes its re-check.
- **discernment: improved.** The spot-check agrees with the gate on two admits and three rejects. The
  lane caught its own v1 counter before data, built and reported the post-data shortcut instead of
  inferring it, corrected the S062 anchor in-round, and turned the gate-edit and fixture-literal
  mistakes into QUALITY 40–41 with failing cases. Limit: the fuzz mis-binding (E1) is the QUALITY 41
  hazard repeated in the scratch copy, and the lane did not catch it.

## Disclosed round incidents (status-neutral)

- The L1 edited `tools/research-gate.sh` in place while wave-2 seats scored it. Five receipts on
  never-committed states (`45d76b4f` ×3, `fc08410e` ×1, `b808e9b5` ×1) belong to no committed
  revision. None is counted as P1 evidence. Mutant and probe receipts on other uncommitted bytes
  are attack evidence only.
- Two `cyber_policy` holds were not retried: CtlC1Shortcut and MutC1Counter. CtlC1Shortcut was the
  pre-data control for the shape that later met the counter.
- Out-of-domain mutants survived both detectors on `94a7be5a` (MutC1GateString b/d: escaped member
  names; MutC1GateDepth b/e: mismatched closers, trailing bytes). The post-falsify repairs declare
  unbalanced brackets and trailing bytes fail-closed. Escaped member names stay unclaimed.

## Routed defects (lane fixes next round)

- **E1 (fuzz binding).** `measure/final/fz-9021{2,3,4}.json` bind gate `b2c07eda…`, a scratch state
  overwritten at 06:23:31-03:00 by the bytes that became `43a1af35`. The report (§Before → after),
  `SCORECARD.md` capability row ("clause 3 rests on the fuzz evidence") and
  `corpus/knowledge/claim-record-fields-r33.md:65-66` say "on the final gate". Append a named
  correction to each. Then either run the fuzz on `43a1af35` with committed receipts, or state that
  no fuzz receipt binds the landed gate.
- **E2 (C1 counter, QUALITY 40).** Generate confuser content per seed, including structural
  characters and escapes inside strings. Score the exact `w2/L1ShortcutMask/mask-gate.sh` against
  the new counter, and commit that receipt, before any candidate. Until then clause 3 has no counter
  verification.
- **E3 (calibration).** `SKILL.md:83` "metadata cases 137–154" is stale (CalibrationSkill33).
- **E4 (measurement binding).** Extend QUALITY 41 to measurements: never cite a receipt whose
  `gate_sha256` is not a committed blob, and re-run any measurement after a scratch edit. Five
  wave-2 receipts are labelled `c1-landed` on uncommitted states (`NoHarmCorpus33`, `ProbeTypes33`,
  `ProbeLongLines33`). Rename them or annotate them as non-revision.
- **E5 (misroot proof).** Record `sha256sum` of both copies in a committed file before deleting a
  misrooted fleet copy. The lane's `cmp` statement for SentinelParser33 has no committed output.

## Operator note (SHONEN)

No box is fully checkable by a non-author as filed. Box 3 (`--selftest` → PASS 251) can be re-run
by a non-author but was not re-run here; its committed log shows PASS 251. Box 4's "`PROVINCE.md`
unchanged" is mechanically true. Box 1 carries a known stale range (E3). Promotion is
operator-owned.
