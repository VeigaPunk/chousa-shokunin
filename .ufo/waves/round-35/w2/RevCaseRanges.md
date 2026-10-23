# RevCaseRanges — round-35 w2 case-range audit (R2 + every `cases N-M` comment)

Reviewer: chousa-r35-w2-RevCaseRanges, 2026-10-23. Scope per assignment: run
`--selftest` on a clone at e87c5d7ea2dbf3730b36a3961de3f06261d015e4, map every
`ok-case` line to its comment block, verify R2's corrected ranges and EVERY
`cases N-M` comment in the gate plus the ranges quoted in SKILL.md.

## Pins (contract requirement)

- Clone: `git clone` of the lane repo, `checkout e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (HEAD verified `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`), at `/tmp/hyaku/chousa-r35/w2/RevCaseRanges/clone`.
- `sha256sum`:
  - clone `tools/research-gate.sh` = `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` — **equals the landed gate pin**, so the base revision already carries the R2 repair; selftest on the clone is a measurement of the landed gate.
  - lane working copy `tools/research-gate.sh` = `1f2fb4f5…ef617` (identical).
  - `.ufo/waves/round-35/repairs/base-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` — matches the round-34 blob pin.
- Selftest receipt: `TMPDIR=/tmp/hyaku/chousa-r35/w2/RevCaseRanges/tmp bash tools/research-gate.sh --selftest` (cwd = clone) → exit 0, `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`; log `logs/selftest.log` sha256 `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12`; 256 `ok-case` lines, 0 `FAIL` lines, numbers exactly sequential 1–256 (verified programmatically: `count 256 min 1 max 256 seq_ok True`).
- Numbering mechanics: the printed number is a run counter (`cases=$((cases + 1))` before each run, e.g. gate:4183, 4220, 4733, 5241, 5598, 5894, 6382, 6638, 6741, 7044, 7239, 7420, 7537, 7611, 7738), so log order = definition order and the log's number→name sequence is ground truth for mapping comments.

## Saturation of the comment sweep

Grepped `cases? [0-9]+` over the whole 8089-line gate in exhaustive page ranges (1–5349, 5350–5694, 5695–6392, 6394–7332, 7334–7898, 7899–8089; 6393 and 7333 covered by the whole-file scan). Result: **exactly 14 case-number comments** (gate lines 5351, 5589, 5695, 5700, 5701, 5753, 5764, 5812, 5855, 5860, 6393, 7333, 7899, 7932); regions 1–5349, 6394–7332 and 7334–7898 contain none. SKILL.md swept the same way (1–75, 76–121 read, 122–591): current-state ranges only at rows 77–84 and notes 107–117; everything else (92–94, 103–104, 180–182, 216–217, 254–255, 300–302, 345–346, 396–400) is explicitly historical narrative.

## Gate comments vs measured ok-case lines (landed gate, all 14 PASS)

| Gate line | Comment claim | Measured ok-case reality | Verdict |
|---|---|---|---|
| 5351 | integrity r7 appended "after the r6 cases so cases 1-64 keep their case numbers" | integrity-* are 65–73 | correct |
| 5589 | pin/drift r8 "so cases 1-74 keep" | pin/drift-* are 75–85 | correct |
| 5695 | r12 scope screen "(cases 86-92)" | scope-* 86–92 | correct |
| 5700–5701 | "Appended after case 85 so cases 1-85 keep their numbers" | scope block follows case 85 | correct |
| 5753 | r12 2a banner "(cases 93-94)" | 93 banner-pin, 94 drift-banner-version | correct |
| 5764 | r12 2b 8 MiB cap "(cases 95-98)" | claims/chain-cap-* 95–98 | correct |
| 5812 | r13 multi-link "(cases 99-102)" | hardlink cases 99–102 | correct |
| 5855 | r14 cross-device "(cases 103-106)" | cross-device 103–106 | correct |
| 5860 | "cases 1-102 keep their bytes" | cross-device appended after 102 | correct |
| 6393 | "`-a`: GNU grep treats a NUL as a line break in a binary file (case 135)" | 135 = json-nul-terminated-manifest | correct |
| 7333 | r31 C2 revision binding "(cases 220-228)" | claims-sha-* 220–228 | correct |
| 7899 | round-34 C1 "(cases 252-253): long spans" | 252 claims-longspan, 253 claims-longspan-line | **correct — R2 verified** |
| 7932 | round-34 attempt-2 C2 "(cases 254-256): the PCRE dead zone" | 254–256 claims-deadzone{,-line,-edge} | **correct — R2 verified** |

The round-34 blob (`repairs/base-gate.sh`) shows the pre-repair state: line 7824 `cases 252-254` (wrong — 254 is the first dead-zone case) and line 7857 `cases 255-257` (wrong — actual 254–256). The base→landed diff (`logs/base-to-landed.diff`, 94 lines) contains **only** the two comment-line fixes for R2, the R1 `slen` hunk (1632→1701-1707) and the C1 grep-pin insertions (332–400, 8036–8040): zero case definitions added, removed, reordered or renumbered — consistent with claims.md R2 "Comment-only fix; no case is renumbered."

## SKILL.md ranges vs measured log (current-state claims, all PASS)

- 7 rows quote `PASS (256 cases, 0 skipped)` — matches the measured summary exactly.
- verify-claims row: claims 21–30 & 41–42 ✓ (21–28 claims-*, 29–30 setup-claims-*, 41–42 boundary); r31 line-binding 216–219 ✓ (c1-*); revision-pin 220–228 ✓; r32 round-31-gap 235–241 ✓; r33 top-level 242–248 ✓; post-falsify 249–251 ✓; **r34 long-span 252–253 ✓ and dead-zone 254–256 (attempt 2) ✓**.
- verify-chain row: chain 31–40 & 43–44 ✓; r32 exempt-hop 229–232 ✓ (chain-exempt-*).
- verify-sweeps 45–54 ✓; verify-integrity 65–73 ✓; verify-all 55–64 & 74 ✓, `--json` delimiter 134–136 ✓, manifest lock 233–234 ✓ (c1lk-*).
- verify-metadata: 137–208 and 210–215, "209 is a claims-surface control" ✓ (209 = claims-registry-colon-deny).
- pin/drift 75–85 ✓; scope note "cases 86-92" ✓; size cap "95-98" ✓; banner "case 93 / case 94" ✓; multi-link "cases 99-102" (+case 101) ✓; cross-device "cases 103-106" (+case 106 fallback) ✓; root-slash "cases 107–111" ✓ (107–111 are exactly the five healed arms).

## Findings

1. **LOW (record gap, erratum candidate — no code defect):** claims.md R2 documents only the attempt-2 comment ("says 'cases 255-257'; actual 254–256"), but the base blob's round-34 C1 comment was *also* wrong (`cases 252-254` at base-gate.sh:7824, actual 252–253) and the landed gate fixed both comments. The claims file is frozen, so per its own rule this should be an appended erratum, not an edit. Everything else in scope is correct: **no stale `cases N-M` comment survives in the landed gate or SKILL.md**.
2. No MEETS-class finding for this item: the R2 repair is exactly as claimed and the numbering invariant ("cases N keep their numbers" across appends) holds at every one of the 7 append seams.

## Residual risk / verification gaps

- The comment→case mapping is verified against this host's measured run (number→name log) plus the base→landed diff showing no definition changes; I did not statically re-derive all 256 definition sites in the source (redundant given the run-counter mechanics and full name/exit alignment). [INFERENCE] flag applies to that redundancy argument only.
- No LSP server answers for shell scripts on this seat (checked implicitly — no shell LSP registered); all checks are text/mechanical and cite line numbers. Grep-output truncation was neutralized by exhaustive range pagination covering every gate line 1–8089 and SKILL.md 1–593.
- Historical SKILL.md tallies (40/44/54/64/74/85 cases, r2–r8) and `case 154` (r25) were not re-run against historical revisions — out of scope; each is self-labeled as history at its site.
- Selftest was run once (61 s wall); no counter/witness runs were in scope for this item. No tool installs (none needed).

## Artifacts

- `logs/selftest.log` (sha256 5311643c…75c12, 263 lines) and `logs/base-to-landed.diff` (94 lines) under `/tmp/hyaku/chousa-r35/w2/RevCaseRanges/`; clone at `/tmp/hyaku/chousa-r35/w2/RevCaseRanges/clone`.
