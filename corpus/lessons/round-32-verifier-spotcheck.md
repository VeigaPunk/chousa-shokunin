# Round 32 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-23 UTC (host clock UTC-3). Runtime model string exposed to this closure session:
`anthropic/claude-opus-5-5`, reached through the configured `task` route; no model parameter was
passed. Round 32 ran twice: attempt 1 (`ChousaR32-16`) landed `4111607c` and died with the
orchestrator at 06:19:06Z; attempt 2 (`ChousaR32A2`) produced the report. This closure used no
work of either attempt's seats.

Five read-only reviewer seats re-checked parts of the evidence: R32C1Frozen, R32C2Confirm,
R32Chrono, R32Prompt, R32NoHarm. None died; none was re-sent. This closure did not execute the
lane's gate (`tools/research-gate.sh`) or its counters (`c1-count*.py`, `c2-count*.py`), per
PROTOCOL §Gate standard, Closure consequence. R32NoHarm ran the plain checker `q33-check.py` on
copies of two committed lesson revisions; that checker is not the gate. Driver digest, copied
from `.ufo/watchdog.log`:

```
2026-10-23T02:50:39-03:00 launch chousa round=32 pgid=1132756 driver=hyaku-inline attempt=1
2026-10-23T03:40:39-03:00 lane-dead-no-report chousa round=32; retry same round (hyaku-inline attempt=1: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z (attempt 1; landed commits kept, uncommitted files untrusted))
2026-10-23T03:40:41-03:00 launch chousa round=32 pgid=3141706 driver=hyaku-inline attempt=2
2026-10-23T05:02:15-03:00 complete chousa round=32; hyaku-inline attempt=2
```

## Decision

- Status `ok`, admitted **false**, verdict `rejected-honest-stop`.
- C1 operability meets its frozen predicate on the landed gate. `APPEND_SERIALIZED` goes from 0/24
  to 24/24 on gate `f4731885…03f0`, seeds 32101 and 32102. The counter bytes are the frozen v2
  counter (`e6bf9531…`). The repairs at `53cf649c` made the locked section stricter; they did not
  change the rule.
- C2 coverage does **not** verify. The lane reports this itself, and this closure confirms it. A
  control that opens no cited source scores 132/132 on the same unamended counter (`8ec1a1ed…`).
  That control ranks files by mtime/inode order, and the fixture writes the 36 resolvable sources
  first. The finding came after data, and the counter was not changed afterwards.
- No axis is harmed. Not every claim verifies, so the round is not admitted.
- Design v2 (`3d586d3a`, 06:59:48Z) came before every candidate receipt. The last control commit is
  `a065845a` (07:20:56Z). The first candidate receipt has utc 07:21:14Z. No control receipt was
  committed after a candidate receipt existed.
- The gate-layout hazard (flat `scratch/gate.sh` puts the `../outside` fixture inside LANE_ROOT)
  touched no counted score.

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H %cI' -- .ufo/reports/round-32/chousa.md` | `chousa-shokunin chousa@shokunin.local b6c90b5781c1… 2026-10-23T05:01:48-03:00`. That is after lane tip `aa472066` (05:00:47-03:00). `merge-base --is-ancestor b6c90b57 origin/master` rc=0 |
| `SHONEN` heading | `grep -n SHONEN .ufo/reports/round-32/chousa.md` | `123:## SHONEN`, four box lines, all `[~]`, matching the four `SHONEN.md` boxes verbatim. Every pointer resolves at `aa472066` (R32Prompt) |
| Cited lane commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` | 8/8 rc=0: 4111607c 3d586d3a f43dd5a3 a065845a 0f96bc1c 5d8a1707 53cf649c aa472066. `8d77e6c1` is a fleet-repo commit (round-29 L0 question), not a lane commit. `bfc0b02b` is a file SHA-256, not a commit: `sha256sum .ufo/waves/round-31/controls/MutOracleC1/v2/oracle-c1.sh` = `bfc0b02b83f5…c617` |
| Round commits authored by lane | `git log --format='%h %an <%ae> %cI' 7a7259f0..aa472066` | 8/8 `chousa-shokunin <chousa@shokunin.local>` |
| Pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=aa472066… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty (`--ignored`: only `.jj/`, `.ufo/interactive-sessions/`); remote `aa472066…` |
| Prompt carries template contract | diff of rendered `templates/round-prompt.md` against `.ufo/prompts/chousa-round-32.md` through `## 5` (R32Prompt) | `IDENTICAL`. §6 is the hyaku addendum and only adds. No L2 route table is quoted; the prompt defers to the host route table, as `MISSION.md` does. Prompt commits: `a993767` at 02:50:37-03:00 (attempt 1) and `dc07d57` at 03:40:39-03:00 (attempt 2). Each is 2 s before its launch line |

