# RevGateDiff — diff audit of the landed gate (round 34 attempt 2, wave 2)

Reviewer: chousa-r34-w2a2-RevGateDiff-9 · 2026-10-23 · Read-only on lane production files; all experiments in `/fast/scratch/hyaku/chousa-r34-a2/w2/RevGateDiff/`.

## Scope and method

Target: `git diff bf7c931a..707da8184a0fc4d10ab3f17271556cdf364f0af5 -- tools/research-gate.sh`; classify every hunk functional / comment / selftest; any functional hunk outside the constant is a finding.

Blob pins (sha256sum):
- Worktree `tools/research-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` = `git show 707da818…:tools/research-gate.sh` — equals the landed prefix `a6307edf687ac0fb`. Worktree `git status --porcelain -- tools/` empty.
- Base blob `git show bf7c931a…:…` = `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58` — matches claims-a2.md ("gate 772a1d8e…3e58").
- Range `bf7c931a..707da818` = 7 commits (7c7eb3a, 2592f9d, fe0f22e, 0af0844, fce3119, bd8c8bd, 707da81). `git log --oneline <range> -- tools/research-gate.sh` lists exactly one: **fe0f22e**. Mode unchanged (`100755`), no rename. Range also touches non-`.ufo/` files (LOG/SCORECARD/SKILL/corpus) — outside this target, gate only audited.
- Scratch extractions: `gate-new.sh`/`gate-old.sh` (shas above re-verified after extraction). No LSP device exists in this seat's tool inventory; text diff + empirical runs used (recorded as unavailability, per protocol).

## Hunk classification (diffstat 57+/16−; every changed line inspected)

**Hunk 1 — `@@ -1563,23 +1563,22 @@` (15+/16−), file lines ~1565-1581.**
- FUNCTIONAL (1 line, exactly the target constant): `TOK_DIRECT_SPAN_MAX=32767` → `TOK_DIRECT_SPAN_MAX=32764` (trailing inline comment reworded — comment part).
- COMMENT (all other 29 changed lines): header line and rewrite of the long-span comment block (old argv-only E2BIG narrative → two-ceiling narrative: execve E2BIG at ≥32768 and PCRE2 compiled-pattern ceiling; "a pattern for a 32764-byte span compiles; 32765 fails").

**Hunk 2 — `@@ -7855,6 +7854,48 @@` (42+/0−), entirely inside `run_selftest()` (function spans new lines 4011→7905; hunk sits immediately before the `if [[ $failures -eq 0 ]]` PASS/exit).**
- SELFTEST (all 42 lines): 10 comment + 32 executable selftest lines — fixtures under `$WORK` only (`lib/deadzone.md`, `deadzglued.md`, `deadztwice.md`, `deadzedge-low.md`, `deadzedge-high.md`), claims files, and 3 `tclaims` calls (`claims-deadzone` DD1-DD3, `claims-deadzone-line` DD4-DD5, `claims-deadzone-edge` DD6-DD7). No `cases=` lines added; `tclaims()` increments `cases` internally (gate-new.sh:4145), so case count +3. Zero runtime-path lines.

**Functional hunks outside the constant: NONE.** The functional delta is exactly `TOK_DIRECT_SPAN_MAX` 32767→32764 plus the selftest block — target confirmed.

Consumer check: `TOK_DIRECT_SPAN_MAX` has exactly one runtime use, `tok_span_offsets` gate-new.sh:1599 `if (( ${#span} > TOK_DIRECT_SPAN_MAX ))` → `tok_span_offsets_chunk` else `tok_span_offsets_direct`. So spans 32765..32767 route to the chunk matcher; ≤32764 unchanged; no other constant/limit reference in the file (grep over blob).

## Re-derivations (commands quoted; all run 2026-10-23)

1. **Boundary claim in the new comment** — GNU `/usr/bin/grep` 3.12-modified, exact gate invocation shape `grep -a -z -b -o -P -- "$p"` with `$p=$(printf '\\x77%.0s' $(seq 1 $n))`:
   `n=32764 GNU_rc=1` (compiles) … `n=32765 GNU_rc=2 /usr/bin/grep: regular expression is too large`. Matches the diff comment, S065's host note (corpus/SOURCES.md:75, "compiled repeated \x41 literals through a 32,764-byte span and rejected 32,765", accessed 2026-10-23), and the committed able-to-fail receipt `.ufo/waves/round-34/measure-a2/deadzone-fixture-vs-gates.txt` (pre-fix gate: both DD1/DD4 `unsupported` with the too-large stderr; landed gate: both `supported`, `VERDICT_BEARING_CLAIMS=2/2`).
