# R51SimplifyAdopter — YAGNI review of the C1 candidate (round 51, wave 1)

Seat: R51SimplifyAdopter (leaf). Scope: `tools/assimilate-rows.py` at
`2a3389da0306e41f1b4797c1bc69017f23a38aef` vs `d603f6f`, plus `corpus/fixtures/assimilate-selftest`
and `corpus/evidence/round51/c1-count.py`. No lane file edited; every experiment ran on copies under
`/dev/shm/chousa-r51-R51SimplifyAdopter/` (deleted at the end). No install was needed.

## 1. Baseline (candidate as landed)

```
$ python3 corpus/evidence/round51/c1-count.py --seed 4242
SELFTEST_DEFAULT=PASS
LEGS=5/5
C1=PASS
$ python3 corpus/evidence/round51/c1-count.py --tool .../tool-cand.py --seed 12345
LEGACY_ALL=PASS rc=0
SOURCE_ONLY=PASS default_rc=0 map=['S505', 'S652'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S688']] all_rc=0 all_map=['S505', 'S652', 'S688']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
C1=PASS
```

## 2. What no frozen leg exercises (measured, not argued)

A wrapper around the candidate logged `out/bodyclash.tsv` for every invocation, then
`c1-count.py --tool wrap.py --seed 4242` (all 8 package runs):

```
rc=0 out=.../s/out CLASH=none        rc=1 out=.../renamed-heading/out CLASH=none
rc=0 out=.../s-all/out CLASH=none    rc=1 out=.../no-heading/out CLASH=none
rc=0 out=.../d1/out CLASH=none       rc=1 out=.../row-outside/out CLASH=none
rc=0 out=.../d2/out CLASH=none       rc=0 out=.../well-formed/out CLASH=none
```

`grep -c bodyclash corpus/evidence/round51/c1-count.py` → `0`, and by construction it cannot fire:
`top = rnd.randint(12, 40)`, minted id `top+1 <= 41`, body-only ids `S{rnd.randint(500, 900)}`
(`c1-count.py:122-123`). The only source of a BODYCLASH finding is one candidate-owned fixture line,
`expected.json` `"BODYCLASH corpus/knowledge/b.md S011"`.

## 3. Deletion experiment (five variants, each rerun)

| variant | deletion | counter (`--tool`, 3 seeds) | selftest |
|---|---|---|---|
| v1 | BODYCLASH branch (`:248`), `lane_ids` (`:438`), clash+WARN (`:442-446`) + fixture line | `LEGS=5/5 C1=PASS` ×3 | 24/24 PASS |
| v2 | v1 − `ASSIMILATE_CITES` (`:315-323`), `import os` (`:91`) | `LEGS=5/5 C1=PASS` | 24/24 PASS |
| v3 | v2 − registry-side `pipe_free` (`:382`) | `LEGS=5/5`, `d2=ok` | 24/24 PASS |
| v4 | v3 + fold `:414` `re.sub(...)` into `pipe_free(c)`; `:365` `refused += registry_problems(...)` | `LEGS=5/5 C1=PASS` | 24/24 PASS |
| v5 | v4 + docstring prose (`:32-33`, `:64`, `:67-68`) | `LEGS=5/5 C1=PASS` ×3 | 24/24 PASS |

v5 is 445 lines against the candidate's 463: **18 lines removable with no leg result changed** (two
more rewritten, not removed). The `--tool` runs do not prove the lane-default leg — it prints
`SELFTEST_DEFAULT=PASS (skipped: --tool)` and is counted as passing — so it was replayed with its own
command in a fake lane tree (`<T>/tools/assimilate-rows.py`, `<T>/corpus/fixtures/assimilate-selftest`):

```
$ cd $T && python3 tools/assimilate-rows.py --selftest
FIXTURES_SHA256=845200e160617afe0a2cd16de4d827486edd151ee08701f7880d00922d366b6a
SELFTEST=PASS findings=24 expected=24
```

The 24 surviving findings are byte-equal to the candidate's 25 minus the BODYCLASH line (`diff` of the
two `FINDING` streams → `IDENTICAL`). The deletion is *coupled*, not free — v1 against unchanged
fixtures: `DIFF missing BODYCLASH corpus/knowledge/b.md S011` / `SELFTEST=FAIL findings=24 expected=25`.

