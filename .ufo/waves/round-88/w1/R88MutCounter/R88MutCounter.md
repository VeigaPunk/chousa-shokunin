# R88MutCounter — round-88 mutation probe (C1 + C2 + the subject tool)

Lane `chousa`, round 88, wave 1, seat `R88MutCounter` (leaf; no subagents, no production edits, no git mutation).
Base `f484d94f`; landed/freeze bytes attacked `4ea9d008abfd2e09cb51649a42678a78f52ac530`. Every run reads committed
bytes of an archive of the freeze commit; no network was used (no GET).

Subject bytes (verified, `receipts/pinned-bytes.txt`; agree with `instrument-pins.txt`):

| instrument | sha256 |
|---|---|
| `corpus/evidence/round88/gate-records-r88.py` | `f5096b02989c6cbd2ae2ad9a40b108182e60db4af77a4a01077045c14e25beac` |
| `corpus/evidence/round88/curation-r88.py` | `f99ac9b7a6fca3045c675cdb6d8e8b0031243cd8d4e318083e3e64b0b7a24c66` |
| `tools/gate-records.py` | `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60` (identical at `f484d94f`, `receipts/base-tree-diffs.txt`) |

Trees: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive <rev> | tar -x -C <scratch>/trees/{freeze,base}`.
Mutation driver: `.ufo/waves/round-88/w1/R88MutCounter/mutate-r88-ext.py` (sha256
`9a958a0ff440bd4b2263eadc7e3c12df3cc5b286cac96c803151d6f7ad3826c1`); all receipts under
`.ufo/waves/round-88/w1/R88MutCounter/receipts/` (77 files; `receipts/summary.txt` is the machine table,
`receipts/mutant-hashes.txt` the before/after hash table).

Detector (as tasked): **a mutant is killed only when the counter's own frozen predicate stops reporting `PASS`** —
`GATE_RECORDS_R88=PASS` (exit 0) for `gate-records-r88.py` on the untouched freeze tree, `CURATION_R88=PASS`
(exit 0) for `curation-r88.py` on the freeze tree. For subject-tool mutants the pristine round-88 counter is pointed
at the mutant (`--tool`). A baseline failure would be inconclusive; there was none.

## 1. Baselines — the frozen predicates hold at the landed revision

| run | receipt | observed lines | rc |
|---|---|---|---|
| C1 pristine on freeze tree | `receipts/base-c1.txt` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` / `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` / `GATE_RECORDS_R88=PASS` | 0 |
| C2 pristine on freeze tree | `receipts/base-c2.txt` | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `CURATION_R88=PASS` | 0 |

Base-revision controls (same instruments, `--root` = `f484d94f` tree): C1 `GATE_RECORDS_R88=PASS`
(`receipts/base-tree-c1.txt`); C2 `CURATION_R88=FAIL` with `WARRANT_OK=16/17`, `LEG_FAIL WARRANT 16/17` and
`WARRANT_UNLINKED … warrant=Q1, Q3 (S215)` (`receipts/base-tree-c2.txt`) — the freeze's `Q1, Q3 → Q1` entry repair is
load-bearing for the C2 landing verdict, and the freeze tree does print `17/17`.

The six existing `mutate-r88.py` counter shapes were re-run through this seat's executor as a control: all six are
**KILLED** (`receipts/existing-*.txt`), matching `controls/receipts/c1-mutants.txt` (6/6).

## 2. C1 counter — six new one-point mutations plus three joint shapes and two kills

Each is one literal replacement of `gate-records-r88.py`; run on the freeze tree with `--repo`
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. `KILLED` = rc ≠ 0 or verdict ≠ `PASS`.

