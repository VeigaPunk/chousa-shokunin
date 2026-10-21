# ScoutIntake — r26 routed self-defects into C1/C2/C3/carried

Read-only static intake for round27/attempt1. Base observed: `git rev-parse HEAD`
= `64eec5d41c7cf7f17f5ce1e968e28b3769952596`. No gate, selftest, counting
command, differential, build, lint or runtime probe was executed. No files
outside this report were written; no tools installed. No LSP device was mounted
in this session, so symbol tracing below is literal source reading with exact
line anchors, not semantic proof. Reported r26 failures are used as ground
truth and were not rerun.

## 1. Closure row and lesson intake (read-only)

`MANIFEST.json` `rounds[414]` is the chousa round26 closure:
`admitted:false`, `verdict:"rejected-harmed"`, `verdicts.operability/
freshness/calibration:"harmed"`, `claims.C1.verdict:"unprovable"`,
`claims.C2/C3.verdict:"harmed"`.

`rounds[414].verification.routed_defects` says, in full:

> "Shared selftest usage assertions, C2 domain/locale/termination, C3 header
> state/token identity/refusal/resource/oracle gaps; incomplete31 falsify
> assignments. Carried concurrent JSON appender race, other readers,
> parent-root/receipt/source-span pairing debt and round12 authentic-dispatcher
> Receipt identity L0 remain open."

`rounds[414].verification.selftest_harm` records the decisive C1 fact:
`FAIL(3/187 cases)` and exit1 at `.ufo/waves/round-26/` evidence, versus a
before-state `PASS161/exit0`; mechanism is the usage harness predicate, not the
gate's usage behavior. Lesson anchors: `corpus/lessons/round-26.md:163`
(FAIL3/187), `:177-183` (R26-M5 through R26-M11), `:190-191` (C1 narrow,
C2/C3 withdrawn). R26-M9 explicitly leaves the inherited entry-reader
colon-path residual open; R26-M10 withdraws any general resource-bounded
registry claim; R26-M11 limits oracle agreement to observed shapes.

## 2. Routing table (defect -> claim -> base code site -> required outcome)

| # | routed self-defect | claim | r26 evidence | base code site (observed) | required outcome |
|---|---|---|---|---|---|
| 1 | Usage harness rejects its own help text: unanchored verdict substring | C1 | `.ufo/waves/round-26/falsify/FNoTrade.md:115-137`; lesson R26-M5 `:177` | `tools/research-gate.sh:6016` inside helper `:6010-6023`; the three cases `:6083-6087`; aggregate `:6242` | Count anchored `^RESEARCH_GATE: ` records, require 0 for usage. Preserve all three case identities, expected exit2, and required diagnostics. |
| 2 | Date shape accepts non-ASCII decimal digits; arithmetic aborts outside the usage guard | C2 | `FDateAsOfUsage.md` F1 | `metadata_iso_date` `:2295-2305`, regex `:2296`, arithmetic `:2297`; CLI check `:6297` is outside the `local LC_ALL=C` at `verify_metadata` `:2539`; second arithmetic `:2549-2550` | ASCII `YYYY-MM-DD` under any inherited locale; non-ASCII digits exit2 with the usage diagnostic, zero verdict records, no raw Bash arithmetic diagnostic. |
| 3 | Recursive `+(0)` leading-zero strip terminates with SIGSEGV before the length bound | C2 | `FDateHugeCadence.md` F1 | `metadata_add_days` `:2343-2355`; strip `:2348`; 7-digit bound `:2350`; arithmetic `:2353` | Nonrecursive decimal normalization. 128KiB leading-zero cadence computes its representable value; all-zero is 0; out-of-range remains unknown; no termination. |
| 4 | Registry header columns survive a non-pipe line and accept a later headerless table | C3 | `FRegistryHeaderless.md:41-83` (R26-M7) | `metadata_registry_load` `:2410-2468`; non-pipe branch `:2412-2415` sets only `header_candidate=0`; indices reset only at `:2454` and `:2466` | Reset `id_col`/`status_col`/`usedby_col` on every non-pipe line; a table is accepted only after a fresh named header. |
| 5 | Header/delimiter cell counts are never compared | C3 | `FRegistryHeaderless.md` FRH-2 G01/G02/G09 | separator branch `:2443-2451` checks only cell shape `^:?-{3,}:?$`; header width is not stored | Separator row must have the same cell count as the header candidate; otherwise no table, exit2. |
| 6 | Consumed-text rescan invents ids and duplicates findings from non-standalone tokens | C3 | `FRegistryIdBoundary.md`; `FRegistryAbsentRow.md` R26-FRA-1; lesson R26-M8 `:180` | `metadata_registry_check_source` `:2472-2506`; prefix strip `:2503` | Advance by match position or tokenize. Standalone ASCII S-ids only; no invented ids; one finding per real occurrence; preserve genuine repeats (`S002,S002` = 2). |
| 7 | Denylist checks truncate a filesystem path at the first `:` | C3 | `FRegistryRegistryDeny.md` FRRD-1; lesson R26-M9 `:181` | `ptr_file_part` `:573-576`; `is_denylist_path` `:595-606` uses it at `:596`; registry calls `:2375` and `:2382`; entry calls `:2584` and `:2591`; canonical pointer target `:636` | A filesystem-path predicate must match the complete path at filesystem call sites; citation-pointer callers keep existing prefix semantics; a denylisted registry path with an earlier `:` is refused before opening. |

