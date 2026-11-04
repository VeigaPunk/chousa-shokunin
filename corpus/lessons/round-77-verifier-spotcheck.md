# Round 77 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed round 77: before `6defa58dbdc40856f4e7dd24df98dc7ebd3459c0`, controls
`e6fcdc4770c2fa73e5ccda99445c4311128d7e0d`, claims freeze `a9530782578723de1364e0a3a47effcde8c85c23`,
dispatch/ready `9fcfb70ba6f202506dfd55f71917dc2d31b3f825`, landing `9874f46d21139dcfa9ca496ad831c4b9300c3d8b`,
final tip / lane HEAD `958a6023c376f4142dd5d995e88754d9e391c6f6`. This review neither improves the
authored round nor re-admits any earlier round. Two read-only `reviewer` seats re-checked the C1
evidence set and the Gate decisions independently; the axis/scope audit seat failed on a provider
auth error and that audit is mine below.

## Conformance and disposition

Status **ok** — a landed report naming checkable committed work, not a marker. Admission **true**,
verdict `admitted`: both declared claims verify, and no owned axis is harmed.

- `git log --format='%an %ae %H %ci' -- .ufo/reports/round-77/chousa.md` (fleet repo) returned
  `chousa-shokunin chousa@shokunin.local e915f43a1c14556829ef9dae82e53af57d31c709 2026-11-04 19:33:02 -0300`.
  The lane tip `958a6023` is 19:32:37, so the report lands last. `git branch -r --contains e915f43a`
  lists `origin/main` and `origin/master` — the report is pushed.
- `scripts/hyaku/jj-lane.sh state …/chousa-shokunin` printed
  `branch=master local=958a6023 remote=958a6023 ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git -C …/chousa-shokunin status --porcelain` printed nothing — no uncommitted round work.
  `git ls-remote origin refs/heads/master` printed `958a6023c376f4142dd5d995e88754d9e391c6f6`, the
  hash the report cites.
- `git merge-base --is-ancestor <hash> refs/heads/master` exited 0 for all five cited hashes
  (`e6fcdc47`, `a9530782`, `9fcfb70b`, `9874f46d`, `958a6023`) plus `6defa58d` and `a519fb0a`; every
  hash exists as a commit authored by `chousa-shokunin`. Ancestry tested against the branch ref,
  never `@{u}` or detached HEAD. `git log 6defa58..958a6023` shows the five round commits, 18:35:40
  → 19:32:37, all lane-authored.
- The report carries `## SHONEN` once with four `[~]` rows, matching the four `- [~]` boxes in
  `SHONEN.md`; the lane wrote no `[x]`. Sections present in order: Work performed, Landed changes,
  Before → after measurements, Sources & frontier, Trend verdicts, SHONEN. Each `[~]` pointer
  resolves: `SKILL.md` `## Decision table` (13), `## Error patterns` (41), `## Checklist
  (executable)` (67), `## Gates` (79); `corpus/fixtures/archives-r9/`; `LOG.md` `## Round 9`;
  `corpus/evidence/round73/controls/preflight-r73.txt`; `PROVINCE.md`.
- Prompt `.ufo/prompts/chousa-round-77.md` is committed by `chousa-shokunin` at `ca72d08d`, 18:04:48 —
  two seconds before the `launch chousa round=77` line. Lines 1–140 are `templates/round-prompt.md`
  with substitutions only (`diff` of the two 140-line windows shows only the `{{LANE}}`/`{{ROUND}}`/
  `{{FLEET_ROOT}}`/`{{AXES}}` fills), so it carries the round-level contract (§1 mission/axes with
  1–3 claims and the lowest-axis duty, §3 the ≥8 one-batched-call L2 floor, §5 commit-then-push and
  push scope, §5 L0 side channel) and the five child-lane items (report path §4, report-lands-last
  with the pushed-hash citation §4, `SHONEN` heading §4, write scope §5). `MISSION.md` §L2 holds no
  alias table — its routing block is bucket-level and advisory (`planner/connector` heavy,
  `executor/scribe/scout` fast, `reviewer/critic/sentinel/revenger/labrat/mutation-tester/simplifier/
  distiller` economy) — so the addendum's alias maps can only be graded for bucket consistency, and
  they are consistent; the prompt quotes no conflicting route map.
- Misroot: fleet `git status --porcelain` shows only orchestrator-owned `.scratch/` entries, a
  modified `.ufo/reports/round-84/kama.md` and a pre-existing untracked `after`; no path names chousa
  or round 77. No file outside the lane repo carries round-77 chousa work.

Conformance defects (status-neutral, routed below): the SKILL registry row's missing owner cell and
absent self-test mode, a mis-resolving QUALITY 142 evidence pointer, a stranded `## Mistakes` row in
the round lesson, census receipts without their exit-code line, and one imprecise sentence in the
frozen claims prose.

