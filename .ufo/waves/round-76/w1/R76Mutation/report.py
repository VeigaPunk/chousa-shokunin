#!/usr/bin/env python3
import hashlib,json,pathlib,shutil
S=pathlib.Path('/fast/scratch/hyaku/chousa-r76/R76Mutation'); L=pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin'); D=L/'.ufo/waves/round-76/w1/R76Mutation'
D.mkdir(parents=True,exist_ok=True)
rows=json.loads((S/'out/results.json').read_text()); restore=json.loads((S/'out/restoration.json').read_text())
assert len(restore)==15 and all(r['exit']==0 for r in restore)
for r in restore:
 expected='b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f' if r['kind']=='matrix' else '217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360'
 assert r['restored_sha256']==expected
shutil.copytree(S/'out',D/'receipts',dirs_exist_ok=True)
for f in ['mutate.py','restore.py','summarize.py','report.py']:
 shutil.copy2(S/f,D/f)
shutil.copytree(S/'witness',D/'witness',dirs_exist_ok=True)
byid={r['id']:r for r in rows}
parts=['# R76Mutation — frozen-instrument mutation probe\n',
'Controls revision: `da9ac7ec684fe9fe9ad5554cab6180057255b76b`. All 15 input files (two instruments, two positive counters, eleven forgers) were compared byte-for-byte with `git show` at that revision; see `R76Mutation/receipts/frozen-audit.txt`. No production edits, commits, network, installations, or subagents. Python 3.14.8; git 2.56.0.\n',
'Axes: defect sensitivity; false-positive resistance; answer-key opacity; timeout containment; exact restoration. The instruments were never amended. Mutants are intentionally defective scratch-only probes, not proposed fixes.\n',
'## Detector and baseline\n',
'Let `S=/fast/scratch/hyaku/chousa-r76/R76Mutation`, `R=$S/replica/corpus/evidence/round76`. Each matrix mutant command was:\n\n```sh\npython3 -B "$R/matrix-battery-v3.py" --matrix "$S/mut/mut-<ID>-matrix-v3.py" --work "$S/work/<ID>" --runs 1 --matrix-timeout 120\n```\n',
'The frozen pair passed this same bounded detector, exit 0, `BATTERY=PASS forgers_rejected=11/11 positive=2/2` (`receipts/baseline.txt`), and passed the two-run control (`receipts/run/BASELINE-runs2.txt`). Baseline pass is required; setup failure is not counted as a kill. Each generated edit asserted its replacement cardinality. A matrix mutant is KILLED only if the frozen battery exits 1; exact PASS/exit 0 means SURVIVED. Battery mutants are scored on the frozen matrix with `--runs 2 --matrix-timeout 120`; unchanged PASS means the positive-control detector did not kill them.\n',
'## Per-mutant results\n',
'| Mutant | Mark | Exit | Actual final output |\n|---|---|---:|---|\n']
for r in rows: parts.append(f"| {r['id']} | {r['verdict']} | {r['exit']} | `{r['summary']}` |\n")
for bid in ['B01','B02']:
 text=(S/f'out/{bid}-frozen.txt').read_text(); summary=[x for x in text.splitlines() if x.startswith('BATTERY=')]; assert summary==['BATTERY=PASS forgers_rejected=11/11 positive=2/2']
 parts.append(f'| {bid} battery | SURVIVED | 0 | `{summary[0]}` |\n')
k=sum(r['verdict']=='KILLED' for r in rows)
parts.append(f'\n**KILLED={k}/15** overall; matrix-only **KILLED={k}/13**. Two battery mutants survived the frozen-matrix positive control. No inconclusive cases. Every survivor below is a coverage finding, not permission to weaken or change the frozen contract.\n')
parts.append('\nExpected detector legs and observed kills: M01 order-twelve and harness-source (both MISS); M02 subject-map (MISS); M09 hang (matrix timeout, MISS); M10 hang (12/12 accepted, MISS); M11 and M12 both positives (MISS). These are frozen-battery failures, not standalone crashes or assumed detections. Detailed RUN marks and misses are in `receipts/results.json`. The remaining assertion/channel removals were expected to exercise the corresponding tree/size/return-code/check-set/summary legs; their exact PASS outputs show those legs did not kill the mutations.\n')
parts.append('\n## Coverage findings and causal witnesses\n')
notes={
'M03-subject-case-name':'Case names leak through commit subjects, but the frozen subject-map only recognises the r75 spelling. An independent v3-name subject oracle reached 12/12 on M03 (exit 0; `receipts/W03-v3-subject.txt`). This is a concrete label-channel blind spot, not arbitrary-forgery speculation.',
'M04-drop-salt':'Removing per-run salt is not detected. Metadata recorder: base tree repeated across two independent M04 runs; frozen base trees differed. Padding still changes mutation trees: only one tree overlapped, so this probe does NOT show that every mutation tree is stable. The frozen tree-identity subject merely compares base/rev equality; it is not a learned tree-id memo.',
'M05-drop-pad':'Removing pad is not detected. All 11 distinct size vectors overlapped across two M05 runs, versus two overlapping vectors for frozen runs. The existing size-map subject maps any size change to C2-6, so it does not exploit class-stable size deltas.',
'M06-accept-child-exit2':'Accepting candidate exit 2 is untested by the frozen subjects: this permissive return-code defect survives. This is distinct from M12 (matrix PASS exits 2), which the positive leg kills.',
'M07-ignore-expected-failed':'Removing the exact failed-check-id assertion survives. Existing forgers remain partially rejected through other conditions, so the battery does not establish that exact failed-id matching is load-bearing.',
'M08-ignore-c2-summary':'Removing the C2 summary assertion survives; the subject set does not force this assertion to be load-bearing.',
'M13-flaky-order':'The first invocation shuffles and the second uses declared order. It survives the required --runs 1 probe, but the two-run frozen battery rejects it (witness below). This is a runs=1 probe limit, not a failure of the frozen default two-run predicate.'}
for r in rows:
 if r['verdict']=='SURVIVED': parts.append(f"- **{r['id']}**: {notes[r['id']]}\n")
