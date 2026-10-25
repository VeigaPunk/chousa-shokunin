# Reference integrity — round-7 coverage-of-integrity move (research-gate)

source: lane HEAD `4835426432f9a2f8cf9516400fec8340ec0bf772` (round-6 records;
no commits by any seat). Before-gate: the round-6 revision
`tools/research-gate.sh` sha256
`0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8`
(`git show HEAD:tools/research-gate.sh`). After-gate (the revision every "after"
line below was measured at): sha256
`3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2` — the mode's
sha moved repeatedly during the wave (this seat observed ten distinct
revisions between the round-6 gate and the settled one: `0fddc88e`,
`e9ab5141`, `9dcc83d5`, `855e9e7d`, `d0e18642`, `f79b40ad`, `b7f6ddd5`,
`6dc7fba4`, `020ecde5`, then `3ba718bf`), so this revision was settled first
(unchanged ≥3 min while polled), then observed identical before and after
every run below. It is the
same revision the fixture README pins and the critic's pinned battery
`GATE_SHA_START`/`END` records.

Fixtures (fixture-author seat, uncommitted under `corpus/fixtures/`):
`integrity-r7.md` sha256
`4310ce86aa45f3d7d4b7d04c4ebf480a7b59748510ab0f132c5411dd8acd1b1b`, twin
`integrity-r7-broken.md`
`fd4e213f03faf9a76bbca3896b11fe6530878e727fefb974043ffb4a9f9a05b8`, companions
`integrity-r7.claims.jsonl` / `integrity-r7-broken.claims.jsonl` (byte-identical,
one sha256 `8e83b23d04e92961f7781e556d600b94a313e083c79d32a517fcb16ec17dabb3`),
contract `integrity-r7.README.md` sha256
`2ef59df319d78072a8fa15d2cca052ca0520c22f4083dcaa3f2343d3bdfc93a2` (read at
this writing; the pair was revised during the wave — an earlier revision put a
dangling source id behind an exempt-status hop, which the landed mode counts
exempt; the pair was re-shaped to non-exempt cells and the README records
that, §The twin defects). All script line numbers below are relative to the
after-gate revision above.
verified-at: 2026-10-16 ~02:58–03:10Z, from the lane cwd, fresh processes,
`--root ..`, local reads only; nothing fetched; the only processes run are the
gate's own section subprocesses; zero network (strace below).
recheck:
`bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..`
· `bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..`
· `bash tools/research-gate.sh --selftest`

## The move

Before (gate `0c3d51ed…`): the five r1–r6 modes each read their own rows; no
mode read the REFERENCES between sections. A Sweeps row naming an undeclared
`claim_id`, a Claims/Negatives `sweep` cell naming an undeclared sweep id, a
Chain `from` cell naming an undeclared claim or source id, a Rejection `ref`
naming an undeclared source id — each passed every mode and the composed
`verify-all` verdict read CLEAN (the fixture README §Before state records both
r7 fixtures composing CLEAN at that gate; this seat independently measured
scratch variants of `full-r6.md` with five distinct dangling cells in two
records — `chain from=C9`, `sweeps claim_id=N9`, `claims sweep=SW9`,
`negatives sweep=SW9`, `rejection ref=S9` — each `RESEARCH_GATE: CLEAN`,
exit 0).

