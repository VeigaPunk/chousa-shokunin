# RevRowR33 — research-gate round-33 C1 v1/v3 counters (SKILL.md Gates row)

Measured over committed bytes: `git archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1` → `/tmp/chousa-r45-RevRowR33/tree`; every counters ran from that tree root. Row = SKILL.md line 102 (read `:raw:102`). Row has **exactly 8 cells** (name | kind | entry | verdict map | self-test | pinned values | write scope | owner) — confirmed.

## Per-cell verdict

**1. name — HOLDS.** `research-gate round-33 C1 v1/v3 counters` names the two entry counters (v1, v3).

**2. kind — HOLDS.** `gate`; both counters implement gate exit contract 0 holds / 1 otherwise / 2 harness.

**3. entry — HOLDS.** `python3 corpus/evidence/round33/c1-count.py` · `python3 corpus/evidence/round33/c1-count-v3.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`). Both files exist in tree (c1-count.py ab6b2ae2…; c1-count-v3.py bd81aeea…), accept `--gate/--seed/--receipt`, and run from lane root with default `--gate tools/research-gate.sh`:
- `python3 corpus/evidence/round33/c1-count.py --seed 12345` → `TOPLEVEL_FIELD_MATCH=144/144`, exit 0.
- `python3 corpus/evidence/round33/c1-count-v3.py --seed 12345` → `TOPLEVEL_FIELD_MATCH=156/156`, exit 0; receipt run seed 9401: `gate_rc=1`, `holds=True` (v3 counts only when the gate exits 1 with a `RESEARCH_GATE: DRIFT` line; counter lines 423-424).

**4. verdict map — HOLDS.** Row: `v1 TOPLEVEL_FIELD_MATCH=144/144 (superseded by corpus/evidence/round33/c1-count-v2.py, design v2, before any candidate; its control receipts stay v1-only evidence) · v3 TOPLEVEL_FIELD_MATCH=156/156 (gate must exit 1 + RESEARCH_GATE: DRIFT; repair E2 replaces v2's six fixed confuser literals with per-seed generated content) · exit 0 iff holds, 1 otherwise, 2 harness`.
- v1 144/144 observed (seeds 12345, 7777; exit 0). Supersession file `c1-count-v2.py` exists (cb354dd1…); claims.md §Design v2 confirms supersession before any candidate (claims.md:93-99). v1 control receipts remain v1-counter receipts (counter_sha256 ab6b2ae2… = c1-count.py). v3 156/156 observed with gate_rc=1 (+DRIFT). Exit 0/1 observed empirically (0 on 156/156, 1 on mask 155/156 runs); exit-2 harness paths verified in code (missing gate / fixture-gen / receipt failure → return 2, c1-count.py:331-344,405-411).

**5. self-test — HOLDS.** Row: `before on the round-32 gate f4731885: 60/144 (v1) and 60/156 (v2, duplicates 0/24); a three-key duplicate gate meets v1 144/144 (critic F1 → v2); the fixture-literal mask gate ae7d4bfc meets v2 156/156 (seeds 3391/3392) → v3; the mask gate misses v3 155/156 on seeds 9401/9402 but meets 156/156 on seed 61111`.
- `f4731885` is the content SHA-256 of the round-32 gate (`f4731885ac0f8307…003f0f`; claims.md:4). Archived copies in tree: `.ufo/waves/round-33/w1/CtlC1DoNothing/research-gate-do-nothing.sh`, `CtlC1BraceDepth/pristine-gate.sh`, etc. Before-receipts committed and matching: `controls/L1-design/c1-base-s3301.json` → 60/144 (seed 3301, gate_sha f4731885…, rc 1); `controls/L1-design-v2/c1v2-base-s3311.json` → 60/156 (seed 3311, duplicates 0/24).
- Three-key duplicate gate: `.ufo/waves/round-33/controls/L1-mistake/three-key-dup-gate.sh`; reran `c1-count.py --gate … --seed 3381` → `144/144`, exit 0. Critic F1 cited in claims.md:95-97; `w1/CriticAxisFit33.md` exists in tree.
- Mask gate: `.ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh`, sha `ae7d4bfc7ac1d262…` (matches). Receipts `mask-s3391/3392.json` → 156/156 (v2 counter cb354dd1…, rc 1); reran `c1-count-v2.py --gate mask-gate.sh --seed 3391` → `156/156`, exit 0.
- Reran `c1-count-v3.py --gate mask-gate.sh` seeds 9401, 9402 → `155/156`, exit 1 each; seed 61111 → `156/156`, exit 0.

**6. pinned values — HOLDS.** Row: `contract corpus/evidence/round33/claims.md (design v2, commits 3b528b9a→e3e24ec8); final gate 43a1af35ca668fe5…4346; v1 controls .ufo/waves/round-33/controls/L1-design/; v2 receipts .ufo/waves/round-33/measure/final/ seeds 3701/3702`.
- `corpus/evidence/round33/claims.md` exists; contains frozen v1 claim + §Design v2. Commits `3b528b9a` (round-33: design v1 before data) and `e3e24ec8` (design v2 before data) resolve in the repo.
- Final-gate sha `43a1af35ca668fe5…4346` = content SHA-256 of the round-33 gate, full `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`; archived copies in tree: `.ufo/waves/round-34/w1/CtlC1DoNothing/base-gate.sh`, `CtlC1BoundaryBlind/base.sh`, etc.
- `controls/L1-design/` exists (c1-base-s3301.json, c1-oracle-s3302/3303.json, oracle-gate.sh, mk-oracle.py). `measure/final/` exists with `c1v2-s3701.json`, `c1v2-s3702.json` → both 156/156, holds=True, seeds 3701/3702, counter cb354dd1….

**7. write scope — HOLDS.** Row: `temp dirs only (keep C1_TMP outside the gate's lane root); receipt only when --receipt given; no network`. Code: mkdtemp under `C1_TMP`/gettempdir (c1-count.py:333-335); receipt written only if `a.receipt` (:395-411); no network paths; env strips `CHOUSA_*` before gate runs (:347).

**8. owner — HOLDS.** `chousa`, consistent with sibling gate rows.

## Findings / residual risk

- No wrong cells. The only correctable nit: the row's gate pins (`f4731885`, `ae7d4bfc`, `43a1af35…`) are **content SHA-256s of gate scripts**, not commit ids — they do not resolve as git objects, but they do resolve to identical archived copies in the committed tree (and claims.md:4 spells out the full f4731885 hash), so every pin is openable at 5e8c7ad.
- Exit-2 harness branch was checked by code inspection, not executed (no harness-error scenario was induced); gate-absent path returns 2 (c1-count.py:331-332).
- No tool installs (none needed). No lane writes; scratch `/tmp/chousa-r45-RevRowR33` removed after this report.
