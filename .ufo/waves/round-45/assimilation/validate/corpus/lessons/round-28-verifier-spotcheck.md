# Round 28 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-22. Runtime model string exposed to this closure session: `anthropic/claude-opus-5-5`
(reached through the configured `task` route; no model parameter was passed).
Lane before `11d7c5da1ee7f6a4e01b1661d14a9d08fb8de01a`; lane after `7c87b9734eb71985e19767af36d57dff89536521`;
fleet report `.ufo/reports/round-28/chousa.md` at fleet commit `60f0810a1fbbff912fbf2865e734b02c8a873234`.
Driver digest (copied from `.ufo/watchdog.log` lines 645 and 654):
`2026-10-21T20:38:11-03:00 launch chousa round=28 pgid=2907258 driver=hyaku-inline attempt=1` and
`2026-10-22T04:58:59-03:00 complete chousa round=28; hyaku-inline attempt=1`.

Boundary: this check read only committed bytes in the lane and fleet repos plus the two opened
sources below. The private original report bodies, operational drafts, the unapproved ruler and
oracle, and the local author branches `hyaku/s3-chousa-r28-author` and `hyaku/s3-ready66-chousa`
were not opened, copied or run. Claims that rest only on those private bytes stay unverified here.

## Decision

**Status `ok`, not admitted: `rejected-honest-stop`.** The report records real committed work
(14 derived record paths at `7c87b973`), so it is not a marker. Its one declared claim, C1
operability, is reported by the author as not achieved, with no after value. I confirmed that
nothing in the landed diff could serve as an after value: no gate, tool or script changed. An
unmet claim cannot be admitted. No axis was harmed. No knowledge entry, capability, Core
graduation or promotion was added.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-28/chousa.md` (fleet) | `chousa-shokunin <chousa@shokunin.local> 60f0810a… 2026-10-21T23:59:41-03:00` | pass |
| `SHONEN` heading, one line per box | read report lines 88–95; `git show 7c87b973:SHONEN.md` | 4 report lines for 4 boxes, all `[~]`, matching the 4 `[~]` boxes in SHONEN.md; no `[x]` | pass |
| Cited lane hashes exist and are ancestors of the branch | report hashes are only `11d7c5da…` and `7c87b973…`; `git cat-file -t` → `commit` for both; `git merge-base --is-ancestor <h> master` → exit 0 for both (also against `origin/master`) | both resolve | pass |
| Lane pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=7c87b973… remote=7c87b973… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| | `git -C <lane> status --porcelain` | empty | pass |
| Lane commit precedes report | lane commit `7c87b973` at 23:47:56-03:00; report commit at 23:59:41-03:00 | ordered | pass |
| Prompt carries template contract | `.ufo/prompts/chousa-round-28.md` committed `001c34a6` (20:38:09, before launch); unified diff of `templates/round-prompt.md` against the prompt up to `## 6.` | 34 diff lines, all placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); sections 1–5 verbatim; addendum §6 appended | pass |
| Report sections in order | read report | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, SHONEN all present in order | pass |

Conformance defects (status-neutral, routed below):

- **D1, run-together tokens.** The report contains 23 distinct digit-glued tokens, for example
  `all69`, `proposal64`, `requested64`, `original187`, `legacy161` and `diagnosis53`. The lesson
  has more, such as `on2026-10-21` and `at most25 words`. Command: regex `\b[a-z]+[0-9]{2,}\b`
  over the report. This trips the goal contract's degraded-prose sentinel.
- **D2, custody vocabulary outside the canonical round.** The report, LOG, SKILL, README and
  lesson use "Parent approval", `CURRENT_MAIN_DIRECTIVE C28_NEGATIVE_PUBLICATION_v2`, private
  original hashes and "report-LAST" publication. These are session-3 custody layers that the
  canonical protocol and the hyaku addendum do not contain.
- **D3, stale statement in committed lane files.** `corpus/lessons/round-28.md` says "No end
  census has been run", and SCORECARD/LOG say no end census is authorised "at this stage". The
  fleet-committed witness `.ufo/waves/hyaku/chousa28-negative-records/parent-census.json` (fleet
  commit `b4b338e9`) records exit 0 against `7c87b973` at 2026-10-22T02:49:09Z. My own re-run
  below also gives exit 0. The lane statements were true when written, but they are now stale.
- **D4, no re-run in the report.** The report gives its SOURCES counting expression as "not a
  command rerun for this draft". PROTOCOL §Evidence standard says "Claimed ≠ re-executed". I
  re-ran the census, and the numbers match (below).
- **D5, long wall time.** 8 h 21 min passed from launch to the driver completion line. The
  report commit landed 4 h 59 min before the driver completion line.

## Claims — re-check against `7c87b973`