## 3. C1 — operability detail

Observed mechanism: `die_usage` (`:390`) always prints `usage` (`:388`), and
`usage` contains the literal line `:385` `Verdict: RESEARCH_GATE: CLEAN|DRIFT`.
The helper at `:6016` rejects any output containing the substring
`RESEARCH_GATE: `; therefore every usage exit contradicts its own required
`rc=2` and the three cases `metadata-asof-invalid`, `metadata-asof-missing`,
`metadata-asof-wrong-mode` (`:6083-6087`) always fail. This is the wrong-layer
assertion named by R26-M5, not a gate behavior defect.

Repair shape (advice, not an edit):

- Mirror the already-correct anchored counter used by `metadata_asof_case`
  (`:5993`): `nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)`, then
  require `${nverdict:-0} -eq 0`. The anchored form ignores the mid-line
  `Verdict: RESEARCH_GATE:` help text and still rejects a real CLEAN/DRIFT
  record at line start.
- Keep `rc=2`, keep the expected diagnostic substring, and keep all three
  case names/argument shapes unchanged. Do not delete cases, relax exit2, or
  accept a verdict on a usage error.
- The independent controls already persisted in
  `corpus/evidence/round27-regressions.py` extract this helper and run a stub:
  correct usage passes; a CLEAN record fails; a DRIFT record fails; exit1
  fails; a missing diagnostic fails; a mid-line non-record mention
  (`note RESEARCH_GATE: not a record`) passes. The helper must stay
  self-contained (no call to another gate function), because the control runs
  its extracted body against a stub.
- Acceptance: full selftest PASS with all 187 original case identities
  preserved; legacy 161 unchanged; numeric score3 remains frozen at r26; no
  resource-safety inference from C1.

## 4. C2 — freshness detail

Two independent defects, both observed at base source:

1. **Locale-dependent date grammar.** `metadata_iso_date` (`:2295`) tests
   `^([0-9]{4})-([0-9]{2})-([0-9]{2})$` at `:2296`. Under a UTF-8 locale Bash's
   `[0-9]` admits non-ASCII numeric code points; the subsequent `10#` arithmetic
   at `:2297` aborts. The CLI check at `:6297` is outside the function-local
   `LC_ALL=C` that `verify_metadata` sets at `:2539`, so the invalid value is not
   converted to the required usage exit2. The reported result is raw Bash
   diagnostics and exit1 (the DRIFT code), with a later abort at `:2550`.
   Required: make the grammar ASCII under any inherited locale (function-local
   `LC_ALL=C` and/or explicit `[0123456789]`), then validate and only afterward
   perform `10#` arithmetic. This must cover every `metadata_iso_date` caller
   (`:2297`, `:2345`, `:6297`, and the entry-side callers already inside the
   pinned `verify_metadata`).
2. **Recursive normalization.** `metadata_add_days` at `:2348` executes
   `digits=${digits##+(0)}` before the `:2350` seven-digit bound. The extglob
   `+(0)` match recurses with run length; reported long leading-zero runs reach
   SIGSEGV with no output, while the same token in plain mode survives.
   Required nonrecursive normalization: strip leading zeros with a bounded
   expression (for example a `^0*([0-9]*)$` match and `BASH_REMATCH`), map an
   empty result to 0, then apply the seven-digit bound and `10#`. Out-of-range
   stays `due=unknown freshness=unknown` with exit0; in-range values compute
   normally.

Persisted C2 controls (`corpus/evidence/round27-regressions.py`): Unicode-digit
rejection under `C` and `en_US.UTF-8` with exit2 and no verdict; 128KiB
leading-zero cadence (`0…090d` -> due `2026-04-02`); 128KiB all-zero cadence;
40-digit huge magnitude -> unknown; maximum representable span
(`0003652058d` -> `9999-12-31`); overflow (`3652059d`) -> unknown; leap
1900/2000/2028/2100; decimal `08d`/`09d`. Preserve years 1–9999, strict
as-of > due overdue semantics, calendar arithmetic, and plain mode. Existing
date differential must remain at 0 mismatches without weakened expectations.

