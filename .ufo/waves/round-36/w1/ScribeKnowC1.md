# ScribeKnowC1 — C1 knowledge-entry report

**VERDICT:** The C1 knowledge-entry draft is complete in the assigned wave directory. Its measured counts come only from the committed construction receipts on seeds 36001 and 36011 and the committed base-control receipt on seed 36001. This seat did not independently re-derive C1 on fresh seeds or run a gate.

## Behavior and touched surfaces

Created `engine-swap-canary-r36.md`, a draft for `corpus/knowledge/engine-swap-canary-r36.md`, under the permitted private wave directory. It starts with the requested `source` / `verified-at` / `recheck` provenance trio, names the 14 receipt scenarios and fields, records landed and before-state counts with counter command forms, gives the base-gate do-nothing reading, quotes the relevant frozen limits, and closes with what the entry does not claim. The draft explicitly says the command forms were not run by its author and that its receipt evidence is not a fresh-seed remeasurement.

No lane production files, counters, witnesses, receipts, gate, Git index, or jj state were modified. No report or artifact was written outside the assigned `w1/ScribeKnowC1/` directory except this required report.

## Evidence and gates

- `.ufo/waves/round-36/measure/c1-after-s36001.json` records `gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`, `ENGINE_SWAP_CANARY=14/14`, and `predicate_holds=true` (fields `gate_sha256`, `label`, `predicate_holds`; read 2026-10-23).
- `.ufo/waves/round-36/measure/c1-after-s36011.json` records the same gate SHA, `14/14`, and `predicate_holds=true` (same fields; read 2026-10-23).
- `.ufo/waves/round-36/measure/c1-before-s36001.json` records base-control SHA `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`, `ENGINE_SWAP_CANARY=10/14`, and `predicate_holds=false` (same fields; read 2026-10-23).
- The frozen claims at `corpus/evidence/round36/claims.md` lines 35–58 and 60–64 state the P1, the four S11–S14 misses, and the base-gate do-nothing control. Lines 121–135 hold the listed limits. The counter CLI at `c1-count.py` lines 381–385 confirms the default gate and `--seed` / `--receipt` options. The knowledge draft lists command forms as frozen-predicate/recheck forms, not as commands executed by this seat.
- Gate SHA values above are observed receipt fields; this seat did not independently hash either gate. No fresh-seed count was performed, so the receipts do not constitute this seat's independent re-derivation.

## Commands executed

1. `timeout 30s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC1` — exit 0; no output. This created the permitted artifact directory.
2. `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC1/engine-swap-canary-r36.md` — exit 0. Decisive output: `6d3f2c2ebd68fb37652669359d0cc2ca5599e76b642d0667c2d03f0734daa0f2  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC1/engine-swap-canary-r36.md`.

No counter, selftest, gate, build, test, git, or jj command was run. Read/glob/grep operations were file-access tools rather than shell commands and have no process exit codes; their decisive results are summarized above and below.

## Files opened or searched (all access date 2026-10-23)

- Validated brief: `.ufo/waves/round-36/w1-briefs/ScribeKnowC1.md`.
- Skill instructions: `/home/vgpnk/.agents/skills/godspeed/SKILL.md`.
- Frozen design: `corpus/evidence/round36/claims.md`.
- Counters/witnesses required by the lane context: `corpus/evidence/round36/c1-count.py`, `corpus/evidence/round36/c2-count.py`, `tools/argv-witness.py`, and `tools/mechanism-witness.py`.
- Receipts: `.ufo/waves/round-36/measure/c1-after-s36001.json` (including its `scenarios` query), `.ufo/waves/round-36/measure/c1-after-s36011.json`, and `.ufo/waves/round-36/measure/c1-before-s36001.json`.
- Existing knowledge style references: `corpus/knowledge/grep-pin-r35.md`, `corpus/knowledge/keyed-engine-output-equivalence-r35.md`, and `corpus/knowledge/long-span-argv-r34.md`.
- The local source page path `/usr/share/man/man1/sha256sum.1.gz` was opened via the file reader, which returned only `sha256sum.1 (3.6KB)`, not readable page text.
- Directory listings inspected: `.ufo/waves/round-36/measure/` and `corpus/knowledge/`.
- Text searches for `S070` in `corpus/` and the lane found no source-row text; lane search hits were wave dispatch/spec/brief material. **[INFERENCE]** The companion S070 source row was not yet integrated when this draft was prepared. The draft cites S070 as routed, but this seat did not verify the man-page text or S070 row. This is the remaining source-provenance limit, not C1 execution evidence.

## Findings and known limits

The committed records support the stated aggregate results on their recorded construction seeds; they do not support claiming that this seat ran the required fresh seeds 36301, 36311, 36321, 36331, or 36341. The entry preserves the frozen design's limits: a semantic query is not proof its answer was used; an output-equivalent call-for-show survives; a gate that reads the recorder may forge records; and the C2 witness shares the call-for-show limit. It does not claim “the engine is genuine.”

Out of scope for this scribe assignment: fresh C1 experiments, fixture attacks, C2 execution, source-row authorship, and product-code edits. No installation or update was made.

## Artifacts

- Draft: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC1/engine-swap-canary-r36.md` — SHA-256 `6d3f2c2ebd68fb37652669359d0cc2ca5599e76b642d0667c2d03f0734daa0f2`.
- Report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeKnowC1.md`.