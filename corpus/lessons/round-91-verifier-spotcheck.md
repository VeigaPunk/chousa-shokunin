# Round 91 — verifier spot-check (non-author, hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `chousa` round 91. Report `.ufo/reports/round-91/chousa.md` (fleet commit `10695a56a0d832f28c0da4ebe3d6b8b46a85b67c`, lane identity `chousa-shokunin <chousa@shokunin.local>`). Lane HEAD `406ac4741764ade04eefbee0f3127c453c03420a` (remote `origin/master` identical, `ahead=0`). Base `265b8633b7e5d1da49da6fb948df9707373fb15c`. This judge did not author the round and re-measured each claim's before→after from committed bytes.

## 1. Step-1 conformance

| check | result | evidence |
|---|---|---|
| report committed by lane identity | pass | `git log --format='%an %ae %H' -- .ufo/reports/round-91/chousa.md` → `chousa-shokunin chousa@shokunin.local 10695a56…` (fleet repo) |
| SHONEN heading, one line per box | pass | `## SHONEN` with four `[~]` lines + pointers in report; no `[x]` without verifier (all `~`, honest) |
| cited commits exist + ancestor of branch | pass | `merge-base --is-ancestor` → ancestor for `7b19dd0b`, `4d00d751` (F3), `67954adc` (C3), `0c85c9ac`, `f4f1a116`, `406ac474` vs `refs/heads/master` |
| lane clean + pushed | pass | `jj-lane.sh state` → `branch=master local=406ac474 remote=406ac474 ahead=0`; `status --porcelain` empty; `ls-remote` identical |
| prompt carries template contract | pass | `## 1 MISSION/AXES binding`, `## 2 1–3 claims`, `## 2b Frontier`, `## 3 L2 floor ≥8`, `## 4 Report contract`, `## 5 commit/push scope`, `## 6 Run-15 addendum`; MISSION L2 floor read from `MISSION.md` lines 53–72 |
| marker vs real report | real report | report carries work performed, 6 landed commits cited, before→after table, census, trends, SHONEN; marker rule does not invoke `failed` |
| fleet worktree leftovers | defect (status-neutral) | `.scratch/closure-*-entry.json`, `run15-state.json`, `l0-questions.md`, `__pycache__` modifications present in fleet repo — not this lane's report commit; left for orchestrator sweep, does not bar admission |

Verdict: step-1 conformance pass; one status-neutral fleet-side leftovers defect recorded for routing.

## 2. Pre-file falsification ledger (Amendment 59)

`python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 91` → `PREFILE-FALSIFICATION: pass claims=3 rows=34 attack_seats=8 findings=0`, exit `0` (re-run at closure; matches report §Prefile falsification).

- Covers every claim in `chousa-shokunin/.ufo/waves/round-91/claims.json` (C1, C2, C3).
- Reads all eight attack seats: `R91ReviewerC1/C2/C3`, `R91CriticClaims`, `R91ExecMutations`, `R91SentinelScope`, `R91ConnectorSiblings`, `R91RevPrior` — each artifact resolves under `.ufo/waves/round-91/w1/`.
- Ledger `claim-falsification.tsv` has 34 data rows (17 `falsifies-wording`, rest `neutral`/`falsifies-number`); each `falsifies-wording` row names its Amendment in `plans/round-91.md` (Amendments 1–24 across C1–C3).
- No failing row — nothing to adjudicate as real vs spurious. Ledger not edited.

## 3. Per-claim re-measurement (non-author rerun; gate standard respected)

Gate standard: the lane's instruments are gates, verified as committed evidence — verdicts, tallies, frozen revisions are quoted from re-runs here without executing the sibling's selftest suite as my own (`tools/research-gate.sh --selftest` is the C3 no-harm gate; its 283-case receipt is committed evidence, not re-executed by the judge).

