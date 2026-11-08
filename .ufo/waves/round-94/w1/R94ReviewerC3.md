# R94ReviewerC3 — round-94 C3 (freshness) attack on carrier C

Seat: R94ReviewerC3 (reviewer, leaf). Canonical planner seat, freeze and integration: `ChousaR94` (L1).
Target: frozen C3 sentence in `.ufo/waves/round-94/claims.md` against carrier
`352924bbea624caf3771ef291be98fd4ec679dda` (F `41038ed7c40cffc4cf86d649a6ba433c4b9eec1a` plus the six
control receipts and the 34-row pins table). Base `0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6`.

Scope discipline: leaf only — no task/subagent dispatch, no `agent://all`, no production edits, no lane or
fleet git/jj mutation, no commits. The only lane writes are this file and
`.ufo/waves/round-94/w1/R94ReviewerC3-receipts/`. Scratch
`/fast/scratch/hyaku/chousa-r94/R94ReviewerC3/` was created with `mkdir -p`, used for the `git clone
--shared` + `checkout C` and every fixture work dir, and deleted before yield. No `/tmp` writes, no
network, no sudo, no sysctl, no host service touched. No tool installed or upgraded this round (Python 3
stdlib + coreutils/git only).

Binding (receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-binding.txt`, rc 0 each): `HEAD=C`;
`git rev-parse F` = `41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`; `git merge-base --is-ancestor F HEAD` rc 0;
`git status --porcelain` empty; sha256 `da49d06896bc683ea782a72261021b9890c24c14694a39498315b6b48d8cd880`
`corpus/evidence/round94/skill-tally-r94.py`, `76840a4180c66f36713741f64bb31c283ed505a82e7ee5bda85af14fe66065a6`
`corpus/evidence/round94/skill-tally-r94-controls.py`.
`git diff --stat F C -- SKILL.md tools/research-gate.sh tools/gate-records.py` prints nothing (rc 0);
`SKILL.md` blob `743f3e3f4bb5f929e04deaf04ed14318e9cf4629`, worktree sha256
`dcdf92341b25553ba84fd3f6c0178161fa2f0e6c74c76b8a7cc92bb1f1c789bc` (receipt
`R94ReviewerC3-receipts/R94ReviewerC3-c3-scope.txt`). The selftest capture has 283 `ok-case` lines and
`RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`.

## Predicate reproduction (K1)

CMD: `python3 -B corpus/evidence/round94/skill-tally-r94.py --root . --selftest corpus/evidence/round94/controls/selftest-r94.txt`
(CWD = the carrier clone) — RC=0, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-counter.txt`:

```
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 TAIL_OWNED_OK=2/2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R94=PASS
```

CMD: `python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work <scratch>/controls-final`
— RC=0, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-controls.txt`:

```
CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1
```

Every one of the 13 control cases prints `OK`; the two moved trees are `r93 rc=0 / r94 rc=1`. K1 is met.

Command abbreviations used below — each receipt's own `CMD:` line is the fully expanded form:
`<C>` = `/fast/scratch/hyaku/chousa-r94/R94ReviewerC3/repo/corpus/evidence/round94/skill-tally-r94.py`;
`<selftest>` = `/fast/scratch/hyaku/chousa-r94/R94ReviewerC3/repo/corpus/evidence/round94/controls/selftest-r94.txt`;
`<mut>` = `/fast/scratch/hyaku/chousa-r94/R94ReviewerC3/work/mut`;
`<fx>` = `/fast/scratch/hyaku/chousa-r94/R94ReviewerC3/work/fx`;
`<controls>` = `/fast/scratch/hyaku/chousa-r94/R94ReviewerC3/work/controls`. Every `<fx>`/`<controls>`
`--root` is a scratch SKILL.md copy plus copies of the two grounding receipts; the predicate and controls
runs use `--root .` at the carrier clone.

## The six assigned questions

**(1) Nearest-preceding-heading tracker at the `## Gates` boundary — HOLDS.**
`gates_start` = line 82; the scope terminator is `## Round26 metadata options and resource qualification`
(line 576), so the tail slice starts at that heading (`gates_end` is the preceding `\n`, index 176266 in
the committed file). The first tail lines are a blank line and that heading; no tally can occur before it.
Fixture A2 (215 tally deleted from Round 27 and re-inserted immediately under the first tail heading) —
CMD `python3 -B <C>/corpus/evidence/round94/skill-tally-r94.py --root <fx>/boundary-owner --selftest <selftest>`,
RC=1, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-boundary.txt`:

```
TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=215 cases tally=PASS (215 cases, 0 skipped) owner=## Round26 metadata options and resource qualification declared=Round27 repair/status correction
```

The boundary heading is tracked (no `<none>`, no bleed back into Gates). Fixture A1 (same tally on the
last Gates line, before the terminator) — RC=1, same receipt: `LEG_FAIL OTHERS declared={('161', '0'): 1, ('256', '0'): 1} observed={('256', '0'): 1, ('161', '0'): 1, ('215', '0'): 1}` plus
`TAIL_OWNER_FINDING TAIL_OWNER_COUNT tally=215 observed=0 declared=1` — a last-Gates-line tally is counted
by `others_ok`, not silently treated as tail.

**(2) Can a tally moved inside the Gates scope hide from the owner leg — HOLDS (no hide).**
Fixture B1 (215 line moved into the Gates table as a standalone row) — CMD `... --root <fx>/inside-gates-standalone ...`,
RC=1, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-inside-gates.txt`:
`OTHERS_OK=0` + `LEG_FAIL OTHERS ... observed={('215', '0'): 1, ('256', '0'): 1, ('161', '0'): 1}` and
`TAIL_OWNER_COUNT tally=215 observed=0`. Fixture B2 (215 appended to a current ``| `research-gate` |`` row,
where `current()` is true) — RC=1, same receipt: `STALE_TALLY PASS (215 cases, 0 skipped) != tool 283/0`,
`TALLY_ROWS=9 STALE_TALLIES=1/9`, `LEG_FAIL TALLY`. Both routes are refused.

**(3) Is `TAIL_OWNED_OK` load-bearing — NO for the printed ratio; YES for `owner_codes`.**
`TAIL_OWNED_OK` is printed at line 258 from `owned_ok` (lines 181, 190–191) but the verdict uses
`tail_ok = tail_counts == TAIL_DECLARED and head_ok and not owner_codes` (line 192); `owned_ok` never
enters `passed`. On a copy with `owned_ok` stubbed from the declarations (`owned_ok = len(TAIL_OWNED)`,
owner codes kept), CMD `python3 -B <mut>/m2-stub-ratio-only.py --root <controls>/moved-tail-215 --selftest <selftest>`,
RC=1, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-mutants.txt`, prints
`TAIL_OWNER_MISMATCH ...` with `TAIL_OWNED_OK=2/2 TAIL_OK=0` and `SKILL_TALLY_R94=FAIL`; on the clean tree
the same mutant is RC=0 with the identical frozen line. The frozen controls run against M2 also prints
`CONTROLS=PASS ...` RC=0 (receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-controls-mutants.txt`). So
stubbing the ratio to 2/2 changes **no** verdict anywhere in the frozen battery.
What does carry the force: M1 drops `not owner_codes` from line 192 — the shipped moved-tail-215 tree then
prints `TAIL_OWNED_OK=1/2 ... TAIL_OK=1 LEGS=4/4 SKILL_TALLY_R94=PASS`, RC=0; M3 empties `owner_codes`
(and stubs the ratio) — same tree RC=0. The committed derivation is genuinely observation-based (the
unmutated moved-tail-215 tree prints `TAIL_OWNED_OK=1/2` and RC=1, receipt
`R94ReviewerC3-receipts/R94ReviewerC3-c3-owner-count.txt`), so the claim is true as shipped; the gap is
that the frozen predicate and controls cannot tell a stubbed ratio from the real one.