Conformance defects (status-neutral): none in step 1. Report defects are routed below (D2, D3).

## Claims — re-check against `aa472066`

Both claims rest on lane-owned counters that drive the lane gate. They are **evidence-verified**
from committed receipts, not re-executed. This closure and its seats re-measured the counter,
gate, and receipt bytes.

| Measurement | Command (lane root) | Observed |
|---|---|---|
| C1 counter frozen | `git log -- corpus/evidence/round32/c1-count-v2.py`; `git show {3d586d3a,53cf649c,aa472066}:…/c1-count-v2.py \| sha256sum` | One add-commit, `3d586d3a`. `e6bf95313ad6…d891` at all three revisions. That equals `counter_sha256` in both final receipts |
| C1 P1 text frozen | `git diff 3d586d3a aa472066 -- corpus/evidence/round32/claims.md` | +27/−0: a "Post-data notes" section appended. The P1 v2 predicate text is unchanged |
| C1 after | `jq '{label,predicate_holds,gate_sha256,counter_sha256}' .ufo/waves/round-32/measure/final/c1-s3210{1,2}.json` | `APPEND_SERIALIZED=24/24`, `true`, gate `f4731885…`, counter `e6bf9531…` on both seeds |
| Final gate identity | `git show {53cf649c,aa472066}:tools/research-gate.sh \| sha256sum` | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` at both |
| C1 before | `jq … controls/L1-design-v2/c1-base-s3201.json`; `git show 7a7259f0:tools/research-gate.sh \| sha256sum` | `0/24`, `predicate_holds=false`, gate `0bc318b3e74a…1258` = the base gate |
| C1 repairs keep the rule | `git diff 5d8a1707 53cf649c -- tools/research-gate.sh` | One functional hunk, inside the C1 critical section. The last-byte probe now reads `/proc/$$/fd/$jfd` instead of the path, so it probes the locked inode. A non-empty manifest that is unreadable under the lock is refused with exit 2. The probe and the append stay in one `flock -x` section on the manifest's own fd. The other hunks only renumber comments |
| C1 tally | census over every committed receipt with `label`+`gate_sha256` (R32C1Frozen, jaq) | `f4731885` ×3, all 24/24 (exact). `10f2fe12`: 20 receipt files, all 24/24 with counter `e6bf9531` (the report says ×18; D2). Every sub-24 receipt is on `0bc318b3`, a mutant, a control, or a gate-less summary row |
| C2 counter frozen | `git log -- corpus/evidence/round32/c2-count-v2.py`; `git diff 3d586d3a aa472066 -- …` | One commit, `3d586d3a`; empty diff. Blob sha256 `8ec1a1ed44f1…3c8a` |
| C2 before/after | `jq … controls/L1-design-v2/c2-base-s322{1,2}.json`, `measure/final/c2-s3211{1,2}.json` | Base 0/132 (record checks fail; raw hop matches 96). Final `EXEMPT_AUDIT_MATCH=132/132` on both seeds, gate `f4731885…` |
| C2 counterexample | `w2/CriticAxis32/metadata-control.sh`, `metadata-open.trace`, `control-metadata-s3232002{1,2}.json` | The control lists `root` with `os.scandir`+`stat` and takes `sorted(entries)[:36]` as positives. The trace shows two opens only: the record file and the root directory (`citation_source_open_count: 0`). Both seeds: `matched:132`, `predicate_holds:true`, counter `8ec1a1ed…` (the committed blob) |
| C2 cause | `c2-count-v2.py` `generate()` (lines 179–255) | R1/R2/R3 write the 36 resolvable sources first (lines 200–215). F1 and every negative that writes into `root` come after (216–255). Sequential `put_file` (188–192) therefore encodes the truth in mtime and inode order |
| C2 found post-data | `git diff --diff-filter=A 53cf649c aa472066`; `git ls-tree 5d8a1707 …/CriticAxis32` | All 13 `CriticAxis32/*` files first appear in `aa472066`; the directory is absent at `5d8a1707`. Receipt utc 07:29Z is after the candidate measurement commit (07:25:26Z) |
| C2 behaviour (axis judgment only) | `grep -E 'exempt' measure/post-falsify/selftest-f4731885.log` | `ok-case 229 chain-exempt-resolvable exit=1`, `230 chain-exempt-unresolvable exit=0`, `231 chain-exempt-judgment exit=0`, `232 chain-exempt-mixed exit=1`. The expected finding ids are committed in the gate (`research-gate.sh:7022,7060,7110`) |
| No harm | `cat measure/final/battery.out` vs `w1/ExecNoHarmBase32/` (R32NoHarm) | Final: claims-r2 17/17 CLEAN; chain-r3 17/22 CLEAN; broken 1/2 DRIFT; observable 3/3; r31 v2 120/120 ×2; v3 132/132 ×2. These are identical to the base battery on `0bc318b3`. The selftest went from 228 to 241 cases (`post-falsify/selftest-f4731885.log:243: PASS (241 cases, 0 skipped)`); the first 228 case lines are byte-identical to base. The 8 `measure/final/*.json` receipts all carry gate `f4731885` |
| SCORECARD | `git diff 7a7259f0 aa472066 -- SCORECARD.md` | One append hunk (`@@ -1802,3 +1802,52 @@`), +49/−0. Operability 3 → 3. C2 is recorded as **not verified**. No existing score is lowered |
| Registry home | `git diff 7a7259f0 aa472066 -- SKILL.md` | Selftest tally updated 228 → 241. New row "research-gate round-32 counters": verdict map, before-gate, pinned values `corpus/evidence/round32/claims.md` (design v2) |

### Chronology and layout (R32Chrono)

- Commits (UTC): `3d586d3a` 06:59:48Z, `f43dd5a3` 07:13:17Z, `a065845a` 07:20:56Z, `0f96bc1c`
  07:21:04Z, `5d8a1707` 07:25:26Z, `53cf649c` 07:47:11Z, `aa472066` 08:00:47Z.
- There are 80 candidate-gate receipts: `10f2fe12` ×67, `d13a76e3` ×4, `f4731885` ×9. Their utc
  values run from 07:21:14Z to 07:56:21Z. The latest control-receipt utc under `controls/` and
  `w1/` is 07:17:53Z. Control JSON adds by commit: 3 + 15 + 566 + 190, and 0 after `a065845a`.
  `w2/Chronology32.md` gives an 18 s gap, and this re-extraction reproduces it.
- Layout: the guard is at `c2-count-v2.py:284-294`. It sets `lane_root = dirname(dirname(gate))`
  and exits 2 before generating a fixture whose tmp dir lies inside that root. It is shown live in
  `w2/MutCounterC2v2/layout-guard-pristine.output.json` (`counter_rc 2`,
  `generate_reached:false`). Flat-path C2 receipts exist only under the **v1** counter (utc ≤
  06:54:28Z): `CtlC2WeakReaderB`, `CtlC2StatusBlindB`, `MutC2CounterB`. Every v2 C2 receipt uses
  a nested `*/tools/research-gate.sh` gate. That covers the base, the 10f2fe12 runs, the final
  runs, and the best controls (C1 12/24 `mkdir-spin/tools/…`, C2 126/132 `gates/*/tools/…`). C1
  has no out-of-corpus fixture, so the hazard does not apply to it. **No counted score used the
  flat layout.**

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| operability | improved | C1 meets frozen P1 v2 (0/24 → 24/24 ×2 on the landed gate, frozen counter). The disclosed behaviour changes (exit 2 on a flock-less host, or on a manifest unreadable under the lock) fail closed and are declared |
| coverage | unprovable-but-better | Non-author ruling, not admission. The frozen measure cannot discriminate: a no-reader control meets it. Committed selftest cases 229–232 do assert the audit's exit and finding id on resolvable, unresolvable, judgment and mixed exempt hops, and the no-harm battery is unchanged. The counter is weak; the gate is not shown wrong. That is better behaviour, but it is not proven by the declared measure |
| depth | unchanged | No depth claim; QUALITY 33–35 were appended without changing existing rows |
| freshness | unchanged | S001–S059 untouched; no recheck changes |
| calibration | unchanged | No calibration claim |
| adjacency | unchanged | `PROVINCE.md` unchanged (`git diff 7a7259f0 aa472066 -- PROVINCE.md` empty) |

## Discernment spot-check (`corpus/lessons/round-32.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S060 Python `fcntl` docs | admit, tier A, call shape only | `curl https://docs.python.org/3/library/fcntl.html` → 200, sha256 `0189dd49…1e56` (the footer-clock variant the lesson names) | agree | The tag-stripped body contains "Perform the lock operation operation on file descriptor fd" exactly once (`grep -cF` = 1), under `fcntl.flock(fd, operation, /)`. "Acquire an exclusive lock." also appears once, under `fcntl.LOCK_EX`, inside `fcntl.lockf`'s cmd list. The corrected row places both quotes correctly. The page defers flock semantics to flock(2), so "call shape only" is the right scope |
| S061 RFC 9110 | admit, tier A, origin-server semantics only | `curl https://www.rfc-editor.org/rfc/rfc9110.txt` → 200, sha256 `21c1cdce…47232a` (matches the row) | agree | "resource is no longer available at the origin server" is found once, at line 7670, in §15.5.11 "410 Gone". The row marks the local-copy reading as lane inference, which is correct: the RFC says nothing about local copies |
| Wikipedia "Link rot" | reject (not opened; lower tier than RFC 9110 for the same point) | `curl -A … https://en.wikipedia.org/wiki/Link_rot` → 200 | agree | The page is tertiary. It mentions 404 only in passing ("returning an error such as HTTP 404") and has no status-code semantics beyond what S061 states primarily |
| Design v1 C1 counter | reject as P1 counter | `jq` on `w1/CtlC1PartialLockB/b-s3247102{1,2}.json` and `v2/mutated-b-probe-only-s3247202{1,2}.json` | agree | The probe-only control gate `034f786b…` scores `APPEND_SERIALIZED=24/24`, `predicate_holds=true`, under counter `9e787e80…`, which is `git show 4111607c:corpus/evidence/round32/c1-count.py \| sha256sum`. Under v2 (`e6bf9531…`) the same gate bytes score 0/24. The v1 counter accepted a wrong gate |

Newly written row re-opened: S060 (`corpus/SOURCES.md:70`) and S061 (`:71`). Quote lengths: 9, 4
and 9 words (`wc -w`), all ≤25.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` printed
`W04 S051 …`, `W04 S053 …` (pre-existing duplicate-URL warnings) and `chousa ok …`; exit 0. Rows
59 → 61 (`grep -c '^| S0' corpus/SOURCES.md` at `7a7259f0` and at `aa472066`).

## Trend verdicts

- **expansion: improved.** There are two new knowledge entries:
  `corpus/knowledge/manifest-append-lock-r32.md` (source S060) and `exempt-hop-audit-r32.md`
  (source S061). Both have `verified-at: 2026-10-23`, and both rows are `mined`. Both sources were
  re-opened above, and the quotes were found. The capability "serialized manifest appends" is
  backed by passing receipts on the frozen counter.
- **quality: improved.** Round-31 routes R1–R6 are repaired. R1: `q33-check.py` prints FAIL (exit
  1) on the `4111607c` lesson and PASS (exit 0) on `aa472066` (R32NoHarm). R2: v3 counter hashes
  match the record. R5: the `bfc0b02b` file hash checks out. QUALITY 33–35 were appended (+23/−0),
  each with a shown-able-to-fail check. No admitted entry failed its re-check.
- **discernment: improved.** This spot-check agrees with the gate on two admits and two rejects.
  The lane's own catches are recorded with evidence: the C2 metadata shortcut, two source
  over-reads corrected before filing, four mislabeled receipts in `CORRECTION.md`, and two C1
  contract breaks repaired. C2 is reported not verified rather than re-scaled. Limit: the C2
  counter flaw reached data, and its proposed criterion is not yet shown able to fail (D1).

## Disclosed round incidents (status-neutral)

- RerunC1b ran `pkill -x sleep`, which killed three sibling `sleep` processes. The lane disclosed
  this. This closure did not trace which sibling runs were affected.
- Three safety-filter holds (`code=cyber_policy`) were not retried: CtlC1ShortcutB,
  CriticPredicateGaps32b, and CtlC1JitterB's v2 re-score wake. Its v1 receipts stand (best 11/24).
- Four receipts on the uncommitted intermediate gate `d13a76e3` are excluded from landed-gate
  evidence, as the report says.

## Routed defects (lane fixes next round)

- **D1 (C2 measure).** Decouple fixture metadata from truth: shuffle creation order and randomise
  mtime/inode order across classes. Score the exact `w2/CriticAxis32/metadata-control.sh` control
  against the new counter before freezing. Land the lesson's proposed criterion as a QUALITY row
  only once it is shown able to fail. Until then, C2's "exempt-hop audit" capability carries no
  counter verification.
- **D2 (report tally).** The report and SCORECARD give "`10f2fe12` ×18" committed C1 receipts. A
  census finds 20 receipt files on that gate, all 24/24. The extra two are critic re-scores,
  apparently excluded under an unstated convention. Evidence standard: a numeric claim carries its
  counting command. State the census command, or correct the count in an appended note.
- **D3 (battery revision binding).** `measure/final/battery.out` has no `gate_sha256`/lane-rev
  header; the base battery logs have one. Gate standard: a verdict names the revision it was
  measured against. Add the header to future battery outputs.
- **D4 (carried).** Nested `"line"`/`"sha256"` keys are still read as the record's own (unanchored
  `json_str`/`json_has_key`). The lane already carries this into its round-33 plan.
- **D5 (seat hygiene).** Seats must not signal processes by name on the shared host (`pkill -x
  sleep`). Scope kills to the seat's own PIDs or process group.

## Operator note (SHONEN)

No box is fully checkable by a non-author as filed. Box 4's sub-claim "`PROVINCE.md` unchanged" is
mechanically true. Box 3's `--selftest` can be re-run by a non-author but was not re-run here. The
other boxes need domain judgment. Promotion is operator-owned.
