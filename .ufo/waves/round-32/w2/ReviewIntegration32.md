# ReviewIntegration32 — full gate-diff review (base 7a7259f0 → candidate 5d8a1707, tools/research-gate.sh 10f2fe12)

Attacked: the merge of C1 (flock-serialized `--json` append), C2 (exempt-hop audit via `chain_probe`), R2 selftest, plus the R4c comment. Looked for unintended changes, duplicated helpers, broken case-numbering comments, leftover conflict text, changes outside the declared regions.

## Verdict: HOLDS

The merged gate is functionally clean: no conflict markers, no duplicated definitions, `bash -n` clean, `git diff --check` clean, all 12 diff hunks sit inside the declared regions, selftest `PASS (241 cases, 0 skipped)` on candidate bytes, and my own counter run reproduced 132/132. Two low-severity documentation defects found (below); nothing that undercuts P1 v2 or P2 v2.

## Evidence

- `git diff 7a7259f0 5d8a1707 -- tools/research-gate.sh` → 12 hunks only: header doc (101,194), usage text (356,396), `chain_probe` + `verify_chain` (1783–1901), `verify_all --json` block (3189), selftest comment + new selftest cases (6799,6869). Nothing outside C1/C2/R2/R4c regions.
- `grep -nE '^(<{7}|>{7}|={7}|\|{7})' gate-landed.sh` → 0 hits; `git diff --check` → clean.
- Duplicate-definition sweep (`grep -nE '^[a-z_0-9]+\(\)' … | uniq -c | awk '$1>1'`) → none. `chain_probe` defined once (landed :1813).
- `bash -n` → OK; `shellcheck -S error` → one SC1087 at :7149 (cosmetic: scalar `$c1lk_ino[` inside a regex string; bash parses correctly).
- flock semantics verified empirically: `exec {jfd}>>f; flock -x "$jfd"` leaves a `FLOCK ADVISORY WRITE` entry in /proc/locks held by the parent after flock(1) exits; `if ! exec {fd}>>dir; then` fails closed (message printed, script continues) rather than aborting. `command -v flock` guard + `exit 2` paths present (:3288–3302).
- Resolved-arm refactor equivalence: base vs landed `verify-chain` on `corpus/fixtures/chain-r3.md` and `chain-r3-broken.md` (copied into scratch lane root) → **byte-identical except the appended `resolvable=N` summary field and timestamps** (17 refused hops and 5 exempt hops reproduce exactly; exempt stays exempt).
- Full selftest on candidate bytes in scratch lane (`tools/research-gate.sh` at `<dir>/tools/`, PROVINCE.md at lane root, TMPDIR outside): `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`, all 13 new cases ok (229–241). (A first run without PROVINCE.md failed `claims-lane-fallback` — scratch-harness artifact, same caveat w1 recorded.)
- My counter run: `c2-count-v2.py --gate <scratch>/lane/tools/research-gate.sh --seed 773312` → `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, `predicate_holds=true`, `gate_sha256=10f2fe12…` → receipt `.ufo/waves/round-32/w2/ReviewIntegration32/c2-s773312.json`.
- L1 measure receipts re-read: all four carry `predicate_holds=true` on `10f2fe12` (after-c1-s32001/2, after-c2-s32011/2).

## Findings (severity ascending)

1. **LOW — `tools/research-gate.sh:7097,7101`**: the r32-C1 selftest comment labels its cases "229:" and "230:", but in the merged gate they run as cases **233 and 234** (selftest2.out: `ok-case 233 c1lk-holder-blocks-append`, `ok-case 234 c1lk-second-append`). The labels are stale from the C1-only build (where they followed 228); the merge put the four C2 cases (229–232) in front. Cosmetic; no reader parses them.

2. **LOW — `tools/research-gate.sh:6910`**: the R4c comment now reads `# ---- r31 C2: … (cases 216-228)` but the sha block runs as cases **220–228** — confirmed by three independent selftest outputs: w1 `ExecNoHarmBase32/selftest.cases:220-228`, the cited `.ufo/waves/round-31/falsify/MutC2Parse/m2-trim-space.selftest.stdout:221-229` (which itself prints 220–228, not "216–228" as `corpus/evidence/round32/r31-repairs.md` row R4 claims it does), and my landed-gate run (`ok-case 220 claims-sha-absent` … `ok-case 228 claims-sha-crlf`). So R4c replaced a stale `216-224` with a different wrong range, and the repair record's evidence sentence misquotes its own source. The nine `tclaims` calls in the block (landed :6911–6978) span exactly 9 cases. Comment-only; no behavioral impact.

## Observation (hazard for other seats, not a gate defect)

The lane **working tree** currently holds a *different* gate: `sha256sum tools/research-gate.sh` = `d13a76e3…` (modified vs HEAD 5d8a1707, whose tree carries the candidate `10f2fe12…`). Any seat that points a counter at the working-tree path silently scores `d13a76e3`, not the candidate — my first run did exactly that (`c2-s773311.json`, kept as evidence: it also scored 132/132). Receipt consumers should check `gate_sha256` == `10f2fe12…`.

## Residual risk / gaps

- Resolved-arm equivalence verified on the two shipped fixtures only; the rewrite is a mechanical extraction into `chain_probe` (`at=` identical because `chain_anchor_at` self-resets `CITE_AT=-` on failure, :1718) — residual risk low.
- `tail -c1` probes the path, not the locked fd: a rename/replace of the manifest mid-run (non-cooperating writer) escapes the lock. Outside the C1 contract (cooperating appenders only), but a real boundary — `[INFERENCE]` exploitable only by writers the contract never promised to serialize.
- The `/proc/locks` wait-for-`->` regex in the selftest (:7149) matches a *blocked* lock entry; correct on this host (case 233 passed), possibly flaky under heavier timing on other kernels.
- `resolvable=%d` is appended unconditionally to the `RESEARCH_GATE:` chain summary — declared surface change; c2-count-v2 checks only the `RESEARCH_GATE: DRIFT` prefix, consistent.
- No installs performed; all commands bounded by `timeout` ≤1500 s; no lane/fleet repo writes; scratch confined to `/fast/scratch/hyaku/chousa-r32/w2/ReviewIntegration32/`.
