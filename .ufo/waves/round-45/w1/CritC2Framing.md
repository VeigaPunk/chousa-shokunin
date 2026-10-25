# CritC2Framing — round 45 wave 1 (critic, C2 framing)

Seat: L1Chousa45.CritC2Framing (leaf; no subagent, no writes outside this file, no network).
Assignment: attack C2's framing as calibration — is the SKILL.md Gates table the lane's self-assessment? Is the entry-point set the right set (list every other gate-like file with a one-line judgement)? Would registering superseded v1 counters mislead? Verdict + strongest objection.
No tools installed (nothing needed; all evidence from committed files and the frozen counter).

## Commands run (verbatim, decisive lines)

`python3 corpus/evidence/round45/c2-count.py --list` (lane root):
```
UNREGISTERED_PATH corpus/evidence/round31/c1-count-v3.py
UNREGISTERED_PATH corpus/evidence/round31/c1-count.py
UNREGISTERED_PATH corpus/evidence/round31/c2-count-v3.py
UNREGISTERED_PATH corpus/evidence/round31/c2-count.py
UNREGISTERED_PATH corpus/evidence/round32/c1-count.py
UNREGISTERED_PATH corpus/evidence/round32/c2-count.py
UNREGISTERED_PATH corpus/evidence/round33/c1-count-v3.py
UNREGISTERED_PATH corpus/evidence/round33/c1-count.py
UNREGISTERED_PATH corpus/evidence/round34/c1-count-v2.py
UNREGISTERED_PATH corpus/evidence/round34/c1-count.py
UNREGISTERED_PATH corpus/evidence/round40/c1-count.py
UNREGISTERED_PATH corpus/evidence/round40/c2-count.py
UNREGISTERED_PATH corpus/evidence/round41/c1-count.py
UNREGISTERED_PATH corpus/evidence/round41/c2-count.py
UNREGISTERED_PATH corpus/evidence/round42/c1-count.py
UNREGISTERED_PATH corpus/evidence/round42/c2-count.py
UNREGISTERED_PATH corpus/evidence/round43/c1-count.py
UNREGISTERED_PATH corpus/evidence/round43/c2-count.py
UNREGISTERED_PATH corpus/evidence/round43/c3-count.py
UNREGISTERED_PATH corpus/evidence/round44/c1-count.py
UNREGISTERED_PATH corpus/evidence/round44/c2-count.py
UNREGISTERED_PATH corpus/evidence/round44/c3-count.py
UNREGISTERED_PATH corpus/evidence/round44/errata-count.py
UNREGISTERED_PATH corpus/evidence/round45/c1-count.py
UNREGISTERED_PATH corpus/evidence/round45/c2-count.py
UNREGISTERED_PATH corpus/evidence/round45/c3-count.py
UNREGISTERED_PATH tools/absent-split.py
UNREGISTERED_PATH tools/parent-lifetime.sh
UNREGISTERED_PATH tools/quarantine-check.py
ENTRY_POINTS=54  GATES_ROWS=18  REGISTERED=25/54  UNREGISTERED=29  C2=FAIL  exit 1
```
Matches the claim's freeze prediction (base 51 + 3 = 54; UNREGISTERED=29). Counter behaves as frozen.

`grep -n '^## ' SKILL.md` → only `## Gates` at line 75 between the section's start and `## Round26 ...` at 491.
Row-grammar probe (same rule as the counter, over SKILL.md): 18 qualifying rows at lines 79,82-84,86-99. Three visible gate rows FAIL the rule: lines 80 (verify-claims), 81 (verify-chain), 85 (verify-metadata) each have 9 pipes but NOT the literal substring `exit` (they spell verdicts as `` `0` clean `` / `` `2` could-not-evaluate ``). So the counter's Gates table has 18 rows; the table itself shows 21 gate rows; 3 are invisible to the counter.

Coverage probe: no qualifying row contains `round31`, `round40`…`round45`, `parent-lifetime`, `absent-split`, or `quarantine-check` → confirmed all 29 unregistered are genuinely absent from the section.

