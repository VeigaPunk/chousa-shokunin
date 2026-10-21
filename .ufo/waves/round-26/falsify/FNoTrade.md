# FNoTrade — round 26 no-harm claim, six axes (critic, calibration)

Seat `ChousaR26R.FNoTrade`, leaf member. This is author-lane advice only: no
outside-judge verdict, no SHONEN claim, and no subagents dispatched.

## Verdict

**The no-harm claim is FALSIFIED at the measured revision `0e9784bd`.** The
target's own `--selftest` fails deterministically: `RESEARCH_GATE_SELFTEST:
FAIL (3/187 cases)`, exit 1. Base `ba333325` gives `PASS (161 cases, 0
skipped)`, exit 0. The pre-registration requires that "Every landed state must
hold: selftest PASS with cases 1–161 identical"
(`corpus/evidence/round26-claims.md:122`). The "cases 1–161 identical" half
holds, because `LEGACY_CASES_SHA=5eac4a7e…` matches base. The "PASS" half fails.

The registered counting probe still exits 0 and prints
`RESEARCH_GATE_SELFTEST: FAIL (3/187 cases)` in its hold section. That
supports the round's own qualification: probe exit 0 is completion, not a
verdict.

Every other registered prediction reproduces at `0e9784bd`:

- `C1_AMPLIFIED=0/4`, with frozen hash/rc unchanged.
- `FRESHNESS_CLASSIFIED=29/29`, `C2_ORACLE_AGREE=29/29`, `C2_CONTROLS_CAUGHT=6/6`.
- `C3_CONTROLS_CAUGHT=5/5`, `C3_POSITIVE_CLEAN=1/1`, `C3_POP_R24PLUS_CLEAN=5/5`.
- Drift `none` and r1 `3/3`.

So the selftest is the one hold that is missing. Outside it, I found no
regression on any existing observable.

The new opt-in `--registry` mode repeats the R26-M1 allocation class inside
this round's own new reader, which is fresh finding F2. That is a calibration
and scope defect in how the mode is described. It is not a harm to an existing
mode.

**Operability score: 3/10, delta 0.** I re-derived it on base and target.
I make no field-readiness inference. Neither C2 nor C3 is read as a claim of
semantic support or truth.

## Target identity

- Revision `0e9784bd52eca456b24d0bc40921480a47f91a2b`, from the lane working
  copy `corpus/evidence/round26-measured-revision.json`. That file is not in
  the commit and its phase is "integrated final run not yet performed". Lane
  `HEAD` equalled it.
- Gate digest: `git show 0e9784bd:tools/research-gate.sh | sha256sum` gives
  `c2c813f1…abc6`. That equals the lane working tree and my sandbox
  (QUALITY 15 holds).
- Sandbox: `git archive` of the target into
  `/tmp/chousa-r26-falsify-FNoTrade/tree` and of the base into `.../base`.
  For the r1 sibling layout I made a byte-identical copy of
  `research/deep-research-2026-09-28/{A,B,C}` (sha256 equal to the fleet
  originals).
- Environment: Linux, 32 CPU, 31 GiB RAM. RSS was taken from Python
  `resource.getrusage(RUSAGE_CHILDREN).ru_maxrss` because `/usr/bin/time` and
  `bc` are absent.
- Tools installed or updated: **none**. Python substituted for the absent
  `time`/`bc`, so no install was needed.
- Every `path:line` cited below is pinned to the `0e9784bd` blobs in the
  sandbox. The lane working copy has since modified
  `corpus/lessons/round-26.md` (uncommitted, not by this seat), so its live
  line numbers may differ.

## Six axes — no-trade audit

| axis | claim/hold | observation at `0e9784bd` | no-harm? |
|---|---|---|---|
| operability | C1 and holds | C1 0/4 bounded at 8,388,000 B (probe). Frozen29 plain hash `3f83ba48…` rc1 equals base. **Selftest FAIL 3/187, exit 1** (base PASS 161) | **harmed hold** (F1) |
| freshness | C2 | 29/29, 29/29, 6/6. Independent edge sweep matches Python `date` on 18 cases. Drift `none` | no harm found |
| calibration | C3 | 5/5, 1/1, 5/5 within spec v1. The "bounded" wording on the new registry reader is contradicted (F2), and owner pointers dangle (F4a) | no existing observable harmed. Record-level inconsistencies cited below |
| depth | not claimed | 3 new entries. Limits sections present and accurate where tested | unchanged, unscored |
| coverage | not claimed | indexed at `corpus/README.md:62-66`, no domain fraction invented | unchanged, unscored |
| adjacency | not claimed | Cochrane, Python and PROV are used inside row scope. The lane-policy inference is labelled (`recheck-due-r26.md`, `registry-link-r26.md`) | unchanged |

### Plain-mode identity (operability and calibration hold), all base-vs-target equal after dropping the timestamp line

- Frozen 29 from the base objects: rc1 and sha `3f83ba48…`, matching the
  receipt.
- Target `corpus/knowledge`, 32 entries, `--root .`: rc1, sha `9b566cb3…`,
  67 lines, byte-identical.
- `corpus/fixtures/metadata-r25/*`: 27/27 identical, 0 differ.
- My four adversarial fixture directories (`c2x` 18, `c3x` 19, `mid` 7,
  `scale` 9 entries): all identical.

### Resource parity (operability hold "no slower or less bounded mode")

**1,000,000-byte shapes (independent of the probe), base → target:**

| shape | RSS KiB, base → target | time, base → target | output sha |
|---|---|---|---|
| newline | 271,544 → 16,232 | 10.55 → 10.34 s | equal |
| header-body | 138,616 → 16,228 | 1.38 → 0.02 s | equal |
| CRLF | 139,368 → 16,220 | 5.31 → 5.18 s | equal |
| header without heading | 138,184 → 16,232 | 7.18 → 7.39 s | equal |
| single long line | 16,156 → 15,448 | 2.09 → 1.82 s | equal |
| 250k-line `verified-at:` continuation | 72,228 → 16,232 | 4.61 → 4.69 s | equal |

**Continuation and headerless scaling at 50k/100k/200k bytes:** linear
(0.21/0.42/0.84 s) and equal on both trees.

**8 MiB probe, base receipt → target:**

| shape | time, base → target |
|---|---|
| s1 | 90.6 → 86.4 s |
| s2 | 11.7 → 0.1 s |
| s3 | 45.7 → 44.2 s |
| s4 | 63.6 → 62.6 s |

No slowdown. The retained time risk disclosed at `SKILL.md:493-497`
(headerless input takes about 86 s at the cap) is accurate and is not new.

## Findings

### F1 — selftest FAIL at the immutable target (fresh; decisive for no-harm)

- Observed three times: during concurrent load, inside
  `round26-measure.sh … all`, and in an isolated rerun. Each time it printed
  `RESEARCH_GATE_SELFTEST: FAIL (3/187 cases)` with exit 1.
- The failing cases are `metadata-asof-invalid`, `metadata-asof-missing` and
  `metadata-asof-wrong-mode`.
- The gate behaviour is correct. For example, `--as-of 2026-02-30` gives rc 2
  with `--as-of must be a valid YYYY-MM-DD date`.
- Root cause is in the test harness. `tools/research-gate.sh:6016` requires
  `$out != *'RESEARCH_GATE: '*`. But `die_usage` (`:390`) always prints
  `usage`, which contains the line `Verdict: RESEARCH_GATE: CLEAN|DRIFT`
  (`:385`). So the predicate is unsatisfiable for any usage exit, and the
  failure is deterministic rather than flaky.
- [INFERENCE] An anchored check such as `grep -c '^RESEARCH_GATE: '`, the form
  the other mode harnesses use, would distinguish a verdict from the usage text.
- Why it went unseen: `LOG.md:1006-1008` records that the C2/C3 identities
  "intentionally ran no further checks". `LOG.md:1031` reserves no-harm
  verdicts for the integrated run. No record claims PASS for `0e9784bd`, so
  this is a missed hold, not a false PASS claim.
- Consequence: the landed shared `--selftest` command (described at
  `SKILL.md:474-476` as unchanged) now exits 1. Any hold battery that keys on
  the selftest exit will go red.
- Not reported by any sibling: I checked the falsify reports in this
  directory with a text search for `3/187` and `selftest.*FAIL`.

### F2 — registry reader amplifies allocation on pipe-dense input (fresh)

`metadata_registry_load` (`tools/research-gate.sh:2361-2470`) splits every
table-shaped line into a per-line `cells` array and trims each cell. The input
is a registry whose header is valid, followed by one long line of `|` runs.
The test is `verify-metadata corpus/knowledge/a.md --root . --registry R`.

| registry bytes | peak RSS KiB | elapsed |
|---|---|---|
| 81 (control) | 12,152 | 0.01 s |
| 1,000,000 | 273,852 | 4.71 s |
| 2,097,152 | 566,604 | 19.19 s |
| 4,194,304 | 1,131,464 | 75.68 s |

- That is about 270 bytes of RSS per input byte, linear. Time grows about ×4
  per doubling (quadratic).
- [INFERENCE, not run] At the 8 MiB cap: roughly 2.2 GiB and about 300 s.
  That is the same order as the base entry reader that R26-M1 fixed.
- Controls that stayed bounded:
  - A row-dense registry of about 40k unique ids in 1 MB: 16,108 KiB, 1.55 s.
  - 1 MB of blank lines before the header: 12,164 KiB, 3.43 s.
- `CORPUS.md` forbids `|` inside any cell, so this input is contract-invalid.
  The reader still accepts it and spends the memory before rejecting
  nothing.
- **Calibration conflict:**
  - `LOG.md:1013` says "C3 adds a bounded fd-snapshot registry reader".
  - The gate help at `tools/research-gate.sh:322` says "checks source S-ids
    against a bounded SOURCES.md table".
  - QUALITY 18 (this round's own criterion) requires naming the unit and
    exercising dense shapes before calling a reader bounded.
  - The closure routing (`MANIFEST.json rounds[395].routed_defects[0]`) says
    "do not advertise generally resource-bounded parsing".
- `SKILL.md:495-497` scopes the RSS result to "the four-shape" entry reader
  and says "other gate readers are not repaired". But the registry reader is
  new this round, not an "other" pre-existing reader.
- This is not a harm to an existing mode, because `--registry` is opt-in and
  new. It is an unexercised resource claim.

### F3 — corroborated, not original (siblings own them)

- **Quadratic `source:` id scan under `--registry`.** The cause is the
  `source_scan=${source_scan#*"$source_match"}` copy per id. Owned by
  `FRegistryIdWidth.md` F2 and `FOverlap.md`. My independent timings for
  `S001 ` × k ids were:

  | ids | time |
  |---|---|
  | 2,000 | 0.11 s |
  | 4,000 | 0.26 s |
  | 8,000 | 0.69 s |
  | 16,000 | 2.16 s |
  | 32,000 | 7.60 s |
  | 64,000 | 26.69 s (71,020 KiB) |

  Plain mode stays at 0.03 s. Each occurrence emits its own finding
  (64,000 findings for one distinct id).
- **Fenced example table shadows the real registry.** Owned by
  `FRegistryHeaderless.md` R26-FRH-4. I reproduced it: a fenced table that
  lists `S100` is loaded as the registry. Every real row then reports
  `META_SOURCE_ROW_MISSING`, while the fenced `S100` entry comes back clean.
  The live `corpus/SOURCES.md` has no fence, so the defect is latent for the
  current corpus.
- **Escaped `\|` cell shifts columns.** This is contract-invalid input. My
  queued-row attempt failed closed (`META_SOURCE_NOT_MINED`). Under the
  11-column schema a false pass needs a path in a shifted status or used-by
  column, which no realistic row has.

### F4 — exact record inconsistencies (calibration)

**a. Dangling owner pointers.** At `0e9784bd`, `SCORECARD.md` has no Round26
section. Its only round-26 heading is `SCORECARD.md:1371` `## Planned — round
26 (not started)`. Yet several files name that section as owner:

- `SKILL.md:476`
- `corpus/README.md:62-66` and `:865`
- `corpus/knowledge/reader-allocation-r26.md:39-40`
- the `verified-at:` lines of `corpus/knowledge/recheck-due-r26.md:2` and
  `registry-link-r26.md:2`

`LOG.md:1031` discloses this as pending, so it is not a false number. Under
QUALITY 9/11, though, the landing must create that owner. It must also
replace the "(not started)" heading and carry plan item 1's disposition into
`SCORECARD.md`. Otherwise five records point at nothing.

**b. "Original command" attribution.** `corpus/lessons/round-26.md:24` says
the operability score was "re-derived by its original command this round",
citing `round26-measure-before.log` (3/3). The receipt actually comes from the
probe's `holds()` variant (`corpus/evidence/round26-measure.sh`, `holds`),
which uses an absolute `$FLEET/research/...` and `--root $FLEET`. The original
command at `SCORECARD.md:29` uses `../research/...` with `--root ..`.

The values agree. I measured both forms and got 3/3 on base and 3/3 on target
in the sibling layout. The original form returns `0/3` with rc 2 "record not
found" in a clone without `../research`, which is the QUALITY 13 layout
dependence. The score stands; the provenance wording is inexact.

**c. Debt-pointer attribution for the appender race.**
`corpus/lessons/round-26.md:23` says the "round25 lesson and hardening ledger
keep their debt pointers". `corpus/knowledge/hardening-r10.md` has no
concurrency or appender-race row. A search for `append|flock|concurren|race`
hits only row 36 (append-only discipline, by-design) and the
"append-only" errata headings. The race's actual pointers are:

- `corpus/lessons/round-25.md:20,31`
- `corpus/knowledge/json-delimiter-r24.md:66-71`
- `corpus/evidence/json-r24-20261019T213117Z-demo.log:26-29`
- `.ufo/waves/round-25/build/ExecAppendRace.md:8-9,24`
- `LOG.md:866-868`

The hardening ledger does own the TOCTOU/filesystem-race residuals
(`:478-482`) and source/span pairing (row 56). So the sentence is right for
those and wrong for the appender race.

**d. Two values for one before-observation.**

- `corpus/evidence/round26-claims.md:30-31`: 2,240,704 KiB in 86.9 s, control
  11,888 KiB, labelled as an L1 probe.
- `corpus/lessons/round-26.md:20` and `reader-allocation-r26.md:11-12`:
  2,238,736 KiB, control 11,644 KiB, which is the receipt.

These are different runs, and both are within the amplified verdict. Low
severity, but under QUALITY 9 the receipt should be named as the owning value.

**e. S038 version drift.** The row anchors "Python3.15.0 documentation served
2026-10-21". The live page fetched today serves **Python 3.15.1**, so the
row's `on-release` recheck has fired. The located `date.toordinal` sentence,
MINYEAR and MAXYEAR are still present. The S037 quote is on p19 in §4.3.4
(Version December 2019), and the S039 sentence is present in the tag-stripped
HTML. No support or truth claim is made from the opened text beyond row
scope.

## Audit: prior routed risk (`MANIFEST.json rounds[395].routed_defects`)

1. **Reader byte cap is not a memory budget.** Exercised (before 4/4
   amplified) and repaired for the metadata entry reader (after 0/4; my 1 MB
   six-shape sweep agrees, with output identical and time parity). The
   closure's instruction "do not advertise generally resource-bounded
   parsing" is honoured for the entry reader (`SKILL.md:493-498`). It is
   breached in wording for the new registry reader (F2).
2. **Battery comment says 154 cases.** Disposed by the append-only comment at
   `corpus/evidence/round25-holds/battery.sh:93-96`, with no history
   rewritten. The battery itself compares only `ok-case` 1–136 plus the exit
   code. [INFERENCE] At the target the exit code becomes 1 because of F1, so
   the r25 battery would also report a selftest mismatch.
3. **Probe exit 0 is completion; carried debts preserved.** Confirmed. The
   probe exited 0 while its own hold printed FAIL (F1).

## Audit: carried concurrent-appender race disposition

- **Consistent counts, not pooled:**
  - r24: 1/3 sixteen-writer runs blank (`json-r24-…-demo.log:29`).
  - r25: 2/6 seeded runs, 0/6 empty controls (`ExecAppendRace.md:8-9`,
    `LOG.md:866-868`, `lessons/round-25.md:20`).
- **Not silently repaired or regressed.** The `--json` append window is
  byte-identical: base `tools/research-gate.sh:2700-2760` equals target
  `:2985-3045`, covering the `tail -c1 | od` probe and the unlocked `>>`
  append. `verify_all()` is byte-identical too. The `flock` candidate stays
  unlanded (`.ufo/waves/round-25/build/unlanded-append-race.patch`).
- **Disposition placement.** "Not claimed; same axis as the routed risk" is
  recorded at `round26-claims.md:15-19`, `LOG.md:971-973`,
  `lessons/round-26.md:6-8,23` and `corpus/README.md:873`. The owning planned
  list `SCORECARD.md:1373-1376` still reads as an unstarted round-26 item
  with no disposition line (QUALITY 11), pending landing (see F4a).
- **Exact inconsistency:** F4c, where the hardening ledger is credited with a
  pointer it does not hold.
- I did not re-run the race this round. That is accurate disclosure, not debt
  closure.

## Calibration limits of this report

- F2's 8 MiB figures are extrapolated from 1, 2 and 4 MiB measurements and
  marked [INFERENCE].
- All other numbers are observed in this seat's sandbox.
- "No harm found" on freshness and calibration is scoped to the observables I
  ran. It is not a proof of absence.
- I did not judge semantic source support beyond quote presence (QUALITY 8).
- The lane's sibling reports were read only to de-duplicate findings. None of
  their results is relied on for F1, F2 or the holds.
