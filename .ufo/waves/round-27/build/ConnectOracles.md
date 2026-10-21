# ConnectOracles — date oracle × registry finding multiplicity

**Assigned item:** connector for C2/C3. Connect the date independent oracle with registry finding
multiplicity and propose a bounded final regression schema. This is read-only analysis: no gate,
selftest, differential, fixture, build, lint, or formatter was executed; no tool was installed. The
only observed execution was a pure-Python `int()`/`datetime` check, labeled [OBS] below. Nothing
here is an admission or a pass claim.

**Read-time identities (the tree moved during this seat).** Base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`.
`tools/research-gate.sh` sha256 `8ee706b29a6c013db5459a70ada2c07eba387788707a3bde7c40a96c75ac4f8f`
(mtime 11:38): the C1 usage-helper repair is already present (`:6010-6028`) with three synthetic
controls (`:6108-6113`); C2 `:2348` and C3 `:2412-2415`, `:2503`, `:2375-2382`, `:2477-2504` still
read as base. `corpus/evidence/round27-regressions.py` exists (untracked at read time), sha256
`3198bf2184637df5715dc5ae4777b7af7b5810c3ba3ae72fcfd0ba3f158aa751`, 183 lines. Because integration
was still landing, the schema below is stated against observable behavior and exact current locations,
not against this byte snapshot.

## 1. The connection: one comparator cannot serve both channels

[SOURCE] The date channel is functional. One `META entry=` record is built per file and printed once,
carrying exactly one `due=`/`freshness=` pair (`tools/research-gate.sh:2737-2768`, `:2774-2778`).
Duplicate records for one entry are therefore a defect, not multiplicity.

[SOURCE] The registry channel is multiset-valued. `metadata_registry_check_source` scans and emits one
finding per matched token occurrence (`tools/research-gate.sh:2477-2504`); `emit_finding` increments
`N_FINDINGS` per line and `N_DRIFT` per warn/crit line (`:392-399`). Two real standalone occurrences
must yield two findings; one occurrence re-scanned must not. The r27 pre-registration already fixes
per-occurrence semantics: `source:` "yields every `\bS[0-9]{3}\b` token"
(`corpus/evidence/round26-claims.md:96-97`), and the current r27 control expects `S002,S002` → 2
(`corpus/evidence/round27-regressions.py:149`).

[CONTRADICTION — calibration] The landed r26 registry oracle erases that same multiplicity:
`source_ids = set(...)` and `findings: set[str]` returned as a sorted list
(`corpus/evidence/round26-registry-oracle.py:122-123,144`), and the driver compares sets
(`corpus/evidence/round26-registry-differential.sh:244-247`). Yet the r26 build report claims
"finding lists retain per-token multiplicity" (`.ufo/waves/round-26/build/ExecC3Oracle.md:39`). The
report and the landed bytes cannot both be right; the bytes are set-based.
`.ufo/waves/round-26/falsify/FRegistryIdBoundary.md:76-98` already observed ×2/×3 duplicate
emissions that this oracle and driver cannot see. Therefore the r26 registry differential remains a
valid finding-ID-set guard on its frozen populations, but it must not adjudicate r27 occurrence
counts. Reusing it would either force dedupe (the wrong fix) or hide duplicate emission.

[OBS — pure Python, no gate] The date oracle has the mirror hazard. `int('0'*131072 + '90')` raises
`ValueError: Exceeds the limit (4300 digits) for integer string conversion`; `int('9'*131072)` also
raises; `date.fromisoformat` rejects the Unicode-digit forms. An oracle that computes
`due = verified + timedelta(int(raw_token))` terminates in the oracle on the required 128KiB
leading-zero fixture — the same failure class as the gate's `digits=${digits##+(0)}` at `:2348`. The
current script sidesteps this by hardcoding the 128KiB due (`round27-regressions.py:97-98`), which is
a literal, not an oracle. This is the non-obvious connection: both sides of the differential must be
long-decimal-safe, or the control measures its own stack.

[SOURCE] The accounting channel is where the two meet. `findings=` is the number of emitted finding
lines and `drift=` the number of warn/crit lines under `CHOUSA_STRICT=0` (`:392-399`, summary
`:2777-2778`). No current case constrains either: the date block checks only `^META entry=` and one
verdict (`round27-regressions.py:113-115`), and the registry block counts only two codes
(`:153-155`). A net-zero substitution — one phantom id replacing one real id with the same code —
passes both.

## 2. Bounded final regression schema

One record per case, emitted as JSON and compared in one pass:

```
Case(id, claim, entry_path, source, verified, recheck, options[], locale,
     rc, meta=(due, freshness, verdict) | None,
     findings=Counter((code, key)), complete,
     summary=(entries, complete, findings, drift) | None,
     baseline_skip=False)
```

**Date oracle (functional; conversion-safe).**
`shape(s) = re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s, re.ASCII)`; calendar validity via
`date(y,m,d)`; `recheck` first whitespace token only (spec v1, `round26-claims.md:59-74`);
`on-release` → `(on-release, event)`; other → `(unknown, unknown)`; `Nd`:
`sig = digits.lstrip('0') or '0'`; if `len(sig) > 7` → unknown (maximum representable span is
3,652,058 days, [OBS]); else `int(sig)`, `verified + timedelta(days=...)`, `OverflowError` →
unknown; freshness is `overdue` iff `as_of > due` strictly. The oracle must assert internally that
`int()` is called only on ≤7 significant digits, and self-check the normalizer on
`'0'*131072+'90'` → 90, `'9'*131072` → unknown, `'0'*65536+'1'+'0'*65536` → unknown. `refused`
entries carry `(refused, refused)`.

**Registry oracle (multiset; multiplicity-preserving).**
Tokenize once, ASCII-only, with a single split: `re.split(r"[^A-Za-z0-9_]+", source_value)`; keep
tokens fully matching `S[0-9]{3,}`; `Counter` the tokens. Resolve first-wins rows from a fresh
named header whose delimiter has exactly the header's cell count. One expectation per token:
missing row → `META_SOURCE_ROW_MISSING`; status ≠ `mined` → `META_SOURCE_NOT_MINED`; mined but no
exact root-relative `used-by` token (after removing leading `./`) → `META_SOURCE_USEDBY_MISSING`.
No tokens → one `META_SOURCE_NO_ROW_ID` (info). Date-only `verified-at` → one
`META_VERIFIED_AT_BARE`. Do not use `set`, and do not reuse the r26 oracle.

**Comparator.**
Parse only anchored lines and compare exactly:
- `^META entry=([^ ]+) .*$` — exactly one per entry; parse `due=`, `freshness=`, `verdict=`; a
  duplicate is a hard failure.
- `^FINDING (CODE) severity=(info|warn|crit) surface=metadata obs=entry=([^ ]+)(?: .*)?$` — key
  `(code, source_id)` for the three source findings, `(code, '')` for the two entry findings,
  `(code, due)` for overdue, `(code, reason)` for refused. Compare the `Counter` and each expected
  severity exactly. No substring matching for records.
- `^RESEARCH_GATE: (CLEAN|DRIFT) \(entries=E complete=C findings=K drift=D\)$` — exactly one;
  `K == |expected Counter|`; `D == count(expected warn|crit)` under `CHOUSA_STRICT=0`; `E`/`C` as
  declared. This is a preservation assertion for the current counter behavior at `:392-399`, not a
  new semantic claim.
- Exit-2 cases: zero `^RESEARCH_GATE: `, zero `^META entry=`, zero `^FINDING `; diagnostic present;
  forbid raw Bash diagnostics (`invalid integer`, `arithmetic syntax`).
- Fixture hygiene: no synthetic line may itself match `^(META entry=|FINDING |RESEARCH_GATE: )`;
  entry names are ASCII-safe `[a-z0-9-]+\.md` so `printf %q` at `:2578` is the identity.

## 3. Case matrix — deltas over the current script

Keep the existing cases; add the following (all synthetic, temp dirs only):

1. **Date preservation:** `on-release` → event; `when-needed` → unknown; plain mode (no flags) emits
   no `due=`/`freshness=` and no `META_RECHECK_OVERDUE`; one NUL entry under `--as-of` →
   `META_ENTRY_REFUSED` crit plus `due=refused freshness=refused`, rc1. Current block lacks event,
   unknown, refused, and plain (`round27-regressions.py:96-105`).
2. **Date arithmetic strength:** `000100d` → 2026-04-11 (kills a global/trailing zero delete);
   `'9'*131072` → unknown; `'0'*65536+'1'+'0'*65536` → unknown; `--as-of 0000-01-01` and
   `--as-of 10000-01-01` → exit 2; one valid ASCII overdue case run under `LC_ALL=C` and a UTF-8
   locale must have identical records (locale independence in both directions).
3. **Registry multiplicity:** `S001,S001` with `used-by: —` → `USEDBY_MISSING` ×2;
   `S999,S999` → `ROW_MISSING` ×2; continuation-line case `x S001S003\n  S001` → 0; `éS002` →
   `NOT_MINED:S002` ×1 (ASCII boundary; a non-ASCII neighbor is a boundary); no-token source
   `xS002 S002x` → one `NO_ROW_ID` info, rc0. Current block covers only `NOT_MINED` and
   `ROW_MISSING` counts and no continuation/unicode/no-id case (`:142-150`).
4. **Registry table state:** HDR(3), prose, unnamed 4-cell `a b c d` + 4-cell SEP → exit 2 (a
   width state must be cleared with the columns; current `:126-134` has no stale-width case);
   unnamed table with no named header at all → exit 2; fresh header after a break remains accepted
   (existing `reorder-clean`).
5. **Registry refusal arms:** NUL registry → exit 2 `refused: nul`; multilink registry → exit 2
   `refused: multilink`. Cheap guards that the denylist refactor did not reorder the refusal arms
   (`:2361-2407`). Not new contract; preserve existing behavior.
6. **Denylist completeness:** existing raw/canon cases plus `synthetic.env:1` → still refused
   (monotone guard: prefix matches `*.env`, full path ends `.env:1`; a full-path-only fix turns this
   into a read), symlink to `a:b/.config/reg.md` → refused, root containing a colon with relative
   `.config` → refused, and entry `synthetic:fixture/.config/entry.md` →
   `META_ENTRY_REFUSED reason=denylist`. The claim sentence is gate-wide
   (`corpus/evidence/round27-claims.md:15`); if L1 scopes the entry arm out, record it as a named
   residual instead of silently dropping the control.
7. **Composition (the connector's core):**
   - `compose-overdue-two-ids`: `source: S002,S002`, `verified-at: 2026-01-02`,
     `recheck: 90d`, `--as-of 2026-10-21`, registry `S002 queued`. Expected: one META
     `due=2026-04-02 freshness=overdue verdict=drift`; `NOT_MINED:S002` ×2; `RECHECK_OVERDUE` ×1;
     `findings=3 drift=3`; `entries=1 complete=1`.
   - `compose-current-clean`: `S001` mined/exact used-by, current date → one META current/clean;
     `findings=0 drift=0`.
   - `compose-info-not-drift`: no-token source plus current date → one `NO_ROW_ID` info,
     `findings=1 drift=0`, verdict clean.
   Current script never passes both flags together.

## 4. Baseline, final, and C1 receipt

**Baseline skip.** Add `--baseline-receipt PATH` (default off). With it, skip only exact case ids
whose cadence has a leading zero run ≥ 65,536 (`leading-128k-zeros`, `allzero-128k`, and any
Z-prefixed variants such as `Z+100d`, `Z+3652058d`, plus the interleaved-zero case); verify the
receipt sha256 and a quoted line (`exit 139`, `.ufo/waves/round-26/falsify/FDateHugeCadence.md:6-11`;
that report is tracked) before printing `BASELINE_SKIP <id> receipt=<sha256>`. Never auto-skip from
an observed signal. The default final run has no skip, uses a 10 s cap on zero-run cases and 30 s
otherwise, and treats a signal death as a mismatch. The script bytes stay the same for both runs;
only the explicit interface differs. Base is expected nonzero and its mismatch-id set is recorded;
final must exit 0.

**C1 receipt (separate command, not the script's exit).** Parse `--selftest` output: exactly one
`RESEARCH_GATE_SELFTEST: PASS (N cases)`; unique `ok-case` names; the three former failures
(`metadata-asof-invalid`, `-missing`, `-wrong-mode`) present; first-161 `ok-case` lines hashing to
`LEGACY_CASES_SHA=5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb`
(`corpus/evidence/round26-inherited-after.log:42-43,48`); `N = 187 + new`. The in-gate controls
cover CLEAN but not DRIFT (`tools/research-gate.sh:6108-6113`); the script's isolated helper block
covers both (`round27-regressions.py:79-93`). Add the DRIFT control in-gate or state that the
independent DRIFT control is the script's, since the claim names "actual CLEAN/DRIFT verdict fails".

**Legacy guards.** Keep `corpus/evidence/round26-date-differential.sh` (functional due/freshness
only; no registry) and `round26-registry-differential.sh` (set-level finding IDs; not multiplicity).
Run both on isolated copies; neither substitutes for the new Counter channel.

## 5. Risks and contradictions to state, not smooth

- **Per-occurrence vs dedupe.** "No duplicate occurrences" in `round27-claims.md:15` can be read two
  ways. Per-occurrence is the only reading consistent with r26's "every token", the r26 build
  report's stated intent, and the current `S002,S002 → 2` control. A dedupe implementation would be
  a claim amendment, not an oracle edit.
- **`drift=` per finding.** Current code counts each warn/crit finding (`:392-399`), not entries with
  a finding. The schema asserts that preserved behavior. If integration defines drift per entry,
  that is a behavior change requiring explicit disposition.
- **r26 oracle set collapse.** Do not reuse it for r27; its own report contradicts its bytes.
- **Locale availability.** `en_US.UTF-8` may be absent; require a locale precheck and report
  `BLOCKED` (exit 2) rather than a silent pass. The r26 receipt lists `C`, `C.utf8`, `en_US.utf8`
  (`.ufo/waves/round-26/falsify/FDateAsOfUsage.md:25-26`).
- **Entry-side denial scope.** If C3 is scoped to the registry reader only, the entry/claims arms
  remain inherited bypasses; name them as residuals, do not claim gate-wide complete-path denial.
- **Counter scope.** Asserting `findings=`/`drift=` is output self-consistency under a pinned
  `CHOUSA_STRICT=0`, grounded in the current emission code; it is not a resource or semantic claim.

## 6. Unrun checks (L1, once after integration)

- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` — final tree, exit 0,
  zero mismatches; base archive with `--baseline-receipt .ufo/waves/round-26/falsify/FDateHugeCadence.md`
  — expected nonzero with the named skips.
- `bash tools/research-gate.sh --selftest` — PASS, 187 original identities plus the new controls.
- `bash corpus/evidence/round26-date-differential.sh` and
  `bash corpus/evidence/round26-registry-differential.sh` on isolated copies — both exit 0; the
  latter is set-level only.
- Plain-mode frozen hash/rc and the r26 holds from `corpus/evidence/round26-measure.sh`, on an
  isolated copy.

**Touched surface:** `.ufo/waves/round-27/build/ConnectOracles.md` only. No production code, test,
fixture, oracle, differential, or gate was edited; no gate or test was executed; no tools installed.
