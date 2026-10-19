# Verification wave — round 16 (loop 1 round 5)

source: 64-seat AgentSwarm wave on openai-codex/gpt-6-luna-max, 2026-10-19; every finding below carries the seat number and its evidence pointer
verified-at: 2026-10-19 (round 16, landed; selftest PASS (111 cases, 0 skipped); gate sha <FILL>)
recheck: `bash tools/research-gate.sh --selftest` (cases 1–110 byte-identical vs r15 receipt; case 111 pins `--root //`)

## Disposition table

Every seat finding is dispositioned as **fix** (landed this round), **absorb** (record corrected), or **named debt** (carried to the round-17 queue).

### Fixes landed this round

| finding | seat | disposition |
|---|---|---|
| `--root //` still refused — `in_root` strips only one `/`, leaving `/` which still renders `//*` | 09, 10, 52 | **FIXED** — `in_root` now strips all trailing slashes in a loop; case 111 pins it |
| r15 battery receipt has wrong fixture paths (A/B/C-r9 under `corpus/fixtures/` not `archives-r9/`; `--root .` vs `--root ..`) | 32, 62 | **FIXED** — battery re-run with correct paths and `--root ..`; receipt replaced, masked diff IDENTICAL |

### Absorbed (record corrected, no gate change)

| finding | seat | disposition |
|---|---|---|
| 8 finding IDs unasserted in selftest: `CHAIN_SOURCE_EPHEMERAL`, `CHAIN_SOURCE_MISSING`, `CHAIN_SOURCE_SESSION`, `CLAIM_SOURCE_EPHEMERAL`, `CLAIM_SPAN_UNEXPECTED`, `POINTER_UNRESOLVED`, `REJECTION_REASON_ABSENT`, `VERIFY_ALL_SECTION_UNAVAILABLE` | 01, 13 | **absorb** — the IDs are emitted and documented; selftest coverage is a named debt (round-17 queue) |
| `wc -c` fallback reads oversized files before refusing (contradicts "refused before any read") | 03, 04 | **absorb** — the named limit is corrected in `hardening-r10` and `mount-alias-r14.md`: the `wc` fallback reads to measure, it does not search content; the "refused unread" contract holds for the primary stat path only |
| Total measurement failure bypasses the cap (all probes fail → falls through to `cat`) | 03 | **absorb** — already disclosed at `SCORECARD.md:582`; named limit, not new |
| `ptr_resolves_meta` root-slash site not exercised by cases 107–110 (claims/sweeps only) | 10, 12 | **absorb** — the site IS fixed (same `in_root` helper); coverage gap named, not a code defect |
| Scope screen: fenced heading can shadow a refused declaration (`load_sections` resets on `## ` without recognizing fences) | 02 | **named debt** — real defect, queue for round 17; the declaration-only contract is documented as declaration-only |
| `LLM benchmarks` passes despite model-quality boundary (`SCOPE_KENGAKU` has `model benchmark(s)` not `LLM benchmark(s)`) | 02 | **named debt** — phrase-list gap, queue for round 17 |
| Scope-refusal coverage overstatement: cases 86–92 don't pin Meta `note` cell or Approval `scope` column | 29 | **absorb** — `scope-refusal-r12.md:59-62` corrected to name the actual pinned surface |
| `full-r6.README.md` says sweeps absent for `full-r6-absent.md` but `## Rejections` makes sweeps applicable | 34 | **absorb** — fixture README corrected; the composed verdict is unchanged (CLEAN) |
| `--json` manifest append doesn't ensure delimiter before new object | 24 | **named debt** — the manifest contract is append-only; the delimiter edge is a real defect for hand-edited manifests |
| `--drift` manifest timestamp masked too broadly (`[^"]*` matches any string, not just valid UTC) | 25 | **named debt** — the volatile contract is shape-scoped by design; tightening the mask is a round-17 candidate |
| `--drift` can't distinguish truncated baseline from valid drift | 26 | **named debt** — the baseline format is documented; truncation detection is a round-17 candidate |
| Sweeps guard: wildcard can cross a symlink inside root to reach outside dir | 20 | **named debt** — the sweep's `readlink -f` canonicalizes the BASE, not each glob match; a symlinked dir inside root resolves to its target and the guard compares that target against the root prefix — a real gap for crafted symlink trees |
| Relative-root missing paths report `OUT_OF_CORPUS` instead of `MISSING` (canon falls back to raw candidate which is relative) | 52 | **named debt** — the refusal class is wrong (crit vs warn) but the refusal itself is correct; the `//`-concat artifact documented in `root-slash-boundary-r15.md` |
| Secret scan doesn't cover cited local source files (scan_secrets runs on record+claims, not resolved source paths) | 40 | **named debt** — a coverage gap; the secrecy surface is documented in PROVINCE.md |
| URI-like citations treated as local paths when a matching file exists | 36 | **named debt** — the boundary held; classification edge case |
| Manifest append outside `--root` succeeds (no containment check on `--json` destination) | 24 | **named debt** — the docs describe `--json PATH` as an output destination; root containment is not claimed |
| Bash 3 compatibility: `[[ =~ ]]`, `coproc`, `${var^^}` etc. are bash-4+ | 56 | **named debt** — bash 3 is not a declared target; if needed, declare bash 4.2+ |
| Empty claims file passes vacuously (no minimum-claim check) | 53 | **absorb** — the contract is documented: CLEAN when every read claim matches; zero claims is zero violations |
| Older knowledge notes carry stale "hardlinks remain carried" status | 05 | **absorb** — the notes are dated snapshots; `hardening-r10` is the live ledger |
| hardening-r10 count phantom (E3 counted bind item as a carried row) | 30, 31 | **absorb** — corrected in E4 addendum; row-true counts recorded |
| Conformance: exploratory claims not declared as such (r15 note claim) | 45 | **absorb** — the r15 depth claim was falsifiable (note exists, measured claims reproduced); the exploratory-claim rule applies to taste-bound claims only |
| FAIL summary omits skipped count (PASS includes it) | 48 | **absorb** — diagnostic asymmetry, not a counter defect |
| `--` delimiter shifts once and stops parsing | 43 | **named debt** — arg-parsing edge, not a defect under documented usage |
| Permission change after preflight can make `verify` abort non-2 | 44 | **named debt** — TOCTOU on readability; the preflight check is the contract |
| `verify` `ptr_resolves_meta` checks relative pointers without canonicalization | 52 | **absorb** — relative pointers resolve under ROOT or LANE_ROOT; the `-f` test is the boundary |
| Chain `to` claim-ID can pass when a matching local file exists (kind-blindness) | 18 | **absorb** — already a carried limitation (`reference-integrity-r7.md:205,265-277`, hardening-r10 item 41) |
| r15 roster internally complete but raw wave file not committed to `.ufo` | 63 | **absorb** — the roster is in the report; the wave file lives in the session log (receipt identity still open via L0) |

