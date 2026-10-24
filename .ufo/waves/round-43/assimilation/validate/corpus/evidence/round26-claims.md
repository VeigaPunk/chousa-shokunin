# Round-26 pre-registration — claims, frozen populations, predictions

Lane `chousa-shokunin`, claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`
(2026-10-21, hyaku round 26, attempt 1; no earlier round-26 attempt in the
fleet watchdog log, no inherited `.ufo/waves/round-26/`). Registered before any
implementation. Counting probe: `corpus/evidence/round26-measure.sh TREE
[c1|c2|c3|holds|all]`; its before-output on `git archive` of the base is
`corpus/evidence/round26-measure-before.log`. Frozen inputs are read from the
base commit object, never from the measured tree.

Source of the plan: `SCORECARD.md` `## Planned — round 26` (lines 1371–1383 at
the base) and the round-25 closure row (`MANIFEST.json` `rounds[395]`), which
admitted round 25 but routed an unexercised risk to this lane: "C1 reader byte
cap is not a practical memory budget: tools/research-gate.sh:2383-2387
materializes every line of an up-to8MiB snapshot into a Bash array". Plan item 1
(`--json` appender serialization) is **not** claimed this round: it is the same
axis as the routed risk (two operability claims would count as one). It stays
carried debt with its r24/r25 reproductions; this is a plan-vs-run disposition
(QUALITY 11), not a closure.

Population: the 29 `corpus/knowledge/*.md` files at the base (`POP` in the
probe). Subpopulation for criterion 6 (prospective from round 24): the five
r24+ entries (`POP24`). As-of date for every freshness computation:
**2026-10-21**.

## Claim 1 — operability: bounded metadata header reader (closure-routed)

Observed at the base (L1 probe, 2026-10-21, before any change): an
8,388,000-byte newline-only `.md` passes the 8 MiB byte cap, and
`verify-metadata` on it peaked at **2,240,704 KiB RSS in 86.9 s** versus
11,888 KiB for a 4-line control — the array at 2383–2387 materializes every
line before the header loop, which itself stops at the first `## `.

Change: the header parse must not materialize the snapshot into a per-line
array (or any structure growing with lines beyond the header). Output on every
existing input stays byte-identical. The existing refusals (denylist, stat,
multilink, size, NUL, read) and fd-bound snapshot are unchanged.

Counting (`round26-measure.sh TREE c1`): four 8,388,000-byte shapes —
`s1-newlines`, `s2-header-body` (valid header, `## Body`, then `x\n` lines),
`s3-crlf`, `s4-header-noheading` (header then `a\n` lines, no heading). A shape
is **amplified** when its run times out (300 s) or its peak RSS exceeds the
4-line control's by more than 8 bytes per input byte. `C1_AMPLIFIED=k/4`.

Predictions: before `C1_AMPLIFIED=4/4`; after `0/4`. Hold: `C1_FROZEN_SHA`
(plain `verify-metadata` over the frozen 29, timestamp line dropped) and
`C1_FROZEN_RC` identical before and after; legacy selftest cases 1–161
identical (`LEGACY_CASES_SHA`). Elapsed seconds are recorded, not claimed.
Axis score: the operability row's r1 construct stays 3/3 inputs → **3/10,
delta 0** (re-derived by its own command); C1's verdict rests on `C1_AMPLIFIED`.

## Claim 2 — freshness: computed recheck due dates (`--as-of`)

