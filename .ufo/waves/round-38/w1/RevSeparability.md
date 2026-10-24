# RevSeparability

## Verdict
The two claims are causally separable in both mutant directions (measured), but §Separability's "c2 … is gate-agnostic" is FALSE on the frozen bytes (base gate → `RECEIPT_BINDING_MATCH=4/7`, not 7/7); the 7/7 the ticket expected exists only after an uncommitted mid-wave rewrite of `expectations.jsonl`, and that rewrite plus three more artifact rewrites orphan all six committed receipts (they now fail `counter-sha256-mismatch` on the live tree).

## Evidence
Lane tip (read-only): `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` = `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`. Gate `tools/research-gate.sh` = `37e2b996…d27d`; base `.ufo/waves/round-37/controls/base-gate-r37.sh` = `a7d3922c…54e8`. Scratch `/tmp/r38-rev-sep` (receipts there). No tools installed; no lane writes (only this report).

Artifact bytes ([[frozen]] = HEAD = what seeds 38201–38207 ran on; worktree hashes now, mtime):
```
corpus/evidence/round38/c1-count.py        frozen da1d915b…  worktree 0ede9085…  00:53:23
corpus/evidence/round38/c2-count.py        frozen bc325cf4…  worktree 5ae3bd8c…  00:50:51
corpus/evidence/round38/verify-receipts.py frozen 756f186c…  worktree eb6aabf2…  00:52:18
corpus/evidence/round38/expectations.jsonl frozen 7cd5d824…  worktree c986c5fd…  00:49:20
corpus/evidence/round38/claims.md          frozen (tip)      worktree +6 lines   00:35:55
```
Frozen copies of all four extracted with `git show HEAD:…` into `/tmp/r38-rev-sep/frozen/`.

Baselines (fresh seeds, landed gate, frozen bytes): `c1-count.py --seed 38206` → `ENV_PIN_CAPTURE_MATCH=7/7`; `c2-count.py --seed 38207` → `RECEIPT_BINDING_MATCH=7/7` (this one bound the already-rewritten table `c986c5fd…`).

**(1) Gate-side single hunk** — copy of the landed gate, line 4001 `"$ENV_BIN" -u CHOUSA_RECORD …` → `env -u CHOUSA_RECORD …` (diff = one −/+ pair; sha256 `1bda0905…`):
```
c1-count --gate /tmp/r38-rev-sep/gauges/capture-only-revert.sh --seed 38201
FAIL env-fn-echo-scrub  echo_lines=1 drift_line='GATE_DRIFT: -GATE_GREP'
FAIL env-fn-root-move   drift_rc=1
FAIL env-fn-suppress    pin_rc=2 pin_file=False
PASS hold-plain, hold-fn-benign, env-override-missing, env-override-fake
ENV_PIN_CAPTURE_MATCH=4/7                      (exit 1)
verify-receipts (both frozen 756f186c and current eb6aabf2) --receipt /tmp/r38-rev-sep/c1-capture-revert-s38201.json
  --gate <mutant> --counter frozen/c1-count.py --expectations frozen/expectations.jsonl
VERIFY: ok                                     (pre==post=1bda0905…)
```
C1's cells are caused by that capture call; C2's binding still verifies an honest 4/7 receipt.

**(2) C2 against the BASE gate a7d3922c with the default r38 c1 counter:**
```
frozen c2-count (bc325cf4) + frozen table, --seed 38202
FAIL hold-receipt-verifies       counter_rc=1 (expect 0)
FAIL foreign-gate-distinguished  counter_rc=1 (expect 0)
FAIL legacy-receipt-refused      counter_rc=1 (expect 0)
PASS self-rewrite-refused, counter-tamper-detected, expect-tamper-detected, body-tamper-detected
RECEIPT_BINDING_MATCH=4/7                      (exit 1)
same gate, worktree c2-count (5ae3bd8c) + worktree table, --seed 38208
RECEIPT_BINDING_MATCH=7/7  (counter_rc=1 observed in all three cells, no longer asserted)
c2 on the capture-revert gate, frozen bytes, --seed 38205 → 5/7 (hold+foreign fail on counter_rc; legacy passes)
```

**(3) Minimal counter-side hunk** — in a copy of frozen `c1-count.py`, line 224 `if sha256_file(gate) != gate_sha_pre:` → `if False:` (byte-diff vs HEAD is exactly that line):
```
c2-count --counter /tmp/r38-rev-sep/mut/c1-count.py (sha 640945b5…) --seed 38203 → 6/7 (only self-rewrite-refused flips)
c2-count … --seed 38210 (worktree table)                                             → 6/7 (same single flip)
mutant c1-count --seed 38204 on the landed gate → ENV_PIN_CAPTURE_MATCH=7/7; verify-receipts ok
same mutant with a stale expectations copy, --seed 38209 → 0/7 (all cells; receipts bind 7cd5d824 vs verifier table c986c5fd)
```

