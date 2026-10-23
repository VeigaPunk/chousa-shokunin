# CritRoundShape — round-35 wave-shape audit

Access date: 2026-10-23. Axes: **operability, calibration**. Read-only, advisory critic review; no judging, admission, integration, dispatch, or gate scoring.

## Counterexamples and smallest safe corrections

### 1. The payload contains 65 seats, not 64

The assignment's 64-seat description is contradicted by all five population surfaces: spec items, validator tasks, standalone task payload, embedded registry, and persisted registry each contain **65**. The validator explicitly records `spawn=65`, `resume=0`, `total=65` at `.ufo/waves/round-35/w2-plan.json:16-20`. The stale 64 appears in `gen-w2-spec.py:2,192`, `w2-spec.json:89`, and `w2-taskcall.json:82` (all paths in this paragraph are beneath `.ufo/waves/round-35/` unless fully prefixed).

**Impact:** calibration: reporting 64 would misstate the denominator and role census. This is not an out-of-band wave: 65 is inside 64–128 and below 256. **Smallest correction:** report 65 and the exact mix below. Do not remove a seat, respawn, or rewrite the historical dispatch to manufacture a 64-seat wave. Correct the stale generator description prospectively, preserving the dispatched bytes as evidence.

### 2. Shared context binds all seats, but 28 individual items lack an absolute lane path

The strict per-item requirement is not satisfied: **37/65** spec prompts and **37/65** emitted task strings contain an absolute path under `/home/vgpnk/Projects/shokunin/chousa-shokunin`; **28/65** do not. A concrete counterexample is `RevGrepSites`, `w2-spec.json:14` / `w2-taskcall.json:7`: the prompt names scratch and system binaries but no absolute lane path; the emitted report trailer remains relative.

The fleet rule is explicit: “The wave `context` and every item must name absolute paths under {{LANE_CWD}}” (`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:110-117`, accessed 2026-10-23). The shared context does name the lane and explain how to resolve relative report trailers (`w2-spec.json:9`, `w2-plan.json:752`). The census therefore also records **65/65 context-plus-task bindings** and **65/65 correct lane-relative report trailers**. This mitigation must not be reported as literal per-item compliance; no misdirected write was demonstrated by this audit.

**Impact:** operability and calibration. **Smallest correction:** disclose the 28-item conformance debt now; add an absolute lane/report-base binding in the common item constructor (`gen-w2-spec.py:79-83`) before a future dispatch. Do not silently alter the current payload or spawn replacement seats.

Missing items, with source prompt / emitted task line numbers in `w2-spec.json` / `w2-taskcall.json`:

| Item | Spec | Task |
|---|---:|---:|
| RevGrepSites | 14 | 7 |
| RevGrepModesA | 19 | 12 |
| RevGrepModesB | 24 | 17 |
| RevGrepModesC | 29 | 22 |
| RevSlenSweep | 59 | 52 |
| CritRoundShape | 89 | 82 |
| MutWitnessThreshold | 134 | 127 |
| ExecPinModeVerify | 184 | 177 |
| ExecPinModeClaims | 189 | 182 |
| ExecPinModeChain | 194 | 187 |
| ExecPinModeSweeps | 199 | 192 |
| ExecPinModeIntegrity | 204 | 197 |
| ExecPinModeAll | 214 | 207 |
| ExecPinModePinDrift | 219 | 212 |
| ExecCensus | 254 | 247 |
| ScoutGrepSites | 259 | 252 |
| ScoutDebris | 264 | 257 |
| ScoutManExecvp | 269 | 262 |
| ScoutManBash | 274 | 267 |
| ScoutManGrep | 279 | 272 |
| ScoutSourcesCensus | 284 | 277 |
| ScoutSkillTally | 289 | 282 |
| ScoutFrontier | 294 | 287 |
| ConnectorOverlap | 299 | 292 |
| ScribeRunbook | 319 | 312 |
| ScribeReportFacts | 324 | 317 |
| ScribeScorecardRow | 329 | 322 |
| ScribeSourcesRows | 334 | 327 |

## Exact numbers the report should carry

| Field | Observed value |
|---|---|
| Shape | One v2 wave payload, `chousa-r35-w2`; the `w2` name is not evidence of a preceding wave |
| Seats in payload | **65** spawned entries; **0** resumes; L1 is not included |
| Role mix | executor **22**, reviewer **11**, mutation-tester **10**, scout **8**, critic **6**, scribe **6**, connector **2** |
| Attack seats, requested definition | reviewer + critic + mutation-tester = **27/65 = 41.53846153846154%** (report **41.54%**) |
| Attack floor | At least **17** seats for 25% of 65; 27 meets this arithmetic constraint |
| Band / cap | **64–128 / 256**, matching policy and validator payload |
| Emitted spawn task calls | **1** non-null `taskCall` object, containing all **65** tasks; **0** `resumeSends` |
| Planner swarm seats | **0** in spec, emitted tasks, standalone tasks, embedded registry, and persisted registry |
| Absolute lane path in individual prompt/task | **37/65**; **28** missing |
| Absolute lane binding including shared context | **65/65** |
| Registry identities recorded after spawn | **0/65**; all **65** `agentId` fields were null at this snapshot |