### Named limits confirmed open (unchanged)

| limit | seats confirming |
|---|---|
| same-device binds stat-invisible | 07, 08 |
| overlay roots (file-vs-root-dir comparison) | 07, 08 |
| TOCTOU | 07, 08 |
| unmeasurable-stat fallback | 03, 07 |
| `--root /` sweeps guard vacuous by declaration | 09, 20 |
| `//`-canon MISSING artifact (pre-fix mechanism changed, same observed) | 28 |

## The corrected battery

The r15 battery receipt is replaced: `corpus/evidence/root-r15-20261019T152000Z-battery.log` now runs `verify` on `corpus/fixtures/archives-r9/{A,B,C}-r9.md` with `--root ..` (the research corpus resolves), plus `verify-claims`, `verify-chain`, `verify-sweeps`, `verify-integrity`, `verify-all` on their respective fixtures. Masked diff vs the pre-round gate (`aabf7f4`): ALL IDENTICAL.

## The `--root //` fix

`in_root` (`tools/research-gate.sh` ~:612) now strips all trailing slashes:

    local c=$1 r=$2
    while [[ $r == */ && $r != / ]]; do r=${r%/}; done
    [[ $r == / ]] && r=
    [[ $c == "$r" || $c == "$r"/* ]]

`pwd -P` preserves `//` (measured: `cd // && pwd -P` → `//`), so a single
`${r%/}` left `/` — which still rendered `//*`. The loop collapses `//` → `/`
→ `""`; `""/*` renders `/*` which matches `/` and every descendant. Selftest
case 111 pins it (`/etc/hostname` read under `CHOUSA_ROOT=//`).
