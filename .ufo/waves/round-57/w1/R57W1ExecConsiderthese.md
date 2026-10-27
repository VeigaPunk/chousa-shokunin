# R57W1ExecConsiderthese — the stable-proposal-ids proposal (considerthese 2026-10-26, proposal 1)

Seat: executor, chousa lane, round 57 wave 1. Read-only on the lane; the only write is this report.
No frozen claim (R57-C2/R57-C3), predicate, target, counter, control or recipe was touched; no lane
file, counter or lesson was edited; no production edit — the L1 lands. No network, no capture read.
Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecConsiderthese/` was deleted before this yield.

## 1. The proposal, quoted

`considerthese/2026-10-26.md:39-41` (section `## Self-improvement proposals (not acted on)`), bullet 1 of 4:

> - **Give my proposals stable ids.** The round-51 scout seat had trouble reconciling its tally
>   (19/9/3 against its own status column). If each proposal carried an id like `CT-20261026-1`,
>   the lane could cite uptake exactly, and I could stop re-raising anything already implemented.

## 2. Sweep: rounds 52–56 already implemented it; ledger state at the tip

Spec sweep, run verbatim (`grep -rn 'CT-2026' <corpus> <.ufo/reports> 2>/dev/null`): 39 hits, in three
files — `corpus/evidence/round54/considerthese-ledger.tsv`,
`corpus/evidence/round55/considerthese-ledger-check.txt`, `corpus/lessons/round-55.md`. The same
proposal across rounds (text at `considerthese/2026-10-26.md:41`): **52** —
`.ufo/waves/round-52/w1/R52ScoutConsiderthese.md:12` "Stable proposal ids `CT-YYYYMMDD-n` … FMT …
names no lane artefact" → FMT; **53** — `.ufo/waves/round-53/w1/R53ScoutConsiderthese.md:9` "P1 |
stable ids `CT-YYYYMMDD-n` (`:41`) | reflection-format only" → reflection-only; **54** —
`corpus/lessons/round-54.md:67` implemented as `corpus/evidence/round54/considerthese-ledger.tsv` +
checker, "ids `CT-YYYYMMDD-n` assigned lane-side (considerthese/ untouched)" → **IMPL**; **55** —
checker hardened into `corpus/evidence/round55/considerthese-ledger-check.py` + receipt → IMPL,
hardened; **56** — `.ufo/waves/round-56/w1/R56ScoutConsiderthese.md` ran the round-55 checker,
`BAD=0` → IMPL, verified.

The ledger already carries the author's four 2026-10-26 proposals, one id per bullet
(`corpus/evidence/round54/considerthese-ledger.tsv:33-36`): `CT-20261026-1` IMPL (this ledger and
checker), `-2` IMPL (`round53/weakness-streak.py`), `-3` IMPL (`round52/verdict-gap.py`), `-4` FMT
(independent reader outside the lane). Live on the tip:

```
$ python3 corpus/evidence/round55/considerthese-ledger-check.py --root .
PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0   exit=0
```

35 bullets exist (4+6+5+4+4+4+4+4 over the eight `considerthese/2026-*.md`) and 35 ledger rows, one
per bullet. The only OPEN row is `CT-20261019-4` (SKILL.md size, no threshold) and the only OPS row
`CT-20261022-2` (orchestrator-owned) — neither fits a round-57 lane claim. **The id scheme is landed
and passing.** But the proposal has two halves and only the first is delivered: "the lane could cite
uptake exactly" — delivered (the tally comes from ledger rows); "**and I could stop re-raising
anything already implemented**" — not delivered, because the ids live only lane-side.
`grep -rn 'ledger\|CT-2026' considerthese/` finds no id in any of the author's eight files except
the proposal text quoting the format (`considerthese/2026-10-26.md:41`), so the author's next daily
file cannot cite an id it has never seen. The lane chose this deliberately (`considerthese/` is the
author's file, not the lane's to edit) — leaving half the ask open with no owner.

## 3. The residual I found: ids are positional, so an id can silently rebind

The scheme derives `n` from the bullet's **ordinal position** in the author's file
(`corpus/evidence/round55/considerthese-ledger-check.py:24-30` mints
`f"CT-{f.stem.replace('-','')}-{n}"`). No ledger row fingerprints the proposal text, so nothing checks
that the bullet an id points at is still the same bullet. Measured on a scratch fixture (never on the
lane), production checker:

```
# 3 bullets, rows CT-20260101-1/-2/-3, author reorders them (Gamma first)
$ python3 corpus/evidence/round55/considerthese-ledger-check.py --root ./root --ledger ./ledger.tsv
PROPOSALS=3 ROWS=3 IMPL=2 FMT=1 OPEN=0 OPS=0 BAD=0   exit=0
```

Exit 0. `CT-20260101-1` now names *Gamma*, `-2` names *Beta*, `-3` names *Alpha*, and the ledger's own
`note` column ("alpha") is contradicted while the check passes. A `CT-` citation names a *position*,
not a proposal. This is distinct from QUALITY 103 (`corpus/QUALITY.md:949`, denominator = full
expected set): there the denominator is right (3 = 3) and the *identity* is wrong. Scratch successor
closing it — 5th ledger column `anchor` = sha256 of the bullet's normalised text, recomputed from
the file, failing `FAIL ANCHOR <id> id rebinds to a different proposal`:

```
$ python3 proto/ledger-anchor-check.py --root ./root --ledger ./ledger5.tsv
FAIL ANCHOR CT-20260101-1 id rebinds to a different proposal
FAIL ANCHOR CT-20260101-3 id rebinds to a different proposal
PROPOSALS=3 ROWS=3 IMPL=2 FMT=1 OPEN=0 OPS=0 BAD=2   exit=1
```

## 4. The related streak idea (`CT-20261026-2`) is landed but stale; its gate is red

`considerthese/2026-10-26.md:42` ("Track recurring weaknesses as streaks"). Landed round 53
(`round53/weakness-streak.py` + `recurring.tsv`), refreshed round 55 (`round55/recurring.tsv`). Both
now FAIL — the streak grew a round and no round refreshed the claimed value:

```
$ python3 corpus/evidence/round53/weakness-streak.py --root . --table corpus/evidence/round53/recurring.tsv
FAIL RW-1 streak=8 claimed=5 first_in_run=49 routed=corpus/evidence/round53/c1-supplement.py frozen counter forgeable
FAIL RW-3 streak=0 claimed=2 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=2   exit=1
$ python3 corpus/evidence/round53/weakness-streak.py --root . --table corpus/evidence/round55/recurring.tsv
FAIL RW-1 streak=8 claimed=7 first_in_run=49 routed=corpus/evidence/round55/c1-count.py frozen counter forgeable
OK   RW-3 streak=0 claimed=0 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=1   exit=1
```
Computed streak 8 (per-round forge-class hits r49 2, r50 2, r51 2, r52 4, r53 2, r54 2, r55 2, r56 2);
claimed 5 (r53 table) / 7 (r55 table). The **SKILL-registered command is the round-53 table**
(`SKILL.md:138`) and it exits 1 on the tip. Round 56 refreshed neither (`corpus/evidence/round56/`
has no `recurring.tsv`; `grep -c recurring corpus/lessons/round-56.md`=0; no QUALITY criterion
mentions `recurring`, so nothing requires the refresh). Two live tracked copies also conflict with
QUALITY 9 "One home per number and finding" (`corpus/QUALITY.md:33`).

## 5. Escape matrix — production checker vs scratch successor (fixtures under scratch)

Production = `corpus/evidence/round55/considerthese-ledger-check.py` (live; registered `SKILL.md:143`);
successor = scratch `proto/ledger-anchor-check.py` (never landed). Both read the **same 4-column
ledger**, so the comparison is apples-to-apples.