## Claim re-checks

C1 is **evidence-verified**, C2 is **re-measured** by me. `matrix-battery-v4.py` is a registered gate
(`SKILL.md` row `round77 order-and-content battery`), so per PROTOCOL §Gate standard (Closure
consequence) I verified its committed evidence — receipts, frozen-run verdict, revision measured —
and did not execute it.

### C1 — operability (lowest scored non-retired axis, 3/10 held)

| step | command | observed |
|---|---|---|
| instrument binding | `sha256sum corpus/evidence/round77/matrix-battery-v4.py corpus/evidence/round76/loader-matrix-v3.py corpus/evidence/round77/forgers/forge-order-matrix.py` | `155fafb1…f106a3d`, `b79d6441…05c81913f`, `e7a12850…b767801c6` — byte-identical to every digest the claims file and the receipts assert |
| before | `controls/before-oracle-v3-committed-bytes.txt` tail | `BATTERY=PASS forgers_rejected=11/11 positive=2/2`, `# exit: 0`, lane rev `9fcfb70b`; the matrix under test is the committed `forge-order-matrix.py` (`MATRIX_SHA256=e7a12850…`) |
| after (predicate) | `controls/after-battery-v4.txt` tail | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`, `# exit: 0`, battery sha `155fafb1…`, matrix sha `b79d6441…` |
| the same forged matrix as matrix-under-test | `controls/forge-as-matrix-summary.txt`, `controls/forge-as-matrix-table.txt` tails | both `BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=REJECTED`, `# exit: 1` |
| order leg load-bearing | `controls/twin-no-permute.txt` tail | `BATTERY=FAIL forgers_rejected=11/11 positive=2/2 oracle=MISS`, `# exit: 1` |
| content leg not the discriminator (disclosed) | `controls/twin-no-content.txt` tail | `BATTERY=PASS … oracle=REJECTED`, `# exit: 0` |
| guard shown able to fail | `controls/mutant-missing-subject.txt` tail | `matrix-battery-v4: missing subject …forge-constant-pass-missing.py`, `# exit: 2` |
| code claims | `grep -n 'randbits\|CONTRACT\|no-permute\|no-content' corpus/evidence/round77/matrix-battery-v4.py` | `random.Random(secrets.randbits(64)).shuffle(order)` (180); twelve-entry `CONTRACT` map (99); `--no-permute`/`--no-content` (216–217) |

Before→after holds on committed bytes with the same forged oracle (`e7a12850…`) on both sides: the
r76 battery passes a matrix that scripts its verdict by invocation count, the v4 battery refuses it,
and the order leg is the closure that does the refusing. Verdict **improved (narrow)**.

Two limits the round states and I confirm: the content leg is a shape requirement (the `--no-content`
twin still passes), and the claim's supporting sentences are falsified by the wave critic —
`rcpt-a1.txt`/`rcpt-a7.txt` reach `BATTERY=PASS …` at exit 0 without scoring a subject (I re-read the
tails: both end on the exact predicate line). The round records that as an instrument limit and as
QUALITY 143 rather than amending frozen bytes after scoring, and its verdict paragraph says C1 "must
not be read as 'the battery cannot be passed by a forgery'". That is the honest reading and it is the
reading I grade.

### C2 — calibration

| step | command | observed |
|---|---|---|
| after (mine) | `python3 -B corpus/evidence/round77/c3-count.py --lane . --base a519fb0a… --rev 9874f46d…` | `C3-1…C3-5 PASS`, `C3=PASS checks=5/5`, `rc=0` |
| before (mine, derived) | `git show 6defa58:corpus/evidence/round76/claims.md \| grep -c '^## Correction'`; `git diff --numstat a519fb0a 6defa58 -- corpus/evidence/round76/claims.md` | `0`; empty (0/0) ⇒ C3-2/3/4/5 fail and C3-1 passes ⇒ `C3=FAIL checks=1/5`, matching `controls/before-c3.txt` |
| superseded clause | `grep -n 'receipt precision' corpus/evidence/round76/claims.md` | line 10 (frozen bytes, unchanged) and line 118 (quoted in the correction block) |
| append-only | `git diff --numstat a519fb0a 9874f46d -- corpus/evidence/round76/claims.md` | `12 0` — twelve added, none deleted |
| block position | `grep -n '^## ' corpus/evidence/round76/claims.md \| tail -2` | `## Shared boundaries`, then `## Correction — round-76 claims prose` (115) as the last section |

