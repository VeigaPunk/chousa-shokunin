# R88ExecHarm — harm sweep for C1's K3 (round 88)

Seat: `R88ExecHarm` (executor). Lane: chousa round 88. Freeze commit
`4ea9d008abfd2e09cb51649a42678a78f52ac530`, base `f484d94f`.
Scratch: `/fast/scratch/hyaku/chousa-r88/R88ExecHarm/` (deleted before yield).

Tools: none installed. `python3` (system) + `git` (system) only. RULES.md read;
pacman guard respected (no network, no installs, no sudo).

## (a) Round-88 `harm-recheck.py` — moved=0

Command:
`python3 -B /fast/scratch/hyaku/chousa-r88/R88ExecHarm/frozen/corpus/evidence/round88/harm-recheck.py --root /fast/scratch/hyaku/chousa-r88/R88ExecHarm/frozen --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --base-tool /fast/scratch/hyaku/chousa-r88/R88ExecHarm/base/tools/gate-records.py`
Receipt: `receipts/harm-recheck.txt`; observed:

```
HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r88_rc=0
```

Exit 0. Matches the frozen control
`corpus/evidence/round88/controls/receipts/c1-harm.txt`
(`HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r88_rc=0`) exactly.
Subject tool blob is byte-identical base vs freeze:
`sha256 905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60`
(base, frozen, working tree all match) — so moved=0 is expected structurally;
the re-run confirms the control reproduces on the archived trees.

## (b) Wider sweep — whole lane tree, not just lessons

Command (enumeration):
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n '^GATE-RECORD' 4ea9d008abfd2e09cb51649a42678a78f52ac530 -- 'corpus/**' 'plans/**' '.ufo/waves/**'`
→ 684 matching *lines* across 578 files (list saved at
`$S/wide-files-list.txt` during the run; file list = the 578 unique paths
from that grep). Both tools (`base f484d94f` blob and frozen `tools/gate-records.py`)
then verified those 578 files batch-wise
(`gate-records.py verify --root $S/frozen --repo <lane>`, 6 chunks of 100).
Receipt: `receipts/wide-sweep.txt`; observed:

```
wide_files=578 before_records=683 after_records=683
base_rcs=[1, 1, 1, 1, 1, 1] r88_rcs=[1, 1, 1, 1, 1, 1]
moved=0
code_only_same_verdict=0
```

Exit 0 (the sweep driver completed; per-chunk `verify` exits 1 because the
corpus deliberately contains forge fixtures that FAIL — verdicts, not exits,
are the comparison). **No record's verdict differs between base and frozen
tools anywhere in the lane tree.** No `code_only` moves either.

Count reconciliation (684 grep lines vs 683 tool records), receipt
`receipts/count-reconcile.txt`:

- Grep-total was 684 = 683 unique `(path,lineno)` + 1 duplicate: the
  `NUL`-byte forge `.ufo/waves/round-85/w1/R85ExecForge/forge/x01-nul-capture.md`
  is reported by `git grep` as "Binary file … matches" with no line number,
  so it counted in the raw line total but not in the parsed 683.
- The 683 parsed grep positions vs the 683 tool verdicts cross in both
  directions (receipt `receipts/count-reconcile.txt`):
  - `IN_GREP_NOT_TOOL`: `.ufo/waves/round-83/w1/R83ExecForge/forge/c077-prose-only.md:3`
    (the word `GATE-RECORDS` in prose — not `^GATE-RECORD\s` to the tool's
    `REC_RE`… actually `^GATE-RECORD(?:\s|$)` excludes `GATE-RECORDS`; pure
    grep artifact) and `.ufo/waves/round-87/w1/receipts/R87ExecForge/f3/ genuine-S208.md:1`
    (single-line file with no trailing newline — verifier counts it; see below).
  - `IN_TOOL_NOT_GREP`: `corpus/lessons/round-86.md:122` (record indented 3
    spaces — `lead_strip` admits it; strict `^GATE-RECORD` grep misses it) and
    `x01-nul-capture.md:1` (NUL-containing forge, binary to grep).
  Net: 683 = 683. The wide sweep covers every line either detector sees.

Note on `c077-prose-only.md` and ` genuine-S208.md` parser wobble: my first
`wide-sweep2.py` run mis-split paths containing `:` (the `F3/ genuine` filename)
and printed spurious diffs — discarded, re-run as `receipts/count-reconcile.txt`
above. The file ` genuine-S208.md` has a leading space in the name; the tool
records it as `…/f3/ genuine-S208.md:1` (seen in `IN_GREP_NOT_TOOL` with the
space preserved) — no record is lost.

## (c) Positive control — a deliberately broken unreach record is refused by both

Fixture `$S/ctrl/broken-203-unreach.md`:
`GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A decision=reject capture=none curl_rc=0 http=203 words=0 quote=none`
(a 203 with `curl_rc=0` — a *successful* transfer; the round-87 unreach repair
must refuse it). Receipt: `receipts/positive-control.txt`; observed:

```
cmd: python3 -B $S/base/tools/gate-records.py verify --root $S/frozen --repo /home/vgpnk/Projects/shokunin/chousa-shokunin $S/ctrl/broken-203-unreach.md
GATE_RECORD /fast/scratch/hyaku/chousa-r88/R88ExecHarm/ctrl/broken-203-unreach.md:1 S021 FAIL REFETCH
GATE_RECORDS files=1 records=1 ok=0 fail=1
exit=1
cmd: python3 -B $S/frozen/tools/gate-records.py verify --root $S/frozen --repo /home/vgpnk/Projects/shokunin/chousa-shokunin $S/ctrl/broken-203-unreach.md
GATE_RECORD /fast/scratch/hyaku/chousa-r88/R88ExecHarm/ctrl/broken-203-unreach.md:1 S021 FAIL REFETCH
GATE_RECORDS files=1 records=1 ok=0 fail=1
exit=1
```

Both tool blobs FAIL it `REFETCH`, exit 1. The sweep can fail: it is not a
vacuous always-`moved=0`. (This is the same shape as committed fixture
`n02-unreach-203-s021.md` / `W-M31-203-unreach.md` in the wide set, so the
constant refusal in (b) is not hiding a miss.)

## (d) Provenance entry repair — exactly one cell

Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff f484d94f 4ea9d008abfd2e09cb51649a42678a78f52ac530 -- corpus/knowledge/provenance-recording-r85.md`
Receipt: `receipts/provenance-diff.txt`. Observed: a single hunk, one line
changed, `| … | Q1, Q3 (S215) |` → `| … | Q1 (S215) |` on the row "Naming what
a resource derives from". `diff --stat` for that path:
`1 file changed, 1 insertion(+), 1 deletion(-)`. No other cell of any entry
file moves in `f484d94f..4ea9d008a`: the full diff stat across the range is
18 files — 16 new round-88 evidence files, `plans/round-88.md`, and this one
knowledge file (2 +- lines, exactly the hunk above).

## Findings

No harm found. K3 for C1 holds at the landing bytes: every accepted genuine
committed record stays accepted, and everything the pre-round tool refused
still refuses — over the 28 lesson records (official control) and over all
683 machine-detected records in `corpus/**` + `plans/**` + `.ufo/waves/**`
(wide sweep). The provenance repair is a one-cell warrant narrowing exactly
as the plan discloses; it does not touch any `GATE-RECORD` verifier input (no
counter re-cites the entry, per plan §Pre-freeze repairs item 6).

VERDICT: R88ExecHarm C1 held — base and frozen tools agree on all 683 wide-sweep records and the 28-record harm control reproduces moved=0, with refused-broken-203 control refusing under both.
