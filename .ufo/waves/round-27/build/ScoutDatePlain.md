# ScoutDatePlain — C2 plain-mode output stability and the opt-in boundary

Seat: ChousaR27.ScoutDatePlain (leaf, static read-only). Base observed:
64eec5d41c7cf7f17f5ce1e968e28b3769952596 (lane master). No edits, no lane Git/jj writes,
no gate/selftest/differential execution, no locale probe, no installs. All line numbers are
base `tools/research-gate.sh` unless a path is given.

## Assigned item

Map (a) the plain-mode (`verify-metadata` without `--as-of`) output that C2 must leave
unchanged, and (b) which repaired code may execute only under `--as-of`. Static prediction
only; the values below are source-read, not measured.

## Verdict

Plain mode is already locale-stable by construction: `verify_metadata` pins
`local LC_ALL=C` (:2539) before the entry glob (:2557) and before every header regex
(:2594, :2698, :2715, :2721, :2728, :2741, :2744). The C2 repairs split cleanly: leading-zero
normalization lives only in `metadata_add_days` (:2343–2359), which has exactly one caller
inside the as-of gate (:2748); only `metadata_iso_date` (:2295) is shared with plain mode
(:2720), and its C-locale postcondition on ASCII input is unchanged by a locale pin or an
ASCII class. **The C2 acceptance, however, contains no plain-mode control**: every C2 row of
`corpus/evidence/round27-regressions.py:96–121` passes `--as-of`, and the date differential
drives only `--as-of` (`corpus/evidence/round26-date-differential.sh:100`). Plain-mode
preservation is therefore unmeasured unless L1 runs the frozen29 hold and/or adds one plain
row.

## 1. Plain-mode byte contract (must not move)

Scope: `verify-metadata PATH [--root R]` with `AS_OF_ARG_SET=0`; the same bytes must hold when
`--registry` is present, since the as-of code is registry-independent. Source quote
(`corpus/knowledge/recheck-due-r26.md`, 13 words): "`--as-of` is opt-in. Without it the
metadata screen retains its old output."

Ordered output, exactly as printed:

1. Banner `research-gate <VERSION> — ts=<TS_UTC> — mode=verify-metadata — path=%q — root=%q`
   (:2772–2773). `ts` is the only volatile field; the frozen witness drops line 1.
2. One `META entry=<%q basename> source=<present|absent> verified_at=<dated|undated|absent>
   recheck=<scheduled|unscheduled|absent> verdict=<clean|drift>` per entry, enumeration order
   (:2765–2769); `base` is `%q`-quoted at :2578; **no ` due=` and no ` freshness=` field**
   because `freshness_fields=''` at :2736 and only the as-of gate populates it (:2762).
3. Refused entry: `META entry=… source=refused verified_at=refused recheck=refused
   verdict=drift` with an empty suffix (:2620–2625), plus `FINDING META_ENTRY_REFUSED` (:2619).
4. All `FINDING <ID> severity=<…> surface=metadata obs=…` lines after all META lines
   (:2774–2775; emit format :395).
5. `METADATA_COMPLETE=<complete>/<files>` (:2776).
6. `RESEARCH_GATE: <CLEAN|DRIFT> (entries=N complete=N findings=N drift=N)` (:2777–2778).
7. Exit 0 CLEAN / 1 DRIFT (:2780–2781); usage/setup exit 2 with zero anchored
   `^RESEARCH_GATE: ` records (:390).

Locale-dependent ordering is already neutralized: `local LC_ALL=C` (:2539) precedes the
`"$path"/*.md` glob (:2557), so C collation fixes entry order under any inherited locale.

## 2. Opt-in boundary — code that may run only under `--as-of`

`AS_OF_ARG_SET` is initialized 0 at :285 and set only by the CLI at :6283; the mode check and
date validation are :6295–6298; metadata dispatch is :6342–6345. It is never environment-derived.
Executed **only when `AS_OF_ARG_SET=1`**:

