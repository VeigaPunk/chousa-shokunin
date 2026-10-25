# ExecC2Count — frozen round-40 `c2-count.py` on the committed tree

Seat: leaf executor (L2). Date: 2026-10-24. Lane tip under test: `6bc90e04ac60307befacd554f7eee2b7284e2652`.
Production edits: none. Writes: this file only. Tool installs: none (no pacman transaction).

## 1. Assigned attack

Run the frozen round-40 `c2-count.py` command on the committed tree and confirm its four
source-derived R2–R5 dispositions and exit code. Claim binding: C2 / P2 —
`R39_CALIBRATION_DISPOSITIONS=4/4`, exit 0, "not prose labels alone".

## 2. Exact command and output (verbatim)

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c2-count.py; echo "EXIT=$?"
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
EXIT=0
```

Matches the committed after-measurement (`corpus/evidence/round40/measure-after.txt`, C2 block, `C2_AFTER_EXIT=0`).

## 3. Committed-tree identity (the counter reads the working tree, so this was proved separately)

| Check | Result |
|---|---|
| `git rev-parse HEAD` | `6bc90e04ac60307befacd554f7eee2b7284e2652` |
| `git diff --stat HEAD -- <all 8 counter inputs>` | empty — working tree == HEAD |
| `git ls-files --error-unmatch` on each input | 8/8 TRACKED (incl. `c1-mutenv-s39003.json`) |
| sole dirty path in lane | `.ufo/waves/round-40/w1/swarm-registry.json` (not read by the counter) |

The counter's inputs are therefore the committed bytes, not uncommitted drafts. Input sha256
(stable before and after every run — see §7): `c2-count.py` `b0da3915…`, dispositions
`b8569060…`, r39 claims `cee81998…`, r39 lesson `35d8cb87…`, SCORECARD `4ee5256e…`, spot-check
`d67dd681…`, r39 spec `6f6b1fbb…`, r39 plan `172f35e2…`, r39 report `01bbed5f…`.

## 4. Independent re-derivation of the four dispositions

Each row is what the counter asserts, then what I measured directly from the committed bytes.

| D | Status | Counter's derivation | Independent measurement | Verdict |
|---|---|---|---|---|
| R2 | corrected | `git ls-files` tracks the receipt **and** the file exists; r39 lesson says "not committed"; r39 claims contain `R2`, the receipt path, `superseded` | receipt tracked + present (190 lines, 6213 B); r39 claims:197 states it *is* committed and is a superseded draft; lesson carries the contradictory "not committed" wording | confirmed |
| R3 | corrected | `git ls-tree -r BASE39/TIP39 -- corpus/knowledge` counts must be **50/52**; r39 report must still carry `29 → 31`; r39 claims must carry `29 → 31` and `50 → 52` | re-ran both `ls-tree` counts: `8c7c867 → 50`, `6ac1007 → 52`; report:132 carries `29 → 31` (stale, preserved); claims:198 carries both numbers | confirmed |
| R4 | not-reproduced | spec `items[].role` Counter == plan `tasks[].agent` Counter, `reviewer==6`, `revenger==2`; report contains `reviewer 6 / critic 5` and `revenger 2`; spot-check contains `reviewer 8 / revenger 0` | parsed both JSONs: 32 rows each, identical 10-role distribution, reviewer 6 / revenger 2; report:168-170 states the same mix and 32 seats; spot-check:74 states the contradictory `reviewer 8 / revenger 0` | confirmed — see §5 |
| R5 | corrected | 4 whole-file substring hits (`two independent runners`, `R5`, `two seeds` in SCORECARD; `L1's construction runs` in **r39** claims) + disposition label | r39 claims:3-5 discloses "the L1's construction runs on seeds 39001/39011 (C1) and 39101 (C2)"; SCORECARD:2234 still carries the stale phrase; SCORECARD:2255-2260 appends the correction | confirmed, with a calibration qualification — see §6 W1 |

