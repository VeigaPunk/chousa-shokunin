# FC3 — Falsification report: C3 control `composed-current-registry`

Round 27 attempt1, landed revision `dd72641e574679c4f7882dd43de072b4c8892d6f` (gate sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`, verified before every probe matrix). Leaf scope: the single control at `corpus/evidence/round27-regressions.py:203-205`.

## Verdict: **HOLDS** (control behaves as claimed; three documented sensitivity limits, no counterexample against the landed gate)

## Item attacked

`composed-current-registry`: registry `| id | status | used-by |` + `| S001 | mined | corpus/knowledge/entry.md |`; entry `source: S001`, `verified-at: 2026-10-21 checked synthetic fixture`, `recheck: 90d`; invocation `verify-metadata <entry> --root <root> --registry <registry> --as-of 2026-10-21`, `LC_ALL=C`, `CHOUSA_STRICT=0`. Expected: exit 0, `due=2027-01-19 freshness=current`, `^FINDING ` count 0, `^RESEARCH_GATE: ` count 1.

## Q1 — Is the expectation derived from the contract, independent of gate code?

Yes. All expectations are hardcoded literals, not computed from gate output or parsed from gate source (only the C1 block regexes gate text). `2027-01-19` = `date(2026,10,21)+timedelta(days=90)` in Python datetime (`python3 -c "from datetime import date,timedelta; print(date(2026,10,21)+timedelta(days=90))"` → `2027-01-19`); sibling `composed-overdue`'s `2026-04-02` likewise. Counts are line-anchored. Gate lines 2772-2774 (`metadata_add_days "$verified_first" "$cadence_days"`) agree.

**Limit 1 (anchor-blindness):** the fixture sets `verified-at == --as-of` (2026-10-21), so a gate anchoring due on *as-of* produces the identical `due=2027-01-19 freshness=current`. The literal is contract-derived but cannot discriminate the due anchor. Demonstrated by mutant M2 below.

## Q2 — Mutation evidence: reverting the targeted fix

`composed-current-registry` targets **no specific C3 fix** — its fixture (well-formed header, no break/prose, plain `S001` source, no denylisted path) matches none of the three repaired shapes (header-state reset, S-id rescan, full-path denylist). It is the claims' "existing well-formed registry behavior remains" guard. Proven at three granularities (each scenario = one gate invocation, probe exit 0, PASS/FAIL printed):

- **Full revert** — base gate `64eec5d4` (sha256 `c2c813f1b425bc4e…`, `git show 64eec5d4…:tools/research-gate.sh > gate-base.sh`): `python3 probe-composed.py gate-base.sh composed-current composed-overdue composed-queued header-break-blank` → `composed-current: PASS rc=0 CLEAN`. The control **passes on the completely un-repaired gate**.
- **M1 registry-blind** — all five `REGISTRY_ARG_SET` sites in the metadata path (`tools/research-gate.sh:2595,2654,2689,2718,2735`) → `(( 0 ))` (mutant sha `5912a6405603037a`): gate never loads or checks the registry. `composed-current: PASS rc=0`. **Limit 2: the named control alone is vacuous w.r.t. registry consultation.** Sibling `composed-queued: FAIL rc=0, count FINDING META_SOURCE_NOT_MINED 0 != 1` — the *pair*, not this control, pins that the registry file was read.
- **M2 as-of-anchored due** — line 2773 `metadata_add_days "$verified_first" …` → `"$AS_OF_ARG"` (mutant sha `b79e5a23e0f89f99`): `composed-current: PASS` (anchor-blind confirmed); `composed-overdue: FAIL rc=0` (got `freshness=current`, required overdue+META_RECHECK_OVERDUE) and my same-class `verified-anchor-probe` (verified `2026-10-01` ≠ as-of, expect `due=2026-12-30`): FAIL on mutant, PASS on landed → landed gate is verified-at-anchored per contract; a distinct-date control would have teeth, this one does not.
- **M3 header-state revert** — removed the non-table reset (`2433-2434`) and the delimiter-width match (`2463`) (mutant sha `5b9f10c42c68f5ec`): `composed-current: PASS`; `header-break-blank: FAIL rc=0` (no refusal). The header fix is detected by its sibling, never by this control.

No run failed for a parse/setup reason; every FAIL above is a behavioral expectation mismatch, i.e. the siblings fail for the *intended* reasons while the named control stays green.

## Q3 — Nearby synthetic inputs of the same class

On the landed gate (all PASS where contract expects pass; probe exit 0):

- `--as-of 2027-01-19` (== due): exit 0, `freshness=current` — strict `as-of>due` overdue semantics hold at the boundary.
- `--as-of 2027-01-20` (due+1): exit 1, `due=2027-01-19 freshness=overdue` + exactly one `META_RECHECK_OVERDUE` finding (gate contract-correct; my probe's `^FINDING ` count 0 expectation there was over-strict, gate right).
- Unicode `verified-at: ２０２６-10-21 …` under `LC_ALL=en_US.UTF-8`: exit 1, `META_VERIFIED_AT_UNDATED`, `due=unknown freshness=unknown` — ASCII grammar enforced on the entry side (function-local `LC_ALL=C`, gate line 2564).
- `verified-at: 2026-10-01` with as-of `2026-10-21`: `due=2026-12-30` — verified-anchored due, contract-correct.

No input found where the landed gate is wrong in this class.

## Counterexamples

None against the landed gate. Counterexamples are against the *control's discriminating power*: it passes on base gate, on a registry-blind gate, and on an as-of-anchored gate (M1/M2/full-revert above). Minimal counterexample for the vacuity claim: mutant M1 + the exact control invocation reproduces `RESEARCH_GATE: CLEAN … findings=0` with a registry file that is never opened.

## Incident (disclosed)

`/tmp/chousa-r27-falsify-FC3` collided with a sibling FC3 leaf's sandbox: at 12:41:42 my `probe.py` there was overwritten with a foreign denylist driver (75 lines, `DRIVER_SUMMARY` output; two mutant-matrix runs consumed it before detection — those runs are discarded). Landed gate, base gate, and all three mutants were sha/marker-verified untouched. All evidence above was re-produced in `/tmp/chousa-r27-falsify-FC3-11` (`probe-composed.py`) with `sha256sum` pinned before each matrix. The foreign file was treated as data and not executed as mine.

## Limits

- Single gate invocations only; full `--selftest` and the whole regression script not run (L1 owns those; L1 measured selftest PASS 210, regressions 58/58 at this revision).
- Duplicate registry id rows (first wins, later silently ignored) and rows after a post-table break (ignored; citing their ids yields `META_SOURCE_ROW_MISSING` rather than `NOT_MINED`) are undeclared-contract areas I probed only by reading, not falsified — residual risk for the block, not for this control.
- No installs performed (pacman transactions paused host-wide; nothing needed).
- Verdict is author-lane advice for round 27, not an admission outside it.