```
ESCAPE                                         | ROUND-55 (production)                      | PROTOTYPE (scratch)
--------------------------------------------------------------------------------------------------
A0 healthy baseline                            | rc=0 PROPOSALS=1 … BAD=0                   | rc=0 PROPOSALS=1 … BAD=0
E1 regex DoS (a|aa)*c on 40a+b                | HUNG/timeout                               | rc=1 FAIL REGEX-BUDGET …
E2 SIZE guard (8MiB target, regex ^a)         | rc=1 FAIL SIZE CT-20260101-1 payload.txt   | rc=1 FAIL SIZE CT-20260101-1 payload.txt
E3 proposal .md symlinked outside root        | rc=0 PROPOSALS=1 … BAD=0                   | rc=1 FAIL PROPOSAL 2026-01-01.md outside root
E4b '## Self-improvement … (archived)'        | rc=1 FAIL MISSING CT-20260102-1            | rc=0 PROPOSALS=1 … BAD=0
E5 author reorders 3 bullets (ids rebind)     | rc=0 PROPOSALS=3 ROWS=3 … BAD=0             | rc=0 (5-col anchor ledger: rc=1 FAIL ANCHOR ×2)
```
E4a (a bullet filed under a non-proposal heading needs no ledger row) is in-contract on both sides.
E1, E3, E4b are escapes the round-56 wave seat reported (`.ufo/waves/round-56/w1/R55W2MutLedgerV2.md`: "4 escapes survived"); **E5 is new to this seat** — that seat tested a heading/pointer/symlink surface but not bullet reordering. I reproduced E1 and E3 independently: E1 hangs the production checker past a 12 s timeout (`timeout 12 …` → exit 124); E3 mints an id from bytes outside the root (production exit 0; prototype `FAIL PROPOSAL … outside root`).
Disposition in the lane: `corpus/lessons/round-55.md:34` records "`considerthese-ledger-check.py` has four surviving escapes (`R55W2MutLedgerV2`) … All routed to round 57; none changes a landed round-55 count." Round 57 is this round, so the routing is live and unlanded: no `corpus/evidence/round57/considerthese-ledger-check.py`, no round-57 receipt, and the round-56 SKILL gate row (`SKILL.md:145`) registers no ledger check — the round-56 scout's green run (`BAD=0`) is a run of the *unfixed* checker, not a landing of the escapes.

## 6. Landing recommendation — LAND a round-57 successor + one lesson note + one QUALITY criterion

Do not re-open the id idea (it is landed); land the successor that makes the ids true and keeps the
streak number true. Items for the L1, in priority order.

**(a) Land `corpus/evidence/round57/considerthese-ledger-check.py`** — successor of the round-55
checker, closing the four escapes routed at `corpus/lessons/round-55.md:34` plus E5. Reference
implementation validated in scratch this wave: parity on the real lane (`PROPOSALS=35 ROWS=35
IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`, exit 0) and E1/E3/E4b/E5 killed (E5 needs the 5-col ledger).

| escape | fix |
|---|---|
| E1 regex DoS | run the cell's `re.search` under a wall-clock budget (SIGALRM, 2 s) → `FAIL REGEX-BUDGET`; cap the target read at 1 MiB |
| E2 stat→read TOCTOU | open the target once, `fstat` the **open fd**, read that fd (never re-open the path) |
| E3 unrooted proposal scan | `resolve()` every `considerthese/*.md`, require it inside `--root` → `FAIL PROPOSAL <name> outside root` |
| E4b archived heading | match the heading exactly (`## Self-improvement proposals`, ignoring an "archived" qualifier), not `startswith` |
| **E5 (new)** | add a 5th ledger column `anchor` = sha256 of the proposal bullet's normalised text; recompute and compare → `FAIL ANCHOR <id> id rebinds to a different proposal` |

The ledger's home should move with it: the round-55 checker still defaults `--ledger` to
`corpus/evidence/round54/considerthese-ledger.tsv`
(`corpus/evidence/round55/considerthese-ledger-check.py:16`), so the round-57 successor should default
to a round-57 table and the round-54 table becomes read-only history (one home — QUALITY 9).

**(b) Lesson note** for `corpus/lessons/round-57.md` (house shape: claim → what was measured → what
it means). Draft text for the L1:

> **Proposal ids are minted, not born — and the round-55 ledger's ids are positions.** The
> `considerthese/2026-10-26` proposal "give my proposals stable ids" was implemented at round 54
> (`corpus/evidence/round54/considerthese-ledger.tsv`, ids `CT-YYYYMMDD-n`, one row per bullet under
> `## Self-improvement proposals`), hardened at round 55 and re-verified at round 56
> (`PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`, exit 0). The scheme derives `n` from the
> bullet's **ordinal position** in the author's file, so an id names a position, not a proposal: on a
> scratch fixture where the author reorders three bullets, the round-55 checker exits 0
> (`PROPOSALS=3 ROWS=3 … BAD=0`) while `CT-20260101-1` has silently rebound from "Alpha" to "Gamma",
> and the ledger's own `note` column is contradicted without any failure. A `CT-` citation is
> therefore not a stable name for a proposal unless the row also fingerprints the proposal's text.
> Round 57 closes this with an `anchor` column (sha256 of the bullet's normalised text) and, in the
> same successor, the four escapes the round-56 wave seat reported (`R55W2MutLedgerV2`: regex DoS
> through the nested-quantifier heuristic, stat→read TOCTOU on the size guard, an unrooted symlinked-
> proposal read, and a mis-matched heading) — routed to round 57 at `corpus/lessons/round-55.md:34`
> and unlanded until now. The author's second half of the ask — "I could stop re-raising anything
> already implemented" — remains unowned: the ids live lane-side and `considerthese/` holds none of
> them, so the next daily file cannot cite an id it has never seen. The lane must not edit the
> author's files; the honest close is to publish the ledger path and the current tally in the round's
> own artefacts and let the author pick the ids up.

**(c) QUALITY criterion** — proposed as criterion 111 (next free: `corpus/QUALITY.md` has 105
numbered criteria, max 110, missing 1–5). Draft:

> 111. **A row's identity is bound to the content it names, not to its position or its free-text
> note.** The round-54/55 `considerthese-ledger.tsv` mints `CT-<file>-<bullet ordinal>` ids and its
> checker compares counts and pointers only, so a reordered proposal bullet rebinds an id while the
> run prints `BAD=0` and exits 0 — the ledger's `note` column then names a different proposal than
> the id does (scratch fixture, round-57 wave `R57W1ExecConsiderthese`: three bullets reordered,
> `PROPOSALS=3 ROWS=3 IMPL=2 FMT=1 OPEN=0 OPS=0 BAD=0`, exit 0). Check: `python3
> corpus/evidence/round57/considerthese-ledger-check.py --root .` — every ledger row carries an
> `anchor` (sha256 of its proposal bullet's normalised text), the checker recomputes each anchor from
> the file, and a row whose anchor disagrees with the bullet now at that id exits 1 with `FAIL
> ANCHOR <id>`; shown able to fail: the reordered fixture → `FAIL ANCHOR CT-20260101-1`,
> `FAIL ANCHOR CT-20260101-3`, exit 1; the same fixture with the bullets in order exits 0.

**(d) The streak table (related proposal `CT-20261026-2`) needs a per-round refresh rule, or it is
not a streak.** Both live tables are stale on the tip and the SKILL-registered one
(`SKILL.md:138` → `corpus/evidence/round53/recurring.tsv`) exits 1 (`RW-1 streak=8 claimed=5`,
`RW-3 streak=0 claimed=2`, `WEAKNESS_ROWS=2 FAILING=2`). The L1 should refresh
`corpus/evidence/round57/recurring.tsv` (RW-1 claimed 8, routed `corpus/evidence/round57/c1-count.py`),
make the round-57 table the one SKILL registers, and add a QUALITY line that a per-round streak
table's claimed value equals the value computed on the round it is written for — otherwise it is
stale the moment the next round lands. **Do not** propose changing R57-C2 or R57-C3: their predicates,
targets, counters and controls are frozen (`corpus/evidence/round57/claims.md`) and nothing in this
item bears on them.

## 7. Limits of this seat's evidence

- All of the above is read-only observation of the lane tip plus scratch fixtures under
  `/fast/scratch/hyaku/chousa-r57/R57W1ExecConsiderthese/` (fixtures, prototype, matrix driver). No
  lane file was modified; no counter, control, predicate or recipe was edited or run against mutated
  inputs. Scratch was deleted before this report was yielded.
- The scratch successor is a **reference implementation, not a landed artefact**; the L1 lands its own.
  It was validated for parity on the real lane and against seven fixtures — not against the lane's
  receipt format or a SKILL gate row.
- The E2 TOCTOU escape was **not** re-measured by this seat (the 21/80 atomic-swap result is the
  round-56 wave seat's, `.ufo/waves/round-56/w1/R55W2MutLedgerV2.md`); I verified only that a static
  8 MiB target is refused by both checkers. The author-side half of the proposal has no lane-side
  test; its recommendation is a publication step, not a check.
- Tooling: none installed or upgraded (no pacman, no uv/npx, no new binary). No network access; no
  capture was read from `corpus/captures/`.

VERDICT: mined the stable-proposal-ids proposal (considerthese/2026-10-26.md:41) — it is ALREADY
IMPLEMENTED since round 54 (`corpus/evidence/round54/considerthese-ledger.tsv`; the checker passes
`PROPOSALS=35 ROWS=35 … BAD=0` at the tip) but SURVIVES a real attack the round-56 wave seat missed:
its ids are positional, so a reordered proposal bullet silently rebinds an id while the check exits
0; recommendation is to LAND a round-57 successor checker with an `anchor` column plus the four
already-routed escapes, and to refresh the related streak table (SKILL-registered copy red today).
