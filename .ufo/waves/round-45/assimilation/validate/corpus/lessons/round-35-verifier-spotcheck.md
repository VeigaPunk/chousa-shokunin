# Round 35 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-23
lane HEAD verified: `c1dbbec33dc6f8ef7e188dff1efae64951c26d05` (base `08be4c9e3a4ebe55d915ce4761c81854286c23ae`)
report: `.ufo/reports/round-35/chousa.md` (committed by the lane identity `chousa-shokunin <chousa@shokunin.local>`, fleet commit `852372f0`; two earlier report commits `dbe9f8cf` and `315d96b0` are superseded revisions of the same path)

Claims are graded as **narrowed by their own errata**, not as their first draft: C1 proves path + version
resolution, refusal shape and output equality (not per-call engine identity); C2 proves the routed matcher
function was entered (not that its body ran). The survivors that produced the narrowing are routed to r36
below, not counted as r35 conformance defects.

## Step-1 conformance

- Report committed by the lane identity: **PASS** — `git log --format='%an %H' -- .ufo/reports/round-35/chousa.md`
  shows `chousa-shokunin 852372f0…`, `chousa-shokunin 315d96b0…`, `chousa-shokunin dbe9f8cf…`.
  The report lands after the work it cites: fleet `852372f0` at 17:35:27 -0300, lane tip `c1dbbec3` at 17:35:17.
- `SHONEN` heading with one line per box: **PASS** — 4 lines, all `[~]` with resolving pointers
  (`SKILL.md` registry rows / checklist item 6, `LOG.md` §Round 35, the counters and the witness command).
  No `[x]` was written by the lane, and none by this verifier (promotion is operator-owned).
- Cited lane commits exist and are ancestors of the branch ref `master` (HEAD is detached): **PASS** (12/12):
  `08be4c9e 0e167649 2b2e0171 e87c5d7e beb04ea1 770a69d6 7d21a333 234c95d4 b6f2c0db 3810bcca 119efa28 c1dbbec3`.
  Content hashes cited as artifact identity were re-derived where they bind a receipt: base gate
  `a6307edf687ac0fb…2995b` = `08be4c9e:tools/research-gate.sh`; first-landing gate `1f2fb4f5…c617` =
  `e87c5d7e:tools/research-gate.sh`; final gate `a47688518e50…c38ad` = `770a69d6`, `038543b2` and `c1dbbec3`
  `tools/research-gate.sh`; hardcoded control `05bdf654…a378` = the committed control script.
  The mutant hashes (`147ded03… fd6d5a8e… 9040dcba… 3a7cbefc… 51ffec6a… 3e5648b8…`) are wave-artifact
  identities, not lane commits; they resolve inside the committed seat reports and were not re-executed.
- Pushed: **PASS** — `jj-lane.sh state` → `local=c1dbbec3… remote=c1dbbec3… ahead=0 behind=0`.
- Uncommitted round work: **PASS at the final tip** — `git -C … status --porcelain` is empty at
  `c1dbbec3` (an earlier 20:35Z observation, mid-settle, showed 3 modified + 21 untracked under
  `.ufo/waves/round-35/w2/`; the settle commit `c1dbbec3` committed them).
- Prompt contract: **PASS** — `.ufo/prompts/chousa-round-35.md` (372 lines) carries the round-level contract
  verbatim (§1 mission/axes SSOT, §2 claims 1–3 + admission, §2b frontier step, §3 L2 floor ≥8 in ONE batch,
  §4 report contract, §5 commit/push scope + L0) and the five child-lane items: report path/filename (§4),
  `SHONEN` heading (§4), commit-hash citation rule (§6.4 "Cite ONLY the helper's final `landed <hash>`"),
  commit-before-report ordering (§6.4 "The report lands last and cites the pushed lane hash"), write scope (§6.3).
  §3's ≥8/one-batch matches `MISSION.md` §L2 concurrency; the prompt quotes no route map, so no bucket can mismatch.
