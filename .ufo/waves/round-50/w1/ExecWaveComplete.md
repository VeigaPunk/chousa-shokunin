# ExecWaveComplete — round 50 / wave 1

Item: wave-completeness gate for fleet wave reports (build + first falsifier).
Writes: this report only. Intended lane path of the draft: `corpus/evidence/round50/wave-complete-check.py`.

## What I built

Exact usage line:

```
python3 wave-complete-check.py <wave-spec.json> <report-dir> [--rev REV --lane DIR]
```

Contract: reads the wave spec's `items[].name`, prints `MISSING <name>` on stdout (spec order,
deduped) for every item whose `<name>.md` is absent from `<report-dir>` — on disk, or inside the
lane's git tree at `--rev` — and exits 1; prints nothing on stdout and exits 0 when every item has
a report. A one-line `OK n/N reports present in <dir>[@rev]` goes to **stderr**, so stdout stays a
pure machine list. Exit 2 on unusable input (`items` absent, an item without `name`, empty `items`,
unresolvable rev, non-git lane, report dir outside the lane): a broken gate must never read as a pass.
`--rev` audits history without a checkout (`git ls-tree -r --name-only <commit> -- <reldir>`).

```python
#!/usr/bin/env python3
"""usage: python3 wave-complete-check.py <wave-spec.json> <report-dir> [--rev REV --lane DIR]

Prints `MISSING <name>` for every spec item whose <name>.md is absent from the
report dir (on disk, or in the lane's git tree at REV), exits 1; exits 0 when
every item has a report; exits 2 on an unusable spec or lane.
"""
import json, os, subprocess, sys


def die(msg):
    print("ERROR " + msg, file=sys.stderr)
    sys.exit(2)


def git(args):
    r = subprocess.run(["git"] + args, capture_output=True, text=True)
    if r.returncode:
        die("git %s: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def names_of(spec, path):
    items = spec.get("items") if isinstance(spec, dict) else None
    if not isinstance(items, list):
        die(path + ": no 'items' list")
    out = []
    for i, it in enumerate(items):
        n = it if isinstance(it, str) else (it.get("name") if isinstance(it, dict) else None)
        if not isinstance(n, str) or not n.strip():
            die("%s: item %d has no 'name'" % (path, i))
        if n not in out:
            out.append(n)
    if not out:
        die(path + ": empty 'items' (an empty wave cannot be complete)")
    return out


def main(argv):
    rev = lane = None
    pos = []
    it = iter(argv[1:])
    for a in it:
        if a == "--rev":
            rev = next(it, None) or die("--rev needs a value")
        elif a == "--lane":
            lane = next(it, None) or die("--lane needs a value")
        else:
            pos.append(a)
    if len(pos) != 2:
        print(__doc__)
        return 2
    spec_path, report_dir = pos
    try:
        spec = json.load(open(spec_path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        die("%s: %s" % (spec_path, exc))
    names = names_of(spec, spec_path)
    if rev is None:
        found = [n for n in names if os.path.isfile(os.path.join(report_dir, n + ".md"))]
    else:
        lane = lane or os.getcwd()
        commit = git(["-C", lane, "rev-parse", "--verify", rev + "^{commit}"]).strip()
        root = git(["-C", lane, "rev-parse", "--show-toplevel"]).strip()
        rel = os.path.relpath(os.path.realpath(report_dir), os.path.realpath(root))
        if rel == ".." or rel.startswith(".." + os.sep):
            die("report dir %s is outside lane %s" % (report_dir, lane))
        pre = "" if rel == "." else rel + "/"
        tracked = set(git(["-C", lane, "ls-tree", "-r", "--name-only", commit, "--", rel]).split("\n"))
        found = [n for n in names if pre + n + ".md" in tracked]
    missing = [n for n in names if n not in found]
    for n in missing:
        print("MISSING " + n)
    print("OK %d/%d reports present in %s" % (len(found), len(names),
          report_dir + ("" if rev is None else "@" + rev)), file=sys.stderr)
    return 1 if missing else 0


sys.exit(main(sys.argv))
```

79 lines, no tabs, stdlib only, no network.

## Evidence

### 1. Fails at the revision round 49 cited

```
$ wc -l wave-complete-check.py
79 wave-complete-check.py
$ python3 wave-complete-check.py $L/.ufo/waves/round-49/w2-spec.json $L/.ufo/waves/round-49/w2 \
    --rev 5275c892273242b5be989336f5d44ce8cbf671f9 --lane $L
MISSING MutA05
MISSING MutSubstance
MISSING ReviewQuality
MISSING ExecReplayC1
MISSING ScribeScorecard
MISSING ScribeTrends
MISSING ScribeShonen
MISSING ScoutPlanned
OK 27/35 reports present in /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-49/w2@5275c892273242b5be989336f5d44ce8cbf671f9
exit=1
$ git -C $L ls-tree -r --name-only 5275c892273242b5be989336f5d44ce8cbf671f9 -- .ufo/waves/round-49/w2 | wc -l
28
```