| id | one point | verdict | mutant output | receipt |
|---|---|---|---|---|
| `N1-D1-pin-drop` | D1 width leg loses `== ROWS_203` | **SURVIVOR** | `…D1_FORGES=3… LEGS=15/15` / `RECONCILED=15/15` / `PASS` | `c1-N1-D1-pin-drop.txt` |
| `N2-CODES-ignore` | `if code in v[1]:` → `if True:` (expected-code match) | **SURVIVOR** | `FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 … LEGS=15/15` / `PASS` | `c1-N2-CODES-ignore.txt` |
| `N3-D1REFUSED-code-lenient` | `d1_refused`/`d2_refused` moved out of the code check | **SURVIVOR** | `D1_REFUSED=3/3 D2_REFUSED=3/3 … LEGS=15/15` / `PASS` | `c1-N3-D1REFUSED-code-lenient.txt` |
| `N4-RECONCILE-ignore` | `if n_ok == got_ok:` → `if True:` | **SURVIVOR** | `RECONCILED=15/15 … LEGS_APPENDED=15` / `PASS` | `c1-N4-RECONCILE-ignore.txt` |
| `N5-MUT-ADMIT-credit` | `mut_admit_killed` drops `accepts == len(d1)` | **SURVIVOR** | `MUT_ADMIT_KILLED=1 … LEGS=15/15` / `PASS` | `c1-N5-MUT-ADMIT-credit.txt` |
| `N6-D2-pin-drop` | D2 width leg loses `== ROWS_203` | **SURVIVOR** | `…D2_FORGES=3… LEGS=15/15` / `PASS` | `c1-N6-D2-pin-drop.txt` |
| `J1-width-pins-drop-both` | both width pins dropped | **SURVIVOR** | `PASS` on freeze; `PASS` on the narrowed probe tree | `c1-J1-…txt`, `probe-P1-J1-pins-both.txt` |
| `J2-width-ok-detached-both` | both width `ok` values replaced by `True` | **SURVIVOR** | `PASS` on freeze; `PASS` on the narrowed probe tree with `RECONCILED=15/15` | `c1-J2-…txt`, `probe-P1-J2-ok-detached.txt` |
| `NAMED-LIMIT-setup-lie` | **joint**: measurement forced false + leg record rewritten to `("SETUP", True, "1/1")` | **SURVIVOR** | `SETUP=0/1 … LEGS=15/15` / `LEG_REREAD=15/15 RECONCILED=15/15` / `GATE_RECORDS_R88=PASS` | `c1-NAMED-LIMIT-setup-lie.txt` |
| `K1-EXPECTED-LEGS-14` | `EXPECTED_LEGS = 14` | KILLED | `LEGS=15/14` / `FAIL` | `c1-K1-EXPECTED-LEGS-14.txt` |
| `K2-DERIVE-NEG-zero` | `derive_neg = 0` | KILLED | `DERIVE_NEG=0` / `FAIL` | `c1-K2-DERIVE-NEG-zero.txt` |

### The named limit in `claims.md` C1 — attacked, and it survives

`claims.md` C1: *“A counter edit that jointly rewrites the leg writer, the receipt files and the reconciliation
survives — that edit is the counter, not a leg misreport.”* I built exactly that edit (`receipts/named-limit-diff.txt`):

```
-            setup_ok = 1 if (p.returncode == 2 and "GATE_RECORDS_ERROR" in p.stderr) else 0
+            setup_ok = 0
...
-                ("SETUP", setup_ok == 1, f"{setup_ok}/1"),
+                ("SETUP", True, "1/1"),
```

The leg tuple feeds `legs`, which feeds the writer (`<work>/legs/<name>.txt`), the receipt re-read, and the
reconciliation's `detail=(\d+)/(\d+)` comparison; writing `1/1` with `ok` makes all three agree on a passing record
whose measurement is false. Observed: `receipts/c1-NAMED-LIMIT-setup-lie.txt` prints
`TOOL=present … SETUP=0/1 … LEGS=15/15`, `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`,
`GATE_RECORDS_R88=PASS` (rc 0), and the written leg receipt says `SETUP=ok detail=1/1`
(`receipts/instrument-SETUP-leg-receipts.txt`). **It survives.** The summary line still exposes the contradiction
(`SETUP=0/1`) that no frozen leg reads; this is the named limit, reported, not argued away.

## 3. C2 counter — eight leg deletions and two kills

Run on the freeze tree. Probe trees are minimal mirrors (registry + the two routed entries, captures symlinked —
`receipts/probe-C2-diffs.txt`); `base` below is the pristine counter on that mirror.