After (gate `3ba718bf…`): a sixth mode, `verify-integrity <record>` (parser
`:3613`; mode `:1764-1890`; doc `:101-129`), resolves every cross-section
reference token against the rows that declare it, and `verify-all` composes it
as a fifth section (`VERIFY_ALL sections=5 …`; native tally plumbing `:1952`,
section order `:1980`, applicability `:2030-2034`, dispatch `:2044`). The
fixture pair's pre-registered contract holds as pre-registered: the positive
composes CLEAN with `INTEGRITY refs=16 resolved=15 unresolved=0`; the twin
composes DRIFT with exactly two `REF_UNRESOLVED` findings, integrity the only
drifting section:

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity state=run verdict=DRIFT findings=2 drift=2 tally=INTEGRITY refs=16 resolved=13 unresolved=2
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2)
exit=1
```

Solo mode on the twin prints one `REF` line per extracted token before the
findings; the two dangling ones read `observed=unresolved verdict=mismatch`
(`:1733-1748` classification, `:1877-1888` summary/verdict).

## The reference model (as landed)

**Declared ids** (`verify_integrity`, `:1778-1811`): source ids from `##
Sources` `id` cells; claim ids from `## Claims` `id` cells **and** `##
Negatives` `id` cells (one claim namespace); sweep ids from `## Sweeps` `id`
cells. Cells are read through the shared r1 reader, so its documented aliases
apply (`src_id` reads as `id`, etc.). Rows with an empty `id` cell declare
nothing — the synthetic row labels used in reports (`H1`, `C1`, `N1`, `SW1`,
`R1`) are display names, not declarations (probe b18 below). There is no
other declaration surface: companion claims files, `## Question` prose and
free text never declare ids.

**Reference cells** (`:1813-1874`) — the only cells scanned:

| section | cells read | aliases |
|---|---|---|
| `## Chain` | `from`, `claim`, `to` (fragment after `#` cut) | claim: `claim_id`, `claim-id` |
| `## Claims` | `sweep`, `source`, `ref`, `pointer` | sweep: `sweeps`, `sweep_id`; source: `src`, `source_id`; ref: `reference`, `cite` |
| `## Negatives` | `sweep`, `where` | sweep: `sweeps`, `sweep_id`; where: `looked_at`, `looked`, `location` |
| `## Sweeps` | `claim_id`, `where` (same reader as verify-sweeps) | claim: `claim-id`, `claim`, `negative_id` |
| `## Rejections` | `ref` | `reference` |

A cell's raw value is split on whitespace, commas and semicolons, and each
token has edge decoration stripped — backticks, quotes, brackets, trailing
`. , ; : ! ?` (`integ_trim`, `:1698-1715`; `integ_cell`, `:1750-1762`). Each
token is then classified once (`integ_token`, `:1733-1748`):

- **declared** (equals a member of one of the three id sets, any shape — not
  only the `…<digit>` forms) → `kind=source|claim|sweep`, counts resolved;
- **undeclared id shape** (`S<digit>…`, `C|N<digit>…`, `SW<digit>…`) →
  `REF_UNRESOLVED` (warn, drift), one finding per occurrence naming kind, id,
  section, row and cell;
- **non-local naming** (URLs; `local:// artifact:// agent:// proc://
  history://`; `external: web: live: chat: session:`) → exempt,
  `reason=non-local`;
- **anything else** (local paths/globs, prose, sentinels, foreign tokens) is
  not an integrity token: not counted, not emitted — the other modes own those.

**Counting** (`:1877-1889`): `INTEGRITY refs=N resolved=M unresolved=K` counts
every extracted token (exempts included); the exempt count is `N−M−K`; each
occurrence counts once; CLEAN iff `K=0` and no finding drifts. In compose, the
same numbers ride the section line as `tally=INTEGRITY …`, appear under
`tallies` in the `--json` manifest line (schema `chousa-verify-all/v1`,
unchanged), and are folded into the composed `findings`/`drift` counters.

**Applicability in compose** (`:2030-2034`): the integrity section runs
whenever at least one other section runs — the input cases measured here:
Markdown record → 5 run sections; claims JSONL as input → claims run, integrity
run `refs=0` CLEAN, structure/chain/sweeps absent (`run=2 absent=3`, exit 0);
an approval-only record → structure drifts its own r1 findings while integrity
runs `refs=0` CLEAN (it never invents references). A record where no other
section runs would report integrity absent rather than a vacuous CLEAN; that
state is not reachable from the inputs measured here (structure runs for every
non-JSONL input).

## Fail-closed semantics

- Any unresolved token drifts the integrity mode: `ROLL=DRIFT`, exit 1, one
  `FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=… id=…
  section=… row=… cell=…` per occurrence (`integ_emit_ref`, `:1717-1731`).
  Severity warn (always drift, strict-independent), consistent with the
  `CHAIN_*`/`SWEEP_*` families.
