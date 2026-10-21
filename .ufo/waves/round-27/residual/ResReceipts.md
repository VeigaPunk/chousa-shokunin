# ResReceipts — round 27 attempt 1, residual post-falsify receipt re-verification

**VERDICT: HOLDS** — every counting command in the post-falsify receipt set reproduces
byte-for-byte at the assigned revision `cb895a2` (gate `a6bc2855…82386`); the falsify
control suite discriminates the checkpoint from the landed gate (4/26 kills before,
0/26 after); the census validates; S043's four cited report lines exist and match. Two
receipt-layer defects and one supersession are reported below (F1/F2 evidence hygiene,
F3 receipt reproducibility, F4 census scope). No landed-gate counterexample was found.

- Seat `ChousaR27-2.ResReceipts-16` · 2026-10-21 · read-only on the lane; the only
  lane write is this report. Target `cb895a2bdd259eb38bec29ef70011d8211a508b5`,
  `tools/research-gate.sh` sha256 `a6bc2855e63045c9ebc0827166756d4da65478a1e255a83903ab459a08582386`.
- Sandboxes (all /tmp): `…-ResReceipts` = `git archive cb895a2 | tar -x`;
  `…-ResReceipts-before` = `git archive dd72641e`; `…-ResReceipts-base` =
  `git archive 64eec5d4`; `…-ResReceipts-r1parent` = sandbox lane copy with the fleet
  `research/deep-research-2026-09-28` (3 files) beside it. Locale inherited
  `LANG=en_US.UTF-8` (no `LC_ALL=C` for the selftest); receipts compared:
  `.ufo/waves/round-27/post-falsify/` (16 files, mtime `2026-10-21 13:47:18 -0300`).

## 1. Reproduction of the nine counting commands (landed gate, sandbox)

| # | command (cwd = sandbox) | exit | decisive output | receipt | agree |
|---|---|---|---|---|---|
| 1 | `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` | 0 | `total 58, mismatches 0` (C1 6 / C2 21 / C3 31) | `regressions-after.stdout` | byte-identical |
| 2 | `python3 corpus/evidence/round27-falsify-controls.py --gate tools/research-gate.sh` | 0 | `total 26, mismatches 0` (C1 5 / C2 8 / C3 13) | `fc-after.stdout` | byte-identical |
| 3 | `python3 corpus/evidence/round27-mechanisms.py tools/research-gate.sh` | 0 | six mechanism counters all `0`; `sha256 a6bc2855…` | `mechanisms-after.json` | byte-identical |
| 4 | `bash tools/research-gate.sh --selftest` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | `selftest-after.log` | byte-identical (whole file) |
| 5 | `grep '^ok-case' selftest.log \| head -161 \| sha256sum` | 0 | `5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb` | expected `5eac4a7e…01cb` | match |
| 6 | `bash <lane>/corpus/evidence/round26-date-differential.sh <sb>/tools/research-gate.sh` | 0 | `DATE_DIFF_AGREE=9024/9024` | `date-diff.log` | byte-identical |
| 7 | `bash <lane>/corpus/evidence/round26-registry-differential.sh <sb>` | 0 | `REGISTRY_DIFF_AGREE=48/48` (+3 suite lines) | `registry-diff.log` | byte-identical |
| 8 | `bash corpus/evidence/round25-meta-differential.sh` (cwd = sandbox root) | 0 | `AGREE=54/54 (fixtures=27, modes normal+strict)` | `meta-diff.log` | byte-identical |
| 9 | `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` | 0 | `GATE_DRIFT: none` | `drift.log` | byte-identical |

Case identity for row 5: `diff <before-selftest> <after-selftest>` differs only at
lines 212–217 (cases 211–215 appended), so cases 1–210 are byte-identical to the
checkpoint run and "210 identities unchanged" holds.

## 2. Extra receipt rows re-derived

