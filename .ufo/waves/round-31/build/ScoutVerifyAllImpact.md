# ScoutVerifyAllImpact — C1/C2 composition impact on verify-all / --json / --pin/--drift

Scout: ChousaR31.ScoutVerifyAllImpact (leaf). Read-only; no tools installed; no network.
All line numbers refer to `tools/research-gate.sh` at the frozen lane commit d78d188
(verify: `git show d78d188:tools/research-gate.sh | sha256sum` = `ac1315dd…835765` = the
tree's sha, matching the gate SHA-256 recorded in `corpus/evidence/round31/claims.md:4`;
`git status --porcelain` clean for `tools/research-gate.sh`).

## 1. How verify-all runs the claims section — fresh solo invocation, yes

- `verify_all_section()` (`tools/research-gate.sh:2868-2899`) invokes each mode as a fresh
  subprocess: `VAS_OUT=$(bash "$SELF" "$mode" "$@" --root "$ROOT" 2>&1)` at **:2872**.
- Claims section entry: `verify_all_section claims verify-claims "$claims_surface"` at
  **:2990** (inside the run loop at :2986-3002). So every claims-mode change propagates into
  verify-all by construction; there is no second claims implementation.
- The section verdict/numbers are parsed from the solo mode's summary:
  - `RESEARCH_GATE:` line regex `^RESEARCH_GATE:[[:space:]](CLEAN|DRIFT)[[:space:]]\((.*)\)$`
    at **:2882-2883** (`$VAS_COUNTS` = the parenthesized count group);
  - `findings=` / `drift=` extracted from that group at **:2889-2890**;
  - native tally `VERDICT_BEARING_CLAIMS=` at **:2892** (stored as `SEC_NATIVE[claims]`);
  - `FINDING ` lines collected at **:2897**.

## 2. How SEC_COUNTS/tallies parse the claims summary

- `SEC_COUNTS[claims]` = the raw parenthesized group of the claims `RESEARCH_GATE:` line
  (**:2998**).
- Manifest: `json_counts()` (**:2850-2863**) turns every `k=v` pair of that group into a JSON
  object (`"tallies"`) at **:3027-3032**; i.e. **every key in the claims summary line becomes
  a manifest tallies field**.
- Text section line: `SECTION claims state=run verdict=… findings=… drift=… tally=<native>`
  at **:3067-3068**.

## 3. Claims summary shape (unchanged by the design)

- Per-claim disposition counting (**:1453-1458**) only increments `N_SUP/N_CON/N_UNS/N_UNP`;
  *every* other `observed` value falls through to `N_MISM` (**:1459-1463**).
- `N_MATCH = N_CLAIMS - N_MISM - N_REFUSED - N_INVALID` (**:1470**); `ROLL=DRIFT` when
  `N_MATCH != N_CLAIMS` (**:1471**).
- Summary printf (**:1473-1474**) always prints the fixed ten counters
  `claims supported contradicted unsupported mismatched unproven refused invalid findings drift`
  (asserted by selftest, e.g. exact string at **:4117**).

## 4. Canonical capture used by --pin/--drift

- Fixture: `gate_pin_fixture()` (**:3122-3171**) writes a hermetic temp dir containing
  `lib/primary.md`, `noise/chat-export-sources.md`, **`claims.jsonl` with the single claim
  `P1` (no `line`, no `sha256` fields)** at **:3127-3129**, and `record.md` (structure +
  chain + sweeps + integrity, one integrity finding).
- Invocation: `bash "$SELF" verify-all record.md --claims claims.jsonl --json manifest.jsonl
  --root .` with cwd = the fixture (**:3185-3189**), stdout → `capture.txt`.
- Capture = normalized `capture.txt` + `GATE_MANIFEST_MARKER` + normalized manifest line
  (**:3193-3200**); normalization masks `ts`/`gate_sha256` only (**:3111-3120**;
  `GATE_DRIFT_VOLATILE_FIELDS='ts gate_sha256'` at **:3101**).