| id | one point | verdict on freeze | probe tree that fires the leg | base on probe | mutant on probe | receipts |
|---|---|---|---|---|---|---|
| `M1-WARRANT-any` | `shares = all(...)` → `any(...)` | **SURVIVOR** `CURATION_R88=PASS` | B1b padding qid (`Q1, Q3`) | `WARRANT_UNLINKED … warrant=Q1, Q3 (S215) resolved=2/2` + `LEG_FAIL WARRANT 16/17`, FAIL | `WARRANT_OK=17/17`, PASS | `c2-M1-…`, `probe-P-B1b-{base,M1}.txt` |
| `M2-FLOOR-qidset-drop` | drops `set(qs) == set(QID_SETS…)` | **SURVIVOR** | caseG relabel (Q10 deleted, Q14 duplicate) | `LEG_FAIL FLOOR … 13/13 floor13`, FAIL | `LEGS=7/7`, PASS | `c2-M2-…`, `probe-P-caseG-{base,M2}.txt` |
| `M3-MIN-TOKENS-1` | `MIN_TOKENS = 7` → `1` | **SURVIVOR** | A1d truncation (`Q11` = `"range"`) | `LEG_FAIL FLOOR … 13/13 floor13`, FAIL | PASS | `c2-M3-…`, `probe-P-A1d-{base,M3}.txt` |
| `M4-FLOOR-floor-drop` | `loc >= fl` → `loc >= 0` | **SURVIVOR** | empty `Q10` quote (12/13 rows) | `LEG_FAIL FLOOR search…=12/12 floor13`, FAIL | PASS | `c2-M4-…`, `probe-P-emptyQ10-{base,M4}.txt` |
| `M5-TEACHES-any-superseder` | disposal via `superseded_by` (non-mined) | **SURVIVOR** | F2 rejected superseder; F2b (S024 and S031 both `rejected`) | `legs=1 unresolved=1` + `LEG_FAIL TEACHES`, FAIL | `TEACHES_UNRESOLVED=0`, PASS | `c2-M5-…`, `probe-P-F2{,-F2b}-{base,M5}.txt` |
| `M6-DEF-CITED-forced` | `DEF_CITED` ok forced `True` | **SURVIVOR** | Q13 quote replaced by Q10’s verbatim text (row Do cell gains `property` so WARRANT survives) | `MODIFIED_DEF_CITED=0` + `LEG_FAIL DEF_CITED 0`, FAIL | PASS | `c2-M6-…`, `probe-P-defcited-{base,M6}.txt` |
| `M7-UNENTAILED-dead` | `unentailed.append(...)` → `pass` | **SURVIVOR** | provenance Never cell gains `modified` | `UNENTAILED_TERM=1` + `LEG_FAIL UNENTAILED … term=modified`, FAIL | PASS | `c2-M7-…`, `probe-P-provmodified-{base,M7}.txt` |
| `M8-SUPERSEDED-dead` | superseded-live check `if False:` | **SURVIVOR** | S021 → `mined`, S032 → `rejected` | `SUPERSEDED_LIVE=1` + `LEG_FAIL SUPERSEDED S021 mined while S032 supersedes it`, FAIL | PASS | `c2-M8-…`, `probe-P-sup-{base,M8}.txt` |
| `K3-EXPECTED-LEGS-6` | `EXPECTED_LEGS = 6` | KILLED (`LEGS=7/6`, FAIL) | — | — | — | `c2-K3-…` |
| `K4-TEACHES-flags-empty` | `teaches_flagged.append` → `pass` | KILLED (`LEG_FAIL TEACHES … flagged=0`, FAIL) | — | — | — | `c2-K4-…` |

Observation (reporting, not a verdict): the `FLOOR` detail string prints only `located/total floorN`, so the A1d
(token-floor) and caseG (qid-set) failures both print `13/13 floor13` while failing — the verdict is right, but the
fired leg’s printed detail does not name which of its three sub-checks failed.

