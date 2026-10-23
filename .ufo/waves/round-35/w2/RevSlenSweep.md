# round-35 v2 wave — RevSlenSweep: dynamic-scope (`local a=$1 b=${#a}`) sweep of research-gate.sh

Reviewer: chousa-r35-w2-RevSlenSweep · 2026-10-23 · read-only on lane production files; no gate edits.
Gate pinned by sha256 before any scoring:
`sha256sum tools/research-gate.sh` → `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (matches landed pin).
Pre-round control blob: `.ufo/waves/round-35/repairs/base-gate.sh` (`a6307edf…`, round-34 gate).

## Verdict

**The landed gate (1f2fb4f5) contains ZERO instances of the one-statement dynamic-scope shape.**
The only instance in the wave's history is the known R1 bug at base-gate L1632, it was **latent**
on the landed call path (caller passed the same value) and **live** under a caller whose visible
`span` differs (probe: offsets=0). The R1 repair is present, correct, and the shape class is closed:
no new instance, no sibling `declare/export/readonly` instance, no MEETS-style bypass via this shape.

## Method (two independent detectors, each with a positive control)

1. **Static**: parse every line-initial `local`/`declare`/`export`/`readonly` statement (backslash
   continuations joined), tokenize words quote/`${}`/`$()`-aware, and flag any RHS that references a
   name assigned earlier **in the same statement** (`${#X}`, any `${X…}` op incl. `: %% # % / [ @ ,
   ^ !`, bare `$X`, `$((…X…))`), plus same-name self-reads (`local x=${x:-}`, intentional idiom).
   - Positive control: base blob → exactly 1 hit, L1632 `slen <- span (${#span})`. No false negatives
     demonstrated; detector reproduces the known bug.
   - Landed gate → **0 hits** (script: `.ufo/waves/round-35/w2/RevSlenSweep/slen-sweep.py`;
     receipt: `sweep-receipt.txt`, both runs `exit=0`).
2. **Empirical poison-differential** (bash semantics, not my parser): for each of the gate's 265
   `local` statements, run the statement verbatim in a fresh bash, twice — once with no caller
   variables, once with every name the statement itself assigns pre-set to sentinel `zzPOISONzz` in
   the caller scope — and `declare -p` all assigned names. A dynamic-scope read makes the two runs
   differ; a repaired statement is byte-identical.
   - Positive control: base blob → exactly 1 DIFFER, L1632 (harness detects the real bug).
   - Landed gate → SAME=213, DIFFER=12, skip=40, **0 real differs**. All 12 DIFFERs are
     `local LC_ALL=C` (lines 1209 1665 1677 1699 1722 1744 2943 2992 3017 3139 3214 3464): poisoning
     the caller's `LC_ALL` makes bash emit a `setlocale` warning on stderr; the A/B assignment values
     are byte-identical (`declare -- LC_ALL="C"`). Harness artifact, not a finding.

## Coverage accounting (landed gate)

- 265 `local` statements total (no multi-line continuations; no `;`/`&&`/`then`/`do`/`else`/`{`
  mid-line `local` — grep over `(;|\||&)\s*local` and `\b(then|do|else|\{)\s+local` returned only
  comment/prose lines; no `eval`-wrapped `local`).
- 213 poisoned SAME + 12 `LC_ALL` stderr-artifact DIFFERs (values identical) = 225 cleared empirically.
- 39 skipped as declaration-only (`local a b c…`, no RHS → no expansion → shape impossible); raw
  lines spot-checked (543 657 752 1476 1782 2590 2592 3948 1706 — all bare name lists).
- 1 skipped as nondeterministic (L2993 `local date=$1 digits=$2 year month day start last_day amount`)
  — manually cleared: only `date=$1 digits=$2` are assigned; no same-statement derivation (the regex
  hit was the variable *name*, not a `$(date)` call).
- Sibling declaration commands (same expansion semantics): 18 line-start `declare`/`export`/
  `readonly` statements, all empty-init (`=()`), bare re-exports (`export LC_ALL`, `export NS_MODE
  NS_FILE …`), or single non-derived assignments (`export CHOUSA_ROOT="$WORK"`). 0 hits. List:
  `/tmp/hyaku/chousa-r35/w2/RevSlenSweep/decl-export-ro.txt`.

## The one historical instance (base blob a6307edf, L1632) — latent vs live

```bash
local hay=$1 span=$2 slen=${#span} chunk pattern occurrence offset resume=0   # base L1632
```
`slen`'s RHS `${#span}` expands before any assignment in the statement, so it reads the caller's
dynamic-scope `span`, not the callee's `$2`.

- **Latent on the landed path**: the only caller, `tok_span_offsets` (base L1593-1602), declares
  `local hay=$1 span=$2` (L1598) and calls `tok_span_offsets_chunk "$hay" "$span"` (L1600) — the
  caller's visible `span` is the identical value, so the wrong-scope read returned the right number.
  Matches the probe header: "In the landed call path the caller's `span` happened to be the same
  value" (.ufo/waves/round-35/repairs/slen-probe.sh, accessed 2026-10-23).
- **Live under a differing caller**: slen-probe sets `span=decoy_span_of_other_length` (26 bytes) in
  the caller scope and calls the matcher with a 32766-byte span. `slen` becomes 26, the whole-span
  confirm `[[ ${hay:offset:slen} == "$span" ]]` never matches → 0 offsets.
  Receipt: base → `SLEN_PROBE offsets=0 first=` **exit=1**; landed → `SLEN_PROBE offsets=1 first=5`
  **exit=0** (slen-probe-receipts.txt). Reproduces the claims-table values 0/1.
- **One-line repair** (already landed): split declaration from derived assignment —
  ```bash
  local hay=$1 span=$2 chunk pattern occurrence offset resume=0   # landed L1700
  local slen                                                      # landed L1706
  slen=${#span}                                                   # landed L1707
  ```
  A plain (non-declaration-command) assignment expands at execution time, after `span` is bound.
  Gate comment states the rule: "slen must be read from the parameter, not from the caller's dynamic
  scope" (tools/research-gate.sh:1701-1702, accessed 2026-10-23). Verified in file.

## Findings by severity

- **Blocker / Major / Minor: none in the landed gate.**
- **Info (verified-good observations, no action):**
  1. R1 repair class is closed: static 0 + empirical 0 + sibling declarations 0 + mid-line/eval 0,
     all against a detector suite with a demonstrated positive control.
  2. Landed repaired statement L1700 is itself safe: every RHS is a literal/positional (`$1 $2 0`);
     no derived expansions remain in any `local` statement.
  3. The `local LC_ALL=C; export LC_ALL` idiom (11 sites) is two statements with no derived RHS —
     safe; only my poison harness notices it (stderr).

## Residual risk and verification gaps

- My tokenizer is a reimplementation; mitigations: (a) it reproduces the known base bug exactly and
  finds nothing else there; (b) the empirical differential does not depend on it for detection
  (only for name enumeration) and shows 0 real differs; (c) all skips were individually cleared.
- Poison test cannot catch a dynamic read whose value is coincidentally the caller's poisoned
  sentinel-independent value — not applicable here since we poison precisely the assigned names.
- Statements inside heredoc fixture *strings* were scanned as lines too (same regex) — none matched;
  a shape hiding only inside non-line-initial heredoc text would evade both detectors
  (grep found no `local` after `;|&{`-like prefixes, so residual exposure ≈ nil) [INFERENCE].
- Scope: gate only (tools/research-gate.sh), per assignment; counters/witness are Python and out of
  the `local` shape's surface.

## Artifacts

- `.ufo/waves/round-35/w2/RevSlenSweep/slen-sweep.py` — static + empirical sweep (positive-control capable).
- `.ufo/waves/round-35/w2/RevSlenSweep/sweep-receipt.txt` — static runs on landed + base (exit=0 both).
- `.ufo/waves/round-35/w2/RevSlenSweep/slen-probe-receipts.txt` — probe receipts both gates.
- Scratch/logs: `/tmp/hyaku/chousa-r35/w2/RevSlenSweep/` (decl-export-ro.txt, raw outputs).
