# ReviewerC2Set — C2 entry-point set, independent re-derivation (round 46, wave 1)

Item: re-derive C2's entry-point set with my own script (no import of `c2-count.py`),
compare set-for-set with `c2-count.py --list`, then judge which named paths are not gates.
Read-only seat. No installs, no fetch, no lane writes besides this file.

## Method

1. `/tmp/chousa-r46-ReviewerC2Set/rederive.py` — independent walk: `os.listdir(tools/)` for (A);
   `os.scandir` over `corpus/evidence/round*` + regex `^(c[0-9]+-count[\w.-]*\.py|verify-receipts\.py|errata-count\.py)$`
   for (B); a generous `[A-Za-z0-9_./-]+\.(py|sh)` token scan of `SCORECARD.md` and
   `corpus/evidence/round*/claims*.md`, `is_file()`-filtered, for (C).
2. Extracted the counter's own union **without importing it** by pointing it at a SKILL file
   with no Gates section, so every entry point prints:

```
$ python3 corpus/evidence/round46/c2-count.py --root . --skill /tmp/.../no-gates.md --list
72 paths printed          # (then) LC_ALL=C sort; comm -3 counter.txt mine.txt  -> EMPTY
$ comm -3 counter.txt mine.txt ; echo shared=$(comm -12 ... | wc -l)
shared=72                 # 72 vs 72, zero one-sided lines
```

So the counter's set and my independent set are **identical, set-for-set** — collation was the
only initial diff artefact (`sort` dictionary order vs Python codepoint order).

## Derived set (current tree) — `A=8  B=50  C=70  UNION=72`

Matching `ENTRY_POINTS=72 (tools=8 counters=50 named=70)`: `A ⊂ C`, `C∩B=48`,
`B\C = {round31/c2-count-v3.py, round44/errata-count.py}`; no registered path owes credit to a longer token.

## Falsifier 1 — the before-line reproduces, but only with a claims.md that skips its own counters