- Drift compare: pass1 exact-match, pass2 same-id field diff, pass3 additions
  (**:3268-3311**); tokens: changed `key`; `-key/+key` dropped/added field; `-id/+id`
  dropped/added line (**:3245-3266**, ids at :3210-3222).

## 5. Impact of C1/C2

- **New observed values `mislocated`/`stale`**: no tally-format change is required or implied
  by the contracts — they simply flow into `N_MISM`, lowering `N_MATCH` → claims section
  DRIFT → composed `VERIFY_ALL` DRIFT (exit 1), `VERDICT_BEARING_CLAIMS` native drops. The
  JSON manifest reflects this via `findings`/`drift` counts only (no new tallies keys).
- **New finding IDs `CLAIM_LINE_MISMATCH` / `CLAIM_SOURCE_REVISION_MISMATCH`**: emitted via
  `emit_finding() warn` (**:392-403**) → `N_FINDINGS++`, `N_DRIFT++`, `ROLL=DRIFT`. No
  further plumbing: verify-all picks them up through the section counts.
- **Canonical capture**: the fixture's `P1` claim carries neither new field ⇒ behavior on the
  hermetic fixture is byte-identical under a minimal implementation ⇒ a pre-change pin keeps
  matching; `--drift` against it prints `GATE_DRIFT: none` (exit 0).
- **The only drift risks** are non-minimal implementation choices:
  1. Adding new unconditional counters to the summary line (**:1473-1474**) ⇒ from fields on
     the VERDICT line and new keys in the manifest tallies ⇒ drift tokens `+mislocated`
     `+stale` (LC_ALL=C sorted) on both paired lines ⇒ `GATE_DRIFT: +mislocated +stale`,
     exit 1. (Also breaks selftest exact-string assertions, e.g. :4117, :4267.)
  2. Printing extra top-level lines in verify-claims (e.g. per-claim debug) that would appear
     inside verify-all's stdout ⇒ `+LINE` tokens.

## 6. Code points for the falsify wave (tools/research-gate.sh)

- **:1367-1392** claim field extraction + `CLAIM_RECORD_INVALID` path — add `line`/`sha256`
  malformed checks (→ `observed=invalid`, `N_INVALID++`).
- **:1394-1401** probe chokepoint (`claim_source_path` :1170-1239) must precede any hashing;
  C2 must hash only after `path=$CLAIM_SRC_PATH` (**:1401**) and before `tok_span_at`
  (**:1405**).
- **:1405-1428** span-found branch — `TOK_L1/TOK_L2` (`at=` from `tok_span_at` :1295-1322)
  are in scope here; the C1 bound check belongs here (start/end vs the parsed N/M).
- **:1429-1451** span-absent branch — unaffected by C1; C2 stale applies regardless of span
  presence.
- **:1453-1465** disposition/match counting — regression-guard that the new observed values
  flow into `N_MISM` (loop is already generic).
- **:1470-1474** summary line — assert no new counters unless deliberate (documented drift).
- **:2881-2897** `verify_all_section` parser — requires the claims summary to keep exactly one
  parenthesized count group with `findings=`/`drift=` keys and the
  `VERDICT_BEARING_CLAIMS=` prefix.
- **:3026-3034** manifest `sec_json` tallies — guard that tallies contain only intended keys.
- **:3122-3171 / :3127-3129** canonical fixture — keep `claims.jsonl` free of `line`/
  `sha256` fields so the baseline stays stable.
- **:22-25, :44-53, :68-70** header docs (finding-id list, claim-field list, `observed`
  enum) — doc-only updates.

## 7. Prediction

- Minimal contract-faithful landing: `--drift` vs a pre-change baseline →
  `GATE_DRIFT: none`, exit 0.
- If implementers add summary counters `mislocated=0 stale=0`:
  `GATE_DRIFT: +mislocated +stale`, exit 1 (and selftest exact-string cases must be updated).

## Limits

- No runs executed (no seat runs the counters this wave; leaf seat). All claims are from
  read-only source reads. No tools installed (none needed). No network used.
