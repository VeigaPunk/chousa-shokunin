# R53ExecHistCounters — round-53 w1: historical counters at C1 candidate v4

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `6365f15` (tree = `32aab5e` for every file measured).
Candidate `sha256(tools/assimilate-rows.py)=32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636`
(581 lines); base `git show 5b550133d79bc09c82d8965cce2e48c2598b8c3e:tools/assimilate-rows.py` →
`sha256=10af959b2b87dad565717b84e68733caab6cb7a940d68fb1c52fca793d4c86f4` (514 lines); diff 102+/35−.
Scratch `$S=/fast/scratch/hyaku/chousa-r53/R53ExecHistCounters` (`TMPDIR=$S/tmp`, `base-tool.py` = the export,
all outputs absolute under `$S/out`), removed at the end. No tool installed; nothing written outside this report and `$S`.

Every command below ran from the lane root with `TMPDIR=$S/tmp`. Base rows use each counter's own `--tool PATH` (all five
counters and supplements have one; `receipt-check.py` has none and reads git only).

## 1. Table — counter · base result · candidate result · changed?

| counter | base (`5b55013`) | candidate (`32aab5e`) | changed? |
|---|---|---|---|
| `round49/c1-count.py` | `SETS_PASS=2/3 C1=FAIL` exit 1 | `SETS_PASS=2/3 C1=FAIL` exit 1 | no — pre-existing (§3) |
| `round49/c1-count.py` + `ASSIMILATE_CITES=all` | `SETS_PASS=3/3 C1=PASS` exit 0 | `SETS_PASS=3/3 C1=PASS` exit 0 | no |
| `round50/c1-count.py` | `LEGS=3/5 C1=FAIL` exit 1 | `LEGS=3/5 C1=FAIL` exit 1 | no — pre-existing (§3) |
| `round50/c1-count.py` + `ASSIMILATE_CITES=all` | `LEGS=5/5 C1=PASS` (`SELFTEST_DEFAULT` skipped: `--tool`) | `LEGS=4/5 C1=FAIL` (`SELFTEST_DEFAULT=FAIL`) | no — leg-set artifact + same ambient env failure on base (§4) |
| `round50/c1-supplement.py` | `SUPPLEMENT_LEGS=4/5 C1_SUPPLEMENT=FAIL` (P7) exit 1 | `SUPPLEMENT_LEGS=4/5 C1_SUPPLEMENT=FAIL` (P7) exit 1 | no — pre-existing (§3) |
| `round50/c1-supplement.py` + `ASSIMILATE_CITES=all` | `5/5 PASS` exit 0 | `5/5 PASS` exit 0 | no |
| `round51/c1-count.py` (×3 base, ×3 cand) | `LEGS=5/5 C1=PASS` exit 0 every run | `LEGS=5/5 C1=PASS` exit 0 every run | no |
| `round51/c1-supplement.py` | `SUPPLEMENT_LEGS=10/10 PASS` exit 0 | `SUPPLEMENT_LEGS=10/10 PASS` exit 0 | no |
| `round51/receipt-check.py --help` | script untouched by v4 (no diff) | usage, exit 0 | no |
| `receipt-check.py corpus/evidence/round52/measure-after.txt` | `RECEIPT_OK rev=643ac77b1097 tool=tools/capture-text.py` `CHECKS=1 OK=1 FAILS=0 RECEIPT_CHECK=PASS` exit 0 | identical | no |
| `tools/assimilate-rows.py --selftest` (clean env) | **FAIL**: `DIFF missing MAP S017->S021 twin` / `DIFF unexpected MAP S017->S021 held`, `findings=28 expected=28` | **PASS** `findings=40 expected=40` | **yes — intended v4** (§2) |
| `receipt-check.py` over **both** receipts, `--tip HEAD` | — | `RECEIPT_TOOL_MOVED …round51/measure-after.txt rev=41b4dca86fc8` → `CHECKS=2 OK=1 FAILS=1 RECEIPT_CHECK=FAIL` exit 1 | **yes — intended v4 consequence** (§5) |
| same, `--tip 5b55013` | `CHECKS=2 OK=2 FAILS=0 RECEIPT_CHECK=PASS` exit 0 | same | no |

