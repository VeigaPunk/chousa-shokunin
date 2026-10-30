# Round 63 (attempt 2) — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)
Date: 2026-10-30. Round closed against lane tip `4a11a71d2e22f2588539b253318cc114bd79b859`, base
`4ece131ca826c646bd28a50802d41bc78d8a9717`, freeze `e5166179197b43c77b58d56b89b8e2523aed0dd3`.
Report: `.ufo/reports/round-63/chousa.md` (fleet, committed by the lane identity `chousa-shokunin`).

## Conformance (step 1)

- Report path/heading: `.ufo/reports/round-63/chousa.md` carries `## SHONEN` with 4 `[~]` lines for the
  4 `SHONEN.md` boxes; no `[x]` anywhere in the report. Real report, not a marker.
- Attribution: `git log --format='%an %H' -- .ufo/reports/round-63/chousa.md` → `chousa-shokunin
  19283331f861610c3d9fbd1fb6e01dee46cdb1b9` (attempt-2 report) — lane identity.
- Ancestry (jj-colocated; tested against `master`, not `@{u}`): `git merge-base --is-ancestor
  e5166179… master` OK; `4a11a71d… master` OK; attempt-1 freeze `62876ef9` exists (`git cat-file -t` →
  commit).
- Pushed and clean: `scripts/hyaku/jj-lane.sh state …/chousa-shokunin` → `branch=master
  local=4a11a71d… remote=4a11a71d… ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` empty.
- Prompt fidelity: `.ufo/prompts/chousa-round-63.md` carries the round-level contract (mission/axes
  binding, L2 ≥8 one-batched, commit-then-push, push scope, L0 channel) and the five child-lane items
  (report path, commit-before-report, SHONEN heading, commit-hash citation, write scope). The §1 axes
  line matches `shokunin.conf` chousa verbatim; the L2 floor matches `MISSION.md` §L2 concurrency.
- Watchdog digest (copied to the closure notes; verified at lines 1925/1930/1950/1963):
  `2026-10-28T21:37:12-03:00 launch chousa round=63 pgid=3041545 driver=hyaku-inline attempt=1` /
  `2026-10-28T23:43:56-03:00 complete chousa round=63; hyaku-inline attempt=1` /
  `2026-10-30T02:38:17-03:00 launch chousa round=63 pgid=957812 driver=hyaku-inline attempt=1` /
  `2026-10-30T03:53:03-03:00 complete chousa round=63; hyaku-inline attempt=1`.

## Claim re-checks (step 2)

Method note: both claims rest on lane-owned instruments (`tools/lane-preflight.py`,
`tools/claims-audit.py` and the batteries/probes that drive them). Per PROTOCOL §Gate standard
(Closure consequence) the closure verified their **committed evidence** — frozen digests, receipts,
self-test tally, revision measured — and did not execute the lane's gates. Every documentary layer
(census, sources, digests, absence claims, diffs, attribution) was re-measured by the closure with its
own commands over committed bytes.