2. **Selftest counts** — old blob `RESEARCH_GATE_SELFTEST: FAIL (10/253 cases)` in my first scratch run; new blob `FAIL (10/256)`; explicit `cases=$((cases + 1))` sites 30↔30 unchanged, `tclaims` calls 56→59. +3 cases, old total 253 — arithmetic and commit-message claim confirmed. Committed receipts `.ufo/waves/round-34/measure-a2/selftest-a2.log` and `battery/selftest.log` show `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)` with `ok-case 254 claims-deadzone`, `255 claims-deadzone-line`, `256 claims-deadzone-edge`.
3. **New cases pass in my env too**: `ok-case 254/255/256` in both my new-gate runs; the 3 new cases are the entire old→new delta (identical ok/FAIL sets otherwise).
4. **My scratch env artifacts (not gate defects)** — first run (forced `TMPDIR=$PWD/tmp`, everything on /fast): 10 failures, byte-identical set on old and new blobs (cross-device / symlink / corpus-root cases can't trigger on a single-device layout). Re-run with default TMPDIR: **FAIL (1/256)** — the only survivor is `claims-lane-fallback`, pre-existing and env-bound (expects the lane fallback to resolve `PROVINCE.md` from the gate's own lane layout; my blob sits bare in scratch → `CLAIM_SOURCE_MISSING`; also fails on the old blob). Committed receipts PASS 256/256 in canonical layout. Scratch logs cited below.

## Findings by severity

**F1 · LOW · comment off-by-one in the landed selftest block.** New comment (gate-new.sh:7857) says "cases 255-257", but the three new cases are numbered **254-256**: proven by committed receipt ok-case numbering and by both my runs (old blob tops out at case 253 = `claims-longspan-line`). Commit messages, SCORECARD and the wave target all say 254-256 — only this in-code comment is off by one. No functional effect; fix is a 1-token comment edit for a later commit.

**F2 · LOW · environment hazard, no committed defect: `grep` is not reliably GNU grep on this host.** In several of my scratch shells plain `grep --version` printed `grep (pi-uu-grep) 0.2.0` (same command in other shells resolves `/usr/bin/grep` = GNU 3.12-modified; PATH differs per ephemeral shell — the binary was never located to a stable dir). Under pi-uu-grep the PCRE2 ceiling is LOWER: the gate-shaped 4×32764-char pattern fails to compile (`PCRE2: error compiling pattern at offset 131060: regular expression is too large`), i.e. the dead zone would extend below 32764. The gate's dependency probe (gate-new.sh:1687, `printf 'x' | grep -a -z -b -o -P`) accepts any grep with those flags, so dead-zone behavior silently depends on which `grep` is first on PATH. All committed evidence is consistent with GNU grep (before-receipts carry the GNU error string; S065 cites `/usr/bin/grep`), and C2's counter surface (32765..32767) routes to the chunk matcher under either grep, so no committed claim is implicated — but any seat re-deriving measurements without pinning `/usr/bin/grep` can get different numbers. Reporting only; not fixed (read-only seat).

**F3 · INFO · `master` has moved one commit past the frozen tip.** `git rev-parse master` = `fe3db76c0ae9fa18…`, parent = `707da818…`, touching only `.ufo/waves/round-34/w2a2-{plan,spec,taskcall}.json` ("wave-2a2 spec/plan/taskcall re-frozen at tip 707da818… gate and counters unchanged" per its message; `git diff --stat` confirms 3 files). Gate untouched since fe0f22e; frozen-tip discipline holds for `tools/`.

## Verdict

Diff audit **PASSES**: functional change is exactly `TOK_DIRECT_SPAN_MAX` 32767→32764 plus the three-case selftest block; zero other functional lines; hunks classified as above. Findings F1 (comment) and F2 (env hazard) are non-blocking, evidence cited. No re-scoring of held C1 shapes was attempted (frozen exclusion respected); no lane production file was written by me except this report at the assigned trailer path.

## Limits and verification gaps

- Could not reproduce `PASS (256 cases, 0 skipped)` in scratch: best re-run 255/256 with the pre-existing env-bound `claims-lane-fallback` (needs a lane layout; fails identically on the base blob). Committed receipts show 256/256 in the canonical environment.
- pi-uu-grep's install location was not pinpointed (ephemeral per-shell PATH entries; no file under `~/.local/bin/grep`); its exact ceiling was bracketed only (compiles 4×29999-char patterns — C1 selftest cases pass in that shell — fails 4×32764).
- Sibling seats own the counter/self-audit re-derivations (c2-count.py 37/37, self-audit 0/0); not duplicated here except as cited receipts.

Scratch artifacts (all under `/fast/scratch/hyaku/chousa-r34-a2/w2/RevGateDiff/`, each <1 MiB): `gate-new.sh` sha256 `a6307edf…995b`, `gate-old.sh` sha256 `772a1d8e…3e58` (full digests as pinned above), `selftest-old.log` (10/253), `selftest-new.log` (10/256, TMPDIR-on-/fast), `selftest-new2.log` (1/256, default TMPDIR; FAIL-case `claims-lane-fallback`).
