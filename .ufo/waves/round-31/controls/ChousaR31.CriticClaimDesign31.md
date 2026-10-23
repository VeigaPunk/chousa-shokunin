# Round 31 — pre-data design review (C1 line binding, C2 revision binding)

Seat: `ChousaR31.CriticClaimDesign31`. Reviewed: `corpus/evidence/round31/claims.md`
(frozen, `d78d1889`, sha256 `08c879a6…`), base gate `tools/research-gate.sh` (`ac1315dd…`),
frozen counters at `d78d1889` (`c1-count.py` `154e09e7…`, `c2-count.py` `20ed105b…`).

Per ticket I ran **only the do-nothing substitute** (the base gate). No gate-substitute control
was built, no candidate implementation was run, no network, no installs. The `env-*` rows are
environment probes, not substitutes; the `v2wt-*`/`v3wt-*` rows re-run the **base gate** with the
counter generation that appeared on disk mid-wave (finding F3). Only receipts are cited; every
run was `timeout 900` from the lane root, receipts under
`.ufo/waves/round-31/controls/ChousaR31.CriticClaimDesign31/`; sandbox
`/fast/scratch/hyaku/chousa-r31/ChousaR31.CriticClaimDesign31/`.

## Receipts

| substitute / probe | counter | seeds | score | receipt |
|---|---|---|---|---|
| do-nothing (base gate) | C1 (v1 `154e09e7`) | 1, 2, 3 | 50/120 each | `base-c1-seed{1,2,3}.json` |
| do-nothing (base gate) | C2 (v1 `20ed105b`) | 1, 2, 3 | 50/120 each | `base-c2-seed{1,2,3}.json` |
| do-nothing, repeat seed 1 | C1 / C2 | 1 | 50/120, receipt identical except `utc`/`elapsed_s` | `det-c1-seed1.json`, `det-c2-seed1.json` |
| do-nothing, counter gen `d201ef4b` (wt) | C1 | 1, 2, 3 | 50/120 each | `v2wt-c1-seed{1,2,3}.json` |
| do-nothing, counter gen `c0a0908c`/`e26c7751` (wt) | C1 / C2 | 1, 2, 3 | 50/120 each | `v3wt-c1-seed{1,2,3}.json`, `v3wt-c2-seed{1,2,3}.json` |
| env `CHOUSA_ROOT=/nonexistent` | C1 | 1 | **0/120** | `env-choosaroot-c1-seed1.json` |
| env `CHOUSA_ROOT=/nonexistent` | C2 | 1 | **0/120** | `env-choosaroot-c2-seed1.json` |
| env temp root under a denylisted `/.config/` | C1 | 1 | **0/120** | `env-denylist-tmp-c1-seed1.json` |
| env `LC_ALL=C LANG=C` | C1 / C2 | 1 | 50/120 | `env-lc-c-c1-seed1.json`, `env-lc-c-c2-seed1.json` |
| env temp root on another filesystem (`/fast`, dev 66309 vs `/tmp` 66308) | C1 | 1 | 50/120 | `env-tmp-fast-c1-seed1.json` |
| audit keep (`--keep`) | C1 / C2 | 3 | 50/120 | `keep-c1-seed3.json`, `keep-c2-seed3.json` |

Every v1 receipt records `counter_sha256` = the frozen commit's counter bytes and
`gate_sha256` = `ac1315dd…` (the base gate), so the 50/120 provenance is exact.

## Findings

### F1 — HIGH — C1 contract contradicts its own B2 class; a literal implementer scores 108/120
`claims.md:27-29`: "bound iff **some** boundary-delimited occurrence of the span starts on line N
… ; **the line numbers are the ones the gate already reports in `at=`**." The base gate reports
`at=` for the **first** accepted occurrence only (`tools/research-gate.sh:1315-1318`:
`TOK_L1/TOK_L2` computed, `TOK_AT` set, `return 0` inside the match loop at :1320). The B2 class
puts the real occurrences on k=2–3 lines and names a **later** one (`c1-count.py@d78d188:103-106`,
`rng.choice(idxs[1:])`). For all 12 B2 claims `at=` ≠ the named line, so the trailing clause, read
as written, yields `mislocated` while the counter's truth is `supported` — 12/120 lost, and with
`TOTAL = 120` exact the predicate fails and the kill rule records a miss for a tool that followed
the sentence. Smallest safe correction: replace the clause with "line numbers use the gate's
existing 1-based newline counting (the convention of `at=`); the bound occurrence need not be the
first, so `at=` may name a different occurrence" — before any data seat, as a version bump.

