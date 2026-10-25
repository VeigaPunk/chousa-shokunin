# R51 Cross-Claim and Cross-Fleet Pattern Analysis (C1, C2, C3)

Seat: R51ConnCrossClaim (leaf connector) · Date: 2026-10-25 · Lane: chousa-shokunin (claims frozen @d603f6f)
Tooling: no installs (RULES.md read, pacman paused); scratch `/dev/shm/chousa-r51-R51ConnCrossClaim/` unused/clean.

## 1. Cross-Claim Pattern in Round 51
- **C1 (operability)**: `tools/assimilate-rows.py` (candidate `2a3389d`) introduces dynamic input generation from fresh random nonces at counting time (`c1-count.py:101-118`), closing the cheat vector exposed in round 50 (CritForgeC1 42-line forge).
- **C2 (depth, sourced)**: Three systematic-review search-record entries adopted by document, resting on seven on-disk captures.
- **C3 (calibration)**: Pointers in SCORECARD.md capabilities rows and SHONEN.md evidence lines resolve at tip (`c3-count.py`).

## 2. Evidence: Sibling-Lane 'Pointer Resolves' & 'Self-Assessment vs Tree' Counters
Command: `grep -rln -e 'dangling' -e 'pointer' /home/vgpnk/Projects/shokunin/*/tools /home/vgpnk/Projects/shokunin/*/corpus/evidence 2>/dev/null`
Read two sibling-lane instruments:
1. **tsukuroi-shokunin** `tools/check-self-assessment.py` (Round 26 C2 calibration, checks K01–K27):
   - Capabilities rows (K16–K19, lines 683–718): extracts backtick tokens, expands `{a,b}`, verifies every path exists in git blob/tree at `--revision` (`paths_at_rev`). For `host-census-gate`, additionally verifies stated case count equals actual `tools/tsukuroi-census.sh --selftest` output at that revision.
   - SHONEN boxes (K20–K23, lines 720–750): verifies all named paths exist at revision and marked boxes carry non-author verifier.
   - Knowledge citations (K24–K27): verifies cited `corpus/knowledge/*.md` exist and are not marked `superseded` in lines 1–20.
   - Quantitative claims (K09–K15): verifies stated table lines in SKILL.md, lesson count in `corpus/lessons/`, lines in `README.md`.
2. **kama-shokunin** `tools/capability-repertoire-audit.py` (lines 145–156):
   - Canonical Capabilities table in SCORECARD.md: checks `unsubstantiated == 0` (every capability row's evidence cell must contain at least one repo-relative path resolving via git `cat-file -e` at `--tip`), and `missing == 0` (every capability in any SCORECARD table is listed).
*(Also noted: `souji-shokunin/tools/souji-declared-evidence.py:120-190` Class A paths, Class B commit objects, Class C sha256 digests).*

## 3. Fleet Calibration Axis in AXES.md vs Chousa C3
- **Fleet Definition** (`AXES.md:15`):
  `| **calibration** | Self-assessment quality: gaps named honestly, confidence graded, overreach caught | SHONEN.md/SCORECARD.md entries match observed repo state |`
- **Does C3 measure AXES.md calibration, or only link-rot?**
  **C3 measures only link-rot** (syntactic pointer existence / non-empty file resolution), NOT calibration as defined in `AXES.md`.
  - Evidence from `c3-count.py:24-26`: *"Named limits: existence, not truth — a pointer to a file that exists but does not show the claimed behaviour passes; pointers outside backtick spans are not read; cells of the Axes table are not read."*
  - C3 checks whether referenced paths exist on disk (`st_size > 0`) or are redirected via `correction: SCORECARD.md:<line> <ptr> -> <tgt>`. It does not execute commands, verify whether the cited evidence actually demonstrates the claimed capability, verify stated scores or case counts, or inspect the `Axes` table where confidence and overreach are graded.

## 4. Blanket-Correction Controls: C3 and Sibling Precedents
- `c3-count.py` passes the `BLANKET` control (`controls/build-c3-controls.py:38-40`, appending `correction: all pointers resolve`) because its parser (`c3-count.py:41`) strictly requires `r"^correction: SCORECARD\.md:(\d+) (\S+) -> (\S+)"` and non-empty target existence.
- **Sibling-lane counter immune to blanket corrections**: **kama-shokunin** `tools/round33-claim-audit.py:86-137`.
  - `correction_rows` requires section `### Round 33 — correction of round-32 gate-control receipt references` with table rows `| <fault> | <cited_path> | <stated_output> |` where fault is in `FAULTS`, exactly one row per fault, `cited_path == correct_path`, and `stated_output` matches the git blob. A blanket correction is ignored and fails with `valid < 3`.
  - Also: `tsukuroi-shokunin/tools/check-self-assessment.py:20-22` explicitly excludes any `correction:` line from qualifying as an ordinal reference.

## 5. Fleet Precedents for C1's Counting-Time Nonce Design
C1 generates dynamic test inputs at counting time from fresh random nonces (`c1-count.py:101-118`). This pattern appears across the fleet:
1. **mado-shokunin** `quality/counters/c1-r40-live-v2.py:28-31, 1181`: `nonce = args.nonce or secrets.token_hex(8)`. Generates dynamic live compositor fixtures (`fixture_for(rev, nonce, ...)`) at counting time inside bwrap sandbox to prevent answer-key hardcoding / forgeable tools.
2. **mori-shokunin** `.ufo/waves/round-31/count-c2-a1.py:54-55`: appends fresh random nonce comments (`<!-- nonce {nonce} -->`) and randomized filenames (`Case` + 6 random chars) to briefs in bwrap sandbox to stop static pattern matching.
3. **chousa-shokunin** `corpus/evidence/round50/c1-supplement.py:41`: injected `nonce = "re-verify-" + secrets.token_hex(4)` into recheck strings.

## 6. UFO-FSD Connector Synthesis & Proposed Move
- **Affected Axes**: `calibration` (primary improvement), `operability` (hardened), `depth` (unharmed).
- **Proposed Move**: Bridge the gap between C3's link-rot check and AXES.md calibration. Synthesize C1's counting-time nonce harness and sibling patterns (`souji` Class C sha256 digests, `tsukuroi` K13 selftest execution): in future calibration rounds, require newly declared capability rows in SCORECARD.md to bind to an executable verification command that evaluates a dynamic run nonce or content digest, ensuring evidence proves actual capability truth rather than mere file existence.
- **Risks**: Increased evaluation latency; brittle historical replays. *Mitigation*: apply executable verification only to newly added capability rows, keeping syntactic pointer resolution for historical rows.
- **Verification**: Run `c3-count.py` and `build-c3-controls.py` on scratch roots; verify that controls `BLANKET`, `DELETED`, `EMPTY` fail (exit 1) while true repairs pass (exit 0).

VERDICT: Proved C3 measures only link-rot (not AXES.md calibration); identified kama round33-claim-audit.py:86 as blanket-immune sibling and mado c1-r40-live-v2.py:1181 / mori count-c2-a1.py:54 as fleet nonce precedents.
