# Sweeps and kept rejections — round-5 coverage mode (research-gate)

source: lane HEAD `45f8f65…` (round-4 records; no commits by any seat at write
time — the round-5 gate and fixtures are uncommitted working-tree files). The
round-5 gate `tools/research-gate.sh` sha256
`55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2`
(observed identical before and after every run below, and stable for >2 min
while the battery ran); the round-4 revision it replaces is
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2`, still
recoverable as `git show HEAD:tools/research-gate.sh`. Fixtures (fixture-author
seat, `corpus/fixtures/`): `sweeps-r5.md` sha256
`025352b75b7b109147fee8b8eb13b4f74eaa1550489e83166ce1dd59cfb14907`,
`sweeps-r5-broken.md` sha256
`f74ea3247e069e711278bb81addda468045053cfe556d8f5a204f3b9ff7abc0c`,
`sweeps-r5-hit.md` sha256
`89650988074e4c371aada8e1fe77cd02d4fa85bc0c3d0a40dc21e12e1a0f78cd`;
`sweeps-r5.README.md` was sha256
`e9178651254841b86e46e98ba4566b568df662ed8c541197ae150f5aba1ebbca` when this
note was last checked (its seat was still finalizing it during the wave; the
three record bytes above are the pinned artifacts).
verified-at: 2026-10-15/16, from the lane cwd, fresh processes, read-only local
opens only; nothing was fetched or executed; zero network (strace, below).
recheck:
`bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..`
· `bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..`
· `bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5.md --root ..`
· `bash tools/research-gate.sh --selftest`

All script line numbers below are relative to the round-5 revision above (the
round-4 numbers quoted for the before-state are relative to `6b83705b…`).

## The move

Round 4 left the last unmeasured r1 structural surface: kept rejections and
negative sweeps. At `6b83705b…` a record passed `verify` as long as a rejection
row had a non-empty `reason` (rejections table, `:605-620`) and a negative row
had a non-empty `sweep` cell (`:525-538`, `:555-564`) — the sweep's content was
never interpreted, never re-run, and a sweep naming nowhere or claiming a false
emptiness passed exactly like a true one. Round 5's falsifiable claim: **after**
`verify-sweeps`, every kept rejection must carry a non-empty reason AND
flip-condition (else `SWEEP_REJECTION_INCOMPLETE`), and every negative sweep
must name where it looked — local path sets are re-run (any glob hit is
`SWEEP_CLAIM_FALSE` naming the hit; zero hits verify), non-local sets stay
exempt-but-counted, and a sweep naming nowhere drifts.

Before-state measured at `6b83705b…` both in the lane and on the exact
round-5 fixture bytes (r4 gate run from a lane-shaped mirror so `LANE_ROOT`
resolved):

```text
verify corpus/fixtures/sweeps-r5.md        → CLEAN (findings=0 drift=0 … rejections=3 approvals=1), exit 0
verify corpus/fixtures/sweeps-r5-broken.md → CLEAN (findings=0 drift=0 … rejections=1 approvals=1), exit 0
verify-sweeps …                            → exit 2 (the r4 CLI reads the token as a positional record path)
```

After-state at `55adb92d…`: the positive fixture closes CLEAN with
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, exit 0; the broken control DRIFTs,
exit 1, naming both `SWEEP_REJECTION_INCOMPLETE` and `SWEEP_CLAIM_FALSE` (full
receipts below).

## Mode design (frozen revision)

`verify-sweeps <record.md>` is a fourth mode beside `verify`, `verify-claims`
and `verify-chain` (dispatch `:2666`; contract in the file header `:70-98` and
in `usage` `:181-188`). It shares the boundary policy: it runs `scan_secrets`
on the record, declares `SRC_PTR` from `## Sources`, and opens/executes nothing.

- **Rejections** (`:1483-1508`): each `## Rejections` data row is read;
  `reason` must be non-empty and a flip cell must be non-empty. The flip cell
  comes from `sweep_flip_cell` (`:1380-1386`): first an exact-key search
  (`flip`, `flip_condition`, `flip-condition`, `flipcondition`, `would_flip`,
  `falsifier`, `flip_when`, `flip_if`, `flips_if`, …), then any column whose
  lowercased key matches `flip|falsif|reversal|counter`. A row missing either
  cell emits `SWEEP_REJECTION_INCOMPLETE` (warn, `:1502`) and counts incomplete.
  Per-row line: `REJECTION id=… ref=… reason=present|absent flip=present|absent
  observed=complete|incomplete verdict=match|mismatch`.