### F2 — HIGH — P1/P2 do not measure the contract's required drift findings
C1 §3 requires `observed=mislocated` **with a new drift finding `CLAIM_LINE_MISMATCH`**
(`claims.md:31`); C2 §2 requires `CLAIM_SOURCE_REVISION_MISMATCH` (`claims.md:78`). Neither tag
exists in the base gate (expected pre-landing) **and neither tag is referenced by either counter**;
both counters parse only `CLAIM id=… observed=…` (`c1-count.py@d78d188:61,215-219`;
`c2-count.py@d78d188:56,204-208`). The gate prints finding lines on stdout
(`emit_finding` `tools/research-gate.sh:392-395`, printed for claims mode at `:1469`), so the
counters *could* assert them. As frozen, a candidate that emits `mislocated`/`stale` with **no
finding** (and `ROLL=CLEAN`) still scores 120/120 and satisfies P1/P2 while leaving the claim's
stated deliverable unimplemented. Correction: one assertion per counter that the tag appears (and
`RESEARCH_GATE: DRIFT` when it does), or drop the finding clause from the contracts.

### F3 — MEDIUM — P1's subject is not identity-stable: both frozen counters were live-edited at the frozen paths mid-wave
At review start both working-tree counters hashed to the frozen commit (`sha256sum`, and every
receipt from that window records those bytes); during this review both files changed in place,
uncommitted, without updating `claims.md` (first `git status` after the first edit: c1 only, then
both):

| file | frozen (`d78d188`) | observed mid-wave | lines |
|---|---|---|---|
| `c1-count.py` | `154e09e7…` | `d201ef4b…` → `c0a0908c…` | 253 → 280 → 296 |
| `c2-count.py` | `20ed105b…` | `e26c7751…` | 242 → 269 |

The rewrite is a "design v2" fixture hardening (fixed sub-variant counts, `SUBVARIANTS` +
asserts; class tables and `TOTAL` unchanged — verified by diff), but `claims.md` still describes
v1 and P1 says "**this counter**". A receipt taken now records a sha that matches no committed
counter, and there is no `counter` path field in the receipt (only `gate`). Correction: commit the
revision as v2 and update `claims.md`'s predicate block to name its sha (or revert the path),
and add `"counter": <path>` to both receipts. `corpus/evidence/round31/__pycache__/` is untracked
litter in the same tree.

