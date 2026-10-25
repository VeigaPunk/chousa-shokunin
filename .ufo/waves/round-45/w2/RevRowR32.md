# Review of SKILL.md Gates row `research-gate round-32 v1 counters` (line 101 @ 5e8c7ad)

Lane commit: `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`
Tree: `/tmp/chousa-r45-RevRowR32/tree` (git archive, counters run from inside it).
Row text (verbatim):
| research-gate round-32 v1 counters | gate | `python3 corpus/evidence/round32/c1-count.py` · `python3 corpus/evidence/round32/c2-count.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`; C1 needs /proc/locks) | `APPEND_SERIALIZED=24/24` · `EXEMPT_AUDIT_MATCH=120/120` exit `0`; any other count exit `1`; harness error exit `2`; SUPERSEDED by `corpus/evidence/round32/c1-count-v2.py`/`c2-count-v2.py` (the round-32 row above) — rejected as P1/P2 counters because controls met them under design v1 (`lessons/round-32.md`) | before on the round-31 gate `0bc318b3`: 8/24 (C1, L1 do-nothing seed 11), 84/120 (C2, seed 21); the v1 counters are met by controls: `CtlC1PartialLockB` probe-only lock 24/24 (`w1/CtlC1PartialLockB/b-s3247102{1,2}.json`); duplicate-finding/no-verdict/clean-exit/stray-unknown outputs 120/120 (`w1/CtlC2NoisyB`, `w1/MutC2CounterB/frozen-*`); case-insensitive/whitespace-collapsing readers 120/120 (`w1/CtlC2WeakReaderB/*-isolated-mutated-*`) | contract `corpus/evidence/round32/claims.md` (design v1, commit `4111607c`); base gate `0bc318b3`; L1 receipts `controls/L1-design/base-s11.json`, `controls/L1-design/c2-base-s21.json`; measured 2026-10-25 on gate `2cb04bdd…` @ `d82cec90`: 24/24, 120/120, both exit 0 | temp dirs only; no network; never writes into the lane (a receipt only when `--receipt` is given) | chousa |

## Verdict: HOLDS (all 8 cells)

Cell 1 name, 2 kind, 8 owner: match the dispatch item (`research-gate round-32 v1 counters`, gate, chousa). HOLDS.

Cell 3 entry — HOLDS.
- `python3 corpus/evidence/round32/c1-count.py` (tree root, default gate `tools/research-gate.sh` present in tree) →
  `APPEND_SERIALIZED=24/24` + per-class lines (F_unterminated 12/12, L_empty 4/4, L_terminated 4/4, L_unterminated 4/4); `C1_EXIT=0`.
- `python3 corpus/evidence/round32/c2-count.py` → `EXEMPT_AUDIT_MATCH=120/120` + 14 per-class lines; `C2_EXIT=0`.
- `/proc/locks` exists (C1 requirement). Both counters ran inside the tree without any argument except defaults.

Cell 4 verdict map — HOLDS (all branches exercised).
- 24/24 and 120/120 → exit 0 (above).
- “any other count exit 1”: stub gate (always exit 0) → `APPEND_SERIALIZED=0/24` exit 1; `EXEMPT_AUDIT_MATCH=0/120` exit 1.
- “harness error exit 2”: `--gate /nonexistent-gate.sh` → `c1-count: gate not found: /nonexistent-gate.sh`, `C1_MISSING_EXIT=2`; same for c2, `C2_MISSING_EXIT=2`.
- Supersession: `corpus/evidence/round32/c1-count-v2.py` and `c2-count-v2.py` exist in tree (glob); “the round-32 row above” = line 89 `research-gate round-32 counters`, whose entry names exactly those two files; `corpus/lessons/round-32.md` exists in tree; `corpus/evidence/round32/claims.md` (design v2 section) records the same rejection narrative (v1 committed at 4111607c; control wave broke both counters before any candidate receipt).

