# R51ExecFixturePerturb — eight perturbations of the new lane default fixtures

Seat R51ExecFixturePerturb, round 51 wave 1. Only write: this file. Lane tree untouched (`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain -- tools/assimilate-rows.py corpus/fixtures/assimilate-selftest` printed nothing).

Pinned revisions (read-only): lane HEAD `cfe6c9fb9b56fa80a3005c1a3aaa522b29966306`; `tools/assimilate-rows.py` blob `091db821e0917d54a9eafd0aa4576f45819d6035`, last touched by `2a3389da0306e41f1b4797c1bc69017f23a38aef` (the C1 candidate). Baseline fixture identity, as the tool itself prints it: `FIXTURES_SHA256=d778c7f58036f76a2557824657a3ff5c1f2f490ea9350a6e40e43d218ed8c8a1`. Every perturbation below is a delta against that digest.

## Method

```
S=/dev/shm/chousa-r51-R51ExecFixturePerturb
cp -a corpus/fixtures/assimilate-selftest "$S/base"; for p in P1..P8; do cp -a "$S/base" "$S/$p"; done
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py --selftest \
  --fixtures "$S/P<n>" --expected "$S/P<n>/expected.json"
```
Baseline run: `rc=0`, `SELFTEST=PASS findings=25 expected=25`, digest `d778c7f5…c8a1`. Each copy got exactly one edit; `diff -ru base P<n>` output is quoted per item. DIFF lines are shown verbatim where few; where a refusal collapsed the run I give the exact counts (`missing`/`unexpected`) and quote every line that names the perturbed object — no line is invented and none is dropped from the counts.

| P | perturbation | rc | findings/expected | names the perturbed finding? |
|---|---|---|---|---|
| P1 | drop registry `S020` row | 1 | 29/25 (18 missing, 22 unexpected) | yes — `missing MAP S014->S020 held` |
| P2 | `\|`→`|` in staged S015 URL | 1 | 3/25 (24 missing, 3 unexpected) | yes — `REFUSED S015: staged row has 12 cells, not 11` |
| P3 | delete b.md `source: S014` line | 1 | 25/25 (2 missing, 2 unexpected) | yes — `missing MAP S014->S020 held` |
| P4 | body-only mention of cited ids in a.md | 0 | 25/25 | n/a — **PASS** |
| P5 | rename `## Registry` heading | 1 | 4/25 (24 missing, 3 unexpected) | yes — `REFUSED registry has no \`## Registry\` heading` |
| P6 | delete expected BODYCLASH line | 1 | 25/24 (0 missing, 1 unexpected) | yes — `unexpected BODYCLASH corpus/knowledge/b.md S011` |
| P7 | swap the two entries (contents exchanged) | 1 | 26/25 (7 missing, 8 unexpected) | yes — ROWUSEDBY/ENTRYCITES flip a.md↔b.md |
| P7b | swap two `source:` lines inside b.md | 0 | 25/25 | n/a — **PASS** |
| P8 | `S012` registry row indented 4 spaces | 1 | 25/25 (1 missing, 1 unexpected) | yes — `missing COLLISIONS S011,S012` |

## Per-perturbation evidence

### P1 — drop the registry S020 escaped-pipe row
`diff -ru base P1`: `-| S020 | Piped doc \| alt — https://example.test/piped | … | 90d | — |`
`rc=1`, `SELFTEST=FAIL findings=29 expected=25`. Naming lines: `DIFF missing MAP S014->S020 held`, `DIFF unexpected MAP S014->S015 append`, plus `unexpected MAP S010->S013 append` / `MAP S013->S014 append` and 19 further lane-id renames. Detected, and it names S020. Side observation: with S020 gone the mint base falls to the new registry maximum S012, so **every** appended id renumbers (S021/S022→S013/S014/S015); the tool has no independent check that a registry is complete, so a dropped row silently renumbers the append block and only `expected.json` notices.

