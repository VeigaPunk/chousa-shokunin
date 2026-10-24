# Round 39 — verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
round: 39
report: .ufo/reports/round-39/chousa.md (fleet commit f713ee1c1c6faf89a2bd66dcb5fab80d0698fb61, author chousa-shokunin)
lane tip: 6ac1007e6a5d699d0742801026554fac1d900b5d (pre-round 8c7c867b66e103712ae33e1d076786f50dd3239e)
dispatch digest (from .ufo/watchdog.log, mutable): launch 2026-10-24T02:24:06-03:00 `launch chousa round=39 pgid=2685723 driver=hyaku-inline attempt=1`; complete 2026-10-24T03:18:39-03:00 `complete chousa round=39; hyaku-inline attempt=1`.

## Step-1 conformance

| Check | Command | Result |
|---|---|---|
| Report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-39/chousa.md` | `chousa-shokunin f713ee1c1c6faf89a2bd66dcb5fab80d0698fb61` — pass; ancestor of fleet HEAD (`git merge-base --is-ancestor f713ee1 HEAD`) — pass |
| SHONEN heading, one line per box | read of report | `## SHONEN` present, 4 boxes all `[~]` with pointers — pass |
| Cited commits exist + ancestor of lane branch | `git merge-base --is-ancestor 6d914e9519ff34717b87f8a0b1bfbd004ddb53ee master` and `… 6ac1007e6… master` | both hold (branch ref, not `@{u}`; HEAD detached as expected) — pass |
| Lane clean + pushed | `scripts/hyaku/jj-lane.sh state chousa-shokunin` | `local=6ac1007e6… remote=6ac1007e6… ahead=0 behind=0 tracked=0 untracked=0` — pass |
| Prompt carries template contract | read of .ufo/prompts/chousa-round-39.md | round-level items (mission/axes §1, L2 floor §3, commit-then-push §5, push scope §5, L0 §5) + five child-lane items (report path §4, report-lands-last §6.4, SHONEN heading §4, commit-hash citation §4/§5, write scope §3) all embedded; no L2 route map quoted that could drift from MISSION.md — pass |
| Marker test | report read | real report with claims, evidence pointers, landed hashes — not a marker |

## Claim re-checks (committed bytes; the gate and counters are sibling-owned and were NOT executed — receipts and digests were re-derived by hand and the receipt verifier run read-only over committed bytes)

### C1 — operability: `ENV_PIN_CAPTURE_MATCH` 7/8 → 8/8 — VERIFIED (with routed defect R1)

- `sha256sum tools/research-gate.sh` at tip and at 6d914e95 = `4253c187…07e3` — equals the `gate_sha256` bound in every after-receipt. Pre-round gate at 8c7c867 = `0447ad14…85a` — equals the committed control `.ufo/waves/round-39/controls/base-gate-r39.sh` and the base receipt's binding. Mutant control = `e1251030…` — matches its receipt.
- Receipt contents re-derived: `c1-base-s39001.json` matched 7/8, `predicate_holds=false`, eighth family (`capture-bash-path-pin`) FAIL with `GATE_DRIFT: -GATE_GREP` / suppress / relative-override-ignored observations — matches the report and claims.md before-state. `c1-after-s39011.json` / `c1-after-s39111.json` matched 8/8, `predicate_holds=true` — matches the after-state. `c1-mutenv-s39013.json` matched 4/8 failing exactly the three `BASH_FUNC_env%%` cells + `capture-bash-path-pin` — matches the discrimination claim.
- All 24 scenario expectation rows across the four c1 receipts tie **byte-exact** to the rows of the committed `expectations.jsonl` (python3 dict compare) — the measurements bind committed expectations content.
- Gate code spot-read: `bash_pin_init`, `RESEARCH_GATE_BASH` override, `BASH_PROVENANCE` refusal (exit 2) present at tools/research-gate.sh:531-579, invoked at line 8672; selftest cases 273–275 at 8566-8584.
- Self-test tally (committed evidence per §Gate standard): LOG.md:1450 and SCORECARD.md:2228 record `PASS (275 cases, 0 skipped)`; SKILL.md Gates table r39 row carries the 275-case selftest line.
- **Defect R1 (routed, must-fix):** the four c1 receipts bind `expect_sha256 3abd2dcb…`, but the committed `expectations.jsonl` hashes to `01cbdc3a…`; `python3 corpus/evidence/round39/verify-receipts.py --receipt receipts/c1-after-s39011.json --gate tools/research-gate.sh --counter corpus/evidence/round39/c1-count.py --expectations corpus/evidence/round39/expectations.jsonl` → `VERIFY-FAIL: expect-sha256-mismatch` (rc 1, re-run by me). The expectations file was edited after the c1 runs (the c2 defect fixes) without re-issuing the c1 receipts. The report's "six committed … all `VERIFY: ok`" is inaccurate for the four c1 receipts. The frozen predicate itself verifies from the receipt contents (8/8 on two seeds against the landed gate digest; no committed lower run exists), so C1 stands — but the receipts as committed do not re-verify. Fix in round 40: regenerate the four c1 receipts against the committed expectations file, or append a claims.md erratum naming the superseded expectations bytes (per the append-only rule).