Carried C2 spec gaps, not acceptance items: duplicate `--as-of` is last-wins
(`FDateAsOfUsage.md` F2), arguments after `--` are ignored (pre-existing),
duplicate `verified-at` is last-wins, `freshness=unknown` carries no finding,
and the frozen measure/differential oracles are Unicode-permissive
(`FDateInvalidVerified.md` side finding 1). Report these; do not silently
tighten the oracles.

## 5. C3 — calibration detail

Three repair classes, matching the three reported failures:

1. **Header state (`FRegistryHeaderless`).** On a non-pipe line the loader
   (`:2412-2415`) clears only `header_candidate`, leaving the three column
   indices live. The next pipe line can therefore be treated as a header
   candidate by the all-three-`>=0` test (`:2463`), and a following delimiter
   accepts the table (`:2448-2451`) even though its cells never named the
   columns. Reported blast radius: on the target `SOURCES.md` with a prose
   column mention and a blank line prepended, the gate produced 11 false
   `META_SOURCE_NOT_MINED` findings (exit1) where the oracle was clean;
   minimal pair S01 vs C01 isolates the stale-index trigger. Fix by resetting
   all three indices on every non-pipe line. Also
   store the header candidate's cell count and require equality with the
   delimiter row's cell count; the separator loop currently validates only
   dash shape. This is required for the persisted `delimiter-too-short` and
   `delimiter-too-long` controls. Keep the `reorder-clean`/`reorder-queued`
   behavior (a fresh named header after prose is accepted and columns are
   rebound by name), and keep exact `used-by` path matching.
2. **Token identity (`FRegistryIdBoundary`, `FRegistryAbsentRow`).** The loop
   at `:2476-2504` consumes with `source_scan=${source_scan#*"$source_match"}`
   (`:2503`), which strips to the first textual occurrence rather than the
   match position. When an id is end-anchored, an earlier glued token such as
   `S001S002` is cut open and the suffix is re-anchored at `^`, inventing
   `S002`/`S003`/`S0003` and inflating findings. Reported effect: four of four
   trigger fixtures became false positives (clean entries reported as drift,
   exit1), and non-standalone duplicates emitted 2–3 identical finding lines
   instead of 1. Fix by advancing from the
   match position or by exact-token scanning with ASCII
   alphanumeric/underscore boundaries (pin `LC_ALL=C` so a non-ASCII suffix
   remains a boundary, preserving the observed `S999é` behavior). Preserve
   3+-digit ids (`S0001`, `S12345` valid; `S01` invalid), genuine repeated
   occurrences (`S002,S002` = 2 findings), and the no-id info finding.
3. **Filesystem-path refusal (`FRegistryRegistryDeny`).** `is_denylist_path`
   (`:595-606`) calls `ptr_file_part` (`:573-576`), which cuts at the first
   `:`. The registry loader applies it to the raw path, `readlink -f` canon and
   `/proc/$$/fd` canon (`:2375`, `:2382`), so `a:b/.config/reg.md` is opened
   and parsed. Reported matrix: 16/16 colon-free deny shapes refused before
   `openat`; 6/6 colon shapes bypassed, read and parsed to CLEAN (rc0).
   Add a sibling full-path predicate that matches the patterns
   against the normalized complete path, and use it at filesystem call sites.
   Keep `is_denylist_path` for citation-pointer inputs (`:621`, `:650`,
   `:1129`, `:1598`) so existing citation-anchor semantics do not change.
   Filesystem sites include registry raw/canon/fdcanon (`:2375`, `:2382`),
   entry raw/canon/fdcanon (`:2584`, `:2591`), and the canonical target in
   `ptr_resolves_meta` (`:636`). The registry path must be refused before
   `exec {registry_fd}<`; a benign colon path (`synthetic:ordinary.md`) stays
   accepted. The persisted controls cover plain denied component, denied
   component after an earlier `:`, denied `.env` suffix after an earlier `:`,
   and the ordinary-colon negative control.

The C3 claim's wording is general ("filesystem-path denylist checks"), while
the reported failure and persisted path controls exercise `--registry`. The
entry-reader colon bypass is an inherited residual (R26-M9, `FRRD-2`). If the
executor applies the new predicate to `:2584/:2591` as well, record that as an
additional synthetic control or explicitly label it unverified; do not claim
the inherited residual repaired on the registry control alone. Existing
well-formed registry behavior and exact used-by rules remain acceptance
conditions.

## 6. Carried — must be reported, not claimed by C1/C2/C3

- Registry resource/output growth: `FNoTrade.md` F2 (pipe-dense load,
  ~270 bytes RSS per input byte, quadratic time), `FOverlap.md` F1
  (one finding per id occurrence; extrapolations are report inferences, not
  measurements here), `FRegistryIdWidth.md` F2 (quadratic `source:` strip).
  A tokenization fix removes the strip's quadratic step but does not bound
  per-occurrence output or the pipe-cell allocation. No "bounded registry"
  claim; QUALITY18 unit naming applies.