- **Sweep items** (`:1509-1526`): all data rows of `## Sweeps`; if that section
  has no rows but `## Negatives` exists, each Negatives row that names a raw
  location is treated as a sweep item — so a sweep may live in either table.
  A row carrying `unresolved|blocked-no-fetch|labelled-dead|not-applicable` in
  a status cell is exempt like an unresolved hop (`:1529-1532`).
- **Where-discovery** (`sweep_raw_where`, `:1388-1395`): a
  `where`/`looked_at`/`looked`/`scope`/`searched`/`paths`/`location`/`targets`
  column, else any column key matching `where|looked|scope|glob|target|locat`,
  else the `sweep` cell.
- **Tokenization** (`sweep_where_tokens`, `:1339-1364`): a whitespace-free
  value is split on commas/semicolons only (a path set); a value containing
  whitespace is read as a command/description and only its structured words
  count — URLs, source ids and path/glob-shaped tokens; other words are ignored
  (`test ! -f lib/ghost.md` names `lib/ghost.md`). Edge quotes/backticks and
  trailing punctuation are stripped (`sweep_trim_token`, `:1324-1337`).
- **Classes** (`sweep_token_class`, `:1311-1322`): `local` (glob- or
  path-shaped: contains `/`, `*`, `?`, or an extension), `nonlocal` (URL,
  `local://`, `external:`, `web:`, `live:`, `chat:`, `session:`), `sourceid`
  (`S[A-Za-z0-9_-]+`), else junk — junk makes the item invalid
  (`SWEEP_LOCATION_ABSENT`, `:1563`), as does an empty location (`:1538`).
- **Boundary guard** (`sweep_path_guarded`, `:1397-1430`): `..` components are
  refused; the deepest non-glob ancestor of each local pattern must
  canonicalize under `ROOT` (the `--root` tree) or `LANE_ROOT`, else the path
  is refused unopened and the item is `refused`
  (`SWEEP_LOCATION_OUT_OF_CORPUS`, crit, `:1571`). An undeclared source id is
  refused too (`SWEEP_LOCATION_UNRESOLVED`, warn, `:1577`).
- **The local re-run** (`sweep_glob_matches`, `:1432-1450`): from `ROOT`, glob
  patterns expand with `nullglob`+`globstar`; a literal path without glob
  characters takes an explicit `-e`/`-L` existence test instead (a measured
  earlier revision made every literal a phantom hit). Any match among the
  local patterns is a hit: `SWEEP_CLAIM_FALSE` (warn, `:1597`) names the first
  hit and lists up to five; the item is `observed=hit verdict=mismatch`.
  Zero hits is `observed=verified verdict=match` (`:1601`).
- **Summary and exit**: `ROLL=DRIFT` unless `verified+exempt = M` and
  `REJECTIONS_OK = L` (`:1613`); `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L`
  (`:1614`), one `RESEARCH_GATE: CLEAN|DRIFT (sweeps=… verified=… exempt=…
  hit=… refused=… invalid=… rejections=… rejections-ok=… findings=… drift=…)`
  (`:1615-1616`), exit 0 CLEAN / 1 DRIFT / 2 usage (`:1618-1619`; no record
  and a missing record both exit 2, measured).

## Flip-condition semantics — what counts as non-vacuous

The bar the mode enforces is **presence**: a flip cell found in a flip-named
column whose value is non-empty after the table's cell trimming. Nothing else
is inspected — no length check, no shape check, no placeholder blacklist, no
comparison against the reason text.

This seat's class probes at `55adb92d…` (twelve records, one variable each,
same well-formed skeleton; flip cell → outcome):

