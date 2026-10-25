# R50MutSelftestV2 — mutation test of the hardened `assimilate-rows.py --selftest` (round 50, wave 2)

Attacked: the seven hardening behaviors of `tools/assimilate-rows.py` disclosed in
`corpus/evidence/round50/claims-erratum.md` §1 (multiset compare, work floor, option
clash, ENTRYCITES dash, 120 s child timeout, tab-free findings,
fixtures-check-before-expected-read). Tested bytes: lane working-tree tool, sha256
`382aca9b7e314180ece70a9e1b34fc8622dbfaedf29f9d3efd51df1a94778cb5` (lane HEAD at test
time `c5b8dca8` — the lane advances during w2; claims frozen at `6a068f2a`). Detector:
the FROZEN counter `corpus/evidence/round50/c1-count.py` (never edited; its PIN
re-verified on every run) plus six out-of-counter probes. Scratch
`/dev/shm/chousa-r50-R50MutSelftestV2` (deleted at end). No tools installed (none
needed); pacman untouched. Mutants are scratch copies run with explicit paths; the
lane file was never opened for write.

## Pristine baseline

```
$ python3 $S/lane/tools/pristine.py --selftest --fixtures $S/c1-fixtures --expected $S/c1-fixtures/expected.json
FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43   # == counter PIN
SELFTEST=PASS findings=26 expected=26                                              # rc=0
$ python3 corpus/evidence/round50/c1-count.py                                      # full frozen counter
BASELINE=PASS rc=0 findings=26 · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS rc=2 ·
R49_REGRESSION=PASS rc=0 · LEGS=5/5 · C1=PASS                                      # rc=0, 1.8 s
```
Detector has teeth: `c1-count.py --tool corpus/evidence/round50/controls/echo-tool.py`
→ `BASELINE=PASS`, `PERTURB_PASS=0/6`, `EXPECTED_BAD=PASS rc=2`, `LEGS=4/5`, `C1=FAIL`, exit 1 observed.

## Mutants (single-point diffs verified against pristine with diff)

| # | pristine line | mutation | sha256 head |
|---|---|---|---|
| M1 | 232–233 | `collections.Counter(want/got)`+`.elements()` → `set(want/got)`+set difference | a650e8bf |
| M2 | 219–221 | knowledge-entry work floor block deleted | d86273e4 |
| M3 | 254–256 | `--selftest` option-clash guard deleted | d061ae2a |
| M4 | 195 | `','.join(ids) if ids else '-'` → `','.join(ids)` | 9c0e561c |
| M5 | 201 | `return [f.replace("\t"," ") for f in found]` → `return found` | 5d66a83e |
| M6 | 168 | `subprocess.run(..., timeout=120)` → timeout kwarg removed | 8da07fa0 |
| M7 | 216–218→226–228 | fixtures check relocated after the expected read | 1118db58 |

## Frozen counter vs mutants: kills 0/7

```
$ python3 corpus/evidence/round50/c1-count.py --tool $S/lane/tools/mutN.py   # N=1..7, ~2 s each
every run: BASELINE=PASS rc=0 findings=26 · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS rc=2 ·
R49_REGRESSION=PASS rc=0 · LEGS=5/5 · C1=PASS · counter-rc=0
```
Why: the six perturbations perturb fixture inputs (adopter behavior), EXPECTED_BAD
covers only the expected-read path, and the round-49 leg drives the tool in normal
mode (its `run_tool` builds `--staged/--knowledge/--registry/--out`, never
`--selftest`). No counter leg reaches any hardening behavior.

## Probes (scratch fixtures; expected files hand-written per the docstring contract)

- A duplicate-expected: c1-fixtures copy with ` "COLLISIONS S011,S012",` twice.
- B no-entry: staged.md+registry.md only; expected `["TOOLEXIT 0","COLLISIONS S011,S012"]`.
- C option clash: `--selftest --staged x --fixtures <pinned> --expected <pinned>`.
- D id-less-entry: + `knowledge/corpus/knowledge/c.md` citing no S-token; expected adds
  ` "ENTRYCITES corpus/knowledge/c.md -",`.
- E tab finding: + `knowledge/corpus/knowledge/x<TAB>y.md` holding invalid UTF-8;
  expected `["TOOLEXIT 1","REFUSED entry not UTF-8: corpus/knowledge/x y.md","COLLISIONS S011,S012"]`.
- F fixtures-order: `--selftest --fixtures $S/probes/nosuch` (dir lacking staged.md).
- F′ order2: fixtures with knowledge/ but no staged.md and no expected.json.