**(4) Does `TAIL_OWNER_COUNT` fire for a duplicated and a deleted tally — FIRES both.**
Fixture D (215 line duplicated under its own heading) — CMD `... --root <fx>/dup-215 ...`, RC=1, receipt
`R94ReviewerC3-receipts/R94ReviewerC3-c3-owner-count.txt`:
`TAIL_OWNER_FINDING TAIL_OWNER_COUNT tally=215 observed=2 declared=1`. Fixture E (215 line deleted) —
RC=1, same receipt: `TAIL_OWNER_COUNT tally=215 observed=0 declared=1`. The shipped `double-tail-215` tree
repeats observed=2 (same receipt).

**(5) Does `moved-to-heading` prove the substring limit — it proves substring containment, not a move.**
The shipped fixture is a one-line rename: `diff -u <C>/SKILL.md <controls>/moved-to-heading/SKILL.md` shows
`-### Round27 repair/status correction — 2026-10-21` / `+### Round27 repair/status correction — 2026-10-21 (alias)`
and nothing else; the tally stays at line 640 in the same section. CMD `... --root <controls>/moved-to-heading ...`,
RC=0, `TAIL_OWNED_OK=2/2 TAIL_OK=1`, receipt
`R94ReviewerC3-receipts/R94ReviewerC3-c3-moved-to-heading.txt`. It passes specifically because the renamed
heading still contains the declared substring: the alias-negative fixture (owner heading renamed to an
alien heading without the substring) is RC=1 with `TAIL_OWNER_MISMATCH ... declared=Round27 repair/status correction`.
A genuine move of the tally under a *new* heading that contains the declared substring is also accepted
(RC=0, same receipt), so named limit 1 is real for a true move — the shipped fixture simply does not
exercise that move, despite its docstring (`skill-tally-r94-controls.py:20-21`) saying "the `215` tally
moved under a heading that merely CONTAINS the declared owner string".

