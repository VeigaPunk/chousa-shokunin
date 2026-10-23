# ScribeKnowC2 — round 36 wave 1

**VERDICT:** C2 knowledge-entry draft completed as an artifact. This seat did not run the C2 counter/witness, gates, or fresh-seed re-derivations and makes no independent execution finding. The opened committed `corpus/SOURCES.md` ends at S068; S069 is not present there at access time, so the draft marks that source link pending and is not ready for admission until the row is committed.

## Axes and behavior recorded

Axes: operability and calibration; this artifact advances calibration documentation only. The draft documents the intended C2 behavior: a distinct-path GNU-reporting `RESEARCH_GATE_GREP` recorder logs each invocation's NUL-delimited argv, and attribution requires each record's full span (or the first 4096 bytes for a dead-zone span) in an argv containing `-a -z -b -o -P`. It distinguishes a query from use of the query's result and includes the legacy V1–V5 scores, renamed V6 control, limits, and the frozen counting command.

## Gates and findings

No gate, counter, selftest, or fresh-seed command was executed. The following are read-only observations from committed receipts, not this seat's execution:

- `c2-after-s36001.json` and `c2-after-s36011.json` pin gate SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` and witness SHA-256 `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e`; each records `WITNESS_PER_RECORD=5/5`, `OUTPUT_EQUIV=5/5`, `LANDED_ATTRIB=pass`, `RENAMED=pass`, and `predicate_holds=true`. These are construction receipts on seeds 36001/36011, not this wave's independent fresh runs.
- `c2-before-legacy-s36001.json` pins the base gate and records `WITNESS_PER_RECORD=2/5`, `OUTPUT_EQUIV=5/5`, `LANDED_ATTRIB=absent`, `RENAMED=fail`. Its per-variant results show legacy witness passes for V2, V3, V5 and fails V1, V4, while all V1–V5 outputs are full (9/9). Its renamed arm is `unparseable`.
- The stub receipts show the documented controls: stub-pass has 0/5 separation and `predicate_holds=false`; stub-fail separates 5/5 but fails landed and renamed arms and also has `predicate_holds=false`.
- The wave brief requests fresh seeds 36301/36311/36321/36331/36341 across the broader task. No claim is made here that those seeds ran or that this seat attacked the C2 fixture.

## Surfaces and artifacts

Lane production files were read-only; no product/source registry files, judge, Git index, or jj state were changed. No tools were installed. The only artifact written under this seat's directory is:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC2/per-record-argv-attribution-r36.md` — SHA-256 `b6b6b81caccb374f2162003e3860c9a735b02b6b72abbcba9b1d7e6ede487b69` (4,586 bytes, below the 1 MiB limit).

The report is at `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC2.md`.

## Commands and outcomes

1. `mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC2` — returned successfully (exit 0); no output line. This created the permitted artifact directory.
2. `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC2/per-record-argv-attribution-r36.md` — exit 0; deciding output line: `b6b6b81caccb374f2162003e3860c9a735b02b6b72abbcba9b1d7e6ede487b69  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC2/per-record-argv-attribution-r36.md`.

No other shell commands were run. The draft's counting command (`python3 corpus/evidence/round36/c2-count.py --seed N --receipt F`) is documented for recheck only and was not executed.

## Files opened (2026-10-23)

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ScribeKnowC2.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-after-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-after-s36011.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-stubpass-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-stubfail-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/keyed-engine-output-equivalence-r35.md`
- `skill://godspeed` (`/home/vgpnk/.agents/skills/godspeed/SKILL.md`)
- `/home/vgpnk/.omp/agent/RULES.md`

The `S069` workspace search returned task/spec references but no `S069` row in the opened committed `corpus/SOURCES.md`. The GNU grep manual itself was not opened in this seat; its S069 linkage remains pending rather than independently verified.

## Out of scope

C1 execution or mutation, fresh C2 runs and fixture attacks, changing the source registry or knowledge tree, production code, judge/commit/push/publish/deploy, and any installation. The cited receipts and draft do not upgrade the construction runs into independent wave evidence.