Cell 5 self-test — HOLDS.
- `0bc318b3` is the SHA-256 prefix of the round-31 gate script `tools/research-gate.sh` (not a commit): claims.md line 4 quotes full sha `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`; git history: commit `23536590` carried a gate blob with that hash (round-31 spotcheck lesson, `git show <rev>:tools/research-gate.sh | sha256sum` → `0bc318b3`).
- L1 receipts match: `controls/L1-design/base-s11.json` (found at `.ufo/waves/round-32/controls/L1-design/base-s11.json`) → seed 11, matched 8, `APPEND_SERIALIZED=8/24`, `predicate_holds=false`; `c2-base-s21.json` → seed 21, matched 84, `EXEMPT_AUDIT_MATCH=84/120`, `predicate_holds=false`.
- Control artifacts exist and carry the claimed values (`w1/…` under `.ufo/waves/round-32/`):
  - `CtlC1PartialLockB/b-s32471021.json`, `b-s32471022.json`: both `matched 24/24`, `predicate_holds=true`.
  - `MutC2CounterB/frozen-duplicate-finding-*` ×4, `frozen-no-verdict-*` ×4, `frozen-clean-exit-*` ×4, `frozen-stray-unknown-*` ×4: sampled receipt = `EXEMPT_AUDIT_MATCH=120/120`, true (4×4 = 16 files; sampled 4).
  - `CtlC2WeakReaderB/*-isolated-mutated-*` ×22 (case-insensitive ×2, whitespace-collapse ×2 sampled): 120/120, true.
  - `CtlC2NoisyB/` exists with duplicate outputs (`bounded-disjoint-duplicate-only-*`, etc.).

Cell 6 pinned values — HOLDS.
- `corpus/evidence/round32/claims.md` exists in tree; design-v1 text byte-identical to `git show 4111607c:corpus/evidence/round32/claims.md` (commit 4111607c resolves; diff = purely added v2 section). Base gate `0bc318b3` resolves as gate-script sha256 (above). L1 receipts exist at the pinned relative location.
- Measured line: current gate script sha256 = `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34` (prefix `2cb04bdd…`) at both `d82cec90` and `5e8c7ad` (file identical). My rerun on identical gate bytes reproduced 24/24, 120/120, both exit 0. (Date itself not independently provable; reproduction matches.)

Cell 7 write scope — HOLDS.
- After all counter runs (without `--receipt`), recursive file list + sizes of the archive tree are identical to a fresh extraction (diff empty) — no writes into the lane.
- `--receipt /tmp/…/c1-receipt.json` created only the given file (schema `chousa-r32-c1-receipt/v1`, matched 24, predicate_holds true, exit 0); no receipt elsewhere.

Row shape: exactly 8 cells (split on `|`, stripped; empty fields dropped) — name | kind | entry | verdict map | self-test | pinned values | write scope | owner.

## Residual risk / gaps
- `2cb04bdd…` and `0bc318b3` are abbreviated gate-script SHA-256s, not commit hashes; a reader expecting commits would not resolve them, but the row's own pinned contract (claims.md) defines them as gate SHA-256s, so this is a notation hazard, not a defect.
- The “measured 2026-10-25” timestamp references a measurement at `d82cec90`; I verified the gate bytes and reproduced the counts/exits on identical bytes, but did not locate the wave-1 receipt file for that specific measurement (receipts are not committed; on-disk .ufo receipts for round 45 w1 were not exhaustively searched).

## Commands exercised (verbatim decisive output)
```
cd /tmp/chousa-r45-RevRowR32/tree
python3 corpus/evidence/round32/c1-count.py   # APPEND_SERIALIZED=24/24; C1_EXIT=0
python3 corpus/evidence/round32/c2-count.py   # EXEMPT_AUDIT_MATCH=120/120; C2_EXIT=0
python3 corpus/evidence/round32/c1-count.py --gate /nonexistent-gate.sh   # c1-count: gate not found …; exit 2
python3 corpus/evidence/round32/c2-count.py --gate /nonexistent-gate.sh   # exit 2
python3 corpus/evidence/round32/c1-count.py --gate <stub exit 0>          # 0/24; exit 1
python3 corpus/evidence/round32/c2-count.py --gate <stub exit 0>          # 0/120; exit 1
git show 23536590:tools/research-gate.sh | sha256sum   # 0bc318b3… (round-31 gate)
sha256sum tools/research-gate.sh   # 2cb04bdd… @ 5e8c7ad = @ d82cec90
git show 4111607c:corpus/evidence/round32/claims.md   # "Round 32 — frozen claims (design v1)"
```
