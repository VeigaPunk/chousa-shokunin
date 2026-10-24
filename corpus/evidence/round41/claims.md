# Round 41 — frozen claims (before data)

freeze author: chousa L1 (host-mapped seat)
date: 2026-10-24
round: 41 (attempt 1)
freeze commit: the commit that lands this file before any counter run against the
landed gate; counters run against the frozen scenario table below.

## C1 — operability (lowest scored non-retired axis, 3/10)

**Axis named by surface (kaidoku r29 rule):** the gate's canonical pin/drift
*invocation surface* — the capture path plus the `verify-all` run whose output the
capture embeds — not the numeric score.

**Measured PATH-resolved surface (before data, instrumentation run 2026-10-24):**
a `--pin` run on the pre-round gate with every candidate tool trapped through a
logging PATH shim produced 728 PATH-resolved external invocations: `tr` 428,
`sed` 251, `date` 14, `readlink` 12, `dirname` 8, `wc` 4, `cat` 4, `od` 2,
`rm` 1, `mktemp` 1, `mkdir` 1, `head` 1, `bash` 1 (the instrumentation's own
wrapper; `grep`, `env`, `sha256sum` resolved only through the existing pins).
The parent gate's capture functions account for `mktemp`, `mkdir`, `cat`, `sed`
(gate_drift_normalize, gate_drift_scan), `rm`, `sort`; every other logged call is
the captured `verify-all` child (or grandchildren it spawns).

**Frozen predicate:** every external invocation attributable to the canonical
capture — parent-side capture functions AND the captured `verify-all` child —
either (a) resolves to a pinned absolute binary verified at startup (the frozen
pin set: mktemp, sed, mkdir, cat, rm, sort, readlink, dirname, date, tr, wc, od,
head, stat — the union of every name the instrumentation observed in either
process, plus sort which fires only on drift reports), or (b) for the child,
resolves under ONE fixed capture PATH of standard binary dirs
(`CAP_CHILD_PATH`, default `/usr/bin:/bin`, override
`RESEARCH_GATE_CAPTURE_PATH`) — the child re-runs the same pin table, so its
pinned names are also absolute. The child's loader environment no longer
inherits `LD_PRELOAD`/`LD_LIBRARY_PATH` from the caller. A caller `PATH` shim
named for any measured surface tool is never invoked; a caller `LD_PRELOAD`

**Kill rule (frozen):** a do-nothing control that meets the target makes the
counter or target wrong (fix before data). Control gate = the pre-round
`tools/research-gate.sh` bytes copied to `.ufo/waves/round-41/controls/base-gate-r41.sh`.
Do-nothing measurements recorded at `.ufo/waves/round-41/controls/` before
landing: `control-before.txt` must show the predicate NOT holding.

**Scenario table (frozen; seed = deterministic paths only, no randomness):**

| cell | name | setup | asserted observable |
|---|---|---|---|
| S1 | base-clean | no shims; `--pin` then `--drift` on the produced baseline | `GATE_DRIFT: none`, exit 0; baseline magic + markers present |
| S2 | trap-inventory | PATH trap dir shadowing {mktemp sed mkdir cat rm sort env bash grep tr date readlink dirname wc od head sha256sum timeout}; `--pin`, `--drift` | after-fix: zero trap-marker entries attributable to the capture or its child (`OUTER` = cwd not under `/tmp/chousa-gate-pin.*`; `CHILD` = cwd under it); before-fix: >0 entries |
| S3 | sed-suppress | trap `sed` = `exit 0` | before: capture normalization loses masking → `--drift` reports volatile tokens (e.g. `ts`) or capture fails → predicate false; after: identical to S1 and shim never invoked |
| S4 | mktemp-preseed | trap `mktemp` prints a pre-seeded dir containing hostile `capture.txt`/`manifest.jsonl` | before: `GATE_CAP_NOTE=fixture-write-failed` or captured content influenced → predicate false; after: real mktemp dir used, shim never invoked |
| S5 | cat-poison | trap `cat` appends one hostile JSONL line when its argv matches `claims.jsonl` in the fixture | before: manifest-lines or verdict-lines != 1 → capture rc=2 or drifted content → predicate false; after: identical to S1, shim never invoked |
| S6 | rm-suppress | trap `rm` = `exit 0` | before: leftover `/tmp/chousa-gate-pin.*` dirs after `--drift` ≥1 → predicate false; after: 0 leftovers and shim never invoked |
| S7 | sort-reverse | tampered baseline (canonical block body edited); trap `sort` reverses order | before: `GATE_DRIFT` token order non-canonical → predicate false; after: canonical `sort -u` order, shim never invoked |
| S8 | mkdir-suppress | trap `mkdir` = `exit 0` | before: fixture-write-failed → predicate false; after: identical to S1, shim never invoked |
| S9 | override-relative | `RESEARCH_GATE_SED=relative/path sed` | after: exit 2 with `SED_PROVENANCE refused`; before: override ignored → predicate false (this cell is after-only; before-fix expectation recorded as `n/a (mechanism absent)` and NOT counted in the tally denominator) |
| S10 | override-nongnu | `RESEARCH_GATE_MKTEMP` → absolute path to a stub printing a non-coreutils `--version` | after: exit 2 `MKTEMP_PROVENANCE refused`; before: `n/a (mechanism absent)` |
| S11 | child-tr | PATH trap `tr` whose shim emits poisoned `tr` output for `A-Z a-z` calls | before: child lower-casing broken → capture content differs → predicate false; after: `CHILD`-tagged trap markers for `tr` = 0 AND capture identical to S1 |
| S12 | loader-env | `LD_PRELOAD=/tmp/cap/ld-mark.so` exported to `--drift`; child `tr` shim records `${LD_PRELOAD:-}` | before: child processes see `LD_PRELOAD` set → predicate false; after: zero child trap-marker records non-empty `LD_PRELOAD` |