The only behavioural change any historical counter sees is the `twin` label on the root fixture package. No historical
counter parses the tool's own count line (`grep -rn 'HELD=\|CITED=\|APPEND='` over the five counters plus
`receipt-check.py`: one hit, `round49/c1-count.py:278`, which prints its *own* metric), and every refusal assertion is
`"REFUSED" in err` (order-insensitive), so v4's new `TWIN=` tail and refusal ordering break no frozen assertion:
`round51/c1-count.py:200`, `round51/c1-supplement.py:165` — nothing else matched.

## 2. The one change, verified as the intended v4 behaviour

```
$ python3 $S/base-tool.py --selftest --fixtures corpus/fixtures/assimilate-selftest     (clean env)
DIFF missing MAP S017->S021 twin
DIFF unexpected MAP S017->S021 held
FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6
SELFTEST=FAIL findings=28 expected=28      exit=1
$ python3 tools/assimilate-rows.py --selftest                                            (clean env)
SELFTEST=PASS findings=40 expected=40      exit=0
```

The commit under test also adds the fixture content (`git show --stat 32aab5e`): root `staged.md` gains
`S017 | New doc A, staged twice — https://example.test/new-a`, `expected.json` gains `cases`
(`cases/twin-recheck`, `cases/refusal-order` ×2 with `entry: []`). Base fails only on the label of that one row — the
`held`→`twin` distinction the claim freezes. Live confirmation on the root package, copied into scratch:

```
$ python3 tools/assimilate-rows.py --staged …/pkg/staged.md --knowledge …/pkg/knowledge \
      --registry …/pkg/registry.md --opened 2026-10-26 --out …/o1 --entry <each of knowledge/corpus/knowledge/*.md>
CITED=6 APPEND=2 HELD=3 TWIN=1
renumber.tsv:  S010 S021 append   S012 S001 held   S013 S022 append
               S014 S020 held     S015 S002 held   S017 S021 twin
```

Three further v4 behaviours, base vs candidate, on `cases/refusal-order` and `cases/twin-recheck` (stderr shown):

```
-- broken registry, no --entry        candidate: REFUSED registry has no `## Registry` heading /
   REFUSED registry rows outside the Registry section: S001 / exit=1, no renumber.tsv, no append.md
                                        base:      COLLISIONS=0 / exit=0        (old hole)
-- broken registry + missing entry    candidate: REFUSED registry… / REFUSED registry rows… / REFUSED entry missing: …
                                        base:      REFUSED entry missing: … first, registry lines after
-- twin row S102 recheck `2026-02-30 — re-verify after release`
   candidate: REFUSED S102: recheck '2026-02-30 — re-verify after release' has no leading valid date or NNd / exit=1
   base:      CITED=2 APPEND=1 HELD=1 / renumber.tsv S102 S002 held / exit=0   (no recheck on the twin row)