**C1 operability — improved (evidence-verified).** Frozen digests re-hashed at the tip and equal to the
freeze's pinned prefixes: `c1-battery-v2.py 0fbfd076e9a6235c`, `run-exhibit-receipts.py 99953077b7cd2d07`,
`exhibits/forge-token.py aabd28d1f3a63837`, `exhibits/overfit-oracle.py 9ebbe9b8a8d61137`. Receipts read
and cross-checked: `controls/exhibits/exhibit-v1-before.txt` — E01/E08/E09 `BATTERY=PASS` in full at
v1's 15+6 legs, E02–E07 accepted on their legs (13 runs; the do-nothing control: the falsifier class
scores 9/9 accepted); `controls/exhibits/exhibit-v2-after.txt` — all nine rejected with per-leg causes
matching the six wave judge holes (E02 control character, E03/E04 non-contract lines, E05/E06 usage rc=2
with bad id on stderr, E07 duplicate summary member), E01 on B07/B08+Z01–Z03, E08/E09 `BATTERY=FAIL` in
full on D16/D17+B07/B08+Z, honest controls accepted; `controls/c1v2-landed-runs.txt` —
`CLEAN=1/1 DEFECTS=17/17 BENIGN=8/8 ZERO=3/3 BATTERY=PASS` rc=0 ×3 seeds; `controls/c1v2-nulls-v2.txt` —
both nulls `BATTERY=FAIL` rc=1; `controls/preflight-full-run-final.txt` — `PREFLIGHT=8/8 FAILED=none
ENV=none SKIPPED=none` rc=0; `controls/c1-on-fixed-tool.txt` — the frozen attempt-1 battery passes the
amended tool ×3. Leg arithmetic consistent (v1 15+6=22, v2 17+8+3=29); battery source carries D16/D17,
B07/B08, Z01–Z03 and the strict-judge control-character/non-contract-line checks. Before→after holds on
the frozen predicate: 9/9 accepted → 9/9 rejected with honest controls kept and nulls failing.

**C2 calibration — improved (evidence-verified).** Absence at base re-derived by the closure:
`git cat-file -e 4ece131c…:tools/claims-audit.py` → absent (matches `controls/audit-before.txt` rc=2).
Digests at tip equal the freeze pins: `claims-audit.py d48247f9c77ac1e7`, `audit-r62.tsv 0364cfe29bb67d6e`,
`audit-r63.tsv 6bbd917a5007f030`, `audit-probe.py 9167ec2a454e4b8e`. Receipt
`controls/audit-after.txt`: `FLAGGED=2/2 AUDIT=FAIL` rc=1 (r62 erratum rows 1 and 13),
`FLAGGED=4/4 AUDIT=FAIL` rc=1 (E1–E4), `AUDIT_SELFTEST=PASS (3 cases)` rc=0, probe tail
`PROBE_FACTS=11/11` rc=0; `corpus/evidence/round63/audit-a2-result.txt`: `FLAGGED=0/4 AUDIT=PASS` rc=0
(pre-freeze self-audit). Seven rule classes confirmed in source; `file-kind` classifies by suffix
(`KIND_SUFFIX`, `kind_of`). The 6-of-18 scoping is stated in the claims file and entry, not narrowed.

**No owned axis harmed.** `git diff 4ece131c… 4a11a71d… -- SCORECARD.md` is purely additive (a
capabilities row `Claims audit` and the attempt-2 planned/verdict sections); no numeric axis score
changed; `PROVINCE.md`, `SHONEN.md`, `AGENTS.md` diffs are empty. Sibling roots were read-only.

## Spot-check (step 3) — 4 of 4 agree

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S146 | admit (A) | `MANWIDTH=1000 man -l /usr/share/man/man1/grep.1.gz \| col -bx`, rendered line 29 (`grep 3.12-2` per `pacman -Q`) | agree | quote exact: "Interpret PATTERNS as fixed strings, not regular expressions." — grounds the fixed-string `verbatim-heading` class |
| S147 | admit (A) | same render for `/usr/share/man/man1/git-log.1.gz`, lines 1374–1378 (`pacman -Qo` → git 2.56.0-1) | agree | `--diff-filter` paragraph at rendered line 1376 opens with the quoted "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M)…" — grounds `git-first-commit` |
| S148 | admit (B, own-work) | `corpus/evidence/round63/audit-probe.txt` | agree | 11 probe lines + `PROBE_FACTS=11/11` present as quoted; expected values authored, observed fields carry the evidence |
| S149 | reject (A page) | `MANWIDTH=1000 man -l /usr/share/man/man1/file.1.gz` NAME line (`pacman -Qo` → file 5.48-1) | agree | NAME renders "file —— determine file type" as quoted; reject is sound: `file-kind` classifies by suffix (`tools/claims-audit.py` `KIND_SUFFIX`), no round claim rests on magic content detection; flip condition recorded |