The false clause is real: the prefreeze receipts name worktree digests and lane revs
(`# lane rev: 6defa58…`, `# oracle sha256: 9bb74e2a…`), not the controls revision, so the frozen
sentence "4 (receipt precision) is honoured by naming the controls revision in every receipt" is
false and the correction block states the corrected fact. Verdict **improved**. The counter is
lexical, as the lesson says: it proves presence, position, quote, phrase and numstat, not the truth
of the corrected sentence.

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** (narrow) | C1 before→after above; the historical numeric 3/10 is deliberately held (0 deletions anywhere in `6defa58..958a6023`, so no score was rewritten) — the SCORECARD row records the verdict with a delta of 0 rather than a re-measured number |
| calibration | **improved** | C2 above; a false sentence in the lane's own frozen prose is corrected append-only and re-derived by a committed counter |
| depth | unchanged | no knowledge entry, decision table or error-pattern row added; `corpus/knowledge/` absent from the round diff |
| coverage | unchanged | `PROVINCE.md` untouched; frontier ground not advanced (the round says so) |
| freshness | unchanged | instruments are revision-pinned and re-measured at the landing, but no drift detector was added |
| adjacency | unchanged | `R77ConnectorA` read the sibling set and absorbed nothing; no sibling file in the diff |

No axis is harmed: the round diff is `+6610 -0` over 93 files — **zero deletions**, so no SCORECARD
score, QUALITY criterion, SOURCES row or LOG entry was rewritten in place. `corpus/knowledge/`,
`corpus/README.md`, `PROVINCE.md` and `SHONEN.md` are absent from the diff.

## Spot-check — gate decisions re-opened (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S190 — the r76 spot-check's routed defect 1 | admit (own-work, B) | `git show 6defa58:corpus/lessons/round-76-verifier-spotcheck.md` line 150 | **agree** | quote present verbatim inside the bold lead of routed defect 1; span 150–155 exact; `wc -w` = 10. A closure record naming the defect is a legitimate B anchor for the claim's *target* — and the lesson says exactly that, that it is not proof the successor closes it |
| S191 — routed defect 3, the false frozen sentence | admit (own-work, B) | same file, lines 163–164 | **agree** | quote spans the wrap exactly as the Gate says ("…naming the" / "superseded text…"); `wc -w` = 11, so the Scribe's correction from 12 to 11 is right and the row carries 11 |
| S192 — this round's own frozen claims file | reject (own-work, C) | `git show a9530782:corpus/evidence/round77/claims.md` line 1 | **agree** | heading present byte-identically (em dash, curly apostrophe); citing a declaration as evidence its predicate holds is circular, the r76 S189 precedent applies, and the recorded flip condition is coherent |
| new-row quotes ≤25 words | — | S190/S191/S192 `teaches` cells | **agree** | each `teaches` is one grounded benefit; the anchors carry revision, line numbers and quote location; `used-by` for the two admits resolves to `corpus/lessons/round-77.md` |
| census | — | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | **agree** | `EXIT=0`; five `W04` duplicate-url warnings, all on pre-existing ids S051/S053/S073/S074/S075, none on S190–S192 |
| registry counts | — | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at HEAD vs `git show 6defa58:…` | **agree** | 192 vs 189; tier `A=123 B=52 C=17` vs `A=123 B=50 C=16`; status `mined=154 queued=19 rejected=19` vs `mined=152 queued=19 rejected=18` — the report's numbers reproduce exactly |

An independent `reviewer` seat re-opened the same three items and reached the same verdicts
(agree/agree/agree), including the 10- and 11-word counts and the exact spans.

## Trend verdicts

- **Expansion: unchanged.** No admitted `knowledge/` entry, no capability row, no province ground:
  `git diff --name-only 6defa58 958a6023` lists no `corpus/knowledge/`, `corpus/README.md` or
  `PROVINCE.md` path. The three registry rows are curation (two admits, one rejection), and a
  rejection is evidence of taste, not expansion.
- **Quality: improved narrowly.** A weaker instrument is superseded by a stronger one with the
  weaker behaviour re-measured on the same forged bytes (`BATTERY=PASS` → `BATTERY=FAIL` at exit 1),
  the closure-removal twin shows the order leg load-bearing, and QUALITY 141–143 are appended with
  lesson grounding. Nothing was weakened: zero deletions in the round diff, and the two instrument
  defects the wave found (a caller's `--work` deleted by `finally`; an unwritable `--work` exiting 1
  instead of 2) are mined and carried rather than left unmarked.
- **Discernment: improved.** This non-author spot-check agrees with both admits and the reject
  (table above); two of the round's own slips — a probe writing into the lane, a control receipt
  naming a digest no committed object carries — were caught and mined before landing, and the Scribe
  corrected a quote count from 12 to 11. The wave critic's falsification became QUALITY 143 and a
  recorded limit instead of a narrowed claim.

## Routed defects (owner chousa, next round)

