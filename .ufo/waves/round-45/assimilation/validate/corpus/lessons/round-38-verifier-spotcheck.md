# Round 38 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
round: 38 (attempt 1) — lane HEAD `870074e8aaf01333c8fe3bdd218eba3a0f2e9a01`, pre-round `95e33de8250ad9da8657d5af03958f4df53165f0`

Judge: hyaku closure seat `closure-chousa-r38`, aided by 5 read-only reviewer seats
(R38Errata, R38Receipts, R38NoHarm, R38Discern, R38Prompt). No gate/counter/verifier was
executed (PROTOCOL §Gate standard, Closure consequence); measurements are byte/hash/jq/git
over committed bytes plus re-opened local sources.

## Dispatch / completion digest (`.ufo/watchdog.log`, mutable — copied per closure contract)

- `2026-10-24T00:03:13-03:00 launch chousa round=38 pgid=1142033 driver=hyaku-inline attempt=1`
- `2026-10-24T01:34:42-03:00 complete chousa round=38; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Verdict | Evidence |
|---|---|---|
| Report committed by lane identity | PASS | `git log --format='%an %H' -- .ufo/reports/round-38/chousa.md` → `chousa-shokunin fd6b25f1f4c759e3551b160a27c2bee374f890ce`; ancestor of `origin/master` (merge-base rc 0) |
| `SHONEN` heading, one line per box | PASS | 4 lines, all `[~]` with pointers; no `[x]` self-attestation |
| Cited lane commits exist + ancestor of branch | PASS | `504c1d2a`, `1f0add70`, `8e93bc91`, `870074e8` all `git merge-base --is-ancestor <h> master` rc 0 |
| Lane repo clean + pushed | PASS | `jj-lane.sh state` → `local=remote=870074e8… ahead=0 behind=0`; `git status --porcelain` empty |
| Prompt carries template contract | PASS | 10/10 items present (mission/axes, L2 floor + hyaku 32–128 swarm with role split, commit-then-push, push scope, L0, report path, lands-last ordering, SHONEN, hash-citation rule, write scope); prompt committed as `chousa-shokunin de3b0d43…`; no L2 route map quoted (routing statement matches MISSION.md host-table rule) |

## Per-claim re-check

### C1 — operability: `ENV_PIN_CAPTURE_MATCH` 2/7 → 7/7 — **verified (re-measured)**

- Own measurement (lane root): `sha256sum tools/research-gate.sh` → `0447ad14…85a` = landed
  bytes. `jq` over `corpus/evidence/round38/receipts/c1-after-{s38001,s38011,s38351}.json`:
  `matched=7`, `predicate_holds=true`, `gate_sha256_pre==gate_sha256_post==0447ad14…`,
  `counter_sha256==6a9600ea…` (=`c1-count.py` measured), `expect_sha256==d34f1735…`
  (=`expectations.jsonl` measured).
- Before: `c1-base-s38001.json` (gate `a7d3922c…` = `.ufo/waves/round-37/controls/base-gate-r37.sh` measured) and `c1-base2-s38003.json` (gate `9fcac047…` = `.ufo/waves/round-38/controls/base-gate-r38.sh` measured): both `matched=2`, `predicate_holds=false`. Both base receipts bind control gates ≠ landed gate, i.e. they refuse the landed gate by binding.
- Seat-observed live runs: `w1/ExecC1Rederive.md` (7/7 vs 2/7, seeds 38211/38231),
  `w2/W2ExecC1Final.md` (7/7 vs 2/7 both controls, seeds 38411/38431, six `VERIFY: ok`) —
  these ran on intermediate revisions (`1f0add70…`/`8e93bc91…`, gate `37e2b996…`).
- Verdict: **met** under the frozen §Erratum 6/13 narrowed reading (function-export
  interposition on the capture's `env` invocation + missing/non-GNU override refusals). The
  falsified general clauses (PATH half, relative-override refusal, positive override
  witness) are each demonstrated by named mutants and pre-registered as the r39 cell family.

### C2 — calibration: `RECEIPT_BINDING_MATCH` 0/7 → 7/7 — **verified (re-measured)**

- Same method on `c2-after-{s38101,s38111,s38371}.json`: `matched=7`, `predicate_holds=true`,
  bindings equal committed bytes (`c2-count.py` `93bf06da…`, gate `0447ad14…`, table
  `d34f1735…`). Base `c2-base-s38101.json`: `matched=0`, `predicate_holds=false` against
  the landed gate — the do-nothing control (r37-counter pipeline) fails on the fixed tree.
- Seat evidence: `w2/W2ExecC2Final.md` (7/7 landed, 0/7 r37-counter control, 7/7 on the r37
  base gate = separability, five `VERIFY: ok`); `w2/W2RevSeparabilityFinal.md`;
  `w2/W2CritLaundering.md` + `w2/W2ScribeKnowledgeC2.md` (the four wave-1 verifier kill
  fixtures refuse by name; verifier weakened in the counter checks is caught at 4/7).
- Reviewer R38Receipts additionally re-implemented every `verify-receipts.py` check
  statically: 9/9 receipts eq-ok on the tip bytes (self-digest, preimages, census, expect
  tie, ok re-derivation, pre==post, strict schema, types).
- Verdict: **met** under the frozen §Erratum 2/10/11 narrowed reading (integrity +
  self-consistency against committed bytes, NOT authorship; `verifier_sha256`/`subject_counter`
  binding carried to r39 and demonstrated live twice).

### Gate selftest / no-harm — **evidence-verified (not executed, per Gate standard)**

- `w2/W2ExecNoHarmFinal.md` observes `RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped)`,
  claims `17/17 CLEAN`, chain `17/22 CLEAN` (5 exempt hops, `drift=0`), broken control DRIFT
  with exactly the two pre-registered sections (`chain`, `sweeps`), archives 3/3 — but at
  revision `8e93bc91…` (gate `37e2b996…`), not the tip.
- Tip transfer: `git diff 8e93bc91 870074e8 -- tools/research-gate.sh` = +6 lines only
  (comment + `unset POSIXLY_CORRECT` between `grep_pin_init` and `env_pin_init`; no selftest
  code, no case-list change) — the 272 PASS at the tip is a sound inference from one hunk,
  recorded as `[INFERENCE]`. The nine tip receipts are the L1's regenerated runs; an
  independent seat-observed counter run on the exact tip bytes exists only in
  `w2/W2MutGateFinal.md` set C (7/7 at seeds 38451/38456).

### Erratum handling per contract — **conformant**

- Frozen-before-data: freeze `504c1d2a` (00:34:21 −03) precedes wave-1 dispatch
  (`w1/swarm-registry.json createdAt 2026-10-24T03:38:41.539Z`); the single post-freeze body
  edit (Erratum 1 bullet, seat-recorded 00:35:55 −03) precedes dispatch and is disclosed.
- Append-only: claims.md numstat `94 0` / `13 0` / `69 0` across the three integrations —
  zero deletions; errata sections are exact prefixes commit-to-commit; no erratum edited in
  place (Erratum 12 corrects Erratum 7 by append).
- Predicates unchanged: the P1 and P2 blocks hash-identical at all four commits; counting
  commands and `matched == 7` conditions untouched.
- expectations.jsonl: exactly one post-freeze edit (`1f0add70`, 6/6, all c2 cells) disclosed
  semantically by Errata 3/4; all 9 tip receipts bind the post-edit table.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 2/7→7/7 measured on both base gates + landed bytes; env pin + override refusal landed; selftest 267→272 |
| calibration | improved | C2 0/7→7/7; receipts bind pre==post + three digests; first in-round self-kills frozen as errata, not absorbed |
| depth | improved | two knowledge entries with mechanism, both delivery mechanisms, kill record, narrowed readings, r39 cells |
| freshness | improved narrowly | r37 knowledge stale wording corrected; S073 supersedes S070's anchor label |
| coverage / adjacency | unchanged | no new measured surface; in-province confirmed (w1/w2 overlap scans, zero network) |

No axis harmed (defect D5 below is a registry-row truncation, routed; it does not touch an
axis score or evidence).

## Discernment spot-check (LEARNING.md — non-author, this file)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S072 admit (bash.info exported functions) | admit | `zcat /usr/share/info/bash.info.gz` lines 1455–1466 + `sha256sum` of the file | agree | quote "Functions may be exported so that child shell processes (those created when executing a separate shell invocation) automatically have them defined" verbatim at decompressed lines 1461–1463; 21 words ≤ 25; file sha matches row; teaches grounds C1's premise; `BASH_FUNC_*` transport honestly left a wave measurement |
| S073 admit (sha256sum(1) anchor-label correction) | admit | `zcat /usr/share/man/man1/sha256sum.1.gz` lines 1–24 | agree | `.SH SYNOPSIS` at 5 (no option entries), `.SH DESCRIPTION` at 8, `-c, --check` is a `.TP` item at 19–20; quote "read checksums from the FILEs and check them" verbatim at line 20, 8 words; `supersedes S070 —` opens teaches; S070 stays mined with valid used-by |
| Reject: second `bash(1)` man-page row | reject (as recorded) | `bash.1.gz` SHELLOPTS paragraph at ~2283; `w1/ScribeSources.md` | **disagree with the record's reason** | the lesson says the rejected candidate was "for the SHELLOPTS paragraph"; the wave evidence (`w1/ScribeSources.md`) rejected `bash.1.gz` *for the same sentence* (S068 holds that file for BASH_ENV). The same-sentence reject is sound; the lesson mischaracterizes the candidate |
| Reject: elided 22-word S072 quote (w1 draft) | reject | bash.info 1461–1464; `w2/W2ScoutFrontier.md` | agree | draft quote carried a `…` elision not present in the source; landed contiguous 21-word fragment is present verbatim |
| Census | — | `sources-census.sh validate --root … chousa` | exit 0 | 73 rows; W04 ×3 (S051/S053 duplicates + expected S073-shared coreutils URL) |

## Trend verdicts

- **expansion: improved** — 71→73 rows; S072/S073 opened this round, enter `mined` citing the
  two new knowledge entries; census exit 0 both ends (re-run here: exit 0).
- **quality: improved** — 7 mistakes mined with class/evidence/captured-by/fix; fixes shown
  able to fail by the wave kills; verifier strengthened twice with regenerated, re-verified
  receipts; my spot-check found the admits sound.
- **discernment: improved** — the lane's first in-round kills of its own frozen claims,
  honestly frozen as Errata 1–13 with predicates' standing receipts distinguished; my two
  disagreements (reject-record wording, Gate URL omission) are routed below for r39 to mine
  into QUALITY.md per LEARNING.md.

## Routed defects for round 39 (lane must fix; none falsifies a claim)

1. **D1 (medium) — frozen candidate-gate hash never superseded in claims.md.** The body
   still names `37e2b996…` as the candidate; the landed gate is `0447ad14…` (+6-line
   POSIXLY_CORRECT hunk at `870074e8`); no erratum names the supersession (SCORECARD/LOG/
   seat reports carry it). Per the lane's own Erratum 6(e) precedent, hash supersessions get
   an erratum.
2. **D2 (low-medium) — counter-harness changes undisclosed in the erratum surface.**
   `base_env()` gained `PYTHON*`/`POSIXLY_CORRECT` scrubs, c2 children run `-E`, timeouts
   raised (`870074e8`); tightening-only, receipts regenerated, but not named by any erratum.
3. **D3 (low) — stale erratum counts.** `LOG.md` says "12 errata"/"§Errata 9–12";
   `SCORECARD.md` says "§Errata 1–12"; claims.md has 13.
4. **D4 (medium) — "final bytes" attribution stale.** SCORECARD/report attach wave-2 seeds
   (38411/38431/38421/38441) and the no-harm battery to the landed bytes; those ran at
   `8e93bc91…`. The tip-byte evidence is the regenerated receipt set (statically verified
   9/9 by this closure) plus the one-hunk diff — label the provenance or re-run on the tip.
5. **D5 (medium) — SKILL.md gates-table row damaged.** The round-37 counters row
   (`SKILL.md:95`) lost its tail during the 267→272 edit: ends `…; no…` (U+2026); the
   `network |` close and the `| chousa |` owner cell are gone. Restore the row from
   `95e33de` + the case-count bump.
6. **D6 (low-medium) — lesson Gate records.** (a) Contract v1 rule 1 requires the URL per
   new row; the Gate records local path only (both SOURCES rows carry the canonical URLs —
   copy them in). (b) Fix the rejected-candidate wording per the spot-check table.
7. **D7 (info) — carried named debt confirmed:** `verifier_sha256`/`subject_counter_sha256`
   unbound (demonstrated live twice); kill rule remains environment-conditioned (Errata 5/6).
   Already named by the lane; closure seconds the r39 priority.

## Admission

Both frozen predicates verify on every committed receipt at the lane tip; the erratum
handling is conformant (frozen-before-data, append-only, predicates unchanged); no axis is
harmed. The lane's requested "ADMIT-with-errata" is granted as **admitted**: the narrowings
are the protocol's append-only correction mechanism applied to prose clauses, while the
measured predicates were only strengthened. Operator ruling request noted; defects D1–D6
ride the routed queue.

Tool installs this closure: none (all checks used installed coreutils/jq/git; no seat
installed anything).