- **r1 observable** (`SCORECARD.md:29`, verbatim) → `VERDICT_BEARING_EXPORTS=3/3`, exit 0
  — matches `r1-observable.log`. (A first attempt gave `0/3` because my lane directory
  was a symlink so `../research/...` did not resolve; a real copied tree gave `3/3`.)
- **Before-state discrimination** (proves the control suite is not vacuous):
  `python3 <cb895a2>/corpus/evidence/round27-falsify-controls.py --gate <dd72641e gate>`
  → exit 1, `total 26, mismatches 4`: `C1 matcher-fault-fails-closed` (0≠1),
  `C2 scale-4mib-leading-zeros` (124≠0), `C3 escaped-pipe-width` (2≠0), `C3
  escaped-pipe-overwide` (0≠2) — identical to receipt `fc-before.json`;
  `round27-regressions.py --gate <dd72641e gate>` → exit 0, `58 / 0 mismatches`,
  `gate_sha256 ca39d14d…` — identical to receipt `regressions-after.json`.

## 3. Timing receipt (`timing.log`) — reproduced except one row

Fixture (4 MiB scale, synthetic, /tmp): entry `source:` line = 4 MiB of `a ` tokens; "registry" mode adds `--registry`, "plain" omits it.

| row | receipt | mine | verdict |
|---|---|---|---|
| `after dense` | rc=0 ms=402 CLEAN | rc=0 ms=408 CLEAN | reproduced |
| `after zeros` | rc=0 ms=827 CLEAN | rc=0 ms=468 CLEAN | same order (sub-second) |
| `before dense` | rc=0 ms=70153 CLEAN | rc=0 ms=73020 CLEAN | reproduced |
| `before zeros` | rc=0 ms=62818 CLEAN | rc=0 ms=65885 CLEAN | reproduced |
| `after dense(plain)` | rc=0 ms=409 CLEAN | rc=0 ms=285 CLEAN | reproduced |
| `before dense(plain)` | rc=0 ms=68240 CLEAN | rc=0 ms=64570 CLEAN | reproduced |
| `base64eec5d dense(plain)` | rc=124 ms=300016 | rc=0 ms=64474 CLEAN | **not reproduced** (F3) |

Every reproduced row prints the same verdict line `RESEARCH_GATE: CLEAN (entries=1
complete=1 findings=0 drift=0)`, so the receipt's "behaviour unchanged, cost repaired"
claim is corroborated: before ≈64–73 s → after ≈0.3–0.5 s (≈150×), consistent with the
CR-strip and token-prefilter repairs.