**(6) Are the two historical owner claims right today — HOLDS.**
Independent derivation (receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-headings.txt`; recognizer
`^#{1,6} ` at column 0): tally `(215,0)` at `SKILL.md:640`, nearest heading `SKILL.md:634`
`### Round27 repair/status correction — 2026-10-21`, which contains the declared
`Round27 repair/status correction`; tally `(283,0)` at `SKILL.md:781`, nearest heading `SKILL.md:758`
`### Round 37 — the claim-pin provenance and the pin-capture environment (2026-10-23)`, which contains
`Round 37 — the claim-pin provenance`. Neither owner claim is wrong. (The fenced shell comment
`# cwd: this lane root...` at `SKILL.md:581` is also treated as a heading; it precedes both owner headings
and owns no declared tally.)

Runtime / identity: one canonical runtime, `python3 -B` (the interpreter does bytecode-free reads only; no
`__pycache__` under the clone — `git status --porcelain` stays empty). The only subprocess in the counter is
the live-mode gate at `skill-tally-r94.py:65-67`, not exercised by the frozen command; the controls invoke
the committed r93 and r94 counters through `sys.executable` for the differential, which is the claim's
design, not a reroute. `resume_continuity_v1` is not applicable: neither C3 instrument has a resume,
continuity or preflight path (`grep -n -i 'resume\|continuity\|preflight'` over both files returns nothing,
rc 1).

## Findings (severity order; no MEDIUM/HIGH; no kill rule fired)

### F1 — LOW — `TAIL_OWNED` coverage is not bound to `TAIL_DECLARED`
Location: `corpus/evidence/round94/skill-tally-r94.py:162` (`TAIL_DECLARED`) and `:166-169` (`TAIL_OWNED`).
The tail verdict requires `tail_counts == TAIL_DECLARED` and checks only the pairs named in `TAIL_OWNED`;
nothing requires the two support sets to be equal. A copy whose `TAIL_DECLARED` gains
`("999","0"): 1` (TAIL_OWNED unchanged), run on a tree with the `999` tally planted under
`### Round 36 — the engine-swap canary and per-record attribution (2026-10-23)`:
CMD `python3 -B <mut>/m5-third-tail-multiset-only.py --root <fx>/third-tail-999 --selftest <selftest>`,
RC=0, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-support-gap.txt`:
`TAIL_TALLIES=3 TAIL_OWNED_OK=2/2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4` + `SKILL_TALLY_R94=PASS`. The `999`
tally has no owner entry and can be moved anywhere in the tail with no finding. Today's tree is not
affected (both tail tallies are declared in both sets), but a maintainer following named limit 4 by adding
only the multiset declaration leaves the new tally owner-blind and the counter green. The reverse
direction fails safe: `TAIL_OWNED` gains `999` without `TAIL_DECLARED` → RC=1 (`LEG_FAIL TAIL`).
Fix: before the loop, assert `{t for t, _c, _o in TAIL_OWNED} == set(TAIL_DECLARED)` and the count
mapping, as a new `TAIL_OWNER_DECL` code; or derive `TAIL_DECLARED` from `TAIL_OWNED`.

### F2 — LOW — heading recognizer is narrower than named limit 2
Location: `corpus/evidence/round94/skill-tally-r94.py:174` (`^#{1,6} ` requires a literal space after the
hashes; the scope terminator at `:93` has the same rule). Named limit 2 says the nearest preceding heading
is "any column-0 `#`…`######` line". A column-0 `###<TAB>Round 36 — ...` inserted between the owner
heading and the 215 tally is not recognized, so the tally keeps the owner heading and passes:
CMD `python3 -B <C>/corpus/evidence/round94/skill-tally-r94.py --root <fx>/tab-heading --selftest <selftest>`,
RC=0, receipt `R94ReviewerC3-receipts/R94ReviewerC3-c3-moved-to-heading.txt` (`TAIL_OWNED_OK=2/2 TAIL_OK=1`,
`SKILL_TALLY_R94=PASS`). No current `SKILL.md` heading uses a tab or bare-`#` form, so this is a latent
boundary only; the finding is that the named limit's wording claims a wider boundary than the code
implements. Fix: `re.match(r"^#{1,6}(?:\s|$)", ln)` in both places, or narrow named limit 2's text.