The receipts name their tree (`controls/c1-before.txt:2`: "`git archive 6e2630a6` … + this round's
counters and fixtures"; `controls/c2-before.txt:2`: "as above"). Measured read-only:

```
bare 6e2630a6                                    → 68 (tools=7 counters=47 named=66) 55/68 UNREGISTERED=13
c2f0e9d as committed                             → 71 (tools=7 counters=50 named=69) 55/71 UNREGISTERED=16
c2f0e9d, three round46 counter names stripped     → 71 (tools=7 counters=50 named=66) 55/71 UNREGISTERED=16
   from claims.md   (same instrument 06c9e9bc)
```
So the quoted 4-tuple is reproducible: at the freeze archive the three counter files exist, so
stripping their *names* from claims.md removes them from leg (C) (`named` 69→66) while leg (B)
still carries the same three files into the union — the union, registered and unregistered legs do
not move. The defect is therefore a **label**, not a baseline: `claims.md:66` should print `named=69`,
and `:40` should not say "base tree" (the bare commit gives 68/13). Real pre-existing debt is 13.

Registration landed while this review ran; the live tree now reads
`ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS`
(`SKILL.md` modified in the worktree). Every other number here is pinned to `HEAD:SKILL.md`
(30 rows, 17 unregistered) plus the instrument blob named below.

## Falsifier 2 — leg (C) is narrower than its frozen sentence

Predicate (C): "every EXISTING repo-relative `*.py`/`*.sh` path that `SCORECARD.md` or a
`corpus/evidence/round*/claims*.md` names". The counter's `NAMED` regex hard-requires a
`tools/` or `corpus/` prefix, and the docstring adds "as a counting command" (not in the frozen
sentence). Literal reading adds 8 existing repo-relative paths, all control artifacts:

```
.ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh   .ufo/waves/round-36/controls/base-gate-r36.sh
.ufo/waves/round-36/controls/ctl-c2-stub-pass.py        .ufo/waves/round-37/controls/base-gate-r37.sh
.ufo/waves/round-38/controls/base-gate-r38.sh           .ufo/waves/round-39/controls/base-gate-r39.sh
.ufo/waves/round-39/controls/mut-gate-path-env.sh       .ufo/waves/round-41/controls/base-gate-r41.sh
```
Two further absolute paths are correctly excluded as not repo-relative (a lane-absolute
`.ufo/waves/round-29/falsify/…/guarded-run.py`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`).
These eight are pinned before-state engine copies and mutants, not lane gates; registering them
would mislead. But the narrowing is undeclared — it belongs in the named limits beside
"row truth is not measured".

## Falsifier 3 — the union is not the committed-gate set

7 committed `corpus/evidence/round*/*.{py,sh}` are outside the union. Four are gate-shaped
verifiers that no leg enumerates (none is named in SCORECARD.md or any `claims*.md`):

- `corpus/evidence/round32/q33-check.py` — explicit `FAIL (exit 1)` contract (docstring).
- `corpus/evidence/round30/rerun-check.py` — audits a stated re-run count against receipts.
- `corpus/evidence/round29/prose-check.py` — lane prose hygiene checker.
- `corpus/evidence/round45/tag-count.py` — QUALITY 64 check **that already has its own Gates
  row** yet is invisible to the counter; delete that row and `UNREGISTERED` stays 0.

So `UNREGISTERED=0 C2=PASS` can coexist with an unregistered committed verifier. The claim's
first sentence ("every committed gate entry point") over-promises relative to legs A/B/C.

## Falsifier 4 — forgeries, pinned by instrument revision

Counts are instrument-dependent, so pin it. The **frozen** instrument (`06c9e9bc`, blob `a222591`,
`p in r`, no fence logic) lets two forgeries through:

```
# fenced 8-pipe row inside ## Gates                     → GATES_ROWS=31 REGISTERED=72/72 UNREGISTERED=0 C2=PASS
# row naming a NONEXISTENT `…/round34/self-audit.pyc`   → GATES_ROWS=31 REGISTERED=56/72 UNREGISTERED=16
```
The current instrument (`60ad448e`, blob `4b30bbe`: fence-aware rows, per-line comment strip,
delimiter-bounded `names()`) refuses both, and keeps the four documented controls refused (prose,
true 7-pipe six-cell row, 8-pipe row without `exit`, row after the next `## `). But a **multi-line**
`<!-- … row … -->` block inside `## Gates` still scores full marks — per-line `re.sub` cannot see
across lines (MutC2Forge's find, reproduced; document pinned to `HEAD:SKILL.md`, base 17):

```
$ python3 …/c2-count.py --root . --skill <HEAD SKILL + multi-line comment>
GATES_ROWS=31 REGISTERED=72/72 UNREGISTERED=0 C2=PASS     exit 0
```
Recording need: the rule changed after seats scored (Admission rule), and `controls/c2-controls.txt`
still lists only the four original classes.

## Judgment — which of the named paths are not gates (do not change the counter)

| path | what it actually is | why a Gates row with a `0`=clean map would mislead |
|---|---|---|
| `corpus/evidence/round30/qr_harness.py` | "loopback harness … (shared by c1-count.py and c2-count.py)" (docstring:1) | a library; its only `sys.exit(2)` is a harness-error path (l.346). It asserts no verdict. |
| `corpus/evidence/round27-mechanisms.py` | "This probe exits0 on successful counting; independent regressions/selftests own verdicts" (docstring:5); payload prints `kind: source-mechanism-probe-not-verdict` (l.38) | always exits 0; SCORECARD:1530-1532 repeats "only a lexical mechanism count, not a behavioral admission gate". |
| `corpus/evidence/round25-measure.sh` | probe; header "Exit 0 means the measurements completed, not claim admission"; SCORECARD:1416 "`round25-measure.sh` is a probe, so exit0 is not a verdict" | same class as `round24-measure.sh`, `round26-measure.sh` ("A probe, not an admission gate: exit 0 only means it ran") and `round25-ledger-recount.py` (exits only on parse error). |
| `corpus/evidence/round33/d2-census.py` | census answering one numeric question; `return 0` unconditionally (tail) | SCORECARD:1859 cites its line as the counting command for a corrected *number*, not a pass/fail. |
| `corpus/evidence/round34/self-audit.py` | "The tool COUNTS, it does not gate: exit is 0 whenever the set was readable, whatever K is" (docstring) | it is D8's named example, so it *must* be registered — but as `kind=counter`, verdict "0 = set readable", never `0`=clean. |

What the counter should not have included: these five **as gates**. Leg (C)'s rule is "named in
SCORECARD/claims", which is not "is a gate"; the counter's own wording ("as a counting command")
would have been the right class but no proximity check implements it. Since the predicate is
frozen, the correct place to absorb this is the `kind`/verdict-map cells — exactly where C2's
declared limit ("row truth is not measured") leaves the pollution unnamed today.

## Verdict

C2's enumeration is faithfully implemented (my independent set is identical, 72/72; the mid-wave
fix touched only row parsing, so the counts stand). Not sound as declared on four counts: the
before-line's `named=66` is not what the committed freeze blob yields (`named=69`), and `:40` calls
the augmented tree the base commit (bare commit: 68 / 13, and 3 of the 16 receipt rows are this
round's own counters); leg (C) drops 10 named paths (8 repo-relative controls, 2 absolute); the
union omits ≥3 gate-shaped committed verifiers plus one already-registered check; and the frozen
instrument admits two forgeries while the current one still admits a multi-line-comment bypass, with
`controls/c2-controls.txt` unchanged. Live target is met: 72/72, `GATES_ROWS=35`, exit 0.

## Residual risk / verification gaps

- Row truth is not measured (declared): five probe/harness paths above will pass with a
  gate-shaped row; only a reader catches it.
- I did not verify the *registered* rows' verdict maps (out of scope; `ReviewGatesSection` owns it).
- `round25-holds/battery.sh` and `round4{5,6}/build-spans.py` are outside the union: instrumentation, not gates.
- Registration landed mid-review (35 rows, 72/72); I did not re-audit the 5 new rows' content —
  their truth is `ReviewGatesSection`'s check, and C2 does not measure it. The multi-line-comment
  bypass above is open at the instrument that produced that PASS.

Cleanup: `/tmp/chousa-r46-ReviewerC2Set/` (scripts, base export, SKILL forgeries) removed.
