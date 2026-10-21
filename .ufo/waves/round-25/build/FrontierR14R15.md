# FrontierR14R15 — drafted `## Frontier` paragraphs (rounds 14, 15)

Target: `chousa-shokunin/corpus/README.md`, insert after the Round 10 paragraph
(`:457–485`, ends `is unchanged.`) and before `Still open and integrator/operator-owned:` (`:487`).
Not edited: this is a read-only seat; the paragraphs below are for the integrator.

## Draft paragraphs

Round 14 ran the bind-alias move its opening registered: the claim and chain chokepoint now refuses a source whose st_dev differs from the resolving root's device (`CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`, crit), and one `stat -c '%s %h %d'` probe serves nlink, size and device. The wave was one 64-seat call on alibaba-token-plan / deepseek-v4.1-flash, 63/64 reports (seat 54 failed on a provider content-filter 400; recorded, not backfilled). The observable moves on the live bypass pair: a tmpfs mounted over an in-root directory reads `observed=supported` CLEAN (`VERDICT_BEARING_CLAIMS=1/1`, rc=0) at the pre-round gate `6b17e50c…`, and `observed=refused` with `CLAIM_SOURCE_CROSS_DEVICE` crit (`0/1`, rc=1) at the landed gate `d8bbd0bf…`. The selftest moves 102 → 106 (`PASS (106 cases, 0 skipped)`). The r12 drift baseline and r1 `3/3` are recorded as holding, but the round's own receipts for those two holds are not on disk. That observable is not saturated: the bypass pair is `mode=claims` only; the class is cross-device aliases only, so same-device binds (stat-invisible), overlay roots, the probe-to-read TOCTOU window and the unmeasurable-stat fail-open remain named limits; freshness is unchanged.

Round 15 ran the `--root /` dead-arm fix the round-14 wave queued: `"$root_r"/*` rendered `//*` at `root_r=/`, so every absolute in-`/` source refused `CLAIM_SOURCE_OUT_OF_CORPUS` crit. The fix is an `in_root()` helper (`tools/research-gate.sh` ~:612) with a materialized local, applied at the three same-class sites (`claim_source_path`, `ptr_resolves_meta`, `sweep_path_guarded`); the opening's one-token form was measured dead on bash 5.3.15 and the pre-registration was corrected before the wave. The wave was one 48-seat call on zai glm-5.3-flash, 48/48 reports. The observable moves on the `/etc/hostname` demo under `CHOUSA_ROOT=/`: the pre-round gate `d8bbd0bf…` refuses `OUT_OF_CORPUS` crit (`0/1`, DRIFT); the landed gate `dd0951d7…` reads it CLEAN `1/1`. The selftest moves 106 → 110 with cases 1–106 byte-identical to the r14 receipt, and `--drift` reads `GATE_DRIFT: none`. The r15 battery receipt on disk does not carry a green hold: it is a `root=.` verify-all run that reports DRIFT (`drift-sections=3 findings=13`), and it has no identity line. That observable is not saturated: the fix covers the pattern arm only, the sweeps guard is vacuous at `/` by declaration, and the r14 limits carry over; freshness is unchanged.

## Grounding (path:line)

