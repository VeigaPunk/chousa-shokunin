# SimplifySelftest — round 50, wave 1: YAGNI review of the C1 candidate

Slice: C1 (operability/plumbing) only — the `--selftest` additions, the round-50
counter, `controls/`, `c1-fixtures/`. C2 is not my seat. No install, no upgrade, no
network; every source opened is a lane file (no capture was needed for this slice).

## Method (why this is stronger than the `--tool` proof the item names)

`c1-count.py --tool X` skips leg 1 (`legs["SELFTEST_DEFAULT"] = True` stub, `c1-count.py:93`), so a
`--tool` proof exercises 4 of 5 legs. I therefore gave each variant a *whole lane tree* so the
counter's own `parents[3]`, `FIX`, `PIN` and `R49` paths resolve and all five legs run:

    git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/chousa-shokunin lane   # HEAD 7754172
    # per variant: git clone -q --shared --no-checkout lane work/<V>; git -C work/<V> archive HEAD corpus tools | tar -x -C work/<V>
    TMPDIR=/dev/shm/chousa-r50-SimplifySelftest/tmp python3 work/<V>/corpus/evidence/round50/c1-count.py

Harness: `/dev/shm/chousa-r50-SimplifySelftest/harness2.py` (exact hunk per variant, then rerun
counter + the no-flags self-test, compare `LEGS=`, `C1=`, `SELFTEST=` and every `FINDING` line
against the unmutated control). Control V0: `LEGS=5/5 C1=PASS`, `SELFTEST=PASS findings=26`.

## Duplication between the two fixture trees (`diff -r`, as asked)

    $ diff -r corpus/fixtures/assimilate-selftest corpus/evidence/round50/c1-fixtures ; echo rc=$?
    rc=0
    $ python3 -c '…sha256 over sorted rel-path+bytes…'   # same function as tool fixtures_digest()
    default c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43
    pinned  c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43

`corpus/fixtures/assimilate-selftest/` (5 files, 2994 bytes, 38 md lines + `expected.json`
with 26 findings) is a byte-exact copy of the pinned `c1-fixtures/`; the default run prints
`FIXTURES_SHA256=c5c56480…cd43`, the counter's `PIN`, for it as well. It carries **no independent fixture authority**.
Only its *existence at that path* is load-bearing:
- D0 delete the tree → `SELFTEST_DEFAULT=FAIL … LEGS=4/5 C1=FAIL` (ERROR fires from the
  expected-file branch, `assimilate-rows.py:212`, not the fixtures guard at `:214`).
- D1 delete the tree **and** point the default at the pinned tree (`:205` one path change) →
  `LEGS=5/5 C1=PASS`.
Tradeoff of D1: −5 duplicated files, +a `tools/` → round-50-evidence-dir coupling and one
authority instead of two for "what the default package is". The frozen predicate requires a
lane default that exits 0 PASS, not a second package, so D1 is leg-neutral but not
consequence-free.

## Deletion candidates — each leg-neutral, proved by rerun

| # | what (path:line) | proof | tradeoff |
|---|---|---|---|
| V1 | `split_cells()` `tools/assimilate-rows.py:146-147` duplicates the identical expression inlined in `staged_rows()` `:109` | V1 → `LEGS=5/5 C1=PASS`, default findings identical | none; two spellings of one split rule (escaped-pipe aware) — delete one |
| V2 | fixtures-missing guard `assimilate-rows.py:214-216` (`SELFTEST=ERROR fixtures … missing`, exit 2) | V2 → 5/5 PASS | unexercised branch: D0 shows the *expected-file* branch shadows it; only reachable with expected.json present and staged/registry absent |
| V3 | `REFUSED` collector `assimilate-rows.py:163` | V3 → 5/5 PASS, P4 still passes on `DIFF unexpected TOOLEXIT 1` | the only human-readable cause line of P4; `REFUSED` is never asserted (0 hits in either `expected.json`) |
| V4 | `if know.is_dir() else []` `assimilate-rows.py:153` | V4 → 5/5 PASS | `Path.rglob` on a missing dir already yields nothing |
| V5 | `if len(cells) == 11:` `assimilate-rows.py:179` | V5 → 5/5 PASS | false branch unreachable: rows are built only from 11-cell staged rows |
| V6 | `timeout=120` + `TimeoutExpired → 124` `c1-count.py:61-63` | V6 → 5/5 PASS | no leg times out; the branch is the counter's own hang guard |
| V7 | `--root` `c1-count.py:78,80` | V7 → 5/5 PASS | no frozen invocation passes `--root`; it only feeds `default_tool` and R49's `--root`, both equal to `LANE` |
| V8 | empty-collision branch `COLLISIONS ids|-` `assimilate-rows.py:166-167` (`if l` filter + `or "-"`) | V8 → 5/5 PASS | no leg has zero collisions; `-` is the form a real run prints, so keep |
| F1 | registry row `S002` `corpus/fixtures/assimilate-selftest/registry.md:8` | F1 → 5/5 PASS, findings identical | inert: never cited, never held, not the max id, no collision |
| F2 | entry header + prose `…/knowledge/corpus/knowledge/a.md:1-6` (`verified-at:`, `recheck:`, heading, `#### Observation`) | F2 → 5/5 PASS, findings identical | the adopter reads only `S###` tokens from an entry; header realism is documentation, not assertion |
| F3 | staged cells 3-6 text (`kind/tier/scope/teaches`) `…/staged.md:5-8` | F3 → 5/5 PASS, findings identical | no finding reads them; cell 6 keeps the escaped pipe that P3 keys on |

