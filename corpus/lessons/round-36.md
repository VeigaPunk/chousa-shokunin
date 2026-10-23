# Round 36 — the engine-swap canary and per-record attribution

Dates are UTC. Attempt 2; attempt 1 froze the claim design and landed the gate fixes at
`700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (`.ufo/watchdog.log` line 980:
`lane-dead-no-report chousa round=36`, orchestrator OOM). Base for the round's before-state is the
round-35 final gate `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`, committed
byte-exact as `.ufo/waves/round-36/controls/base-gate-r36.sh`.

- **C1 operability** (lowest scored axis, 3/10; surface: the gate's matcher provenance and the tools
  its receipt names as identity) — the gate and its counter separate an output-equivalent engine
  swap in fourteen scenarios; before 10/14, after 14/14 on seeds 36001/36011 (construction) and
  36301/36311/36361 (wave + L1 re-derivation).
- **C2 calibration** (surface: the lane's measurement method) — the witness attributes the matcher
  PER RECORD through the pinned engine's argv channel; before 2/5, after 5/5 on seeds
  36001/36011/36301/36311/36371, with the renamed matcher passing.

Two claims, distinct axes. The round-35 routed defects 3, 4, 7 and erratum 15 are repairs R1-R5,
not claims.

## What happened

- Attempt 1 (inherited): froze `corpus/evidence/round36/claims.md` (P1/P2, kill rules, limits,
  R1-R6) and landed the gate edits — `sha256_hex_file` for the manifest/`--pin` hashes (S11),
  `json_unescape` in a `LC_ALL=C` scope with hand-rolled two/three-byte UTF-8 (S12), the
  `CHOUSA_GREP_PIN_ECHO` scrub in the `--pin` capture environment (S13), the `GATE_GREP:*` drift
  token (S14), and selftest cases 257-261 (256 → 261). Named as inherited in the report; the wave
  re-verified the tracked bytes are `CMP_IDENTICAL` to the freeze commit (ScoutInherited).
- Attempt 2 landed the measurement and the corpus: wave 1 (36 seats) re-derived both claims on
  fresh seeds, attacked the fixtures and drafted the frontier artifacts; the L1 re-derived C1
  14/14 on seed 36361 and C2 5/5 on seed 36371; the no-harm battery held
  (`SentNoHarm.md`: claims 17/17, chain 17/22, broken control 1/2, archives 3/3); the selftest
  passed 261 cases under default, `LC_ALL=C` and a scratch `TMPDIR` (`ExecSelftest.md`).
- Three C1 scenarios assert less than their names claim (S7 `len(rec_matches) >= 1` accepts one
  argv; S8 compares the echo to a live `--version` and reads no matcher argv; S9 truncates and
  never reads the recorder log). S10's per-record attribution is what keeps a no-call gate from
  scoring 14/14. Recorded as the claim's narrowed reading and as QUALITY 52; not a kill — the
  claim's text is met and the limit was not previously stated.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| number-drift (a tool's own stated count contradicts its committed receipt) | `corpus/evidence/round36/c2-count.py` docstring says the round-35 battery "separates only 3/5 (V3 and V5 pass it)"; `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json` reports `matched: 2` with V2, V3 and V5 `witness: pass` (re-derived on fresh seed 36321, `w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json`) | **none in-round** — the counter's printed label excludes the before-count, so no run could move the sentence; QUALITY 50 added | docstring corrected in round 36 (repair R7); QUALITY 50 requires every number in a tool's prose to name the receipt field that yields it |
| landing (crash debris left in an evidence directory) | at attempt-2 start `git -C chousa-shokunin status --porcelain` showed `?? corpus/evidence/round36/__pycache__/` (one CPython 3.14 pyc of `c2-count.py`, 20,219 B, mtime 18:00:17 -0300); it predates the freeze commit `18:03:56 -0300` | **none** — no rule covered build residue in `corpus/evidence/`; QUALITY 43 covers misrooted copies only | pyc removed, `corpus/**/__pycache__/` added to `.gitignore`; named in the report (the ScribeLesson seat looked after the removal and could not see it — its "unverified" verdict is the honest record) |
| number-drift (in this round's own dispatch text) | the wave-1 brief said the measure directory holds 11 committed receipts; `w1/ScoutReceipts.md` counts 8 (`ls .ufo/waves/round-36/measure/*.json \| wc -l`) | the wave's own ScoutReceipts seat, before the count was cited in the report | report and knowledge entries cite 8; no dispatch text is rewritten |
| survivor (a scenario passes without the behaviour its name claims) | `w1/ScoutC1Counter.md` §Vacuity candidates 1-3: S9's recorder log is truncated at line 534 and never read after S7; S8 reads no matcher argv; S7 accepts one argv | the wave's own scout seat; the claim's §Limits named only S6's arm | claim reading narrowed in SCORECARD/report; QUALITY 52 makes an assertion/name mismatch a defect |
| scope (a repair scrubbed the variable but not the mechanism that can re-introduce it) | R1 added `-u CHOUSA_GREP_PIN_ECHO` to the `--pin` capture environment, but the inner bash still sources `BASH_ENV`: a one-line `export CHOUSA_GREP_PIN_ECHO=1` there embeds `GATE_GREP:` in the baseline and the unchanged gate then reports false drift (`w1/RevPinContract.md` F1, reproduced with the exact commands) | **none** — no counter arm sets a `BASH_ENV` exporter, so the wave's reviewer found it and no receipt could have; QUALITY 46 covers resolution, not capture-environment inheritance | reported in claims §Erratum 7 and SCORECARD planned-r37 (`-u BASH_ENV` at `research-gate.sh:3921`), **not** applied post-data: a gate edit after measurement would void every `gate_sha256` receipt |

## Gate

Rows added this round: **S069**, **S070** (68 → 70 rows; census `validate` exit 0 with the two
standing W04 warnings for S051/S053). Both opened locally on 2026-10-23; no network.

- **S069** GNU `grep(1)` manual, `-b`/`--byte-offset` under `-o` —
  `/usr/share/man/man1/grep.1.gz`, decompressed lines 382–391, quote at 387–391; GNU grep
  3.12-modified (2025-03-21), installed `grep 3.12-2`; file SHA-256 `9b027d02…85ba`. Located
  quote (13 words by `printf '%s\n' '<quote>' | wc -w`): "If -o (--only-matching) is specified, print the offset of the matching part
  itself." The page states the offset semantics; it says nothing about attributing records to argv,
  which is the lane's method [INFERENCE].
- **S070** GNU coreutils `sha256sum(1)` — `/usr/share/man/man1/sha256sum.1.gz`, decompressed lines
  4–11, 19–20, 54–56, quote at line 11; coreutils 9.12-2; file SHA-256 `93c17dff…403f`. Located
  quote (6 words): "Print or check SHA256 (256-bit) checksums." The page does not define a
  validation policy; the gate's 64-lowercase-hex rule is the lane's choice (256 bits = 64 hex
  digits) [INFERENCE].
- **Rejected candidates** (kept as reasoning, no row written): (a) man7.org's `grep(1)` HTML page —
  not opened this round, and the installed page was opened instead; a URL row claiming the
  installed page's bytes would be a reference-drift. (b) POSIX `grep` specification — an external
  fetch with no operator approval this round; deferred, not rejected on merit. (c) `locale(7)` for
  the C-locale decode — the arm's evidence is the installed binary's measured behaviour plus the
  selftest case, not a documented norm; a row would overclaim.
- **Status / recheck / used-by changes:** none in place. S069/S070 enter `mined` with their
  `used-by` set at creation (no old→new transition).
- **Census receipt (this round):** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
  → exit 0, `rows 70` (A 64 / B 1 / C 5; mined 47 / queued 19 / rejected 4), warnings W04 ×2
  (S051, S053); `census` → `chousa rows 70`. Before: exit 0, `rows 68` (A 62 / B 1 / C 5; mined 45 /
  queued 19 / rejected 4).
- **Knowledge admission candidates:** `engine-swap-canary-r36.md` and
  `per-record-argv-attribution-r36.md` were drafted by wave scribes, then admitted by the L1 after
  the wave's audits (`w1/CritLessonGate.md`, `w1/ScoutC1Counter.md`, `w1/ScoutC2Counter.md`) and the
  corrections it demanded (heading overclaim, V1/V4 admission wording, S070 policy labelling, S11
  refusal observation) landed before the commit.
- **Spot-check pointer (pending, not satisfied):** the non-author round-36 spot-check is the hyaku
  closure's; its verdict is not this lesson's to write. Marked **pending**, not satisfied. Wave
  cross-checks — `w1/ScribeSrcGrep.md` and
  `w1/ScribeSrcSha.md` (row drafts), `w1/ExecC2LegacyCtl.md` (before-state re-derivation),
  `w1/ScoutC2Counter.md` (channel and patch audit). The non-author round-36 spot-check is the
  hyaku closure's; its verdict is not this lesson's to write.

Sourced claim: C2 rests on S069 (opened this round); C1's S11 arm rests on S070 (opened this
round).

## Spot-check intake

One row per routed defect in `corpus/lessons/round-35-verifier-spotcheck.md` §Routed defects 1-9:

| # | Debt / disagreement | Disposition |
|---|---|---|
| 1 | Lesson `## Gate` incomplete (no rejects, no spot-check) | **fixed** — this lesson's `## Gate` carries the three rejected source candidates and marks the spot-check duty pending |
| 2 | r35 report's wave-return figure stale (60/65 vs 62) | **carried** — the filed r35 report is never rewritten; this report states its own counts (34 of 36) with the counting command |
| 3 | `CHOUSA_GREP_PIN_ECHO` inherited by the `--pin` capture | **fixed** R1 (`-u CHOUSA_GREP_PIN_ECHO`); residual `BASH_ENV` re-export hole named in `claims.md` §Erratum 7 and planned-r37 |
| 4 | `verify-all --json` hashes via PATH `sha256sum \| cut`, non-empty only | **fixed** R3 (`sha256_hex_file`, 64-lowercase-hex, exit 2); the claim-body hash at `:2002` remains open (planned r37) |
| 5 | C1 cannot see per-call engine identity; receipts lack `counter_sha256` | **partly fixed** — S10's per-record canary + S7/S10 receipts; `counter_sha256` still absent (carried, planned r37) |
| 6 | C2 witness limits (global threshold, forgeable PS4, body-replaced, one-call) | **fixed** — new argv witness separates all five (V2/V3/V5 were admitted); prefix-64 bypass found and recorded (§Erratum 8) |
| 7 | Locale seam at `json_unescape` | **fixed** R4 (hand-built UTF-8 in `LC_ALL=C`, cases 257-258); a different seam at `:1015` found and carried (§Erratum 13) |
| 8 | S068 quote anchor 391-395 vs 390-396 | **refused** — no teaching is wrong and SOURCES rows are append-only; a correction would need a supersede row, not an edit (r37 candidate) |
| 9 | r35 "lane tip at landing" staleness | **carried** — filed bytes not rewritten; this report cites one lane hash per claim |

**Row errata (non-author re-open, `w1/RevSourcesNew.md`):** S069 and S070 both re-opened
**VERBATIM** (compressed file SHA-256s match, every quoted word and line exact, `teaches` supported,
`used-by` resolves). One cosmetic defect recorded, not edited in place (append-only): S070's anchor
cell labels decompressed lines 19-20 as "SYNOPSIS" while the `-c, --check` text sits under
DESCRIPTION (SYNOPSIS is lines 5-7). A supersede row is a round-37 candidate; the row's `teaches`
and scope are unaffected.