| site | base lines | notes |
|---|---|---|
| as-of day precompute | :2548–2552 | `asof_days` only used at :2756 |
| refused-entry suffix | :2620–2623 | empty in plain mode |
| freshness block + `META_RECHECK_OVERDUE` | :2736–2763 (finding :2757–2760) | sole producer of `due=`/`freshness=` and the only new finding |
| `metadata_add_days` | :2343–2359 | one caller, :2748 |
| `metadata_days_from_iso` | :2338–2341 | one caller, :2755 |
| `metadata_civil_from_days` | :2324–2336 | one caller, :2358 |
| `metadata_days_from_civil` | :2310–2322 | callers :2340, :2353, :2355, :2550 — all as-of paths |
| `--as-of` parse/validate | :6281–6283, :6295–6298 | parse needs 2 args; invalid value exits 2 |
| new selftest helper/fixtures | :5983–6087 | test-only, executes only under `--selftest` |

Executed in **both** modes and therefore required to be decision-identical on C-locale input:

- `metadata_iso_date` (:2295–2308), called at :2720 for `recheck=` classification in plain
  mode. It must keep shape (`YYYY-MM-DD`) **and** full calendar validation: `2026-02-30`
  must stay false, or plain case `metadata-invalid-calendar` (:5908–5909) flips
  `recheck=unscheduled` to `scheduled`.
- the function-wide `local LC_ALL=C` at :2539. Do not remove it: the header regexes at
  :2594, :2698, :2715, :2721, :2728, :2741, :2744 all depend on it under UTF-8 locales.
- `emit_finding` (:392–403) is shared; no new finding may be emitted outside the as-of gate.

## 3. Required invariants for the C2 patch

- **I1** Zero normalization stays inside `metadata_add_days`. Do not add a magnitude/length
  test to the plain-mode `recheck` classification (:2721) or the as-of capture (:2741): a
  128 KiB zero-run cadence must still print `recheck=scheduled` in plain mode with no
  `due=`/`freshness=` and no termination.
- **I2** A long zero-prefixed cadence computes its representable value: 131072 zeros + `90d`
  → due = verified-at + 90 days; all-zero → due = verified-at. Out-of-range after
  normalization (> 7 significant digits or past 9999-12-31) stays `unknown`.
- **I3** `metadata_iso_date` rejects non-ASCII decimal digits under every inherited locale
  (function-local `local LC_ALL=C`, or an explicit `[0123456789]` class, or both). Either is
  a no-op for plain mode because :2539 already supplies C; it only fixes the unpinned CLI
  call at :6297.
- **I4** Keep :2539; keep the calendar checks in :2299–2307.
- **I5** Helper functions must remain output-free; all bytes still come from :2772–2778.
- **I6** `freshness_fields` stays `''` in plain mode at both allocation sites; the suffix is
  appended only inside the gate (:2762), never at META assembly (:2765–2769).
- **I7** Exit codes and anchored `RESEARCH_GATE: ` cardinality unchanged (1 record on a real
  run, 0 on usage exits).

Hazards — wrong fixes that would either crash or change plain mode:

- Keeping `${digits##+(0)}` (:2348) → extglob recursion SIGSEGV on long zero runs.
- Replacing it with a shell loop (`while [[ $digits == 0* ]]; do digits=${digits#0}; done`)
  → O(n²) copying on 128 KiB; not termination but an unbounded time cost.
- Evaluating `10#` before stripping → arithmetic on a 131k-digit constant.
- Applying the 7-digit bound before normalization → `0003652058d` becomes unknown
  (breaks the max-span requirement); the bound must apply to the significant suffix.
- Adding a cadence-range finding in plain mode, or rejecting long cadences as
  `unscheduled` — both change plain bytes and are outside the C2 spec.
- Removing `shopt -s extglob` (:256) to dodge the crash: :2348 is the only extglob use
  found, but removing it is unnecessary blast radius; remove only the expansion.

## 4. Existing witnesses and the control gap

- **Byte witness (strongest):** `corpus/evidence/round26-measure.sh:79–83` runs plain
  `verify-metadata` over the frozen 29 entries (populated from the immutable base commit,
  `round26-measure.sh:11–12,30–32`, so r27 knowledge/SOURCES additions cannot alter it),
  drops only the banner and prints `C1_FROZEN_RC` / `C1_FROZEN_SHA`. Recorded baseline
  (`corpus/evidence/round26-measure-before.log:10`, repeated in
  `round26-inherited-after.log:10`):
  `C1_FROZEN_RC=1 C1_FROZEN_SHA=3f83ba4844cac8d2057b47661be225f84a5945fc7c1db739ec2070b6aa2a4a37`.
  Any plain-mode drift in META/finding/complete/verdict bytes changes this SHA. Not run here.