The control battery with each mutant in place of `curation-r88.py` (`receipts/c2-controls-vs-mutants.txt`) catches
only the four whose deleted conjunct a round-87 forgery exercises: `M1` → `CASE_DEVIATION B1b-padding-qid`, `M2` →
`CASE_DEVIATION caseG-relabel`, `M3` → `CASE_DEVIATION A1d-truncate`, `M5` → `CASE_DEVIATION F2-rejected-superseder`
(each `FORGERY_REFUSED=4/5`, `R87_ACCEPTED_FORGERY=5/5`). `M4`, `M6`, `M7` and `M8` leave the controls at
`CONTROLS=PASS` (`FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5`): no frozen forgery exercises the numeric floor, the
`DEF_CITED` citation, the `UNENTAILED` detector or the `SUPERSEDED` detector, so those four deletions pass **both**
the counter’s own predicate and the control battery.

## 4. Subject tool — the three assigned shapes (the unreach shape in two spellings)

Pristine counter, `--tool <mutant>`, on the freeze tree.

| id | edit | verdict | observed | receipt |
|---|---|---|---|---|
| `T1a-unreach-http-203` | `success = … and 200 <= int(kv["http"]) < 300` → `… and kv["http"] == "203"` (drops the derivation literal) | CAUGHT | `MUT_UNREACH_DERIVED=0 MUT_UNREACH_KILLED=0` / `LEG_FAIL MUT_UNREACH derived=0 killed=0` / FAIL | `tool-T1a-unreach-http-203.txt` |
| `T1b-unreach-203-only-literal-kept` | same semantic, literal kept: `… 200 <= int(kv["http"]) < 300 and kv["http"] == "203"` | **SURVIVOR** | `MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 … LEGS=15/15` / `GATE_RECORDS_R88=PASS` | `tool-T1b-unreach-203-only-literal-kept.txt` |
| `T2-admit-int-lt-300` | admit REFETCH `r[6] == "200"` → `int(r[6]) < 300` | CAUGHT | `FORGED_REFUSED=359/362 EXPECTED_CODE=359/362 D1_REFUSED=0/3 MUT_ADMIT_DERIVED=0` / `LEG_FAIL FORGED/CODES/D1_REFUSED/MUT_ADMIT` / FAIL | `tool-T2-admit-int-lt-300.txt` |
| `T3-git-blob-empty-bytes` | `return b.stdout if … else None` → `return b""` | CAUGHT | `POSITIVE=11/15 FRESH_POSITIVE=3/5 RC=2/4 MUT_ADMIT_KILLED=0 MUT_UNREACH_KILLED=0` / 5 `LEG_FAIL` / FAIL | `tool-T3-git-blob-empty-bytes.txt` |

`T1a` is killed **only** by the derivation binding (`MUT_UNREACH_DERIVED=0`), not by behaviour: its 203-class answers
are identical to the repaired tool’s. `T1b` is the same 203-only rule with the literal left in the bytes and it is
**not detected at all** — the frozen battery prints `PASS` for a tool that treats a 204 (a 2xx success, S216) as a
failed transfer. Direct behavioural probe on the P1 mirror (S022’s refetch row demoted to `http=204`):

```
GATE-RECORD S022 url=https://pubmed.ncbi.nlm.nih.gov/28912002/ fetched=2026-11-08T02:16:21Z tier=A decision=reject capture=none curl_rc=0 http=204 words=0 quote=none
pristine tool: FAIL REFETCH   (2xx is a successful response; the unreach claim cannot be grounded)
T1b tool:      OK            (success test narrowed to 203)
```

(`receipts/probe-T1b-204-unreach.txt`, rc 1 vs rc 0.)

## 5. Every survivor, the leg that should have killed it, and that leg firing on a probe

C1 (probe tree `P1` = freeze tree with one committed row demoted, `S022 … http 203 → 204`; diff in
`receipts/probe-P1-diff.txt`):

