# RevPreregC3 — C3 falsification (registry link). Seat ChousaR26.RevPreregC3-3, 2026-10-21

Reviewed: frozen spec `corpus/evidence/round26-claims.md` (f361d12, Claim 3) against landed
candidate `tools/research-gate.sh` at 0e9784b (gate sha256 c2c813f1b425bc4e…, worktree-clean;
tree changed mid-session — my first pre-landing grep for "registry" returned zero hits).
Axes: falsification power, construct validity (spec↔impl↔QUALITY 6), gaming resistance, blast
radius, evidence sufficiency. Static review only; no gate/probe executed; no installs.

## Findings

- HIGH (spec↔impl drift, silent) Tokenizer width: spec v1 freezes `\bS[0-9]{3}\b` (exactly 3) and
  rows "S + three digits"; impl uses `S[0-9]{3,}` both sides — tools/research-gate.sh:2433
  (`^S[0-9]{3,}$`), :2474 (token regex). Consequence: entry citing "S0001" (typo for S001) →
  impl `META_SOURCE_ROW_MISSING` warn (drift, rc1); spec would say no-S-id → `…NO_ROW_ID` info
  (clean). Selftest :6204-6219 (`metadata-registry-positive-continuations`, row id `S0001`,
  expected clean) locks the widened grammar in; the c3 probe has no 4-digit control, so the drift
  is invisible to the registered counting. Needs `{3}` or a registered disposition (QUALITY 11).
- HIGH (spec↔impl drift, silent) used-by semantics: spec says "token whose **last path
  component** equals the entry basename"; impl requires the full trimmed token (after repeated
  `./` strip) to equal the entry's root-relative path — tools/research-gate.sh:2488-2500
  (`[[ -n $entry_path && $token == "$entry_path" ]]`). Both directions differ:
  (a) impl false-positives vs spec — used-by `knowledge/foo.md` under root `corpus/`, or any
  mined-row citation when `entry_path` is empty (file outside `--root`, :2509-2518 else-branch)
  warns `META_SOURCE_USEDBY_MISSING` regardless of the registry naming the entry;
  (b) spec's basename rule would pass a same-basename file in another directory (the
  same-named-file false-negative class my ticket probes) — impl avoids that class but only by
  deviating from the frozen construct. Probe controls (:6186-6190) cannot distinguish the two
  semantics: no bare-basename or cross-directory fixture exists.
- MEDIUM (evidence, gaming) C3 population metric is one-sided and oracle-free: a checker that
  never fires scores `C3_POP_R24PLUS_CLEAN=5/5`; unlike C2 there is no independent oracle in
  round26-measure.sh c3(). Gaming vectors against the probe run: ignore `--registry` FILE and
  read `$root/corpus/SOURCES.md` (same copy), or fingerprint fixture/pop24 names and suppress
  findings — holds (selftest, LEGACY_CASES_SHA first-161, drift, exports) would all pass. The
  printed FINDING grep plus the claims' adjudication clause are the only counters. Cheap fix: a
  sensitivity control that flips one registry status/used-by in a mutated copy and requires the
  finding to appear.
- MEDIUM (impl narrower than spec) Table scan stops at the first non-`|…|` line once a header was
  found — tools/research-gate.sh:2413-2415 (`((header_found)) && break`). Spec: "rows = table
  rows" of the FILE. A second registry block after a prose gap (or rows appended after notes) is
  silently unparsed → stale first-table rows win → `ROW_MISSING`/`NOT_MINED` false positives.
  Current SOURCES.md is one contiguous table, so unobserved today.
- LOW Duplicate ids: first row wins, no duplicate signal (:2434) — matches spec but is silent;
  under the lane's append-only errata culture a corrected row appended later is dead data unless
  given a new id (the S019→S029 supersedes pattern). A `META_SOURCE_ROW_DUPLICATE` info would
  close the trap; spec doesn't ask for it.
- LOW Ragged rows: missing status/used-by cells become `''` (:2435-2436) → `NOT_MINED` warn on a
  row that merely has too few cells; spec silent.
- CONFIRMED (operability core holds) Registry refusals complete and match spec: denylist
  :2375, unreadable/regular :2371-2372, stat :2387-2391, multilink :2392-2393, size :2394-2397,
  NUL :2399-2400, read :2401-2402 → exit 2 via die_usage :2407; `--registry` rejected outside
  verify-metadata :6299-6301; plain mode untouched (guards :2629, :2664, :2693, :2710) → C1
  byte-identity and legacy cases unthreatened. `metadata_verified_at_bare` :2523-2527 matches
  spec wording (leading date shape consumed, remainder must be all spaces; calendar-invalid
  shape still consumed).
- CONFIRMED (legacy scope) All 24 legacy (pre-r24) frozen entries carry zero `S[0-9]{3,}` tokens
  in their source blocks (base ba33332 scan; only POP24 hits: citation-chain S003,S005;
  claim-support S006,S007; contextual S002,S003,S004; json-delimiter S001,S013;
  metadata-screen S029,S033). So legacy entries get `NO_ROW_ID` info only — the claims' legacy
  carve-out holds empirically; impl has no exemption path but needs none at base.
- OBSERVATION (population prediction) Every cited id above is `mined` in the base registry and
  every used-by cell is the exact root-relative path the probe reproduces
  (`$W/pop24/corpus/knowledge/<f>` vs `corpus/knowledge/<f>`, probe :196-201) → candidate
  should print `C3_POP_R24PLUS_CLEAN=5/5` with zero FINDING lines; any deviation is a checker
  defect, not registry data.

## Calibration vs operability — verdict on the claim label

The five checks are truth-tracking *necessary* conditions of QUALITY 6 (row exists, mined,
used-by names entry, verified-at not bare) and the controls prove each code fires — that is
link-integrity operability. The calibration substance lives only in the pre-registered
adjudication clause: the checker cannot see whether a `mined` row was ever opened (self-asserted
registry data), never cross-checks the entry's URL/anchor against the row's `source`/`anchor`
cells (criterion 6 requires both), and accepts any non-space text after the verified-at date.
Calling C3 "calibration" is justified only with adjudicated pop24 findings; the probe number
alone cannot carry it.

## Residual risk / gaps

No dynamic run performed (read-only seat): c3-on-candidate, the sensitivity control, and a
same-basename/cross-directory fixture remain unexecuted — the two HIGH findings are code-read
facts, not probe outputs. Implicit-false-positive classes (S-id inside a URL/quote token) are
latent only — the frozen corpus contains none.

VERDICT: C3's operability core is sound and spec-faithful on refusals/exits/legacy, but the landed
candidate silently diverges from the frozen spec v1 on token width ({3,} vs 3) and used-by
matching (exact path vs last component), both locked by selftest and invisible to the registered
probe — amend spec or code via a registered disposition before counting C3 as calibration.
