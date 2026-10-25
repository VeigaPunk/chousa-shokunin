# CritC2Framing — round 47 wave 1 (critic, leaf)

Item: attack R47-C2 as a CALIBRATION claim (AXES.md:15 — "Self-assessment quality … SHONEN.md/SCORECARD
entries match observed repo state"). Is UNREGISTERED+DANGLING such a count? Is the dependence leg real
dependence? List executables a Gates row should carry that even the round-47 set misses. Recommend honest
SCORECARD wording. No edits to lane files. Lane HEAD `a15610a59aaeaf43b79ccc650acee4bd4da00341`.
Pins (sha256): r47 c2-count.py `36b3934e…36d1`; r46 c2-count.py `f93cb107…046f` (= R46_SHA, instrument
unchanged); SKILL.md `0fcdc442…d2d1`; QUALITY.md `8c989355…35e2`. No tools installed. No fetch.

## Verdict

**Plumbing presented as calibration; the count overstates the gap.** MISMATCHES=25 is a registry-completeness
count measured with a naive table parser. Only 8 of the 25 are self-assessment-vs-repo mismatches (7 genuine
omissions plus 1 malformed row). 10 come from the counter splitting on escaped `\|`. 3 are controls. 1 is a
placement choice. 3 are this round's own new counters. The dependence leg counts any literal, so a comment
can add a path. It also misses a real `$SCRIPT_DIR/…` call. The claim holds as a fixable plumbing claim. The
calibration wording must be narrowed (below). The predicate, counter, floor and target stay as frozen.

## Commands run (verbatim decisive lines)

1. `python3 corpus/evidence/round47/c2-count.py --list` (lane, HEAD) →
   `ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7)` `FLOOR=92` `GATES_ROWS=36` `REGISTERED=67/92`
   `UNREGISTERED=25` `DANGLING=0` `MISMATCHES=25` `C2=FAIL`, exit 1 (= the frozen "before").
2. `/tmp/…/breakdown.py` (imports both pinned counters, rebuilds the set, classifies each unregistered path) →
   `{('abc','anyrow'): 15, ('abc','norow'): 3, ('chk','norow'): 6, ('dep','norow'): 1}`;
   `DEP_NAMER corpus/evidence/round25-meta-oracle.py <- corpus/evidence/round25-meta-differential.sh`;
   literal kinds across all 92 entry-point sources: `KINDS {'code': 32, 'docstring': 51, 'string': 33, 'comment': 6}`.
3. `/tmp/…/pipes.py` (naive `split("|")` vs GFM split on unescaped `|`, per unregistered `anyrow` path) →
   10 paths at `SKILL.md:114`: `naive_cells=14 … naive_c3_exit=False | gfm_cells=8 gfm_idx=[2] gfm_c3_exit=True | escaped_pipes=6`.
   `SKILL.md:100` (mechanism-witness): `naive_cells=11 … gfm_cells=11 … gfm_c3_exit=False` (cell 3 = `` `WITNESS=pass ``).
   `SKILL.md:97/98/106` (base-gate-r38/39/41.sh) and `SKILL.md:88` (round29/c1-count.py): path in cell 4
   ("self-test"/before), verdict map has exit.
4. Mutation probes on `git archive HEAD` copies under /tmp (lane untouched):
   - `cmt`: append `# not run, history only: corpus/evidence/round45/build-spans.py` to round47/c1-count.py →
     `ENTRY_POINTS=93 (abc=84 dependence=+2 …)` `UNREGISTERED=26` `MISMATCHES=26`.
   - `pipe`: replace the six `\|` with `/` on SKILL.md:114 only (punctuation inside a code span) →
     `REGISTERED=77/92` `UNREGISTERED=15` `MISMATCHES=15`.
   - `base`: identical to command 1.
5. `/tmp/…/composed.py` (basename/`$DIR/`/sibling-import resolution inside every entry point) →
   `MISSED norow corpus/evidence/round26-registry-oracle.py <- corpus/evidence/round26-registry-differential.sh:9 | ORACLE=$SCRIPT_DIR/round26-registry-oracle.py`
   (run at the `python3 "$ORACLE" "$dir" …` line of the same file). No other miss.
6. `/tmp/…/invoke.py` (every tracked *.py/*.sh in corpus/evidence, tools, .ufo/waves = 1057 files; lines with
   subprocess/Popen/os.system/bash/python3/source/exec/runpy/import) → no entry point calls a non-set path via a
   literal. 34 out-of-set callees, all called only from non-entry `.ufo/waves` scratch (e.g. round-34
   `controls/L1-gates/*_ctl.py`, round-35 `span_search.py`). The out-of-set executables under corpus/evidence and
   tools are `round25-holds/battery.sh`, `round25-sources-census.sh`, `round26-registry-oracle.py`,
   `round45/build-spans.py`, `round46/controls/{always-pass,cite-only,name-oracle}.py` and
   `round47/controls/{always-exit-1,base-tool-r46,neg-word-refuser}.py`.
7. `/tmp/…/selfdocs.py` (paths named by the self-assessment docs, checked against the set) → `SHONEN.md: named=1 not_in_eps=0`,
   `LOG.md: 17/0`, `lessons: 62/4` (round-30 `leak-map.py`, round-31 `oracle-c1.sh`, round-33
   `ExecNoHarmBase33/battery.sh`, `round45/build-spans.py`). Absolute out-of-lane literals:
   `corpus/evidence/round41/c2-count.py:14,18` → fleet `scripts/sources-census.sh` (CALLED via `subprocess.run`);
   `tools/quarantine-check.py:26` → shokuknow `quote-lint.py` (docstring: "NEVER run from this lane").

## Finding 1 — is MISMATCHES a calibration count? (impacted: calibration)

AXES.md:15 measures calibration as the lane's own *self-assessment entries* against observed state. SCORECARD's
Axes table carries no calibration score (SCORECARD.md:7 lists operability only). The self-assessment that C2
tests is the round-46 verdict row (`REGISTERED=81/81 UNREGISTERED=0`, SCORECARD.md:2460) and capability row 46
(SCORECARD.md:2479). Breakdown of the 25:

| class | n | paths | self-assessment mismatch? |
|---|---:|---|---|
| counter artifact: escaped `\|` at SKILL.md:114 | 10 | round24–27 instruments | **no** — GFM renders entry=cell 2, verdict has exit |
| malformed row: unescaped `\|` at SKILL.md:100 | 1 | tools/mechanism-witness.py | **yes** — rendered verdict map loses `exit` |
| never in any row: QUALITY `Check:` / dependence | 7 | mask-gate.sh, receipt-binding.py, slen-probe.sh, prose-check.py, rerun-check.py, q33-check.py, round25-meta-oracle.py | **yes** — the round-46 claim "covers the verifiers the verdicts name" was overreach |
| controls named in the before cell | 3 | .ufo/waves/round-38/39/41 `controls/base-gate-rNN.sh` | **no** — these are base-gate snapshots; moving them into `entry` would register a non-gate (claims.md:98 limit) |
| counter in the self-test cell | 1 | corpus/evidence/round29/c1-count.py (SKILL.md:88) | placement only |
| this round's own counters | 3 | round47/c{1,2,3}-count.py | **no** — created at freeze; no prior self-assessment |

Counterexample (command 4 `pipe`): changing punctuation inside one code span, with no registry content change,
cuts MISMATCHES 25→15. Ten of the "mismatches" measure the parser, not the lane's honesty. The fix (removing
`\|` from row 114) is legitimate but cosmetic. It must not be scored as calibration movement.

## Finding 2 — is the dependence leg real dependence? (impacted: calibration, operability)

No. Leg D is "a repo-relative path literal anywhere in an entry point's source". 90 of the 122 literal hits are
docstring, comment or non-call string; 32 sit in code (command 2). Its single current contribution happens to be
real (`round25-meta-differential.sh:40` runs `python3 corpus/evidence/round25-meta-oracle.py`). Both failure
directions are demonstrated:
- **Over-inclusion**: a comment that says "not run" adds a path and a mismatch (command 4 `cmt`: 92→93, 25→26).
  It also raises ENTRY_POINTS, so FLOOR can be padded by comments. The live analogue is quarantine-check.py:26,
  a docstring naming a checker it says is NEVER run. That literal is excluded today only because it is absolute
  and out of lane.
- **Under-inclusion**: `round26-registry-differential.sh:9` → `$SCRIPT_DIR/round26-registry-oracle.py` is a real
  call the leg misses (command 5). `round41/c2-count.py` calls fleet `scripts/sources-census.sh` (out of lane,
  invisible to any leg; not registrable in-lane — note it, don't count it).
Honest name for leg D: "mentioned-by-entry-point closure", not "dependence".

## Finding 3 — executables a Gates row should carry that the round-47 set misses

1. `corpus/evidence/round26-registry-oracle.py` — called by a registered instrument (above). **Should carry.**
   It is the one true dependence miss.
2. `corpus/evidence/round46/build-spans.py` is already registered (SKILL.md:118). Its predecessor
   `corpus/evidence/round45/build-spans.py` is named in lesson round-45.md:42 and SCORECARD.md:2480 only via r46. It is a
   builder, not a verdict. **Classify it**: register it as a non-gating builder, or record it as an exempt builder.
3. Controls driving claim verdicts, none in the set: `round46/controls/{always-pass,cite-only,name-oracle}.py`
   (round46 c1-controls.txt:2,10,18) and `round47/controls/{always-exit-1,base-tool-r46,neg-word-refuser}.py`
   (c1-controls.txt:3,13,23; neg-word-refuser imports base-tool-r46 via `with_name`). These are not gates. The
   honest move is one `kind=control` row per round, or a stated exemption. Silently omitting them is wrong too.
4. Lesson-named `.ufo/waves` executables (`round-30/controls/CriticHarnessIntegrity/leak-map.py`, flagged
   *unreviewed* by round-30.md:184; `round-31/controls/MutOracleC1/v2/oracle-c1.sh`;
   `round-33/w1/ExecNoHarmBase33/battery.sh`, cited as the D3 battery in round-33.md:25). The lessons are
   self-assessment records that no leg reads. These are not gate candidates, but no leg records an exemption for them.
5. `round25-holds/battery.sh`, `round25-sources-census.sh` — out of set, named only in evidence/README.md:1083.
   Historical; exempt them explicitly.
None of these is a predicate change. They are scope notes for the named-limit line and the lesson.

## Smallest safe correction (no change to predicate, counter, floor or target)

- Fix SKILL.md:100: escape the pipes in `` `WITNESS=pass\|fail\|unparseable\|timeout …` `` so `exit` lands in cell 3.
  This is a real rendered-table defect.
- Register the 7 never-rowed paths plus `round26-registry-oracle.py` (in an entry cell, with a real verdict map).
- For SKILL.md:114, rewrite the `\|` alternatives (e.g. `c1/c2/c3/holds/all`). Record in the lesson that this
  satisfies a parser limitation of the frozen counter (escaped pipes). It is not a registry defect.
- base-gate-r38/39/41.sh: do NOT relabel them as gate entries. If the counter forces this, put them in a
  `kind=control` row whose entry says "control base gate, not a gate". Name this the claims.md:98 limit in action.

## Recommended SCORECARD wording (C2 row)

> C2 calibration (tag: plumbing) — gate registry vs the round-46 self-assessment "every verifier the verdicts
> name is registered" (SCORECARD.md:2460). Frozen counter `MISMATCHES` 25 → [after]. Of the 25, 8 were real
> self-assessment mismatches: 7 executables that QUALITY/SKILL name or an entry point runs were in no Gates row,
> and 1 row (SKILL.md:100) lost its exit map to unescaped pipes. The other 17 do not measure calibration:
> 10 were the counter's escaped-pipe split at SKILL.md:114, 3 are this round's own new counters, 3 are control
> base-gates and 1 is a counter placement. The "dependence" leg is a mention closure: it counts docstring and
> comment literals and misses `$VAR/`-composed calls (round26-registry-oracle.py). Row truth and the
> gate-vs-control distinction remain a reader's check. **Calibration: improved narrowly (8 real mismatches closed).**

Score impact: do not give calibration a numeric score from this count. The Axes table has no calibration
row, and ≥10/25 of the count depends on the parser.