1. **`SKILL.md` registry row `round77 order-and-content battery` is missing its owner cell.**
   `awk 'NR==154{gsub(/\|/,"|")} END{}'`-style cell count: header line 154 has 8 cells, row 168 has
   7; the row ends at write scope and no `| chousa |` closes it. Fix: append the owner cell (a new
   row naming the row it corrects, or a registry correction line), since the registry is
   append-only evidence.
2. **The registered gate has no self-test over isolated fixtures.** `matrix-battery-v4.py` exposes
   only `--matrix/--work/--runs/--matrix-timeout/--no-permute/--no-content`; the registry's
   "self-test" cell names the predicate and the twins, and the source's own docstring calls the
   twins "mutation evidence, never the predicate". §Gate standard (Self-test) requires a
   self-invocation mode asserting both exit code and a stable expected finding-id over temp trees.
   Ship it, or re-register the row as a `probe` with the reason. The same row's exit map should also
   name the non-argparse exit-2 paths (`missing matrix`, `missing subject`, `missing oracle`,
   non-positive `--runs`/`--matrix-timeout`).
3. **QUALITY 142's evidence pointer does not resolve.** The row cites `R77SentinelA` S1/S2,
   `receipts/02c-work-unwritable.*`; no such file exists — `02c` is `02c-work-is-file.stderr`, and the
   unwritable cases are `receipts/02b-work-unwritable.stderr` and
   `receipts/02j-work-existing-unwritable.txt`. Under §Evidence standard an unreachable pointer does
   not exist. Fix by a criterion row that supersedes 142 and names the resolving receipts.
4. **`corpus/lessons/round-77.md` `## Mistakes` is structurally broken.** The header and two rows sit
   at lines 40–43; the third row (the control-receipt digest slip) is stranded at line 73, after the
   `## Boundaries` paragraph, so it renders as literal text and the mined mistake is easy to miss.
   Fix in the next lesson with a correction entry that names the stranded row, or an erratum block
   appended after the filed bytes.
5. **The census receipts carry no exit code.** `.ufo/waves/round-77/census-{start,end}.txt` hold the
   six output lines but no `EXIT=` line, while the frontier step requires both outputs *and* their
   exit codes. The report's `EXIT=0` is true — my run printed `EXIT=0` — but the receipt is not
   self-contained, unlike `controls/*.txt`, which all end `# exit: N`. Add the exit line at write
   time.
6. **`c3-count.py`'s tree side follows the working tree, not a pinned revision.** Run at HEAD with
   `--rev a519fb0a` it prints `C3=FAIL checks=4/5` (C3-4 alone failing) because checks 2/3/5 read the
   worktree, so a before-state receipt is reproducible only from the before revision. This is the
   r76 routed defect 2 class ("the lane leg follows a moving ref") one layer out. Fix: take a tree
   revision (`--tree REV` or read every check through `git show`), so a receipt names one revision
   for both sides.
7. **Frozen prose imprecision, recorded not amended.** `corpus/evidence/round77/claims.md` says the
   battery "runs the eleven round-76 forgers and two positives — byte-identical sources under
   `corpus/evidence/round76/`"; the positives are `corpus/evidence/round74/correction-count.py` and
   `corpus/evidence/round75/ref-counter.py`. Byte-identity holds (13/13 sha256 prefixes in
   `before-oracle-v3.txt` match committed bytes); the path grouping is loose. Also `claims.md`'s
   Before paragraph cites `before-oracle-v3.txt` without the caveat that its oracle is a pre-guard
   scratch copy (`9bb74e2a…`), which only the receipts disclose. Frozen bytes stay frozen; record the
   correction in the next lesson.
8. **Wave settlement attestation, recurring.** `w1-results.json` carries 12 entries with
   `output: null`; five seat reports are retained (`R77ConnectorA/CriticA/ScoutA/ScribeA/SentinelA`)
   and seven seats settled with no retained terminal record — the r76 routed defect 5 again. The
   round records it instead of glossing it. Fix: make the seat's `Report:` trailer path mandatory at
   settle time (the wave spec already carries the path) so evidence survives an orchestrator kernel
   restart, rather than relying on `output` capture.

## Notes for the operator

The four `SHONEN.md` boxes now look checkable by a non-author reviewer from committed artifacts
alone: `SKILL.md` carries the decision table, error patterns, executable checklist and gate registry
with resolvable sources; an end-to-end task is logged (`LOG.md` Round 9 with
`corpus/fixtures/archives-r9/`); executability is receipted
(`corpus/evidence/round73/controls/preflight-r73.txt`); and `PROVINCE.md` plus the round-77 lesson's
Boundaries section bound the domain. This spot-check writes no `[x]` and makes no promotion ruling —
promotion is operator-owned.
