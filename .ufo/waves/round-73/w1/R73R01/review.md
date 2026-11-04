# R73R01 — adversarial review of the round-73 frozen artifacts

Seat: R73R01 (attack role, leaf). Scope: (a) predicate identity across r71/r72/r73 claims, (b) the frozen C2
counter, (c) re-derivability of claims.md over committed bytes, (d) the C1 counting-command surface.
Reviewed at: freeze commit A `a0f094c272dcb09f1bf79e2c9057d7ea20b7ac7b` (lane HEAD), base
`f748abbb6bf58388e732facd4ecec5612419c457` (parent; the r72 spot-check tip). Verified by `git log`/`git
diff-tree` that A's parent is the base and A carries exactly the five frozen paths (census-start.txt,
SCORECARD.md, c2-count.py, claims.md, before-r73-greps.txt, probe-r73-sizing.txt). All citations are to
committed bytes at A unless marked untracked. Demos cited below live in `demos/` beside this file.

## Commands run (my own receipts)

- `python3 -B corpus/evidence/round73/c2-count.py --selftest` → `SELFTEST=PASS mutations=7/7`, rc **0**.
- `python3 -B corpus/evidence/round73/c2-count.py --lane /home/vgpnk/Projects/shokunin/chousa-shokunin --rev
  f748abbb…457 --base f748abbb…457` → `CHECK C2-1..C2-5 FAIL`, `CHECK C2-6 PASS`, `CHECK C2-7 PASS`,
  `C2=FAIL checks=2/7`, rc **1** — byte-identical to the frozen control's recorded run
  (corpus/evidence/round73/controls/before-r73-greps.txt, final block). C2-6/C2-7 pass **vacuously** at the
  base (nothing removed, receipts untouched) — a do-nothing round scores exactly 2/7, as the control claims.
- V72-2 arithmetic re-run: `git show 6dd6c82…:SCORECARD.md | grep -c "18 healthy"` → 3; `git show
  7f7ea19a…:SCORECARD.md | grep -c "18 healthy"` → 2 (demos/demoE-tree-reruns.log).
- No tools installed; no lane mutations; the two counter commands and read-only git are the only execution.

## (a) Predicate identity — side by side

**r71** (corpus/evidence/round71/claims.md:64-72):

> Verdict rule, frozen before measurement: battery completes with verdict line (anchored count 1) + preflight
> completes with `SKIPPED=none` → C1 improved ON THAT PREDICATE (…the gate's red state is disclosed everywhere
> it is cited and the operability SCORE remains its historical 3/10…); if the bounded battery still dies before
> its verdict line, or the preflight cannot complete within its budget, C1 lands honest-stop again with the red
> receipts committed as the defect record and the residual routed (the remaining arm would be the by-name skip
> with its coverage cost, or the operator's flock decision); no predicate is edited after measurement.

**r72** (corpus/evidence/round72/claims.md:7):

> battery completes with verdict line (anchored `^RESEARCH_GATE_SELFTEST:` count 1) + preflight completes with
> `SKIPPED=none` → improved ON THAT PREDICATE, with the gate's red disclosed everywhere it is cited and the
> operability score unmoved; if the bounded battery still dies before its verdict line, or the preflight cannot
> complete within its budget → honest-stop again, receipts committed as the defect record and the residual
> routed. No predicate is edited after measurement.

**r73** (corpus/evidence/round73/claims.md:38-44):

> The rule, **carried unchanged from the r70/r71/r72 claims files**: **battery completes with its verdict line
> (anchored `^RESEARCH_GATE_SELFTEST:` count 1) + preflight completes with `SKIPPED=none` (its G08 line naming
> its real result) → improved ON THAT PREDICATE**, with the gate's actual result (PASS or FAIL, and the
> ok/FAIL/skip case tallies) disclosed everywhere the predicate is cited and the operability score unmoved; if
> the bounded battery still dies before its verdict line, or the preflight cannot complete within its budget →
> honest-stop again, receipts committed as the defect record and the residual routed. No predicate is edited
> after measurement, and no measured FAIL is reported as a pass.

Drift analysis → **F7** below. Completing arm: semantically identical across all three (anchored count 1 +
SKIPPED=none). Honest-stop arm: identical r72→r73; r71 additionally named the residual arms (by-name skip /
operator flock decision), dropped since r72 — pre-existing, not introduced by r73.