### P2 — remove the `\|` from the staged S015 URL
`diff -ru base P2`: `-| S015 | … https://example.test/other\| alt |` / `+| S015 | … https://example.test/other| alt |`
`rc=1`, `SELFTEST=FAIL findings=3 expected=25`; the three findings are `TOOLEXIT 1`, `REFUSED S015: staged row has 12 cells, not 11`, `COLLISIONS S011,S012`. Detected and named, fail-closed (nothing claimed). Mechanism: the raw pipe is caught by the escaped-pipe splitter's cell count (`ESC_SPLIT`, `tools/assimilate-rows.py:102`), **not** by URL identity — `url_of` (`:110`) stops at the raw `|` and would still have yielded `example.test/other`, i.e. the same document. D2 is the load-bearing guard here, not D1.

### P3 — delete a `source:` line of b.md
`diff -ru base P3`: `-source: S014 — https://example.test/piped — section 5`
`rc=1`, `SELFTEST=FAIL findings=25 expected=25` (counts cancel), full DIFF set:
```
DIFF missing ENTRYCITES corpus/knowledge/b.md S001,S002,S011,S020
DIFF missing MAP S014->S020 held
DIFF unexpected BODYONLY corpus/knowledge/b.md S014
DIFF unexpected ENTRYCITES corpus/knowledge/b.md S001,S002,S011,S014
```
Detected and named (S014). This is the intended `--cites source` semantics: the still-present body mention of S014 becomes body-only instead of cited. No BODYCLASH for S014 because S014 is not a lane id — the clash arm stays covered by S011.

### P4 — add a body-only mention of a cited id to a.md
`diff -ru base P4`: `+- The first document (S010) and the third (S013) are mentioned again in the body.`
`rc=0`, `SELFTEST=PASS findings=25 expected=25`, digest `845c402b…1244`. The PASS is informative, not vacuous: a direct run on the copy rewrote the new line to `- The first document (S021) and the third (S022) are mentioned again in the body.` and `bodyonly.tsv` stayed `a.md S016` / `b.md S011`. A body mention of an already-cited id is substituted but never counted — correct under the frozen C1 predicate.

### P5 — rename the registry heading
`diff -ru base P5`: `-## Registry` / `+## Registry of sources`
`rc=1`, `SELFTEST=FAIL findings=4 expected=25`; unexpected lines:
```
DIFF unexpected REFUSED registry has no `## Registry` heading
DIFF unexpected REFUSED registry rows outside the Registry section: S001, S002, S011, S012, S020
DIFF unexpected TOOLEXIT 1
```
Detected and named; D3 refuses. Nit: the second REFUSED line is misleading — with no Registry heading `seen` is False and `inside` stays False, so `registry_problems` (`:168-186`, append at `:184-185`) reports every row as "outside the Registry section" of a section that does not exist. Refusal is still correct and fail-closed.

### P6 — delete the expected BODYCLASH line
`diff -ru base P6`: `- "BODYCLASH corpus/knowledge/b.md S011",`
`rc=1`, `SELFTEST=FAIL findings=25 expected=24`, single DIFF: `DIFF unexpected BODYCLASH corpus/knowledge/b.md S011`. Detected and named. Proves `expected.json` is a human-authored tripwire, not derived from the tool's own output.

### P7 — swap two entries (two readings, both run)
(a) contents exchanged between `a.md` and `b.md` (`diff -ru base P7` shows the three `source:` lines and `# Entry A`/`# Entry B` swapping files). `rc=1`, `SELFTEST=FAIL findings=26 expected=25`, full DIFF set:
```
DIFF missing BODYCLASH corpus/knowledge/b.md S011
DIFF missing BODYONLY corpus/knowledge/a.md S016
DIFF missing BODYONLY corpus/knowledge/b.md S011
DIFF missing ENTRYCITES corpus/knowledge/a.md S003,S016,S021,S022
DIFF missing ENTRYCITES corpus/knowledge/b.md S001,S002,S011,S020
DIFF missing ROWUSEDBY S021 corpus/knowledge/a.md
DIFF missing ROWUSEDBY S022 corpus/knowledge/a.md
DIFF unexpected BODYCLASH corpus/knowledge/a.md S011
DIFF unexpected BODYONLY corpus/knowledge/a.md S011
DIFF unexpected BODYONLY corpus/knowledge/b.md S016
DIFF unexpected ENTRYCITES corpus/knowledge/a.md S001,S002,S011,S020
DIFF unexpected ENTRYCITES corpus/knowledge/b.md S003,S016,S021,S022
DIFF unexpected ROWUSEDBY S021 corpus/knowledge/b.md
DIFF unexpected ROWUSEDBY S022 corpus/knowledge/b.md
DIFF unexpected STRIPPED S021 used-by
```
Detected; every naming line points at the swapped entry paths. (b) pure order — swap b.md's `source: S012` and `source: S014` lines: `rc=0`, `SELFTEST=PASS`, digest `fe13d2b1…d1a1`. Citation order is not load-bearing (`cited` is sorted by id), so the entry-level order the fixture actually encodes is filename sort, which a content swap is the observable form of.