No finding *line* is deletable: `c1-count.py:100` requires observed == 26 == expected, so every
one of the 26 expected lines is load-bearing (dropping one flips a leg — S1).

## Load-bearing — sensitivity controls (the harness is not blind)

| # | mutation | result |
|---|---|---|
| S1 | drop `STRIPPED S015 cell6-pipe` from the **default** expected.json | `SELFTEST_DEFAULT=FAIL … expected=25 … LEGS=4/5 C1=FAIL` |
| S2 | `ROWSTATUS {lid} {cells[7]}` → `{cells[6]}` | `BASELINE=FAIL … LEGS=3/5 C1=FAIL` |
| S3 | drop the `TOOLEXIT` collector | `BASELINE=FAIL PERTURB_PASS=5/6 LEGS=2/5 C1=FAIL` |
| S4 | drop the `os.execv` delegation from `controls/echo-tool.py:13-14` and `const-tool.py:10-11` | echo `LEGS=4/5`→`3/5`, const `2/5`→`1/5`, both via `R49_REGRESSION=FAIL rc=1` |

S4 answers the controls question: the delegation branch is *not* dead — leg 5 drives the
control through the adopter's real interface, so a control may fake only `--selftest`. The
recorded control evidence also still reproduces at HEAD (all three controls rerun, line for
line: `2/5`, `4/5`, `2/5`, `C1=FAIL`), and `controls/tool-before.py` is byte-exactly the base
tool (`sha256 4b995dbc…` == `git show 3c51da7:tools/assimilate-rows.py`) — provenance, not
weight. Three copies of the same 4-line fixture digest exist (`c1-count.py:52-56`,
`assimilate-rows.py:197-201`, `echo-tool.py:22-24`); the control's copy is what makes it pass
`BASELINE`, so none is deletable.

## In-flight edit — not the frozen candidate

`tools/assimilate-rows.py` changed under this seat mid-measurement (working copy
`sha256 382aca9b…`, 380 lines, mtime 18:38:21) — not mine, and not `ec52e63` (363 lines,
`sha256 bff32c11…`). Every line number above is HEAD/`ec52e63`-relative and my proofs ran on a
clone of HEAD. The edit still scores `C1=PASS` under `--tool`; it adds four more no-leg
branches, each leg-neutral (harness3.py, 4-leg `--tool` proof, control `W0` `LEGS=5/5`):
`W1` tab-strip `:201`, `W2` `ENTRYCITES … -` `:195`, `W3` `--selftest takes only …` `:255`,
`W4` observe timeout `TOOLEXIT 124` `:170`. Its multiset comparison `:232` strengthens the
comparison and is not a deletion candidate (no leg carries a duplicate finding).

## Calibration notes (for the Gate reader, not a change proposal)

- Leg 1 is vacuous in every `--tool` proof run (`legs["SELFTEST_DEFAULT"] = True`): a `--tool`
  score of `5/5` is really 4 legs. Only a no-flag run makes it live (control V0 shows it).
- `REFUSED` is the one grammar kind never asserted: P4 emits
  `DIFF unexpected REFUSED S011: recheck '2026-13-45 — …' has no leading valid date or NNd`
  (26 `DIFF missing` + this + `DIFF unexpected TOOLEXIT 1`, `findings=3`), and both expected
  files hold zero `REFUSED` lines (`grep -c REFUSED` → 0).
- The counter holds one number twice: `PIN` at `:47`/gate `:83` (exit 2) and `:100`
  (FAIL). Both are frozen by the kill rule; not a candidate.

## Lane state (deviation disclosed)

`harness.py` v1 (superseded) took `p = COUNTER` for its counter variants and wrote the two
mutated sources back into the **lane** working tree `corpus/evidence/round50/c1-count.py`
(V6, V7 hunks). Restored with
`git show HEAD:corpus/evidence/round50/c1-count.py > corpus/evidence/round50/c1-count.py`:
`sha256 ea3dd4227634dc0c29a15f3187983560bfcd954b98d021dd1a3fcc6c259fde86` equals the HEAD blob,
`git diff` empty for that path. I never wrote `tools/` or either fixture tree; `git status`
now shows the sibling's in-flight `tools/assimilate-rows.py` edit, the pre-existing
`.ufo/waves/round-49/w2/ScoutPlanned.md` and untracked round-50 wave files — none of them mine.
All measurements above are against the scratch clone of HEAD 7754172.

## Verdict

VERDICT: attacked C1's self-test for dead weight — 8 code/branch candidates (V1-V8) and 3
inert fixture hunks (F1-F3) are each provably leg-neutral under a full 5-leg rerun, the lane
default fixture tree is a byte-identical copy of the pinned one whose content is inert (only
its path is load-bearing; D1 removes it at `LEGS=5/5`), the in-flight edit adds 4 more
leg-neutral branches, and 4 sensitivity controls confirm the harness flips a leg when a
leg-bearing line moves; C1 stays `LEGS=5/5 C1=PASS` at HEAD.