At the base, `recheck:` grammar (`YYYY-MM-DD`, `<N>d`, `on-release`) is only
classified scheduled/unscheduled; no mode computes when an entry is due, so a
past-due entry is indistinguishable from a current one (QUALITY 6: "A
`recheck:` that is only a command leaves 'overdue' uncomputable").

Spec v1: `verify-metadata PATH [--root PATH] [--as-of YYYY-MM-DD]`.
`--as-of` is valid only with `verify-metadata`; an absent or calendar-invalid
value exits 2. Without `--as-of`, output is byte-identical to the base. With
it, every per-entry line gains ` due=<D> freshness=<F>` immediately before
` verdict=`:

- V = the leading `YYYY-MM-DD` of `verified-at:` when calendar-valid, else none.
- R = the recheck value's first whitespace-delimited token (existing rule).
- R a calendar-valid ISO date → `due=R`; R `<N>d` and V present → `due=V+N`
  days (proleptic Gregorian); R `on-release` → `due=on-release
  freshness=event`; anything else (including `<N>d` without V, or no recheck)
  → `due=unknown freshness=unknown`.
- Dated due: `freshness=overdue` iff as-of is strictly after due, else
  `current`. Overdue emits `FINDING META_RECHECK_OVERDUE severity=warn
  surface=metadata obs=entry=<basename> due=<D> as_of=<A>` (drift).
- Refused entries carry `due=refused freshness=refused`.

Counting (`c2`): `FRESHNESS_CLASSIFIED=k/29` (frozen lines carrying a well-formed
`due=… freshness=… verdict=…`), `C2_ORACLE_AGREE=k/29` (independent Python
oracle written from this spec, inside the probe), `C2_CONTROLS_CAUGHT=k/6`
(overdue, current, date-past, event, unknown, boundary due==as-of → current).
Predictions: before 0/29, 0/29, 0/6 (flag absent → exit 2); after 29/29,
29/29, 6/6. Oracle disagreements are adjudicated against this spec, never
by editing the oracle to match. No numeric freshness score is invented.

## Claim 3 — calibration: criterion-6 registry link (`--registry`)

At the base nothing checks that a `source:` S-id exists, is `mined`, and that
its `used-by` names the entry, nor that `verified-at:` says what was checked;
round 25 shipped a presence screen and said so (R25-M10).

Spec v1: `verify-metadata PATH [--root PATH] --registry FILE`. FILE is a
`SOURCES.md`-shaped registry read through the same fd-bound, size-capped,
denylist/multilink/NUL-refusing reader; unreadable/refused FILE or a registry
with no table whose header has `id`, `status`, `used-by` columns exits 2.
Rows = table rows whose `id` cell is `S` + three digits; columns are located
by header name; the first row of a duplicated id wins. The `source:` value
(key line plus continuation lines, as for the other keys) yields every
`\bS[0-9]{3}\b` token. Findings:

- no S-id in `source:` → `META_SOURCE_NO_ROW_ID` info (legacy-compatible);
- an id with no row → `META_SOURCE_ROW_MISSING` warn;
- a row whose status is not `mined` → `META_SOURCE_NOT_MINED` warn;
- a mined row whose `used-by` has no comma-separated, trimmed token whose last
  path component equals the entry basename → `META_SOURCE_USEDBY_MISSING` warn;
- `verified-at:` whose value after the leading date has no non-space text →
  `META_VERIFIED_AT_BARE` warn.

Without `--registry`, output is byte-identical to the base.

Counting (`c3`): `C3_CONTROLS_CAUGHT=k/5` (missing, queued, usedby, bare, noid),
`C3_POSITIVE_CLEAN=k/1`, and `C3_POP_R24PLUS_CLEAN=k/5` over the frozen r24+
entries with the **base** registry. Predictions: before 0/5, 0/1, 0/5 (flag
absent → exit 2); after 5/5, 1/1. The population figure is an observation,
not a prediction: every finding is adjudicated as a true criterion-6 defect or
a checker false positive, and true defects are named (calibration), never
hidden by relaxing the check. Legacy (pre-r24) entries are outside criterion
6 and are not graded by it.

## Separability, holds, harms

Each claim is testable with the others absent: C1 changes only the reader's
internal representation (plain output identical), C2 and C3 are separate
flags. Every landed state must hold: selftest PASS with cases 1–161 identical,
`--drift` vs the r12 baseline unchanged from the base result, r1
`VERDICT_BEARING_EXPORTS=3/3`. A harm on any axis (changed legacy output, a
lost refusal, a slower or less bounded mode) voids admission.

## Sourced claim

Claim 2's knowledge entry must cite at least one `SOURCES.md` row opened in
round 26 (registry rows written only after opening, with Gate quote).

## Spec-v1 correction — 2026-10-21, during build (append-only)

The SOURCE contract v1 (`../CORPUS.md:89,107`) overrides two original C3
design choices above: ids are `S` + **three or more** digits (standalone
ASCII alphanumeric/underscore boundaries), and `used-by` is an **exact
repo-relative entry path**, derived relative to `--root` (only leading `./`
is normalized), not a matching basename. The basename rule would falsely
approve a same-named file under another directory. These changes do not alter
the frozen control expectations; S0001 is a valid id (the initial oracle
seat's example saying non-id is superseded).

C2 arithmetic is decimal (strip leading zeros before conversion), never
evaluates user text as a Bash arithmetic expression, and never wraps an
integer. A cadence whose computed date falls outside 0001-01-01 through
9999-12-31, or whose magnitude exceeds safe computation, yields
`due=unknown freshness=unknown`; it does not terminate the process. Existing
six controls and frozen29 predictions remain unchanged. These are input
domain clarifications, not relaxed acceptance thresholds.

## Composition and recovery clarification — same round26 attempt1

When both opt-in metadata flags are given, both independent screens apply:
the per-entry due/freshness fields are retained, registry findings are also
retained, and a single entry/final verdict reflects the union of findings.
Neither flag is silently ignored. With neither flag, the frozen plain-output
hash/rc is still mandatory after cumulative integration, not only after C1.
This composition clarification does not change any frozen control expectation.

The counting script is a probe, not an admission gate: after-values must all
match their registered predictions, the plain-output hash and legacy holds
must agree, and each flag's behavior must withstand independent failing
controls. A standalone `C1_AMPLIFIED=0/4`, classified-entry count, or exit0
does not establish a pass. The build probe-attack report demonstrates these
counterexamples. Its C2/C3 synthetic adapters are not final-code mutations.

Replacement coordinator `ChousaR26R` inherits the original build64 and
pre-registration at `f361d12e`; no new claim or build wave is introduced.
Original unfinished identities may finish their original work, but provider
deaths are retained and never replaced. All final measurements identify the
helper-landed executable bytes; inherited prose is not substituted for runs.