## (b) Counter review — c2-count.py, seven checks

Structure: PATHS c2-count.py:52; RECEIPTS :53-56; heading/phrase literals :56-62; check() :90-118; load()
:125-134 (git show at `--rev` for the three files :126; numstat base→rev :128-131; name-only base→rev over the
two receipts :132-133). Every check binds **on committed bytes alone** (git show / git diff against explicit
revs); nothing reads the working tree, so the counter can neither be gamed by nor score uncommitted state.

| check | do-nothing at base | binds committed bytes | smallest text satisfying it without a real correction |
|---|---|---|---|
| C2-1 | FAIL (count 0) | yes | append one exact line `## Round 72 correction entry` to LOG.md |
| C2-2 | FAIL | yes | under that heading, one line containing `8426`, `8435`, `exempt` — order and roles free (→ F3) |
| C2-3 | FAIL | yes | append heading `## Correction — round-72 spot-check` (the U+2014 em dash must match; ASCII hyphen fails — a real binding) + one line containing `V72-1 V72-2 8426 8435 7f7ea19a 6dd6c82` |
| C2-4 | FAIL | yes | append `## Round 72 correction note` + a line `V72-1 V72-2` |
| C2-5 | FAIL | yes | same last lesson section contains the three frozen phrases; one line suffices |
| C2-6 | PASS (vacuous) | yes | nothing to do — pure appends never violate; a binary-marked diff evades it entirely (→ F9) |
| C2-7 | PASS (vacuous) | yes | touch nothing — but only 2 receipt paths are protected (→ F8) |

**Net: ~3 appended keyword-salad lines across the three PATHS files score C2=PASS 7/7 with no correction
content, no citation and no receipt** — demonstrated through the counter's own pure check():
demos/demoCD-counter-bypass.log (`KEYWORD-SALAD` block, all seven PASS).

What the counter does bind well (stated for balance): single-instance anchored headings (any second
rstrip-equal heading line — including a quotation at column 0 — fails C2-1/C2-3/C2-4); LAST-section scoping
(section() takes the last exact heading, c2-count.py:66-75); exact tree-phrase co-presence (C2-5); deletion
freedom (C2-6); two-receipt immutability (C2-7); the mutation selftest genuinely kills one mutation per check
(7/7 observed). The em-dash heading and the 40-hex tree hashes embedded in required phrases are hard-to-hit
literals. The counter's weakness is not per-check forgery of a single field; it is that no check binds **truth
or roles**, only token presence (F3, F8).

### Findings

**F3 (HIGH, attacks C2-2/C2-3/C2-5 role-binding).** The checks are substring-presence only (missing(),
c2-count.py:100-102; LESSON_NAMES :57; TREE_PHRASES :58-62). An entry asserting the **inverted** calibration —
"the unguarded assignment at tools/research-gate.sh:8426 exits; the grep at :8435 is set-e-exempt" — scores
C2=PASS 7/7 (demos/demoCD-counter-bypass.log, `INVERTED-ROLES` block). Ground truth: tools/research-gate.sh:8426
is the grep inside the `&&` list (`grep -q '^GATE_GREP: ' -- "$WORK/r36-pin.txt" && p36_ok=0`, set-e-exempt as
a non-final list member), :8435 is the bare assignment `p36_out=$(bash "$SELF" --pin …)` whose failure exits;
confirmed by my read of :8414-8448 and by the routed source (corpus/lessons/round-72-verifier-spotcheck.md:90,
§6 V72-1). Smallest binding: freeze the corrected sentences as exact literals the way C2-5 freezes tree phrases
(e.g. require "grep" within the same line as "8426" and "exempt", and "8435" with "rc=2"/"exits"), or quote the
full corrected sentence as a frozen phrase pair.

**F8 (MEDIUM, attacks C2-7 vs the claim's own status-neutrality sentence).** claims.md:72-73 promises "the r72
verdicts, predicates and receipt bytes stay undisturbed", but C2-7 diffs exactly two paths (c2-count.py:53-56,
:132-133). corpus/evidence/round72/claims.md (the r72 predicate bytes), before-r72-greps.txt,
after-r72-corrections.txt, probe-r72-sizing.txt and the LOG/SCORECARD r72 verdict rows are all mutable with C2
still 7/7. Smallest binding: extend C2-7 to `git diff --name-only <base> <rev> -- corpus/evidence/round72/` →
empty (and optionally the r72 verdict rows in LOG/SCORECARD).