| survivor | leg that should kill it | exists? | leg firing on a probe (receipt line) | survivor on the probe |
|---|---|---|---|---|
| `N1` | `D1_WIDTH` (the `ROWS_203` pin) | yes | `probe-P1-base.txt`: `LEG_FAIL D1_WIDTH 2/2/2 pin3` (also `D2_WIDTH`) | single `N1` on P1 is still FAIL via `D2_WIDTH` (`probe-P1-N1-pin-drop.txt`); `J1` (both pins) is `PASS` on P1 (`probe-P1-J1-pins-both.txt`) |
| `N6` | `D2_WIDTH` | yes | `probe-P1-base.txt`: `LEG_FAIL D2_WIDTH 2/2/2 pin3` | symmetric: single `N6` still FAIL via `D1_WIDTH` (`probe-P1-N6-pin-drop.txt`); `J1` PASS |
| `N2` | `CODES` (expected code in refused set) | yes | `probe-P2-tier-wrong-base.txt`: `LEG_FAIL CODES 350/362`, 12 `WRONG_CODE … expected=TIER got=WORDS` | `N2` on P2: `EXPECTED_CODE=362/362 … PASS` (`probe-P2-tier-wrong-N2.txt`) |
| `N3` | `D1_REFUSED` | yes | `probe-P2b-d1-wrong-base.txt`: `LEG_FAIL D1_REFUSED 0/3` | `N3` on P2b still FAIL via `CODES` (shadowed, `probe-P2b-d1-wrong-N3.txt`); `N2` on P2b is `PASS` (`probe-P2b-d1-wrong-N2.txt`) — deleting the code check also makes the D1 tally code-blind, so `N2` subsumes `N3` |
| `N4` | `RECONCILED` (detail/`ok` reconciliation) | yes | `probe-P3-detached-instrument-base.txt`: `RECONCILED=14/15` / `GATE_RECORDS_R88=FAIL` on the E4 shape (`SETUP=ok detail=0/1`) | `N4` on the same instrument: `RECONCILED=15/15` / `PASS` (`probe-P3-detached-instrument-N4.txt`) |
| `N5` | `MUT_ADMIT` (derived mutant must accept D1) | yes | `probe-P4-admit-203-gate-base.txt`: `MUT_ADMIT_KILLED=0` / `LEG_FAIL MUT_ADMIT derived=1 killed=0` | `N5` on the same tool: `PASS` (`probe-P4-admit-203-gate-N5.txt`) |
| `J1` | `D1_WIDTH`/`D2_WIDTH` pins | yes | `probe-P1-base.txt`: both `2/2/2 pin3` | `PASS` on P1 (`probe-P1-J1-pins-both.txt`) — the tree has 2 pairs, `ROWS_203=3`, predicate PASS |
| `J2` | `RECONCILED` | yes, but blind | `probe-P1-base.txt`: base FAILs; `RECONCILED=13/15` comes from the *failing* width legs | `PASS` on P1 with `LEG_REREAD=15/15 RECONCILED=15/15` while the width details read `2/2/2 pin3` (`probe-P1-J2-ok-detached.txt`): the parser `detail=(\d+)/(\d+)` reads only the first `n/m` pair, so the pin mismatch is invisible |
| `NAMED-LIMIT` | none (named limit) | no | — | survives on the freeze tree; see §2 |

C2 (probe mirrors in `receipts/probe-C2-diffs.txt`): every survivor’s leg exists and fires on its probe — the
`base` column in the §3 table (`probe-P-B1b-base`, `probe-P-caseG-base`, `probe-P-A1d-base`, `probe-P-emptyQ10-base`,
`probe-P-F2-base`, `probe-P-F2b-base`, `probe-P-defcited-base`, `probe-P-provmodified-base`, `probe-P-sup-base`), and
each corresponding mutant prints `CURATION_R88=PASS` on the same mirror. The C2 counter has no reconciliation of a
leg's `ok` against a measured detail (only a leg-count check, which is why the leg-deletion kills fire), so none of
these deletions is detectable from the landing tree. The separate controls battery catches `M1`, `M2`, `M3` and `M5`
on their round-87 forgeries (`receipts/c2-controls-vs-mutants.txt`), but it stays `CONTROLS=PASS` under `M4`, `M6`,
`M7` and `M8`: for those four the only detector is the probe mirror built here, not any frozen instrument.

Tool: `T1b`’s offending rule *is* the tool’s `REFETCH`/2xx check, exercised by `D2_REFUSED`; the leg exists
(`D2_REFUSED=3/3` holds), but its input class is built only from refetch rows with `http == "203"`
(`build_d2_203_rejects` / `_qualifying_203`), so no frozen input contains a 2xx other than 203. The direct 204 probe
above shows the class the leg would need and does not have.