- **Plain selftest:** `metadata_case` (:5704–5745) invokes plain mode at :5722; 26 plain
  invocations (:5754–5985) assert full META-line substrings, `METADATA_COMPLETE`, and the
  summary. They are substring checks: an **appended** ` due=…`/` freshness=…` after
  `verdict=clean` would still pass, and no case asserts absence of these fields.
- **No C2 plain control:** `round27-regressions.py` `run()` defaults to plain mode (:60–66)
  but every C2 row passes `--as-of` (:110–121); `round26-date-differential.sh` only builds
  `--as-of` batches (:100). The claims' "preserve … plain mode" (`round27-claims.md:11`,
  12 words: "Preserve year1–9999, strict as-of>due overdue semantics, calendar arithmetic,
  and plain mode.") is therefore unmeasured by the r27 counting command.

## 5. Suggested plain-mode controls (new rows; no existing assertion weakened)

Use the existing `run()` with no options (plain mode) and the same synthetic entry helper:

1. `C2/plain-zero-prefix`: entry `verified-at: 2026-01-02 checked`, `recheck: <131072 zeros>90d`.
   Expect rc 0; exactly one line matching
   `^META entry=entry\.md source=present verified_at=dated recheck=scheduled verdict=clean$`;
   `METADATA_COMPLETE=1/1`; `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`;
   zero lines matching `^META entry=.*( due=| freshness=)`.
2. `C2/as-of-zero-prefix` (paired): same file with `--as-of 2026-10-21`; expect rc 1 and
   `due=2026-04-02 freshness=overdue` with exactly one `^RESEARCH_GATE: ` record. This is the
   opt-in proof: plain row stable, as-of row computes.
3. Optional hold: run `bash corpus/evidence/round26-measure.sh <tree> c1` from an isolated
   copy and require `C1_FROZEN_RC=1` and SHA `3f83ba48…`; this is the only byte-exact plain
   witness and it is population-immutable.

## 6. Observed candidate delta (ExecDates clone, static)

The in-progress diff in `.ufo/waves/round-27/work/ExecDates` (base 64eec5d) adds
`local LC_ALL=C` to `metadata_iso_date` and `metadata_add_days`, replaces :2348 with
`[[ $digits =~ ^0*([0-9]*)$ ]]` + `BASH_REMATCH[1]`, and adds a locale usage helper plus
128 KiB fixtures. Static assessment against §2: the ERE capture executes only through
`metadata_add_days` (opt-in); the locale pins are idempotent under :2539, so plain output is
predicted unchanged. Two flags:

- The Unicode usage case prints `skip-case` when no installed locale admits Unicode digits.
  A skip is not a passing control; the independent control remains
  `round27-regressions.py:118–121` (`LC_ALL=en_US.UTF-8`), which also forbids
  `cannot change locale`. L1 should record which branch actually ran.
- No plain-mode row is added; §5 is still needed for the "preserve plain mode" acceptance.

## Unrun checks

No gate, selftest, differential, regression, locale-enumeration or SHA recomputation was run;
the frozen SHA and rc are inherited receipts, not remeasured. No network, host, /proc,
live-process, strace, mount, namespace or debugger probe. LSP was not queried for this item
(static shell source, no server attached to the lane files).

## Remaining unknowns

- Bash glob collation under a function-local `LC_ALL=C` is taken from shell semantics, not
  executed here.
- Whether the integrated tree will still carry :2539 after the C1/C3 patches; L1 should diff
  the final `verify_metadata` before accepting plain-mode preservation.

VERDICT: C2 can be repaired without touching plain-mode bytes — cadence normalization is
structurally as-of-only and the shared `metadata_iso_date` hardening is a C-locale no-op — but
the r27 control set does not currently observe plain mode, so the frozen29 SHA hold and one
new plain/opt-in row are required to make that preservation falsifiable.
