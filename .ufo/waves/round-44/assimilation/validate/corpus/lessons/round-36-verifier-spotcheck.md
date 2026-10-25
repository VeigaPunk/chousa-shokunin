# Round 36 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-23
lane HEAD verified: `f19589d63e291328ac647e5434188fc56310ba9b` (round start `86bfc0f4f63c4e4dc8dcd8eb2e96dfeab1639f06`; inherited attempt-1 freeze `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`)
report: `.ufo/reports/round-36/chousa.md` (committed by the lane identity `chousa-shokunin <chousa@shokunin.local>`, fleet commit `0f3507a5dc766de7c567d0baa26eba2870e4b470`; earlier commits `47e6a3a9 786d9526 8cd3887d` are superseded revisions of the same path)

This verifier is a fresh dispatch of the hyaku orchestrator, non-author by construction: it wrote
nothing in this lane before this file. Claims are graded as measured on the landed bytes, narrowed
by the lane's own errata where the errata removed a reading (C1's S7-S9 vacuity candidates, the
call-for-show and prefix-64 survivors), and any narrowing is routed, not silently counted.

## Step-1 conformance

- **Report committed by the lane identity: PASS.** `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-36/chousa.md`
  → four commits, all `chousa-shokunin <chousa@shokunin.local>`; the final one is
  `0f3507a5dc766de7c567d0baa26eba2870e4b470` (18:48:32 -0300, after the lane tip `f19589d6` at 18:47:10) —
  the report is not a marker: it carries work items with evidence pointers, a `LOG.md`-tied landed-changes
  table and checkable commit hashes.
- **Report bytes are the landed bytes: PASS.** `git show 0f3507a5:.ufo/reports/round-36/chousa.md | sha256sum`
  = worktree `sha256sum` = `f75ac468ffb743abc979855e03f748c4ebb9870466a102031d16a5d15606be99`;
  `git merge-base --is-ancestor 0f3507a5 HEAD` → true (fleet HEAD `c47b65fcf8ef8c9e93869ba7e13f27ed9e4373bd`).
- **`SHONEN` heading, one line per box: PASS.** Line 188 `## SHONEN`, four lines, all `[~]` with
  resolvable pointers; no `[x]` written by the lane, and none written by this verifier
  (promotion is operator-owned).
- **Cited lane commits exist and are ancestors of `refs/heads/master`: PASS (6/6).** HEAD is detached
  (jj-colocated, expected); ancestry tested against the branch ref, never `@{u}`:
  `76597487c8c3f963465cdbcfcabe91acd1ea2500` (round work), `6b3aba52f046bae0bf7b48fcf8e4eda16e20aff7`
  (late seat), `e66c4563e3a76c90dcbb37e834cd07b533199849` (critic corrections), `f19589d6…` (source re-open),
  plus `700bd5fc…` (inherited freeze) and `86bfc0f4…` (round-start base).
  Content identity re-derived where the claim binds it: `86bfc0f4:tools/research-gate.sh` →
  `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (the base control);
  `700bd5f` and `f19589d6` `tools/research-gate.sh` → `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`
  (the landed gate); `f19589d6:tools/argv-witness.py` → `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e`;
  `tools/argv-witness.py` is absent at `86bfc0f4` (new capability, as claimed).
- **Pushed and no uncommitted round work: PASS.** `jj-lane.sh state` →
  `branch=master local=f19589d6… remote=f19589d6… ahead=0 behind=0`; `git status --porcelain` empty.
  The one inherited dirty path (`corpus/evidence/round36/__pycache__/`) is discarded and gitignored
  (`.gitignore:3` `corpus/**/__pycache__/`); a regenerated ignored pyc (18:31) is build residue, not round work.
- **Prompt carries the template contract: PASS.** `.ufo/prompts/chousa-round-36.md` carries the
  round-level items (§1 mission/axes, §3 L2 floor "at least 8" — matching `MISSION.md:55` — §5
  commit-then-push, push scope, L0 channel) and all five child-lane items: report path (:101), the
  `SHONEN` heading requirement (:118), write scope (:259), the hash-citation rule ("Cite ONLY the
  helper's final `landed <hash>` line", :281) and report-lands-last (:325). No route map is quoted,
  so no `MISSION.md` bucket mismatch exists. Round shape is honest: one v1 wave of 36 seats
  (`.ufo/waves/round-36/w1-taskcall.json`, roles 15 executor / 5 scout / 5 scribe / 4 reviewer /
  2 critic / 2 mutation-tester / 1 each sentinel, simplifier, connector; 10 attack-role seats = 28%),
  one dead seat, plus a 3-seat residual call = 39 total (cap 128); wave 2 not dispatched and w2 empty.
  Task texts lead with the byte-identical Godspeed directive, name absolute lane paths and carry the
  `Report:` trailer; 36/36. Briefs: 36 seat files + `CONTEXT.md`.

## Per-claim re-check (commands run by this verifier)

C1 — operability. Landed gate `a7d3922c…`:

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 corpus/evidence/round36/c1-count.py --gate tools/research-gate.sh --seed 36401 --receipt /tmp/r36v-c1-36401.json
ENGINE_SWAP_CANARY=14/14   (exit 0; receipt predicate_holds=true, gate_sha256=a7d3922c…)
$ … --seed 36411 …
ENGINE_SWAP_CANARY=14/14   (exit 0; predicate_holds=true)
```