28 entries = 27 `.md` + `swarm-registry.json`; 35 spec items − 27 = the 8 lines above. The revision
is the one round 49 cited: `corpus/lessons/round-49-verifier-spotcheck.md:6,21,28` (lane HEAD measured
at `5275c892…`).

### 2. Against the current tree it does NOT print none — it prints four

```
$ python3 wave-complete-check.py $L/.ufo/waves/round-49/w2-spec.json $L/.ufo/waves/round-49/w2
MISSING ExecReplayC1
MISSING ScribeScorecard
MISSING ScribeTrends
MISSING ScribeShonen
OK 31/35 reports present in /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-49/w2
exit=1
```

The item expected no names here. The tree does not support that expectation, and the four absences
are real seat-report gaps, not gate noise:

```
$ for n in ExecReplayC1 ScribeScorecard ScribeTrends ScribeShonen; do printf '%s: ' $n; \
    git -C $L log --all --oneline --diff-filter=A -- ".ufo/waves/round-49/w2/$n.md" | wc -l; done
ExecReplayC1: 0
ScribeScorecard: 0
ScribeTrends: 0
ScribeShonen: 0
```

- None of the four was ever added to `.ufo/waves/round-49/w2/` at any commit (all counts 0), so this
  is not a rev-vs-worktree artefact.
- `ExecReplayC1.md` exists only at `.ufo/waves/round-49/w1/ExecReplayC1.md`; the w1 spec's item of that
  name is a *different* item (`w1 reportDir .ufo/waves/round-49/w1`, `w2 reportDir .ufo/waves/round-49/w2`,
  `same item text? False`). A gate that searched upward for a same-named file would false-pass another
  wave's seat — which is why the gate is report-dir-exact.
- The three scribe *deliverables* did land as production text, so the work is not lost: `SCORECARD.md:2562`
  (`## Round 49 verdict`), `corpus/lessons/round-49-verifier-spotcheck.md:87` (`## Trend verdicts`) and
  `:102` (`## SHONEN`). What is missing is the per-seat report, i.e. the round-49 routed defect
  "seat reports uncommitted at filing" is still visible at the tip — and this gate surfaces it in one command.

### 3. Self-test of the gate itself (routed defect: "no self-test for a reusable gate")

```
$ python3 wave-complete-check.py $L/.ufo/waves/round-49/w2-spec.json allrep          # 35 stub reports
OK 35/35 reports present in allrep
exit=0                                                                              # no stdout
$ python3 wave-complete-check.py empty.json allrep
ERROR empty.json: empty 'items' (an empty wave cannot be complete)                  exit=2
$ python3 wave-complete-check.py noname.json allrep
ERROR noname.json: item 0 has no 'name'                                             exit=2
$ python3 wave-complete-check.py ... --rev deadbeef --lane $L
ERROR git -C … rev-parse --verify deadbeef^{commit}: fatal: Needed a single revision exit=2
$ python3 wave-complete-check.py ... allrep --rev 5275c89… --lane $L
ERROR report dir allrep is outside lane /home/vgpnk/Projects/shokunin/chousa-shokunin exit=2
$ python3 wave-complete-check.py .../nope
OK 0/35 reports present in /dev/shm/chousa-r50-ExecWaveComplete/nope                exit=1  # fail-loud
$ python3 wave-complete-check.py only-one
usage: python3 wave-complete-check.py <wave-spec.json> <report-dir> [--rev REV --lane DIR]   exit=2
```

## Calibration note

- Presence, not content: the self-test stubs are one-byte files and pass — an empty report still counts
  as filed. That limit is deliberate (content is the reviewer's axis) and is stated here rather than hidden.
- Exact-name, report-dir-only matching; no upward search, no sibling-wave fallback (see the
  `ExecReplayC1` false-pass hazard above).
- The stderr summary keeps the audit trail (27/35, 31/35, 0/35) while stdout stays exactly the `MISSING` list.

## Boundaries honoured

- Only write: this report. The script above is a draft for L1 to integrate at
  `corpus/evidence/round50/wave-complete-check.py`.
- Git use is read-only (`rev-parse`, `ls-tree`, `log`) against the lane; no index/jj/state writes, nothing
  written under `/home/vgpnk/Projects/shokuknow`, no sibling lane touched.
- Scratch `/dev/shm/chousa-r50-ExecWaveComplete/` (script, stub spec/dirs) removed; `rm -rf` reported below.
- No install, no upgrade, no network. Nothing was dispatched.

```
$ rm -rf /dev/shm/chousa-r50-ExecWaveComplete && ls /dev/shm | grep -c chousa-r50-ExecWaveComplete
0
```

VERDICT: built the wave-completeness gate and first-falsified it — it holds at rev 5275c89 (8 named gaps, exit 1) and on every self-test mode, but the "current tree prints none" expectation fails: the tip still lacks 4 round-49 w2 seat reports (ExecReplayC1, ScribeScorecard, ScribeTrends, ScribeShonen), the routed "seat reports uncommitted at filing" defect.