The spec, standalone payload, and registry have identical name-to-role maps; all 65 names, expanded prompts, and task bodies are distinct. The standalone `w2-taskcall.json` parses identically to `w2-plan.json.taskCall`, and its context equals the spec context. These are the static receipt's `identity`, `one_call`, `roles`, `attack`, and `paths` results, not assertions about successful seat completion.

Policy evidence: `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json:83-90`; the validator mirrors the matching band/cap at `w2-plan.json:4-14`. Fleet shape, attack-share and unchanged-one-call requirements are at `lane-addendum.md:50-60`.

## One-task-call and planner authority: supported facts and limits

`w2-plan.json:751-1080` contains one taskCall and `:1081` an empty resume list. The validator's source `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:1236-1238` sets `dispatch.calls` to 1 when spawns exist. Its dispatch serialization (`:1282-1316`, specifically `:1307-1309`) emits a single object and does **not** copy the literal `dispatch` field. Thus **one emitted taskCall / source-implied dispatch.calls=1** is supported. A claim that the saved JSON literally contains `dispatch.calls=1` is false. A claim that the live parent invoked `task` exactly once needs its actual tool transcript; these artifacts alone do not establish invocation count. The 65 null registry handles also do not establish completed/returned/dead-seat counts.

No additional planner seat appears in the five wave seat inventories. The authoritative mapping is **L1 holds the §3 planner seat**, not an extra L2 role (`lane-addendum.md:75-78`); bounded planning data-walk items include `ScoutFrontier`, `ConnectorOverlap`, and `ConnectorCorpus` (`gen-w2-spec.py:424-442`; corresponding `w2-spec.json:292-304`). The policy's two native-profile planner declarations (`ufo-wave-policy-v2.json:99-103,212-216`) describe frozen topology, not two dispatched planners. The validator explicitly excludes planner from swarm roles (`ufo-swarm-wave.mjs:246-259,910-915`). Item descriptions support this mapping, not proof that the L1 completed its planning work.

A recursive filename census under `.ufo/waves/round-35/` returned only `w2-spec.json`, `w2-plan.json`, `w2-taskcall.json`, and `w2/swarm-registry.json` for spec/plan/taskcall/registry JSON patterns. No second wave artifact was found; absence here is not a substitute for a complete parent dispatch transcript.

## Evidence and commands actually exercised

All shell commands below exited **0**. No counters, selftests, formatter, linter, validator process, canonical judge, other orchestration runtime, network call, install, or git/jj command was run.

1. `timeout 60s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/repairs/base-gate.sh`
   - Landed: `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`.
   - Base: `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`.
2. `timeout 60s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritRoundShape /tmp/hyaku/chousa-r35/w2/CritRoundShape`
3. From `/tmp/hyaku/chousa-r35/w2/CritRoundShape`:
   `timeout 60s env TMPDIR=/tmp/hyaku/chousa-r35/w2/CritRoundShape python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritRoundShape/audit-round-shape.py --output /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritRoundShape/shape-receipt.json`
   - Printed the JSON census reproduced above. This is a static reader/counter, not a validator or judge invocation.
4. `timeout 60s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritRoundShape/audit-round-shape.py /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritRoundShape/shape-receipt.json`
   - Audit program: `6b1feca64b20692f129d71402b13ca47c6d5f56cfb3a7a2a64fbfa568f750e5f`.
   - Receipt: `a5a15876d9486ef97b09744fd380c5d7356672d6ff524dc5ffee258075e25a70`.

The receipt also pins every input by SHA-256, including spec `6e8864554ada4967692f8bb140d6ac96bd2cca31b09765493f927642192ec00c`, payload `9f755b619cdf806ba4c4dba25be55b6eae0fbf9a07840b6758555526d628e1f2`, taskcall copy `5f082426de613cf4666a5429c1b3606c490dcec330eab84119c25a8d2ff8a3a3`, and registry `d5308b607ef047e4690002ef6820aa4ff39854ca2e16deaa0522fc0a48605e31`. All generated files are under 1 MiB and inside this seat's allowed artifact directory, except this required report.

Required background sources were opened in order: `claims.md`, `c1-count.py`, `c2-count.py`, `mechanism-witness.py`, `slen-probe.sh`. No C1/P1 or C2/P2 result is independently claimed by this scoped audit. The findings are fixable reporting/conformance defects, not a demonstrated capability tradeoff; admission and axis judgments remain exclusively with the canonical Rust judge.
