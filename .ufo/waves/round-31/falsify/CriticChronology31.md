# CriticChronology31 — pre-data chronology of the C1/C2 counters (round 31, WAVE 2 FALSIFY)

Role: UFO-FSD critic. Target: the pre-data rule — no candidate scored before the control receipts
were committed, and design v2 frozen before data. I read committed bytes only, ran no counter
(chronology item; counters frozen), installed no tool, wrote only here and in
`falsify/CriticChronology31/`. Machine-readable inventory of all 761 receipt-shaped rows:
`falsify/CriticChronology31/receipt-inventory.tsv` (family, class, utc, counter_sha256,
gate_sha256, seed, matched, predicate_holds, path).

## Method

`git log --format='%H %cI %s'`, `git show <rev>:<path> | sha256sum`, and every `*.json` under
`.ufo/waves/round-31/` carrying `counter_sha256`+`gate_sha256`+`utc`+`matched` (561 rows), plus
186 rows carrying a counter hash without a `utc` (harness `.output.json` / `-run.json` /
`probe-manifest` wrappers; they inherit their sibling's identity and are excluded from ordering).
Counter and gate identities are taken from hashes, never from receipt prose.

Identity anchors (computed from the commits, not quoted from reports):

| rev | cI (UTC) | c1-count.py | c2-count.py | research-gate.sh |
|---|---|---|---|---|
| d78d1889 v1 frozen | 04:19:59Z | 154e09e7… (C1v1) | 20ed105b… (C2v1) | ac1315dd… base |
| 8070f92b design v2 | 04:37:44Z | c3aca35d… (C1v2) | 1064fdb3… (C2v2) | ac1315dd… base |
| 86188116 control receipts | 04:43:18Z | c3aca35d… | 1064fdb3… | ac1315dd… |
| c17948a7 C1 landed | 04:43:27Z | c3aca35d… | 1064fdb3… | **3b5279eb…** |
| 6d0ae19f C2 landed | 04:43:51Z | c3aca35d… | 1064fdb3… | **c23d7537…** |
| ee1024fd tip | 04:45:09Z | c3aca35d… | 1064fdb3… | c23d7537… |

Worktree hashes now: c1 `c3aca35d…`, c2 `1064fdb3…`, gate `c23d7537…` — counters unchanged since
v2 froze; `git status` clean for `controls/` and `measure/`, so receipt bytes on disk are the
committed bytes.

## Chronology table (C1/C2 counter receipts, grouped; n = receipts binding that identity)

| class | family | counter | gate | n | utc span | max matched |
|---|---|---|---|---|---|---|
| control | CtlBaselineJunk | C1v1/C2v1 | base ac1315dd / scratch | 54 | 04:22:01–04:22:19Z | 58 |
| control | CtlNoReaderC2 | C2v1 | scratch | 5 | 04:22:11–04:22:12Z | 86 |
| control | ChousaR31.CtlShortcutC2 | C2v1 | scratch | 39 | 04:23:11–04:23:44Z | **120** (trim-spaced seed 9002) |
| control | ChousaR31.CriticClaimDesign31 | C1v1/C2v1 | base | 12 | 04:23:29–04:28:05Z | 50 |
| control | MutOracleC1 | C1v1 | scratch | 41 | 04:23:38–04:25:24Z | 120 (oracle, disclosed) |
| control | MutOracleC2 | C2v1 | scratch | 59 | 04:24:05–04:26:14Z | **120** (oracle + trim mutant) |
| control | CtlDeterminism31 | C1v1/C2v1 | scratch | 44 | 04:24:24–04:25:41Z | **120** (truth-fed replay; dup-replay mutant) |
| control | CtlShortcutC1 | C1v1 | scratch | 30 | 04:26:11–04:32:31Z | **120** (`endpoint-exact` ×3, 04:32:30Z) |
| control | CriticClaimDesign31/AxisFit31 | **draft** d201ef4b, ce7f844b, c0a0908c, e26c7751 | base | 20 | 04:27:59–04:30:14Z | 50 |
| control | CtlNoReaderC1 | C1v1 + draft 81fe5015 | scratch | 22 | 04:34:35–04:34:57Z | 90 |
| control | CtlBaselineJunk/v2 | C1v2/C2v2 | base / scratch | 54 | 04:39:24–04:39:37Z | 58 |
| control | CtlNoReaderC1/v2, CtlNoReaderC2/v2 | C1v2/C2v2 | scratch | 12 | 04:38:31–04:38:42Z | 91 |
| control | ChousaR31.CtlShortcutC2/v2 | C2v2 | scratch | 39 | 04:39:12–04:39:15Z | 118 |
| control | MutOracleC1/v2, MutOracleC2/v2 | C1v2/C2v2 | scratch | 63 | 04:39:00–04:40:20Z | 120 (oracle, disclosed) |
| control | CtlShortcutC1/v2 | C1v2 | scratch / base | 40 | 04:40:12–04:40:46Z | 116 |
| **candidate** | measure/ (L1) | C1v2 | C1 landed 3b5279eb | 2 | **04:43:33–04:43:34Z** | 120 |
| **candidate** | measure/ (separability) | C2v2 | C1 landed 3b5279eb | 1 | 04:43:36Z | 50 (expected) |
| **candidate** | measure/ (L1) | C2v2 | C2 landed c23d7537 | 2 | **04:43:53–04:43:54Z** | 120 |
| **candidate** | measure/ (tip re-runs) | C1v2 | C2 landed c23d7537 | 2 | 04:43:56–04:43:58Z | 120 |
| **candidate** | measure/ (separability) | C1v2 / C2v2 | c2only build a2219835 | 2 | 04:44:04–04:44:06Z | 50 / 120 |
| post-data | falsify/* | C1v2/C2v2 | landed gates, scratch, candidates | 218 | 04:47:21–05:05:41Z | 120 |

## Verdict on the rule itself: holds

1. **First candidate-data receipt is after both anchors.** Earliest row binding a landed-candidate
   gate is `measure/after-c1-run1.json`, utc **04:43:33Z**, gate `3b5279eb…` = the gate committed at
   c17948a7 (**04:43:27Z**). It follows 8070f92b (04:37:44Z) by 5 m 49 s and 86188116 (04:43:18Z)
   by 15 s. C2's first is `measure/after-c2-run1.json` 04:43:53Z vs 6d0ae19f 04:43:51Z and
   86188116 04:43:18Z. Margins are thin (15 s / 35 s) but the order is unambiguous in the
   committer dates *and* in the gate hashes (a pre-landing run cannot bind 3b5279eb/c23d7537).
2. **No candidate was scored earlier under another identity.** The build-wave candidate gates
   `6c581ccf…` (ExecC1Impl) and `41b294fd…` (ExecC2Impl) first appear only in the falsify wave —
   04:52:08Z and 04:54:21Z — i.e. post-data. No pre-v2 receipt binds any candidate gate.
3. **Order inside the control wave is correct.** v1 controls 04:22–04:35Z → design v2 commit
   04:37:44Z → v2 re-scores 04:38:31–04:40:46Z → control-receipts commit 04:43:18Z → candidate
   data 04:43:33Z. No v2-hash receipt predates 8070f92b; none of the 561 timestamped rows falls
   outside its own revision's window.
4. **The disclosed lane-gate window left no receipt trace, so no committed measurement is
   contaminated.** Zero rows have a utc in 04:26:19–04:26:45.9Z. The lane-gate rows bracketing it
   are 04:26:11Z and 04:27:59Z, both `ac1315dd…` (base) — corroborating the disclosed restore.
   Every pre-landing lane-gate row in the tree is `ac1315dd…`; the first non-base lane-gate hash
   is 3b5279eb at 04:43:33Z.

## Findings (all fixable; none voids P1/P2 on the committed bytes)

**F1 (material) — the "every control re-scored under v2" sentence is false for CtlDeterminism31.**
claims.md Disclosures (c) states "every control is re-scored under v2 before any candidate is
scored." Committed evidence: 7 of 10 `controls/` families have a `v2/` directory; **CtlDeterminism31
has none** — its 98 receipts all bind v1 hashes (49 × 154e09e7, 49 × 20ed105b). This is the one
family whose v1 rows reach the predicate on *both* counters: `c1-exit0-external-truth-replay.json`
and `c2-…` (matched 120, predicate_holds true, 04:24:45Z), `c1-duplicate-replay-mutated/restored`
and c2 twins (120, 04:25:32/41Z). Its own report declares the truth-fed replay "not an admissible
source-skipping control", but claims.md never carries that exclusion, and v2 item 4 was itself
derived from this family's findings (harness errors exit 2; duplicate id → `none`) — a rule change
that makes its earlier 120/120 duplicate-replay rows non-transferable. Under v2 those rows were
never re-measured. Impacted: pre-data completeness of the control wave (operability of the
negative claim "no control met either counter"). Smallest safe correction: either add
`controls/CtlDeterminism31/v2/` receipts for both counters, or narrow (c) to "every control except
CtlDeterminism31's inadmissible truth-fed/duplicate stubs, excluded as follows: …" and record the
exclusion in claims.md.

**F2 (material) — a contract-conformant implementation reached each predicate pre-v2, and
claims.md does not say so.** Disclosures (a) records that CriticSeparability31 "built its own
scratch C1 and C2 sketches and ran the v1 counters on them at 04:26-04:28Z" but omits the result:
its report (`build/CriticSeparability31.md` §2) records the C1-only build at **120/120** (seeds 1
and 2) and the C2-only build at **120/120**, at ~04:26–04:28Z, i.e. before 8070f92b (04:37:44Z).
The design's oracle rule requires a full-contract oracle hitting 120/120 to be "disclosed as a
reference"; MutOracle's 120/120 is disclosed in claims.md item 1, this one is not. The transcript
(`history://ChousaR31.CriticSeparability31`) shows the counter invocations
(`python3 v1/corpus/evidence/round31/c1-count.py …`) against scratch clones of d78d1889, so the
run is established, not inferred. Impacted: the honesty of "no data before freeze" — a 120/120 is
the most consequential pre-freeze result and it is stated only in a build report. Smallest safe
correction: extend Disclosures (a) with the two 120/120 results and the note that they are
one-sided scratch probes, not round-31 candidates.

**F3 (material) — an undisclosed predicate-value control hit before v2.**
`controls/CtlShortcutC1/endpoint-exact-seed9310{11,12,13}.json` score **120/120** (counter
154e09e7 = v1, gate d1193ff5 scratch, predicate_holds true) at **04:32:30–04:32:31Z**, before v2
froze. Under v2 the same control falls to 112/120 (`…/v2/endpoint-exact-seed9340{11,12,13}`), so
the leak *was* closed — the 8070f92b subject even says "endpoint/start-only leaks closed". But
claims.md item 1 narrates the leak as a "**C2** sub-variant leak" and names only C2 instances
(CtlShortcutC2 trim-spaced 120/120 seed 9002, 04:23:14Z; MutOracleC2 trim mutant 120/120). A C1
shortcut met the C1 counter at the predicate value on three seeds and is named nowhere in
claims.md. Impacted: the accuracy of the v2 rationale. Smallest safe correction: rename item 1 to
cover both counters and cite the three `endpoint-exact` receipts.

**F4 (minor) — the disclosed 84/120 run is unreceipted and therefore unauditable.** Disclosures
(b) asserts the L1 ran an uncommitted v2 draft of c1-count.py (seed 1) on the lane gate and saw
84/120. No row anywhere in the lane has a utc in the disclosed window 04:26:19–04:26:45.9Z, and no
row binds the lane gate to any non-`ac1315dd` hash before 04:43:33Z; the nearest rows are
`MutOracleC2/bash-cat-restored-*` at 04:26:14Z, and those are a scratch gate (`96d63bcd…`). The
second half of the sentence ("the same counter on the base gate prints 50/120") *is* supported —
the draft counter `d201ef4b…` on the base gate scores 50/120 in
`ChousaR31.CriticAxisFit31/working-v2-c1-seed31/32.json` at 04:27:59–04:28:01Z. So one clause of
a disclosure that justifies the whole measurement protocol (gate SHA-256 checked before each run)
has no `counter_sha256` and no `gate_sha256` behind it. Impacted: auditability, not the predicate.
Smallest safe correction: state in (b) that no receipt exists for the 84/120 observation and cite
the two 50/120 draft receipts as the only committed evidence.

**F5 (minor) — three receipt families name counter bytes that exist nowhere in the tree.** 20
receipts under `controls/ChousaR31.CriticClaimDesign31/` and `…/CriticAxisFit31/`, plus 11 under
`CtlNoReaderC1/`, carry draft hashes `d201ef4b…`, `ce7f844b…`, `c0a0908c…`, `e26c7751…`,
`81fe5015…`; none is any committed revision of either counter. Disclosure (c) covers this
generically ("the counters were edited in the working tree during the control wave") but not the
count of distinct uncommitted identities. All such rows are ≤ 91/120 and bind the base gate, so
none affects the "no control met the counter" claim. Smallest safe correction: name the five draft
hashes in (c) and note that none is reproducible.

## Limits

- Read-only on the lane: no git/jj writes, no counter executed (the counters are frozen; re-running
  was not needed to establish ordering and would have added a post-data row).
- The 186 timestamp-less wrapper rows are excluded from the ordering; they inherit identity from
  the sibling receipt they wrap, and none introduces a gate hash absent from the timestamped set.
- Committer dates, not dates of file content, are the ordering evidence; a forged/clock-skewed
  committer date is out of scope of these bytes. Hashes make the *content* ordering
  (base → 3b5279eb → c23d7537) independent of the clock.
- `.ufo/waves/round-31/falsify/` is untracked at the lane tip, so falsify-wave receipts (218 rows,
  04:47–05:05Z) are worktree-only as of this read; they are post-data and irrelevant to the rule.
- No network was used; no tool was installed or updated.

## Verdict

The pre-data rule holds on the committed bytes: the first candidate-data receipt (04:43:33Z) is
after the design-v2 commit (04:37:44Z) and after the control-receipts commit (04:43:18Z), and no
candidate gate was scored under any earlier identity. The rule's *supporting narrative* is
defective in three places worth fixing before a verifier relies on it: F1 (an un-re-scored control
family stated as re-scored), F2/F3 (a 120/120 pre-freeze result and a 120/120 pre-v2 control hit
not disclosed in claims.md), F4/F5 (an unreceipted exception and unreproducible draft identities).