- Report minimum content: **PASS** (work performed with pointers; landed changes tied to `LOG.md` §Round 35;
  before→after per claim with commands and measured commits; Sources & frontier with census; three trend
  verdicts; `SHONEN`). **Defect:** the wave section still reads "60 of 65 seat reports are on disk at the
  final integration commit" while its own cited tip `c1dbbec3` holds 62 `w2/*.md` seat reports, and it names
  only the dead `CritWitnessBlind` — the 3 still-missing items (`CritWitnessBlind`, `ExecC1Fresh1`,
  `ExecPinModeSelftest`) are not named anywhere in the report. Status-neutral (the report is real work).
  Minor: the Landed-changes row "lane tip at landing `b6f2c0db`" is stale against the header's `c1dbbec3`.

## Per-claim re-check (commands run by this verifier, observed output)

Snapshots, not the live worktree: `git archive <commit> | tar -x -C /tmp/…` for base `08be4c9e` and final
`c1dbbec3`. At the final tip, `tools/research-gate.sh` = `a4768851…c38ad`, `c1-count.py` = `da207fd7…15e3`,
`c2-count.py` = `557fdbf0…9171`, `tools/mechanism-witness.py` = `9f537bfd…52b3` — byte-identical to the
`038543b2` snapshot. Fresh receipts were written to scratch (`/tmp/r35-verify/`, session-scoped, not cited);
the re-runnable command plus the label below is the evidence.

### C1 — operability, narrowed reading: **VERIFIED**

- `C1_TMP=<dir> python3 corpus/evidence/round35/c1-count.py --gate /tmp/chousa-r35-base/tools/research-gate.sh --seed 3501`
  → `GREP_PIN_MATCH=0/9`, exit 1, receipt `gate_sha256=a6307edf687a…` (base bytes).
- Same counter, final snapshot, `--seed 3701` → `GREP_PIN_MATCH=9/9`, exit 0, `gate_sha256=a47688518e50…`;
  `--seed 3711` → `GREP_PIN_MATCH=9/9`, exit 0. (Also `--seed 3601/3611` against the identical `73921312`
  snapshot → 9/9 both.)
- Cheapest control `--gate .ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh --seed 3501` →
  `GREP_PIN_MATCH=3/9`, exit 1, `gate_sha256=05bdf6543858…` — the obvious fix does not meet P1.
- Narrowed reading confirmed by what the counter reports (S1–S9: path, source, version, refusals, output
  equality) and by the code: `grep_pin_init` is called at `research-gate.sh:8060`, after usage parsing and
  before every mode's record read; refusal is exit 2 with `GREP_PROVENANCE`. The open-ordering claim rests on
  the wave's strace evidence, as the report states; this verifier did not re-run strace, and the report does
  not claim the counter shows it.

### C2 — calibration, as a routing witness: **VERIFIED**

- `C2_TMP=<dir> python3 corpus/evidence/round35/c2-count.py --gate tools/research-gate.sh --seed 3701`
  → `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`, exit 0, `gate_sha256=a47688518e50…`;
  `--seed 3711` → identical. Both keyed engines are output-full (9/9) and witness-fail (chunk stamps 0).
- Direct run `python3 tools/mechanism-witness.py --gate tools/research-gate.sh --seed 3701` →
  `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)` — the 9-vs-8 slack the report names.
- Counter controls: always-pass witness → `WITNESS_SEPARATED=0/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`, exit 1;
  always-fail witness → `WITNESS_SEPARATED=2/2 … LANDED_WITNESS=fail`, exit 1; absent battery →
  `WITNESS_SEPARATED=0/2 battery=absent`, exit 1.
- The narrowed reading ("the routed matcher was entered, not that its body ran") matches the mechanism:
  the witness counts function-entry stamps. The report's forgeable-PS4, one-record-shortcut and body-replaced
  survivors are consistent with that reading and are routed below.

### Repairs (not claims)