Round 14
- Wave 64 seats, 63/64, seat 54 failed: `SCORECARD.md:681–684`; `LOG.md:601`; `.ufo/reports/round-14/chousa.md:11–12, :116`.
- Gate `6b17e50c…` → `d8bbd0bf…`: `SCORECARD.md:690, :696`; `LOG.md:605`. Command check: `git show f472dbc:tools/research-gate.sh | sha256sum` → `6b17e50c…`; `git show e17742f:…` → `d8bbd0bf…`.
- Bypass pair: `corpus/evidence/mount-r14-20261019T132025Z-bypass-before.log:2–5` (observed=supported, 1/1, CLEAN, rc=0); `-bypass-after.log:2–6` (refused, CROSS_DEVICE crit, 0/1, DRIFT, rc=1). Header line of both: `mode=claims`.
- Selftest 102 → 106: `LOG.md:596` and `SCORECARD.md:693` (102 before; no r13 selftest receipt on disk, so cases 1–102 `cmp` is unverifiable here); receipt `mount-r14-…-selftest.log:107` `PASS (106 cases, 0 skipped)`; 106 `ok-case` lines (`grep -c`).
- Battery: `mount-r14-…-battery.log:1–2` (summary only, "ALL IDENTICAL"); `SCORECARD.md:705–707`.
- Drift none and r1 3/3: `SCORECARD.md:693–694`, `LOG.md:596, :605`; no r14 drift or tally receipt in `corpus/evidence/`.
- Claim scope: `SCORECARD.md:711` says "claims + chain + verify-all … refuse alike"; only claims receipts exist on disk.
- Verdicts: `SCORECARD.md:711–716, :718–725`; capability `:731`; `LOG.md:607`.
- Named limits: `corpus/knowledge/mount-alias-r14.md:39–58`; header `:3–5`.

Round 15
- Opening claim, 48/48: `SCORECARD.md:739–741`; `LOG.md:613–615, :619`; `.ufo/reports/round-15/chousa.md:8`.
- Pre-registration correction (inline form dead): `LOG.md:621`; `corpus/knowledge/root-slash-boundary-r15.md:41–45`.
- Gate `d8bbd0bf…` → `dd0951d7…`: `SCORECARD.md:743, :751`; `LOG.md:624`. Command check: `git show aabf7f4:…` → `d8bbd0bf…`; `git show 58cf0b9:…` → `dd0951d7…`.
- Demo: `corpus/evidence/root-r15-20261019T152000Z-demo.log:3–6` (before: OUT_OF_CORPUS crit, 0/1, DRIFT), `:10–12` (after: supported, 1/1, CLEAN). No rc printed in this file.
- Selftest 106 → 110: `root-r15-…-selftest.log:107–110`, `PASS (110 cases, 0 skipped)` at `:110`; cases 1–106 vs `mount-r14-…-selftest.log`: `cmp` IDENTICAL (command output: `IDENTICAL_1_106`).
- Drift: `root-r15-…-drift.log:1` `GATE_DRIFT: none`.
- r1 3/3: `SCORECARD.md:749` only; no tally on disk (`grep EXPORTS` on r14/r15 receipts: no hit).
- Battery, DRIFT on disk: `root-r15-…-battery.log:113` (verify-all, `root=.`), `:114` structure DRIFT, `:122` claims 0/3, `:126` chain 0/3, `:132` `drift-sections=3 findings=13`, `:133` DRIFT. Contradicts `SCORECARD.md:767` and `corpus/evidence/README.md:642` ("ALL IDENTICAL", unqualified). `.ufo/reports/round-16/chousa.md:14` says the file was replaced with `--root ..`; the on-disk file still shows `root=.`.
- Verdicts: `SCORECARD.md:771–776, :778–781`; `LOG.md:626`.
- Knowledge: `corpus/knowledge/root-slash-boundary-r15.md:7–20` (dead arm), `:36` (in_root), `:51–59` (sites), `:61–74` (limits).

## Other findings (not in the two paragraphs)

- `corpus/README.md` Frontier has Round 2–10 (`:321–457`) and Round 24 (`:491`) only; Round 11–13 and 16–23 paragraphs are absent. Round 14/15 are the two this item asked for.
- `LOG.md:603` still cites `mount-r14-20261019T125621Z-…`; on-disk names are `132025Z`. The append-only fix at `LOG.md:625` covers only `:596`; `corpus/knowledge/hardening-r10.md:516–518` carries the correction.
- `LOG.md:645` (round-16 battery line) reads `Gate dd0951d7… → <FILL>`: an unfilled placeholder.
- Tool install/update: none (sha256sum, git show, grep, cmp, cut were already present).

VERDICT: two paragraphs drafted and grounded; the r15 battery "green" hold is not supported by the on-disk receipt and is stated as such, not papered over.