### F4 — MEDIUM — the environment can zero the score, and a harness failure is scored as a design miss
The counters inherit the caller's environment (`subprocess.run(...)` with no `env=`,
`c1-count.py@d78d188:209`, `c2-count.py@d78d188:213`) and never sanitise it, while the gate
overrides the passed `--root` from the environment (`tools/research-gate.sh:1332`,
`ROOT=${CHOUSA_ROOT:-$ROOT}`). Measured: `CHOUSA_ROOT=/nonexistent` → **0/120** on both counters
(every claim `observed=refused`); a temp root under a denylisted `/.config/` →
**0/120** (`tools/research-gate.sh:604`, `*/.config/*` deny). A gate exit ∉ {0,1} or a timeout
scores every claim `none` and the counter returns 1 (a miss), never its documented 2 ("harness
error", `c1-count.py@d78d188:29-30,215`). Under the kill rule that convicts the design for a
contaminated host. Correction: invoke with `env -u CHOUSA_ROOT` (or pass `CHOUSA_ROOT=<root>`
explicitly), record `TMPDIR`/`LC_ALL`/`CHOUSA_ROOT` in the receipt, and return 2 when 100 % of
claims are `refused`/`none`. Not cross-device: sources are always created under the declared root,
so `CLAIM_SOURCE_CROSS_DEVICE` cannot fire — confirmed with a temp root on `/fast` (50/120).
Locale is not a factor for the base gate: `LC_ALL=C` gives 50/120 on both.

### F5 — LOW — the universal "no run lower" clause turns contaminated runs into design misses
`claims.md:47-48` "no run of this counter on that revision in round 31 prints a lower count", with
the kill rule at `:51`. Combined with F4, any later run with a stray `CHOUSA_ROOT`/denylisted
`TMPDIR` is a recorded "miss" that cannot be distinguished from a real defect. Correction: qualify
with "run with a clean environment (recorded in the receipt)".

### F6 — LOW — end-line semantics for a span ending in a newline are undefined
`claims.md:27-29` says an occurrence "starts on line N and ends on line M", but does not say how a
span that ends with `\n` ends a line; the gate's own formula is
`TOK_L2 = TOK_L1 + count_nl(span)` (`tools/research-gate.sh:1316`), which puts `"a\nb\n"` on two
lines after a one-newline start. Not exercised (C1 spans are single-line or `first\nsecond` with no
trailing newline; C2 spans are single-line). Correction: state the formula, or forbid trailing
newlines in `"line"`-bearing spans.

### F7 — LOW — "fresh-seed" and "on the landed lane revision" are not pinned
`claims.md:46-47`; the counters default to `os.urandom` (`c1-count.py@d78d188:195`) and record the
seed. Operationally fine; define "fresh" as "seeds not already used by any receipted run". The
receipt names no revision — "landed lane revision" is checkable only by matching `counter_sha256`
and `gate_sha256` against the commit, which is fine but makes F3's in-place edits invisible to
anyone reading a receipt alone.

### F8 — LOW — bounded fixture leaks (none near 120)
`M5_beyond_eof` always names a line past EOF (`c1-count.py@d78d188:139`) while generated files have
14–30 lines (`:93`), so "line value > 30 ⇒ mislocated" is a free 6-point peeking rule. A
truth-blind substitute can also beat the do-nothing baseline: invalid-format detection alone scores
`C1 = 12 (I1) + 42 (B*) = 54` and `C2 = 14 (I1) + 40 (R1+N1) = 54`, or 64 if it also compares
`sha256` against `sha256(span)` (S3, 10) — all above 50, so **50/120 is the base gate's score, not
a floor** (analytic, `[INFERENCE]`, derived from `CLASS_COUNTS` × truth; I did not build these
substitutes per ticket). Strongest source-reading shortcut derivable from the class tables is
**108/120**: first-occurrence/`at=`-only binding loses B2 (12), raw-substring-on-named-line loses
M2 (12). Nothing I can derive approaches 120; reaching it needs the full rule (all occurrences,
token boundaries at both edges, multi-line spans, absent-span precedence).

### F9 — INFO — verified non-defects
* Before value: exactly **50/120** on both counters and seeds 1, 2, 3, matching `claims.md:54-57`
  and `:101-102` class-for-class (C1: 12+12+12+6 supported + 8 unsupported; C2: 24+10+16), and
  invariant under both mid-wave counter rewrites (seeds 1–3).
* Determinism: same seed → byte-identical receipt except `utc`/`elapsed_s`.
* P1/P2 wording is the same sentence in `claims.md:45-48` / `:93-96` and the counter docstrings
  (`c1-count.py@d78d188:4-7`, `c2-count.py@d78d188:6-9`), and the code condition is `matched == TOTAL` with
  `TOTAL = 120` written as `predicate_holds` (`c1:232`, `c2:221`) — no drift there.
* C1 JSON escapes: the gate's `json_str`/`json_unescape` preserve in-string spaces
  (`" 4"→" 4"`, `"4 "→"4 "`) and decode raw and `\u2013`-escaped en dashes identically (verbatim
  slice probed in sandbox), and the record-level trim does not touch in-string spaces — all 12
  `INVALID_VALUES` are reliably distinguishable.
* C2 CRLF: 27/120 fixture sources were CRLF at seed 3 and the base gate still matched R1 24/24 and
  R2 10/10; single-line spans cannot be perturbed by line endings, and the newline-variant stale
  class checks the hash, not the span.
* Separability holds at the fixture level: C1 fixture 114 `line` / 0 `sha256`, C2 104 `sha256` /
  0 `line`, every claim `expect=supported` (measured from `--keep` copies).

## Impacted axes
- **coverage (C1)**: F1, F6, F8.
- **operability (C2)**: F2 (finding clause), F4.
- **measurement integrity / provenance (both)**: F2, F3, F4, F5.
- **no harm**: not touched.

## Verdict
**design broken (redesign needed): the C1 predicate's subject sentence contradicts its own B2 fixture class
(`claims.md:29` → 108/120 for a literal implementer), and P1/P2 never observe the two drift
findings their contracts require** — both fixable by amending the frozen text (and committing the
counter generation that appeared on disk mid-wave); the fixture itself holds: do-nothing is exactly
50/120 on seeds 1–3, deterministic, and no shortcut I can derive from the class tables exceeds
108/120.