**F9 (LOW, attacks C2-6).** load() scores numstat adds with `int(parts[0]) if parts[0].isdigit() else 0`
(c2-count.py:131); git prints `-` for binary-marked diffs, so a diff containing a NUL byte evades C2-6 with
lines removed. Exotic but real; a `parts[0] == "-"` guard would close it.

## (c) Re-derivability of claims.md over committed bytes

Sentences a closure **can** re-derive with one command (verified): the case-258 body "22.58 s, rc 0,
RESEARCH_GATE: CLEAN" (probe-r73-sizing.txt); the ~40x arithmetic (900/22.58); every before-control count
(before-r73-greps.txt states tree + commands); the in-tree gate sha256 at base (control, "byte identity"
block); the V72-2 3-vs-2 arithmetic (re-run, demo E); the G08 7200 s default (tools/lane-preflight.py:268).

Sentences/counts that **cannot** be so re-derived:

**F4 (HIGH, attacks claims.md:14 and :48).** "PREFLIGHT=7/7 … **in 1.79 s**" / "G01–G07 measured **1.79 s**" —
no committed byte carries this number. The probe receipt's preflight block contains no elapsed line (its only
timing is `ELAPSED=22.58 rc_child=0` for the case-258 body); a corpus-wide `grep "1\.79"` matches claims.md
itself plus unrelated round-27–32 artifacts; within corpus/evidence/round73/ excluding claims.md: zero hits
(demos/demoE-tree-reruns.log, rc 1). This is the round's own V72-2 class — a count whose re-derivation context
(receipt) is missing — inside the freeze that imposes that standard on r72 (claims.md:87-89). Smallest fix: the
probe receipt carries the elapsed reading.