| cell | outcome |
|---|---|
| (missing) | `flip=absent observed=incomplete` → `SWEEP_REJECTION_INCOMPLETE`, DRIFT exit 1 |
| (single space) | same as missing (trimmed) → DRIFT exit 1 |
| `-` | `flip=present observed=complete` → CLEAN exit 0 |
| `TBD` | complete → CLEAN |
| `none` | complete → CLEAN |
| `see reason above` | complete → CLEAN |
| the reason text restated | complete → CLEAN |
| `flip if this is incorrect` | complete → CLEAN |
| `if wrong then flip` | complete → CLEAN |
| `if the sun rises in the west` (never fires) | complete → CLEAN |
| `when better evidence appears` (vague) | complete → CLEAN |
| a concrete falsifiable condition | complete → CLEAN |

So the non-vacuity claim this round can honestly make is *structural*: an
absent or blank flip-condition is caught; a vacuous-but-non-empty string is
not. The placeholder/tautology/never-fires/vague classes pass, and that is the
mode's named limit, not a hidden one — the fixture README states the same in
its own words ("It does not prove the flip-condition is *good* (a placeholder
string would pass)", `sweeps-r5.README.md:178-180`). The gate never adjudicates
meaning anywhere (the r2-r4 limits stand verbatim), so a presence check is the
only non-vacuity bar it can falsify locally; the class table above is the
measured boundary of that bar, including the vacuity classes it cannot reach.

## The local-emptiness re-check

What the re-run verifies is the **emptiness of the named location set**: the
local pattern(s) the sweep names must match no existing path under the boundary
at this revision. Three consequences are worth stating plainly:

- Any match is a false emptiness claim: `SWEEP_CLAIM_FALSE` names the first hit
  (`first=p`, root-relative as globbed from `ROOT`) and up to five listed
  paths. The broken control's W1 names
  `chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md` — a file that really
  exists — and the run reports `hits=1 first=chousa-shokunin/corpus/fixtures/
  sweeps-r5-hit.md`.
- The positive control's W1 names
  `research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/saved-*`;
  neither glob matches anything at the pinned revision (`ls` exits 2 on both,
  re-derived by this seat), so the item verifies (`hits=0 observed=verified`).
