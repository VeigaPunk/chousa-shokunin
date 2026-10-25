# Round 42 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_swe)
date: 2026-10-24
reviewer identity: `Kimi fresh closure agent` (fresh, non-author; no subagents dispatched; no external fetch)
lane repo measured at: `e0f4895c48d6c6e739ce9deb614b97c771a3a096` (pushed tip; `jj-lane.sh state` → `ahead=0 behind=0`, `local=remote=e0f4895…`)
base: `872bf3a3507875b382313f955d15960f9638256f`

## Step-1 conformance

- Report `.ufo/reports/round-42/chousa.md` committed in fleet repo under lane identity:
  `git log --format='%an <%ae> %H' -- .ufo/reports/round-42/chousa.md` →
  `chousa-shokunin <chousa@shokunin.local> 980859a48a156f76bc6872e608150de9a8dcfe8c` — PASS.
- `SHONEN` heading present at report line 154 with four `[~]` lines, one per box — PASS.
- Cited hashes exist and are ancestors of the branch:
  `git merge-base --is-ancestor <h> master` → exit 0 for `e0f4895c…`, `dd63b6cf…`,
  `872bf3a3…` — PASS.
- Lane pushed: `jj-lane.sh state` → `ahead=0` — PASS.
- Prompt `.ufo/prompts/chousa-round-42.md` (478 lines) carries the full contract: MISSION/AXES
  binding, 1–3 claims rule, frontier step, commit-then-push ordering, push scope, L0 side
  channel, report path, SHONEN heading requirement, hash citation rule, write scope, and the
  §6 hyaku addendum including item-10 wave-4 quarantine-first — PASS.
- Not a marker: report carries work performed, evidence pointers, measurements, sources &
  frontier, trend verdicts, SHONEN — PASS.

### Uncommitted-path finding (driver verify warned `WARN lane repo has uncommitted changes: 40 paths`)

`git status --porcelain` → 4 `M` + 36 `??`, all inherited/orchestrator-side, none authored by
this round and none in this round's commit:

- `M .ufo/waves/round-40/w1/swarm-registry.json`, `M .ufo/waves/round-41/w1/swarm-registry.json`
  — prior-wave registry rewrites (seat-registry mutation by earlier waves).
- `M PROVINCE.md` — mode-bit only (`100644 → 100755`), no content diff; inherited.
- `M corpus/evidence/round41/receipts/cells/cells.json` — r41 D2's counter rewrites this file
  on every run (disclosed in r41/r42 reports).
- `?? .ufo/waves/round-40/w1/*.md` (33 files) and `?? .ufo/waves/round-41/w1/*.md` (3 files)
  — orchestrator-dispatched seat reports from prior waves, not lane-authored round-42 work.

All 40 match the report's own "Inherited working-copy state" disclosure. Left untouched; named
here for the record. No uncommitted round-42 lane work exists.

## Claims — re-measured vs evidence-verified

### C1 — operability (lowest scored non-retired axis, 3/10): RE-MEASURED, verdict `improved`