### F3 — LOW — the `moved-to-heading` control does not move the tally
Location: `corpus/evidence/round94/skill-tally-r94-controls.py:20-21` (docstring) and `:172-173`
(`alias_heading = OWNER215 + " (alias)"`; `text.replace(OWNER215, alias_heading, 1)`). The fixture renames
the owner heading in place; the diff against the landing `SKILL.md` is exactly that one heading line and
the tally stays at line 640. CMD `... --root <controls>/moved-to-heading ...`, RC=0, receipt
`R94ReviewerC3-receipts/R94ReviewerC3-c3-moved-to-heading.txt`. The substring limit itself is confirmed by
a genuine move under a new containing heading (RC=0) and by the alias-negative rename to a non-containing
heading (RC=1), both in the same receipt. Fix: move the line under a *different* heading that contains the
declared string (or rename the case and docstring to say "owner heading contains an alias").

### F4 — LOW — `TAIL_OWNED_OK` is an observation, not a verdict input
Location: `corpus/evidence/round94/skill-tally-r94.py:180-192` and `:258`. The committed ratio is derived
from observed headings (moved-tail-215 → `TAIL_OWNED_OK=1/2`, RC=1), but no verdict consumes it; the force
is `owner_codes` inside `tail_ok` (line 192). A ratio-stub copy (M2) passes the entire frozen battery —
predicate on the clean tree identical, controls `CONTROLS=PASS` RC=0 — while printing `TAIL_OWNED_OK=2/2`
on a moved tree that it still refuses. Evidence: receipts
`R94ReviewerC3-receipts/R94ReviewerC3-c3-mutants.txt` and
`R94ReviewerC3-receipts/R94ReviewerC3-c3-controls-mutants.txt`; the full owner-stub (M3) is caught by the
controls only through the `double-tail-215` needle (`MOVED_REFUSED=0/2`, `DOUBLE_REFUSED=0/1`, RC=1).
This is K4's enforceability gap: the clause "`TAIL_OWNED_OK` computed from the declarations instead of the
observed headings" is checkable only by reading the code. Fix: assert `TAIL_OWNED_OK=1/2` as a second
needle on the `moved-tail-215` control, so a stubbed ratio fails a control.