Before control, base gate extracted from `86bfc0f4:tools/research-gate.sh` (`a4768851…`) on fresh seed 36421:

```
$ python3 corpus/evidence/round36/c1-count.py --gate /tmp/r36v-base-gate.sh --seed 36421 …
ENGINE_SWAP_CANARY=10/14   (exit 1; S11-manifest-hash-shim, S12-locale-c, S13-pin-echo-isolation,
                            S14-pin-drift-token FAIL — exactly the four reported holes)
```

→ **C1 met under P1 as reported: 10/14 → 14/14, re-measured on two fresh seeds plus the before control.**
Narrowed as the lane states: S1-S10 also pass the base control; the four newly discriminated behaviours
are S11-S14; S7-S9 assert the echo/refusal contract, not per-call engine identity (QUALITY 52).

C2 — calibration. Landed gate + landed witness:

```
$ python3 corpus/evidence/round36/c2-count.py --gate tools/research-gate.sh --witness tools/argv-witness.py --seed 36401 …
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass  (exit 0; predicate_holds=true)
$ … --seed 36411 …   same four fields, exit 0, predicate_holds=true
```

Before control, base gate + `86bfc0f4:tools/mechanism-witness.py` (`9f537bfd…`) on fresh seed 36421:

```
WITNESS_PER_RECORD=2/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=absent RENAMED=fail  (exit 1;
V1,V4 fail the witness; V2,V3,V5 pass it; V6 renamed → unparseable)
```