I re-ran the frozen counter myself at the pushed tip:

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ git rev-parse HEAD → e0f4895c48d6c6e739ce9deb614b97c771a3a096
$ python3 corpus/evidence/round42/c1-count.py
SLICE_REDERIVE_MATCH PASS  tool=24 independent=24
EXAMINE_RUNS         PASS  exit=0
QUOTES_EXAMINED      PASS  examined=43 expected=43
NO_SKIPPED_QUOTE     PASS  every examined quote carries a status
REPRODUCIBLE         PASS  two runs identical=True
POSITIVE_CONTROL     PASS  fold=exact strict=True
NEGATIVE_CONTROL     PASS  fold=None strict=False
MUTANT_DETECTED      PASS  mutant=23 base=24
SLICE_REDERIVE_MATCH=24/24
QUOTES_EXAMINED=43/43
REPRODUCIBLE=1/1
POSITIVE_CONTROL=1/1
NEGATIVE_CONTROL=1/1
MUTANT_DETECTED=1/1
exit 0
```

Every reported figure reproduces verbatim. The do-nothing control
(`controls/c1-control-before.txt`, committed) records the tool-absent run exiting 1 — the
counter fails where the work was not done. The counter grades rule-consistency, completeness
and discrimination of the derivation — not live-web truth (stated limit, accepted).

### C2 — calibration: RE-MEASURED, verdict `improved`

```
$ python3 corpus/evidence/round42/c2-count.py
VERDICTED=24/24
CLASS_CONSISTENT=24/24
REASON_NONEMPTY=24/24
FLIP_NONEMPTY=24/24
VOCAB_OK=24/24
DUPLICATE_ROWS=0
ROWS_OUTSIDE_SLICE=0
C2=PASS
exit 0
```

All reported figures reproduce verbatim. The flipped-row do-nothing control
(`controls/c2-control-before.txt`, committed) records `CLASS_CONSISTENT=23/24` with
`MISMATCH S093 table=present independent=absent` and exit 1 — the counter discriminates a
planted false row. C2 grades rule-consistency and completeness of the adjudication, not the
truth of the underlying "absent" judgement (stated limit, accepted; the `absent`-class split
is named as round-43 work).

### No-harm check

`git diff 872bf3a3… e0f4895c…` is purely additive: 25 files, +4942/−0. `SCORECARD.md` gains
only the round-42 block (all six axis rows read improved-or-unchanged) and a r43 `Planned`
block; `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-42.md` are
append-only; no lane-authored file was rewritten. No axis is harmed.

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 re-measured above; the quarantine scope is now one committed command with receipts and discriminating controls |
| calibration | improved | C2 re-measured above; 24/24 verdicts consistent with an independent re-examination |
| depth | improved (narrow) | `corpus/lessons/round-42.md` records the frozen rule, four mined mistakes with captured-by and fix, QUALITY 59–60 each citing their lesson and a shown-able-to-fail case |
| coverage | improved (narrow) | a new measured surface (24 rows / 43 quotes) the lane did not hold; no coverage-map row advanced by design (quarantine-first) |
| freshness | improved (narrow) | S077 opened from an installed copy with sha256 recorded; register + every consulted capture digested in `receipts/digests.txt` |
| adjacency | unchanged | nothing absorbed from siblings; campaign tree and sibling repos read-only; zero egress |

## Discernment spot-check (non-author; LEARNING.md)

| item | lane decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S077 row (admit, new `SOURCES.md` row) | tier A, mined, quote "Pdftotext converts Portable Document Format (PDF) files to plain text." (DESCRIPTION, lines 12–13) | `/usr/share/man/man1/pdftotext.1.gz` | **agree** | `sha256sum` → `50dd56df96821e172abfcfdef75995c076ca3cb4602c99c6cb58f0d25abf4a27` (matches row); `zcat … | sed -n '10,15p'` prints the quoted sentence verbatim under `.SH DESCRIPTION`; `pdftotext -v` → `pdftotext version 26.08.0`. Located quote, tier and anchor all verify. |
| S086 row (reject — verdict `absent`) | `absent`: longest runs 4/46 and 2/29; "the page does not carry the quoted Chinese text at all" | register row (S086, `https://www.ncpssd.cn/`) + committed capture `.qcache/76914d78c20094f677dea77d.txt` (15270 bytes) | **agree** | I re-derived the longest contiguous common run myself (NFKC + whitespace-collapse): quote1 → 4 of 46, quote2 → 2 of 29, neither exact substring present. Matches the adjudication table verbatim; `absent` is the right verdict. |
| S077 register row (verdict `unverifiable`) | `unverifiable`: local capture is a 265-char `Client Challenge` bot wall | `.qcache/01f657b3d0ab045c494b3f92.txt` | **agree** | The capture is 267 bytes of `Client Challenge` interstitial, not the cited article — the register's `payload-absent` class ("every relevant source fetched cleanly") is indeed unreliable for this row. `unverifiable` is right and is correctly never called a fabrication. (Cosmetic: report says "265-char", file is 267 bytes / ~265 chars of text.) |
| S100–S103 family (verdict `unverifiable`) | `unverifiable`: register unchecked family, class cell names no locator | register `## Rows whose quotes were NEVER CHECKED` table | **agree** | Register row S100's cited-source cell is literally `#### Gate — S100` — no locator exists. `unverifiable`, not fabrication, is the correct call. |