- The recorded command is **never executed**, and its `observed` prose ("zero
  matches …") is never compared: the mode reads the command cell for
  structured words and globs those. It is therefore a location/existence
  re-check, not a content-grep re-run, and it cannot tell whether an empty
  location set is the *right* place to have looked. `..` components and
  absolute paths are handled by the shared guard, not by the sweep's own
  command.

## The exempt class

Exempt items are counted in `M` but never verified — `verified+exempt = M` is
what CLEAN requires. Three routes reach exemption: a non-local target (URLs,
`external:`/`web:`/`live:`/`chat:`/`session:` forms — a content sweep "carries
no probe the gate could re-run"); a declared source id (present in
`## Sources`); or a status cell marked `unresolved|blocked-no-fetch|
labelled-dead|not-applicable`. This seat's four-class probe at `55adb92d…`
closed `VERIFIED_SWEEPS=0/4` with all four items `observed=exempt
verdict=exempt`, CLEAN. Refusal is distinct from exemption: an out-of-corpus
path (crit) or an undeclared source id still DRIFTs.

## Receipts (round-5 revision, run by this seat)

All runs at gate sha256 `55adb92d…`, identical before and after each run
(sampled); lane cwd; fresh processes; `--root ..`; fixtures at the shas in the
header.

- Positive fixture, `bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..` → exit 0:

  ```text
  SWEEP id=W1 where=research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/s looked=local hits=0 at=- observed=verified verdict=match
  SWEEP id=W2 where=https://kotobank.jp/ looked=non-local hits=- at=- observed=exempt verdict=exempt
  REJECTION id=R1 ref=research/README.md:12 reason=present flip=present observed=complete verdict=match
  REJECTION id=R2 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 reason=present flip=present observed=complete verdict=match
  REJECTION id=R3 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:63 reason=present flip=present observed=complete verdict=match
  VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3
  RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=3 rejections-ok=3 findings=0 drift=0)
  ```

  (The W1 `where=` display is truncated at 80 chars by `chain_disp`; the cell
  holds the two globs.)
- Broken control, `… verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..` → exit 1:

  ```text
  SWEEP id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md looked=local hits=1 at=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md observed=hit verdict=mismatch
  REJECTION id=R1 ref=research/README.md:12 reason=present flip=absent observed=incomplete verdict=mismatch
  FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=flip
  FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md hits=1 first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md listed=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md
  VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1
  RESEARCH_GATE: DRIFT (sweeps=1 verified=0 exempt=0 hit=1 refused=0 invalid=0 rejections=1 rejections-ok=0 findings=2 drift=2)
  ```

- Selftest: `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST:
  PASS (54 cases)`, exit 0. A line-diff of the case lines against the 44-case
  r4 capture shows cases 1-44 **byte-identical** (empty diff); the ten added
  cases are `sweeps-pass`, `sweeps-fail-planted-hit`,
  `sweeps-fail-rejection-incomplete`, `sweeps-fail-unnamed`,
  `sweeps-fail-out-of-corpus`, `sweeps-fail-unresolved-id`,
  `sweeps-fail-counting`, `sweeps-pass-cell-command`,
  `setup-sweeps-no-path`, `setup-sweeps-missing-file`.
- Regressions at `55adb92d…`, each byte-identical to the `6b83705b…` run after
  normalizing only the `ts=` field: claims `VERDICT_BEARING_CLAIMS=17/17`
  CLEAN exit 0; chain `RESOLVED_HOPS=17/22` CLEAN exit 0; broken chain
  `RESOLVED_HOPS=1/2` DRIFT exit 1; the r1 A/B/C observable each DRIFT exit 1
  (3/3). Chain mode also holds on the new positive fixture:
  `RESOLVED_HOPS=2/3` CLEAN exit 0.
- Exit contract: `verify-sweeps` with no record → exit 2 (`record path
  required`); a missing record → exit 2; positive CLEAN → 0; broken DRIFT → 1.
- Zero network: `strace -f -e trace=network` around the positive run recorded
  0 socket/connect/sendto/recvfrom lines (992 trace lines of process/signal
  noise); run exit 0.
- Flip-condition class table and exempt-class probe: verbatim outcomes above,
  produced by this seat's own twelve + four scratch records (outside the lane).
- Ground truth without the gate: `ls
  research/deep-research-2026-09-28/kotobank-* …/saved-*` → both absent
  (exit 2); `chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md` exists and
  contains the token `ghost-sweep-token` on line 4.

## Open items

- **Semantic vacuity passes** (class table above): the mode screens presence,
  not quality. Candidate follow-up: reject a small explicit placeholder set
  (`-`, `none`, `TBD`, `n/a`) and exact reason-restatement — not built here and
  not asserted as sufficient.
- **Section absence is not flagged by this mode.** A record with no
  `## Rejections` and no sweep rows at all closes `VERIFIED_SWEEPS=0/0
  REJECTIONS_OK=0/0`, CLEAN (measured); the r1 `verify` mode is what flags the
  missing sections (`REJECTION_DROPPED …`), so the modes compose rather than
  duplicate. A future revision could make the sweeps mode require the sections
  to exist.
- **The recorded command is never re-run** and its `observed` prose is never
  compared (design, not debt): the re-check is a glob/existence test over the
  named locations. A sweep can be empty because the wrong glob was named.
- **Fixture README (resolved during the wave, recorded for the trail):** an
  intermediate revision still described the swept W1 as the pre-move
  `grep -nE 'https?://'` command and expected a `…:4` line-suffixed hit; the
  fixture-author seat resynced it to the landed glob contract and filled its
  Execution record with the same `55adb92d…` receipts reproduced here
  (`sweeps-r5.README.md:82-116`, `:130-173`). `sweeps-r5.md` and
  `sweeps-r5-broken.md` were stable from `22:07`; `sweeps-r5-hit.md` was
  reshaped at `22:13` (token still on line 4) and re-measured — the receipts
  above were re-run against the final bytes.
- Carried residuals from earlier rounds (unchanged here): in-root hardlinks
  bypass path canonicalization; no source size cap; banner still reads
  `research-gate-r1` (cosmetic). No hardlink or size issue affects this mode's
  re-run, which only globs and existence-tests paths.
- **Receipt identity (round 1) — STILL OPEN.** These are lane-local evidence
  runs, not queue taskKey/expected-receipt bags; no `task_…` value may be
  invented and no Sighting is claimed. No scalar score, no promotion, no
  field-readiness claim. No commits by this seat.