## Residual risk

- **Fence-unaware tracker.** `SKILL.md:581` (`# cwd: this lane root. All reads remain local; no entry text is
  executed.`, inside a ```sh fence) is recognized as a heading (headings receipt). No declared tally sits
  between it and the next real heading, so no current effect; named limit 2's "any column-0 `#`…`######`
  line" discloses the behavior, but a tally moved between 581 and 616 would be attributed to a shell comment.
- **Literal-space rule** (F2) also applies to the Gates-scope terminator at `:93`: a `##<TAB>…` heading would
  not end the Gates scope.
- **Raw `str.find("## Gates")` at `:89`.** Today the substring occurs once (line 82; no `### Gates`). An
  earlier `### Gates` anywhere would be matched inside that heading and shift the scope; the failure
  direction is false-failure (everything after the fake boundary becomes tail and fires `HIST_SCOPE_BLEED`),
  not silent acceptance.
- **Substring owner match.** `owner in h` accepts any heading containing the declared string anywhere in the
  tail (named limit 1; the genuine-move fixture confirms it for a true move).
- **Tail multiset keyed by `(cases, skipped)`.** Two different tallies with the same pair are
  indistinguishable; today 215/283 are distinct.
- **Live mode not exercised.** The frozen command uses the committed capture; the `--selftest`-omitted path
  (`bash tools/research-gate.sh --selftest`, `:65-67`) was not run. That live binding is r90's, unchanged
  here.

## Verification gaps

- K4's ratio-vacuity clause is only inspectable in code; M2 proves the frozen predicate and controls accept
  a declaration-derived `TAIL_OWNED_OK` (F4).
- `moved-to-heading` does not test a genuine move (F3); my genuine-move and alias-negative fixtures do, but
  they were scratch-only and are represented by the preserved receipt.
- `TAIL_OWNED`/`TAIL_DECLARED` support equality is untested (F1).
- Tab/bare-`#` heading forms were not arbitrated with a CommonMark parser (none installed, no network):
  F2 is a code-versus-named-limit wording mismatch, not a Markdown-validity ruling.
- The fixture driver and mutant sources lived under scratch and were deleted; each receipt preserves the
  exact command, the observed line(s) and the exit code, and the one-line mutations are quoted in F1/F4.

Counter that binds this seat: every finding above names the exact command, the preserved receipt path, the
observed line and the exit code; no unrun check is presented as passed. No kill rule fired: K1 predicate
met at C (rc 0); K2 controls rc 0, positive passing, r93 accepting both moved trees
(`MOVED_PRIOR_ACCEPTED=2/2`); K3 the clean tree's only tail tallies are the two declared pairs under the
declared headings; K4 the committed owner derivation is observation-based (moved tree → `TAIL_OWNED_OK=1/2`,
RC=1; a nonexistent declared owner → RC=1), with F4 as its enforcement gap.

VERDICT: R94ReviewerC3 C3 held — the frozen predicate and controls reproduce exactly at C (both rc 0) and the owner leg refuses both moved-tail trees, but `TAIL_OWNED_OK` is not load-bearing and four low-severity gaps (owner-set support equality, the literal-space heading rule, a non-moving alias control, and the non-load-bearing ratio) are named with receipts.
