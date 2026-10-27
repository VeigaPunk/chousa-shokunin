# R53DraftSkillGates — SKILL.md `## Gates` rows for round 53

seat: R53DraftSkillGates (chousa lane, wave 1). Draft only: no SKILL.md edit, no counter or claims change; the only lane write is this report.

## Ground read

- `corpus/evidence/round53/claims.md` at lane commit `a6ff732c70011f11c9beb681d832cedc6e75f566` (`git log -1 -- claims.md`): C1 = adopter v4 (twin label, `HELD=`/`TWIN=`, recheck pre-pass, registry-first refusal), C2 = three entries over five documents.
- `SKILL.md:76` `## Gates` — the section ends at the next `## ` heading, `SKILL.md:529`. Superseded row at `SKILL.md:130` (`assimilate-rows`), round-52 style row at `SKILL.md:135`. A row is eight cells: name, kind, entry, verdict map, self-test, pinned values, write scope, owner.
- `tools/assimilate-rows.py` docstring (lines 1–120): `held` only when a Registry row already carries the URL, `twin` for a second staged row of the same run (same lane id, nothing appended), registry refusal printed first and also without `--entry`, recheck checked for held and twin rows, `HELD=`/`TWIN=` on the count line, `--entry` optional/repeatable, `cases` in `expected.json`.
- Exit paths read in code: `c1-count.py:315-384` (`TOOL=absent` → every leg fails, exit 1; `ENV_CHANGED`/`ENV git show failed` → exit 2), `c2-count.py:150-166,255-292` (`NO_BASE_OR_REGISTER` → exit 2; the `ok` conjunction), `build-spans.py:209-268` (`--check` `STALE`, refused quote → exit 1, no cache → exit 2).

## Commands and observed output

1. Registry counter, lane as it stands (before integration):
```
$ TMPDIR=/fast/scratch/hyaku/chousa-r53/R53DraftSkillGates python3 corpus/evidence/round47/c2-count.py --list
UNREGISTERED_PATH corpus/evidence/round53/build-spans.py
UNREGISTERED_PATH corpus/evidence/round53/c1-count.py
UNREGISTERED_PATH corpus/evidence/round53/c2-count.py
ENTRY_POINTS=135 (abc=106 dependence=+9 check_named=+20)
FLOOR=92
GATES_ROWS=58
REGISTERED=132/135
UNREGISTERED=3
DANGLING=0
MISMATCHES=3
C2=FAIL
rc=1
```
The three unregistered entry points are exactly the round-53 counter set the second row names.

2. Adopter v4 self-test, lane default package:
```
$ TMPDIR=/fast/scratch/hyaku/chousa-r53/R53DraftSkillGates python3 tools/assimilate-rows.py --selftest
… 40 FINDING lines (root package, then its three cases) …
FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6
SELFTEST=PASS findings=40 expected=40
rc=0
```
`corpus/fixtures/assimilate-selftest/expected.json` has keys `['findings', 'cases']`, root `findings` 28, `cases` 3; the digest covers the root package and the three case packages.

