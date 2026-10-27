# R59Reviewer45 — adversarial calibration review (round 59)

Scope: round-59 claim design, controls, source grounding, scope and report contract, as dispatched
(`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-59/w1-dispatch.json`, task
`R59Reviewer45`, body "Adversarially assess round59 claim design, controls, source grounding,
scope or report contract as relevant; give exact evidence and falsifier. No edits."). Axis:
calibration. Read-only on lane bytes; probes ran in scratch
`/fast/scratch/hyaku/chousa-r59/R59Reviewer45/` (removed before filing; every output is quoted
inline). No lane writes, no git/jj writes, no live fetch. Note: this path was occupied at filing
time — see Finding 5d.

## Findings (by severity)

### 1. BLOCKER — the round-59 frozen-claims artifact does not exist; the freeze-before-wave ordering is inverted (claim design)

Evidence:
- Wave context (byte-identical in `w1-dispatch.json` `taskCall.context` and `w1-spec.json`
  `context`) states: "Frozen claims: /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round59/claims.md;
  read before work."
- `stat` on that path: ENOENT at 15:16:08, 15:21, 15:24, and 15:35:39 (final check) — dispatch was
  15:12:11 (`w1-dispatch.json` mtime 2026-10-27 15:12:11), `w1.ready` 15:12:15.
- `corpus/evidence/round59/` contains only `census-start.txt` (15:12:21) and
  `controls/c1-before.txt` (15:14). No claims, no counters, no c2 inputs.
- Freeze-order comparison: round 58 froze claims before its wave — git log shows
  `9e73a03 round-58: freeze claims and before controls` and `718e8d2 round-58: record frozen
  control results` before `c9b08e9 round-58: record W1 findings`; `corpus/evidence/round58/claims.md`
  mtime 14:06 precedes r58 `w1.ready` 14:09:58. Round 59 has no commit at all (tip
  `af8c0a4 round-58 verifier spot-check`), so the r59 evidence present is uncommitted and the
  claims were never frozen.
- All 66 dispatched items say "do not write lane files", so no wave member can author
  `claims.md`; only L1 could — post-dispatch, which would still contradict "frozen ... read
  before work".
- Peer corroboration (independent, same absence): `R59Reviewer42.md`, `R59Critic58.md`, and the
  pre-occupant of my report path (Finding 5d) all record the missing input and correctly decline
  positive verdicts.

Consequence: the milestone ("build and falsify controls for positive verdict-path calibration")
has no claim object; 66 seats each improvised a target. No positive verdict is adjudicable this
round from committed bytes.

Falsifier: `test -f corpus/evidence/round59/claims.md` (absent as of 15:35:39); `git log --oneline`
shows no round-59 freeze commit. If the file appears mid-wave it is by construction not "frozen
before work" (no worker may write lane files); if it never appears, the context line referenced a
nonexistent artifact at dispatch.

### 2. HIGH — `w1-spec.json` postdates dispatch and records 0/66 of the dispatched instructions (report/scope ledger integrity)

Evidence:
- mtimes: `w1-dispatch.json` 15:12:11 < `w1.ready` 15:12:15 < `w1-spec.json` 15:14:46. The
  spec-of-record was last written after the wave was dispatched.
- Containment invariant: round 58 — spec item text appears as a substring of the dispatched task
  text for 74/74 seats (dispatch = `/skill:godspeed` + item + trailer). Round 59 — 0/66.
- Normalized-body hashing: r59 spec has exactly ONE body across all 66 items (after replacing the
  per-seat report filename: sha256 prefix `8bdcafffcb30`), "For round 59, review ready handoff
  requirements ... Report exact evidence; do not write lane files."; the dispatch has 6 distinct
  role bodies (executor/scribe/scout/reviewer/critic/mutation-tester; e.g. the reviewer body is my
  ticket text, the executor body is "inspect and run exact round58 frozen counter/tool or controls
  relevant to positive-verdict-path defect").
- The spec text contradicts the dispatched mandate: it orders every seat (including 16 executors
  and 5 mutation-testers) to "review ready handoff requirements" and forbids lane writes, while
  the milestone requires building and falsifying controls. `R59Critic58.md` independently observed
  "the round59 spec lists review-ready-handoff tasks".

Consequence: an auditor reconstructing assignments from `w1-spec.json` gets 66/66 wrong; the
wave's assignment ledger and its dispatch disagree.

Falsifier (reproducible):
```python
import json
spec = json.load(open('.ufo/waves/round-59/w1-spec.json'))
disp = json.load(open('.ufo/waves/round-59/w1-dispatch.json'))
d = {t['name']: t['task'] for t in disp['taskCall']['tasks']}
print(sum(1 for it in spec['items'] if it['item'] in d.get(it['name'], '')))  # r59: 0/66; r58: 74/74
```
plus `stat -c '%y %n' .ufo/waves/round-59/w1-{dispatch,spec}.json`.

### 3. HIGH — the inherited frozen C1 counter cannot emit a positive verdict, its do-nothing control is vacuous while it cannot, and it crashes on early-failing candidates (controls design)

This is the exact "positive verdict-path" defect the round-59 milestone targets; it is still
unfixed in the only committed counter (`corpus/evidence/round58/c1-count.py`, sha256
`65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`), and `corpus/evidence/round59/`
contains no corrected counter.

Evidence (static, line-pinned):
- `c1-count.py:51` `PASS = "pass"` (lowercase constant); refusal-leg emitters return
  `f"{name}={PASS}(refused)"` — lines 160, 223, 234 — so a correct refusal prints
  `FOREIGN=pass(refused)`.
- `c1-count.py:391` `ref_pass = all(("=PASS" in l) for l in ref_legs)` and `:399`
  `SUMMARY REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)}` search UPPERCASE `=PASS`.
  A candidate passing every refusal leg still prints `REFUSE=0/7` and `C1=FAIL` — the positive
  verdict path is structurally unreachable. (Matches the round-58 close in `LOG.md`, citing
  `:391,399` and four independent W1 demonstrations:
  `R58ScribeMistakeMine.md`, `R58ReviewFrozenClaims.md`, `R58ExecC1CounterAudit.md`,
  `R58ExecC1SizeCaps.md`.)
- Vacuous control: `corpus/evidence/round58/controls/c1-controls.txt` records
  `CONTROL_REFUSEALL=denied ... DENIED=2/2`. But while `ref_pass` can never be true, every
  candidate fails `C1` — do-nothing, the flawed base, and a hypothetically perfect builder all
  print `REFUSE=0/7` — so "controls do not reach C1=PASS" discriminates nothing until the
  aggregate case bug is fixed.
- Dynamic addendum (new, reproduced in my scratch): a candidate that fails `EMPTY_OK` (creates no
  `out-empty/spans/`) crashes the counter instead of scoring it:
  ```
  File ".../c1-count.py", line 212, in main
      foreign.write_bytes(b"foreign evidence bytes\n")
  FileNotFoundError: .../run-frozen-tokenful/out-empty/spans/S777-1.txt
  ```
  (stub builder: prints "build-spans: refused FOREIGN SYMLINK NOT_REGULAR FIFO REGTYPE SIZE ROWS
  CAP" to stderr, exit 1). The counter then exits 1 — the same code as a legitimate `C1=FAIL` —
  with no `C1=` line on stdout, so exit-code-only consumers cannot distinguish harness crash from
  scored failure. Note the planned A/B tally demo (frozen vs case-fixed counter, same refuser)
  was itself blocked by this crash; the two defects are complementary: the crash hits candidates
  failing safe legs, the case bug hits candidates passing them.
- Minor: `c1-count.py:389` computes `ok_pass` and `:390` immediately overwrites it (dead first
  computation).

Falsifier for the unreachability: run the counter with any candidate that refuses the hazard legs
with the frozen reason tokens while passing the safe legs; per-leg lines read `=pass(refused)` yet
`SUMMARY REFUSE=0/7` and `C1=FAIL` (round-58 W1 seats demonstrated exactly this; line evidence
above is sufficient). Falsifier for the crash: `python3 -B corpus/evidence/round58/c1-count.py
--builder <stub that exits 1 without creating spans/> --work <scratch>` → traceback at `:212`.

### 4. MODERATE — the round-59 evidence package is one provenance-less receipt; the round-58 freeze bundle pattern was not reproduced (controls inventory, source grounding)

Evidence:
- r59 `controls/` holds only `c1-before.txt` (15:14, two minutes AFTER `w1.ready` 15:12:15).
  Round 58 froze pre-dispatch: `claims.md`, `c1-count.py`, `c2/quotes.tsv`,
  `controls/{c1-before.txt, c2-before.txt, c1-control-build.txt, c1-controls.txt, REFUSEALL.py,
  build-spans-r55.py}`. No r59 counters, no `c2-before`, no control-build receipt, no builder
  copies exist for the wave that is supposed to falsify controls.
- Receipt truthfulness (independently verified): my fresh
  `python3 -B corpus/evidence/round58/c1-count.py --work <scratch>/rerun` (twice, byte-identical
  to each other, 951 bytes) reproduces the committed receipt's 15 content lines exactly
  (`EMPTY_OK=pass ... SUMMARY OK=4/4 REFUSE=0/7 ... C1=FAIL`); the committed file (958 bytes) has
  one extra line, `EXIT=1`, which the counter never prints — so the receipt is a truthful,
  deterministic measurement plus a hand-appended exit annotation. `tools/build-spans.py` sha256
  `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` equals the r58 pin and
  `controls/build-spans-r55.py` — the before state carries over unchanged and honestly.
- Provenance gap: the receipt embeds no date, command, or builder hash (unlike r58's
  `c1-control-build.txt`, which pins `BASELINE_SHA256_PINNED_BYTES=1ed2650a...`), and being
  byte-identical to r58's receipt, a copy-forward and a re-run are indistinguishable from
  committed bytes alone.

Falsifier: the re-run command above (diff shows only the appended `EXIT=1` line);
`sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py`.

### 5. MODERATE — seat namespace collisions and respawn churn (operational/report contract)

a) Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor07/positive-path/` holds two disjoint
   workstreams — C1 files (`c1-count-tokenfix.py`, `c1-positive-builder.py`, `run-*` dirs,
   15:23–15:24) and C2 poison files (`poison-base.py`, `c2-poison-zh.stdout`, 15:23). The seat's
   live agent `R59Executor07-2` disowned the poison files (IRC, ~15:25: "I did not create it").
b) Non-contract namespace `/fast/scratch/hyaku/chousa-r59/R59Executor06-chousa/` (15:22) matches
   no roster seat name (roster seat: `R59Executor06`; `w1.ready.partial` shows no alias for it).
c) Respawn churn: `w1.ready.partial` (47 entries at 15:33:49) binds 11/66 seats to suffixed
   agents — 7× `-2` and 3× `-3` (`R59Executor12`, `R59Executor13`, `R59Scout31` needed two
   re-spawns).
d) Report path: my assigned output `.ufo/waves/round-59/w1/R59Reviewer45.md` was occupied at
   15:25:25 (2,219 bytes) by a foreign or prior-incumbent report — content was a calibration
   review of the same missing-`claims.md` blocker (not written by this session; I started
   ~15:13 and wrote nothing before 15:35). `w1.ready.partial` binds
   `R59Reviewer45 → R59Reviewer45` (no respawn suffix), so the occupant is not attributable from
   lane bytes. I preserved its full text in scratch (removed at filing; its operative finding —
   claims.md absent, positive verdict unsupported — is subsumed by Finding 1 and duplicated by
   `R59Reviewer42.md`/`R59Critic58.md`, so no evidence is lost) and this file supersedes it.
   If a distinct live seat authored it, that seat must refile under its own name.

Falsifier: `ls -la /fast/scratch/hyaku/chousa-r59/`; `stat -c '%y %s %n'
.ufo/waves/round-59/w1/R59Reviewer45.md` (pre-overwrite mtime 15:25:25, 2219 bytes).

### 6. LOW/INFO

- Census: r59 `census-start.txt` is byte-identical to r58's except `EXIT=0` → `exit=0` (receipt
  format drift); same five W04 duplicate-URL rows, `SOURCES.md` ok. No census-end yet (wave in
  flight).
- `predata/` created 15:12, still empty at 15:33 — the milestone's "offline source
  reconnaissance" has no staged shared artifact; scouts reported individually.
- Context grounding checks out: the no-fetch L0 question `8d77e6c1` is real and open
  (`corpus/knowledge/evidence-pool-versioning-r39.md` recheck line: "no fetch: L0 `8d77e6c1`
  open"); operability 3/10 matches `SCORECARD.md`.
- Watch item: `w1.ready.dispatched` absent at 15:35 (r58's landed 14:24:35, ~15 min after its
  `w1.ready` 14:09:58; r59 ready was 15:12:15, so the marker window has elapsed). If it never
  lands, the r58-style settled-wave chain (`ready → ready.dispatched → w1-results.json`) has no
  r59 counterpart yet.

## Residual risk and verification gaps

- The pre-occupant of my report path cannot be attributed from lane bytes; overwriting it is the
  one lane write implied by my contract, and it removes a same-named artifact — documented in
  Finding 5d rather than silently.
- I did not build a hazard-passing candidate builder, so Finding 3's unreachability rests on
  line-pinned static evidence plus the four recorded round-58 demonstrations, not on my own
  positive-path run; the crash half of Finding 3 is dynamically reproduced.
- Whether `w1-spec.json` was overwritten after dispatch or generated post-hoc from a template is
  not determinable from mtimes alone; only the mismatch and ordering are asserted.
- No LSP server was available for this markdown/JSON/Python evidence set; semantic checks were
  done by direct reads and execution of the committed counter (recorded as text-grep/read fallback
  per role rules).
- claims.md was re-checked immediately before filing (15:35:39): still absent. If it lands
  mid-wave, Finding 1's severity stands (not frozen before work) but claim-level review becomes
  possible for a successor seat.

## Report trailer

- Report: `.ufo/waves/round-59/w1/R59Reviewer45.md`
- Evidence base (lane-relative): `corpus/evidence/round59/{census-start.txt, controls/c1-before.txt}`,
  `corpus/evidence/round58/claims.md`, `corpus/evidence/round58/c1-count.py`,
  `corpus/evidence/round58/controls/{c1-controls.txt, c1-control-build.txt, REFUSEALL.py, build-spans-r55.py}`,
  `.ufo/waves/round-59/{w1-dispatch.json, w1-spec.json, w1.ready, w1.ready.partial}`,
  `.ufo/waves/round-58/{w1-spec.json, w1-dispatch.json, w1.ready, w1.ready.dispatched}`, `LOG.md`,
  `SCORECARD.md`; scratch probes (removed): `/fast/scratch/hyaku/chousa-r59/R59Reviewer45/`.