```

## 3. The three pre-existing failures are NOT v4 — base reproduces each byte-for-byte

```
$ python3 corpus/evidence/round49/c1-count.py            (candidate)   $ … --tool $S/base-tool.py
SET_C … BY_DOC=3/5 EXTRA=0 REWRITE=0/1 … -> FAIL                       SET_C … BY_DOC=3/5 EXTRA=0 REWRITE=0/1 … -> FAIL
SETS_PASS=2/3 C1=FAIL exit=1                                           SETS_PASS=2/3 C1=FAIL exit=1
$ env ASSIMILATE_CITES=all python3 …round49/c1-count.py  (cand and base): SETS_PASS=3/3 C1=PASS exit=0 (SET_C BY_DOC=5/5 REWRITE=1/1)
$ python3 corpus/evidence/round50/c1-count.py            (candidate)   $ … --tool $S/base-tool.py
SELFTEST_DEFAULT=PASS   BASELINE=FAIL rc=1 findings=?                  SELFTEST_DEFAULT=PASS (skipped: --tool)   BASELINE=FAIL rc=1 findings=?
LEGS=3/5 C1=FAIL exit=1                                                LEGS=3/5 C1=FAIL exit=1
$ python3 corpus/evidence/round50/c1-supplement.py       (candidate)   $ … --tool $S/base-tool.py
P7_NONCE_EXCLUSIVE=FAIL  H1..H4=PASS  SUPPLEMENT_LEGS=4/5 C1_SUPPLEMENT=FAIL exit=1   identical on base
$ env ASSIMILATE_CITES=all …round50/c1-supplement.py     (candidate and base): 5/5 C1_SUPPLEMENT=PASS exit=0
```

Cause, and it is round-51 drift, not v4: both round-49 and round-50 predicates were frozen on the all-token reading of
citations, and the round-51 tool made `source`-only the default with `ASSIMILATE_CITES` as the escape (tool docstring,
lines 86-87: "it restores the round-49 counter (`ASSIMILATE_CITES=all …` passes) but not the round-50"). P7's expected
`DIFF` set is a 3-line all-token set (`missing ROWRECHECK S014 2026-12-01`, `missing STRIPPED S014 recheck`,
`unexpected ROWRECHECK S014 <nonce>`), while the source-only default observes 21 findings against 26 expected
(`findings=21 expected=26`, 21 DIFF lines: `BODYONLY`/`BODYCLASH` lines in, 13 MAP/ROW/STRIPPED/ENTRYCITES lines
missing) — reproduced by hand on a scratch copy of the pinned package. Under `ASSIMILATE_CITES=all` the observed set is
exactly those 3 lines and P7 passes on both tools.
Reproducibility: each counter run twice per mode — `2/3 FAIL` ×2,
`3/3 PASS` ×2, `3/5 FAIL` ×2, `4/5 FAIL` ×2, and `round51/c1-count.py` 3× per tool all `LEGS=5/5`.

## 4. Why the round-50 counter reads `5/5` for base and `4/5` for the candidate under `cites=all`

`SELFTEST_DEFAULT` runs the *lane* tool (there is no `--tool` for it, by its own design), so with `--tool` the base row
skips the leg. Probed directly at the same package and env — base: `SELFTEST=FAIL findings=37 expected=28`; candidate:
`SELFTEST=FAIL findings=49 expected=40`. Both fail; the default fixture root is the source-mode package, so an ambient
`ASSIMILATE_CITES=all` breaks it for either tool. The leg-set difference is the counter's `--tool` skip, not behaviour.

## 5. Risks / notes for the L1 (report only, no change proposed)

- v4 stales the round-51 receipt under `receipt-check.py` at HEAD (`RECEIPT_TOOL_MOVED rev=41b4dca86fc8
  tool=tools/assimilate-rows.py`); at `--tip 5b55013` it is `RECEIPT_OK`. This is the checker working as designed (a
  receipt that measures code the tip no longer has), but the round-53 after-receipt must pin the new tool revision or
  the check stays red. `round52/measure-after.txt` pins `tools/capture-text.py`, so it is unaffected.
- Round-49 and round-50 frozen counters are only green under `ASSIMILATE_CITES=all`; the round-51 counter and supplement
  are green in both env and in both tools. Any future leg that runs them without that env will read red for reasons
  unrelated to v4.
- Not measured here (out of this seat): the round-53 `c1-count.py` legs and the C2 counter; the v4 behaviour on the
  campaign package; anything needing the registry beyond what these counters read.

VERDICT: ran all ten historical checks (round-49 count +cites-all, round-50 count +cites-all, round-50 supplement, round-51 count ×3, round-51 supplement, receipt-check --help and on the round-52 receipt, lane selftest) against candidate `32aab5e` and base `5b55013` — no regression attributable to v4; the single difference is the intended `twin` label (base `DIFF missing MAP S017->S021 twin` / `unexpected … held`, candidate `SELFTEST=PASS 40/40`, live `CITED=6 APPEND=2 HELD=3 TWIN=1`), and the three red legs (round-49 default, round-50 default, round-50 P7) reproduce identically on the base tool and turn green on both under `ASSIMILATE_CITES=all`.