- R1: `bash .ufo/waves/round-35/repairs/slen-probe.sh /tmp/chousa-r35-base/tools/research-gate.sh` →
  `SLEN_PROBE offsets=0 first=`, exit 1; on the final gate → `SLEN_PROBE offsets=1 first=5`, exit 0.
- R2: `research-gate.sh:7920` says `cases 252-253`, `:7953` says `cases 254-256`; the committed selftest log
  labels 252 `claims-longspan`, 253 `claims-longspan-line`, 254 `claims-deadzone`, 255 `claims-deadzone-line`,
  256 `claims-deadzone-edge` — comments match the run.
- R3: 26 top-level `w2a2/*.md` reports tracked (`git ls-files '.ufo/waves/round-34/w2a2/*.md' | awk -F/ 'NF==5'`
  = 26; the unquoted shell-glob form the report prints also yields 26; the quoted git pathspec yields 36 only
  because it recurses into fixture subdirectories). `ExecC2Oracle/boundary-diff.txt` is tracked at `6a3cc32`.

## No axis harmed

- `git diff 08be4c9e c1dbbec3 -- SCORECARD.md` → one append hunk at the file end, 53 insertions, 0 deletions;
  no earlier score edited. `PROVINCE.md` diff is empty.
- No-harm battery (committed `w2/ExecNoHarm/comparison.json`): 14/14 rows `base_equal_after_timestamp_mask` and
  `tip_equal_after_timestamp_mask` true; `BATTERY_RESULT=PASS`. Committed selftest log:
  `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`.
- Census: `scripts/sources-census.sh validate --root … chousa` → exit 0, two standing W04 duplicate-URL
  warnings (S051/S053); rows 66 → 68 (`awk` row count at base and final).
- The two known landed defects (pin echo in the `--pin` capture; `verify-all --json` unpinned `sha256sum|cut`)
  are pre-existing/known, named in the report and claims.md erratum, and do not harm a scored axis this round.

## Discernment spot-check (LEARNING.md §Discernment is checked from outside)

The lesson's `## Gate` records only admitted rows and no explicit rejected candidate, so the reject sample
below is taken from the round's recorded gate decisions (the narrowed draft clauses in the report's Sources
section and the lesson's `## Mistakes`). The missing rejects in `## Gate` are a conformance defect, routed below.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S067 exec(3) | admit | `/usr/share/man/man3/exec.3.gz` | agree | sha256 `2f1badd3…b1523` matches the row; the 17-word quote is verbatim at decompressed lines 107–110; the page states the PATH list, not its order (the only "in that order" is `/bin`, `/usr/bin` at line 200); `execvp.3.gz` is a `.so man3/exec.3` stub |
| S068 bash(1), narrowed | admit | `/usr/share/man/man1/bash.1.gz` | agree (pointer note) | sha256 `b68beb3e…bdffe` matches; the 21-word `BASH_ENV` quote is present and the paragraph anchor 388–404 contains it; the parenthetical "quote at 391–395" is one line short at each end — the quoted words span 390–396 (390 `When`, 396 `in the environment`) |
| S068's original exported-function clause | reject | `/usr/share/man/man1/bash.1.gz` | agree | decompressed 388–404 contains no `export`/`function`/`later definition` (grep exit 1); the exported-functions text is at 5294–5304. The landed row excludes that clause and scopes itself to `BASH_ENV`; it carries the corrected anchor |
| S067's first-draft "PATH components searched in order" | reject | `/usr/share/man/man3/exec.3.gz` | agree | the page's search paragraph states the colon-separated list only; order is not stated. The row moves the order claim to the counter's S1 measurement, which is the right home |
| C2 axis fit (`CritC2AxisFit`) | narrowed, not argued away | `SCORECARD.md` C2 row; report C2 verdict | agree | the row and report both state P2 measures receipt strength, not the lane's self-assessment accuracy; the claim is admitted only as a routing witness |

No disagreement in the sample. S068 is clean as landed; the anchor defect the wave found is resolved.

## Trend verdicts (non-author)

