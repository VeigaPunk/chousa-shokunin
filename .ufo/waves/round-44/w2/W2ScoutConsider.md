# W2ScoutConsider — which 2026-10-24 proposal round 43 mined

Seat: W2ScoutConsider (scout, leaf). No subagent dispatch.
Axes walked: operability (the mined name is a committed citation, and the round-42 shortfall it points at was re-counted here), calibration (the source file still says "not acted on"; mining is not the bullet's full wording; a draft prompt is not a landed criterion), depth (the four bullets, the narrowing, and the two siblings that are also still unimplemented).
Milestone: Round 44 wave 2: genuine seats after the usage-error wave.
Measured HEAD: `043f19a1db91288947493d9f879e61e7a9f07241` (`round-44: freeze parent-lifetime, disposition, and RFC quote claims before scoring`, 2026-10-24 21:46:56 -0300). This seat did not commit, did not run `jj`, and did not edit `considerthese/2026-10-24.md` or any other production file.

No lane production file, git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` was written. No network. No fetch. No install. Pacman was not invoked. The only file written is this report.

## Answer

- **Already mined by round 43:** **Track prepared-but-undispatched waves** (`considerthese/2026-10-24.md:60-61`). Landed as QUALITY criterion 61 in commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
- **Still unimplemented (the one named here):** **Count claim errata per round** (`considerthese/2026-10-24.md:62-63`). It is not a QUALITY criterion. `corpus/QUALITY.md` still ends at criterion 61.

The other two bullets in that section are also unimplemented. They are named below so "one" is not read as "the only one left."

## The four bullets, as the file still prints them

`considerthese/2026-10-24.md:56` still heads the section `## Self-improvement proposals (not acted on)`. That heading was not revised after round 43. The four bullets are:

1. **Tag each round as research ground or plumbing.** (`:58-59`) One ledger column: new research coverage, or hardening the gate's own tools.
2. **Track prepared-but-undispatched waves.** (`:60-61`) A fixed line listing waves that were validated but never ran, and seat reports left uncommitted, to surface the L2 gap from rounds 39-41 the day it happens.
3. **Count claim errata per round.** (`:62-63`) Round 35 needed nine. Erratum density as a daily calibration signal: a round whose claims need many narrowings after freezing was frozen too broad.
4. **Spot re-verify one receipt a week.** (`:64-66`) A read-only run of the latest `verify-receipts.py` over a sample of receipts. The author says this needs approval, because it goes beyond the then read-only remit.

File sha256 `5837fc7de0a5456072592e1b5d332dc1fb3eb51bfc6f5ca2680e72347a7696ba`. Last commit touching that path: `ab9d3fdd6b9238956b14d9544e64cbee3a9aa919` (`considerthese: 2026-10-24 daily review (rounds 34a2-41)`). `git status --porcelain` on `considerthese/2026-10-24.md`, `corpus/QUALITY.md`, `corpus/lessons/round-43.md`, and `LOG.md` printed no lines. The source file's own "not acted on" label is stale for bullet 2 and still true for bullets 1, 3, and 4.

## Mined: Track prepared-but-undispatched waves

`git blame -L 542,552 -- corpus/QUALITY.md` attributes every line of criterion 61 to `737f40b` (`round-43: split the absent class and adopt one locally re-opened search-log entry`, 2026-10-24 20:52:23 -0300). `git log -1 -- corpus/QUALITY.md` is that same commit. A pickaxe for the contiguous string `Track prepared-but-undispatched waves` returns nothing, because the citation is split across lines 551-552. The pickaxe for `Track prepared-but-undispatched` returns `737f40b`.

Verbatim criterion, worktree sha256 `1c20bb39ad604699198b2622f47d22be8126aa6bc2ea200e38c679ebedf50511` (same bytes the round-43 scribe recorded; this seat re-hashed, it did not copy that hash on faith):

```
61. **A validated wave spec is not a completed dispatch.** A spec, a plan, and a
    registry whose agent ids are null are preparation. A dispatch is complete only
    when the dispatcher stayed alive until each seat settled, and the record names
    the seats that returned a report and the seats that died. Counting a prepared
    spec as a dispatched wave hides the shortfall. Check: the round report's wave
    section cites seat reports or names the dead seats with their last error; a
    registry of null ids with zero reports is a shortfall, not a completed wave.
    Shown able to fail: round 42's `w1/swarm-registry.json` has 64 members and null
    agent ids, and zero seat reports landed. Operator proposal mined from
    `considerthese/2026-10-24.md` (2026-10-24), "Track prepared-but-undispatched
    waves". — `lessons/round-43.md`.
```

Same mining, two other committed sentences:

- `LOG.md:1553`: `QUALITY 61 mined from considerthese/2026-10-24.md: a validated spec is not a completed dispatch.`
- `corpus/lessons/round-43.md:26`: mistake class `prepared-as-dispatched`, fix `QUALITY 61; a spec is not a dispatch.` Lesson sha256 `ff8f54498ef7e8849a47e06cea1907a86b4720017fa3d1f87922a72a95f53adf`.

This seat's recount of the shown-able-to-fail registry (read-only; members is a dict keyed by seat name, not a list):

```
MEMBERS 64
AGENTID_NULL 64
AGENTID_NON_NULL 0
ROUND42_MD 0
```

`git ls-files .ufo/waves/round-42` printed seven paths and no seat-report markdown: `gen-w1-spec.py`, `w1-dispatch.json`, `w1-plan.err`, `w1-plan.json`, `w1-run.err`, `w1-spec.json`, `w1/swarm-registry.json`. The 64 / null / zero sentence holds on this worktree. That is this seat's count, not a re-run of a frozen counter.

### Narrowing (mined is not the bullet's full wording)

The bullet asked for a fixed line listing waves validated but never run, and seat reports left uncommitted, aimed at the L2 gap in rounds 39-41. Criterion 61 is a completion rule for a round report's wave section, and its shown-able-to-fail example is round 42's null-id registry, not the rounds 39-41 L2 gap.

Those earlier rounds already used the phrase before this file was mined. `LOG.md:1464-1465` (round 39) says the L2 floor was met by preparing a validated spec, `0 dispatched / 0 dead`, `prepared-but-undispatched itemized in the report`. `SCORECARD.md:2208-2210` says the same for round 39. That is the phenomenon the bullet names. It is not criterion 61, and it is not a daily fixed line added to the consider-file ledger. The consider file's own ledger (`:11-20`) is still `Round | Outside verdict | Key number`. No research/plumbing column, no undispatched-wave column, no errata-count column.

`SCORECARD.md:2376` records the mining as `quality improved (... QUALITY 61)`. It does not claim the bullet's fixed line now exists.

## Still unimplemented: Count claim errata per round

Named because it is the bullet a later round-44 seat was told to draft from, and because the production tree still has no such criterion. Drafting is not landing.

Evidence it has not landed:

- `corpus/QUALITY.md` is 552 lines. The last heading matching `^[0-9]+\. \*\*` is line 542, criterion 61. Headings 6 through 61 are 56 such lines (`rg -c` printed `56`). Criteria 1-5 use a different heading form and were not re-read this seat. There is no criterion 62 in the file.
- `git log -1 -- corpus/QUALITY.md` is `737f40b`, the round-43 commit. HEAD `043f19a1` (round-44 freeze) did not append a criterion.
- Exact title `Count claim errata per round` outside `.ufo/` hits two paths only: `considerthese/2026-10-24.md` and `corpus/evidence/round44/seat-logs/ScribeQuality62.prompt`. That prompt says `Draft QUALITY criterion 62 from the unimplemented considerthese proposal "Count claim errata per round"` and `Do not edit QUALITY.md or considerthese`. A prompt that forbids the edit is not an implementation. This seat did not read a landed `W2ScribeQ62.md`; absence of a sibling report is not evidence either way, and was not treated as one.
- No `erratum density` or `claim errata per round` hit in `corpus/lessons/`, `SCORECARD.md`, or `LOG.md` except the consider file itself (the production-title search printed only the consider file and that prompt).

Round 35's "nine" is the consider file's number (`:62`, and `:14` "nine claim errata (7-15)"). This seat did not re-count those errata. An unrun check has not passed. The unimplemented claim does not depend on that nine being re-derived.

## The other two, also unimplemented

Not the one this report is required to name. Recorded so the census is not a single-bullet search.

- **Tag each round as research ground or plumbing.** Exact title outside `.ufo/` hits only `considerthese/2026-10-24.md`. `SCORECARD.md:2198` contains the word `plumbing` in `--tmp plumbing` (dead-field deletions). That is not this bullet. The round-43 verdict table (`SCORECARD.md:2359-2363`) is `claim / axis | before → after | counting command | verdict`. No research-ground column. The consider file's ledger was not given one either.
- **Spot re-verify one receipt a week.** Exact title outside `.ufo/` hits only `considerthese/2026-10-24.md`. The bullet itself withholds the run pending approval. Repo search found `corpus/evidence/round38/verify-receipts.py` and `corpus/evidence/round39/verify-receipts.py` as round-scoped counters, not a weekly sample runner. This seat did not search crontab, systemd timers, or a cloud-agent schedule outside the repo. Absence in the repo is not proof that no external job exists. No QUALITY criterion, lesson, or LOG entry records that weekly run. That is the claim.

## Not run

`c1-count.py`, `c2-count.py`, `c3-count.py`, `verify-receipts.py`, validator `plan`, validator `run`, any dispatcher, any fetch. `LOG.md` and `corpus/lessons/round-43.md` claim C1/C2/C3 results. Those sentences were read. They were not executed here. An unrun check has not passed.

## Touched surfaces

- Written: `.ufo/waves/round-44/w2/W2ScoutConsider.md` (this file).
- Read: `considerthese/2026-10-24.md`, `corpus/QUALITY.md` (criterion headings and 542-552), `corpus/lessons/round-43.md`, `LOG.md` (1460-1465 and 1553), `SCORECARD.md` (2195-2213 and 2348-2376), `.ufo/waves/round-42/w1/swarm-registry.json` (parsed, not edited), `AGENTS.md`.
- Not written: the consider file, QUALITY.md, lessons, LOG, SCORECARD, git index, jj, fleet, sibling lanes, shokuknow.