| claim | method | commands (lane root) | observed | reported | verdict |
|---|---|---|---|---|---|
| C1 operability | re-measured | `git diff --quiet F3 -- <instruments pins expected selftest>` exit 0; `git diff --quiet C3 -- controls/receipts` exit 0; `python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --work <scratch> --rev 4d00d7519290569879f853d7122b82a927cda1f3 --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907`; `python3 -B corpus/evidence/round91/control-forgeries-r91.py --work <scratch>` | `CONTROL_DRIVER_R91=PASS` `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6`, `SELF_PIN OK rev=F3 receipts_rev=C3`; forgeries `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` exit 0 | identical (`after/c1-verify.txt`, `after/c1-forgeries.txt` byte-identical to rerun) | verified |
| C2 calibration | re-measured | `python3 -B corpus/evidence/round91/curation-r91.py --root .`; `python3 -B corpus/evidence/round91/curation-r91-controls.py --root . --work <scratch>` | `CURATION_R91=PASS` `LEGS_MEASURED=13/13 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 TFREQ_MAX_DF=3 UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0`; controls `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7` exit 0 | identical (`after/c2-counter.txt`, `after/c2-controls.txt`) | verified |
| C3 freshness | re-measured + committed-evidence gate | `python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt`; `python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root . --work <scratch>` | `SKILL_TALLY_R91=PASS` `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`; controls `OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` exit 0 | identical (`after/c3-counter.txt`, `after/c3-controls.txt`); selftest receipt committed (`controls/selftest-r91.txt`, 283 cases, 0 skipped) | verified |

Before states (committed receipts, not memories): C1 `controls/receipts/c1-before.txt` `PRIOR_ACCEPTED=6/6` on r90 driver; C2 `c2-before.txt` `PRIOR_ACCEPTED=4/4` + `DUPCOUNT_R90=2`; C3 `c3-before.txt` `SKILL_TALLY_R90=PASS` on base prose with `CASE_RANGE_OK=1/2 MISLABELED=6`. Do-nothing control cannot reach any after-state — each before counter accepts what the after counter refuses.

Frozen state: F3 `4d00d751` instruments/pins/expected/selftest byte-identical at landing (`git diff --quiet F3` exit 0); C3 `67954adc` receipts byte-identical. No predicate token, target, or number moved after freeze. Two earlier freeze/carrier pairs (`160b658b`/`d02a950f`, `37831ce8`/`b8fc99a1`) superseded pre-wave and pre-scoring per plan §§Pre-wave freeze repair 1–2 — not violations.

No exploratory claim this round — no `unprovable-but-better` ruling required from the judge.

## 4. No-harm check

`git diff 265b8633..406ac474 -- SCORECARD.md` — adds Round-91 verdict section only (operability/calibration/freshness `improved`, depth/coverage/adjacency `unchanged`); `tools/research-gate.sh` + `tools/gate-records.py` byte-identical at base and landing (`git diff --quiet <base> <landing> -- tools/` exit 0); `corpus/SOURCES.md` diff empty (219 rows); `SKILL.md` diff is exactly the one case-range clause (r39 `bash-pin cases 273–275` + r82 `pin-override cases 276–283, of which bash-pin-override cases 282–283`). No axis harmed.

## 5. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | six forgery classes refused where r90 accepts all six; header-key/pin/self-pin legs re-measured by judge |
| calibration | improved | QSHAPE/SOURCE/TFREQ legs + double-count fix re-measured; four tree forgeries + 7 round-90 regressions refused |
| freshness | improved | case-range re-derived (`282–283` vs prose `276–283`; `bashenv 273–275`); old prose refused, repaired clause passes |
| depth | unchanged | no `corpus/knowledge/` entry; source work is re-open + refused fetch (S221 `curl rc 28`) |
| coverage | unchanged | registry 219 → 219 rows; census exit 0 both ends |
| adjacency | unchanged | connector scan read-only; nothing absorbed |

Admission: every claim verifies, no axis harmed → admitted.