## 4. Verdicts per candidate

- **BODYCLASH / `bodyclash.tsv` / `lane_ids` / the WARN — KEEP.** Not in the frozen predicate and
  deletable with zero leg change, but not dead: on the real staged package it fires. Run on
  `SOURCES.append.md` + `knowledge/` from the staged package, `corpus/SOURCES.md`, `--out <scratch>`,
  the three theme entries:
  `WARN corpus/knowledge/japanese-search-record-r38.md: body-only staged id S105 is also a lane id and reads as that row`
  plus S097 (×2), S105 (×2), S106; `BODYONLY=5 CITED=7 APPEND=7 HELD=0`. Those are exactly the ids the
  round brief says must never be carried over, so this is the round's own live detector. Cost: one
  fixture line is its only coverage, so that row MUST stay.
- **`ASSIMILATE_CITES` — DROP (or measure it).** No leg sets it; `grep -rn ASSIMILATE_CITES` over the
  lane finds only the tool itself. Its sole buyer is a one-shot frozen counter, and there it works:
  `tool-cand.py --selftest --fixtures <round50 c1-fixtures>` exits 1 with 5 `DIFF missing` lines, and
  with `ASSIMILATE_CITES=all` prints `SELFTEST=PASS findings=26 expected=26` plus the pin
  `c5c56480...`. But that counter passes no flag (`round50/c1-count.py:61`) and the claims already put
  it outside the predicate with `LEGACY_ALL` preserving its behaviour — a second channel for a need the
  claim disowns, costing 8 code lines, an import and 3 docstring lines that nothing measures.
- **`--cites all` — KEEP.** Named by the frozen predicate, used twice by legs (`LEGACY_ALL`, the
  `all_map` half of `SOURCE_ONLY`). Removing it fails both.
- **Registry-side `pipe_free` (`:382`) — KEEP, for symmetry only.** v3 proves no leg needs it (D2's
  escape sits *before* the URL, where `url_of`'s `[^\s|]+` already stops; lane `corpus/SOURCES.md` holds
  0 escaped pipes). It closes only `URL\|alt` with no space. Deleting it leaves the registry path
  asymmetric with the staged path — a second convention, worse than one unexercised branch.

## 5. Duplicate authority (same rule, two copies — fold, don't delete)

- `:414` `cells[i] = re.sub(r"\s*\\?\|\s*", " / ", c)` re-states `pipe_free`'s body (`:156`) in the same
  file; one rewrite rule, two literals, and the next edit drifts one. Use `pipe_free(c)` (v4/v5).
- `:315-323` the `cites` resolution and its validation are written twice, with two names (`sc`,
  `cites`) and two identical messages; v2 collapses to `cites = a.cites or "source"`.
- `:365` `refused += [f"{p}" for p in registry_problems(reg_text)]` — the f-string is a no-op.
- `:438` `{s for s in base}` is `set(base)`.

## 6. Fixture rows and drift

Every row id in `staged.md`/`registry.md` is named by an expected finding (`S001 S002 S010-S016 S020`;
`unexercised: []`) — no orphan row; the only removable one is the BODYCLASH line, which §4 keeps.
Drift nit: `:313` still prints `assimilate-rows: --selftest takes only --fixtures and --expected`
(rc=2) while `--selftest ... --cites all` is accepted and exercised
(`SELFTEST=PASS findings=26 expected=26`) — stale message, the round-50 "filename drift" class.

## 7. Preserved contract

Every frozen leg (SELFTEST_DEFAULT, LEGACY_ALL, SOURCE_ONLY, PIPE_IDENTITY, REGISTRY_STRUCTURE) and the
round-50 pin (`c5c56480...`, 26 findings) hold on all five variants and on the landed tool. My
recommendation changes no predicate: keep BODYCLASH and `--cites all`, drop the env var, fold the two
duplicate rules. Nothing here was landed — the L1 integrates.

VERDICT: attacked the C1 adopter for dead surface — proved 18 lines (BODYCLASH cluster, `ASSIMILATE_CITES`, a duplicate regex, a no-op f-string) deletable with `LEGS=5/5 C1=PASS` and `SELFTEST=PASS` intact, but BODYCLASH fires 5× on the real staged package (S097/S105/S106) so only the env override is genuine surplus; `--cites all` plus the env var is one knob too many.
