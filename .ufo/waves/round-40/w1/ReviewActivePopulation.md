# Review — active r39 receipt population (round 40, w1)

**Seat:** ReviewActivePopulation (leaf L2, no dispatch). **Lane:** chousa. **Round:** 40, attempt 1.
**Lane HEAD at audit:** `6bc90e04ac60307befacd554f7eee2b7284e2652`. **Worktree state:** clean when the
census and the 6/6 run were taken (only a sibling's `swarm-registry.json` touch). During the audit a
concurrent, non-mine round-41 edit appeared — `tools/research-gate.sh` (+85 lines, “capture-tool pins
(round-41 C1)”, mtime 04:23:46) and `corpus/SOURCES.md` (+2, 04:25:12) — plus untracked
`corpus/evidence/round41/` and `.ufo/waves/round-41/`. I did not touch them. They change the live
result of the frozen counter; §1d and F1 quantify it. **Scope:** read-only; no lane production file,
index, or jj state modified. All probes ran under `/tmp`.
**Assigned attack:** audit `corpus/evidence/round40/active-r39-receipts.tsv` against every committed
r39 receipt and the three round-40 replacement receipts; identify any omission, duplicate, or stale
receipt mislabeled active.

## Verdict

**Against the committed tree the manifest is accurate under the frozen P1, and C1's exact success string
re-derives.** Running the counter against a clean HEAD archive prints `R39_ACTIVE_RECEIPTS=6/6`, exit 0
(§1d). No omission, no path/file duplicate, and no stale receipt is active: the six rows are exactly the
set of committed receipts that verify against the committed gate/counter/verifier/expectation bytes, and
all four excluded r39 receipts fail by name. The three round-40 replacements are faithful 1:1 re-seals
of their originals, differing only in the two digest fields that had gone stale.

The findings below are record-level, predicate-coverage, and live-state operability defects. None
falsifies the recorded round-40 measurements at their measured commits. Highest severity is **F1**: the
counter reads live worktree bytes, so the same frozen command printed 6/6 before and 2/6 after an
unrelated round-41 gate edit — the active population is commit-accurate but not commit-bound.

## 1. Census — every committed receipt, classified

Command (lane root):

```
python3 - <<'EOF'
import json, pathlib, subprocess, sys
root = pathlib.Path('.').resolve()
active = set()
for line in (root/'corpus/evidence/round40/active-r39-receipts.tsv').read_text().splitlines():
    if line and not line.startswith('#') and not line.startswith('receipt\t'):
        active.add(line.split('\t')[0])
files = sorted(list((root/'corpus/evidence/round39/receipts').glob('*.json')) + list((root/'corpus/evidence/round40/receipts').glob('*.json')))
for f in files:
    rel = str(f.relative_to(root))
    d = json.loads(f.read_text())
    gate = d['gate']; counter = str(root/d['counter']); exps = str(root/d['expectations'])
    p = subprocess.run([sys.executable, str(root/'corpus/evidence/round39/verify-receipts.py'),
                        '--receipt', str(f), '--gate', gate, '--counter', counter, '--expectations', exps],
                       capture_output=True, text=True, cwd=root)
    out=(p.stdout or p.stderr).strip().splitlines()[0]
    print(f"{'ACTIVE' if rel in active else 'outside':7} {rel:70} rc={p.returncode} {out}")
EOF
```

Output (verbatim):

```
outside corpus/evidence/round39/receipts/c1-after-s39011.json                  rc=1 VERIFY-FAIL: expect-sha256-mismatch
ACTIVE  corpus/evidence/round39/receipts/c1-after-s39111.json                  rc=0 VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
outside corpus/evidence/round39/receipts/c1-base-s39001.json                   rc=1 VERIFY-FAIL: expect-sha256-mismatch
outside corpus/evidence/round39/receipts/c1-mutenv-s39003.json                 rc=1 VERIFY-FAIL: counter-sha256-mismatch
outside corpus/evidence/round39/receipts/c1-mutenv-s39013.json                 rc=1 VERIFY-FAIL: expect-sha256-mismatch
ACTIVE  corpus/evidence/round39/receipts/c2-after-s39101.json                  rc=0 VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
ACTIVE  corpus/evidence/round39/receipts/c2-after-s39121.json                  rc=0 VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
ACTIVE  corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json      rc=0 VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
ACTIVE  corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json       rc=0 VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
ACTIVE  corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json     rc=0 VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
```

Ten receipts total: 7 committed r39 files, 3 committed round-40 replacements. Six are active; four are
outside and all four refuse. Per-row role data (from each receipt body):

| Active receipt | seed | matched | `predicate_holds` | `receipt_sha256` |
|---|---|---|---|---|
| `c1-base-s39001-regenerated.json` | 39001 | 7/8 | false (base gate control) | `93255b23…` |
| `c1-after-s39011-regenerated.json` | 39011 | 8/8 | true | `eceb771a…` |
| `c1-mutenv-s39013-regenerated.json` | 39013 | 4/8 | false (mutant control) | `e362c695…` |
| `c1-after-s39111.json` | 39111 | 8/8 | true | `caa888f0…` |
| `c2-after-s39101.json` | 39101 | 8/8 | true | `51615d8d…` |
| `c2-after-s39121.json` | 39121 | 8/8 | true | `b0abd051…` |

All six bind `expect_sha256 = 01cbdc3a8208a257…`, counter `91618e91…` (c1) or `43849e9a…` (c2),
verifier `1b6e0de6…`, and gate bytes `0447ad14…` / `4253c187…` / `e1251030…`.

### 1a. Omission — none

The active population is exactly the verifiable population. Four r39 receipts are outside:

- `c1-base-s39001`, `c1-after-s39011`, `c1-mutenv-s39013` — superseded by the three round-40 re-seals;
  each refuses `expect-sha256-mismatch` (they bind the pre-edit digest `3abd2dcb…`).
- `c1-mutenv-s39003` — refuses `counter-sha256-mismatch`: it binds `1c3b2a9e…`, while the only committed
  revision of `corpus/evidence/round39/c1-count.py` hashes `91618e91…` (`git log --oneline --
  corpus/evidence/round39/c1-count.py` → one commit, `6d914e9`), so the bound counter bytes are not in
  the committed tree. `ReviewR2CommitTruth.md:106-107` independently reports `git cat-file -t
  1c3b2a9e…` failing.

No committed receipt that verifies is absent from the manifest: the six active rows are all `rc=0`, and
every non-active row is `rc=1`. The replacement set is 1:1 with the three intended originals (same seed,
gate path, gate digest, counter digest, verifier digest, scenario census; see §2).

### 1b. Duplicate — no row/file duplicate; two label-only replications

- Six unique row paths (`len(rows) == 6`, `len(set) == 6`).
- Ten unique receipt file digests, so no copy is active under two names:

```
$ sha256sum corpus/evidence/round39/receipts/*.json corpus/evidence/round40/receipts/*.json | awk '{print $1}' | sort -u | wc -l
10
```

- Semantic duplication: hashing each active receipt body with `seed` and `receipt_sha256` removed yields
  **4 distinct bodies**, not 6:

```
$ python3 - <<'EOF'
import json, pathlib, hashlib
root=pathlib.Path('.')
bodies={}
for line in (root/'corpus/evidence/round40/active-r39-receipts.tsv').read_text().splitlines():
    if not line or line.startswith('#') or line.startswith('receipt\t'): continue
    r=line.split('\t')[0]; d=json.loads((root/r).read_text())
    body=json.dumps({k:v for k,v in d.items() if k not in ('seed','receipt_sha256')},sort_keys=True)
    h=hashlib.sha256(body.encode()).hexdigest()[:16]
    bodies.setdefault(h,[]).append(pathlib.Path(r).name)
print('distinct scenario bodies:',len(bodies))
for h,names in bodies.items(): print(h,names)
EOF
distinct scenario bodies: 4
44e42fd48deac246 ['c1-base-s39001-regenerated.json']
3631dcae11939692 ['c1-after-s39011-regenerated.json', 'c1-after-s39111.json']
0621e3df05fd25b4 ['c1-mutenv-s39013-regenerated.json']
6e8cc87b52aa8d5b ['c2-after-s39101.json', 'c2-after-s39121.json']
```

The landed-gate pair differs only in `seed` and `receipt_sha256` (diff hunks at `13c13` and `186c186`),
and the c2 pair likewise. This is the two-seed replication the r39 P1 requires, not a duplicate
row; the round-40 claim counts *receipts*, not independent measurements. Any future prose that calls
6/6 six independent runs would be false — distinct evidence bodies are four.

Predicate-coverage edge (not a current defect): `c1-count.py` dedupes manifest *path strings* only, so
six byte-identical receipts under six distinct paths pass. Synthetic probe (copies in `/tmp/rpdup`,
counter imported with `MANIFEST` re-pointed; no lane writes):

```
/tmp/rpdup/d1.json: ok VERIFY: ok receipt=d1.json gate=research-gate.sh counter=c1-count.py
/tmp/rpdup/d2.json: ok VERIFY: ok receipt=d2.json gate=research-gate.sh counter=c1-count.py
/tmp/rpdup/d3.json: ok VERIFY: ok receipt=d3.json gate=research-gate.sh counter=c1-count.py
/tmp/rpdup/d4.json: ok VERIFY: ok receipt=d4.json gate=research-gate.sh counter=c1-count.py
/tmp/rpdup/d5.json: ok VERIFY: ok receipt=d5.json gate=research-gate.sh counter=c1-count.py
/tmp/rpdup/d6.json: ok VERIFY: ok receipt=d6.json gate=research-gate.sh counter=c1-count.py
R39_ACTIVE_RECEIPTS=6/6
exit= 0
```

Control checks that do work: a 6-row manifest with one path repeated → `R39_RECEIPT_MANIFEST=
unexpected-population`, exit 2; five rows → same. The `./`-alias variant of this hole is owned and
reproduced by `CriticC1Predicate.md` (path-alias masking a missing receipt).

### 1c. Stale receipt mislabeled active — none

All six active rows verify against current bytes (census above). Same-identity rerouting is refused,
not silently re-bound:

```
$ for t in "c1-base-s39001-regenerated.json|tools/research-gate.sh|corpus/evidence/round39/c1-count.py" "c1-mutenv-s39013-regenerated.json|.ufo/waves/round-39/controls/base-gate-r39.sh|corpus/evidence/round39/c1-count.py" "c1-after-s39011-regenerated.json|tools/research-gate.sh|corpus/evidence/round39/c2-count.py"; do IFS='|' read -r r g c <<<"$t"; printf '%s: ' "$r"; python3 corpus/evidence/round39/verify-receipts.py --receipt corpus/evidence/round40/receipts/$r --gate "$g" --counter "$c"; echo "rc=$?"; done
c1-base-s39001-regenerated.json: VERIFY-FAIL: gate-sha256-mismatch
rc=1
c1-mutenv-s39013-regenerated.json: VERIFY-FAIL: gate-sha256-mismatch
rc=1
c1-after-s39011-regenerated.json: VERIFY-FAIL: counter-sha256-mismatch
rc=1
```

One canonical runtime: the counter invokes the committed verifier with `sys.executable` and resolves
every row's gate/counter under `ROOT`; there is no alternate verifier or counter path in the population.

### 1d. Live-state sensitivity — 6/6 on the committed tree, 2/6 on the drifted worktree

While this audit ran, a concurrent round-41 edit changed `tools/research-gate.sh` in the worktree
(`git diff --stat tools/research-gate.sh corpus/SOURCES.md` → `2 files changed, 87 insertions(+)`;
gate diff header “capture-tool pins (round-41 C1)”). The same frozen counter, run against committed HEAD
bytes in a read-only archive, still passes:

```
$ rm -rf /tmp/rphead && mkdir -p /tmp/rphead && git archive HEAD corpus/evidence/round39 corpus/evidence/round40 tools/research-gate.sh .ufo/waves/round-39/controls | tar -x -C /tmp/rphead
$ cd /tmp/rphead && sha256sum tools/research-gate.sh && python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"
4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3  tools/research-gate.sh
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: ok VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=6/6
EXIT=0
```

The same command in the drifted worktree:

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
EXIT=1
```

Only the two rows bound to frozen control copies (`.ufo/waves/round-39/controls/base-gate-r39.sh`,
`mut-gate-path-env.sh`) survive; the four rows bound to the live `tools/research-gate.sh` fail. The
counter and verifier stream the path they are given (`sha256_file(args.gate)`), so they cannot tell a
committed byte string from an in-flight worktree edit.

## 2. The three replacements are re-seals, and the re-seal is sound

`diff` of each original against its round-40 replacement is exactly two hunks — `expect_sha256` (line 4)
and `receipt_sha256` (line 13) — for all three pairs:

```
$ for f in c1-base-s39001 c1-after-s39011 c1-mutenv-s39013; do
    diff corpus/evidence/round39/receipts/$f.json corpus/evidence/round40/receipts/$f-regenerated.json | grep -c '^[<>]'; done
4
4
4
```

Four diff lines per pair = exactly one removed and one added line in each of two hunks (`4c4`
`expect_sha256`, `13c13` `receipt_sha256`). So `seed`, `gate`, `gate_sha256{,_pre,_post}`, `counter`, `counter_sha256`, `verifier_sha256`,
`scenarios`, `observed`, `matched`, `predicate_holds` are byte-identical to the r39 originals. This is a
re-seal, not a new measurement — the observations carry forward.

That carry-forward is justified, and this is the root cause of R1. The pre-edit expectations bytes
reconstruct exactly:

```
$ python3 - <<'EOF'
import hashlib, json, subprocess
cur = open('corpus/evidence/round39/expectations.jsonl').read().splitlines()
r38 = [l for l in subprocess.run(['git','show','1f0add7:corpus/evidence/round38/expectations.jsonl'],
       capture_output=True, text=True).stdout.splitlines() if l.strip()]
c1 = [l for l in cur if json.loads(l)['counter'] == 'c1']
c2r38 = [l for l in r38 if json.loads(l)['counter'] == 'c2']
candidate = c1 + c2r38 + [cur[-1]]
print(hashlib.sha256(('\n'.join(candidate) + '\n').encode()).hexdigest())
print(hashlib.sha256(('\n'.join(c1) + '\n').encode()).hexdigest())
EOF
3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480
703adb31ddf7b8f4a702a2431775569d6ace712b6dae48cb006135164124b7be
```

The first line is the reconstructed pre-edit file digest — exactly the stale value all four old c1
receipts bind (`3abd2dcb…`); the committed file hashes `01cbdc3a…`. The second line is the c1-family
digest, invariant across the edit. The intermediate file is not in git; the SHA-256 match is the
evidence that the c1 rows were byte-identical when the three receipts were generated.

The c1 rows in the intermediate are byte-identical to the committed ones; only c2 rows (which no c1
receipt reads) changed between the stale receipts' file mtimes (02:49–02:56) and the passing receipts'
mtimes (03:03–03:07). Therefore the three c1 receipts' per-scenario `expect` ties and observations were
never inconsistent with the frozen c1 expectations; every row's `ok` re-derives under the current file.
The stale field was whole-file identity alone.

Consequence and recommendation (not applied; read-only seat): `expect_sha256` is `sha256_file()` over
the entire `expectations.jsonl` (`verify-receipts.py` expectation-binding block), so an edit to *any*
family invalidates every family's receipts. The verifier already pins the receipt's scenario census to
the frozen family ids and each row's `expect` to the frozen row, so the file-wide digest adds cross-family
churn rather than binding strength. A family-scoped digest — here `703adb31ddf7b8f4…` over the 8 c1 rows,
invariant across the edit — would have left the three receipts valid. This is a design improvement for
the next round, not a defect in the current claim.

## 3. Findings (severity order)

### F1 — medium — active-population verification is worktree-bound, not commit-bound

The frozen counter printed `R39_ACTIVE_RECEIPTS=6/6` on the clean tree and `2/6` after a concurrent
round-41 edit to `tools/research-gate.sh` (§1d), with no receipt or manifest change. Four of the six
active rows bind the live worktree path `tools/research-gate.sh`; only the base and mutant controls bind
frozen copies under `.ufo/waves/round-39/controls/`. Mechanism: `c1-count.py` passes `ROOT / gate` and
`verify-receipts.py` hashes the live file; neither resolves the audited commit, and neither records one.
Consequences: (i) the claim’s phrase “committed gate … bytes” holds only while the worktree equals the
audited commit; (ii) any future change to the landed gate silently invalidates 4/6 active rows and turns
C1 red without touching evidence; (iii) a reviewer re-running after a later round edits the gate will
see 2/6 and could wrongly conclude the round-40 claim was false. This does **not** falsify C1: at
`d164f88` and `6bc90e0` with a matching tree, 6/6 held and the committed after-measurement is faithful.
Fix (future): freeze the landed-gate bytes used by the four rows under
`.ufo/waves/round-39/controls/` (as base/mutant already do) and point the manifest there, or have the
verifier read `git show <pinned-commit>:<path>` and print the audited commit in its `VERIFY: ok` line.

### F2 — medium — the round-40 lesson and non-author spot-check misstate the r39 directory census

`corpus/lessons/round-40.md:11`:

> “The seven-file r39 receipt directory has one superseded draft and six active receipts after the
> correction.”

`corpus/lessons/round-40-verifier-spotcheck.md:32`:

> “r39 receipt dir → 7 files (6 active + 1 superseded)”

The manifest says otherwise:

```
$ awk -F'\t' '!/^#/ && $1!="receipt" && NF==3 {if ($1 ~ /round39/) a++; else if ($1 ~ /round40/) b++} END {printf "r39_rows=%d r40_rows=%d total=%d\n", a, b, a+b}' corpus/evidence/round40/active-r39-receipts.tsv
r39_rows=3 r40_rows=3 total=6
```

The r39 directory holds **3 active + 3 superseded-by-reissue + 1
superseded draft**; the six active receipts span both directories. The round-40 claims kill rule
(`claims.md:19`) itself says the four superseded originals stay outside the active population, so the
lesson contradicts the claim it reports on. The spot-check presents this as a verified census (“All
reported histograms match”), so the error propagates into the independent review. Impact is record
accuracy (a promotion reader would believe three superseded originals are active), not C1.
Fix: append a correction to the lesson and spot-check note stating “six active receipts across two
directories (3 in `round39/receipts`, 3 in `round40/receipts`)”.

### F3 — medium-low — “dispositioned under C2” is true for one of four superseded originals

`corpus/evidence/round40/claims.md:19`:

> “The four superseded originals remain outside the active population and are dispositioned under C2.”

`corpus/evidence/round40/routed-defect-dispositions.json` has keys `R2,R3,R4,R5`; the only receipt path
it cites is `corpus/evidence/round39/receipts/c1-mutenv-s39003.json` (R2). `c2-count.py:60` likewise
requires only that one file; it never references `c1-base-s39001`, `c1-after-s39011`, or
`c1-mutenv-s39013`. The three reissued originals are dispositioned only in the r39 claims Erratum R1
(`corpus/evidence/round39/claims.md:196`) and the round-40 lesson table (`:27`) — not in the C2 record
the sentence names. Because P2 checks only R2–R5, it prints 4/4 while this sentence is false. The
substance is covered (the erratum names the three re-seals); the claim's attribution is not.
Fix: append an erratum changing “dispositioned under C2” to “dispositioned under the R1 erratum
(`corpus/evidence/round39/claims.md:196`) and R2”, or add an R1 block to the disposition record naming
the three re-sealed originals as superseded. No counter change is needed for the four-row predicate.

### F4 — low-medium — the before-control cites a commit where the counter does not exist

`controls/control-before.txt` and `claims.md:15` cite lane tip
`691d26476ac39b8ec8b65155b41199e6f6d1f299`. That commit contains no `corpus/evidence/round40/` at all:

```
$ git ls-tree -r --name-only 691d264 -- corpus/evidence/round40
<no output>
$ git archive 691d264 corpus/evidence/round40 | tar -t
fatal: pathspec 'corpus/evidence/round40' did not match any files
tar: This does not look like a tar archive
tar: Exiting with failure status due to previous errors
```

The first commit that contains the counter and manifest is the freeze commit `6c01a41`. Reproduction
from a read-only archive of that tree (no worktree, no lane writes):

```
$ rm -rf /tmp/rpfreeze && mkdir -p /tmp/rpfreeze && git archive 6c01a41 corpus/evidence/round39 corpus/evidence/round40 tools/research-gate.sh .ufo/waves/round-39/controls | tar -x -C /tmp/rpfreeze
$ cd /tmp/rpfreeze && python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: fail VERIFY-FAIL: unreadable-receipt [Errno 2] No such file or directory: '/tmp/rpfreeze/corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json'
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: unreadable-receipt [Errno 2] No such file or directory: '/tmp/rpfreeze/corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json'
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: fail VERIFY-FAIL: unreadable-receipt [Errno 2] No such file or directory: '/tmp/rpfreeze/corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json'
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=3/6
EXIT=1
```

So the recorded 3/6 is faithful at the freeze tree, but the “Before” attribution is one commit early;
a re-runner checking out the cited tip gets `can't open file '…/round40/c1-count.py'`, not 3/6. The same
error is in the C2 control citation (`claims.md:29`). This converges independently with
`CriticC1Control.md` F1. The manifest and counter bytes are identical at `6c01a41` and HEAD
(`e4623159…`, `d9b38b57…`), so the control's population is the same one measured after.
Fix: errata the cited before-tree to `6c01a41` (freeze), or state “measured in the freeze worktree.”

### F5 — low — c2 active receipts bind an absolute subject path; verification is checkout-path pinned

`c2-after-s39101.json` / `c2-after-s39121.json` carry
`"subject_counter": "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c1-count.py"`,
and the verifier resolves that string verbatim (`subject-counter-unreadable` branch). Simulated
relocation (copy of the receipt with the prefix rewritten to `/nonexistent/clone/…`, self-digest
re-sealed):

```
VERIFY-FAIL: subject-counter-unreadable /nonexistent/clone/corpus/evidence/round39/c1-count.py
rc= 1
```

Consequences: (i) the two c2 rows cannot verify from a checkout at another root; (ii) in a second
checkout on this host, they would verify against the *original* tree's counter bytes, not the tree under
test — a wrong-tree hazard that the digest cannot detect because the path is outside the counter's
`ROOT`. The manifest's own receipt/gate/counter columns are root-relative and portable; only this
receipt-internal field is not. Not a C1 defect (C1's six rows all use manifest-resolved paths), but an
operability limit worth a schema fix (store the subject path relative to the repo root or bind only
basename + digest).

### F6 — low — “reruns” in the manifest comment overstates what the replacements are

`active-r39-receipts.tsv:2` says “The three round-40 **reruns** are required active replacements.” The
files are re-seals: byte-identical bodies except the two digest fields (§2). The frozen claim only says
the receipts are “issued”/repaired, and no predicate depends on a fresh run, so this is wording. It
converges with `CriticC1Scope.md` F2. Fix belongs with the F3 erratum: “re-seals (carrying forward the
r39 observations, re-binding the expectation digest)”.

## 4. Residual risk and verification gaps

- **Authorship/truth is not established** (verifier's own stated limit). My audit proves byte identity
  and internal consistency; it cannot distinguish an honest re-seal from a copy-paste with a new
  `expect_sha256`. The 02:56/03:03 timestamps and the exact digest reconstruction make the re-seal
  reading the only supported one, but it is inference from artifacts, not authentication.
- **Observations were not re-executed.** I did not run the r39 `c1-count.py` scenarios (they write
  receipts and execute the gate), so the 7/8, 8/8, 4/8 observations are checked only for `ok`/count
  re-derivation against frozen expects. A live re-run is the one check that would turn carried-forward
  observations into re-measured ones.
- **Verification state:** the census and the 6/6 run were taken with the worktree matching HEAD; the
  HEAD-archive replay (§1d) re-proves 6/6 from committed bytes. The 2/6 result comes from a concurrent,
  non-mine round-41 edit to `tools/research-gate.sh`, not from the round-40 delivery; I neither modified
  nor reverted it. Any later reader should re-run against a clean checkout of the audited commit.
- **F5’s relocation is simulated** by rewriting the subject path, not by a second checkout at a new root.
- **`lsp` unavailable:** `read xd://lsp` → “No such tool: xd://lsp. Mounted devices: ast_edit, debug.”
  No language server answers these JSON/TSV/Python artifacts in this seat; caller/definition checks were
  therefore done by running the committed verifier and reading the counter, not by `references`/
  `diagnostics`.
- **Out of scope:** r37/r38 receipts beyond the census, C2's R2–R5 dispositions (owned by the C2
  reviewer), and the s39003 superseded-draft truth (owned by `ReviewR2CommitTruth`).

## 5. Tooling

No installs, no pacman transactions (host-wide pause respected), no network fetches. Probes used
`python3`, `git archive`/`ls-tree`, `diff`, and `/tmp` copies only; production lane files untouched.

## Artifact pointers (absolute)

- Manifest: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/active-r39-receipts.tsv`
- Counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/c1-count.py`
- Verifier: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/verify-receipts.py`
- Receipts: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/receipts/` and
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/receipts/`
- Controls: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/controls/control-before.txt`,
  `…/r1-stale-before.txt`
- Dispositions: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/routed-defect-dispositions.json`
- Claim/citations: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/claims.md:9,15,19,29`;
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/claims.md:196`;
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40.md:11,27`;
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40-verifier-spotcheck.md:32`
- Probe evidence: `/tmp/rpfreeze` (freeze-tree 3/6 replay), `/tmp/rpdup` (duplicate probe),
  `/tmp/c2-relocated.json` (relocation probe)