## 6. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S070 re-open (`sha256sum(1)`) | admit [~ short, scored through Gate] | `/usr/share/man/man1/sha256sum.1.gz` (sha256 `93c17dff…` re-measured `sha256sum` identical); decompressed line 11 `Print or check SHA256 (256\-bit) checksums.`; rendered 7-word quote "Print or check SHA256 (256-bit) checksums." | agree | row's anchor (decompressed line 11, rendered form) resolves verbatim to the installed page; tier A for the digest-print/check scope holds; ≤25-word quote verified |
| S001 rev-form Gate record (`tools/research-gate.sh:9010`) | admit | `g gate-records.py verify` semantics; `grep -n RESEARCH_GATE_SELFTEST` → line 9010 `printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n'`; `words=4` | agree | rev-form record verifies at F3; count-word 4 matches four tokens, not the draft 5 |
| S221 attempt | reject (no row) | `refetch.tsv` `28 000`, `grep -c '| S221 |' corpus/SOURCES.md` → 0 | agree | no bytes through capture on 2026-11-08 → no row written is correct; TFREQ grounded in lane's own entries instead |
| S001–S013 path anchor spot | admit | SOURCES.md Paths keep earlier row ids stable after supersession note (S073 `supersedes S070` anchor-only) | agree | append-only discipline holds; no row id reused |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → `chousa ok` exit 0 (re-run by judge); five pre-existing `W04` duplicate-URL warnings (`S051`, `S053`, `S073`, `S074`, `S075`) unchanged. Registry 219 rows confirmed by reviewer count (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → 219).

## 7. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | 219 → 219 rows; no new `knowledge/` entry; S221 refused to fetch, no row |
| quality | improved | three instruments hardened with red-before witnesses re-derived by judge; QUALITY 203–210 mined (8 criteria visible in `corpus/QUALITY.md`) |
| discernment | improved | freeze re-cut twice pre-wave; 24 pre-file amendments, most narrowing to measured behavior; `PREFILE-FALSIFICATION: pass`, 34 rows over all three claims |

## 8. Routed defects (next round)

From `corpus/lessons/round-91.md` §Routed work (lane-owned, already durable in lesson + SCORECARD planned-r92):

1. **operability** — gate `passed` on `EXACT_OK` (strip leading whitespace); pin the executed script (a `script=` column or execute-only-the-pinned-path); make `instrument-pins.txt` self-pinned and refuse duplicated paths (`PIN_DUPLICATE`); resolve `--expected`/`--receipts`/`__file__` against the base they are read from; `--work` with `TMPDIR` default; move Amendment 10's external pre-step into the procedure text; make `emit` require explicit `--receipts`; fresh legs under `bash -c` with scrubbed env.
2. **calibration** — QSHAPE before the shared first-cell filter; pin decision-row width and count per entry; tokenise the `used-by` cell; two-directional `source_link` assertions; correct docstring df numbers (5 and 8 under 24 units).
3. **freshness** — scope both regexes to the Gates-table cell; bind the r82 block range or drop it; pin the historical multiset so a deleted quote changes the verdict; bind exact case names and case count; add selftest receipt to the on-disk pin set; controls accept any landing clause the claim names.
4. **carried debt** — round-74 "source-blind order oracle", QUALITY 173's successful-refused record form, r80 backlog Gate ids.
5. **fleet-side (status-neutral)** — untracked/modified chaff in the fleet worktree (`.scratch/closure-*-entry.json`, `run15-state.json`, `__pycache__`) is not this lane's debt; orchestrator sweep only.

## 9. Dispatch digest (per instructions)

```
2026-11-08T07:53:17-03:00 launch chousa round=91 pgid=952200 driver=hyaku-inline attempt=1
2026-11-08T08:56:33-03:00 complete chousa round=91; hyaku-inline attempt=1
```

Judged by the non-author closure judge; no lane-authored file was edited.