**Counter:** `python3 corpus/evidence/round41/c1-count.py [--gate PATH]`.
Prints `CAPTURE_PIN_MATCH=<k>/<n>` where `<n>` = number of cells whose
expectation applies at the tested revision (S9/S10 excluded before-fix), `<k>` =
cells with `predicate_holds=true`; exits 0 iff k==n, else 1. Emits per-cell JSON
receipts under `corpus/evidence/round41/receipts/` (attributable trap markers,
capture outputs, refusal texts, leftover-dir counts). **Before target:** the
control gate must score < n/12 (currently expected ~7/12 — do-nothing fails the
predicate, required for the claim to count). **After target:** `12/12` on the
landed gate, `predicate_holds=true` for every cell.

**Named limits (frozen):**
- The trap-PATH list covers the 2026-10-24 measured surface only; a tool not in
  the measured set is outside this claim.
- SHELLOPTS=noexec still disables the gate body before any pin runs (carried
  r37 residual).
- `RESEARCH_GATE_CAPTURE_PATH` lets a caller widen the child PATH by choice;
  refusal rules apply to the per-tool overrides, not to the PATH escape hatch
  itself.
- Exported-function interposition (`BASH_FUNC_sed%%` etc.) targets the CHILD's
  own resolution, which the fixed CAP_CHILD_PATH covers only for binaries the
  child looks up by name; a caller-exported *function* named e.g. `sed` still
  reaches the child shell through BASH_FUNC_* and is a named limit unless
  separately demonstrated (r37/r38 function-delivery channel).
- The `verify_all` section children are already pinned (r39); this claim adds
  the capture fixture/cleanup/normalize side and the child's PATH + loader env.

## C2 — calibration (W04 duplicate-URL disposition alignment)

**Frozen predicate:** every `W04` warning row emitted by the maintained census
at the measured revision carries a committed disposition (id + rationale +
evidence pointer) in `corpus/evidence/round41/w04-dispositions.tsv`.

**Counter:** `python3 corpus/evidence/round41/c2-count.py` — runs the census,
joins W04 ids against the TSV, prints `W04_DISPOSITIONED=<k>/<n>`; exit 0 iff
k==n AND n≥1. **Before target:** `0/<n>` (no TSV committed) — do-nothing fails.
**After target:** `<n>/<n>` — S051/S053 (same-page, distinct-section study pairs
documented in the r30 search log), S073 (contract-required supersede row for
S070), S074 (intentionally retained rejected duplicate-row proposal), and any
row this round adds on an already-cited page (S075: the coreutils manual page
S073 anchors at #cksum-c, re-cited at #mktemp-d — a fifth warning, dispositioned
same-page-distinct-section). `<n>` is the census warning count at the measured
revision, so the predicate stays join-based, not literal-4. The
contract makes `source`/`scope` cells immutable except through
supersede/rejection rows, and W04 is advisory (never fails validation), so the
disposition records the semantic reason rather than editing rows.

**Kill rule:** a TSV naming ids not in the census output, or with empty
evidence cells, fails the counter (the count is joins-verified, not file-exists).

## Separability

C1 touches `tools/research-gate.sh` + `corpus/evidence/round41/c1-count.py` +
receipts; C2 touches only `corpus/evidence/round41/c2-count.py` +
`w04-dispositions.tsv` + lesson rows. Neither depends on the other's landing:
c1-count verifies on the pre-C2 tree; c2-count verifies on the pre-C1 tree.

## Sourced-claim binding

C1's knowledge note (`corpus/knowledge/capture-path-pin-r41.md`) must cite
S075 (mktemp man page) and S076 (sed info/man page) opened this round, plus
S067 (exec PATH resolution) and S071/S072 as prior-art pins.