### C2 — calibration: `RECEIPT_BINDING_MATCH` 8/8, r38 pipeline refuses — VERIFIED

- `verify-receipts.py` re-derived on `c2-after-s39121.json` against committed bytes → `VERIFY: ok` (rc 0, re-run by me). Same for `c2-after-s39101.json` field-by-field: matched 8/8, `predicate_holds=true`, `verifier_sha256 1b6e0de6…` = sha256 of committed `verify-receipts.py`, `subject_counter_sha256 91618e91…` = sha256 of committed `c1-count.py` (both at tip and at 6d914e95).
- Before-state re-derived: `verify-receipts.py --receipt corpus/evidence/round38/receipts/c1-after-s38001.json --gate tools/research-gate.sh --counter corpus/evidence/round38/c1-count.py --expectations corpus/evidence/round38/expectations.jsonl` → `VERIFY-FAIL: predicate-mismatch` (rc 1, re-run by me) — the committed r38 receipt refuses under the r39 verifier, as claimed.
- Verifier code spot-read (verify-receipts.py:133-139, 196-206): counter/expect/verifier/subject digests re-derived from committed bytes with named refusals `counter-sha256-mismatch`, `expect-sha256-mismatch`, `verifier-sha256-mismatch`, `subject-counter-sha256-mismatch` — matches the claim text.
- c2 receipt scenario rows tie to committed `expectations.jsonl` rows (verifier's expect-tie passed live).

### No axis harmed

`git diff 8c7c867 6ac1007e6 -- SCORECARD.md` adds only the r38 attribution correction (D4) and the round-39 section (claim table + per-axis verdicts + round-40 candidates); no pre-existing axis row changed. `git diff --stat … -- tools/research-gate.sh` = 134 insertions, 5 deletions (pin machinery + selftest cases only). Per-axis verdicts: operability improved (C1), calibration improved (C2), depth improved (2 knowledge entries), coverage unchanged, freshness improved narrowly, adjacency unchanged — re-derived above; none harmed.

### Routed-defect repairs D1–D6 (round-38 closure) — all landed

- D1/D2: `corpus/evidence/round38/claims.md` Erratum 14 (hash supersession `37e2b996…` → `0447ad14…`) and Erratum 15 appended, body untouched — verified by read.
- D3: erratum counts corrected — SCORECARD r38 section now says "§Errata 1–13" (was 1–12); LOG.md:1419 `§Errata 9–13`; LOG.md:1422 `frozen claims + 13 errata`; r38 lesson `## Correction` block (D3 item) — verified.
- D4: SCORECARD r38 attribution note (wave-2 seeds at integration revision `8e93bc91…`, tip evidence = regenerated receipts + one-hunk diff) — verified in the diff.
- D5: SKILL.md r37 counters row restored — the row now ends `| chousa |` with 8 cells/9 pipes (9th pipe before the trailing empty), diff shows the old owner-less row replaced; selftest bump 272→275 at SKILL.md:696 — verified.
- D6: r38 lesson correction block with URLs per contract rule 1 (S072 bash.info URL at decompressed line 30; S073 coreutils cksum-c URL as roff tty-link) + rejected-candidate wording correction — verified by read.

## Discernment spot-check (LEARNING.md — from outside)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S071 (env(1) manual) — re-opened this round, used-by extended | admit / re-cite | `/usr/share/man/man1/env.1.gz` — `sha256sum` = `4ae797e6…fb27` (matches row); `zcat \| sed -n '27,29p'` shows `-u, --unset=NAME` `.TP` at line 27 and "remove variable from the environment" at line 28 | **agree** | row anchor exact (DESCRIPTION lines 27–28, quote at 28, 6 words ≤ 25); the new knowledge entry's citation of the `-u` scrub semantics is grounded; used-by old→new change logged in the lesson |
| Rejected candidate: second `bash(1)` row | reject (S068 holds the file) | `corpus/SOURCES.md` S068 — `/usr/share/man/man1/bash.1.gz`, scope BASH_ENV startup file, mined | **agree** | S068 already holds the same file; the corrected lesson wording (D6b) matches: a same-file same-sentence duplicate, not a distinct scope |
| Rejected candidate: third `sha256sum(1)` row | reject (S070/S073 cover both scopes) | `corpus/SOURCES.md` S070 + S073 — both `/usr/share/man/man1/sha256sum.1.gz`, S073 `supersedes S070` anchor-label correction | **agree** | two mined rows already hold both scopes of the same file; a third row would add no new ground |

- Newly written SOURCES.md rows this round: none (registry 73 → 73, A 67/B 1/C 5; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 73 at 8c7c867 and at tip). No new-row quote to check; the one touched row (S071 used-by old→new) re-opened above and agrees.
- Census re-run: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, with exactly the 3 standing W04 duplicate-URL warnings named in the report (S051, S053, S073) — agree.
- Lesson `## Gate` quote check: "remove variable from the environment" = 6 words ≤ 25, located at decompressed line 28 — agree.

## Trend verdicts (closure grades)

- **expansion: improved** — two knowledge entries admitted on new round ground (`git diff --name-only … -- corpus/knowledge/` = exactly `capture-bash-pin-r39.md`, `receipt-verifier-subject-r39.md`), each with provenance trio (source/verified-at/recheck verified by read); S071 re-cited by new work. (The report's count "29 → 31" is wrong — the cited command gives 50 → 52; the trend itself is verified by the diff. Routed defect R3.)
- **quality: improved** — the r38 closure's two disagreements became named fixes (D3 count corrections, D6 lesson correction block — verified above); QUALITY criterion 56 lands from the three vacuous-fixture self-catches whose fixes are shown able to fail on the controls (base 7/8, mutant 4/8, named refusals — re-derived above); census exit 0 at closure; no older entry failed its re-check in this pass.
- **discernment: improved** — the lane's own in-round counter runs caught three authoring defects (identical-bytes doctored subject; stderr-only crash as "weakening"; benign PATH-`env` shim), mined as `## Mistakes` rows with class/evidence/captured-by/fix (verified by read); the routed repairs D1–D6 landed as named artifacts (verified above); this outside spot-check agrees with the gate on the admit and both rejects.

## Routed defects for round 40

- **R1 (must-fix):** four committed c1 receipts bind a stale `expect_sha256` (`3abd2dcb…`) that matches no committed bytes; they refuse `expect-sha256-mismatch` under the committed verifier. Regenerate the c1 receipts against the committed `expectations.jsonl` or append a claims.md erratum naming the superseded expectations bytes; correct the report/LOG "receipts (6), all VERIFY: ok" wording in the next report.
- **R2:** the superseded drafting receipt `c1-mutenv-s39003.json` (binding uncommitted bytes `89022659…` gate / `1c3b2a9e…` counter) is committed although the lesson records it as "not committed", and the report/LOG say "receipts (6)" while seven files are committed. Name it as superseded in the claims erratum (append-only; do not delete committed bytes).
- **R3:** report's knowledge-count claim "`ls corpus/knowledge/*.md | wc -l` 29 → 31" is wrong (observed 50 → 52 at the cited commits); keep counting commands re-derivable.
- **R4 (minor):** report's wave role mix (reviewer 6 / revenger 2) does not match the validated spec (`w1-spec.json`: reviewer 8 / revenger 0; totals 32 both).
- **R5 (minor):** SCORECARD's "two independent runners" overstates — both C1 receipt runs are the L1's own construction runs (the claims.md freeze itself discloses this); the host-mapping disclosure covers it, but the wording should say "two seeds".

## Admission

**ADMIT.** Both frozen predicates verify from committed bytes; the discrimination controls re-derive; no owned axis is harmed; the routed repairs D1–D6 landed. Claims were re-measured over committed receipt bytes (counts, digests, scenario-row ties) and evidence-verified where the lane owns the machinery (self-test tally, frozen claims, verifier refusals) per PROTOCOL §Gate standard closure consequence; the gate and counters themselves were not executed. Defects R1–R5 are status-neutral and routed above; R1 is the must-fix.