**F5 (MEDIUM, attacks the whole sizing probe).** probe-r73-sizing.txt records **no git revision and no
instrument digest** anywhere — no `git rev-parse`/`sha256sum` line. The tree of its 22.58 s, rc 0, and
PREFLIGHT=7/7 counts is unstated, and the pre-freeze working tree is unreconstructable (6 dirty paths exist at
review time). before-r73-greps.txt pins the gate digest only at the base tip, not at the probe moment. Smallest
binding: header lines `git rev-parse HEAD` + `sha256sum tools/research-gate.sh` in the probe (the D-70 lesson:
a count line's tree is part of its context — claims.md:87-89).

**F6 (MEDIUM, attacks claims.md:17-18 and :71-72).** "S180 admitted, S181 rejected" / "opened this round as
S180": corpus/SOURCES.md at commit A contains **zero** S180/S181 rows (`git show a0f094c:corpus/SOURCES.md |
grep -c "S180\|S181"` → 0, rc 1 — demo E; registry 179 at base per the control). The claims' cited ground does
not exist in committed bytes at the freeze; it becomes derivable only if the closure itself lands those rows —
the closure cites its own future output. The lesson path cited alongside does exist
(corpus/lessons/round-72-verifier-spotcheck.md §6, :88-91, verified). Smallest fix: land the rows in the freeze
commit or cite the lesson path alone.

**F10 (LOW, attacks claims.md:35-36).** "the r71 landing blob": no claims file or control names the r71 landing
commit id; before-r73-greps.txt pins only the working-tree sha256 at base. Re-deriving "d5d48128… = the r71
landing blob" requires multi-command git archaeology (find the r71-era commit touching
tools/research-gate.sh, then show|sha256sum), not one command. Smallest fix: name the r71 landing commit id in
the control.

**F11 (LOW, attacks claims.md:18-20).** Wave facts (11 seats, band 8–16, `.ufo/waves/round-73/w1.ready`) ground
only in untracked files (`git status`: `?? .ufo/waves/round-73/w1.ready`, `w1-spec.json`, `w1-dispatch.json`) —
not re-derivable over committed bytes at the freeze.

**F12 (LOW, precedent, attacks the command family's form).** r71 claims.md:76-77 name
`corpus/evidence/round71/controls/after-battery-completes-r71.txt` and `after-full-preflight-r71.txt` as
paste-able counting commands with expected counts 1/1; **neither file exists** (ls corpus/evidence/round71/controls/
— 7 files, neither present). r71 honest-stopped and the receipts never landed; nothing in the command form
detects a named-but-never-produced receipt. The r73 commands (claims.md:64-66) share this form.

## (d) The C1 counting commands — satisfiability without the real instrument

The three commands (claims.md:64-66): anchored verdict count 1 over `controls/battery-r73.txt`; unanchored
`SKIPPED=none` count 1 and anchored `^PREFLIGHT=` count 1 over `controls/preflight-r73.txt`. Method discipline
(claims.md:51-55) promises receipts whose first header names the measured revision and unset budgets and whose
headers never begin with the verdict token — **no counting command checks any of that**; claims.md:59 excludes
only "the r72 bytes".

**Grep 1 (`^RESEARCH_GATE_SELFTEST:` = 1) — satisfiable by a receipt the round-73 instrument did not produce:
YES, without hand-writing anything.** 35 committed files under corpus/evidence/ carry exactly one anchored
verdict line (r13–r25 era receipts, 85–161 cases). Demo A: copying
`corpus/evidence/round25-holds/holds/selftest.log` to the battery-r73 name gives anchored count **1**, rc 0
(demos/demoA-grep1-relocated.log) — genuinely instrument-produced bytes, wrong run, wrong era, wrong case count
(136 vs the canonical 275, LOG.md:2134). A hand-written one-liner (`RESEARCH_GATE_SELFTEST: PASS (275 cases)`,
the exact printf shape at tools/research-gate.sh:8746/:8749) also satisfies. Smallest binding: one added
command — `grep -c '^ok-case\|^FAIL-case\|^skip-case' …/battery-r73.txt` → 275 — which kills every relocated
receipt (85–161, or the r72 partial's 260, before-r73-greps.txt:8) and every hand-written one-liner (0); or a
verdict-shape grep pinned to the :8746/:8749 formats.

**Greps 2+3 (`SKIPPED=none` = 1, `^PREFLIGHT=` = 1) — satisfiable by a receipt the real instrument did not
produce: YES, in the instrument's own summary format for a FAILING run.** lane-preflight.py:9/:327 print
`SKIPPED=none` whenever nothing was skipped, orthogonal to FAILED. Demo B1: a two-line file whose only content
is `PREFLIGHT=1/8 FAILED=G01,…,G08 ENV=none SKIPPED=none` scores 1 and 1 — an all-gates-FAILED preflight
reaches C1's counting commands. Demo B2: a header that merely narrates "the SKIPPED=none state" scores 1 with
**zero preflight output** — the D-70-2 unanchored-quote class; the claims' header rule (claims.md:53-54) guards
only the verdict token, not `SKIPPED=none`. Smallest binding: replace greps 2+3 with one full-line grep
`^PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none$` (the exact :327 emission for a full passing run), plus a
header-revision binding (`head -1 | grep -c <landing-tip>` → 1) to pin the receipt to the measured revision the
claims already promise.

Both smallest bindings are single added grep commands in the same block; none is applied here (finding only,
per assignment).

## Residual risk and verification gaps

- The untracked `corpus/evidence/round73/controls/battery-r73.txt` / `preflight-r73.txt` exist in the working
  tree at review time (the L1's in-flight single-writer C1 run). I deliberately did not read or score them: my
  item is the frozen command surface, and the findings above apply to whatever bytes land. If the L1 wants
  F1/F2 mooted, the two added greps in (d) are the cheap closure.
- The manifest critical-section claim (claims.md:4-6, "lines 3970–3981 runs instead of failing closed") is
  verified at the byte level (flock guard inside that range) and behaviorally via the probe's `flock -n … rc
  0`, but the section was not executed — no gate run beyond my item's two counter commands.
- No LSP server answers for .sh/.py in this environment; all checks are byte-level greps and direct command
  runs. Every finding here is a byte/count claim, so text-level verification is the appropriate standard; grep
  unavailability of semantics is recorded, not presented as proof.
- corpus/QUALITY.md is dirty (the L1's in-flight edit); not reviewed, out of my item scope.

## Scratch

/fast/scratch/hyaku/chousa-r73/w1/R73R01 — deleted before yield (demo artifacts preserved in demos/ here).
