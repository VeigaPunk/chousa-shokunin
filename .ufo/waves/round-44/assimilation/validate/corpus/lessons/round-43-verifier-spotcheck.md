# Round 43 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_swe)
date: 2026-10-24
reviewer identity: `Kimi fresh closure agent` (fresh, non-author; no subagents dispatched; no external fetch)
lane repo measured at: `a0ecc586b1c686a035388c5ed522cacfe55e372f` (pushed tip; `jj-lane.sh state` → `ahead=0 behind=0`, `local=remote=a0ecc586…`, branch `master`)
work commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`
base: `15f9f3fbd3c17b2155f718c67cbef0624034cf6d`

Claim counters were re-executed from `git archive` trees of those hashes under `/tmp/chousa-r43-closure/`. The lane working copy was not checked out and was not edited except for this file.

## Step-1 conformance

- Report `.ufo/reports/round-43/chousa.md` committed in the fleet repo under lane identity:
  `git log --format='%an %H' -- .ufo/reports/round-43/chousa.md` →
  `chousa-shokunin 15b1284890a999c99e8e298692d58e0c6480966f`. Author and committer
  `chousa-shokunin <chousa@shokunin.local>`. `git merge-base --is-ancestor 15b1284890a999c99e8e298692d58e0c6480966f HEAD` exit 0. Porcelain on that path empty. PASS.
- `SHONEN` heading present (report lines 125–135) with four `[~]` lines, one per box, each with a resolvable pointer. PASS. Boxes are checkable by a non-author; promotion is operator-owned and was not exercised.
- Cited lane hashes exist and are ancestors of `refs/heads/master` (not `@{u}`):
  `15f9f3fbd3c17b2155f718c67cbef0624034cf6d`, `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`,
  `a0ecc586b1c686a035388c5ed522cacfe55e372f` — each `merge-base --is-ancestor` exit 0.
  Both round commits are `chousa-shokunin <chousa@shokunin.local>`. PASS.
- Pushed: `jj-lane.sh state` → `ahead=0 behind=0`; `git ls-remote origin refs/heads/master` →
  `a0ecc586b1c686a035388c5ed522cacfe55e372f`. Git HEAD is detached at that same hash. PASS.
- Prompt `.ufo/prompts/chousa-round-43.md` carries template sections 1–5 (MISSION/AXES binding, 1–3 claims, frontier step, L2 floor, report contract including SHONEN / Sources & frontier / Trend verdicts, commit-then-push, push scope, L0) plus the §6 hyaku addendum. The literal token `commit-before-report` is absent; section 5 states commit-then-push and the report path, and the prompt requires a PROTOCOL re-read. PASS.
- Not a marker: work performed, evidence pointers, landed hashes, measurements, sources & frontier, trend verdicts, SHONEN. PASS.
- Dispatch digest copied from `.ufo/watchdog.log` (mutable):
  `2026-10-24T20:59:39-03:00 launch chousa round=43 pgid=2257195 driver=hyaku-inline attempt=1`
  `2026-10-24T21:28:08-03:00 complete chousa round=43; hyaku-inline attempt=1`

### Uncommitted paths (driver verify warned 39)

`git status --porcelain` → 39 lines: 3 `M` + 36 `??`. None name round 43. Left untouched. Not swept.

- `M .ufo/waves/round-40/w1/swarm-registry.json`
- `M .ufo/waves/round-41/w1/swarm-registry.json`
- `M corpus/evidence/round41/receipts/cells/cells.json`
- `?? .ufo/waves/round-40/w1/*.md` — 33 untracked seat reports
- `?? .ufo/waves/round-41/w1/*.md` — 3 untracked seat reports (`ConnectorSiblingScan.md`, `ExecC2Before.md`, `MutateC2Join.md`)

`PROVINCE.md` is not in the porcelain. `stat` mode `644`; index `100644`; `git diff -- PROVINCE.md` is empty; base→tip numstat for `PROVINCE.md` is empty. The r42 mode-bit debt was restored and is not still dirty. The other 39 paths match the report's inherited r40/r41 disclosure and the already-filed L0. No uncommitted round-43 lane work.

## Claims — re-measured

Surfaces of C1–C3 are byte-identical between work `737f40b6` and tip `a0ecc586` (`diff -rq` on `corpus/evidence/round43` empty; `absent-split.py` and the knowledge entry `cmp` identical). Base `15f9f3fb` lacks the tool, the three counters, the split table, and the knowledge entry. `tools/research-gate.sh`, `SKILL.md`, and `corpus/README.md` have empty base→tip numstat. The research-gate selftest was not re-executed (Gate standard: committed evidence). `ExecNoHarmGate.md` records `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)` and `EXIT_CODE=0` against the unchanged gate. Evidence-verified, not re-run.

### C1 operability — re-measured, holds

`python3 corpus/evidence/round43/c1-count.py` at the tip archive and again at the work archive:

```
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

exit 0 both times. Tool stdout detail: `misquote=9 not-carried=6`. Independent read of `absent-split.tsv` (15 data rows, no header): not-carried S080 S082 S086 S088 S104 S114 (6); misquote S084 S093 S094 S105 S108 S110 S111 S112 S116 (9).

Missing-tool control, counter pointed at the absent base path: `TOOL_PRESENT FAIL`, `C1=FAIL`, exit 1.

`MUTANT_DETECTED` compares a sliced id list with the expected ids; it does not execute a mutant tool. The claim's stated do-nothing control is the missing tool, and that control exits 1. Not a claim failure.

Verdict: **improved**. Score scale remains 3→3, as the lane recorded; the new command is the move.

### C2 calibration — re-measured, holds

`python3 corpus/evidence/round43/c2-count.py` at the tip archive:

```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
```

exit 0. `--flip S086`:

```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
```

exit 1. The counter recomputes R43-SPLIT itself (NFKC, whitespace collapse, longest run, bound 1/2). It does not import `absent-split.py`. It reads the campaign register and `.qcache` locally. No fetch.

Verdict: **improved**.

### C3 depth — re-measured, holds

`python3 corpus/evidence/round43/c3-count.py` at the tip archive:

```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
```

exit 0. Missing-entry control against the base path: `C3=FAIL entry-missing`, exit 1.

Independent of the counter: URL sha256 prefix is `2cef078d8f9f87802e19e770`. Capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt` exists, 80107 bytes, sha256 `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`. The 12-word quote is at byte offset 17383. mtime `2026-10-23T20:40:06-0300`, before launch `2026-10-24T20:59:39-0300`.

Verdict: **improved**.

### Other owned axes

- **coverage: improved.** One new mined row (S078) and one knowledge entry on ground the lane did not hold. `corpus/README.md` was not rewritten; the lane disclosed that. The row and the entry are the move.
- **freshness: unchanged.** The lane's scorecard says improved narrowly. The only open is a capture written the day before launch. No live surface was re-checked. Not harmed. Routed below so the next scorecard does not repeat the inflation.
- **adjacency: unchanged.** Lane S077 was not overwritten. Campaign tree was not edited. No sibling repo is in this lane's diff.

No owned axis harmed. `SCORECARD.md` base→tip is append-only (+26).

## Discernment spot-check

Census, re-run at write time: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` exit 0, five W04 (S051, S053, S073, S074, S075), then `chousa ok`. Matches `corpus/evidence/round43/receipts/census-end.txt`.

Validate-before-append: `sources-census.sh validate --file` on the committed mirror `.ufo/waves/round-43/assimilation/validate/corpus/SOURCES.md` exit 0, same five W04, no E03/E04. The committed `validate-census.txt` has the same warning lines and a `file ok` line.

SOURCES diff base→tip is one added registry row (S078). No other row's status, recheck, or used-by changed. S078 cells: tier A, status `mined`, opened `2026-10-24`, recheck `365d` (prose stripped), used-by `corpus/knowledge/search-log-method-r39.md`. Knowledge entry `recheck: 365d` matches. Lesson located quote is 12 words (≤25) and is the capture substring. The teaches cell is a 24-word paraphrase (`Design and keep…` is not a contiguous capture span). The contract's located quote lives in the Gate, and that quote checks. Not a second quote, and not a failed row.

Collision: `assimilation/collisions` is the single line `S077`. Renumber map keeps lane S077 as the pdftotext manual, refuses staged S077 (DOI bot wall), adopts staged S118's Europe PMC URL as lane S078, and refuses staged S078 (Cochrane) onto that id. Indented fixture collisions are `S077` and `S118`; column-zero ids are only `S077`. Handled by document, not by adding one to 118.

No new external fetch this round. Round-43 counters do not open the network. The only added `urlopen` is a copied historical file under `assimilation/validate/corpus/evidence/round29/c1-count.py`, not a round-43 fetch. This closure made no external fetch.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/search-log-method-r39.md` (lane S078, staged S118 by URL) | admit | `.qcache/2cef078d8f9f87802e19e770.txt` (sha256 `833b13e3…`, offset 17383); SOURCES row S078 | agree | Entry cites `source: S078 —` and not S118. URL matches the row. 12-word quote is in the capture. The two other sentences named in the entry are also in that capture (offsets 17628 and 44580). Recheck `365d`, used-by the entry. |
| `search-log-fields-r36.md` | reject | `.qcache/01f657b3d0ab045c494b3f92.txt` (267 bytes, 265 chars) and `.qcache/02b3b0e812df68ca305c7bc3.txt` | agree | Staged S077 capture contains `Client Challenge` and does not contain `PRISMA`. Japanese capture (6333 bytes) does not contain `参照日`. Admitting the field list would cite an unreopened article. |
| `search-tracking-record-r40.md` | reject | `.qcache/0ae65ac01b93119d3c2f3fed.txt` (27737 bytes; URL sha256 prefix of the JMLA PDF) | agree | Exact span `should be reported in Column 2` is absent. `Column 2` occurs 9 times and `reported in Column 2` once, so the column claim is not a contiguous sentence in this rendering. |
| SOURCES S078 row | new row | same Europe PMC capture; lesson Gate quote | agree | ≤25-word located quote is in the capture. Recheck normalized to `365d`. used-by is only the admitted entry. Teaches cell is a paraphrase, not that quote. |

## Wave reconciliation

Re-counted from committed bytes, not from the report's prose.

- `w1-spec.json` items 64. `w1-dispatch.json` and `w1-plan.json` `counts` `{spawn:64, resume:0, total:64}`; `taskCall.tasks` 64.
- Settle table 64 data rows: outcome `report` 48, `dead` 16. Roles: reviewer 8, critic 8, mutation-tester 6, sentinel 2, revenger 2 (attack 26, 40.6%); executor 12, scout 10, scribe 8, connector 4, simplifier 4.
- `w1/*.md` is 48 files. Every settle `report` name has a file. No dead name has a file. No file is outside the settle table. Dead seats were not replaced and are not credited.
- `w1/swarm-registry.json` has 64 members and every `agentId` is null, with no outcome field. That registry is a prepared spec, not a completion receipt. QUALITY 61 already says a spec is not a dispatch. Completion evidence used here is the 48 report files plus the settle table.

The report's waiter-parent / `pids 0` / `kimi --agent-file` sentences do not resolve to a committed script, log, or pid file (`git grep` of the tip for those strings hits the fleet report only). Seat counts above do not depend on that sentence. Routed.

## Trend verdicts

- **expansion: improved** — one new mined row (S078) and one admitted knowledge entry on ground the lane did not hold, citing that row. Census 77→78 by the report's counting command, re-counted on the archives.
- **quality: improved** — both split counters fail their do-nothing controls under this re-run; the admitted entry's quote re-checks in the capture; the 265/267 conflation was corrected by an append-only erratum (re-measured 267 bytes and 265 characters) rather than left unmarked. No admitted entry failed its re-check.
- **discernment: improved** — the lane reported `unchanged` because it had no outside review. This pass is that review. It agrees with the gate on the admit and on both rejects.

## Routed defects

Already filed, not duplicated: fetch-scope `8d77e6c1`; register staleness (`.ufo/l0-questions.md` chousa round-43); inherited r40/r41 working-tree disposition (same file). Those stay open.

1. Parent-lifetime receipt does not resolve. Next round must commit the launcher/waiter log (or stop asserting `kimi --agent-file`, `pids 0`, and a waiter parent). Seat counts are not this defect.
2. Freshness self-grade. Next scorecard must not call a pre-round cache open a freshness improvement. Closure grade is unchanged, not harmed.

Round-42 routes landed here and not re-opened: the absent-class split (9/6, flip fails); the 265/267 erratum; S077 collision by document. The r42 wave shortfall is partly closed (48 reports, 16 dead, not replaced) and the residual is defect 1.