- Inherited entry-reader colon bypass (`FRegistryRegistryDeny.md` FRRD-2) if
  not covered by the full-path predicate.
- Registry grammar/oracle limits: fence/indent/comment/blockquote and
  first-table-wins (`FRegistryHeaderless.md` FRH-4), two-table selection and
  duplicate `source:` last-wins (`FRegistryAbsentRow.md` notes), gate/oracle
  whitespace and `strip("|")` differences (`FRH-3`, `FRegistryBareVerified.md`
  F1/F3), `META_VERIFIED_AT_BARE` being a nonblank-tail screen only
  (`FRegistryBareVerified.md` F2), silent malformed ids
  (`FRegistryIdWidth.md` O1).
- Backlink identity depends on caller `--root`; symlink identity is
  undocumented (`FOverlap.md` F2). Not changed by the denylist predicate.
- Concurrent JSON appender race, other readers, parent-root/receipt/source-span
  pairing debt, and round12 authentic-dispatcher Receipt identity L0
  (`rounds[414].verification.routed_defects`). These are outside C1–C3.
- r26 verification incompleteness: 31 falsify assignments returned no report;
  missing reports are not green. No missing finding is inferred clean.
- Public-source conclusions from r26 stay withdrawn unless independently
  revalidated; no full criterion6 semantic verification and no new
  field-readiness claim follows from these repairs.
- C1's allocation result is narrow (four frozen shapes) and score3/10 is
  frozen; no universal resource-safety inference. Long-token crash baseline
  for the final counting run uses the committed r26 failure receipt; the unsafe
  old reproduction is not rerun and its baseline skip must be recorded
  explicitly.

## 7. Checks not run here / L1 verification obligations

Not run by this seat: `bash tools/research-gate.sh --selftest`,
`python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`,
the date and registry differential scripts, frozen metadata checks,
`round26-measure.sh`, any 8MiB or long-token probe, build/lint/formatters.
No reported r26 failure was reproduced.

L1 runs verification once after all changes land. Expected observable results:
the counting command on an isolated base archive shows the C1/C2/C3 baseline
mismatches (with the unsafe long-token baseline skip recorded and the committed
r26 receipt cited); the same command unchanged on the integrated tree reports
`mismatches: 0` with its three per-claim totals; the full selftest reports
PASS with all 187 original case identities preserved and the new independent
harness controls passing. Record the actual case total as observed (a tree
carrying the three added in-selftest control cases would report 190 absent
other changes), rather than asserting the original 187-case total by
assumption. The existing date differential and frozen metadata checks retain
0 mismatches and unchanged expectations. Record all exit codes.

Report trailer: seat `ChousaR27.ScoutIntake` (leaf scout); lane root = this
directory (`chousa-shokunin`); base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`;
read-only static intake; production edits: none; installs/updates: none; LSP:
not mounted, so line anchors are literal source reads; unrun checks listed
above; this is author-lane advice, not outside admission.

## 8. Addendum — concurrent working-tree observation (added after initial write)

After the source reads above, `git status`/`git diff` showed uncommitted
production-lane changes I did not make and did not execute: `tools/
research-gate.sh` (+27/-1), `corpus/QUALITY.md` (+18), `corpus/SOURCES.md`
(+11), and an updated `corpus/evidence/round27-regressions.py`. The gate diff
inserts a C1 helper `metadata_asof_usage_accepts()` at working-tree
`:6010-6014`, calls it from `metadata_asof_usage_case()`, and adds three
`metadata_asof_usage_control_case` cases at `:6108-6113`. No C2/C3 gate hunk
was present at observation time.

Consequences for this report, stated as static observations only:

- All line anchors in sections 2–5 are **base** (`64eec5d4`) anchors. The
  working-tree C1 insertion shifts later gate lines by +5; re-resolve anchors
  against the base commit or the private clone, not the dirty file.
- The persisted control script in the working tree now extracts both
  `metadata_asof_usage_accepts` and `metadata_asof_usage_case`, so the original
  self-containment caveat in §3 is superseded for that version: any helper the
  extracted body calls must be in the extraction list. The anchored-count
  predicate itself is the claimed shape.
- The three added selftest cases would make the working-tree selftest count
  190 against the reported 187-case base, absent any other case change. The
  claim requires all 187 original identities preserved, not a silent
  total change; L1 should verify original identities explicitly and record the
  added-control count, rather than treating a `(190 cases)` PASS line as the
  original 187-case hold by itself.
- No status is claimed for these concurrent changes: they were not run. This
  addendum does not review or admit them.
