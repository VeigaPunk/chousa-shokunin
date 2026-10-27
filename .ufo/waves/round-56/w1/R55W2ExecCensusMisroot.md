# R55W2ExecCensusMisroot — census + hygiene at 29cfb12a (round-55 W2 item, dispatched in round 56)

scratch `/fast/scratch/hyaku/chousa-r56/R55W2ExecCensusMisroot/` (exported TMPDIR; removed at exit). No counter,
probe, battery tool or LibreOffice ran; no git mutation; no install; the lane was read via `git`/`find`/`stat` only.
The frozen rev is not the live worktree HEAD, so every claim is measured twice: extracted 29cfb12a tree (`$S/lane55`)
and the live worktree.

```
$ git -C …/chousa-shokunin archive 29cfb12abd70f688b48c0d17f31e636f2d81104a | tar -x -C $S/lane55
$ git -C …/chousa-shokunin log --oneline 29cfb12a..HEAD
99eff0e round-56: C2 integration — entry grey-literature-field-china-r42 by document (rows S127-S130, S118 used-by) …
0c2f4ce round-56: W1 spec/dispatch (69 seats …)
46e1758 round-56: C1 candidate — the build-spans gate battery …
41c5892 round-56: freeze — claims C1 … and C2 …
```

## 1. Row count (expect 126)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' $S/lane55/corpus/SOURCES.md
126
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
130
```

126 at the frozen rev: matches. Live 130 = 126 + S127-S130 (round-56 C2 rows, 99eff0e). The seat command as written
(`--root /home/vgpnk/Projects/shokunin`) parses the live worktree, not a rev: run literally today it prints 130 — a 4-row
apparent overcount. See Risks.

## 2. Registry validation

```
$ cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa; echo "EXIT=$?"
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

At the frozen rev (`bash scripts/sources-census.sh validate $S/lane55`): identical five W04 warnings + `lane55 ok`,
EXIT=0. Zero E-codes; W04 (`same URL across scopes`) is a warning and moves no lane status, so the round-55 registry is
clean at 29cfb12a on the same five rows it has been clean on since round 4x.
## 3. Tier/status histograms (CORPUS.md manual census, frozen rev)
```
rows: 126 · malformed: 0 · tier: A=105 B=16 C=5 · status: mined=102 queued=19 rejected=5
dup-ids: (none printed) · enum/tier-inflation: (none printed) · mined rows with missing used-by path: 0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census $S/lane55
lane55	rows	126
lane55	tier.A	105 · tier.B	16 · tier.C	5
lane55	status.mined	102 · status.queued	19 · status.rejected	5
FLEET	rows 126 / tier.A 105 / tier.B 16 / tier.C 5 / tier.invalid 0 / queued 19 / mined 102 / rejected 5 / invalid 0 / missing 0
EXIT=0
```

Manual (CORPUS.md) and maintained (`census`) histograms agree exactly, and every `used-by` path of every `mined` row
resolves inside the extracted tree: no dangling `used-by`, no tier/kind/status enum violation, no community-at-A.

## 4. Fleet-root misroots (untracked files whose content names chousa round 55)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | wc -l
0
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --ignored=matching -uall | wc -l
122
```

The untracked fleet-root set is empty, so the content filter's domain is empty: zero misroots, nothing listed, nothing
moved or deleted. The 122 ignored entries decompose as 22 `*-shokunin/` lane dirs (fleet `.gitignore:1`), 97 `.ufo`
entries (mostly `.ufo/state/*` driver runtime, `.ufo/watchdog.log`, `shokunin-train-*/{xconnector,xsentinel}-scratch/`),
`.tower/` and 3 `.jj`; no chousa round-55/56 stray among them. Fleet-root `.ufo/waves/` holds 61 dirs, all `shokunin*`
train waves — no fleet-root `round-55`/`round-56` dir. Caveat (by design): the fleet repo ignores every `*-shokunin/`, so
a lane-internal stray could never show here; §5 covers that side.

## 5. Lane worktree status (expect only W1/W2 reports and markers)

Snapshot during the wave: 41 lines, all `??`, zero `M`/`D`/`A` —

```
38 *.md  = .ufo/waves/round-56/w1/ reports (14 R55W2* + 24 R56*)
 3 non-md = .ufo/waves/round-56/w1.ready · …/w1.ready.dispatched · corpus/evidence/round56/c1-measure-after.txt
```

Filtering out `.ufo/waves/round-56/w1*/` and `corpus/evidence/round56/` leaves nothing. Two non-report entries are the
wave markers; the third is the L1's round-56 C1 after-measurement receipt (`head -1`: `# R56-C1 after-measurement (L1)
at lane master 99eff0e… (C1 inputs unchanged since … 46e1758 … -> empty)`). Legitimate evidence, not a misroot, but it
is untracked, neither a report nor a marker — the integrator must decide whether it lands with C1's measurement; the
count is time-dependent (69 seats dispatched, 41 entries at this read).

## 6. `__pycache__` left by the round's counters

```
$ find corpus/evidence/round56 -name '__pycache__' -o -name '*.pyc'      # nothing
$ stat -c '%y %s %n' corpus/evidence/round55/__pycache__/c1-count.cpython-314.pyc
2026-10-27 00:38:16 45218 corpus/evidence/round55/__pycache__/c1-count.cpython-314.pyc
$ stat -c '%y %n' tools/__pycache__/capture-text.cpython-314.pyc
2026-10-27 01:15:08 tools/__pycache__/capture-text.cpython-314.pyc
$ git check-ignore -v corpus/evidence/round55/__pycache__/c1-count.cpython-314.pyc
.gitignore:3:corpus/**/__pycache__/	…round55/__pycache__/c1-count.cpython-314.pyc
```
Round-56's evidence dir is clean; the round-55 counter run at 00:38 today left its ignored, untracked
`corpus/evidence/round55/__pycache__/c1-count.cpython-314.pyc` (45 KB), and `tools/__pycache__/capture-text` landed at
01:15 mid-wave. Neither touches the registry or the tracked tree, but runs are not uniformly
`PYTHONDONTWRITEBYTECODE=1`. Pre-existing debt, untouched (my write boundary is this report): 18 `__pycache__/*.pyc` are
committed from rounds 30/32/35/43/45 (`git ls-files | grep pycache`), 0 from rounds 55/56.

## Risks / notes for the integrator

- A rev-pinned census cannot be measured from the fleet root once the lane has commits: `--root` reads the live
  worktree (130 rows today). Literal run → apparent 4-row failure; extracted-rev run → 126; rev-pinned counts must extract.
- `corpus/evidence/round56/c1-measure-after.txt` is untracked (receipt, not report/marker) — landing decision needed.
- Ignored pycache debris at `corpus/evidence/round55/` and `tools/`, plus 18 older tracked pycache files (rounds 30–45);
  no network, no counter, no mutation, no install; five W04 pre-existing and identical at both revs.

VERDICT: attacked round-55's census/hygiene claim at 29cfb12a — 126 rows, `validate` exit 0 with the same 5 W04
warnings, CORPUS.md histograms matching the maintained census (A=105/B=16/C=5, mined=102/queued=19/rejected=5, 0
malformed, 0 dangling `used-by`), zero fleet-root misroots, lane untracked set = reports+markers+one receipt, round-56
evidence free of pycache — the claim SURVIVED, with the calibration caveat and the receipt/pycache debris recorded above.
