# R51MutAdopter — C1 mutation test: 12 one-line mutants of `tools/assimilate-rows.py` (round 51 wave 1)

Target: lane commit `2a3389da0306e41f1b4797c1bc69017f23a38aef` (`git log -1 -- tools/assimilate-rows.py` → "round-51: assimilate-rows candidate (source-only citation, bodyonly/bodyclash, escaped-pipe identity, registry-structure refusal, --cites/ASSIMILATE_CITES) ..."), working tree clean for the file, sha256 `bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d`.
No tool installs (none needed; operator authorization noted, unused). Scratch `/dev/shm/chousa-r51-R51MutAdopter/` only; `TMPDIR` pointed there for every counter run, so counters wrote nothing outside it and stdout. Each mutant = pristine copy + ONE line (all 12 `diff`s logged in scratch; e.g. MUT5 `ESC_SPLIT.split(s.strip())` → `s.strip().split("|")`; MUT10 `cites = a.cites or …` → `cites = "source"`; MUT8/12 write → `pass`). One run aborted and was redone: MUT11 first edit left a stray `:` (SyntaxError caught by `py_compile` in the runner), fixed, rerun clean.
Detectors per mutant: `python3 corpus/evidence/round51/c1-count.py --tool <mutant>` (its `SELFTEST_DEFAULT` prints `PASS (skipped: --tool)` every run; `C1=` mirrors `LEGS`) and `python3 <mutant> --selftest --fixtures corpus/fixtures/assimilate-selftest`.

## Baselines (pristine)

```
$ python3 corpus/evidence/round51/c1-count.py
LEGACY_ALL=PASS rc=0
SOURCE_ONLY=PASS default_rc=0 map=['S756', 'S870'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S841']] all_rc=0 all_map=['S756', 'S841', 'S870']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
C1=PASS
$ python3 tools/assimilate-rows.py --selftest
FIXTURES_SHA256=d778c7f58036f76a2557824657a3ff5c1f2f490ea9350a6e40e43d218ed8c8a1
SELFTEST=PASS findings=25 expected=25
```

## Counter leg lines — `c1-count.py --tool mutNN.py` (unseeded; survivors re-run at `--seed 1` and `--seed 2`, identical result)

`LEGACY_ALL=PASS rc=0` in every run except MUT10 (`LEGACY_ALL=FAIL rc=1`); that line is elided below.

```
MUT01:
SOURCE_ONLY=FAIL default_rc=0 map=['S514', 'S649', 'S788'] appended=2 bodyonly=[] all_rc=0 all_map=['S514', 'S649', 'S788']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=4/5
MUT02:
SOURCE_ONLY=PASS default_rc=0 map=['S535', 'S769'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S735']] all_rc=0 all_map=['S535', 'S735', 'S769']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
MUT03:
SOURCE_ONLY=PASS default_rc=0 map=['S565', 'S712'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S710']] all_rc=0 all_map=['S565', 'S710', 'S712']
PIPE_IDENTITY=FAIL d1=no d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=4/5
MUT04:
SOURCE_ONLY=PASS default_rc=0 map=['S860', 'S884'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S780']] all_rc=0 all_map=['S780', 'S860', 'S884']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
MUT05:
SOURCE_ONLY=PASS default_rc=0 map=['S704', 'S743'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S607']] all_rc=0 all_map=['S607', 'S704', 'S743']
PIPE_IDENTITY=FAIL d1=ok d2=no
REGISTRY_STRUCTURE=PASS 4/4
LEGS=4/5
MUT06:
SOURCE_ONLY=PASS default_rc=0 map=['S560', 'S613'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S602']] all_rc=0 all_map=['S560', 'S602', 'S613']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
MUT07:
SOURCE_ONLY=PASS default_rc=0 map=['S676', 'S891'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S678']] all_rc=0 all_map=['S676', 'S678', 'S891']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=FAIL 3/4
LEGS=4/5
MUT08:
SOURCE_ONLY=FAIL default_rc=0 map=['S569', 'S894'] appended=1 bodyonly=[] all_rc=0 all_map=['S569', 'S639', 'S894']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=4/5
MUT09:
SOURCE_ONLY=PASS default_rc=0 map=['S558', 'S620'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S643']] all_rc=0 all_map=['S558', 'S620', 'S643']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
MUT10:
LEGACY_ALL=FAIL rc=1
SOURCE_ONLY=FAIL default_rc=0 map=['S668', 'S748'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S803']] all_rc=0 all_map=['S668', 'S748']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=3/5
MUT11:
SOURCE_ONLY=PASS default_rc=0 map=['S670', 'S832'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S890']] all_rc=0 all_map=['S670', 'S832', 'S890']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
MUT12:
SOURCE_ONLY=PASS default_rc=0 map=['S561', 'S849'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S586']] all_rc=0 all_map=['S561', 'S586', 'S849']
PIPE_IDENTITY=PASS d1=ok d2=ok
REGISTRY_STRUCTURE=PASS 4/4
LEGS=5/5
```