→ **C2 met under P2 as reported: 2/5 → 5/5, renamed matcher no longer false-killed; before/after re-measured.**
The reading stays a *query* witness (the round's own call-for-show and prefix-64 errata; see routed items).

Kill-rule scan (receipts under `.ufo/waves/round-36/` and `corpus/evidence/round36/`): every receipt whose
`gate_sha256` is the landed `a7d3922c…` and whose `witness_sha256` is the landed `e6832e0b…` sits at target
(14/14 or 5/5, `predicate_holds=true`). The four lower landed-gate receipts all carry `predicate_holds=false`
and non-landed witness bytes — `c2-stubpass-s36001.json` 0/5 (always-pass stub, `ee0e0cc7…`) and three
`MutC2AttrKey/art/rec-global-*.json` 0/5 (global-count mutant, `7fb47738…`). The 11/14 receipts pair the base
gate (`a4768851…`) with one repaired scenario; the 12/14 receipt pairs a non-executing-pin gate
(`5c028fed…`). No lower label was produced by the landed gate with the landed witness. Kill rule holds.

No-harm is **evidence-verified, not re-executed** (PROTOCOL §Gate standard, never execute a sibling's gate):
`w1/ExecSelftest.md` records `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)` under default, `LC_ALL=C`
and a scratch `TMPDIR`, pinned to gate `a7d3922c…` and `master=700bd5f`, with cases 257-261 listed;
`w1/SentNoHarm.md` records claims 17/17, chain 17/22, broken control 1/2, archives 3/3;
`w1/ExecNewCases.md` documents 257-261 absent from the 256-case base suite.

## Per-axis verdicts (six SCORECARD axes)

| axis | verdict | reason |
|---|---|---|
| operability | **improved** | C1 re-measured 10/14 → 14/14 on fresh seeds with the before control reproduced; four gate holes now separated. The round-1 archive scale stays 3 → 3 (delta 0), the lane's recorded convention (rounds 25, 29, 31-35; closures graded operability improved there on the same pattern). |
| calibration | **improved** | C2 re-measured 2/5 → 5/5 with `LANDED_ATTRIB=pass` and `RENAMED=pass`; the before-state failure mode (false-killing a rename) is gone. |
| coverage | unchanged | no coverage claim this round; SOURCES 68 → 70 is the frontier step, not a coverage measure. |
| depth | unchanged | no independent domain-fact or depth claim; the knowledge entries scope themselves to the lane's own gate and witness. |
| freshness | unchanged | no new drift detector or cross-revision freshness claim; the drift token is a gate-contract cell, not freshness. |
| adjacency | unchanged | no network; both new rows are installed local pages; independent token sweep of every sibling repo's committed `HEAD` tree for `WITNESS_PER_RECORD|ENGINE_SWAP_CANARY|argv-witness|RESEARCH_GATE_GREP` → zero hits outside this lane, matching the connector's scan (its one disclosed limit, mori's `worktrees/round-19` copies, is a worktree-only gap recorded `[INFERENCE]` with sha256 `722e44bb…`). |

## Discernment spot-check (LEARNING.md)

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → **exit 0**,
`chousa ok`, rows **70** (A 64 / B 1 / C 5; mined 47 / queued 19 / rejected 4 — recounted from the table),
two standing W04 duplicate-URL warnings (S051, S053), before count at `86bfc0f4` = 68.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S069 GNU `grep(1)` `-o`+`-b` | admit (tier A, mined) | `/usr/share/man/man1/grep.1.gz`, opened locally 2026-10-23 | **agree** | file SHA-256 `9b027d02…85ba` matches the row; `.SS "Output Line Prefix Control"` at decompressed 382; quote at 387-391 is verbatim — "If -o (--only-matching) is specified, print the offset of the matching part itself." (13 words by `wc -w`, inside the 25-word limit); `teaches` is the quote plus its direct consequence; `used-by` (`corpus/knowledge/per-record-argv-attribution-r36.md`) resolves. |
| S070 GNU coreutils `sha256sum(1)` | admit (tier A, mined) | `/usr/share/man/man1/sha256sum.1.gz`, opened locally 2026-10-23 | **agree** | file SHA-256 `93c17dff…403f` matches; quote at line 11 is verbatim "Print or check SHA256 (256-bit) checksums." (6 words); broader span lines 4-11, 54-56 verified; `used-by` (`corpus/knowledge/engine-swap-canary-r36.md`) resolves. One label defect confirmed: lines 19-20 (`-c, --check`) sit under DESCRIPTION, not SYNOPSIS — the lane recorded the nit and deferred a supersede row; a label fix must be a new row, never an edit. |
| man7.org `grep(1)` HTML page | reject (no row) | the rejected candidate itself; the installed page was opened instead | **agree** | CORPUS contract v1 writes a row only after its source is opened this round; a URL row asserting the installed page's bytes would be reference drift. The reject is on procedure, not merit. |
| POSIX `grep` specification | reject (deferred) | not fetched | **agree** | the lane's no-external-fetch-without-operator-approval rule binds; deferral is not a merit rejection and the lesson says so. |
| `locale(7)` for the C-locale decode | reject (overclaim) | `/usr/share/man/man7/locale.7.gz` | **agree** | the page documents categories (`LC_ALL`, `LC_CTYPE`) and refers to `printf(3)`; it does not document bash `printf %b`'s locale-bound decoding, which is what the arm measured. A row would attribute behaviour to a page that does not state it. |

## Trend verdicts

- **expansion: improved.** `ls corpus/knowledge/*r36.md` → 2 admitted entries
  (`engine-swap-canary-r36.md`, `per-record-argv-attribution-r36.md`), each with the
  `source:`/`verified-at:`/`recheck:` trio and each resting on a row opened this round; SOURCES 68 → 70;
  two capability rows added.
- **quality: improved.** Four gate holes closed and measured by the before/after above; selftest 256 → 261
  with cases 257-261 documented as failing on the base behaviour; the pin-coverage ledger is measured
  (`w1/ExecModeCoverage/`: 1 recorder call, `--version`, 0 matcher calls for the two exempt modes).
- **discernment: improved.** The round's own docstring drift was caught against a receipt and mined
  into QUALITY 50; the C1 vacuity candidates were named by a seat that did not run the counter
  (QUALITY 52); S11/S12 point value was established by mutation; survivors (call-for-show 14/14,
  prefix-64 bypass 5/5) are on the record as errata rather than defended. One seat died
  (`CritC1Swap`, provider `cyber_policy`) and stays dead in the evidence; nothing was prettified.

## Routed defects the lane must fix next round

1. **Report internal contradiction (erratum owed).** `.ufo/reports/round-36/chousa.md:91` says the
   `RevSourcesNew` seat "did not return", while `:165` cites its VERBATIM result and lane commit
   `f19589d6` landed it. Append an erratum naming the superseded sentence; do not rewrite filed bytes.
2. **Report number drift (erratum owed).** `:156` says the lesson carries the S069 quote at "15 words";
   the lesson says 13 and the quote is 13 words. Correct in the next round's record.
3. **Kill-rule wording incomplete.** `:128-131` names only base-gate runs and the always-pass stub as the
   lower labels; the committed set also holds 11/14 (base gate + one repaired scenario), 12/14
   (non-executing-pin gate `5c028fed…`) and the global-count mutant witness at 0/5 on the landed gate.
   The substantive rule holds (all lower receipts are `predicate_holds=false` and non-landed bytes);
   reword so the evidence set matches the sentence.
4. **S070 anchor label.** Lines 19-20 are labelled SYNOPSIS but sit under DESCRIPTION; land a supersede
   row in round 37 (append-only — never edit the filed row).
5. **Cosmetic leftovers.** Empty untracked `.ufo/waves/round-36/w2/` from attempt 2 (never dispatched) and
   a regenerated ignored `corpus/evidence/round36/__pycache__/c2-count.cpython-314.pyc` (18:31, after the
   removal): no round work, but remove both and state it.
6. **Carried debt, already in `SCORECARD.md` planned r37 — keep it visible:** the `BASH_ENV` re-export hole
   in `--pin` capture (Erratum 7); the prefix-64 attribution bypass (Erratum 8); the call-for-show limit
   (Erratum 9); the metadata-screener locale seam at `research-gate.sh:1015` (Erratum 13); S7-S9 scenario
   assertions tightened to their names; the three dead fields in `tools/argv-witness.py`.

## Notes for the operator

The four SHONEN boxes look checkable by a non-author from this closure's evidence: box 1 from the
`SKILL.md` gate/tool rows and the two r36 knowledge entries, box 2 from `LOG.md` §Round 36 and the
committed receipts, box 3 from commands this verifier ran (`c1-count.py` and `c2-count.py` both execute
from the lane root and reproduce their targets), box 4 from the independent sibling token sweep above.
Promotion remains operator-owned; no `[x]` was written here.