## 4. Census and S043

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`.
- S043 (`corpus/SOURCES.md:53`) cites four falsify reports; all four cited lines exist
  and match the row's scope text ("escaped-pipe width over-rejection, per-token cost,
  long-line CR strip, usage-matcher fail-open"):

| citation | content (verbatim head) | matches scope |
|---|---|---|
| `FC3ValidTable27.md:59` | "`IFS='|' read -a` splits on `\|`, so the header counts 5 cells against 4 delimiter cells… over-rejection" | escaped-pipe width over-rejection |
| `IntegTokenCost.md:20` | "the landed iteration introduces a new 12–34× per-source time regression" | per-token cost |
| `FC2Allzero128K07.md:18` | "quadratic CR strip `line=${line%$'\r'}` (identical statement in base), generic to any long line" | long-line CR strip |
| `FC1CorrectUsageWithHelp00.md:7` | "the landed helper fails open when its record matcher errors" | usage-matcher fail-open |

  Each report's own header targets `dd72641e…` / gate `ca39d14d…`, matching the row's
  scope column; all four are this lane's own falsify reports ("own-work … not outside
  admission" holds) and all are tracked at `cb895a2`.

## 5. Findings

**F1 — MEDIUM (evidence hygiene, corpus layer): the committed corpus/evidence
"after" artifacts describe the PRE-repair gate, not the landed gate.** `cb895a2`
did not refresh them (`git show cb895a2 --stat` touches only `corpus/SOURCES.md`,
`corpus/evidence/round27-falsify-controls.py`, `corpus/lessons/round-27.md`).
Attack: `git show cb895a2:corpus/evidence/round27-regressions-after.json` →
`gate_sha256 ca39d14db907…92f84` (expected `a6bc2855…`); `…/round27-mechanisms-after.json`
→ `sha256 ca39d14d…`; `…/round27-selftest-after.log` → `PASS (210 cases, 0 skipped)`.
All three are byte-identical (ts/tmp normalised) to my `dd72641e` runs: the
checkpoint's artifacts filed under an "after" name. Impact: an auditor reading
`corpus/evidence/` sees a 210-case selftest and the superseded gate digest; the
landed-gate evidence exists only under `.ufo/waves/round-27/post-falsify/`. Class:
control/coverage weakness (evidence layer), not a landed-gate behaviour defect; the
artifacts are base-identical (inherited from `dd72641e`).

**F2 — MEDIUM (same-identity / supersession): the lane working tree has already moved
past the revision the receipts describe.** `sha256sum tools/research-gate.sh` in the
lane → `438c0fcb0c4f97231090554203b9e625360c60a647b8f83163168009a330e806` ≠ receipt
gate `a6bc2855…`; `git diff --stat cb895a2 -- tools/research-gate.sh` → 16 changed
lines (escaped-pipe split/width rework in `metadata_registry_load`; header width back
to `${#cells[@]}`); `corpus/evidence/round27-falsify-controls.py` → `768a140e…` ≠
receipt `8d841d6a…`, with 4 new controls. Attack: `sha256sum tools/research-gate.sh`
→ `438c0fcb…` (exit 0). Impact: no receipt in the set describes the live gate and the
`a6bc2855` hash quoted in the round-27 registry row is stale; my verification targeted
`cb895a2` as assigned and the working-tree delta was not reviewed (other seats).

**F3 — LOW (receipt reproducibility): `timing.log`'s base row is not reproducible at
the scale of the other rows and the receipt records no fixture recipe.**
`base64eec5d dense(plain) rc=124 ms=300016` vs my base gate (`64eec5d4`, gate
`c2c813f1…`) at the same 4 MiB scale → rc=0 ms=64474 CLEAN; at 8 MiB the base refuses
the source instead of timing out (rc=1, `RESEARCH_GATE: DRIFT (entries=1 complete=0
findings=1 drift=1)`, 11 ms). The base row was measured on a different fixture and is
not checkable from the committed artifacts; the before/after comparison it supports is
reproduced.

**F4 — LOW (census scope): `sources-census.sh validate` checks row shape, id/date/status
enums and `used-by` path existence, not the `anchor` column's file/line citations.**
`chousa ok` does not certify S043's four line citations; I verified them by hand (§4).

**F5 — LOW (base-identical / inherited): nothing in the receipt set depends on the base
gate except the timing row (F3); the four controls that kill the checkpoint but not the
landed gate are the falsify-wave suite, new at `cb895a2`.**

## 6. Residual risk and verification gaps

- F1: the corpus/evidence layer still advertises the pre-repair gate and a 210-case
  selftest; consumers reading it rather than the wave receipts understate the landed
  state until those artifacts are refreshed.
- F2: receipts pin gate `a6bc2855` while the working tree is `438c0fcb`; until the
  tree is re-committed and re-receipted, no receipt describes the live gate.
- F3: the timing receipt's base row stays unverifiable without a recorded fixture.
- Out of scope here: the 63 falsify reports' individual claims; the correctness of the
  working-tree escaped-pipe rework; whether the working tree still passes the four
  suites (it moved while I measured). Host load inflated wall times by a few percent;
  no receipt disagreement is attributable to it (exit codes and verdict lines are
  load-independent).

## 7. Tooling

No installs or downloads; only preinstalled `bash`, `python3` (3.14), `git`, coreutils and
the repo's own scripts. Nothing in the lane was changed except this report (the
concurrent working-tree modification, F2, is another agent's work).
