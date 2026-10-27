# R53ReviewAdopter — C1 candidate v4, line-by-line review (round 53 wave 1)

Seat: R53ReviewAdopter | /skill:godspeed
Scope: diff `a6ff732c70011f11c9beb681d832cedc6e75f566` -> `32aab5edd70e43145cae72ec872278f3bc6efba7` on
`tools/assimilate-rows.py` + `corpus/fixtures/assimilate-selftest`, read against the frozen R53-C1 predicate
(`corpus/evidence/round53/claims.md`) and the tool's own docstring.
Scratch: `/fast/scratch/hyaku/chousa-r53/R53ReviewAdopter/` (TMPDIR set there; every command below ran there;
tool copied to `tool-candidate.py` — the lane tree was never written).

## Verdict

No predicate-breaking defect. The candidate lands the round-52 routed items: (a) second staged row for a
this-run-minted URL is now labelled `twin` (base line 438 said `held`); (b) recheck validated for every cited
row including held/twin (base checked only inside the append loop after `if action != "append": continue`); (c)
registry refusals seeded first into `refused` (base appended them after entry refusals); (d) broken registry is
refused also without `--entry`. The frozen counter passes `LEGS=8/8` against the candidate at seed 7. Findings
below are three low observations + two docstring nits; none blocks.

## What the diff does (anchors)

- Tool lines ~35, ~76-95, ~250-333 (selftest/cases/DIFF order), ~421-445 (no-entry refusal), ~447-465
  (refused seeded with `reg_bad`), ~485-520 (twin label in mapping; recheck pre-pass over `cited`).
- Mapping order: registry-held checked before this-run minted, so a registry-carried URL is never a twin.
- `HELD=`/`TWIN=` count line counts mapping labels (`held_n`/`twin_n`).

## Evidence (commands, observed output)

### 1. Default selftest (new fixture incl. cases) — PASS
`python3 tool-candidate.py --selftest --cites source --fixtures <lane>/corpus/fixtures/assimilate-selftest`
-> `FINDING MAP S017->S021 twin`, case runs (twin-recheck REFUSED S102; refusal-order registry-before-entry;
no-entry registry refusal), `FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6`,
`SELFTEST=PASS findings=40 expected=40`, exit 0. Digest independently recomputed and equal.

### 2. Base tool fails the same fixture exactly on the twin label (fixture genuinely covers the routed defect)
`python3 base-tool.py --selftest ...` -> rc 1; `DIFF missing MAP S017->S021 twin` / `DIFF unexpected MAP S017->S021 held`.

### 3. Recheck pre-pass, held row (P1)
staged S101 URL held by registry, recheck `2026-02-30 — bad`; `--entry` cites it.
rc 1; stderr: `REFUSED S101: recheck '2026-02-30 — bad' has no leading valid date or NNd`; out/ has
`collisions reg-ids staged-ids` only — no `renumber.tsv`, no `append.md`.

### 4. Recheck pre-pass, twin row (P4)
S102 twin of S101 with `2026-04-31 — bad` -> rc 1, `REFUSED S102: ...`; no claim files.

### 5. Multiple bad rechecks reported together (P10, one twin S102 + one held S103)
rc 1, stderr lists both: `REFUSED S102: ... 2026-02-30 ...` then `REFUSED S103: ... 2026-13-01 ...`; no claim files.

### 6. Twin = same lane id, nothing appended (P2)
`renumber.tsv`: `S101 S002 append twin.test/u` / `S102 S002 twin twin.test/u`; `append.md` has the one minted row;
stdout `CITED=2 APPEND=1 HELD=0 TWIN=1`.

### 7. held only when the registry carries the URL (P3)
both S101/S102 carry a registry URL -> `S101 S001 held` / `S102 S001 held`; `append.md` empty (0 bytes);
`CITED=2 APPEND=0 HELD=2 TWIN=0`.

### 8. Registry-before-entry refusal order (P5)
broken registry + missing entry, `--entry` absent first then good:
rc 1; stderr order: `REFUSED registry has no `## Registry` heading`, `REFUSED registry rows outside the Registry section: S001`, `REFUSED entry missing: corpus/knowledge/absent.md`. Matches the counter's ORDER leg.