- In compose, integrity is a normal section: the composed verdict is DRIFT iff
  any run section drifts; the twin shows a composed DRIFT whose ONLY drifting
  section is integrity, with structure/claims/chain/sweeps byte-identical to
  the positive's tallies (the twin's two defect lines sit in cells no other
  mode reads).
- Exit contract unchanged: 0 CLEAN / 1 DRIFT / 2 setup-usage. Measured:
  `verify-integrity` missing record → 2; `verify-all` missing record → 2;
  `--claims` outside `verify-all` → 2; `--json` with a missing directory → 2
  (selftest cases 72/73 pin the two new setup exits).
- The section tally is the solo mode's tally BY CONSTRUCTION: the section runs
  `bash "$SELF" verify-integrity "$record"` as a fresh subprocess
  (`verify_all_section`, `:1929`; native tally extraction `:1952`), so composed
  and solo numbers cannot drift apart.

## Exempt classes (exempt-but-counted)

1. **Exempt-status rows.** A chain row whose status is `unresolved |
   blocked-no-fetch | rejected | labelled-dead | not-applicable` (`:1814`), and
   a sweeps/negatives row whose status is `unresolved | blocked-no-fetch |
   labelled-dead | not-applicable` (`:1841-1844`, `:1856-1859`) has its
   reference tokens counted **exempt** rather than required to resolve — both
   tokens that would have resolved (measured: N2's `sweep=SW2` reads
   `observed=exempt verdict=exempt status=unresolved` in both r7 twins and the
   positive's exempt=1) and id-shaped undeclared ones (measured: probe b3's
   exempt hop citing `S9` composes CLEAN with 3 exempt tokens; probe b30's
   unresolved-status sweep row naming `S9` likewise CLEAN, exempt=3). This is
   a named boundary, not a closure: **an undeclared id behind an exempt status
   passes**. The boundary is pinned by the impl's own selftest case
   `integrity-exempt-counted` (case 70), and the r7 fixture pair deliberately
   keeps both defect cells on non-exempt rows, measuring the exempt class in
   place through N2's token rather than asserting against it.
2. **Non-local namings** wherever a location is named: exempt with
   `reason=non-local`, never a finding — a URL is not a local declaration the
   gate could resolve. Declared/undeclared classification still applies first,
   so an undeclared `S…` id is a reference even if it appears beside a URL.
3. **Not counted at all** (neither resolved nor exempt): local paths/globs,
   prose words, and foreign tokens — e.g. `to=research/…/A-shokunin-tradition.md`
   (probe b22) and every claim `pointer` path cell pass through unread. These
   are the other modes' surface; integrity never double-counts them.

## Extraction limits — the critic's attack catalog, dispositioned

The critic seat's r7 catalog (29 attack records b1–b34, each a single-cell
mutation of `full-r6.md`, plus two probes by this seat, P1/P2) was run
through the settled revision by this seat and, independently, by the critic's
pinned battery at the same gate sha — both witnesses produce identical exit
codes for all 29. Classes and dispositions:

| class (probes) | measured at `3ba718bf…` | disposition |
|---|---|---|
| dangling claim id in sweeps `claim_id` (b1, b9), claims `sweep` (b5), negatives `sweep` (b6) | DRIFT, `REF_UNRESOLVED` naming the cell | **caught** |
| dangling claim id in chain `from` (b2); dangling source id in chain `to` (b4) | DRIFT; b4 also drifts at r6 via chain mode | **caught** |
| dangling source id in sweeps `where` (b7) | DRIFT; r5's `SWEEP_LOCATION_UNRESOLVED` also catches | **caught** |
| synthetic sweep ids — `## Sweeps` `id` column emptied (b32) | DRIFT: N1's `sweep=SW1` is now undeclared | **caught** (declarations need explicit `id` cells) |
| prefix collisions — claims renamed C10/C20/C30 while hops cite C1/C2/C3 (b12) | DRIFT ×3 — exact-match, no prefix resolution | **correct negative** |
| duplicate declarations — two rows declare `C1` (b17) | DRIFT only because hop 2's `C2` is now undeclared; the duplicate itself is not flagged | **named limit** — duplicate ids are tolerated; declared-ness is set membership |
| id-proofing: backticks, trailing punctuation (b27, b28); `C.` (b26) | b27/b28 trim then resolve CLEAN; `C.` trims to `C`, not id-shaped → not counted | **trimmed-and-resolved** (b27/b28); **named limit** (b26: non-id-shaped variants pass) |
| lowercase variants — `c1` in `from` (b11), `sw1` in claims `sweep` (b34) | CLEAN, not counted: the id shapes are case-sensitive | **named limit (fail-open)** — a lowercase id-shaped token is invisible |
| wrong-namespace but declared — `N1` in claims `sweep` (b20), `S1` in chain `from` (b21), `S1` in claims `sweep` (b24) | CLEAN: declared-is-declared; kind is recorded (e.g. `kind=source` in `from`) | **named limit** — the model checks declared-ness, not kind correctness |
| companion-only / foreign ids — `FC1` in `from` (b23) | CLEAN, not counted (not id-shaped; companions are not a declaration surface) | **named limit** |
| unscanned columns — nonexistent id in chain `notes` (b13), a `cites` column (b33); this seat's P2 (`S9`/`C9` in `notes`) | CLEAN: only the listed cells are read | **named limit** — prose outside reference cells is invisible (fail-open) |
| prose inside a reference cell — this seat's P1: `S9` mentioned in a space-form `where` cell | DRIFT, `kind=source id=S9 section=sweeps … cell=where` | **named limit (fail-closed direction)** — prose in a reference cell can be over-extracted into a false positive; a declared `S…` mention would resolve silently |
| to-fragment form — `to=S1#quote:…` (b16) | integrity cuts the fragment and resolves `S1`; the run drifts via the STRUCTURE section's r1 pointer check (`CHAIN_HOP_UNRESOLVED`), not integrity | **pre-existing r1-vs-r3 seam** — structure still refuses fragment pointers that chain mode resolves; named, not fixed by this round |

Both directions are therefore honest and named: the mode is fail-closed for
anything it extracts (an unresolved id-shaped token drifts), and its
un-caught classes are all under-extraction — tokens it never sees (lowercase
variants, non-id shapes, unscanned cells, exempt-status rows, companion
ids) or never requires to resolve. None of the named limits is silently
tolerated; each is dispositioned above as **named limit** and belongs to a
future round's scope if it is to be closed.

## Evidence (this seat's battery, single pinned revision)

Everything below was run fresh-process from the lane cwd against gate
`3ba718bf…`, re-checked identical before and after; stdout verbatim except
`ts=` and elisions marked `…`.