**Committed receipts on the live tree:** for all six in `corpus/evidence/round38/receipts/`, `verify-receipts.py --receipt … --gate <recorded> --counter <worktree>` → `VERIFY-FAIL: counter-sha256-mismatch`. With frozen counter/table bytes: `VERIFY: ok` for 6/6 (`c1-base-s38001.json` only against the base gate, else `gate-sha256-mismatch`).

## Findings
1. **BLOCKER (wave integrity) — the frozen artifacts were rewritten mid-wave, uncommitted.** `expectations.jsonl` 00:49:20, `c2-count.py` 00:50:51, `verify-receipts.py` 00:52:18, `c1-count.py` 00:53:23; `git status` shows all four plus `claims.md` as ` M`. claims.md states nothing changes after the first wave receipt; the table edit redefines three c2 cells. Consequence: every committed receipt is orphaned — 6/6 `VERIFY-FAIL: counter-sha256-mismatch` on the live tree, and any re-run of the round's C2 predicate now measures a different predicate against different counter bytes. Either revert to `504c1d2` or land the change as a committed erratum plus regenerated receipts; a half-state cannot satisfy C2's own "no committed run prints a lower count" rule.
2. **HIGH — §Separability's gate-agnosticism is false on the frozen table.** `c2` on the base gate is 4/7 (seed 38202). The three failing cells assert `counter_rc == 0` — the subject counter's exit code on the supplied gate — and `c1-count.py` returns 1 whenever `matched < 7` (`c1-count.py:262` at HEAD). So at freeze, C2 could not be measured as satisfied by a gate that fails C1: "Either lands without the other" did not hold.
3. **MEDIUM — the rewrite manufactures agnosticism by deleting the observations.** Same probe, same gate: 4/7 frozen (seed 38202) vs 7/7 edited (seed 38208). The `counter_rc=1` is still present in the 7/7 receipt; the three `counter_rc` keys were removed from three rows of `expectations.jsonl` (diff lines for `hold-receipt-verifies`, `foreign-gate-distinguished`, `legacy-receipt-refused`). If gate-independence is to be claimed, assert the dependency explicitly (`counter_rc in {0,1}` + receipt-existence binding), not omit it.
4. **MEDIUM — C1's five separation cells ride on two disjoint hunks.** Capture-line-only revert fails exactly echo/root/suppress; both `env-override-*` cells still pass because `env_pin_init` (`tools/research-gate.sh:492-522`) independently refuses. The single-hunk mutant demonstrates 3 of the 5 cells; the startup-pin half needs its own mutant to show its two cells are load-bearing.
5. **MEDIUM — minimal C2-breaking counter hunk: one line, 5 chars.** `if sha256_file(gate) != gate_sha_pre:` → `if False:` moves c2 7/7→6/7 (only `self-rewrite-refused`) and leaves c1 at 7/7 with a verifying receipt (seeds 38203/38210 vs 38204). The faithful F1 restoration (hash after the run) flips the same cell [INFERENCE: same cell by construction, not separately run].
6. **MEDIUM — receipts do not bind the verifier.** No `verifier_sha256` field exists in either counter's receipt body, so `verify-receipts.py` changed at 00:52:18 (+88 lines: census check, per-row `ok` re-derivation, `predicate` required) silently re-adjudicates every existing receipt with no receipt-level record. Measured: the same receipt+bytes under frozen (`756f186c`) and current (`eb6aabf2`) verifiers both return `VERIFY: ok` for the honest 4/7 cases, so no divergence today — but nothing detects a future one.
7. **LOW — per-receipt gate path is required for a sweep.** `receipts/c1-base-s38001.json` yields `VERIFY-FAIL: gate-sha256-mismatch` against `tools/research-gate.sh` and `VERIFY: ok` against the base gate. A blanket `verify-receipts` sweep over `receipts/` must read `gate` from each body.
8. **LOW — a subject counter copy carrying its own expectation table collapses c2 to 0/7** (seed 38209), all cells, because receipts bind the copy's `expect_sha256` while `c2-count.py` verifies against the canonical table. Mutant-based c2 measurements must refresh the copy's table first (seed 38210 does; seed 38209 measures hash divergence, not the hunk).
9. **NOTE (frontier) — the post-drift `c1-count.py` hardens the label correctly**: `holds = matched == 7 and total == 7` and unlinks a stale `--receipt` path on refusal. The label fix is sound; the problem is that it landed uncommitted and mid-wave, alongside a predicate-changing table edit.

## Limits
- One run per (gate, counter, table) triple; seeds 38201–38210. Numbers are pinned to the artifact hashes above—my c2 runs before 00:49 can never be re-derived against the live tree, only against `/tmp/r38-rev-sep/frozen/` or `git show HEAD:`.
- Findings 1–4, 6 are observations of worktree state and byte hashes, not attribution: I did not identify which process wrote the files, and I made no lane writes beyond this report.
- Not probed: the pin-init-only mutant (F4's second direction), an absent-`gate_sha256`-alias receipt, and whether the hardened verifier rejects a re-sealed observation doctoring (its stated purpose) — all open, none claimed.
- Time-box reached after the third requested measurement plus the drift discovery; no further attacks were run.