### 9. Combined broken registry + bad recheck (P6)
rc 1; stderr prints only the two registry REFUSED lines; the bad recheck is never reported (F1).

### 10. No-`--entry` semantics (P7)
broken registry -> rc 1, registry REFUSED lines, out/ = `collisions reg-ids staged-ids`; sound registry -> rc 0,
no stderr, same three files, stdout `COLLISIONS=0`.

### 11. `--selftest` cases validation (E1-E6)
`cases` as an object; case missing `fixtures`; case fixture dir missing; case `findings` not a list; case `entry`
not a list; root `findings` not a list -> each: rc 2 and `SELFTEST=ERROR expected file <exp>: <message>`.
`--selftest --opened 2026-01-01` -> rc 2, `--selftest takes only --fixtures and --expected`.

### 12. DIFF order catches a pure permutation (O1)
expected has the two registry REFUSED lines swapped (same multiset): no `DIFF missing/unexpected`; rc 1; emits
`DIFF order cases/refusal-order: REFUSED registry has no `## Registry` heading (want REFUSED registry rows outside the Registry section: S001)` and the mirror line; `SELFTEST=FAIL findings=40 expected=40`.

### 13. Frozen counter corroboration (seed 7, --per-leg 1)
`python3 corpus/evidence/round53/c1-count.py --tool tool-candidate.py --seed 7 --per-leg 1`
-> all legs PASS; `REAL ... count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']`; `REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5`;
`LEGS=8/8`, `C1=PASS`, exit 0.

## Findings

- **F1 (low, info):** when a broken registry and a bad recheck coincide (P6), only the registry refusals print;
  the recheck line is suppressed because the `refused` block returns before the pre-pass. Exit 1 either way, so the
  frozen predicate (registry lines before entry lines; recheck refusal contract) is not violated — but the operator
  does not learn about the recheck. The counter never combines these (RECHECK leg has no other refusal), so this is
  counter-invisible.
- **F2 (low):** a refused no-`--entry` run leaves a previous run's claim files in `--out` (P8: `renumber.tsv`
  survived an earlier entry run after the refused no-entry run), while the entry path unlinks them ("a refusal never
  leaves a previous run's claim behind"). Docstring "Refusals (exit 1, nothing claimed)" holds for the run itself;
  the asymmetry is undocumented. Not a predicate break.
- **F3 (docstring nit):** "checked and printed FIRST, before any entry is read" overstates: `reg_bad` is computed
  before entries but printed only after entries are read — still first among REFUSED lines (P5). The 11-cells
  refusal (`staged row has N cells, not 11`) remains absent from the docstring refusal list (pre-existing at base).
- **F4 (docstring nit):** the `DIFF order` shape omits the case-name prefix actually printed for cases
  (`cases/refusal-order: `, O1).

## Docstring-vs-code check (asked points)

- Refusals list: registry (with and without `--entry`), entry missing/not UTF-8, no-URL, recheck incl. held/twin —
  all match code; F3 covers the two gaps.
- Named-limit paragraph: matches (append first, twin later to the same id, `used-by` across twins, first staged
  row's tier/scope kept, held rows never widened).
- `HELD=` meaning: code counts cited rows mapped `held`; docstring gloss `<registry rows>` is acceptable.
- Exit-code doc (0 done / 1 refused / 2 usage): reproduced, incl. `--selftest` with other options -> 2.

## Residual risk / verification gaps

- I ran the frozen counter once (seed 7); the three independent unseeded runs are the executor seat's evidence.
- The combined registry+recheck scenario (F1) is not exercised by the counter; verified manually only.
- In `--cites all` mode the pre-pass now also validates body-token rows' rechecks — a behavior change beyond the
  claimed source-mode semantics; not counter-monitored.

Report: .ufo/waves/round-53/w1/R53ReviewAdopter.md
VERDICT: attacked the C1 candidate v4 diff line-by-line against the frozen predicate and docstring — no blocking
defect; held/twin recheck validation, registry-first ordering, no-entry registry refusal, cases validation (exit 2)
and the REFUSED-order comparison all verified by repro; three low findings and two docstring nits recorded.