### P8 — registry row indented 4 spaces
`diff -ru base P8`: `-| S012 | Last doc — … |` / `+    | S012 | Last doc — … |`
`rc=1`, `SELFTEST=FAIL findings=25 expected=25`, full DIFF set:
```
DIFF missing COLLISIONS S011,S012
DIFF unexpected COLLISIONS S011
```
Detected and named (S012), but only through the pinned COLLISIONS line. The child itself exited 0 and said nothing: a direct run printed `COLLISIONS=1`, `CITED=5 APPEND=2 HELD=3`, `BODYONLY=2`, `rc=0`, no REFUSED, no WARN naming S012, and `reg-ids` was `S001 S002 S011 S020` — S012 simply vanished. `ROW_RE`/`GREP_RE` both bound the indent at `{0,3}` (`tools/assimilate-rows.py:99-100`), and `registry_problems` reuses `ROW_RE` (`:180`), so a row indented 4+ spaces is neither counted, nor used as a mint base, nor refused as "outside the Registry section". The 0-3 bound is documented in the tool docstring, so this is a documented limit and not a C1 falsification; it is an unguarded edge, and no fixture case pins the "silently dropped" outcome except by COLLISIONS. Lane registry checked for it: `^ {4,}\s*\|\s*S\d{3,}` matched nothing in `corpus/SOURCES.md` or the staged `SOURCES.append.md`, so no current lane row is lost this way. Decision for L1, not this seat: either widen the row grammar (changes both the collision count and D3's detector) or state the 0-3 bound as registry grammar in QUALITY/PROVINCE.

## Surviving perturbations

P4 and P7b both survive (`SELFTEST=PASS`), and both should: they are perturbations the frozen predicate says are irrelevant — a body mention of an id that is already cited, and the order of `source:` lines within an entry. Neither weakens a finding: P4's PASS still proves the new body occurrence is substituted, and P7b's PASS still proves all five maps/rows. No perturbation that removes, renames, re-identifies or reorders a document, an entry or a registry row survived. The one survival that would be wrong — a registry row made invisible by 4-space indentation — is not silent at the selftest level (P8 fails) but is silent at the tool level.

## Tooling

No install or upgrade. Note: the session shell's builtin `grep` (`grep (pi-uu-grep) 0.2.0`) returned 0 matches for `grep -E '^[-+][^-+]'` on a file whose line 8 begins `+- `; evidence was re-collected with `diff -ru` and `awk`, and the anomaly reported to `xd://report_issue`. Scratch `/dev/shm/chousa-r51-R51ExecFixturePerturb` deleted.

VERDICT: attacked the new default fixture package with eight perturbations (plus one order variant) — all seven destructive perturbations are detected and named (P1/P2/P3/P5/P6/P7/P8, rc=1), P4 and P7b correctly survive, and P8 exposes an unguarded 4-space-indent edge where a registry row disappears with exit 0.