Executable inventory: `find . -type f \( -name '*.py' -o -name '*.sh' -o -name '*.bash' -o -name '*.zsh' -o -name '*.rb' \)` → 969 files (mostly `.ufo/waves/**` historical artifacts); full listing was written to scratch and checked; per-class judgement below.

## Verdict

The claim is internally consistent and the counter is faithful to the predicate. The framing is **calibration as coverage of a name pattern, not correctness of the account**. That is a fixable-by-drafting scope, but it has one live inconsistency (the table itself already mis-attributes a registered counter) and one forced-mislead (10 of the 29 registrations are for superseded/frozen counters). C2 as written is a passable *inventory sweep*; it is not a truth check on the self-assessment, and the drafting must not pretend otherwise.

## Q1 — Is the Gates table the lane's self-assessment?

Yes in intent: the claim says exactly that (claims.md:43-44), and the counter treats the committed tree as the observed state. But the measured property is only *path membership inside rows that satisfy a grammar heuristic*. Three consequences:
1. A row that fails the heuristic is invisible even though it is a real gate row. Already true: lines 80/81/85 (verify-claims, verify-chain, verify-metadata) are gate rows (they name entry points and verdict maps) yet dropped — GATES_ROWS=18 vs 21 actual rows. Today no path depends on those rows alone, so no false pass; the fragility is future (a new gate documented in a row without the literal word `exit` escapes, in both directions).
2. Path membership is per-substring, not per-row identity: any row containing the path registers it, even a row describing a *different* gate. Already true: `corpus/evidence/round32/c2-count-v3.py` is registered only because the **round-33** row (SKILL.md:90) names it; the round-32 row (SKILL.md:89) names `c2-count-v2.py`. A reader cannot tell from the table which counter measured round 32 — the account is self-inconsistent and C2 cannot see it.
3. Verdict-map correctness is out of scope (claims.md:66-67 names it a reader's check). Fine, but then C2 is bookkeeping, not calibration of *behavior*.

## Q2 — Is the entry-point set the right set?

Mostly right for the intended surface (standing tool CLIs + per-round counters); all 7 `tools/` files are real CLIs (two run via `python3` though not chmod +x: absent-split.py, quarantine-check.py). Two systematic gaps:

Over-inclusion — 10 of the 29 demanded registrations are superseded/frozen files the lane itself labels dead:
- round31: c1-count.py, c2-count.py (r31 design v2 counters, superseded by r32 rows), c1-count-v3.py, c2-count-v3.py (not r31's counters; the v3 is *cited* by round33 claims as a behavior authority: round33/claims.md:24 `corpus/evidence/round31/c1-count-v3.py:43`).
- round32: c1-count.py, c2-count.py — "v1 unchanged and no longer counted" (round32/claims.md:145,163).
- round33: c1-count.py — "stays committed and unedited; its control receipts remain evidence for v1 only" (round33/claims.md:98); c1-count-v3.py (unlisted draft/reference).
- round34: c1-count.py, c1-count-v2.py — v1/v2 superseded by v3 (round34/claims.md:96,142; the row itself notes "v1/v2 counters kept frozen and superseded", SKILL.md:91).

Under-inclusion — committed executables under corpus/evidence that a reader could call gates, excluded by the naming rule (one-line judgement each):
- round34/self-audit.py — a calibration counter in all but name (frozen predicate, count of mismatches between self-assessment and repo, exit 1 on fail); historical (r34 attempt-2), superseded by later C2 rounds. Closest to a genuine miss.
- round32/q33-check.py — QUALITY-33 check reading receipts, exit 1 on FAIL; one-off attribution check.
- round29/prose-check.py — prose hygiene checker with exit semantics; r29 seat tool, not standing.
- round30/rerun-check.py — audits stated re-run counts against receipts; one-off.
- round30/qr_harness.py — harness for the r30 counters; already named in a row; fixture, not a gate.
- round33/d2-census.py — receipt census CLI (D2 repair artifact); a census, not a gate.
- round25-ledger-recount.py, round25-meta-oracle.py, round26-registry-oracle.py — oracles/differential support for r25-26 checks; historical.
- round27-falsify-controls.py, round27-mechanisms.py, round27-regressions.py — r27 exploration probes.
- .sh: round24-measure.sh, round25-measure.sh, round26-measure.sh (measure drivers), round25-holds/battery.sh (fixture), round25-meta-differential.sh (exits 1 on disagreement — gate-like, historical), round26-date-differential.sh, round26-registry-differential.sh (differential probes), round25-sources-census.sh (frozen census CLI), round33/no-name-signals.sh (D5 hygiene scanner, one-off).
Judgement: none is a *standing* gate; all are museum/historical artifacts. Excluding them is defensible and registering them would mislead — but the predicate's words are "every committed gate entry point", so the gap is between the stated scope and the realized proxy. Recommend: say so in the drafted rows/claims (a one-line note that the table covers the standing surface, not every historical executable), rather than silently relying on the naming heuristic.

`.ufo/waves/**` (969-file bulk): probes, mutants, controls, gate snapshot copies (e.g. round-41/controls/base-gate-r41.sh, ctl-c2-stub-*.py, mutant counters, `round-43/assimilation/validate/` mirror of corpus/evidence). Correctly excluded: they are fixtures/controls/history, not entry points.

## Q3 — Would registering superseded v1 counters mislead a reader?

Yes — if drafted as ordinary rows (kind `gate`, verdict map, self-test), a reader concludes 10 dead counters are live gates. The lane's own convention already distinguishes them ("kept frozen and superseded"); the fix is to mark each such row `superseded` (kind cell or self-test cell) with the live successor named. Note the counter cannot tell a superseded annotation from a live one, so this is a drafting obligation, not a checkable one. Alternative (cleaner, matches "default clean cutover"): delete the 10 dead files so the tree and the table agree — the predicate measures the observed tree, so ENTRY_POINTS would shrink to the live 44 and the sweep's demand disappears. Deletion is a production write; seats may not do it — recommend it to the main agent as the stronger option, with annotated rows as the fallback. Round-31 v3 files are the exception: they are cited as contract reference, so deleting them would break round33 claims' citations; annotate rather than delete those two.

## Strongest objection (counterexample)

The account is already self-inconsistent on a *registered* path and the counter cannot see it: `corpus/evidence/round32/c2-count-v3.py` passes C2 today by appearing inside the round-33 row while round-32's own row registers `c2-count-v2.py` — two counters for one round, each registered under a different round's row, and no row states which measures round 32. This is exactly the failure class calibration is supposed to catch (identity confusion, duplicate authority), and the frozen predicate structurally cannot catch it. Therefore C2's PASS (once the 29 rows exist) does not certify that the Gates table is a coherent account — only that every name-pattern match appears somewhere in it. Smallest safe correction within the frozen predicate: drafting rule — each entry-point path appears only in the row(s) that describe that gate, and superseded versions are explicitly labelled; plus a one-line limitation note in claims.md that the sweep checks coverage, not row identity/verdicts. This does not change a predicate, counter, or target.

## Pointers
- Predicate/claim: corpus/evidence/round45/claims.md:41-69 (frozen; commit d82cec904bf0fb8736886b9f17be913c7807427a).
- Counter source: corpus/evidence/round45/c2-count.py:28 (regex), :45-55 (row rule).
- Row-grammar blind rows: SKILL.md:80,81,85 (no literal `exit`).
- Mis-attributed registration: SKILL.md:89 (r32 v2) vs :90 (r32 v3 under r33 row).
- Superseded markers: round32/claims.md:145,163; round33/claims.md:98; round34/claims.md:96,142; SKILL.md:91.
- Round31 v3 citation: round33/claims.md:24.
- Main-gate rows present: SKILL.md:79,82-84,86-99.
