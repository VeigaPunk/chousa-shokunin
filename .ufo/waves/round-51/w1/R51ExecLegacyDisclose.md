# R51ExecLegacyDisclose — what the older one-shot counters print at the C1 candidate

axes: calibration (a counter's revision and fixture semantics are named, not implied) · operability (does the round-49/50 tooling still run) · depth (the new default package is shown, not asserted). scratch: `/dev/shm/chousa-r51-R51ExecLegacyDisclose/` and `/dev/shm/chousa-r51-legacy-git.9Ty7MM`, both removed at the end. No install, no network, no lane write except this report.

## 1. Harness

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 2a3389da0306e41f1b4797c1bc69017f23a38aef | tar -x -C /dev/shm/chousa-r51-R51ExecLegacyDisclose/tree ; echo $?   →  0
$ cd /dev/shm/chousa-r51-R51ExecLegacyDisclose/tree && sha256sum tools/assimilate-rows.py
bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d  tools/assimilate-rows.py
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --quiet 2a3389d HEAD -- corpus/fixtures/assimilate-selftest tools/assimilate-rows.py SKILL.md ; echo $?   →  0
$ echo "[${ASSIMILATE_CITES-unset}]"   →  [unset]     # (a) below is literally the unmodified environment
```

`echo $? 0` on the `diff --quiet` means the candidate's tool, default fixtures and `SKILL.md` are byte-identical to tip `cfe6c9f`. The export alone cannot reach the round-49 legs: `corpus/evidence/round49/c1-count.py:46,366-371` derives `LANE = __file__.parents[3]` and runs `git -C LANE archive 414a2ec6… corpus` / `ls-tree`; a `git archive` export has no `.git`, so both modes print `NO_BASE_REV` exit 2 before any leg. So I built a second harness with the same candidate bytes and a real object store — no commit, no branch change:

```
$ D=$(mktemp -d -p /dev/shm chousa-r51-legacy-git.XXXXXX) && git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/chousa-shokunin "$D" && cp -a /dev/shm/chousa-r51-R51ExecLegacyDisclose/tree/. "$D"/
$ git -C "$D" rev-parse --show-toplevel ; git -C "$D" cat-file -t 414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
/dev/shm/chousa-r51-legacy-git.9Ty7MM
commit
$ sha256sum "$D"/tools/assimilate-rows.py   →  bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d
```

`$D`'s HEAD is `cfe6c9f`; its working tree is `2a3389d`'s bytes; the counters read only its object store.

## 2. Every leg line and exit code

Leg lines verbatim, one row per counter and mode. `P1…P6` are the six perturbation lines, identical in all four round-50 runs: `PERTURB P1 applied=1 rc=1 -> PASS` … `PERTURB P6 applied=1 rc=1 -> PASS`.

| counter (harness) | (a) no env change | exit | (b) `ASSIMILATE_CITES=all` | exit |
|---|---|---|---|---|
| `round49/c1-count.py` (export) | `BASE_REV=414a2ec…` · `TOOL=present sha256=bdaf80f4…` · `NO_BASE_REV` | 2 | identical | 2 |
| `round49/c1-count.py` ($D) | `SET_A … BY_DOC=9/9 REWRITE=2/2 … PASS` · `SET_B … BY_DOC=3/3 REWRITE=1/1 … PASS` · `SET_C … BY_DOC=3/5 REWRITE=0/1 … FAIL` · `GUARD … COLLISIONS=['S002'] PASS` · `PIPE … CELLS=11 RECHECK=90d … PASS` · `SETS_PASS=2/3` · `C1=FAIL` | 1 | `SET_A PASS` · `SET_B PASS` · `SET_C … BY_DOC=5/5 REWRITE=1/1 … PASS` · `GUARD PASS` · `PIPE PASS` · `SETS_PASS=3/3` · `C1=PASS` | 0 |
| `round50/c1-count.py` (export) | `SELFTEST_DEFAULT=PASS` · `BASELINE=FAIL rc=1 findings=?` · `PERTURB_PASS=6/6` · `EXPECTED_BAD=PASS rc=2` · `R49_REGRESSION=FAIL rc=2` · `LEGS=3/5` · `C1=FAIL` | 1 | `SELFTEST_DEFAULT=FAIL` · `BASELINE=PASS rc=0 findings=26` · `PERTURB_PASS=6/6` · `EXPECTED_BAD=PASS rc=2` · `R49_REGRESSION=FAIL rc=2` · `LEGS=3/5` · `C1=FAIL` | 1 |
| `round50/c1-count.py` ($D) | same as export but `R49_REGRESSION=FAIL rc=1` | 1 | `SELFTEST_DEFAULT=FAIL` · `BASELINE=PASS rc=0 findings=26` · `PERTURB_PASS=6/6` · `EXPECTED_BAD=PASS rc=2` · `R49_REGRESSION=PASS rc=0` · `LEGS=4/5` · `C1=FAIL` | 1 |
| `round50/c1-supplement.py` (export) | `P7_NONCE_EXCLUSIVE=FAIL` · `H1_DUPLICATE_EXPECTED=PASS` · `H2_NO_ENTRY=PASS` · `H3_OPTION_CLASH=PASS` · `H4_ENTRYCITES_DASH=PASS` · `SUPPLEMENT_LEGS=4/5` · `C1_SUPPLEMENT=FAIL` | 1 | all five `=PASS` · `SUPPLEMENT_LEGS=5/5` · `C1_SUPPLEMENT=PASS` | 0 |
| `round51/c1-count.py` ((a) in export, (b) in `$D` — same bytes, no git use) | `SELFTEST_DEFAULT=PASS` · `LEGACY_ALL=PASS rc=0` · `SOURCE_ONLY=PASS default_rc=0 map=['S722','S780'] appended=1 bodyonly=[['corpus/knowledge/e.md','S535']] all_rc=0 all_map=['S535','S722','S780']` · `PIPE_IDENTITY=PASS d1=ok d2=ok` · `REGISTRY_STRUCTURE=PASS 4/4` · `LEGS=5/5` · `C1=PASS` | 0 | `SELFTEST_DEFAULT=FAIL` · `LEGACY_ALL=PASS rc=0` · `SOURCE_ONLY=FAIL default_rc=0 map=['S700','S719','S834'] appended=2 bodyonly=[] all_rc=0 all_map=['S700','S719','S834']` · `PIPE_IDENTITY=PASS` · `REGISTRY_STRUCTURE=PASS 4/4` · `LEGS=3/5` · `C1=FAIL` | 1 |

`SET_C` in full, the one round-49 leg the change moves: `SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=3/5 EXTRA=0 REWRITE=0/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> FAIL`. The round-51 counter seeds from `os.urandom` (`c1-count.py:101`), so its `SOURCE_ONLY` id lists differ run to run (`['S722','S780']` vs `['S693','S787']`); every other printed line is stable.

## 3. Which leg fails under (b), and why

| counter | leg failing under (b) | cause |
|---|---|---|
| `round49/c1-count.py` | **none** — `SETS_PASS=3/3`, `C1=PASS`, exit 0 | its expectation is the round-50 all-ids reading; the pin restores agreement |
| `round50/c1-count.py` | `SELFTEST_DEFAULT` (leg 1) | leg 1 runs `tool --selftest` with no flags, i.e. the **lane default package**, now the source-mode package; the env forces all-mode on it → `SELFTEST=FAIL findings=35 expected=25` |
| `round50/c1-supplement.py` | **none** — `SUPPLEMENT_LEGS=5/5`, exit 0 | only its nonce leg depends on citation mode; the pin restores the exclusive set |

Under (a) the failures are the mirror image: round-49 `SET_C` (5 body ids against the 3 ids on the entry's `source:` lines), round-50 `BASELINE` + `R49_REGRESSION`, supplement `P7`.

**The lane default package is the source-mode package — shown, not asserted.** The tool's own digest of `corpus/fixtures/assimilate-selftest/` is `d778c7f5…`, and 3 of its 25 expected findings are `BODYONLY`/`BODYCLASH` — the kinds `tools/assimilate-rows.py:64` marks "(source mode only)":

```
$ python3 tools/assimilate-rows.py --selftest
FINDING BODYONLY corpus/knowledge/a.md S016
FINDING BODYONLY corpus/knowledge/b.md S011
FINDING BODYCLASH corpus/knowledge/b.md S011
FIXTURES_SHA256=d778c7f58036f76a2557824657a3ff5c1f2f490ea9350a6e40e43d218ed8c8a1
SELFTEST=PASS findings=25 expected=25                      exit 0
$ python3 tools/assimilate-rows.py --selftest --cites all      # same package, other mode
DIFF missing BODYONLY corpus/knowledge/a.md S016
DIFF missing BODYONLY corpus/knowledge/b.md S011
DIFF missing BODYCLASH corpus/knowledge/b.md S011
SELFTEST=FAIL findings=35 expected=25                      exit 1   # same FIXTURES_SHA256=d778c7f5…
```

The round-50 pinned package is the other one and is unmodified (`PIN_CHANGED` never fired; its digest equals the counter's pin `c5c56480…`, 26 findings, 0 `BODYONLY`/`BODYCLASH`): `--fixtures corpus/evidence/round50/c1-fixtures` prints `SELFTEST=FAIL findings=20 expected=26` exit 1 by default and `SELFTEST=PASS findings=26 expected=26` exit 0 with `--cites all`. So round-50's two legs are **mutually exclusive** at the candidate: no single mode makes `SELFTEST_DEFAULT` and `BASELINE` both pass, and the counter has no mode switch of its own. The tool's own docstring says it (`tools/assimilate-rows.py:66-68`: "the round-50 pinned package needs `all` … the frozen round-49 and round-50 counters call the tool with no flag and need `all`; an explicit `--cites` wins").

P7's exclusive set under (a) is 17 lines, not 3 — the nonce still appears and S014 is still renumbered, but S015 (body-only in `a.md`) vanishes and S014 loses its used-by/stripped findings:

```
default: rc=1 ndiff=17   DIFF missing ROWRECHECK S014 2026-12-01 … DIFF unexpected ROWRECHECK S014 re-verify-fa0961c7 …
all:     rc=1 ndiff=3    DIFF missing ROWRECHECK S014 2026-12-01 / DIFF missing STRIPPED S014 recheck / DIFF unexpected ROWRECHECK S014 re-verify-fa0961c7
```

## 4. Harmed, or tied to the earlier revision?

**Tied to the earlier tool revision.** A neutral reader with this receipt has to say the change did not damage the older instruments, because each still reaches its own verdict at the candidate's own bytes (`bdaf80f4…`, the sha the counters print) once the single documented knob is set: round-49 `SETS_PASS=3/3 C1=PASS` exit 0, supplement `SUPPLEMENT_LEGS=5/5` exit 0, round-50's six perturbations and `EXPECTED_BAD` unchanged in both modes, the round-50 fixture package untouched (`c5c56480…` = its pin, printed on every run). No older counter was edited; the new default is a *new* package and the old semantics survive behind one env variable the tool documents.

Two facts stop it being a clean "unharmed": (i) with no env change each older counter prints `C1=FAIL` (round-50 `LEGS=3/5`, supplement 4/5) — the default flipped, so an unqualified re-run is red; (ii) the SKILL row still states the old default numbers (`SKILL.md:130`: "lane default … `SELFTEST=PASS findings=26 expected=26`, `FIXTURES_SHA256=c5c56480…`"), false at the tip (observed `findings=25 expected=25`, `d778c7f5…`). That stale row, not a broken counter, is the one thing a reader would call harm.

## 5. Proposed SKILL.md gate-row sentence

Replace, in the `assimilate-rows` row's notes cell (`SKILL.md:130`), the fragment from "lane default (no flags, fixtures `corpus/fixtures/assimilate-selftest/`) →" through "exit 0" with exactly:

> lane default (no flags, fixtures `corpus/fixtures/assimilate-selftest/`, source mode) → `SELFTEST=PASS findings=25 expected=25`, `FIXTURES_SHA256=d778c7f58036f76a2557824657a3ff5c1f2f490ea9350a6e40e43d218ed8c8a1`, exit 0; the round-50 pinned package `corpus/evidence/round50/c1-fixtures/` (`FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, `findings=26 expected=26`) is the all-mode package and passes only with `--cites all` or `ASSIMILATE_CITES=all`, which the frozen round-49 and round-50 counters need at the r51 candidate `2a3389da0306e41f1b4797c1bc69017f23a38aef` (tool sha256 `bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d`): there `round49/c1-count.py` prints `SETS_PASS=3/3 C1=PASS` exit 0 and `round50/c1-count.py` prints `LEGS=4/5 C1=FAIL` exit 1 (`SELFTEST_DEFAULT=FAIL`) under that pin, and `LEGS=3/5` exit 1 with no env change.