Census re-derived: `sources-census.sh validate` exit 0, `chousa ok`, only the five pre-existing W04
duplicate-url warnings (S051/S053/S073/S074/S075); rows `grep -cE` 145 (base) → 149 (tip); tiers
A/B/C 113/25/7 → 116/26/7; status mined/queued/rejected 118/19/8 → 121/19/9; `corpus/SOURCES.md`
diff base→tip has zero removed lines (purely additive, no old→new cell edits). Assimilation counts
match the freeze commit stat: reg-ids 145, staged-ids 114, collisions 64.

## Per-axis verdicts and trends

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 as above (falsifier class closed on frozen counters; G04/G05 benign shapes pinned) |
| calibration | improved | C2 as above (no-instrument → committed checker with committed detections; own claims audited pre-freeze) |
| depth | unchanged | entry states classes and limits; no existing entry deepened |
| coverage | unchanged | no new province surface; checker audits the lane's own artifacts |
| freshness | unchanged | no fetch; local installed pages only |
| adjacency | unchanged | sibling roots read-only; PROVINCE diff empty |

- expansion — **improved (narrowly).** `git grep -l 'claims-audit' 4ece131c… -- corpus/knowledge/`
  returns nothing (closure re-run, rc=1); the entry lands on that absent ground citing three rows opened
  and mined this round; one capability row enters SCORECARD.
- quality — **improved (narrowly).** The demonstrated false-positive class (G04/G05) is fixed and pinned
  as benign legs; the attempt-1 battery's demonstrated acceptance of the falsifier class is closed by a
  measured v2; no admitted entry was found false.
- discernment — **improved.** The lane filed `unchanged` pending the non-author spot-check; this closure
  performed it: all four of the round's gate decisions (3 admits, 1 reject) re-opened and agreed, and the
  round disclosed its limits before data (12 of 18 erratum statements left prose-only; the checker named
  a screen a reader outranks). LEARNING.md's improved condition (spot-check agrees on admits and
  rejects) is met; no QUALITY.md criterion was added without a lesson.
- No trade: quality is not harmed, so no operator ruling is required (LEARNING.md canonical rule).

## Routed defects (lane to fix next round; status-neutral)

1. **Unreceipted on-sibling verification.** The report and the lesson (line 61) assert the G04/G05
   post-fix runs on real sibling roots (`kagi/kake/tameshi --only G04,G05 → 2/2 each`) with no committed
   receipt; only the pre-fix FAIL side is committed (attempt-1 `CritC1GateRules.md`). The fix is pinned
   indirectly by the receipted benign legs (B07/B08 pass in `c1v2-landed-runs.txt` ×3). Commit the
   sibling-run receipt next round.
2. **Stale count in report text.** "lane `PREFLIGHT=5/5`" in the report's work items is unreconciled
   with the committed final receipt `PREFLIGHT=8/8` (5 run gates vs 8 incl. selftests) and carries no
   pointer. Superseded by the receipt; name the counting run or drop the figure.
3. **L2 floor unmet (0 seats).** Disclosed by the lane; caused by the orchestrator's 2026-10-30 dispatch
   pause (quoted verbatim in the report, claims file and lesson). The wave-carried attack items (mutation
   pass on both instruments, non-author forger, entailment read) stay routed to round 64.
4. **Scratch-path provenance.** `claims-a2.md` cites the `c1-on-fixed-tool` origin under a deleted
   `/fast/scratch` path; the committed copy resolves, but future receipts should name only committed paths.

Operator note (promotion is operator-owned): all four SHONEN boxes look checkable by a non-author from
the committed record (SKILL.md decision tables/checklists with cited sources and a populated gate
registry; end-to-end round work logged in LOG.md with receipts; instructions executed by receipts;
PROVINCE accurate and unchanged).