Note on R5's reading scope: `freeze_discloses_l1` reads **r39** `claims.md`, not round-40
`claims.md`. That is correct — the disclosure ("frozen before the prepared wave's independent
runs") lives in the r39 frozen body at line 5, which is exactly what the disposition cites
(`claims.md:3-5`). Round-40 claims contain no such sentence and are not consulted.

## 5. R4, the only conditional disposition ("not-reproduced **only if**")

The binding requires the committed spec, validator plan, and report to agree *against* the
spot-check. All three agree, and the spot-check is contradicted by the very bytes it cites:

| Artifact | reviewer | revenger | total |
|---|---|---|---|
| `w1-spec.json` at spot-check commit `691d264` | 6 | 2 | 32 |
| `w1-plan.json` at spot-check commit `691d264` | 6 | 2 | 32 |
| `w1-spec.json` / `w1-plan.json` at HEAD `6bc90e0` | 6 / 6 | 2 / 2 | 32 / 32 |
| fleet r39 report:168-170 | 6 | 2 | 32 |
| spot-check:74 ("the validated spec") | 8 | 0 | 32 |

`git log -- .ufo/waves/round-39/w1-spec.json .ufo/waves/round-39/w1-plan.json` returns a single
commit (`6d914e9`): the spec and plan were never modified after creation. There is no
intervening change that could explain 8/0, so the spot-check misstated the artifact it claims
to have validated. `not-reproduced` is the only disposition the committed evidence supports,
and no source artifact was rewritten to make it so. Confirmed.

## 6. Calibration: do the four cells actually depend on their sources?

Run in a throwaway `git clone --shared` at `/tmp/c2audit/lane` (lane repo read-only, lane index
and jj state untouched; the clone is disposable). One mutation per row, `git reset --hard`
plus re-copying the out-of-repo fleet report between rows.

| Mutant | Intended break | rc | Cells failing |
|---|---|---|---|
| baseline | — | 0 | none (4/4) |
| M1 dispositions `R4.status → corrected` | R4 | 1 | R4 |
| M2 spot-check `reviewer 8 / revenger 0 → …2` | R4 | 1 | R4 |
| M3 fleet report `29 → 31` corrupted | R3 | 1 | R3 |
| M8 r39 claims `50 → 52` corrupted | R3 | 1 | R3 |
| M9 plan `reviewer → revenger` | R4 | 1 | R4 |
| M4 superseded receipt `git rm`'d | R2 | 1 | R2 |
| N5 receipt path in r39 claims renamed | R2 | 1 | R2 |
| N2 every `two seeds` purged from SCORECARD | R5 | 1 | R5 |
| N4 every `not committed` purged from lesson | R2 | 1 | R2 |
| M6 disposition record deleted | all | 1 | R2,R3,R4,R5 (0/4) |
| **N1** round-40 R5 correction bullet deleted | R5 | **0** | **none (4/4)** |
| **N3** receipt-adjacent "not committed" flipped | R2 | **0** | **none (4/4)** |
| **M7** all 14 `evidence` pointers falsified | pointers | **0** | **none (4/4)** |
| **N6** all `evidence` arrays deleted | pointers | **0** | **none (4/4)** |

Do-nothing control re-derived independently: frozen counter applied to the pre-correction tree
`691d264` (where `corpus/evidence/round40/` contains no files) →

```
R2_DISPOSITION=missing-or-unverified
R3_DISPOSITION=missing-or-unverified
R4_DISPOSITION=missing-or-unverified
R5_DISPOSITION=missing-or-unverified
R39_CALIBRATION_DISPOSITIONS=0/4
CONTROL_EXIT=1
```

byte-consistent with `.ufo/waves/round-40/controls/control-before.txt:20-25` (0/4, `C2_EXIT=1`).
So the 0 → 4 movement is real and every cell except R5 is source-coupled.

### Residual weaknesses (none of these contradict P2's formal predicate; all are next-round hardening)

- **W1 (R5, material).** All five R5 conjuncts are labels; there is no derived measurement.
  Deleting the *entire* round-40 R5 correction bullet still yields 4/4 exit 0 (N1) because
  each SCORECARD substring is satisfied elsewhere — `two independent runners` at line 2234,
  `R5` at line 2054 (`R5 selftest cases`), `two seeds` at lines 1818/2234. A correction bullet
  saying anything (or nothing) passes. R5's "corrected" is effectively self-declared by the
  disposition record. Suggested hardening: require the exact correction text
  (`two seeds, both L1 construction runs`) inside the round-40 SCORECARD section.
- **W2 (R2, minor).** `"not committed" in lesson` is not receipt-scoped. Flipping the
  receipt-adjacent wording at lesson:27 still passes (N3) because the unrelated line 25
  (`/tmp/chousa-r39-c2.log — not committed`) satisfies it. The claims-side path anchor is
  the real coupling (N5 fails). Suggested: require the receipt path adjacent to the phrase.
- **W3 (pointer integrity, minor).** The 14 `evidence` pointers are never dereferenced
  (M7, N6 pass). Independently, 13/14 resolve to existing paths at valid line ranges; the
  14th is a section anchor (`SCORECARD.md:## Round 40 — closure corrections to r39 (R2–R5)`,
  heading present at line 2255) and is valid only by heading lookup, not machine-checked.
  R3's evidence list also cites `c2-count.py` itself (self-reference) rather than the derived
  count — harmless, since the counter recomputes the counts via `git ls-tree`.
- **W4 (control wording, precision).** Claims §C2 "Before" says the command was run "at lane
  tip `691d264`"; that tree has **no** `corpus/evidence/round40/` (0 files). `c2-count.py` was
  introduced later, at `6c01a41`. The recorded output reproduces exactly when the frozen
  counter is applied to the `691d264` tree, so the control is valid — only the phrasing
  ("at lane tip" implies the script was in the tree). Suggested wording: "frozen counter applied
  to the tree at 691d264".

## 7. Operability

| Probe | Result |
|---|---|
| cwd independence (`python3 /abs/…/c2-count.py` from `/tmp`) | 4/4, exit 0 — all paths resolve via `__file__` |
| determinism (3 consecutive lane runs) | identical output, `md5 61c0e9e13a11bdaa4a758e969aee52c3` |
| read-only | sha256 of all 9 inputs identical before/after; no repo mutation |
| missing fleet report (`../.ufo/reports/round-39/chousa.md`) | `R39_CORRECTION_COUNTER_ERROR=[Errno 2] …`, **exit 2** |
| corrupt r39 spec JSON | `R39_CORRECTION_COUNTER_ERROR=Expecting property name…`, **exit 2** |
| unresolvable git revision | `R39_CORRECTION_COUNTER_ERROR=fatal: not a tree object`, **exit 2** |

Error discipline is clean: 0 = all four, 1 = below four, 2 = unreadable/unparseable input
(messages on stderr, no traceback). Portability caveat: the counter is **not self-contained
in the lane repo** — it reads the fleet report outside `ROOT`, so a lane-only checkout returns
exit 2 rather than a miss.

## 8. Verdict

**P2 is met as frozen.** `python3 corpus/evidence/round40/c2-count.py` on lane tip
`6bc90e04ac60307befacd554f7eee2b7284e2652` prints `R39_CALIBRATION_DISPOSITIONS=4/4` and
exits 0. All four dispositions are source-derived and independently confirmed against the
committed bytes; R4's conditional `not-reproduced` is the only disposition the committed spec,
validator plan, and report permit. The counter discriminates: every genuine source mutation
fails exactly its intended cell, the deleted-record control falls to 0/4, and the pre-correction
tree reproduces the committed 0/4 do-nothing control.

Qualification, for the record rather than as a refutation: P2's intent sentence ("re-derive …
not count prose labels alone") holds for R2 (git tracking), R3 (two `git ls-tree` counts), and
R4 (two JSON counter parses + equality); it holds only nominally for R5, which has no derived
measurement and survives deletion of the SCORECARD correction it is meant to certify (W1).
That is a defect in the R5 cell's strength, not in the 4/4 result.

## 9. Artifact pointers (resolvable)

- Counter under test: `corpus/evidence/round40/c2-count.py` (`b0da39157d0b15127575fc9cf36f683ec11fe1db73f58c91dcbeaa60520bdeac`)
- Disposition record: `corpus/evidence/round40/routed-defect-dispositions.json` (`b856906012c02f12500e285089f30bb93da033a57b18de549e4e8795521f31cb`)
- Frozen claim: `corpus/evidence/round40/claims.md` §C2 / P2
- Committed control: `.ufo/waves/round-40/controls/control-before.txt:20-25`
- Committed after-measurement: `corpus/evidence/round40/measure-after.txt` §C2
- R4 sources: `.ufo/waves/round-39/w1-spec.json`, `.ufo/waves/round-39/w1-plan.json`,
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/chousa.md:168-170`,
  `corpus/lessons/round-39-verifier-spotcheck.md:74`
- This report: `.ufo/waves/round-40/w1/ExecC2Count.md`
- Mutant matrix run: ephemeral `/tmp/c2audit/lane` (`git clone --shared`); results reproduced
  in §6, not a durable artifact.