| Claim | Reported before → after | My measurement | Re-measured or evidence-verified | Verdict |
|---|---|---|---|---|
| C1 operability: canonical claim-source ancestor over-refusal plus complete denied-path attribution, with the original holds | before: R27 grouped receipt `.ufo/waves/round-27/residual/ResNoHarm.md:53–69`; after: none, "not achieved / unprovable" | `git diff --name-status 11d7c5da 7c87b973` lists only LOG, SCORECARD, SKILL, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-28.md` and 8 files under `corpus/evidence/round28-safe/`. No `tools/`, gate, script or `corpus/knowledge/` path changed. `git show 11d7c5da:.ufo/waves/round-27/residual/ResNoHarm.md` lines 53–69 hold the F2 table: 9 ancestor identities in one grouped row, base exit 0 versus dd/cb exit 1 `CLAIM_SOURCE_SESSION`. | Re-measured. The before resolves as cited. The absence of an after value is confirmed by the diff. | `unprovable`. Honest stop: the target as declared is not met. |

Supporting counts in the report that I re-derived (procedural only; none of them is a claim
after value):

- SOURCES census, using the CORPUS.md census commands over each revision's `corpus/SOURCES.md`.
  At `11d7c5da`: `rows=43 malformed=0 tier: A=37 B=1 C=5 status: mined=20 queued=19 rejected=4 dups:`
  (none). At `7c87b973`: `rows=45 malformed=0 tier: A=39 B=1 C=5 status: mined=22 queued=19 rejected=4 dups:`
  (none). This matches the report's "43→45 rows: A37→39 … mined20→22". The diff adds rows
  S044–S045 and one Search log paragraph. No earlier row changed.
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
  exit 0, `chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`.
- `corpus/evidence/round28-safe/native-seats.json`: 69 records, all `completed`. Phases: 64
  proposal-wave, 3 initial-data-walk and 2 ordinary-distillation-review. Roles: reviewer 25,
  scout 14, critic 9, sentinel 6, connector 5, revenger 3, executor 3, scribe 2, planner 1 and
  distiller 1. These match the report. Attack-role seats (reviewer + critic) are 34 of 69.
  I recomputed every `derived_record_sha256` under the stated hash rule (sorted keys, compact
  separators, the field itself excluded), and **69/69 match**. 3 records carry a null original
  hash, as disclosed. 2 records are marked VOID, as disclosed.
- All five JSON evidence files parse.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | `unprovable` | C1 has no after value. No gate, tool or script changed. |
| coverage | unchanged | `corpus/knowledge/` and `PROVINCE.md` are unchanged in the diff. |
| depth | unchanged | SKILL.md only gained an appended status section. No decision table or error pattern changed. |
| freshness | unchanged | No entry was re-verified this round. |
| calibration | unchanged | The SCORECARD diff appends one round-28 section and edits no existing score row. Every self-reported count I re-derived matches the repo (SOURCES, cohort, hashes, no-implementation), so I found 0 mismatches. D3 is a time-stale statement, not a false self-score. |
| adjacency | unchanged | No sibling-domain absorption appears in the diff. |

No axis is `harmed`. Command: `git -C chousa-shokunin diff 11d7c5da 7c87b973 -- SCORECARD.md`,
which shows only additions after line 1564.

## Discernment spot-check

Source: `corpus/lessons/round-28.md` `## Gate`.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S044 Python `os.path` docs, scoped to API semantics | admit (tier A docs, mined) | https://docs.python.org/3/library/os.path.html, opened 2026-10-22; page title "Python 3.15.1 documentation" | agree | The quote "Return the longest common sub-path of each pathname in the iterable paths." appears verbatim under `os.path.commonpath` (15 words, within the 25-word limit). The `commonprefix` entry says "This function may return invalid paths because it works a character at a time", which supports the row's `teaches` cell. Official documentation is primary for this API scope. The served version 3.15.1 matches the row's anchor. |
| S045 R27 canonical ancestor diagnosis, scoped to a historical record | admit (tier A own-work, mined) | `git show 11d7c5da:.ufo/waves/round-27/residual/ResNoHarm.md`, line 66 | agree | Line 66 reads verbatim "**The diagnostic misattributes the cause:** it says `path=src.md` when the denied component is the ancestor." The cited span 53–69 is the F2 finding. Tier A holds only for the narrow scope "what was recorded", because this is a review report rather than gate output. The row keeps that scope and grants no policy authority. |
| Reject: "API definitions as authority for a privacy exemption" | reject | same S044 page | agree | The `os.path` page defines path computation and says nothing about denylist or privacy policy. Using `commonpath` semantics to approve a root exemption would be an unsupported inference. |
| GNU manual requests that timed out | excluded, no row written | not re-opened (no URL committed) | agree | No row was written and no claim was derived from these requests. |

The spot-check agrees with the gate on 2 admits and 1 reject.

## Trend verdicts

- **expansion: unchanged.** `git diff --name-status 11d7c5da 7c87b973 -- corpus/knowledge` is
  empty. Two source rows are not expansion (CORPUS.md SOURCES rule 4).
- **quality: unchanged.** No entry was re-verified, deepened or superseded. QUALITY.md is
  unchanged. No entry was found false and left unmarked.
- **discernment: improved.** The outside spot-check agrees with the gate on admits and on a
  reject (LEARNING.md trend table, "improved when"). This rests on 2 scoped source admits and 1
  inference reject in a round that stopped. The author's own verdict was "unchanged".

## Routed defects (lane fixes next round)

1. D3: append a dated correction to LOG/lesson saying the end census ran (exit 0, witness
   `parent-census.json` at fleet `b4b338e9`). Do not rewrite the old entries.
2. D1: write separated tokens (`all 69`, `64 proposals`, `on 2026-10-21`) in new prose, and fix
   the spacing in rows S041–S045 through a superseding note if they are ever touched.
3. D2: stop carrying "Parent approval", directive IDs and private-hash custody prose into lane
   records. The canonical round, the addendum and this closure are the whole process.
4. C1 stays open. Next round: declare an after-state that one command over committed bytes can
   re-derive. The R27 C3 complete-path versus prefix-control conflict and the ancestor
   over-refusal (S045) are still unresolved. This is the same axis and surface for the second
   round running, so a third round on it would trip the frontier-rotation sentinel.
5. D4: the report's before→after counts must be re-run commands with their observed output.

SHONEN: the four boxes are all `[~]`, and their pointers are lane assertions. None can be
checked fully by a non-author from this round's bytes. No `[x]` was written. Promotion is
operator-owned.