Results (rc + decisive lines; unlisted mutants agree with pristine):
- A: pristine, M2–M7 rc=1 `DIFF missing COLLISIONS S011,S012`; **M1 rc=0 `SELFTEST=PASS
  findings=26 expected=27`** — a duplicated expected finding passes.
- B: pristine, M1, M3–M7 rc=2 `SELFTEST=ERROR … no knowledge entry`; **M2 rc=0
  `SELFTEST=PASS findings=2 expected=2`** — an entry-less selftest passes.
- C: pristine, M1, M2, M4–M7 rc=2 stderr `assimilate-rows: --selftest takes only
  --fixtures and --expected`; **M3 rc=0 `SELFTEST=PASS findings=26`** — `--staged x`
  silently ignored.
- D: pristine, M1–M3, M5–M7 rc=0 PASS 27/27; **M4 rc=1 `DIFF missing ENTRYCITES
  corpus/knowledge/c.md -` + `DIFF unexpected ENTRYCITES corpus/knowledge/c.md `**
  (trailing space, no dash).
- E: pristine, M1–M4, M6, M7 rc=0 PASS 3/3; **M5 rc=1 `DIFF unexpected REFUSED entry
  not UTF-8: corpus/knowledge/x\ty.md`** — a raw tab (0x09) reaches the finding line.
- F: pristine rc=2 `SELFTEST=ERROR …: staged.md or registry.md missing`; **M7 rc=2
  `SELFTEST=ERROR …: no knowledge entry — …`** (misattributes a missing-staged
  fixture as entry-less).
- F′: pristine rc=2 `SELFTEST=ERROR fixtures …: staged.md or registry.md missing`;
  **M7 rc=2 `SELFTEST=ERROR expected file …/expected.json: [Errno 2] No such file or
  directory`** — blames the expected file while the fixtures are the broken part.

## Verdicts

| mutant | frozen counter | killed by | verdict |
|---|---|---|---|
| M1 multiset→set | survived | probe A only | gap in frozen counter |
| M2 work floor removed | survived | probe B only | gap |
| M3 option clash removed | survived | probe C only | gap |
| M4 ENTRYCITES dash removed | survived | probe D only | gap |
| M5 tab filter removed | survived | probe E only | gap |
| M6 timeout removed | survived | nothing | not killable without a hang |
| M7 fixtures-check order | survived | probes F/F′ only | gap |

M6, stated as required: killing it needs a fixture whose child run exceeds 120 s, so
the detector itself blocks ≥120 s first — the tool's selftest would hang, and the
frozen counter only recovers via its own `run()` timeout=120 (rc 124 → leg failure),
a kill that costs a guaranteed ≥120 s hang per leg. No cheap fixture hangs the child:
every child read is `is_file()`-gated (FIFOs and symlink loops are refused, not hung),
so M6 is reported survived, not falsified by any bounded detector.

## Coverage finding (informational; frozen counter not edited)

The frozen counter's kill power over the hardened self-test is 0/7: M1–M5 and M7 are
killed only by probes outside it. The C1 predicate's own kill rule still holds (all
legs passed on pristine; echo-tool fails PERTURB), so this is a counter-coverage gap,
not a claim defect. The six probe designs above are the missing legs; per tasking
they are recorded here, not added to the counter.

## Restoration evidence

- Lane tool sha256 before = after all runs:
  `382aca9b7e314180ece70a9e1b34fc8622dbfaedf29f9d3efd51df1a94778cb5`; the lane file
  was never opened for write; no git/jj state touched.
- Pinned fixtures: every counter run re-verified `FIXTURES_SHA256` == PIN
  `c5c56480…` (BASELINE=PASS embeds that check); final pristine re-run after all
  mutant runs → `SELFTEST=PASS findings=26 expected=26` rc=0 (restored-bytes leg).
- Transient /tmp writes were made only by FROZEN code (counter's perturbation
  `mkdtemp`, the tool's `observe()` mkdtemp, round-49 counter's TemporaryDirectory),
  each cleaned by its own finally; all seat-owned scratch was under
  `/dev/shm/chousa-r50-R50MutSelftestV2` and is deleted (closing line below).

VERDICT: attacked the seven hardening behaviors of `assimilate-rows.py --selftest`
with seven single-point mutants — frozen counter kills 0/7 (every run C1=PASS);
out-of-counter probes kill 6/7 (M1 multiset, M2 floor, M3 clash, M4 dash, M5 tab,
M7 check order, each by exactly one probe), M6 timeout survived (not killable
without a hang): coverage gap in the frozen counter found, contract unchanged.