- expansion — **improved**: three new admitted knowledge entries (`grep-pin-r35`, `keyed-engine-output-equivalence-r35`,
  `bash-local-expansion-r35`) and two new tier-A source rows (S067, S068, 66 → 68, census exit 0), each entry
  present in `corpus/README.md`'s table with `source:`/`verified-at:`/`recheck:`. The round truthfully states it
  closes no `## Frontier` row.
- quality — **improved**: a real contract hole (PATH-resolved matcher) closed and hardened; the latent `slen`
  defect repaired with a probe that fails on the old bytes (re-run both directions here); case-range comments
  corrected against the selftest's own labels; QUALITY 45–49 added, each citing the lesson; the 14-row no-harm
  battery and the 256-case selftest show no regression; no admitted entry failed re-check.
- discernment — **improved**: the round falsified its own instruments before closure (six independent seats on
  the C1 engine-identity class, four on the C2 witness), recorded every survivor as a narrowing in SCORECARD and
  claims.md §Erratum instead of arguing it away, and this outside sample agrees on every decision checked.
  Caveat (routed): the lesson's `## Gate` does not record rejected candidates or the outside spot-check result.

## SHONEN note for the operator (promotion is operator-owned)

All four boxes are `[~]`. The underlying evidence is checkable by a non-author and consistent: the SKILL rows and
checklist item 6 resolve and name the exact commands; `LOG.md` §Round 35 carries the round entry; the counter
receipts (`final/c1-s*.json`, `final/c2-s*.json`) and the committed selftest log carry the stated labels; the
`PROVINCE.md` diff is empty. This file supplies the outside judgment for the round; a named outside reviewer can
close the boxes at the next promotion review.

## Routed defects (for the lane's next round)

1. **Lesson `## Gate` is incomplete** — no rejected candidates and no spot-check result (CORPUS.md requires
   candidates, admitted, rejected with reasons, spot-check). The reject decisions exist only in `## Mistakes`
   and the report. r36: add the rejects and this file's pointer.
2. **Report wave-return figure is stale at its own cited tip** — says 60/65; `c1dbbec3` holds 62 seat reports;
   the 3 without a report (`CritWitnessBlind` dead, `ExecC1Fresh1`, `ExecPinModeSelftest`) are unnamed in the
   report. Append an erratum with the final count and the names.
3. **Known landed defect (already routed):** `CHOUSA_GREP_PIN_ECHO=1` is inherited by the `--pin` capture body,
   so a baseline pinned with the echo on makes `--drift` report `GATE_DRIFT: -LINE` against an unchanged gate.
4. **Known pre-existing defect (erratum 13):** `verify-all --json` builds `record_sha256`/`gate_sha256` with
   `sha256sum | cut` resolved through `PATH` and validates them only for non-emptiness (`research-gate.sh:3668-3671`).
5. **C1 narrowed reading / r36 canary:** the C1 counter reads the `GATE_GREP:` echo as a string and cannot see
   per-call engine identity; receipts lack `counter_sha256`. The r36 semantic canary is the planned fix.
6. **C2 witness limits:** aggregate stamp threshold (9 stamps for 8 long records), forgeable `PS4` channel,
   body-replaced matcher and one-call-for-show all survive; per-record attribution is the r36 requirement
   (QUALITY 49).
7. **Locale seam (erratum 14, pin-independent):** `json_unescape` (`research-gate.sh:1398-1449`) lacks the
   `LC_ALL=C` scope the matchers carry; `LC_ALL=C --selftest` fails 10/256 with the pin bypassed. r36 pins a
   locale and adds a C-locale selftest arm.
8. **Minor pointer precision:** the S068 parenthetical quote anchor 391–395 vs the actual word span 390–396;
   the paragraph anchor 388–404 is correct, so no teaching is wrong.
9. **Minor report staleness:** the Landed-changes row "lane tip at landing `b6f2c0db`" vs the header's `c1dbbec3`;
   correct the row in the next report's erratum, never by rewriting the filed bytes.