- **Fixture pair** (the round's falsifiable claim, both sides measured):
  at the r6 gate both fixtures compose `CLEAN sections=4 run=4` (README
  §Before state; this seat's five-defect scratch variants replicate the class);
  at the settled gate the positive composes CLEAN `run=5` and the twin DRIFT
  `drift-sections=1` with the two findings quoted above.
- **Selftest**: `RESEARCH_GATE_SELFTEST: PASS (74 cases)`, exit 0. Case lines
  1–64 are BYTE-IDENTICAL to the round-6 receipt
  (`corpus/evidence/compose-r6-20261016T020330Z-selftest.log`; `cmp` clean on
  the extracted case lines; the critic's pinned battery independently reports
  `CASES-1-64-BYTE-IDENTICAL YES`). The ten new cases are exactly the r7
  family: `integrity-pass`, `integrity-fail-dangling-claim` (sweeps
  `claim_id`), `integrity-fail-dangling-source` (rejection `ref`),
  `integrity-fail-dangling-chain-claim` (chain `from`), `integrity-fail-dangling-sweep`
  (claims `sweep`), `integrity-exempt-counted`, `integrity-fail-counting`, two
  setup exits, and the composed `all-dangling` — covering dangling-claim,
  dangling-source, consistent-resolve, exempt-counted and counting as the
  round required.
- **Regressions at the settled gate**: claims fixture `VERDICT_BEARING_CLAIMS=17/17`
  CLEAN; chain fixture `RESOLVED_HOPS=17/22` CLEAN, broken control `1/2` DRIFT;
  sweeps fixture `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN, broken control
  DRIFT; r6 trio: `full-r6.md` CLEAN `run=5` with integrity
  `refs=13 resolved=12 unresolved=0`, `full-r6-broken.md` DRIFT
  `drift-sections=2` (chain+sweeps, unchanged), `full-r6-absent.md` CLEAN
  `run=4 absent=1` with integrity `refs=2 resolved=2`; round-1 observable
  intact: the three archived inputs each exit 1 with exactly one `RESEARCH_GATE:
  DRIFT` summary (3/3).
- **Manifest**: one composed run with `--json` to scratch appends one
  `chousa-verify-all/v1` line carrying the five sections; the integrity object
  reads `{"name":"integrity","state":"run","verdict":"CLEAN","findings":0,
  "drift":0,"tallies":{"refs":16,"resolved":15,"unresolved":0,"exempt":1,…},
  "native":"INTEGRITY refs=16 resolved=15 unresolved=0"}` — a superset of the
  solo summary; the append-only `>>` policy is unchanged (`:2087`).
- **Zero network**: `strace -f -e trace=network` around a composed twin run:
  **0** socket/connect/sendto/recvfrom lines in 9007 trace lines.
- **Second witness**: the critic's pinned battery at the same `GATE_SHA_START`
  reproduces the full exit-code table, the fixture verdicts, solo ref counts,
  selftest PASS, byte-stability, manifest and strace results; the fixture
  README's §After-state block independently records the same twin outputs at
  the same revision.

## What the integrity CLEAN does not prove

Declared-ness is not kind-correctness (b20/b21/b24 pass cross-namespace), not
semantic correctness (two rows may declare the same id, b17), not spelling
robustness (case and non-id-shape variants pass, b11/b26/b34), and not
completeness (unscanned columns and exempt-status rows are outside the model,
b3/b13/b30/b33/P2). References are extracted per the listed cells and
resolved by exact membership in the record's own declaration sets; a CLEAN
integrity section says every token it could see that looked like a reference
resolved to a declared row in that record — nothing about whether the
referenced row is the RIGHT row, or whether the referencing cell's prose was
meant as a reference at all (P1). Composition inherits all of this plus the
r1–r6 limits the previous notes name.

## Open items

- **Named extraction limits (above), not closed**: case-sensitive id shapes;
  non-id-shape variants; duplicate declarations; unscanned columns; companion
  id surface; exempt-status blanket exemption; prose over-extraction inside
  reference cells. Each is dispositioned, none is silently tolerated.
- **r1-vs-r3 seam (b16)**: `structure` refuses to-fragment pointers that
  `chain` mode resolves; pre-existing, surfaced by the catalog, not touched
  this round.
- Carried residuals from earlier rounds (unchanged): in-root hardlinks bypass
  path canonicalization; no source size cap; the banner still reads
  `research-gate-r1` (cosmetic).
- **Receipt identity (round 1) — STILL OPEN.** These are lane-local evidence
  runs, not queue taskKey/expected-receipt bags; no `task_…` value may be
  invented and no Sighting is claimed. No scalar score, no promotion, no
  field-readiness claim. No commits by this seat; this note and the seat's
  scratch (declared ephemeral, cleaned) are its only outputs. A later revision
  that changes the extraction rule should re-derive this note's after-state
  from the record bytes and the fixture README's contract.

Round-12 disposition (2026-10-19, append-only): any r2-carried residual this note names — the banner `research-gate-r1` and the absent source-read size cap — landed at round 12 (`VERSION=v2`, r12 baseline re-pinned, `knowledge/gate-baseline-r12.md`; 8 MiB cap `CLAIM_SOURCE_READ_TOO_LARGE`/`CHAIN_SOURCE_READ_TOO_LARGE` at the shared chokepoint). In-root hardlinks remain carried. This note's own claims are otherwise unchanged.
