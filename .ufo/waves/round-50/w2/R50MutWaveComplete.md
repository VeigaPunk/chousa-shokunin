# R50MutWaveComplete — mutation test: corpus/evidence/round50/wave-complete-check.py

Target at lane HEAD c5b8dca85f759c7a772225fe036e7bb9a809b91c; pristine sha256
`1f449f1c61a87f890516851029451071db41e6055679ee598baaa945db07c0a1` (byte-identical after
the campaign — restoration below). No tool installs (operator rule noted; pacman paused;
none needed). Mutants + fixtures lived under `/dev/shm/chousa-r50-R50MutWaveComplete/`
(deleted at end). Rev-mode runs only READ the lane (`rev-parse`, `ls-tree`); the lane was
never mutated — mutants were scratch copies run with `--lane`/`--rev` pointing at the lane
or a disposable git fixture. M4/M5 are spec-content probes against pristine code.

## Baselines (pristine; both real specs — deterministic, not inconclusive)
```
$ git -C $L show 5275c892273242b5be989336f5d44ce8cbf671f9:.ufo/waves/round-49/w2-spec.json > scratch/spec-r49w2.json  # 35 items
$ python3 scratch/pristine/wave-complete-check.py scratch/spec-r49w2.json $L/.ufo/waves/round-49/w2 --rev 5275c892… --lane $L
→ exit 1; stdout: MISSING MutA05 | MutSubstance | ReviewQuality | ExecReplayC1 |
  ScribeScorecard | ScribeTrends | ScribeShonen | ScoutPlanned
  stderr: OK 27/35 reports present in …/round-49/w2@5275c89227324…
$ python3 scratch/pristine/wave-complete-check.py $L/.ufo/waves/round-50/w1-spec.json $L/.ufo/waves/round-50/w1
→ exit 1; stderr: OK 29/42 reports present in …/round-50/w1
  stdout (truncated): MISSING MineConsider | ExecMirrorCensus | ExecInfStaged | ExecReplayC1 |
  ExecFormProbe | CritForgeC1 | CritForgeC2 | ReviewProvince | ReviewQuarMap | …
```
Exit 1 with these exact missing sets IS the documented contract (incompleteness reported);
both cells are the pristine reference for the matrix. Real specs checked: 0 duplicate
names, 0 names containing `/` (r49w2 35 items, r50w1 42 items).

## Fixture git repo (disposable; toplevel verified before any commit)
`D=/dev/shm/chousa-r50-R50MutWaveComplete/gitfix/lane`; `git -C $D rev-parse --show-toplevel`
== D → True. Commit R1=2ec4a51261be (only `wave/.keep`); commit R2=7129f0237c32 (adds
`wave/alpha.md`, `wave/beta.md` **0 bytes**, `wave/gamma.md`, `wave/delta` (no `.md`),
`wave/sub/inner.md`, and root-level `escape.md`). Report dir = `$D/wave` in all cells.

## Mutants (one-line changes, count-verified replacements on scratch copies)
- m1 missing reported OK: `missing = [n for n in names if n not in found]` → `missing = []`
- m2 on-disk consulted first in rev mode: rev-branch `found` gains `os.path.isfile(os.path.join(report_dir, n + ".md")) or …`
- m3 stub probe (strict variant): disk-branch adds `and os.path.getsize(os.path.join(report_dir, n + ".md")) > 0`
- m4 spec probe: item name with `/` (`sub/inner`) and `..` (`../escape`) — pristine code
- m5 spec probe: items `["zeta","zeta"]` — pristine code
- m6 zero items exit 0: deletes guard `if not out: die(path + ": empty 'items' …")`
- m7 suffix dropped: both branches lose `+ ".md"`

## Kill matrix (exit pristine→mutant; `=` = byte-identical output; K killed, S survived-in-context)
| mutant | fixture disk | fixture rev | R49 @5275c892 | R50 w1 | verdict |
|---|---|---|---|---|---|
| m1 | F4 1→0; F8 1→0 | F1R1 1→0 | 1→0 (stdout emptied) | 1→0 (stdout emptied) | **KILLED** |
| m2 | = (disk path untouched) | F1R1 1→0; F6R2 1→0 | 1→1 but OK 27/35→31/35, missing 8→4 | = (disk mode) | **KILLED** |
| m3 | F2 0→1 | = | = | = | **KILLED** (probe; see named limit) |
| m4 | accepted (defect) | F5R2 accepted; F6R2 rejected | n/a (no live names) | n/a | **SURVIVED** |
| m5 | accepted silently | n/a | n/a (0 dups live) | n/a | **SURVIVED** |
| m6 | F7 2→0 | F7 2→0 | = | = | **KILLED** |
| m7 | F3 0→1; F4 1→0 | F1R2 0→1; F5R2 0→1 | 27/35→0/35 | 29/42→0/42 | **KILLED** |