3. Round-50 pinned package under v4 (`--cites all`): `FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, `SELFTEST=PASS findings=26 expected=26`, `rc=0` — the pin the r50/r51 counters hold still passes on v4.

4. Provenance: `sha256sum tools/assimilate-rows.py` → `32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636`; `git log -1 --format='%H %s' -- tools/assimilate-rows.py` → `32aab5edd70e43145cae72ec872278f3bc6efba7` (`round-53: C1 candidate — adopter v4 …`); `git status --short tools/assimilate-rows.py corpus/fixtures/assimilate-selftest/` printed nothing.

5. Row registration, measured on a scratch copy of the lane tree (`tar -C <lane> --exclude=.git -cf - . | tar -C <scratch>/lane-copy -xf -`, rows spliced after `SKILL.md:135`):
```
$ TMPDIR=/fast/scratch/hyaku/chousa-r53/R53DraftSkillGates python3 lane-copy/corpus/evidence/round47/c2-count.py --root lane-copy --list
ENTRY_POINTS=135 (abc=106 dependence=+9 check_named=+20)
FLOOR=92
GATES_ROWS=60
REGISTERED=135/135
UNREGISTERED=0
DANGLING=0
MISMATCHES=0
C2=PASS
rc=0
```
The lane's `SKILL.md` was never written; this is a copy-only measurement of the drafted text.

6. Before/control receipts read, not re-run: `controls/c1-before.txt` — base `LEGS=1/8` (REGRESS only) on three unseeded runs and `--seed 7`, counter exit 1; controls BASE 1/8, CONST 0/8, REFUSE 0/8, RELABEL 5/8 (RECHECK/ORDER/NOENTRY fail), ALLTWIN 2/8. `controls/c2-before.txt` — `ENTRIES=0/3 BOUND=0/5 SUBSTANCE=FAIL C2=FAIL` exit 1. `controls/c2-controls.txt` — STAGED `REF_ID_UNBOUND=12 BOUND=0/5`; TOOLED (its adopter run: `CITED=6 APPEND=5 HELD=1`, exit 0) `BOUND=5/5 REF_ID_UNBOUND=4 ANCHOR_BOUND=0/5`, both `C2=FAIL`.

## Draft rows — append inside `## Gates` after `SKILL.md:135`; row 1 supersedes `SKILL.md:130` by name