parts.append('- **B01-forger-single-run**: the battery scores only runs[0] for forgers. It passes the frozen matrix, yet misses M13 at two runs. The frozen battery rejects the same M13.\n- **B02-positive-exit2**: the battery accepts positive matrix exits in {0,2}. It passes the frozen matrix and accepts M12; the pristine battery kills M12.\n')
for file in ['W13-frozen','W13-B01','W12-B02','W03-v3-subject']:
 lines=(S/f'out/{file}.txt').read_text().splitlines(); summaries=[x for x in lines if x.startswith(('BATTERY=','LOADER_MATRIX='))]
 parts.append(f"\n`receipts/{file}.txt`: {'; '.join('`'+x+'`' for x in summaries)}.\n")
parts.append('''
Paired witness commands (all under S):
```sh
python3 -B "$R/matrix-battery-v3.py" --matrix "$S/mut/mut-M13-flaky-order-matrix-v3.py" --work "$S/work/W13-frozen" --runs 2 --matrix-timeout 120 # exit 1
python3 -B "$R/mut-B01-forger-single-run-battery-v3.py" --matrix "$S/mut/mut-M13-flaky-order-matrix-v3.py" --work "$S/work/W13-B01" --runs 2 --matrix-timeout 120 # exit 0
python3 -B "$R/mut-B02-positive-exit2-battery-v3.py" --matrix "$S/mut/mut-M12-pass-exits-2-matrix-v3.py" --work "$S/work/W12-B02" --runs 1 --matrix-timeout 120 # exit 0
python3 -B "$S/mut/mut-M03-subject-case-name-matrix-v3.py" --counter "$S/witness/forge-subject-map-v3.py" --work "$S/work/W03" # exit 0
```
Battery-mutant frozen-matrix commands replace the first program by `$R/mut-B01-forger-single-run-battery-v3.py` / `$R/mut-B02-positive-exit2-battery-v3.py`, use `$R/loader-matrix-v3.py` as matrix and `$S/work/B01-frozen` / `$S/work/B02-frozen` as work: both exit 0.

M02/M03 use `$S/corrected/mut-<ID>-matrix-v3.py` and `$S/work/corrected-<ID>` in the matrix command above (exit 1 / 0 respectively); W03 likewise uses the corrected matrix path and `$S/work/corrected-W03`. An initial draft accidentally also removed `--allow-empty`; those draft measurements were superseded by isolated subject-only mutations retaining the flag. The reported sources/hashes/diffs/results are the corrected versions. Both corrected paths were then restored and re-scored by the same bounded detector (exit 0). This correction does not change the counted defect set.

## Exact restoration and provenance

`receipts/mutant-sources/` retains every defective source; matching `.diff` receipts record the changes. `receipts/restoration.json` records each mutant hash, restored hash, exact detector argv, exit and summary. All thirteen matrix paths and both battery paths were restored byte-for-byte and the same bounded detector re-run on EACH restored file: 15/15 exit 0 with exact PASS. Restored matrix SHA256 `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f`; restored battery SHA256 `217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360`. Production bytes were not mutated.

Limit: randomized one-run matrix probes are evidence for their observed saltings, not universal proofs. M13's two-run witness explicitly distinguishes the requested one-run attack sweep from the actual frozen predicate. M04 alone does not remove random mutation padding. Surviving assertion removals show missing sensitivity, not acceptance of any particular untested forgery.

Self-evaluation: accuracy 4 (probabilistic probes, explicitly bounded); completeness 4 (15 mutants and exact restored reruns, not an exhaustive mutation space); clarity 4 (per-mutant table plus receipts); actionability 4 (exact commands and causal witnesses); conciseness 4 (long receipts retained separately). Overall 4.0/5. Improvements for a future claim, not this freeze: broader subject-name oracle; adaptive metadata memorisation; targeted subjects that distinguish return-code/check-set/summary assertions. The user should agree these are findings, not integration decisions.
''')
(L/'.ufo/waves/round-76/w1/R76Mutation.md').write_text(''.join(parts))
print(f'REPORT_WRITTEN KILLED={k}/15')