## Key cells (command + observed output)
```
$ python3 …/pristine/wave-complete-check.py f1.json $D/wave --rev R1 --lane $D      # alpha.md on disk, NOT in R1 tree
  exit 1  MISSING alpha  |  OK 0/1 …
$ python3 …/m2/wave-complete-check.py   f1.json $D/wave --rev R1 --lane $D
  exit 0  (no stdout)    |  OK 1/1 …                                  # worktree consulted → wrong at pinned rev
$ python3 …/m2/wave-complete-check.py spec-r49w2.json $L/.ufo/waves/round-49/w2 --rev 5275c892… --lane $L
  exit 1  MISSING MutA05|MutSubstance|ReviewQuality|ScoutPlanned  |  OK 31/35 … # 4 late-landed worktree files counted
$ python3 …/pristine/wave-complete-check.py f2.json $D/wave        # beta.md = 0 bytes
  exit 0  OK 1/1 reports present …                                      # stub accepted by pristine
$ python3 …/m3/wave-complete-check.py f2.json $D/wave
  exit 1  MISSING beta | OK 0/1 …
$ python3 …/pristine/wave-complete-check.py f7.json $D/wave        # {"items":[]}
  exit 2  ERROR …f7.json: empty 'items' (an empty wave cannot be complete)
$ python3 …/m6/wave-complete-check.py f7.json $D/wave
  exit 0  OK 0/0 reports present …
$ python3 …/m7/wave-complete-check.py spec-r49w2.json $L/.ufo/waves/round-49/w2 --rev 5275c892… --lane $L
  exit 1  MISSING ReopenS096…(all 35) | OK 0/35 …; and f4: bare `delta` flipped to OK 1/1 (false positive)
```

## Findings
1. **m4 SURVIVED — no name validation.** Pristine, disk branch: item `sub/inner` satisfied by
   `$D/wave/sub/inner.md` (F5 exit 0, OK 1/1); item `../escape` satisfied by `$D/escape.md`
   OUTSIDE the report dir (F6 exit 0, OK 1/1) — `..` traversal escape. Rev branch: nested
   `wave/sub/inner.md` matched via `ls-tree -r` (F5R2 exit 0) but `../escape` correctly MISSING
   (F6R2 exit 1). Both real specs carry zero slash-names, so no live impact; coverage finding
   only. Contract untouched (frozen at 6a068f2a).
2. **m5 SURVIVED — duplicates silently deduped.** `names_of` keeps first occurrence
   (`if n not in out`); spec `["zeta","zeta"]` with no report → one `MISSING zeta`,
   `OK 0/1` (F8): the count line reports the deduped length, so a 2-item spec reads as 1.
   No warning, exit unchanged. Undocumented in the usage line. Real specs: 0 duplicates.
3. **m3 — named limit (stated as tasked):** pristine counts a 0-byte report as present
   (F2 exit 0); presence is file-existence, no substance floor. The strict variant is
   detectable (F2 0→1), so the limit is observable, not a blind spot; named limit of the
   check, not a proposed change.
4. Killed set confirms the load-bearing points: exit-1 reporting (m1), rev-tree authority
   over the worktree (m2 — caught by both fixture and the real R49 spec), empty-wave guard
   (m6), and the `.md` suffix in BOTH branches (m7: false negatives 0/35 and 0/42 on real
   specs, false positive on extensionless file).

## Restoration evidence
```
$ sha256sum $L/corpus/evidence/round50/wave-complete-check.py   # after
1f449f1c61a87f890516851029451071db41e6055679ee598baaa945db07c0a1   (== before)
$ git -C $L diff --stat HEAD -- corpus/evidence/round50/wave-complete-check.py   # empty (0 lines)
$ ls /dev/shm/chousa-r50-R50MutWaveComplete → No such file or directory (scratch deleted)
```
Only lane write: this report file. No network, no live fetch, no staged-package writes.

VERDICT: attacked wave-complete-check.py with 7 mutants across fixture-disk/fixture-rev/real-r49w2@5275c892/real-r50w1 — m1, m2, m6, m7 killed (m2 also by the real r49 spec: worktree consulted at a pinned rev); m3 probe killed, exposing the named 0-byte-stub limit; SURVIVED: m4 (spec names with path separators accepted on disk incl. `..` escape; rev branch accepts nested but blocks `..`) and m5 (duplicate names silently deduped, count line misstates spec length) — coverage findings, frozen contract unchanged.