```SKILL.md
| `assimilate-rows (v4, round 53)` (supersedes `assimilate-rows` (r49 C1; addendum section 10 adopter; r50 `--selftest`; r51 `--cites`/`ASSIMILATE_CITES`, header-only `source:` citation, `bodyonly.tsv`/`bodyclash.tsv`, escaped-pipe identity, registry-structure and unknown-source refusals) by name; candidate v4 at `32aab5edd70e43145cae72ec872278f3bc6efba7` over base `5b550133` adds the same-run `twin` label, the `HELD=`/`TWIN=` count line, the recheck pre-pass over held and twin rows, and a registry refusal printed before any entry refusal and also with no `--entry`) | tool | `python3 tools/assimilate-rows.py --staged FILE --knowledge DIR --registry FILE --opened YYYY-MM-DD --out DIR [--entry REL ...] [--cites source or all]` · `python3 tools/assimilate-rows.py --selftest [--fixtures DIR] [--expected FILE] [--cites source or all]` (the adopter writes only under `--out`: `reg-ids`, `staged-ids`, `collisions`; with entries also `renumber.tsv` (`staged_id lane_id action url`, action `held` only when a lane Registry row already carries the URL, `twin` when an earlier-cited staged row of the same run minted that id — same lane id, nothing appended — else `append`), `append.md`, `stripped.tsv`, the rewritten entries and, in source mode, `bodyonly.tsv` and, when a body-only staged id is also a lane id, `bodyclash.tsv`; the registry is read and refused before any entry, with or without `--entry`; `--entry` is repeatable and optional; an entry cites the id right after `source:` on a header line above its first `####` heading, and an entry's own ids only are substituted in it; `--cites` defaults to `source`; env `ASSIMILATE_CITES=source or all` sets the default of both modes, an explicit flag winning; the self-test writes nothing in the lane) | adopter exit `0` done (`COLLISIONS=n`, `CITED= APPEND= HELD= TWIN=`, source mode `BODYONLY=n`, one stderr `WARN <entry>: body-only staged id <S###> is also a lane id` per clash) · `1` refused (registry with no `## Registry` heading or with an `S###` row outside it — every registry `REFUSED` line printed before any entry `REFUSED` line, and refused also with no `--entry`; entry missing or not UTF-8; cited staged row not 11 cells or no URL; a recheck with no leading valid date/`NNd`/cadence, held and twin rows included (`REFUSED <staged id>: recheck`); a `source:` id that is neither a staged row nor a Registry row, or a lane row this run also mints — no `renumber.tsv`, no `append.md`) · `2` usage (missing file, non-UTF-8 input, invalid `--opened`, absolute or `..` entry, `ASSIMILATE_CITES` other than source/all, `--selftest` with any adopter option); self-test `0` PASS · `1` `DIFF missing`/`DIFF unexpected` · `2` fixtures or expected file missing or unparseable | lane default `python3 tools/assimilate-rows.py --selftest` → `SELFTEST=PASS findings=40 expected=40`, `FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6` over the root package plus the three `cases` of `expected.json`; the round-50 package `corpus/evidence/round50/c1-fixtures/` with `--cites all` → `findings=26 expected=26`, digest `c5c56480…`; scored by `python3 corpus/evidence/round53/c1-count.py` (frozen `LEGS=8/8`, REAL pinned) and `python3 corpus/evidence/round51/c1-count.py` (`LEGS=5/5`); tool-rev: 32aab5edd70e43145cae72ec872278f3bc6efba7 tool: tools/assimilate-rows.py digest: sha256:32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636 | lane default package `corpus/fixtures/assimilate-selftest/` (hand-written `expected.json`, QUALITY 73; the r53 `cases` are inside the digest); round-50 package digest pinned in `corpus/evidence/round50/c1-count.py` (`PIN`) and `corpus/evidence/round51/c1-count.py` (`R50_PIN`, exit 2 `PIN_CHANGED`); `held` is reserved for a row the Registry already carries (the ALLTWIN control, every non-append row labelled `twin`, scores 2/8); a body token naming a lane row of another document that is not a staged id passes through unlisted | self-test: own `tempfile.mkdtemp`, no lane write; adopter: writes only under `--out`; no network | chousa |
| `chousa round-53 counters and checks` | gate | `python3 corpus/evidence/round53/c1-count.py [--tool PATH] [--seed N] [--per-leg K] [--work DIR]` (scratch under `--work` or `$TMPDIR`, removed on exit; every package, id, host, path, entry name and recheck drawn fresh per seed, with randomised registry-row indentation, heading separator, URL scheme, trailing `/` and host case) · `python3 corpus/evidence/round53/c2-count.py [--root LANE] [--lane-only]` · `python3 corpus/evidence/round53/build-spans.py [--root LANE] [--cache DIR] [--check]` (its own `.docx` reader, so C2 does not run the round-52 `capture-text` tool) · controls `python3 corpus/evidence/round53/controls/build-c1-controls.py [--seed N]`, `corpus/evidence/round53/controls/build-c2-controls.py` | C1 exit `0` only with `LEGS=8/8` (`TWIN`, `HELD`, `MIX`, `RECHECK`, `ORDER`, `NOENTRY`, `REAL`, `REGRESS`) and `C1=PASS`; `1` a leg failed (a missing `--tool` prints `TOOL=absent <path>` and fails every leg, exit 1); `2` env (`ENV_CHANGED real-pin=<hex> (want 8e6484ed…)` when the REAL pin, the round-50 `expected.json` or the round-51 counter is absent or changed; `ENV git show failed` when the `BASE_REV` registry cannot be read). C2 exit `0` only with `ENTRIES=n/3` ≥ 2 and `ENTRIES+REFUSED_ENTRIES=3`, `BOUND>=3` and `BOUND+REFUSED=5`, `REF_ID_UNBOUND=0`, `NEW_GROUND=n/n`, `QUOTE_ROWS` with `ON_BOUND=n/n` and `n>0`, `SPAN_IDS=BOUND` (`min 3 each`), `QUOTES_IN_SPAN`/`QUOTES_IN_ENTRY`/`QUOTES_IN_LESSON`/`QUOTE_SHORT`/`SPAN_CONTEXT` each `n/n`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=BOUND`, `INFERENCE_GROUNDED=n/n`, `QUARANTINE_VERDICTS` complete and `QUARANTINE_BLOCKED_ADOPTED=0`; `--lane-only` prints `CAPTURE_BOUND=skipped`; `1` otherwise; `2` `NO_BASE_OR_REGISTER`/usage. build-spans `0` `SPANS_ROWS=n WRITTEN=n`, or under `--check` `SPANS_ROWS=n STALE=0`; `1` a refused quote (`build-spans: refused <reason>`) or `SPANS_HEADER_STALE`/`SPANS_ROW_STALE`/`SPANS_FILE_STALE`/`SPANS_ROW_EXTRA`/`SPANS_FILE_ORPHAN`; `2` usage/env (no capture cache) | pins `BASE_REV` `5b550133d79bc09c82d8965cce2e48c2598b8c3e` in both counters; C1 `REAL_PIN` `8e6484edbff80ebe167f6378c7eb7c6214b57d4d50380a43e700386714f3689b` (sha256 over the campaign `SOURCES.append.md` plus the three staged entries, exit 2 on mismatch) and `R50_PIN` `c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`; C2 `CACHE` and `REGISTER` under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/`. Before receipts `corpus/evidence/round53/controls/c1-before.txt` (base `LEGS=1/8`, REGRESS only, on three unseeded runs and `--seed 7`, counter exit 1; controls BASE 1/8, CONST 0/8, REFUSE 0/8, RELABEL 5/8 — RECHECK/ORDER/NOENTRY fail — and ALLTWIN 2/8), `c2-before.txt` (`ENTRIES=0/3 BOUND=0/5 SUBSTANCE=FAIL C2=FAIL` exit 1), `c2-controls.txt` (STAGED `REF_ID_UNBOUND=12 BOUND=0/5`; TOOLED `BOUND=5/5 REF_ID_UNBOUND=4 ANCHOR_BOUND=0/5`, both `C2=FAIL`) | frozen in `corpus/evidence/round53/claims.md` at lane commit `a6ff732c70011f11c9beb681d832cedc6e75f566`; C1 target `LEGS=8/8` on three unseeded runs and `--seed 7`, C2 target `C2=PASS` with `ENTRIES>=2` and `BOUND>=3` | C1 and C2 are read-only on the lane and write only their scratch under `--work`/`$TMPDIR`; build-spans writes `corpus/evidence/round53/spans.tsv` and `spans/` and nothing under `--check`; no network | chousa |
```

## Findings

- F1 (measured) The registry counter sees only eight-cell rows. With the round-53 row at seven cells the copy printed `GATES_ROWS=59 REGISTERED=132/135` with all three round-53 paths still unregistered; after adding the missing write-scope cell it printed `GATES_ROWS=60 REGISTERED=135/135 MISMATCHES=0 C2=PASS`. The delivered rows each carry eight cells.
- F2 (limit) Until the L1 integrates both rows the lane registry stays at `REGISTERED=132/135 … C2=FAIL` exit 1; that is the pre-integration state, not a counter defect. Registration is a property of `SKILL.md`, so it can only be measured on a copy.
- F3 Adopter v4 moves the lane-default self-test from 27 to 40 findings and digest `3b7ad258…` to `9822ad59…` (the r51 row's values) because `expected.json` gained three `cases`; the r50 pin `c5c56480…` is unchanged and still passes (26/26).
- F4 (limit) I re-ran only the two self-test legs. Before/control counts in the second row are quoted from the committed receipts `controls/c1-before.txt`, `c1-before.txt` controls block, `c2-before.txt`, `c2-controls.txt`; I did not run C1/C2 against their targets (other seats own that measurement).
- F5 `--entry` is optional and repeatable in v4 (`--help` shows `[--entry ENTRY]`, `add_argument(..., action="append")`); the row states both the exit-0 sound-registry/no-entry path and the refused broken-registry path.
- Out of scope, untouched: `corpus/evidence/round53/claims.md`, the counters, entries, spans and `corpus/lessons/round-53.md`; no production file, git index or jj state written.

## Tooling

No install or upgrade (none needed). All commands ran with `TMPDIR=/fast/scratch/hyaku/chousa-r53/R53DraftSkillGates`; scratch (including the 265 MB lane copy) removed after this report was written; no network.

VERDICT: attacked the round-53 gate registry — drafted the adopter-v4 superseding row and the round-53 counter row, and measured on a scratch copy that they take `REGISTERED=132/135 UNREGISTERED=3 MISMATCHES=3 C2=FAIL` (lane) to `GATES_ROWS=60 REGISTERED=135/135 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS` rc 0, with the adopter's `--selftest` observed at `findings=40 expected=40` digest `9822ad59…` and the r50 package at `26/26` digest `c5c56480…`.