## 6. Side finding (outside the item, for the L1's decision)

The round-51 counter is not hermetic against the same variable: `corpus/evidence/round51/c1-count.py:106,148` run the default-mode legs with no `--cites` and no env scrub, so `ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py` prints `LEGS=3/5 C1=FAIL` exit 1 (`SELFTEST_DEFAULT=FAIL`, `SOURCE_ONLY=FAIL … bodyonly=[]`); its `LEGACY_ALL` leg passes an explicit `--cites all` and is unaffected. One-line fix: `env={**os.environ, "ASSIMILATE_CITES": "source"}` in `run()` plus `"--cites","source"` on the default-mode `adopt()` call.

## Risks / blockers

- The export-tree leg of `round49/c1-count.py` is unmeasurable by construction (`NO_BASE_REV`, exit 2, both modes); any round-51 receipt citing its numbers must name the git-backed harness, not a bare export.
- `round50/c1-count.py`'s `R49_REGRESSION` leg inherits the ambient `ASSIMILATE_CITES` into the child, so one line reads `FAIL rc=2` (no git), `FAIL rc=1` (git, no env) and `PASS rc=0` (git, all) — three causes for one line.
- No SKILL/QUALITY edit was made; §5 is a draft sentence for the L1. Nothing committed; no index or jj state touched.

VERDICT — attacked the claim that the older one-shot counters still disclose the C1 candidate: ran every leg of round-49, round-50 and the supplement in both modes plus round-51 (a) and (b), in a `git archive` export and in a git-backed copy of the same bytes; round-49 is fully green under `ASSIMILATE_CITES=all` (`SETS_PASS=3/3`, exit 0) and fails only `SET_C` without it, round-50 can never reach 5/5 because its default leg reads the new source-mode package (`d778c7f5…`, 25 findings) while its pinned package is all-mode (`c5c56480…`, 26), and the supplement's P7 needs the pin (3 vs 17 DIFF lines); verdict "tied to the earlier revision", with the stale `SKILL.md:130` numbers the only real harm and a replacement sentence drafted.
