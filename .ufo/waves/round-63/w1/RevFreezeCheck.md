# RevFreezeCheck — round 63, wave w1 (reviewer, freeze check, read-only)

## Findings

1. **Freeze check passes on the files as they stand.** Two runs (the second after the wave commit was visible) agree.
   The `CHECK` lines are verbatim.
2. **Context digest matches the claims file.** The wave context carries exactly one 64-hex token, the claims digest, and
   `sha256sum` of the claims file equals it.
3. **Every path the context names is present, except five that the claims declare as created by the round.** No
   undeclared missing pointer found. Details in the table below.
4. **The frozen instruments are unchanged since the freeze commit.** `git diff --stat 62876ef HEAD -- corpus/evidence/round63 tools SKILL.md corpus/knowledge/revision-binding-r31.md` is empty, and `git log -- corpus/evidence/round63/claims.md` shows only `62876ef`.
5. **Wave files are committed and clean.** `w1-spec.json`, `w1-dispatch.json`, `w1-run.err` and `freeze-check-live.txt` are in
   HEAD `c8bfcc6`. Working-tree status of `.ufo/waves/round-63` is `??` only for `w1.ready`, `w1.ready.dispatched`, `w1/`.
   `w1.ready` is not tracked, so it is not yet a committed artifact.
6. **Observation, not a freeze failure:** `.ufo/waves/round-63/w1.ready.partial` existed at 23:30 during my first pass
   and was gone by my later listing. The freeze check does not read it. The L1 should confirm which file the
   dispatcher treats as the ready signal.

## CHECK lines (run 1, verbatim)

```
$ python3 -B tools/freeze-check.py --claims corpus/evidence/round63/claims.md --dispatch .ufo/waves/round-63/w1-dispatch.json --spec .ufo/waves/round-63/w1-spec.json --ready .ufo/waves/round-63/w1.ready; echo EXIT=$?
CHECK CLAIMS_NONEMPTY PASS 15038 bytes sha256=6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5
CHECK CONTEXT_DIGEST PASS context carries 6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5
CHECK CONTEXT_SPEC_EQ PASS identical (4332 chars)
CHECK DIGEST_STRAY PASS no 64-hex token other than the claims digest
CHECK NAMES PASS 69 names match in order, roles match agents
CHECK BODY_RENDER PASS 69/69 dispatch tasks equal the rendered spec items
CHECK READY_DISPATCH PASS ready -> /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-63/w1-dispatch.json
CHECK READY_IDENT PASS lane=chousa round=63 wave=w1 agree with dispatch, spec and location
FAILED_CHECKS=none
FREEZE_CHECK=PASS
EXIT=0
```

Run 2 (repeated after the wave commit was visible) printed the same nine lines and `EXIT=0`. No `WARN` lines were printed.
`.ufo/waves/round-63/freeze-check-live.txt` (committed in `c8bfcc6`) carries the same nine `CHECK` lines and the same
`FAILED_CHECKS=none` / `FREEZE_CHECK=PASS` tail.

## Digest checks

```
$ sha256sum corpus/evidence/round63/claims.md
6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5  corpus/evidence/round63/claims.md
$ (wave context digest tokens, extracted with a read-only Python regex over w1-spec.json .context)
['6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5']
CTX_LEN 4332  CTX_EQ_DISPATCH True
```

Claims-named prefixes, against `sha256sum` of the frozen bytes (`corpus/evidence/round63/...`):

```
MATCH c1-battery.py 0073fba73c89aaf8        want 0073fba73c89aaf8
MATCH c2-count.py 606207e224c0b7cf          want 606207e224c0b7cf
MATCH controls/pos-ref-preflight.py 07683086fd6c6b41 want 07683086fd6c6b41
MATCH controls/run-c1-controls.py 8e9bd4c3e304b5f0   want 8e9bd4c3e304b5f0
MATCH controls/run-c2-controls.py 8b2b371340b01b58   want 8b2b371340b01b58
MATCH controls/candidate-git-revision-probe.py ccd702f4e9a2f7c4 want ccd702f4e9a2f7c4
MATCH controls/c2-positive-entry.md 93ad2c681783b6ce want 93ad2c681783b6ce
MATCH controls/candidate-git-rows.txt cfdf7b117c26a07f want cfdf7b117c26a07f
```

## Path existence (context and claims)

Method: read the wave context in full (it is one 4332-char line, so read in 600-char chunks), then read `claims.md`.
Each path was tested with `os.path.exists` on the absolute path, and with `ls -la` for the ones that matter.
Note on my own tooling: my first resolver joined relative names onto several base directories and mislabelled hits
with the base it tried first. Absolute names were tested as given and are reliable. The relative names I re-tested
with explicit prefixes (`corpus/evidence/round63/controls/...`), so the table is the corrected one.

