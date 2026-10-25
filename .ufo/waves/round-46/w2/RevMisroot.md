# RevMisroot — misroot sweep: untracked fleet-root files naming chousa / round-46

Seat `L1Chousa46.RevMisroot`, round 46 wave 2 (falsify). Lane tip under test
`d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` (verified, `2026-10-25 07:22:07 -0300`).
Fleet repo read at `d1642b36`, 2026-10-25T07:38:28-03:00. Read-only; nothing deleted,
moved, installed or upgraded.

## 0. Verdict

**Zero misrooted chousa / round-46 artifacts among the untracked files.** Exactly one
untracked file names chousa — `.scratch/goal-20261025-hyaku-12h.md:63` — and it is a
fleet-level hyaku rotation line, not chousa round-46 material. The sweep is exhaustive
over the untracked set; two readings of the assigned scope both yield the same artifact
answer (§3), and the stratum `git status --porcelain` cannot see is measured separately
(§4) rather than assumed clean.

## 1. The command, verbatim

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | awk '{print $1}' | sort | uniq -c
      7 ??
     17 M
```

24 lines total; 17 tracked-modified (14 `.ufo/state/*.report-baseline`, `.ufo/watchdog.log`,
`scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md`), 7 untracked. `-uall` expands
the two untracked directories to the same 7 leaf files:

| untracked file | names chousa | names round-46 | attribution |
|---|---|---|---|
| `.omp/mcp.json` | no | no | harness MCP config (285 B, `rea` server disabled) |
| `.scratch/goal-20261025-hyaku-12h.md` | **yes, :63** | no | fleet hyaku goal/rotation log, by design at fleet root |
| `.ufo/state/kotoba.report-baseline` | no | no | `69 e3b0c442…` (count + empty-payload sha) |
| `.ufo/state/kotodama.report-baseline` | no | no | `70 e3b0c442…` |
| `.ufo/state/revenger.report-baseline` | no | no | `69 e3b0c442…` |
| `.ufo/waves/round-24/w2/RevUnlandedResolution.md` | no | no | tabi r24 w2 (`L1Tabi24…`, lane root `tabi-shokunin`) |
| `.ufo/waves/round-69/w1/ScoutAmp.md` | no | no | kotoba r69 w1 (base `a238989a…` exists only in `kotoba-shokunin/`) |

Content regex used on each file: `grep -n -i -E 'chousa|round[-_ ]?46|\br46\b'`. The two
untracked wave reports return empty on all three token families; the three baseline files
are `<n> <sha256(empty)>` one-liners and return empty as well.

## 2. The single hit, resolvable

`.scratch/goal-20261025-hyaku-12h.md` line 63 (verbatim, 95 bytes):

```
mado, kama on their 3rd. Next block: chousa (0 this run), kumitate, kotoba, revenger, kotodama,
```

Pointers: token `chousa` at **byte 3520** (line 63 begins at byte 3464; `grep -bo` agrees);
file sha256 `23aaf2e23d1794b6a53962d1f2ce035349a6b8d955c34d603afc170afc01a9f5`; the line sits in
the lane-rotation paragraph, and the file carries no chousa round-46 state, claim, counter or
report text. `[INFERENCE]` — that it is not a chousa artifact rests on its content (rotation
schedule), not on a rule the file states about itself.

## 3. Scope reading — stated, not silently resolved

The assignment says "untracked file at the fleet root **or** under its `.ufo/waves/`", which
admits two readings, and they differ in the hit count:

* **Narrow** (depth-1 of the fleet repo + `.ufo/waves/**`): depth-1 untracked files = **0**
  (`awk -F/ 'NF==1'` over the 7); `.ufo/waves/**` = 2 files, both grep-empty → **0 hits**.
* **Broad** (every untracked file, which is what the sweep must mean to be a misroot check):
  7 files → **1 hit**, §2.

Wave 1 (`w1/ConnectSiblings.md:56-70`) used the broad reading and reached the same
conclusion, including the same `.scratch` line. My independent re-run of the current bytes
agrees with it; the narrow reading would have reported zero hits and hidden the one mention.

## 4. Stratum the command cannot see (measured, because it is the real blind spot)

`git status --porcelain` excludes ignored paths, and the fleet `.gitignore:1` rule
`*-shokunin/` makes every lane repo (including `chousa-shokunin/`) one ignored entry — so
lane-side untracked files can never appear in the fleet porcelain by construction, and the
sweep is only sound as an *outside-the-lane* check. Ignored inventory from
`git ls-files --others --ignored --exclude-standard`:

* **152 files** under `.tower/` (comms/quarantine): **33 lines name chousa across 13 files,
  0 name round-46.** Representative hits — `missions/M12-r100-assimilation-census.md:28`
  ("…tabi 39, revenger 27, chousa 25…"), `inbox/20261024-r100-assimilation-census-tower-survey-summary.md:28,37,40`
  ("…chousa 25…", "quarantine-first tabi, revenger, chousa, kotodama", "except chousa may judge
  them as source through its own gate"), `inbox/20261024-r100-recovery-census-tower-survey-summary.md:27`
  (chousa next=42 row). These are fleet dispatch/census records that *mention* the lane; none
  is a chousa-owned artifact, and all pre-date round 46 (2026-10-24 campaign).
* **36 files** under `.ufo/waves/` (ignored sentinel scratch): **0 chousa lines**; **19
  round-46 lines in 2 files**, both audio-shokunin path inventories —
  `shokunin-train-20261013-w5/xsentinel-scratch/new-w5-files.txt:155-156` and
  `shokunin-train-20261101-w10/xsentinel-scratch/audio-5415115-swept-files.txt:492-508`
  (`corpus/live/…/round-46/*.wav`). Different lane's round 46; not chousa's.
* **25,270 entries under `.jj/repo`** excluded as VCS internals (not artifacts).
* **0** ignored files at depth 1; 0 under `.scratch/` and `.omp/`.

So: no chousa round-46 material exists anywhere the untracked sweep could or could not see,
outside the lane itself and the tracked fleet-level prompt.

## 5. Tracked fleet-root paths that legitimately name both (context, not hits)

`.ufo/prompts/chousa-round-46.md` (sha256 `423f5404f319648f01696b21b95b6791631062f982c19e1ddd31e7bea1314470`,
tracked) is the fleet dispatch prompt; its line 101 designates the fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-46/chousa.md`. That file does **not** exist;
the directory holds four tracked sibling reports (`kake.md`, `kotoba.md`, `kotodama.md`,
`kumitate.md`). Absent + untracked-absent = pending write at round close, not a misroot, and
if it were written while untracked this sweep would catch it.

## 6. Delta against wave 1, named so it is not mistaken for a new finding

`w1/ConnectSiblings.md:17,62` listed `.ufo/reports/round-69/revenger.md` in its untracked row.
At current bytes it is **tracked** (`git log --diff-filter=A` → `80d22f76 2026-10-25
07:20:45`; amended `d13b28ec 07:25:25`), so a literal re-run returns 7 untracked files of
which 6 overlap wave 1's list. That is a time delta against a fleet commit, not a method
error; wave 1's zero-misroot conclusion survives re-derivation.

## 7. Remaining unknowns

* Whether ignored `.tower/` dispatch records count as "at the fleet root" in the operator's
  sense. I measured them (§4) and report them as a stratum rather than as hits, because the
  assigned command cannot return them; if the intent is "any chousa material at fleet root",
  the answer is still no artifact — 33 mentions in fleet-owned records only.
* Whether a chousa round-46 artifact was written outside the lane and then deleted: not
  recoverable from the worktree; the tracked-path scan
  (`git ls-files | grep -iE 'chousa|round[-_]?46'`) shows only `.ufo/prompts/chousa-round-*.md`
  (and closures), i.e. no report/counter under a chousa name outside the lane.

Confidence: high on all counts (§1, §4, §5, §6 are verbatim command output); the only
`[INFERENCE]` is the ownership attribution of the §2 line.