## Kill matrix (L_ALL / S_ONLY / PIPE / REG = counter legs; ST = `--selftest` on lane default fixtures, format `PASS findings expected`)

| mut | one-line defect | L_ALL | S_ONLY | PIPE | REG | ST | verdict |
|---|---|---|---|---|---|---|---|
| 01 | source_ids reads every line (drops the `source:` filter) | P | F | P | P | FAIL 35/25 | killed |
| 02 | source_ids requires `source: ` (space after the colon) | P | P | P | P | PASS 25/25 | **SURVIVES** |
| 03 | pipe_free dropped on staged identity (D1 off) | P | P | F d1 | P | FAIL 30/25 | killed |
| 04 | pipe_free dropped on registry identity | P | P | P | P | PASS 25/25 | **SURVIVES** |
| 05 | registry cells split on plain pipe (D2 off) | P | P | F d2 | P | FAIL 29/25 | killed |
| 06 | registry_problems drops missing-heading message | P | P | P | P | PASS 25/25 | **SURVIVES** |
| 07 | registry_problems drops outside-rows message | P | P | P | F 3/4 | PASS 25/25 | killed |
| 08 | bodyonly.tsv never written | P | F | P | P | FAIL 23/25 | killed |
| 09 | bodyonly scoped to the entry's own source_ids, not globally cited | P | P | P | P | PASS 25/25 | **SURVIVES** |
| 10 | `--cites all`/ASSIMILATE_CITES forced to source | F | F | P | P | PASS 25/25 | killed |
| 11 | used-by uses all tokens in source mode | P | P | P | P | PASS 25/25 | **SURVIVES** |
| 12 | bodyclash.tsv never written | P | P | P | P | FAIL 24/25 | killed |

MUT07's failing sub-leg, run directly: `REGISTRY row-outside rc=0 -> FAIL` (renamed-heading / no-heading / well-formed all PASS). MUT12's selftest diff: missing `BODYCLASH corpus/knowledge/b.md S011` (24 findings vs 25). Both lines observed verbatim in the runs above.

## Survivors — coverage findings, not contract changes. Kill case for each, empirically confirmed (pristine vs mutant on micro-packages in scratch)

- **MUT02** — a spaceless source line `source:S601 — https://…`. Confirmed: pristine `CITED=1`, `map=S601 S002 append`; mut02 `CITED=0`, `BODYONLY corpus/knowledge/e.md⇥S601`. Neither detector's fixtures contain a spaceless `source:` line.
- **MUT04** — registry row whose URL is directly followed by an escaped pipe (`… https://h4.example/held\|alt`). Confirmed: pristine `map=S601 S001 held`; mut04 `map=S601 S002 append` — mints a duplicate row for an already-held URL. Counter d2 and lane fixture S020 both place the pipe *before* the URL (`Piped doc \| alt — https://…`), where both readings find the same URL.
- **MUT06** — a registry missing the `## Registry` heading and carrying no S### rows. Confirmed: pristine exits 1 `REFUSED` (no heading); mut06 exits 0 and mints `S601->S001 append`. The counter's no-heading/renamed-heading registries still refuse under the mutant via the outside-rows arm, so REGISTRY_STRUCTURE stays 4/4.
- **MUT09** — an id cited by entry A on a `source:` line but only body-mentioned in entry B. Confirmed: pristine bodyonly empty; mut09 `bodyonly=corpus/knowledge/b.md⇥S601`. The counter uses one entry per leg; lane fixtures have no cross-entry case (body-only S016/S011 are cited by nobody).
- **MUT11** — `used-by` from all tokens: entry B body-mentions a staged id appended on entry A's `source:` line. Confirmed, appended S601 row used-by: pristine `corpus/knowledge/a.md`; mut11 `corpus/knowledge/a.md, corpus/knowledge/b.md`. No counter leg asserts ROWUSEDBY, and no lane entry mentions another's append twin (b.md never mentions S010/S013).

## Restoration

After all runs: `sha256sum tools/assimilate-rows.py` → `bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d` (unchanged); `cmp pristine.py <lane tool>` → identical; `git status --porcelain -- tools/assimilate-rows.py` → empty. Scratch `/dev/shm/chousa-r51-R51MutAdopter/` deleted on finish.
VERDICT: attacked the frozen C1 contract with 12 behaviour-class mutants of the candidate tool — 7 killed by the c1-count legs + lane selftest, 5 survivors (MUT02/04/06/09/11) are detector coverage gaps each shown against a confirmed killing case; no predicate/target/counter touched; lane tool byte-identical before and after.