| Named by | Path | Status |
|---|---|---|
| context | `corpus/evidence/round63/claims.md` | exists (sha matches) |
| context | `tools/lane-preflight.py` | **absent — declared "Created by the round"** |
| context | `corpus/evidence/round63/controls/pos-ref-preflight.py` | exists |
| context | `corpus/evidence/round63/c1-battery.py` | exists |
| context | `corpus/evidence/round63/controls/` | exists |
| context | `corpus/evidence/round63/c2-count.py` | exists |
| context | `corpus/evidence/round63/controls/c2-positive-entry.md` | exists |
| context | `corpus/evidence/round63/controls/candidate-git-rows.txt` | exists |
| context | `corpus/evidence/round63/controls/candidate-git-revision-probe.py` | exists |
| context | `corpus/evidence/round63/controls/candidate-git-revision-probe.txt` | exists |
| context | `SKILL.md`, `tools/`, `corpus/` | exist |
| context | `.ufo/waves/round-63/w1/<your-name>.md` | report path, not yet written by design |
| context | `/fast/scratch/hyaku/chousa-r63/<your-name>/` | scratch, parent exists; seat-owned, not created by me |
| context | `/home/vgpnk/.omp/agent/RULES.md` | exists |
| claims | `corpus/knowledge/git-revision-identity-r63.md` | **absent — declared "Created by the round"** |
| claims | `corpus/evidence/round63/git-revision-probe.py` | **absent — declared "Created by the round"** |
| claims | `corpus/evidence/round63/git-revision-probe.txt` | **absent — declared "Created by the round"** |
| claims | `corpus/lessons/round-63.md` | **absent — declared "Created by the round"** |
| claims | `corpus/evidence/round63/controls/{c1-before,c1-controls,c1-reference-runs,c2-before,c2-controls}.txt` | exist |
| claims | `corpus/evidence/round63/controls/{run-c1-controls,run-c2-controls}.py` | exist |
| claims | `corpus/evidence/round63/controls/null-{pass,fail,diff-oracle,selfreport}.py` | exist |
| claims | `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `corpus/SOURCES.md` | exist |
| claims | `corpus/knowledge/revision-binding-r31.md`, `corpus/lessons/round-62-verifier-spotcheck.md` | exist |
| claims | `.ufo/waves/round-63/census-start.txt` | exists |
| claims | `.ufo/waves/round-59`, `round-60`, `round-61` (named as `round-59..61`) | exist |
| claims | `tools/freeze-check.py`, `tools/assimilate-rows.py`, `tools/research-gate.sh` | exist |
| claims | `scripts/sources-census.sh` (fleet root, `/home/vgpnk/Projects/shokunin/scripts/`) | exists (fleet, not lane) |
| claims | `corpus/lessons/round-<N>.md`, `corpus/knowledge/*.md`, `.ufo/waves/round-59..61` | pattern/range notation, not single files |

Counted missing: **k = 5** (`tools/lane-preflight.py`, `corpus/knowledge/git-revision-identity-r63.md`,
`corpus/evidence/round63/git-revision-probe.py`, `corpus/evidence/round63/git-revision-probe.txt`,
`corpus/lessons/round-63.md`). All five are in the claims' own "Created by the round" list and the claims say so
explicitly, so none is a false pointer. **Undeclared missing pointers: 0.**

Per-seat output paths named only in item prompts (for example `ExecCiteCheck/probe-cite-check.py`,
`ScribeGate/gate.md`) are seat deliverables. They are outside the context/claims set I was asked to check and are not
counted. `ExecCiteCheck/probe-cite-check.py` already exists in the w1 directory at the time of my last listing.

## Git revision check (read-only)

```
$ git -C <lane> cat-file -t 62876ef90154714bfa806fbbec7890a9ff11b179      -> commit
$ git -C <lane> cat-file -t a847a37cc263c80417ee1cdf650de33e2f91a839      -> commit
$ git -C <lane> merge-base --is-ancestor 62876ef... HEAD                    -> yes
$ git -C <lane> show 62876ef:corpus/evidence/round63/claims.md | sha256sum  -> 6c46b2cc...c70f5  -
$ git -C <lane> log --oneline -3 -- corpus/evidence/round63/claims.md      -> 62876ef round-63: freeze claims, ...
$ git -C <lane> log --oneline 62876ef..HEAD                                 -> c8bfcc6 round-63: wave w1 spec, dispatch (validated v2), freeze check
```

HEAD is `c8bfcc6`, one commit past the `62876ef` freeze commit named in the context. That commit adds only wave files
(`freeze-check-live.txt`, `gen-w1-spec.py`, `w1-dispatch.json`, `w1-run.err`, `w1-spec.json`). It does not touch the
frozen instruments.

## Scope and disclosures

- No writes to the lane except this report. No git mutation; read-only git only. No scratch created; nothing to delete.
- No subagent dispatch (leaf). No network.
- The `CHECK` run is the orchestrator's own gate, executed read-only with `-B`.
- INFERENCE: the `.ufo/waves/round-63/w1.ready.partial` file that vanished between passes is a dispatcher artifact. I did not verify this.

## Verdict

VERDICT: FREEZE_CHECK=PASS missing_files_cited=5