## 6. Findings (coverage, not claim defects)

1. **C1 named limit is real and reproducible.** A two-line joint edit (measurement false + self-consistent leg
   record) prints `GATE_RECORDS_R88=PASS`; the summary still prints `SETUP=0/1`. Named limit confirmed, not hidden.
2. **C1 width pin is only jointly defended.** Either pin can be deleted undetected (`N1`, `N6`); deleting both (`J1`)
   passes a tree with 2 of the 3 frozen 203 pairs. The reconciliation cannot see it because its regex reads only the
   first `n/m` pair (`J2`: `RECONCILED=15/15` with `2/2/2 pin3`).
3. **C1 expected-code leg is deletable.** `N2` passes a tool that refuses a tier forgery with `WORDS` (base: 350/362);
   `N3` (D1 tally code-blind) is shadowed by `CODES`, and `N2` subsumes it on the same probe.
4. **C1 receipt integrity is deletable alone** (`N4`), and the MUT_ADMIT acceptance measurement is creditable by fiat
   (`N5`) — both survive the landing tree and are only caught by their own probes.
5. **The 2xx≠203 unreach class is unmeasured.** `T1b` passes the entire frozen battery; a 204 `url/unreach` record is
   accepted, while the pristine tool refuses it. `T1a` (the literal-dropping spelling) is caught only by
   `MUT_UNREACH_DERIVED=0`, not behaviourally.
6. **All eight C2 leg deletions survive `CURATION_R88=PASS`.** The controls battery catches the four whose
   round-87 forgery exercises the deleted conjunct (`M1`/`M2`/`M3`/`M5`); `M4` (numeric floor), `M6` (`DEF_CITED`),
   `M7` (`UNENTAILED`) and `M8` (`SUPERSEDED`) survive the controls too — no frozen forgery exercises those legs.
7. **`FLOOR`’s printed detail is lossy**: qid-set and token-floor failures print `13/13 floor13`; only the verdict
   shows the failure.

No survivor changes a landing verdict: both frozen predicates print `PASS` at `4ea9d008` with the pinned bytes, and
none of the mutated counters is the landed counter. Nothing here is a defect in the landed repair; each survivor is a
place where the frozen predicate cannot see its own weakening.

## 7. Bounds, deviations, cleanup

- Leaf seat: no subagents, no `agent://all`, no production edits, no lane/fleet git or jj mutation, no commits, no
  sudo, no sysctl, no service restart, no network. Only the wave output folder and the scratch dir were written.
- Probe instruments are *inputs*, not counted mutants: the P3 E4-shape counter uses two edits
  (measurement false + `ok` detached, `ok`/detail honest), and the C2 mirrors use the same single-cell edits as
  `curation-r88-controls.py` (the DEF-CITED probe also moves one Do-cell word so the warrant stays satisfiable after
  Q13's quote is replaced). All counted mutations are single literal replacements except `J1`, `J2` and the
  explicitly joint `NAMED-LIMIT`.
- No run was inconclusive: every mutated instrument exited deterministically and printed a verdict; baselines passed
  (a failing baseline would have been reported as inconclusive).
- Scratch `/fast/scratch/hyaku/chousa-r88/R88MutCounter` (trees, mutant dirs, probe mirrors) was deleted after the
  receipts were copied to the wave folder. The receipts record the scratch command lines used at run time; the driver
  regenerates the trees, mutants and probes from the two revision archives.
- Tooling: none installed or upgraded (nothing was needed).

VERDICT: R88MutCounter C1 held — the frozen `GATE_RECORDS_R88=PASS` reproduces at `4ea9d008` and the C1 kill rules did not fire; nine counter mutants survive its own predicate (the named joint limit among them) and `T1b` shows the 2xx≠203 unreach class is unmeasured, reported as coverage findings.
VERDICT: R88MutCounter C2 held — the frozen `CURATION_R88=PASS` reproduces at `4ea9d008` with the repaired `Q1 (S215)` row (base tree 16/17) and the C2 kill rules did not fire; all eight leg deletions survive the counter's own predicate; four fall to the frozen forgeries, all eight only to the probe mirrors built here.