The lane's `## Gate` also admits the runnable surface + counters + table and rejects the whole
staged package this round under item-10 quarantine-first; I agree with both — adoption without
a verdict per row would have imported the register's stale class column, which this round
proved unreliable.

`sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, five
pre-existing W04 advisories (S051, S053, S073, S074, S075) as the report names.

## Item-10 / S077 collision / no-fetch checks

- **No adoption**: the committed diff contains no `SOURCES.append` import and no knowledge
  entry; `SOURCES.md` grew by exactly one row (S077) — quarantine-first honored.
- **S077 collision real**: `merge/chousa/SOURCES.append.md`'s first id is S077; lane's next
  free id is S077 (registry max now S077 after this round's row). The report's renumber-by-
  document note and the L0 question match the item-10 rule; nothing depended on the answer
  this round.
- **No external fetch**: the committed diff adds no capture material; every receipt reads the
  committed `.qcache` and installed files; digests are recorded for all consulted bytes. The
  one new source (S077) is the installed man page — consistent with the no-egress claim.
- **L0 append**: `chousa | round-42` line present in `.ufo/l0-questions.md`, committed in
  `980859a4` (report + l0 file only — within lane main-repo write scope; integrator owns its
  durability, now committed).
- **Wave shortfall honest**: `w1/swarm-registry.json` has 64 members, every `agentId: null`;
  `w1-dispatch.json` carries `taskCall` with 64 tasks, `counts: {spawn:64, total:64}`. The
  report's "issued but not settled, 0 seat reports, 0 claimed, 0 dead" is what the committed
  evidence shows — an honest wave shortfall, not a fabricated completed dispatch. The two
  claims do not rest on any seat verdict (counters run by the lane against its own controls).

## Trend verdicts

- **expansion: improved** — one opened source row (S077, mined), one lesson, and one new
  runnable surface (the lane's quarantine scope) on ground the lane did not hold. The measure
  is the new surface plus the row, and it verifies.
- **quality: improved** — both counters re-verified by me against their do-nothing controls;
  the register's class column was shown unreliable (S077 bot wall) and the lane's rule now
  checks capture FORM; no admitted entry failed its re-check.
- **discernment: improved** — the lane reported `unchanged` because it had no outside review;
  this pass IS the outside non-author spot-check, and it agrees with the gate on the admit
  (S077), the reject (S086 `absent`), and the unverifiable family (S077, S100–S103). The
  sample is now externally checked with agreement on both sides of the gate.

## Routed defects for round 43 (lane must fix)

1. `absent`-class split named but not landed: separate "the source carries the text and the
   row quotes it wrongly" (e.g. S093 79/120) from "the source does not carry it" (e.g. S086
   4/46) — already in `SCORECARD.md` planned for r43; keep it routed until landed.
2. Wave shortfall: 64-seat dispatch issued but unsettled at budget close — name the
   dispatch-completion mechanism in r43 (a receipt the wave seats actually ran, or a smaller
   validated wave that settles inside the budget). Recorded as honest shortfall, not a defect
   of the claims.
3. Inherited working-tree debt: `PROVINCE.md` mode bit, two modified prior-wave
   swarm-registries, r41 `cells.json`, and 36 untracked r40/r41 seat reports remain
   uncommitted — the lane's respawn rule requires resolving lane-authored leftovers;
   orchestrator-owned seat reports need an operator/orchestrator decision (commit as wave
   evidence or leave). Named, not swept.
4. Register staleness upstream (operator-side, not lane-fixable): the register's `## By lane`
   summary (chousa 20) and header (194/324) are stale vs the derived 24; the M12 census's 25
   is not reproduced by the operator's own extraction recipe. Route to the campaign owner via
   the existing L0 channel.
5. Cosmetic: report says "265-char" for the S077 capture; the file is 267 bytes. Non-blocking.
